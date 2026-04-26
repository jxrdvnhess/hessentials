import Link from "next/link";
import type { Metadata } from "next";
import { STYLE_ARTICLES } from "../../data/style";

export const metadata: Metadata = {
  title: "Style — Hessentials",
  description:
    "Jordan Hess on what to wear, what to keep, what to ignore. A taste system translated into real life.",
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
          A taste system translated into real life. What to wear, what to keep,
          what to ignore.
        </p>
      </section>

      {/* ---------- Grid ---------- */}
      <section className="mx-auto w-full max-w-6xl px-6 pb-32 sm:px-10 md:pb-40">
        <ul className="grid grid-cols-1 gap-x-12 gap-y-16 sm:grid-cols-2 sm:gap-x-14 md:gap-x-20 md:gap-y-20">
          {STYLE_ARTICLES.map((article) => (
            <li key={article.slug}>
              <Link
                href={`/style/${article.slug}`}
                className="group block transition-opacity duration-500 ease-out"
              >
                <h2 className="font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30">
                  {article.title}
                </h2>

                <p className="text-pretty mt-4 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[17px]">
                  {article.subtitle}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </main>
  );
}
