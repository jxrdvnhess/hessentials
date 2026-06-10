import type { Metadata } from "next";
import Mock from "../Mock";

export const metadata: Metadata = {
  title: "About mock — C, the comparison",
  robots: { index: false, follow: false },
};

/**
 * C — THE COMPARISON. A narrow console, two nearly identical vessels,
 * one brought slightly forward. No indication which is correct; the
 * viewer starts discerning. The most direct translation of the essay.
 */
export default function AboutMockComparison() {
  return <Mock src="/about/the-man-scene-c.png" width={1040} height={1560} />;
}
