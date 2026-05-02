"use client";

/**
 * Shop edit — detail form.
 *
 * Mirrors the field layout of the import page so muscle memory carries
 * across. Differences from import:
 *
 *   - Slug is read-only (rename = delete + re-import).
 *   - Image list is read-only — to change images, delete and re-import.
 *   - Reason field is editable here (this is where editorial copy lands).
 *
 * The save button writes via PATCH to the slug-keyed route. On 200, a
 * "saved" line appears; on error, the message surfaces below the form.
 */

import { useState } from "react";
import type { ExtractionMethod } from "../../../../data/shop";
import type { ProductForClient } from "./page";

const LABEL_CLS =
  "block text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55";
const INPUT_CLS =
  "mt-2 w-full border border-[#1f1d1b]/15 bg-white/40 px-3 py-2 font-serif text-[15px] text-[#1f1d1b] outline-none focus:border-[#1f1d1b]/40";
const TEXTAREA_CLS = `${INPUT_CLS} min-h-[80px] resize-y leading-[1.5]`;
const BUTTON_CLS =
  "inline-flex items-center justify-center border border-[#1f1d1b]/30 px-5 py-2.5 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b] transition-colors hover:bg-[#1f1d1b] hover:text-[#f6f1e7] disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-transparent disabled:hover:text-[#1f1d1b]";

export function EditClient({
  initial,
  tree,
}: {
  initial: ProductForClient;
  tree: Record<string, string[]>;
}) {
  const categories = Object.keys(tree);
  const [name, setName] = useState(initial.name);
  const [brand, setBrand] = useState(initial.brand);
  const [category, setCategory] = useState<string>(initial.category);
  const [subcategory, setSubcategory] = useState<string>(initial.subcategory);
  const [reason, setReason] = useState(initial.reason);
  const [priceRange, setPriceRange] = useState(initial.priceRange);
  const [url, setUrl] = useState(initial.url);
  const [extractionMethod, setExtractionMethod] = useState<ExtractionMethod>(
    initial.extractionMethod
  );
  const [htmlSelector, setHtmlSelector] = useState(initial.htmlPriceSelector);
  const [priceFloor, setPriceFloor] = useState(
    initial.priceFloor != null ? String(initial.priceFloor) : ""
  );

  const [saving, setSaving] = useState(false);
  const [savedAt, setSavedAt] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const dirty =
    name !== initial.name ||
    brand !== initial.brand ||
    category !== initial.category ||
    subcategory !== initial.subcategory ||
    reason !== initial.reason ||
    priceRange !== initial.priceRange ||
    url !== initial.url ||
    extractionMethod !== initial.extractionMethod ||
    htmlSelector !== initial.htmlPriceSelector ||
    priceFloor !== (initial.priceFloor != null ? String(initial.priceFloor) : "");

  const onSave = async () => {
    setError(null);
    setSaving(true);
    try {
      const res = await fetch(`/api/admin/shop-item/${initial.slug}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          brand,
          category,
          subcategory: subcategory || undefined,
          reason,
          priceRange,
          url,
          images: initial.images,
          extractionMethod,
          htmlPriceSelector:
            extractionMethod === "html" ? htmlSelector : undefined,
          priceFloor: priceFloor ? Number(priceFloor) : null,
        }),
      });
      const payload = (await res.json()) as { ok?: boolean; error?: string };
      if (!res.ok || !payload.ok) {
        throw new Error(payload.error ?? `HTTP ${res.status}`);
      }
      setSavedAt(new Date().toISOString());
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-10">
      <section className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div>
          <label htmlFor="slug" className={LABEL_CLS}>
            Slug — read only
          </label>
          <input
            id="slug"
            value={initial.slug}
            readOnly
            className={`${INPUT_CLS} font-mono text-[13px] text-[#1f1d1b]/55`}
          />
        </div>
        <div>
          <label htmlFor="name" className={LABEL_CLS}>
            Name
          </label>
          <input
            id="name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className={INPUT_CLS}
          />
        </div>
        <div>
          <label htmlFor="brand" className={LABEL_CLS}>
            Brand
          </label>
          <input
            id="brand"
            value={brand}
            onChange={(e) => setBrand(e.target.value)}
            className={INPUT_CLS}
          />
        </div>
        <div>
          <label htmlFor="category" className={LABEL_CLS}>
            Category
          </label>
          <select
            id="category"
            value={category}
            onChange={(e) => {
              const next = e.target.value;
              setCategory(next);
              if (subcategory && !(tree[next] ?? []).includes(subcategory)) {
                setSubcategory("");
              }
            }}
            className={INPUT_CLS}
          >
            {!categories.includes(category) && (
              <option value={category}>{category} (legacy)</option>
            )}
            {categories.map((c) => (
              <option key={c} value={c}>
                {c}
              </option>
            ))}
          </select>
          {!categories.includes(category) && (
            <p className="mt-2 font-serif text-[12px] italic text-[#a23a23]/80">
              Legacy category — switch to a new top-level and pick a
              subcategory.
            </p>
          )}
        </div>
        <div>
          <label htmlFor="subcategory" className={LABEL_CLS}>
            Subcategory
          </label>
          <input
            id="subcategory"
            list="edit-subcategories"
            value={subcategory}
            onChange={(e) =>
              setSubcategory(
                e.target.value
                  .toLowerCase()
                  .replace(/[^a-z0-9-]+/g, "-")
                  .replace(/-+/g, "-")
              )
            }
            className={`${INPUT_CLS} font-mono text-[13px]`}
            placeholder={
              categories.includes(category)
                ? (tree[category] ?? []).slice(0, 2).join(" / ") ||
                  "kebab-case"
                : "pick a category first"
            }
          />
          <datalist id="edit-subcategories">
            {(tree[category] ?? []).map((sub) => (
              <option key={sub} value={sub} />
            ))}
          </datalist>
        </div>
        <div className="sm:col-span-2">
          <label htmlFor="reason" className={LABEL_CLS}>
            Reason — editorial
          </label>
          <textarea
            id="reason"
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            className={TEXTAREA_CLS}
            placeholder="One line. The reason this earns its place."
          />
        </div>
        <div>
          <label htmlFor="priceRange" className={LABEL_CLS}>
            Price range
          </label>
          <input
            id="priceRange"
            value={priceRange}
            onChange={(e) => setPriceRange(e.target.value)}
            className={INPUT_CLS}
          />
        </div>
        <div>
          <label htmlFor="extractionMethod" className={LABEL_CLS}>
            Extraction method
          </label>
          <select
            id="extractionMethod"
            value={extractionMethod}
            onChange={(e) =>
              setExtractionMethod(e.target.value as ExtractionMethod)
            }
            className={INPUT_CLS}
          >
            <option value="json-ld">json-ld</option>
            <option value="shopify">shopify</option>
            <option value="html">html</option>
            <option value="manual">manual</option>
          </select>
        </div>
        {extractionMethod === "html" && (
          <div className="sm:col-span-2">
            <label htmlFor="selector" className={LABEL_CLS}>
              HTML price selector
            </label>
            <input
              id="selector"
              value={htmlSelector}
              onChange={(e) => setHtmlSelector(e.target.value)}
              className={`${INPUT_CLS} font-mono text-[13px]`}
              placeholder=".product-price .amount"
            />
          </div>
        )}
        <div>
          <label htmlFor="priceFloor" className={LABEL_CLS}>
            Price floor — optional
          </label>
          <input
            id="priceFloor"
            value={priceFloor}
            onChange={(e) =>
              setPriceFloor(e.target.value.replace(/[^0-9.]/g, ""))
            }
            className={INPUT_CLS}
            inputMode="decimal"
          />
        </div>
        <div className="sm:col-span-2">
          <label htmlFor="url" className={LABEL_CLS}>
            Source URL
          </label>
          <input
            id="url"
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className={INPUT_CLS}
          />
        </div>
      </section>

      {/* Images — read-only at this surface. */}
      <section className="border-t border-[#1f1d1b]/15 pt-8">
        <p className={LABEL_CLS}>Images — read only</p>
        <p className="mt-2 font-serif text-[13px] italic text-[#1f1d1b]/55">
          To change images, delete this product and re-import.
        </p>
        <ul className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
          {initial.images.map((src, i) => (
            <li key={src} className="border border-[#1f1d1b]/15">
              <div className="relative aspect-square bg-[#f0e9d9]">
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img
                  src={src}
                  alt=""
                  className="absolute inset-0 h-full w-full object-cover"
                />
              </div>
              <div className="px-2 py-1.5 text-[10px] uppercase tracking-[0.18em] text-[#1f1d1b]/55">
                {i + 1}
                {i === 0 ? " — primary" : ""}
              </div>
            </li>
          ))}
        </ul>
      </section>

      {/* Save */}
      <section className="flex flex-wrap items-center gap-4 border-t border-[#1f1d1b]/15 pt-8">
        <button
          type="button"
          onClick={onSave}
          disabled={saving || !dirty}
          className={BUTTON_CLS}
        >
          {saving ? "Saving…" : dirty ? "Save changes" : "No changes"}
        </button>
        {savedAt && !error && (
          <p className="font-serif text-[13px] italic text-[#1f1d1b]/65">
            Saved {new Date(savedAt).toLocaleTimeString()}.
          </p>
        )}
        {error && (
          <p className="font-mono text-[12px] text-[#a23a23]">{error}</p>
        )}
      </section>
    </div>
  );
}
