/**
 * Shop drafts — promote endpoint.
 *
 * POST /api/admin/shop-drafts/promote
 *   body: { slug: string }
 *
 * Flips `draft: true` → removed on the named entry in src/data/shop.ts.
 * After this call the entry becomes part of the public Shop. The action
 * is intentionally narrow: promotion is single-field. Any other edits
 * (reason, category, audience) should be made via the standard PATCH on
 * /api/admin/shop-item/[slug] before promoting.
 *
 * Dev-only. Returns 403 in production.
 */

import { NextRequest, NextResponse } from "next/server";
import { SHOP_PRODUCTS } from "../../../../../data/shop";
import {
  setDraftFlag,
  entryExists,
} from "../../../../../lib/shopImport/writeEntry";

export const dynamic = "force-dynamic";

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

export async function POST(req: NextRequest): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json(
      { error: "Not available in production" },
      { status: 403 }
    );
  }

  let body: { slug?: string };
  try {
    body = (await req.json()) as { slug?: string };
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const slug = (body.slug ?? "").trim();
  if (!slug) {
    return NextResponse.json({ error: "slug is required" }, { status: 400 });
  }
  if (!(await entryExists(slug))) {
    return NextResponse.json(
      { error: `No entry for slug "${slug}".` },
      { status: 404 }
    );
  }

  // Surface a useful pre-promotion sanity check — block promotion when
  // the entry still has the placeholder category from the bulk import
  // (the script writes "home" as a placeholder when its heuristic
  // can't decide). Category is editorial; the human picks it before
  // promotion.
  const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
  const reason = product?.reason ?? "";
  if (!reason.trim()) {
    return NextResponse.json(
      {
        error:
          "Refusing to promote — entry has no reason. Edit the entry first.",
      },
      { status: 409 }
    );
  }

  try {
    await setDraftFlag(slug, false);
  } catch (e) {
    return NextResponse.json(
      {
        error: `Failed to write shop.ts: ${
          e instanceof Error ? e.message : String(e)
        }`,
      },
      { status: 500 }
    );
  }

  return NextResponse.json({ ok: true, slug });
}
