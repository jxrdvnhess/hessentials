"use client";

import { useEffect, useRef, useState } from "react";

type PoemLineProps = {
  /** The italic line to reveal. */
  children: string;
  /**
   * Milliseconds the dissolve takes. The poem lines use a long dissolve
   * (~1.6s); the closing tagline lands slightly more slowly (~2.0s) so
   * it settles before the next section begins.
   */
  durationMs?: number;
  /** Inline padding above/below — vertical breathing room inside the gap. */
  className?: string;
};

/**
 * A single italic poem line, centered in the cream gap between two
 * cinematic sections of the homepage.
 *
 * BEHAVIOR
 *   The line is invisible on mount, then fades in via a slow, eased
 *   dissolve the first time it scrolls into view. No transform, no
 *   slide, no typewriter — the eye should catch the line in mid-arrival,
 *   not chase it.
 *
 * MOTION
 *   Opacity-only. Cubic ease-out. Long duration (1.6s default). Reduced
 *   motion users skip the fade — line mounts already-visible.
 *
 * ARCHITECTURAL NOTE
 *   FadeOnScroll already exists, but its 500ms default and 0.12 threshold
 *   are tuned for editorial photo reveals, not for type that needs to
 *   "catch in mid-arrival." The poem wants a longer, later dissolve.
 *   Composing on top of FadeOnScroll's defaults via props would require
 *   passing through enough overrides that a small dedicated component
 *   reads cleaner.
 */
export default function PoemLine({
  children,
  durationMs = 1600,
  className = "",
}: PoemLineProps) {
  const ref = useRef<HTMLParagraphElement | null>(null);
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

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setShown(true);
            observer.disconnect();
            break;
          }
        }
      },
      // 0.6 threshold + negative bottom margin — line waits until it's
      // genuinely centered in the viewport before starting the dissolve.
      { threshold: 0.6, rootMargin: "0px 0px -10% 0px" }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  const opacity = !armed || shown ? 1 : 0;

  return (
    <section
      aria-hidden
      className={`flex w-full justify-center px-6 ${className}`}
    >
      <p
        ref={ref}
        className="text-balance max-w-[36rem] text-center font-serif text-[clamp(1.25rem,2vw,1.625rem)] italic leading-[1.4] text-[#1f1d1b]/65"
        style={{
          opacity,
          transitionProperty: "opacity",
          transitionDuration: `${durationMs}ms`,
          transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
        }}
      >
        {children}
      </p>
    </section>
  );
}
