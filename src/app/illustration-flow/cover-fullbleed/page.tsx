import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "The cover — full bleed study",
  robots: { index: false, follow: false },
};

/**
 * LOCAL BRAINSTORM — not linked in nav, noindex, uncommitted.
 *
 * Full-bleed variant of the cover homepage, to compare against the
 * feathered version at /illustration-flow/homepage. Here the cover
 * illustration fills the viewport and the cover story overlays it —
 * the most literal reading of "the homepage IS the cover."
 *
 * Caveats this mock makes visible (judge with these in mind):
 *  - The bedroom is composed landscape with soft dissolve edges; cropped
 *    to fill the screen, those honest edges are lost and it reads more
 *    like a hero than a made object. A real full-bleed cover would be
 *    generated PORTRAIT with deliberate empty space reserved for the
 *    masthead and title.
 *  - The global masthead (sticky header) still sits as a band on top;
 *    a true full-bleed cover would float the masthead transparently
 *    over the art (a global-header change, not done here).
 *
 * Throwaway route — delete before anything ships.
 */

const COVER = "/arc-bedroom.jpg";

const COVER_LINES = [
  { kicker: "Recipes", line: "Food that earns its place.", href: "/recipes" },
  { kicker: "Living", line: "Some things feel good. Some things work.", href: "/living" },
  { kicker: "Style", line: "What to wear. What to keep. What to ignore.", href: "/style" },
  { kicker: "Practice", line: "Honest practice. No doctrine.", href: "/practice" },
];

export default function CoverFullBleedStudy() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      {/* ========== FULL-BLEED COVER ========== */}
      <section className="relative flex min-h-[92svh] w-full items-center justify-center overflow-hidden">
        {/* The cover fills the frame. */}
        <Image
          src={COVER}
          alt=""
          fill
          priority
          sizes="100vw"
          className="object-cover object-center"
        />
        {/* The faintest cream wash so the serif holds over the busier
            lower third — kept very light so it never reads as a scrim. */}
        <div
          aria-hidden
          className="absolute inset-0"
          style={{
            background:
              "radial-gradient(120% 90% at 50% 42%, rgba(248,246,243,0.55) 0%, rgba(248,246,243,0.12) 45%, rgba(248,246,243,0) 70%)",
          }}
        />

        {/* Cover story overlaid. */}
        <div className="relative mx-auto max-w-3xl px-6 text-center">
          <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/55">
            June 2026
          </p>
          <h1 className="mt-8 font-serif text-[clamp(2.75rem,7vw,5.25rem)] font-normal italic leading-[1.0] tracking-[-0.02em] text-balance text-[#2b1f17]">
            Half revealed.
          </h1>
          <p className="text-pretty mx-auto mt-7 max-w-xl font-serif text-[clamp(1.125rem,1.7vw,1.4rem)] italic leading-[1.5] text-[#1f1d1b]/75">
            In January we are designing a house. In June we are discovering
            which rooms we actually live in.
          </p>
          <Link
            href="/half-revealed"
            className="mt-9 inline-block font-serif text-[17px] italic text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-70"
          >
            Read the article&nbsp;&nbsp;&rarr;
          </Link>
        </div>
      </section>

      {/* ========== COVER LINES — below the fold, on the clean page ====== */}
      <section className="px-6 pb-28 pt-24 sm:px-10 md:px-16 md:pb-36 md:pt-28">
        <p className="text-center text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/45">
          Always here
        </p>
        <ul className="mx-auto mt-10 grid max-w-3xl grid-cols-1 gap-x-14 gap-y-8 sm:grid-cols-2">
          {COVER_LINES.map((c) => (
            <li key={c.kicker} className="text-center sm:text-left">
              <Link href={c.href} className="group inline-block">
                <p className="text-[10.5px] uppercase tracking-[0.24em] text-[#1f1d1b]/40">
                  {c.kicker}
                </p>
                <p className="mt-1.5 font-serif text-[18px] italic leading-[1.35] text-[#1f1d1b]/90 transition-opacity duration-300 ease-out group-hover:opacity-60">
                  {c.line}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
