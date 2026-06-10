import type { Metadata } from "next";
import Mock from "../Mock";

export const metadata: Metadata = {
  title: "About mock — A, the shelf",
  robots: { index: false, follow: false },
};

/**
 * A — THE SHELF. Three objects, one gap where a fourth was. The
 * environment reveals a choice, not a preference. Most "selection."
 */
export default function AboutMockShelf() {
  return <Mock src="/about/the-man-scene-a.png" width={1040} height={1560} />;
}
