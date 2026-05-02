"use client";

/**
 * Shop import — client component.
 *
 * Handles three phases:
 *
 *   1. URL paste → POST GET /preview SSE stream. As events arrive, fields
 *      paint into the form one at a time. Image thumbnails appear when
 *      each `image-ok` event lands so the page feels live.
 *   2. Review → user picks a category (required), tweaks anything wrong,
 *      optionally sets priceFloor, deselects unwanted images.
 *   3. Commit → POST /commit. On success, shows the resulting public
 *      paths and clears for the next import.
 *
 * Voice: declarative, sentence case. No "thoughtfully populated", no
 * "your product is ready". Just states.
 */

import { useCallback, useMemo, useRef, useState } from "react";
import type { ExtractionMethod } from "../../../data/shop";

type ParsedPayload = {
  name: string;
  brand: string;
  prices: number[];
  soldOut: boolean;
  images: string[];
  audience: ("mens" | "womens")[];
  extractionMethod: ExtractionMethod;
  host: string;
  priceRange: string;
  slug: string;
  slugCollision: boolean;
};

type Audience = "mens" | "womens";
type AudienceOption = "none" | "mens" | "womens" | "both";

function audienceToOption(a: readonly Audience[]): AudienceOption {
  const set = new Set(a);
  if (set.has("mens") && set.has("womens")) return "both";
  if (set.has("mens")) return "mens";
  if (set.has("womens")) return "womens";
  return "none";
}

function optionToAudience(opt: AudienceOption): Audience[] {
  if (opt === "none") return [];
  if (opt === "both") return ["mens", "womens"];
  return [opt];
}

const AUDIENCE_LABELS: Record<AudienceOption, string> = {
  none: "None",
  mens: "Mens only",
  womens: "Womens only",
  both: "Gender-neutral (both)",
};

type ImageState = {
  source: string;
  /** "pending" before probe completes, "ok" or "err" after. */
  status: "pending" | "ok" | "err";
  contentType?: string;
  bytes?: number | null;
  error?: string;
  selected: boolean;
};

type Phase = "idle" | "fetching" | "review" | "committing" | "done" | "error";

type CommitResponse = {
  ok?: boolean;
  slug?: string;
  saved?: { source: string; publicPath: string }[];
  failed?: { source: string; error: string }[];
  error?: string;
};

const LABEL_CLS =
  "block text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/55";
const INPUT_CLS =
  "mt-2 w-full border border-[#1f1d1b]/15 bg-white/40 px-3 py-2 font-serif text-[15px] text-[#1f1d1b] outline-none focus:border-[#1f1d1b]/40";
const BUTTON_CLS =
  "inline-flex items-center justify-center border border-[#1f1d1b]/30 px-5 py-2.5 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b] transition-colors hover:bg-[#1f1d1b] hover:text-[#f6f1e7] disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:bg-transparent disabled:hover:text-[#1f1d1b]";

export function ImportClient({
  tree,
}: {
  /** Top-level key → canonical subcategories. Free-text new subs are allowed. */
  tree: Record<string, string[]>;
}) {
  const categories = Object.keys(tree);
  const [url, setUrl] = useState("");
  const [phase, setPhase] = useState<Phase>("idle");
  const [streamLine, setStreamLine] = useState("");
  const [errorMsg, setErrorMsg] = useState("");

  // Editable form state — fed from the SSE stream, then user-editable.
  const [parsed, setParsed] = useState<ParsedPayload | null>(null);
  const [slug, setSlug] = useState("");
  const [name, setName] = useState("");
  const [brand, setBrand] = useState("");
  const [category, setCategory] = useState<string>("");
  const [subcategory, setSubcategory] = useState<string>("");
  const [audience, setAudience] = useState<Audience[]>([]);
  const [reason, setReason] = useState("");
  const [reasonState, setReasonState] = useState<
    "idle" | "generating" | "error"
  >("idle");
  const [reasonError, setReasonError] = useState<string | null>(null);
  const [priceRange, setPriceRange] = useState("");
  const [priceFloor, setPriceFloor] = useState("");
  const [extractionMethod, setExtractionMethod] =
    useState<ExtractionMethod>("manual");
  const [htmlSelector, setHtmlSelector] = useState("");
  const [images, setImages] = useState<ImageState[]>([]);

  const [commitResult, setCommitResult] = useState<CommitResponse | null>(
    null
  );

  const abortRef = useRef<AbortController | null>(null);

  const reset = useCallback(() => {
    abortRef.current?.abort();
    abortRef.current = null;
    setUrl("");
    setPhase("idle");
    setStreamLine("");
    setErrorMsg("");
    setParsed(null);
    setSlug("");
    setName("");
    setBrand("");
    setCategory("");
    setSubcategory("");
    setAudience([]);
    setReason("");
    setReasonState("idle");
    setReasonError(null);
    setPriceRange("");
    setPriceFloor("");
    setExtractionMethod("manual");
    setHtmlSelector("");
    setImages([]);
    setCommitResult(null);
  }, []);

  const startStream = useCallback(async () => {
    setErrorMsg("");
    setCommitResult(null);
    setParsed(null);
    setImages([]);
    setPhase("fetching");
    setStreamLine("Reading source.");

    const controller = new AbortController();
    abortRef.current = controller;

    try {
      const res = await fetch(
        `/api/admin/shop-import/preview?url=${encodeURIComponent(url)}`,
        { signal: controller.signal }
      );
      if (!res.ok) {
        throw new Error(`Preview HTTP ${res.status}`);
      }
      if (!res.body) throw new Error("No response stream");

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        // SSE messages are separated by a blank line.
        let sep = buffer.indexOf("\n\n");
        while (sep !== -1) {
          const raw = buffer.slice(0, sep);
          buffer = buffer.slice(sep + 2);
          handleEvent(raw);
          sep = buffer.indexOf("\n\n");
        }
      }
    } catch (e) {
      if ((e as Error).name === "AbortError") return;
      setPhase("error");
      setErrorMsg(e instanceof Error ? e.message : String(e));
    }

    function handleEvent(block: string) {
      const lines = block.split("\n");
      let event = "message";
      let data = "";
      for (const line of lines) {
        if (line.startsWith("event:")) event = line.slice(6).trim();
        else if (line.startsWith("data:")) data += line.slice(5).trim();
      }
      let payload: unknown = null;
      try {
        payload = data ? JSON.parse(data) : null;
      } catch {
        // ignore malformed
      }

      if (event === "phase" && payload) {
        const p = payload as { phase: string };
        if (p.phase === "fetching") setStreamLine("Reading source.");
      } else if (event === "parsed" && payload) {
        const p = payload as ParsedPayload;
        setParsed(p);
        setSlug(p.slug);
        setName(p.name);
        setBrand(p.brand);
        setPriceRange(p.priceRange);
        // URL-based audience hint from the extractor; the user can
        // override before commit via the dropdown.
        setAudience(p.audience ?? []);
        setExtractionMethod(p.extractionMethod);
        setImages(
          p.images.map((src) => ({
            source: src,
            status: "pending",
            selected: true,
          }))
        );
        setStreamLine(
          p.images.length
            ? `Parsed. Probing ${p.images.length} image${
                p.images.length === 1 ? "" : "s"
              }.`
            : "Parsed. No images found."
        );
      } else if (event === "image-ok" && payload) {
        const p = payload as {
          index: number;
          source: string;
          contentType: string;
          bytes: number | null;
        };
        setImages((curr) =>
          curr.map((img, i) =>
            i === p.index
              ? {
                  ...img,
                  status: "ok",
                  contentType: p.contentType,
                  bytes: p.bytes,
                }
              : img
          )
        );
      } else if (event === "image-err" && payload) {
        const p = payload as { index: number; error: string };
        setImages((curr) =>
          curr.map((img, i) =>
            i === p.index
              ? { ...img, status: "err", error: p.error, selected: false }
              : img
          )
        );
      } else if (event === "done") {
        setPhase("review");
        setStreamLine("Ready to review.");
      } else if (event === "error" && payload) {
        const p = payload as { error: string };
        setPhase("error");
        setErrorMsg(p.error);
      }
    }
  }, [url]);

  const onGenerateReason = useCallback(async () => {
    if (!name || !brand || !category) {
      setReasonError("Need name, brand, and category before generating.");
      return;
    }
    setReasonState("generating");
    setReasonError(null);
    try {
      const res = await fetch("/api/admin/generate-reason", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name,
          brand,
          category,
          subcategory: subcategory || undefined,
          url,
        }),
      });
      const payload = (await res.json()) as {
        reason?: string;
        refined?: boolean;
        error?: string;
      };
      if (!res.ok || !payload.refined || !payload.reason) {
        setReasonState("error");
        setReasonError(payload.error ?? `HTTP ${res.status}`);
        return;
      }
      setReason(payload.reason);
      setReasonState("idle");
    } catch (e) {
      setReasonState("error");
      setReasonError(e instanceof Error ? e.message : String(e));
    }
  }, [name, brand, category, subcategory, url]);

  const onCommit = useCallback(async () => {
    if (!category) {
      setErrorMsg("Pick a category before committing.");
      return;
    }
    if (!parsed) return;

    const selectedImages = images.filter((i) => i.selected).map((i) => i.source);
    if (!selectedImages.length) {
      setErrorMsg("Select at least one image.");
      return;
    }

    setPhase("committing");
    setErrorMsg("");
    setStreamLine("Downloading images and writing shop.ts.");

    try {
      const res = await fetch("/api/admin/shop-import/commit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          slug,
          name,
          brand,
          category,
          subcategory: subcategory || undefined,
          audience,
          reason,
          priceRange,
          url,
          images: selectedImages,
          extractionMethod,
          htmlPriceSelector:
            extractionMethod === "html" ? htmlSelector : undefined,
          priceFloor: priceFloor ? Number(priceFloor) : undefined,
        }),
      });
      const payload = (await res.json()) as CommitResponse;
      if (!res.ok || !payload.ok) {
        setPhase("error");
        setErrorMsg(payload.error ?? `Commit HTTP ${res.status}`);
        return;
      }
      setCommitResult(payload);
      setPhase("done");
      setStreamLine("Saved. Reason field is empty — fill in editorially.");
    } catch (e) {
      setPhase("error");
      setErrorMsg(e instanceof Error ? e.message : String(e));
    }
  }, [
    category,
    subcategory,
    audience,
    reason,
    parsed,
    images,
    slug,
    name,
    brand,
    priceRange,
    url,
    extractionMethod,
    htmlSelector,
    priceFloor,
  ]);

  const canStart =
    phase === "idle" || phase === "review" || phase === "done" || phase === "error";

  const reviewable = phase === "review" || phase === "committing";
  const canCommit = reviewable && phase !== "committing";

  const slugWarning = useMemo(() => {
    if (!parsed) return "";
    if (parsed.slugCollision && slug === parsed.slug) {
      return "A product with that slug already exists. The next free name was chosen.";
    }
    return "";
  }, [parsed, slug]);

  return (
    <div className="space-y-10">
      {/* URL input */}
      <section>
        <label htmlFor="url" className={LABEL_CLS}>
          Source URL
        </label>
        <div className="mt-2 flex flex-col gap-3 sm:flex-row">
          <input
            id="url"
            type="url"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            disabled={!canStart}
            placeholder="https://example.com/products/..."
            className={`${INPUT_CLS} mt-0 flex-1`}
            onKeyDown={(e) => {
              if (e.key === "Enter" && url && canStart) {
                e.preventDefault();
                startStream();
              }
            }}
          />
          <button
            type="button"
            onClick={startStream}
            disabled={!url || phase === "fetching"}
            className={BUTTON_CLS}
          >
            {phase === "fetching" ? "Reading…" : "Read"}
          </button>
          {phase !== "idle" && (
            <button type="button" onClick={reset} className={BUTTON_CLS}>
              Reset
            </button>
          )}
        </div>

        {streamLine && (
          <p className="mt-3 font-serif text-[13px] italic text-[#1f1d1b]/55">
            {streamLine}
          </p>
        )}
        {errorMsg && (
          <p className="mt-3 font-mono text-[12px] leading-[1.5] text-[#a23a23]">
            {errorMsg}
          </p>
        )}
      </section>

      {/* Parsed fields */}
      {parsed && (
        <section className="space-y-6 border-t border-[#1f1d1b]/15 pt-10">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
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
              <label htmlFor="slug" className={LABEL_CLS}>
                Slug
              </label>
              <input
                id="slug"
                value={slug}
                onChange={(e) =>
                  setSlug(
                    e.target.value
                      .toLowerCase()
                      .replace(/[^a-z0-9-]+/g, "-")
                      .replace(/-+/g, "-")
                  )
                }
                className={`${INPUT_CLS} font-mono text-[13px]`}
              />
              {slugWarning && (
                <p className="mt-2 font-serif text-[12px] italic text-[#1f1d1b]/55">
                  {slugWarning}
                </p>
              )}
            </div>
            <div>
              <label htmlFor="category" className={LABEL_CLS}>
                Category (required)
              </label>
              <select
                id="category"
                value={category}
                onChange={(e) => {
                  const next = e.target.value;
                  setCategory(next);
                  // Wipe subcategory when the parent changes — it almost
                  // certainly isn't valid under the new top-level.
                  if (
                    subcategory &&
                    !(tree[next] ?? []).includes(subcategory)
                  ) {
                    setSubcategory("");
                  }
                  // Audience fallback: when nothing was inferred from
                  // the URL, derive from a gendered top-level. The
                  // user can still override.
                  if (audience.length === 0) {
                    if (next === "mens") setAudience(["mens"]);
                    else if (next === "womens") setAudience(["womens"]);
                  }
                }}
                className={INPUT_CLS}
              >
                <option value="">Select a category</option>
                {categories.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label htmlFor="subcategory" className={LABEL_CLS}>
                Subcategory (optional)
              </label>
              <input
                id="subcategory"
                list="import-subcategories"
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
                  category
                    ? (tree[category] ?? []).slice(0, 2).join(" / ") ||
                      "kebab-case"
                    : "pick a category first"
                }
                disabled={!category}
              />
              <datalist id="import-subcategories">
                {(tree[category] ?? []).map((sub) => (
                  <option key={sub} value={sub} />
                ))}
              </datalist>
              {subcategory &&
                category &&
                !(tree[category] ?? []).includes(subcategory) && (
                  <p className="mt-2 font-serif text-[12px] italic text-[#1f1d1b]/55">
                    New subcategory — will save on the product. Add it to
                    categories.ts to make it canonical.
                  </p>
                )}
            </div>
            <div className="sm:col-span-2">
              <label htmlFor="audience" className={LABEL_CLS}>
                Audience
              </label>
              <select
                id="audience"
                value={audienceToOption(audience)}
                onChange={(e) =>
                  setAudience(
                    optionToAudience(e.target.value as AudienceOption)
                  )
                }
                className={INPUT_CLS}
              >
                {(["none", "mens", "womens", "both"] as AudienceOption[]).map(
                  (opt) => (
                    <option key={opt} value={opt}>
                      {AUDIENCE_LABELS[opt]}
                    </option>
                  )
                )}
              </select>
              <p className="mt-2 font-serif text-[12px] italic text-[#1f1d1b]/55">
                Gender-neutral items appear in both Mens and Womens shop
                pillars.
              </p>
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
              {parsed.prices.length > 0 && (
                <p className="mt-2 font-mono text-[11px] text-[#1f1d1b]/55">
                  Source variants: {parsed.prices.map((p) => `$${p}`).join(", ")}
                  {parsed.soldOut ? " (sold out)" : ""}
                </p>
              )}
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
                Price floor (optional)
              </label>
              <input
                id="priceFloor"
                value={priceFloor}
                onChange={(e) =>
                  setPriceFloor(e.target.value.replace(/[^0-9.]/g, ""))
                }
                className={INPUT_CLS}
                inputMode="decimal"
                placeholder="e.g. 50"
              />
            </div>
            <div className="sm:col-span-2">
              <div className="flex items-baseline justify-between gap-3">
                <label htmlFor="reason" className={LABEL_CLS}>
                  Reason (editorial)
                </label>
                <div className="flex items-center gap-3">
                  {reasonError && (
                    <span className="font-mono text-[10px] text-[#a23a23]">
                      {reasonError}
                    </span>
                  )}
                  <button
                    type="button"
                    onClick={onGenerateReason}
                    disabled={
                      reasonState === "generating" ||
                      !name ||
                      !brand ||
                      !category
                    }
                    className="border border-[#1f1d1b]/40 px-3 py-1.5 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b] transition-colors hover:bg-[#1f1d1b] hover:text-[#f6f1e7] disabled:cursor-not-allowed disabled:opacity-30 disabled:hover:bg-transparent disabled:hover:text-[#1f1d1b]"
                  >
                    {reasonState === "generating"
                      ? "Drafting…"
                      : reason
                      ? "Regenerate"
                      : "Generate"}
                  </button>
                </div>
              </div>
              <textarea
                id="reason"
                value={reason}
                onChange={(e) => setReason(e.target.value)}
                placeholder="One line. The reason this earns its place. Or click Generate."
                className={`${INPUT_CLS} min-h-[72px] resize-y leading-[1.5] placeholder:italic placeholder:text-[#1f1d1b]/35`}
              />
              <p className="mt-2 font-serif text-[12px] italic text-[#1f1d1b]/55">
                Generated lines are drafts — review before commit.
              </p>
            </div>
          </div>

          {/* Images */}
          <div className="border-t border-[#1f1d1b]/15 pt-8">
            <p className={LABEL_CLS}>Images (primary first)</p>
            {images.length === 0 ? (
              <p className="mt-3 font-serif text-[14px] italic text-[#1f1d1b]/55">
                No images parsed from the source.
              </p>
            ) : (
              <ul className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
                {images.map((img, i) => (
                  <li
                    key={img.source}
                    className={`group relative border ${
                      img.selected
                        ? "border-[#1f1d1b]/30"
                        : "border-[#1f1d1b]/10 opacity-50"
                    }`}
                  >
                    <button
                      type="button"
                      onClick={() =>
                        setImages((curr) =>
                          curr.map((c, ci) =>
                            ci === i
                              ? { ...c, selected: !c.selected }
                              : c
                          )
                        )
                      }
                      className="block w-full"
                      title={img.source}
                    >
                      <div className="relative aspect-square bg-[#f0e9d9]">
                        {img.status === "ok" ? (
                          // Plain <img>: this is admin-only, dev-only, and
                          // remote hosts aren't in next.config remotePatterns.
                          // eslint-disable-next-line @next/next/no-img-element
                          <img
                            src={img.source}
                            alt=""
                            className="absolute inset-0 h-full w-full object-cover"
                          />
                        ) : img.status === "pending" ? (
                          <div className="absolute inset-0 flex items-center justify-center text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/40">
                            Probing…
                          </div>
                        ) : (
                          <div className="absolute inset-0 flex items-center justify-center px-2 text-center text-[10px] uppercase tracking-[0.22em] text-[#a23a23]/70">
                            {img.error ?? "Failed"}
                          </div>
                        )}
                      </div>
                      <div className="flex items-center justify-between border-t border-[#1f1d1b]/10 px-2 py-1.5">
                        <span className="text-[10px] uppercase tracking-[0.18em] text-[#1f1d1b]/55">
                          {i + 1}
                          {i === 0 ? " (primary)" : ""}
                        </span>
                        <span className="text-[10px] uppercase tracking-[0.18em] text-[#1f1d1b]/45">
                          {img.selected ? "Keep" : "Skip"}
                        </span>
                      </div>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Commit */}
          <div className="flex flex-wrap items-center gap-4 border-t border-[#1f1d1b]/15 pt-8">
            <button
              type="button"
              onClick={onCommit}
              disabled={!canCommit}
              className={BUTTON_CLS}
            >
              {phase === "committing" ? "Saving…" : "Commit to shop.ts"}
            </button>
            <p className="font-serif text-[13px] italic text-[#1f1d1b]/55">
              Writes images to /public/shop and appends an entry to
              src/data/shop.ts.
            </p>
          </div>
        </section>
      )}

      {/* Commit result */}
      {commitResult?.ok && (
        <section className="border-t border-[#1f1d1b]/15 pt-8">
          <p className={LABEL_CLS}>Saved</p>
          <p className="mt-3 font-serif text-[15px] text-[#1f1d1b]">
            Slug:{" "}
            <span className="font-mono text-[13px]">
              {commitResult.slug}
            </span>
          </p>
          {commitResult.saved && commitResult.saved.length > 0 && (
            <ul className="mt-4 space-y-1 font-mono text-[12px] text-[#1f1d1b]/75">
              {commitResult.saved.map((s) => (
                <li key={s.publicPath}>{s.publicPath}</li>
              ))}
            </ul>
          )}
          {commitResult.failed && commitResult.failed.length > 0 && (
            <div className="mt-5">
              <p className={LABEL_CLS}>Failed</p>
              <ul className="mt-2 space-y-1 font-mono text-[12px] text-[#a23a23]">
                {commitResult.failed.map((f) => (
                  <li key={f.source}>
                    {f.source} — {f.error}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <p className="mt-6 font-serif text-[14px] italic text-[#1f1d1b]/65">
            Now open src/data/shop.ts and write the reason line.
          </p>
        </section>
      )}
    </div>
  );
}
