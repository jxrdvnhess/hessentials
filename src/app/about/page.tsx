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
 * About — the essay, inside a room after a decision.
 *
 *   The backdrop (illustration/about_room.py) is a made graphite drawing of a
 *   wall in raking light where a picture once hung: the un-faded rectangle the
 *   frame protected, the nail still above it, the room's light falling past.
 *   Observed, not symbolized — nothing announces itself; meaning accumulates.
 *
 *   The wall pins (sticky) while the essay scrolls through the open light on
 *   the left, so the reader reads from inside the room. Dark ink on the lit
 *   wall; a faint cream wash lifts the type off the graphite shading. The
 *   essay is a worked proof — a discerning reader's residue on the words
 *   (circle, underline, margin rule; see AboutEssay).
 *
 *   Earlier directions — the photoreal hacienda, the made-drawing backdrop,
 *   and the name-as-wallpaper studies — are all retired. The page is a place,
 *   not a brand mark.
 */
export default function AboutPage() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <section aria-label="About Hessentials" className="relative w-full">
        <div className="absolute inset-0">
          <div className="sticky top-0 h-screen w-full overflow-hidden">
            <Image
              src="/about/about-room.jpg"
              alt=""
              fill
              sizes="100vw"
              quality={92}
              priority
              className="object-cover object-center"
            />
            {/* Soft cream wash over the reading (left) side — lifts dark ink
                off the wall's graphite shading without darkening the room. */}
            <div
              aria-hidden
              className="pointer-events-none absolute inset-0 hidden md:block"
              style={{
                background:
                  "linear-gradient(to right, rgba(244,240,232,0.84) 0%, rgba(244,240,232,0.52) 32%, rgba(244,240,232,0.12) 50%, rgba(244,240,232,0) 60%)",
              }}
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

        <div className="relative z-10 px-7 pb-[90vh] pt-[30vh] sm:px-10 md:max-w-[47vw] md:pl-[7vw] md:pr-[2vw]">
          <AboutEssay variant="inline" />
        </div>
      </section>
    </main>
  );
}
