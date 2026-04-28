"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { shuffleArray } from "../lib/shuffle";

/** Lightweight article projection — the page passes only what the index
 *  needs to render, not the full HTML body. */
export type PracticeIndexArticle = {
  slug: string;
  title: string;
  excerpt: string;
  group: PracticeGroup;
};

export type PracticeGroup = "Daily" | "Inner" | "Cyclical";

const FILTERS = ["All", "Daily", "Inner", "Cyclical"] as const;
type Filter = (typeof FILTERS)[number];

type Props = {
  articles: PracticeIndexArticle[];
  /** Slugs surfaced in a "Start Here" rail on the default ("All") view. */
  featuredSlugs?: string[];
};

/**
 * Practice index list with filter row.
 *
 * Same composition pattern as Living: a curated "Start Here" rail above
 * the rest, and a filter row that narrows by group when a single bucket
 * is selected. The buckets here are the editorial frame Practice sits in:
 *
 *   Daily     — small things returned to (walk, compliment, silence,
 *               single object, the stone you carry)
 *   Inner     — practices that work on the interior life (sound baths,
 *               11:11, Mass, tarot, what you write down)
 *   Cyclical  — once-a-year or once-a-life shifts (annual review,
 *               stopping drinking)
 */
export default function PracticeFilter({ articles, featuredSlugs = [] }: Props) {
  const [active, setActive] = useState<Filter>("All");

  const { featured, rest } = useMemo(() => {
    const bySlug = new Map(articles.map((a) => [a.slug, a]));
    const featuredList = featuredSlugs
      .map((slug) => bySlug.get(slug))
      .filter((a): a is PracticeIndexArticle => Boolean(a));
    const featuredSet = new Set(featuredList.map((a) => a.slug));
    const restList = articles.filter((a) => !featuredSet.has(a.slug));
    return { featured: featuredList, rest: restList };
  }, [articles, featuredSlugs]);

  const [shuffledRest, setShuffledRest] =
    useState<PracticeIndexArticle[]>(rest);
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setShuffledRest(shuffleArray(rest));
  }, [rest]);

  const filtered = useMemo(() => {
    if (active === "All") return null;
    return articles.filter((a) => a.group === active);
  }, [articles, active]);

  const showStartHere = active === "All" && featured.length > 0;

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

      {filtered &&
        (filtered.length === 0 ? (
          <p className="mx-auto max-w-xl px-6 text-center font-serif text-[18px] italic text-[#1f1d1b]/55">
            More entries arriving soon.
          </p>
        ) : (
          <ArticleGrid articles={filtered} />
        ))}

      {!filtered && (
        <>
          {showStartHere && (
            <>
              <SectionLabel
                eyebrow="Start Here"
                headline="A few to start with"
                subline="Read one. Come back to the rest."
              />
              <ArticleGrid articles={featured} variant="featured" />
              <SectionLabel
                eyebrow="More"
                subline="Read what pulls you."
                spacing="between"
              />
            </>
          )}
          {shuffledRest.length === 0 && !showStartHere ? (
            <p className="mx-auto max-w-xl px-6 text-center font-serif text-[18px] italic text-[#1f1d1b]/55">
              More entries arriving soon.
            </p>
          ) : (
            <ArticleGrid articles={shuffledRest} />
          )}
        </>
      )}
    </>
  );
}

/* ---------- Internal pieces ---------- */

type SectionLabelProps = {
  eyebrow: string;
  headline?: string;
  subline?: string;
  spacing?: "default" | "between";
};

function SectionLabel({
  eyebrow,
  headline,
  subline,
  spacing = "default",
}: SectionLabelProps) {
  const topMargin =
    spacing === "between" ? "mt-24 sm:mt-32 md:mt-40" : "mt-0";
  return (
    <div
      className={`mx-auto mb-12 max-w-3xl px-6 text-center sm:mb-16 sm:px-10 ${topMargin}`}
    >
      <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
        {eyebrow}
      </p>
      {headline && (
        <h2 className="text-pretty mt-5 font-serif text-[clamp(1.4rem,2.3vw,1.85rem)] leading-[1.25] text-[#1f1d1b]">
          {headline}
        </h2>
      )}
      {subline && (
        <p className="text-pretty mx-auto mt-3 max-w-xl font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
          {subline}
        </p>
      )}
    </div>
  );
}

type ArticleGridProps = {
  articles: PracticeIndexArticle[];
  variant?: "default" | "featured";
};

function ArticleGrid({ articles, variant = "default" }: ArticleGridProps) {
  const isFeatured = variant === "featured";
  const gapY = isFeatured
    ? "gap-y-20 md:gap-y-24"
    : "gap-y-16 md:gap-y-20";
  const titleSize = isFeatured
    ? "text-[clamp(1.65rem,2.9vw,2.2rem)]"
    : "text-[clamp(1.5rem,2.6vw,2rem)]";
  const excerptSize = isFeatured
    ? "text-[16px] sm:text-[17px] md:text-[18px]"
    : "text-[16px] sm:text-[17px]";

  return (
    <ul
      className={`mx-auto grid w-full max-w-6xl grid-cols-1 gap-x-12 px-6 sm:grid-cols-2 sm:gap-x-14 sm:px-10 md:gap-x-20 ${gapY}`}
    >
      {articles.map((article) => (
        <li key={article.slug}>
          <Link
            href={`/practice/${article.slug}`}
            className="group block transition-opacity duration-500 ease-out"
          >
            <h2
              className={`font-serif ${titleSize} font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30`}
            >
              {article.title}
            </h2>

            {article.excerpt && (
              <p
                className={`text-pretty mt-4 font-serif italic leading-[1.55] text-[#1f1d1b]/65 ${excerptSize}`}
              >
                {article.excerpt}
              </p>
            )}
          </Link>
        </li>
      ))}
    </ul>
  );
}
