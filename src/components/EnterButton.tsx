"use client";

import { MouseEvent } from "react";

// Slow, calm easing — gentle in, gentle out.
const easeInOutCubic = (t: number) =>
  t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

const SCROLL_DURATION_MS = 1600;

function smoothScrollTo(target: HTMLElement, duration: number) {
  const start = window.scrollY;
  const end = target.getBoundingClientRect().top + start;
  const distance = end - start;
  const startTime = performance.now();

  const step = (now: number) => {
    const t = Math.min((now - startTime) / duration, 1);
    window.scrollTo(0, start + distance * easeInOutCubic(t));
    if (t < 1) requestAnimationFrame(step);
  };

  requestAnimationFrame(step);
}

type EnterButtonProps = {
  targetId: string;
  className?: string;
  children?: React.ReactNode;
};

export default function EnterButton({
  targetId,
  className,
  children = "Enter",
}: EnterButtonProps) {
  const handleClick = (event: MouseEvent<HTMLAnchorElement>) => {
    const target = document.getElementById(targetId);
    if (!target) return;

    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (prefersReducedMotion) {
      // Honor the user's preference — let the native anchor jump handle it.
      return;
    }

    event.preventDefault();
    smoothScrollTo(target, SCROLL_DURATION_MS);
    history.replaceState(null, "", `#${targetId}`);
  };

  return (
    <a href={`#${targetId}`} onClick={handleClick} className={className}>
      {children}
    </a>
  );
}
