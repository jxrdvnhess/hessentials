import Image from "next/image";
import Link from "next/link";
import DailyIntent from "../components/DailyIntent";
import Wordmark from "../components/Wordmark";

export default function EnterPage() {
  return (
    <main className="min-h-screen overflow-x-hidden bg-[#fbfaf4] text-[#1f1d1b]">
      {/* Cache the home hub's plaster environment before the user clicks Enter. */}
      <link
        rel="preload"
        as="image"
        href="/soft-plaster-texture-with-plant-shadows.png"
      />

      <section
        aria-label="Hessentials"
        className="relative flex min-h-[100svh] flex-col items-center justify-center overflow-hidden px-6 text-center"
      >
        {/*
          Symbol → Wordmark transformation.
          Both elements share a single visual center. The wordmark is the
          layout-defining child (its width sets the wrapper). The symbol
          overlays via absolute positioning. The symbol fades in, sweeps a
          single 360° at constant linear velocity (silent-clock movement),
          then quietly elongates into a flat horizontal bar. The wordmark
          emerges from that same bar shape — the handoff is shape-shared,
          not a fade. See globals.css for the chained phase animations.
        */}
        <div className="relative mb-10 inline-flex items-center justify-center">
          <div className="wordmark-emerge">
            <Wordmark size="large" priority />
          </div>
          <div
            aria-hidden
            className="symbol-sweep pointer-events-none absolute inset-0 flex items-center justify-center"
          >
            <Image
              src="/hessentials-symbol.png"
              alt=""
              width={2048}
              height={2048}
              priority
              fetchPriority="high"
              decoding="sync"
              sizes="640px"
              className="block h-auto w-[clamp(88px,10vw,128px)]"
            />
          </div>
        </div>

        <DailyIntent />

        <Link
          href="/home"
          prefetch
          style={{ animationDelay: "4.7s" }}
          className="fade-up inline-block border border-[#1f1d1b]/55 px-9 py-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/80 transition-colors duration-500 ease-out hover:border-[#1f1d1b]/75 hover:text-[#1f1d1b] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/50 focus-visible:ring-offset-4 focus-visible:ring-offset-[#fbfaf4]"
        >
          Enter
        </Link>
      </section>
    </main>
  );
}
