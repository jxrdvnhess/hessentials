import type { Metadata } from "next";
import Mock from "../Mock";

export const metadata: Metadata = {
  title: "About mock — D, the painter",
  robots: { index: false, follow: false },
};

/**
 * D — THE PAINTER. Jordan's direction, 2026-06-11: the man mid-paint,
 * roller at the wet edge. The painted side of the wall is the essay's
 * living area — the cream wash the page already uses to lift the text
 * becomes diegetic. He is the reason the words have somewhere to sit.
 */
export default function AboutMockPainter() {
  return <Mock src="/about/the-man-scene-d.png" width={1040} height={1560} />;
}
