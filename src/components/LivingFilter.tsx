"use client";

import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import { shuffleArray } from "../lib/shuffle";
import SectionDivider from "./SectionDivider";

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

// Stable module-level reference for the empty default. Without this,
// an inline `featuredSlugs = []` in the signature would create a new
// array on every render, the useMemo below would recompute `rest` (new
// ref), the shuffle effect would re-fire, setState would trigger a
// re-render — an infinite loop that visually presents as the article
// list "shaking" continuously. Surfaced after the equal-treatment pass
// dropped the `featuredSlugs` prop at the call site.
const EMPTY_SLUGS: readonly string[] = [];

type Props = {
  articles: LivingIndexArticle[];
  /**
   * Slugs that should appear in the "Start Here" rail on the default
   * ("All") view, in the order specified. When a specific group filter
   * is active the rail collapses and all matching articles render in a
   * single uniform grid.
   */
  featuredSlugs?: readonly string[];
};

/**
 * Living index list with filter row.
 *
 * Default ("All") view renders two tiers:
 *   1. "Start Here" — a curated handful of pieces (slightly emphasized),
 *      in editor-defined order.
 *   2. "The Rest" — everything else, shuffled on each visit so a
 *      returning reader doesn't see the same sequence twice.
 *
 * Selecting a specific group (Systems / Environment / Rituals) collapses
 * the hierarchy and shows a single uniform grid for that bucket.
 *
 * Server-side render uses the unshuffled order so hydration is
 * deterministic; the client re-orders after mount.
 */
export default function LivingFilter({
  articles,
  featuredSlugs = EMPTY_SLUGS,
}: Props) {
  const [active, setActive] = useState<Filter>("All");

  // Featured / rest split — featured holds its declared order; rest is
  // everything not featured, eligible for the visit-time shuffle.
  const { featured, rest } = useMemo(() => {
    const bySlug = new Map(articles.map((a) => [a.slug, a]));
    const featuredList = featuredSlugs
      .map((slug) => bySlug.get(slug))
      .filter((a): a is LivingIndexArticle => Boolean(a));
    const featuredSet = new Set(featuredList.map((a) => a.slug));
    const restList = articles.filter((a) => !featuredSet.has(a.slug));
    return { featured: featuredList, rest: restList };
  }, [articles, featuredSlugs]);

  const [shuffledRest, setShuffledRest] =
    useState<LivingIndexArticle[]>(rest);
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
      {/* Filter row — active pill carries a hairline underline (per §2.3).
          Inactive pills are plain text; hover surfaces a faint cream
          underline as an interactivity signal. No pill shapes, no
          borders, no fills. */}
      <div className="mx-auto mb-16 max-w-4xl px-6 text-center sm:mb-20 sm:px-10">
        <ul className="flex flex-wrap items-center justify-center gap-x-7 gap-y-3 text-[11px] uppercase leading-none tracking-[0.24em] sm:text-[12px]">
          {FILTERS.map((filter) => {
            const isActive = filter === active;
            return (
              <li key={filter}>
                <button
                  type="button"
                  onClick={() => setActive(filter)}
                  aria-pressed={isActive}
                  className={[
                    "filter-pill cursor-pointer transition-colors duration-500 ease-out",
                    isActive
                      ? "filter-pill-active text-[#1f1d1b]"
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

      {/* Filtered (single-group) view */}
      {filtered &&
        (filtered.length === 0 ? (
          <p className="mx-auto max-w-xl px-6 text-center font-serif text-[18px] italic text-[#1f1d1b]/55">
            More entries arriving soon.
          </p>
        ) : (
          <ArticleGrid articles={filtered} />
        ))}

      {/* Default ("All") view — Start Here + The Rest */}
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
              {/* "h" motif marks the transition between the curated
                  Start Here set and the broader archive (per §2.1). */}
              <SectionDivider />
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
  /**
   * "between" tightens the top margin so a label that sits between two
   * grids doesn't double up on the spacing the previous grid already
   * supplies.
   */
  spacing?: "default" | "between";
};

function SectionLabel({
  eyebrow,
  headline,
  subline,
  spacing = "default",
}: SectionLabelProps) {
  // The "between" variant follows directly after a SectionDivider, so
  // its top margin is intentionally light — the divider supplies the
  // section break above.
  const topMargin =
    spacing === "between" ? "mt-2 sm:mt-4" : "mt-0";
  return (
    <div
      className={`mx-auto mb-12 flex max-w-3xl flex-col items-center px-6 text-center sm:mb-16 sm:px-10 ${topMargin}`}
    >
      {/* Hairline above the all-caps label (per §2.2). 80px wide,
          0.5px, tonal cream — anchors the label as architecture. */}
      <span
        aria-hidden
        className="block w-20"
        style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
      />
      <p className="mt-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
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
  articles: LivingIndexArticle[];
  /**
   * "featured" gives titles a touch more weight and adds a little extra
   * vertical breathing room — a hierarchy adjustment, not a redesign.
   */
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

  // Tightened column gap (~40–56px) per §2.4 — was ~80–100px. Cards
  // themselves untouched; only the spacing between them tightens.
  //
  // Row hairlines: above every row except the first (the SectionLabel
  // already supplies a break above the first row). Hairlines render as
  // their own grid items spanning both columns; on mobile (single
  // column) they're hidden — the single-column rhythm reads cleaner
  // without dividers between every card.
  const cols = 2;

  return (
    <ul
      className={`mx-auto grid w-full max-w-6xl grid-cols-1 gap-x-10 px-6 sm:grid-cols-2 sm:gap-x-12 sm:px-10 md:gap-x-14 ${gapY}`}
    >
      {articles.flatMap((article, idx) => {
        const els = [];
        // Insert a row hairline before every row after the first (only
        // on the 2-col layout — mobile is a single stack).
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
          <li key={article.slug}>
            <Link
              href={`/living/${article.slug}`}
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
        );
        return els;
      })}
    </ul>
  );
}
