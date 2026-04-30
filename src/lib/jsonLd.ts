/**
 * JSON-LD structured data generators (Schema.org).
 *
 * Each function returns a plain object suitable for serialization into
 * a `<script type="application/ld+json">` tag via the JsonLd component
 * (see `src/components/JsonLd.tsx`).
 *
 * Why this exists:
 *   Google can index plain HTML, but structured data is the difference
 *   between a blue link and a rich result — recipe cards with cook
 *   time and an image, products with price + availability, articles
 *   that surface in Top Stories. For an editorial brand without
 *   established domain authority, rich results are the highest-leverage
 *   one-time SEO improvement available.
 *
 * What we publish:
 *   Organization + WebSite — root-level identity, every page.
 *   Article — Living, Style, Practice articles.
 *   Recipe — Recipes (richest schema; cooking time, ingredients,
 *            steps, yield).
 *   Product + Offer — Shop items.
 *
 * What we deliberately don't publish:
 *   AggregateRating / Review — would require ratings data we don't
 *     collect, and faking them violates Google's structured data
 *     policy.
 *   Author Person URLs — Jordan / Aurelian don't have separate "author
 *     pages" by URL. Author is published as a Person object inline.
 */

import type { Recipe, Ingredient } from "../types/recipe";
import type { ShopProduct } from "../data/shop";

const SITE = "https://hessentials.co";
const BRAND_NAME = "Hessentials";
const LOGO_URL = `${SITE}/og-image.png`;
/**
 * Fallback image used when a piece of content doesn't carry its own.
 * Google's Recipe rich-results spec requires `image` (not optional —
 * missing it invalidates the entire Recipe block), and Article rich
 * results gain Top Stories eligibility when one is present. Pointing
 * at the site OG image gets the schema validated; per-piece images
 * become a content task to upgrade rich-result quality.
 */
const FALLBACK_IMAGE = `${SITE}/og-image.png`;

/* ---------- Helpers ---------- */

/**
 * Promote a path to an absolute URL. Schema.org `url` fields and
 * `image` URLs should be absolute so they resolve correctly when
 * Google crawls them in isolation from the page.
 */
export function absoluteUrl(pathOrUrl: string): string {
  if (/^https?:\/\//.test(pathOrUrl)) return pathOrUrl;
  if (pathOrUrl.startsWith("/")) return `${SITE}${pathOrUrl}`;
  return `${SITE}/${pathOrUrl}`;
}

/**
 * Convert recipe meta time strings ("30 min", "1 hr 15 min", "1 hour")
 * to ISO 8601 durations ("PT30M", "PT1H15M"). Returns undefined when
 * the input doesn't match anything we recognize — the schema field
 * stays unset rather than reporting a wrong duration.
 */
export function parseDurationToIso(input: string | undefined): string | undefined {
  if (!input) return undefined;
  const lower = input.toLowerCase();
  let hours = 0;
  let minutes = 0;
  const hourMatch = lower.match(/(\d+(?:\.\d+)?)\s*(?:h|hr|hrs|hour|hours)/);
  const minMatch = lower.match(/(\d+(?:\.\d+)?)\s*(?:m|min|mins|minute|minutes)/);
  if (hourMatch) hours = parseFloat(hourMatch[1]);
  if (minMatch) minutes = parseFloat(minMatch[1]);
  if (!hourMatch && !minMatch) {
    // bare integer — treat as minutes
    const bare = lower.match(/^\s*(\d+(?:\.\d+)?)\s*$/);
    if (bare) minutes = parseFloat(bare[1]);
  }
  if (!hours && !minutes) return undefined;
  let out = "PT";
  if (hours) out += `${Math.round(hours)}H`;
  if (minutes) out += `${Math.round(minutes)}M`;
  return out;
}

/**
 * Convert "Serves 4" / "Yields 12" / "4" to a recipeYield value.
 * Schema.org accepts a free-form string here, so we lightly normalize.
 */
export function parseYield(meta: { serves?: string; yields?: string } | undefined): string | undefined {
  if (!meta) return undefined;
  return meta.serves ?? meta.yields ?? undefined;
}

/**
 * Combine an ingredient's quantity / name / note into a single
 * recipeIngredient string (Schema.org expects strings, not structured
 * objects, for this field).
 */
export function ingredientToString(ing: Ingredient): string {
  const parts: string[] = [];
  if (ing.quantity) parts.push(ing.quantity);
  parts.push(ing.name);
  if (ing.note) parts.push(`(${ing.note})`);
  return parts.join(" ");
}

/**
 * Strip the "By " prefix some bylines carry ("By J.D.H." → "J.D.H.").
 * Returns the canonical brand name when no byline is supplied so the
 * Author field is never empty (Article schema requires it).
 */
export function normalizeAuthor(byline: string | undefined): string {
  if (!byline) return BRAND_NAME;
  return byline.replace(/^by\s+/i, "").trim() || BRAND_NAME;
}

/**
 * Parse a price string like "$95", "$1,400", or "$1,400–$1,800" into
 * a structured representation suitable for an Offer or AggregateOffer.
 * Returns `null` when nothing parseable is present (caller should
 * skip the offers field rather than emit invalid data).
 */
export function parsePriceRange(
  input: string | undefined
):
  | { kind: "single"; price: number }
  | { kind: "range"; lowPrice: number; highPrice: number }
  | null {
  if (!input) return null;
  const cleaned = input.replace(/[$,\s]/g, "");
  // en/em dash, hyphen, or "to" all valid range separators
  const rangeMatch = cleaned.match(/^([\d.]+)[–—-](?:[\s]*)([\d.]+)$/);
  if (rangeMatch) {
    const lo = parseFloat(rangeMatch[1]);
    const hi = parseFloat(rangeMatch[2]);
    if (Number.isFinite(lo) && Number.isFinite(hi)) {
      return { kind: "range", lowPrice: lo, highPrice: hi };
    }
  }
  const singleMatch = cleaned.match(/^([\d.]+)$/);
  if (singleMatch) {
    const p = parseFloat(singleMatch[1]);
    if (Number.isFinite(p)) return { kind: "single", price: p };
  }
  return null;
}

/* ---------- Root schemas ---------- */

/**
 * Organization schema — the publishing entity. Emitted once at root
 * (layout) so Google can connect every page to a single business
 * identity.
 */
export function organizationSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "Organization",
    name: BRAND_NAME,
    url: SITE,
    logo: {
      "@type": "ImageObject",
      url: LOGO_URL,
    },
    sameAs: [
      // Add social profile URLs as they come online (Instagram,
      // Pinterest, etc.). Each one strengthens entity recognition.
    ],
  };
}

/**
 * WebSite schema with SitelinksSearchBox potentialAction. Google may
 * surface a search box directly in branded SERPs when it trusts the
 * action's URL pattern. The site has /search wired (SiteSearch
 * component) so this is real, not aspirational.
 */
export function websiteSchema() {
  return {
    "@context": "https://schema.org",
    "@type": "WebSite",
    name: BRAND_NAME,
    url: SITE,
    publisher: {
      "@type": "Organization",
      name: BRAND_NAME,
    },
    potentialAction: {
      "@type": "SearchAction",
      target: {
        "@type": "EntryPoint",
        urlTemplate: `${SITE}/search?q={search_term_string}`,
      },
      "query-input": "required name=search_term_string",
    },
  };
}

/* ---------- Article schema ---------- */

type ArticleSchemaInput = {
  /** Path or absolute URL of the canonical article page. */
  url: string;
  headline: string;
  description?: string;
  /** ISO 8601 (e.g., "2026-04-15"). Optional — Article works without. */
  datePublished?: string;
  /** Plain text — "By J.D.H." style byline. */
  byline?: string;
  /** Optional path or URL to a representative image. */
  image?: string;
  /** Schema.org @type — defaults to Article; pass "BlogPosting" for
   *  pillar articles if Google starts treating that as more
   *  appropriate. Article is the safe default. */
  type?: "Article" | "BlogPosting";
};

export function articleSchema({
  url,
  headline,
  description,
  datePublished,
  byline,
  image,
  type = "Article",
}: ArticleSchemaInput) {
  const author = normalizeAuthor(byline);
  return {
    "@context": "https://schema.org",
    "@type": type,
    headline,
    ...(description ? { description } : {}),
    ...(datePublished ? { datePublished } : {}),
    author: {
      "@type": "Person",
      name: author,
    },
    publisher: {
      "@type": "Organization",
      name: BRAND_NAME,
      logo: {
        "@type": "ImageObject",
        url: LOGO_URL,
      },
    },
    ...(image ? { image: absoluteUrl(image) } : {}),
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": absoluteUrl(url),
    },
  };
}

/* ---------- Recipe schema ---------- */

type RecipeSchemaInput = {
  url: string;
  recipe: Recipe;
  /** One-line description used in metadata. */
  description?: string;
};

export function recipeSchema({ url, recipe, description }: RecipeSchemaInput) {
  const totalTime = parseDurationToIso(recipe.meta?.time);
  const recipeYield = parseYield(recipe.meta);
  const author = normalizeAuthor(recipe.byline);

  return {
    "@context": "https://schema.org",
    "@type": "Recipe",
    name: recipe.title,
    ...(description ? { description } : recipe.opening ? { description: recipe.opening } : {}),
    author: {
      "@type": "Person",
      name: author,
    },
    publisher: {
      "@type": "Organization",
      name: BRAND_NAME,
      logo: {
        "@type": "ImageObject",
        url: LOGO_URL,
      },
    },
    image: recipe.image?.src ? absoluteUrl(recipe.image.src) : FALLBACK_IMAGE,
    ...(totalTime ? { totalTime } : {}),
    ...(recipeYield ? { recipeYield } : {}),
    recipeIngredient: recipe.ingredients.map(ingredientToString),
    recipeInstructions: recipe.method.map((step, i) => ({
      "@type": "HowToStep",
      position: i + 1,
      text: step,
    })),
    mainEntityOfPage: {
      "@type": "WebPage",
      "@id": absoluteUrl(url),
    },
  };
}

/* ---------- Product schema ---------- */

type ProductSchemaInput = {
  url: string;
  product: ShopProduct;
};

export function productSchema({ url, product }: ProductSchemaInput) {
  // Schema uses the curated `priceRange` rather than the live fetch.
  // Reasoning: the live fetch can fail or briefly drift; the curated
  // priceRange is "last known good" and Jordan's editorial source of
  // truth. Structured data should never be wrong, even if it's a few
  // dollars stale. Single value → Offer; range → AggregateOffer.
  let offers: object | undefined;
  const parsed = parsePriceRange(product.priceRange);
  if (parsed?.kind === "single") {
    offers = {
      "@type": "Offer",
      price: parsed.price.toFixed(2),
      priceCurrency: "USD",
      url: product.url,
      availability: "https://schema.org/InStock",
    };
  } else if (parsed?.kind === "range") {
    offers = {
      "@type": "AggregateOffer",
      lowPrice: parsed.lowPrice.toFixed(2),
      highPrice: parsed.highPrice.toFixed(2),
      priceCurrency: "USD",
      offerCount: 1,
      url: product.url,
      availability: "https://schema.org/InStock",
    };
  }

  return {
    "@context": "https://schema.org",
    "@type": "Product",
    name: product.name,
    description: product.reason,
    brand: {
      "@type": "Brand",
      name: product.brand,
    },
    category: product.category,
    image: absoluteUrl(product.image),
    url: absoluteUrl(url),
    ...(offers ? { offers } : {}),
  };
}
