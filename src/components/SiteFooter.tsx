"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import Symbol from "./Symbol";
import NewsletterSignup from "./NewsletterSignup";

const LEGAL_LINKS = [
  { label: "Privacy", href: "/privacy" },
  { label: "Terms", href: "/terms" },
  { label: "Affiliate Disclosure", href: "/affiliate-disclosure" },
  { label: "Contact", href: "mailto:hello@hessentials.co", external: true },
];

export default function SiteFooter() {
  const pathname = usePathname();
  // No footer on the Enter Page — gateway stays clean.
  if (pathname === "/") return null;

  const year = new Date().getFullYear();

  return (
    <footer
      aria-label="Site"
      className="border-t border-[#1f1d1b]/10 px-6 sm:px-10 md:px-16"
    >
      {/* ---------- Newsletter band ---------- */}
      <section
        aria-label="Newsletter"
        className="py-16 md:py-20"
      >
        <NewsletterSignup />
      </section>

      {/* ---------- Hairline divider ---------- */}
      <div className="border-t border-[#1f1d1b]/10" aria-hidden />

      {/* ---------- Brand + legal band ---------- */}
      <section className="py-14 text-center md:py-16">
        <div className="mx-auto flex max-w-3xl flex-col items-center gap-y-6">
          <Link
            href="/home"
            aria-label="Hessentials — home"
            className="inline-block transition-opacity duration-500 ease-out hover:opacity-70"
          >
            <Symbol size="xl" alt="Hessentials" />
          </Link>

          <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/50 sm:text-[12px]">
            Hessentials
          </p>

          <p className="font-serif text-[16px] italic leading-[1.4] text-[#1f1d1b]/55 sm:text-[17px]">
            Not everything works. This does.
          </p>

          <p className="mt-2 text-[10px] uppercase tracking-[0.24em] text-[#1f1d1b]/35 sm:text-[11px]">
            © {year}
          </p>

          <nav
            aria-label="Legal"
            className="mt-6 flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-[10px] uppercase tracking-[0.24em] text-[#1f1d1b]/35 sm:text-[11px]"
          >
            {LEGAL_LINKS.map((link, i) => (
              <span key={link.href} className="flex items-center gap-x-5">
                {link.external ? (
                  <a
                    href={link.href}
                    className="transition-colors duration-300 hover:text-[#1f1d1b]/70"
                  >
                    {link.label}
                  </a>
                ) : (
                  <Link
                    href={link.href}
                    className="transition-colors duration-300 hover:text-[#1f1d1b]/70"
                  >
                    {link.label}
                  </Link>
                )}
                {i < LEGAL_LINKS.length - 1 && (
                  <span aria-hidden="true" className="text-[#1f1d1b]/20">
                    ·
                  </span>
                )}
              </span>
            ))}
          </nav>
        </div>
      </section>
    </footer>
  );
}
