/**
 * Shop drafts — unstage endpoint.
 *
 * POST /api/admin/shop-drafts/unstage
 *   body: { slug: string }
 *
 * Removes the named draft from src/data/shop.ts and records a stub
 * entry in `data/shop-import-pending.json` so the row stays visible
 * for review (under /admin/shop-drafts → Pending). Images are NOT
 * deleted — they may be reused on a re-stage.
 *
 * Distinct from /api/admin/shop-item/[slug] DELETE, which is
 * destructive (removes entry + images).
 *
 * Dev-only. Returns 403 in production.
 */

import fs from "node:fs/promises";
import path from "node:path";
import { NextRequest, NextResponse } from "next/server";
import { SHOP_PRODUCTS } from "../../../../../data/shop";
import {
  deleteShopEntry,
  entryExists,
} from "../../../../../lib/shopImport/writeEntry";

export const dynamic = "force-dynamic";

const PENDING_FILE = path.join(
  process.cwd(),
  "data",
  "shop-import-pending.json"
);

type PendingFile = {
  entries: PendingEntry[];
};

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
  stagedAt: string;
};

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

  let body: { slug?: string; reason?: string };
  try {
    body = (await req.json()) as { slug?: string; reason?: string };
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const slug = (body.slug ?? "").trim();
  const reasonNote = (body.reason ?? "sent back from drafts").trim();

  if (!slug) {
    return NextResponse.json({ error: "slug is required" }, { status: 400 });
  }
  if (!(await entryExists(slug))) {
    return NextResponse.json(
      { error: `No entry for slug "${slug}".` },
      { status: 404 }
    );
  }

  const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
  if (!product) {
    return NextResponse.json(
      { error: `Slug exists in shop.ts but not in runtime bundle.` },
      { status: 409 }
    );
  }

  // 1. Append to pending JSON.
  const pending = await readPending();
  const existing = pending.entries.findIndex(
    (e) => e.directUrl === product.url || e.candidate?.slug === slug
  );
  const record: PendingEntry = {
    sourceArticle: undefined,
    articleUrl: undefined,
    anchor: undefined,
    directUrl: product.url,
    flags: [reasonNote],
    candidate: {
      slug: product.slug,
      name: product.name,
      brand: product.brand,
      category: product.category,
      audience: [...(product.audience ?? [])],
      reason: product.reason,
      priceRange: product.priceRange,
      url: product.url,
      images: [...(product.images ?? [product.image])],
      extractionMethod: product.extractionMethod ?? "manual",
    },
    stagedAt: new Date().toISOString(),
  };
  if (existing >= 0) pending.entries[existing] = record;
  else pending.entries.push(record);
  await writePending(pending);

  // 2. Remove from shop.ts.
  try {
    await deleteShopEntry(slug);
  } catch (e) {
    return NextResponse.json(
      {
        error: `Failed to remove from shop.ts: ${
          e instanceof Error ? e.message : String(e)
        }`,
      },
      { status: 500 }
    );
  }

  return NextResponse.json({ ok: true, slug });
}
