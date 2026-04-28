import Link from "next/link";
import { CURRENT_READING } from "../data/aurelian-weekly";

/**
 * Aurelian — This Week (home hero panel).
 *
 * Right-side anchor in the hero, paired against the H1. Pulls from
 * CURRENT_READING so it stays in sync with /aurelian's This Week block
 * — when Aurelian's weekly reading rolls over on Monday, this panel
 * updates with it.
 *
 * Desktop only — hidden sub-md per spec §1.3. On mobile the hero CTA
 * cluster returns to the left column (handled in home/page.tsx).
 *
 * Animation: fade-up delay-4 — one beat after the H1 (delay-3).
 *
 * Editorial note: `excerpt` is a hand-picked sharpest line from the
 * weekly reading, NOT the opening sentence. Edit alongside `paragraphs`
 * in src/data/aurelian-weekly.ts.
 */
export default function AurelianThisWeekPanel() {
  const { range, headline, excerpt } = CURRENT_READING;

  return (
    <aside
      aria-label="Aurelian — This Week"
      className="fade-up delay-4 absolute right-10 top-1/2 hidden w-[340px] -translate-y-1/2 border-l border-[#1f1d1b]/12 pl-7 md:block lg:right-16 lg:w-[360px]"
    >
      <div className="text-[11px] uppercase leading-[1.5] tracking-[0.28em] text-[#1f1d1b]/55">
        Aurelian &middot; This Week
      </div>
      <div className="mt-1.5 text-[10.5px] uppercase leading-[1.5] tracking-[0.25em] text-[#1f1d1b]/40">
        {range}
      </div>
      <h3 className="text-balance mt-6 font-serif text-[25px] italic leading-[1.22] tracking-[-0.005em] text-[#1f1d1b]">
        {headline}
      </h3>
      <div
        aria-hidden
        className="mt-6 h-px w-7"
        style={{ backgroundColor: "rgba(31,29,27,0.4)" }}
      />
      <p className="mt-5 text-[13.5px] leading-[1.55] text-[#1f1d1b]/70">
        {excerpt}
      </p>
      <Link
        href="/aurelian"
        className="mt-7 inline-block font-serif text-[16px] italic text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-70"
      >
        Read this week&nbsp;&nbsp;&rarr;
      </Link>
    </aside>
  );
}
