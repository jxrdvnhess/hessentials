import Link from "next/link";
import type { Metadata } from "next";
import Mock from "./Mock";

export const metadata: Metadata = {
  title: "About — still figure mock",
  robots: { index: false, follow: false },
};

/**
 * PREVIEW MOCK — not linked in nav, noindex. Live /about untouched.
 *
 * Baseline: the figure alone on the site's plaster ground. The three
 * environment studies (Jordan's art direction, 2026-06-10 — evidence,
 * not possessions) sit at /a, /b, /c:
 *
 *   A — the shelf: three objects, one gap.
 *   B — the window: light falling, nothing else.
 *   C — the comparison: two near-identical vessels, one forward.
 *
 * If adopted, the chosen version replaces the about-room backdrop.
 */
export default function AboutFigureMock() {
  return (
    <>
      <nav
        aria-label="Variants"
        className="fixed left-1/2 top-4 z-50 -translate-x-1/2 rounded-full bg-[#f8f6f3]/85 px-5 py-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 backdrop-blur-sm"
      >
        <span className="mr-4">Figure</span>
        <Link href="/illustration-flow/about-figure/a" className="mr-4 hover:text-[#1f1d1b]">
          A · Shelf
        </Link>
        <Link href="/illustration-flow/about-figure/b" className="mr-4 hover:text-[#1f1d1b]">
          B · Window
        </Link>
        <Link href="/illustration-flow/about-figure/c" className="mr-4 hover:text-[#1f1d1b]">
          C · Comparison
        </Link>
        <Link href="/illustration-flow/about-figure/frame" className="hover:text-[#1f1d1b]">
          Frame
        </Link>
      </nav>
      <Mock src="/about/the-man-about.png" width={560} height={1560} />
    </>
  );
}
