import type { Metadata } from "next";
import Link from "next/link";
import Image from "next/image";
import { notFound } from "next/navigation";
import {
  CATEGORY_KEYS,
  categoryLabel,
  subcategoryLabel,
  type Category,
} from "../../../../data/shop";
import { productsForSubcategory } from "../../../../lib/shop";
import { fetchAllPrices } from "../../../../lib/pricing/fetchPrice";

/**
 * `/shop/<pillar>/<subcategory>` — the deepest level of the Shop
 * hierarchy. Renders a clean product grid only: no mosaic, no
 * drill-down hero. The persistent Shop menu (in the layout) still
 * carries the pillar/subcategory context as a breadcrumb at the top.
 *
 * Validation: the slug segment must match a CATEGORY_KEY (otherwise
 * it's a product detail under `/shop/[slug]`, and the second
 * segment makes no sense). Returns notFound for non-pillar parents.
 *
 * Empty state: pillar exists but no products live under that
 * subcategory yet. Renders a quiet "Nothing here yet." rather than
 * a 404 — this matches the public shop's empty-filter state.
 */

const PILLAR_SET: ReadonlySet<string> = new Set<string>(CATEGORY_KEYS);
function isPillar(value: string): value is Category {
  return PILLAR_SET.has(value);
}

type Params = { slug: string; subcategory: string };

export const revalidate = 43200;

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug, subcategory } = await params;
  if (!isPillar(slug)) return { title: "Shop — Hessentials" };
  return {
    title: `${subcategoryLabel(subcategory)} — ${categoryLabel(
      slug
    )} — Shop — Hessentials`,
  };
}

export default async function ShopSubcategoryPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug, subcategory } = await params;
  if (!isPillar(slug)) notFound();

  const products = productsForSubcategory(slug, subcategory);
  const prices = await fetchAllPrices(products);

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <section className="mx-auto flex w-full max-w-2xl flex-col items-center px-6 pt-12 pb-10 text-center sm:px-10 sm:pt-16 sm:pb-14">
        <span
          aria-hidden
          className="block w-20"
          style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
        />
        <p className="mt-6 mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
          {/* Breadcrumb-style eyebrow */}
          <Link
            href={`/shop/${slug}`}
            className="text-[#1f1d1b]/55 transition-colors duration-300 ease-out hover:text-[#1f1d1b]"
          >
            {categoryLabel(slug)}
          </Link>
          <span aria-hidden className="mx-3 text-[#1f1d1b]/30">
            ·
          </span>
          <span>Subcategory</span>
        </p>
        <h1 className="font-serif text-[clamp(2rem,4.5vw,3rem)] font-normal leading-[1.05] tracking-[-0.01em]">
          {subcategoryLabel(subcategory)}
        </h1>
        <p className="mx-auto mt-5 max-w-md font-serif text-[13px] leading-[1.6] text-[#1f1d1b]/55 sm:text-[14px]">
          {products.length}{" "}
          {products.length === 1 ? "piece" : "pieces"} under{" "}
          {categoryLabel(slug)}.
        </p>
      </section>

      <section className="mx-auto w-full max-w-7xl px-6 pb-32 sm:px-10 md:pb-40">
        {products.length === 0 ? (
          <p className="py-24 text-center font-serif text-[17px] italic text-[#1f1d1b]/55">
            Nothing here yet.
          </p>
        ) : (
          <ul className="grid grid-cols-1 gap-x-6 gap-y-12 sm:grid-cols-2 sm:gap-x-8 sm:gap-y-14 lg:grid-cols-3 lg:gap-x-10 lg:gap-y-16">
            {products.map((product) => {
              const price = prices[product.slug];
              return (
                <li key={product.slug}>
                  <article className="group">
                    <Link
                      href={`/shop/${product.slug}`}
                      className="block focus:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/40"
                    >
                      <div className="relative aspect-[4/5] w-full overflow-hidden bg-[#faf9f5]">
                        <Image
                          src={product.image}
                          alt={`${product.brand} — ${product.name}`}
                          fill
                          sizes="(min-width: 1024px) 30vw, (min-width: 640px) 45vw, 100vw"
                          className="object-contain p-3 transition-transform duration-500 ease-out group-hover:scale-[1.02] sm:p-4"
                        />
                      </div>
                      <div className="mt-5">
                        <h3 className="font-serif text-[clamp(1.05rem,1.5vw,1.25rem)] font-normal leading-[1.3] tracking-[-0.01em] text-[#1f1d1b]">
                          {product.name}
                        </h3>
                        <div className="mt-2 flex items-baseline justify-between gap-4">
                          <p className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/55 sm:text-[12px]">
                            {product.brand}
                          </p>
                          {price?.soldOut ? (
                            <span className="text-[10px] uppercase tracking-[0.24em] text-[#1f1d1b]/45">
                              Sold out
                            </span>
                          ) : (
                            <span className="font-serif text-[14px] tracking-[0.04em] text-[#1f1d1b]/55">
                              {price?.display ?? product.priceRange}
                            </span>
                          )}
                        </div>
                        <p className="mt-3 text-pretty font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/80 sm:text-[17px]">
                          {product.reason}
                        </p>
                      </div>
                    </Link>
                  </article>
                </li>
              );
            })}
          </ul>
        )}
      </section>
    </main>
  );
}
