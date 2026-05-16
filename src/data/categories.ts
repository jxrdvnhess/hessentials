/**
 * Hessentials Shop — category tree.
 *
 * Two-level taxonomy:
 *
 *   <category>
 *     <subcategory>
 *
 * Source of truth for both the public shop filter and the admin
 * import/edit forms. Add a new top-level by editing this file and
 * running typecheck — the data file's `category` field is closed-world
 * via the union type derived below.
 *
 * Subcategories are open by intent: the form lets you type any string,
 * with autocomplete from the canonical list here. New subcategories
 * persist on the product itself; the canonical list is the editorial
 * default. To formalize a new subcategory's order or label, edit it
 * here directly.
 *
 * Keys are lowercase kebab. Display goes through `LABEL` map below.
 */

export type CategoryDef = {
  label: string;
  subcategories: readonly string[];
};

/**
 * Edit this object to add / reorder / rename categories.
 *
 * `as const satisfies` gives a closed-world `Category` union type
 * derived from the keys here. Any new top-level requires a typecheck
 * pass on shop.ts after the migration runs.
 */
export const CATEGORY_TREE = {
  mens: {
    label: "Men",
    /**
     * 2026-05-16: `basics` removed — too broad to filter usefully.
     * The wardrobe-basics intent now lives in the "Quiet Uniform"
     * atmosphere collection (cuts across categories). Tees and tanks
     * get their own subcategory; everything else top-related without
     * being outerwear sits under `shirts`.
     */
    subcategories: [
      "shirts",
      "t-shirts-and-tanks",
      "pants",
      "shorts",
      "knitwear",
      "outerwear",
      "footwear",
      "swim",
      "suiting",
    ],
  },
  womens: {
    label: "Women",
    /**
     * 2026-05-16: `basics` and `shirts` removed. Women's tops break
     * along the same logic as men's: t-shirts and tanks get their
     * own subcategory; the rest go under `tops`. We don't carry a
     * "shirts" sub here because in editorial use women's tops are
     * rarely button-up shirts — the category drifts toward blouses,
     * twist tops, halter tops, etc.
     */
    subcategories: [
      "tops",
      "t-shirts-and-tanks",
      "pants",
      "dresses",
      "skirts",
      "knitwear",
      "outerwear",
      "footwear",
      "swim",
    ],
  },
  accessories: {
    label: "Accessories",
    subcategories: [
      "bags",
      "eyewear",
      "watches",
      "jewelry",
      "leather-goods",
      "hats",
      "scarves",
      "belts",
      "socks",
    ],
  },
  grooming: {
    label: "Grooming",
    subcategories: ["hair", "skin", "fragrance", "body", "shaving"],
  },
  home: {
    label: "Home",
    /**
     * Trimmed 2026-05-16 — `kitchen`, `glassware`, `dinnerware`,
     * `serveware`, `vessels` moved to `cooking` per Chateau's
     * lived-object directive. The home parent now reads as
     * "everything that's not a cooking object or a personal-care
     * item." `candles` added as a real canonical sub.
     */
    subcategories: [
      "bedding",
      "bath",
      "furniture",
      "lighting",
      "table",
      "table-linens",
      "stationery",
      "laundry",
      "hardware",
      "storage",
      "entryway",
      "candles",
    ],
  },
  cooking: {
    label: "Cooking",
    /**
     * Lived-object category — see `data/sourcing-policy.md`. Cuts
     * across the old `home/kitchen` and `provisions/pantry` from the
     * department-store taxonomy. Earns first-class status because
     * the archive thinks in terms of how objects are used at the
     * counter, not which retail floor they'd sit on.
     *
     * `dinnerware` / `glassware` / `serveware` added 2026-05-16 as
     * the table-objects bucket migrated out of `home`.
     */
    subcategories: [
      "prep",
      "coffee",
      "picnic",
      "pantry",
      "ceramics",
      "tools",
      "salt-cellar",
      "countertop-vessels",
      "dinnerware",
      "glassware",
      "serveware",
    ],
  },
  travel: {
    label: "Travel",
    subcategories: [
      "luggage",
      "kits",
      "small-leather-goods",
      "bags",
      "organization",
      "drinkware",
      "outdoor",
      "totes",
    ],
  },
  provisions: {
    label: "Provisions",
    subcategories: [
      "beverages",
      "pantry",
      "sundries",
      "salt",
      "spices",
      "water",
      "tea",
    ],
  },
} as const satisfies Record<string, CategoryDef>;

/** Closed-world category union derived from the tree keys. */
export type Category = keyof typeof CATEGORY_TREE;

/**
 * Subcategory is intentionally `string` — the canonical list above is
 * the editorial default but new subcategories can be created at order
 * entry. Validation against the canonical list is advisory, not strict.
 */
export type Subcategory = string;

/** Display order for the public filter row and admin pickers. */
export const CATEGORY_KEYS: readonly Category[] = Object.keys(
  CATEGORY_TREE
) as Category[];

/** "mens" → "Mens", etc. Falls back to the key Title Cased. */
export function categoryLabel(key: string): string {
  if (key in CATEGORY_TREE) {
    return CATEGORY_TREE[key as Category].label;
  }
  return key.charAt(0).toUpperCase() + key.slice(1);
}

/**
 * Subcategory labels that need to deviate from the
 * kebab-case → title-case default. Add to this map whenever a
 * subcategory key would render awkwardly under the default rule.
 *
 * Convention: use "&" instead of the word "and" in display. Keys
 * stay kebab-case so URLs stay clean; only the rendered label uses
 * the ampersand. Examples below.
 */
const SUBCATEGORY_LABELS: Readonly<Record<string, string>> = {
  "t-shirts-and-tanks": "T Shirts & Tanks",
};

/**
 * "leather-goods" → "Leather Goods". Used for subcategory display.
 *
 * Looks up `SUBCATEGORY_LABELS` first so the editorial overrides
 * (ampersands, special casing) win over the mechanical title-case
 * pass. Falls through to title-case-from-key otherwise.
 */
export function subcategoryLabel(key: string): string {
  if (key in SUBCATEGORY_LABELS) return SUBCATEGORY_LABELS[key];
  return key
    .split("-")
    .map((s) => (s ? s.charAt(0).toUpperCase() + s.slice(1) : s))
    .join(" ");
}

/** Returns the canonical subcategories for a category, or [] if unknown. */
export function subcategoriesFor(
  category: string
): readonly string[] {
  if (category in CATEGORY_TREE) {
    return CATEGORY_TREE[category as Category].subcategories;
  }
  return [];
}
