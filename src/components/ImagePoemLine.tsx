"use client";

import { useEffect, useRef, useState, type CSSProperties } from "react";

type ImagePoemLineProps = {
  /** The italic line. */
  children: string;
  /**
   * Absolute-positioning anchors. Pass any combination of top/right/bottom/left
   * (numbers as %, or strings with units). The component renders inside an
   * absolutely positioned wrapper that itself sits inside the parent image's
   * relative container.
   */
  position: {
    top?: string;
    right?: string;
    bottom?: string;
    left?: string;
    /** Optional max-width for the line block (defaults to a sensible cap). */
    maxWidth?: string;
    /** Inline-style transform (e.g., centering tricks). */
    transform?: string;
    /** Text alignment within the block. Default "left". */
    align?: "left" | "center" | "right";
  };
  /** Type size band per §1.2 — 40px / 48px / 56px. */
  size?: "sm" | "md" | "lg";
  /**
   * Reveal delay relative to the natural intersection trigger. Used to land
   * the closing line ~200ms after the four poem lines settle.
   */
  delayMs?: number;
  /**
   * Optional thesis standfirst that pairs with the poem line. When present,
   * renders below the line as a print pull-quote with hairlines bracketing
   * top and bottom. Desktop only (md+) — on smaller breakpoints the
   * standfirst should render outside the image (see Frame 3 mobile cream
   * block in home/page.tsx).
   */
  standfirst?: string;
};

const SIZE_PX: Record<NonNullable<ImagePoemLineProps["size"]>, string> = {
  sm: "clamp(2rem, 3.5vw, 2.5rem)",   // ~32–40px
  md: "clamp(2.25rem, 4vw, 3rem)",    // ~36–48px
  lg: "clamp(2.5rem, 4.5vw, 3.5rem)", // ~40–56px
};

/**
 * In-image poem line.
 *
 * Replaces the cream-gap PoemLine. Each line sits absolutely inside its
 * parent image's relative wrapper, in an art-directed low-detail zone of
 * the photograph (per §1.2 of the design refinement brief).
 *
 * TYPE
 *   Italic serif, weight 500 to survive textured photographic backgrounds.
 *   Cream `#f1ece2` at 95% opacity (full white reads digital).
 *   Line-height 1.2.
 *
 * HAIRLINE
 *   0.5px, 80px wide, centered to the text alignment. Same cream at 95%.
 *   16px gap below the line.
 *
 * REVEAL
 *   Opacity 0 → 95% over ~650ms ease-out, triggered when the line's
 *   center crosses ~70% of viewport height. Once revealed, stays.
 *   Reduced-motion users mount already-visible.
 */
export default function ImagePoemLine({
  children,
  position,
  size = "md",
  delayMs = 0,
  standfirst,
}: ImagePoemLineProps) {
  const ref = useRef<HTMLDivElement | null>(null);
  const [armed, setArmed] = useState(false);
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const reduce =
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) return;

    // eslint-disable-next-line react-hooks/set-state-in-effect
    setArmed(true);

    // Trigger when the element's bottom crosses ~70% of viewport height —
    // i.e., when the line itself is sitting in the upper-middle of the
    // viewport, not just barely entering.
    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            if (delayMs > 0) {
              window.setTimeout(() => setShown(true), delayMs);
            } else {
              setShown(true);
            }
            observer.disconnect();
            break;
          }
        }
      },
      { threshold: 0.5, rootMargin: "0px 0px -30% 0px" }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [delayMs]);

  const align = position.align ?? "left";
  const wrapperStyle: CSSProperties = {
    position: "absolute",
    top: position.top,
    right: position.right,
    bottom: position.bottom,
    left: position.left,
    maxWidth: position.maxWidth ?? "min(38rem, 60%)",
    transform: position.transform,
    textAlign: align,
    pointerEvents: "none",
  };

  const targetOpacity = !armed || shown ? 0.95 : 0;

  return (
    <div
      ref={ref}
      aria-hidden
      className="z-10"
      style={wrapperStyle}
    >
      <p
        className="font-serif italic leading-[1.2] text-balance"
        style={{
          fontSize: SIZE_PX[size],
          fontWeight: 500,
          color: "#f1ece2",
          opacity: targetOpacity,
          transitionProperty: "opacity",
          transitionDuration: "650ms",
          transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
          textShadow: "0 1px 24px rgba(20, 18, 16, 0.35)",
        }}
      >
        {children}
      </p>
      <span
        aria-hidden
        className={[
          "block",
          align === "center"
            ? "mx-auto"
            : align === "right"
            ? "ml-auto"
            : "mr-auto",
        ].join(" ")}
        style={{
          width: standfirst ? "80px" : "80px",
          height: "0.5px",
          marginTop: "16px",
          backgroundColor: "#f1ece2",
          opacity: targetOpacity,
          transitionProperty: "opacity",
          transitionDuration: "650ms",
          transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
        }}
      />

      {/* Optional standfirst — desktop only. The first hairline above
          this paragraph is the existing one rendered above; this block
          adds the standfirst body and a closing hairline. Cream
          #f1ece2 at ~95% opacity, italic serif, magazine pull-quote
          treatment per Frame 3 §2.1. Hidden on mobile because the
          standfirst would crowd the poem line at small sizes — see
          home/page.tsx for the mobile cream-block fallback. */}
      {standfirst && (
        <div
          className="hidden md:block"
          style={{
            opacity: targetOpacity,
            transitionProperty: "opacity",
            transitionDuration: "650ms",
            transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
          }}
        >
          <p
            className={[
              "font-serif italic text-balance",
              align === "center"
                ? "mx-auto"
                : align === "right"
                ? "ml-auto"
                : "mr-auto",
            ].join(" ")}
            style={{
              marginTop: "16px",
              maxWidth: "min(30rem, 100%)",
              fontSize: "clamp(1.125rem, 1.5vw, 1.375rem)",
              lineHeight: 1.32,
              color: "#f1ece2",
              opacity: 0.95,
              textShadow: "0 1px 24px rgba(20, 18, 16, 0.35)",
            }}
          >
            {standfirst}
          </p>
          <span
            aria-hidden
            className={[
              "block",
              align === "center"
                ? "mx-auto"
                : align === "right"
                ? "ml-auto"
                : "mr-auto",
            ].join(" ")}
            style={{
              width: "80px",
              height: "0.5px",
              marginTop: "16px",
              backgroundColor: "#f1ece2",
              opacity: 0.55,
            }}
          />
        </div>
      )}
    </div>
  );
}
