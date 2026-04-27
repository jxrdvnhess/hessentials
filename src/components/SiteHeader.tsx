"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Wordmark from "./Wordmark";
import SiteSearch from "./SiteSearch";
import MobileMenu from "./MobileMenu";

const NAV_LINKS: ReadonlyArray<{ label: string; href: string }> = [
  { label: "Recipes", href: "/recipes" },
  { label: "Living", href: "/living" },
  { label: "Style", href: "/style" },
  { label: "Shop", href: "/shop" },
  { label: "Aurelian", href: "/aurelian" },
  { label: "About", href: "/about" },
];

/**
 * Global site header.
 *
 * Sticky across every interior page, hidden on the Enter Page (`/`) so the
 * gateway stays clean. The wordmark anchors the bar; nav and search sit to
 * its right. The wordmark-press arrival animation is preserved on `/home`
 * so the hub still has its quieter sense of arrival.
 *
 * Background is a vertical gradient + blur, masked to fade out at the
 * bottom edge. The intent is that the bar should feel like atmosphere, not
 * a defined element — no detectable line as content scrolls beneath it.
 */
export default function SiteHeader() {
  const pathname = usePathname();
  if (pathname === "/") return null;

  const isHome = pathname === "/home";

  return (
    <header aria-label="Site" className="sticky top-0 z-40 w-full">
      {/* Soft wash — the bar exists, but its edge does not. */}
      <div
        aria-hidden
        className="pointer-events-none absolute inset-0 -z-10 backdrop-blur-[8px]"
        style={{
          backgroundImage:
            "linear-gradient(to bottom, rgba(248,246,243,0.78) 0%, rgba(248,246,243,0.55) 55%, rgba(248,246,243,0) 100%)",
          maskImage:
            "linear-gradient(to bottom, black 50%, transparent 100%)",
          WebkitMaskImage:
            "linear-gradient(to bottom, black 50%, transparent 100%)",
        }}
      />

      <div className="mx-auto flex w-full max-w-[1400px] items-center justify-between gap-6 px-6 py-2.5 sm:px-10 sm:py-3 md:px-16">
        <Link
          href="/home"
          aria-label="Hessentials — home"
          className={[
            "inline-block shrink-0",
            isHome ? "wordmark-press" : "",
          ]
            .filter(Boolean)
            .join(" ")}
        >
          <Wordmark size="nav" priority={isHome} />
        </Link>

        <div className="flex items-center gap-5 sm:gap-8 md:gap-10">
          <nav
            aria-label="Primary"
            className="hidden items-center gap-6 md:flex md:gap-8 lg:gap-10"
          >
            {NAV_LINKS.map((link) => {
              const active =
                pathname === link.href ||
                pathname.startsWith(`${link.href}/`);
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={[
                    "text-[11px] uppercase leading-none tracking-[0.22em] transition-colors duration-500 ease-out",
                    active
                      ? "text-[#1f1d1b]"
                      : "text-[#1f1d1b]/55 hover:text-[#1f1d1b]/85",
                  ].join(" ")}
                >
                  {link.label}
                </Link>
              );
            })}
          </nav>

          <MobileMenu links={NAV_LINKS} />
          <SiteSearch />
        </div>
      </div>
    </header>
  );
}
