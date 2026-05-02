/**
 * Shop import — image downloader.
 *
 * Per the shop convention, every product's gallery lives at
 * `/public/shop/<slug>-N.jpg`, primary first. This module fetches the
 * remote image bytes, normalizes them to JPEG via sharp, and writes
 * to disk under the slug-based names.
 *
 * Sharp is shipped transitively by Next.js for /image processing, so
 * it's always available at runtime. We avoid converting transparent
 * PNG/WebP backgrounds aesthetically by flattening on a white canvas
 * — product photography is conventionally on white anyway.
 *
 * Failure mode: a single image fetch failing does NOT abort the rest.
 * The caller gets back a list of saved paths in source order, with
 * `null` slots where a download failed.
 */

import fs from "node:fs/promises";
import path from "node:path";
import sharp from "sharp";

const PUBLIC_SHOP_DIR = path.join(process.cwd(), "public", "shop");
const FETCH_TIMEOUT_MS = 12000;

export type SavedImage = {
  /** The source remote URL. */
  source: string;
  /** Path under /public, ready to drop into shop.ts. e.g. "/shop/foo-1.jpg" */
  publicPath: string;
};

export type SaveResult = {
  saved: SavedImage[];
  /** Source URLs that failed, in input order. */
  failed: { source: string; error: string }[];
};

async function downloadOne(url: string): Promise<Buffer> {
  const res = await fetch(url, {
    headers: {
      "User-Agent":
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
      Accept: "image/*",
    },
    signal: AbortSignal.timeout(FETCH_TIMEOUT_MS),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`Image HTTP ${res.status}`);
  }
  const buf = Buffer.from(await res.arrayBuffer());
  if (buf.byteLength < 1024) {
    throw new Error(`Image too small (${buf.byteLength} bytes)`);
  }
  return buf;
}

async function normalizeToJpeg(input: Buffer): Promise<Buffer> {
  // Flatten on white so PNG / WebP transparency doesn't render as black
  // when re-encoded to JPEG. Product photography is conventionally white.
  return sharp(input)
    .rotate() // honor EXIF orientation
    .flatten({ background: "#ffffff" })
    .jpeg({ quality: 88, mozjpeg: true })
    .toBuffer();
}

/**
 * Download every image in `sources`, save under
 * `/public/shop/<slug>-{1..N}.jpg`. Returns the resulting public paths
 * in input order, with failures collected separately.
 *
 * `slug` is trusted — the caller is expected to have run it through
 * `buildSlug`/`ensureUnique` already. We still resolve the final path
 * with `path.resolve` and assert it stays inside PUBLIC_SHOP_DIR.
 */
export async function saveImagesForSlug(
  slug: string,
  sources: string[]
): Promise<SaveResult> {
  await fs.mkdir(PUBLIC_SHOP_DIR, { recursive: true });

  const saved: SavedImage[] = [];
  const failed: { source: string; error: string }[] = [];

  // Sequential — these endpoints often rate-limit, and three to five
  // images per product is cheap to fetch in series.
  let writeIndex = 1;
  for (const src of sources) {
    try {
      const raw = await downloadOne(src);
      const jpeg = await normalizeToJpeg(raw);
      const fileName = `${slug}-${writeIndex}.jpg`;
      const fullPath = path.join(PUBLIC_SHOP_DIR, fileName);
      const resolved = path.resolve(fullPath);
      if (!resolved.startsWith(path.resolve(PUBLIC_SHOP_DIR) + path.sep)) {
        throw new Error("Refusing to write outside /public/shop");
      }
      await fs.writeFile(resolved, jpeg);
      saved.push({ source: src, publicPath: `/shop/${fileName}` });
      writeIndex += 1;
    } catch (e) {
      failed.push({
        source: src,
        error: e instanceof Error ? e.message : String(e),
      });
    }
  }

  return { saved, failed };
}
