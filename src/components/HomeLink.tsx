"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { MouseEvent, ReactNode } from "react";

type HomeLinkProps = {
  children: ReactNode;
  className?: string;
  /** Accessible label — defaults to "Hessentials — home". */
  ariaLabel?: string;
};

/**
 * HomeLink — wrapper around `<Link href="/" />` that ensures clicking
 * the wordmark or symbol always lands at the top of the homepage.
 *
 * Cross-page clicks (e.g. /recipes → /) are already handled by Next.js
 * Link's default scroll behavior. Same-page clicks (you're on / and
 * click the wordmark) don't trigger a navigation, so without this
 * handler nothing happens — the user expects to be returned to the top.
 *
 * Behavior:
 *   - pathname !== "/"  →  Link navigates normally; Next.js scrolls to top.
 *   - pathname === "/"  →  preventDefault + window.scrollTo({ top: 0,
 *                          behavior: "smooth" }).
 *
 * Reduced-motion: smooth scrolling is gated by `behavior` — browsers
 * respecting prefers-reduced-motion (Safari, Firefox, Chrome 124+) jump
 * instead of animating, which is the right read.
 */
export default function HomeLink({
  children,
  className,
  ariaLabel = "Hessentials — home",
}: HomeLinkProps) {
  const pathname = usePathname();

  const handleClick = (e: MouseEvent<HTMLAnchorElement>) => {
    if (pathname === "/") {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  return (
    <Link
      href="/"
      aria-label={ariaLabel}
      className={className}
      onClick={handleClick}
    >
      {children}
    </Link>
  );
}
