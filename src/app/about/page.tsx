import Image from "next/image";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "About — Hessentials",
  description: "An editorial home for choosing well.",
};

/**
 * About — magazine feature opener.
 *
 *   Hero image at the top in its native landscape proportion (the
 *   hacienda morning shot is 1537×1023 — cropping it into a portrait
 *   frame breaks the composition). Type B feature-frame treatment
 *   (rounded 20px) so it speaks the same vocabulary as the homepage.
 *
 *   Writing follows underneath in a narrow column: eyebrow, italic
 *   serif headline, then four paragraphs of body. Reads in fifteen
 *   seconds. Stops.
 *
 *   Page ends; standard SiteFooter takes the close (hacienda image +
 *   newsletter + legal). No in-page footer here — duplicating what
 *   the global footer already does is wasted effort.
 */
export default function AboutPage() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Hero image ---------- */}
      <section
        aria-hidden
        className="px-6 pt-12 sm:px-10 sm:pt-16 md:px-16 md:pt-20"
      >
        <figure className="mx-auto max-w-[1100px]">
          <div className="overflow-hidden rounded-[20px]">
            <Image
              src="/home/hacienda-03-morning.jpg"
              alt=""
              width={1537}
              height={1023}
              sizes="(min-width: 1180px) 1100px, (min-width: 768px) calc(100vw - 8rem), calc(100vw - 3rem)"
              quality={95}
              priority
              className="block h-auto w-full"
            />
          </div>
        </figure>
      </section>

      {/* ---------- Writing ---------- */}
      <section
        aria-label="Hessentials"
        className="mx-auto w-full max-w-[640px] px-6 pt-20 pb-32 sm:px-8 sm:pt-24 sm:pb-40 md:pt-28 md:pb-48"
      >
        <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px]">
          About
        </p>

        <h1 className="mt-8 font-serif text-[clamp(1.875rem,3.4vw,2.625rem)] font-normal italic leading-[1.2] tracking-[-0.012em] text-balance text-[#1f1d1b] sm:mt-10">
          An editorial home for choosing well.
        </h1>

        <div className="mt-12 max-w-[520px] font-serif text-[clamp(1.0625rem,1.4vw,1.1875rem)] font-normal leading-[1.6] text-[#1f1d1b]/85 sm:mt-14">
          <p>Modern life got loud. Most of it doesn&rsquo;t matter.</p>

          <p className="mt-6">
            Hessentials is for the small decisions that hold up &mdash; what
            to cook, what to keep, what to buy, what to ignore.
          </p>

          <p className="mt-6">
            Not trends. Not algorithms. Not a performance of taste.
          </p>

          <p className="mt-6">Only what proves itself.</p>
        </div>

        {/* Signature line — closes the About page with quiet authorship.
            The brand is editorial, not anonymous; the visitor should
            leave knowing one person stands behind the filter. */}
        <p className="mt-16 max-w-[520px] font-serif text-[clamp(0.9375rem,1.15vw,1.0625rem)] italic leading-[1.6] text-[#1f1d1b]/55 sm:mt-20">
          Run by Jordan Hess. Every piece passes the same test before it
          gets in.
        </p>
      </section>
    </main>
  );
}
