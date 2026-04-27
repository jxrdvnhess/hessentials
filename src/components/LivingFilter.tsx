"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { shuffleArray } from "../lib/shuffle";

/** Lightweight article projection — the page passes only what the index
 *  needs to render, not the full HTML body. */
export type LivingIndexArticle = {
  slug: string;
  title: string;
  excerpt: string;
  group: LivingGroup;
};

export type LivingGroup = "Systems" | "Environment" | "Rituals";

const FILTERS = ["All", "Systems", "Environment", "Rituals"] as const;
type Filter = (typeof FILTERS)[number];

type Props = {
  articles: LivingIndexArticle[];
};

/**
 * Living index list with filter row.
 *
 * "All" is the default and shows every article in a flat, shuffled order
 * — re-shuffles on each page visit so a returning reader doesn't see the
 * same sequence twice. Selecting a specific group (Systems / Environment
 * / Rituals) narrows to that bucket in declared order, no shuffle.
 *
 * Server-side render uses the unshuffled order so hydration is
 * deterministic; the client re-orders after mount.
 */
export default function LivingFilter({ articles }: Props) {
  const [active, setActive] = useState<Filter>("All");

  const [shuffled, setShuffled] = useState<LivingIndexArticle[]>(articles);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setShuffled(shuffleArray(articles));
  }, [articles]);

  const visible = useMemo(() => {
    if (active === "All") return shuffled;
    return articles.filter((a) => a.group === active);
  }, [articles, shuffled, active]);

  return (
    <>
      {/* Filter row */}
      <div className="mx-auto mb-16 max-w-4xl px-6 text-center sm:mb-20 sm:px-10">
        <ul className="flex flex-wrap items-center justify-center gap-x-6 gap-y-3 text-[11px] uppercase leading-none tracking-[0.24em] sm:text-[12px]">
          {FILTERS.map((filter) => {
            const isActive = filter === active;
            return (
              <li key={filter}>
                <button
                  type="button"
                  onClick={() => setActive(filter)}
                  aria-pressed={isActive}
                  className={[
                    "cursor-pointer transition-colors duration-500 ease-out",
                    isActive
                      ? "text-[#1f1d1b]"
                      : "text-[#1f1d1b]/40 hover:text-[#1f1d1b]/75",
                  ].join(" ")}
                >
                  {filter}
                </button>
              </li>
            );
          })}
        </ul>
      </div>

      {/* List */}
      {visible.length === 0 ? (
        <p className="mx-auto max-w-xl px-6 text-center font-serif text-[18px] italic text-[#1f1d1b]/55">
          More entries arriving soon.
        </p>
      ) : (
        <ul className="mx-auto grid w-full max-w-6xl grid-cols-1 gap-x-12 gap-y-16 px-6 sm:grid-cols-2 sm:gap-x-14 sm:px-10 md:gap-x-20 md:gap-y-20">
          {visible.map((article) => (
            <li key={article.slug}>
              <Link
                href={`/living/${article.slug}`}
                className="group block transition-opacity duration-500 ease-out"
              >
                <h2 className="font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30">
                  {article.title}
                </h2>

                {article.excerpt && (
                  <p className="text-pretty mt-4 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[17px]">
                    {article.excerpt}
                  </p>
                )}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
