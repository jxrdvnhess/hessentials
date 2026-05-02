/**
 * Shop import — writer for src/data/shop.ts.
 *
 * The data file is hand-curated TypeScript, not JSON. We preserve that
 * shape: the new entry is appended to `SHOP_PRODUCTS` as a formatted
 * object literal, slotted in just before the array's closing `];`.
 *
 * Design choices:
 *   - text-based insertion, not AST rewrite. Cheaper, no dependency,
 *     and the data file's shape is stable enough that anchor matching
 *     is reliable. The anchor is the literal `\n];\n\nexport function`
 *     that follows the SHOP_PRODUCTS array — there's only one in the
 *     file.
 *   - `reason` is written as `""` and the `// REASON` comment marker
 *     is dropped onto the line. Editorial copy is Jordan's; this file
 *     just lays the wiring.
 *   - `category` is required by the type, so the caller MUST pass one.
 *     The extractor doesn't guess.
 *   - `priceFloor` is optional and omitted when zero/undefined.
 */

import fs from "node:fs/promises";
import path from "node:path";
import type {
  ShopCategory,
  ExtractionMethod,
  Subcategory,
} from "../../data/shop";

export type NewShopEntry = {
  slug: string;
  name: string;
  brand: string;
  category: ShopCategory;
  /**
   * Two-level taxonomy leaf. Optional only during the migration
   * window — new imports should always carry one.
   */
  subcategory?: Subcategory;
  /** Editorial — left blank by default. */
  reason?: string;
  priceRange: string;
  url: string;
  /** Pre-resolved /shop/<slug>-N.jpg paths, primary first. */
  images: string[];
  extractionMethod: ExtractionMethod;
  htmlPriceSelector?: string;
  priceFloor?: number;
};

const SHOP_FILE = path.join(process.cwd(), "src", "data", "shop.ts");

/** TypeScript-string-literal escape — keeps quotes and backslashes safe. */
function tsString(value: string): string {
  return `"${value.replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"`;
}

/** Render the new entry as the same shape as the existing entries. */
export function formatEntry(entry: NewShopEntry): string {
  const lines: string[] = ["  {"];
  lines.push(`    slug: ${tsString(entry.slug)},`);
  lines.push(`    name: ${tsString(entry.name)},`);
  lines.push(`    brand: ${tsString(entry.brand)},`);
  lines.push(`    category: ${tsString(entry.category)},`);
  if (entry.subcategory && entry.subcategory.trim().length > 0) {
    lines.push(`    subcategory: ${tsString(entry.subcategory.trim())},`);
  }
  // Reason is left empty by the import flow and filled in editorially.
  // When empty, drop a TODO marker so the next pass spots it; once
  // filled, the line is clean.
  const reason = entry.reason ?? "";
  lines.push(
    reason.trim().length === 0
      ? `    reason: ${tsString(reason)}, // TODO: editorial reason`
      : `    reason: ${tsString(reason)},`
  );
  lines.push(`    priceRange: ${tsString(entry.priceRange)},`);
  lines.push(`    url: ${tsString(entry.url)},`);

  const primary = entry.images[0] ?? "";
  lines.push(`    image: ${tsString(primary)},`);
  if (entry.images.length > 1) {
    lines.push(`    images: [`);
    for (const img of entry.images) {
      lines.push(`      ${tsString(img)},`);
    }
    lines.push(`    ],`);
  }
  lines.push(`    extractionMethod: ${tsString(entry.extractionMethod)},`);
  if (entry.extractionMethod === "html" && entry.htmlPriceSelector) {
    lines.push(
      `    htmlPriceSelector: ${tsString(entry.htmlPriceSelector)},`
    );
  }
  if (typeof entry.priceFloor === "number" && entry.priceFloor > 0) {
    lines.push(`    priceFloor: ${entry.priceFloor},`);
  }
  lines.push(`  },`);
  return lines.join("\n");
}

/**
 * Read the existing slugs out of the source file. Used by the caller
 * to ensure uniqueness before formatting an entry.
 *
 * Naive regex — relies on the curated style of the data file. The
 * authoritative validator is the TS compiler at build time.
 */
export async function readExistingSlugs(): Promise<Set<string>> {
  const source = await fs.readFile(SHOP_FILE, "utf8");
  const slugs = new Set<string>();
  const re = /^\s*slug:\s*"([^"]+)"/gm;
  let m: RegExpExecArray | null;
  while ((m = re.exec(source)) !== null) {
    slugs.add(m[1]);
  }
  return slugs;
}

/**
 * Append the entry to SHOP_PRODUCTS in src/data/shop.ts.
 *
 * Anchor: the closing `\n];\n\nexport function getProductBySlug` that
 * follows SHOP_PRODUCTS. We assert the anchor matches exactly once —
 * if the file shape changes upstream, this throws loudly rather than
 * silently inserting at the wrong place.
 */
export async function appendShopEntry(entry: NewShopEntry): Promise<void> {
  const source = await fs.readFile(SHOP_FILE, "utf8");
  const ANCHOR = "\n];\n\nexport function getProductBySlug";
  const idx = source.indexOf(ANCHOR);
  if (idx === -1) {
    throw new Error(
      "shop.ts anchor not found — has the file been restructured?"
    );
  }
  if (source.indexOf(ANCHOR, idx + 1) !== -1) {
    throw new Error(
      "shop.ts anchor matched more than once — refusing to write."
    );
  }

  const block = formatEntry(entry);
  const before = source.slice(0, idx);
  const after = source.slice(idx);
  const next = `${before}\n${block}${after}`;
  await fs.writeFile(SHOP_FILE, next, "utf8");
}

/**
 * Find the start/end line indices of an entry block in shop.ts by slug.
 *
 * Each entry is a multi-line object literal:
 *
 *     ␣␣{
 *     ␣␣␣␣slug: "X",
 *     ␣␣␣␣...
 *     ␣␣},
 *
 * The walk: locate the line `␣␣␣␣slug: "<target>",`, walk backward for
 * the nearest `␣␣{`, walk forward for the nearest `␣␣},`. Returns line
 * indices into the split-by-newline array, both inclusive. Caller is
 * expected to splice on those indices.
 */
function escapeRegExp(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function locateBlockLines(
  lines: string[],
  slug: string
): { start: number; end: number } | null {
  const slugLine = `    slug: "${slug}",`;
  let slugIdx = -1;
  for (let i = 0; i < lines.length; i += 1) {
    if (lines[i] === slugLine) {
      if (slugIdx !== -1) return null; // duplicate — refuse
      slugIdx = i;
    }
  }
  if (slugIdx === -1) {
    // Fallback to a tolerant regex match in case quoting differs (e.g.
    // a slug containing characters that aren't in the strict literal).
    const re = new RegExp(`^\\s+slug:\\s*"${escapeRegExp(slug)}",?\\s*$`);
    for (let i = 0; i < lines.length; i += 1) {
      if (re.test(lines[i])) {
        if (slugIdx !== -1) return null;
        slugIdx = i;
      }
    }
  }
  if (slugIdx === -1) return null;

  let start = -1;
  for (let i = slugIdx - 1; i >= 0; i -= 1) {
    if (lines[i] === "  {") {
      start = i;
      break;
    }
    // If we walked past another entry's closing line, the file is malformed.
    if (lines[i] === "  },") return null;
  }
  if (start === -1) return null;

  let end = -1;
  for (let i = slugIdx + 1; i < lines.length; i += 1) {
    if (lines[i] === "  },") {
      end = i;
      break;
    }
    if (lines[i] === "  {") return null;
  }
  if (end === -1) return null;

  return { start, end };
}

/**
 * Read the current saved values for one product directly from shop.ts.
 *
 * The runtime SHOP_PRODUCTS array is the source of truth for read paths,
 * but routes that mutate the file want to confirm the entry exists in
 * the source before staging a write. This is a thin presence check.
 */
export async function entryExists(slug: string): Promise<boolean> {
  const source = await fs.readFile(SHOP_FILE, "utf8");
  const lines = source.split("\n");
  return locateBlockLines(lines, slug) !== null;
}

/**
 * Replace the entry for `slug` with a freshly formatted block. Throws
 * if the slug isn't found, or is found more than once. The replacement
 * may carry a different slug — useful for renames, but the caller is
 * responsible for image-path consistency.
 */
export async function replaceShopEntry(
  slug: string,
  next: NewShopEntry
): Promise<void> {
  const source = await fs.readFile(SHOP_FILE, "utf8");
  const lines = source.split("\n");
  const range = locateBlockLines(lines, slug);
  if (!range) {
    throw new Error(`shop.ts: no entry for slug "${slug}" (or duplicate).`);
  }
  const block = formatEntry(next).split("\n");
  const out = [
    ...lines.slice(0, range.start),
    ...block,
    ...lines.slice(range.end + 1),
  ].join("\n");
  await fs.writeFile(SHOP_FILE, out, "utf8");
}

/**
 * Remove the entry for `slug` from SHOP_PRODUCTS. Caller is responsible
 * for separately deleting the entry's images from /public/shop.
 */
export async function deleteShopEntry(slug: string): Promise<void> {
  const source = await fs.readFile(SHOP_FILE, "utf8");
  const lines = source.split("\n");
  const range = locateBlockLines(lines, slug);
  if (!range) {
    throw new Error(`shop.ts: no entry for slug "${slug}" (or duplicate).`);
  }
  const out = [
    ...lines.slice(0, range.start),
    ...lines.slice(range.end + 1),
  ].join("\n");
  await fs.writeFile(SHOP_FILE, out, "utf8");
}
