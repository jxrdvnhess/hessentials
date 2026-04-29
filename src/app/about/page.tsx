import Image from "next/image";
import type { Metadata } from "next";
import AboutEssay from "../../components/AboutEssay";

export const metadata: Metadata = {
  title: "About — Hessentials",
  description: "An editorial home for choosing well.",
};

/**
 * About — sticky-backdrop hero (2026-04-29 spec).
 *
 *   merida_moment_5.jpg becomes a full-bleed sticky backdrop. The
 *   essay scrolls over the left half of the image; the image stays
 *   pinned for the duration of the essay, then releases and the page
 *   continues into the global SiteFooter (merida_moment_6 + newsletter
 *   + legal) unchanged.
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
 *   Mobile (sub-md): sticky pattern is abandoned per spec — sticky
 *   over portrait crops always reads worse than a clean stacked
 *   layout. Image renders as a standard hero, essay flows beneath in
 *   normal document order.
 */
export default function AboutPage() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      {/* ---------- DESKTOP (md+) — sticky backdrop ---------- */}
      <section
        aria-label="About Hessentials"
        className="relative hidden w-full md:block"
      >
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
              className="object-cover object-center"
            />
            {/* Subtle left-side scrim — only enough to hold cream type
                against the wall. Transparent on the right (table side
                stays clean). */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0"
              style={{
                background:
                  "linear-gradient(to right, rgba(20,18,16,0.32) 0%, rgba(20,18,16,0.18) 22%, rgba(20,18,16,0) 55%)",
              }}
            />
          </div>
        </div>

        {/* Foreground — text column. Drives the section's height via
            top/bottom padding so the sticky has scroll runway. */}
        <div className="relative z-10 max-w-[50vw] pt-[50vh] pb-[100vh] pl-[8vw] pr-[2vw]">
          <AboutEssay variant="overlay" />
        </div>
      </section>

      {/* ---------- MOBILE (sub-md) — stacked hero + flow ---------- */}
      <section
        aria-label="About Hessentials"
        className="block md:hidden"
      >
        <div className="relative aspect-[4/5] w-full overflow-hidden">
          <Image
            src="/about/merida-moment-5.jpg"
            alt=""
            fill
            sizes="100vw"
            quality={95}
            priority
            className="object-cover object-center"
          />
        </div>
        <div className="px-6 pt-12 pb-20 sm:px-8 sm:pt-16">
          <AboutEssay variant="inline" />
        </div>
      </section>
    </main>
  );
}
