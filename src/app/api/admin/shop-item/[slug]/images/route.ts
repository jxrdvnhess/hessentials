/**
 * Shop item — image management.
 *
 *   POST   /api/admin/shop-item/[slug]/images   body: { source: string }
 *           Download the remote image, save it content-addressed under
 *           public/shop/<slug>/<sha1>.jpg, append to the entry's
 *           images array, persist. Returns the updated images list.
 *
 *   DELETE /api/admin/shop-item/[slug]/images   body: { index: number }
 *           Remove image at `index` from the entry's images array.
 *           The file on disk is NOT deleted — content-addressed images
 *           may be referenced elsewhere, and the cost of orphan bytes
 *           is small. To purge unreferenced files, run a separate
 *           `clean-orphans` pass (out of scope here).
 *
 * Both routes preserve every other field on the entry. They piggyback
 * on the existing `replaceShopEntry` writer with a minimal NewShopEntry
 * built from the runtime SHOP_PRODUCTS state.
 *
 * Dev-only — 403 in production.
 */

import { NextRequest, NextResponse } from "next/server";
import { SHOP_PRODUCTS } from "../../../../../../data/shop";
import { replaceShopEntry } from "../../../../../../lib/shopImport/writeEntry";
import { saveOneContentAddressed } from "../../../../../../lib/shopImport/saveImages";

export const dynamic = "force-dynamic";

type RouteContext = { params: Promise<{ slug: string }> };

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

function notAvailable() {
  return NextResponse.json({ error: "Not available" }, { status: 403 });
}

function notFound(slug: string) {
  return NextResponse.json(
    { error: `No product with slug "${slug}".` },
    { status: 404 }
  );
}

/**
 * Build a NewShopEntry from a runtime ShopProduct + an explicit images
 * override. Used by both POST and DELETE to feed `replaceShopEntry`.
 */
function entryFor(slug: string, nextImages: string[]) {
  const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
  if (!product) return null;
  return {
    slug: product.slug,
    name: product.name,
    brand: product.brand,
    category: product.category,
    subcategory: product.subcategory,
    audience: [...(product.audience ?? [])] as ("mens" | "womens")[],
    dateAdded: product.dateAdded,
    reason: product.reason,
    priceRange: product.priceRange,
    url: product.url,
    images: nextImages,
    extractionMethod: product.extractionMethod ?? "manual",
    priceFloor: product.priceFloor,
    htmlPriceSelector: product.htmlPriceSelector,
    draft: product.draft,
  };
}

export async function POST(
  req: NextRequest,
  ctx: RouteContext
): Promise<NextResponse> {
  if (isProd()) return notAvailable();

  const { slug } = await ctx.params;
  const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
  if (!product) return notFound(slug);

  let body: { source?: string };
  try {
    body = (await req.json()) as { source?: string };
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }
  const source = (body.source ?? "").trim();
  if (!source) {
    return NextResponse.json({ error: "source is required" }, { status: 400 });
  }
  try {
    new URL(source);
  } catch {
    return NextResponse.json(
      { error: "source must be a valid URL" },
      { status: 400 }
    );
  }

  // Download + content-address.
  let saved;
  try {
    saved = await saveOneContentAddressed(slug, source);
  } catch (e) {
    return NextResponse.json(
      {
        error: `Failed to save image: ${
          e instanceof Error ? e.message : String(e)
        }`,
      },
      { status: 502 }
    );
  }

  // Append to images array — skip if the public path is already present
  // (content-addressed means the same image always produces the same
  // path, so a duplicate add is a no-op).
  const currentImages = product.images ?? [product.image];
  const nextImages = currentImages.includes(saved.publicPath)
    ? currentImages
    : [...currentImages, saved.publicPath];

  const entry = entryFor(slug, nextImages);
  if (!entry) return notFound(slug);
  try {
    await replaceShopEntry(slug, entry);
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
  return NextResponse.json({
    ok: true,
    slug,
    images: nextImages,
    added: saved.publicPath,
    alreadyPresent:
      nextImages === currentImages ||
      currentImages.includes(saved.publicPath),
  });
}

export async function DELETE(
  req: NextRequest,
  ctx: RouteContext
): Promise<NextResponse> {
  if (isProd()) return notAvailable();

  const { slug } = await ctx.params;
  const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
  if (!product) return notFound(slug);

  let body: { index?: number };
  try {
    body = (await req.json()) as { index?: number };
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }
  const index = body.index;
  if (typeof index !== "number" || !Number.isInteger(index) || index < 0) {
    return NextResponse.json(
      { error: "index must be a non-negative integer" },
      { status: 400 }
    );
  }

  const currentImages = product.images ?? [product.image];
  if (index >= currentImages.length) {
    return NextResponse.json(
      { error: `index out of bounds (have ${currentImages.length} images)` },
      { status: 400 }
    );
  }
  if (currentImages.length <= 1) {
    return NextResponse.json(
      { error: "Refusing to remove the last image — every product needs one." },
      { status: 409 }
    );
  }

  const nextImages = currentImages.filter((_, i) => i !== index);
  const entry = entryFor(slug, nextImages);
  if (!entry) return notFound(slug);
  try {
    await replaceShopEntry(slug, entry);
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
  return NextResponse.json({ ok: true, slug, images: nextImages });
}
