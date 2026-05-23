"use client";

import { useEffect } from "react";
import { trackArticleRead } from "../lib/analytics";

type Props = {
  pillar: "living" | "style" | "practice";
  slug: string;
};

/**
 * ArticleScrollTracker
 *
 * Renders nothing. Wires a scroll listener that fires `article_read`
 * once per page when the user crosses 75% of the document body.
 *
 * Why 75% and not the GA4 enhanced-measurement default: enhanced
 * measurement fires `scroll` at 90%, which is too late to register as
 * "this person actually read the piece" — by then they've likely
 * already scrolled past the closing byline into the onward nav. 75%
 * lands inside the body, on the final reading beat.
 *
 * The listener self-unmounts after the first crossing so the event
 * fires at most once per page view.
 */
export default function ArticleScrollTracker({ pillar, slug }: Props) {
  useEffect(() => {
    let fired = false;

    const check = () => {
      if (fired) return;
      const doc = document.documentElement;
      const scrolled = window.scrollY + window.innerHeight;
      const total = doc.scrollHeight;
      if (total <= 0) return;
      const ratio = scrolled / total;
      if (ratio >= 0.75) {
        fired = true;
        trackArticleRead({ pillar, slug });
        window.removeEventListener("scroll", check);
      }
    };

    // Short pages: a short article may already pass 75% on first paint.
    // Run an initial check on next frame so we catch that case without
    // racing layout.
    const rafId = window.requestAnimationFrame(check);

    window.addEventListener("scroll", check, { passive: true });
    return () => {
      window.cancelAnimationFrame(rafId);
      window.removeEventListener("scroll", check);
    };
  }, [pillar, slug]);

  return null;
}
