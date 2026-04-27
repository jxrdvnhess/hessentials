"use client";

import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useRef, useState } from "react";
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
 * Site footer.
 *
 * On every page after the homepage, the page closes inside the
 * "hacienda" photograph instead of on a separate cream slab. The image
 * is the primary surface; the footer (newsletter + brand mark + tagline
 * + legal) is layered into the safe zones over a quiet darken.
 *
 * Suppressed on:
 *   /        — Enter Page (gateway stays clean)
 *   /home    — homepage closes inside its own photograph (HomeFooterOverlay
 *              on hacienda-04-cleanup.jpg). Same cinematic logic; the
 *              homepage just owns its own closing image.
 */
export default function SiteFooter() {
  const pathname = usePathname();
  if (pathname === "/") return null;
  if (pathname === "/home") return null;
  return <CinematicFooter />;
}

/**
 * Cinematic image footer.
 *
 * IMAGE
 *   /hacienda-footer-master.jpg — wide hacienda interior. Doorway is the
 *   anchor; everything else is secondary.
 *
 *     Desktop  object-position 35% center  → biases doorway to left-
 *              third, leaves the right plaster wall + sideboard for the
 *              footer overlay. Section ~60–75vh.
 *
 *     Mobile   object-position center      → doorway centred. Section
 *              ~70–85vh; the table drops to the lower third.
 *
 * REVEAL
 *   The whole footer (photograph + darken + editorial copy) is one
 *   moment. Opacity is scroll-LINKED to the section's progress through
 *   the viewport: it begins resolving as the user scrolls toward it,
 *   eased so most of the change happens late — quiet, then suddenly
 *   the room is there. Reduced-motion users skip the curve.
 *
 * SAFE ZONES
 *   Type never sits over: the doorway opening, the bright exterior, or
 *   the wine glass. On desktop the overlay anchors to the lower-right
 *   quadrant (plaster wall / sideboard / table shadow). On mobile the
 *   overlay sits along the bottom edge inside the darken.
 */
function CinematicFooter() {
  const sectionRef = useRef<HTMLElement | null>(null);
  // Lazy initializer keeps SSR markup correct; reduced-motion users
  // mount already-revealed. The effect still resets to 1 on the client
  // for the reduced-motion case because SSR can't read matchMedia.
  const reducedMotion =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const [revealOpacity, setRevealOpacity] = useState<number>(
    reducedMotion ? 1 : 0
  );
  const year = new Date().getFullYear();

  // Scroll-LINKED reveal. Section progress 0 = top of section at the
  // bottom of the viewport (just entering); 1 = bottom of section at
  // the top of the viewport (just leaving). Mapping:
  //
  //     progress 0.00 → 0.05    opacity 0   (held — they crest the page)
  //     progress 0.05 → 0.40    opacity 0 → 1 (eased)
  //     progress 0.40+          opacity 1   (settled)
  //
  // The whole footer (image, gradient, copy) shares this opacity so
  // it reads as one moment rather than a sequence of arrivals.
  useEffect(() => {
    const el = sectionRef.current;
    if (!el) return;
    const reduced = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (reduced) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setRevealOpacity(1);
      return;
    }

    const REVEAL_START = 0.05;
    const REVEAL_END = 0.4;

    let raf = 0;
    const compute = () => {
      raf = 0;
      const node = sectionRef.current;
      if (!node) return;
      const vh = window.innerHeight;
      const rect = node.getBoundingClientRect();
      const sectionHeight = rect.height;
      let p = (vh - rect.top) / (vh + sectionHeight);
      if (p < 0) p = 0;
      else if (p > 1) p = 1;

      let t = (p - REVEAL_START) / (REVEAL_END - REVEAL_START);
      if (t < 0) t = 0;
      else if (t > 1) t = 1;
      // Ease-out cubic — quiet at the start, resolves toward the end.
      const eased = 1 - Math.pow(1 - t, 3);
      setRevealOpacity(eased);
    };

    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(compute);
    };

    compute();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);
    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <footer
      ref={sectionRef}
      aria-label="Site"
      className="relative w-full overflow-hidden"
    >
      {/* ---------- Image stage ---------- */}
      <div className="relative h-[clamp(620px,80vh,940px)] w-full md:h-[clamp(560px,72vh,820px)]">
        <Image
          src="/hacienda-footer-master.jpg"
          alt=""
          fill
          quality={92}
          sizes="100vw"
          // Mobile: doorway centred vertically. Desktop: doorway biased
          // to left-third so the right wall is free for the overlay.
          className="object-cover object-center md:object-[35%_center]"
          // Opacity is scroll-driven (no CSS transition — smoothness
          // comes from the rAF-throttled handler). Filter softens the
          // photograph so the page lands inside it, not against it.
          style={{
            opacity: revealOpacity,
            filter: "brightness(0.92) saturate(0.95) contrast(1.02)",
          }}
        />

        {/* Mobile darken — bottom band where the overlay sits. */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 md:hidden"
          style={{
            opacity: revealOpacity,
            backgroundImage:
              "linear-gradient(to bottom, transparent 32%, rgba(20,18,16,0.42) 60%, rgba(20,18,16,0.82) 100%)",
          }}
        />

        {/* Desktop darken — radial in the lower-right quadrant only. */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 hidden md:block"
          style={{
            opacity: revealOpacity,
            backgroundImage:
              "radial-gradient(ellipse 64% 76% at 92% 88%, rgba(20,18,16,0.68), rgba(20,18,16,0.32) 50%, transparent 78%)",
          }}
        />

        {/* ---------- Brand block — anchored mid-low ----------
            Sizing, spacing, and tone match the homepage closer
            (HomeFooterOverlay): Symbol xl, gap-y-4 between rows, the
            same opacity hierarchy on eyebrow and tagline. Centered on
            mobile; right-anchored on desktop so the column sits over
            the plaster wall and clears the doorway / wine glass. */}
        <div
          className="
            pointer-events-auto absolute inset-x-6 bottom-24 mx-auto flex
            max-w-md flex-col items-center gap-y-4 text-center
            sm:bottom-28
            md:inset-auto md:right-[6vw] md:bottom-[18vh] md:max-w-[360px] md:mx-0
          "
          style={{ opacity: revealOpacity }}
        >
          <NewsletterSignup variant="light" />

          <div className="mt-2">
            <Link
              href="/home"
              aria-label="Hessentials — home"
              className="inline-block transition-opacity duration-500 ease-out hover:opacity-70"
            >
              <Symbol size="xl" variant="inverse" alt="Hessentials" />
            </Link>
          </div>

          <p className="text-[11px] uppercase tracking-[0.28em] text-[#f8f6f3]/70 sm:text-[12px]">
            Hessentials
          </p>

          <p className="font-serif text-[16px] italic leading-[1.4] text-[#f8f6f3]/75 sm:text-[17px]">
            This is what stayed.
          </p>
        </div>

        {/* ---------- Utility row — anchored at the bottom-left edge ----------
            One line, left-aligned, no dividers. Legal nav and © year
            flow as plain flex items separated only by gap. The page's
            last whisper, set apart from the brand block above-right. */}
        <nav
          aria-label="Legal"
          className="
            pointer-events-auto absolute bottom-5 left-6 right-6 flex
            flex-wrap items-center gap-x-6 gap-y-2
            text-[10px] uppercase tracking-[0.24em] text-[#f8f6f3]/65
            sm:bottom-6 sm:gap-x-7 sm:text-[11px]
            md:left-[6vw] md:right-auto md:bottom-[3.5vh]
          "
          style={{ opacity: revealOpacity }}
        >
          {LEGAL_LINKS.map((link) =>
            link.external ? (
              <a
                key={link.href}
                href={link.href}
                className="transition-colors duration-300 hover:text-[#f8f6f3]"
              >
                {link.label}
              </a>
            ) : (
              <Link
                key={link.href}
                href={link.href}
                className="transition-colors duration-300 hover:text-[#f8f6f3]"
              >
                {link.label}
              </Link>
            )
          )}
          <span className="text-[#f8f6f3]/55">© {year}</span>
        </nav>
      </div>
    </footer>
  );
}
