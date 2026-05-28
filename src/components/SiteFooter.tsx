"use client";

import Link from "next/link";
import HomeLink from "./HomeLink";
import Symbol from "./Symbol";
import NewsletterSignup from "./NewsletterSignup";

type LegalLink = { label: string; href: string; external?: boolean };

const LEGAL_LINKS: readonly LegalLink[] = [
  { label: "Privacy", href: "/privacy" },
  { label: "Terms", href: "/terms" },
  { label: "Affiliate Disclosure", href: "/affiliate-disclosure" },
  { label: "Contact", href: "mailto:hello@hessentials.co", external: true },
];

/**
 * Site footer — clean cream treatment.
 *
 * Rewritten 2026-05-27 per the Homepage Version Next brief. The prior
 * footer landed inside a full-bleed AI-photorealistic image
 * (/splash/morning-merida.jpg) with a scroll-linked reveal animation;
 * that image violated the brand doctrine (Hessentials does not
 * counterfeit human experience) and was removed site-wide. The
 * "This is what stayed." line came off with it — without the villa
 * the "this" had no antecedent.
 *
 * What remains: brand monogram, HESSENTIALS wordmark text, newsletter
 * signup, legal links, © year. All on the site's cream ground. One
 * unified layout for every breakpoint — the old desktop image-overlay
 * vs mobile cream-block split no longer applies once the image is
 * gone.
 *
 * The scroll-linked reveal animation was also removed. Per the
 * scroll-listener-analytics memory (prior incident where scroll-driven
 * JS broke event tracking), removing this is a small structural win
 * in addition to closing the doctrine violation.
 */
export default function SiteFooter() {
  const year = new Date().getFullYear();

  return (
    <footer
      aria-label="Site"
      className="relative w-full border-t border-[#1f1d1b]/10"
    >
      <div className="mx-auto flex max-w-[420px] flex-col items-center gap-y-10 px-6 pt-20 pb-12 text-center sm:px-8 sm:pt-24 sm:pb-14 md:max-w-[480px] md:pt-28">
        {/* Brand monogram — clickable home affordance. */}
        <HomeLink className="inline-block transition-opacity duration-500 ease-out hover:opacity-70">
          <Symbol size="xl" alt="Hessentials" />
        </HomeLink>

        {/* HESSENTIALS wordmark — small tracked uppercase text label
            paired with the monogram. */}
        <p className="-mt-4 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px]">
          Hessentials
        </p>

        {/* Newsletter signup — inherits the default pillar tagline
            from the NewsletterSignup component's pathname inference,
            so non-pillar routes (homepage, legal, etc.) get the
            site-wide line; pillar routes get pillar-specific copy. */}
        <NewsletterSignup variant="default" source="footer" />

        {/* Legal nav — first row links, second row Contact + © year. */}
        <nav
          aria-label="Legal"
          className="mt-3 flex flex-col items-center gap-y-3 text-[10.5px] uppercase tracking-[0.24em] text-[#1f1d1b]/45 sm:text-[11px]"
        >
          <div className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2">
            {LEGAL_LINKS.slice(0, 3).map((link) => (
              <Link
                key={link.href}
                href={link.href}
                className="transition-colors duration-300 hover:text-[#1f1d1b]/75"
              >
                {link.label}
              </Link>
            ))}
          </div>
          <div className="flex items-center gap-x-5">
            <a
              href={LEGAL_LINKS[3].href}
              className="transition-colors duration-300 hover:text-[#1f1d1b]/75"
            >
              {LEGAL_LINKS[3].label}
            </a>
            <span className="text-[#1f1d1b]/30">·</span>
            <span className="text-[#1f1d1b]/40">© {year}</span>
          </div>
        </nav>
      </div>
    </footer>
  );
}
