import type { Metadata } from "next";
import HomepageWallpaper from "../../components/HomepageWallpaper";

/**
 * /wallpaper-test — storm zone integration test.
 *
 * Validates the locked storm trio (storm-a, storm-b, storm-c) in context
 * before we commit calm and clearing generation to specific aspect ratios
 * and zone allocations. Separate route from the real homepage so this
 * doesn't touch production while we evaluate.
 *
 * What this surfaces:
 *   - Storm tiles at actual viewport scale on desktop AND mobile (the
 *     hardest case — the storm tile at 19.68% density survived the
 *     390px-wide mobile test earlier; this confirms in context)
 *   - Seamless tile repeat in the sub-zones (no visible horizontal
 *     boundary as the page scrolls)
 *   - Variant transitions between sub-zones (A → B → C → A...) reading
 *     as weather, not pattern
 *   - Text legibility over wallpaper at multiple densities and viewport
 *     sizes
 *   - Performance: 3 WebP tiles totaling ~1.6MB, comparable to the
 *     retiring cinematic photo budget
 *
 * Removed from the route map once the homepage adopts the wallpaper —
 * this is a scaffolding route, not a permanent surface.
 */

export const metadata: Metadata = {
  title: "Wallpaper test — Hessentials",
  description: "Internal test route for storm-zone wallpaper integration.",
  robots: { index: false, follow: false },
};

export default function WallpaperTestPage() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <HomepageWallpaper />

      {/* Placeholder content that approximates the real homepage section
          heights. Lets us validate text legibility over wallpaper at
          actual scale without coupling this test to the production page. */}

      <section className="relative z-10 flex min-h-[88vh] items-center px-6 sm:px-10 md:px-16">
        <div className="max-w-[520px]">
          <p className="mb-5 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px] md:mb-10">
            Hessentials
          </p>
          <h1 className="font-serif text-[clamp(2.5rem,7vw,4.5rem)] font-normal leading-[1.02] tracking-[-0.02em]">
            Life, edited well.
          </h1>
          <p className="mt-5 font-serif text-[clamp(1.125rem,1.9vw,1.5rem)] italic leading-[1.45] text-[#1f1d1b]/70 md:mt-8">
            Placeholder hero subhead — content mimicking the real homepage
            for in-context legibility evaluation.
          </p>
        </div>
      </section>

      <section className="relative z-10 px-6 py-14 sm:px-10 sm:py-16 md:px-16 md:py-20">
        <div className="mx-auto max-w-[480px] text-center">
          <p className="mb-4 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55">
            Currently
          </p>
          <p className="font-serif text-[18px] italic leading-[1.5] text-[#1f1d1b]/75">
            A placeholder Currently block, sized like the real one. Storm
            tile should sit behind without competing for attention.
          </p>
        </div>
      </section>

      <section className="relative z-10 border-t border-[#1f1d1b]/10 px-6 py-14 sm:px-10 sm:py-16 md:px-16 md:py-20">
        <div className="mx-auto max-w-md text-center">
          <p className="mb-4 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55">
            Newsletter
          </p>
          <p className="font-serif text-[15px] italic leading-[1.45] text-[#1f1d1b]/65">
            Placeholder newsletter tagline copy. Sent when it&rsquo;s worth a
            note.
          </p>
        </div>
      </section>

      {/* A few tall blocks so the page actually scrolls through multiple
          tile sub-zones. Each block roughly mirrors the cinematic-frame
          heights the wallpaper is replacing. */}
      {[1, 2, 3, 4].map((i) => (
        <section
          key={i}
          className="relative z-10 flex min-h-[80vh] items-center justify-center px-6 sm:px-10 md:px-16"
        >
          <div className="max-w-[440px] text-center">
            <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/45">
              Section {i}
            </p>
            <p className="mt-4 font-serif text-[clamp(1rem,1.6vw,1.25rem)] italic leading-[1.5] text-[#1f1d1b]/65">
              Placeholder block at hero-image height, so the storm zone
              gets validated across multiple variant sub-zones during a
              normal scroll.
            </p>
          </div>
        </section>
      ))}

      <section className="relative z-10 px-6 py-20 text-center">
        <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/45">
          End of wallpaper test
        </p>
        <p className="mt-3 font-serif text-[14px] italic text-[#1f1d1b]/55">
          You stayed.
        </p>
      </section>
    </main>
  );
}
