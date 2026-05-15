import fs from "node:fs/promises";
import path from "node:path";
import { parseFrontmatter, markdownToHtml } from "./living";
import {
  CATEGORY_TREE,
  SHOP_PRODUCTS,
  type Category,
  type ShopProduct,
} from "../data/shop";

const ESSAY_DIR = path.join(process.cwd(), "content", "shop", "essays");

/* ---------- Pillar filtering ---------- */

/**
 * Pillars whose membership extends through the audience field.
 * `/shop/mens` shows products with `category === "mens"` OR
 * `audience.includes("mens")`. Same for womens. All other pillars
 * filter strictly by category.
 *
 * The set is closed-world to "mens" / "womens" so the rule doesn't
 * silently broaden if a third audience tag ever lands in the data.
 */
const AUDIENCE_PILLARS = new Set<Category>(["mens", "womens"]);

/**
 * The public-facing list. Drops anything marked `draft: true` — those
 * entries are mechanically staged by the bulk import flow and live
 * only inside /admin/shop-drafts until a human promotes them.
 *
 * Every public read path should source from this, not from
 * SHOP_PRODUCTS directly.
 */
export const LIVE_PRODUCTS: readonly ShopProduct[] = SHOP_PRODUCTS.filter(
  (p) => p.draft !== true
);

/**
 * Return the products that belong to a pillar.
 *
 * For mens / womens: the union of `category === pillar` and any
 * product whose `audience` array includes that pillar — powers the
 * cross-pillar listing (e.g. a tote tagged for both mens and womens
 * surfaces in both routes without being duplicated in the data).
 *
 * Source order is preserved so curated arrangements in shop.ts
 * carry through. Drafts are excluded — see LIVE_PRODUCTS.
 */
export function productsForPillar(pillar: Category): ShopProduct[] {
  if (AUDIENCE_PILLARS.has(pillar)) {
    return LIVE_PRODUCTS.filter(
      (p) =>
        p.category === pillar ||
        (p.audience ?? []).includes(pillar as "mens" | "womens")
    );
  }
  return LIVE_PRODUCTS.filter((p) => p.category === pillar);
}

/** Pillar membership + subcategory match (case-insensitive). */
export function productsForSubcategory(
  pillar: Category,
  subcategory: string
): ShopProduct[] {
  const sub = subcategory.toLowerCase();
  return productsForPillar(pillar).filter(
    (p) => (p.subcategory ?? "").toLowerCase() === sub
  );
}

/**
 * Distinct subcategories present under a pillar, in canonical order
 * (CATEGORY_TREE first, then any extras observed on products).
 * Used by the drill-down hero on `/shop/[pillar]`.
 */
export function subcategoriesPresentForPillar(
  pillar: Category
): string[] {
  const products = productsForPillar(pillar);
  const present = new Set<string>(
    products.map((p) => p.subcategory ?? "").filter((s) => s.length > 0)
  );
  const canonical = CATEGORY_TREE[pillar]?.subcategories ?? [];
  const ordered: string[] = [];
  for (const s of canonical) if (present.has(s)) ordered.push(s);
  for (const s of present)
    if (!(canonical as readonly string[]).includes(s)) ordered.push(s);
  return ordered;
}

/* ---------- Atmosphere collections ---------- */

/**
 * Return every live product whose `atmosphereCollection` array
 * contains the given atmosphere name (case-insensitive). Atmosphere
 * collections cut across operational categories — a single atmosphere
 * page mixes Home + Cooking + Travel + Mens + Womens + etc., curated
 * by emotional weather rather than retail taxonomy.
 */
export function productsForAtmosphere(atmosphere: string): ShopProduct[] {
  const target = atmosphere.toLowerCase();
  return LIVE_PRODUCTS.filter((p) =>
    (p.atmosphereCollection ?? []).some(
      (a) => a.toLowerCase() === target
    )
  );
}

/**
 * Pick a representative image for an atmosphere card on the homepage.
 * First product in the atmosphere with a populated `image`. Returns
 * undefined for empty atmospheres — callers should skip those.
 */
export function representativeImageForAtmosphere(
  atmosphere: string
): string | undefined {
  return productsForAtmosphere(atmosphere).find((p) => p.image)?.image;
}

export type ShopEssay = {
  /** The product slug this essay belongs to. */
  slug: string;
  /** Optional override headline. Falls back to product name on the page. */
  title?: string;
  /** Rendered HTML body. */
  html: string;
};

/**
 * Look up an editorial essay for a given product slug.
 *
 * Essays are markdown files at `content/shop/essays/<slug>.md`. They are
 * optional — products without an essay still render with the basic info
 * (image, brand, reason, CTA), the page just gets shorter.
 */
export async function getShopEssay(
  slug: string
): Promise<ShopEssay | null> {
  try {
    const filePath = path.join(ESSAY_DIR, `${slug}.md`);
    const source = await fs.readFile(filePath, "utf8");
    const { data, content } = parseFrontmatter(source);
    return {
      slug,
      title: data.title || undefined,
      html: markdownToHtml(content),
    };
  } catch {
    return null;
  }
}
