import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { CATEGORY_TREE } from "../../../data/categories";
import { SHOP_PRODUCTS } from "../../../data/shop";
import { classifyProduct } from "../../../lib/shopImport/classify";
import { MigrateClient, type Row } from "./MigrateClient";

export const metadata: Metadata = {
  title: "Migrate categories — Admin",
  robots: { index: false, follow: false },
};

/**
 * Admin migration surface.
 *
 * Lists every product with its old (legacy) category, the auto-classifier's
 * proposed (newCategory, newSubcategory), and the current values from
 * shop.ts. Each row is editable — pick a different top-level, type a
 * different subcategory. Apply writes the changes to shop.ts via the
 * batch endpoint.
 *
 * Dev-only — 404 in production.
 */
export const dynamic = "force-dynamic";

export default function MigrateCategoriesPage() {
  if (process.env.NODE_ENV === "production") notFound();

  const newKeys = Object.keys(CATEGORY_TREE);
  const rows: Row[] = SHOP_PRODUCTS.map((p) => {
    const migrated = newKeys.includes(p.category);
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

  // Build category → subcategories[] for the picker autocomplete.
  const tree: Record<string, string[]> = {};
  for (const [k, v] of Object.entries(CATEGORY_TREE)) {
    tree[k] = [...v.subcategories];
  }

  const stillToMigrate = rows.filter((r) => !r.migrated).length;

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <div className="mx-auto w-full max-w-7xl px-6 pt-12 pb-24 sm:px-10 md:pt-16">
        <header className="mb-10">
          <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45">
            Admin
          </p>
          <h1 className="mt-3 font-serif text-[clamp(1.75rem,3.5vw,2.5rem)] font-normal leading-[1.1] tracking-[-0.01em]">
            Migrate categories
          </h1>
          <p className="mt-4 max-w-2xl font-serif text-[15px] italic leading-[1.5] text-[#1f1d1b]/65">
            Old categories on the left. Auto-classifier proposal in the
            middle. Edit anything, then apply. Apply writes shop.ts row
            by row — partial failures stop and report what was written.
          </p>
          <p className="mt-3 font-serif text-[13px] italic text-[#1f1d1b]/55">
            {rows.length} products. {stillToMigrate} still on legacy categories.
          </p>
        </header>

        <MigrateClient rows={rows} tree={tree} />
      </div>
    </main>
  );
}
