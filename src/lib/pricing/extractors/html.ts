import type { ExtractedPrice } from "../types";

/**
 * HTML / CSS-selector extractor — the fallback of last resort.
 *
 * Used only when JSON-LD is missing or unparseable AND the source is
 * not on a platform we know how to query (Shopify). Each product that
 * relies on this method must declare a `htmlPriceSelector` — a CSS
 * selector pointing at the element that contains the displayed price.
 *
 * Selectors break when the source site changes its markup. The admin
 * surface flags failed extractions so Jordan can update the selector
 * (or migrate to a more robust method) without the price quietly
 * going stale.
 *
 * No availability detection here — assume in stock unless a future
 * extension adds a soldOutSelector.
 */

/**
 * Find the first match for a CSS selector in raw HTML. Implemented
 * without a DOM parser to keep the bundle small — Hessentials Shop is
 * tiny, and a regex-based attribute selector works for the kinds of
 * markup we'd ever target with this fallback.
 *
 * Supports:
 *   tagname[attr="value"]
 *   tagname.class
 *   .class
 *   #id
 *
 * Anything fancier should switch to a real parser. By design the HTML
 * extractor is meant to handle a handful of edge cases, not be a
 * general-purpose scraping framework.
 */
function findFirstSelector(html: string, selector: string): string | null {
  const trimmed = selector.trim();

  // #id
  const idMatch = trimmed.match(/^#([\w-]+)$/);
  if (idMatch) {
    const re = new RegExp(
      `<([a-z0-9]+)[^>]*\\sid=["']${idMatch[1]}["'][^>]*>([\\s\\S]*?)</\\1>`,
      "i"
    );
    return html.match(re)?.[2] ?? null;
  }

  // .class (matches class attribute containing this token)
  const classMatch = trimmed.match(/^\.([\w-]+)$/);
  if (classMatch) {
    const re = new RegExp(
      `<([a-z0-9]+)[^>]*\\sclass=["'][^"']*\\b${classMatch[1]}\\b[^"']*["'][^>]*>([\\s\\S]*?)</\\1>`,
      "i"
    );
    return html.match(re)?.[2] ?? null;
  }

  // tag.class
  const tagClassMatch = trimmed.match(/^([a-z0-9]+)\.([\w-]+)$/i);
  if (tagClassMatch) {
    const [, tag, cls] = tagClassMatch;
    const re = new RegExp(
      `<${tag}[^>]*\\sclass=["'][^"']*\\b${cls}\\b[^"']*["'][^>]*>([\\s\\S]*?)</${tag}>`,
      "i"
    );
    return html.match(re)?.[1] ?? null;
  }

  // tag[attr="value"]
  const attrMatch = trimmed.match(
    /^([a-z0-9]+)\[([\w-]+)=["']([^"']+)["']\]$/i
  );
  if (attrMatch) {
    const [, tag, attr, value] = attrMatch;
    const re = new RegExp(
      `<${tag}[^>]*\\s${attr}=["']${value}["'][^>]*>([\\s\\S]*?)</${tag}>`,
      "i"
    );
    return html.match(re)?.[1] ?? null;
  }

  throw new Error(
    `htmlPriceSelector "${selector}" uses an unsupported pattern. ` +
      `Use #id, .class, tag.class, or tag[attr="value"].`
  );
}

/** Strip tags and decode the small set of entities most pricing
 *  blocks actually contain. Returns trimmed text. */
function stripTags(snippet: string): string {
  return snippet
    .replace(/<[^>]+>/g, " ")
    .replace(/&nbsp;/g, " ")
    .replace(/&amp;/g, "&")
    .replace(/&#x?[\da-f]+;/gi, "")
    .replace(/\s+/g, " ")
    .trim();
}

/** Pull every USD-style number out of a piece of text. */
function readPrices(text: string): number[] {
  const matches = text.match(/\$\s*[\d,]+(?:\.\d{2})?/g) ?? [];
  return matches
    .map((m) => Number(m.replace(/[^0-9.]/g, "")))
    .filter((n) => Number.isFinite(n) && n > 0);
}

export async function extractHtml(
  url: string,
  selector: string
): Promise<ExtractedPrice> {
  const res = await fetch(url, {
    headers: {
      "User-Agent":
        "Mozilla/5.0 (compatible; HessentialsBot/1.0; +https://hessentials.co)",
      Accept: "text/html,application/xhtml+xml",
    },
    next: { revalidate: 43200 },
    // Hard 4s ceiling — see jsonLd extractor for rationale.
    signal: AbortSignal.timeout(4000),
  });
  if (!res.ok) {
    throw new Error(`Source HTTP ${res.status}`);
  }
  const html = await res.text();
  const inner = findFirstSelector(html, selector);
  if (inner === null) {
    throw new Error(`Selector "${selector}" matched nothing`);
  }
  const text = stripTags(inner);
  const prices = readPrices(text);
  if (!prices.length) {
    throw new Error(
      `Selector "${selector}" matched, but no USD price found inside`
    );
  }
  const cleaned = Array.from(new Set(prices)).sort((a, b) => a - b);
  return { variants: cleaned, soldOut: false };
}
