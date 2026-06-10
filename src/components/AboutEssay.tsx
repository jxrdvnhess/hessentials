"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";

type Variant = "overlay" | "inline";

type AboutEssayProps = {
  /**
   * `overlay` — cream type rendered on top of the dark hacienda image
   * (desktop sticky-backdrop pattern). Includes a small text-shadow
   * for character depth against the photograph.
   *
   * `inline` — dark type on the cream page background (mobile fallback,
   * stacked beneath the image). No shadow, no scrim.
   */
  variant: Variant;
};

/**
 * Editing residue — the page marking itself.
 *
 * Not illustration. The real-world marks a discerning reader leaves on a
 * page: a rule in the margin beside the line that matters, a word circled,
 * a phrase underlined. Graphite over the printed ink, so it reads as
 * annotation on a worked proof — evidence of judgment, observed, not a
 * concept of judgment, invented. Kept faint and slightly uneven on purpose.
 */
const GRAPHITE = "rgba(58,52,47,0.5)";

function MarginRule() {
  return (
    <svg
      aria-hidden
      viewBox="0 0 6 100"
      preserveAspectRatio="none"
      className="pointer-events-none absolute -left-4 top-1 h-[calc(100%-0.5rem)] w-[6px] sm:-left-6"
      style={{ color: GRAPHITE }}
    >
      <path d="M3 1 Q1.4 24 3 49 T2.6 99" fill="none" stroke="currentColor" strokeWidth="1.3" strokeLinecap="round" />
    </svg>
  );
}

function CircleWord({ children }: { children: ReactNode }) {
  return (
    <span className="relative inline-block">
      {children}
      <svg
        aria-hidden
        viewBox="0 0 200 80"
        preserveAspectRatio="none"
        className="pointer-events-none absolute left-1/2 top-1/2 h-[1.95em] w-[122%] -translate-x-1/2 -translate-y-1/2"
        style={{ color: GRAPHITE }}
      >
        <path
          d="M44 13 C13 16 5 41 27 59 C58 75 150 73 183 53 C199 43 195 16 148 9 C106 3 62 8 38 16"
          fill="none"
          stroke="currentColor"
          strokeWidth="1.8"
          strokeLinecap="round"
        />
      </svg>
    </span>
  );
}

function Underline({ children }: { children: ReactNode }) {
  return (
    <span className="relative inline-block whitespace-nowrap">
      {children}
      <svg
        aria-hidden
        viewBox="0 0 200 10"
        preserveAspectRatio="none"
        className="pointer-events-none absolute -bottom-[0.22em] left-0 h-[6px] w-full"
        style={{ color: GRAPHITE }}
      >
        <path d="M2 6 Q52 2.5 100 5 T198 4" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
      </svg>
    </span>
  );
}

/**
 * About — personal essay (Master Update Brief §4 + 2026-04-29 sticky
 * backdrop spec).
 *
 * Two presentations of the same copy:
 *
 *   overlay — desktop. Sits over the sticky merida_moment_5 backdrop
 *   in a left-side column (positioning + scrim are handled by the
 *   parent <AboutPage />, not here). Cream #f1ece2 at 95% with a
 *   subtle character text-shadow.
 *
 *   inline — mobile. Stacks beneath the hero image in normal flow.
 *   Dark warm-near-black on the cream page background. No scrim, no
 *   shadow.
 *
 * Signature is rendered from /public/about/jordan-signature.png via
 * CSS mask-image so the ink takes whatever color we want — currentColor
 * for inheritance, switched per variant.
 */
export default function AboutEssay({ variant }: AboutEssayProps) {
  const ref = useRef<HTMLDivElement | null>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;

    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setVisible(true);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setVisible(true);
            observer.disconnect();
            break;
          }
        }
      },
      { threshold: 0.05 }
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  const isOverlay = variant === "overlay";

  // Overlay: cream #f1ece2 at 95%, subtle text-shadow for character
  // depth against the photograph (paired with the AboutPage left scrim).
  // Inline: warm near-black on cream page; no shadow.
  const textColor = isOverlay ? "#f1ece2" : "#1f1d1b";
  const textOpacity = isOverlay ? 0.95 : 0.92;
  const textShadow = isOverlay
    ? "0 1px 14px rgba(0, 0, 0, 0.45), 0 0 1px rgba(0, 0, 0, 0.3)"
    : "none";

  return (
    <div
      ref={ref}
      className="relative"
      style={{
        opacity: visible ? 1 : 0,
        transitionProperty: "opacity",
        transitionDuration: "700ms",
        transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
      }}
    >
      <div
        className="font-serif italic text-[16px] leading-[1.65] sm:text-[18px] md:text-[20px] md:leading-[1.7]"
        style={{
          color: textColor,
          opacity: textOpacity,
          textShadow,
        }}
      >
        {/* The opening line is the de facto headline — wrap it as the
            page <h1> so screen readers and crawlers have an anchor.
            Visual register stays the same (no font/size shift); the
            tag swap is purely semantic. */}
        <h1 className="font-[inherit] text-[inherit] leading-[inherit] tracking-[inherit] m-0">
          For as long as I can remember, the people in my life have asked
          me what I think.
        </h1>

        <p className="mt-5">
          What to wear to the thing. How to set the table. Which flowers
          for the dinner. What pot to buy. What to cook when nothing in
          the fridge looks like dinner. Whether the apartment is worth it.
          Whether the wedding gift is too much or not enough.
        </p>

        <p className="mt-5">
          I don&rsquo;t think this is unusual. Most people have someone
          they call. I&rsquo;m the person a lot of people call.
        </p>

        <p className="mt-5">
          It isn&rsquo;t trained or formal. I have an eye for what&rsquo;s
          right, and I trust it. The work is in the discernment &mdash;
          knowing what holds up and what doesn&rsquo;t, when something is
          technically fine but energetically off, what&rsquo;s the real
          version of a thing and what&rsquo;s the performance of one.
        </p>

        <p className="mt-5">
          My instinct is to refine. To look at something and see
          what&rsquo;s slightly off, then make the small adjustments that
          move it from fine to right. That&rsquo;s what I do with
          everything &mdash; meals, rooms, sentences, plans. Hessentials
          is what happens when that instinct gets pointed at the entire
          small-decisions catalog of a life.
        </p>

        <p className="mt-5">
          It&rsquo;s the formalization of something that was already
          happening.
        </p>

        <p className="mt-5">
          Most editorial brands lean on personality or trends or aesthetic
          moods. I wanted to build one that leaned on{" "}
          <CircleWord>discernment</CircleWord> itself.
        </p>

        <p className="mt-5">So this is Hessentials.</p>

        <p className="mt-5">
          A curated editorial home for choosing well. Food, home, style,
          practice. The small decisions that hold up &mdash; what to cook,
          what to keep, what to buy, what to ignore. Not trends. Not
          algorithms. Not a performance of taste. Only what{" "}
          <Underline>proves itself</Underline>.
        </p>

        <p className="relative mt-5">
          <MarginRule />
          Every piece passes one test before it gets in: does it refuse a
          false binary and occupy a third stance with standards. If it
          does, it stays. If it doesn&rsquo;t, it doesn&rsquo;t.
        </p>

        <p className="mt-5">That&rsquo;s all of it.</p>

        <Signature variant={variant} />
      </div>
    </div>
  );
}

/**
 * Hand-drawn signature from /public/about/jordan-signature.png (508×492
 * RGBA — heart on the left, JH-with-flourish on the right).
 *
 * Rendered via CSS mask-image so the ink takes the cream/dark color the
 * variant wants. The PNG itself can stay near-black; the mask uses the
 * alpha channel and the box's backgroundColor fills it.
 *
 * Sized to roughly 2-3 lines of body text height; aspect 508:492
 * preserves the proportions.
 */
function Signature({ variant }: { variant: Variant }) {
  const isOverlay = variant === "overlay";
  const inkColor = isOverlay ? "#f1ece2" : "#1f1d1b";
  const inkOpacity = isOverlay ? 0.95 : 0.85;

  return (
    <div
      aria-label="Jordan Hess"
      className="mt-10 sm:mt-12"
      style={{
        width: "clamp(110px, 14vw, 150px)",
        aspectRatio: "508 / 492",
        backgroundColor: inkColor,
        opacity: inkOpacity,
        WebkitMaskImage: "url(/about/jordan-signature.png)",
        maskImage: "url(/about/jordan-signature.png)",
        WebkitMaskSize: "contain",
        maskSize: "contain",
        WebkitMaskRepeat: "no-repeat",
        maskRepeat: "no-repeat",
        WebkitMaskPosition: "left center",
        maskPosition: "left center",
      }}
    />
  );
}
