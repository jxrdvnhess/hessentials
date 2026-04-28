import Image from "next/image";
import type { Metadata } from "next";
import SectionDivider from "../../components/SectionDivider";

export const metadata: Metadata = {
  title: "About — Hessentials",
  description: "An editorial home for choosing well.",
};

/**
 * About — magazine feature opener.
 *
 *   Hero image at the top, sized to support the manifesto rather than
 *   lead it (per §2.5). The brand position is *the standard, not the
 *   personality* — capping the image's max-width brings it down to
 *   ~50–55% viewport height on most desktops while preserving the
 *   landscape composition (no crop). Type B feature-frame treatment
 *   (rounded 20px) is preserved so it still speaks the homepage's
 *   visual vocabulary.
 *
 *   Writing follows underneath in a narrow column: eyebrow, italic
 *   serif headline, then four paragraphs of body. Reads in fifteen
 *   seconds. Stops.
 *
 *   Page ends; standard SiteFooter takes the close (hacienda image +
 *   newsletter + legal). No in-page footer here — duplicating what
 *   the global footer already does is wasted effort.
 *
 *   Note: §2.5 of the design refinement brief offered two options for
 *   reducing the hero photo's prominence — (A) reduce size, or (B)
 *   move to a side anchor. Option A is implemented here as the more
 *   restrained move. If Option B reads better in production, the
 *   change is small and isolated to this file.
 */
export default function AboutPage() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Hero image — reduced (§2.5 option A) ---------- */}
      <section
        aria-hidden
        className="px-6 pt-12 sm:px-10 sm:pt-16 md:px-16 md:pt-20"
      >
        <figure className="mx-auto max-w-[720px]">
          <div className="overflow-hidden rounded-[20px]">
            <Image
              src="/home/hacienda-03-morning.jpg"
              alt=""
              width={1537}
              height={1023}
              sizes="(min-width: 800px) 720px, (min-width: 768px) calc(100vw - 8rem), calc(100vw - 3rem)"
              quality={95}
              priority
              className="block h-auto w-full"
            />
          </div>
        </figure>
      </section>

      {/* "h" motif transitioning from hero photo to manifesto (§2.1). */}
      <SectionDivider />

      {/* ---------- Writing ---------- */}
      <section
        aria-label="Hessentials"
        className="mx-auto w-full max-w-[640px] px-6 pb-32 sm:px-8 sm:pb-40 md:pb-48"
      >
        {/* Hairline above the page eyebrow (§2.2). */}
        <span
          aria-hidden
          className="block w-20"
          style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
        />
        <p className="mt-6 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px]">
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
