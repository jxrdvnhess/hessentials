import Image from "next/image";
import type { Metadata } from "next";
import AboutEssay from "../../../../components/AboutEssay";

export const metadata: Metadata = {
  title: "About mock — the frame",
  robots: { index: false, follow: false },
};

/**
 * PREVIEW MOCK — Jordan's frame direction, 2026-06-10.
 *
 * The drawing and the essay are one object: the back-facing figure
 * adjusts a large, slightly crooked frame, and the About essay lives
 * INSIDE the frame. The text container sits at the frame's interior
 * coordinates (from illustration/about_frame.py) and carries the same
 * 0.8deg rotation, so the frame literally holds the ideas. Scrolling
 * happens inside the frame via plain CSS overflow — no scroll JS.
 *
 * Figure, wall, frame, text. Nothing else.
 *
 * Mobile: the composition needs width; small screens get the drawing,
 * then the essay in normal flow beneath it.
 */
export default function AboutFrameMock() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      {/* Desktop: one-viewport composition, the essay scrolls inside the frame */}
      <section
        aria-label="About Hessentials — frame mock"
        className="hidden h-screen items-center justify-center overflow-hidden md:flex"
      >
        <div className="relative h-[94vh] max-w-[94vw]" style={{ aspectRatio: "1180 / 1240" }}>
          <Image
            src="/about/the-man-frame.png"
            alt=""
            fill
            priority
            sizes="94vh"
            className="pointer-events-none select-none object-contain"
          />
          {/* The frame's interior — x 116..690, y 440..1130 of 1180x1240,
              rotated with the drawn frame about the same center. */}
          <div
            className="absolute"
            style={{
              left: "9.83%",
              top: "35.48%",
              width: "48.64%",
              height: "55.65%",
              transform: "rotate(0.8deg)",
            }}
          >
            <div className="h-full overflow-y-auto px-[7%] py-[8%] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
              <AboutEssay variant="inline" />
            </div>
          </div>
        </div>
      </section>

      {/* Small screens: drawing above, essay in normal flow */}
      <section className="px-7 pb-24 pt-16 md:hidden">
        <Image
          src="/about/the-man-frame.png"
          alt=""
          width={1180}
          height={1240}
          priority
          className="mx-auto mb-12 w-full max-w-md"
        />
        <AboutEssay variant="inline" />
      </section>
    </main>
  );
}
