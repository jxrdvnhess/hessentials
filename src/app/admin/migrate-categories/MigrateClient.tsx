"use client";

/**
 * Migration table — client component.
 *
 * Each row shows: legacy category, proposal (auto-classifier), current
 * value (from shop.ts), and editable inputs to override. The user
 * "accepts proposal" per row (or batch), edits anything wrong, then
 * applies all changes.
 *
 * The Apply button posts an array of {slug, category, subcategory} to
 * /api/admin/migrate-categories. The endpoint applies them one at a
 * time and returns the list of slugs successfully written. Idempotent
 * rows (no diff) are skipped server-side.
 */

import { useMemo, useState } from "react";

export type Row = {
  slug: string;
  brand: string;
  name: string;
  legacyCategory: string;
  currentCategory: string;
  currentSubcategory: string;
  proposal: {
    category: string;
    subcategory: string;
    confidence: "high" | "medium" | "low";
    note?: string;
  };
  migrated: boolean;
};

type RowState = {
  category: string;
  subcategory: string;
};

const INPUT_CLS =
  "w-full border border-[#1f1d1b]/15 bg-white/40 px-2 py-1.5 font-serif text-[14px] text-[#1f1d1b] outline-none focus:border-[#1f1d1b]/40";
const BUTTON_CLS =
  "inline-flex items-center justify-center border border-[#1f1d1b]/30 px-5 py-2.5 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b] transition-colors hover:bg-[#1f1d1b] hover:text-[#f6f1e7] disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-transparent disabled:hover:text-[#1f1d1b]";

const CONFIDENCE_COLOR: Record<Row["proposal"]["confidence"], string> = {
  high: "text-[#1f1d1b]/55",
  medium: "text-[#b88830]",
  low: "text-[#a23a23]",
};

export function MigrateClient({
  rows,
  tree,
}: {
  rows: Row[];
  tree: Record<string, string[]>;
}) {
  // Initial state: if the row is already migrated, use its current values;
  // otherwise stage the proposal as the proposed write.
  const [state, setState] = useState<Record<string, RowState>>(() => {
    const init: Record<string, RowState> = {};
    for (const r of rows) {
      if (r.migrated) {
        init[r.slug] = {
          category: r.currentCategory,
          subcategory: r.currentSubcategory,
        };
      } else {
        init[r.slug] = {
          category: r.proposal.category,
          subcategory: r.proposal.subcategory,
        };
      }
    }
    return init;
  });

  const [applying, setApplying] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [written, setWritten] = useState<string[]>([]);

  const dirtyRows = useMemo(() => {
    return rows.filter((r) => {
      const s = state[r.slug];
      return (
        s &&
        (s.category !== r.currentCategory ||
          (s.subcategory ?? "") !== (r.currentSubcategory ?? ""))
      );
    });
  }, [rows, state]);

  const onApplyAll = async () => {
    setError(null);
    setApplying(true);
    setWritten([]);
    try {
      const changes = dirtyRows.map((r) => ({
        slug: r.slug,
        category: state[r.slug].category,
        subcategory: state[r.slug].subcategory,
      }));
      const res = await fetch("/api/admin/migrate-categories", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ changes }),
      });
      const payload = (await res.json()) as {
        ok?: boolean;
        error?: string;
        written?: string[];
      };
      if (!res.ok || !payload.ok) {
        setError(payload.error ?? `HTTP ${res.status}`);
        setWritten(payload.written ?? []);
        return;
      }
      setWritten(payload.written ?? []);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setApplying(false);
    }
  };

  const onAcceptAllProposals = () => {
    setState((curr) => {
      const next = { ...curr };
      for (const r of rows) {
        if (!r.migrated) {
          next[r.slug] = {
            category: r.proposal.category,
            subcategory: r.proposal.subcategory,
          };
        }
      }
      return next;
    });
  };

  return (
    <div>
      <div className="mb-6 flex flex-wrap items-center gap-4">
        <button
          type="button"
          onClick={onAcceptAllProposals}
          className="border border-[#1f1d1b]/15 px-4 py-2 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/65 transition-colors hover:border-[#1f1d1b]/30 hover:text-[#1f1d1b]"
        >
          Stage all proposals
        </button>
        <button
          type="button"
          onClick={onApplyAll}
          disabled={applying || dirtyRows.length === 0}
          className={BUTTON_CLS}
        >
          {applying
            ? "Applying…"
            : dirtyRows.length === 0
            ? "No changes staged"
            : `Apply ${dirtyRows.length} change${
                dirtyRows.length === 1 ? "" : "s"
              }`}
        </button>
        {error && (
          <p className="font-mono text-[12px] text-[#a23a23]">{error}</p>
        )}
        {written.length > 0 && !error && (
          <p className="font-serif text-[13px] italic text-[#1f1d1b]/65">
            Wrote {written.length} row{written.length === 1 ? "" : "s"}.
            Refresh to re-read shop.ts.
          </p>
        )}
      </div>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-left text-[14px] text-[#1f1d1b]">
          <thead>
            <tr className="border-b border-[#1f1d1b]/15 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
              <th className="py-3 pr-4 font-normal">Product</th>
              <th className="py-3 pr-4 font-normal">Legacy</th>
              <th className="py-3 pr-4 font-normal">Proposal</th>
              <th className="py-3 pr-4 font-normal w-[160px]">Category</th>
              <th className="py-3 pr-4 font-normal w-[180px]">Subcategory</th>
              <th className="py-3 font-normal">State</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((r) => {
              const s = state[r.slug];
              const dirty =
                s.category !== r.currentCategory ||
                s.subcategory !== r.currentSubcategory;
              const datalistId = `subs-${r.slug}`;
              return (
                <tr
                  key={r.slug}
                  className={`border-b border-[#1f1d1b]/8 align-top ${
                    dirty ? "bg-[#f0e9d9]/40" : ""
                  }`}
                >
                  <td className="py-3 pr-4">
                    <div className="font-serif text-[15px] leading-[1.3]">
                      {r.name}
                    </div>
                    <div className="mt-1 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/50">
                      {r.brand}
                    </div>
                    <div className="mt-1 font-mono text-[11px] text-[#1f1d1b]/45">
                      {r.slug}
                    </div>
                  </td>
                  <td className="py-3 pr-4 text-[12px] uppercase tracking-[0.18em] text-[#1f1d1b]/55">
                    {r.legacyCategory}
                  </td>
                  <td className="py-3 pr-4">
                    <div className="font-mono text-[12px] text-[#1f1d1b]/65">
                      {r.proposal.category}
                      <span className="text-[#1f1d1b]/30"> / </span>
                      {r.proposal.subcategory}
                    </div>
                    <div
                      className={`mt-1 text-[10px] uppercase tracking-[0.18em] ${
                        CONFIDENCE_COLOR[r.proposal.confidence]
                      }`}
                    >
                      {r.proposal.confidence}
                      {r.proposal.note ? ` — ${r.proposal.note}` : ""}
                    </div>
                  </td>
                  <td className="py-3 pr-4">
                    <select
                      aria-label="Category"
                      value={s.category}
                      onChange={(e) =>
                        setState((curr) => ({
                          ...curr,
                          [r.slug]: {
                            ...curr[r.slug],
                            category: e.target.value,
                            // Wipe subcategory if it isn't valid for the
                            // newly-picked top-level. The user re-types.
                            subcategory: tree[e.target.value]?.includes(
                              curr[r.slug].subcategory
                            )
                              ? curr[r.slug].subcategory
                              : "",
                          },
                        }))
                      }
                      className={INPUT_CLS}
                    >
                      <option value={r.currentCategory}>
                        {r.currentCategory}
                      </option>
                      {Object.keys(tree).map((k) =>
                        k === r.currentCategory ? null : (
                          <option key={k} value={k}>
                            {k}
                          </option>
                        )
                      )}
                    </select>
                  </td>
                  <td className="py-3 pr-4">
                    <input
                      list={datalistId}
                      value={s.subcategory}
                      onChange={(e) =>
                        setState((curr) => ({
                          ...curr,
                          [r.slug]: {
                            ...curr[r.slug],
                            subcategory: e.target.value
                              .toLowerCase()
                              .replace(/[^a-z0-9-]/g, "-")
                              .replace(/-+/g, "-"),
                          },
                        }))
                      }
                      className={`${INPUT_CLS} font-mono text-[12px]`}
                      placeholder="kebab-case"
                    />
                    <datalist id={datalistId}>
                      {(tree[s.category] ?? []).map((sub) => (
                        <option key={sub} value={sub} />
                      ))}
                    </datalist>
                  </td>
                  <td className="py-3 text-[10px] uppercase tracking-[0.18em]">
                    {written.includes(r.slug) ? (
                      <span className="text-[#1f1d1b]/65">Saved</span>
                    ) : dirty ? (
                      <span className="text-[#b88830]">Staged</span>
                    ) : r.migrated ? (
                      <span className="text-[#1f1d1b]/45">Migrated</span>
                    ) : (
                      <span className="text-[#1f1d1b]/45">Legacy</span>
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
