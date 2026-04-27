import Link from "next/link";
import { notFound } from "next/navigation";
import type { Metadata } from "next";
import { SHOP_PRODUCTS, getProductBySlug } from "../../../data/shop";
import { getShopEssay } from "../../../lib/shop";
import ProductGallery from "../../../components/ProductGallery";

type Params = { slug: string };

export function generateStaticParams() {
  return SHOP_PRODUCTS.map((p) => ({ slug: p.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug } = await params;
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
  const product = getProductBySlug(slug);
  if (!product) notFound();

  const essay = await getShopEssay(slug);

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
              {product.category}
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

            <p className="mt-8 font-serif text-[15px] tracking-[0.04em] text-[#1f1d1b]/55">
              {product.priceRange}
            </p>

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

              <p className="max-w-xs text-[10px] uppercase tracking-[0.22em] leading-[1.7] text-[#1f1d1b]/35 sm:text-[11px]">
                Hessentials may earn a small commission.{" "}
                <Link
                  href="/affiliate-disclosure"
                  className="underline decoration-[#1f1d1b]/25 underline-offset-[3px] transition-colors duration-500 ease-out hover:decoration-[#1f1d1b]/60"
                >
                  Disclosure
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
    </main>
  );
}
