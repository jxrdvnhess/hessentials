/**
 * Category migration — batch apply.
 *
 * GET  /api/admin/migrate-categories  → returns proposals for every product
 * POST /api/admin/migrate-categories  → applies the supplied (slug, category, subcategory)
 *                                       triples to shop.ts, one replaceShopEntry per row
 *
 * The POST body is an array — each row carries the new (category,
 * subcategory) for the slug. We re-build a NewShopEntry from the
 * runtime SHOP_PRODUCTS state, swap the two fields, and call
 * replaceShopEntry. All rows are applied in one pass; if any single
 * row fails we abort and return what we wrote so the operator can
 * inspect.
 *
 * Dev-only — 403 in production. shop.ts only exists in the repo;
 * mutating it on a deployed server is meaningless.
 */

import { NextRequest, NextResponse } from "next/server";
import { CATEGORY_KEYS, type Category } from "../../../../data/categories";
import { SHOP_PRODUCTS } from "../../../../data/shop";
import {
  classifyProduct,
  type Proposal,
} from "../../../../lib/shopImport/classify";
import {
  replaceShopEntry,
  type NewShopEntry,
} from "../../../../lib/shopImport/writeEntry";

export const dynamic = "force-dynamic";

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

type Row = {
  slug: string;
  brand: string;
  name: string;
  legacyCategory: string;
  /** Already-migrated rows return their current values here. */
  currentCategory: string;
  currentSubcategory: string;
  /** Auto-classifier proposal (only meaningful when currentSubcategory is empty). */
  proposal: Proposal;
  /** True iff currentCategory is one of the new top-levels. */
  migrated: boolean;
};

export async function GET(): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json({ error: "Not available" }, { status: 403 });
  }

  const newKeys = new Set<string>(CATEGORY_KEYS);
  const rows: Row[] = SHOP_PRODUCTS.map((p) => {
    const migrated = newKeys.has(p.category);
    const proposal = classifyProduct({
      legacyCategory: p.category,
      slug: p.slug,
      name: p.name,
      brand: p.brand,
    });
    return {
      slug: p.slug,
      brand: p.brand,
      name: p.name,
      legacyCategory: p.category,
      currentCategory: p.category,
      currentSubcategory: p.subcategory ?? "",
      proposal,
      migrated,
    };
  });

  return NextResponse.json({
    rows,
    categoryKeys: [...CATEGORY_KEYS],
  });
}

type ApplyBody = {
  changes?: Array<{
    slug: string;
    category: string;
    subcategory: string;
  }>;
};

export async function POST(req: NextRequest): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json({ error: "Not available" }, { status: 403 });
  }

  let body: ApplyBody;
  try {
    body = (await req.json()) as ApplyBody;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const changes = Array.isArray(body.changes) ? body.changes : [];
  if (!changes.length) {
    return NextResponse.json(
      { error: "No changes supplied" },
      { status: 400 }
    );
  }

  const newKeys = new Set<string>(CATEGORY_KEYS);
  const written: string[] = [];
  for (const change of changes) {
    const slug = change.slug?.trim();
    const category = change.category?.trim();
    const subcategory = change.subcategory?.trim();
    if (!slug || !category) {
      return NextResponse.json(
        {
          error: `Bad row: ${JSON.stringify(change)}`,
          written,
        },
        { status: 400 }
      );
    }
    if (!newKeys.has(category)) {
      return NextResponse.json(
        {
          error: `category "${category}" is not in CATEGORY_TREE`,
          written,
        },
        { status: 400 }
      );
    }
    if (subcategory && !/^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$/.test(subcategory)) {
      return NextResponse.json(
        {
          error: `subcategory "${subcategory}" must be lowercase kebab-case`,
          written,
        },
        { status: 400 }
      );
    }

    const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
    if (!product) {
      return NextResponse.json(
        { error: `Unknown slug: ${slug}`, written },
        { status: 404 }
      );
    }

    // Skip if both fields already equal what we'd write — saves disk
    // churn on idempotent re-applies.
    if (
      product.category === category &&
      (product.subcategory ?? "") === subcategory
    ) {
      continue;
    }

    const next: NewShopEntry = {
      slug,
      name: product.name,
      brand: product.brand,
      category: category as Category,
      subcategory: subcategory || undefined,
      reason: product.reason,
      priceRange: product.priceRange,
      url: product.url,
      images: product.images ?? [product.image],
      extractionMethod: product.extractionMethod ?? "manual",
      htmlPriceSelector: product.htmlPriceSelector,
      priceFloor: product.priceFloor,
    };

    try {
      await replaceShopEntry(slug, next);
      written.push(slug);
    } catch (e) {
      return NextResponse.json(
        {
          error: `Failed at ${slug}: ${
            e instanceof Error ? e.message : String(e)
          }`,
          written,
        },
        { status: 500 }
      );
    }
  }

  return NextResponse.json({ ok: true, written });
}
