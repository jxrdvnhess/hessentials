import Image from "next/image";
import Link from "next/link";

/**
 * "Half revealed." featured moment — homepage second fold.
 *
 * Midyear Practice piece. Restored from the MemorialDayModule
 * "featured moment" pattern (image left, italic-serif headline right,
 * framing copy, italic CTA). NOT the HomePracticeTeaser pillar-
 * article-preview pattern.
 *
 * Replaces the Memorial Day featured moment in the same slot, same
 * component, same typographic register. Only the copy, the image,
 * and the linked article change.
 *
 * No eyebrow (matching how the Memorial Day block ran). The headline
 * carries the moment alone.
 *
 * GATED: this module is built and ready but is intentionally not yet
 * wired into src/app/page.tsx. Per the publish brief the block must
 * not go live with a placeholder image; it stays out of the homepage
 * until /public/half-revealed.jpg lands. See the reinstatement comment
 * in page.tsx.
 *
 * Image: a made painting (dusk interior, no figures, visible
 * brushwork) per image-brief-half-revealed.md — not a captured photo.
 */
export default function HalfRevealedModule() {
  return (
    <section
      aria-labelledby="half-revealed-headline"
      className="relative w-full pb-24 sm:pb-32 md:pb-40"
    >
      <div className="mx-auto w-full max-w-[1400px] px-6 sm:px-10 md:px-16">
        <div className="grid grid-cols-1 items-center gap-y-10 md:grid-cols-12 md:gap-x-12 lg:gap-x-16">
          {/* ---------- Image ----------
              Linked to the article. Group hover lets the image
              ease toward the same /70 register as the CTA so
              the whole card reads as one editorial surface. */}
          <Link
            href="/half-revealed"
            aria-label="Read the Half revealed. article"
            className="group block md:col-span-7"
          >
            <div className="relative aspect-[3/2] w-full overflow-hidden">
              <Image
                src="/half-revealed.jpg"
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
              id="half-revealed-headline"
              className="text-balance font-serif text-[clamp(1.875rem,3.4vw,2.625rem)] font-normal italic leading-[1.18] tracking-[-0.012em] text-[#2b1f17]"
            >
              <Link
                href="/half-revealed"
                className="transition-opacity duration-300 ease-out hover:opacity-70"
              >
                Half revealed.
              </Link>
            </h2>

            <div
              aria-hidden
              className="mt-7 h-px w-7"
              style={{ backgroundColor: "rgba(31,29,27,0.4)" }}
            />

            <p className="mt-6 max-w-[28rem] text-[14px] leading-[1.6] text-[#1f1d1b]/70 sm:text-[14.5px]">
              In January we are designing a house. In June we are
              discovering which rooms we actually live in.
            </p>

            <Link
              href="/half-revealed"
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
