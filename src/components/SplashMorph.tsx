"use client";

import { useEffect, useState } from "react";

const COOKIE_NAME = "hessentials_splash_seen";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 30; // 30 days
const TOTAL_DURATION_MS = 2950;
const SKIP_FADE_MS = 200;

function setSeenCookie() {
  document.cookie = `${COOKIE_NAME}=1; max-age=${COOKIE_MAX_AGE}; path=/; samesite=lax`;
}

/**
 * Splash morph — first-visit arrival sequence on /home.
 *
 * Four movements, total runtime ~3 seconds:
 *   1. Hold (1500ms)         — full-bleed splash image, nothing else
 *   2. Mask reveal (200ms)   — image dims to "visible only inside the
 *                              wordmark letterforms" at full-screen scale
 *   3. Scale + translate     — masked wordmark animates from full-screen
 *      (900ms)                 to its masthead landing position; the
 *                              homepage underneath fades in alongside
 *   4. Color settle (350ms)  — image-in-letters crossfades to the brand's
 *                              warm-near-black wordmark color
 *
 * Keyed CSS animations carry the actual motion (see globals.css). This
 * component is the small state machine that:
 *   - decides whether to play (cookie + prefers-reduced-motion)
 *   - mounts the overlay markup for keyframe animations to bind to
 *   - listens for skip input (click / key / touch / wheel)
 *   - sets the cookie on completion or skip
 *   - tears down once the sequence ends
 *
 * Suppression of the masthead during the morph happens via a server-rendered
 * `splash-pending` class on documentElement (see /home/page.tsx for the
 * server-side cookie check + inline script that sets the class before paint).
 * That class triggers the page-fade-in keyframe for header + main; this
 * component runs the overlay's own keyframes on the same 2950ms timeline.
 */
export default function SplashMorph() {
  // Render strategy:
  //   render = "running"  — splash overlay visible, animation playing
  //   render = "skipping" — overlay fading out (200ms), page fading in
  //   render = "done"     — return null; class also removed from document
  const [render, setRender] = useState<"running" | "skipping" | "done">(
    "running"
  );

  useEffect(() => {
    const reduce = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    if (reduce) {
      // No animation. Set cookie, drop the splash class, unmount.
      setSeenCookie();
      document.documentElement.classList.remove("splash-pending");
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setRender("done");
      return;
    }

    // Sequence completes naturally
    const completeTimer = window.setTimeout(() => {
      setSeenCookie();
      document.documentElement.classList.remove("splash-pending");
      setRender("done");
    }, TOTAL_DURATION_MS);

    // Skip on any user input
    let skipped = false;
    const skip = () => {
      if (skipped) return;
      skipped = true;
      window.clearTimeout(completeTimer);
      setSeenCookie();

      // Add the skipping class so the page fades to opacity 1 over
      // SKIP_FADE_MS (handled by CSS).
      document.documentElement.classList.add("splash-skipping");
      // Drive the overlay's own fade-out via state (CSS targets
      // .splash-overlay[data-render="skipping"]).
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

    return () => {
      window.clearTimeout(completeTimer);
      document.removeEventListener("click", skip);
      document.removeEventListener("keydown", skip);
      document.removeEventListener("touchstart", skip);
      document.removeEventListener("wheel", skip);
    };
  }, []);

  if (render === "done") return null;

  // The overlay is the actor. All four movements are CSS keyframe
  // animations bound to .splash-overlay and its children. Layers:
  //   .splash-fullbleed         — Movement 1 image, fades out in Movement 2
  //   .splash-wordmark--image   — image revealed through wordmark mask;
  //                               opacity-on in Movement 2, scale/translate
  //                               in Movement 3, opacity-off in Movement 4
  //   .splash-wordmark--color   — solid brand color through same mask;
  //                               opacity-on in Movement 4 (the crossfade)
  return (
    <div
      aria-hidden
      className="splash-overlay"
      data-render={render}
    >
      <div className="splash-fullbleed" />
      <div className="splash-wordmark splash-wordmark--image" />
      <div className="splash-wordmark splash-wordmark--color" />
    </div>
  );
}
