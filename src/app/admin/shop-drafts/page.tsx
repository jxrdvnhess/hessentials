import fs from "node:fs/promises";
import path from "node:path";
import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  SHOP_PRODUCTS,
  CATEGORY_TREE,
  CATEGORY_KEYS,
  categoryLabel,
} from "../../../data/shop";
import { ShopDraftsClient } from "./ShopDraftsClient";

export const metadata: Metadata = {
  title: "Admin / Shop drafts",
  robots: { index: false, follow: false },
};

/**
 * Admin shop drafts — Hessentials Shop.
 *
 * Lists every entry currently flagged `draft: true` in src/data/shop.ts.
 * Drafts are bulk-import staging records — they live here until a human
 * promotes them or sends them back. No autopublish; the only path to
 * public visibility is the Promote button per row.
 *
 * Below the drafts: a `Pending` section sourced from
 * `data/shop-import-pending.json`, which holds NEEDS HUMAN rows the
 * bulk import couldn't safely stage (insufficient images, mangled
 * names, draft-review prefix on Chateau's Thoughts).
 *
 * Page header surfaces the Editorial Standard product filter as a
 * mental checklist the reviewer should run before clicking Promote —
 * the filter is not enforced in code, only displayed. Product
 * judgment is editorial, not algorithmic. Restraint over volume.
 *
 * Dev-only — 404 in production.
 */
export const dynamic = "force-dynamic";

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

async function readPending(): Promise<PendingEntry[]> {
  const file = path.join(process.cwd(), "data", "shop-import-pending.json");
  try {
    const raw = await fs.readFile(file, "utf8");
    const parsed = JSON.parse(raw) as PendingFile;
    return parsed.entries ?? [];
  } catch {
    return [];
  }
}

export default async function AdminShopDraftsPage() {
  if (process.env.NODE_ENV === "production") notFound();

  const drafts = SHOP_PRODUCTS.filter((p) => p.draft === true).map((p) => ({
    slug: p.slug,
    name: p.name,
    brand: p.brand,
    category: p.category,
    subcategory: p.subcategory ?? "",
    audience: [...(p.audience ?? [])] as ("mens" | "womens")[],
    reason: p.reason,
    priceRange: p.priceRange,
    url: p.url,
    image: p.image,
    extractionMethod: p.extractionMethod ?? "manual",
    stabilityTier: p.stabilityTier,
    sourceArticle: undefined as string | undefined,
    sourceArticleUrl: undefined as string | undefined,
  }));

  const pending = await readPending();

  const tree: Record<string, string[]> = {};
  for (const [k, v] of Object.entries(CATEGORY_TREE)) {
    tree[k] = [...v.subcategories];
  }
  const categories = [...CATEGORY_KEYS].map((k) => ({
    key: k,
    label: categoryLabel(k),
  }));

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <div className="mx-auto w-full max-w-6xl px-6 pt-12 pb-24 sm:px-10 md:pt-16">
        <header className="mb-12">
          <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45">
            Admin
          </p>
          <h1 className="mt-3 font-serif text-[clamp(1.75rem,3.5vw,2.5rem)] font-normal leading-[1.1] tracking-[-0.01em]">
            Shop drafts
          </h1>
          <p className="mt-4 max-w-2xl font-serif text-[15px] italic leading-[1.5] text-[#1f1d1b]/65">
            Mechanically staged from the editorial audit. Nothing here
            is public yet. Promote one entry at a time, send the rest
            back. Restraint is the answer when it is.
          </p>
          <div className="mt-6 flex flex-wrap gap-3 text-[11px] uppercase tracking-[0.22em]">
            <Link
              href="/admin/shop-edit"
              className="border border-[#1f1d1b]/15 px-4 py-2 text-[#1f1d1b]/65 transition-colors hover:border-[#1f1d1b]/30 hover:text-[#1f1d1b]"
            >
              Live shop
            </Link>
            <Link
              href="/admin/shop-import"
              className="border border-[#1f1d1b]/15 px-4 py-2 text-[#1f1d1b]/65 transition-colors hover:border-[#1f1d1b]/30 hover:text-[#1f1d1b]"
            >
              Import one
            </Link>
          </div>

          {/* Editorial Standard product filter — read before promoting. */}
          <section className="mt-10 border-l border-[#1f1d1b]/15 pl-6">
            <p className="text-[10px] uppercase tracking-[0.28em] text-[#1f1d1b]/55">
              Product filter
            </p>
            <p className="mt-3 max-w-2xl font-serif text-[13px] italic leading-[1.55] text-[#1f1d1b]/70">
              Before promoting any object, ask:
            </p>
            <ul className="mt-3 max-w-2xl space-y-2 font-serif text-[14px] leading-[1.5] text-[#1f1d1b]/80">
              <li>
                Would this still feel correct if no commission existed?
              </li>
              <li>
                Would this still feel tasteful if it stopped trending
                tomorrow?
              </li>
              <li>Does this object deepen the article&apos;s argument?</li>
              <li>
                Does this feel discovered through discernment or surfaced
                through algorithms?
              </li>
              <li>
                Does this feel like a thing someone quietly keeps for
                years?
              </li>
            </ul>
            <p className="mt-4 max-w-2xl font-serif text-[12px] italic leading-[1.55] text-[#1f1d1b]/55">
              If the answer weakens at any point, do not promote.
            </p>
          </section>

          <p className="mt-8 font-serif text-[13px] italic text-[#1f1d1b]/55">
            {drafts.length} draft{drafts.length === 1 ? "" : "s"}
            {pending.length > 0 && ` · ${pending.length} pending`}
          </p>
        </header>

        <ShopDraftsClient
          drafts={drafts}
          pending={pending}
          categories={categories}
          tree={tree}
        />
      </div>
    </main>
  );
}
