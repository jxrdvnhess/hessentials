"use client";

import Image from "next/image";
import { useCallback, useEffect, useState } from "react";

/**
 * ProductGallery — restrained editorial carousel for shop detail pages.
 *
 * Renders the active image at full size, with hover-revealed prev/next arrows
 * and a quiet thumbnail row beneath. Arrows fade in when the cursor enters the
 * frame; on touch devices they sit at a lower opacity so the affordance is
 * still visible. Keyboard users can press ←/→ when the frame is focused.
 *
 * If only one image is supplied, the arrows, counter, and thumbnail row are
 * all suppressed and the component renders a single static frame.
 */
type Props = {
  images: string[];
  alt: string;
  /**
   * Brand-name fallback retained for backward compatibility with consumers
   * that still pass it. Currently unused inside the component — the cream
   * frame on its own communicates the loading state — but we keep the
   * prop so existing callers don't need to change.
   */
  fallback?: string;
};

export default function ProductGallery({ images, alt }: Props) {
  const [active, setActive] = useState(0);
  const safeImages = images.length > 0 ? images : [];
  const count = safeImages.length;

  // Reset index if the source list shrinks (e.g. during HMR while editing).
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (active >= count) setActive(0);
  }, [active, count]);

  const goPrev = useCallback(() => {
    setActive((i) => (i - 1 + count) % count);
  }, [count]);

  const goNext = useCallback(() => {
    setActive((i) => (i + 1) % count);
  }, [count]);

  if (count === 0) return null;

  const showControls = count > 1;

  // Tailwind classes shared by both arrow buttons. Arrows are invisible by
  // default and fade in when the cursor enters the frame (group-hover) or the
  // frame receives keyboard focus (focus-visible inside the group). On touch
  // devices that have no hover, they sit at a quieter resting opacity so the
  // affordance is still visible.
  const arrowBase =
    "absolute top-1/2 -translate-y-1/2 flex h-10 w-10 items-center justify-center rounded-full " +
    "bg-[#f8f6f3]/90 text-[#1f1d1b] backdrop-blur-sm " +
    "border border-[#1f1d1b]/10 shadow-[0_1px_3px_rgba(31,29,27,0.08)] " +
    "opacity-0 transition-opacity duration-300 ease-out " +
    "group-hover:opacity-100 group-focus-within:opacity-100 focus-visible:opacity-100 " +
    "hover:bg-[#f8f6f3] " +
    "[@media(hover:none)]:opacity-75 sm:h-11 sm:w-11";

  return (
    <div>
      {/* Main frame.
          Background is a soft warm white; product images render with
          `object-contain` so the entire product is always visible
          (no top/sides/bottom cropped off). When a source image's
          natural ratio doesn't match this 4/5 frame, the empty area
          becomes a quiet near-white field — blends with the white
          backgrounds most brands shoot on. */}
      <div
        className="group relative aspect-[4/5] w-full overflow-hidden bg-[#faf9f5] focus:outline-none"
        role={showControls ? "group" : undefined}
        aria-label={
          showControls
            ? `${alt} — image ${active + 1} of ${count}`
            : undefined
        }
        tabIndex={showControls ? 0 : undefined}
        onKeyDown={(e) => {
          if (!showControls) return;
          if (e.key === "ArrowLeft") {
            e.preventDefault();
            goPrev();
          } else if (e.key === "ArrowRight") {
            e.preventDefault();
            goNext();
          }
        }}
      >
        {safeImages.map((src, i) => (
          <Image
            key={src}
            src={src}
            alt={i === 0 ? alt : `${alt} — view ${i + 1}`}
            fill
            sizes="(min-width: 768px) 58vw, 100vw"
            quality={95}
            unoptimized
            priority={i === 0}
            className={`object-contain p-6 sm:p-8 transition-opacity duration-700 ease-out ${
              i === active ? "opacity-100" : "opacity-0"
            }`}
          />
        ))}

        {showControls && (
          <>
            <button
              type="button"
              onClick={goPrev}
              aria-label="Previous image"
              className={`${arrowBase} left-3 sm:left-4`}
            >
              <span aria-hidden className="text-[15px] leading-none">
                ←
              </span>
            </button>
            <button
              type="button"
              onClick={goNext}
              aria-label="Next image"
              className={`${arrowBase} right-3 sm:right-4`}
            >
              <span aria-hidden className="text-[15px] leading-none">
                →
              </span>
            </button>

            {/* Subtle position counter — reinforces that there is more to see. */}
            <div
              aria-hidden
              className="absolute bottom-3 right-3 rounded-full bg-[#f8f6f3]/85 px-3 py-[6px] text-[10px] tracking-[0.2em] text-[#1f1d1b]/65 backdrop-blur-sm border border-[#1f1d1b]/10 opacity-0 transition-opacity duration-300 ease-out group-hover:opacity-100 group-focus-within:opacity-100 [@media(hover:none)]:opacity-80 sm:bottom-4 sm:right-4"
            >
              {String(active + 1).padStart(2, "0")} / {String(count).padStart(2, "0")}
            </div>
          </>
        )}
      </div>

      {/* Thumbnail row.
          Same near-white frame + object-contain as the main view, so
          a thumbnail is a faithful preview of what the main frame
          will show — never a different crop. */}
      {showControls && (
        <div className="mt-5 flex flex-wrap gap-3 sm:mt-6 sm:gap-4">
          {safeImages.map((src, i) => {
            const isActive = i === active;
            return (
              <button
                key={src}
                type="button"
                onClick={() => setActive(i)}
                aria-label={`Show image ${i + 1} of ${count}`}
                aria-current={isActive ? "true" : undefined}
                className="group relative aspect-[4/5] w-16 shrink-0 overflow-hidden bg-[#faf9f5] sm:w-20"
              >
                <Image
                  src={src}
                  alt=""
                  fill
                  sizes="80px"
                  quality={75}
                  unoptimized
                  className={`object-contain p-1.5 transition-opacity duration-500 ease-out ${
                    isActive
                      ? "opacity-100"
                      : "opacity-55 group-hover:opacity-85 group-focus-visible:opacity-85"
                  }`}
                />
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
