"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import {
  SHOP_CATEGORIES,
  SHOP_PRODUCTS,
  type ShopCategory,
  type ShopProduct,
} from "../data/shop";
import type { PriceFetchResult } from "../lib/pricing/types";
import { shuffleArray } from "../lib/shuffle";

/**
 * Shop grid — editorial mosaic.
 *
 * The site pulls product photography from many different brand CDNs. Each
 * brand uses different lighting, crops, and backgrounds — there is no way
 * to fully unify them. Rather than fight that inconsistency we frame it:
 * cards run at varied aspect ratios so the page reads like a Tumblr-style
 * photo blog rather than a uniform product grid. The variation provides
 * its own rhythm; the brand inconsistency becomes part of the texture.
 *
 * Layout: CSS multi-column masonry. Items flow naturally and break-inside
 * is avoided. On phones the whole grid collapses to a single column at the
 * canonical 4/5 ratio (no Tetris on mobile — vertical scroll is enough).
 *
 * Each card's aspect ratio is assigned deterministically by its position
 * in the visible (filtered) array, so the same filter always produces the
 * same mosaic — no flicker on hydrate, no surprise re-tiling.
 */

type Filter = ShopCategory | "All";

const ALL_FILTERS: readonly Filter[] = ["All", ...SHOP_CATEGORIES] as const;

/**
 * Aspect-ratio cycle for desktop / tablet. Designed so adjacent cards in a
 * column have visibly different heights without any single ratio dominating.
 * Mobile ignores this and uses a fixed 4/5 for clean vertical stacking.
 */
const ASPECT_CYCLE = [
  "4 / 5",
  "3 / 4",
  "4 / 5",
  "5 / 7",
  "1 / 1",
  "4 / 5",
  "5 / 6",
  "3 / 5",
  "4 / 5",
  "4 / 5",
  "5 / 7",
  "3 / 4",
] as const;

/** Horizontal travel (px) above which a touch is treated as a swipe and
    the underlying Link click is suppressed. Tuned to feel decisive on
    iOS without eating accidental taps. */
const SWIPE_THRESHOLD = 40;

function ProductCard({
  product,
  aspect,
  price,
}: {
  product: ShopProduct;
  /** CSS aspect-ratio value for the image frame (e.g. "4 / 5"). Applied
   *  on sm+; mobile collapses to the canonical 4/5 below. */
  aspect: string;
  /** Resolved price for this product. May be live, manual fallback, or
   *  a sold-out signal. The card never recomputes — it just renders. */
  price: PriceFetchResult;
}) {
  const detailHref = `/shop/${product.slug}`;
  const images = product.images ?? [product.image];
  const hasGallery = images.length > 1;
  const [active, setActive] = useState(0);

  const swipeStartX = useRef<number | null>(null);
  const wasSwipe = useRef(false);

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

  // Tailwind classes shared by both arrow buttons. Same pattern as
  // ProductGallery on the detail page, scaled down for grid cards.
  const arrowBase =
    "absolute top-1/2 -translate-y-1/2 z-20 flex h-8 w-8 items-center justify-center rounded-full " +
    "bg-[#f8f6f3]/90 text-[#1f1d1b] backdrop-blur-sm " +
    "border border-[#1f1d1b]/10 shadow-[0_1px_3px_rgba(31,29,27,0.08)] " +
    "opacity-0 transition-opacity duration-300 ease-out " +
    "group-hover:opacity-100 group-focus-within:opacity-100 focus-visible:opacity-100 " +
    "hover:bg-[#f8f6f3] " +
    "[@media(hover:none)]:opacity-70 sm:h-9 sm:w-9";

  return (
    <article className="group">
      {/* Image frame — varied aspect ratio drives the mosaic.
          The inline aspectRatio applies at every breakpoint; the
          single-column mobile stack just has visibly different
          heights, which reads as the same editorial rhythm.

          Background is a soft warm white because we render product
          shots with `object-contain` (no cropping). When a source
          image's natural ratio doesn't match the frame, the empty
          space becomes letterbox — a near-white tone blends with
          the white product backgrounds most brands shoot on, so the
          edges don't read as cut-offs. */}
      <div
        className="relative w-full overflow-hidden bg-[#faf9f5] touch-pan-y"
        style={{ aspectRatio: aspect }}
        onTouchStart={hasGallery ? handleTouchStart : undefined}
        onTouchEnd={hasGallery ? handleTouchEnd : undefined}
        onKeyDown={hasGallery ? handleKeyDown : undefined}
      >
        <Link
          href={detailHref}
          aria-label={`${product.brand} — ${product.name}, read more`}
          onClick={handleLinkClick}
          className="absolute inset-0 focus:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/40 focus-visible:ring-offset-2 focus-visible:ring-offset-[#f8f6f3]"
        >
          {images.map((src, i) => (
            <Image
              key={src}
              src={src}
              alt={`${product.brand} — ${product.name}`}
              fill
              sizes="(min-width: 1280px) 22vw, (min-width: 1024px) 28vw, (min-width: 640px) 45vw, 100vw"
              className={[
                // `object-contain` guarantees the whole product is
                // visible. Slight padding gives every product a
                // consistent inset so they read as objects on a field
                // rather than packed-edge collages.
                "object-contain p-3 sm:p-4 transition-[opacity,transform] duration-500 ease-out",
                i === active
                  ? "opacity-100 group-hover:scale-[1.02]"
                  : "opacity-0",
              ].join(" ")}
            />
          ))}
        </Link>

        {hasGallery && (
          <>
            {/* Hover-revealed prev / next arrows — fade in when the
                cursor enters the card. On touch devices (no hover)
                they sit at a quieter resting opacity so the
                affordance is visible without dominating the image. */}
            <button
              type="button"
              aria-label="Previous image"
              onClick={(e) => {
                e.preventDefault();
                e.stopPropagation();
                prev();
              }}
              className={`${arrowBase} left-2 sm:left-3`}
            >
              <span aria-hidden className="text-[13px] leading-none">
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
              className={`${arrowBase} right-2 sm:right-3`}
            >
              <span aria-hidden className="text-[13px] leading-none">
                →
              </span>
            </button>

            {/* Position counter — reinforces "there's more here" without
                shouting. Hidden until hover; visible on touch. */}
            <div
              aria-hidden
              className="pointer-events-none absolute right-2 top-2 z-20 rounded-full border border-[#1f1d1b]/10 bg-[#f8f6f3]/85 px-2 py-[3px] text-[9.5px] tracking-[0.18em] text-[#1f1d1b]/70 backdrop-blur-sm opacity-0 transition-opacity duration-300 ease-out group-hover:opacity-100 group-focus-within:opacity-100 [@media(hover:none)]:opacity-75 sm:right-3 sm:top-3 sm:text-[10px]"
            >
              {String(active + 1).padStart(2, "0")} /{" "}
              {String(images.length).padStart(2, "0")}
            </div>

            {/* Position dots — secondary indicator. Bumped from 6px to
                8px and lifted to a higher resting opacity so the
                affordance is legible on every card, not just the one
                under the cursor. Each dot is its own jump target. */}
            <div
              className="pointer-events-none absolute inset-x-0 bottom-3 z-10 flex justify-center gap-2"
              aria-hidden="false"
            >
              {images.map((_, i) => (
                <button
                  key={i}
                  type="button"
                  aria-label={`Show image ${i + 1} of ${images.length}`}
                  aria-current={i === active}
                  onClick={(e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    goTo(i);
                  }}
                  className={[
                    "pointer-events-auto h-2 w-2 rounded-full border border-[#1f1d1b]/15 transition-all duration-300 ease-out",
                    i === active
                      ? "bg-[#f8f6f3] scale-110"
                      : "bg-[#f8f6f3]/65 hover:bg-[#f8f6f3]/95",
                  ].join(" ")}
                />
              ))}
            </div>
          </>
        )}
      </div>

      <Link href={detailHref} className="block">
        <div className="mt-5">
          <h3 className="font-serif text-[clamp(1.05rem,1.5vw,1.25rem)] font-normal leading-[1.3] tracking-[-0.01em] text-[#1f1d1b]">
            {product.name}
          </h3>
          <div className="mt-2 flex items-baseline justify-between gap-4">
            <p className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/55 sm:text-[12px]">
              {product.brand}
            </p>
            {price.soldOut ? (
              // Sold-out tag replaces the price on cards. Reads as a
              // small uppercase aside, matching the brand label across
              // the gap — no exclamation, no urgency.
              <span
                aria-label="Sold out"
                className="text-[10px] uppercase tracking-[0.24em] text-[#1f1d1b]/45"
              >
                Sold out
              </span>
            ) : (
              <span
                aria-label={`Price ${price.display}`}
                className="font-serif text-[14px] tracking-[0.04em] text-[#1f1d1b]/55"
              >
                {price.display}
              </span>
            )}
          </div>
          <p className="mt-3 text-pretty font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/80 sm:text-[17px]">
            {product.reason}
          </p>
          <span className="mt-4 inline-flex items-baseline gap-2 text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/55 transition-colors duration-500 ease-out group-hover:text-[#1f1d1b] sm:text-[12px]">
            Details
            <span aria-hidden className="text-[12px]">
              →
            </span>
          </span>
        </div>
      </Link>
    </article>
  );
}

export default function ShopGrid({
  prices,
}: {
  /** Slug → resolved price. Server-rendered upstream; the grid never
   *  fetches. Missing entries fall back to the static priceRange so
   *  the grid stays render-stable even mid-deploy. */
  prices: Record<string, PriceFetchResult>;
}) {
  const [filter, setFilter] = useState<Filter>("All");

  // Helper: every card needs a price. If the upstream map is missing a
  // slug for any reason, synthesize a manual fallback from the static
  // priceRange — the card never renders without something to show.
  const priceFor = (product: ShopProduct): PriceFetchResult =>
    prices[product.slug] ?? {
      display: product.priceRange,
      live: false,
      soldOut: false,
      method: "manual",
    };

  // Re-shuffle on every page visit. Server-side render keeps the declared
  // order (deterministic, hydration-safe); after mount we swap to a freshly
  // shuffled array so every arrival feels like a new editorial spread when
  // the visitor lands on "All". Specific category filters keep their
  // declared order — narrowing should feel predictable.
  const [shuffled, setShuffled] = useState<ShopProduct[]>(SHOP_PRODUCTS);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setShuffled(shuffleArray(SHOP_PRODUCTS));
  }, []);

  const products = useMemo(
    () =>
      filter === "All"
        ? shuffled
        : SHOP_PRODUCTS.filter((p) => p.category === filter),
    [filter, shuffled]
  );

  return (
    <>
      {/* ---------- Filter row ----------
          Mirrors the pillar-page filter treatment exactly: flat ul,
          space-separated, no middle-dot separators, active item
          carries the filter-pill underline. Brings Shop into parity
          with Recipes / Living / Practice so all four filter rows
          read as one system. */}
      <nav aria-label="Filter shop by category" className="mb-12 sm:mb-16">
        <ul className="flex flex-wrap items-center justify-center gap-x-7 gap-y-3 text-[11px] uppercase leading-none tracking-[0.24em] sm:text-[12px]">
          {ALL_FILTERS.map((label) => {
            const active = filter === label;
            return (
              <li key={label}>
                <button
                  type="button"
                  aria-pressed={active}
                  onClick={() => setFilter(label)}
                  className={[
                    "filter-pill cursor-pointer transition-colors duration-500 ease-out",
                    active
                      ? "filter-pill-active text-[#1f1d1b]"
                      : "text-[#1f1d1b]/40 hover:text-[#1f1d1b]/75",
                  ].join(" ")}
                >
                  {label}
                </button>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* ---------- Mosaic ----------
          CSS multi-column gives natural masonry — items flow into the
          shortest column, varied aspect ratios fill the gaps, and
          `break-inside: avoid` keeps each card whole. Mobile collapses
          to a single column. */}
      {products.length === 0 ? (
        <p className="py-24 text-center font-serif text-[17px] italic text-[#1f1d1b]/55">
          Nothing here yet.
        </p>
      ) : (
        <ul className="columns-1 gap-x-6 [column-fill:_balance] sm:columns-2 sm:gap-x-8 lg:columns-3 lg:gap-x-10 xl:columns-4">
          {products.map((product, i) => (
            <li
              key={product.slug}
              className="mb-12 break-inside-avoid sm:mb-14 lg:mb-16"
            >
              <ProductCard
                product={product}
                aspect={ASPECT_CYCLE[i % ASPECT_CYCLE.length]}
                price={priceFor(product)}
              />
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
