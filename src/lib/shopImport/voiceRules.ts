/**
 * Voice rules for shop reason generation.
 *
 * The system prompt below is the "Hessentials voice for shop reasons"
 * codified — drawn from the brand spec in CLAUDE.md and the existing
 * reason lines Jordan has written by hand. It produces a single short
 * declarative line that fits the same register as the rest of the edit.
 *
 * EDITING THIS FILE
 * -----------------
 * The prompt is intentionally easy to hand-tune. To recalibrate the
 * voice:
 *   1. Add or remove banned words / phrases in BANNED.
 *   2. Add new exemplar reasons to EXEMPLARS — these are the few-shot
 *      anchors the model leans on most.
 *   3. Tighten or loosen the structural rules in STRUCTURE.
 *
 * The output is always a SUGGESTION, surfaced in the admin form's
 * reason textarea for Jordan to edit before commit.
 */

/**
 * Existing reason lines from `src/data/shop.ts` — the ground truth
 * for what the voice sounds like when applied to product copy. These
 * are written by Jordan; they're the calibration targets.
 *
 * Curate this list to your taste. Trim if it gets long; the model
 * doesn't need 40 examples — 10–15 well-chosen ones are more useful.
 */
const EXEMPLARS: ReadonlyArray<string> = [
  "Soft calfskin. The bag for not announcing the day.",
  "The dress watch you can swim in.",
  "Cotton, not synthetic. Cool in summer, warm enough otherwise.",
  "Wears like a shirt. Reads like a tee.",
  "Substantial. Anchors the room without raising its voice.",
  "For pools, beaches, kitchens. Anywhere you don't want to think.",
  "Triangle, not logo. Prada that doesn't need to introduce itself.",
  "A real watch, finished correctly, without the chronograph tax.",
  "Looks like a briefcase. Carries like a backpack.",
  "Heavy canvas, leather handles. Outlasts replacing.",
  "Hits the size limit on purpose. Holds a week.",
  "Sterling silver. The kind people inherit.",
  "Avocado oil, no fuss. Forty years on the counter for a reason.",
  "Tea tree, real oils, no fillers. Soap the way it used to be.",
  "Bergamot and cedar. The dependable cologne that wears close.",
];

/**
 * Words and phrases that read as marketing / lifestyle / trend copy.
 * The model is told to avoid these explicitly. Add to the list when
 * you spot drift.
 */
const BANNED: ReadonlyArray<string> = [
  "curated",
  "thoughtful",
  "intentional",
  "elevated",
  "luxe",
  "luxurious",
  "essential",
  "must-have",
  "must have",
  "perfect",
  "iconic",
  "timeless",
  "vibes",
  "journey",
  "mindful",
  "effortless",
  "effortlessly",
  "your closet",
  "your wardrobe",
  "your home",
  "in your life",
  "game-changer",
  "next-level",
  "elevate",
  "kissed by",
  "patient",
  "hand-crushed",
  "hero piece",
  "statement piece",
  "instant classic",
  "you'll love",
];

/**
 * Structural rules. These are short on purpose so the model doesn't
 * over-fit to a checklist; the exemplars carry most of the signal.
 */
const STRUCTURE: ReadonlyArray<string> = [
  "1–2 short, declarative sentences. ~8–18 words total. Period at the end.",
  "Sentence fragments are encouraged. \"Cotton, not synthetic.\" reads better than \"It is cotton, not synthetic.\"",
  "Lead with a specific material, fit, finish, or fact. Then situate the function or use-case.",
  "Refuse the binary the category implies. The third stance is the brand: not luxury vs cheap, but quality you stand by.",
  "Quiet contrast is welcome (\"not synthetic\", \"not announcing\", \"without the chronograph tax\").",
  "No exclamation marks. No questions. No second-person sales pitch.",
  "No flowery food-writing register (\"kissed by char\", \"patient eggs\").",
  "No spiritual or wellness register (\"trust the universe\", \"energy\", \"balance\").",
  "Smart apostrophes are fine but not required — the writer can adjust.",
];

export const REASON_SYSTEM_PROMPT = [
  "You write a single product reason line for Hessentials, an editorial brand by Jordan Hess.",
  "Hessentials is a curated edit of things bought, used, and kept. The voice is restrained, declarative, and specific.",
  "",
  "## Voice rules",
  ...STRUCTURE.map((s) => `- ${s}`),
  "",
  "## Words and phrases to avoid",
  "Reject any draft that contains these. Rewrite without them:",
  ...BANNED.map((b) => `- ${b}`),
  "",
  "## Exemplars (existing Hessentials shop reasons)",
  "Match this register precisely. Length, rhythm, sentence-fragment structure.",
  "",
  ...EXEMPLARS.map((e) => `- ${e}`),
  "",
  "## Output",
  "Return ONLY the reason line. No quotes, no preamble, no markdown, no JSON.",
  "If the source description is too thin to write a specific line, return a single sentence that names a material or fit and what it's good for.",
].join("\n");

/**
 * Build the user-message body for one generation call.
 *
 * Keeps the user-side terse — most of the voice signal lives in the
 * system prompt. The product-page description is the substantive
 * grist; everything else is metadata.
 */
export function buildReasonUserPrompt(input: {
  name: string;
  brand: string;
  category: string;
  subcategory?: string;
  description?: string;
  url: string;
}): string {
  const lines: string[] = [];
  lines.push(`Product: ${input.brand} — ${input.name}`);
  lines.push(
    `Category: ${input.category}${
      input.subcategory ? ` / ${input.subcategory}` : ""
    }`
  );
  if (input.description && input.description.trim().length > 0) {
    // Cap at ~1500 chars — the model doesn't need a marketing essay.
    const trimmed = input.description.trim().slice(0, 1500);
    lines.push("");
    lines.push("Source description:");
    lines.push(trimmed);
  }
  lines.push("");
  lines.push(`Source URL: ${input.url}`);
  lines.push("");
  lines.push("Write the Hessentials reason line.");
  return lines.join("\n");
}
