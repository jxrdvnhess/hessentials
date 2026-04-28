import Image from "next/image";
import type { Metadata } from "next";
import AboutEssay from "../../components/AboutEssay";

export const metadata: Metadata = {
  title: "About — Hessentials",
  description: "An editorial home for choosing well.",
};

/**
 * About — full-bleed hero with overlay essay (per Master Update Brief §4).
 *
 *   Single image, single essay, single signature, footer. The brevity
 *   is the design.
 *
 *   Hero: merida_moment_5.jpg, full-bleed, 80–90vh desktop / 70vh
 *   mobile. Object-cover, focal point biased toward the right (table
 *   side) so the empty plaster wall on the left holds the essay.
 *
 *   Essay: italic serif throughout, ~18–22px desktop / 16px mobile,
 *   line-height 1.6–1.7, max column 480–540px desktop / 280–320px
 *   mobile. Cream #f1ece2 at 95%. Soft scrim under the column.
 *
 *   Signature: hand-drawn heart + JH initials SVG (Jordan provides).
 *   Sits ~32–48px below the closing line, 140px desktop / 110px mobile,
 *   inheriting the cream essay color via currentColor. Placeholder
 *   rendered until the SVG arrives.
 *
 *   Page ends; standard SiteFooter takes the close (merida_moment_6 +
 *   "This is what stayed." + newsletter + legal). No "h" motif here.
 *   No section header hairlines here. The brevity is the design.
 */
export default function AboutPage() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      {/* ---------- Hero image + essay overlay ----------
          Min-height: 70vh on mobile, ~85vh on desktop. Section grows
          taller if the essay column needs more vertical room (the
          essay is the gravity here — the image accommodates the text,
          not the other way around). Image focal point biased toward
          the right table area so the empty plaster wall on the left
          holds the essay column. */}
      <section
        aria-label="About Hessentials"
        className="relative w-full overflow-hidden"
      >
        {/* Image fills the section as a background; AboutEssay drives
            the section's height via its own min-h + py. */}
        <Image
          src="/about/merida-moment-5.jpg"
          alt=""
          fill
          sizes="100vw"
          quality={95}
          priority
          className="object-cover object-[72%_center] md:object-[68%_center]"
        />

        <AboutEssay />
      </section>
    </main>
  );
}
