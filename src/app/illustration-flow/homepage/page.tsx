import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "The cover — study",
  robots: { index: false, follow: false },
};

/**
 * LOCAL BRAINSTORM — not linked in nav, noindex, uncommitted.
 *
 * The homepage rebuilt as the COVER, per the doctrine amendment
 * (2026-06-07, "The Homepage Is the Cover").
 *
 * Two layers:
 *  - Masthead (permanent): the global SiteHeader and SiteFooter render
 *    here automatically; the issue line, cover story, and cover lines
 *    are the only body. The standards stay.
 *  - Cover (per issue): ONE cover illustration + ONE cover story + the
 *    cover lines into the rest of the issue. No rotation, no sequence,
 *    no arc. The selections change.
 *
 * June 2026 cover: "Half revealed." Cover art = the bedroom, chosen as
 * the best illustration of the QUESTION (something happened here), not
 * of the article. The paper belongs to the artwork: the drawing feathers
 * into the clean cream interface; the interface itself stays flat ivory,
 * never a paper texture.
 *
 * Throwaway route — delete before anything ships.
 */

const COVER = "/arc-bedroom.jpg";

// The drawing dissolves into the page ground (#f8f6f3) — ink on the
// interface, not a sheet laid on top. No texture on the interface itself.
const featherAll: React.CSSProperties = {
  WebkitMaskImage:
    "radial-gradient(120% 132% at 50% 44%, #000 58%, rgba(0,0,0,0) 100%)",
  maskImage:
    "radial-gradient(120% 132% at 50% 44%, #000 58%, rgba(0,0,0,0) 100%)",
};

// Cover lines — the teasers into the rest of the issue. Pillar voices,
// kept subordinate to the cover.
const COVER_LINES = [
  { kicker: "Recipes", line: "Food that earns its place.", href: "/recipes" },
  { kicker: "Living", line: "Some things feel good. Some things work.", href: "/living" },
  { kicker: "Style", line: "What to wear. What to keep. What to ignore.", href: "/style" },
  { kicker: "Practice", line: "Honest practice. No doctrine.", href: "/practice" },
];

export default function CoverHomepageStudy() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      {/* ========== THE COVER ========== */}
      <section className="px-6 pt-14 sm:px-10 md:px-16 md:pt-20">
        {/* Issue line — the only thing above the cover story. */}
        <p className="text-center text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/45">
          June 2026
        </p>

        {/* Cover story title + the question (its dek). The title is the
            issue's story; the masthead wordmark above (global header) is
            the publication. */}
        <div className="mx-auto mt-10 max-w-3xl text-center md:mt-14">
          <h1 className="font-serif text-[clamp(2.75rem,7vw,5rem)] font-normal italic leading-[1.02] tracking-[-0.02em] text-balance text-[#2b1f17]">
            Half revealed.
          </h1>
          <p className="text-pretty mx-auto mt-7 max-w-xl font-serif text-[clamp(1.125rem,1.7vw,1.4rem)] italic leading-[1.5] text-[#1f1d1b]/70">
            In January we are designing a house. In June we are discovering
            which rooms we actually live in.
          </p>
        </div>

        {/* Cover illustration — the face of the issue. One image. */}
        <Link
          href="/half-revealed"
          aria-label="Read the article — Half revealed."
          className="group mx-auto mt-12 block w-full max-w-[1080px] md:mt-16"
        >
          <Image
            src={COVER}
            alt=""
            width={1402}
            height={1122}
            style={featherAll}
            priority
            className="h-auto w-full transition-opacity duration-500 ease-out group-hover:opacity-90"
          />
        </Link>

        {/* Enter the issue. */}
        <div className="mt-10 text-center md:mt-12">
          <Link
            href="/half-revealed"
            className="inline-block font-serif text-[17px] italic text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-70"
          >
            Read the article&nbsp;&nbsp;&rarr;
          </Link>
        </div>
      </section>

      {/* ========== COVER LINES — into the rest of the issue ========== */}
      <section className="px-6 pb-28 pt-24 sm:px-10 md:px-16 md:pb-36 md:pt-32">
        <div aria-hidden className="mx-auto mb-12 h-px w-10 bg-[#1f1d1b]/15" />
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
