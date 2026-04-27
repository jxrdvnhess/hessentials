"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  useScrollRevealStack,
  revealStyle,
} from "../lib/useScrollRevealStack";

type Article = { title: string; url: string; payoff: string };

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
    payoff: "fast, rich, and actually satisfying.",
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
    payoff: "the one detail people actually notice.",
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
    payoff: "what it's actually doing to your clothes.",
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

const RETHINKING: Article[] = [
  {
    title: "the anti-trend rule",
    url: "/style/the-anti-trend-rule",
    payoff: "what to ignore. and how.",
  },
  {
    title: "style is not gendered",
    url: "/style/style-is-not-gendered",
    payoff: "the rule that's already breaking.",
  },
  {
    title: "you're not bad with plants",
    url: "/living/youre-not-bad-with-plants",
    payoff: "the lie you keep telling yourself.",
  },
  {
    title: "why most kitchens are set up wrong",
    url: "/living/why-most-kitchens-are-set-up-wrong",
    payoff: "the layout problem nobody fixes.",
  },
  {
    title: "it's usually the small things",
    url: "/style/its-usually-the-small-things",
    payoff: "the small things doing the heavy lifting.",
  },
  {
    title: "ditch the coffee machine, get an espresso machine",
    url: "/living/ditch-the-coffee-machine-get-an-espresso-machine",
    payoff: "the upgrade you'll never undo.",
  },
];

const SLOTS = [
  { label: "Cooking", articles: COOKING },
  { label: "Wearing", articles: WEARING },
  { label: "Refining", articles: REFINING },
  { label: "Shopping", articles: SHOPPING },
  { label: "Rethinking", articles: RETHINKING },
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
};

export default function RightNow({
  variant = "default",
  hideEyebrow = false,
}: RightNowProps) {
  // Initial state matches SSR output to avoid hydration mismatch.
  // Randomization fires after mount; refresh = new pick across all slots.
  const [picks, setPicks] = useState<Article[]>(() =>
    SLOTS.map((s) => s.articles[0])
  );

  useEffect(() => {
    // Deliberate: server renders the first article in each slot to keep
    // hydration deterministic, then the client randomizes once after mount.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setPicks(SLOTS.map((s) => pickRandom(s.articles)));
  }, []);

  // Scroll-LINKED reveal (not timer-triggered). Reveal is tied to the
  // wrapper's scroll progress through the viewport, so every row gets
  // its turn regardless of where it sits in the stack. Strict
  // sequential gating ensures no row appears before the row above is
  // essentially complete — fast scroll and slow scroll produce the
  // same ordered emergence, just compressed/stretched in time.
  //
  // Eyebrow ("Currently") is row 0; the five SLOTS follow as rows 1–5.
  const { wrapperRef, setRow, progress } = useScrollRevealStack(
    SLOTS.length + 1,
    { followLagSeconds: 0.6 }
  );

  const light = variant === "light";

  // Light variant uses cream tones at the same opacity values so the
  // overlay reads against a darkened image with the same hierarchy.
  const eyebrow = light
    ? "text-[#f8f6f3]/65"
    : "text-[#1f1d1b]/50";
  const preEyebrow = light
    ? "text-[#f8f6f3]/40"
    : "text-[#1f1d1b]/35";
  const slotLabel = light
    ? "text-[#f8f6f3]/55"
    : "text-[#1f1d1b]/40";
  const articleTitle = light
    ? "text-[#f8f6f3]/95"
    : "text-[#1f1d1b]/90";
  const articlePayoff = light
    ? "text-[#f8f6f3]/70"
    : "text-[#1f1d1b]/55";

  return (
    <div ref={wrapperRef as React.RefObject<HTMLDivElement>} className="right-now">
      {!hideEyebrow && (
        <div
          ref={setRow(0)}
          style={revealStyle(progress[0] ?? 0)}
          className="mb-7"
        >
          <p
            className={`mb-2 font-serif text-[12px] italic leading-none sm:text-[13px] ${preEyebrow}`}
          >
            Lately
          </p>
          <p
            className={`text-[11px] uppercase leading-none tracking-[0.26em] sm:text-[12px] ${eyebrow}`}
          >
            Currently
          </p>
        </div>
      )}
      <ul className="space-y-6">
        {SLOTS.map((slot, i) => {
          const article = picks[i];
          // Row index in the reveal stack: eyebrow is 0; slots are 1+.
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
                  className={`inline-flex items-baseline gap-2 font-serif text-[17px] italic leading-[1.35] transition-opacity duration-300 ease-out group-hover:opacity-60 sm:text-[18px] ${articleTitle}`}
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
