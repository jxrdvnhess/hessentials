"use client";

import { useEffect, useRef, useState } from "react";

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
        <p>
          For as long as I can remember, the people in my life have asked
          me what I think.
        </p>

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
          moods. I wanted to build one that leaned on discernment itself.
        </p>

        <p className="mt-5">So this is Hessentials.</p>

        <p className="mt-5">
          A curated editorial home for choosing well. Food, home, style,
          practice. The small decisions that hold up &mdash; what to cook,
          what to keep, what to buy, what to ignore. Not trends. Not
          algorithms. Not a performance of taste. Only what proves itself.
        </p>

        <p className="mt-5">
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
