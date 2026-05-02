/**
 * Shop import — slug generation.
 *
 * The shop's image convention is `/shop/<slug>-N.jpg` and the data file
 * keys every product by `slug`. The shop's existing slugs follow a
 * `<brand>-<short-name>` pattern in lowercase kebab — e.g.
 * "loewe-goya-thin-briefcase", "omega-aqua-terra-small-seconds".
 *
 * `buildSlug(brand, name)` mirrors that convention. `ensureUnique`
 * appends `-2`, `-3`, … when the proposed slug collides with an
 * existing entry.
 */

const SMALL_WORDS = new Set([
  "and",
  "or",
  "the",
  "a",
  "an",
  "of",
  "for",
  "in",
  "to",
  "with",
]);

function kebab(input: string): string {
  return input
    .toLowerCase()
    // common ligatures / accents → ASCII
    .normalize("NFKD")
    .replace(/[̀-ͯ]/g, "")
    // ampersand → "and"
    .replace(/&/g, " and ")
    // strip anything that isn't alnum / space / hyphen
    .replace(/[^a-z0-9\s-]/g, " ")
    .trim()
    .split(/\s+/)
    .filter((w) => w.length > 0)
    .join("-")
    .replace(/-+/g, "-");
}

/** "Massimo Dutti" + "Linen-Cotton Double-Collar T-Shirt" → "massimo-dutti-linen-cotton-double-collar-t-shirt" */
export function buildSlug(brand: string, name: string): string {
  const brandPart = kebab(brand);
  // Trim small words from the head/middle of name when the resulting slug
  // gets long — keeps things readable. Always preserves first/last word.
  const nameWords = kebab(name).split("-").filter(Boolean);
  let nameSlug = nameWords.join("-");
  if (nameSlug.length + brandPart.length > 60 && nameWords.length > 3) {
    const trimmed = nameWords.filter(
      (w, i) =>
        i === 0 || i === nameWords.length - 1 || !SMALL_WORDS.has(w)
    );
    nameSlug = trimmed.join("-");
  }
  const combined = [brandPart, nameSlug].filter(Boolean).join("-");
  return combined.replace(/-+/g, "-").replace(/^-|-$/g, "");
}

export function ensureUnique(
  proposed: string,
  existing: ReadonlySet<string>
): string {
  if (!existing.has(proposed)) return proposed;
  let i = 2;
  while (existing.has(`${proposed}-${i}`)) i += 1;
  return `${proposed}-${i}`;
}
