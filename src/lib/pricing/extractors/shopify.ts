import type { ExtractedPrice } from "../types";

/**
 * Shopify extractor.
 *
 * Every Shopify storefront exposes a public JSON view of any product
 * page at `${product-url}.json`. The payload includes the full variant
 * list with `price` (a string in major units) and `available` per
 * variant. This avoids HTML scraping entirely on Shopify-hosted shops
 * (Away, Bedsure, Clayton & Crume, LV Furniture, Ahlem, etc.).
 *
 * The product URL is normalized down to `/products/<handle>` before
 * `.json` is appended — Shopify ignores query strings and fragments
 * but rejects mistyped paths, so we keep the handle and drop the rest.
 */

type ShopifyMoney = {
  amount?: string | number;
  currency_code?: string;
};

type ShopifyVariant = {
  title?: string;
  price?: string | number;
  available?: boolean;
  /**
   * Multi-currency Shopify storefronts include a `presentment_prices`
   * array on each variant. When present, we use it to validate the
   * currency. When absent, the bare `price` is in the storefront's
   * base currency — assume USD and the per-product priceFloor will
   * catch any wildly wrong numbers.
   */
  presentment_prices?: { price?: ShopifyMoney }[];
};

type ShopifyProductJson = {
  product?: {
    variants?: ShopifyVariant[];
  };
};

/**
 * Shopify variant titles for sample swatches / replacement parts.
 * These get filtered out before formatting so a $25 fabric sample
 * doesn't become the displayed "From $25" of a $1,800 chair. The
 * per-product `priceFloor` is the proper backstop; this is a
 * belt-and-suspenders heuristic for the obvious cases.
 */
const NON_PRODUCT_VARIANT_TITLE = /^(swatch|sample|fabric sample|leather sample|replacement|spare|warranty|gift card|gift wrap)\b/i;

/**
 * Strip the URL down to the canonical Shopify product path. Drops
 * trailing `?…`, `#…`, and any path segments after `/products/<handle>`.
 */
function shopifyJsonUrl(url: string): string {
  const u = new URL(url);
  // /products/handle is always followed by 0 or more extra segments.
  const match = u.pathname.match(/^(.*?\/products\/[^/]+)/);
  if (!match) {
    throw new Error("URL does not contain a Shopify /products/ path");
  }
  u.pathname = `${match[1]}.json`;
  u.search = "";
  u.hash = "";
  return u.toString();
}

function readPrice(value: string | number | undefined): number | null {
  if (typeof value === "number" && Number.isFinite(value) && value > 0) {
    return value;
  }
  if (typeof value === "string") {
    const cleaned = value.replace(/[^0-9.]/g, "");
    if (!cleaned) return null;
    const num = Number(cleaned);
    return Number.isFinite(num) && num > 0 ? num : null;
  }
  return null;
}

export async function extractShopify(url: string): Promise<ExtractedPrice> {
  const jsonUrl = shopifyJsonUrl(url);
  const res = await fetch(jsonUrl, {
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
      Accept: "application/json",
    },
    next: { revalidate: 43200 },
    // Hard 4s ceiling — see jsonLd extractor for rationale.
    signal: AbortSignal.timeout(4000),
  });
  if (!res.ok) {
    throw new Error(`Shopify HTTP ${res.status}`);
  }
  const payload = (await res.json()) as ShopifyProductJson;
  const variants = payload.product?.variants ?? [];
  if (!variants.length) {
    throw new Error("Shopify payload contained no variants");
  }

  const prices: number[] = [];
  let availableCount = 0;
  const seenCurrencies = new Set<string>();
  for (const v of variants) {
    // Drop obvious non-product variants by title (samples, swatches,
    // gift wrap). Per-product priceFloor catches the rest.
    if (v.title && NON_PRODUCT_VARIANT_TITLE.test(v.title)) continue;

    const p = readPrice(v.price);
    if (p === null) continue;
    prices.push(p);
    if (v.available !== false) availableCount += 1;

    // Currency check via presentment_prices when available.
    const presentment = v.presentment_prices;
    if (Array.isArray(presentment)) {
      for (const entry of presentment) {
        const code = entry?.price?.currency_code;
        if (typeof code === "string" && code.length) {
          seenCurrencies.add(code.toUpperCase());
        }
      }
    }
  }
  if (!prices.length) {
    throw new Error("Shopify variants contained no usable price");
  }

  // When presentment_prices revealed currencies and none of them is
  // USD, refuse the result — the storefront is non-USD.
  if (seenCurrencies.size > 0 && !seenCurrencies.has("USD")) {
    throw new Error(
      `Shopify presentment currencies were ${[...seenCurrencies].join(", ")}; no USD`
    );
  }

  const cleaned = Array.from(new Set(prices)).sort((a, b) => a - b);
  return {
    variants: cleaned,
    // Sold out only if every variant is unavailable.
    soldOut: availableCount === 0,
  };
}
