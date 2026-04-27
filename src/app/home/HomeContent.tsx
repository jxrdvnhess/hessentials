"use client";

import Link from "next/link";
import Wordmark from "../../components/Wordmark";
import { useArrivalPhase } from "../../components/ArrivalProvider";

const NAV_LINKS = [
  { label: "Recipes", href: "/recipes" },
  { label: "Living", href: "/living" },
  { label: "Style", href: "#style" },
  { label: "Aurelian", href: "/aurelian" },
  { label: "About", href: "/about" },
] as const;

export default function HomeContent() {
  const phase = useArrivalPhase();
  const isPending = phase === "pending";
  const isFirst = phase === "first";

  /** Apply fade-up + delay only on first arrival; otherwise render in place. */
  const reveal = (delay: string) =>
    [
      isPending ? "opacity-0" : "",
      isFirst ? "fade-up" : "",
      isFirst ? delay : "",
    ]
      .filter(Boolean)
      .join(" ");

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <header className="flex items-center justify-between px-6 pt-10 sm:px-10 md:px-16 md:pt-12">
        <Link
          href="/home"
          aria-label="Hessentials — home"
          className={[
            "inline-block",
            isPending ? "opacity-0" : "",
            isFirst ? "wordmark-press" : "",
          ]
            .filter(Boolean)
            .join(" ")}
        >
          <Wordmark size="medium" priority />
        </Link>

        {/*
          Desktop nav only. On phones / small tablets the global SiteHeader
          carries the Menu drawer — duplicating a 5-link inline row here
          would overflow narrow iPhones (the wordmark + 5 nav items exceed
          a 320–390px viewport). Mobile users get the same destinations
          via the sticky header above this hero.
        */}
        <nav
          aria-label="Primary"
          className={`hidden md:block ${reveal("delay-2")}`.trim()}
        >
          <ul className="flex items-center gap-12 text-[12px] uppercase leading-none tracking-[0.22em] text-[#1f1d1b]/65">
            {NAV_LINKS.map(({ label, href }) => (
              <li key={href}>
                <Link
                  href={href}
                  className="transition-colors duration-500 ease-out hover:text-[#1f1d1b]"
                >
                  {label}
                </Link>
              </li>
            ))}
          </ul>
        </nav>
      </header>

      <section className="px-6 pt-32 pb-32 sm:px-10 md:px-16 md:pt-44 md:pb-48">
        <div className="grid items-end gap-12 md:grid-cols-12 md:gap-16">
          <div className={`${reveal("delay-3")} md:col-span-8`.trim()}>
            <p className="mb-10 text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/65 sm:mb-12 sm:text-[12px]">
              Hessentials
            </p>

            <h1 className="font-serif text-[clamp(2.5rem,7vw,4.75rem)] font-normal leading-[1.04] tracking-[-0.02em] text-balance max-w-[16ch]">
              Taste, organized into a way of living.
            </h1>
          </div>

          <div className={`${reveal("delay-4")} md:col-span-4`.trim()}>
            <p className="text-pretty text-[17px] leading-[1.65] text-[#1f1d1b]/75 md:text-[18px]">
              An editorial home for the objects, rituals, rooms, and small
              decisions that hold up.
            </p>

            <p className="mt-10 text-[11px] uppercase leading-none tracking-[0.24em] text-[#1f1d1b]/55 sm:text-[12px]">
              Currently
            </p>
            <Link
              href="/recipes/mediterranean-shrimp-white-beans"
              className="mt-4 inline-flex items-baseline gap-3 font-serif text-[20px] italic leading-[1.3] text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-60 sm:text-[22px]"
            >
              Mediterranean Shrimp &amp; White Beans
              <span aria-hidden className="text-[14px] not-italic">
                →
              </span>
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}
