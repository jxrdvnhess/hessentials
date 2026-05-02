import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { ImportClient } from "./ImportClient";
import { CATEGORY_TREE } from "../../../data/shop";

export const metadata: Metadata = {
  title: "Shop import — Admin",
  // Belt-and-suspenders. The page is unlinked and dev-only, but the
  // noindex pairs with the runtime 403 from the commit endpoint.
  robots: { index: false, follow: false },
};

/**
 * Admin shop import surface — Hessentials Shop.
 *
 * Paste a product URL → fields stream in as the source page is fetched
 * and parsed. Pick a category, edit anything wrong, hit Commit. Images
 * download to /public/shop/<slug>-N.jpg and a new entry is appended to
 * SHOP_PRODUCTS in src/data/shop.ts. The `reason` field is left blank
 * for editorial fill-in.
 *
 * Dev-only. The page renders 404 in production; the underlying API
 * routes also refuse to run in production.
 */
export const dynamic = "force-dynamic";

export default function AdminShopImportPage() {
  if (process.env.NODE_ENV === "production") {
    notFound();
  }
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <div className="mx-auto w-full max-w-4xl px-6 pt-12 pb-24 sm:px-10 md:pt-16">
        <header className="mb-10">
          <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45">
            Admin
          </p>
          <h1 className="mt-3 font-serif text-[clamp(1.75rem,3.5vw,2.5rem)] font-normal leading-[1.1] tracking-[-0.01em]">
            Shop import
          </h1>
          <p className="mt-4 max-w-xl font-serif text-[15px] italic leading-[1.5] text-[#1f1d1b]/65">
            Paste a product URL. Fields populate as the source is read.
            Reason and category stay editorial.
          </p>
        </header>

        <ImportClient
          tree={Object.fromEntries(
            Object.entries(CATEGORY_TREE).map(([k, v]) => [
              k,
              [...v.subcategories],
            ])
          )}
        />
      </div>
    </main>
  );
}
