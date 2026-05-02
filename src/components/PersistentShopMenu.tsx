"use client";

/**
 * PersistentShopMenu — secondary nav that lives across every Shop
 * route. Sits directly under the main Hessentials nav.
 *
 * Pillar list (launch): All / Mens / Accessories / Grooming /
 * Travel / Home. Provisions and Womens are intentionally omitted —
 * see Brief 5.1 (Provisions hidden until inventory grows; Womens
 * activates once curation is ready, see Brief 2.6).
 *
 * Hover behavior:
 *   - Each non-All pillar opens a dropdown panel listing its
 *     subcategories.
 *   - The first item in every dropdown is `ALL <PILLAR>` linking to
 *     the pillar overview.
 *   - 150ms close delay on mouseleave so users don't lose the panel
 *     on diagonal mouse paths.
 *
 * Click behavior:
 *   - Clicking the pillar name navigates to `/shop/[pillar]`,
 *     equivalent to clicking ALL inside the dropdown.
 *
 * Active state:
 *   - When on `/shop/[pillar]`, that pillar carries the inverted
 *     dark treatment persistently.
 *   - When on `/shop/[pillar]/[subcategory]`, the pillar stays
 *     inverted and the active subcategory appears as a small-caps
 *     breadcrumb next to it.
 *
 * Mobile:
 *   - The bar collapses to a single BROWSE button.
 *   - Tapping it opens a full-screen overlay listing all pillars
 *     and subcategories vertically. Same content, different shape.
 *
 * Routing convention:
 *   - The Shop is structured at `/shop/<segment>` where `<segment>`
 *     is either a pillar key or a product slug. `/shop/[slug]`
 *     branches based on whether the value matches a CATEGORY_KEY.
 *   - Subcategory routes live at `/shop/<pillar>/<subcategory>`.
 */

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  CATEGORY_TREE,
  SHOP_PRODUCTS,
  categoryLabel,
  subcategoryLabel,
  type Category,
} from "../data/shop";

/**
 * Launch pillar order. Hand-curated, not derived. WOMENS sits
 * between MENS and ACCESSORIES per the addendum.
 *
 * Provisions remains intentionally absent.
 *
 * Pillars with zero products (after the audience-aware filter) are
 * hidden at runtime — see `pillarHasProducts` below. WOMENS
 * therefore reveals itself automatically once at least one matching
 * product lands; no code change required.
 */
const PILLARS: readonly Category[] = [
  "mens",
  "womens",
  "accessories",
  "grooming",
  "travel",
  "home",
];

const AUDIENCE_PILLARS = new Set<Category>(["mens", "womens"]);

/**
 * Mirror of the lib/shop.ts `productsForPillar` rule, restated here
 * so the menu (a client component) can decide visibility without
 * importing the server-only essay/markdown layer of lib/shop.ts.
 */
function pillarHasProducts(pillar: Category): boolean {
  if (AUDIENCE_PILLARS.has(pillar)) {
    return SHOP_PRODUCTS.some(
      (p) =>
        p.category === pillar ||
        (p.audience ?? []).includes(pillar as "mens" | "womens")
    );
  }
  return SHOP_PRODUCTS.some((p) => p.category === pillar);
}

/** ms to wait after mouseleave before collapsing the dropdown. */
const HOVER_CLOSE_DELAY_MS = 150;

type ParsedPath = {
  /** True when the current path is a shop route. */
  isShop: boolean;
  /** Active pillar (if URL is `/shop/<pillar>` or deeper). */
  activePillar: Category | null;
  /** Active subcategory (if URL is `/shop/<pillar>/<subcategory>`). */
  activeSubcategory: string | null;
};

function parsePath(pathname: string): ParsedPath {
  const isShop = pathname === "/shop" || pathname.startsWith("/shop/");
  const segments = pathname.replace(/^\/+|\/+$/g, "").split("/");
  // segments: ["shop"] | ["shop", "<segment>"] | ["shop", "<pillar>", "<sub>"] | ...
  const second = segments[1];
  const third = segments[2];
  const isPillar = !!second && (PILLARS as readonly string[]).includes(second);
  return {
    isShop,
    activePillar: isPillar ? (second as Category) : null,
    activeSubcategory: isPillar && third ? third : null,
  };
}

export default function PersistentShopMenu() {
  const pathname = usePathname() ?? "/";
  const { isShop, activePillar, activeSubcategory } = parsePath(pathname);

  /**
   * Hide pillars with zero products. The list updates implicitly as
   * curation evolves. Memoized — SHOP_PRODUCTS is bundled at build
   * time so this only ever runs once per mount.
   */
  const visiblePillars = useMemo(
    () => PILLARS.filter((p) => pillarHasProducts(p)),
    []
  );

  const [hoverPillar, setHoverPillar] = useState<Category | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const closeTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  const cancelClose = useCallback(() => {
    if (closeTimer.current) {
      clearTimeout(closeTimer.current);
      closeTimer.current = null;
    }
  }, []);
  const scheduleClose = useCallback(() => {
    cancelClose();
    closeTimer.current = setTimeout(() => {
      setHoverPillar(null);
    }, HOVER_CLOSE_DELAY_MS);
  }, [cancelClose]);

  // Close mobile overlay and any open dropdown on route change so
  // navigation feels native. Setting state in an effect is the
  // intended pattern here — there's no other way to react to
  // pathname changes at the menu level.
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setMobileOpen(false);
    setHoverPillar(null);
  }, [pathname]);

  if (!isShop) return null;

  return (
    <nav
      aria-label="Shop"
      className="relative z-30 border-b border-[#1f1d1b]/10 bg-[#f8f6f3]"
      onMouseLeave={scheduleClose}
    >
      <div className="mx-auto flex w-full max-w-7xl items-center px-6 sm:px-10">
        {/* ---------- Desktop bar ---------- */}
        <ul className="hidden flex-wrap items-center gap-x-7 gap-y-2 py-3 text-[11px] uppercase leading-none tracking-[0.22em] sm:flex">
          {/* All — flat link, no dropdown. */}
          <li>
            <Link
              href="/shop"
              className={[
                "inline-flex items-center px-2 py-1 transition-colors duration-300 ease-out",
                pathname === "/shop"
                  ? "bg-[#1f1d1b] text-[#f8f6f3]"
                  : "text-[#1f1d1b]/65 hover:text-[#1f1d1b]",
              ].join(" ")}
              onMouseEnter={() => {
                cancelClose();
                setHoverPillar(null);
              }}
            >
              All
            </Link>
          </li>

          {/* Pillar items with hover dropdowns. */}
          {visiblePillars.map((p, i) => {
            const subs = [...CATEGORY_TREE[p].subcategories];
            const isActive = activePillar === p;
            const isOpen = hoverPillar === p;
            return (
              <li
                key={p}
                className="relative"
                onMouseEnter={() => {
                  cancelClose();
                  setHoverPillar(p);
                }}
              >
                {/* The middle dot belongs visually with the previous
                    pillar — render it before each pillar except the
                    first one in the list. The All link sits before
                    this map and gets its own dot here. */}
                <span aria-hidden className="mr-7 -ml-4 text-[#1f1d1b]/30">
                  {i === 0 ? "·" : ""}
                </span>
                <Link
                  href={`/shop/${p}`}
                  className={[
                    "inline-flex items-center px-2 py-1 transition-colors duration-300 ease-out",
                    isActive
                      ? "bg-[#1f1d1b] text-[#f8f6f3]"
                      : "text-[#1f1d1b]/65 hover:text-[#1f1d1b]",
                  ].join(" ")}
                  aria-haspopup={subs.length > 0 ? "menu" : undefined}
                  aria-expanded={isOpen ? true : undefined}
                >
                  {categoryLabel(p)}
                </Link>

                {/* Subcategory breadcrumb when this pillar is active
                    AND a subcategory is the current route. */}
                {isActive && activeSubcategory && (
                  <span className="ml-3 inline-flex items-center text-[#1f1d1b]/55">
                    <span aria-hidden className="mr-3 text-[#1f1d1b]/30">
                      ·
                    </span>
                    {subcategoryLabel(activeSubcategory)}
                  </span>
                )}

                {/* Dropdown panel — flat, no shadow, top hairline,
                    cream body. Items invert on hover. */}
                {subs.length > 0 && (
                  <div
                    role="menu"
                    aria-label={`${categoryLabel(p)} subcategories`}
                    className={[
                      "absolute left-0 top-full z-30 min-w-[200px] border-t border-[#1f1d1b]/15 bg-[#f8f6f3]",
                      "transition-opacity duration-200 ease-out",
                      isOpen
                        ? "opacity-100 pointer-events-auto"
                        : "opacity-0 pointer-events-none",
                    ].join(" ")}
                  >
                    <ul className="py-1">
                      <li>
                        <Link
                          href={`/shop/${p}`}
                          className="block px-6 py-3 text-[#1f1d1b] transition-colors duration-200 ease-out hover:bg-[#1f1d1b] hover:text-[#f8f6f3]"
                        >
                          All {categoryLabel(p)}
                        </Link>
                      </li>
                      {subs.map((sub) => {
                        const subActive =
                          isActive && activeSubcategory === sub;
                        return (
                          <li key={sub}>
                            <Link
                              href={`/shop/${p}/${sub}`}
                              className={[
                                "block px-6 py-3 transition-colors duration-200 ease-out",
                                subActive
                                  ? "bg-[#1f1d1b] text-[#f8f6f3]"
                                  : "text-[#1f1d1b] hover:bg-[#1f1d1b] hover:text-[#f8f6f3]",
                              ].join(" ")}
                            >
                              {subcategoryLabel(sub)}
                            </Link>
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

        {/* ---------- Mobile button ---------- */}
        <button
          type="button"
          onClick={() => setMobileOpen(true)}
          className="block py-3 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b] sm:hidden"
        >
          {activePillar
            ? `Browse · ${categoryLabel(activePillar)}${
                activeSubcategory
                  ? ` · ${subcategoryLabel(activeSubcategory)}`
                  : ""
              }`
            : "Browse"}
        </button>
      </div>

      {/* ---------- Mobile overlay ---------- */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-[#f8f6f3] sm:hidden">
          <div className="flex items-center justify-between border-b border-[#1f1d1b]/15 px-6 py-4">
            <span className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
              Shop
            </span>
            <button
              type="button"
              onClick={() => setMobileOpen(false)}
              className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]"
              aria-label="Close menu"
            >
              Close
            </button>
          </div>
          <ul className="px-6 py-6">
            <li className="mb-6">
              <Link
                href="/shop"
                className={[
                  "inline-block text-[20px] uppercase tracking-[0.22em]",
                  pathname === "/shop"
                    ? "text-[#1f1d1b]"
                    : "text-[#1f1d1b]/65",
                ].join(" ")}
              >
                All
              </Link>
            </li>
            {visiblePillars.map((p) => {
              const subs = [...CATEGORY_TREE[p].subcategories];
              const isActive = activePillar === p;
              return (
                <li key={p} className="mb-8">
                  <Link
                    href={`/shop/${p}`}
                    className={[
                      "block text-[20px] uppercase tracking-[0.22em]",
                      isActive ? "text-[#1f1d1b]" : "text-[#1f1d1b]/65",
                    ].join(" ")}
                  >
                    {categoryLabel(p)}
                  </Link>
                  {subs.length > 0 && (
                    <ul className="mt-3 ml-1 space-y-2">
                      {subs.map((sub) => {
                        const subActive =
                          isActive && activeSubcategory === sub;
                        return (
                          <li key={sub}>
                            <Link
                              href={`/shop/${p}/${sub}`}
                              className={[
                                "block text-[12px] uppercase tracking-[0.22em]",
                                subActive
                                  ? "text-[#1f1d1b]"
                                  : "text-[#1f1d1b]/55",
                              ].join(" ")}
                            >
                              {subcategoryLabel(sub)}
                            </Link>
                          </li>
                        );
                      })}
                    </ul>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      )}
    </nav>
  );
}
