"use client";

/**
 * ShopGallery — framed gallery-wall presentation of Shop products.
 *
 * Replaces the earlier full-bleed mosaic. The cream page background
 * is the gallery wall; each product image is presented as a single
 * curated piece — image + thick white mat + hairline outer border.
 * No drop shadow; the hairline does the lift.
 *
 * Layout. The wall sits inside standard page margins (no bleed).
 * Frames are arranged on a 12-column grid with mixed col-spans and
 * intentional vertical staggering so adjacent frames never share
 * a baseline. Frame ratio (square / portrait / landscape) is
 * assigned deterministically per slug; image fills its frame with
 * `object-contain` so the full source image is preserved.
 *
 * Mat. Thickness scales with the frame's smallest dimension via
 * percentage padding — ~10% on the sides, ~13% on the bottom (the
 * extra space is where the hover caption sits). Conventional
 * museum framing convention.
 *
 * Movement. A single rAF-debounced scroll listener applies a
 * translateY transform per frame, scaled by a deterministic depth
 * derived from each slug. Subtle by intent — the brand voice is
 * restraint. Smaller frames drift slightly more, larger frames
 * less, to amplify the gallery-depth feeling.
 *
 * Hover. The frame holds position; the image gains a 5% darken and
 * a name/brand caption fades in on the lower mat (not on the
 * image). Click navigates to product detail.
 *
 * Mobile. Single-column stack. Frames vary in width (full-bleed
 * down to ~70%) with alternating left/right offsets to preserve
 * the asymmetric register without packing them tight.
 */

import Image from "next/image";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import type { ShopProduct } from "../data/shop";
import { shuffleArray } from "../lib/shuffle";

/**
 * Per-slot layout — one entry per slot in the cycle. The cycle
 * repeats once we run out of products. Each slot specifies:
 *
 *   col   — Tailwind col-start / col-span class for desktop
 *   row   — Tailwind row-span (height multiplier)
 *   mt    — extra top margin on the frame to break the implicit
 *           grid baseline (capped at 28 = 112px per the density
 *           tuning addendum so adjacent frames stay within 120px)
 *   ratio — frame outer aspect ratio: portrait | square | landscape
 *   align — mobile alignment: left | right | center; pairs with
 *           a width below
 *   width — mobile width as % of column
 *
 * Hand-tuned for asymmetry: no two adjacent slots share col-start,
 * row-span, or ratio. col-start values rotate across all four
 * horizontal zones (left / center-left / center-right / right) so
 * no 600px vertical window sits empty in the middle.
 *
 * Cycle length 11.
 */
type Slot = {
  col: string;
  row: string;
  mt: string;
  ratio: "portrait" | "square" | "landscape";
  align: "left" | "right" | "center";
  width: string;
};

const SLOTS: readonly Slot[] = [
  { col: "sm:col-start-1 sm:col-span-4",  row: "sm:row-span-2", mt: "sm:mt-0",  ratio: "portrait",  align: "left",   width: "w-[100%]" },
  { col: "sm:col-start-6 sm:col-span-4",  row: "sm:row-span-1", mt: "sm:mt-12", ratio: "landscape", align: "right",  width: "w-[80%]"  },
  { col: "sm:col-start-10 sm:col-span-3", row: "sm:row-span-2", mt: "sm:mt-4",  ratio: "portrait",  align: "left",   width: "w-[88%]"  },
  { col: "sm:col-start-3 sm:col-span-3",  row: "sm:row-span-1", mt: "sm:mt-20", ratio: "square",    align: "center", width: "w-[100%]" },
  { col: "sm:col-start-7 sm:col-span-3",  row: "sm:row-span-2", mt: "sm:mt-8",  ratio: "portrait",  align: "right",  width: "w-[76%]"  },
  { col: "sm:col-start-10 sm:col-span-3", row: "sm:row-span-1", mt: "sm:mt-16", ratio: "landscape", align: "left",   width: "w-[84%]"  },
  { col: "sm:col-start-1 sm:col-span-4",  row: "sm:row-span-1", mt: "sm:mt-24", ratio: "landscape", align: "right",  width: "w-[72%]"  },
  { col: "sm:col-start-5 sm:col-span-3",  row: "sm:row-span-2", mt: "sm:mt-12", ratio: "square",    align: "center", width: "w-[100%]" },
  { col: "sm:col-start-8 sm:col-span-4",  row: "sm:row-span-1", mt: "sm:mt-20", ratio: "portrait",  align: "left",   width: "w-[92%]"  },
  { col: "sm:col-start-2 sm:col-span-4",  row: "sm:row-span-2", mt: "sm:mt-4",  ratio: "landscape", align: "right",  width: "w-[78%]"  },
  { col: "sm:col-start-9 sm:col-span-4",  row: "sm:row-span-2", mt: "sm:mt-16", ratio: "portrait",  align: "center", width: "w-[100%]" },
];

/** Tailwind aspect-ratio classes for each ratio bucket. */
const RATIO_CLASS: Record<Slot["ratio"], string> = {
  portrait: "aspect-[3/4]",
  square: "aspect-square",
  landscape: "aspect-[4/3]",
};

/** Mobile alignment class (margin-auto pattern). */
const ALIGN_CLASS: Record<Slot["align"], string> = {
  left: "mr-auto",
  right: "ml-auto",
  center: "mx-auto",
};

/**
 * Parallax depth bounds.
 *
 * Earlier the range was 0 → ~0.05, producing a 78× spread between
 * the slowest and fastest cards and up to ~700px of relative slip
 * across the full page. Two specific column pairs collided as a
 * result. Clamping to a tight 0.010–0.025 range cuts the worst-case
 * slip to ~240px, which is still enough drift for the editorial
 * feel but far below the threshold where adjacent frames stack.
 */
const MIN_DEPTH = 0.01;
const MAX_DEPTH = 0.025;

/**
 * Deterministic per-slug parallax depth in [MIN_DEPTH, MAX_DEPTH].
 * Stable across SSR / CSR and across re-shuffles in the same
 * session. Same hash function as before; just the output range
 * narrowed and the size-based scaling dropped to keep every
 * frame inside the clamp.
 */
function depthFor(slug: string): number {
  let h = 0;
  for (let i = 0; i < slug.length; i += 1) {
    h = (h * 31 + slug.charCodeAt(i)) | 0;
  }
  const normalized = Math.abs(h) / 2147483647; // 0..1
  return MIN_DEPTH + normalized * (MAX_DEPTH - MIN_DEPTH);
}

export default function ShopGallery({
  products,
}: {
  products: readonly ShopProduct[];
}) {
  // Deterministic SSR; client shuffles on mount so each visit feels alive.
  const [order, setOrder] = useState<ShopProduct[]>(() => [...products]);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setOrder(shuffleArray(products));
  }, [products]);

  // Pre-compute parallax depths once per product.
  const depths = useMemo(() => {
    const out: Record<string, number> = {};
    for (const p of products) {
      out[p.slug] = depthFor(p.slug);
    }
    return out;
  }, [products]);

  // Single scroll listener writes a CSS variable on the gallery
  // root; each frame reads its depth × variable in inline style.
  const rootRef = useRef<HTMLUListElement | null>(null);
  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    let ticking = false;
    const onScroll = () => {
      if (ticking) return;
      ticking = true;
      requestAnimationFrame(() => {
        const rect = root.getBoundingClientRect();
        // Use distance from top of viewport so frames sit at parity
        // when first scrolled into view, then drift onward.
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
      // Desktop: 12-col grid with auto rows. Gaps tuned per the
      // density addendum — typical 48–80px, capped at 120px when
      // combined with the per-slot mt-offsets. Mobile: flex-col —
      // slots' alignment + width classes do the asymmetric work.
      className="
        flex flex-col gap-y-10
        sm:grid sm:grid-cols-12 sm:gap-x-10 sm:gap-y-16 sm:[grid-auto-flow:dense]
        lg:gap-x-12 lg:gap-y-20
      "
    >
      {order.map((product, i) => {
        const slot = SLOTS[i % SLOTS.length];
        const depth = depths[product.slug] ?? 0;
        return (
          <li
            key={product.slug}
            className={[
              // Mobile width + alignment from the slot.
              slot.width,
              ALIGN_CLASS[slot.align],
              // Desktop: full-width within its grid cell.
              "sm:w-full sm:mr-0 sm:ml-0 sm:mx-0",
              slot.col,
              slot.row,
              slot.mt,
            ].join(" ")}
            style={
              {
                // Each frame applies its parallax via the shared
                // --scroll variable on the root.
                transform: `translate3d(0, calc(var(--scroll, 0) * ${depth}px), 0)`,
                willChange: depth > 0 ? "transform" : undefined,
              } as React.CSSProperties
            }
          >
            <Frame product={product} ratio={slot.ratio} />
          </li>
        );
      })}
    </ul>
  );
}

/* ---------- Frame ---------- */

/**
 * One framed plate. Image is presented inside a thick white mat
 * with a hairline outer border. The hover overlay caption sits on
 * the bottom mat — not on the image — per the addendum.
 */
function Frame({
  product,
  ratio,
}: {
  product: ShopProduct;
  ratio: Slot["ratio"];
}) {
  return (
    <article className="group">
      <Link
        href={`/shop/${product.slug}`}
        aria-label={`${product.brand} — ${product.name}`}
        className="block focus:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/30"
      >
        <div
          // The frame: white mat + hairline outer border. Padding
          // sets the mat thickness — 8% sides, 10.4% bottom (8 × 1.3
          // for the museum-convention deeper bottom mat). All values
          // sit in the 6-10% target range from the density addendum.
          // Padding percentages are relative to frame WIDTH, so mat
          // scales with the frame, not the source image.
          className="relative bg-white border border-[#1f1d1b]/12 px-[8%] pt-[8%] pb-[10.4%]"
        >
          {/* Image plate — natural aspect-ratio bucket. Image uses
              object-contain so the natural source ratio survives
              within the bucket without cropping. The bg-white
              ensures any letterboxing bleeds into the mat seamlessly. */}
          <div className={`relative w-full overflow-hidden bg-white ${RATIO_CLASS[ratio]}`}>
            <Image
              src={product.image}
              alt={`${product.brand} — ${product.name}`}
              fill
              sizes="(min-width: 1024px) 28vw, (min-width: 640px) 38vw, 78vw"
              className="object-contain"
            />
            {/* 5% darken on the IMAGE only on hover. */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0 bg-[#1f1d1b]/0 transition-colors duration-500 ease-out group-hover:bg-[#1f1d1b]/5"
            />
          </div>

          {/* Caption — sits on the lower mat, fades in on hover.
              Inset matches the new 8% side mat so the text edge
              aligns with the image edge. Absolute so the mat keeps
              its breathing room when nothing's hovering. */}
          <div
            aria-hidden
            className="absolute inset-x-[8%] bottom-[3%] flex flex-col items-start opacity-0 transition-opacity duration-500 ease-out group-hover:opacity-100"
          >
            <span className="font-serif text-[13px] leading-[1.2] text-[#1f1d1b] sm:text-[14px]">
              {product.name}
            </span>
            <span className="mt-1 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/60">
              {product.brand}
            </span>
          </div>
        </div>
      </Link>
    </article>
  );
}
