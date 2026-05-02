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
import { Fragment, useEffect, useMemo, useState } from "react";

type Item = {
  slug: string;
  name: string;
  brand: string;
  category: string;
  subcategory: string;
  audience: ("mens" | "womens")[];
  priceRange: string;
  reason: string;
  hasReason: boolean;
  /** ISO timestamp; "" for legacy entries that haven't been backfilled. */
  dateAdded: string;
  /** Fallback ordering when dateAdded ties (or is empty for both). */
  addedIndex: number;
};

/**
 * Compact format for the DATE ADDED column.
 * Within 30 days: "May 2". Older: "Apr 28, 2026".
 */
function formatDateAdded(iso: string): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  const now = Date.now();
  const ageMs = now - d.getTime();
  const within30 = ageMs >= 0 && ageMs < 30 * 24 * 60 * 60 * 1000;
  return within30
    ? d.toLocaleDateString("en-US", { month: "short", day: "numeric" })
    : d.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        year: "numeric",
      });
}

/**
 * Compact audience indicator for the list view.
 * `[]` → "" (omitted), `["mens"]` → "M", `["womens"]` → "W",
 * `["mens","womens"]` → "M · W". Order-insensitive.
 */
function audienceMark(a: readonly ("mens" | "womens")[]): string {
  const set = new Set(a);
  if (set.has("mens") && set.has("womens")) return "M · W";
  if (set.has("mens")) return "M";
  if (set.has("womens")) return "W";
  return "";
}

/** Cap the reason preview at this many characters; ellipsis if longer. */
const REASON_PREVIEW_MAX = 60;

function previewReason(reason: string): string {
  if (reason.length <= REASON_PREVIEW_MAX) return reason;
  return reason.slice(0, REASON_PREVIEW_MAX).trimEnd() + "…";
}

/* ---------- Sort model ---------- */

type SortKey =
  | "product"
  | "brand"
  | "category"
  | "price"
  | "reason"
  | "dateAdded";
type SortDirection = "asc" | "desc";
type SortState = { key: SortKey; direction: SortDirection };

/** Default first-click direction for each sort. */
function defaultDirectionFor(key: SortKey): SortDirection {
  return key === "dateAdded" ? "desc" : "asc";
}

/** The cleared / initial state — DATE ADDED desc, per the brief. */
const DEFAULT_SORT: SortState = { key: "dateAdded", direction: "desc" };

/** localStorage key for sort persistence. */
const SORT_STORAGE_KEY = "hessentials.admin.shopedit.sort";

const VALID_SORT_KEYS = new Set<SortKey>([
  "product",
  "brand",
  "category",
  "price",
  "reason",
  "dateAdded",
]);

/** Parse a stored value, returning DEFAULT_SORT on any malformed input. */
function readStoredSort(): SortState {
  if (typeof window === "undefined") return DEFAULT_SORT;
  try {
    const raw = window.localStorage.getItem(SORT_STORAGE_KEY);
    if (!raw) return DEFAULT_SORT;
    const parsed = JSON.parse(raw) as { column?: string; direction?: string };
    if (
      typeof parsed.column === "string" &&
      VALID_SORT_KEYS.has(parsed.column as SortKey) &&
      (parsed.direction === "asc" || parsed.direction === "desc")
    ) {
      return {
        key: parsed.column as SortKey,
        direction: parsed.direction,
      };
    }
  } catch {
    // ignore malformed storage
  }
  return DEFAULT_SORT;
}

/**
 * Three-click cycle:
 *   default direction → reverse direction → cleared (back to DEFAULT_SORT)
 * Same logic for every sort key, including dateAdded itself (clicking
 * it once flips desc→asc, twice clears back to desc).
 */
function nextSort(curr: SortState, key: SortKey): SortState {
  const def = defaultDirectionFor(key);
  if (curr.key !== key) return { key, direction: def };
  if (curr.direction === def) {
    return { key, direction: def === "asc" ? "desc" : "asc" };
  }
  return DEFAULT_SORT;
}

/** Pull the lower bound of a priceRange string ("$1,400–$1,800" → 1400). */
function priceLower(s: string): number {
  const m = s.match(/\$([\d,]+(?:\.\d+)?)/);
  if (!m) return Number.POSITIVE_INFINITY;
  return Number(m[1].replace(/,/g, ""));
}

function buildComparator(
  sort: SortState,
  categoryOrder: string[]
): (a: Item, b: Item) => number {
  const dir = sort.direction === "asc" ? 1 : -1;
  switch (sort.key) {
    case "product":
      return (a, b) => dir * a.name.localeCompare(b.name);
    case "brand":
      return (a, b) =>
        dir *
        (a.brand.localeCompare(b.brand) || a.name.localeCompare(b.name));
    case "category": {
      const idx = (cat: string) => {
        const i = categoryOrder.indexOf(cat);
        return i === -1 ? Number.POSITIVE_INFINITY : i;
      };
      return (a, b) => {
        const cd = idx(a.category) - idx(b.category);
        if (cd !== 0) return dir * cd;
        const sd = a.subcategory.localeCompare(b.subcategory);
        if (sd !== 0) return dir * sd;
        return dir * a.name.localeCompare(b.name);
      };
    }
    case "price":
      return (a, b) => dir * (priceLower(a.priceRange) - priceLower(b.priceRange));
    case "reason":
      return (a, b) => {
        // ascending = with-reason first; descending = missing first.
        const av = a.hasReason ? 0 : 1;
        const bv = b.hasReason ? 0 : 1;
        if (av !== bv) return dir * (av - bv);
        return a.name.localeCompare(b.name);
      };
    case "dateAdded": {
      // Sort by ISO timestamp (lexicographic compare works for ISO).
      // Empty / unparseable strings fall back to addedIndex as a stable
      // proxy so legacy entries retain their array order within a tie.
      return (a, b) => {
        const cmp = a.dateAdded.localeCompare(b.dateAdded);
        if (cmp !== 0) return dir * cmp;
        return dir * (a.addedIndex - b.addedIndex);
      };
    }
  }
}

/* ---------- Sortable column header ---------- */

/**
 * One sortable label inside a `<th>`. Renders a button that cycles
 * default → reverse → cleared on click; shows a small ↑ / ↓ arrow
 * inline when this sort is active. Hover state: subtle underline.
 *
 * For columns where the header reads as one piece (CATEGORY, PRICE,
 * REASON, DATE ADDED), a single `<SortLabel>` fills the cell. For
 * the PRODUCT / BRAND header, two `<SortLabel>` instances sit side
 * by side with a slash between them.
 */
function SortLabel({
  sortKey,
  sort,
  setSort,
  children,
}: {
  sortKey: SortKey;
  sort: SortState;
  setSort: React.Dispatch<React.SetStateAction<SortState>>;
  children: React.ReactNode;
}) {
  const active = sort.key === sortKey;
  const arrow = active ? (sort.direction === "asc" ? " ↑" : " ↓") : "";
  return (
    <button
      type="button"
      aria-pressed={active}
      onClick={() => setSort((s) => nextSort(s, sortKey))}
      className={[
        "cursor-pointer transition-colors duration-300 ease-out",
        "hover:underline hover:underline-offset-4 hover:decoration-[#1f1d1b]/40",
        active ? "text-[#1f1d1b]" : "text-[#1f1d1b]/55 hover:text-[#1f1d1b]/85",
      ].join(" ")}
    >
      {children}
      {arrow}
    </button>
  );
}

/* ---------- Component ---------- */

export function ShopEditList({
  items,
  categoryOrder,
}: {
  items: Item[];
  /** Canonical pillar order, passed in from the server (CATEGORY_KEYS). */
  categoryOrder: string[];
}) {
  const [rows, setRows] = useState(items);
  const [query, setQuery] = useState("");
  // Seed with DEFAULT_SORT on the server render; hydrate from
  // localStorage on the client mount. Two-step pattern keeps the
  // server-rendered HTML stable.
  const [sort, setSort] = useState<SortState>(DEFAULT_SORT);
  useEffect(() => {
    // Mount-time hydration from localStorage. The setState-in-effect
    // rule doesn't apply cleanly here — there's no server-safe way to
    // read browser storage at construct time. Matches the same pattern
    // used in ShopGrid's shuffle hydration.
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setSort(readStoredSort());
  }, []);
  // Persist every sort change. The brief uses { column, direction }
  // as the storage shape — keep that contract verbatim so it's
  // legible when inspected in DevTools.
  useEffect(() => {
    if (typeof window === "undefined") return;
    try {
      window.localStorage.setItem(
        SORT_STORAGE_KEY,
        JSON.stringify({ column: sort.key, direction: sort.direction })
      );
    } catch {
      // Quota / private mode — silent.
    }
  }, [sort]);
  const [confirming, setConfirming] = useState<string | null>(null);
  const [pending, setPending] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lastDeleted, setLastDeleted] = useState<{
    slug: string;
    images: number;
  } | null>(null);

  /**
   * Live filter — case-insensitive substring match against the fields
   * a human would actually type when looking for a product.
   */
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    if (!q) return rows;
    return rows.filter(
      (r) =>
        r.name.toLowerCase().includes(q) ||
        r.brand.toLowerCase().includes(q) ||
        r.slug.toLowerCase().includes(q) ||
        r.category.toLowerCase().includes(q) ||
        r.subcategory.toLowerCase().includes(q) ||
        r.audience.some((a) => a.includes(q))
    );
  }, [rows, query]);

  /** Sorted, post-filter list. Used directly when CATEGORY isn't active. */
  const sorted = useMemo(() => {
    const cmp = buildComparator(sort, categoryOrder);
    return [...filtered].sort(cmp);
  }, [filtered, sort, categoryOrder]);

  /**
   * When CATEGORY is the active sort, group the sorted list into
   * pillar sections. Each section carries a divider header (PILLAR · COUNT)
   * and the items in that pillar. Pillars with zero post-filter items
   * are dropped — no empty dividers.
   */
  const sections: { divider: { name: string; count: number } | null; rows: Item[] }[] =
    useMemo(() => {
      if (sort.key !== "category") {
        return [{ divider: null, rows: sorted }];
      }
      // sorted is already in (pillar order, subcategory, name) sequence,
      // so a single pass is enough to break it into contiguous groups.
      const out: {
        divider: { name: string; count: number } | null;
        rows: Item[];
      }[] = [];
      let currentCat: string | null = null;
      let currentRows: Item[] = [];
      for (const r of sorted) {
        if (r.category !== currentCat) {
          if (currentCat !== null) {
            out.push({
              divider: {
                name: currentCat.toUpperCase(),
                count: currentRows.length,
              },
              rows: currentRows,
            });
          }
          currentCat = r.category;
          currentRows = [r];
        } else {
          currentRows.push(r);
        }
      }
      if (currentCat !== null) {
        out.push({
          divider: {
            name: currentCat.toUpperCase(),
            count: currentRows.length,
          },
          rows: currentRows,
        });
      }
      return out;
    }, [sort.key, sorted]);

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
      <div className="mb-5 flex flex-wrap items-center gap-3">
        <input
          type="search"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search by name, brand, slug, or category"
          className="w-full max-w-md border border-[#1f1d1b]/20 bg-white/40 px-3 py-2 font-serif text-[14px] text-[#1f1d1b] outline-none placeholder:italic placeholder:text-[#1f1d1b]/40 focus:border-[#1f1d1b]/40"
        />
        <p className="font-serif text-[12px] italic text-[#1f1d1b]/55">
          {filtered.length} of {rows.length}
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
              {/* PRODUCT column has two sort axes — name and brand. The
                  cell stacks both visually, so each word in the header
                  is independently clickable. Slash separator matches
                  the admin breadcrumb pattern. */}
              <th className="py-3 pr-4 font-normal">
                <SortLabel sortKey="product" sort={sort} setSort={setSort}>
                  Product
                </SortLabel>
                <span className="mx-2 text-[#1f1d1b]/30">/</span>
                <SortLabel sortKey="brand" sort={sort} setSort={setSort}>
                  Brand
                </SortLabel>
              </th>
              <th className="py-3 pr-4 font-normal">
                <SortLabel sortKey="category" sort={sort} setSort={setSort}>
                  Category
                </SortLabel>
              </th>
              <th className="py-3 pr-4 font-normal">
                <SortLabel sortKey="price" sort={sort} setSort={setSort}>
                  Price
                </SortLabel>
              </th>
              <th className="py-3 pr-4 font-normal">
                <SortLabel sortKey="reason" sort={sort} setSort={setSort}>
                  Reason
                </SortLabel>
              </th>
              <th className="py-3 pr-4 font-normal text-right">
                <SortLabel sortKey="dateAdded" sort={sort} setSort={setSort}>
                  Date added
                </SortLabel>
              </th>
              <th className="py-3 font-normal text-right">Actions</th>
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 ? (
              <tr>
                <td
                  colSpan={6}
                  className="py-12 text-center font-serif text-[14px] italic text-[#1f1d1b]/55"
                >
                  No matches.
                </td>
              </tr>
            ) : null}

            {sections.map((section, si) => (
              <Fragment key={section.divider?.name ?? `flat-${si}`}>
                {section.divider && (
                  <tr aria-hidden className="border-0">
                    {/* Divider sits in the PRODUCT column with the rest of
                        the row empty (colSpan={6}). Generous top padding
                        — roughly 1.5× a standard row's height — gives
                        breathing room between pillars; standard bottom
                        padding keeps the first product visually attached.
                        First divider also picks up this top padding,
                        which gives the table a nice breathing zone under
                        the column headers. */}
                    <td
                      colSpan={6}
                      className="border-0 pt-20 pb-3 align-baseline"
                    >
                      <span className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45">
                        {section.divider.name}
                      </span>
                      <span className="ml-3 font-serif text-[12px] italic text-[#1f1d1b]/55">
                        · {section.divider.count}
                      </span>
                    </td>
                  </tr>
                )}
                {section.rows.map((row) => (
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
                      {audienceMark(row.audience) && (
                        <div
                          className="mt-1 font-mono text-[10px] tracking-[0.12em] text-[#1f1d1b]/45"
                          aria-label={`Audience: ${row.audience.join(", ")}`}
                        >
                          {audienceMark(row.audience)}
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
                        // Faint em dash signals "absence" without shouting.
                        // The only legitimate em-dash use post-consistency-pass.
                        <span
                          aria-label="No reason yet"
                          className="font-serif text-[16px] text-[#1f1d1b]/25"
                        >
                          —
                        </span>
                      )}
                    </td>
                    <td
                      className="py-3 pr-4 text-right font-mono text-[11px] text-[#1f1d1b]/55 whitespace-nowrap"
                      title={row.dateAdded || undefined}
                    >
                      {formatDateAdded(row.dateAdded)}
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
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
