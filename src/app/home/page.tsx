import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";
import FadeOnScroll from "../../components/FadeOnScroll";
import RightNow from "../../components/RightNow";

export const metadata: Metadata = {
  title: "Hessentials",
  description:
    "A system for choosing what holds. Food, home, style, and the small decisions that shape how life actually feels.",
};

const THE_EDIT = [
  { title: "The 5 things I cook every week", href: "/recipes" },
  {
    title: "The kitchen setup that changed everything",
    href: "/living/the-kitchen-setup-that-makes-you-cook-more",
  },
  {
    title: "Getting dressed without overthinking it",
    href: "/style/the-uniform-is-not-boring",
  },
  { title: "What I keep buying again", href: "/shop" },
  { title: "Hosting without making it a production", href: "/living" },
] as const;

export default function HomePage() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Hero — full hero in a single viewport. 2-col grid, top-aligned. ---------- */}
      <section className="px-6 pt-20 pb-28 sm:px-10 md:px-16 md:pt-28 md:pb-32">
        <div className="grid items-start gap-x-12 gap-y-16 md:grid-cols-12 md:gap-x-16">
          <div className="fade-up delay-3 md:col-span-7">
            <p className="mb-10 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px]">
              A more intentional way to live
            </p>

            <h1 className="font-serif text-[clamp(2.75rem,8vw,5.25rem)] font-normal leading-[1.02] tracking-[-0.02em] text-balance">
              Life, edited well.
            </h1>

            <p className="text-pretty mt-8 max-w-xl font-serif text-[clamp(1.25rem,1.9vw,1.5rem)] italic leading-[1.45] text-[#1f1d1b]/70">
              A system for choosing what holds.
            </p>
          </div>

          <div className="fade-up delay-4 md:col-span-5">
            <div className="max-w-[26rem] space-y-1 text-pretty font-serif text-[clamp(1.125rem,1.6vw,1.375rem)] italic leading-[1.5] text-[#1f1d1b]/70">
              <p>Too many options.</p>
              <p>Too much noise.</p>
              <p className="pt-4 not-italic font-sans text-[12px] uppercase tracking-[0.26em] text-[#1f1d1b]/55">
                This is what holds.
              </p>
            </div>

            <div className="mt-10 max-w-[26rem]">
              <RightNow />
            </div>
          </div>
        </div>
      </section>

      {/* ---------- A pause — full-bleed lifestyle image. Punctuation, not a section. ---------- */}
      <FadeOnScroll
        as="section"
        durationMs={550}
        threshold={0.1}
        className="relative w-full"
        style={{ contain: "layout paint" }}
      >
        <div className="relative aspect-[4/5] w-full min-h-[60vh] sm:aspect-auto sm:h-[88vh] sm:max-h-[1000px] sm:min-h-0">
          <Image
            src="/home/hessentials-couple-lifestyle.png"
            alt=""
            fill
            sizes="100vw"
            quality={90}
            className="object-cover object-[62%_50%] sm:object-center"
            style={{ filter: "contrast(0.97) saturate(0.96) brightness(1.015)" }}
          />
        </div>
      </FadeOnScroll>

      {/* ---------- The Edit — proves what we actually do here ---------- */}
      <section
        aria-labelledby="the-edit-heading"
        className="px-6 pt-32 pb-24 sm:px-10 md:px-16 md:pb-32 md:pt-40"
      >
        <div className="mb-12 flex items-baseline justify-between gap-6 md:mb-16">
          <p
            id="the-edit-heading"
            className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/50 sm:text-[12px]"
          >
            The Edit
          </p>
          <p className="font-serif text-[14px] italic leading-none text-[#1f1d1b]/45 sm:text-[15px]">
            What this place is actually for.
          </p>
        </div>

        <ul className="grid grid-cols-1 gap-x-12 gap-y-8 sm:grid-cols-2 md:grid-cols-3 md:gap-x-16 md:gap-y-12">
          {THE_EDIT.map(({ title, href }) => (
            <li key={title}>
              <Link
                href={href}
                className="group block border-t border-[#1f1d1b]/10 pt-5 transition-colors duration-500 ease-out hover:border-[#1f1d1b]/35"
              >
                <span className="flex items-baseline gap-3 font-serif text-[clamp(1.125rem,1.7vw,1.375rem)] font-normal leading-[1.25] tracking-[-0.01em] text-balance text-[#1f1d1b]/85 transition-colors duration-500 ease-out group-hover:text-[#1f1d1b]">
                  <span className="flex-1">{title}</span>
                  <span
                    aria-hidden
                    className="text-[12px] not-italic text-[#1f1d1b]/35 transition-colors duration-500 ease-out group-hover:text-[#1f1d1b]/75"
                  >
                    →
                  </span>
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      {/* ---------- Reality — closing line ---------- */}
      <section className="px-6 pb-20 pt-2 text-center sm:px-10 md:px-16 md:pb-28">
        <p className="font-serif text-[clamp(1.125rem,1.7vw,1.375rem)] italic leading-[1.4] text-[#1f1d1b]/55">
          Not everything works. This does.
        </p>
      </section>
    </main>
  );
}
