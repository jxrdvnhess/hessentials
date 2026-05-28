/**
 * HomepageWallpaper — full storm-clearing-calm arc, content-sized.
 *
 * Sectioned CSS only, per the wallpaper spec: no parallax, no scroll
 * listeners, no Next/Image. CSS background-image is simpler for tiling
 * and avoids reintroducing the scroll-driven JS path flagged in the
 * brand-voice memory (broke analytics in a prior incident).
 *
 * SIZING (revised 2026-05-27 after first in-context review)
 *
 *   The wallpaper container is `position: absolute; inset: 0` — it
 *   stretches to fill its parent (typically <main>), whose height is
 *   driven by content. Zones are percentages of that height:
 *
 *     storm 50% / clearing 15% / calm 35%    (Addendum B)
 *
 *   The earlier fixed-vh implementation broke this: a fixed 800vh of
 *   wallpaper against ~500vh of test content meant the user never
 *   scrolled past storm; the 50/15/35 ratio was in the markup but never
 *   experienced. Percentage zones map the ratio to whatever the actual
 *   content scroll length is.
 *
 * STORM ZONE
 *
 *   Storm uses three locked tile variants (storm-a, storm-b, storm-c)
 *   plus a repeat (a-b-c-a) for non-alternating in-zone variation.
 *   Each variant sub-zone gets equal share of the storm allocation
 *   (100 / sequence_length % of storm). The reader perceives variation,
 *   not loop. Tile-to-tile boundaries inside a variant sub-zone are
 *   seamless because the tile was offset-and-inpainted.
 *
 * CLEARING + CALM
 *
 *   Each is a single tile that tiles seamlessly within its zone height.
 *
 * RENDERING
 *
 *   All tiles render at 85% viewport width (background-size: 85% auto)
 *   for a modest scale-down of branch thickness — the first review
 *   showed branches reading too thick at full viewport width. Tiles
 *   have alpha-channel cream knockouts; the site's cream (--cream-bg in
 *   globals.css) shows through the negative space, including the small
 *   margins on either side of the 85% tile.
 *
 * KNOWN ISSUES
 *
 *   Hero copy legibility against the top of the storm zone is logged in
 *   spec Section 10.1, deferred until full arc is judged in motion.
 *   Sub-zone joins between variants (where storm-a ends and storm-b
 *   begins) may show as a faint horizontal band if the two variants
 *   differ in local density. Cross-variant join fixing is the next item
 *   after the sizing review.
 */

type StormVariant = "a" | "b" | "c";

const DEFAULT_STORM_SEQUENCE: StormVariant[] = ["a", "b", "c", "a"];

export interface HomepageWallpaperProps {
  /** Storm variant order. Default A-B-C-A produces non-alternating variation. */
  stormSequence?: StormVariant[];
  /** Zone allocation as percentages of the parent's height. Defaults are
   *  Addendum B: storm 50 / clearing 15 / calm 35. The three numbers
   *  must sum to 100. */
  stormPct?: number;
  clearingPct?: number;
  calmPct?: number;
}

export default function HomepageWallpaper({
  stormSequence = DEFAULT_STORM_SEQUENCE,
  stormPct = 50,
  clearingPct = 15,
  calmPct = 35,
}: HomepageWallpaperProps = {}) {
  // Shared tile styling — 85% scale-down so storm linework reads finer
  // behind type (see "RENDERING" notes above).
  const tileStyle = {
    backgroundSize: "85% auto",
    backgroundRepeat: "repeat-y" as const,
    backgroundPosition: "top center",
  };

  // Within the storm zone, each variant sub-zone gets an equal share.
  // With sequence length 4, each is 25% of the storm zone (= 12.5% of
  // total wallpaper height under default 50/15/35).
  const stormSubZonePct = 100 / stormSequence.length;

  return (
    <div
      aria-hidden
      // `inset: 0` makes the wallpaper stretch to fill the positioned
      // parent (main). No explicit height needed — the parent's content-
      // driven height is what we want the wallpaper to follow.
      className="pointer-events-none absolute inset-0 -z-10 w-full"
    >
      {/* Storm zone — Addendum B's 50% allocation by default. Four
          variant sub-zones inside, each rendering one of the three
          storm tiles. */}
      <div className="w-full" style={{ height: `${stormPct}%` }}>
        {stormSequence.map((variant, i) => (
          <div
            key={`storm-${variant}-${i}`}
            className="w-full"
            style={{
              height: `${stormSubZonePct}%`,
              backgroundImage: `url(/wallpaper/storm-${variant}.webp)`,
              ...tileStyle,
            }}
          />
        ))}
      </div>

      {/* Clearing zone — Addendum B's 15% "fast break" allocation. */}
      <div
        className="w-full"
        style={{
          height: `${clearingPct}%`,
          backgroundImage: "url(/wallpaper/clearing.webp)",
          ...tileStyle,
        }}
      />

      {/* Calm zone — Addendum B's 35% "extends" allocation. */}
      <div
        className="w-full"
        style={{
          height: `${calmPct}%`,
          backgroundImage: "url(/wallpaper/calm.webp)",
          ...tileStyle,
        }}
      />
    </div>
  );
}
