/**
 * Shop drafts — stage a pending row with user-filled fields.
 *
 * POST /api/admin/shop-drafts/stage-pending
 *   body: {
 *     directUrl: string,
 *     fields: {
 *       name: string,
 *       brand: string,
 *       reason: string,
 *       category: Category,
 *       subcategory?: string,
 *       priceRange: string,
 *       audience?: ("mens" | "womens")[],
 *       images?: string[],   // override source URLs; falls back to
 *                            //   pending candidate.images, then a
 *                            //   fresh extractProduct() if neither.
 *     }
 *   }
 *
 * Behavior:
 *   1. Look up the pending entry by `directUrl`.
 *   2. Resolve image source URLs: prefer `fields.images`, then the
 *      candidate's images, then a fresh extract.
 *   3. Download images, append the entry to `src/data/shop.ts` as a
 *      draft, and cull the pending row.
 *
 * Distinct from `rescrape-pending`: this endpoint trusts the
 * user-provided fields rather than re-deriving them from the page.
 * Both endpoints converge on the same draft-stage write.
 *
 * Dev-only. Returns 403 in production.
 */

import fs from "node:fs/promises";
import path from "node:path";
import { NextRequest, NextResponse } from "next/server";
import {
  SHOP_CATEGORIES,
  type Category,
  type ExtractionMethod,
} from "../../../../../data/shop";
import { extractProduct } from "../../../../../lib/shopImport/extract";
import { buildSlug, ensureUnique } from "../../../../../lib/shopImport/slug";
import { saveImagesForSlug } from "../../../../../lib/shopImport/saveImages";
import {
  appendShopEntry,
  readExistingSlugs,
  type NewShopEntry,
} from "../../../../../lib/shopImport/writeEntry";

export const dynamic = "force-dynamic";

const PENDING_FILE = path.join(
  process.cwd(),
  "data",
  "shop-import-pending.json"
);

type PendingEntry = {
  rowIndex?: number;
  sourceArticle?: string;
  articleUrl?: string;
  anchor?: string;
  directUrl: string;
  flags?: string[];
  candidate: {
    slug?: string;
    name: string;
    brand: string;
    category?: string;
    audience?: string[];
    reason?: string;
    priceRange?: string;
    url: string;
    images?: string[];
    extractionMethod?: string;
  };
  stagedAt?: string;
};

type PendingFile = { entries: PendingEntry[] };

async function readPending(): Promise<PendingFile> {
  try {
    const raw = await fs.readFile(PENDING_FILE, "utf8");
    return JSON.parse(raw) as PendingFile;
  } catch {
    return { entries: [] };
  }
}

async function writePending(data: PendingFile): Promise<void> {
  await fs.mkdir(path.dirname(PENDING_FILE), { recursive: true });
  await fs.writeFile(
    PENDING_FILE,
    JSON.stringify(data, null, 2) + "\n",
    "utf8"
  );
}

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

function badRequest(message: string): NextResponse {
  return NextResponse.json({ error: message }, { status: 400 });
}

type Body = {
  directUrl?: string;
  fields?: {
    name?: string;
    brand?: string;
    reason?: string;
    category?: string;
    subcategory?: string;
    priceRange?: string;
    audience?: string[];
    images?: string[];
  };
};

export async function POST(req: NextRequest): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json(
      { error: "Not available in production" },
      { status: 403 }
    );
  }

  let body: Body;
  try {
    body = (await req.json()) as Body;
  } catch {
    return badRequest("Invalid JSON body");
  }

  const directUrl = (body.directUrl ?? "").trim();
  if (!directUrl) return badRequest("directUrl is required");
  try {
    new URL(directUrl);
  } catch {
    return badRequest("directUrl must be a valid URL");
  }

  const fields = body.fields ?? {};
  const name = (fields.name ?? "").trim();
  const brand = (fields.brand ?? "").trim();
  const reason = (fields.reason ?? "").trim();
  const category = (fields.category ?? "").trim();
  const subcategory = (fields.subcategory ?? "").trim() || "uncategorized";
  const priceRange = (fields.priceRange ?? "").trim();

  if (!name) return badRequest("name is required");
  if (!brand) return badRequest("brand is required");
  if (!SHOP_CATEGORIES.includes(category as Category)) {
    return badRequest(
      `category must be one of: ${SHOP_CATEGORIES.join(", ")}`
    );
  }
  if (!/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(subcategory)) {
    return badRequest(
      "subcategory must be lowercase kebab-case (or empty for placeholder)"
    );
  }
  if (!priceRange) return badRequest("priceRange is required");

  const audience = (fields.audience ?? [])
    .map((a) => String(a).trim().toLowerCase())
    .filter((a): a is "mens" | "womens" => a === "mens" || a === "womens");
  const audienceUnique = Array.from(new Set(audience));

  // Look up the pending entry. The endpoint trusts the form, but it
  // still needs the pending record so it can carry the original
  // extractionMethod (and so it can cull the entry on success).
  const pending = await readPending();
  const idx = pending.entries.findIndex((e) => e.directUrl === directUrl);
  if (idx < 0) {
    return NextResponse.json(
      { error: `No pending entry with directUrl "${directUrl}"` },
      { status: 404 }
    );
  }
  const entry = pending.entries[idx];

  // Resolve image source URLs:
  //   1. body.fields.images (explicit override)
  //   2. candidate.images
  //   3. a fresh extractProduct() against the source
  let imageSources: string[] = [];
  if (fields.images && fields.images.length > 0) {
    imageSources = fields.images.filter(Boolean);
  } else if (entry.candidate.images && entry.candidate.images.length > 0) {
    imageSources = entry.candidate.images.filter(Boolean);
  } else {
    try {
      const scrape = await extractProduct(directUrl);
      imageSources = scrape.images;
    } catch (e) {
      return NextResponse.json(
        {
          error: `No candidate images on file and rescrape failed: ${
            e instanceof Error ? e.message : String(e)
          }`,
        },
        { status: 502 }
      );
    }
  }
  if (imageSources.length === 0) {
    return badRequest(
      "No image sources available — paste image URLs into the form or import via /admin/shop-import"
    );
  }

  // Resolve extraction method — prefer the pending candidate's value
  // (so the live pricing extractor matches what the bulk script chose
  // when first ingesting). Fall back to manual.
  const candidateMethod = entry.candidate.extractionMethod ?? "manual";
  const validMethods: ReadonlySet<ExtractionMethod> = new Set([
    "json-ld",
    "shopify",
    "html",
    "manual",
  ]);
  const extractionMethod: ExtractionMethod = validMethods.has(
    candidateMethod as ExtractionMethod
  )
    ? (candidateMethod as ExtractionMethod)
    : "manual";

  // Slug: prefer candidate.slug, else build from brand + name.
  const existingSlugs = await readExistingSlugs();
  const proposedSlug = (entry.candidate.slug ?? "").trim() || buildSlug(brand, name);
  const slug = ensureUnique(proposedSlug, existingSlugs);

  // Download images.
  const saveResult = await saveImagesForSlug(slug, imageSources);
  if (saveResult.saved.length === 0) {
    return NextResponse.json(
      {
        error: "No images could be downloaded",
        failed: saveResult.failed,
      },
      { status: 502 }
    );
  }

  const newEntry: NewShopEntry = {
    slug,
    name,
    brand,
    category: category as Category,
    subcategory,
    audience: audienceUnique.length > 0 ? audienceUnique : undefined,
    dateAdded: new Date().toISOString(),
    reason,
    priceRange,
    url: directUrl,
    images: saveResult.saved.map((s) => s.publicPath),
    extractionMethod,
    draft: true,
  };

  try {
    await appendShopEntry(newEntry);
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

  // Cull pending row.
  pending.entries.splice(idx, 1);
  await writePending(pending);

  return NextResponse.json({
    ok: true,
    slug,
    saved: saveResult.saved,
    failed: saveResult.failed,
  });
}
