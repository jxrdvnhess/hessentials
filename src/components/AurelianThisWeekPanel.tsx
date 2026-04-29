import Link from "next/link";
import { CURRENT_READING } from "../data/aurelian-weekly";

type AurelianThisWeekLayout = "desktop-aside" | "mobile-stacked";

type Props = {
  /**
   * `desktop-aside`  — absolute right-side anchor in the homepage hero,
   *                    paired against the H1. Hidden below md.
   * `mobile-stacked` — relative block stacked beneath the hero copy,
   *                    full-width inside the hero column. Hidden md and up.
   *
   * Same content in both layouts so a mobile visitor meets the same
   * editorial moment a desktop visitor does.
   */
  layout: AurelianThisWeekLayout;
};

/**
 * Aurelian — This Week (home hero panel).
 *
 * Pulls from CURRENT_READING so it stays in sync with /aurelian's This
 * Week block — when Aurelian's weekly reading rolls over on Monday,
 * this panel updates with it.
 *
 * Animation: fade-up delay-4 — one beat after the H1 (delay-3) on both
 * layouts so the panel arrives in the same rhythm.
 *
 * Editorial note: `excerpt` is a hand-picked sharpest line from the
 * weekly reading, NOT the opening sentence. Edit alongside `paragraphs`
 * in src/data/aurelian-weekly.ts.
 */
export default function AurelianThisWeekPanel({ layout }: Props) {
  const { range, headline, excerpt } = CURRENT_READING;

  // The desktop layout is an absolute right-side aside; the mobile
  // layout is a relative stacked block. Same internal content tree;
  // only the wrapper geometry differs.
  const wrapperClass =
    layout === "desktop-aside"
      ? "fade-up delay-4 absolute right-10 top-1/2 hidden w-[340px] -translate-y-1/2 border-l border-[#1f1d1b]/20 pl-7 md:block lg:right-16 lg:w-[360px]"
      : "fade-up delay-4 mt-12 block max-w-[480px] border-l border-[#1f1d1b]/20 pl-6 md:hidden";

  return (
    <aside aria-label="Aurelian — This Week" className={wrapperClass}>
      <div className="text-[11px] uppercase leading-[1.5] tracking-[0.28em] text-[#1f1d1b]/55">
        Aurelian &middot; This Week
      </div>
      <div className="mt-1.5 text-[10.5px] uppercase leading-[1.5] tracking-[0.25em] text-[#1f1d1b]/40">
        {range}
      </div>
      <h3 className="text-balance mt-5 font-serif text-[22px] italic leading-[1.22] tracking-[-0.005em] text-[#1f1d1b] sm:text-[24px] md:mt-6 md:text-[25px]">
        {headline}
      </h3>
      <div
        aria-hidden
        className="mt-5 h-px w-7 md:mt-6"
        style={{ backgroundColor: "rgba(31,29,27,0.4)" }}
      />
      <p className="mt-4 text-[13.5px] leading-[1.55] text-[#1f1d1b]/70 md:mt-5">
        {excerpt}
      </p>
      <Link
        href="/aurelian"
        className="mt-6 inline-block font-serif text-[16px] italic text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-70 md:mt-7"
      >
        Read this week&nbsp;&nbsp;&rarr;
      </Link>
    </aside>
  );
}
