import type { Metadata } from "next";
import Mock from "../Mock";

export const metadata: Metadata = {
  title: "About mock — B, the window",
  robots: { index: false, follow: false },
};

/**
 * B — THE WINDOW. A window, the thrown patch of late sun reaching
 * toward him across the floor. Nothing else. Most contemplative,
 * least symbolic.
 */
export default function AboutMockWindow() {
  return <Mock src="/about/the-man-scene-b.png" width={1040} height={1560} />;
}
