/**
 * Shop drafts — rescrape a pending row and (when possible) promote
 * it to a staged draft, in one click.
 *
 * POST /api/admin/shop-drafts/rescrape-pending
 *   body: { directUrl: string }
 *
 * Steps:
 *   1. Look up the pending entry by `directUrl` in
 *      `data/shop-import-pending.json`. Its existing fields carry the
 *      editorial reason and (often) brand/name/images — we never
 *      overwrite those with scraped marketing copy.
 *   2. Re-run `extractProduct(directUrl)` against the live source.
 *   3. Merge: prefer the candidate's editorial fields; pull fresh
 *      prices and (if no candidate images) fresh images.
 *   4. If we now have at least one image AND a price range, save the
 *      images, append the entry to `src/data/shop.ts` as a draft,
 *      and cull the pending row.
 *   5. If we still can't satisfy the staging threshold, return the
 *      scrape result without writing anything. The client renders the
 *      result so the reviewer sees what came back.
 *
 * Editorial fields (name, brand, reason, category) are PRESERVED from
 * the pending entry. The point of the rescrape is the operational
 * data (prices, images), not the voice.
 *
 * Dev-only. Returns 403 in production.
 */

import fs from "node:fs/promises";
import path from "node:path";
import { NextRequest, NextResponse } from "next/server";
import {
  SHOP_CATEGORIES,
  type Category,
  type ExtractionMethod,
} from "../../../../../data/shop";
import { extractProduct } from "../../../../../lib/shopImport/extract";
import { suggestPriceRange } from "../../../../../lib/shopImport/formatPriceRange";
import { buildSlug, ensureUnique } from "../../../../../lib/shopImport/slug";
import { saveImagesForSlug } from "../../../../../lib/shopImport/saveImages";
import {
  appendShopEntry,
  readExistingSlugs,
  type NewShopEntry,
} from "../../../../../lib/shopImport/writeEntry";

export const dynamic = "force-dynamic";

const PENDING_FILE = path.join(
  process.cwd(),
  "data",
  "shop-import-pending.json"
);

type PendingEntry = {
  rowIndex?: number;
  sourceArticle?: string;
  articleUrl?: string;
  anchor?: string;
  directUrl: string;
  flags?: string[];
  candidate: {
    slug?: string;
    name: string;
    brand: string;
    category?: string;
    audience?: string[];
    reason?: string;
    priceRange?: string;
    url: string;
    images?: string[];
    extractionMethod?: string;
  };
  stagedAt?: string;
};

type PendingFile = { entries: PendingEntry[] };

async function readPending(): Promise<PendingFile> {
  try {
    const raw = await fs.readFile(PENDING_FILE, "utf8");
    return JSON.parse(raw) as PendingFile;
  } catch {
    return { entries: [] };
  }
}

async function writePending(data: PendingFile): Promise<void> {
  await fs.mkdir(path.dirname(PENDING_FILE), { recursive: true });
  await fs.writeFile(
    PENDING_FILE,
    JSON.stringify(data, null, 2) + "\n",
    "utf8"
  );
}

const VALID_METHODS: ReadonlySet<ExtractionMethod> = new Set([
  "json-ld",
  "shopify",
  "html",
  "manual",
]);

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

export async function POST(req: NextRequest): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json(
      { error: "Not available in production" },
      { status: 403 }
    );
  }

  let body: { directUrl?: string };
  try {
    body = (await req.json()) as { directUrl?: string };
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const directUrl = (body.directUrl ?? "").trim();
  if (!directUrl) {
    return NextResponse.json(
      { error: "directUrl is required" },
      { status: 400 }
    );
  }
  try {
    new URL(directUrl);
  } catch {
    return NextResponse.json(
      { error: "directUrl must be a valid URL" },
      { status: 400 }
    );
  }

  // 1. Find the pending entry by URL. Anchor on this so callers don't
  //    have to round-trip the entire candidate payload — the file on
  //    disk stays the source of truth.
  const pending = await readPending();
  const idx = pending.entries.findIndex((e) => e.directUrl === directUrl);
  if (idx < 0) {
    return NextResponse.json(
      { error: `No pending entry with directUrl "${directUrl}"` },
      { status: 404 }
    );
  }
  const entry = pending.entries[idx];

  // 2. Run the extractor.
  let scrape;
  try {
    scrape = await extractProduct(directUrl);
  } catch (e) {
    return NextResponse.json(
      {
        error: `Scrape failed: ${
          e instanceof Error ? e.message : String(e)
        }`,
      },
      { status: 502 }
    );
  }

  const priceRange = suggestPriceRange(scrape.prices);
  // Merge images: prefer the freshly scraped list; fall back to whatever
  // images the pending row already carried (often valid CDN URLs that
  // just couldn't be parsed when first ingested).
  const images =
    scrape.images && scrape.images.length > 0
      ? scrape.images
      : entry.candidate.images ?? [];

  // Editorial-preserving fields. The point of the rescrape is the
  // operational data (price, images, extraction method) — not the voice.
  const name = entry.candidate.name?.trim() || scrape.name?.trim() || "";
  const brand = entry.candidate.brand?.trim() || scrape.brand?.trim() || "";
  const reason = (entry.candidate.reason ?? "").trim();
  const candidateCategory = (entry.candidate.category ?? "").trim();
  const category: Category | "" = SHOP_CATEGORIES.includes(
    candidateCategory as Category
  )
    ? (candidateCategory as Category)
    : "";
  const extractionMethod: ExtractionMethod = VALID_METHODS.has(
    scrape.extractionMethod as ExtractionMethod
  )
    ? (scrape.extractionMethod as ExtractionMethod)
    : VALID_METHODS.has(
        (entry.candidate.extractionMethod ?? "manual") as ExtractionMethod
      )
    ? ((entry.candidate.extractionMethod ?? "manual") as ExtractionMethod)
    : "manual";

  // Common preview payload — returned in both staged and not-staged cases
  // so the client can show what came back.
  const preview = {
    name,
    brand,
    priceRange,
    prices: scrape.prices,
    imageCount: images.length,
    images: images.slice(0, 6), // keep response small
    extractionMethod,
    candidateCategory: candidateCategory || null,
  };

  // 3. Staging eligibility — only proceed if we have a usable price
  //    range AND at least one image. Below that bar, return the scrape
  //    so the reviewer can see what's missing.
  if (!priceRange || images.length === 0 || !name || !brand || !category) {
    const blockers: string[] = [];
    if (!priceRange) blockers.push("no price range");
    if (images.length === 0) blockers.push("no images");
    if (!name) blockers.push("no name");
    if (!brand) blockers.push("no brand");
    if (!category) blockers.push("no category");
    return NextResponse.json({
      ok: true,
      staged: false,
      blockers,
      preview,
    });
  }

  // 4. Stage as draft.
  const existingSlugs = await readExistingSlugs();
  const proposedSlug = (entry.candidate.slug ?? "").trim() || buildSlug(brand, name);
  const slug = ensureUnique(proposedSlug, existingSlugs);

  const saveResult = await saveImagesForSlug(slug, images);
  if (saveResult.saved.length === 0) {
    return NextResponse.json(
      {
        ok: false,
        error: "No images could be downloaded after rescrape",
        preview,
        failed: saveResult.failed,
      },
      { status: 502 }
    );
  }

  const audience = (entry.candidate.audience ?? []).filter(
    (a): a is "mens" | "womens" => a === "mens" || a === "womens"
  );

  const newEntry: NewShopEntry = {
    slug,
    name,
    brand,
    category,
    // Pending rows rarely carry a subcategory. Stage with the same
    // placeholder the bulk script uses; the drafts row's inline picker
    // will let the reviewer set the real one before promoting.
    subcategory: "uncategorized",
    audience: audience.length > 0 ? audience : undefined,
    dateAdded: new Date().toISOString(),
    reason,
    priceRange,
    url: directUrl,
    images: saveResult.saved.map((s) => s.publicPath),
    extractionMethod,
    draft: true,
  };

  try {
    await appendShopEntry(newEntry);
  } catch (e) {
    return NextResponse.json(
      {
        ok: false,
        error: `Failed to write shop.ts: ${
          e instanceof Error ? e.message : String(e)
        }`,
        preview,
        savedImages: saveResult.saved,
      },
      { status: 500 }
    );
  }

  // 5. Cull pending row.
  pending.entries.splice(idx, 1);
  await writePending(pending);

  return NextResponse.json({
    ok: true,
    staged: true,
    slug,
    saved: saveResult.saved,
    failed: saveResult.failed,
    preview,
  });
}
