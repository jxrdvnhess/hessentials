import Image from "next/image";
import Link from "next/link";

/**
 * Mother's Day editorial module — homepage second fold.
 *
 * Sits directly below the hero. The hero's bottom edge bleeds into
 * this module's image, so the user sees the table photograph cueing
 * continuation as they finish reading the H1.
 *
 * Layout: image left, text right on md+. The text column rhymes with
 * the AurelianThisWeekPanel typography (eyebrow → italic-serif
 * headline → body framing copy → italic "Read this week →"-style link)
 * so the section reads as a sibling editorial moment, not a different
 * design language. Mobile stacks image on top, text below.
 *
 * Spacing: minimal top padding so the image acts as the hero's fold
 * cue; generous bottom padding so the module breathes before the
 * "Some moments hold." photograph below.
 */
export default function MothersDayModule() {
  return (
    <section
      aria-labelledby="mothers-day-headline"
      className="relative w-full pb-24 sm:pb-32 md:pb-40"
    >
      <div className="mx-auto w-full max-w-[1400px] px-6 sm:px-10 md:px-16">
        <div className="grid grid-cols-1 items-center gap-y-10 md:grid-cols-12 md:gap-x-12 lg:gap-x-16">
          {/* ---------- Image ----------
              Linked to the guide. Group hover lets the image
              ease toward the same /70 register as the CTA so
              the whole card reads as one editorial surface. */}
          <Link
            href="/mothers-day"
            aria-label="Read the Mother's Day guide"
            className="group block md:col-span-7"
          >
            <div className="relative aspect-[3/2] w-full overflow-hidden">
              <Image
                src="/mothers-day-table.jpg"
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
            <p className="text-[11px] uppercase leading-[1.5] tracking-[0.28em] text-[#1f1d1b]/55">
              Mother&rsquo;s Day
            </p>

            <h2
              id="mothers-day-headline"
              className="text-balance mt-6 font-serif text-[clamp(1.875rem,3.4vw,2.625rem)] font-normal italic leading-[1.18] tracking-[-0.012em] text-[#2b1f17]"
            >
              <Link
                href="/mothers-day"
                className="transition-opacity duration-300 ease-out hover:opacity-70"
              >
                Not a gift guide. A better way to get it right.
              </Link>
            </h2>

            <div
              aria-hidden
              className="mt-7 h-px w-7"
              style={{ backgroundColor: "rgba(31,29,27,0.4)" }}
            />

            <p className="mt-6 max-w-[28rem] text-[14px] leading-[1.6] text-[#1f1d1b]/70 sm:text-[14.5px]">
              Most Mother&rsquo;s Day plans swing between overdone and
              forgettable. This is the third option.
            </p>

            <Link
              href="/mothers-day"
              className="mt-8 inline-block font-serif text-[16px] italic text-[#1f1d1b] transition-opacity duration-300 ease-out hover:opacity-70"
            >
              Read the guide&nbsp;&nbsp;&rarr;
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
