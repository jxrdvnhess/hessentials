/**
 * Default `priceRange` string for an import preview.
 *
 * The shop's existing `priceRange` strings are tight ranges using an
 * en-dash with no surrounding spaces — "$1,400–$1,800" — per the
 * brand's typography rules. Single-price products use "$95".
 *
 * This matches the curated style. The admin UI lets Jordan override
 * the default before commit.
 */

function formatDollars(amount: number): string {
  const hasCents = Math.round(amount * 100) % 100 !== 0;
  return hasCents
    ? `$${amount.toLocaleString("en-US", {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })}`
    : `$${Math.round(amount).toLocaleString("en-US")}`;
}

export function suggestPriceRange(prices: number[]): string {
  if (!prices.length) return "";
  const min = Math.min(...prices);
  const max = Math.max(...prices);
  if (min === max) return formatDollars(min);
  return `${formatDollars(min)}–${formatDollars(max)}`;
}
