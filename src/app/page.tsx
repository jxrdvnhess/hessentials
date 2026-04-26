import Image from "next/image";
import Link from "next/link";
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
          overlays via absolute positioning. Animations are synced: symbol
          drops, holds, expands large (scale 4), holds at peak, then
          shrinks back small as it fades. The wordmark emerges from the
          same center during the symbol's contraction.
        */}
        <div className="relative mb-10 inline-flex items-center justify-center">
          <div className="wordmark-emerge">
            <Wordmark size="large" priority />
          </div>
          <div
            aria-hidden
            className="symbol-drop-morph pointer-events-none absolute inset-0 flex items-center justify-center"
          >
            <Image
              src="/hessentials-symbol.png"
              alt=""
              width={2048}
              height={2048}
              priority
              sizes="640px"
              className="block h-auto w-[clamp(88px,10vw,128px)]"
            />
          </div>
        </div>

        <p
          style={{ animationDelay: "3.1s" }}
          className="fade-up mx-auto mb-10 max-w-xl font-serif text-[clamp(1.125rem,1.7vw,1.375rem)] italic leading-[1.45] text-[#1f1d1b]/65 sm:mb-12"
        >
          The things that make everyday life feel a little better.
        </p>

        <Link
          href="/home"
          prefetch
          style={{ animationDelay: "3.5s" }}
          className="fade-up inline-block border border-[#1f1d1b]/55 px-9 py-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/80 transition-colors duration-500 ease-out hover:border-[#1f1d1b]/75 hover:text-[#1f1d1b] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/50 focus-visible:ring-offset-4 focus-visible:ring-offset-[#fbfaf4]"
        >
          Enter
        </Link>
      </section>
    </main>
  );
}
