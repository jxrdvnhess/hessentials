/**
 * Shop item — re-scrape from source URL.
 *
 * POST /api/admin/shop-item/[slug]/rescrape
 *   body: { url?: string }
 *
 * Re-runs the JSON-LD / OG extractor against the entry's source URL
 * (or `body.url` if the caller is testing a replacement). Returns the
 * scraped fields as JSON — no writes. The edit form decides per-field
 * whether to adopt the new values.
 *
 * Use cases:
 *   - The product page was updated (better images, new price).
 *   - The original scrape missed structured data that's now available.
 *   - The URL itself has changed and you want to preview the new
 *     scrape before saving.
 *
 * Dev-only — 403 in production.
 */

import { NextRequest, NextResponse } from "next/server";
import { SHOP_PRODUCTS } from "../../../../../../data/shop";
import { extractProduct } from "../../../../../../lib/shopImport/extract";
import { suggestPriceRange } from "../../../../../../lib/shopImport/formatPriceRange";

export const dynamic = "force-dynamic";

type RouteContext = { params: Promise<{ slug: string }> };

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

export async function POST(
  req: NextRequest,
  ctx: RouteContext
): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json({ error: "Not available" }, { status: 403 });
  }

  const { slug } = await ctx.params;
  const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
  if (!product) {
    return NextResponse.json(
      { error: `No product with slug "${slug}".` },
      { status: 404 }
    );
  }

  // Allow an override URL so the user can preview a candidate
  // replacement before committing the URL change on the form.
  let body: { url?: string };
  try {
    body = (await req.json().catch(() => ({}))) as { url?: string };
  } catch {
    body = {};
  }
  const url = (body.url ?? product.url).trim();
  if (!url) {
    return NextResponse.json({ error: "url is required" }, { status: 400 });
  }
  try {
    new URL(url);
  } catch {
    return NextResponse.json(
      { error: "url must be a valid URL" },
      { status: 400 }
    );
  }

  let scrape;
  try {
    scrape = await extractProduct(url);
  } catch (e) {
    return NextResponse.json(
      {
        error: `Scrape failed: ${
          e instanceof Error ? e.message : String(e)
        }`,
      },
      { status: 502 }
    );
  }

  const priceRangeSuggestion = suggestPriceRange(scrape.prices);

  return NextResponse.json({
    ok: true,
    slug,
    url,
    scraped: {
      name: scrape.name,
      brand: scrape.brand,
      description: scrape.description,
      prices: scrape.prices,
      priceRangeSuggestion,
      soldOut: scrape.soldOut,
      images: scrape.images,
      audience: scrape.audience,
      extractionMethod: scrape.extractionMethod,
    },
  });
}
