"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  useScrollRevealStack,
  revealStyle,
} from "../lib/useScrollRevealStack";

type Article = { title: string; url: string; payoff: string };

/**
 * Shared picks singleton. Both the desktop overlay and the mobile
 * cream block are separate <RightNow /> instances (they live in
 * different DOM positions — overlay is absolute inside Image 03,
 * cream block is its own section below). To keep them showing the
 * same article in each slot (Frame 4 §3.5 bug fix), we share state
 * via a module-level cache + subscriber set:
 *
 *   - Server render: every instance returns the deterministic initial
 *     picks (first article in each slot) so SSR is stable.
 *   - Client mount: the first instance to fire its useEffect picks
 *     once, writes to the cache, and broadcasts to any other instance
 *     already mounted. Subsequent instances read from the cache.
 *
 * Result: both overlay and cream-block render the same four picks.
 */
let cachedPicks: Article[] | null = null;
const subscribers = new Set<(p: Article[]) => void>();

const COOKING: Article[] = [
  {
    title: "mediterranean shrimp with white beans",
    url: "/recipes/mediterranean-shrimp-white-beans",
    payoff: "weeknight food that dresses up.",
  },
  {
    title: "sunday rigatoni",
    url: "/recipes/sunday-rigatoni",
    payoff: "the pot you make on a slow afternoon.",
  },
  {
    title: "lemon chicken with olives and herbs",
    url: "/recipes/lemon-chicken-with-olives-and-herbs",
    payoff: "bright, briny, almost too easy.",
  },
  {
    title: "tuscan orzo",
    url: "/recipes/tuscan-orzo",
    payoff: "fast, rich, satisfying.",
  },
  {
    title: "caprese chicken",
    url: "/recipes/caprese-chicken",
    payoff: "summer on a plate, year-round.",
  },
  {
    title: "creamy tuscan chicken orzo",
    url: "/recipes/creamy-tuscan-chicken-orzo",
    payoff: "the one you'll cook on repeat.",
  },
  {
    title: "soft scrambled eggs with herbs",
    url: "/recipes/soft-scrambled-eggs-with-herbs",
    payoff: "the breakfast that ruins all others.",
  },
];

const WEARING: Article[] = [
  {
    title: "the uniform is not boring",
    url: "/style/the-uniform-is-not-boring",
    payoff: "the closet stops negotiating with you.",
  },
  {
    title: "casual is not a free pass",
    url: "/style/casual-is-not-a-free-pass",
    payoff: "it only looks effortless.",
  },
  {
    title: "texture is the outfit",
    url: "/style/texture-is-the-outfit",
    payoff: "color is loud. texture is louder.",
  },
  {
    title: "the 5-piece rule",
    url: "/style/the-5-piece-rule",
    payoff: "fewer pieces. better outfits.",
  },
  {
    title: "the bag sets the tone",
    url: "/style/the-bag-sets-the-tone",
    payoff: "the one detail people notice.",
  },
  {
    title: "the signature piece",
    url: "/style/the-signature-piece",
    payoff: "the thing that makes the look yours.",
  },
];

const REFINING: Article[] = [
  {
    title: "the one pot that does everything",
    url: "/living/the-one-pot-that-does-everything",
    payoff: "stop owning twelve. own one.",
  },
  {
    title: "why you don't cook more",
    url: "/living/why-you-dont-cook-more",
    payoff: "it isn't discipline. it's the geography.",
  },
  {
    title: "the 10-minute reset",
    url: "/living/the-10-minute-reset",
    payoff: "the small habit that changes the night.",
  },
  {
    title: "stop using fabric softener",
    url: "/living/stop-using-fabric-softener",
    payoff: "what it's doing to your clothes.",
  },
  {
    title: "the entryway test",
    url: "/style/the-entryway-test",
    payoff: "if it works here, the rest of the house does.",
  },
  {
    title: "stop buying plush blankets, use cotton",
    url: "/living/stop-buying-plush-blankets-use-cotton",
    payoff: "the upgrade nobody talks about.",
  },
];

const SHOPPING: Article[] = [
  {
    title: "the goya thin briefcase",
    url: "/shop/loewe-goya-thin-briefcase",
    payoff: "soft calfskin. doesn't announce the day.",
  },
  {
    title: "court leather sneakers",
    url: "/shop/prada-court-leather-sneakers",
    payoff: "the sneaker you keep wearing once you stop trying to look young.",
  },
  {
    title: "the cotton waffle blanket",
    url: "/shop/bedsure-waffle-blanket",
    payoff: "cotton, not synthetic. the upgrade nobody talks about.",
  },
  {
    title: "the aquaracer, quartz",
    url: "/shop/tag-heuer-aquaracer-quartz",
    payoff: "a real watch, finished correctly.",
  },
  {
    title: "the louxor frame",
    url: "/shop/ahlem-louxor",
    payoff: "hand-finished in france. people notice without knowing why.",
  },
  {
    title: "arizona, oiled leather",
    url: "/shop/birkenstock-arizona-leather",
    payoff: "you stop noticing them after five minutes.",
  },
];

// RETHINKING was removed from CURRENTLY in the 2026-04-30 trim. Its
// register — refusing assumptions, introspection — is the most
// Practice-coded of the slots, and Practice now holds its own
// statement teaser on the homepage. Pulling Rethinking sharpens that
// distinction so CURRENTLY reads as four content rotations and the
// Practice teaser stands alone with its own depth.

const SLOTS = [
  { label: "Cooking", articles: COOKING },
  { label: "Wearing", articles: WEARING },
  { label: "Refining", articles: REFINING },
  { label: "Shopping", articles: SHOPPING },
] as const;

function pickRandom<T>(items: readonly T[]): T {
  return items[Math.floor(Math.random() * items.length)];
}

type RightNowProps = {
  /** "default" — dark on cream (hero usage). "light" — cream on dark image (overlay usage). */
  variant?: "default" | "light";
  /** When true, the "Lately Currently" eyebrow is suppressed (because
   *  it's already shown elsewhere — e.g. as an overlay on the image
   *  above this block on mobile). */
  hideEyebrow?: boolean;
  /**
   * When true, the wrapper applies a slide-in-from-right animation as
   * it enters the viewport — magazine-page-turn feel (cubic-bezier
   * slow-start/hard-finish). Replays on re-entry. Wrapped in
   * prefers-reduced-motion: no-preference so motion-sensitive users
   * see the panel arrive statically. Per Frame 4 §3.4 — only the
   * desktop overlay variant uses it.
   */
  withSlideIn?: boolean;
};

export default function RightNow({
  variant = "default",
  hideEyebrow = false,
  withSlideIn = false,
}: RightNowProps) {
  // Picks come from the shared singleton (see top-of-file). Initial
  // state matches SSR output (first article in each slot) to avoid
  // hydration mismatch; the client-side mount upgrades to the cached
  // randomized picks (or runs the pick once if this instance is first).
  const [picks, setPicks] = useState<Article[]>(
    () => cachedPicks ?? SLOTS.map((s) => s.articles[0])
  );

  useEffect(() => {
    // First instance to mount picks once and broadcasts.
    if (cachedPicks === null) {
      cachedPicks = SLOTS.map((s) => pickRandom(s.articles));
      subscribers.forEach((cb) => cb(cachedPicks!));
    }
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setPicks(cachedPicks);
    subscribers.add(setPicks);
    return () => {
      subscribers.delete(setPicks);
    };
  }, []);

  // Scroll-LINKED reveal (not timer-triggered). Reveal is tied to the
  // wrapper's scroll progress through the viewport, so every row gets
  // its turn regardless of where it sits in the stack. Strict
  // sequential gating ensures no row appears before the row above is
  // essentially complete — fast scroll and slow scroll produce the
  // same ordered emergence, just compressed/stretched in time.
  //
  // Row 0: "Currently" eyebrow (suppressed when hideEyebrow is true).
  // Rows 1–4: the four rotating SLOTS.
  const { wrapperRef, setRow, progress } = useScrollRevealStack(
    SLOTS.length + 1,
    { followLagSeconds: 0.6 }
  );

  // Slide-in animation (desktop overlay only). Replays on re-entry —
  // toggling the .is-visible class via IntersectionObserver. Reduced
  // motion is handled in CSS via @media (prefers-reduced-motion) so
  // we don't need a JS guard here. Observes the same node as the
  // scroll-reveal wrapper (wrapperRef), so no duplicate ref needed.
  useEffect(() => {
    if (!withSlideIn) return;
    const node = wrapperRef.current;
    if (!node) return;
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.intersectionRatio > 0.25) {
            node.classList.add("is-visible");
          } else if (entry.intersectionRatio === 0) {
            // Out of view — reset so re-entry replays the animation.
            node.classList.remove("is-visible");
          }
        }
      },
      { threshold: [0, 0.25, 0.5] }
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, [withSlideIn, wrapperRef]);

  const light = variant === "light";

  // Light variant uses warm cream `#f1ece2` (per §1.3) at high opacity so
  // type reads against a darkened photographic background. The dark
  // (cream-zone) variant keeps the existing warm-near-black hierarchy.
  const eyebrow = light
    ? "text-[#f1ece2]/95"
    : "text-[#1f1d1b]/50";
  const preEyebrow = light
    ? "text-[#f1ece2]/80"
    : "text-[#1f1d1b]/35";
  // Slot labels (COOKING / WEARING / REFINING / SHOPPING): clean
  // uppercase sans, letter-spaced. Cream at 95% on the overlay so
  // they read clearly against the photograph. Per §1.3.
  const slotLabel = light
    ? "text-[#f1ece2]/95"
    : "text-[#1f1d1b]/40";
  // Article links — keep italic, slightly heavier weight (font-medium),
  // cream at 95% on the overlay. Heavier weight applied via a class on
  // the link span itself below.
  const articleTitle = light
    ? "text-[#f1ece2]/95"
    : "text-[#1f1d1b]/90";
  // Supporting deks (payoff lines beneath each link): cream at 80% for
  // hierarchy beneath the link itself. Per §1.3.
  const articlePayoff = light
    ? "text-[#f1ece2]/80"
    : "text-[#1f1d1b]/55";

  // The .right-now-light class keys the slide-in animation + character
  // text-shadow defined in globals.css (Frame 4 §3.3, §3.4).
  const wrapperClass = ["right-now", light ? "right-now-light" : ""]
    .filter(Boolean)
    .join(" ");

  return (
    <div
      ref={wrapperRef as React.RefObject<HTMLDivElement>}
      className={wrapperClass}
    >
      {/* Row 0 — Currently eyebrow. The rotating set below is what's
          on rotation right now. Suppressed only when the eyebrow lives
          on the image above (mobile morning overlay case). Per Frame
          4 §3.1 the old "Start here / The 5 things I cook every week"
          row was removed — Currently leads now. Rows 1–4 (CURRENTLY
          dropped from 5 → 4 slots in the 2026-04-30 trim — RETHINKING
          retired in favor of the Practice statement teaser). */}
      {!hideEyebrow && (
        <div
          ref={setRow(0)}
          style={revealStyle(progress[0] ?? 0)}
          className="mb-7"
        >
          <p
            className={`text-[11px] uppercase leading-none tracking-[0.26em] sm:text-[12px] ${eyebrow}`}
          >
            Currently
          </p>
          <p
            className={`mt-2.5 font-serif text-[12.5px] italic leading-[1.4] sm:text-[13px] ${preEyebrow}`}
          >
            What&rsquo;s in rotation right now.
          </p>
        </div>
      )}
      <ul className="space-y-6">
        {SLOTS.map((slot, i) => {
          const article = picks[i];
          // Row index in the reveal stack: Currently eyebrow is 0, slots
          // start at 1.
          const rowIndex = i + 1;
          return (
            <li
              key={slot.label}
              ref={setRow(rowIndex)}
              style={revealStyle(progress[rowIndex] ?? 0)}
            >
              <p
                className={`text-[10.5px] uppercase tracking-[0.24em] sm:text-[11px] ${slotLabel}`}
              >
                {slot.label}
              </p>
              <Link href={article.url} className="group mt-1 inline-block">
                <span
                  className={`inline-flex items-baseline gap-2 font-serif text-[17px] italic leading-[1.35] transition-opacity duration-300 ease-out group-hover:opacity-60 sm:text-[18px] ${
                    light ? "font-medium" : ""
                  } ${articleTitle}`}
                >
                  {article.title}
                  <span aria-hidden className="text-[12px] not-italic">
                    →
                  </span>
                </span>
                <span
                  className={`mt-1 block text-[13px] leading-[1.45] transition-opacity duration-300 ease-out group-hover:opacity-60 sm:text-[13.5px] ${articlePayoff}`}
                >
                  {article.payoff}
                </span>
              </Link>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
