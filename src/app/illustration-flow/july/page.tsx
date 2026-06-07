import type { Metadata } from "next";
import IssueCover, { type Issue } from "../_lib/IssueCover";

export const metadata: Metadata = { title: "July issue — durability test", robots: { index: false, follow: false } };

const JULY: Issue = {
  monthYear: "July 2026",
  title: "What grew.",
  dek: "In spring it was a plan on paper. By July, the conditions have answered.",
  coverSrc: "/cover-july.jpg",
  essayHref: "/what-grew",
  currently: [
    ["In the Kitchen", "Cooking in the heat.", "/recipes"],
    ["At Home", "Open windows, less on.", "/living"],
    ["On the Table", "Plain, and enough.", "/style"],
    ["In Practice", "Reading the conditions.", "/practice"],
  ],
  whisper: "A thing planted in the wrong conditions has not failed. It has told you the conditions were wrong.",
};

export default function Page() {
  return <IssueCover issue={JULY} />;
}
