"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
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
 * Site footer.
 *
 * Every page closes inside the cinematic photograph rather than on a
 * separate cream slab. The image is the primary surface; the footer
 * (newsletter + brand mark + tagline + legal) is layered into the safe
 * zones over a quiet darken.
 *
 * The homepage used to own its own closer (HomeFooterOverlay on
 * merida-moment-4.jpg) — that image and its "What was real, stayed."
 * line moved into the Practice statement teaser, and the site close
 * unified to this universal footer.
 */
export default function SiteFooter() {
  return <CinematicFooter />;
}

/**
 * Cinematic image footer.
 *
 * IMAGE
 *   /splash/morning-merida.jpg — morning bedroom, raking sun, unmade
 *   linens, a figure crossing the archway. The previous dusk-courtyard
 *   image read as architectural showcase; this one carries human
 *   presence and morning-light register, keeping the footer's emotional
 *   tone in step with the editorial voice. Same asset is used in the
 *   /home splash sequence — the repetition is intentional.
 *   The dusk image is archived at /merida-courtyard-dusk-archived.jpg
 *   for reuse later (Aurelian, Practice, future newsletter header).
 *
 * DESKTOP (md+)
 *   Image fills 60–75vh. Newsletter / symbol / tagline overlay anchors
 *   to the lower-right (over the plaster wall, clear of the doorway and
 *   wine glass). Legal nav sits at the bottom-left edge. The page lands
 *   inside the photograph.
 *
 * MOBILE (< md)
 *   Image becomes a clean hero (no overlaid text — type was unreadable
 *   on top of portrait-cropped image features). A cream-colored footer
 *   block below holds the newsletter, symbol, tagline, legal, and ©
 *   year in a properly stacked layout with editorial breathing room.
 *   This is the same brand close, composed for the device.
 *
 * REVEAL
 *   The image fades in as the section enters the viewport (scroll-LINKED,
 *   eased ease-out cubic). Reduced-motion users mount already-revealed.
 */
function CinematicFooter() {
  const sectionRef = useRef<HTMLElement | null>(null);
  const reducedMotion =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const [revealOpacity, setRevealOpacity] = useState<number>(
    reducedMotion ? 1 : 0
  );
  const year = new Date().getFullYear();

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
      className="relative w-full"
    >
      {/* ---------- Image stage ----------
          Mobile: 3:2 landscape crop. The 4:5 portrait crop we used to
                  ship cropped the source (1672×941, ~16:9) into a narrow
                  vertical strip — only the doorway zone read, and the
                  bed on the left and the figure-shadow on the right
                  both got chopped off. 3:2 lets ~85% of the source
                  width show on a 390-430px viewport, so the full
                  composition (linens / doorway / figure / shadow) lands
                  the way it does on desktop. The brand whisper
                  (wordmark + tagline) still sits at the bottom; the
                  cream block holds newsletter + legal beneath.
          Desktop: 72vh+ with full overlay zones (aspect matches). */}
      <div className="relative aspect-[3/2] w-full overflow-hidden md:aspect-auto md:h-[clamp(560px,72vh,820px)]">
        <Image
          src="/splash/morning-merida.jpg"
          alt=""
          fill
          quality={92}
          sizes="100vw"
          className="object-cover object-center"
          style={{
            opacity: revealOpacity,
            // Slight darken + warm bias so cream type sits cleanly on
            // the linens and shadow wall. Tune after live preview if
            // any zone fights the type.
            filter: "brightness(0.94) saturate(0.98) contrast(1.02)",
          }}
        />

        {/* DESKTOP-ONLY: radial darken in lower-right quadrant. */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 hidden md:block"
          style={{
            opacity: revealOpacity,
            backgroundImage:
              "radial-gradient(ellipse 64% 76% at 92% 88%, rgba(20,18,16,0.68), rgba(20,18,16,0.32) 50%, transparent 78%)",
          }}
        />

        {/* MOBILE-ONLY: bottom darken + brand whisper overlay. */}
        <div
          aria-hidden
          className="pointer-events-none absolute inset-0 md:hidden"
          style={{
            opacity: revealOpacity,
            backgroundImage:
              "linear-gradient(to bottom, transparent 50%, rgba(20,18,16,0.28) 75%, rgba(20,18,16,0.65) 100%)",
          }}
        />
        <div
          className="absolute inset-x-0 bottom-9 flex flex-col items-center text-center md:hidden"
          style={{ opacity: revealOpacity }}
        >
          <p
            className="font-serif text-[20px] italic leading-[1.3] text-[#f1ece2] sm:text-[22px]"
            style={{ opacity: 0.95 }}
          >
            This is what stayed.
          </p>
          <p className="mt-3 text-[11px] uppercase tracking-[0.3em] text-[#f8f6f3]/85">
            Hessentials
          </p>
        </div>

        {/* DESKTOP-ONLY: brand block, anchored mid-low-right. */}
        <div
          className="
            pointer-events-auto absolute right-[6vw] bottom-[18vh] mx-0 hidden
            max-w-[360px] flex-col items-center gap-y-4 text-center
            md:flex
          "
          style={{ opacity: revealOpacity }}
        >
          <NewsletterSignup variant="light" />

          <p
            className="mt-3 font-serif text-[24px] italic leading-[1.3] text-[#f1ece2] sm:text-[26px]"
            style={{ opacity: 0.95 }}
          >
            This is what stayed.
          </p>

          <div className="mt-1">
            <HomeLink className="inline-block transition-opacity duration-500 ease-out hover:opacity-70">
              <Symbol size="xl" variant="inverse" alt="Hessentials" />
            </HomeLink>
          </div>

          <p className="text-[12px] uppercase tracking-[0.28em] text-[#f8f6f3]/70">
            Hessentials
          </p>
        </div>

        {/* DESKTOP-ONLY: legal nav, bottom-left. */}
        <nav
          aria-label="Legal"
          className="
            pointer-events-auto absolute bottom-[3.5vh] left-[6vw] hidden
            flex-wrap items-center gap-x-7 gap-y-2 text-[11px] uppercase
            tracking-[0.24em] text-[#f8f6f3]/65 md:flex
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

      {/* ---------- MOBILE-ONLY: cream block below image ----------
          The cleanup image carries the brand whisper (Hessentials /
          "This is what stayed."); this block holds the rest —
          symbol, newsletter, legal. Two halves of one composition. */}
      <div className="block md:hidden">
        <div className="mx-auto flex max-w-[420px] flex-col items-center gap-y-8 px-6 pt-14 pb-10 text-center sm:px-8 sm:pt-16 sm:pb-12">
          <HomeLink className="inline-block transition-opacity duration-500 ease-out hover:opacity-70">
            <Symbol size="xl" alt="Hessentials" />
          </HomeLink>

          <NewsletterSignup variant="default" />

          <nav
            aria-label="Legal"
            className="mt-3 flex flex-col items-center gap-y-3 text-[10.5px] uppercase tracking-[0.24em] text-[#1f1d1b]/45"
          >
            <div className="flex items-center gap-x-5">
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
      </div>
    </footer>
  );
}
