import type { Metadata } from "next";
import Wordmark from "../../components/Wordmark";

/**
 * /paused — the closed sign.
 *
 * While the site is paused (see src/middleware.ts) every route is
 * rewritten here, URL intact, so nothing breaks when the doors open
 * again.
 *
 * Type only. An illustration of a closed shop performs the closing;
 * the wordmark and one line state it. Wordmark, a short hairline, two
 * lines, and a great deal of nothing. No nav, no footer, no newsletter,
 * no way further in — a closed shop doesn't hand you a catalogue.
 *
 * The rule is a plain 52px hairline rather than the homepage's drawn
 * HandRule: the wobble is a warmth cue that belongs on a page with
 * content in it. Here it would be the only gesture on the page, and a
 * lone gesture reads as a statement.
 *
 * Chrome is suppressed the same way /curtain-test does it — SiteHeader
 * and FooterGate both bail on this pathname, and the gate additionally
 * stamps a header so rewritten routes drop it too.
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
    <main className="relative z-10 flex min-h-[100svh] flex-col items-center justify-center px-6 py-20 text-center text-[#1f1d1b]">
      {/* `large` is the documented entry-screen size. Don't override the
          width with a utility class — Wordmark owns it, and a second w-*
          utility of equal specificity wins or loses by CSS order, not by
          where it sits in the className string. */}
      <Wordmark size="large" priority />

      <div className="my-11 h-px w-[52px] bg-[#1f1d1b]/25 md:my-12" aria-hidden />

      <p className="font-serif text-[clamp(1.35rem,2.6vw,1.9rem)] italic leading-[1.3] text-[#2b1f17]">
        Closed for a short while.
      </p>
      <p className="mt-6 max-w-[25rem] text-[13.5px] leading-[1.8] text-[#1f1d1b]/55">
        The site is under renovation. It opens again when it&rsquo;s good.
      </p>
    </main>
  );
}
