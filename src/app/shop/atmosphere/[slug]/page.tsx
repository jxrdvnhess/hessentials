import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  LAUNCH_ATMOSPHERES,
  atmosphereSlug,
  atmosphereNameFromSlug,
} from "../../../../data/atmospheres";
import { productsForAtmosphere } from "../../../../lib/shop";
import { fetchAllPrices } from "../../../../lib/pricing/fetchPrice";
import { ProductCard } from "../../../../components/ProductCard";

/**
 * `/shop/atmosphere/<slug>` — atmosphere collection landing page.
 *
 * Atmosphere collections are emotional groupings that cut across the
 * operational category tree. This route renders every live product
 * whose `atmosphereCollection` array contains the named atmosphere,
 * regardless of category.
 *
 * Per Chateau's 2026-05-15 post-live audit:
 *
 *   "Atmosphere collections should become the emotional front door.
 *   Operational categories remain necessary, but they should no longer
 *   dominate the experience emotionally."
 *
 * Pre-renders the launch-facing atmospheres at build time via
 * `generateStaticParams`; renders any other atmosphere name found in
 * products' `atmosphereCollection` arrays on demand.
 *
 * 12-hour ISR matching the rest of the Shop.
 */

export const revalidate = 43200;

type Params = { slug: string };

export function generateStaticParams() {
  return LAUNCH_ATMOSPHERES.map((name) => ({ slug: atmosphereSlug(name) }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug } = await params;
  const name = atmosphereNameFromSlug(slug);
  if (!name) return { title: "Shop — Hessentials" };
  return {
    title: `${name} — Shop — Hessentials`,
    description: `Objects in the ${name} atmosphere — chosen for emotional coherence, not category.`,
  };
}

export default async function AtmospherePage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  const name = atmosphereNameFromSlug(slug);
  if (!name) notFound();

  const products = productsForAtmosphere(name);
  if (products.length === 0) notFound();

  const prices = await fetchAllPrices(products);

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Top — breadcrumb ---------- */}
      <nav
        aria-label="Breadcrumb"
        className="mx-auto w-full max-w-7xl px-6 pt-10 sm:px-10 md:px-16 md:pt-12"
      >
        <ol className="flex flex-wrap items-baseline gap-x-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[11px]">
          <li>
            <Link
              href="/shop"
              className="inline-flex items-baseline gap-2 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/80"
            >
              <span aria-hidden>←</span>
              Shop
            </Link>
          </li>
          <li className="flex items-baseline gap-2">
            <span aria-hidden className="text-[#1f1d1b]/25">
              /
            </span>
            <span>Atmosphere</span>
          </li>
        </ol>
      </nav>

      {/* ---------- Title spread ---------- */}
      <section className="mx-auto w-full max-w-3xl px-6 pt-12 pb-12 text-center sm:px-10 md:pt-16 md:pb-16">
        <p className="text-[10px] uppercase tracking-[0.28em] text-[#1f1d1b]/45 sm:text-[11px]">
          Atmosphere
        </p>
        <h1 className="mt-4 font-serif text-[clamp(2rem,4vw,3rem)] font-normal leading-[1.05] tracking-[-0.01em]">
          {name}
        </h1>
        <p className="mx-auto mt-5 max-w-md font-serif text-[14px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[15px]">
          {products.length} {products.length === 1 ? "object" : "objects"} across the archive that share this emotional weather.
        </p>
      </section>

      {/* ---------- Grid ---------- */}
      <section className="mx-auto w-full max-w-7xl px-6 pb-32 sm:px-10 md:pb-40">
        <ul className="grid grid-cols-1 gap-x-6 gap-y-12 sm:grid-cols-2 sm:gap-x-8 sm:gap-y-14 lg:grid-cols-3 lg:gap-x-10 lg:gap-y-16">
          {products.map((product) => {
            const fetched = prices[product.slug];
            const price = fetched ?? {
              display: product.priceRange,
              live: false,
              soldOut: false,
              method: "manual" as const,
            };
            return (
              <li key={product.slug}>
                <ProductCard product={product} price={price} />
              </li>
            );
          })}
        </ul>
      </section>
    </main>
  );
}
