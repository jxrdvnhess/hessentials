import Image from "next/image";
import type { Metadata } from "next";
import {
  SHOP_CATEGORIES,
  SHOP_INTRO,
  type ShopProduct,
} from "../../data/shop";

export const metadata: Metadata = {
  title: "Shop — Hessentials",
  description:
    "A curated edit of products that have stayed. Things bought, used, and returned to — because they actually work in real life.",
};

function ProductCard({ product }: { product: ShopProduct }) {
  return (
    <article className="group">
      <a
        href={product.url}
        target="_blank"
        rel="noopener noreferrer"
        aria-label={`${product.brand} — ${product.name}, view item`}
        className="block"
      >
        <div className="relative aspect-[4/5] w-full overflow-hidden bg-[#ebe7df]">
          {/* Quiet placeholder behind the image — visible until the file lands. */}
          <div className="absolute inset-0 flex items-center justify-center px-6 text-center">
            <span className="font-serif text-[clamp(0.95rem,1.2vw,1.125rem)] italic leading-[1.4] text-[#1f1d1b]/35">
              {product.brand}
            </span>
          </div>
          <Image
            src={product.image}
            alt={`${product.brand} — ${product.name}`}
            fill
            sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 90vw"
            className="object-cover transition-transform duration-700 ease-out group-hover:scale-[1.02]"
          />
        </div>
      </a>

      <div className="mt-6">
        <h3 className="font-serif text-[clamp(1.05rem,1.5vw,1.25rem)] font-normal leading-[1.3] tracking-[-0.01em] text-[#1f1d1b]">
          {product.name}
        </h3>
        <div className="mt-2 flex items-baseline justify-between gap-4">
          <p className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/55 sm:text-[12px]">
            {product.brand}
          </p>
          <span
            aria-label="Price range"
            className="font-serif text-[14px] tracking-[0.04em] text-[#1f1d1b]/55"
          >
            {product.priceRange}
          </span>
        </div>
        <p className="mt-4 text-pretty font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/80 sm:text-[17px]">
          {product.reason}
        </p>
        <a
          href={product.url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-5 inline-flex items-baseline gap-2 text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/65 transition-colors duration-500 ease-out hover:text-[#1f1d1b] sm:text-[12px]"
        >
          View Item
          <span aria-hidden className="text-[12px]">
            →
          </span>
        </a>
      </div>
    </article>
  );
}

export default function ShopPage() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ---------- */}
      <section className="mx-auto w-full max-w-2xl px-6 pt-16 pb-10 text-center sm:px-10 md:pt-24">
        <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
          Shop
        </p>
        <div className="mx-auto max-w-xl space-y-4 text-pretty font-serif text-[clamp(1.125rem,1.8vw,1.375rem)] italic leading-[1.45] text-[#1f1d1b]/75">
          {SHOP_INTRO.split(/\n\s*\n/).map((p, i) => (
            <p key={i}>{p}</p>
          ))}
        </div>
      </section>

      {/* ---------- Categories ---------- */}
      <div className="mx-auto w-full max-w-7xl px-6 pb-32 sm:px-10 md:pb-40">
        {SHOP_CATEGORIES.map((category, idx) => (
          <section
            key={category.slug}
            id={category.slug}
            aria-labelledby={`${category.slug}-heading`}
            className={
              idx === 0
                ? "pt-12 sm:pt-16"
                : "pt-20 sm:pt-28"
            }
          >
            <header className="mb-10 flex flex-col items-center gap-3 text-center sm:mb-12 sm:flex-row sm:items-baseline sm:justify-between sm:gap-x-8 sm:text-left">
              <div className="flex items-baseline gap-x-5">
                <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/45 sm:text-[12px]">
                  {category.number}
                </p>
                <h2
                  id={`${category.slug}-heading`}
                  className="font-serif text-[clamp(1.625rem,3vw,2.25rem)] font-normal leading-[1.1] tracking-[-0.02em] text-balance"
                >
                  {category.name}
                </h2>
              </div>
              <p className="text-pretty max-w-md font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[16px]">
                {category.pov}
              </p>
            </header>

            <ul className="grid grid-cols-2 gap-x-6 gap-y-12 sm:grid-cols-3 sm:gap-x-8 sm:gap-y-14 lg:grid-cols-4 lg:gap-x-10">
              {category.products.map((product) => (
                <li key={product.slug}>
                  <ProductCard product={product} />
                </li>
              ))}
            </ul>
          </section>
        ))}
      </div>
    </main>
  );
}
