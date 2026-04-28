import Symbol from "./Symbol";

type SectionDividerProps = {
  /**
   * Vertical spacing band. "default" is for normal section transitions
   * (~32–48px above and below). "tight" reduces the breath when the
   * adjacent sections are already generously spaced.
   */
  spacing?: "default" | "tight";
};

/**
 * Quiet "h" motif at section transitions across the site (per §2.1 of
 * the 2026-04-28 design refinement brief).
 *
 * Renders the existing Hessentials Symbol at xs (~16px) with reduced
 * opacity so the dark mark reads as a tonal-cream tint against the
 * plaster background — present but not announced. Centered horizontally,
 * with breath above and below so it reads as architectural punctuation,
 * not a glyph dropped into the body.
 *
 * Where to use:
 *   - Pillar pages: between tagline+dek block and "Start Here";
 *     between "Start Here" and "More" / "The Rest"
 *   - Aurelian: between hero and "This Week"
 *   - About: between hero photo and manifesto body
 *
 * Where NOT to use:
 *   - Inside the home image arc (images are self-bridging)
 *   - Within section bodies
 *   - Inside cards or grids
 */
export default function SectionDivider({
  spacing = "default",
}: SectionDividerProps) {
  const padding =
    spacing === "tight"
      ? "py-6 sm:py-7"
      : "py-10 sm:py-12";

  return (
    <div
      aria-hidden
      className={`flex w-full justify-center ${padding}`}
    >
      <span className="opacity-25">
        <Symbol size="xs" />
      </span>
    </div>
  );
}
