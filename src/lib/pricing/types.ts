/**
 * Pricing fetch types — Hessentials Shop.
 *
 * Each Shop product can declare an `extractionMethod` that tells the
 * pricing layer how to read the *current* retail price from the source
 * URL. The static `priceRange` on the product remains the manual
 * fallback / last-known-good when fetch fails or is unconfigured.
 *
 * The fetch layer is intentionally conservative:
 *   - On success → live price + ISO timestamp.
 *   - On any failure → fall back to static priceRange, log error.
 *   - Sold-out → `soldOut: true`, display still resolves.
 *
 * No exceptions escape the fetch layer. Pages render predictably.
 */

export type ExtractionMethod =
  /** Parse <script type="application/ld+json"> Product schema. */
  | "json-ld"
  /** Hit the Shopify product JSON endpoint at `${url}.json`. */
  | "shopify"
  /** Scrape with a per-product CSS selector. Last resort. */
  | "html"
  /** No fetch — display the static priceRange as-is. Default for products
   *  without an extractionMethod set. */
  | "manual";

/**
 * Normalized output of any extractor. The fetch layer turns this into
 * a `PriceFetchResult`, then the pricing format helper turns the
 * `variants` array into a display string ("$1,800" or "From $850").
 *
 * Extractors enforce currency at their boundary — JSON-LD reads
 * `priceCurrency` and rejects non-USD; Shopify reads the storefront's
 * base currency and rejects non-USD; HTML assumes the displayed
 * currency on the page (caller's responsibility to pick a USD URL).
 */
export type ExtractedPrice = {
  /** All variant prices in USD whole or fractional dollars. Length 1+. */
  variants: number[];
  /** True if every variant is unavailable / sold out at the source. */
  soldOut: boolean;
};

/**
 * What the pricing layer hands to UI. Pages render directly from this
 * — no further normalization required.
 */
export type PriceFetchResult = {
  /** Display string. "$1,800" / "From $850" / "$890–$1,050" / "Sold out". */
  display: string;
  /**
   * True iff this came from a successful live fetch this cycle. False
   * for the static priceRange fallback (whether by config or by error).
   */
  live: boolean;
  /**
   * ISO timestamp of the successful fetch. Only set when `live` is
   * true. Used by the detail page for the "Last verified" line.
   */
  lastVerified?: string;
  /** True if the source reports sold-out / unavailable. */
  soldOut: boolean;
  /** Which extractor produced this (or 'manual' for the fallback). */
  method: ExtractionMethod;
  /** Error message if the fetch failed. Surfaces in the admin page. */
  error?: string;
};
