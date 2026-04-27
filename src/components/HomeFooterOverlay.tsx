"use client";

import Link from "next/link";
import Symbol from "./Symbol";
import NewsletterSignup from "./NewsletterSignup";
import {
  useScrollRevealStack,
  revealStyle,
} from "../lib/useScrollRevealStack";

type LegalLink = { label: string; href: string; external?: boolean };

const LEGAL_LINKS: readonly LegalLink[] = [
  { label: "Privacy", href: "/privacy" },
  { label: "Terms", href: "/terms" },
  { label: "Affiliate Disclosure", href: "/affiliate-disclosure" },
  { label: "Contact", href: "mailto:hello@hessentials.co", external: true },
];

const ROW_COUNT = 6; // newsletter, symbol, wordmark, tagline, year, legal

/**
 * Homepage-specific footer overlay.
 *
 * Lifted onto the last photograph (Image 04 — Cleanup) so the page closes
 * inside the world it built, not on a separate cream slab below it.
 *
 * Reveal is scroll-LINKED via the wrapper's progress through the
 * viewport. Strict sequential gating guarantees no row appears before
 * the row above is essentially complete.
 *
 * Layout: tight vertical rhythm and minimal bottom padding so the
 * legal links sit near the very bottom edge of the photograph.
 */
export default function HomeFooterOverlay() {
  const { wrapperRef, setRow, progress } = useScrollRevealStack(ROW_COUNT, {
    followLagSeconds: 0.6,
  });
  const year = new Date().getFullYear();

  return (
    <div
      ref={wrapperRef as React.RefObject<HTMLDivElement>}
      className="pointer-events-auto absolute inset-x-0 bottom-0 px-6 pb-6 sm:px-10 sm:pb-7 md:px-16 md:pb-8"
    >
      <div className="mx-auto flex max-w-3xl flex-col items-center gap-y-4 text-center">
        {/* 0 — Newsletter */}
        <div
          ref={setRow(0)}
          style={revealStyle(progress[0] ?? 0)}
          className="w-full"
        >
          <NewsletterSignup variant="light" />
        </div>

        {/* 1 — Symbol */}
        <div
          ref={setRow(1)}
          style={revealStyle(progress[1] ?? 0)}
          className="mt-2"
        >
          <Link
            href="/home"
            aria-label="Hessentials — home"
            className="inline-block transition-opacity duration-500 ease-out hover:opacity-70"
          >
            <Symbol size="xl" variant="inverse" alt="Hessentials" />
          </Link>
        </div>

        {/* 2 — Wordmark text */}
        <p
          ref={setRow(2)}
          style={revealStyle(progress[2] ?? 0)}
          className="text-[11px] uppercase tracking-[0.28em] text-[#f8f6f3]/70 sm:text-[12px]"
        >
          Hessentials
        </p>

        {/* 3 — Tagline */}
        <p
          ref={setRow(3)}
          style={revealStyle(progress[3] ?? 0)}
          className="font-serif text-[16px] italic leading-[1.4] text-[#f8f6f3]/75 sm:text-[17px]"
        >
          This is what stayed.
        </p>

        {/* 4 — Year */}
        <p
          ref={setRow(4)}
          style={revealStyle(progress[4] ?? 0)}
          className="text-[10px] uppercase tracking-[0.24em] text-[#f8f6f3]/50 sm:text-[11px]"
        >
          © {year}
        </p>

        {/* 5 — Legal */}
        <nav
          ref={setRow(5)}
          style={revealStyle(progress[5] ?? 0)}
          aria-label="Legal"
          className="mt-1 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-[10px] uppercase tracking-[0.24em] text-[#f8f6f3]/50 sm:text-[11px]"
        >
          {LEGAL_LINKS.map((link, i) => (
            <span key={link.href} className="flex items-center gap-x-5">
              {link.external ? (
                <a
                  href={link.href}
                  className="transition-colors duration-300 hover:text-[#f8f6f3]/85"
                >
                  {link.label}
                </a>
              ) : (
                <Link
                  href={link.href}
                  className="transition-colors duration-300 hover:text-[#f8f6f3]/85"
                >
                  {link.label}
                </Link>
              )}
              {i < LEGAL_LINKS.length - 1 && (
                <span aria-hidden="true" className="text-[#f8f6f3]/25">
                  ·
                </span>
              )}
            </span>
          ))}
        </nav>
      </div>
    </div>
  );
}
