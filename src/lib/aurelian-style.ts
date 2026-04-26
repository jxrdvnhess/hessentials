/**
 * Aurelian — Style Reading Engine
 *
 * Generates the "How This Shows Up in Style" section from a user's Big
 * Three selections. Works with one, two, or three placements. Returns
 * null when nothing usable is selected.
 *
 * The output is a structured object the renderer iterates over — only
 * sections with available data are rendered. Tension and synthesis
 * blocks only appear when two or more placements are selected.
 *
 * Voice: Aurelian (psychological pattern intelligence) crossed with
 * Château (style discipline). No aesthetic labels, no trend names, no
 * gendered prescriptions, no "must-have" or "elevate" language.
 */

import { SIGNS, type Element, type Selection, type Sign } from "../data/aurelian";
import {
  ELEMENT_COUNTERWEIGHT,
  STYLE_SIGNATURES,
  type StylePlacementBlock,
} from "../data/aurelian-style";

/* ---------- Types ---------- */

export type StylePlacementSection = {
  /** "Rising" / "Moon" / "Sun" — used in the section eyebrow. */
  placementLabel: string;
  /** Sign display name, e.g. "Taurus". */
  signName: string;
  /** One-line description of how this sign presents at this placement. */
  description: string;
  /** 3 practical wardrobe items for this placement. */
  favors: readonly string[];
};

export type StyleTension = {
  /** Named pattern: "polished arrival, sensory interior", etc. */
  pattern: string;
  /** One paragraph explaining the gap. */
  paragraph: string;
};

export type StyleReading = {
  /** Fixed opening copy, surfaced for the renderer. */
  opening: string;
  /** Soft note shown when only one placement is selected. */
  partialNote?: string;
  naturalSignal?: StylePlacementSection;
  comfortLayer?: StylePlacementSection;
  expressionLayer?: StylePlacementSection;
  styleTension?: StyleTension;
  /** 4–6 wardrobe-strategy lines (not products). */
  recommendations: readonly string[];
  /** Closing paragraph that connects the pattern back to Hessentials. */
  hessentialsDirection: string;
};

/* ---------- Fixed copy ---------- */

const OPENING =
  "Style is not aesthetic first. It is alignment. Most people dress for how they want to be perceived. Very few dress in a way their system can actually sustain. This is where the gap usually lives.";

const PARTIAL_NOTE =
  "This is one layer of the picture. Add the other placements above when you know them — the reading sharpens with each one.";

/* ---------- Helpers ---------- */

function isSign(value: Selection): value is Sign {
  return value !== "" && value !== "unknown";
}

function elementOf(sign: Sign): Element {
  return SIGNS[sign].element;
}

/** Surface phrases for the named pattern, keyed by the Rising element. */
const RISING_SURFACE: Record<Element, string> = {
  fire: "direct arrival",
  earth: "composed arrival",
  air: "polished arrival",
  water: "soft arrival",
};

/** Interior phrases keyed by the Moon element. */
const MOON_INTERIOR: Record<Element, string> = {
  fire: "fast interior",
  earth: "sensory interior",
  air: "shifting interior",
  water: "private interior",
};

/** Identity phrases keyed by the Sun element. */
const SUN_IDENTITY: Record<Element, string> = {
  fire: "decisive expression",
  earth: "lasting expression",
  air: "calibrated expression",
  water: "atmospheric expression",
};

/* ---------- Section builders ---------- */

function buildSection(
  placementLabel: "Rising" | "Moon" | "Sun",
  sign: Sign,
  block: StylePlacementBlock
): StylePlacementSection {
  return {
    placementLabel,
    signName: SIGNS[sign].name,
    description: block.description,
    favors: block.favors.slice(0, 3),
  };
}

export function buildNaturalSignal(
  rising: Selection
): StylePlacementSection | undefined {
  if (!isSign(rising)) return undefined;
  return buildSection("Rising", rising, STYLE_SIGNATURES[rising].rising);
}

export function buildComfortLayer(
  moon: Selection
): StylePlacementSection | undefined {
  if (!isSign(moon)) return undefined;
  return buildSection("Moon", moon, STYLE_SIGNATURES[moon].moon);
}

export function buildExpressionLayer(
  sun: Selection
): StylePlacementSection | undefined {
  if (!isSign(sun)) return undefined;
  return buildSection("Sun", sun, STYLE_SIGNATURES[sun].sun);
}

/* ---------- Tension ---------- */

export function buildStyleTension(args: {
  sun: Selection;
  moon: Selection;
  rising: Selection;
}): StyleTension | undefined {
  const sunSign = isSign(args.sun) ? args.sun : null;
  const moonSign = isSign(args.moon) ? args.moon : null;
  const risingSign = isSign(args.rising) ? args.rising : null;

  const known = [sunSign, moonSign, risingSign].filter(
    (s): s is Sign => s !== null
  );
  if (known.length < 2) return undefined;

  // All three the same sign
  if (
    sunSign &&
    moonSign &&
    risingSign &&
    sunSign === moonSign &&
    sunSign === risingSign
  ) {
    const name = SIGNS[sunSign].name;
    return {
      pattern: `concentrated ${SIGNS[sunSign].element}`,
      paragraph: `When all three placements land on ${name}, the system runs in one register. The wardrobe should feel coherent, almost severe in its consistency. The risk is becoming locked into one mode of presentation — the work is finding depth inside a tight signature instead of breadth across registers.`,
    };
  }

  // All same element (but not all same sign)
  const elements = known.map(elementOf);
  const allSameElement = elements.every((e) => e === elements[0]);
  if (allSameElement) {
    const el = elements[0];
    return {
      pattern: `concentrated ${el}`,
      paragraph: `Every placement runs on ${el}. The wardrobe will be strong at ${describeElementStrength(el)} and underweight in ${ELEMENT_COUNTERWEIGHT[el]}. Lean into the dominant register, but bring in one counterweight piece so the system doesn't fold in on itself.`,
    };
  }

  // Build a name from the available placements
  const surface =
    risingSign !== null ? RISING_SURFACE[elementOf(risingSign)] : null;
  const interior =
    moonSign !== null ? MOON_INTERIOR[elementOf(moonSign)] : null;
  const identity =
    sunSign !== null ? SUN_IDENTITY[elementOf(sunSign)] : null;

  const parts = [surface, interior, identity].filter(
    (p): p is string => p !== null
  );
  const pattern = parts.join(", ");

  // Paragraph composed from the contrasts that are actually present
  const paragraph = composeTensionParagraph({
    surface,
    interior,
    identity,
    risingName: risingSign ? SIGNS[risingSign].name : null,
    moonName: moonSign ? SIGNS[moonSign].name : null,
    sunName: sunSign ? SIGNS[sunSign].name : null,
  });

  return { pattern, paragraph };
}

function describeElementStrength(el: Element): string {
  switch (el) {
    case "fire":
      return "presence and movement";
    case "earth":
      return "structure and quality";
    case "air":
      return "variation and styling intelligence";
    case "water":
      return "softness and atmosphere";
  }
}

function composeTensionParagraph(args: {
  surface: string | null;
  interior: string | null;
  identity: string | null;
  risingName: string | null;
  moonName: string | null;
  sunName: string | null;
}): string {
  const lines: string[] = [];

  // Rising vs. Moon: the perception/sustainability gap
  if (args.surface && args.interior) {
    lines.push(
      `The look reads as ${args.surface} — that's the ${args.risingName} signal landing first. Underneath, the ${args.moonName} moon is a ${args.interior}. The gap is between how you arrive and what you can actually sustain in the clothes.`
    );
  }

  // Rising vs. Sun: the surface/long-arc gap
  if (args.surface && args.identity && !args.interior) {
    lines.push(
      `The look reads as ${args.surface} — that's the ${args.risingName} signal. The ${args.sunName} sun is building a ${args.identity}. The gap is between first impression and long-term direction. The wardrobe should narrow it.`
    );
  }

  // Moon vs. Sun: the comfort/identity gap
  if (args.interior && args.identity && !args.surface) {
    lines.push(
      `Inside, the ${args.moonName} moon is a ${args.interior}. Over time, the ${args.sunName} sun is expressing a ${args.identity}. The gap is between what you can sustain day-to-day and where the wardrobe is heading. Closing it is the project.`
    );
  }

  // Three-layer synthesis
  if (args.surface && args.interior && args.identity) {
    lines.push(
      `That's the triangle: ${args.surface} on the surface, ${args.interior} underneath, ${args.identity} in the long arc. Where these line up is where the wardrobe holds. Where they don't, the look will drain you to maintain — or it will read smaller than you actually are.`
    );
  }

  return lines.join(" ");
}

/* ---------- Recommendations ---------- */

export function buildStyleRecommendations(args: {
  sun: Selection;
  moon: Selection;
  rising: Selection;
}): readonly string[] {
  const known: Sign[] = [];
  if (isSign(args.rising)) known.push(args.rising);
  if (isSign(args.moon)) known.push(args.moon);
  if (isSign(args.sun)) known.push(args.sun);

  if (known.length === 0) return [];

  // Pool the favors from the actual placements that are selected
  const pool: string[] = [];
  if (isSign(args.rising))
    pool.push(...STYLE_SIGNATURES[args.rising].rising.favors);
  if (isSign(args.moon))
    pool.push(...STYLE_SIGNATURES[args.moon].moon.favors);
  if (isSign(args.sun)) pool.push(...STYLE_SIGNATURES[args.sun].sun.favors);

  // De-duplicate (case-insensitive). Preserve the first occurrence order.
  const seen = new Set<string>();
  const distilled: string[] = [];
  for (const item of pool) {
    const key = item.trim().toLowerCase();
    if (seen.has(key)) continue;
    seen.add(key);
    distilled.push(item);
  }

  // Always-on Hessentials principles, added when room remains
  const universal = [
    "fewer pieces with better weight and texture",
    "repeatable silhouettes over assembled outfits",
    "alignment between perception and lived comfort",
  ];

  // Element counterweight — if all selected placements share an element,
  // surface the missing register as a strategy line
  const elements = known.map(elementOf);
  const allSame = elements.every((e) => e === elements[0]);
  if (allSame) {
    const el = elements[0];
    distilled.push(
      `add one counterweight piece — ${ELEMENT_COUNTERWEIGHT[el]}`
    );
  }

  // Mix in universals if we're under 6 lines
  for (const u of universal) {
    if (distilled.length >= 6) break;
    if (!seen.has(u.toLowerCase())) distilled.push(u);
  }

  return distilled.slice(0, 6);
}

/* ---------- Hessentials direction (closing) ---------- */

export function buildHessentialsStyleDirection(args: {
  sun: Selection;
  moon: Selection;
  rising: Selection;
}): string {
  const known: Sign[] = [];
  if (isSign(args.rising)) known.push(args.rising);
  if (isSign(args.moon)) known.push(args.moon);
  if (isSign(args.sun)) known.push(args.sun);

  if (known.length === 0) return "";

  const elements = known.map(elementOf);
  const allSame = elements.every((e) => e === elements[0]);
  const allSameSign =
    known.length >= 2 && known.every((s) => s === known[0]);

  if (allSameSign) {
    return "For this system, Hessentials style is about depth inside a tight signature, not range. The wardrobe should reduce noise, not add new registers. Refine the few pieces that already work — that's where the long arc lives.";
  }

  if (allSame) {
    return directionForElement(elements[0]);
  }

  // Mixed elements — synthesis-leaning close
  return "For this system, Hessentials style is alignment over aesthetic. The wardrobe should reduce the gap between how you arrive and what you can sustain — not perform a category, not perform a trend. Edit toward what already feels accurate.";
}

function directionForElement(el: Element): string {
  switch (el) {
    case "fire":
      return "For this system, Hessentials style is presence without performance. The wardrobe should hold the room without raising its voice. Choose pieces with weight and shape — the kind that read decisive even when nothing is being announced.";
    case "earth":
      return "For this system, Hessentials style is quality that compounds. The wardrobe should be built like infrastructure, not assembled from trends. Fewer pieces, better material, longer arc.";
    case "air":
      return "For this system, Hessentials style is intelligent range. The wardrobe should give you variation without clutter — separates that recombine, proportions you've already solved, taste edited rather than expanded.";
    case "water":
      return "For this system, Hessentials style is softness with discipline. The wardrobe should feel sustaining rather than draining — fluid materials, considered cuts, and structure where it's needed so the look doesn't dissolve.";
  }
}

/* ---------- Public entry ---------- */

export function generateStyleReading(args: {
  sun: Selection;
  moon: Selection;
  rising: Selection;
}): StyleReading | null {
  const knownCount = [args.sun, args.moon, args.rising].filter(isSign).length;
  if (knownCount === 0) return null;

  const naturalSignal = buildNaturalSignal(args.rising);
  const comfortLayer = buildComfortLayer(args.moon);
  const expressionLayer = buildExpressionLayer(args.sun);
  const styleTension = buildStyleTension(args);
  const recommendations = buildStyleRecommendations(args);
  const hessentialsDirection = buildHessentialsStyleDirection(args);

  return {
    opening: OPENING,
    partialNote: knownCount === 1 ? PARTIAL_NOTE : undefined,
    naturalSignal,
    comfortLayer,
    expressionLayer,
    styleTension,
    recommendations,
    hessentialsDirection,
  };
}
