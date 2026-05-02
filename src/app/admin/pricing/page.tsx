import type { Metadata } from "next";
import { SHOP_PRODUCTS } from "../../../data/shop";
import { fetchAllPrices } from "../../../lib/pricing/fetchPrice";
import { PricingTable, type PricingRow } from "./PricingTable";

export const metadata: Metadata = {
  title: "Admin / Pricing",
  // Keep this page out of any crawler index. It's not linked from the
  // public site but the noindex/nofollow is belt-and-suspenders.
  robots: { index: false, follow: false },
};

/**
 * Admin pricing surface — Hessentials Shop.
 *
 * Not linked from the public site. Lives at /admin/pricing for Jordan
 * to spot-check the live pricing system: which extractor each product
 * is using, the resolved display string, the verified date, and any
 * error message that produced a fallback.
 *
 * Force-dynamic so every visit re-fetches every product. The grid and
 * detail pages still use the 12h ISR cycle for the public surface;
 * this page is intentionally heavier so failed extractors surface
 * immediately when checked.
 */
export const dynamic = "force-dynamic";

export default async function AdminPricingPage() {
  const prices = await fetchAllPrices(SHOP_PRODUCTS);

  // Sort: errors first, then live, then manual. Errors surface fastest.
  const rows = SHOP_PRODUCTS.map((p) => ({
    product: p,
    price: prices[p.slug],
  })).sort((a, b) => {
    const score = (r: (typeof rows)[number]) => {
      if (r.price.error) return 0;
      if (r.price.live) return 1;
      return 2;
    };
    return score(a) - score(b);
  });

  const errorCount = rows.filter((r) => r.price.error).length;
  const liveCount = rows.filter((r) => r.price.live && !r.price.error).length;
  const manualCount = rows.length - errorCount - liveCount;

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <div className="mx-auto w-full max-w-6xl px-6 pt-12 pb-24 sm:px-10 md:pt-16">
        <header className="mb-10">
          <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45">
            Admin
          </p>
          <h1 className="mt-3 font-serif text-[clamp(1.75rem,3.5vw,2.5rem)] font-normal leading-[1.1] tracking-[-0.01em]">
            Pricing
          </h1>
          <p className="mt-4 max-w-xl font-serif text-[15px] italic leading-[1.5] text-[#1f1d1b]/65">
            Live state of every Shop listing. Errors surface here, not
            on the public page.
          </p>

          <dl className="mt-8 flex flex-wrap gap-x-10 gap-y-3 text-[12px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
            <div className="flex items-baseline gap-2">
              <dt>Live</dt>
              <dd className="font-serif text-[15px] tracking-normal text-[#1f1d1b]">
                {liveCount}
              </dd>
            </div>
            <div className="flex items-baseline gap-2">
              <dt>Manual</dt>
              <dd className="font-serif text-[15px] tracking-normal text-[#1f1d1b]">
                {manualCount}
              </dd>
            </div>
            <div className="flex items-baseline gap-2">
              <dt>Errors</dt>
              <dd className="font-serif text-[15px] tracking-normal text-[#1f1d1b]">
                {errorCount}
              </dd>
            </div>
          </dl>
        </header>

        <PricingTable
          rows={rows.map<PricingRow>(({ product, price }) => ({
            slug: product.slug,
            name: product.name,
            brand: product.brand,
            method: price.method,
            display: price.display,
            live: price.live,
            soldOut: price.soldOut,
            error: price.error ?? null,
            lastVerified: price.lastVerified ?? null,
          }))}
        />
      </div>
    </main>
  );
}
