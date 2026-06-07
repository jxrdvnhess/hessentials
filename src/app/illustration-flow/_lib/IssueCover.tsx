import Image from "next/image";
import Link from "next/link";

/**
 * LOCAL BRAINSTORM — the issue engine. Content-driven: the page is fixed
 * (masthead, the locked D+C cover treatment, departments, closing); only
 * the `issue` content changes. June and July run this same component — the
 * durability test of the homepage system. Throwaway / noindex per route.
 */

export type Issue = {
  monthYear: string;
  title: string;
  dek: string;
  coverSrc: string;
  essayHref: string;
  currently: readonly (readonly [string, string, string])[];
  whisper: string;
};

const NAV = [
  ["Recipes", "/recipes"], ["Living", "/living"], ["Style", "/style"],
  ["Practice", "/practice"], ["Shop", "/shop"], ["Aurelian", "/aurelian"],
  ["About", "/about"],
] as const;

// Locked direction (D + C): broad, embedded, edges feathered into the page.
const FEATHER_STRONG: React.CSSProperties = {
  WebkitMaskImage: "radial-gradient(112% 122% at 54% 48%, #000 50%, rgba(0,0,0,0) 95%)",
  maskImage: "radial-gradient(112% 122% at 54% 48%, #000 50%, rgba(0,0,0,0) 95%)",
};

function HandRule({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 1200 8" preserveAspectRatio="none" className={`block h-[7px] w-full ${className}`} aria-hidden>
      <path d="M0 4 Q 150 2.2 300 4 T 600 4 T 900 4 T 1200 4" fill="none" stroke="#1f1d1b" strokeOpacity="0.32" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

export default function IssueCover({ issue }: { issue: Issue }) {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <style>{`.sticky.top-0.z-40{display:none!important}`}</style>
      <div className="mx-auto max-w-[1180px] border-x border-[#1f1d1b]/[0.07] px-6 sm:px-10 md:px-14">
        {/* MASTHEAD — permanent. */}
        <header className="flex items-end justify-between gap-6 pt-10 md:pt-12">
          <div>
            <Image src="/hessentials-wordmark.png" alt="Hessentials" width={994} height={255} priority className="h-[30px] w-auto md:h-[34px]" />
            <p className="mt-3 font-serif text-[13px] italic leading-none text-[#1f1d1b]/55">Life, edited well.</p>
          </div>
          <nav className="hidden items-center gap-x-6 pb-1 lg:flex">
            {NAV.map(([label, href]) => (
              <Link key={href} href={href} className="text-[11px] uppercase tracking-[0.18em] text-[#1f1d1b]/60 transition-colors duration-300 hover:text-[#1f1d1b]">{label}</Link>
            ))}
            <span aria-hidden className="text-[#1f1d1b]/40">⌕</span>
          </nav>
        </header>
        <HandRule className="mt-6" />

        {/* THE COVER — locked D+C treatment, content from `issue`. */}
        <section className="relative grid grid-cols-1 items-center gap-y-8 py-12 md:grid-cols-12 md:gap-y-0 md:py-16">
          <Link href={issue.essayHref} aria-label={`Read the essay — ${issue.title}`} className="group order-2 md:order-none md:row-start-1 md:col-start-3 md:col-end-13">
            <Image
              src={issue.coverSrc}
              alt=""
              width={1024}
              height={1536}
              priority
              style={FEATHER_STRONG}
              className="mx-auto h-auto w-[74%] max-w-[340px] transition-opacity duration-500 ease-out group-hover:opacity-90 md:ml-auto md:mr-0 md:w-full md:max-w-[820px]"
            />
          </Link>
          <div className="relative z-10 order-1 md:order-none md:row-start-1 md:col-start-1 md:col-end-8">
            <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/45">{issue.monthYear}</p>
            <h1 className="mt-6 font-serif text-[clamp(3rem,7vw,5.5rem)] font-medium leading-[0.95] tracking-[-0.015em] text-[#2b1f17]">{issue.title}</h1>
            <p className="text-pretty mt-7 max-w-[23rem] font-serif text-[clamp(1.125rem,1.5vw,1.35rem)] italic leading-[1.5] text-[#1f1d1b]/70">{issue.dek}</p>
            <Link href={issue.essayHref} className="group/cta mt-9 inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/70 transition-colors duration-300 hover:text-[#1f1d1b]">
              <span className="border-b border-[#1f1d1b]/30 pb-1 transition-colors duration-300 group-hover/cta:border-[#1f1d1b]/70">Read the essay</span>
              <span aria-hidden>→</span>
            </Link>
          </div>
        </section>

        <HandRule />

        {/* CURRENTLY */}
        <section className="py-10 md:py-12">
          <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/45">Currently</p>
          <ul className="mt-8 grid grid-cols-2 gap-x-8 gap-y-9 md:grid-cols-4">
            {issue.currently.map(([label, line, href]) => (
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

        {/* CLOSING WHISPER + SIGNATURE */}
        <footer className="flex items-end justify-between gap-8 py-9">
          <p className="max-w-[34rem] font-serif text-[clamp(0.95rem,1.4vw,1.15rem)] italic leading-[1.45] text-[#1f1d1b]/55">{issue.whisper}</p>
          <span className="shrink-0 font-serif text-[18px] italic text-[#1f1d1b]/45">JH</span>
        </footer>
      </div>
    </main>
  );
}
