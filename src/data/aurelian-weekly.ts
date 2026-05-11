/**
 * Aurelian — weekly reading.
 *
 * A short editorial reading published weekly. Aurelian applies his
 * framework to the current cyclical/astrological moment and names what
 * the week is asking of attention. The reading is non-interactive — it
 * sits alongside the Big Three tool, not inside it.
 *
 * Update cadence: weekly, on Monday morning. Update the editorial copy
 * (`headline`, `paragraphs`, `excerpt`) in `CURRENT_READING_COPY` below.
 * The date fields (`weekOf`, `range`) auto-compute from today's date —
 * no manual date editing required. See `getCurrentReading()`.
 *
 * Voice rules — lockstep with `aurelianRecognition.ts`:
 *   - Calm, observational, behavioral, third-person.
 *   - No predictions, no future-tense forecasts.
 *   - No mysticism, no flattery.
 *   - One short sentence per paragraph minimum.
 *   - Cyclical/seasonal framing (Taurus season, mid-spring, Beltane week)
 *     is safer than transit-specific claims. Don't fabricate transits.
 */

export type AurelianWeeklyReading = {
  /** The Monday that begins the reading's week. ISO date — auto-computed. */
  weekOf: string;
  /** Display string: "May 4–10, 2026" or "April 27–May 3, 2026".
   *  Date and numeric ranges use an en dash (U+2013) with no surrounding
   *  spaces — editorial convention. Auto-computed from today's date. */
  range: string;
  /** Short scene-setting headline (one sentence). */
  headline: string;
  /** 3–5 paragraphs of body. Each paragraph ~50–80 words. */
  paragraphs: string[];
  /**
   * Single hand-picked sharpest line for the home-page panel.
   * Editorial choice — must NOT be the opening sentence (per spec).
   * Update when `paragraphs` changes.
   */
  excerpt: string;
};

/**
 * Editorial copy for the current week. The Monday scheduled task
 * (Cowork: aurelian-weekly-monday) drafts a new entry here each Monday;
 * Jordan reviews and pushes via GitHub Desktop. Date fields are NOT
 * stored here — they're computed at render time from today's date.
 */
const CURRENT_READING_COPY = {
  headline:
    "Late Taurus, when starting begins to substitute for finishing.",
  paragraphs: [
    "Mid-May sits in the last full week of Taurus, two weeks past Beltane and ten days short of Gemini. The growing arc is steady but not yet hot. The year's character at this point is duration, not announcement — the part of spring that asks whether the work begun in April is still the work being done in May. Most years, the answer is no. The work has been quietly replaced by its cousin: something close, something newer, something that absorbs the same effort without owing the same finish.",

    "The pattern this week is the pull to start a new thread before the current one is finished. The thread offered is usually dressed in the language of completion — the next version, the proper application of what was learned, the project that will use the skill better. It is rarely that. It is the appetite for beginnings interrupting the harder discipline of endings. Taurus does not punish the appetite. It just notices when the appetite shows up first.",

    "It shows up at the 80% mark — the room half-styled instead of one room finished, the draft re-read for a reason to keep going or a reason to stop. The list in the margin grows. The unfinished sits across the desk. A new idea appears with surprising clarity at the same hour the old one was about to land. The clarity is real and also early. Both can be true and the order still matters.",

    "The watch point is the small voice that proposes what is next while the current thing is still mid-sentence. The proposal sounds like momentum. It is usually flight. The week's practice is one finish before any new start — not as principle, but as test. What is already in motion is closer to done than the appetite is willing to admit. Finishing it is the week's quiet weight.",
  ],
  excerpt:
    "What is already in motion is closer to done than the appetite is willing to admit.",
} as const;

/* -----------------------------------------------------------------
   Date helpers — auto-compute the current Mon→Sun window.

   The editorial cadence anchors to US Eastern. We resolve "today's
   date" in that timezone so the week rolls over on Monday morning
   wherever Vercel's edge lives, not on Sunday-evening UTC.
-------------------------------------------------------------------- */

const EDITORIAL_TIMEZONE = "America/New_York";

const MONTH_NAMES = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
] as const;

const EN_DASH = "–";

/**
 * Returns the Monday (Y/M/D, in EDITORIAL_TIMEZONE) that begins the
 * week containing `now`. Implemented via Intl.DateTimeFormat so DST
 * and timezone offsets are correct without a date library.
 */
function getMondayOfWeek(now: Date): { year: number; month: number; day: number } {
  const fmt = new Intl.DateTimeFormat("en-CA", {
    timeZone: EDITORIAL_TIMEZONE,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    weekday: "short",
  });
  const parts = fmt.formatToParts(now);
  const get = (type: string) =>
    parts.find((p) => p.type === type)?.value ?? "";
  const weekday = get("weekday");
  const year = Number(get("year"));
  const month = Number(get("month"));
  const day = Number(get("day"));

  const dowMap: Record<string, number> = {
    Sun: 0,
    Mon: 1,
    Tue: 2,
    Wed: 3,
    Thu: 4,
    Fri: 5,
    Sat: 6,
  };
  const dow = dowMap[weekday] ?? 1;
  // Days to subtract to land on Monday. Sunday → 6 days back.
  const daysBack = dow === 0 ? 6 : dow - 1;

  // Anchor a UTC date at noon on the local-tz date, subtract daysBack.
  // Noon avoids any DST-crossing edge cases when shifting by whole days.
  const anchor = new Date(Date.UTC(year, month - 1, day, 12, 0, 0));
  anchor.setUTCDate(anchor.getUTCDate() - daysBack);
  return {
    year: anchor.getUTCFullYear(),
    month: anchor.getUTCMonth() + 1,
    day: anchor.getUTCDate(),
  };
}

function addDays(
  ymd: { year: number; month: number; day: number },
  n: number,
): { year: number; month: number; day: number } {
  const d = new Date(Date.UTC(ymd.year, ymd.month - 1, ymd.day, 12, 0, 0));
  d.setUTCDate(d.getUTCDate() + n);
  return {
    year: d.getUTCFullYear(),
    month: d.getUTCMonth() + 1,
    day: d.getUTCDate(),
  };
}

function pad(n: number): string {
  return n < 10 ? `0${n}` : String(n);
}

/**
 * Format the Mon→Sun window per the brand typography rules:
 *   - same month:    "May 4–10, 2026"
 *   - cross-month:   "April 27–May 3, 2026"
 *   - cross-year:    "December 29, 2025–January 4, 2026"
 * En dash, no surrounding spaces.
 */
function formatRange(
  monday: { year: number; month: number; day: number },
  sunday: { year: number; month: number; day: number },
): string {
  const mMonthName = MONTH_NAMES[monday.month - 1];
  const sMonthName = MONTH_NAMES[sunday.month - 1];

  if (monday.year !== sunday.year) {
    return `${mMonthName} ${monday.day}, ${monday.year}${EN_DASH}${sMonthName} ${sunday.day}, ${sunday.year}`;
  }
  if (monday.month !== sunday.month) {
    return `${mMonthName} ${monday.day}${EN_DASH}${sMonthName} ${sunday.day}, ${sunday.year}`;
  }
  return `${mMonthName} ${monday.day}${EN_DASH}${sunday.day}, ${sunday.year}`;
}

/**
 * Returns the current week's reading with auto-computed date fields.
 * Call this from server components — pages that consume it should set
 * `revalidate` so the date refreshes without a redeploy.
 */
export function getCurrentReading(now: Date = new Date()): AurelianWeeklyReading {
  const monday = getMondayOfWeek(now);
  const sunday = addDays(monday, 6);
  return {
    weekOf: `${monday.year}-${pad(monday.month)}-${pad(monday.day)}`,
    range: formatRange(monday, sunday),
    headline: CURRENT_READING_COPY.headline,
    paragraphs: [...CURRENT_READING_COPY.paragraphs],
    excerpt: CURRENT_READING_COPY.excerpt,
  };
}
