/**
 * Aurelian — Style Signature Library
 *
 * Companion data to /src/data/aurelian.ts. Twelve signs × three placements.
 * Each placement has its own description + practical wardrobe direction.
 *
 * Voice: Aurelian (pattern intelligence) crossed with Château (style
 * discipline). No aesthetic labels, no trend names, no shopping addiction
 * energy. The job is wardrobe behavior, not horoscope outfits.
 *
 * Favors are biased per placement so the three rendered sections don't
 * repeat: Rising favors lean toward visual signal/silhouette; Moon favors
 * lean toward fabric/wearability; Sun favors lean toward investment and
 * the long arc of a wardrobe.
 */

import type { Element, Sign } from "./aurelian";

export type StylePlacementBlock = {
  /** One-line description: how this sign presents at this placement. */
  description: string;
  /** 3–5 practical wardrobe directions for this placement. */
  favors: readonly string[];
  /** 2–4 things that usually create friction at this placement. */
  avoids: readonly string[];
  /** One sentence connecting this sign to the Hessentials worldview. */
  hessentialsTranslation: string;
};

export type StyleSignature = {
  rising: StylePlacementBlock;
  moon: StylePlacementBlock;
  sun: StylePlacementBlock;
};

/* ---------- Element style behavior ---------- */

export const ELEMENT_STYLE_NEED: Record<Element, string> = {
  fire: "movement, visibility, energy, immediacy",
  earth: "structure, material quality, repetition, durability",
  air: "variation, styling intelligence, proportion, lightness",
  water: "softness, mood, sensory atmosphere, emotional protection",
};

export const ELEMENT_COUNTERWEIGHT: Record<Element, string> = {
  fire: "earth — so the look does not become impulsive or overexposed",
  earth: "air or fire — so the look does not become heavy or overly controlled",
  air: "earth — so the wardrobe feels anchored",
  water: "structure — so the look does not dissolve",
};

/* ---------- Sign × Placement library ---------- */

export const STYLE_SIGNATURES: Record<Sign, StyleSignature> = {
  aries: {
    rising: {
      description:
        "Direct, active, immediate. The look needs movement and clarity, not over-styling.",
      favors: [
        "clean lines with energy",
        "sharper cuts that cut a clear silhouette",
        "one strong focal point",
      ],
      avoids: ["over-layering", "fussy styling", "outfits that feel too planned"],
      hessentialsTranslation: "Choose pieces that let action stay clean.",
    },
    moon: {
      description:
        "Needs freedom of movement and nothing that feels fussy, restrictive, or overly managed.",
      favors: [
        "fabrics that breathe",
        "pieces that move with the body",
        "unfussy daily layers",
      ],
      avoids: [
        "delicate pieces that require constant adjustment",
        "restrictive fits",
        "anything that has to be babied",
      ],
      hessentialsTranslation: "Choose pieces that let action stay clean.",
    },
    sun: {
      description:
        "Expresses decisiveness, vitality, and self-directed momentum.",
      favors: [
        "one signature outerwear piece",
        "decisive silhouettes that age into character",
        "a wardrobe that reads ready, not rehearsed",
      ],
      avoids: [
        "outfits that read as overworked",
        "trend pieces that won't survive a year",
        "complicated styling",
      ],
      hessentialsTranslation: "Choose pieces that let action stay clean.",
    },
  },

  taurus: {
    rising: {
      description:
        "Grounded, composed, sensual without trying. The visual signal is steadiness.",
      favors: [
        "structured basics with weight",
        "leather and suede surfaces",
        "considered shoes",
      ],
      avoids: [
        "anything visually frantic",
        "cheap-feeling fabric on the surface layer",
        "trend pieces that read as costume",
      ],
      hessentialsTranslation:
        "Invest in fewer things that feel better every time you wear them.",
    },
    moon: {
      description:
        "Needs softness, weight, texture, and physical ease. Comfort is not optional.",
      favors: [
        "weighty knits",
        "washed cottons and soft linen",
        "soft tailoring that doesn't bind",
      ],
      avoids: [
        "uncomfortable shoes",
        "scratchy or thin fabric",
        "rigid construction worn for long days",
      ],
      hessentialsTranslation:
        "Invest in fewer things that feel better every time you wear them.",
    },
    sun: {
      description:
        "Expresses quality, permanence, restraint, and taste that builds over time.",
      favors: [
        "natural materials chosen for the long arc",
        "investment outerwear",
        "pieces that age well into a signature",
      ],
      avoids: [
        "disposable trend pieces",
        "synthetic fabric on hero pieces",
        "buying volume instead of quality",
      ],
      hessentialsTranslation:
        "Invest in fewer things that feel better every time you wear them.",
    },
  },

  gemini: {
    rising: {
      description:
        "Quick, alert, conversational. The look benefits from flexibility and slight variation.",
      favors: [
        "interesting collars or cuffs",
        "considered separates over one-note outfits",
        "one element that catches the eye",
      ],
      avoids: [
        "rigid uniforms",
        "outfits that feel too final",
        "heavy looks with no movement",
      ],
      hessentialsTranslation:
        "Build a wardrobe with intelligent range, not clutter.",
    },
    moon: {
      description:
        "Needs options, lightness, and the ability to shift mood without rebuilding the whole outfit.",
      favors: [
        "modular layers",
        "fabric that reads light without reading flimsy",
        "pieces that mix two or three ways",
      ],
      avoids: [
        "heavy single-use outfits",
        "anything that locks the day into one register",
        "overly committed silhouettes",
      ],
      hessentialsTranslation:
        "Build a wardrobe with intelligent range, not clutter.",
    },
    sun: {
      description:
        "Expresses intelligence, adaptability, and movement through contrast.",
      favors: [
        "a wardrobe of separates that recombine",
        "two or three repeatable silhouettes with variations",
        "range built from fewer, smarter pieces",
      ],
      avoids: [
        "accumulating in pursuit of variety",
        "buying for novelty",
        "treating volume as range",
      ],
      hessentialsTranslation:
        "Build a wardrobe with intelligent range, not clutter.",
    },
  },

  cancer: {
    rising: {
      description:
        "Soft, guarded, familiar. The look should feel approachable but protected.",
      favors: [
        "soft layers",
        "familiar silhouettes done well",
        "gentle structure that reads put-together",
      ],
      avoids: [
        "harsh styling",
        "cold minimalism",
        "anything that reads emotionally false",
      ],
      hessentialsTranslation:
        "Let comfort look intentional, not accidental.",
    },
    moon: {
      description:
        "Needs emotional ease, softness, and clothing that feels lived-in without looking neglected.",
      favors: [
        "washed cottons and broken-in fabric",
        "knits that feel familiar after the first wear",
        "clothes that don't ask the body to perform",
      ],
      avoids: [
        "uncomfortable tailoring",
        "stiff fabric on long days",
        "anything that has to be earned by the body",
      ],
      hessentialsTranslation:
        "Let comfort look intentional, not accidental.",
    },
    sun: {
      description:
        "Expresses care, memory, protection, and personal history.",
      favors: [
        "pieces with quiet history that get better worn",
        "sentimental staples used carefully",
        "quality you'll actually keep",
      ],
      avoids: [
        "outfits assembled for someone else's eye",
        "discarding pieces that still work",
        "buying past the point of memory",
      ],
      hessentialsTranslation:
        "Let comfort look intentional, not accidental.",
    },
  },

  leo: {
    rising: {
      description:
        "Warm, visible, present. The look needs a point of arrival.",
      favors: [
        "statement outerwear",
        "strong color used with control",
        "one memorable piece per outfit",
      ],
      avoids: [
        "looks that feel apologetic",
        "dull styling",
        "cheap drama",
      ],
      hessentialsTranslation:
        "Presence does not require excess. It requires authorship.",
    },
    moon: {
      description:
        "Needs dignity, recognition, and clothing that does not make the person feel diminished.",
      favors: [
        "well-cut basics that respect the body",
        "beautiful grooming as part of the outfit",
        "clothes that make you feel met",
      ],
      avoids: [
        "anything that flattens presence",
        "ill-fitting essentials",
        "wearing something you have to apologize for",
      ],
      hessentialsTranslation:
        "Presence does not require excess. It requires authorship.",
    },
    sun: {
      description:
        "Expresses authorship, generosity, and a desire to be visibly self-possessed.",
      favors: [
        "elevated basics with presence",
        "signature pieces built to hold the room",
        "quality that doesn't require captioning",
      ],
      avoids: [
        "trend bait",
        "performance dressing",
        "loud pieces with no underlying quality",
      ],
      hessentialsTranslation:
        "Presence does not require excess. It requires authorship.",
    },
  },

  virgo: {
    rising: {
      description:
        "Clean, composed, observant. Details register before volume does.",
      favors: [
        "excellent tailoring",
        "crisp basics",
        "considered detail at the cuff and collar",
      ],
      avoids: [
        "sloppy fit",
        "chaotic prints",
        "garments that need constant fixing",
      ],
      hessentialsTranslation:
        "Refinement is not decoration. It is control of the details.",
    },
    moon: {
      description:
        "Needs order, fit, utility, and clothing that does not create low-grade tension.",
      favors: [
        "pieces that fit precisely",
        "organized color palette",
        "garments that function as designed",
      ],
      avoids: [
        "fabric that pills or wrinkles by lunch",
        "fussy styling that requires babysitting",
        "the wrong size, kept anyway",
      ],
      hessentialsTranslation:
        "Refinement is not decoration. It is control of the details.",
    },
    sun: {
      description:
        "Expresses refinement, precision, usefulness, and quiet discernment.",
      favors: [
        "repeatable silhouettes built well",
        "the wardrobe refined over time, not expanded",
        "useful before decorative",
      ],
      avoids: [
        "buying past your actual rotation",
        "decorative pieces that don't function",
        "perfectionism that prevents wear",
      ],
      hessentialsTranslation:
        "Refinement is not decoration. It is control of the details.",
    },
  },

  libra: {
    rising: {
      description:
        "Polished, graceful, socially intelligent. The look lands through proportion and balance.",
      favors: [
        "balanced proportions",
        "elegant separates",
        "considered accessories used sparingly",
      ],
      avoids: [
        "clashing elements",
        "awkward proportions",
        "outfits that feel unresolved",
      ],
      hessentialsTranslation:
        "Beauty works best when it looks inevitable.",
    },
    moon: {
      description:
        "Needs harmony, beauty, and clothing that feels visually resolved.",
      favors: [
        "soft tailoring",
        "fabric that drapes correctly",
        "outfits that feel finished without being staged",
      ],
      avoids: [
        "visual noise",
        "anything that has to be argued with in the mirror",
        "pieces that fight each other",
      ],
      hessentialsTranslation:
        "Beauty works best when it looks inevitable.",
    },
    sun: {
      description:
        "Expresses taste, relational intelligence, and aesthetic calibration.",
      favors: [
        "a quietly calibrated palette",
        "pieces chosen for proportion over statement",
        "taste that builds without effort to prove it",
      ],
      avoids: [
        "indecision dressed as range",
        "buying out of social pressure",
        "letting taste outsource itself",
      ],
      hessentialsTranslation:
        "Beauty works best when it looks inevitable.",
    },
  },

  scorpio: {
    rising: {
      description:
        "Controlled, private, intense. The look benefits from restraint and depth.",
      favors: [
        "darker palettes",
        "strong silhouettes",
        "minimal but intentional styling",
      ],
      avoids: [
        "bright chaos",
        "trend exposure",
        "anything that reads as eager",
      ],
      hessentialsTranslation: "Let the restraint do the work.",
    },
    moon: {
      description:
        "Needs privacy, emotional armor, and clothing that creates a sense of containment.",
      favors: [
        "fabric with weight",
        "contained tailoring",
        "pieces that feel protective",
      ],
      avoids: [
        "exposing styling that isn't chosen",
        "thin fabric in cold rooms",
        "anything that reads as available",
      ],
      hessentialsTranslation: "Let the restraint do the work.",
    },
    sun: {
      description:
        "Expresses depth, power, focus, and refusal to be overexposed.",
      favors: [
        "investment pieces with depth",
        "restraint as signature",
        "quality that doesn't announce itself",
      ],
      avoids: [
        "logos that explain you",
        "trend cycles",
        "buying for visibility instead of intent",
      ],
      hessentialsTranslation: "Let the restraint do the work.",
    },
  },

  sagittarius: {
    rising: {
      description:
        "Open, energetic, mobile. The look needs ease, movement, and lived-in confidence.",
      favors: [
        "relaxed tailoring",
        "easy layers",
        "shoes that walk and still read intentional",
      ],
      avoids: [
        "outfits that cannot handle real life",
        "restrictive fits",
        "too much polish",
      ],
      hessentialsTranslation:
        "Style should be able to leave the house without asking permission.",
    },
    moon: {
      description:
        "Needs freedom, range, and clothing that does not make the body feel trapped.",
      favors: [
        "travel-ready pieces",
        "fabric that handles weather and dinner",
        "clothes with movement built in",
      ],
      avoids: [
        "precious items that get worn twice",
        "stiff fits",
        "anything you'd resent packing",
      ],
      hessentialsTranslation:
        "Style should be able to leave the house without asking permission.",
    },
    sun: {
      description:
        "Expresses expansion, humor, candor, and appetite for experience.",
      favors: [
        "a wardrobe that travels well",
        "broken-in over staged",
        "pieces that earn their place by being used",
      ],
      avoids: [
        "hoarding pieces for an imagined occasion",
        "buying ahead of an actual life",
        "polish that prevents wear",
      ],
      hessentialsTranslation:
        "Style should be able to leave the house without asking permission.",
    },
  },

  capricorn: {
    rising: {
      description:
        "Composed, serious, capable. The look should signal structure without trying too hard.",
      favors: [
        "strong tailoring",
        "structured outerwear",
        "excellent shoes",
      ],
      avoids: [
        "unserious details",
        "anything that looks temporary",
        "flimsy construction at the surface",
      ],
      hessentialsTranslation: "Build the wardrobe like infrastructure.",
    },
    moon: {
      description:
        "Needs durability, competence, and clothing that feels reliable under pressure.",
      favors: [
        "reliable cuts you don't have to think about",
        "durable fabric",
        "pieces that hold up to long days",
      ],
      avoids: [
        "fussy maintenance",
        "fabric that can't take a meeting",
        "outfits that fall apart by 5pm",
      ],
      hessentialsTranslation: "Build the wardrobe like infrastructure.",
    },
    sun: {
      description:
        "Expresses authority, discipline, longevity, and earned taste.",
      favors: [
        "investment staples chosen once and kept",
        "timeless outerwear",
        "the wardrobe built to outlast trend cycles",
      ],
      avoids: [
        "disposable basics",
        "rotating the closet for novelty",
        "buying status instead of quality",
      ],
      hessentialsTranslation: "Build the wardrobe like infrastructure.",
    },
  },

  aquarius: {
    rising: {
      description:
        "Interesting, cool, slightly removed. The look should have intelligence and a point of difference.",
      favors: [
        "unexpected proportions",
        "architectural pieces",
        "one element that breaks convention",
      ],
      avoids: [
        "trend uniforms",
        "anything too socially obvious",
        "performative dressing",
      ],
      hessentialsTranslation:
        "The difference should look intentional, not performative.",
    },
    moon: {
      description:
        "Needs autonomy, space, and clothing that does not feel socially prescribed.",
      favors: [
        "room to breathe in the silhouette",
        "unusual basics",
        "fabric that doesn't read as borrowed",
      ],
      avoids: [
        "anything you wouldn't choose alone",
        "pieces bought to belong",
        "outfits that feel rented from a moment",
      ],
      hessentialsTranslation:
        "The difference should look intentional, not performative.",
    },
    sun: {
      description:
        "Expresses independence, perspective, and refusal to be overly categorized.",
      favors: [
        "a wardrobe with a point of view",
        "restrained oddity",
        "the difference earned over time, not staged",
      ],
      avoids: [
        "category dressing",
        "buying difference for difference's sake",
        "joining a uniform you don't believe in",
      ],
      hessentialsTranslation:
        "The difference should look intentional, not performative.",
    },
  },

  pisces: {
    rising: {
      description:
        "Soft, fluid, atmospheric. The look reads through mood more than structure.",
      favors: [
        "fluid silhouettes",
        "tonal dressing",
        "gentle layering",
      ],
      avoids: [
        "harsh rigidity",
        "overly sharp styling",
        "anything too literal",
      ],
      hessentialsTranslation: "Let softness have discipline.",
    },
    moon: {
      description:
        "Needs ease, softness, and clothing that does not interrupt emotional or sensory flow.",
      favors: [
        "soft textures",
        "clothes with movement",
        "fabric that doesn't demand attention",
      ],
      avoids: [
        "uncomfortable structure",
        "anything that creates sensory noise",
        "stiff fabric on emotionally heavy days",
      ],
      hessentialsTranslation: "Let softness have discipline.",
    },
    sun: {
      description:
        "Expresses imagination, empathy, permeability, and subtle beauty.",
      favors: [
        "a wardrobe of mood pieces edited well",
        "soft signatures",
        "beauty without insistence",
      ],
      avoids: [
        "drifting into a closet that doesn't function",
        "buying past the point of use",
        "softness without selection",
      ],
      hessentialsTranslation: "Let softness have discipline.",
    },
  },
};
