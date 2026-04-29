type Author = "Jordan" | "Aurelian";

type BylineProps = {
  /**
   * The author signing the piece. Defaults to Jordan if unset, per
   * the brief: pieces written or refined by Jordan get BY JORDAN HESS;
   * pieces written by Aurelian (the editorial intelligence) get
   * BY AURELIAN. Accepts loose strings so existing content fields
   * (e.g. "By Jordan Hess", "J.D.H.") fall through to the default
   * without per-piece migration.
   */
  author?: Author | string;
};

/**
 * Byline — the closing signature on every editorial piece.
 *
 * Bottom-of-article placement, eyebrow typography, no date, no role,
 * no descriptor, no link. Visual rhyme with the existing eyebrow
 * marks across the site (MOTHER'S DAY, AURELIAN · THIS WEEK,
 * HESSENTIALS) — same font, small caps, letter-spacing, muted ink.
 *
 * The byline doesn't perform; it commits.
 */
export default function Byline({ author }: BylineProps) {
  const name = author === "Aurelian" ? "AURELIAN" : "JORDAN HESS";

  return (
    <p
      className="mt-12 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]"
      aria-label={`Author: ${name}`}
    >
      By {name}
    </p>
  );
}
