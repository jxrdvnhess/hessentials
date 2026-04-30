import Image from "next/image";
import type { Metadata } from "next";
import AboutEssay from "../../components/AboutEssay";

export const metadata: Metadata = {
  title: "About — Hessentials",
  description: "An editorial home for choosing well.",
};

/**
 * About — sticky-backdrop hero.
 *
 *   merida_moment_5.jpg becomes a full-bleed sticky backdrop. The
 *   essay scrolls over the image; the image stays pinned for the
 *   duration of the essay, then releases and the page continues into
 *   the global SiteFooter unchanged.
 *
 *   Pattern: relative section → absolute child fills it and contains
 *   the sticky h-screen image → relative-positioned essay column drives
 *   section height via top/bottom padding.
 *
 *   Padding math:
 *     pt-[50vh]   — first line sits ~halfway up the viewport at scroll
 *                   0, landing on the wall portion of the image so the
 *                   user sees it immediately and knows to scroll
 *     pb-[100vh]  — sticky releases at the same scroll position the
 *                   last line exits the top (clean release, no dead
 *                   pinned-image runway after the essay)
 *
 *   Mobile (2026-04-30 unification): same sticky pattern as desktop.
 *   The earlier mobile-stacked variant was reconsidered — with
 *   object-left so the wall area dominates the portrait crop, a
 *   uniform vertical scrim for legibility, and the existing cream +
 *   text-shadow on AboutEssay's overlay variant, the editorial weight
 *   (image present through the whole read, signature on the image)
 *   carries to mobile.
 */
export default function AboutPage() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <section aria-label="About Hessentials" className="relative w-full">
        {/* Background layer — fills the entire section. The sticky
            child inside it pins to the viewport top while this layer
            (i.e., the section) is in view. Once the section's bottom
            scrolls past the viewport top, the sticky releases. */}
        <div className="absolute inset-0">
          <div className="sticky top-0 h-screen w-full overflow-hidden">
            <Image
              src="/about/merida-moment-5.jpg"
              alt=""
              fill
              sizes="100vw"
              quality={95}
              priority
              className="object-cover object-left md:object-center"
            />
            {/* MOBILE scrim — uniform vertical darken across the full
                photograph so cream type reads cleanly anywhere in the
                column on a portrait crop. Subtle so the wall still
                carries. */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0 md:hidden"
              style={{
                background:
                  "linear-gradient(to bottom, rgba(20,18,16,0.40) 0%, rgba(20,18,16,0.32) 50%, rgba(20,18,16,0.45) 100%)",
              }}
            />
            {/* DESKTOP scrim — left-side gradient. Holds cream type
                against the wall; transparent on the right (table side
                stays photographically clean). */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0 hidden md:block"
              style={{
                background:
                  "linear-gradient(to right, rgba(20,18,16,0.32) 0%, rgba(20,18,16,0.18) 22%, rgba(20,18,16,0) 55%)",
              }}
            />
          </div>
        </div>

        {/* Foreground — text column. Drives the section's height via
            top/bottom padding so the sticky has scroll runway. Mobile
            uses the full column width with page padding; desktop
            constrains to the left half of the viewport. */}
        <div className="relative z-10 px-6 pt-[50vh] pb-[100vh] sm:px-8 md:max-w-[50vw] md:pl-[8vw] md:pr-[2vw]">
          <AboutEssay variant="overlay" />
        </div>
      </section>
    </main>
  );
}
