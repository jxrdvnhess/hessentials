import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import {
  CATEGORY_KEYS,
  SHOP_PRODUCTS,
  getProductBySlug,
  categoryLabel,
  subcategoryLabel,
  type Category,
} from "../../../data/shop";
import { getShopEssay } from "../../../lib/shop";
import { fetchProductPrice } from "../../../lib/pricing/fetchPrice";
import { formatVerifiedDate } from "../../../lib/pricing/format";
import ProductGallery from "../../../components/ProductGallery";
import JsonLd from "../../../components/JsonLd";
import { productSchema } from "../../../lib/jsonLd";
import PillarView from "./PillarView";

type Params = { slug: string };

/**
 * Same dynamic segment serves two surfaces: pillar pages
 * (`/shop/<pillar>`) and product detail (`/shop/<slug>`). The
 * brief specifies this URL shape; we branch on whether the value
 * matches a CATEGORY_KEY rather than splitting routes.
 */
const PILLAR_SET: ReadonlySet<string> = new Set<string>(CATEGORY_KEYS);
function isPillar(value: string): value is Category {
  return PILLAR_SET.has(value);
}

/**
 * 12-hour ISR (43200 seconds). Detail pages regenerate so the live
 * price + verified date stay fresh without hitting the source on
 * every render.
 *
 * Next.js requires this to be a literal — see the matching constant
 * `PRICING_REVALIDATE_SECONDS` in `src/lib/pricing/fetchPrice.ts`;
 * keep the two in sync.
 */
export const revalidate = 43200;

export function generateStaticParams() {
  // Both pillar pages and product detail pages share this dynamic
  // segment — pre-render both sets so SSG covers everything.
  return [
    ...CATEGORY_KEYS.map((slug) => ({ slug })),
    ...SHOP_PRODUCTS.map((p) => ({ slug: p.slug })),
  ];
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug } = await params;
  if (isPillar(slug)) {
    return {
      title: `${categoryLabel(slug)} — Shop — Hessentials`,
    };
  }
  const product = getProductBySlug(slug);
  if (!product) return { title: "Shop — Hessentials" };

  return {
    title: `${product.name} — ${product.brand} — Hessentials`,
    description: product.reason,
    openGraph: {
      title: `${product.name} — ${product.brand}`,
      description: product.reason,
      images: [{ url: product.image }],
      type: "article",
    },
  };
}

export default async function ShopProductPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  // Pillar branch — when the segment matches a CATEGORY_KEY, render
  // the pillar surface (mosaic + subcategory drill-down) instead of
  // a product detail page.
  if (isPillar(slug)) {
    return <PillarView pillar={slug} />;
  }

  const product = getProductBySlug(slug);
  if (!product) notFound();

  const [essay, price] = await Promise.all([
    getShopEssay(slug),
    fetchProductPrice(product),
  ]);

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Top — back link ---------- */}
      <div className="mx-auto w-full max-w-7xl px-6 pt-10 sm:px-10 md:px-16 md:pt-12">
        <Link
          href="/shop"
          className="inline-flex items-baseline gap-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/80 sm:text-[11px]"
        >
          <span aria-hidden>←</span>
          Shop
        </Link>
      </div>

      {/* ---------- Spread — image + meta side-by-side ---------- */}
      <section className="mx-auto w-full max-w-7xl px-6 pt-10 pb-16 sm:px-10 md:px-16 md:pt-16 md:pb-24">
        <div className="grid items-start gap-x-12 gap-y-12 md:grid-cols-12 md:gap-x-16">
          {/* Image */}
          <div className="md:col-span-7">
            <ProductGallery
              images={product.images ?? [product.image]}
              alt={`${product.brand} — ${product.name}`}
              fallback={product.brand}
            />
          </div>

          {/* Meta */}
          <div className="md:col-span-5 md:sticky md:top-24">
            <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/45 sm:text-[12px]">
              {categoryLabel(product.category)}
              {product.subcategory ? (
                <>
                  <span aria-hidden className="mx-2 text-[#1f1d1b]/25">
                    /
                  </span>
                  {subcategoryLabel(product.subcategory)}
                </>
              ) : null}
            </p>

            <p className="mt-6 text-[12px] uppercase tracking-[0.24em] text-[#1f1d1b]/55 sm:text-[13px]">
              {product.brand}
            </p>

            <h1 className="mt-3 font-serif text-[clamp(2rem,4.5vw,3.25rem)] font-normal leading-[1.05] tracking-[-0.02em] text-balance">
              {product.name}
            </h1>

            <p className="mt-6 max-w-md font-serif text-[clamp(1.125rem,1.5vw,1.25rem)] italic leading-[1.5] text-[#1f1d1b]/75">
              {product.reason}
            </p>

            {price.soldOut ? (
              // Sold-out reads as a small uppercase aside — same
              // register as the category label above, so it doesn't
              // shout. The CTA below still links out (the page may
              // restock).
              <p className="mt-8 text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/55 sm:text-[12px]">
                Sold out
              </p>
            ) : (
              <p className="mt-8 font-serif text-[15px] tracking-[0.04em] text-[#1f1d1b]/55">
                {price.display}
              </p>
            )}

            {/* Verified date — italic, small, beneath the price. Only
                renders for successful live fetches; manual / fallback
                listings stay quiet (no date is more honest than a
                stale one). */}
            {price.live && price.lastVerified && (
              <p className="mt-2 font-serif text-[12px] italic leading-[1.4] text-[#1f1d1b]/40 sm:text-[13px]">
                Last verified {formatVerifiedDate(price.lastVerified)}
              </p>
            )}

            <div className="mt-10 flex flex-col items-start gap-4">
              <a
                href={product.url}
                target="_blank"
                rel="noopener noreferrer"
                className="group inline-flex items-baseline gap-3 border-b border-[#1f1d1b]/30 pb-2 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b] transition-colors duration-500 ease-out hover:border-[#1f1d1b] sm:text-[12px]"
              >
                View at {product.brand}
                <span aria-hidden className="text-[12px]">
                  →
                </span>
              </a>

              {/* Affiliate disclosure — sits directly below the
                  primary buy link per FTC proximity guidance. Quiet
                  but legible: sentence-case serif, /55 opacity. Not
                  a warning banner, not a footnote. */}
              <p className="max-w-sm font-serif text-[12px] leading-[1.6] text-[#1f1d1b]/55 sm:text-[13px]">
                This page contains affiliate links. Hessentials may earn a
                commission at no cost to you.{" "}
                <Link
                  href="/affiliate-disclosure"
                  className="underline decoration-[#1f1d1b]/30 underline-offset-[3px] transition-colors duration-500 ease-out hover:decoration-[#1f1d1b]/70"
                >
                  Full disclosure
                </Link>
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ---------- Essay (optional) ---------- */}
      {essay && (
        <section className="px-6 pb-32 sm:px-10 md:px-16 md:pb-40">
          <div className="mx-auto w-full max-w-2xl">
            <div className="mb-12 flex justify-center md:mb-16">
              <span
                aria-hidden
                className="font-serif text-[18px] text-[#1f1d1b]/30"
              >
                —
              </span>
            </div>
            <article
              className="prose-editorial"
              dangerouslySetInnerHTML={{ __html: essay.html }}
            />
          </div>
        </section>
      )}

      {/* ---------- Bottom — onward ---------- */}
      <nav
        aria-label="Continue browsing"
        className="mx-auto mt-32 mb-24 max-w-2xl px-6 text-center sm:mt-40 sm:px-10 md:mt-48 md:mb-32"
      >
        <Link
          href="/shop"
          className="inline-flex items-baseline gap-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/80 sm:text-[11px]"
        >
          <span aria-hidden>←</span>
          Shop
        </Link>
        <p className="mt-6 font-serif text-[15px] italic leading-[1.6] text-[#1f1d1b]/50 sm:text-[16px]">
          More worth keeping.
        </p>
      </nav>

      {/* Product structured data — surfaces price + brand + image
          in shopping-related rich results. Uses the curated
          priceRange (single → Offer, range → AggregateOffer); see
          jsonLd.ts for the parsing rationale. */}
      <JsonLd
        data={productSchema({
          url: `/shop/${product.slug}`,
          product,
        })}
      />
    </main>
  );
}
