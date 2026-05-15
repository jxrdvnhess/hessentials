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
  /**
   * Cross-pillar audience tags. Empty array elides the field entirely.
   * Single-value arrays render as `audience: ["mens"]`.
   */
  audience?: ("mens" | "womens")[];
  /**
   * ISO timestamp written verbatim to the entry. Caller is expected
   * to set this to `new Date().toISOString()` on fresh imports;
   * preserved as-is when an existing entry is replaced (so re-saving
   * a product through the edit form doesn't change its added date).
   */
  dateAdded?: string;
  /** Editorial — left blank by default. */
  reason?: string;
  priceRange: string;
  url: string;
  /** Pre-resolved /shop/<slug>-N.jpg paths, primary first. */
  images: string[];
  extractionMethod: ExtractionMethod;
  htmlPriceSelector?: string;
  priceFloor?: number;
  /**
   * Staging flag for the bulk-import flow. When `true`, the entry is
   * held back from public read paths until promoted via the drafts
   * admin. Omitted / `false` for live entries.
   */
  draft?: boolean;
  /**
   * Operational stability tier (1-4) — see `data/sourcing-policy.md`.
   * Optional; emitted only when set.
   */
  stabilityTier?: 1 | 2 | 3 | 4;
  /**
   * Atmosphere collections this object belongs to. Emitted as a
   * literal array when non-empty.
   */
  atmosphereCollection?: string[];
  /**
   * Tier 1 emotional territory (short phrase). Emitted as a string
   * when present.
   */
  territoryWeather?: string;
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
  if (entry.audience && entry.audience.length > 0) {
    // Render as a literal array — order preserved as passed in.
    const items = entry.audience.map((a) => tsString(a)).join(", ");
    lines.push(`    audience: [${items}],`);
  }
  if (entry.dateAdded && entry.dateAdded.trim().length > 0) {
    lines.push(`    dateAdded: ${tsString(entry.dateAdded.trim())},`);
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
  if (entry.draft === true) {
    lines.push(`    draft: true,`);
  }
  if (
    typeof entry.stabilityTier === "number" &&
    entry.stabilityTier >= 1 &&
    entry.stabilityTier <= 4
  ) {
    lines.push(`    stabilityTier: ${entry.stabilityTier},`);
  }
  if (entry.atmosphereCollection && entry.atmosphereCollection.length > 0) {
    const items = entry.atmosphereCollection
      .map((a) => tsString(a))
      .join(", ");
    lines.push(`    atmosphereCollection: [${items}],`);
  }
  if (entry.territoryWeather && entry.territoryWeather.trim().length > 0) {
    lines.push(`    territoryWeather: ${tsString(entry.territoryWeather.trim())},`);
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
 * Anchor: the literal `\n];\n` that closes SHOP_PRODUCTS. The data
 * file has exactly one such line (verified by the duplicate-match
 * guard below). Keying on just the array close — rather than on
 * what comes after it — keeps the writer robust to comment edits
 * on the downstream `getProductBySlug` export.
 */
export async function appendShopEntry(entry: NewShopEntry): Promise<void> {
  const source = await fs.readFile(SHOP_FILE, "utf8");
  const ANCHOR = "\n];\n";
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

/**
 * Flip the `draft` flag on a single entry without re-rendering the
 * surrounding block. Used by /admin/shop-drafts — promoting an entry
 * is conceptually a single-field edit, not a full PATCH, and a
 * surgical edit preserves any manual touches the entry has accrued
 * (whitespace, ordering, optional fields).
 *
 *   - `next === true`  → ensure `    draft: true,` is present just before
 *     the closing `  },`. Idempotent.
 *   - `next === false` → remove the existing `    draft: true,` line if
 *     present. Idempotent.
 *
 * Throws if the slug isn't found, or is found more than once.
 */
export async function setDraftFlag(
  slug: string,
  next: boolean
): Promise<void> {
  const source = await fs.readFile(SHOP_FILE, "utf8");
  const lines = source.split("\n");
  const range = locateBlockLines(lines, slug);
  if (!range) {
    throw new Error(`shop.ts: no entry for slug "${slug}" (or duplicate).`);
  }

  const draftLine = "    draft: true,";
  const existingDraftIdx = lines
    .slice(range.start, range.end + 1)
    .findIndex((l) => /^\s*draft:\s*true,?\s*$/.test(l));

  if (next === true) {
    if (existingDraftIdx !== -1) return; // already true
    // Insert right before the closing `  },` line.
    const insertAt = range.end;
    const out = [
      ...lines.slice(0, insertAt),
      draftLine,
      ...lines.slice(insertAt),
    ].join("\n");
    await fs.writeFile(SHOP_FILE, out, "utf8");
    return;
  }

  // next === false → remove the draft line if present.
  if (existingDraftIdx === -1) return;
  const absoluteIdx = range.start + existingDraftIdx;
  const out = [
    ...lines.slice(0, absoluteIdx),
    ...lines.slice(absoluteIdx + 1),
  ].join("\n");
  await fs.writeFile(SHOP_FILE, out, "utf8");
}
