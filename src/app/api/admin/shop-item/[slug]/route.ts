/**
 * Shop item — read / update / delete by slug.
 *
 *   GET    /api/admin/shop-item/[slug]   → returns the product JSON
 *   PATCH  /api/admin/shop-item/[slug]   → replaces the entry in shop.ts
 *   DELETE /api/admin/shop-item/[slug]   → removes the entry + images
 *
 * Slug renames are intentionally NOT supported here — changing a slug
 * would break image references and any external links. To rename,
 * delete and re-import.
 *
 * Image management is also out of scope for this endpoint. The PATCH
 * body's `images` array is treated as the new ordered list of public
 * paths; the caller is expected to pass exactly the existing files
 * back. Adding new images is done via /api/admin/shop-import.
 *
 * Dev-only. Returns 403 in production.
 */

import { NextRequest, NextResponse } from "next/server";
import {
  SHOP_CATEGORIES,
  SHOP_PRODUCTS,
  type Category,
  type ExtractionMethod,
} from "../../../../../data/shop";
import {
  replaceShopEntry,
  deleteShopEntry,
  entryExists,
  type NewShopEntry,
} from "../../../../../lib/shopImport/writeEntry";
import { deleteImagesForSlug } from "../../../../../lib/shopImport/deleteImages";

export const dynamic = "force-dynamic";

const VALID_METHODS: ReadonlySet<ExtractionMethod> = new Set([
  "json-ld",
  "shopify",
  "html",
  "manual",
]);

type RouteContext = { params: Promise<{ slug: string }> };

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

function badRequest(message: string): NextResponse {
  return NextResponse.json({ error: message }, { status: 400 });
}

function notFound(slug: string): NextResponse {
  return NextResponse.json(
    { error: `No product with slug "${slug}".` },
    { status: 404 }
  );
}

export async function GET(
  _req: NextRequest,
  ctx: RouteContext
): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json({ error: "Not available" }, { status: 403 });
  }
  const { slug } = await ctx.params;
  const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
  if (!product) return notFound(slug);
  return NextResponse.json({ product });
}

type PatchBody = {
  name?: string;
  brand?: string;
  category?: string;
  subcategory?: string;
  reason?: string;
  priceRange?: string;
  url?: string;
  images?: string[];
  extractionMethod?: string;
  htmlPriceSelector?: string;
  priceFloor?: number | null;
};

export async function PATCH(
  req: NextRequest,
  ctx: RouteContext
): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json({ error: "Not available" }, { status: 403 });
  }
  const { slug } = await ctx.params;

  if (!(await entryExists(slug))) return notFound(slug);

  let body: PatchBody;
  try {
    body = (await req.json()) as PatchBody;
  } catch {
    return badRequest("Invalid JSON body");
  }

  const name = (body.name ?? "").trim();
  const brand = (body.brand ?? "").trim();
  const category = (body.category ?? "").trim();
  const subcategory = (body.subcategory ?? "").trim();
  const reason = body.reason ?? "";
  const priceRange = (body.priceRange ?? "").trim();
  const url = (body.url ?? "").trim();
  const extractionMethod = (body.extractionMethod ?? "manual").trim();
  const images = Array.isArray(body.images) ? body.images : [];

  if (!name) return badRequest("name is required");
  if (!brand) return badRequest("brand is required");
  if (!SHOP_CATEGORIES.includes(category as Category)) {
    return badRequest(
      `category must be one of: ${SHOP_CATEGORIES.join(", ")}`
    );
  }
  if (subcategory && !/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(subcategory)) {
    return badRequest("subcategory must be lowercase kebab-case");
  }
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
  if (!images.length) return badRequest("at least one image path is required");

  const next: NewShopEntry = {
    slug,
    name,
    brand,
    category: category as Category,
    subcategory: subcategory || undefined,
    reason,
    priceRange,
    url,
    images,
    extractionMethod: extractionMethod as ExtractionMethod,
    priceFloor:
      typeof body.priceFloor === "number" && body.priceFloor > 0
        ? body.priceFloor
        : undefined,
    htmlPriceSelector: body.htmlPriceSelector?.trim() || undefined,
  };

  try {
    await replaceShopEntry(slug, next);
  } catch (e) {
    return NextResponse.json(
      {
        error: `Failed to write shop.ts: ${
          e instanceof Error ? e.message : String(e)
        }`,
      },
      { status: 500 }
    );
  }

  return NextResponse.json({ ok: true, slug });
}

export async function DELETE(
  _req: NextRequest,
  ctx: RouteContext
): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json({ error: "Not available" }, { status: 403 });
  }
  const { slug } = await ctx.params;

  if (!(await entryExists(slug))) return notFound(slug);

  try {
    await deleteShopEntry(slug);
  } catch (e) {
    return NextResponse.json(
      {
        error: `Failed to update shop.ts: ${
          e instanceof Error ? e.message : String(e)
        }`,
      },
      { status: 500 }
    );
  }

  // Image unlink is best-effort — entry is already gone from shop.ts.
  let removedImages: string[] = [];
  try {
    removedImages = await deleteImagesForSlug(slug);
  } catch (e) {
    return NextResponse.json({
      ok: true,
      slug,
      removedImages: [],
      imageError: e instanceof Error ? e.message : String(e),
    });
  }

  return NextResponse.json({ ok: true, slug, removedImages });
}
