import type { Metadata } from "next";
import CurtainBackground from "../../components/CurtainBackground";

/**
 * /curtain-test — atmospheric prototype test.
 *
 * A falsifiable test of whether a fixed-position curtain video, sitting
 * behind editorial text, can serve as Hessentials' homepage atmosphere
 * without violating the brand doctrine (ignorable, non-spectacular,
 * peripheral). The live homepage is untouched. Jordan lives with this
 * under real conditions before deciding whether to spec it into the
 * production homepage.
 *
 * Intentionally bare: no nav, no header, no footer, no editorial
 * modules. Just the curtain, the overlay tint, and the type. The
 * minimum surface needed to evaluate the experience.
 *
 * Editorial text is the opening of "11:11 is a real practice" from
 * content/practice/. Real Hessentials copy, brand serif at the
 * .prose-editorial scale (18px / 1.75) used elsewhere on the site.
 */

export const metadata: Metadata = {
  title: "Curtain test — Hessentials",
  description: "Internal test route for curtain-atmosphere prototype.",
  robots: { index: false, follow: false },
};

export default function CurtainTestPage() {
  return (
    <>
      <CurtainBackground />
      <main className="relative z-10 min-h-screen text-[#1f1d1b]">
        <div className="mx-auto flex min-h-screen max-w-[640px] flex-col justify-center px-6 py-20 sm:px-10 md:px-12">
          <article className="prose-editorial">
            <p>
              If you&rsquo;ve spent any time on the internet, you&rsquo;ve seen the
              claim: 11:11 is a sign from the universe, a moment of
              synchronicity, a cosmic wink that you should make a wish
              or take it as confirmation that you&rsquo;re &ldquo;on the right
              path.&rdquo;
            </p>
            <p>
              That isn&rsquo;t what&rsquo;s happening, and the framing does more
              harm than good. It teaches people to wait for an outside
              signal before they act on what they already know.
            </p>
            <p>But there&rsquo;s something real underneath it.</p>
          </article>
        </div>
      </main>
    </>
  );
}
