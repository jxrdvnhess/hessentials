"use client";

import {
  useEffect,
  useRef,
  useState,
  type CSSProperties,
  type ReactNode,
} from "react";

type FadeOnScrollProps = {
  children: ReactNode;
  /** Tailwind/inline-friendly extra classes for the wrapper element. */
  className?: string;
  /** Element type. Defaults to <div>. Use "section" / "figure" as needed. */
  as?: "div" | "section" | "figure";
  /** Inline style passthrough — used for things like `aria-hidden` containers. */
  style?: CSSProperties;
  /** Fade duration in ms. */
  durationMs?: number;
  /** Trigger threshold (0–1). Default 0.12 — fires just as it enters view. */
  threshold?: number;
  /** Top/bottom margin on the observer's root viewport, e.g. "0px 0px -10% 0px". */
  rootMargin?: string;
};

/**
 * Reveals children with an opacity fade the first time they enter the
 * viewport. Used for editorial pacing — the lifestyle image fading in as
 * the reader scrolls past the hero. Opacity-only. No transform, no scale.
 *
 * Visibility model is inverted on purpose: the SSR / no-JS / print-mode
 * default is **visible**. JS arms the wrapper after mount (briefly hiding
 * it), then the IntersectionObserver reveals it. This way crawlers,
 * print-to-PDF, and JS-disabled clients always see the content.
 *
 * Respects `prefers-reduced-motion` — those users skip the fade entirely.
 */
export default function FadeOnScroll({
  children,
  className = "",
  as = "div",
  style,
  durationMs = 500,
  threshold = 0.12,
  rootMargin = "0px",
}: FadeOnScrollProps) {
  const ref = useRef<HTMLElement | null>(null);
  const [armed, setArmed] = useState(false);
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    // Reduced-motion users: don't arm. Element stays at its SSR default
    // (visible). No flash, no transition.
    const reduce =
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) return;

    // Arm: hide immediately. Brief flash on slow first paint, but ensures
    // the IntersectionObserver fade is visible when it fires.
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
      { threshold, rootMargin }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [threshold, rootMargin]);

  const Tag = as;
  // Visible by default. Hidden only when JS has armed the element AND it
  // hasn't been intersected yet.
  const opacity = !armed || shown ? 1 : 0;
  const mergedStyle: CSSProperties = {
    transitionProperty: "opacity",
    transitionDuration: `${durationMs}ms`,
    transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
    opacity,
    ...style,
  };

  return (
    <Tag
      ref={ref as React.RefObject<HTMLDivElement>}
      className={className}
      style={mergedStyle}
    >
      {children}
    </Tag>
  );
}
