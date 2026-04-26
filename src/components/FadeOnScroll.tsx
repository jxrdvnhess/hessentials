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
 * Mounts the children at opacity 0, then transitions to 1 the first time the
 * element intersects the viewport. Used for editorial pacing — the lifestyle
 * image fading into view as the reader scrolls past the hero. Opacity-only.
 * No transform, no scale. Respects `prefers-reduced-motion`.
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
  const [shown, setShown] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    // Reduced-motion users skip the fade — show immediately. setState here is
    // browser-only (matchMedia isn't safe at SSR) so the effect is the right
    // place to read it; we set once and bail.
    const reduce =
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setShown(true);
      return;
    }

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
  const mergedStyle: CSSProperties = {
    transitionProperty: "opacity",
    transitionDuration: `${durationMs}ms`,
    transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
    opacity: shown ? 1 : 0,
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
