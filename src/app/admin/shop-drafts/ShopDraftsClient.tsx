"use client";

/**
 * Shop drafts — client view.
 *
 * Per-draft row with inline category/audience pickers and three
 * actions: Promote, Send back, Delete. Edit-everything-else flows
 * through the existing /admin/shop-edit/[slug] form via a per-row
 * link — duplicating the full editor here would just create drift.
 *
 * After a successful action the row removes itself from local state
 * and the page is refreshed via router so subsequent reads (drafts
 * count, listings) reflect the change.
 */

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

type DraftRow = {
  slug: string;
  name: string;
  brand: string;
  category: string;
  subcategory: string;
  audience: ("mens" | "womens")[];
  reason: string;
  priceRange: string;
  url: string;
  image: string;
  extractionMethod: string;
  stabilityTier?: 1 | 2 | 3 | 4;
};

type PendingRow = {
  rowIndex?: number;
  sourceArticle?: string;
  articleUrl?: string;
  anchor?: string;
  directUrl: string;
  flags?: string[];
  candidate: {
    name: string;
    brand: string;
    reason?: string;
    images?: string[];
    url: string;
  };
};

type Props = {
  drafts: DraftRow[];
  pending: PendingRow[];
  categories: { key: string; label: string }[];
  tree: Record<string, string[]>;
};

type Status =
  | { kind: "idle" }
  | { kind: "saving" }
  | { kind: "error"; message: string };

export function ShopDraftsClient({
  drafts,
  pending,
  categories,
  tree,
}: Props) {
  const [rows, setRows] = useState<DraftRow[]>(drafts);
  const [pendingRows, setPendingRows] = useState<PendingRow[]>(pending);

  if (rows.length === 0 && pendingRows.length === 0) {
    return (
      <p className="font-serif text-[15px] italic text-[#1f1d1b]/55">
        No drafts. The bulk import either hasn&apos;t run, or every
        staged entry has already been promoted or sent back.
      </p>
    );
  }

  return (
    <div className="space-y-12">
      {rows.length > 0 && (
        <section>
          <h2 className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55">
            Staged drafts
          </h2>
          <ul className="mt-6 space-y-8">
            {rows.map((d) => (
              <DraftCard
                key={d.slug}
                draft={d}
                categories={categories}
                tree={tree}
                onRemove={(slug) =>
                  setRows((cur) => cur.filter((r) => r.slug !== slug))
                }
              />
            ))}
          </ul>
        </section>
      )}

      {pendingRows.length > 0 && (
        <section>
          <h2 className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55">
            Pending — needs human
          </h2>
          <p className="mt-3 max-w-2xl font-serif text-[13px] italic text-[#1f1d1b]/55">
            Bulk import couldn&apos;t safely stage these. Click a row to
            open the editor, fill in the missing fields, and stage as a
            draft. <strong className="font-normal not-italic">Rescrape</strong> re-runs
            the extractor against the live source to populate price /
            images for you.
          </p>
          <ul className="mt-6 space-y-6">
            {pendingRows.map((p, i) => (
              <PendingCard
                key={`${p.directUrl}-${i}`}
                pending={p}
                categories={categories}
                tree={tree}
                onStaged={(directUrl) =>
                  setPendingRows((cur) =>
                    cur.filter((r) => r.directUrl !== directUrl)
                  )
                }
              />
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}

/* ---------- Single pending row ---------- */

/**
 * Pending row state.
 *
 *   collapsed — title + reason only (default).
 *   open      — inline editor expanded; user can fill missing fields
 *               and Stage as draft, or Rescrape to auto-populate
 *               price/images.
 *
 *  `note` carries inline feedback ("rescrape filled in 5 images / no
 *  price") so the user knows what happened without leaving the row.
 */
type PendingStatus =
  | { kind: "idle" }
  | { kind: "rescraping" }
  | { kind: "staging" }
  | { kind: "note"; message: string }
  | { kind: "error"; message: string };

function PendingCard({
  pending,
  categories,
  tree,
  onStaged,
}: {
  pending: PendingRow;
  categories: { key: string; label: string }[];
  tree: Record<string, string[]>;
  onStaged: (directUrl: string) => void;
}) {
  const router = useRouter();
  const [open, setOpen] = useState(false);
  const [status, setStatus] = useState<PendingStatus>({ kind: "idle" });

  // Editable form state — initialized from the candidate. The
  // rescrape path writes back into the same state so the user sees
  // their form filled in.
  const [name, setName] = useState(pending.candidate.name);
  const [brand, setBrand] = useState(pending.candidate.brand);
  const [reason, setReason] = useState(pending.candidate.reason ?? "");
  const [category, setCategory] = useState<string>("");
  const [subcategory, setSubcategory] = useState<string>("");
  const [priceRange, setPriceRange] = useState<string>("");
  const [audience, setAudience] = useState<("mens" | "womens")[]>([]);

  const subcategoryOptions = tree[category] ?? [];
  const audienceLabel =
    audience.length === 0
      ? "None"
      : audience.length === 2
      ? "Gender-neutral"
      : audience[0] === "mens"
      ? "Mens only"
      : "Womens only";

  async function onRescrape() {
    setStatus({ kind: "rescraping" });
    let res: Response;
    try {
      res = await fetch("/api/admin/shop-drafts/rescrape-pending", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ directUrl: pending.directUrl }),
      });
    } catch (e) {
      setStatus({
        kind: "error",
        message: e instanceof Error ? e.message : String(e),
      });
      return;
    }

    type ServerOk = {
      ok: true;
      staged: boolean;
      slug?: string;
      blockers?: string[];
      preview: {
        name: string;
        brand: string;
        priceRange: string;
        imageCount: number;
        extractionMethod: string;
        candidateCategory: string | null;
      };
    };
    type ServerErr = { ok?: false; error: string };

    const body = (await res.json().catch(() => ({}))) as
      | ServerOk
      | ServerErr;

    if (!res.ok || (body && "ok" in body && body.ok === false)) {
      const message =
        "error" in body && body.error
          ? body.error
          : `Rescrape failed (HTTP ${res.status})`;
      setStatus({ kind: "error", message });
      return;
    }

    const ok = body as ServerOk;
    if (ok.staged) {
      onStaged(pending.directUrl);
      router.refresh();
      return;
    }

    // Pull fresh values back into the form so the user only fills
    // the remaining gaps (typically category).
    if (ok.preview.name && !name) setName(ok.preview.name);
    if (ok.preview.brand && !brand) setBrand(ok.preview.brand);
    if (ok.preview.priceRange) setPriceRange(ok.preview.priceRange);
    if (ok.preview.candidateCategory) setCategory(ok.preview.candidateCategory);
    setOpen(true);

    const blockerNote =
      (ok.blockers ?? []).length > 0
        ? `Rescrape filled ${ok.preview.imageCount} image${
            ok.preview.imageCount === 1 ? "" : "s"
          }. Still missing: ${(ok.blockers ?? []).join(", ")}.`
        : `Rescrape filled ${ok.preview.imageCount} image${
            ok.preview.imageCount === 1 ? "" : "s"
          }, price ${ok.preview.priceRange || "—"}.`;
    setStatus({ kind: "note", message: blockerNote });
  }

  async function onStage() {
    setStatus({ kind: "staging" });
    const payload = {
      directUrl: pending.directUrl,
      fields: {
        name: name.trim(),
        brand: brand.trim(),
        reason: reason.trim(),
        category,
        subcategory: subcategory.trim(),
        priceRange: priceRange.trim(),
        audience,
      },
    };

    let res: Response;
    try {
      res = await fetch("/api/admin/shop-drafts/stage-pending", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    } catch (e) {
      setStatus({
        kind: "error",
        message: e instanceof Error ? e.message : String(e),
      });
      return;
    }

    const body = (await res.json().catch(() => ({}))) as {
      ok?: boolean;
      error?: string;
      slug?: string;
    };

    if (!res.ok || body.ok !== true) {
      setStatus({
        kind: "error",
        message: body.error ?? `Stage failed (HTTP ${res.status})`,
      });
      return;
    }

    onStaged(pending.directUrl);
    router.refresh();
  }

  const busy = status.kind === "rescraping" || status.kind === "staging";

  return (
    <li className="border-t border-[#1f1d1b]/10 pt-5">
      <div className="flex flex-wrap items-baseline justify-between gap-3">
        <button
          type="button"
          onClick={() => setOpen((v) => !v)}
          className="group flex items-baseline gap-3 text-left"
        >
          <span
            aria-hidden
            className={[
              "inline-block text-[10px] text-[#1f1d1b]/45 transition-transform",
              open ? "rotate-90" : "",
            ].join(" ")}
          >
            ▸
          </span>
          <span className="font-serif text-[15px] leading-[1.4] decoration-[#1f1d1b]/15 underline-offset-4 group-hover:underline">
            {pending.candidate.brand} — {pending.candidate.name}
          </span>
        </button>
        <button
          type="button"
          onClick={onRescrape}
          disabled={busy}
          className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b] underline decoration-[#1f1d1b]/25 underline-offset-4 transition-colors hover:decoration-[#1f1d1b]/60 disabled:opacity-50"
        >
          {status.kind === "rescraping" ? "Rescraping…" : "Rescrape"}
        </button>
      </div>
      {pending.flags && pending.flags.length > 0 && (
        <p className="mt-1 text-[11px] uppercase tracking-[0.18em] text-[#1f1d1b]/55">
          {pending.flags.join(" · ")}
        </p>
      )}
      <p className="mt-2 font-serif text-[13px] italic text-[#1f1d1b]/65">
        {pending.candidate.reason || <em>(no reason)</em>}
      </p>
      <p className="mt-2 break-all text-[12px] text-[#1f1d1b]/45">
        <a
          href={pending.directUrl}
          target="_blank"
          rel="noreferrer"
          className="hover:text-[#1f1d1b]/80"
        >
          {pending.directUrl}
        </a>
      </p>

      {/* ---------- Inline editor ---------- */}
      {open && (
        <div className="mt-5 space-y-4 border-l border-[#1f1d1b]/15 pl-5">
          <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
            <label className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
                Name
              </span>
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
              />
            </label>
            <label className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
                Brand
              </span>
              <input
                value={brand}
                onChange={(e) => setBrand(e.target.value)}
                className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
              />
            </label>
          </div>

          <label className="flex flex-col gap-1">
            <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
              Reason
            </span>
            <textarea
              value={reason}
              onChange={(e) => setReason(e.target.value)}
              rows={3}
              className="border border-[#1f1d1b]/20 bg-transparent px-3 py-2 font-serif text-[14px] leading-[1.5]"
            />
          </label>

          <div className="grid grid-cols-1 gap-3 md:grid-cols-3">
            <label className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
                Category
              </span>
              <select
                value={category}
                onChange={(e) => {
                  setCategory(e.target.value);
                  setSubcategory("");
                }}
                className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
              >
                <option value="">— pick —</option>
                {categories.map((c) => (
                  <option key={c.key} value={c.key}>
                    {c.label}
                  </option>
                ))}
              </select>
            </label>
            <label className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
                Subcategory
              </span>
              <input
                list={`pending-sub-${pending.directUrl}`}
                value={subcategory}
                onChange={(e) => setSubcategory(e.target.value)}
                placeholder={subcategoryOptions[0] ?? "uncategorized"}
                className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
              />
              <datalist id={`pending-sub-${pending.directUrl}`}>
                {subcategoryOptions.map((s) => (
                  <option key={s} value={s} />
                ))}
              </datalist>
            </label>
            <label className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
                Audience
              </span>
              <select
                value={audienceLabel}
                onChange={(e) => {
                  const v = e.target.value;
                  if (v === "Mens only") setAudience(["mens"]);
                  else if (v === "Womens only") setAudience(["womens"]);
                  else if (v === "Gender-neutral")
                    setAudience(["mens", "womens"]);
                  else setAudience([]);
                }}
                className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
              >
                <option value="None">None</option>
                <option value="Mens only">Mens only</option>
                <option value="Womens only">Womens only</option>
                <option value="Gender-neutral">Gender-neutral</option>
              </select>
            </label>
          </div>

          <div className="grid grid-cols-1 gap-3 md:grid-cols-[1fr_auto]">
            <label className="flex flex-col gap-1">
              <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
                Price range
              </span>
              <input
                value={priceRange}
                onChange={(e) => setPriceRange(e.target.value)}
                placeholder="$45–$60"
                className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
              />
            </label>
            <div className="flex items-end">
              <button
                type="button"
                onClick={onStage}
                disabled={
                  busy ||
                  !name.trim() ||
                  !brand.trim() ||
                  !category ||
                  !priceRange.trim()
                }
                className="border border-[#1f1d1b]/60 bg-[#1f1d1b] px-4 py-2 text-[11px] uppercase tracking-[0.22em] text-[#f6f1e7] transition-colors hover:bg-[#1f1d1b]/85 disabled:opacity-40"
              >
                {status.kind === "staging" ? "Staging…" : "Stage as draft"}
              </button>
            </div>
          </div>

          <p className="text-[11px] italic text-[#1f1d1b]/45">
            Images use the candidate&apos;s existing source URLs (or a fresh
            rescrape if none). After staging, open the draft card above to
            adjust images, atmosphere, or stability tier.
          </p>
        </div>
      )}

      {status.kind === "note" && (
        <p className="mt-3 font-serif text-[12px] italic text-[#1f1d1b]/60">
          {status.message}
        </p>
      )}

      {status.kind === "error" && (
        <p className="mt-3 font-serif text-[13px] italic text-[#a3431f]">
          {status.message}
        </p>
      )}
    </li>
  );
}

/* ---------- Single draft row ---------- */

function DraftCard({
  draft,
  categories,
  tree,
  onRemove,
}: {
  draft: DraftRow;
  categories: { key: string; label: string }[];
  tree: Record<string, string[]>;
  onRemove: (slug: string) => void;
}) {
  const router = useRouter();

  const [category, setCategory] = useState(draft.category);
  const [subcategory, setSubcategory] = useState(draft.subcategory);
  const [audience, setAudience] = useState<("mens" | "womens")[]>(
    draft.audience
  );
  const [status, setStatus] = useState<Status>({ kind: "idle" });

  const audienceLabel =
    audience.length === 0
      ? "None"
      : audience.length === 2
      ? "Gender-neutral"
      : audience[0] === "mens"
      ? "Mens only"
      : "Womens only";

  /** Patch the entry on disk with current row state (category, sub,
   *  audience). Used implicitly before Promote and on explicit Save. */
  async function patchEntry(): Promise<boolean> {
    setStatus({ kind: "saving" });
    const res = await fetch(`/api/admin/shop-item/${draft.slug}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: draft.name,
        brand: draft.brand,
        category,
        subcategory: subcategory || "uncategorized",
        audience,
        reason: draft.reason,
        priceRange: draft.priceRange || "Manual",
        url: draft.url,
        images: [draft.image],
        extractionMethod: draft.extractionMethod,
      }),
    });
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as {
        error?: string;
      };
      setStatus({ kind: "error", message: body.error ?? `HTTP ${res.status}` });
      return false;
    }
    setStatus({ kind: "idle" });
    return true;
  }

  async function onPromote() {
    if (!draft.reason.trim()) {
      setStatus({
        kind: "error",
        message: "This draft has no reason. Open Edit and add one before promoting.",
      });
      return;
    }
    const ok = await patchEntry();
    if (!ok) return;
    setStatus({ kind: "saving" });
    const res = await fetch("/api/admin/shop-drafts/promote", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ slug: draft.slug }),
    });
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as { error?: string };
      setStatus({
        kind: "error",
        message: body.error ?? `Promote failed (HTTP ${res.status})`,
      });
      return;
    }
    onRemove(draft.slug);
    router.refresh();
  }

  async function onUnstage() {
    if (
      !confirm(
        `Send "${draft.brand} ${draft.name}" back to the pending queue?\n\nThe entry will be removed from shop.ts. Images are preserved.`
      )
    ) {
      return;
    }
    setStatus({ kind: "saving" });
    const res = await fetch("/api/admin/shop-drafts/unstage", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ slug: draft.slug }),
    });
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as { error?: string };
      setStatus({
        kind: "error",
        message: body.error ?? `Unstage failed (HTTP ${res.status})`,
      });
      return;
    }
    onRemove(draft.slug);
    router.refresh();
  }

  async function onDelete() {
    if (
      !confirm(
        `Delete "${draft.brand} ${draft.name}" permanently?\n\nThe entry and its images will be removed. This cannot be undone from the UI.`
      )
    ) {
      return;
    }
    setStatus({ kind: "saving" });
    const res = await fetch(`/api/admin/shop-item/${draft.slug}`, {
      method: "DELETE",
    });
    if (!res.ok) {
      const body = (await res.json().catch(() => ({}))) as { error?: string };
      setStatus({
        kind: "error",
        message: body.error ?? `Delete failed (HTTP ${res.status})`,
      });
      return;
    }
    onRemove(draft.slug);
    router.refresh();
  }

  const subcategoryOptions = tree[category] ?? [];

  return (
    <li className="grid grid-cols-[120px_1fr] gap-6 border-t border-[#1f1d1b]/10 pt-6 md:grid-cols-[160px_1fr]">
      {/* Thumbnail */}
      <div className="relative aspect-square w-full bg-[#f3eee3]">
        {draft.image && (
          <Image
            src={draft.image}
            alt={`${draft.brand} ${draft.name}`}
            fill
            sizes="160px"
            className="object-cover"
            unoptimized
          />
        )}
      </div>

      {/* Body */}
      <div>
        <div className="flex flex-wrap items-baseline justify-between gap-3">
          <div>
            <div className="flex items-baseline gap-2">
              <p className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
                {draft.brand}
              </p>
              {draft.stabilityTier ? (
                // Tiny tier badge — small, declarative, no color noise.
                // 1 reads as "Forever Infrastructure"; 4 reads as
                // "manual-only / fragile" by convention. See
                // data/sourcing-policy.md.
                <span
                  title={`Stability tier ${draft.stabilityTier} — see data/sourcing-policy.md`}
                  className="text-[9px] uppercase tracking-[0.18em] text-[#1f1d1b]/45"
                >
                  T{draft.stabilityTier}
                </span>
              ) : null}
            </div>
            <h3 className="mt-1 font-serif text-[18px] leading-[1.3]">
              {draft.name}
            </h3>
          </div>
          <p className="text-[12px] uppercase tracking-[0.18em] text-[#1f1d1b]/55">
            {draft.priceRange || <em>price?</em>}
          </p>
        </div>

        <p className="mt-3 font-serif text-[14px] italic leading-[1.5] text-[#1f1d1b]/80">
          {draft.reason || (
            <em className="text-[#1f1d1b]/45">
              (no reason — open Edit and add one)
            </em>
          )}
        </p>

        <div className="mt-4 grid grid-cols-1 gap-3 md:grid-cols-3">
          {/* Category */}
          <label className="flex flex-col gap-1">
            <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
              Category
            </span>
            <select
              value={category}
              onChange={(e) => {
                setCategory(e.target.value);
                setSubcategory(""); // clear sub when top changes
              }}
              className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
            >
              <option value="">— pick —</option>
              {categories.map((c) => (
                <option key={c.key} value={c.key}>
                  {c.label}
                </option>
              ))}
            </select>
          </label>

          {/* Subcategory */}
          <label className="flex flex-col gap-1">
            <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
              Subcategory
            </span>
            <input
              list={`sub-${draft.slug}`}
              value={subcategory}
              onChange={(e) => setSubcategory(e.target.value)}
              className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
              placeholder={subcategoryOptions[0] ?? ""}
            />
            <datalist id={`sub-${draft.slug}`}>
              {subcategoryOptions.map((s) => (
                <option key={s} value={s} />
              ))}
            </datalist>
          </label>

          {/* Audience */}
          <label className="flex flex-col gap-1">
            <span className="text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
              Audience
            </span>
            <select
              value={audienceLabel}
              onChange={(e) => {
                const v = e.target.value;
                if (v === "Mens only") setAudience(["mens"]);
                else if (v === "Womens only") setAudience(["womens"]);
                else if (v === "Gender-neutral") setAudience(["mens", "womens"]);
                else setAudience([]);
              }}
              className="border border-[#1f1d1b]/20 bg-transparent px-3 py-1.5 font-serif text-[14px]"
            >
              <option value="None">None</option>
              <option value="Mens only">Mens only</option>
              <option value="Womens only">Womens only</option>
              <option value="Gender-neutral">Gender-neutral</option>
            </select>
          </label>
        </div>

        <div className="mt-5 flex flex-wrap items-center gap-3 text-[11px] uppercase tracking-[0.22em]">
          <button
            onClick={onPromote}
            disabled={status.kind === "saving"}
            className="border border-[#1f1d1b]/60 bg-[#1f1d1b] px-4 py-2 text-[#f6f1e7] transition-colors hover:bg-[#1f1d1b]/85 disabled:opacity-50"
          >
            Promote to live
          </button>
          <button
            onClick={onUnstage}
            disabled={status.kind === "saving"}
            className="border border-[#1f1d1b]/30 px-4 py-2 text-[#1f1d1b] transition-colors hover:bg-[#1f1d1b] hover:text-[#f6f1e7] disabled:opacity-50"
          >
            Send back
          </button>
          <Link
            href={`/admin/shop-edit/${draft.slug}`}
            className="border border-[#1f1d1b]/15 px-4 py-2 text-[#1f1d1b]/65 transition-colors hover:border-[#1f1d1b]/30 hover:text-[#1f1d1b]"
          >
            Edit
          </Link>
          <a
            href={draft.url}
            target="_blank"
            rel="noreferrer"
            className="text-[#1f1d1b]/55 hover:text-[#1f1d1b]/85"
          >
            Source ↗
          </a>
          <button
            onClick={onDelete}
            disabled={status.kind === "saving"}
            className="ml-auto text-[#1f1d1b]/45 hover:text-[#1f1d1b]/85 disabled:opacity-50"
          >
            Delete
          </button>
        </div>

        {status.kind === "error" && (
          <p className="mt-3 font-serif text-[13px] italic text-[#a3431f]">
            {status.message}
          </p>
        )}
      </div>
    </li>
  );
}
