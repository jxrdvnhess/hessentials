import type { Metadata } from "next";
import StyleIndex from "../../components/StyleIndex";

export const metadata: Metadata = {
  title: "Style — Hessentials",
  description:
    "J.D.H. on what to wear, what to keep, what to ignore.",
};

export default function StyleIndexPage() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ---------- */}
      <section className="mx-auto w-full max-w-3xl px-6 pt-16 pb-12 text-center sm:px-10 md:pt-24">
        <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
          Style
        </p>
        <p className="text-pretty mx-auto max-w-2xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] italic leading-[1.4] text-[#1f1d1b]/80">
          What to wear. What to keep. What to ignore.
        </p>
        <p className="mx-auto mt-6 max-w-md text-[13px] leading-[1.6] text-[#1f1d1b]/55 sm:text-[14px]">
          A few of these will do most of the work.
        </p>
      </section>

      {/* ---------- Index (Start Here + grouped sections) ---------- */}
      <section className="mx-auto w-full max-w-6xl px-6 pb-32 sm:px-10 md:pb-40">
        <StyleIndex />
      </section>
    </main>
  );
}
