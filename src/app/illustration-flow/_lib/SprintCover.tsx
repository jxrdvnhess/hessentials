import Image from "next/image";
import Link from "next/link";

/**
 * LOCAL BRAINSTORM ENGINE — shared by the A/B/C/D sprint routes.
 * Same editorial page; only the cover treatment changes per variant.
 * Not linked in nav, noindex via each route. Throwaway — delete before ship.
 */

type Variant = "A" | "B" | "C" | "D" | "FINAL";

const V: Record<
  Variant,
  { label: string; src: string; img: string; imax: string; txt: string; feather: "none" | "subtle" | "strong"; op: string }
> = {
  A: { label: "A · Current", src: "/cover-june.jpg",
       img: "md:col-start-6 md:col-end-13", imax: "md:max-w-[500px]", txt: "md:col-start-1 md:col-end-7", feather: "none", op: "" },
  B: { label: "B · Architectural", src: "/cover-june.jpg",
       img: "md:col-start-5 md:col-end-13", imax: "md:max-w-[640px]", txt: "md:col-start-1 md:col-end-8", feather: "subtle", op: "" },
  C: { label: "C · Embedded drawing", src: "/cover-june.jpg",
       img: "md:col-start-3 md:col-end-13", imax: "md:max-w-[760px]", txt: "md:col-start-1 md:col-end-8", feather: "strong", op: "opacity-90" },
  D: { label: "D · No figure", src: "/cover-june-nofigure.jpg",
       img: "md:col-start-5 md:col-end-13", imax: "md:max-w-[640px]", txt: "md:col-start-1 md:col-end-8", feather: "subtle", op: "" },
  // D's composition (no figure) + C's philosophy (embedded, broad, no image
  // boundary) — the approved direction. Refined drawing + intentional light.
  FINAL: { label: "Final · D + C", src: "/cover-june-final.jpg",
       img: "md:col-start-3 md:col-end-13", imax: "md:max-w-[820px]", txt: "md:col-start-1 md:col-end-8", feather: "strong", op: "" },
};

const FEATHER: Record<"none" | "subtle" | "strong", React.CSSProperties | undefined> = {
  none: undefined,
  subtle: {
    WebkitMaskImage: "radial-gradient(128% 138% at 56% 46%, #000 74%, rgba(0,0,0,0) 100%)",
    maskImage: "radial-gradient(128% 138% at 56% 46%, #000 74%, rgba(0,0,0,0) 100%)",
  },
  strong: {
    WebkitMaskImage: "radial-gradient(112% 122% at 54% 48%, #000 50%, rgba(0,0,0,0) 95%)",
    maskImage: "radial-gradient(112% 122% at 54% 48%, #000 50%, rgba(0,0,0,0) 95%)",
  },
};

const NAV = [
  ["Recipes", "/recipes"], ["Living", "/living"], ["Style", "/style"],
  ["Practice", "/practice"], ["Shop", "/shop"], ["Aurelian", "/aurelian"],
  ["About", "/about"],
] as const;

const CURRENTLY = [
  ["In the Kitchen", "Early summer suppers.", "/recipes"],
  ["At Home", "Open windows. Edited rooms.", "/living"],
  ["On the Table", "Simple settings that last.", "/style"],
  ["In Practice", "Thoughts for the season.", "/practice"],
] as const;

function HandRule({ className = "" }: { className?: string }) {
  return (
    <svg viewBox="0 0 1200 8" preserveAspectRatio="none" className={`block h-[7px] w-full ${className}`} aria-hidden>
      <path d="M0 4 Q 150 2.2 300 4 T 600 4 T 900 4 T 1200 4" fill="none" stroke="#1f1d1b" strokeOpacity="0.32" strokeWidth="1" strokeLinecap="round" />
    </svg>
  );
}

export default function SprintCover({ variant }: { variant: Variant }) {
  const v = V[variant];
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <style>{`.sticky.top-0.z-40{display:none!important}`}</style>
      {/* variant marker */}
      <div className="fixed bottom-4 left-4 z-50 rounded-full border border-[#1f1d1b]/15 bg-[#f8f6f3]/90 px-3 py-1 text-[10px] uppercase tracking-[0.2em] text-[#1f1d1b]/55 backdrop-blur">
        {v.label}
      </div>

      <div className="mx-auto max-w-[1180px] border-x border-[#1f1d1b]/[0.07] px-6 sm:px-10 md:px-14">
        {/* MASTHEAD */}
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

        {/* THE COVER */}
        <section className="relative grid grid-cols-1 items-center gap-y-8 py-12 md:grid-cols-12 md:gap-y-0 md:py-16">
          <Link href="/half-revealed" aria-label="Read the essay — Half revealed." className={`group order-2 md:order-none md:row-start-1 ${v.img}`}>
            <Image
              src={v.src}
              alt=""
              width={1024}
              height={1536}
              priority
              style={FEATHER[v.feather]}
              className={`mx-auto h-auto w-[74%] max-w-[340px] transition-opacity duration-500 ease-out group-hover:opacity-90 md:ml-auto md:mr-0 md:w-full ${v.imax} ${v.op}`}
            />
          </Link>
          <div className={`relative z-10 order-1 md:order-none md:row-start-1 ${v.txt}`}>
            <p className="text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/45">June 2026</p>
            <h1 className="mt-6 font-serif text-[clamp(3rem,7vw,5.5rem)] font-medium leading-[0.95] tracking-[-0.015em] text-[#2b1f17]">Half revealed.</h1>
            <p className="text-pretty mt-7 max-w-[23rem] font-serif text-[clamp(1.125rem,1.5vw,1.35rem)] italic leading-[1.5] text-[#1f1d1b]/70">
              In January we are designing a house. In June we are discovering which rooms we actually live in.
            </p>
            <Link href="/half-revealed" className="group/cta mt-9 inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/70 transition-colors duration-300 hover:text-[#1f1d1b]">
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

        {/* CLOSING */}
        <footer className="flex items-center justify-between gap-6 py-9">
          <p className="font-serif text-[clamp(0.95rem,1.4vw,1.15rem)] italic leading-[1.4] text-[#1f1d1b]/55">The year isn&rsquo;t half over. It&rsquo;s half revealed.</p>
          <span className="font-serif text-[18px] italic text-[#1f1d1b]/45">JH</span>
        </footer>
      </div>
    </main>
  );
}
