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
    "Taurus closes mid-week, and the year shifts from weight to sketch.",
  paragraphs: [
    "This week crosses the threshold from Taurus to Gemini. Wednesday is the last day of fixed earth — the mode that holds one thing until it sets. Thursday opens mutable air — the mode that sketches five things to see which one breathes. The growing arc is past announcement and past consolidation. The plants are in. The work is started. It enters articulation. The season stops asking what to keep and starts asking what to say.",

    "The pattern is the pull from one thread to many. Taurus reads slowly. Gemini reads adjacent. The tension is between thickness and lightness — between the long sentence and the four short ones, between the single project finished and the four adjacent ones touched lightly. Neither is wrong. The week is the moment the appetite shifts, and the shift is faster than the work behind it.",

    "It shows up as tab count. The browser climbing past what one mind can hold. The half-finished thing on the desk and three new openings in the margin, each with surprising momentum. Conversations grow longer and conclusions grow shorter. A new collaborator appears, a new idea, a new angle on something already underway. The desk acquires more surfaces than it can keep flat. The day fragments into adjacent sketches. None of them sit still.",

    "The watch point is the instinct to chase the third opening before the second one is read. The mind likes new doors. New doors are easier than the long hall. Recognition shows up small — the tab opened and not read, the message half-drafted, the idea named before the last one was finished. The shift is real and also early. The week is the one where the mouth opens before the ear catches up.",
  ],
  excerpt:
    "The season stops asking what to keep and starts asking what to say.",
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
