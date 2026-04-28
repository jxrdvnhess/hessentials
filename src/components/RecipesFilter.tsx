"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { shuffleArray } from "../lib/shuffle";

type FilterableRecipe = {
  slug: string;
  title: string;
  description: string;
  tags: string[];
  /** Optional, quiet secondary cue (e.g. "Weeknight staple"). */
  cue?: string;
};

type RecipesFilterProps = {
  recipes: FilterableRecipe[];
  /**
   * Slugs to exclude from the default "All" view (e.g. recipes already
   * surfaced in a "Start here" block above). They still appear under
   * specific tag filters so narrowing remains complete.
   */
  deferSlugs?: readonly string[];
};

const FILTERS = [
  { label: "All", hint: null },
  { label: "Weeknight", hint: "fast, reliable" },
  { label: "Slow", hint: "worth it" },
  { label: "Hosting", hint: "people over" },
  { label: "Pantry", hint: "you already have this" },
  { label: "Vegetarian", hint: null },
] as const;

type Filter = (typeof FILTERS)[number]["label"];

function matchesFilter(recipe: FilterableRecipe, filter: Filter): boolean {
  if (filter === "All") return true;
  return recipe.tags.some(
    (t) => t.toLowerCase() === filter.toLowerCase()
  );
}

export default function RecipesFilter({
  recipes,
  deferSlugs,
}: RecipesFilterProps) {
  const [active, setActive] = useState<Filter>("All");
  const deferred = useMemo(
    () => new Set(deferSlugs ?? []),
    [deferSlugs]
  );

  // Shuffle once on mount so every page visit lands on a fresh order
  // when the visitor is browsing "All". Specific tag filters keep the
  // recipes' declared order (narrowing should feel predictable).
  // Pattern: SSR renders the declared order (deterministic, hydration-safe);
  // the client re-orders after mount. The setState-in-effect lint warning
  // is suppressed below — this is exactly the SSR-then-randomize pattern
  // the rule discourages, but here it's the intended behavior.
  const [shuffled, setShuffled] = useState<FilterableRecipe[]>(recipes);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setShuffled(shuffleArray(recipes));
  }, [recipes]);

  const visible = useMemo(
    () =>
      active === "All"
        ? shuffled.filter((r) => !deferred.has(r.slug))
        : recipes.filter((r) => matchesFilter(r, active)),
    [recipes, shuffled, active, deferred]
  );

  return (
    <>
      <div className="mx-auto mb-16 max-w-4xl px-6 text-center sm:mb-20 sm:px-10">
        <ul className="flex flex-wrap items-baseline justify-center gap-x-7 gap-y-3 text-[11px] uppercase leading-none tracking-[0.24em] sm:text-[12px]">
          {FILTERS.map(({ label, hint }) => {
            const isActive = label === active;
            return (
              <li key={label}>
                <button
                  type="button"
                  onClick={() => setActive(label)}
                  className={[
                    "filter-pill cursor-pointer transition-colors duration-500 ease-out",
                    isActive
                      ? "filter-pill-active text-[#1f1d1b]"
                      : "text-[#1f1d1b]/40 hover:text-[#1f1d1b]/75",
                  ].join(" ")}
                  aria-pressed={isActive}
                >
                  {label}
                  {hint && (
                    <span
                      className={[
                        // Hidden on mobile — the inline hint pushed the filter row
                        // to 4–5 wrapped lines on phones. Visible on sm+ where the
                        // extra context aids scanning without crowding the layout.
                        "ml-2 hidden text-[11px] normal-case tracking-normal sm:inline",
                        isActive
                          ? "text-[#1f1d1b]/55"
                          : "text-[#1f1d1b]/30",
                      ].join(" ")}
                    >
                      ({hint})
                    </span>
                  )}
                </button>
              </li>
            );
          })}
        </ul>
      </div>

      {visible.length === 0 ? (
        <p className="mx-auto max-w-xl px-6 text-center font-serif text-[18px] italic text-[#1f1d1b]/55">
          Nothing under that filter yet. More entries arriving.
        </p>
      ) : (
        <ul className="mx-auto grid w-full max-w-6xl grid-cols-1 gap-x-10 gap-y-16 px-6 sm:grid-cols-2 sm:gap-x-12 sm:px-10 md:gap-x-14 md:gap-y-20">
          {visible.flatMap((recipe, idx) => {
            const cols = 2;
            const els = [];
            // Row hairline above every row after the first (sm+).
            if (idx > 0 && idx % cols === 0) {
              els.push(
                <li
                  key={`hr-${idx}`}
                  aria-hidden
                  className="hidden sm:col-span-2 sm:block"
                >
                  <span
                    className="block w-full"
                    style={{
                      height: "0.5px",
                      backgroundColor: "#c8bfae",
                    }}
                  />
                </li>
              );
            }
            els.push(
              <li key={recipe.slug}>
                <Link
                  href={`/recipes/${recipe.slug}`}
                  className="group block transition-opacity duration-500 ease-out"
                >
                  {recipe.cue && (
                    <p className="mb-3 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/40 sm:text-[11px]">
                      {recipe.cue}
                    </p>
                  )}
                  <h2 className="font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30">
                    {recipe.title}
                  </h2>
                  <p className="text-pretty mt-4 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[17px]">
                    {recipe.description}
                  </p>
                </Link>
              </li>
            );
            return els;
          })}
        </ul>
      )}
    </>
  );
}
