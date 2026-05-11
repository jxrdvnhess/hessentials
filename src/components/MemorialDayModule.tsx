import Image from "next/image";
import Link from "next/link";

/**
 * Memorial Day featured moment — homepage second fold.
 *
 * Restored from the archived MothersDayModule "featured moment"
 * component pattern (image left, italic-serif headline right, body
 * framing copy, italic CTA). NOT the HomePracticeTeaser pillar-
 * article-preview pattern.
 *
 * Sits between the hero section and the first cinematic image
 * (merida-moment-1, "Some moments hold."). The image at the left
 * peeks below the hero at the fold and cues continuation as the
 * user finishes reading the H1.
 *
 * Layout: image left, text right on md+. The text column rhymes
 * with the AurelianThisWeekPanel typography on the hero so the
 * section reads as a sibling editorial moment. Mobile stacks image
 * on top, text below.
 *
 * Block copy (sentence case with periods per brief): the headline
 * incorporates "Memorial Day." so there is no separate eyebrow.
 *
 * Spacing: minimal top padding so the image acts as the hero's
 * fold cue; generous bottom padding so the module breathes before
 * the cinematic arc below.
 */
export default function MemorialDayModule() {
  return (
    <section
      aria-labelledby="memorial-day-headline"
      className="relative w-full pb-24 sm:pb-32 md:pb-40"
    >
      <div className="mx-auto w-full max-w-[1400px] px-6 sm:px-10 md:px-16">
        <div className="grid grid-cols-1 items-center gap-y-10 md:grid-cols-12 md:gap-x-12 lg:gap-x-16">
          {/* ---------- Image ----------
              Linked to the article. Group hover lets the image
              ease toward the same /70 register as the CTA so
              the whole card reads as one editorial surface. */}
          <Link
            href="/memorial-day"
            aria-label="Read the Memorial Day article"
            className="group block md:col-span-7"
          >
            <div className="relative aspect-[3/2] w-full overflow-hidden">
              <Image
                src="/memorial-day.jpg"
                alt=""
                fill
                sizes="(min-width: 768px) 58vw, 100vw"
                quality={92}
                priority
                className="object-cover transition-opacity duration-500 ease-out group-hover:opacity-90"
              />
            </div>
          </Link>

          {/* ---------- Text column ---------- */}
          <div className="md:col-span-5 md:pl-2 lg:pl-4">
            <h2
              id="memorial-day-headline"
              className="text-balance font-serif text-[clamp(1.875rem,3.4vw,2.625rem)] font-normal italic leading-[1.18] tracking-[-0.012em] text-[#2b1f17]"
            >
              <Link
                href="/memorial-day"
                className="transition-opacity duration-300 ease-out hover:opacity-70"
              >
                Memorial Day. Not the start of summer.
              </Link>
            </h2>

            <div
              aria-hidden
              className="mt-7 h-px w-7"
              style={{ backgroundColor: "rgba(31,29,27,0.4)" }}
            />

            <p className="mt-6 max-w-[28rem] text-[14px] leading-[1.6] text-[#1f1d1b]/70 sm:text-[14.5px]">
              The day the calendar catches up to what&rsquo;s already
              happening.
            </p>

            <Link
              href="/memorial-day"
              className="mt-8 inline-block font-serif text-[16px] italic text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-70"
            >
              Read the article&nbsp;&nbsp;&rarr;
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
