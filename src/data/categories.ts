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
    label: "Mens",
    subcategories: [
      "shirts",
      "pants",
      "shorts",
      "knitwear",
      "outerwear",
      "footwear",
      "swim",
      "suiting",
      "basics",
    ],
  },
  womens: {
    label: "Womens",
    subcategories: [
      "shirts",
      "pants",
      "dresses",
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
      "belts",
    ],
  },
  grooming: {
    label: "Grooming",
    subcategories: ["hair", "skin", "fragrance", "body", "shaving"],
  },
  home: {
    label: "Home",
    subcategories: [
      "bedding",
      "kitchen",
      "furniture",
      "lighting",
      "bath",
      "stationery",
      "laundry",
      "table",
    ],
  },
  travel: {
    label: "Travel",
    subcategories: ["luggage", "kits", "small-leather-goods"],
  },
  provisions: {
    label: "Provisions",
    subcategories: ["beverages", "pantry", "sundries"],
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

/** "leather-goods" → "Leather Goods". Used for subcategory display. */
export function subcategoryLabel(key: string): string {
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
