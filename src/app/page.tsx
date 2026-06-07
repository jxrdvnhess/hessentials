import type { Metadata } from "next";
import RightNow from "../components/RightNow";
import Symbol from "../components/Symbol";
import AurelianThisWeekPanel from "../components/AurelianThisWeekPanel";
import HalfRevealedModule from "../components/HalfRevealedModule";
import NewsletterSignup from "../components/NewsletterSignup";
import UnderRenovation from "../components/UnderRenovation";

export const metadata: Metadata = {
  title: "Hessentials",
  description:
    "Food, home, and style for people who want better defaults, not more options. Recipes, rooms, and small upgrades worth the time.",
  alternates: {
    canonical: "/",
  },
};

/**
 * Revalidate hourly so the Aurelian This Week panel's auto-computed
 * date range (`May 4–10, 2026`) rolls over within an hour of Monday
 * morning without requiring a redeploy. Editorial copy still rolls
 * with a push — see src/data/aurelian-weekly.ts.
 */
export const revalidate = 3600;

/**
 * Homepage — Version Next (2026-05-27).
 *
 * Subtractive edit per the Homepage Version Next brief. The cinematic
 * Mérida photo arc (Image 01/02/03 + the Practice statement teaser
 * that carried "What was real, stayed.") came off — AI-photorealistic
 * imagery violates the brand doctrine: Hessentials does not
 * counterfeit human experience. The page now moves from the
 * Memorial Day featured moment directly into the clean cream
 * SiteFooter (also de-Mérida'd in the same brief).
 *
 * Kept, unchanged: the hero (H1 + subhead + "Less to decide. More
 * that works." + Aurelian This Week panel), the CURRENTLY pillar
 * previews, the inline newsletter.
 *
 * Featured moment slot (2026-06-07): Memorial Day archived off the
 * homepage now that the holiday has passed. Replaced by the
 * "Half revealed." midyear Practice piece (HalfRevealedModule +
 * /half-revealed), now live with its made image at
 * /public/half-revealed.jpg.
 *
 * Atmosphere now comes from spacing, typography, pacing, and
 * restraint — not from a hero or background image carrying the
 * weight. This is version one of an accumulation, not the final
 * system; "continuity" and "the final system" are explicitly out of
 * scope at this stage.
 *
 * Prior architecture documented for the next iteration:
 *   - The Cinematic component was inline in this file and is
 *     removed with the sections that used it.
 *   - HomePracticeTeaser and ImagePoemLine remain in the codebase
 *     as orphaned components — not deleted per scope-strict rule.
 *   - merida-moment-*.jpg assets remain in /public/home/ but are
 *     no longer referenced.
 */

const GAP_FOOTER = "96px"; // featured moment → SiteFooter — preserved from prior arc closer

export default function HomePage() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      {/* ---------- Hero — H1 left, Aurelian This Week panel right (md+).
          §1.2 — min-h compressed to 42vh with items-end so the H1 sits
          near the bottom and CURRENTLY enters the viewport at ~30–40%
          of its height (first cut of a film, not a portrait).
          §1.3 — Aurelian This Week panel anchors the right side on md+;
          on mobile, the original "If you're new, start here / Aurelian"
          CTA cluster returns to the left column. */}
      <section className="relative flex min-h-0 items-start px-6 pt-14 pb-4 sm:px-10 md:min-h-[88vh] md:items-end md:pt-24 md:px-16">
        <div className="fade-up delay-3 max-w-[520px]">
          <p className="mb-5 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px] md:mb-10">
            Hessentials
          </p>
          <h1 className="font-serif text-[clamp(2.5rem,7vw,4.5rem)] font-normal leading-[1.02] tracking-[-0.02em] text-balance">
            Life, edited well.
          </h1>
          <p className="text-pretty mt-5 font-serif text-[clamp(1.125rem,1.9vw,1.5rem)] italic leading-[1.45] text-[#1f1d1b]/70 md:mt-8">
            Food, home, and style for people who want better defaults, not more options.
          </p>
          {/* Direct, blunt clarification. Tells the reader what they're getting. */}
          <p className="mt-3 max-w-[420px] text-[13px] leading-[1.55] text-[#1f1d1b]/55 sm:text-[13.5px] md:mt-6">
            Less to decide. More that works.
          </p>
          {/* Mobile Aurelian This Week — replaces the old "If you're
              new, start here / Aurelian — a short reading" CTA cluster
              so mobile visitors meet the same editorial moment desktop
              visitors do. Same content as the desktop aside, stacked
              under the hero copy. Tightened mt on mobile so the
              headline sits above the fold at 390x844. */}
          <AurelianThisWeekPanel layout="mobile-stacked" />
        </div>

        {/* Aurelian This Week — desktop right-side aside (md+). */}
        <AurelianThisWeekPanel layout="desktop-aside" />

        {/* Hero asymmetry mark — quiet "h" anchoring the upper-right
            quadrant. Hidden on md+ (the Aurelian panel now anchors that
            zone with real content). */}
        <div
          aria-hidden
          className="pointer-events-none absolute right-6 top-12 hidden opacity-25 sm:right-10 sm:block md:hidden"
        >
          <Symbol size="xs" />
        </div>
      </section>

      {/*
        Currently — pillar previews (COOKING / WEARING / REFINING /
        SHOPPING). The highest-intent surface on the site — editorial
        navigation into what's on rotation right now — so it reads
        first, before the seasonal feature. Visible at every breakpoint.
      */}
      <section
        aria-label="Currently"
        className="px-6 pt-12 pb-4 sm:px-10 sm:pt-14 md:px-16 md:pt-16 md:pb-6"
      >
        <div className="mx-auto max-w-[480px]">
          <RightNow variant="default" />
        </div>
      </section>

      {/*
        Inline newsletter — sits between Currently and the seasonal
        feature so a mobile visitor meets the form before the seasonal
        feature opens. The footer instance still ships; this one closes
        the gap for visitors who never reach the close. No pop-up, no
        sticky bar.
      */}
      <section
        aria-label="Newsletter"
        className="border-t border-[#1f1d1b]/10 px-6 py-14 sm:px-10 sm:py-16 md:px-16 md:py-20"
      >
        <NewsletterSignup pillar="default" source="inline" />
      </section>

      {/*
        Featured moment — "Half revealed." midyear Practice piece.

        Sits in the slot Memorial Day (and Mother's Day before it)
        occupied. Memorial Day was archived off the homepage; its
        component and the /memorial-day article page remain in the repo
        per the Mother's Day convention (direct link stands). The made
        dusk-interior drawing lives at /public/half-revealed.jpg.
      */}
      <div style={{ marginTop: "4vh" }}>
        <HalfRevealedModule />
      </div>

      {/*
        "Under renovation" placeholder graphic — hand-drawn scaffolding +
        tools + hanging sign. Approved by Jordan, landed alongside Version
        Next per a separate brief. Sits on the cream ground (the SVG
        carries its own slightly warmer linen ground so it reads as a
        contained moment, not as a section change). Symmetric 96px
        gutters above and below before the SiteFooter takes over.
      */}
      <div style={{ marginTop: GAP_FOOTER, marginBottom: GAP_FOOTER }}>
        <UnderRenovation />
      </div>
    </main>
  );
}
