import Image from "next/image";
import Link from "next/link";
import Wordmark from "../components/Wordmark";

/**
 * Entry / splash page.
 *
 * Stripped to its three load-bearing elements:
 *   1. Wordmark — the symbol → wordmark transformation on load.
 *   2. Tagline — the single line the brand wants the visitor to leave with.
 *   3. Enter — the named, single entry point into the site.
 *
 * The daily-intent block was removed deliberately. The splash exists to
 * set the tone, not to deliver content; content lives at /home onward.
 */
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
        <div className="relative mb-12 inline-flex items-center justify-center sm:mb-14">
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

        {/* Tagline — single editorial line; arrives after the wordmark settles. */}
        <p
          style={{ animationDelay: "4.0s" }}
          className="fade-up mx-auto mb-12 max-w-xl font-serif text-[clamp(1.0625rem,1.6vw,1.25rem)] italic leading-[1.55] text-[#1f1d1b]/70 sm:mb-14"
        >
          Choosing well, and standing by it.
        </p>

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
