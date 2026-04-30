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

type ShopifyVariant = {
  price?: string | number;
  available?: boolean;
};

type ShopifyProductJson = {
  product?: {
    variants?: ShopifyVariant[];
  };
};

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
        "Mozilla/5.0 (compatible; HessentialsBot/1.0; +https://hessentials.co)",
      Accept: "application/json",
    },
    next: { revalidate: 43200 },
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
  for (const v of variants) {
    const p = readPrice(v.price);
    if (p === null) continue;
    prices.push(p);
    if (v.available !== false) availableCount += 1;
  }
  if (!prices.length) {
    throw new Error("Shopify variants contained no usable price");
  }

  const cleaned = Array.from(new Set(prices)).sort((a, b) => a - b);
  return {
    variants: cleaned,
    // Sold out only if every variant is unavailable.
    soldOut: availableCount === 0,
  };
}
