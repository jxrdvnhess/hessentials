/**
 * Fisher-Yates shuffle.
 *
 * Returns a new shuffled array — does not mutate the input.
 *
 * Used by the index grids on /recipes, /living, /style, and /shop. Each
 * grid runs this once on mount (inside a useEffect), then renders the
 * shuffled order. Server-side render keeps the original declared order
 * so hydration is deterministic; the client re-orders on the first
 * paint after mount, giving every visit a fresh sequence without
 * causing a hydration mismatch warning.
 */
export function shuffleArray<T>(items: readonly T[]): T[] {
  const arr = items.slice();
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}
