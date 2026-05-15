"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import {
  SHOP_CATEGORIES,
  SHOP_PRODUCTS,
  categoryLabel,
  subcategoryLabel,
  CATEGORY_TREE,
  type Category,
  type ShopProduct,
} from "../data/shop";
import type { PriceFetchResult } from "../lib/pricing/types";
import { shuffleArray } from "../lib/shuffle";
import { ProductCard } from "./ProductCard";

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

type Filter = Category | "All";

const ALL_FILTERS: readonly Filter[] = ["All", ...SHOP_CATEGORIES] as const;

/** Render label for a filter pill — "All" is literal; others go through categoryLabel. */
function pillLabel(f: Filter): string {
  return f === "All" ? "All" : categoryLabel(f);
}

/**
 * Subcategories per category, restricted to those with products.
 *
 * Computed once at module load: canonical order from CATEGORY_TREE
 * first (subcategories declared in `categories.ts`), then any extras
 * that products use but the canonical list doesn't carry. Categories
 * with zero subcategories yield an empty array — the row stays
 * collapsed when that top-level is hovered.
 */
const SUBCATEGORIES_BY_CATEGORY: Record<Category, string[]> = (() => {
  const out = {} as Record<Category, string[]>;
  for (const cat of SHOP_CATEGORIES) {
    // Cast `readonly [...]` literal-tuple from `as const satisfies` down
    // to a plain string set for `.has()` against runtime subcategories.
    const canonical = new Set<string>(CATEGORY_TREE[cat].subcategories);
    const present = new Set<string>(
      SHOP_PRODUCTS.filter(
        (p) => p.category === cat && p.draft !== true
      ).map((p) => p.subcategory)
    );
    const ordered: string[] = [];
    for (const s of CATEGORY_TREE[cat].subcategories) {
      if (present.has(s)) ordered.push(s);
    }
    for (const s of present) {
      if (!canonical.has(s)) ordered.push(s);
    }
    out[cat] = ordered;
  }
  return out;
})();

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



export default function ShopGrid({
  prices,
}: {
  /** Slug → resolved price. Server-rendered upstream; the grid never
   *  fetches. Missing entries fall back to the static priceRange so
   *  the grid stays render-stable even mid-deploy. */
  prices: Record<string, PriceFetchResult>;
}) {
  const [filter, setFilter] = useState<Filter>("All");
  const [subFilter, setSubFilter] = useState<string | null>(null);
  /**
   * Hover preview state — when a top-level pill is hovered, its
   * subcategories appear below even if the user hasn't clicked it
   * yet. The pre-clear timeout gives the user a window to glide from
   * top-level to subcategory pill without the row vanishing mid-move.
   */
  const [hoverCat, setHoverCat] = useState<Category | null>(null);
  const hoverClearRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const onPillEnter = (cat: Category) => {
    if (hoverClearRef.current) {
      clearTimeout(hoverClearRef.current);
      hoverClearRef.current = null;
    }
    setHoverCat(cat);
  };
  const onNavLeave = () => {
    if (hoverClearRef.current) clearTimeout(hoverClearRef.current);
    hoverClearRef.current = setTimeout(() => setHoverCat(null), 180);
  };

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
  // declared order — narrowing should feel predictable. Drafts (bulk
  // import staging records) are excluded from every public path.
  const LIVE = useMemo(
    () => SHOP_PRODUCTS.filter((p) => p.draft !== true),
    []
  );
  const [shuffled, setShuffled] = useState<ShopProduct[]>(LIVE);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setShuffled(shuffleArray(LIVE));
  }, [LIVE]);

  const products = useMemo(() => {
    let list =
      filter === "All"
        ? shuffled
        : LIVE.filter((p) => p.category === filter);
    if (subFilter) list = list.filter((p) => p.subcategory === subFilter);
    return list;
  }, [filter, subFilter, shuffled, LIVE]);

  /** Clear subcategory filter whenever the top-level changes — a sub
   *  selection rarely makes sense across categories. */
  const setTopFilter = (next: Filter) => {
    setFilter(next);
    setSubFilter(null);
  };

  return (
    <>
      {/* ---------- Filter row ----------
          Mirrors the pillar-page filter treatment exactly: flat ul,
          space-separated, no middle-dot separators, active item
          carries the filter-pill underline.

          Hovering any top-level pill reveals a vertical dropdown of
          its subcategories, anchored directly under the pill. The
          dropdown carries no surface — no card, no shadow, no border
          — just typography over the page texture. Same uppercase
          tracking as the row above; subcategories stack vertically.

          The dropdown floats absolutely, so the grid below does NOT
          shift when it appears. The 180ms pre-clear timeout on
          `mouseLeave` lets the cursor cross from pill to dropdown
          without flicker. */}
      <nav
        aria-label="Filter Shop by category"
        className="mb-12 sm:mb-16"
        onMouseLeave={onNavLeave}
      >
        <ul className="flex flex-wrap items-center justify-center gap-x-7 gap-y-3 text-[11px] uppercase leading-none tracking-[0.24em] sm:text-[12px]">
          {ALL_FILTERS.map((key) => {
            const active = filter === key;
            const isCat = key !== "All";
            const subs = isCat ? SUBCATEGORIES_BY_CATEGORY[key as Category] : [];
            const dropdownOpen = isCat && hoverCat === key && subs.length > 0;
            return (
              <li key={key} className="relative">
                <button
                  type="button"
                  aria-pressed={active}
                  aria-haspopup={subs.length > 0 ? "menu" : undefined}
                  aria-expanded={dropdownOpen ? true : undefined}
                  onClick={() => setTopFilter(key)}
                  onMouseEnter={
                    isCat ? () => onPillEnter(key as Category) : undefined
                  }
                  className={[
                    "filter-pill cursor-pointer transition-colors duration-500 ease-out",
                    active
                      ? "filter-pill-active text-[#1f1d1b]"
                      : "text-[#1f1d1b]/40 hover:text-[#1f1d1b]/75",
                  ].join(" ")}
                >
                  {pillLabel(key)}
                </button>

                {/* Vertical dropdown — anchored directly beneath this
                    pill, centered horizontally. Always rendered for
                    categories with subs (so fade-out animates); pointer
                    events and opacity gate visibility. The `pt-4`
                    padding bridges the pill ↔ dropdown gap so the
                    cursor doesn't traverse non-nav space when moving
                    down to a sub item. */}
                {isCat && subs.length > 0 && (
                  <div
                    role="menu"
                    aria-label={`${pillLabel(key)} subcategories`}
                    onMouseEnter={() => onPillEnter(key as Category)}
                    className={[
                      "absolute left-1/2 top-full z-30 -translate-x-1/2 pt-4",
                      "transition-opacity duration-300 ease-out",
                      dropdownOpen
                        ? "opacity-100 pointer-events-auto"
                        : "opacity-0 pointer-events-none",
                    ].join(" ")}
                  >
                    <ul className="flex flex-col items-center gap-y-3 text-[10px] uppercase leading-none tracking-[0.22em] sm:text-[11px]">
                      {subs.map((sub) => {
                        const subActive =
                          subFilter === sub && filter === key;
                        return (
                          <li key={sub} className="whitespace-nowrap">
                            <button
                              type="button"
                              role="menuitemcheckbox"
                              aria-checked={subActive}
                              onClick={() => {
                                // Click from a hover preview commits the
                                // top-level too — the user has clearly
                                // chosen this branch.
                                if (filter !== key) {
                                  setFilter(key as Category);
                                }
                                setSubFilter((curr) =>
                                  curr === sub ? null : sub
                                );
                              }}
                              className={[
                                "cursor-pointer transition-colors duration-300 ease-out",
                                subActive
                                  ? "text-[#1f1d1b]"
                                  : "text-[#1f1d1b]/55 hover:text-[#1f1d1b]",
                              ].join(" ")}
                            >
                              {subcategoryLabel(sub)}
                            </button>
                          </li>
                        );
                      })}
                    </ul>
                  </div>
                )}
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
