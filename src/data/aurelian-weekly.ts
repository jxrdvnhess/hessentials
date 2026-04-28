/**
 * Aurelian — weekly reading.
 *
 * A short editorial reading published weekly. Aurelian applies his
 * framework to the current cyclical/astrological moment and names what
 * the week is asking of attention. The reading is non-interactive — it
 * sits alongside the Big Three tool, not inside it.
 *
 * Update cadence: weekly, on Monday morning. Update the `weekOf` date
 * and rewrite `paragraphs` (3–5 paragraphs, ~250–400 words total).
 * Keep voice rules in lockstep with `aurelianRecognition.ts`:
 *   - Calm, observational, behavioral, third-person.
 *   - No predictions, no future-tense forecasts.
 *   - No mysticism, no flattery.
 *   - One short sentence per paragraph minimum.
 */

export type AurelianWeeklyReading = {
  /** The Monday that begins the reading's week. ISO date. */
  weekOf: string;
  /** Display string: "April 27 — May 3, 2026". */
  range: string;
  /** Short scene-setting headline (one sentence). */
  headline: string;
  /** 3–5 paragraphs of body. Each paragraph ~50–80 words. */
  paragraphs: string[];
};

export const CURRENT_READING: AurelianWeeklyReading = {
  weekOf: "2026-04-27",
  range: "April 27 — May 3, 2026",
  headline:
    "The week the year stops asking you to hurry and starts asking you to settle.",
  paragraphs: [
    "Late April lands in the slow middle of Taurus season — the section of the year where momentum from the spring push is supposed to translate into ground. Most people skip the translation. They try to keep the velocity that worked in early April, and the body, which is now finally asleep through the night again, begins quietly refusing the pace.",

    "The pattern this week is the gap between what the calendar still asks for and what the body has already decided. Meetings will run at the same speed they did six weeks ago. The rooms will be just as loud. What's different is that you are no longer producing the same heat to meet them, and the part of you that's been bracing through it has begun to drop the brace without your permission.",

    "Read this as information, not as resistance. The rest the body is requesting is the same rest the year has been pointing toward since the spring equinox. The slow middle is the season's gift, and it only arrives once. Skip it and the summer arrives unsteady; honor it and the next push runs on real fuel.",

    "The watch point: agreeing in the room to the cadence the room is running at, then privately running a different cadence on the way home. The cost of that gap is small for a week and unsustainable past a month. The week's small practice is naming the actual pace once, out loud, to one person who needs to hear it. Most weeks ask for more. This one asks for less, on purpose.",
  ],
};
