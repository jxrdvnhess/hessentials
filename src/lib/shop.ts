import fs from "node:fs/promises";
import path from "node:path";
import { parseFrontmatter, markdownToHtml } from "./living";

const ESSAY_DIR = path.join(process.cwd(), "content", "shop", "essays");

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
