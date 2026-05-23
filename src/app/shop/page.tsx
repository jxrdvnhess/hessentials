import type { Metadata } from "next";
import {
  SHOP_INTRO,
  SHOP_SUBTITLE,
  categoryLabel,
  type Category,
} from "../../data/shop";
import {
  LIVE_PRODUCTS,
  productsForPillar,
  productsForAtmosphere,
  representativeImageForAtmosphere,
} from "../../lib/shop";
import {
  LAUNCH_ATMOSPHERES,
  atmosphereSlug,
} from "../../data/atmospheres";
import ShopGallery from "../../components/ShopGallery";
import DrillDownHero, { type DrillBlock } from "../../components/DrillDownHero";

export const metadata: Metadata = {
  title: "Shop — Hessentials",
  description:
    "Things bought, used, and returned to. The ones that held up.",
  alternates: {
    canonical: "/shop",
  },
};

/**
 * 12-hour ISR. Same cadence as the live pricing layer. The mosaic
 * randomizes on the client so each visit feels fresh without
 * thrashing source sites or invalidating the static cache.
 */
export const revalidate = 43200;

/**
 * Pillar order for the drill-down hero on `/shop`. Hand-curated.
 * Mirrors Chateau's eight approved top-level categories. Pillars
 * with zero matching products are hidden via the filter below.
 */
const LANDING_PILLARS: readonly Category[] = [
  "mens",
  "womens",
  "accessories",
  "grooming",
  "home",
  "cooking",
  "travel",
  "provisions",
];

/** First product in a pillar that has a primary image — used as the hero hover image. */
function representativeImage(pillar: Category): string | undefined {
  const first = productsForPillar(pillar).find((p) => p.image);
  return first?.image;
}

export default function ShopPage() {
  const pillarBlocks: DrillBlock[] = LANDING_PILLARS
    // Hide pillars with zero matching products. WOMENS reveals
    // automatically once at least one product lands.
    .filter((p) => productsForPillar(p).length > 0)
    .map((p) => ({
      label: categoryLabel(p),
      href: `/shop/${p}`,
      image: representativeImage(p),
    }));

  // Atmosphere blocks — Chateau's launch-facing list. Atmospheres
  // with zero matching products are hidden so the surface always
  // reflects what's actually in the archive. Per Chateau's
  // 2026-05-15 audit: atmosphere is the emotional front door;
  // categories sit underneath as the operational backbone.
  const atmosphereBlocks: DrillBlock[] = LAUNCH_ATMOSPHERES.filter(
    (name) => productsForAtmosphere(name).length > 0
  ).map((name) => ({
    label: name,
    href: `/shop/atmosphere/${atmosphereSlug(name)}`,
    image: representativeImageForAtmosphere(name),
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
        <h1 className="mt-6 mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px] font-normal">
          Shop
        </h1>
        <p className="font-serif text-[clamp(1.125rem,1.6vw,1.25rem)] italic leading-[1.4] text-[#1f1d1b]/70">
          {SHOP_INTRO}
        </p>
        <p className="mx-auto mt-5 max-w-md font-serif text-[13px] leading-[1.6] text-[#1f1d1b]/55 sm:text-[14px]">
          {SHOP_SUBTITLE}
        </p>
      </section>

      {/* ---------- Atmosphere — the emotional front door ----------
          Cards grouped by atmosphere collection. Cuts across
          operational categories: Snow Peak's titanium mug appears in
          Soft Travel, Morning Ritual, Portable Ritual, etc. simultane-
          ously. Per Chateau's 2026-05-15 audit, this is now the lead
          surface; categories sit beneath. */}
      <DrillDownHero eyebrow="By atmosphere" blocks={atmosphereBlocks} />

      {/* ---------- Gallery wall ----------
          Framed plates on the cream page. Standard page margins,
          no bleed. ShopGallery handles randomization, asymmetric
          placement, parallax, and hover. */}
      <section
        aria-label="All products"
        className="mx-auto w-full max-w-7xl px-6 pb-32 sm:px-10 md:pb-40"
      >
        <ShopGallery products={[...LIVE_PRODUCTS]} />
      </section>

      {/* ---------- Pillar drill-down ----------
          Operational categories — the secondary navigation surface.
          Atmosphere leads emotionally; categories handle the
          "I know what I want" reader. */}
      <DrillDownHero eyebrow="Browse by category" blocks={pillarBlocks} />
    </main>
  );
}
