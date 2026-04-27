"use client";

import { useEffect, useRef, useState } from "react";

type Options = {
  /**
   * Section progress at which the FIRST row begins revealing (0-1).
   * Default 0 — row 0 starts the moment the wrapper enters the bottom
   * of the viewport.
   */
  startOffset?: number;
  /**
   * Section progress span over which a single row reveals.
   * Larger = slower per row. Default 0.06.
   */
  revealSpan?: number;
  /**
   * Section progress increment between consecutive row START points.
   * Smaller = tighter cascade; larger = more breathing room.
   * Default 0.05.
   */
  stagger?: number;
  /**
   * Strict sequential gate. Row N is held at progress 0 until row N-1
   * reaches at least this much progress. Default 0.75.
   */
  gate?: number;
  /**
   * Time constant (in seconds) for the displayed-progress to catch
   * up to the scroll-driven target progress. Bigger = laggier. Roughly
   * 95% of the catch-up happens within 3 × this value. Default 0.18 —
   * the reveal trails the scroll by ~half a second of perceived motion.
   * Set to 0 for an instant follow (no lag).
   */
  followLagSeconds?: number;
};

/**
 * Scroll-LINKED, lag-smoothed staggered reveal for a stack of rows
 * inside a wrapper section.
 *
 * Two layers:
 *
 *   1. TARGET progress is computed from the wrapper's scroll position
 *      (section progress 0..1 across its travel through the viewport).
 *      Each row gets its own [start, end] window and is gated strictly
 *      sequentially (row N held at 0 until row N-1 reaches `gate`).
 *
 *   2. DISPLAYED progress smooths exponentially toward target over
 *      ~`followLagSeconds`. So the reveal trails the scroll itself
 *      by a perceptible beat — when the user stops scrolling the
 *      reveal is still completing. This avoids the "already there"
 *      feeling of a perfectly scroll-locked animation.
 *
 * Section progress definition:
 *   0 — wrapper top is at viewport bottom (just entering)
 *   1 — wrapper bottom is at viewport top (just leaving)
 *
 * Usage:
 *   const { wrapperRef, setRow, progress } = useScrollRevealStack(rows);
 *
 *   <div ref={wrapperRef}>
 *     <p ref={setRow(0)} style={revealStyle(progress[0])}>...</p>
 *   </div>
 *
 * `prefers-reduced-motion` short-circuits — all rows report fully
 * revealed and no listener / loop is attached.
 */
export function useScrollRevealStack(count: number, options: Options = {}) {
  const {
    startOffset = 0,
    revealSpan = 0.06,
    stagger = 0.05,
    gate = 0.75,
    followLagSeconds = 0.18,
  } = options;

  const wrapperRef = useRef<HTMLElement | null>(null);
  const rowRefs = useRef<(HTMLElement | null)[]>([]);

  const reducedMotion =
    typeof window !== "undefined" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Displayed (animated) progress — what the consumer renders. Target
  // is held in a ref so scroll updates don't trigger React renders;
  // only the smoothing loop writes to React state.
  const [displayed, setDisplayed] = useState<number[]>(() =>
    new Array(count).fill(reducedMotion ? 1 : 0)
  );

  const targetRef = useRef<number[]>(new Array(count).fill(0));
  const displayedRef = useRef<number[]>(
    new Array(count).fill(reducedMotion ? 1 : 0)
  );

  useEffect(() => {
    if (reducedMotion) {
      // Reduced-motion users: skip the smoothing loop entirely and
      // just present everything as fully revealed. This is needed in
      // addition to the lazy state initializer because SSR can't read
      // matchMedia and so initial state may have been computed with
      // reducedMotion=false.
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setDisplayed(new Array(count).fill(1));
      return;
    }

    let scrollRaf = 0;
    let smoothRaf = 0;
    let lastFrameTime = 0;
    const tau = followLagSeconds; // time constant for exp decay

    // -------- Compute target progress from scroll position --------
    const computeTarget = (): number[] => {
      const wrapper = wrapperRef.current;
      const next = new Array<number>(count).fill(0);
      if (!wrapper) return next;

      const vh = window.innerHeight;
      const rect = wrapper.getBoundingClientRect();
      const sectionHeight = rect.height;

      let sectionProgress = (vh - rect.top) / (vh + sectionHeight);
      if (sectionProgress < 0) sectionProgress = 0;
      else if (sectionProgress > 1) sectionProgress = 1;

      let prev = 1; // row 0 is never gated
      for (let i = 0; i < count; i++) {
        const start = startOffset + i * stagger;
        let p = (sectionProgress - start) / revealSpan;
        if (p < 0) p = 0;
        else if (p > 1) p = 1;
        if (prev < gate) p = 0;
        next[i] = p;
        prev = p;
      }
      return next;
    };

    // -------- Smoothing loop: pulls displayed toward target --------
    const smoothStep = (now: number) => {
      const dt = lastFrameTime ? (now - lastFrameTime) / 1000 : 0;
      lastFrameTime = now;

      // Decay factor of the *gap* between current and target.
      //   tau == 0      → snap (no lag)
      //   dt == 0       → no time elapsed, decay = 1, no movement
      //   dt > 0        → 0 < decay < 1, gap shrinks
      // Math.exp(0) = 1 naturally satisfies the dt==0 case; the previous
      // `dt > 0` guard was a bug that made every first frame snap.
      const decay = tau > 0 ? Math.exp(-Math.max(dt, 0) / tau) : 0;

      const target = targetRef.current;
      const cur = displayedRef.current;
      let allConverged = true;

      for (let i = 0; i < count; i++) {
        const next = target[i] + (cur[i] - target[i]) * decay;
        cur[i] = next;
        if (Math.abs(next - target[i]) > 0.0008) {
          allConverged = false;
        }
      }

      // One React state update per frame keeps consumers in sync. The
      // array is recreated so React's referential check fires the
      // re-render.
      setDisplayed(cur.slice());

      if (!allConverged) {
        smoothRaf = requestAnimationFrame(smoothStep);
      } else {
        smoothRaf = 0;
        lastFrameTime = 0;
      }
    };

    const startSmoothing = () => {
      if (smoothRaf) return;
      lastFrameTime = 0; // first frame's dt will be 0; no jump
      smoothRaf = requestAnimationFrame(smoothStep);
    };

    // -------- Scroll handler: updates target, kicks smoothing --------
    const updateTarget = () => {
      targetRef.current = computeTarget();
      startSmoothing();
    };

    const onScroll = () => {
      if (scrollRaf) return;
      scrollRaf = requestAnimationFrame(() => {
        scrollRaf = 0;
        updateTarget();
      });
    };

    updateTarget();
    window.addEventListener("scroll", onScroll, { passive: true });
    window.addEventListener("resize", onScroll);

    return () => {
      window.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", onScroll);
      if (scrollRaf) cancelAnimationFrame(scrollRaf);
      if (smoothRaf) cancelAnimationFrame(smoothRaf);
    };
  }, [
    count,
    startOffset,
    revealSpan,
    stagger,
    gate,
    followLagSeconds,
    reducedMotion,
  ]);

  /** Stable ref-setter for row index `i`. */
  const setRow = (i: number) => (el: HTMLElement | null) => {
    rowRefs.current[i] = el;
  };

  return { wrapperRef, setRow, progress: displayed };
}

/**
 * Compute inline style for a row given its 0..1 progress.
 *
 * Holds opacity = progress and a small upward translate that resolves
 * to 0 at full reveal. Untransitioned — smoothness comes from the
 * smoothing loop (rAF + exponential decay), not from CSS transitions
 * (which would compound with the lag and cause smearing).
 */
export function revealStyle(progress: number): React.CSSProperties {
  return {
    opacity: progress,
    transform: `translateY(${(1 - progress) * 10}px)`,
  };
}
