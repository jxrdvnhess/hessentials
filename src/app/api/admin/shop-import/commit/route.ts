/**
 * Shop import — commit endpoint.
 *
 * POST /api/admin/shop-import/commit
 *   body: {
 *     slug, name, brand, category, priceRange, url,
 *     images: string[],            // remote source URLs to download
 *     extractionMethod, priceFloor?, htmlPriceSelector?
 *   }
 *
 * Side effects:
 *   1. Downloads each image to /public/shop/<slug>-N.jpg (sequential).
 *   2. Appends a new entry to SHOP_PRODUCTS in src/data/shop.ts with
 *      `reason: ""` left blank for editorial fill-in.
 *
 * Refuses to write if the slug already exists.
 *
 * Dev-only. Returns 403 in production. The shop data file is in the
 * repo; mutating it on a deployed server makes no sense and would be
 * lost on the next deploy.
 */

import { NextRequest, NextResponse } from "next/server";
import {
  SHOP_CATEGORIES,
  subcategoriesFor,
  type Category,
  type ExtractionMethod,
} from "../../../../../data/shop";
import { saveImagesForSlug } from "../../../../../lib/shopImport/saveImages";
import {
  appendShopEntry,
  readExistingSlugs,
  type NewShopEntry,
} from "../../../../../lib/shopImport/writeEntry";

export const dynamic = "force-dynamic";

const VALID_METHODS: ReadonlySet<ExtractionMethod> = new Set([
  "json-ld",
  "shopify",
  "html",
  "manual",
]);

type CommitBody = {
  slug?: string;
  name?: string;
  brand?: string;
  category?: string;
  subcategory?: string;
  audience?: string[];
  reason?: string;
  priceRange?: string;
  url?: string;
  images?: string[];
  extractionMethod?: string;
  priceFloor?: number;
  htmlPriceSelector?: string;
};

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

function badRequest(message: string): NextResponse {
  return NextResponse.json({ error: message }, { status: 400 });
}

export async function POST(req: NextRequest): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json(
      { error: "Not available in production" },
      { status: 403 }
    );
  }

  let body: CommitBody;
  try {
    body = (await req.json()) as CommitBody;
  } catch {
    return badRequest("Invalid JSON body");
  }

  // Validate required fields
  const slug = (body.slug ?? "").trim();
  const name = (body.name ?? "").trim();
  const brand = (body.brand ?? "").trim();
  const category = (body.category ?? "").trim();
  const subcategory = (body.subcategory ?? "").trim();
  const audienceInput = Array.isArray(body.audience) ? body.audience : [];
  const audience = audienceInput
    .map((a) => String(a).trim().toLowerCase())
    .filter((a): a is "mens" | "womens" => a === "mens" || a === "womens");
  // De-duplicate while preserving order.
  const audienceUnique = Array.from(new Set(audience));
  const reason = (body.reason ?? "").trim();
  const priceRange = (body.priceRange ?? "").trim();
  const url = (body.url ?? "").trim();
  const extractionMethod = (body.extractionMethod ?? "manual").trim();
  const images = Array.isArray(body.images) ? body.images : [];

  if (!slug || !/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(slug)) {
    return badRequest("slug must be lowercase kebab-case");
  }
  if (!name) return badRequest("name is required");
  if (!brand) return badRequest("brand is required");
  if (!SHOP_CATEGORIES.includes(category as Category)) {
    return badRequest(
      `category must be one of: ${SHOP_CATEGORIES.join(", ")}`
    );
  }
  // Subcategory is advisory — the canonical list is in categories.ts but
  // free-text values are allowed, so new subcategories can be created at
  // import time. We just enforce kebab-case.
  if (subcategory && !/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(subcategory)) {
    return badRequest("subcategory must be lowercase kebab-case");
  }
  // Best-effort visibility on canonical fit — log but don't block.
  void subcategoriesFor(category);
  if (!priceRange) return badRequest("priceRange is required");
  try {
    new URL(url);
  } catch {
    return badRequest("url must be a valid URL");
  }
  if (!VALID_METHODS.has(extractionMethod as ExtractionMethod)) {
    return badRequest(
      `extractionMethod must be one of: ${[...VALID_METHODS].join(", ")}`
    );
  }
  if (!images.length) return badRequest("at least one image is required");

  // Slug collision guard
  const existing = await readExistingSlugs();
  if (existing.has(slug)) {
    return NextResponse.json(
      { error: `slug "${slug}" already exists in shop.ts` },
      { status: 409 }
    );
  }

  // 1. Download images
  const saveResult = await saveImagesForSlug(slug, images);
  if (!saveResult.saved.length) {
    return NextResponse.json(
      {
        error: "No images could be downloaded",
        failed: saveResult.failed,
      },
      { status: 502 }
    );
  }

  // 2. Append entry
  const entry: NewShopEntry = {
    slug,
    name,
    brand,
    category: category as Category,
    subcategory: subcategory || undefined,
    audience: audienceUnique.length > 0 ? audienceUnique : undefined,
    // Stamp creation time at commit. Edits via PATCH preserve the
    // original dateAdded — see /api/admin/shop-item/[slug].
    dateAdded: new Date().toISOString(),
    reason,
    priceRange,
    url,
    images: saveResult.saved.map((s) => s.publicPath),
    extractionMethod: extractionMethod as ExtractionMethod,
    priceFloor:
      typeof body.priceFloor === "number" && body.priceFloor > 0
        ? body.priceFloor
        : undefined,
    htmlPriceSelector: body.htmlPriceSelector?.trim() || undefined,
  };

  try {
    await appendShopEntry(entry);
  } catch (e) {
    return NextResponse.json(
      {
        error: `Failed to write shop.ts: ${
          e instanceof Error ? e.message : String(e)
        }`,
        savedImages: saveResult.saved,
      },
      { status: 500 }
    );
  }

  return NextResponse.json({
    ok: true,
    slug,
    saved: saveResult.saved,
    failed: saveResult.failed,
  });
}
