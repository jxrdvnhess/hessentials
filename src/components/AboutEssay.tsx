"use client";

import { useEffect, useRef, useState } from "react";

/**
 * About — personal essay overlay (Master Update Brief §4.3–4.8).
 *
 * Sits on top of merida_moment_5.jpg. Italic serif throughout, cream
 * #f1ece2 at 95% opacity, with a soft full-column scrim beneath for
 * consistent legibility across the long text. Single fade-in as the
 * image enters the viewport — the whole essay arrives as one block.
 *
 * Signature placeholder renders until Jordan's SVG (heart + JH
 * initials) arrives — see <SignaturePlaceholder /> below for swap point.
 */
export default function AboutEssay() {
  const ref = useRef<HTMLDivElement | null>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;

    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setVisible(true);
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        for (const entry of entries) {
          if (entry.isIntersecting) {
            setVisible(true);
            observer.disconnect();
            break;
          }
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className="relative flex min-h-[70vh] w-full items-center py-20 sm:py-24 md:min-h-[85vh] md:py-28"
      style={{
        opacity: visible ? 1 : 0,
        transitionProperty: "opacity",
        transitionDuration: "700ms",
        transitionTimingFunction: "cubic-bezier(0.22, 1, 0.36, 1)",
      }}
    >
      {/* Column wrapper — sits in the left half on desktop, centered on
          mobile (image's empty wall is on the left at all sizes). */}
      <div className="relative w-full px-6 sm:px-10 md:pl-[6vw] md:pr-0">
        <div className="relative mx-auto w-full max-w-[320px] sm:max-w-[420px] md:mx-0 md:max-w-[520px]">
          {/* Soft scrim under the column — radial fade so it darkens the
              text zone without reading as a discrete block. ~30% peak,
              fading to transparent at the edges. */}
          <div
            aria-hidden
            className="pointer-events-none absolute -inset-x-12 -inset-y-10 sm:-inset-x-16 md:-inset-x-20 md:-inset-y-14"
            style={{
              backgroundImage:
                "radial-gradient(ellipse 65% 75% at 50% 50%, rgba(20,18,16,0.42) 0%, rgba(20,18,16,0.32) 45%, transparent 90%)",
            }}
          />

          {/* Essay body. */}
          <div
            className="relative font-serif italic text-[16px] leading-[1.65] sm:text-[18px] md:text-[20px] md:leading-[1.7]"
            style={{ color: "#f1ece2", opacity: 0.95 }}
          >
            <p>
              For as long as I can remember, the people in my life have
              asked me what I think.
            </p>

            <p className="mt-5">
              What to wear to the thing. How to set the table. Which
              flowers for the dinner. What pot to buy. What to cook
              when nothing in the fridge looks like dinner. Whether the
              apartment is worth it. Whether the wedding gift is too
              much or not enough.
            </p>

            <p className="mt-5">
              I don&rsquo;t think this is unusual. Most people have
              someone they call. I&rsquo;m the person a lot of people
              call.
            </p>

            <p className="mt-5">
              It isn&rsquo;t trained or formal. I have an eye for
              what&rsquo;s right, and I trust it. The work is in the
              discernment &mdash; knowing what holds up and what
              doesn&rsquo;t, when something is technically fine but
              energetically off, what&rsquo;s the real version of a
              thing and what&rsquo;s the performance of one.
            </p>

            <p className="mt-5">
              My instinct is to refine. To look at something and see
              what&rsquo;s slightly off, then make the small adjustments
              that move it from fine to right. That&rsquo;s what I do
              with everything &mdash; meals, rooms, sentences, plans.
              Hessentials is what happens when that instinct gets
              pointed at the entire small-decisions catalog of a life.
            </p>

            <p className="mt-5">
              It&rsquo;s the formalization of something that was already
              happening.
            </p>

            <p className="mt-5">
              Most editorial brands lean on personality or trends or
              aesthetic moods. I wanted to build one that leaned on
              discernment itself.
            </p>

            <p className="mt-5">So this is Hessentials.</p>

            <p className="mt-5">
              A curated editorial home for choosing well. Food, home,
              style, practice. The small decisions that hold up &mdash;
              what to cook, what to keep, what to buy, what to ignore.
              Not trends. Not algorithms. Not a performance of taste.
              Only what proves itself.
            </p>

            <p className="mt-5">
              Every piece passes one test before it gets in: does it
              refuse a false binary and occupy a third stance with
              standards. If it does, it stays. If it doesn&rsquo;t, it
              doesn&rsquo;t.
            </p>

            <p className="mt-5">That&rsquo;s all of it.</p>

            {/* Signature — placeholder until Jordan's SVG arrives.
                Inherits cream via currentColor; ~140px wide desktop /
                110px mobile; aligned left with the essay column. */}
            <div
              aria-label="Signature"
              className="mt-10 sm:mt-12"
              style={{ color: "#f1ece2", opacity: 0.95 }}
            >
              <SignaturePlaceholder />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

/**
 * SIGNATURE — placeholder.
 *
 * Final asset is a hand-drawn SVG from Jordan: a heart on the left,
 * JH initials on the right (half-print/half-cursive), separated by
 * ~8–12px. Black/near-black ink on transparent background, drawn at
 * roughly 120–160px wide.
 *
 * To swap: drop the SVG into /public/about/signature.svg and replace
 * the placeholder below with:
 *
 *   <Image
 *     src="/about/signature.svg"
 *     alt="Jordan Hess"
 *     width={140}
 *     height={48}
 *     className="block w-[110px] sm:w-[140px] [filter:invert(1)_brightness(1.5)]"
 *   />
 *
 * (Or use `<object data="/about/signature.svg" />` so currentColor
 * works if the SVG uses `fill="currentColor"`.)
 *
 * The placeholder below holds the layout slot at the spec'd dimensions
 * so the page composes correctly until the asset lands.
 */
function SignaturePlaceholder() {
  return (
    <div
      className="flex items-end gap-3"
      style={{ height: "48px", width: "140px" }}
    >
      {/* Heart — placeholder outline. */}
      <svg
        viewBox="0 0 32 32"
        fill="none"
        stroke="currentColor"
        strokeWidth="1.6"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="h-7 w-7 shrink-0"
        aria-hidden
      >
        <path d="M16 27 C 7 21, 4 14, 8 9 C 11 5, 15 7, 16 11 C 17 7, 21 5, 24 9 C 28 14, 25 21, 16 27 Z" />
      </svg>
      {/* JH initials — placeholder hand-style. */}
      <span
        className="font-serif italic"
        style={{ fontSize: "30px", lineHeight: 1, letterSpacing: "-0.02em" }}
      >
        JH
      </span>
    </div>
  );
}
