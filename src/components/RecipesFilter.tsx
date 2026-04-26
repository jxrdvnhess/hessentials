"use client";

import { useMemo, useState } from "react";
import Link from "next/link";

type FilterableRecipe = {
  slug: string;
  title: string;
  description: string;
  tags: string[];
};

type RecipesFilterProps = {
  recipes: FilterableRecipe[];
};

const FILTERS = [
  "All",
  "Weeknight",
  "Slow",
  "Hosting",
  "Pantry",
  "Vegetarian",
] as const;

type Filter = (typeof FILTERS)[number];

function matchesFilter(recipe: FilterableRecipe, filter: Filter): boolean {
  if (filter === "All") return true;
  return recipe.tags.some(
    (t) => t.toLowerCase() === filter.toLowerCase()
  );
}

export default function RecipesFilter({ recipes }: RecipesFilterProps) {
  const [active, setActive] = useState<Filter>("All");

  const visible = useMemo(
    () => recipes.filter((r) => matchesFilter(r, active)),
    [recipes, active]
  );

  return (
    <>
      <div className="mx-auto mb-16 max-w-4xl px-6 text-center sm:mb-20 sm:px-10">
        <ul className="flex flex-wrap items-center justify-center gap-x-6 gap-y-3 text-[11px] uppercase leading-none tracking-[0.24em] sm:text-[12px]">
          {FILTERS.map((filter) => {
            const isActive = filter === active;
            return (
              <li key={filter}>
                <button
                  type="button"
                  onClick={() => setActive(filter)}
                  className={[
                    "cursor-pointer transition-colors duration-500 ease-out",
                    isActive
                      ? "text-[#1f1d1b]"
                      : "text-[#1f1d1b]/40 hover:text-[#1f1d1b]/75",
                  ].join(" ")}
                  aria-pressed={isActive}
                >
                  {filter}
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
        <ul className="mx-auto grid w-full max-w-6xl grid-cols-1 gap-x-12 gap-y-16 px-6 sm:grid-cols-2 sm:gap-x-14 sm:px-10 md:gap-x-20 md:gap-y-20">
          {visible.map((recipe) => (
            <li key={recipe.slug}>
              <Link
                href={`/recipes/${recipe.slug}`}
                className="group block transition-opacity duration-500 ease-out"
              >
                <h2 className="font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30">
                  {recipe.title}
                </h2>
                <p className="text-pretty mt-4 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[17px]">
                  {recipe.description}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
