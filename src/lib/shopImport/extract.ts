/**
 * Shop import — product metadata extractor.
 *
 * Single HTTP fetch, single parse pass. Pulls everything we can derive
 * automatically from a public product URL:
 *
 *   - name              from JSON-LD Product.name, fallback OG title, fallback <title>
 *   - brand             from JSON-LD Product.brand.name, fallback OG site_name, fallback domain
 *   - prices            from JSON-LD Offers / AggregateOffer (variants + sold-out)
 *   - images            from JSON-LD Product.image (string | string[] | ImageObject), then OG
 *   - extractionMethod  best-guess by URL shape (Shopify /products/ → "shopify", else "json-ld")
 *
 * The reason / category / priceFloor fields are intentionally NOT extracted —
 * those are editorial / judgment calls. The admin UI leaves them blank for
 * Jordan to fill in.
 *
 * Reuses the same JSON-LD walking primitives as src/lib/pricing/extractors/jsonLd.ts.
 * If that file's parsing strategy ever changes, mirror it here.
 */

import type { ExtractionMethod } from "../../data/shop";

export type ExtractedProduct = {
  name: string;
  brand: string;
  /** Sorted ascending, deduplicated, in USD. May be empty. */
  prices: number[];
  /** True iff every observed Offer reported sold-out availability. */
  soldOut: boolean;
  /** Absolute image URLs, in source order, deduplicated. */
  images: string[];
  /** Best-guess extractor for the live pricing layer. */
  extractionMethod: ExtractionMethod;
  /** Domain stripped to host (no www.) — used as a brand fallback. */
  host: string;
};

const FETCH_TIMEOUT_MS = 8000;

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

/** Strip <script type="application/ld+json"> blocks and JSON-parse each. */
function extractJsonLdBlocks(html: string): unknown[] {
  const blocks: unknown[] = [];
  const regex =
    /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  let match: RegExpExecArray | null;
  while ((match = regex.exec(html)) !== null) {
    const raw = match[1].trim();
    if (!raw) continue;
    try {
      const decoded = raw
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"');
      blocks.push(JSON.parse(decoded));
    } catch {
      // Many sites embed templated/broken JSON-LD — skip silently.
    }
  }
  return blocks;
}

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
  if (Array.isArray(obj["@graph"])) {
    for (const item of obj["@graph"] as unknown[]) yield* findProducts(item);
  }
  for (const key of ["mainEntity", "isVariantOf", "hasVariant"]) {
    if (obj[key]) yield* findProducts(obj[key]);
  }
}

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
  for (const key of ["offers", "itemOffered", "hasVariant", "isVariantOf"]) {
    if (obj[key]) yield* findOffers(obj[key]);
  }
}

function readNumber(value: unknown): number | null {
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

function readString(value: unknown): string | null {
  if (typeof value === "string") {
    const trimmed = value.trim();
    return trimmed.length ? trimmed : null;
  }
  return null;
}

/** schema.org image can be string | string[] | ImageObject | ImageObject[]. */
function readImages(value: unknown, acc: string[]): void {
  if (!value) return;
  if (typeof value === "string") {
    const t = value.trim();
    if (t) acc.push(t);
    return;
  }
  if (Array.isArray(value)) {
    for (const item of value) readImages(item, acc);
    return;
  }
  if (typeof value === "object") {
    const url = (value as Record<string, unknown>)["url"];
    if (typeof url === "string" && url.trim()) acc.push(url.trim());
    const contentUrl = (value as Record<string, unknown>)["contentUrl"];
    if (typeof contentUrl === "string" && contentUrl.trim()) {
      acc.push(contentUrl.trim());
    }
  }
}

function readBrand(value: unknown): string | null {
  if (!value) return null;
  if (typeof value === "string") return value.trim() || null;
  if (Array.isArray(value)) {
    for (const item of value) {
      const found = readBrand(item);
      if (found) return found;
    }
    return null;
  }
  if (typeof value === "object") {
    const obj = value as Record<string, unknown>;
    const name = obj["name"];
    if (typeof name === "string" && name.trim()) return name.trim();
  }
  return null;
}

/** Read `<meta property="X">` and `<meta name="X">` tags, all values. */
function readMetaTag(html: string, property: string): string | null {
  const escaped = property.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  // property="og:title" content="..."
  const re1 = new RegExp(
    `<meta[^>]+(?:property|name)=["']${escaped}["'][^>]+content=["']([^"']+)["']`,
    "i"
  );
  // content="..." property="og:title"  (some sites order them this way)
  const re2 = new RegExp(
    `<meta[^>]+content=["']([^"']+)["'][^>]+(?:property|name)=["']${escaped}["']`,
    "i"
  );
  const m = html.match(re1) ?? html.match(re2);
  return m ? m[1].trim() : null;
}

function readMetaTagAll(html: string, property: string): string[] {
  const escaped = property.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  const re = new RegExp(
    `<meta[^>]+(?:property|name)=["']${escaped}["'][^>]+content=["']([^"']+)["']`,
    "gi"
  );
  const out: string[] = [];
  let m: RegExpExecArray | null;
  while ((m = re.exec(html)) !== null) {
    out.push(m[1].trim());
  }
  return out;
}

function readTitleTag(html: string): string | null {
  const m = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  if (!m) return null;
  return m[1]
    .replace(/\s+/g, " ")
    .trim()
    .replace(/&amp;/g, "&")
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"');
}

/** Best-guess extractor based on URL shape — matches what Jordan curates by hand. */
function guessExtractionMethod(url: string): ExtractionMethod {
  try {
    const u = new URL(url);
    if (/\/products\/[^/]+/.test(u.pathname)) return "shopify";
  } catch {
    // ignore
  }
  return "json-ld";
}

function hostOf(url: string): string {
  try {
    return new URL(url).host.replace(/^www\./, "");
  } catch {
    return "";
  }
}

function absolutize(maybeUrl: string, base: string): string {
  try {
    return new URL(maybeUrl, base).toString();
  } catch {
    return maybeUrl;
  }
}

/** Title-case a domain segment for fallback brand display ("loewe" → "Loewe"). */
function titleizeHost(host: string): string {
  const root = host.split(".")[0];
  if (!root) return "";
  return root
    .split(/[-_]/)
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
    .join(" ");
}

export async function fetchProductPage(url: string): Promise<string> {
  const res = await fetch(url, {
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
      Accept: "text/html,application/xhtml+xml",
    },
    signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Source HTTP ${res.status}`);
  }
  return res.text();
}

export function parseProductPage(
  html: string,
  sourceUrl: string
): ExtractedProduct {
  const blocks = extractJsonLdBlocks(html);

  let name: string | null = null;
  let brand: string | null = null;
  const imageAcc: string[] = [];
  const variants: number[] = [];
  let availabilityCount = 0;
  let soldOutCount = 0;

  for (const block of blocks) {
    for (const product of findProducts(block)) {
      if (!name) name = readString(product["name"]);
      if (!brand) brand = readBrand(product["brand"]);
      readImages(product["image"], imageAcc);

      for (const offer of findOffers(product)) {
        const single = readNumber(offer["price"]);
        if (single !== null) variants.push(single);
        const low = readNumber(offer["lowPrice"]);
        if (low !== null) variants.push(low);
        const high = readNumber(offer["highPrice"]);
        if (high !== null) variants.push(high);

        const avail = offer["availability"];
        if (typeof avail === "string") {
          availabilityCount += 1;
          if (SOLD_OUT_AVAILABILITY.has(avail)) soldOutCount += 1;
        }
      }
    }
  }

  // OG fallbacks for name/brand
  if (!name) name = readMetaTag(html, "og:title") ?? readTitleTag(html);
  if (!brand) {
    brand =
      readMetaTag(html, "og:site_name") ??
      readMetaTag(html, "product:brand") ??
      titleizeHost(hostOf(sourceUrl));
  }
  // Always merge OG / Twitter images alongside JSON-LD — many product
  // pages embed only the primary image in JSON-LD and stash the rest
  // of the gallery in og:image entries (or, for Shopify, the
  // .json endpoint — handled in the orchestrator below).
  for (const img of readMetaTagAll(html, "og:image")) imageAcc.push(img);
  for (const img of readMetaTagAll(html, "og:image:secure_url")) {
    imageAcc.push(img);
  }
  const twitterImg = readMetaTag(html, "twitter:image");
  if (twitterImg) imageAcc.push(twitterImg);
  const twitterImgSrc = readMetaTag(html, "twitter:image:src");
  if (twitterImgSrc) imageAcc.push(twitterImgSrc);

  // Absolutize + dedupe images
  const seen = new Set<string>();
  const images: string[] = [];
  for (const raw of imageAcc) {
    const abs = absolutize(raw, sourceUrl);
    if (!seen.has(abs)) {
      seen.add(abs);
      images.push(abs);
    }
  }

  const prices = Array.from(new Set(variants.filter((v) => v > 0))).sort(
    (a, b) => a - b
  );

  const soldOut =
    availabilityCount > 0 && soldOutCount === availabilityCount;

  return {
    name: name ?? "",
    brand: brand ?? "",
    prices,
    soldOut,
    images,
    extractionMethod: guessExtractionMethod(sourceUrl),
    host: hostOf(sourceUrl),
  };
}

/**
 * Shopify storefronts publish every product at `/products/<handle>.json`,
 * including the full image gallery as `product.images[].src`. Most
 * Shopify product pages only embed the primary image in JSON-LD, so
 * this is how we recover the rest of the gallery.
 *
 * Returns absolute image URLs in source order. Quietly returns `[]`
 * on any error — the orchestrator falls back to whatever images the
 * HTML / OG tags surfaced.
 */
async function fetchShopifyGallery(productUrl: string): Promise<string[]> {
  try {
    const u = new URL(productUrl);
    const match = u.pathname.match(/^(.*?\/products\/[^/]+)/);
    if (!match) return [];
    u.pathname = `${match[1]}.json`;
    u.search = "";
    u.hash = "";
    const res = await fetch(u.toString(), {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        Accept: "application/json",
      },
      signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
      cache: "no-store",
    });
    if (!res.ok) return [];
    const payload = (await res.json()) as {
      product?: {
        images?: Array<{ src?: string; position?: number }>;
        image?: { src?: string };
      };
    };
    const out: string[] = [];
    const list = payload.product?.images ?? [];
    // Sort by position so primary lands first when the API hands them
    // back in update-time order.
    const sorted = [...list].sort(
      (a, b) => (a.position ?? 0) - (b.position ?? 0)
    );
    for (const img of sorted) {
      if (typeof img.src === "string" && img.src.trim()) {
        out.push(img.src.trim());
      }
    }
    return out;
  } catch {
    return [];
  }
}

/**
 * Cap the number of images we surface to the import form. The form
 * renders thumbnails, so an extreme-case page with 30+ images would
 * produce visual noise. Eight is plenty for a curated edit and lets
 * the user deselect down to the chosen handful.
 */
const MAX_IMAGES = 10;

export async function extractProduct(url: string): Promise<ExtractedProduct> {
  const html = await fetchProductPage(url);
  const result = parseProductPage(html, url);

  // For Shopify URLs, the .json endpoint carries the full gallery —
  // typically more than the JSON-LD `Product.image`. Prepend so the
  // user sees the full list without having to re-import.
  if (result.extractionMethod === "shopify") {
    const gallery = await fetchShopifyGallery(url);
    if (gallery.length > 0) {
      const seen = new Set(result.images);
      const merged: string[] = [];
      // Shopify gallery first (more complete), then anything we found
      // from JSON-LD / OG that isn't a duplicate.
      for (const img of gallery) {
        const abs = absolutize(img, url);
        if (!seen.has(abs)) {
          seen.add(abs);
          merged.push(abs);
        }
      }
      for (const img of result.images) {
        if (!seen.has(img)) {
          seen.add(img);
          merged.push(img);
        }
      }
      result.images = merged;
    }
  }

  if (result.images.length > MAX_IMAGES) {
    result.images = result.images.slice(0, MAX_IMAGES);
  }

  return result;
}
