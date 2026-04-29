// =============================================================================
// PARKED — not imported anywhere as of 2026-04-29.
//
// This component implemented a light-wash splash sequence (cream wash blooms
// over the photograph, then homepage materializes against the held cream).
// It was pulled from /page.tsx after Jordan decided "no splash for now."
// The companion CSS in globals.css was also removed.
//
// Kept in the repo (rather than deleted) because the next splash spec —
// when it lands — may reuse the cookie/skip/reduced-motion plumbing,
// the image-load gate, or the keyframe-driven animation pattern. If the
// next spec is sufficiently different to make this useless, delete it.
//
// Open issue at the time of parking: the brief that followed this code
// (monogram-to-wordmark unfold) hit a hard precondition — the monogram H
// (upright Roman serif) and the wordmark H (italic serif) are different
// glyphs. The splash is on hold pending a re-cut of either mark.
// =============================================================================

"use client";

import { useEffect, useState } from "react";

const COOKIE_NAME = "hessentials_splash_seen";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 30; // 30 days
const TOTAL_DURATION_MS = 3500;
const SKIP_FADE_MS = 200;
const IMAGE_LOAD_GRACE_MS = 200;

function setSeenCookie() {
  document.cookie = `${COOKIE_NAME}=1; max-age=${COOKIE_MAX_AGE}; path=/; samesite=lax`;
}

/**
 * Splash light-wash — first-visit homepage arrival sequence.
 *
 * The photograph holds, then its highlights bloom while a cream wash
 * fades up over it, the cream is held briefly, and the homepage
 * materializes against the cream as the wash fades out — all four
 * surfaces share the same cream value (`--cream-bg`) so the cream
 * itself never moves.
 *
 * Four movements, total runtime 3500ms:
 *   1. Hold (1500ms)         — full-bleed photograph, nothing else
 *   2. Light wash (900ms)    — image filter brightens + desaturates
 *                              while cream overlay fades from 0 → 1
 *   3. Cream hold (300ms)    — pure cream fills the viewport
 *   4. Homepage arrival      — wash fades 1 → 0 while header + main
 *      (800ms)                 fade 0 → 1 against the held cream
 *
 * All keyframes live in globals.css; this component is the small
 * state machine that:
 *   - bypasses entirely under `prefers-reduced-motion`
 *   - bypasses if the splash image hasn't finished loading after the
 *     200ms grace window (never block on a slow connection)
 *   - listens for skip input (click / key / touch / wheel) and cuts
 *     to homepage with a 200ms fade
 *   - sets the 30-day `hessentials_splash_seen` cookie on completion
 *     or skip so returning visitors land directly on the homepage
 *   - tears down the overlay markup and removes the `splash-pending`
 *     class once the sequence ends
 *
 * Mounted by /page.tsx only when the cookie is absent. /page.tsx also
 * emits a tiny inline script that sets `splash-pending` on <html>
 * synchronously before paint, so the SSR'd opacity-0 rule on
 * header + main applies before any first-paint flash.
 */
export default function SplashMorph() {
  const [render, setRender] = useState<"running" | "skipping" | "done">(
    "running"
  );

  useEffect(() => {
    const reduce = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (reduce) {
      setSeenCookie();
      document.documentElement.classList.remove("splash-pending");
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setRender("done");
      return;
    }

    // ---------- Image-load gate ----------
    // Never block on the photograph. The preload link in /page.tsx kicked
    // off the download before this component mounted; if the browser has
    // it ready, the probe's `complete` flag will already be true. If not,
    // we give it a small grace window and bail to homepage if it still
    // isn't ready — better to skip the splash than to hold on a blank
    // viewport waiting for bytes.
    const probe = new window.Image();
    probe.src = "/splash/morning-merida.jpg";

    const startSequence = () => {
      // Sequence completes naturally
      const completeTimer = window.setTimeout(() => {
        setSeenCookie();
        document.documentElement.classList.remove("splash-pending");
        setRender("done");
      }, TOTAL_DURATION_MS);

      let skipped = false;
      const skip = () => {
        if (skipped) return;
        skipped = true;
        window.clearTimeout(completeTimer);
        setSeenCookie();
        document.documentElement.classList.add("splash-skipping");
        setRender("skipping");
        window.setTimeout(() => {
          document.documentElement.classList.remove("splash-pending");
          document.documentElement.classList.remove("splash-skipping");
          setRender("done");
        }, SKIP_FADE_MS);
      };

      document.addEventListener("click", skip);
      document.addEventListener("keydown", skip);
      document.addEventListener("touchstart", skip, { passive: true });
      document.addEventListener("wheel", skip, { passive: true });

      cleanups.push(() => {
        window.clearTimeout(completeTimer);
        document.removeEventListener("click", skip);
        document.removeEventListener("keydown", skip);
        document.removeEventListener("touchstart", skip);
        document.removeEventListener("wheel", skip);
      });
    };

    const bailToHome = () => {
      setSeenCookie();
      document.documentElement.classList.remove("splash-pending");
      setRender("done");
    };

    const cleanups: Array<() => void> = [];

    if (probe.complete && probe.naturalWidth > 0) {
      // Image already cached — start immediately. CSS keyframes have
      // been running on the overlay since first render; this just
      // arms the timers and listeners.
      startSequence();
    } else {
      // Wait briefly for the preload to finish.
      let resolved = false;
      probe.addEventListener("load", () => {
        if (resolved) return;
        resolved = true;
        window.clearTimeout(graceTimer);
        startSequence();
      });
      const graceTimer = window.setTimeout(() => {
        if (resolved) return;
        resolved = true;
        bailToHome();
      }, IMAGE_LOAD_GRACE_MS);
      cleanups.push(() => window.clearTimeout(graceTimer));
    }

    return () => {
      for (const fn of cleanups) fn();
    };
  }, []);

  if (render === "done") return null;

  return (
    <div
      aria-hidden
      className="splash-overlay"
      data-render={render}
    >
      <div className="splash-image" />
      <div className="splash-wash" />
    </div>
  );
}
