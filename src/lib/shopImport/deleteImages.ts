/**
 * Shop import — image cleanup utility.
 *
 * Removes every `/public/shop/<slug>-N.<ext>` file for a given slug.
 * Used by the delete endpoint and (later) by the edit page when an
 * image is removed from a product.
 *
 * Path-traversal guard: every resolved path must stay inside
 * `/public/shop`. We refuse to unlink anything outside that tree.
 */

import fs from "node:fs/promises";
import path from "node:path";

const PUBLIC_SHOP_DIR = path.join(process.cwd(), "public", "shop");

/** Matches `<slug>-1.jpg`, `<slug>-12.png`, etc. Anchored at both ends. */
function matchesSlug(slug: string, fileName: string): boolean {
  const escaped = slug.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  return new RegExp(`^${escaped}-\\d+\\.(?:jpg|jpeg|png|webp|avif)$`, "i").test(
    fileName
  );
}

export async function deleteImagesForSlug(slug: string): Promise<string[]> {
  if (!/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(slug)) {
    throw new Error(`Refusing to delete with malformed slug: ${slug}`);
  }
  let entries: string[];
  try {
    entries = await fs.readdir(PUBLIC_SHOP_DIR);
  } catch {
    return [];
  }
  const deleted: string[] = [];
  const dirReal = path.resolve(PUBLIC_SHOP_DIR) + path.sep;
  for (const entry of entries) {
    if (!matchesSlug(slug, entry)) continue;
    const full = path.resolve(path.join(PUBLIC_SHOP_DIR, entry));
    if (!full.startsWith(dirReal)) continue;
    try {
      await fs.unlink(full);
      deleted.push(`/shop/${entry}`);
    } catch {
      // Don't abort the loop — a missing file is fine.
    }
  }
  return deleted;
}
