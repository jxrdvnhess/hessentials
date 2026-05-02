/**
 * PillarView — server component that renders the `/shop/<pillar>`
 * surface. Same two-section structure as the `/shop` landing
 * (mosaic + drill-down hero), but everything is filtered to the
 * pillar in question.
 *
 * The drill-down on a pillar page lists subcategories instead of
 * pillars. The first block is always `All <Pillar>` linking back
 * to the same pillar overview (matches the persistent menu's
 * dropdown affordance).
 *
 * Live at `/shop/<pillar>` via the parent route's branch — the
 * parent page chooses between this and product detail based on
 * whether the segment matches a CATEGORY_KEY.
 */

import {
  categoryLabel,
  subcategoryLabel,
  type Category,
} from "../../../data/shop";
import {
  productsForPillar,
  productsForSubcategory,
  subcategoriesPresentForPillar,
} from "../../../lib/shop";
import ShopMosaic from "../../../components/ShopMosaic";
import DrillDownHero, {
  type DrillBlock,
} from "../../../components/DrillDownHero";

export default function PillarView({ pillar }: { pillar: Category }) {
  const products = productsForPillar(pillar);
  const subs = subcategoriesPresentForPillar(pillar);

  // First product per subcategory whose image is set — used as the
  // hover image for the drill-down block.
  const subImage = (sub: string): string | undefined => {
    const first = productsForSubcategory(pillar, sub).find((p) => p.image);
    return first?.image;
  };

  // First product overall — used as the hero image for the "All <Pillar>" block.
  const allImage = products.find((p) => p.image)?.image;

  const blocks: DrillBlock[] = [
    {
      label: `All ${categoryLabel(pillar)}`,
      href: `/shop/${pillar}`,
      image: allImage,
    },
    ...subs.map((sub) => ({
      label: subcategoryLabel(sub),
      href: `/shop/${pillar}/${sub}`,
      image: subImage(sub),
    })),
  ];

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro — pillar name as the page heading ---------- */}
      <section className="mx-auto flex w-full max-w-2xl flex-col items-center px-6 pt-12 pb-10 text-center sm:px-10 sm:pt-16 sm:pb-14">
        <span
          aria-hidden
          className="block w-20"
          style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
        />
        <p className="mt-6 mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
          Shop
        </p>
        <h1 className="font-serif text-[clamp(2rem,4.5vw,3rem)] font-normal leading-[1.05] tracking-[-0.01em]">
          {categoryLabel(pillar)}
        </h1>
        <p className="mx-auto mt-5 max-w-md font-serif text-[13px] leading-[1.6] text-[#1f1d1b]/55 sm:text-[14px]">
          {products.length} {products.length === 1 ? "piece" : "pieces"}.
        </p>
      </section>

      {/* ---------- Mosaic ---------- */}
      <section
        aria-label={`${categoryLabel(pillar)} products`}
        className="px-1 sm:px-1.5"
      >
        <ShopMosaic products={products} />
      </section>

      {/* ---------- Drill-down hero (subcategories) ---------- */}
      {subs.length > 0 && (
        <DrillDownHero eyebrow="Browse by subcategory" blocks={blocks} />
      )}
    </main>
  );
}
