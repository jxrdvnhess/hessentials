import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Link from "next/link";
import {
  SHOP_PRODUCTS,
  CATEGORY_TREE,
  type ShopProduct,
} from "../../../../data/shop";
import { EditClient } from "./EditClient";

export const metadata: Metadata = {
  title: "Admin / Edit product",
  robots: { index: false, follow: false },
};

/**
 * Admin shop edit detail — Hessentials Shop.
 *
 * Edit form prefilled from SHOP_PRODUCTS. Slug is intentionally
 * read-only (renaming would break image refs and external links).
 * Image management is deferred — to change images, delete and
 * re-import.
 *
 * Dev-only — 404 in production.
 */
export const dynamic = "force-dynamic";

type PageProps = { params: Promise<{ slug: string }> };

export default async function AdminShopEditDetailPage({
  params,
}: PageProps) {
  if (process.env.NODE_ENV === "production") notFound();

  const { slug } = await params;
  const product = SHOP_PRODUCTS.find((p) => p.slug === slug);
  if (!product) notFound();

  const initial: ProductForClient = {
    slug: product.slug,
    name: product.name,
    brand: product.brand,
    category: product.category,
    subcategory: product.subcategory ?? "",
    audience: [...(product.audience ?? [])],
    reason: product.reason,
    priceRange: product.priceRange,
    url: product.url,
    image: product.image,
    images: product.images ?? [product.image],
    extractionMethod: product.extractionMethod ?? "manual",
    htmlPriceSelector: product.htmlPriceSelector ?? "",
    priceFloor: product.priceFloor ?? null,
  };

  const tree: Record<string, string[]> = {};
  for (const [k, v] of Object.entries(CATEGORY_TREE)) {
    tree[k] = [...v.subcategories];
  }

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <div className="mx-auto w-full max-w-4xl px-6 pt-12 pb-24 sm:px-10 md:pt-16">
        <header className="mb-10">
          <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45">
            Admin / Edit
          </p>
          <h1 className="mt-3 font-serif text-[clamp(1.75rem,3.5vw,2.5rem)] font-normal leading-[1.1] tracking-[-0.01em]">
            {product.name}
          </h1>
          <p className="mt-2 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
            {product.brand}
          </p>
          <div className="mt-6 flex flex-wrap gap-3 text-[11px] uppercase tracking-[0.22em]">
            <Link
              href="/admin/shop-edit"
              className="border border-[#1f1d1b]/15 px-4 py-2 text-[#1f1d1b]/65 transition-colors hover:border-[#1f1d1b]/30 hover:text-[#1f1d1b]"
            >
              ← All products
            </Link>
            <Link
              href={`/shop/${product.slug}`}
              className="border border-[#1f1d1b]/15 px-4 py-2 text-[#1f1d1b]/65 transition-colors hover:border-[#1f1d1b]/30 hover:text-[#1f1d1b]"
              target="_blank"
              rel="noreferrer"
            >
              View public page ↗
            </Link>
          </div>
        </header>

        <EditClient initial={initial} tree={tree} />
      </div>
    </main>
  );
}

/**
 * Plain shape used to seed the client form. We deliberately avoid
 * passing the full ShopProduct so the client doesn't import the data
 * type directly.
 */
export type ProductForClient = {
  slug: ShopProduct["slug"];
  name: string;
  brand: string;
  /** Top-level — may still be a Legacy* string for unmigrated products. */
  category: ShopProduct["category"];
  subcategory: string;
  /** Cross-pillar audience tags. Defaults to [] (None). */
  audience: ("mens" | "womens")[];
  reason: string;
  priceRange: string;
  url: string;
  image: string;
  images: string[];
  extractionMethod: NonNullable<ShopProduct["extractionMethod"]>;
  htmlPriceSelector: string;
  priceFloor: number | null;
};
