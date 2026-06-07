import type { Metadata } from "next";
import IssueCover, { type Issue } from "../_lib/IssueCover";

export const metadata: Metadata = { title: "June — through the lens (retrospective)", robots: { index: false, follow: false } };

const JUNE_RETRO: Issue = {
  monthYear: "June 2026",
  title: "Half revealed.",
  dek: "In January we are designing a house. In June we are discovering which rooms we actually live in.",
  coverSrc: "/cover-june-retro.jpg",
  essayHref: "/half-revealed",
  currently: [
    ["In the Kitchen", "Early summer suppers.", "/recipes"],
    ["At Home", "Open windows. Edited rooms.", "/living"],
    ["On the Table", "Simple settings that last.", "/style"],
    ["In Practice", "Thoughts for the season.", "/practice"],
  ],
  whisper: "The year isn’t half over. It’s half revealed.",
};

export default function Page() {
  return <IssueCover issue={JUNE_RETRO} />;
}
