import type { Metadata } from "next";
import { SHOP_INTRO } from "../../data/shop";
import ShopGrid from "../../components/ShopGrid";

export const metadata: Metadata = {
  title: "Shop — Hessentials",
  description:
    "Things bought, used, and returned to. The ones that held up.",
};

export default function ShopPage() {
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
      </section>

      {/* ---------- Filter + Grid ---------- */}
      <div className="mx-auto w-full max-w-7xl px-6 pt-8 pb-32 sm:px-10 sm:pt-12 md:pb-40">
        <ShopGrid />
      </div>
    </main>
  );
}
