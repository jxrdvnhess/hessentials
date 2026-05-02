/**
 * Shop import — SSE preview endpoint.
 *
 * GET /api/admin/shop-import/preview?url=<encoded-url>
 *
 * Streams events as the source URL is fetched, parsed, and probed:
 *
 *   event: phase     data: { phase: "fetching" }
 *   event: parsed    data: { name, brand, prices, soldOut, images, extractionMethod, host, priceRange, slug }
 *   event: image-ok  data: { index, source, contentType, bytes }
 *   event: image-err data: { index, source, error }
 *   event: done      data: {}
 *   event: error     data: { error }
 *
 * The image-ok / image-err events come in source order so the client can
 * paint thumbnail tiles live. They confirm reachability — they do NOT
 * download to disk. Disk writes happen in /commit.
 *
 * Dev-only. Returns 403 in production.
 */

import { NextRequest } from "next/server";
import { extractProduct } from "../../../../../lib/shopImport/extract";
import { suggestPriceRange } from "../../../../../lib/shopImport/formatPriceRange";
import {
  buildSlug,
  ensureUnique,
} from "../../../../../lib/shopImport/slug";
import { readExistingSlugs } from "../../../../../lib/shopImport/writeEntry";

export const dynamic = "force-dynamic";

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

function sseEvent(event: string, data: unknown): string {
  return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
}

async function probeImage(
  index: number,
  source: string,
  controller: ReadableStreamDefaultController<Uint8Array>,
  encoder: TextEncoder
): Promise<void> {
  try {
    const res = await fetch(source, {
      method: "HEAD",
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
      },
      signal: AbortSignal.timeout(6000),
    });
    if (!res.ok) {
      // Some CDNs reject HEAD — fall back to a ranged GET.
      const ranged = await fetch(source, {
        method: "GET",
        headers: {
          Range: "bytes=0-1023",
          "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        },
        signal: AbortSignal.timeout(6000),
      });
      if (!ranged.ok) throw new Error(`HTTP ${res.status}`);
      controller.enqueue(
        encoder.encode(
          sseEvent("image-ok", {
            index,
            source,
            contentType: ranged.headers.get("content-type") ?? "",
            bytes: Number(ranged.headers.get("content-length")) || null,
          })
        )
      );
      return;
    }
    controller.enqueue(
      encoder.encode(
        sseEvent("image-ok", {
          index,
          source,
          contentType: res.headers.get("content-type") ?? "",
          bytes: Number(res.headers.get("content-length")) || null,
        })
      )
    );
  } catch (e) {
    controller.enqueue(
      encoder.encode(
        sseEvent("image-err", {
          index,
          source,
          error: e instanceof Error ? e.message : String(e),
        })
      )
    );
  }
}

export async function GET(req: NextRequest): Promise<Response> {
  if (isProd()) {
    return new Response("Not available in production", { status: 403 });
  }

  const url = req.nextUrl.searchParams.get("url");
  if (!url) {
    return new Response("Missing ?url=", { status: 400 });
  }
  try {
    new URL(url);
  } catch {
    return new Response("Malformed url", { status: 400 });
  }

  const encoder = new TextEncoder();

  const stream = new ReadableStream<Uint8Array>({
    async start(controller) {
      const send = (event: string, data: unknown) =>
        controller.enqueue(encoder.encode(sseEvent(event, data)));

      try {
        send("phase", { phase: "fetching" });
        const extracted = await extractProduct(url);

        const existing = await readExistingSlugs();
        const slug = ensureUnique(
          buildSlug(extracted.brand, extracted.name),
          existing
        );

        send("parsed", {
          ...extracted,
          slug,
          priceRange: suggestPriceRange(extracted.prices),
          slugCollision: existing.has(buildSlug(extracted.brand, extracted.name)),
        });

        // Probe images sequentially — preserves index order, gentle
        // on rate-limited CDNs.
        for (let i = 0; i < extracted.images.length; i += 1) {
          await probeImage(i, extracted.images[i], controller, encoder);
        }

        send("done", {});
      } catch (e) {
        send("error", {
          error: e instanceof Error ? e.message : String(e),
        });
      } finally {
        controller.close();
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
      // The Next dev server doesn't buffer SSE by default; this is a
      // belt-and-suspenders header for proxy setups.
      "X-Accel-Buffering": "no",
    },
  });
}
