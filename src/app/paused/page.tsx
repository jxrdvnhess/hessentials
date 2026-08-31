import type { Metadata } from "next";
import Wordmark from "../../components/Wordmark";
import UnderRenovation from "../../components/UnderRenovation";

/**
 * /paused — the closed-storefront sign.
 *
 * While the site is paused (see src/middleware.ts) every route is
 * rewritten here, URL intact, so nothing breaks when the doors open
 * again. This is the sign taped to the inside of the glass: wordmark,
 * the approved hand-drawn renovation scene, two lines of type. No nav,
 * no footer, no newsletter, no way further in. A closed shop doesn't
 * hand you a catalogue.
 *
 * The illustration already says "sorry for the mess. under renovation."
 * so the type underneath states the fact and stops. Chrome is suppressed
 * the same way /curtain-test does it — SiteHeader and FooterGate both
 * bail on this pathname.
 *
 * noindex/nofollow: this is a temporary state, and the real pages should
 * keep their own indexing history rather than have Google recrawl the
 * whole site as one placeholder.
 */

export const metadata: Metadata = {
  title: "Hessentials",
  description: "Closed for a short while.",
  robots: { index: false, follow: false },
  alternates: { canonical: "/" },
};

export default function PausedPage() {
  return (
    <main className="relative z-10 flex min-h-[100svh] flex-col items-center justify-center px-6 py-16 text-[#1f1d1b]">
      <Wordmark size="large" priority className="mb-10 md:mb-14" />

      <UnderRenovation />

      <div className="mt-10 max-w-[34rem] text-center md:mt-14">
        <p className="font-serif text-[clamp(1.25rem,2.4vw,1.6rem)] italic leading-[1.35] text-[#2b1f17]">
          Closed for a short while.
        </p>
        <p className="mx-auto mt-5 max-w-[26rem] text-[14px] leading-[1.7] text-[#1f1d1b]/60">
          The whole thing is being rebuilt. It opens again when it&rsquo;s good.
        </p>
      </div>
    </main>
  );
}
