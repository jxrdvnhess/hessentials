import type { Metadata } from "next";
import SprintCover from "../_lib/SprintCover";

export const metadata: Metadata = { title: "Cover sprint — B", robots: { index: false, follow: false } };

export default function Page() {
  return <SprintCover variant="B" />;
}
