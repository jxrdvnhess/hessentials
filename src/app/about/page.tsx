import Image from "next/image";
import type { Metadata } from "next";
import AboutEssay from "../../components/AboutEssay";

export const metadata: Metadata = {
  title: "About — Hessentials",
  description: "An editorial home for choosing well.",
  alternates: {
    canonical: "/about",
  },
};

/**
 * About — the essay on the painted side of the wall (2026-06-11).
 *
 *   The backdrop (illustration/about_wall_page.py) is a made drawing of
 *   THE MAN halfway through painting a tall wall in the brand's first
 *   admitted color (clay). The painted side is the essay's living
 *   area — the wash that used to lift the type off the backdrop is now
 *   diegetic: he is the reason the words have somewhere to sit. The
 *   working evidence (roller on its pole, the unfinished strip, the
 *   tray and open can at his feet) stays right of the reading column,
 *   at body height and below; the settled field stays calm where the
 *   reading happens. Cooperative, not quiet.
 *
 *   The wall pins (sticky) while the essay scrolls through the settled
 *   clay field on the left, so the reader reads from inside the room
 *   being made. No cream scrim on desktop — the paint itself carries
 *   the legibility.
 *
 *   Mobile keeps the portrait study (the-man-scene-d.png) with the
 *   vertical wash; the landscape composition needs the width to mean
 *   anything.
 *
 *   Earlier directions — the photoreal hacienda, the picture-that-hung
 *   room, the A/B/C evidence studies — are retired by this page.
 */
export default function AboutPage() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <section aria-label="About Hessentials" className="relative w-full">
        <div className="absolute inset-0">
          <div className="sticky top-0 h-screen w-full overflow-hidden">
            {/* Desktop — landscape wall, composed for the reading column */}
            <Image
              src="/about/about-wall-wide.jpg"
              alt=""
              fill
              sizes="100vw"
              quality={92}
              priority
              className="hidden object-cover object-center md:block"
            />
            {/* Mobile — portrait study; the vertical wash carries the text */}
            <Image
              src="/about/the-man-scene-d.png"
              alt=""
              fill
              sizes="100vw"
              quality={92}
              priority
              className="object-cover object-center md:hidden"
            />
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0 md:hidden"
              style={{
                background:
                  "linear-gradient(to bottom, rgba(244,240,232,0.86) 0%, rgba(244,240,232,0.62) 46%, rgba(244,240,232,0.86) 100%)",
              }}
            />
          </div>
        </div>

        <div className="relative z-10 px-7 pb-[90vh] pt-[30vh] sm:px-10 md:max-w-[44vw] md:pl-[6vw] md:pr-[2vw]">
          <AboutEssay variant="inline" />
        </div>
      </section>
    </main>
  );
}
