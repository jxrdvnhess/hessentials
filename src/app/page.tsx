import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";
import { getCurrentReading } from "../data/aurelian-weekly";

export const metadata: Metadata = {
  title: "Hessentials",
  description:
    "A curated editorial home for choosing well. One issue at a time — food, home, style, and the conditions underneath a considered life.",
  alternates: { canonical: "/" },
};

/**
 * Revalidate hourly so the Aurelian This Week band's auto-computed date
 * range rolls over within an hour of Monday morning without a redeploy.
 */
export const revalidate = 3600;

/**
 * Homepage — the cover model (2026-06-07).
 *
 * The homepage is the current issue's COVER (doctrine Amendment II). Two
 * layers: the permanent masthead (the global SiteHeader) and the monthly
 * cover (one cover illustration + cover story). The standards stay; the
 * selections change.
 *
 * Direction (locked): D + C — evidence-only made drawing, no figure,
 * embedded into the page on the same sheet as the type (edges feathered
 * into the cream); the page composition carries the weight, never a hero
 * banner. Illustration craft keeps improving over time; the system does
 * not wait for it.
 *
 * Aurelian — This Week gets its own prominent band: the covers, essays,
 * and recipes rotate, but Aurelian returns weekly, so it's the strongest
 * recurring relationship on the site and reads as one.
 *
 * Deferred (brand-system phase, intentionally not in this launch):
 *   - Masthead restyle (tagline "Life, edited well." + drawn rule into
 *     the global SiteHeader), the page frame, and retiring RightNow's
 *     scroll-reveal. Tracked for the next pass.
 *
 * June issue cover: /public/cover-june-final.jpg. Swap the const below to
 * change the cover; everything else is content, not structure.
 */

const COVER = "/cover-june-final.jpg";

// Locked treatment: broad, embedded, edges dissolved into the page.
const FEATHER_STRONG: React.CSSProperties = {
  WebkitMaskImage: "radial-gradient(112% 122% at 54% 48%, #000 50%, rgba(0,0,0,0) 95%)",
  maskImage: "radial-gradient(112% 122% at 54% 48%, #000 50%, rgba(0,0,0,0) 95%)",
};

const CURRENTLY = [
  ["In the Kitchen", "Early summer suppers.", "/recipes"],
  ["At Home", "Open windows. Edited rooms.", "/living"],
  ["On the Table", "Simple settings that last.", "/style"],
  ["In Practice", "Thoughts for the season.", "/practice"],
] as const;

function HandRule({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 1200 8" preserveAspectRatio="none" className={`block h-[7px] w-full ${className}`} aria-hidden>
      <path d="M0 4 Q 150 2.2 300 4 T 600 4 T 900 4 T 1200 4" fill="none" stroke="#1f1d1b" strokeOpacity="0.3" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

export default function HomePage() {
  const { range, headline, excerpt } = getCurrentReading();

  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <div className="mx-auto max-w-[1180px] px-6 sm:px-10 md:px-14">
        {/* ============ THE COVER ============ */}
        <section className="relative grid grid-cols-1 items-center gap-y-8 pt-8 pb-12 md:grid-cols-12 md:gap-y-0 md:pt-12 md:pb-16">
          <Link
            href="/half-revealed"
            aria-label="Read the essay — Half revealed."
            className="group order-2 md:order-none md:col-start-3 md:col-end-13 md:row-start-1"
          >
            <Image
              src={COVER}
              alt=""
              width={1024}
              height={1536}
              priority
              style={FEATHER_STRONG}
              className="mx-auto h-auto w-[74%] max-w-[340px] transition-opacity duration-500 ease-out group-hover:opacity-90 md:ml-auto md:mr-0 md:w-full md:max-w-[820px]"
            />
          </Link>
          <div className="relative z-10 order-1 md:order-none md:col-start-1 md:col-end-8 md:row-start-1">
            <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/45">June 2026</p>
            <h1 className="mt-6 font-serif text-[clamp(3rem,7vw,5.5rem)] font-medium leading-[0.95] tracking-[-0.015em] text-[#2b1f17]">
              Half revealed.
            </h1>
            <p className="text-pretty mt-7 max-w-[23rem] font-serif text-[clamp(1.125rem,1.5vw,1.35rem)] italic leading-[1.5] text-[#1f1d1b]/70">
              In January we are designing a house. In June we are discovering which rooms we actually live in.
            </p>
            <Link
              href="/half-revealed"
              className="group/cta mt-9 inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/70 transition-colors duration-300 hover:text-[#1f1d1b]"
            >
              <span className="border-b border-[#1f1d1b]/30 pb-1 transition-colors duration-300 group-hover/cta:border-[#1f1d1b]/70">
                Read the essay
              </span>
              <span aria-hidden>→</span>
            </Link>
          </div>
        </section>

        <HandRule />

        {/* ============ AURELIAN — THIS WEEK (the recurring relationship) ============ */}
        <section aria-label="Aurelian — This Week" className="py-14 text-center md:py-20">
          <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/50">Aurelian — This Week</p>
          <p className="mt-3 text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/40">{range}</p>
          <h2 className="text-balance mx-auto mt-7 max-w-2xl font-serif text-[clamp(1.6rem,2.8vw,2.2rem)] font-normal italic leading-[1.25] text-[#2b1f17]">
            {headline}
          </h2>
          <p className="mx-auto mt-5 max-w-md text-[14px] leading-[1.6] text-[#1f1d1b]/65">{excerpt}</p>
          <Link
            href="/aurelian"
            className="mt-8 inline-block font-serif text-[16px] italic text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-70"
          >
            Read this week&nbsp;&nbsp;&rarr;
          </Link>
        </section>

        <HandRule />

        {/* ============ CURRENTLY ============ */}
        <section aria-label="Currently" className="py-12 md:py-14">
          <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/45">Currently</p>
          <ul className="mt-8 grid grid-cols-2 gap-x-8 gap-y-9 md:grid-cols-4">
            {CURRENTLY.map(([label, line, href]) => (
              <li key={label}>
                <Link href={href} className="group block">
                  <p className="font-serif text-[17px] leading-[1.2] text-[#2b1f17]">{label}</p>
                  <p className="mt-2 font-serif text-[14px] italic leading-[1.4] text-[#1f1d1b]/60">{line}</p>
                  <span className="mt-3 inline-block text-[13px] text-[#1f1d1b]/40 transition-colors duration-300 group-hover:text-[#1f1d1b]/80">→</span>
                </Link>
              </li>
            ))}
          </ul>
        </section>

        <HandRule />

        {/* ============ CLOSING WHISPER ============ */}
        <div className="flex items-end justify-between gap-8 py-9">
          <p className="max-w-[34rem] font-serif text-[clamp(0.95rem,1.4vw,1.15rem)] italic leading-[1.45] text-[#1f1d1b]/55">
            The year isn&rsquo;t half over. It&rsquo;s half revealed.
          </p>
          <span className="shrink-0 font-serif text-[18px] italic text-[#1f1d1b]/45">JH</span>
        </div>
      </div>
    </main>
  );
}
