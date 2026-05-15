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
 * Earlier revisions added per-slot top-margin offsets (mt-4..mt-24)
 * to break the implicit grid baseline. Those have been removed:
 * with mixed row-spans and `grid-auto-flow:dense`, the offsets
 * pushed frames past their grid-cell boundary and visually
 * collided with the next row's frame. Asymmetry now comes from
 * row-span variation, ratio variation, and column rotation alone —
 * which is enough.
 *
 * Cycle length 11.
 */
type Slot = {
  col: string;
  row: string;
  ratio: "portrait" | "square" | "landscape";
  align: "left" | "right" | "center";
  width: string;
};

const SLOTS: readonly Slot[] = [
  { col: "sm:col-start-1 sm:col-span-4",  row: "sm:row-span-2", ratio: "portrait",  align: "left",   width: "w-[100%]" },
  { col: "sm:col-start-6 sm:col-span-4",  row: "sm:row-span-1", ratio: "landscape", align: "right",  width: "w-[80%]"  },
  { col: "sm:col-start-10 sm:col-span-3", row: "sm:row-span-2", ratio: "portrait",  align: "left",   width: "w-[88%]"  },
  { col: "sm:col-start-3 sm:col-span-3",  row: "sm:row-span-1", ratio: "square",    align: "center", width: "w-[100%]" },
  { col: "sm:col-start-7 sm:col-span-3",  row: "sm:row-span-2", ratio: "portrait",  align: "right",  width: "w-[76%]"  },
  { col: "sm:col-start-10 sm:col-span-3", row: "sm:row-span-1", ratio: "landscape", align: "left",   width: "w-[84%]"  },
  { col: "sm:col-start-1 sm:col-span-4",  row: "sm:row-span-1", ratio: "landscape", align: "right",  width: "w-[72%]"  },
  { col: "sm:col-start-5 sm:col-span-3",  row: "sm:row-span-2", ratio: "square",    align: "center", width: "w-[100%]" },
  { col: "sm:col-start-8 sm:col-span-4",  row: "sm:row-span-1", ratio: "portrait",  align: "left",   width: "w-[92%]"  },
  { col: "sm:col-start-2 sm:col-span-4",  row: "sm:row-span-2", ratio: "landscape", align: "right",  width: "w-[78%]"  },
  { col: "sm:col-start-9 sm:col-span-4",  row: "sm:row-span-2", ratio: "portrait",  align: "center", width: "w-[100%]" },
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

  // Parallax is desktop-only. On mobile the gallery becomes a
  // single flex-column with limited gap-y between frames; a CSS
  // transform that slides one frame upward by 100–240px will
  // visually collide with the frame above it (the transform
  // doesn't reflow layout). Track viewport so we can no-op the
  // transform under sm.
  const [isDesktop, setIsDesktop] = useState(false);
  useEffect(() => {
    const mq = window.matchMedia("(min-width: 640px)");
    const apply = () => setIsDesktop(mq.matches);
    apply();
    mq.addEventListener("change", apply);
    return () => mq.removeEventListener("change", apply);
  }, []);

  // Single scroll listener writes a CSS variable on the gallery
  // root; each frame reads its depth × variable in inline style.
  // Listener is disabled on mobile so --scroll stays at 0.
  const rootRef = useRef<HTMLUListElement | null>(null);
  useEffect(() => {
    const root = rootRef.current;
    if (!root) return;
    if (!isDesktop) {
      root.style.setProperty("--scroll", "0");
      return;
    }
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
  }, [isDesktop]);

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
      // Desktop: 12-col grid with auto rows. Per-slot mt-offsets
      // were removed (they collided with grid row tracks under
      // mixed row-spans), so gap-y carries the vertical breathing
      // room alone. Mobile: flex-col — slots' alignment + width
      // classes do the asymmetric work.
      className="
        flex flex-col gap-y-10
        sm:grid sm:grid-cols-12 sm:gap-x-10 sm:gap-y-20 sm:[grid-auto-flow:dense]
        lg:gap-x-12 lg:gap-y-24
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
            ].join(" ")}
            style={
              {
                // Each frame applies its parallax via the shared
                // --scroll variable on the root. Desktop-only —
                // mobile leaves the transform off so frames stack
                // cleanly in a single flex column.
                transform: isDesktop
                  ? `translate3d(0, calc(var(--scroll, 0) * ${depth}px), 0)`
                  : undefined,
                willChange: isDesktop && depth > 0 ? "transform" : undefined,
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

/** Horizontal travel (px) above which a touch is treated as a swipe
 *  and the underlying Link click is suppressed. Tuned to feel decisive
 *  on iOS without eating accidental taps. */
const SWIPE_THRESHOLD = 40;

/**
 * One framed plate. Image is presented inside a thick white mat
 * with a hairline outer border. The hover overlay caption sits on
 * the bottom mat — not on the image — per the addendum.
 *
 * When a product carries multiple images, the frame becomes a small
 * gallery: horizontal swipe on touch devices, hover-revealed arrows
 * in the side mat on desktop. Click still navigates to detail; the
 * swipe handler suppresses the click when horizontal travel exceeds
 * SWIPE_THRESHOLD. Caption shows on hover for pointer devices and
 * defaults to visible on touch devices (no hover state).
 */
function Frame({
  product,
  ratio,
}: {
  product: ShopProduct;
  ratio: Slot["ratio"];
}) {
  const images = product.images ?? [product.image];
  const hasGallery = images.length > 1;
  const [active, setActive] = useState(0);
  // Image-load skeleton state. While `loaded` is false, the image
  // plate carries a slightly-darker-than-page-bg fill so the frame
  // outlines itself before the asset arrives (otherwise white-on-cream
  // reads as "missing content" on slow connections). One flag covers
  // the whole frame — the first image to load clears the skeleton for
  // the entire plate. Subsequent gallery images load against the white
  // plate beneath.
  const [loaded, setLoaded] = useState(false);

  const swipeStartX = useRef<number | null>(null);
  const wasSwipe = useRef(false);

  // Mobile caption reveal — caption only fades in when the card sits
  // in the vertical center band of the viewport. On touch devices
  // there's no hover, so the band gives readers a quiet "you've
  // stopped on this one" cue without making every caption permanent.
  // Desktop ignores this state; hover drives the caption there.
  const frameRef = useRef<HTMLDivElement | null>(null);
  const [inCenterBand, setInCenterBand] = useState(false);
  useEffect(() => {
    const el = frameRef.current;
    if (!el) return;
    // rootMargin negative top/bottom by 40% leaves a 20% center band.
    // Anything intersecting that band is "centered enough" to read.
    const obs = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.target === el) setInCenterBand(entry.isIntersecting);
        }
      },
      { rootMargin: "-40% 0px -40% 0px", threshold: 0 }
    );
    obs.observe(el);
    return () => obs.disconnect();
  }, []);

  const goTo = (i: number) =>
    setActive(((i % images.length) + images.length) % images.length);
  const next = () => goTo(active + 1);
  const prev = () => goTo(active - 1);

  const handleTouchStart = (e: React.TouchEvent) => {
    swipeStartX.current = e.touches[0].clientX;
    wasSwipe.current = false;
  };
  const handleTouchEnd = (e: React.TouchEvent) => {
    if (swipeStartX.current === null) return;
    const dx = e.changedTouches[0].clientX - swipeStartX.current;
    swipeStartX.current = null;
    if (Math.abs(dx) > SWIPE_THRESHOLD) {
      wasSwipe.current = true;
      if (dx < 0) next();
      else prev();
    }
  };
  const handleLinkClick = (e: React.MouseEvent) => {
    if (wasSwipe.current) {
      e.preventDefault();
      wasSwipe.current = false;
    }
  };
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (!hasGallery) return;
    if (e.key === "ArrowLeft") {
      e.preventDefault();
      prev();
    } else if (e.key === "ArrowRight") {
      e.preventDefault();
      next();
    }
  };

  // Arrow buttons — sit centered vertically in the side mat, not on
  // the image plate. Subtle: hairline border, near-transparent fill,
  // fade in on hover for pointer devices, faint resting state on
  // touch so the affordance is visible without dominating.
  const arrowBase =
    "absolute top-1/2 -translate-y-1/2 z-10 flex h-7 w-7 items-center justify-center rounded-full " +
    "border border-[#1f1d1b]/15 bg-white/70 text-[#1f1d1b]/80 backdrop-blur-sm " +
    "opacity-0 transition-opacity duration-300 ease-out " +
    "group-hover:opacity-100 group-focus-within:opacity-100 focus-visible:opacity-100 " +
    "hover:bg-white hover:text-[#1f1d1b] " +
    "[@media(hover:none)]:opacity-60";

  return (
    <article className="group">
      <div
        ref={frameRef}
        className="relative bg-white border border-[#1f1d1b]/12 px-[8%] pt-[8%] pb-[10.4%] touch-pan-y"
        onTouchStart={hasGallery ? handleTouchStart : undefined}
        onTouchEnd={hasGallery ? handleTouchEnd : undefined}
        onKeyDown={hasGallery ? handleKeyDown : undefined}
      >
        <Link
          href={`/shop/${product.slug}`}
          aria-label={`${product.brand} — ${product.name}`}
          onClick={handleLinkClick}
          className="block focus:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/30"
        >
          {/* Image plate. With multiple images, we fade between them
              by toggling opacity — same pattern as ProductCard. */}
          <div className={`relative w-full overflow-hidden bg-white ${RATIO_CLASS[ratio]}`}>
            {/* Skeleton — covers the plate until the first image
                load completes. Flat fill, no shimmer (per brand
                restraint). Fades to transparent so the white plate
                takes over once we have something to show. */}
            <div
              aria-hidden
              className={[
                "pointer-events-none absolute inset-0 bg-[#ebe7e0] transition-opacity duration-500 ease-out",
                loaded ? "opacity-0" : "opacity-100",
              ].join(" ")}
            />
            {images.map((src, i) => (
              <Image
                key={src}
                src={src}
                alt={`${product.brand} — ${product.name}`}
                fill
                sizes="(min-width: 1024px) 28vw, (min-width: 640px) 38vw, 78vw"
                onLoad={() => setLoaded(true)}
                className={[
                  "object-contain transition-opacity duration-500 ease-out",
                  i === active ? "opacity-100" : "opacity-0",
                ].join(" ")}
              />
            ))}
            {/* 5% darken on the IMAGE only on hover. */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0 bg-[#1f1d1b]/0 transition-colors duration-500 ease-out group-hover:bg-[#1f1d1b]/5"
            />
          </div>

          {/* Caption — sits on the lower mat. Fades in on hover for
              pointer devices. On touch devices there's no hover, so
              we reveal only when the card sits in the viewport center
              band (see frameRef + IntersectionObserver). That keeps
              the mobile scroll experience calm — captions only show
              for the product the reader has stopped on. */}
          <div
            aria-hidden
            className={[
              "absolute inset-x-[8%] bottom-[3%] flex flex-col items-start",
              "opacity-0 transition-opacity duration-500 ease-out",
              "group-hover:opacity-100",
              inCenterBand ? "[@media(hover:none)]:opacity-100" : "",
            ].join(" ")}
          >
            <span className="font-serif text-[11px] leading-[1.2] text-[#1f1d1b] sm:text-[14px]">
              {product.name}
            </span>
            <span className="mt-1 text-[9px] uppercase tracking-[0.22em] text-[#1f1d1b]/60 sm:text-[10px]">
              {product.brand}
            </span>
          </div>
        </Link>

        {hasGallery && (
          <>
            <button
              type="button"
              aria-label="Previous image"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                prev();
              }}
              className={`${arrowBase} left-[1.5%]`}
            >
              <span aria-hidden className="text-[12px] leading-none">
                ←
              </span>
            </button>
            <button
              type="button"
              aria-label="Next image"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                next();
              }}
              className={`${arrowBase} right-[1.5%]`}
            >
              <span aria-hidden className="text-[12px] leading-none">
                →
              </span>
            </button>
          </>
        )}
      </div>
    </article>
  );
}
