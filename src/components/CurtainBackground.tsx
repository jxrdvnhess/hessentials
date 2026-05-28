"use client";

/**
 * CurtainBackground — atmospheric curtain video, fixed behind content.
 *
 * Falsifiable test for whether a fixed-position curtain video can serve
 * as Hessentials' homepage atmosphere without violating the brand
 * doctrine — ignorable, non-spectacular, peripheral. Lives at
 * /curtain-test; not wired into production.
 *
 * SEAM HANDLING
 *
 *   Source is a 16.12s loop (the original 8.08s clip re-encoded at
 *   half speed via setpts=2*PTS for a more languid character — the
 *   first round at native speed felt rushed). A naive single-video
 *   loop produces a visible snap at every restart. The fix here is
 *   two stacked video elements, both playing continuously, offset by
 *   half the source length. When the visible video approaches its
 *   seam (last ~0.95s), a CSS opacity transition hands visibility to
 *   the other video, which is at the middle of its own playback. The
 *   loop happens invisibly. Swap repeats every ~8s.
 *
 * MOBILE + REDUCED-MOTION
 *
 *   Below the md breakpoint (~767px) and for prefers-reduced-motion:
 *   reduce, the video is replaced with the still poster image — same
 *   atmosphere, no playback. Avoids iOS dynamic-viewport jitter on
 *   position:fixed video and the battery cost of continuous decode.
 *
 * TUNABLE VARIABLES
 *
 *   All knobs at the top of the file. Jordan adjusts these during the
 *   live-with-it phase without a code round-trip.
 */

import { useEffect, useRef, useState } from "react";

// ────────────────────────────────────────────────────────────────────
//  TUNABLES — adjust freely
// ────────────────────────────────────────────────────────────────────

/** Flat color layered between the video and the content. Defaults to
 *  the brand cream so the test reads chromatically consistent with
 *  the live site. */
const OVERLAY_TINT = "#f8f6f3";

/** How opaque the overlay tint is, 0–1. Higher = more cream over the
 *  video. Starting point per brief: 0.60. */
const OVERLAY_OPACITY = 0.6;

/** Soften the video itself before the tint is applied. 1 = full
 *  saturation; lower lifts the whole video toward cream. */
const VIDEO_OPACITY = 1.0;

/** How long the opacity crossfade between the two video elements
 *  takes, in milliseconds. 600–1000ms feels natural; shorter feels
 *  abrupt, longer makes the rhythm of crossfades more visible. */
const CROSSFADE_DURATION_MS = 800;

/** Where the second video starts playing relative to the first, in
 *  seconds. With a 16.12s source, half-offset (~8s) gives evenly-
 *  spaced crossfades. */
const B_OFFSET_SECONDS = 8.06;

// ────────────────────────────────────────────────────────────────────
//  Source constants (matched to the encoded asset; do not tune)
// ────────────────────────────────────────────────────────────────────

const VIDEO_PATH = "/curtain/curtain.mp4";
const POSTER_PATH = "/curtain/curtain-poster.jpg";

/** Source clip length in seconds. Matches the encoded file's duration. */
const VIDEO_LENGTH_SECONDS = 16.12;

/** How early before the seam to begin the crossfade. The crossfade
 *  should END at the seam, so it begins (CROSSFADE_DURATION + small
 *  buffer) before. */
const SEAM_TRIGGER_OFFSET_SECONDS =
  CROSSFADE_DURATION_MS / 1000 + 0.15;

export default function CurtainBackground() {
  const videoARef = useRef<HTMLVideoElement | null>(null);
  const videoBRef = useRef<HTMLVideoElement | null>(null);

  // Which video is currently the primary (visible) layer. Crossfade
  // happens when this swaps; React state change drives the CSS
  // opacity transition on both elements.
  const [primary, setPrimary] = useState<"a" | "b">("a");

  // Mirror primary into a ref so the timeupdate handlers (created
  // once at mount) read the current value without stale-closure bugs.
  const primaryRef = useRef<"a" | "b">("a");
  primaryRef.current = primary;

  // Guard against multiple state updates during a single crossover.
  // timeupdate fires ~4x/sec; without this guard we'd trigger
  // setPrimary multiple times for every seam.
  const transitioningRef = useRef(false);

  // Mode determines whether we render the video pair or the still
  // poster. SSR-safe default: 'video'; useEffect downgrades to
  // 'still' on mobile or reduced-motion users.
  const [mode, setMode] = useState<"video" | "still">("video");

  useEffect(() => {
    if (typeof window === "undefined") return;
    const isMobile = window.matchMedia("(max-width: 767px)").matches;
    const reduceMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;
    if (isMobile || reduceMotion) {
      setMode("still");
    }
  }, []);

  // Set Video B's start offset once both elements are loaded. Without
  // this the two videos would play in unison and the crossfade would
  // do nothing.
  useEffect(() => {
    if (mode !== "video") return;
    const b = videoBRef.current;
    if (!b) return;
    const handleLoaded = () => {
      try {
        b.currentTime = B_OFFSET_SECONDS;
      } catch {
        // Some browsers throw if currentTime is set before metadata
        // is fully ready; the loadedmetadata handler catches the
        // retry path. Safe to swallow.
      }
    };
    if (b.readyState >= 1) {
      handleLoaded();
    } else {
      b.addEventListener("loadedmetadata", handleLoaded, { once: true });
      return () => b.removeEventListener("loadedmetadata", handleLoaded);
    }
  }, [mode]);

  // Check whether the currently-primary video is approaching its
  // seam. If so, swap primary, which triggers the CSS crossfade.
  const checkSeam = (which: "a" | "b") =>
    (e: React.SyntheticEvent<HTMLVideoElement>) => {
      if (which !== primaryRef.current) return;
      if (transitioningRef.current) return;
      const video = e.currentTarget;
      if (
        video.currentTime >=
        VIDEO_LENGTH_SECONDS - SEAM_TRIGGER_OFFSET_SECONDS
      ) {
        transitioningRef.current = true;
        setPrimary(which === "a" ? "b" : "a");
        // Re-allow swaps once we're clear of the seam zone, plus a
        // small safety margin.
        window.setTimeout(() => {
          transitioningRef.current = false;
        }, CROSSFADE_DURATION_MS + 400);
      }
    };

  return (
    <div
      aria-hidden
      className="pointer-events-none fixed inset-0 -z-0 overflow-hidden"
      // -z-0 keeps it behind content (which sits at z-10 in the test
      // page). pointer-events-none so the user never clicks the
      // background by accident.
    >
      {mode === "video" && (
        <>
          <video
            ref={videoARef}
            src={VIDEO_PATH}
            poster={POSTER_PATH}
            autoPlay
            muted
            loop
            playsInline
            preload="auto"
            onTimeUpdate={checkSeam("a")}
            className="absolute inset-0 h-full w-full object-cover"
            style={{
              opacity: primary === "a" ? VIDEO_OPACITY : 0,
              transition: `opacity ${CROSSFADE_DURATION_MS}ms ease-in-out`,
            }}
          />
          <video
            ref={videoBRef}
            src={VIDEO_PATH}
            poster={POSTER_PATH}
            autoPlay
            muted
            loop
            playsInline
            preload="auto"
            onTimeUpdate={checkSeam("b")}
            className="absolute inset-0 h-full w-full object-cover"
            style={{
              opacity: primary === "b" ? VIDEO_OPACITY : 0,
              transition: `opacity ${CROSSFADE_DURATION_MS}ms ease-in-out`,
            }}
          />
        </>
      )}

      {mode === "still" && (
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `url(${POSTER_PATH})`,
            backgroundSize: "cover",
            backgroundPosition: "center",
            opacity: VIDEO_OPACITY,
          }}
        />
      )}

      {/* Overlay tint between background and content */}
      <div
        className="absolute inset-0"
        style={{
          backgroundColor: OVERLAY_TINT,
          opacity: OVERLAY_OPACITY,
        }}
      />
    </div>
  );
}
