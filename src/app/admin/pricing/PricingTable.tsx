"use client";

/**
 * Pricing admin — searchable table.
 *
 * The page server-fetches every product's price (in parallel) and
 * passes the resulting rows in. This component just adds a live
 * search filter on name / brand / slug / display string + the table
 * markup.
 */

import { useMemo, useState } from "react";
import { formatVerifiedDate } from "../../../lib/pricing/format";

export type PricingRow = {
  slug: string;
  name: string;
  brand: string;
  method: string;
  display: string;
  live: boolean;
  soldOut: boolean;
  error: string | null;
  lastVerified: string | null;
};

export function PricingTable({ rows }: { rows: PricingRow[] }) {
  const [query, setQuery] = useState("");

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return rows;
    return rows.filter(
      (r) =>
        r.name.toLowerCase().includes(q) ||
        r.brand.toLowerCase().includes(q) ||
        r.slug.toLowerCase().includes(q) ||
        r.display.toLowerCase().includes(q) ||
        r.method.toLowerCase().includes(q) ||
        (r.error ?? "").toLowerCase().includes(q)
    );
  }, [rows, query]);

  return (
    <>
      <div className="mb-6 flex flex-wrap items-center gap-3">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, brand, slug, method, or error"
          className="w-full max-w-md border border-[#1f1d1b]/20 bg-white/40 px-3 py-2 font-serif text-[14px] text-[#1f1d1b] outline-none placeholder:italic placeholder:text-[#1f1d1b]/40 focus:border-[#1f1d1b]/40"
        />
        <p className="font-serif text-[12px] italic text-[#1f1d1b]/55">
          {visible.length} of {rows.length}
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-[14px] text-[#1f1d1b]">
          <thead>
            <tr className="border-b border-[#1f1d1b]/15 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
              <th className="py-3 pr-4 font-normal">Product</th>
              <th className="py-3 pr-4 font-normal">Method</th>
              <th className="py-3 pr-4 font-normal">Display</th>
              <th className="py-3 pr-4 font-normal">State</th>
              <th className="py-3 pr-4 font-normal">Verified</th>
              <th className="py-3 font-normal">Error</th>
            </tr>
          </thead>
          <tbody>
            {visible.length === 0 ? (
              <tr>
                <td
                  colSpan={6}
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
                </td>
                <td className="py-3 pr-4 text-[12px] uppercase tracking-[0.18em] text-[#1f1d1b]/65">
                  {row.method}
                </td>
                <td className="py-3 pr-4 font-serif text-[14px] text-[#1f1d1b]">
                  {row.display}
                </td>
                <td className="py-3 pr-4 text-[12px] uppercase tracking-[0.18em]">
                  {row.error ? (
                    <span className="text-[#a23a23]">Error</span>
                  ) : row.soldOut ? (
                    <span className="text-[#1f1d1b]/55">Sold out</span>
                  ) : row.live ? (
                    <span className="text-[#1f1d1b]">Live</span>
                  ) : (
                    <span className="text-[#1f1d1b]/55">Manual</span>
                  )}
                </td>
                <td className="py-3 pr-4 font-serif text-[13px] italic text-[#1f1d1b]/55">
                  {row.lastVerified
                    ? formatVerifiedDate(row.lastVerified)
                    : "—"}
                </td>
                <td className="py-3 max-w-md break-words font-mono text-[11px] leading-[1.4] text-[#a23a23]">
                  {row.error ?? ""}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}
