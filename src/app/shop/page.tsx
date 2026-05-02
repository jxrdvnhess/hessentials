import type { Metadata } from "next";
import {
  SHOP_INTRO,
  SHOP_PRODUCTS,
  SHOP_SUBTITLE,
  categoryLabel,
  type Category,
} from "../../data/shop";
import { productsForPillar } from "../../lib/shop";
import ShopMosaic from "../../components/ShopMosaic";
import DrillDownHero, { type DrillBlock } from "../../components/DrillDownHero";

export const metadata: Metadata = {
  title: "Shop — Hessentials",
  description:
    "Things bought, used, and returned to. The ones that held up.",
};

/**
 * 12-hour ISR. Same cadence as the live pricing layer. The mosaic
 * randomizes on the client so each visit feels fresh without
 * thrashing source sites or invalidating the static cache.
 */
export const revalidate = 43200;

/**
 * Pillar order for the drill-down hero on `/shop`. Hand-curated to
 * match the persistent menu (which also excludes Provisions and
 * Womens at launch).
 */
const LANDING_PILLARS: readonly Category[] = [
  "mens",
  "accessories",
  "grooming",
  "travel",
  "home",
];

/** First product in a pillar that has a primary image — used as the hero hover image. */
function representativeImage(pillar: Category): string | undefined {
  const first = productsForPillar(pillar).find((p) => p.image);
  return first?.image;
}

export default function ShopPage() {
  const blocks: DrillBlock[] = LANDING_PILLARS.map((p) => ({
    label: categoryLabel(p),
    href: `/shop/${p}`,
    image: representativeImage(p),
  }));

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ----------
          Reduced version of the previous /shop intro. The mosaic
          carries the page; the intro lines up the brand voice and
          steps aside. */}
      <section className="mx-auto flex w-full max-w-2xl flex-col items-center px-6 pt-12 pb-10 text-center sm:px-10 sm:pt-16 sm:pb-14">
        <span
          aria-hidden
          className="block w-20"
          style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
        />
        <p className="mt-6 mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
          Shop
        </p>
        <p className="font-serif text-[clamp(1.125rem,1.6vw,1.25rem)] italic leading-[1.4] text-[#1f1d1b]/70">
          {SHOP_INTRO}
        </p>
        <p className="mx-auto mt-5 max-w-md font-serif text-[13px] leading-[1.6] text-[#1f1d1b]/55 sm:text-[14px]">
          {SHOP_SUBTITLE}
        </p>
      </section>

      {/* ---------- Mosaic ----------
          Full-bleed asymmetric grid. Edges run to the viewport so
          the imagery carries. ShopMosaic handles randomization,
          parallax, and hover overlays. */}
      <section aria-label="All products" className="px-1 sm:px-1.5">
        <ShopMosaic products={SHOP_PRODUCTS} />
      </section>

      {/* ---------- Drill-down hero ---------- */}
      <DrillDownHero eyebrow="Browse by pillar" blocks={blocks} />
    </main>
  );
}
