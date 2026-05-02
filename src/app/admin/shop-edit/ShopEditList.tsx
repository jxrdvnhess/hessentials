"use client";

/**
 * Shop edit — list view.
 *
 * Client component because each row owns a delete confirmation
 * lifecycle. The actual DELETE is fired against the API route; on
 * success the row is filtered out of the local list (and a refresh
 * is suggested so SHOP_PRODUCTS reflects the file change).
 */

import Link from "next/link";
import { useMemo, useState } from "react";

type Item = {
  slug: string;
  name: string;
  brand: string;
  category: string;
  subcategory: string;
  priceRange: string;
  reason: string;
  hasReason: boolean;
};

/** Cap the reason preview at this many characters; ellipsis if longer. */
const REASON_PREVIEW_MAX = 60;

function previewReason(reason: string): string {
  if (reason.length <= REASON_PREVIEW_MAX) return reason;
  return reason.slice(0, REASON_PREVIEW_MAX).trimEnd() + "…";
}

export function ShopEditList({ items }: { items: Item[] }) {
  const [rows, setRows] = useState(items);
  const [query, setQuery] = useState("");
  const [confirming, setConfirming] = useState<string | null>(null);
  const [pending, setPending] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastDeleted, setLastDeleted] = useState<{
    slug: string;
    images: number;
  } | null>(null);

  /**
   * Live filter — case-insensitive substring match against the fields
   * a human would actually type when looking for a product. The search
   * runs over `rows` (post-delete state), not the original `items`.
   */
  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return rows;
    return rows.filter(
      (r) =>
        r.name.toLowerCase().includes(q) ||
        r.brand.toLowerCase().includes(q) ||
        r.slug.toLowerCase().includes(q) ||
        r.category.toLowerCase().includes(q) ||
        r.subcategory.toLowerCase().includes(q)
    );
  }, [rows, query]);

  const onDelete = async (slug: string) => {
    setError(null);
    setPending(slug);
    try {
      const res = await fetch(`/api/admin/shop-item/${slug}`, {
        method: "DELETE",
      });
      const payload = (await res.json()) as {
        ok?: boolean;
        error?: string;
        removedImages?: string[];
      };
      if (!res.ok || !payload.ok) {
        throw new Error(payload.error ?? `HTTP ${res.status}`);
      }
      setRows((curr) => curr.filter((r) => r.slug !== slug));
      setLastDeleted({
        slug,
        images: payload.removedImages?.length ?? 0,
      });
      setConfirming(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setPending(null);
    }
  };

  return (
    <div>
      {/* Search — single input, filters on name / brand / slug / category. */}
      <div className="mb-6 flex flex-wrap items-center gap-3">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, brand, slug, or category"
          className="w-full max-w-md border border-[#1f1d1b]/20 bg-white/40 px-3 py-2 font-serif text-[14px] text-[#1f1d1b] outline-none placeholder:italic placeholder:text-[#1f1d1b]/40 focus:border-[#1f1d1b]/40"
        />
        <p className="font-serif text-[12px] italic text-[#1f1d1b]/55">
          {visible.length} of {rows.length}
        </p>
      </div>

      {error && (
        <p className="mb-4 font-mono text-[12px] text-[#a23a23]">{error}</p>
      )}
      {lastDeleted && (
        <p className="mb-4 font-serif text-[13px] italic text-[#1f1d1b]/65">
          Deleted <span className="font-mono">{lastDeleted.slug}</span>.{" "}
          {lastDeleted.images} image{lastDeleted.images === 1 ? "" : "s"}{" "}
          removed.
        </p>
      )}

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-[14px] text-[#1f1d1b]">
          <thead>
            <tr className="border-b border-[#1f1d1b]/15 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
              <th className="py-3 pr-4 font-normal">Product</th>
              <th className="py-3 pr-4 font-normal">Category</th>
              <th className="py-3 pr-4 font-normal">Price</th>
              <th className="py-3 pr-4 font-normal">Reason</th>
              <th className="py-3 font-normal text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {visible.length === 0 ? (
              <tr>
                <td
                  colSpan={5}
                  className="py-12 text-center font-serif text-[14px] italic text-[#1f1d1b]/55"
                >
                  No matches.
                </td>
              </tr>
            ) : null}
            {visible.map((row) => (
              <tr
                key={row.slug}
                className="border-b border-[#1f1d1b]/8 align-top"
              >
                <td className="py-3 pr-4">
                  <div className="font-serif text-[15px] leading-[1.3]">
                    {row.name}
                  </div>
                  <div className="mt-1 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/50">
                    {row.brand}
                  </div>
                  <div className="mt-1 font-mono text-[11px] text-[#1f1d1b]/45">
                    {row.slug}
                  </div>
                </td>
                <td className="py-3 pr-4 text-[12px] uppercase tracking-[0.18em] text-[#1f1d1b]/65">
                  {row.category}
                  {row.subcategory && (
                    <div className="mt-0.5 text-[10px] tracking-[0.18em] text-[#1f1d1b]/45">
                      / {row.subcategory}
                    </div>
                  )}
                </td>
                <td className="py-3 pr-4 font-serif text-[14px]">
                  {row.priceRange}
                </td>
                <td className="max-w-[28ch] py-3 pr-4">
                  {row.hasReason ? (
                    <span
                      className="font-serif text-[13px] italic leading-[1.4] text-[#1f1d1b]/75"
                      title={row.reason}
                    >
                      {previewReason(row.reason)}
                    </span>
                  ) : (
                    <span className="text-[12px] uppercase tracking-[0.18em] text-[#a23a23]">
                      Missing
                    </span>
                  )}
                </td>
                <td className="py-3 text-right">
                  {confirming === row.slug ? (
                    <span className="inline-flex items-center gap-2">
                      <span className="font-serif text-[13px] italic text-[#1f1d1b]/65">
                        Sure?
                      </span>
                      <button
                        type="button"
                        disabled={pending === row.slug}
                        onClick={() => onDelete(row.slug)}
                        className="border border-[#a23a23]/40 px-3 py-1.5 text-[10px] uppercase tracking-[0.22em] text-[#a23a23] transition-colors hover:bg-[#a23a23] hover:text-[#f6f1e7] disabled:opacity-40"
                      >
                        {pending === row.slug ? "Deleting…" : "Delete"}
                      </button>
                      <button
                        type="button"
                        onClick={() => setConfirming(null)}
                        disabled={pending === row.slug}
                        className="border border-[#1f1d1b]/15 px-3 py-1.5 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/65 hover:border-[#1f1d1b]/30 disabled:opacity-40"
                      >
                        Cancel
                      </button>
                    </span>
                  ) : (
                    <span className="inline-flex items-center gap-2">
                      <Link
                        href={`/admin/shop-edit/${row.slug}`}
                        className="border border-[#1f1d1b]/30 px-3 py-1.5 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b] transition-colors hover:bg-[#1f1d1b] hover:text-[#f6f1e7]"
                      >
                        Edit
                      </Link>
                      <button
                        type="button"
                        onClick={() => setConfirming(row.slug)}
                        className="border border-[#1f1d1b]/15 px-3 py-1.5 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/65 transition-colors hover:border-[#a23a23]/40 hover:text-[#a23a23]"
                      >
                        Delete
                      </button>
                    </span>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
