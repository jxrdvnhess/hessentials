#!/usr/bin/env node
/**
 * Hessentials Shop — bulk import from editorial audit.
 *
 * Walks `data/shop-import-master.csv` (Chateau's audit), and for every row:
 *
 *   1. EDITORIAL REMOVAL — DIRECT URL is literally "REMOVE FROM ARTICLE".
 *      Restraint is a feature. No staging. Logged for article-body edits.
 *
 *   2. FAILED — scrape returns 404 / 403 / 410 / 429 / 5xx, or never emits
 *      a parsed result. Not staged. Logged with error.
 *
 *   3. NEEDS HUMAN — scrape succeeded but the row falls below the bar
 *      (fewer than 3 images, mangled name + no guess, empty prices,
 *      or Chateau's Thoughts is `[DRAFT, NEEDS CHATEAU REVIEW]`).
 *      Held back from shop.ts; written to `data/shop-import-pending.json`.
 *
 *   4. STAGED-DRAFT — everything clean. Entry appended to
 *      `src/data/shop.ts` with `draft: true`. Awaiting promotion via
 *      `/admin/shop-drafts`. Images saved content-addressed under
 *      `public/shop/<slug>/<sha1>.jpg`.
 *
 * The CSV is the source of truth. The scraper provides images + prices;
 * everything editorial (brand, reason) comes from the CSV verbatim.
 *
 *   USAGE
 *     node scripts/shop-bulk-import.mjs                   # dry-run
 *     node scripts/shop-bulk-import.mjs --commit          # actually write
 *     node scripts/shop-bulk-import.mjs --csv=path        # alt CSV path
 *     node scripts/shop-bulk-import.mjs --row=42          # one row only
 *     node scripts/shop-bulk-import.mjs --no-git          # skip per-row commits
 *
 * Dry-run is the default. No file writes, no image downloads, no git
 * commits. The JSON report and stdout summary describe what *would* happen.
 *
 * See `cowork-bulk-import-brief.md` and `Hessentials_Shop_Editorial_Standard`
 * for the editorial logic this implements.
 */

import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

// ----------------------------------------------------------------------
// CLI argument parsing
// ----------------------------------------------------------------------

const __filename = fileURLToPath(import.meta.url);
const REPO_ROOT = path.resolve(path.dirname(__filename), "..");

function parseArgs(argv) {
  const args = {
    commit: false,
    csv: path.join(REPO_ROOT, "data", "shop-import-master.csv"),
    row: null,
    git: true,
    retryFailed: false,
    retryThin: false,
    emitChateau: false,
    cleanDuplicates: false,
  };
  for (const raw of argv.slice(2)) {
    if (raw === "--commit") args.commit = true;
    else if (raw === "--no-git") args.git = false;
    else if (raw === "--retry-failed") args.retryFailed = true;
    else if (raw === "--retry-thin") args.retryThin = true;
    else if (raw === "--emit-chateau") args.emitChateau = true;
    else if (raw === "--clean-duplicates") args.cleanDuplicates = true;
    else if (raw.startsWith("--csv=")) args.csv = path.resolve(raw.slice(6));
    else if (raw.startsWith("--row=")) args.row = Number(raw.slice(6));
    else if (raw === "-h" || raw === "--help") {
      console.log(
        "Usage:\n" +
          "  node scripts/shop-bulk-import.mjs [--commit] [--csv=path] [--row=N] [--no-git]\n" +
          "  node scripts/shop-bulk-import.mjs --retry-failed [--commit]\n" +
          "  node scripts/shop-bulk-import.mjs --retry-thin [--commit]\n" +
          "  node scripts/shop-bulk-import.mjs --emit-chateau\n" +
          "\n" +
          "  --retry-failed     Re-scrape previous failed rows via Playwright Chromium.\n" +
          "                     Excludes 404/410 — those are editorial, not scrape.\n" +
          "                     Requires:\n" +
          "                       npm install --save-dev playwright\n" +
          "                       npx playwright install chromium\n" +
          "  --retry-thin       Re-scrape previous needs-human rows whose only\n" +
          "                     blocker was image count (\"only N image(s)\"). Uses\n" +
          "                     the same Playwright path; the DOM image-fallback\n" +
          "                     can often raise the count past the staging gate.\n" +
          "  --emit-chateau     Re-emit data/shop-import-needs-chateau.md from the\n" +
          "                     existing report without re-scraping.\n" +
          "  --clean-duplicates Find draft entries that share a URL with another\n" +
          "                     draft (suffixed -2/-3/...) and remove the\n" +
          "                     suffixed copies. Deletes their image dirs too.\n" +
          "                     Dry-run by default; --commit to apply."
      );
      process.exit(0);
    }
  }
  return args;
}

const ARGS = parseArgs(process.argv);

// ----------------------------------------------------------------------
// Constants
// ----------------------------------------------------------------------

const SHOP_FILE = path.join(REPO_ROOT, "src", "data", "shop.ts");
const PENDING_FILE = path.join(REPO_ROOT, "data", "shop-import-pending.json");
/**
 * Report files are split by mode to keep dry-runs from corrupting
 * commit-mode state. `REPORT_FILE` is the canonical record of the
 * last live run (read by retry + --emit-chateau); the dry-run file
 * is purely informational.
 */
const REPORT_FILE = path.join(REPO_ROOT, "data", "shop-bulk-import-report.json");
const REPORT_DRYRUN_FILE = path.join(
  REPO_ROOT,
  "data",
  "shop-bulk-import-report.dryrun.json"
);
const CHATEAU_FILE = path.join(REPO_ROOT, "data", "shop-import-needs-chateau.md");

/**
 * Read the canonical (commit-mode) report; fall back to the dry-run
 * one when no commit run has happened yet. Used by retry and
 * --emit-chateau, which need the most authoritative snapshot of state.
 */
async function readReportPreferringCommit() {
  try {
    return JSON.parse(await fs.readFile(REPORT_FILE, "utf8"));
  } catch {
    try {
      return JSON.parse(await fs.readFile(REPORT_DRYRUN_FILE, "utf8"));
    } catch {
      return null;
    }
  }
}
const PUBLIC_SHOP_DIR = path.join(REPO_ROOT, "public", "shop");

const FETCH_UA =
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36";

const EDITORIAL_REMOVAL_MARKER = /^\s*REMOVE\s+FROM\s+ARTICLE\s*$/i;
// The brief described the prefix as `[DRAFT, NEEDS CHATEAU REVIEW]` in
// Chateau's Thoughts. Chateau's finished audit uses `FLAG FOR JORDAN:`
// in the `audit_note (context)` column for the same intent — route the
// row to NEEDS HUMAN. Match either signal in either column.
const DRAFT_REVIEW_PREFIX = /^\s*\[DRAFT,\s*NEEDS\s+CHATEAU\s+REVIEW\]/i;
const AUDIT_FLAG_PREFIX = /^\s*FLAG\s+FOR\s+JORDAN:/i;

const VOICE_BANNED = [
  { needle: /\bmust-have\b/i, label: "must-have" },
  { needle: /\bperfect for\b/i, label: "perfect for" },
  { needle: /\belevate your\b/i, label: "elevate your" },
  { needle: /\bobsessed with\b/i, label: "obsessed with" },
  { needle: /\bluxury essential\b/i, label: "luxury essential" },
  { needle: /\binvestment piece\b/i, label: "investment piece" },
  { needle: /!/, label: "exclamation point" },
  { needle: /—/, label: "em dash" },
];

// ----------------------------------------------------------------------
// CSV parser — quoted-field handling, doubled-quote escapes.
// ----------------------------------------------------------------------

function parseCsv(source) {
  // Strip BOM if present.
  if (source.charCodeAt(0) === 0xfeff) source = source.slice(1);

  const rows = [];
  let field = "";
  let row = [];
  let inQuotes = false;

  for (let i = 0; i < source.length; i += 1) {
    const c = source[i];
    if (inQuotes) {
      if (c === '"') {
        if (source[i + 1] === '"') {
          field += '"';
          i += 1;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else {
      if (c === '"') {
        inQuotes = true;
      } else if (c === ",") {
        row.push(field);
        field = "";
      } else if (c === "\n" || c === "\r") {
        if (c === "\r" && source[i + 1] === "\n") i += 1;
        row.push(field);
        rows.push(row);
        row = [];
        field = "";
      } else {
        field += c;
      }
    }
  }
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function asRecords(rows) {
  if (rows.length === 0) return [];
  const header = rows[0].map((h) => h.trim());
  const out = [];
  for (let i = 1; i < rows.length; i += 1) {
    const r = rows[i];
    if (r.length === 1 && r[0].trim() === "") continue;
    const rec = {};
    for (let j = 0; j < header.length; j += 1) {
      rec[header[j]] = (r[j] ?? "").trim();
    }
    rec.__rowIndex = i + 1; // 1-based incl. header line
    out.push(rec);
  }
  return out;
}

// ----------------------------------------------------------------------
// Slug generation — mirrors src/lib/shopImport/slug.ts
// ----------------------------------------------------------------------

const SMALL_WORDS = new Set([
  "and", "or", "the", "a", "an", "of", "for", "in", "to", "with",
]);

function kebab(input) {
  return input
    .toLowerCase()
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/&/g, " and ")
    .replace(/[^a-z0-9\s-]/g, " ")
    .trim()
    .split(/\s+/)
    .filter((w) => w.length > 0)
    .join("-")
    .replace(/-+/g, "-");
}

function buildSlug(brand, name) {
  const brandPart = kebab(brand);
  const nameWords = kebab(name).split("-").filter(Boolean);
  let nameSlug = nameWords.join("-");
  if (nameSlug.length + brandPart.length > 60 && nameWords.length > 3) {
    const trimmed = nameWords.filter(
      (w, i) =>
        i === 0 || i === nameWords.length - 1 || !SMALL_WORDS.has(w)
    );
    nameSlug = trimmed.join("-");
  }
  return [brandPart, nameSlug]
    .filter(Boolean)
    .join("-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "");
}

function ensureUnique(proposed, existing) {
  if (!existing.has(proposed)) return proposed;
  let i = 2;
  while (existing.has(`${proposed}-${i}`)) i += 1;
  return `${proposed}-${i}`;
}

// ----------------------------------------------------------------------
// Scraper — JSON-LD + OG fallback. Narrow port of extractProduct.
// ----------------------------------------------------------------------

const FETCH_TIMEOUT_MS = 12000;

function decodeHtmlEntities(s) {
  return s
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

function* extractJsonLdBlocks(html) {
  const re =
    /<script[^>]+type=["']application\/ld\+json["'][^>]*>([\s\S]*?)<\/script>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const raw = decodeHtmlEntities(m[1].trim());
    if (!raw) continue;
    try {
      yield JSON.parse(raw);
    } catch {
      // ignore
    }
  }
}

function flattenJsonLd(node, out = []) {
  if (!node) return out;
  if (Array.isArray(node)) {
    for (const n of node) flattenJsonLd(n, out);
    return out;
  }
  if (typeof node !== "object") return out;
  out.push(node);
  if (node["@graph"]) flattenJsonLd(node["@graph"], out);
  return out;
}

function isProductNode(node) {
  const t = node["@type"];
  if (!t) return false;
  if (Array.isArray(t)) return t.some((x) => /Product/i.test(String(x)));
  return /Product/i.test(String(t));
}

function pickProductNode(blocks) {
  for (const root of blocks) {
    for (const n of flattenJsonLd(root)) {
      if (isProductNode(n)) return n;
    }
  }
  return null;
}

function extractImagesFromProduct(node) {
  const img = node?.image;
  if (!img) return [];
  if (typeof img === "string") return [img];
  if (Array.isArray(img)) {
    return img
      .map((x) => (typeof x === "string" ? x : x?.url))
      .filter((x) => typeof x === "string" && x.length > 0);
  }
  if (typeof img === "object" && img?.url) return [img.url];
  return [];
}

function extractOgFromHtml(html) {
  const out = {};
  const re =
    /<meta\s+(?:property|name)=["']([^"']+)["']\s+content=["']([^"']*)["'][^>]*>/gi;
  let m;
  while ((m = re.exec(html)) !== null) {
    const k = m[1].toLowerCase();
    if (
      !out[k] &&
      (k.startsWith("og:") || k.startsWith("twitter:") || k === "description")
    ) {
      out[k] = decodeHtmlEntities(m[2]);
    }
  }
  // Multi-image og:image — capture all.
  const ogImages = [];
  const re2 =
    /<meta\s+property=["']og:image(?::secure_url)?["']\s+content=["']([^"']+)["'][^>]*>/gi;
  let m2;
  while ((m2 = re2.exec(html)) !== null) ogImages.push(decodeHtmlEntities(m2[1]));
  out.__images = Array.from(new Set(ogImages));
  return out;
}

function extractTitleTag(html) {
  const m = /<title[^>]*>([\s\S]*?)<\/title>/i.exec(html);
  return m ? decodeHtmlEntities(m[1]).trim() : "";
}

function dedupePreserveOrder(arr) {
  const seen = new Set();
  const out = [];
  for (const x of arr) {
    if (!x) continue;
    if (seen.has(x)) continue;
    seen.add(x);
    out.push(x);
  }
  return out;
}

function absolutize(base, candidate) {
  try {
    return new URL(candidate, base).toString();
  } catch {
    return null;
  }
}

function pickPricesFromProduct(node) {
  const prices = [];
  const visit = (offer) => {
    if (!offer || typeof offer !== "object") return;
    const p = offer.price ?? offer.lowPrice ?? offer.highPrice;
    if (p !== undefined && p !== null) {
      const n = Number(p);
      if (Number.isFinite(n) && n > 0) prices.push(n);
    }
    if (Array.isArray(offer.offers)) for (const o of offer.offers) visit(o);
    if (offer.offers && !Array.isArray(offer.offers)) visit(offer.offers);
  };
  if (node?.offers) visit(node.offers);
  return Array.from(new Set(prices)).sort((a, b) => a - b);
}

/**
 * Pure HTML → product extraction. No network. Used by both the
 * fetch-based scrape (raw server HTML) and the Playwright-based
 * retry (post-render DOM serialization).
 */
function extractFromHtml(html, baseUrl) {
  const blocks = Array.from(extractJsonLdBlocks(html));
  const product = pickProductNode(blocks);
  const og = extractOgFromHtml(html);
  const titleTag = extractTitleTag(html);

  let name = "";
  if (product?.name) name = String(product.name).trim();
  if (!name) name = (og["og:title"] || og["twitter:title"] || "").trim();
  if (!name) name = titleTag;

  let brand = "";
  if (product?.brand) {
    brand =
      typeof product.brand === "string"
        ? product.brand
        : product.brand?.name || "";
  }
  if (!brand) brand = (og["og:site_name"] || "").trim();

  let description = "";
  if (product?.description) description = String(product.description).trim();
  if (!description) description = (og["og:description"] || og.description || "").trim();

  const imagesFromProduct = extractImagesFromProduct(product || {});
  const imagesFromOg = og.__images || [];
  const images = dedupePreserveOrder(
    [...imagesFromProduct, ...imagesFromOg]
      .map((u) => absolutize(baseUrl, u))
      .filter(Boolean)
  );

  const prices = pickPricesFromProduct(product || {});

  return { name, brand, description, images, prices };
}

async function scrapeUrl(url) {
  let res;
  try {
    res = await fetch(url, {
      headers: { "User-Agent": FETCH_UA, Accept: "text/html,*/*" },
      redirect: "follow",
      signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
    });
  } catch (e) {
    return { ok: false, status: 0, error: `Network: ${e.message ?? e}` };
  }
  if (!res.ok) {
    return { ok: false, status: res.status, error: `Source HTTP ${res.status}` };
  }
  const html = await res.text();
  const parsed = extractFromHtml(html, url);
  return { ok: true, status: res.status, ...parsed };
}

// ----------------------------------------------------------------------
// Title-case + name cleanup
// ----------------------------------------------------------------------

function isScreamingUppercase(s) {
  if (!s) return false;
  const letters = s.replace(/[^A-Za-z]/g, "");
  if (letters.length < 8) return false;
  return letters === letters.toUpperCase();
}

const TITLE_LOWER = new Set([
  "a", "an", "and", "as", "at", "but", "by", "for", "in", "of",
  "on", "or", "the", "to", "with",
]);

function titleCase(input) {
  return input
    .toLowerCase()
    .split(/(\s+|[-/])/)
    .map((tok, i, all) => {
      if (/^\s+$/.test(tok) || tok === "-" || tok === "/") return tok;
      if (i !== 0 && i !== all.length - 1 && TITLE_LOWER.has(tok)) return tok;
      return tok.charAt(0).toUpperCase() + tok.slice(1);
    })
    .join("");
}

function stripParentheticalSize(name) {
  // "Foo Bar (3 oz)" → "Foo Bar". Drop only the trailing parenthetical
  // if it looks like a size/volume unit; keep editorial parentheticals.
  return name.replace(
    /\s*\(\s*\d[\d.,/\s]*(oz|ml|fl|g|kg|lb|in|cm|mm|"|cl)?\s*\)\s*$/i,
    ""
  );
}

function cleanName(rawName, productNameGuess) {
  let candidate = (rawName || "").trim();
  if (isScreamingUppercase(candidate) || candidate.length > 80 || !candidate) {
    const fallback = (productNameGuess || "").trim();
    if (fallback) candidate = fallback;
  }
  candidate = stripParentheticalSize(candidate);
  if (isScreamingUppercase(candidate)) candidate = titleCase(candidate);
  return candidate.trim();
}

// ----------------------------------------------------------------------
// Category + audience heuristics
// ----------------------------------------------------------------------

function proposeCategory(anchor, name) {
  const text = `${anchor} ${name}`.toLowerCase();
  const has = (...needles) => needles.some((n) => text.includes(n));

  if (
    has(
      "candle", "lamp", "mirror", "throw", "sofa", "blanket",
      "speaker", "dimmer", "dutch oven", "espresso machine",
      "espresso", "coffee", "dinnerware", "plate", "napkin",
      "tablecloth", "pot", "pan", "skillet"
    )
  ) {
    return "home";
  }
  if (has("olive oil", "salt", "vinegar", "honey")) return "provisions";
  if (
    has(
      "fragrance", "cologne", "edt", "edp", "perfume",
      "shampoo", "soap", "shaving", "deodorant", "moisturizer"
    )
  ) {
    return "grooming";
  }
  if (
    has(
      "watch", "sneaker", "loafer", "tote", "bag", "crossbody",
      "earrings", "hoops", "ring", "necklace", "wallet", "belt", "sunglasses"
    )
  ) {
    return "accessories";
  }
  if (has("luggage", "suitcase", "carry-on", "carryon")) return "travel";

  // Mens / womens last — they're broader and easier to over-match.
  if (has("women", "womens", "skirt", "dress", "blouse")) return "womens";
  if (has(" men ", " mens", "trouser", " polo")) return "mens";

  return "";
}

function proposeAudience(sourceArticle, anchor, name) {
  const article = (sourceArticle || "").toLowerCase();
  if (article.includes("style-is-not-gendered")) return "Gender-neutral";
  const text = `${anchor} ${name}`.toLowerCase();
  if (/\b(men|men's|mens)\b/.test(text)) return "Mens only";
  if (/\b(women|women's|womens)\b/.test(text)) return "Womens only";
  return "None";
}

// ----------------------------------------------------------------------
// shop.ts read / write — text-anchor insertion (mirrors writeEntry.ts)
// ----------------------------------------------------------------------

async function readShopFile() {
  return fs.readFile(SHOP_FILE, "utf8");
}

function existingSlugsFrom(source) {
  const slugs = new Set();
  const re = /^\s*slug:\s*"([^"]+)"/gm;
  let m;
  while ((m = re.exec(source)) !== null) slugs.add(m[1]);
  return slugs;
}

/**
 * Build a URL → { slug, draft } map by walking the entry blocks in
 * shop.ts. Used for URL-keyed idempotency — running the same row
 * twice must NOT create a second entry with a `-2` slug; it must
 * skip. (Two different rows whose brand+name slugify identically
 * still get `-2` via ensureUnique — that's a separate concern.)
 */
function existingUrlMapFrom(source) {
  const lines = source.split("\n");
  const map = new Map();
  let inEntry = false;
  let slug = "";
  let url = "";
  let draft = false;
  for (const line of lines) {
    if (line === "  {") {
      inEntry = true;
      slug = "";
      url = "";
      draft = false;
      continue;
    }
    if (!inEntry) continue;
    if (line === "  },") {
      if (url) map.set(url, { slug, draft });
      inEntry = false;
      continue;
    }
    const sm = /^\s*slug:\s*"([^"]+)"/.exec(line);
    if (sm) slug = sm[1];
    const um = /^\s*url:\s*"([^"]+)"/.exec(line);
    if (um) url = um[1];
    if (/^\s*draft:\s*true,?\s*$/.test(line)) draft = true;
  }
  return map;
}

function existingDraftSlugsFrom(source) {
  // Match entry blocks that contain `draft: true`. Walk by lines.
  const lines = source.split("\n");
  const drafts = new Set();
  let inEntry = false;
  let entrySlug = "";
  let entryHasDraft = false;
  for (const line of lines) {
    if (line === "  {") {
      inEntry = true;
      entrySlug = "";
      entryHasDraft = false;
      continue;
    }
    if (!inEntry) continue;
    if (line === "  },") {
      if (entrySlug && entryHasDraft) drafts.add(entrySlug);
      inEntry = false;
      continue;
    }
    const slugMatch = /^\s*slug:\s*"([^"]+)"/.exec(line);
    if (slugMatch) entrySlug = slugMatch[1];
    if (/^\s*draft:\s*true,?\s*$/.test(line)) entryHasDraft = true;
  }
  return drafts;
}

function tsString(value) {
  return `"${value.replace(/\\/g, "\\\\").replace(/"/g, '\\"')}"`;
}

function formatEntry(entry) {
  const lines = ["  {"];
  lines.push(`    slug: ${tsString(entry.slug)},`);
  lines.push(`    name: ${tsString(entry.name)},`);
  lines.push(`    brand: ${tsString(entry.brand)},`);
  lines.push(`    category: ${tsString(entry.category)},`);
  if (entry.subcategory && entry.subcategory.trim()) {
    lines.push(`    subcategory: ${tsString(entry.subcategory.trim())},`);
  }
  if (entry.audience && entry.audience.length > 0) {
    const items = entry.audience.map((a) => tsString(a)).join(", ");
    lines.push(`    audience: [${items}],`);
  }
  if (entry.dateAdded) {
    lines.push(`    dateAdded: ${tsString(entry.dateAdded)},`);
  }
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
    for (const img of entry.images) lines.push(`      ${tsString(img)},`);
    lines.push(`    ],`);
  }
  lines.push(`    extractionMethod: ${tsString(entry.extractionMethod)},`);
  if (typeof entry.priceFloor === "number" && entry.priceFloor > 0) {
    lines.push(`    priceFloor: ${entry.priceFloor},`);
  }
  if (entry.draft === true) lines.push(`    draft: true,`);
  lines.push(`  },`);
  return lines.join("\n");
}

async function appendShopEntry(entry) {
  const source = await readShopFile();
  // Anchor on the unique array-close line. Robust to comment shape
  // changes on the export functions that follow SHOP_PRODUCTS.
  const ANCHOR = "\n];\n";
  const idx = source.indexOf(ANCHOR);
  if (idx === -1) {
    throw new Error("shop.ts anchor not found — refusing to write.");
  }
  if (source.indexOf(ANCHOR, idx + 1) !== -1) {
    throw new Error("shop.ts anchor matched more than once.");
  }
  const block = formatEntry(entry);
  const next = `${source.slice(0, idx)}\n${block}${source.slice(idx)}`;
  await fs.writeFile(SHOP_FILE, next, "utf8");
}

// ----------------------------------------------------------------------
// Image saving — content-addressed under public/shop/<slug>/<sha1>.jpg
// ----------------------------------------------------------------------

let sharpLib = null;
async function ensureSharp() {
  if (sharpLib) return sharpLib;
  // Lazy — dry-run never imports it.
  sharpLib = (await import("sharp")).default;
  return sharpLib;
}

async function fetchImageBytes(url) {
  const res = await fetch(url, {
    headers: { "User-Agent": FETCH_UA, Accept: "image/*" },
    signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
  });
  if (!res.ok) throw new Error(`Image HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.byteLength < 1024) throw new Error(`Image too small (${buf.byteLength}b)`);
  return buf;
}

async function saveImagesContentAddressed(slug, sources) {
  const sharp = await ensureSharp();
  const dir = path.join(PUBLIC_SHOP_DIR, slug);
  await fs.mkdir(dir, { recursive: true });

  const saved = [];
  const failed = [];
  for (const src of sources) {
    try {
      const raw = await fetchImageBytes(src);
      const jpeg = await sharp(raw)
        .rotate()
        .flatten({ background: "#ffffff" })
        .jpeg({ quality: 88, mozjpeg: true })
        .toBuffer();
      const hash = createHash("sha1").update(jpeg).digest("hex").slice(0, 16);
      const filename = `${hash}.jpg`;
      const full = path.join(dir, filename);
      // Content-addressed → existence == identity. Skip if already there.
      if (!existsSync(full)) {
        await fs.writeFile(full, jpeg);
      }
      saved.push({ source: src, publicPath: `/shop/${slug}/${filename}` });
    } catch (e) {
      failed.push({ source: src, error: e?.message ?? String(e) });
    }
  }
  return { saved, failed };
}

// ----------------------------------------------------------------------
// Git — one commit per staged row
// ----------------------------------------------------------------------

function gitCommit(slug) {
  if (!ARGS.git) return null;
  try {
    execFileSync("git", ["add", "src/data/shop.ts", `public/shop/${slug}`], {
      cwd: REPO_ROOT,
      stdio: "ignore",
    });
    execFileSync(
      "git",
      [
        "commit",
        "-m",
        `Shop: stage draft "${slug}" from editorial audit`,
        "--no-verify",
      ],
      { cwd: REPO_ROOT, stdio: "ignore" }
    );
    const hash = execFileSync("git", ["rev-parse", "HEAD"], {
      cwd: REPO_ROOT,
      encoding: "utf8",
    }).trim();
    return hash;
  } catch (e) {
    return { error: e?.message ?? String(e) };
  }
}

// ----------------------------------------------------------------------
// Voice lint of existing entries
// ----------------------------------------------------------------------

function lintExistingShop(source) {
  const warnings = [];
  // Walk entries by anchor `  {` … `  },` blocks.
  const lines = source.split("\n");
  let inEntry = false;
  let entrySlug = "";
  let entryReason = "";
  let entryDraft = false;
  for (const line of lines) {
    if (line === "  {") {
      inEntry = true;
      entrySlug = "";
      entryReason = "";
      entryDraft = false;
      continue;
    }
    if (!inEntry) continue;
    if (line === "  },") {
      if (entryReason && !entryDraft) {
        const hits = [];
        for (const rule of VOICE_BANNED) {
          if (rule.needle.test(entryReason)) hits.push(rule.label);
        }
        if (hits.length > 0) {
          warnings.push({ slug: entrySlug, reason: entryReason, hits });
        }
      }
      inEntry = false;
      continue;
    }
    const sm = /^\s*slug:\s*"([^"]+)"/.exec(line);
    if (sm) entrySlug = sm[1];
    const rm = /^\s*reason:\s*"((?:[^"\\]|\\.)*)"/.exec(line);
    if (rm) entryReason = rm[1].replace(/\\"/g, '"').replace(/\\\\/g, "\\");
    if (/^\s*draft:\s*true,?\s*$/.test(line)) entryDraft = true;
  }
  return warnings;
}

// ----------------------------------------------------------------------
// Pending queue (NEEDS HUMAN)
// ----------------------------------------------------------------------

async function loadPending() {
  try {
    const raw = await fs.readFile(PENDING_FILE, "utf8");
    return JSON.parse(raw);
  } catch {
    return { entries: [] };
  }
}

async function savePending(data) {
  await fs.mkdir(path.dirname(PENDING_FILE), { recursive: true });
  await fs.writeFile(PENDING_FILE, JSON.stringify(data, null, 2) + "\n", "utf8");
}

// ----------------------------------------------------------------------
// Per-row dispatch
// ----------------------------------------------------------------------

function priceRangeFrom(prices) {
  if (!prices || prices.length === 0) return "";
  const fmt = (n) => {
    if (Number.isInteger(n)) return `$${n.toLocaleString("en-US")}`;
    return `$${n.toFixed(2)}`;
  };
  if (prices.length === 1) return fmt(prices[0]);
  const lo = prices[0];
  const hi = prices[prices.length - 1];
  if (lo === hi) return fmt(lo);
  return `${fmt(lo)}–${fmt(hi)}`;
}

function inferExtractionMethod(url) {
  try {
    const u = new URL(url);
    if (u.pathname.includes("/products/")) return "shopify";
  } catch {
    /* ignore */
  }
  return "json-ld";
}

async function processRow(row, ctx, scrapeFn = scrapeUrl) {
  const directUrl = (row["DIRECT PRODUCT URL FOR SALE"] ?? "").trim();
  const article = row.source_article ?? "";
  const articleUrl = row.article_url ?? "";
  const anchor = row.anchor_text ?? "";
  const brandCsv = row.brand ?? "";
  const guess = row.product_name_guess ?? "";
  const thought = row["Chateau's Thoughts"] ?? "";
  const auditNote = row["audit_note (context)"] ?? "";

  const base = {
    rowIndex: row.__rowIndex,
    sourceArticle: article,
    articleUrl,
    anchor,
    brand: brandCsv,
    directUrl,
  };

  // 1. EDITORIAL REMOVAL
  if (EDITORIAL_REMOVAL_MARKER.test(directUrl)) {
    return { ...base, bucket: "editorial-removal" };
  }

  // 1a. Flag-only rows. Chateau's audit occasionally puts a
  // `FLAG FOR JORDAN:` message in the DIRECT URL or audit_note cell
  // — the URL is unusable, but the row is not a scrape failure, it's
  // an editorial decision pending. Route to NEEDS HUMAN with the
  // flag content visible inline.
  const flagSources = [directUrl, auditNote, thought];
  const flagSignal = flagSources.find((s) => AUDIT_FLAG_PREFIX.test(s));
  if (flagSignal) {
    return {
      ...base,
      bucket: "needs-human",
      flags: [flagSignal.trim()],
      candidate: {
        slug: undefined,
        name: row.product_name_guess || row.anchor_text || "(unknown)",
        brand: brandCsv,
        category: "",
        audience: [],
        reason: thought,
        priceRange: "",
        url: /^https?:\/\//i.test(directUrl) ? directUrl : "",
        images: [],
        extractionMethod: "manual",
        proposedAudience: "None",
      },
    };
  }

  if (!directUrl || !/^https?:\/\//i.test(directUrl)) {
    return { ...base, bucket: "failed", error: "No DIRECT URL on row" };
  }

  // 2. Scrape (default: fetch-based; retry mode passes Playwright)
  const scrape = await scrapeFn(directUrl);
  if (!scrape.ok) {
    return { ...base, bucket: "failed", status: scrape.status, error: scrape.error };
  }

  // Compose candidate fields
  const name = cleanName(scrape.name, guess);
  if (!name) {
    return { ...base, bucket: "failed", error: "No product name from scrape or guess" };
  }

  const proposedSlug = buildSlug(brandCsv || scrape.brand || "", name);
  const slug = ensureUnique(proposedSlug, ctx.existingSlugs);

  const audienceLabel = proposeAudience(articleUrl, anchor, name);
  const audienceArr =
    audienceLabel === "Mens only"
      ? ["mens"]
      : audienceLabel === "Womens only"
      ? ["womens"]
      : audienceLabel === "Gender-neutral"
      ? ["mens", "womens"]
      : [];

  const category = proposeCategory(anchor, name);

  const priceRange = priceRangeFrom(scrape.prices);
  const extractionMethod = inferExtractionMethod(directUrl);

  const candidate = {
    slug,
    name,
    brand: brandCsv,
    category, // may be ""
    audience: audienceArr,
    reason: thought, // verbatim
    priceRange,
    url: directUrl,
    images: scrape.images,
    extractionMethod,
    proposedAudience: audienceLabel,
  };

  // 3. NEEDS HUMAN — apply gates
  const flags = [];
  if (scrape.images.length < 3) flags.push(`only ${scrape.images.length} image(s)`);
  if (isScreamingUppercase(scrape.name) && !guess) flags.push("mangled scraper name, no guess fallback");
  if (!scrape.prices || scrape.prices.length === 0) flags.push("empty prices");
  if (DRAFT_REVIEW_PREFIX.test(thought)) flags.push("[DRAFT, NEEDS CHATEAU REVIEW]");
  if (AUDIT_FLAG_PREFIX.test(auditNote)) flags.push(`FLAG FOR JORDAN: ${auditNote.replace(/^FLAG FOR JORDAN:\s*/i, "").trim()}`);

  if (flags.length > 0) {
    return {
      ...base,
      bucket: "needs-human",
      candidate,
      flags,
    };
  }

  return { ...base, bucket: "staged-draft", candidate };
}

// ----------------------------------------------------------------------
// Playwright-based scraper (retry mode)
// ----------------------------------------------------------------------

let playwrightLib = null;
async function ensurePlaywright() {
  if (playwrightLib) return playwrightLib;
  try {
    playwrightLib = await import("playwright");
  } catch {
    throw new Error(
      "Playwright not installed. Install with:\n" +
        "  npm install --save-dev playwright\n" +
        "  npx playwright install chromium"
    );
  }
  return playwrightLib;
}

/**
 * Build a Playwright-backed scrape function bound to a shared browser
 * context. Same return shape as `scrapeUrl` so it slots into
 * `processRow` without further changes.
 *
 * Strategy:
 *   - real Chromium with a desktop UA + viewport so anti-bot heuristics
 *     classify us as a human-driven browser (defeats most 403s)
 *   - wait for `domcontentloaded` first, then for `networkidle` with a
 *     soft timeout — most retailers finish lazy-loading product images
 *     within a couple seconds of network quiet
 *   - extract from the post-render DOM serialization, reusing the same
 *     JSON-LD + OG + title path used by the fetch-based scraper
 */
function makeBrowserScrape(browserContext) {
  return async function scrapeViaBrowser(url) {
    const page = await browserContext.newPage();
    try {
      const response = await page.goto(url, {
        waitUntil: "domcontentloaded",
        timeout: 20000,
      });
      // Some sites return 200 but redirect to a 404-flavored landing
      // page. Treat any 4xx/5xx as a fail so the bucket routing stays
      // consistent with the fetch path.
      const status = response?.status() ?? 0;
      if (status >= 400) {
        return { ok: false, status, error: `Source HTTP ${status}` };
      }
      // Best-effort wait for lazy-loaded product images. Soft timeout —
      // not all retailers ever reach true idle, but the DOM tends to be
      // complete enough by then.
      await page
        .waitForLoadState("networkidle", { timeout: 6000 })
        .catch(() => {});
      const html = await page.content();
      const parsed = extractFromHtml(html, page.url());

      // Image fallback — JSON-LD and OG often miss the actual product
      // photography (especially on retailers that use React/lazy-load
      // architectures where the structured metadata is sparse). Scan
      // the rendered DOM for product <img> tags only when we don't
      // already have enough.
      if (parsed.images.length < 3) {
        const domImages = await scanProductImagesFromDom(page);
        const absolute = domImages
          .map((u) => absolutize(page.url(), u))
          .filter(Boolean);
        parsed.images = dedupePreserveOrder([
          ...parsed.images,
          ...absolute,
        ]);
      }

      // Price fallback — same architectural shape as the image
      // fallback. JSON-LD `offers` is frequently absent on retailers
      // who render their price client-side. The DOM still has a
      // currency-formatted price string somewhere; we just have to
      // find it without picking up "Free Shipping over $50".
      if (parsed.prices.length === 0) {
        const domPrices = await scanProductPriceFromDom(page);
        parsed.prices = domPrices;
      }

      return { ok: true, status, ...parsed };
    } catch (e) {
      const msg = e?.message ?? String(e);
      // Map Playwright timeouts to a Network bucket for the report.
      const error = /Timeout|timeout/.test(msg)
        ? `Network: ${msg.split("\n")[0]}`
        : `Network: ${msg}`;
      return { ok: false, status: 0, error };
    } finally {
      await page.close().catch(() => {});
    }
  };
}

/**
 * Walk the rendered DOM for product images. Runs inside the page
 * context via `page.evaluate`, so the function body is serialized to
 * the browser — no imports / closures across the boundary.
 *
 * Heuristics, in order of priority:
 *   1. Filter out anything smaller than 200×200 (icons, sprites,
 *      tracking pixels, UI chrome).
 *   2. Walk ancestors looking for hint classes/ids — `product`,
 *      `gallery`, `hero`, `pdp`, `main-image`, `primary-image`,
 *      `product-photo`. Hits get a +1 score.
 *   3. Walk ancestors for *negative* hints — `related`, `recommended`,
 *      `cross-sell`, `nav`, `footer`, `menu`. Those entire subtrees
 *      get dropped (don't surface "people also bought" tiles).
 *   4. For each candidate, pull the highest-resolution URL from
 *      `srcset` when present — many retailers serve 400w → 1600w
 *      variants and the unaltered `src` is often the smallest.
 *   5. Sort by hint score, then by image area; cap at 8 candidates.
 *
 * Returns absolute URLs (or page-relative if currentSrc was relative
 * — caller absolutizes against the page's final URL).
 */
async function scanProductImagesFromDom(page) {
  try {
    return await page.evaluate(() => {
      const candidates = [];
      const seen = new Set();
      const POSITIVE = /\b(product|gallery|hero|pdp|main-image|primary-image|product-photo|product-image|product__media)\b/;
      const NEGATIVE = /\b(related|recommended|cross-sell|you-may|also-like|footer|nav|menu|breadcrumb|thumbnail-nav)\b/;

      function bestFromSrcset(srcset) {
        if (!srcset) return null;
        const entries = srcset.split(",").map((s) => s.trim());
        let bestUrl = null;
        let bestScore = -1;
        for (const e of entries) {
          const parts = e.split(/\s+/);
          const url = parts[0];
          if (!url) continue;
          const desc = parts[1] || "";
          // "1920w" → 1920, "2x" → 2 × 1000 to outrank width-less entries
          let score = 0;
          if (/w$/.test(desc)) score = parseFloat(desc);
          else if (/x$/.test(desc)) score = parseFloat(desc) * 1000;
          else score = 1;
          if (score > bestScore) {
            bestScore = score;
            bestUrl = url;
          }
        }
        return bestUrl;
      }

      const imgs = Array.from(document.querySelectorAll("img"));
      for (const img of imgs) {
        const w = img.naturalWidth || img.width || 0;
        const h = img.naturalHeight || img.height || 0;
        if (w < 200 || h < 200) continue;

        // Walk ancestors looking for class/id hints.
        let hint = 0;
        let skip = false;
        let el = img;
        let depth = 0;
        while (el && depth < 8) {
          const id = (el.id || "").toString().toLowerCase();
          const cls = ((el.className && el.className.toString) ? el.className.toString() : "").toLowerCase();
          const tag = (el.getAttribute && el.getAttribute("data-testid")) || "";
          const blob = id + " " + cls + " " + (typeof tag === "string" ? tag.toLowerCase() : "");
          if (NEGATIVE.test(blob)) {
            skip = true;
            break;
          }
          if (POSITIVE.test(blob)) {
            hint = 1;
            break;
          }
          el = el.parentElement;
          depth += 1;
        }
        if (skip) continue;

        let url =
          bestFromSrcset(img.getAttribute("srcset")) ||
          img.currentSrc ||
          img.src;
        if (!url || url.startsWith("data:") || url.startsWith("blob:")) continue;

        if (seen.has(url)) continue;
        seen.add(url);
        candidates.push({ url, area: w * h, hint });
      }

      candidates.sort((a, b) => (b.hint - a.hint) || (b.area - a.area));
      return candidates.slice(0, 8).map((c) => c.url);
    });
  } catch {
    return [];
  }
}

/**
 * Walk the rendered DOM for product prices. Runs inside the page
 * context via `page.evaluate`. Strategy mirrors the image scanner:
 * positive class hints to qualify candidate elements, negative
 * hints to disqualify entire subtrees, plus per-element strike-
 * through style filtering.
 *
 * Avoidance patterns built in:
 *   - "Free Shipping over $X" — currency string but ancestors won't
 *     carry a price-related class
 *   - "Compare at $X" / "Was $X" — disqualified by negative class
 *     hints (was-price, compare-price, original-price)
 *   - "$X/mo" financing — disqualified by per-month / installment in
 *     ancestors, or filtered numerically (> 50000 plausibility)
 *   - struck-through prices — disqualified by inline
 *     `text-decoration: line-through` walking up to 6 ancestors
 *
 * Requires a positive class hint to trust a number — being
 * conservative is the right side to err on. Better an empty result
 * than the wrong price on a Shop card.
 */
async function scanProductPriceFromDom(page) {
  try {
    return await page.evaluate(() => {
      const CURRENCY_RE =
        /(?:^|[^A-Za-z0-9_])(?:\$|USD\s?|US\$)\s?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)/g;
      const POSITIVE =
        /\b(price|product-price|product__price|current-price|selling-price|regular-price|pdp-price|sale-price|offer-price|now-price|item-price|price-now|price-current|price-display|price-final)\b/;
      const NEGATIVE =
        /\b(was-price|compare-price|compare-at|strikethrough|original-price|crossed-out|line-through|free-shipping|subscription|monthly|per-month|installment|financing|tax-included|related|recommended|cross-sell|you-may|also-like|breadcrumb|nav|menu|footer|review|rating)\b/;

      const candidates = [];

      const all = document.querySelectorAll(
        "*:not(script):not(style):not(noscript)"
      );
      for (const el of all) {
        // Use the element's own text, not children's. We want the
        // leaf-most element holding the price string.
        const ownText = Array.from(el.childNodes)
          .filter((n) => n.nodeType === 3)
          .map((n) => n.textContent || "")
          .join("")
          .trim();
        if (!ownText || ownText.length > 200) continue;

        CURRENCY_RE.lastIndex = 0;
        const matches = [...ownText.matchAll(CURRENCY_RE)];
        if (matches.length === 0) continue;

        // Walk ancestors for hints / strike-through.
        let hint = 0;
        let skip = false;
        let curr = el;
        let depth = 0;
        while (curr && depth < 6) {
          const id = (curr.id || "").toString().toLowerCase();
          const cls =
            curr.className && curr.className.toString
              ? curr.className.toString().toLowerCase()
              : "";
          const blob = id + " " + cls;
          if (NEGATIVE.test(blob)) {
            skip = true;
            break;
          }
          if (POSITIVE.test(blob)) {
            hint = 1;
          }
          if (curr.style) {
            const td =
              curr.style.textDecoration || curr.style.textDecorationLine;
            if (td && /line-through/.test(td)) {
              skip = true;
              break;
            }
          }
          curr = curr.parentElement;
          depth += 1;
        }
        if (skip) continue;
        if (hint === 0) continue;

        for (const m of matches) {
          const raw = m[1].replace(/,/g, "");
          const n = parseFloat(raw);
          // Plausibility filter — below $0.50 is noise (badges,
          // ratings); above $50,000 is implausible for a Shop product.
          if (Number.isFinite(n) && n >= 0.5 && n < 50000) {
            candidates.push(n);
          }
        }
      }

      const seen = new Set();
      const prices = [];
      for (const n of candidates) {
        if (seen.has(n)) continue;
        seen.add(n);
        prices.push(n);
      }
      prices.sort((a, b) => a - b);
      return prices;
    });
  } catch {
    return [];
  }
}

/**
 * Filter predicates for the two retry modes. Both go through the
 * same Playwright + image-fallback path; the difference is which
 * rows from the previous report get re-tested.
 *
 *   FAILED      bot-blocked, network, 5xx — exclude 404/410 (editorial)
 *               and "no DIRECT URL" (also editorial).
 *
 *   THIN        needs-human rows whose flags include "only N image(s)".
 *               These scrapes succeeded; they just didn't surface
 *               enough images in JSON-LD/OG. The DOM image-fallback
 *               in Playwright mode can rescue many of them.
 */
const RETRY_FILTERS = {
  failed: (r) => {
    if (r.bucket !== "failed") return false;
    const err = r.error ?? "";
    if (/HTTP 404|HTTP 410/.test(err)) return false;
    if (/No DIRECT URL/.test(err)) return false;
    return true;
  },
  thin: (r) => {
    if (r.bucket !== "needs-human") return false;
    const flags = Array.isArray(r.flags) ? r.flags : [];
    // Retry when image count or empty prices are blockers — both have
    // a DOM fallback now. Skip rows flagged with [DRAFT, NEEDS
    // CHATEAU REVIEW] or FLAG FOR JORDAN — those are editorial holds,
    // not data deficiencies.
    const isEditorialHold = flags.some((f) =>
      /CHATEAU REVIEW|FLAG FOR JORDAN/i.test(String(f))
    );
    if (isEditorialHold) return false;
    return flags.some((f) =>
      /only \d+ image|empty prices/i.test(String(f))
    );
  },
};

/**
 * Retry pass. Reads the previous report, joins each candidate row
 * back to its CSV record, and re-runs the staging logic through a
 * real browser — same Playwright path used for both failed-row
 * recovery and thin needs-human recovery.
 */
async function runRetryMode(mode = "failed") {
  const label = mode === "thin" ? "retry thin" : "retry failed";
  console.log(
    `Hessentials Shop — ${label} (${ARGS.commit ? "COMMIT" : "DRY-RUN"})`
  );
  console.log(`  report: ${path.relative(REPO_ROOT, REPORT_FILE)}`);
  console.log(`  csv:    ${path.relative(REPO_ROOT, ARGS.csv)}`);
  if (!ARGS.commit) {
    console.log("  (dry-run: no writes, no downloads, no commits)");
  }
  console.log("");

  // 1. Previous report — prefer the canonical commit-mode file.
  const report = await readReportPreferringCommit();
  if (!report) {
    console.error(
      `No report at ${REPORT_FILE}. Run a normal pass first.`
    );
    process.exit(1);
  }

  // 2. Candidate rows — filter shape depends on mode.
  const filter = RETRY_FILTERS[mode] ?? RETRY_FILTERS.failed;
  const retryable = report.rows.filter(filter);
  console.log(`Retry candidates: ${retryable.length}`);
  if (retryable.length === 0) {
    console.log("Nothing to retry.");
    return;
  }

  // 3. Re-read CSV to recover full row data
  const csvText = await fs.readFile(ARGS.csv, "utf8");
  const csvRows = asRecords(parseCsv(csvText));
  const byRowIndex = new Map(csvRows.map((r) => [r.__rowIndex, r]));

  // 4. Existing slug / draft sets — both grow as we stage
  const shopSource = await readShopFile();
  const existingSlugs = existingSlugsFrom(shopSource);
  const existingDrafts = existingDraftSlugsFrom(shopSource);
  const existingUrlMap = existingUrlMapFrom(shopSource);

  // 5. Boot Playwright
  const { chromium } = await ensurePlaywright();
  const browser = await chromium.launch({ headless: true });
  const browserContext = await browser.newContext({
    userAgent: FETCH_UA,
    viewport: { width: 1440, height: 900 },
    locale: "en-US",
    extraHTTPHeaders: {
      "Accept-Language": "en-US,en;q=0.9",
    },
  });

  const scrapeFn = makeBrowserScrape(browserContext);
  const ctx = { existingSlugs };
  const updatedRows = [];
  // Within-run URL map — covers the case where the CSV has two rows
  // with the same DIRECT URL and the first one stages successfully.
  // existingUrlMap is built once at the start; without this, the second
  // row would re-stage with a `-N` suffix.
  const stagedThisRun = new Map();

  try {
    for (const prev of retryable) {
      const row = byRowIndex.get(prev.rowIndex);
      if (!row) {
        updatedRows.push({
          ...prev,
          retryError: "Row missing from CSV — was the CSV edited?",
        });
        continue;
      }

      // URL-keyed idempotency — check both shop.ts state and anything
      // we've staged in this loop already.
      const rowDirectUrl = (row["DIRECT PRODUCT URL FOR SALE"] ?? "").trim();
      if (rowDirectUrl && stagedThisRun.has(rowDirectUrl)) {
        updatedRows.push({
          ...prev,
          bucket: "duplicate",
          firstSlug: stagedThisRun.get(rowDirectUrl),
        });
        console.log(
          `  [dup ] row ${prev.rowIndex}  ${rowDirectUrl} → ${stagedThisRun.get(rowDirectUrl)}`
        );
        continue;
      }
      if (rowDirectUrl && existingUrlMap.has(rowDirectUrl)) {
        const present = existingUrlMap.get(rowDirectUrl);
        const bucket = present.draft ? "already-staged" : "already-live";
        updatedRows.push({
          ...prev,
          bucket,
          skipped: true,
          existingSlug: present.slug,
        });
        console.log(
          `  [skip] row ${prev.rowIndex}  ${present.slug} (URL already in shop.ts)`
        );
        continue;
      }

      const res = await processRow(row, ctx, scrapeFn);

      // Mutations under --commit only
      if (res.bucket === "staged-draft" && ARGS.commit) {
        try {
          const imgs = await saveImagesContentAddressed(
            res.candidate.slug,
            res.candidate.images
          );
          if (!imgs.saved.length) {
            res.bucket = "failed";
            res.error = "No images downloaded";
            res.imageFailures = imgs.failed;
          } else {
            await appendShopEntry({
              slug: res.candidate.slug,
              name: res.candidate.name,
              brand: res.candidate.brand,
              category: res.candidate.category || "home",
              subcategory: "uncategorized",
              audience: res.candidate.audience,
              dateAdded: new Date().toISOString(),
              reason: res.candidate.reason,
              priceRange: res.candidate.priceRange,
              url: res.candidate.url,
              images: imgs.saved.map((s) => s.publicPath),
              extractionMethod: res.candidate.extractionMethod,
              draft: true,
            });
            existingSlugs.add(res.candidate.slug);
            existingDrafts.add(res.candidate.slug);
            stagedThisRun.set(res.candidate.url, res.candidate.slug);
            res.imagesSaved = imgs.saved;
            const commit = gitCommit(res.candidate.slug);
            if (commit && typeof commit === "string") res.commitHash = commit;
            else if (commit) res.commitError = commit.error;
          }
        } catch (e) {
          res.bucket = "failed";
          res.error = `commit step: ${e?.message ?? e}`;
        }
      }

      // Pending queue write (NEEDS HUMAN under --commit)
      if (res.bucket === "needs-human" && ARGS.commit) {
        const pending = await loadPending();
        const idx = pending.entries.findIndex(
          (e) => e.directUrl === res.directUrl
        );
        const record = {
          rowIndex: res.rowIndex,
          sourceArticle: res.sourceArticle,
          articleUrl: res.articleUrl,
          anchor: res.anchor,
          directUrl: res.directUrl,
          flags: res.flags,
          candidate: res.candidate,
          stagedAt: new Date().toISOString(),
        };
        if (idx >= 0) pending.entries[idx] = record;
        else pending.entries.push(record);
        await savePending(pending);
      }

      const label =
        res.bucket === "staged-draft"
          ? "stag"
          : res.bucket === "needs-human"
          ? "need"
          : res.bucket === "failed"
          ? "fail"
          : res.bucket;
      const slugOrUrl = res.candidate?.slug ?? res.directUrl.slice(0, 60);
      const tail =
        res.bucket === "failed"
          ? `  ← ${res.error ?? ""}`
          : res.bucket === "needs-human"
          ? `  flags: ${res.flags.join(", ")}`
          : "";
      console.log(`  [${label}] row ${res.rowIndex}  ${slugOrUrl}${tail}`);
      updatedRows.push(res);
    }
  } finally {
    await browser.close();
  }

  // 6. Merge results back into the report. The retry row replaces the
  // previous failed row in-place; everything else passes through.
  const byKey = new Map(updatedRows.map((r) => [r.rowIndex, r]));
  const mergedRows = report.rows.map((r) => byKey.get(r.rowIndex) ?? r);

  const counts = {
    "staged-draft": 0,
    "needs-human": 0,
    failed: 0,
    "editorial-removal": 0,
    duplicate: 0,
    "already-staged": 0,
    "already-live": 0,
  };
  for (const r of mergedRows) counts[r.bucket] = (counts[r.bucket] ?? 0) + 1;

  console.log("");
  console.log("Retry summary");
  const promoted = updatedRows.filter((r) => r.bucket === "staged-draft").length;
  const pendingNew = updatedRows.filter((r) => r.bucket === "needs-human").length;
  const stillFailed = updatedRows.filter((r) => r.bucket === "failed").length;
  console.log(`  recovered → staged-draft   ${promoted}`);
  console.log(`  recovered → needs-human    ${pendingNew}`);
  console.log(`  still failing              ${stillFailed}`);
  console.log("");
  console.log("New overall counts");
  for (const [k, v] of Object.entries(counts)) console.log(`  ${k.padEnd(18)} ${v}`);

  // 7. Rewrite the report file with merged rows
  const merged = {
    ...report,
    generatedAt: new Date().toISOString(),
    mode: ARGS.commit ? "commit-retry" : "dry-run-retry",
    counts,
    rows: mergedRows.map((r) => ({
      rowIndex: r.rowIndex,
      sourceArticle: r.sourceArticle,
      articleUrl: r.articleUrl,
      anchor: r.anchor,
      directUrl: r.directUrl,
      bucket: r.bucket,
      slug: r.candidate?.slug ?? r.slug,
      proposedCategory: r.candidate?.category ?? r.proposedCategory,
      proposedAudience:
        r.candidate?.proposedAudience ?? r.proposedAudience,
      flags: r.flags,
      error: r.error,
      commitHash: r.commitHash,
      firstSlug: r.firstSlug,
    })),
  };
  // Retry-commit writes to the canonical file; retry-dryrun writes to
  // its own. A dry-run retry never overwrites the live state.
  const retryOut = ARGS.commit ? REPORT_FILE : REPORT_DRYRUN_FILE;
  await fs.writeFile(retryOut, JSON.stringify(merged, null, 2) + "\n", "utf8");
  console.log("");
  console.log(`Report:  ${path.relative(REPO_ROOT, retryOut)}`);
}

/**
 * Find duplicate draft entries in shop.ts — entries sharing a URL
 * where one slug is the canonical form and the others carry `-2`,
 * `-3`, … suffixes from `ensureUnique`. Remove the suffixed copies
 * (the canonical one stays). Also deletes their content-addressed
 * image directories under `public/shop/<slug>/`.
 *
 * Dry-run by default. Pass --commit to actually delete.
 *
 * The duplicate detection works on URL — a defense against the
 * slug-based idempotency bug shipped briefly in this script:
 * proposing a slug AFTER ensureUnique meant existingDrafts.has()
 * never matched and the same URL got staged repeatedly with `-N`
 * suffixes. URL-keyed cleanup is order-independent and reliable.
 */
async function runCleanDuplicatesMode() {
  console.log(
    `Hessentials Shop — clean duplicates (${ARGS.commit ? "COMMIT" : "DRY-RUN"})`
  );
  if (!ARGS.commit) {
    console.log("  (dry-run: no writes, no deletions)");
  }
  console.log("");

  const shopSource = await readShopFile();
  const lines = shopSource.split("\n");

  // Walk every draft entry, recording slug + url + draft flag.
  const drafts = [];
  let inEntry = false;
  let slug = "";
  let url = "";
  let isDraft = false;
  for (const line of lines) {
    if (line === "  {") {
      inEntry = true;
      slug = "";
      url = "";
      isDraft = false;
      continue;
    }
    if (!inEntry) continue;
    if (line === "  },") {
      if (slug && url && isDraft) drafts.push({ slug, url });
      inEntry = false;
      continue;
    }
    const sm = /^\s*slug:\s*"([^"]+)"/.exec(line);
    if (sm) slug = sm[1];
    const um = /^\s*url:\s*"([^"]+)"/.exec(line);
    if (um) url = um[1];
    if (/^\s*draft:\s*true,?\s*$/.test(line)) isDraft = true;
  }

  // Group drafts by URL. URLs with >1 draft are the duplicate cases.
  const byUrl = new Map();
  for (const d of drafts) {
    if (!byUrl.has(d.url)) byUrl.set(d.url, []);
    byUrl.get(d.url).push(d.slug);
  }
  const dupGroups = [...byUrl.entries()].filter(([, slugs]) => slugs.length > 1);

  if (dupGroups.length === 0) {
    console.log("No duplicate draft URLs found. Nothing to clean.");
    return;
  }

  console.log(`Found ${dupGroups.length} URL${dupGroups.length === 1 ? "" : "s"} staged more than once:\n`);

  // For each group, pick the canonical slug (the one without `-N`
  // suffix, or the shortest if none qualifies). Remove the rest.
  const toRemove = [];
  for (const [groupUrl, slugs] of dupGroups) {
    // Prefer the slug with no trailing -<digits>; fall back to the
    // shortest one.
    const noSuffix = slugs.find((s) => !/-\d+$/.test(s));
    const canonical = noSuffix ?? [...slugs].sort((a, b) => a.length - b.length)[0];
    const removing = slugs.filter((s) => s !== canonical);
    console.log(`  ${groupUrl}`);
    console.log(`    keep:   ${canonical}`);
    for (const r of removing) console.log(`    remove: ${r}`);
    for (const r of removing) toRemove.push(r);
  }

  console.log("");
  console.log(`Total entries to remove: ${toRemove.length}`);

  if (!ARGS.commit) {
    console.log("");
    console.log("Re-run with --commit to apply.");
    return;
  }

  // Apply removals. Use the existing line-by-line block locator
  // logic (mirrored in writeEntry.ts's locateBlockLines).
  for (const slugToRemove of toRemove) {
    const current = await readShopFile();
    const cLines = current.split("\n");
    const range = locateEntryBlock(cLines, slugToRemove);
    if (!range) {
      console.log(`  [warn] couldn't find ${slugToRemove}, skipping`);
      continue;
    }
    const next = [
      ...cLines.slice(0, range.start),
      ...cLines.slice(range.end + 1),
    ].join("\n");
    await fs.writeFile(SHOP_FILE, next, "utf8");
    // Image dir cleanup — content-addressed under public/shop/<slug>/
    const imgDir = path.join(PUBLIC_SHOP_DIR, slugToRemove);
    try {
      await fs.rm(imgDir, { recursive: true, force: true });
    } catch {
      // ignore — dir may not exist
    }
    console.log(`  [del ] ${slugToRemove}`);
    // Per-entry git commit, same pattern as the staging path.
    if (ARGS.git) {
      try {
        execFileSync("git", ["add", "src/data/shop.ts", `public/shop/${slugToRemove}`], {
          cwd: REPO_ROOT,
          stdio: "ignore",
        });
        execFileSync(
          "git",
          [
            "commit",
            "-m",
            `Shop: clean duplicate draft "${slugToRemove}"`,
            "--no-verify",
          ],
          { cwd: REPO_ROOT, stdio: "ignore" }
        );
      } catch {
        // Either nothing to commit (image dir didn't exist) or pre-commit hooks fired.
      }
    }
  }
  console.log("");
  console.log(`Removed ${toRemove.length} duplicate draft entr${toRemove.length === 1 ? "y" : "ies"}.`);
}

/**
 * Locate a single entry block in shop.ts by slug. Returns inclusive
 * line indices `{start, end}` of the `  {` … `  },` pair, or null
 * if the slug isn't found exactly once.
 */
function locateEntryBlock(lines, slug) {
  const slugLine = `    slug: "${slug}",`;
  let slugIdx = -1;
  for (let i = 0; i < lines.length; i += 1) {
    if (lines[i] === slugLine) {
      if (slugIdx !== -1) return null;
      slugIdx = i;
    }
  }
  if (slugIdx === -1) return null;
  let start = -1;
  for (let i = slugIdx - 1; i >= 0; i -= 1) {
    if (lines[i] === "  {") {
      start = i;
      break;
    }
    if (lines[i] === "  },") return null;
  }
  let end = -1;
  for (let i = slugIdx + 1; i < lines.length; i += 1) {
    if (lines[i] === "  },") {
      end = i;
      break;
    }
    if (lines[i] === "  {") return null;
  }
  if (start === -1 || end === -1) return null;
  return { start, end };
}

/**
 * Read the existing report and re-emit the Chateau dead-URL markdown.
 * No scraping, no mutations. Useful for regenerating the editorial
 * brief after a fresh CSV without paying for a full network walk.
 */
async function runEmitChateauMode() {
  const report = await readReportPreferringCommit();
  if (!report) {
    console.error(
      `No report at ${REPORT_FILE}. Run the script normally first.`
    );
    process.exit(1);
  }
  const deadUrlRows = (report.rows ?? []).filter(
    (r) =>
      r.bucket === "failed" &&
      (/HTTP 404|HTTP 410/.test(r.error ?? "") ||
        /No DIRECT URL/.test(r.error ?? ""))
  );
  if (deadUrlRows.length === 0) {
    console.log("No dead URLs in the current report.");
    return;
  }
  const md = buildChateauList(deadUrlRows);
  await fs.writeFile(CHATEAU_FILE, md, "utf8");
  console.log(
    `Wrote ${path.relative(REPO_ROOT, CHATEAU_FILE)} — ${deadUrlRows.length} dead URL${deadUrlRows.length === 1 ? "" : "s"}.`
  );
}

// ----------------------------------------------------------------------
// Main
// ----------------------------------------------------------------------

async function main() {
  if (ARGS.cleanDuplicates) {
    await runCleanDuplicatesMode();
    return;
  }
  if (ARGS.emitChateau) {
    await runEmitChateauMode();
    return;
  }
  if (ARGS.retryFailed) {
    await runRetryMode("failed");
    return;
  }
  if (ARGS.retryThin) {
    await runRetryMode("thin");
    return;
  }
  console.log(
    `Hessentials Shop — bulk import (${ARGS.commit ? "COMMIT" : "DRY-RUN"})`
  );
  console.log(`  csv:    ${path.relative(REPO_ROOT, ARGS.csv)}`);
  console.log(`  shop:   src/data/shop.ts`);
  console.log(`  images: public/shop/<slug>/<sha1>.jpg`);
  if (!ARGS.commit) {
    console.log(`  (dry-run: no writes, no downloads, no commits)`);
  }
  console.log("");

  let csvText;
  try {
    csvText = await fs.readFile(ARGS.csv, "utf8");
  } catch (e) {
    console.error(`Failed to read CSV at ${ARGS.csv}: ${e.message ?? e}`);
    process.exit(1);
  }

  const rows = asRecords(parseCsv(csvText));
  const filtered = ARGS.row ? rows.filter((r) => r.__rowIndex === ARGS.row) : rows;
  console.log(`Loaded ${rows.length} row(s) from CSV; processing ${filtered.length}.`);
  console.log("");

  const shopSource = await readShopFile();
  const existingSlugs = existingSlugsFrom(shopSource);
  const existingDrafts = existingDraftSlugsFrom(shopSource);
  const existingUrlMap = existingUrlMapFrom(shopSource);

  // Voice lint pass — independent of row processing.
  const voiceWarnings = lintExistingShop(shopSource);

  const ctx = { existingSlugs };
  const results = [];

  // URL → first slug seen, for de-duplicating cross-article references.
  const urlToSlug = new Map();

  for (const row of filtered) {
    // URL-keyed idempotency — short-circuit BEFORE scraping if this
    // URL is already in shop.ts (draft or live). Slug-based checks
    // fired too late: ensureUnique would have already suffixed `-2`
    // and the post-collision slug never matched the existing one.
    const rowDirectUrl = (row["DIRECT PRODUCT URL FOR SALE"] ?? "").trim();
    if (rowDirectUrl && existingUrlMap.has(rowDirectUrl)) {
      const present = existingUrlMap.get(rowDirectUrl);
      const bucket = present.draft ? "already-staged" : "already-live";
      results.push({
        rowIndex: row.__rowIndex,
        sourceArticle: row.source_article,
        articleUrl: row.article_url,
        anchor: row.anchor_text,
        brand: row.brand,
        directUrl: rowDirectUrl,
        bucket,
        skipped: true,
        existingSlug: present.slug,
      });
      console.log(`  [skip] row ${row.__rowIndex}  ${present.slug} (URL already in shop.ts)`);
      continue;
    }

    const res = await processRow(row, ctx);

    // Cross-article duplicate handling — re-stage only once.
    const url = res.directUrl;
    if (res.bucket === "staged-draft" && urlToSlug.has(url)) {
      results.push({
        ...res,
        bucket: "duplicate",
        firstSlug: urlToSlug.get(url),
      });
      console.log(`  [dup ] row ${res.rowIndex}  ${url}  → ${urlToSlug.get(url)}`);
      continue;
    }

    // Mutations only when --commit.
    if (res.bucket === "staged-draft" && ARGS.commit) {
      try {
        const imgs = await saveImagesContentAddressed(
          res.candidate.slug,
          res.candidate.images
        );
        if (!imgs.saved.length) {
          res.bucket = "failed";
          res.error = "No images downloaded";
          res.imageFailures = imgs.failed;
        } else {
          await appendShopEntry({
            slug: res.candidate.slug,
            name: res.candidate.name,
            brand: res.candidate.brand,
            category: res.candidate.category || "home", // placeholder — human picks on draft page
            subcategory: "uncategorized", // placeholder — human picks on draft page
            audience: res.candidate.audience,
            dateAdded: new Date().toISOString(),
            reason: res.candidate.reason,
            priceRange: res.candidate.priceRange,
            url: res.candidate.url,
            images: imgs.saved.map((s) => s.publicPath),
            extractionMethod: res.candidate.extractionMethod,
            draft: true,
          });
          existingSlugs.add(res.candidate.slug);
          existingDrafts.add(res.candidate.slug);
          urlToSlug.set(url, res.candidate.slug);
          res.imagesSaved = imgs.saved;
          res.imageFailures = imgs.failed;
          const commit = gitCommit(res.candidate.slug);
          if (commit && typeof commit === "string") res.commitHash = commit;
          else if (commit) res.commitError = commit.error;
        }
      } catch (e) {
        res.bucket = "failed";
        res.error = `commit step: ${e?.message ?? e}`;
      }
    } else if (res.bucket === "staged-draft") {
      // Dry-run — still track URL→slug so duplicates are detected.
      urlToSlug.set(url, res.candidate.slug);
    }

    // Pending queue write (NEEDS HUMAN).
    if (res.bucket === "needs-human" && ARGS.commit) {
      const pending = await loadPending();
      const existing = pending.entries.findIndex((e) => e.directUrl === res.directUrl);
      const record = {
        rowIndex: res.rowIndex,
        sourceArticle: res.sourceArticle,
        articleUrl: res.articleUrl,
        anchor: res.anchor,
        directUrl: res.directUrl,
        flags: res.flags,
        candidate: res.candidate,
        stagedAt: new Date().toISOString(),
      };
      if (existing >= 0) pending.entries[existing] = record;
      else pending.entries.push(record);
      await savePending(pending);
    }

    const label =
      res.bucket === "staged-draft"
        ? "stag"
        : res.bucket === "needs-human"
        ? "need"
        : res.bucket === "failed"
        ? "fail"
        : res.bucket === "editorial-removal"
        ? "rmv "
        : res.bucket;
    const slugOrUrl = res.candidate?.slug ?? res.directUrl.slice(0, 50);
    const tail =
      res.bucket === "failed"
        ? `  ← ${res.error ?? ""}`
        : res.bucket === "needs-human"
        ? `  flags: ${res.flags.join(", ")}`
        : "";
    console.log(`  [${label}] row ${res.rowIndex}  ${slugOrUrl}${tail}`);

    results.push(res);
  }

  // ----- Summary -----
  const counts = {
    "staged-draft": 0,
    "needs-human": 0,
    failed: 0,
    "editorial-removal": 0,
    duplicate: 0,
    "already-staged": 0,
    "already-live": 0,
  };
  for (const r of results) counts[r.bucket] = (counts[r.bucket] ?? 0) + 1;

  console.log("");
  console.log("Summary");
  for (const [k, v] of Object.entries(counts)) console.log(`  ${k.padEnd(18)} ${v}`);

  // ----- Failure breakdown -----
  const failed = results.filter((r) => r.bucket === "failed");
  if (failed.length) {
    console.log("");
    console.log("Failed rows (by error pattern):");
    const byError = new Map();
    for (const r of failed) {
      const key = (r.error ?? "").split(":")[0].trim() || "(unknown)";
      if (!byError.has(key)) byError.set(key, []);
      byError.get(key).push(r);
    }
    for (const [k, list] of [...byError.entries()].sort((a, b) => b[1].length - a[1].length)) {
      console.log(`  ${k}  (${list.length})`);
      for (const r of list) {
        console.log(`    row ${r.rowIndex}  ${r.directUrl}`);
      }
    }
  }

  // ----- Editorial removal list -----
  const removals = results.filter((r) => r.bucket === "editorial-removal");
  if (removals.length) {
    console.log("");
    console.log("Editorial removals — article body edits needed:");
    for (const r of removals) {
      console.log(`  ${r.sourceArticle}`);
      console.log(`    anchor: ${r.anchor}`);
      console.log(`    article: ${r.articleUrl}`);
    }
  }

  // ----- Voice lint -----
  if (voiceWarnings.length) {
    console.log("");
    console.log(`Existing-entry voice warnings: ${voiceWarnings.length}`);
    for (const w of voiceWarnings) {
      console.log(`  ${w.slug}  [${w.hits.join(", ")}]`);
    }
  }

  // ----- Report file -----
  const report = {
    generatedAt: new Date().toISOString(),
    mode: ARGS.commit ? "commit" : "dry-run",
    csv: path.relative(REPO_ROOT, ARGS.csv),
    counts,
    rows: results.map((r) => ({
      rowIndex: r.rowIndex,
      sourceArticle: r.sourceArticle,
      articleUrl: r.articleUrl,
      anchor: r.anchor,
      directUrl: r.directUrl,
      bucket: r.bucket,
      slug: r.candidate?.slug,
      proposedCategory: r.candidate?.category,
      proposedAudience: r.candidate?.proposedAudience,
      flags: r.flags,
      error: r.error,
      commitHash: r.commitHash,
      firstSlug: r.firstSlug,
    })),
    existingEntriesVoiceWarnings: voiceWarnings,
  };
  // Dry-run writes to its own file — never overwrites the canonical
  // commit-mode report. Commit-mode writes to the canonical file. Both
  // surface the same shape so retry/--emit-chateau can read either.
  const outFile = ARGS.commit ? REPORT_FILE : REPORT_DRYRUN_FILE;
  await fs.mkdir(path.dirname(outFile), { recursive: true });
  await fs.writeFile(outFile, JSON.stringify(report, null, 2) + "\n", "utf8");

  // ----- Dead-URL list for Chateau -----
  // 404 / 410 / "No DIRECT URL" rows. These are editorial problems —
  // the product page doesn't exist anymore, or the row never had a
  // usable URL. Chateau either finds a replacement or marks the row
  // REMOVE FROM ARTICLE on the next CSV pass. Only the commit-mode
  // run regenerates the Chateau file (dry-run shouldn't overwrite an
  // editorial brief built off a real network pass).
  const deadUrlRows = results.filter(
    (r) =>
      r.bucket === "failed" &&
      (/HTTP 404|HTTP 410/.test(r.error ?? "") ||
        /No DIRECT URL/.test(r.error ?? ""))
  );
  if (deadUrlRows.length > 0 && ARGS.commit) {
    const md = buildChateauList(deadUrlRows);
    await fs.writeFile(CHATEAU_FILE, md, "utf8");
  }

  console.log("");
  console.log(`Report:   ${path.relative(REPO_ROOT, outFile)}`);
  if (ARGS.commit && counts["needs-human"] > 0) {
    console.log(`Pending:  ${path.relative(REPO_ROOT, PENDING_FILE)}`);
  }
  if (deadUrlRows.length > 0 && ARGS.commit) {
    console.log(
      `Chateau:  ${path.relative(REPO_ROOT, CHATEAU_FILE)}  (${deadUrlRows.length} dead URL${deadUrlRows.length === 1 ? "" : "s"})`
    );
  } else if (deadUrlRows.length > 0) {
    console.log(
      `Chateau:  (${deadUrlRows.length} dead URL${deadUrlRows.length === 1 ? "" : "s"} — re-run with --commit or use --emit-chateau)`
    );
  }
}

/**
 * Format the dead-URL rows as a Markdown brief. Grouped by source
 * article so the editorial pass can move article by article rather
 * than URL by URL. Plain prose, no preciousness.
 */
function buildChateauList(rows) {
  const byArticle = new Map();
  for (const r of rows) {
    const key = r.sourceArticle || "(unknown article)";
    if (!byArticle.has(key)) byArticle.set(key, []);
    byArticle.get(key).push(r);
  }
  const out = [];
  out.push("# Shop import — dead URLs");
  out.push("");
  out.push(
    `${rows.length} row${rows.length === 1 ? "" : "s"} where the source URL is dead (404, 410, or missing). Each one is an editorial decision: find a current URL for the same product, swap it for a different product that serves the same argument, or remove the anchor.`
  );
  out.push("");
  out.push("Generated by `scripts/shop-bulk-import.mjs`. Edit `data/shop-import-master.csv` to mark replacements or removals; re-run the script to pick them up.");
  out.push("");
  out.push("---");
  out.push("");

  const articles = [...byArticle.keys()].sort();
  for (const article of articles) {
    const list = byArticle.get(article);
    out.push(`## ${article}`);
    const articleUrl = list[0]?.articleUrl;
    if (articleUrl) {
      out.push("");
      out.push(`Source: ${articleUrl}`);
    }
    out.push("");
    for (const r of list) {
      const status =
        /HTTP 404/.test(r.error ?? "")
          ? "404"
          : /HTTP 410/.test(r.error ?? "")
          ? "410"
          : "no url";
      out.push(`- **${r.brand || "?"}** — ${r.anchor || "(no anchor text)"}  _(${status})_`);
      if (r.directUrl && r.directUrl.startsWith("http")) {
        out.push(`  ${r.directUrl}`);
      }
    }
    out.push("");
  }
  return out.join("\n");
}

main().catch((e) => {
  console.error("Bulk import crashed:", e);
  process.exit(1);
});
