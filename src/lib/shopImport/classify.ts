/**
 * Shop import — auto-classifier for category migration.
 *
 * Given an existing product (legacy category + slug + name + brand),
 * propose a (category, subcategory) pair from the new two-level
 * taxonomy in `src/data/categories.ts`.
 *
 * Heuristics, in order of priority:
 *
 *   1. Direct legacy mapping for unambiguous cats (Bags → accessories/bags,
 *      Eyewear → accessories/eyewear, Travel → travel/luggage, etc.).
 *   2. Keyword matching on slug + name to pick a subcategory.
 *   3. Brand allow-list to pick a top-level (most current Apparel is mens
 *      because the inventory is mens-leaning today; this can be tuned per
 *      product in the migration UI).
 *
 * The classifier returns one proposal plus a `confidence` score and a
 * short `note` so the migration UI can surface borderline cases. None
 * of these proposals are written without human review — the migration
 * page is editable per row.
 */

import type { Category } from "../../data/categories";

export type Proposal = {
  category: Category;
  subcategory: string;
  confidence: "high" | "medium" | "low";
  note?: string;
};

export type ClassifierInput = {
  legacyCategory: string;
  slug: string;
  name: string;
  brand: string;
};

/**
 * Word-boundary keyword match. "short-sleeve t-shirt" must NOT match
 * the needle "short" because "short" is a substring of "short-sleeve".
 * We treat hyphens as word boundaries so multi-word kebab slugs work.
 */
const has = (haystack: string, ...needles: string[]): boolean => {
  const tokens = haystack.split(/[\s\-_/]+/).filter(Boolean);
  return needles.some((n) =>
    tokens.some(
      (t) => t === n || t === n + "s" || (n.endsWith("e") && t === n + "d")
    )
  );
};

/** Items obviously sold in a women's market — keep tight, this is editorial. */
const WOMENS_BRANDS = new Set<string>([
  // Reserved for future expansion. Today's inventory has no womens-only
  // brands; the closet is mens-leaning. Add brands here as they ship.
]);

/** Brands whose inventory is unambiguously mens. */
const MENS_BRANDS = new Set<string>([
  "Goodfellow & Co.",
  "Abercrombie",
  "Uniqlo",
  "Massimo Dutti",
]);

function classifyApparel(input: ClassifierInput): Proposal {
  const text = `${input.slug} ${input.name}`.toLowerCase();
  const brand = input.brand;

  let topLevel: Category;
  let topConfidence: Proposal["confidence"];
  if (WOMENS_BRANDS.has(brand)) {
    topLevel = "womens";
    topConfidence = "high";
  } else if (MENS_BRANDS.has(brand)) {
    topLevel = "mens";
    topConfidence = "high";
  } else {
    // No data on the brand — classify as mens by default (matches today's
    // inventory) and flag low-confidence so the editor catches mistakes.
    topLevel = "mens";
    topConfidence = "low";
  }

  // Priority order matters. "short-sleeve t-shirt" tokenizes to tokens
  // including both "short" and "shirt"; we want shirts to win. Tops
  // are checked before shorts/pants for that reason.
  let sub = "shirts";
  if (has(text, "swim", "trunk")) sub = "swim";
  else if (has(text, "tee", "shirt", "tank", "polo", "henley", "oxford"))
    sub = "shirts";
  else if (has(text, "sweater", "knit", "cardigan", "merino", "cashmere"))
    sub = "knitwear";
  else if (has(text, "jacket", "coat", "parka", "blazer", "outer"))
    sub = "outerwear";
  else if (has(text, "suit", "tuxedo")) sub = "suiting";
  else if (has(text, "dress")) sub = "dresses";
  else if (has(text, "jean", "trouser", "chino", "pant", "slack")) sub = "pants";
  else if (has(text, "short")) sub = "shorts";

  return {
    category: topLevel,
    subcategory: sub,
    confidence: topConfidence,
    note: topConfidence === "low" ? "Mens by default — confirm." : undefined,
  };
}

function classifyWatchesJewelry(input: ClassifierInput): Proposal {
  const text = `${input.slug} ${input.name}`.toLowerCase();
  if (has(text, "bracelet", "necklace", "ring", "earring", "pendant", "chain")) {
    return {
      category: "accessories",
      subcategory: "jewelry",
      confidence: "high",
    };
  }
  return {
    category: "accessories",
    subcategory: "watches",
    confidence: "high",
  };
}

function classifyHome(input: ClassifierInput): Proposal {
  const text = `${input.slug} ${input.name}`.toLowerCase();
  if (has(text, "blanket", "pillow", "sheet", "duvet", "comforter", "bed")) {
    return { category: "home", subcategory: "bedding", confidence: "high" };
  }
  if (has(text, "table", "chair", "sofa", "stool", "shelf", "desk", "bench")) {
    return { category: "home", subcategory: "furniture", confidence: "high" };
  }
  if (has(text, "lamp", "light", "sconce", "pendant", "lantern")) {
    return { category: "home", subcategory: "lighting", confidence: "high" };
  }
  if (
    has(text, "daybook", "notebook", "journal", "paper", "pen", "pencil", "card")
  ) {
    return { category: "home", subcategory: "stationery", confidence: "high" };
  }
  if (has(text, "dryer", "washer", "laundry", "iron")) {
    return { category: "home", subcategory: "laundry", confidence: "high" };
  }
  if (has(text, "knife", "pan", "pot", "kettle", "kitchen", "chef")) {
    return { category: "home", subcategory: "kitchen", confidence: "high" };
  }
  if (has(text, "towel", "bath", "shower", "tub")) {
    return { category: "home", subcategory: "bath", confidence: "high" };
  }
  if (has(text, "plate", "bowl", "glass", "tableware", "carafe", "candle")) {
    return { category: "home", subcategory: "table", confidence: "high" };
  }
  return {
    category: "home",
    subcategory: "bedding",
    confidence: "low",
    note: "Defaulted to bedding — confirm.",
  };
}

function classifyGrooming(input: ClassifierInput): Proposal {
  const text = `${input.slug} ${input.name}`.toLowerCase();
  if (
    has(text, "edt", "edp", "eau de", "fragrance", "cologne", "perfume", "parfum")
  ) {
    return { category: "grooming", subcategory: "fragrance", confidence: "high" };
  }
  if (has(text, "shave", "razor", "shaving")) {
    return { category: "grooming", subcategory: "shaving", confidence: "high" };
  }
  if (
    has(
      text,
      "hair",
      "pomade",
      "clay",
      "shampoo",
      "conditioner",
      "wax",
      "gel",
      "grooming"
    )
  ) {
    // "clay" / "cream" can be hair OR skin — context matters. The Aveda
    // products are explicitly "Pure-Formance Grooming" → hair.
    if (has(text, "eye", "face", "moisturizer", "serum")) {
      return { category: "grooming", subcategory: "skin", confidence: "high" };
    }
    return { category: "grooming", subcategory: "hair", confidence: "high" };
  }
  if (has(text, "eye", "face", "moisturizer", "serum", "cleanser", "toner")) {
    return { category: "grooming", subcategory: "skin", confidence: "high" };
  }
  if (has(text, "soap", "wash", "lotion", "body")) {
    return { category: "grooming", subcategory: "body", confidence: "high" };
  }
  return {
    category: "grooming",
    subcategory: "body",
    confidence: "low",
    note: "Defaulted to body — confirm.",
  };
}

function classifyProvisions(input: ClassifierInput): Proposal {
  const text = `${input.slug} ${input.name}`.toLowerCase();
  if (
    has(text, "water", "coffee", "tea", "wine", "beer", "spirit", "tonic", "soda")
  ) {
    return { category: "provisions", subcategory: "beverages", confidence: "high" };
  }
  return {
    category: "provisions",
    subcategory: "pantry",
    confidence: "medium",
  };
}

function classifyFootwear(input: ClassifierInput): Proposal {
  // Today's inventory is unisex Birkenstocks. Default to mens/footwear;
  // editor can switch to womens or accessories on review.
  void input;
  return {
    category: "mens",
    subcategory: "footwear",
    confidence: "low",
    note: "Mens/footwear by default — confirm gender.",
  };
}

function classifyEyewear(input: ClassifierInput): Proposal {
  void input;
  return {
    category: "accessories",
    subcategory: "eyewear",
    confidence: "high",
  };
}

function classifyTravel(input: ClassifierInput): Proposal {
  const text = `${input.slug} ${input.name}`.toLowerCase();
  if (has(text, "carry", "suitcase", "trunk", "duffel", "luggage")) {
    return { category: "travel", subcategory: "luggage", confidence: "high" };
  }
  return {
    category: "travel",
    subcategory: "luggage",
    confidence: "medium",
  };
}

function classifyBags(input: ClassifierInput): Proposal {
  void input;
  return {
    category: "accessories",
    subcategory: "bags",
    confidence: "high",
  };
}

/**
 * Top-level dispatcher. The legacy category drives the route; if a
 * product carries a category we don't recognize, fall back to a
 * low-confidence accessories/bags guess so the editor sees the row
 * flagged.
 */
export function classifyProduct(input: ClassifierInput): Proposal {
  switch (input.legacyCategory) {
    case "Apparel":
      return classifyApparel(input);
    case "Footwear":
      return classifyFootwear(input);
    case "Bags":
      return classifyBags(input);
    case "Watches & Jewelry":
      return classifyWatchesJewelry(input);
    case "Eyewear":
      return classifyEyewear(input);
    case "Travel":
      return classifyTravel(input);
    case "Home":
      return classifyHome(input);
    case "Grooming":
      return classifyGrooming(input);
    case "Provisions":
      return classifyProvisions(input);
    default:
      return {
        category: "accessories",
        subcategory: "bags",
        confidence: "low",
        note: `Unknown legacy category "${input.legacyCategory}".`,
      };
  }
}
