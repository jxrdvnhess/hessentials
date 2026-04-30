/**
 * Price formatting — Hessentials Shop.
 *
 * Every variant array (from any extractor) becomes a single display
 * string here. The brand has retired tier markers ($/$$/$$$); the
 * display is always either a single price or, when variants differ,
 * a "From $X" prefix using the lowest variant.
 *
 * The "From" prefix was the chosen v1 over an explicit range — it
 * keeps cards quiet and never overstates what the lowest entry costs.
 */

/**
 * Round a number to USD. Most sources return whole dollars; some
 * (Shopify, JSON-LD) return floats — round to the nearest dollar
 * unless cents are non-trivial.
 */
function formatDollars(amount: number): string {
  // If the price has meaningful cents (e.g. $7.99, $12.50), keep them.
  // Otherwise drop them — Hessentials carries luxury items where $4,200
  // is read more cleanly than $4,200.00.
  const hasCents = Math.round(amount * 100) % 100 !== 0;
  return hasCents
    ? `$${amount.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}`
    : `$${Math.round(amount).toLocaleString("en-US")}`;
}

/**
 * Format a non-empty array of variant prices into a single display
 * string. Single-variant → "$X". Multi-variant → "From $X" using the
 * minimum (per the v1 display decision).
 *
 * Throws if `variants` is empty — extractors must return at least one.
 */
export function formatVariants(variants: number[]): string {
  if (!variants.length) {
    throw new Error("formatVariants: no variants provided");
  }
  if (variants.length === 1) {
    return formatDollars(variants[0]);
  }
  const min = Math.min(...variants);
  // If every variant is the same price, drop the prefix.
  const allSame = variants.every((v) => v === min);
  return allSame ? formatDollars(min) : `From ${formatDollars(min)}`;
}

/**
 * Human-readable date for the "Last verified" line. Renders as
 * "Apr 30, 2026" — short month, no day-of-week, no time. The italic
 * register on the detail page softens it further.
 */
export function formatVerifiedDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}
