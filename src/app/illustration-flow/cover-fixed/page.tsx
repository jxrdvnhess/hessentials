import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "The cover — fixed plane study",
  robots: { index: false, follow: false },
};

/**
 * LOCAL BRAINSTORM — not linked in nav, noindex, uncommitted.
 *
 * The cover-model homepage: a fixed cover plane the page travels over,
 * then the issue's recurring editorial furniture (Aurelian This Week,
 * Currently rotators) scrolling up over it on solid cream.
 *
 * - Cover image is object-contain so the FULL drawing shows (bag, shoes,
 *   the whole composition). The contain margins are the page cream
 *   (#f8f6f3) = the drawing's own ground, so the seams are invisible.
 * - Pure CSS `position: fixed` — NO scroll-listener JS (analytics scar).
 * - Below-cover modules are static mocks here; they map to the real
 *   AurelianThisWeekPanel and RightNow components.
 * - This month the cover IS the Practice feature (Half Revealed =
 *   Practice — Reflection), so there is no separate Practice block.
 *
 * Throwaway route — delete before anything ships.
 */

// Art-directed responsive cover: portrait fills tall phones, a wide
// composition fills desktop. One image can't full-bleed both aspects.
const COVER_MOBILE = "/cover-june-2026.jpg"; // portrait (2:3)
const COVER_DESKTOP = "/arc-bedroom.jpg"; // TEMP wide stand-in — replace with the wide June cover

const CURRENTLY = [
  { kicker: "Cooking", title: "mediterranean shrimp with white beans", payoff: "weeknight food that dresses up.", href: "/recipes/mediterranean-shrimp-white-beans" },
  { kicker: "Wearing", title: "the uniform is not boring", payoff: "the closet stops negotiating with you.", href: "/style/the-uniform-is-not-boring" },
  { kicker: "Refining", title: "the one pot that does everything", payoff: "stop owning twelve. own one.", href: "/living/the-one-pot-that-does-everything" },
  { kicker: "Shopping", title: "the goya thin briefcase", payoff: "soft calfskin. doesn't announce the day.", href: "/shop/loewe-goya-thin-briefcase" },
];

export default function CoverFixedStudy() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      {/* ---------- Fixed cover plane — pinned, full-bleed (cover) -------
           Edge to edge, top to bottom. Wide composition on desktop,
           portrait on mobile — each fills its own aspect without the
           letterbox of object-contain. ---------- */}
      <div className="fixed inset-0 z-0">
        <Image
          src={COVER_DESKTOP}
          alt=""
          fill
          priority
          sizes="100vw"
          className="hidden object-cover object-center md:block"
        />
        <Image
          src={COVER_MOBILE}
          alt=""
          fill
          priority
          sizes="100vw"
          className="object-cover object-center md:hidden"
        />
      </div>

      {/* ---------- First screen: cover story over the fixed plane ------- */}
      <section className="relative z-10 flex min-h-[94svh] w-full items-center justify-center px-6">
        <div
          className="mx-auto max-w-3xl px-10 py-12 text-center"
          style={{
            background:
              "radial-gradient(70% 72% at 50% 50%, rgba(248,246,243,0.82) 0%, rgba(248,246,243,0.45) 52%, rgba(248,246,243,0) 100%)",
          }}
        >
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

      {/* ========== CONTENTS — rises on solid cream over the fixed cover ==
           The recurring editorial furniture of the issue. ============== */}
      <div className="relative z-10 bg-[#f8f6f3]">
        {/* ---- Aurelian — This Week (maps to AurelianThisWeekPanel) ---- */}
        <section className="border-t border-[#1f1d1b]/10 px-6 py-20 text-center sm:px-10 md:py-24">
          <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/50">
            Aurelian — This Week
          </p>
          <p className="mt-3 text-[12px] uppercase tracking-[0.2em] text-[#1f1d1b]/40">
            June 1–7, 2026
          </p>
          <h2 className="text-balance mx-auto mt-7 max-w-2xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal italic leading-[1.25] text-[#2b1f17]">
            The light is near its peak, and the year is near its midpoint.
          </h2>
          <p className="mx-auto mt-5 max-w-md font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/60">
            It feels like a fresh page. It is the same page, later.
          </p>
          <Link
            href="/aurelian"
            className="mt-8 inline-block font-serif text-[16px] italic text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-70"
          >
            Read this week&nbsp;&nbsp;&rarr;
          </Link>
        </section>

        {/* ---- Currently — the rotators (maps to RightNow) ---- */}
        <section className="border-t border-[#1f1d1b]/10 px-6 py-20 sm:px-10 md:px-16 md:py-24">
          <div className="mx-auto max-w-[1100px]">
            <div className="text-center">
              <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/50">
                Currently
              </p>
              <p className="mt-2.5 font-serif text-[13px] italic text-[#1f1d1b]/40">
                What&rsquo;s in rotation right now.
              </p>
            </div>
            <ul className="mt-12 grid grid-cols-1 gap-x-14 gap-y-10 sm:grid-cols-2">
              {CURRENTLY.map((c) => (
                <li key={c.kicker}>
                  <Link href={c.href} className="group block">
                    <p className="text-[10.5px] uppercase tracking-[0.24em] text-[#1f1d1b]/40">
                      {c.kicker}
                    </p>
                    <p className="mt-1.5 font-serif text-[18px] italic leading-[1.35] text-[#1f1d1b]/90 transition-opacity duration-300 ease-out group-hover:opacity-60">
                      {c.title}{" "}
                      <span className="text-[12px] not-italic">&rarr;</span>
                    </p>
                    <p className="mt-1 text-[13px] leading-[1.45] text-[#1f1d1b]/55">
                      {c.payoff}
                    </p>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <p className="mx-auto mt-16 max-w-md text-center text-[12px] leading-[1.6] text-[#1f1d1b]/35">
            Below this: the global footer (newsletter + legal) closes the
            page. The cover above is pinned; this cream contents panel slid
            up over it — pure CSS, no scroll-script.
          </p>
        </section>
      </div>
    </main>
  );
}
