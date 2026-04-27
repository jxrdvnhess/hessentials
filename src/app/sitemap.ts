import type { MetadataRoute } from "next";
import fs from "node:fs/promises";
import path from "node:path";
import { recipes } from "../data/recipes";
import { STYLE_ARTICLES } from "../data/style";
import { SHOP_PRODUCTS } from "../data/shop";

const SITE = "https://hessentials.co";

/**
 * Build-time sitemap generator. Combines:
 *   - Static top-level pages
 *   - Dynamic routes from data sources (recipes, style, shop)
 *   - Living articles from the /content/living markdown directory
 *
 * Output served by Next.js at /sitemap.xml.
 */
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const now = new Date();

  // ---------- Static pages ----------
  // Inner array is typed against the Sitemap entry shape so each
  // `changeFrequency` value narrows to the literal union expected by
  // Next's MetadataRoute.Sitemap (rather than widening to `string`).
  type StaticEntry = Omit<MetadataRoute.Sitemap[number], "lastModified">;
  const staticEntries: StaticEntry[] = [
    { url: `${SITE}/`, priority: 1.0, changeFrequency: "monthly" },
    { url: `${SITE}/home`, priority: 1.0, changeFrequency: "weekly" },
    { url: `${SITE}/about`, priority: 0.8, changeFrequency: "yearly" },
    { url: `${SITE}/aurelian`, priority: 0.8, changeFrequency: "monthly" },
    { url: `${SITE}/recipes`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${SITE}/living`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${SITE}/style`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${SITE}/shop`, priority: 0.9, changeFrequency: "weekly" },
    { url: `${SITE}/privacy`, priority: 0.3, changeFrequency: "yearly" },
    { url: `${SITE}/terms`, priority: 0.3, changeFrequency: "yearly" },
    {
      url: `${SITE}/affiliate-disclosure`,
      priority: 0.3,
      changeFrequency: "yearly",
    },
  ];
  const staticRoutes: MetadataRoute.Sitemap = staticEntries.map((entry) => ({
    ...entry,
    lastModified: now,
  }));

  // ---------- Dynamic — recipes ----------
  const recipeRoutes: MetadataRoute.Sitemap = recipes.map((r) => ({
    url: `${SITE}/recipes/${r.slug}`,
    lastModified: now,
    priority: 0.7,
    changeFrequency: "monthly",
  }));

  // ---------- Dynamic — style ----------
  const styleRoutes: MetadataRoute.Sitemap = STYLE_ARTICLES.map((a) => ({
    url: `${SITE}/style/${a.slug}`,
    lastModified: now,
    priority: 0.7,
    changeFrequency: "monthly",
  }));

  // ---------- Dynamic — shop products ----------
  const shopRoutes: MetadataRoute.Sitemap = SHOP_PRODUCTS.map((p) => ({
    url: `${SITE}/shop/${p.slug}`,
    lastModified: now,
    priority: 0.6,
    changeFrequency: "monthly",
  }));

  // ---------- Dynamic — living articles (from /content/living/*.md) ----------
  let livingSlugs: string[] = [];
  try {
    const livingDir = path.join(process.cwd(), "content", "living");
    const entries = await fs.readdir(livingDir);
    livingSlugs = entries
      .filter((file) => file.endsWith(".md"))
      .map((file) => file.replace(/\.md$/, ""));
  } catch {
    // Directory missing or unreadable at build time — ship without these.
  }
  const livingRoutes: MetadataRoute.Sitemap = livingSlugs.map((slug) => ({
    url: `${SITE}/living/${slug}`,
    lastModified: now,
    priority: 0.7,
    changeFrequency: "monthly",
  }));

  return [
    ...staticRoutes,
    ...recipeRoutes,
    ...styleRoutes,
    ...shopRoutes,
    ...livingRoutes,
  ];
}
