import type { Metadata } from "next";
import { SHOP_INTRO, SHOP_PRODUCTS } from "../../data/shop";
import ShopGrid from "../../components/ShopGrid";
import { fetchAllPrices } from "../../lib/pricing/fetchPrice";

export const metadata: Metadata = {
  title: "Shop — Hessentials",
  description:
    "Things bought, used, and returned to. The ones that held up.",
};

/**
 * 12-hour ISR (43200 seconds). Shop index regenerates with every
 * revalidation cycle so live prices stay current without thrashing
 * source sites on every request.
 *
 * Next.js requires this to be a literal — see the matching constant
 * `PRICING_REVALIDATE_SECONDS` in `src/lib/pricing/fetchPrice.ts`;
 * keep the two in sync.
 */
export const revalidate = 43200;

export default async function ShopPage() {
  // Resolve every product's display price server-side. fetchAllPrices
  // never throws — failures fall back to the static priceRange — so the
  // grid always has a complete map.
  const prices = await fetchAllPrices(SHOP_PRODUCTS);

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ---------- */}
      <section className="mx-auto w-full max-w-2xl px-6 pt-16 pb-8 text-center sm:px-10 md:pt-24">
        <p className="mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
          Shop
        </p>
        <p className="font-serif text-[clamp(1.125rem,1.6vw,1.25rem)] italic leading-[1.4] text-[#1f1d1b]/70">
          {SHOP_INTRO}
        </p>
        {/* The price-tier legend ($ / $$ / $$$ / $$$$) was removed —
            redundant now that every card shows actual dollar amounts.
            The pt on the grid section below was bumped to preserve the
            breathing room above the category nav. */}
      </section>

      {/* ---------- Filter + Grid ---------- */}
      <div className="mx-auto w-full max-w-7xl px-6 pt-14 pb-32 sm:px-10 sm:pt-16 md:pb-40">
        <ShopGrid prices={prices} />
      </div>
    </main>
  );
}
