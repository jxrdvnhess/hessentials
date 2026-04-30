import type { Metadata } from "next";
import { SHOP_PRODUCTS } from "../../../data/shop";
import { fetchAllPrices } from "../../../lib/pricing/fetchPrice";
import { formatVerifiedDate } from "../../../lib/pricing/format";

export const metadata: Metadata = {
  title: "Pricing — Admin",
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

        <div className="overflow-x-auto">
          <table className="w-full border-collapse text-left text-[14px] text-[#1f1d1b]">
            <thead>
              <tr className="border-b border-[#1f1d1b]/15 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
                <th className="py-3 pr-4 font-normal">Product</th>
                <th className="py-3 pr-4 font-normal">Method</th>
                <th className="py-3 pr-4 font-normal">Display</th>
                <th className="py-3 pr-4 font-normal">State</th>
                <th className="py-3 pr-4 font-normal">Verified</th>
                <th className="py-3 font-normal">Error</th>
              </tr>
            </thead>
            <tbody>
              {rows.map(({ product, price }) => (
                <tr
                  key={product.slug}
                  className="border-b border-[#1f1d1b]/8 align-top"
                >
                  <td className="py-3 pr-4">
                    <div className="font-serif text-[15px] leading-[1.3]">
                      {product.name}
                    </div>
                    <div className="mt-1 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/50">
                      {product.brand}
                    </div>
                  </td>
                  <td className="py-3 pr-4 text-[12px] uppercase tracking-[0.18em] text-[#1f1d1b]/65">
                    {price.method}
                  </td>
                  <td className="py-3 pr-4 font-serif text-[14px] text-[#1f1d1b]">
                    {price.display}
                  </td>
                  <td className="py-3 pr-4 text-[12px] uppercase tracking-[0.18em]">
                    {price.error ? (
                      <span className="text-[#a23a23]">Error</span>
                    ) : price.soldOut ? (
                      <span className="text-[#1f1d1b]/55">Sold out</span>
                    ) : price.live ? (
                      <span className="text-[#1f1d1b]">Live</span>
                    ) : (
                      <span className="text-[#1f1d1b]/55">Manual</span>
                    )}
                  </td>
                  <td className="py-3 pr-4 font-serif text-[13px] italic text-[#1f1d1b]/55">
                    {price.lastVerified
                      ? formatVerifiedDate(price.lastVerified)
                      : "—"}
                  </td>
                  <td className="py-3 max-w-md break-words font-mono text-[11px] leading-[1.4] text-[#a23a23]">
                    {price.error ?? ""}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </main>
  );
}
