import Image from "next/image";
import type { Metadata } from "next";
import AboutEssay from "../../../components/AboutEssay";

export const metadata: Metadata = {
  title: "About — still figure mock",
  robots: { index: false, follow: false },
};

/**
 * PREVIEW MOCK — not linked in nav, noindex. Live /about untouched.
 *
 * About, version next: no backdrop image. The page sits on the site's
 * own plaster ground like every other page. The essay reads on the
 * left; on the right, THE MAN stands — a made line drawing, back
 * turned, clothed, still (illustration/about_figure.py). He is present
 * while the text runs. No mirror, no motion, no interaction; the
 * column is CSS sticky so he simply stays, the way a person stands in
 * a room you're reading in.
 *
 * Mobile: the figure steps aside entirely; the essay reads alone.
 *
 * If adopted, this replaces the about-room backdrop at /about.
 */
export default function AboutFigureMock() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <section
        aria-label="About Hessentials — still figure mock"
        className="mx-auto w-full max-w-6xl px-7 sm:px-10 md:grid md:grid-cols-[minmax(0,53%)_minmax(0,1fr)] md:gap-x-[5vw]"
      >
        <div className="pb-[35vh] pt-[26vh]">
          <AboutEssay variant="inline" />
        </div>

        <div aria-hidden className="hidden md:block">
          <div className="sticky top-0 flex h-screen items-end justify-center pb-[7vh]">
            <Image
              src="/about/the-man-about.png"
              alt=""
              width={560}
              height={1560}
              priority
              className="h-[76vh] w-auto opacity-90"
            />
          </div>
        </div>
      </section>
    </main>
  );
}
