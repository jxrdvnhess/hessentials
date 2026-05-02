import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import { SHOP_PRODUCTS } from "../../../data/shop";
import { ShopEditList } from "./ShopEditList";

export const metadata: Metadata = {
  title: "Admin / Shop edit",
  robots: { index: false, follow: false },
};

/**
 * Admin shop edit index — Hessentials Shop.
 *
 * Lists every product in SHOP_PRODUCTS with per-row Edit / Delete
 * actions. Edit links to /admin/shop-edit/<slug>. Delete fires a
 * client-side confirm and calls the DELETE route.
 *
 * Dev-only — 404 in production.
 */
export const dynamic = "force-dynamic";

export default function AdminShopEditPage() {
  if (process.env.NODE_ENV === "production") notFound();

  const items = [...SHOP_PRODUCTS]
    .map((p) => ({
      slug: p.slug,
      name: p.name,
      brand: p.brand,
      category: p.category,
      subcategory: p.subcategory ?? "",
      priceRange: p.priceRange,
      reason: p.reason.trim(),
      hasReason: p.reason.trim().length > 0,
    }))
    .sort((a, b) => a.brand.localeCompare(b.brand));

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <div className="mx-auto w-full max-w-6xl px-6 pt-12 pb-24 sm:px-10 md:pt-16">
        <header className="mb-10">
          <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45">
            Admin
          </p>
          <h1 className="mt-3 font-serif text-[clamp(1.75rem,3.5vw,2.5rem)] font-normal leading-[1.1] tracking-[-0.01em]">
            Shop edit
          </h1>
          <p className="mt-4 max-w-xl font-serif text-[15px] italic leading-[1.5] text-[#1f1d1b]/65">
            Every Shop listing in one place. Edit to refine. Delete
            removes the entry and its images.
          </p>
          <div className="mt-6 flex flex-wrap gap-3 text-[11px] uppercase tracking-[0.22em]">
            <Link
              href="/admin/shop-import"
              className="border border-[#1f1d1b]/30 px-4 py-2 text-[#1f1d1b] transition-colors hover:bg-[#1f1d1b] hover:text-[#f6f1e7]"
            >
              + Import new
            </Link>
            <Link
              href="/admin/migrate-categories"
              className="border border-[#1f1d1b]/15 px-4 py-2 text-[#1f1d1b]/65 transition-colors hover:border-[#1f1d1b]/30 hover:text-[#1f1d1b]"
            >
              Migrate categories
            </Link>
            <Link
              href="/admin/pricing"
              className="border border-[#1f1d1b]/15 px-4 py-2 text-[#1f1d1b]/65 transition-colors hover:border-[#1f1d1b]/30 hover:text-[#1f1d1b]"
            >
              Pricing
            </Link>
          </div>
          <p className="mt-6 font-serif text-[13px] italic text-[#1f1d1b]/55">
            {items.length} products. {items.filter((i) => !i.hasReason).length}{" "}
            missing a reason.
          </p>
        </header>

        <ShopEditList items={items} />
      </div>
    </main>
  );
}
