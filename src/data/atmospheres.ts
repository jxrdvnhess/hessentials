/**
 * Hessentials Shop — atmosphere collections.
 *
 * Atmosphere collections are emotional groupings that cut across the
 * operational category tree. A single product can sit in several at
 * once (a Snow Peak titanium mug is `Soft Travel` AND `Morning Ritual`
 * AND `Portable Ritual` AND `Analog Objects`).
 *
 * Per Chateau's 2026-05-15 post-live audit, atmosphere collections
 * become the emotional front door of the Shop. Categories remain
 * necessary for operational navigation but are no longer the dominant
 * surface.
 *
 * The canonical list of names lives here. The full editorial register
 * (spanning categories, emotional register, example products) lives in
 * `data/sourcing-policy.md` and in the Object Archive workbook.
 *
 * `LAUNCH_ATMOSPHERES` is the foreground set — what surfaces on the
 * Shop homepage. The rest of the atmospheres referenced in products'
 * `atmosphereCollection` arrays still render via the dynamic route at
 * `/shop/atmosphere/[slug]`, they just don't lead the homepage.
 */

/**
 * Launch-facing atmosphere collections. Order matters — the homepage
 * renders these in declared order. New atmospheres get added at the
 * end unless they specifically need top placement.
 */
export const LAUNCH_ATMOSPHERES: readonly string[] = [
  "Soft Travel",
  "Kitchen Counter Objects Worth Leaving Out",
  "The Good Lamp Rule",
  "Things That Improve a Tuesday",
  "Hotel Energy at Home",
  "Quiet Uniform",
  "Pantry Rituals",
  "Portable Ritual",
  "Correct Low",
  "Warm Minimalism",
  "Weeknight Table",
  "Rainy Morning Objects",
  "Useful Beauty",
  "Object With Memory",
  "Things That Age Correctly",
] as const;

/**
 * Canonical kebab-case slug for an atmosphere name. Used for URLs:
 * `/shop/atmosphere/<slug>`. Reversible via `atmosphereSlugToName`.
 *
 * "Soft Travel"                                 → "soft-travel"
 * "Kitchen Counter Objects Worth Leaving Out"   → "kitchen-counter-objects-worth-leaving-out"
 * "Things That Improve a Tuesday"               → "things-that-improve-a-tuesday"
 */
export function atmosphereSlug(name: string): string {
  return name
    .toLowerCase()
    .replace(/&/g, "and")
    .replace(/[^a-z0-9\s-]/g, "")
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .join("-");
}

/**
 * Match a URL slug back to a canonical atmosphere name. Falls back to
 * a title-cased rendering of the slug for atmospheres not in
 * LAUNCH_ATMOSPHERES (so any `atmosphereCollection` value still gets
 * a viewable page).
 */
export function atmosphereNameFromSlug(slug: string): string | null {
  const hit = LAUNCH_ATMOSPHERES.find((name) => atmosphereSlug(name) === slug);
  if (hit) return hit;
  // Free-text fallback: title-case the slug words.
  const parts = slug.split("-").filter(Boolean);
  if (parts.length === 0) return null;
  return parts
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}
