import type { ExtractedPrice } from "../types";

/**
 * JSON-LD extractor.
 *
 * Most modern e-commerce sites embed structured data in
 * `<script type="application/ld+json">` blocks. The Product schema
 * (https://schema.org/Product) carries an `offers` field — either a
 * single Offer or an AggregateOffer / array of Offers across variants.
 *
 * This extractor pulls every numeric `price` it finds in any Offer
 * descendant of any Product node, regardless of nesting depth. That
 * tolerance matters: source sites nest these inconsistently, and
 * reaching only the top-level Offer would miss most variant pricing.
 *
 * Availability detection is best-effort: if every Offer reports an
 * out-of-stock-style availability, `soldOut` is set to true.
 */

const SOLD_OUT_AVAILABILITY = new Set([
  "https://schema.org/OutOfStock",
  "http://schema.org/OutOfStock",
  "OutOfStock",
  "https://schema.org/SoldOut",
  "http://schema.org/SoldOut",
  "SoldOut",
  "https://schema.org/Discontinued",
  "http://schema.org/Discontinued",
  "Discontinued",
]);

/**
 * Recursively pull `<script type="application/ld+json">` payloads out
 * of a raw HTML string. Returns parsed JS values (ignores blocks that
 * fail to parse — many sites embed templated/broken JSON-LD).
 */
function extractJsonLdBlocks(html: string): unknown[] {
  const blocks: unknown[] = [];
  const regex =
    /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  let match: RegExpExecArray | null;
  while ((match = regex.exec(html)) !== null) {
    const raw = match[1].trim();
    if (!raw) continue;
    try {
      // Some sites encode HTML entities inside JSON-LD. The most common
      // offender is `&amp;`. Decode the common ones cheaply.
      const decoded = raw
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"');
      blocks.push(JSON.parse(decoded));
    } catch {
      // ignore malformed blocks
    }
  }
  return blocks;
}

/**
 * Walk an arbitrary JSON-LD value tree and yield every node whose
 * `@type` indicates a Product (singular or array form).
 */
function* findProducts(node: unknown): Generator<Record<string, unknown>> {
  if (!node || typeof node !== "object") return;
  if (Array.isArray(node)) {
    for (const item of node) yield* findProducts(item);
    return;
  }
  const obj = node as Record<string, unknown>;
  const type = obj["@type"];
  const isProduct =
    type === "Product" || (Array.isArray(type) && type.includes("Product"));
  if (isProduct) yield obj;
  // @graph wraps multi-node JSON-LD docs.
  if (Array.isArray(obj["@graph"])) {
    for (const item of obj["@graph"] as unknown[]) yield* findProducts(item);
  }
  // Walk known nesting points without scanning every key (cheap).
  for (const key of ["mainEntity", "isVariantOf", "hasVariant"]) {
    if (obj[key]) yield* findProducts(obj[key]);
  }
}

/**
 * Walk an arbitrary value tree and yield every Offer node. Used to
 * collect all variant prices regardless of how the source site nests
 * them under a Product.
 */
function* findOffers(node: unknown): Generator<Record<string, unknown>> {
  if (!node || typeof node !== "object") return;
  if (Array.isArray(node)) {
    for (const item of node) yield* findOffers(item);
    return;
  }
  const obj = node as Record<string, unknown>;
  const type = obj["@type"];
  const isOffer =
    type === "Offer" ||
    type === "AggregateOffer" ||
    (Array.isArray(type) &&
      (type.includes("Offer") || type.includes("AggregateOffer")));
  if (isOffer) yield obj;
  // Recurse into common containers.
  for (const key of ["offers", "itemOffered", "hasVariant", "isVariantOf"]) {
    if (obj[key]) yield* findOffers(obj[key]);
  }
}

/**
 * Coerce an Offer.price field (string | number | undefined) to a
 * positive number. Returns null when the value is missing or unusable.
 */
function readPrice(value: unknown): number | null {
  if (typeof value === "number" && Number.isFinite(value) && value > 0) {
    return value;
  }
  if (typeof value === "string") {
    // Strip common formatting: currency symbols, commas, whitespace.
    const cleaned = value.replace(/[^0-9.]/g, "");
    if (!cleaned) return null;
    const num = Number(cleaned);
    return Number.isFinite(num) && num > 0 ? num : null;
  }
  return null;
}

export async function extractJsonLd(url: string): Promise<ExtractedPrice> {
  const res = await fetch(url, {
    headers: {
      // A plausible UA gets us past the most basic bot filters
      // without being deceptive. Many sites serve no JSON-LD to
      // unrecognized agents.
      "User-Agent":
        "Mozilla/5.0 (compatible; HessentialsBot/1.0; +https://hessentials.co)",
      Accept: "text/html,application/xhtml+xml",
    },
    // Next.js fetch caching — see fetchPrice.ts for the orchestration.
    next: { revalidate: 43200 },
    // Hard 4s ceiling. Without this, slow / hostile sources hang the
    // Next.js static export and the build fails after the page export
    // timeout. A timeout error is caught by fetchPrice and falls back
    // to the static priceRange — quiet, predictable.
    signal: AbortSignal.timeout(4000),
  });
  if (!res.ok) {
    throw new Error(`Source HTTP ${res.status}`);
  }
  const html = await res.text();
  const blocks = extractJsonLdBlocks(html);
  if (!blocks.length) {
    throw new Error("No JSON-LD blocks found");
  }

  const variants: number[] = [];
  let availabilityCount = 0;
  let soldOutCount = 0;
  // Currency check: when a priceCurrency appears anywhere in the
  // collected Offers, every observed currency must be USD. If the
  // source serves anything else we refuse the result rather than
  // mislabelling foreign-denominated prices as dollars.
  const seenCurrencies = new Set<string>();

  for (const block of blocks) {
    for (const product of findProducts(block)) {
      for (const offer of findOffers(product)) {
        const single = readPrice(offer["price"]);
        if (single !== null) variants.push(single);

        // AggregateOffer carries lowPrice / highPrice instead.
        const low = readPrice(offer["lowPrice"]);
        if (low !== null) variants.push(low);
        const high = readPrice(offer["highPrice"]);
        if (high !== null) variants.push(high);

        const currency = offer["priceCurrency"];
        if (typeof currency === "string" && currency.length) {
          seenCurrencies.add(currency.toUpperCase());
        }

        const avail = offer["availability"];
        if (typeof avail === "string") {
          availabilityCount += 1;
          if (SOLD_OUT_AVAILABILITY.has(avail)) soldOutCount += 1;
        }
      }
    }
  }

  if (seenCurrencies.size > 0) {
    const nonUsd = [...seenCurrencies].filter((c) => c !== "USD");
    if (nonUsd.length) {
      throw new Error(
        `JSON-LD reported non-USD currency: ${nonUsd.join(", ")}`
      );
    }
  }

  // Deduplicate and drop suspicious zeros.
  const cleaned = Array.from(
    new Set(variants.filter((v) => v > 0))
  ).sort((a, b) => a - b);

  if (!cleaned.length) {
    throw new Error("JSON-LD contained no usable price");
  }

  // Sold-out only if every observed availability said so. If no
  // availability strings appeared at all, assume in stock.
  const soldOut =
    availabilityCount > 0 && soldOutCount === availabilityCount;

  return { variants: cleaned, soldOut };
}
