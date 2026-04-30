import type { ShopProduct } from "../../data/shop";
import { extractJsonLd } from "./extractors/jsonLd";
import { extractShopify } from "./extractors/shopify";
import { extractHtml } from "./extractors/html";
import { formatVariants } from "./format";
import type { ExtractedPrice, PriceFetchResult } from "./types";

/**
 * Pricing fetch entry point.
 *
 * Each Shop product declares (or omits) an `extractionMethod`. The
 * caller hands a product in; the fetch layer routes to the right
 * extractor, formats the variant list with `formatVariants`, and
 * returns a `PriceFetchResult` ready for UI consumption.
 *
 * Failure handling:
 *   - Any extractor throw is caught here.
 *   - The result falls back to the static `priceRange` from the
 *     product (manual / last-known-good).
 *   - The error is captured for the admin surface, but no exception
 *     escapes — pages render every time.
 *
 * Caching:
 *   - Each extractor's underlying `fetch` already requests a 12-hour
 *     revalidation from Next.js (43200 seconds).
 *   - This layer adds nothing on top — pages that read a price are
 *     expected to either be statically generated with `revalidate` or
 *     forced dynamic for the admin surface.
 */

const REVALIDATE_SECONDS = 43200;
export const PRICING_REVALIDATE_SECONDS = REVALIDATE_SECONDS;

async function runExtractor(
  product: ShopProduct
): Promise<ExtractedPrice> {
  switch (product.extractionMethod) {
    case "json-ld":
      return extractJsonLd(product.url);
    case "shopify":
      return extractShopify(product.url);
    case "html":
      if (!product.htmlPriceSelector) {
        throw new Error(
          "extractionMethod is 'html' but no htmlPriceSelector is set"
        );
      }
      return extractHtml(product.url, product.htmlPriceSelector);
    default:
      throw new Error(
        `Unknown extractionMethod: ${product.extractionMethod}`
      );
  }
}

/**
 * Resolve the displayed price for a single product. Always succeeds —
 * fall-back to the static priceRange covers every error path.
 */
export async function fetchProductPrice(
  product: ShopProduct
): Promise<PriceFetchResult> {
  // Manual mode: no fetch attempted. Display the curated string as-is.
  if (
    !product.extractionMethod ||
    product.extractionMethod === "manual"
  ) {
    return {
      display: product.priceRange,
      live: false,
      soldOut: false,
      method: "manual",
    };
  }

  try {
    const extracted = await runExtractor(product);
    const display = extracted.soldOut
      ? "Sold out"
      : formatVariants(extracted.variants);
    return {
      display,
      live: true,
      lastVerified: new Date().toISOString(),
      soldOut: extracted.soldOut,
      method: product.extractionMethod,
    };
  } catch (e) {
    // Quiet fallback — on failure, render the static priceRange. The
    // admin surface is where the failure surfaces; the public page
    // never breaks.
    return {
      display: product.priceRange,
      live: false,
      soldOut: false,
      method: product.extractionMethod,
      error: e instanceof Error ? e.message : String(e),
    };
  }
}

/**
 * Resolve prices for every product in parallel. Used by the index
 * page so the grid renders with one upstream wave per ISR cycle.
 */
export async function fetchAllPrices(
  products: ReadonlyArray<ShopProduct>
): Promise<Record<string, PriceFetchResult>> {
  const entries = await Promise.all(
    products.map(async (p) => [p.slug, await fetchProductPrice(p)] as const)
  );
  return Object.fromEntries(entries);
}
