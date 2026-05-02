"use client";

/**
 * ShopMosaic — full-bleed asymmetric mosaic of product imagery.
 *
 * Layout. CSS grid with mixed col-span / row-span values cycling
 * through a curated pattern so adjacent tiles read as varied
 * without devolving into a uniform product wall. `auto-flow: dense`
 * fills gaps left by tall/wide tiles. The grid bleeds to the
 * viewport edges and uses thin gutters (4–8px) so the imagery
 * carries the page rather than the framing.
 *
 * Randomization. The server renders the products in their canonical
 * SHOP_PRODUCTS order so SSR is deterministic and hydration-safe.
 * On mount the client swaps to a freshly shuffled array — every
 * arrival feels alive without producing a flicker.
 *
 * Parallax. Each tile gets a small parallax depth (0…0.05) assigned
 * once on mount. On scroll, a single rAF-debounced listener applies
 * `transform: translate3d(0, -scrollY * depth, 0)` to the row
 * container of each tile. Subtle by intent — the brand voice is
 * restraint.
 *
 * Hover. Each tile darkens 10% with the product name and brand in
 * small-caps at the bottom-left.
 */

import Image from "next/image";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import type { ShopProduct } from "../data/shop";
import { shuffleArray } from "../lib/shuffle";

/**
 * Tile-shape cycle. Cells live on a 6-column grid; row height is
 * fixed (see `auto-rows-...`). The pattern is hand-tuned to avoid
 * long stretches of same-size tiles — adjacent shapes always
 * differ. Cycles every 11 tiles.
 *
 * Each entry is a Tailwind class string applied to the wrapper
 * element. Mobile collapses the grid to two columns; the spans
 * still apply but degrade naturally.
 */
const TILE_SHAPES: readonly string[] = [
  "col-span-3 row-span-2",
  "col-span-3 row-span-1",
  "col-span-2 row-span-1",
  "col-span-2 row-span-2",
  "col-span-3 row-span-1",
  "col-span-3 row-span-1",
  "col-span-2 row-span-2",
  "col-span-2 row-span-1",
  "col-span-3 row-span-1",
  "col-span-3 row-span-2",
  "col-span-2 row-span-1",
];

/** Max parallax depth; 0 means no drift, 1 means tile moves with scroll. */
const MAX_DEPTH = 0.05;

/**
 * Deterministic hash → 0–1 normalization, used to assign each tile
 * a stable parallax depth. Deterministic so SSR and CSR agree, and
 * so lint stays clean (no `Math.random` in a useMemo).
 */
function depthFor(slug: string): number {
  let h = 0;
  for (let i = 0; i < slug.length; i += 1) {
    h = (h * 31 + slug.charCodeAt(i)) | 0;
  }
  // 2147483647 = max int32; abs(h) / that ≈ [0, 1].
  return (Math.abs(h) / 2147483647) * MAX_DEPTH;
}

export default function ShopMosaic({
  products,
}: {
  products: readonly ShopProduct[];
}) {
  // Deterministic SSR; client swaps to a shuffled order on mount.
  const [order, setOrder] = useState<ShopProduct[]>(() => [...products]);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setOrder(shuffleArray(products));
  }, [products]);

  // Per-tile parallax depths derived deterministically from each
  // slug. Stable across re-shuffles and SSR/CSR transitions.
  const depths = useMemo(() => {
    const out: Record<string, number> = {};
    for (const p of products) out[p.slug] = depthFor(p.slug);
    return out;
  }, [products]);

  // Single scroll listener applies a transform via CSS variable on
  // the grid root; each tile reads its depth from a per-tile style.
  const rootRef = useRef<HTMLUListElement | null>(null);
  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        // Use the grid's distance from the top of the page so tiles
        // start at parity at the natural reading position and drift
        // as the user scrolls past.
        const rect = root.getBoundingClientRect();
        const offset = -rect.top;
        root.style.setProperty("--scroll", `${offset}`);
        ticking = false;
      });
    };
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  if (order.length === 0) {
    return (
      <p className="py-24 text-center font-serif text-[17px] italic text-[#1f1d1b]/55">
        Nothing here yet.
      </p>
    );
  }

  return (
    <ul
      ref={rootRef}
      className="grid grid-cols-2 gap-1 [grid-auto-flow:dense] auto-rows-[160px] sm:grid-cols-6 sm:gap-1.5 sm:auto-rows-[180px] md:auto-rows-[200px] lg:auto-rows-[220px]"
    >
      {order.map((product, i) => {
        const shape = TILE_SHAPES[i % TILE_SHAPES.length];
        const depth = depths[product.slug] ?? 0;
        return (
          <li
            key={product.slug}
            className={`group relative overflow-hidden bg-[#f0e9d9] ${shape}`}
            style={
              {
                // Each tile reads `--scroll` from the root and applies
                // a translateY scaled by its depth. Negative depth
                // means the tile lags behind the scroll.
                transform: `translate3d(0, calc(var(--scroll, 0) * ${depth}px), 0)`,
                willChange: depth > 0 ? "transform" : undefined,
              } as React.CSSProperties
            }
          >
            <Link
              href={`/shop/${product.slug}`}
              className="absolute inset-0 block focus:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/40"
              aria-label={`${product.brand} — ${product.name}`}
            >
              <Image
                src={product.image}
                alt={`${product.brand} — ${product.name}`}
                fill
                sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                className="object-cover transition-transform duration-700 ease-out group-hover:scale-[1.02]"
              />
              {/* 10% darken overlay on hover. */}
              <div
                aria-hidden
                className="pointer-events-none absolute inset-0 bg-[#1f1d1b]/0 transition-colors duration-500 ease-out group-hover:bg-[#1f1d1b]/10"
              />
              {/* Name + brand caption — fades in with the overlay. */}
              <div
                aria-hidden
                className="absolute inset-x-0 bottom-0 flex flex-col items-start p-4 text-[#f8f6f3] opacity-0 transition-opacity duration-500 ease-out group-hover:opacity-100 sm:p-5"
              >
                <span className="font-serif text-[14px] leading-[1.2] sm:text-[15px]">
                  {product.name}
                </span>
                <span className="mt-1 text-[10px] uppercase tracking-[0.22em] text-[#f8f6f3]/85">
                  {product.brand}
                </span>
              </div>
            </Link>
          </li>
        );
      })}
    </ul>
  );
}
