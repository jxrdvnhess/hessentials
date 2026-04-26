"use client";

import Image from "next/image";
import Link from "next/link";
import { useMemo, useState } from "react";
import {
  SHOP_CATEGORIES,
  SHOP_PRODUCTS,
  type ShopCategory,
  type ShopProduct,
} from "../data/shop";

/**
 * Shop grid with an inline editorial filter row.
 *
 * The grid is a single curated array — categories are tags, not sections.
 * The filter narrows what's visible without rearranging order.
 */

type Filter = ShopCategory | "All";

const ALL_FILTERS: readonly Filter[] = ["All", ...SHOP_CATEGORIES] as const;

function ProductCard({ product }: { product: ShopProduct }) {
  const detailHref = `/shop/${product.slug}`;
  return (
    <article className="group">
      <Link
        href={detailHref}
        aria-label={`${product.brand} — ${product.name}, read more`}
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
            sizes="(min-width: 1024px) 25vw, (min-width: 640px) 33vw, 50vw"
            // Bypass Next's server-side fetch — some brand CDNs (Aveda, Omega,
            // others likely) reject non-browser requests, killing the
            // optimizer. Browser-side load uses real headers and just works.
            unoptimized
            className="object-cover transition-transform duration-700 ease-out group-hover:scale-[1.02]"
          />
        </div>

        <div className="mt-6">
          <h3 className="font-serif text-[clamp(1.05rem,1.5vw,1.25rem)] font-normal leading-[1.3] tracking-[-0.01em] text-[#1f1d1b]">
            {product.name}
          </h3>
          <div className="mt-2 flex items-baseline justify-between gap-4">
            <p className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/55 sm:text-[12px]">
              {product.brand}
            </p>
            <span
              aria-label={`Price range ${product.priceRange}`}
              className="font-serif text-[14px] tracking-[0.04em] text-[#1f1d1b]/55"
            >
              {product.priceRange}
            </span>
          </div>
          <p className="mt-4 text-pretty font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/80 sm:text-[17px]">
            {product.reason}
          </p>
          <span className="mt-5 inline-flex items-baseline gap-2 text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/55 transition-colors duration-500 ease-out group-hover:text-[#1f1d1b] sm:text-[12px]">
            Read
            <span aria-hidden className="text-[12px]">
              →
            </span>
          </span>
        </div>
      </Link>
    </article>
  );
}

export default function ShopGrid() {
  const [filter, setFilter] = useState<Filter>("All");

  const products = useMemo(
    () =>
      filter === "All"
        ? SHOP_PRODUCTS
        : SHOP_PRODUCTS.filter((p) => p.category === filter),
    [filter]
  );

  return (
    <>
      {/* ---------- Filter row ---------- */}
      <nav
        aria-label="Filter shop by category"
        className="mb-12 flex flex-wrap items-center justify-center gap-x-4 gap-y-3 px-2 sm:mb-16 sm:gap-x-6"
      >
        {ALL_FILTERS.map((label, idx) => {
          const active = filter === label;
          return (
            <span
              key={label}
              className="flex items-center gap-x-4 sm:gap-x-6"
            >
              {idx > 0 && (
                <span
                  aria-hidden
                  className="hidden text-[10px] text-[#1f1d1b]/25 sm:inline"
                >
                  ·
                </span>
              )}
              <button
                type="button"
                aria-pressed={active}
                onClick={() => setFilter(label)}
                className={[
                  "cursor-pointer text-[11px] uppercase leading-none tracking-[0.24em] transition-colors duration-500 ease-out sm:text-[12px]",
                  active
                    ? "text-[#1f1d1b]"
                    : "text-[#1f1d1b]/45 hover:text-[#1f1d1b]/80",
                ].join(" ")}
              >
                {label}
              </button>
            </span>
          );
        })}
      </nav>

      {/* ---------- Grid ---------- */}
      {products.length === 0 ? (
        <p className="py-24 text-center font-serif text-[17px] italic text-[#1f1d1b]/55">
          Nothing here yet.
        </p>
      ) : (
        <ul className="grid grid-cols-2 gap-x-6 gap-y-12 sm:grid-cols-3 sm:gap-x-8 sm:gap-y-14 lg:grid-cols-4 lg:gap-x-10">
          {products.map((product) => (
            <li key={product.slug}>
              <ProductCard product={product} />
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
