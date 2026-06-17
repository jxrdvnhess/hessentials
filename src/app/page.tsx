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

/**
 * Currently — each department surfaces one current pick, and the set
 * rotates hourly (deterministic by the clock, so there's no client JS and
 * no flash — see the scroll-listener scar). The value is fixed at
 * render/revalidation, server-side.
 *
 * Recipes are chosen by season (early-summer plates). The other three lead
 * with editorial strength and, where GA shows it, traction: as of
 * 2026-06-07 only one article ("What the Cows Know") has meaningful reads,
 * so ranking by analytics would be noise. These sets stay editorially
 * curated until article-level traffic is real; the shape here is already
 * what a GA-driven "top + needs-a-boost" feed will populate. Lines reuse
 * the pieces' own approved copy (recipe descriptions, Style subtitles,
 * titles) — not new editorial.
 */
type Pick = { line: string; href: string };
type Department = { label: string; picks: readonly Pick[] };

const CURRENTLY: readonly Department[] = [
  {
    label: "In the Kitchen",
    picks: [
      { line: "The plate that asks the least and gives the most.", href: "/recipes/tomato-and-burrata-with-warm-olive-oil" },
      { line: "The summer plate, simplified.", href: "/recipes/caprese-chicken" },
      { line: "Charred salmon. Sharp citrus. Cool dill.", href: "/recipes/grilled-salmon-with-citrus-and-dill-yogurt" },
      { line: "Cucumber, tomato, feta. Lemon and oil.", href: "/recipes/chopped-mediterranean-salad" },
    ],
  },
  {
    label: "At Home",
    picks: [
      { line: "Summer bedding: cotton, not plush.", href: "/living/stop-buying-plush-blankets-use-cotton" },
      { line: "You're not bad with plants.", href: "/living/youre-not-bad-with-plants" },
      { line: "Stop owning twelve. Own one.", href: "/living/the-one-pot-that-does-everything" },
    ],
  },
  {
    label: "On the Table",
    picks: [
      { line: "Same food, different plate. A different meal.", href: "/style/the-dinner-plate-is-a-style-object" },
      { line: "Some rooms aren't dressed well.", href: "/style/your-home-has-an-outfit-too" },
      { line: "It argues before you say a word.", href: "/style/the-entryway-test" },
    ],
  },
  {
    label: "In Practice",
    picks: [
      { line: "What was I watching?", href: "/practice/what-was-i-watching" },
      { line: "What the cows know.", href: "/practice/what-the-cows-know" },
      { line: "I stopped drinking at 30.", href: "/practice/i-stopped-drinking-at-30" },
      { line: "Five minutes. No app.", href: "/practice/silence-five-minutes-no-app" },
    ],
  },
];

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
        {/* ===== MASTHEAD LOCKUP — homepage only =====
            The wordmark lives in the global header above; here the tagline +
            drawn rule complete the cover masthead, so the homepage reads as
            the front of the current issue. Interior pages keep just the clean
            global bar and go straight into content. */}
        <div className="pt-6 md:pt-8">
          <p className="font-serif text-[clamp(1rem,1.6vw,1.25rem)] italic leading-none text-[#1f1d1b]/60">
            Life, edited well.
          </p>
        </div>
        <HandRule className="mt-5 md:mt-6" />

        {/* ============ THE COVER ============ */}
        <section className="relative grid grid-cols-1 items-center gap-y-8 pt-9 pb-12 md:grid-cols-12 md:gap-y-0 md:pt-12 md:pb-16">
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
            {CURRENTLY.map((dept, i) => {
              // Deterministic hourly rotation, offset per department so they
              // don't all advance in lockstep. This is a Server Component
              // baked per ISR revalidation (revalidate=3600), so reading the
              // clock is intentional and safe — the value is fixed in the
              // cached HTML for the hour, never re-evaluated on a client; no
              // client JS, no scroll listener.
              // eslint-disable-next-line react-hooks/purity
              const seed = Math.floor(Date.now() / 3_600_000) + i;
              const pick = dept.picks[seed % dept.picks.length];
              return (
                <li key={dept.label}>
                  <Link href={pick.href} className="group block">
                    <p className="font-serif text-[17px] leading-[1.2] text-[#2b1f17]">{dept.label}</p>
                    <p className="mt-2 font-serif text-[14px] italic leading-[1.4] text-[#1f1d1b]/60">{pick.line}</p>
                    <span className="mt-3 inline-block text-[13px] text-[#1f1d1b]/40 transition-colors duration-300 group-hover:text-[#1f1d1b]/80">→</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </section>

      </div>
    </main>
  );
}
