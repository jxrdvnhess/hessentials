import type { Metadata } from "next";
import StyleIndex from "../../components/StyleIndex";
import SectionDivider from "../../components/SectionDivider";

export const metadata: Metadata = {
  title: "Style — Hessentials",
  description:
    "J.D.H. on what to wear, what to keep, what to ignore.",
};

export default function StyleIndexPage() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ---------- */}
      <section className="mx-auto flex w-full max-w-3xl flex-col items-center px-6 pt-16 pb-12 text-center sm:px-10 md:pt-24">
        {/* Hairline above the pillar eyebrow (§2.2). */}
        <span
          aria-hidden
          className="block w-20"
          style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
        />
        <p className="mt-6 mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
          Style
        </p>
        <p className="text-pretty mx-auto max-w-2xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] italic leading-[1.4] text-[#1f1d1b]/80">
          What to wear. What to keep. What to ignore.
        </p>
        {/* Secondary-tier subtitle (Style / Shop): font-serif
            13/14px at /55 opacity. Primary tier (Living / Practice)
            sits at 15/16px /55. */}
        <p className="mx-auto mt-6 max-w-md font-serif text-[13px] leading-[1.6] text-[#1f1d1b]/55 sm:text-[14px]">
          A few of these will do most of the work.
        </p>
      </section>

      {/* "h" motif transitioning from intro into the index (§2.1). */}
      <SectionDivider />

      {/* ---------- Index (Start Here + grouped sections) ---------- */}
      <section className="mx-auto w-full max-w-6xl px-6 pb-32 sm:px-10 md:pb-40">
        <StyleIndex />
      </section>
    </main>
  );
}
