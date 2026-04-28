"use client";

import Link from "next/link";
import { FormEvent, useEffect, useRef, useState } from "react";
import {
  generateReading,
  PLACEMENT_LABEL,
  SIGN_LABELS,
  type Placement,
  type ReadingResult,
  type Selection,
} from "../data/aurelian";
import AurelianStyle from "./AurelianStyle";

type Field = {
  placement: Placement;
  label: string;
  helper: string;
  includeUnknown: boolean;
  required: boolean;
};

const FIELDS: Field[] = [
  {
    placement: "sun",
    label: "Sun",
    helper: "Identity",
    includeUnknown: false,
    required: false,
  },
  {
    placement: "moon",
    label: "Moon",
    helper: "Inner life",
    includeUnknown: true,
    required: false,
  },
  {
    placement: "rising",
    label: "Rising",
    helper: "Arrival",
    includeUnknown: true,
    required: false,
  },
];

type SignSelectProps = {
  field: Field;
  value: Selection;
  onChange: (value: Selection) => void;
};

function SignSelect({ field, value, onChange }: SignSelectProps) {
  return (
    <label className="block">
      <span className="mb-3 block text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/55 sm:text-[12px]">
        {field.label}
        <span className="ml-2 normal-case tracking-normal text-[#1f1d1b]/35">
          — {field.helper}
        </span>
      </span>
      <span className="relative block">
        <select
          value={value}
          onChange={(e) => onChange(e.target.value as Selection)}
          required={field.required}
          className="w-full appearance-none border-b border-[#1f1d1b]/20 bg-transparent py-3 pr-8 font-serif text-[18px] italic leading-tight text-[#1f1d1b] transition-colors duration-300 ease-out hover:border-[#1f1d1b]/45 focus:border-[#1f1d1b]/60 focus:outline-none sm:text-[19px]"
        >
          <option value="" disabled>
            Choose
          </option>
          {SIGN_LABELS.map(({ value: v, label }) => (
            <option key={v} value={v}>
              {label}
            </option>
          ))}
          {field.includeUnknown && (
            <option value="unknown">I don&rsquo;t know</option>
          )}
        </select>
        <span
          aria-hidden
          className="pointer-events-none absolute right-1 top-1/2 -translate-y-1/2 font-serif text-[14px] text-[#1f1d1b]/40"
        >
          ▾
        </span>
      </span>
    </label>
  );
}

function EmDash() {
  return (
    <div
      aria-hidden
      className="my-12 text-center font-serif text-[18px] text-[#1f1d1b]/30 sm:my-14"
    >
      —
    </div>
  );
}

/* ---------- Fixed deepening copy ---------- */

const WHAT_THIS_MEANS = [
  {
    label: "Where this shows up",
    body:
      "This pattern usually appears first in timing. When you move. When you wait. When you say yes before the internal system has finished deciding. When people assume they understand you because they have only met the version that arrives first.",
  },
  {
    label: "Where it costs you",
    body:
      "The cost is rarely dramatic at first. It shows up as over-explaining. Over-functioning. Privately recalibrating after publicly agreeing. Needing more time than people think you need. Appearing clearer than you feel.",
  },
  {
    label: "What changes when you see it",
    body:
      "Once the pattern is named, it becomes easier to stop arguing with yourself. You can separate instinct from pressure. Timing from avoidance. Readiness from performance. That is where the work begins.",
  },
];

export default function BigThree() {
  const [sun, setSun] = useState<Selection>("");
  const [moon, setMoon] = useState<Selection>("");
  const [rising, setRising] = useState<Selection>("");
  const [result, setResult] = useState<ReadingResult | null>(null);
  const [submitToken, setSubmitToken] = useState(0);
  const [emptyMessage, setEmptyMessage] = useState<string | null>(null);
  const readingRef = useRef<HTMLDivElement | null>(null);
  /** Latest submit token — used to drop stale refinement responses. */
  const latestTokenRef = useRef(0);

  // Reset reading whenever any selection changes after a reading has rendered.
  useEffect(() => {
    if (result !== null) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setResult(null);
      setEmptyMessage(null);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sun, moon, rising]);

  // Smooth-scroll the reading into view after it renders.
  useEffect(() => {
    if (!result || !readingRef.current) return;
    const node = readingRef.current;
    const id = window.setTimeout(() => {
      node.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 80);
    return () => window.clearTimeout(id);
  }, [submitToken, result]);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const reading = generateReading(sun, moon, rising);
    if (!reading) {
      setEmptyMessage(
        "Choose at least one placement above. One is enough to begin."
      );
      setResult(null);
      return;
    }
    setEmptyMessage(null);
    setResult(reading);
    const nextToken = submitToken + 1;
    setSubmitToken(nextToken);
    latestTokenRef.current = nextToken;

    // Background recognition-test pass. Fire-and-forget. Replaces the
    // synthesis / realLife / watchPoint / pattern fields when it returns.
    (async () => {
      try {
        const response = await fetch("/api/aurelian/refine", {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            reading,
            signs: { sun, moon, rising },
          }),
        });
        if (!response.ok) return;
        const data = (await response.json()) as {
          reading?: ReadingResult;
          refined?: boolean;
        };
        // Drop stale responses if the user has since re-submitted or cleared.
        if (latestTokenRef.current !== nextToken) return;
        if (!data.reading) return;
        setResult(data.reading);
      } catch {
        // Silently fall back to the locally generated reading.
      }
    })();
  };

  return (
    <div className="mx-auto w-full max-w-3xl">
      <form onSubmit={handleSubmit} className="space-y-12">
        <div className="grid gap-10 sm:gap-12 md:grid-cols-3 md:gap-10">
          <SignSelect
            field={FIELDS[0]}
            value={sun}
            onChange={(v) => setSun(v)}
          />
          <SignSelect
            field={FIELDS[1]}
            value={moon}
            onChange={(v) => setMoon(v)}
          />
          <SignSelect
            field={FIELDS[2]}
            value={rising}
            onChange={(v) => setRising(v)}
          />
        </div>

        <div className="text-center">
          {emptyMessage && (
            <p className="mb-6 text-[13px] leading-[1.65] text-[#1f1d1b]/60 sm:text-[14px]">
              {emptyMessage}
            </p>
          )}
          <button
            type="submit"
            className="inline-block cursor-pointer border border-[#1f1d1b]/70 px-9 py-4 text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b] transition-opacity duration-500 ease-out hover:opacity-60 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/60 focus-visible:ring-offset-4 focus-visible:ring-offset-[#f8f6f3]"
          >
            Read
          </button>
        </div>
      </form>

      {result && (
        <div
          key={submitToken}
          ref={readingRef}
          aria-live="polite"
          className="result-fade mx-auto mt-28 max-w-[32rem] text-[18px] leading-[1.85] text-[#1f1d1b]/85 sm:mt-36 sm:text-[19px]"
        >
          {/* Opening */}
          <p className="text-pretty font-serif italic text-[#1f1d1b]/65">
            {result.opening}
          </p>

          <EmDash />

          {/* Placement sections */}
          <div className="space-y-12">
            {result.placements.map((p) => (
              <div key={p.placement}>
                <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
                  {PLACEMENT_LABEL[p.placement]} — {p.signName}
                </p>
                <p className="text-pretty font-serif italic leading-[1.7] text-[#1f1d1b]/85">
                  {p.text}
                </p>
              </div>
            ))}
          </div>

          <EmDash />

          {/* Synthesis */}
          <section aria-label="Synthesis">
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              Synthesis
            </p>
            <p className="text-pretty">{result.synthesis}</p>
          </section>

          <EmDash />

          {/* Real-life pattern */}
          <section aria-label="Real-life pattern">
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              Real-life pattern
            </p>
            <p className="text-pretty">{result.realLife}</p>
          </section>

          <EmDash />

          {/* Watch point */}
          <section aria-label="Watch point">
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              Watch point
            </p>
            <p className="text-pretty">{result.watchPoint}</p>
          </section>

          <EmDash />

          {/* Closing */}
          <p className="text-pretty text-center font-serif italic text-[#1f1d1b]/55">
            {result.closing}
          </p>

          {/* ---------- What This Actually Means ---------- */}
          <section
            aria-label="What this actually means"
            className="mx-auto mt-32 max-w-[34rem] sm:mt-44"
          >
            <h2 className="text-center font-serif text-[clamp(1.75rem,3.4vw,2.375rem)] font-normal leading-[1.1] tracking-[-0.02em] text-[#1f1d1b]">
              What This Actually Means
            </h2>
            <p className="mx-auto mt-8 max-w-[28rem] text-center font-serif italic leading-[1.6] text-[#1f1d1b]/65">
              A chart does not matter because it sounds accurate. It matters when
              it changes how you understand your own behavior.
            </p>

            <div className="mt-16 space-y-12 sm:mt-20 sm:space-y-14">
              {WHAT_THIS_MEANS.map((entry, i) => (
                <div
                  key={entry.label}
                  className={
                    i > 0
                      ? "border-t border-[#1f1d1b]/15 pt-12 sm:pt-14"
                      : ""
                  }
                >
                  <p className="mb-5 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
                    {entry.label}
                  </p>
                  <p className="text-pretty leading-[1.85]">{entry.body}</p>
                </div>
              ))}
            </div>
          </section>

          {/* ---------- How This Shows Up in Style ---------- */}
          <AurelianStyle sun={sun} moon={moon} rising={rising} />

          {/* ---------- Now Wander ---------- */}
          <section
            aria-label="Continue"
            className="mx-auto mt-32 max-w-[34rem] text-center sm:mt-44"
          >
            <p className="mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              Now wander
            </p>
            <p className="text-pretty mx-auto max-w-md font-serif text-[clamp(1.125rem,1.6vw,1.25rem)] italic leading-[1.55] text-[#1f1d1b]/70">
              Read what pulls you. Cook something specific. The rest of
              the site is here.
            </p>
            <ul className="mt-10 flex flex-wrap items-center justify-center gap-x-6 gap-y-3 text-[11px] uppercase leading-none tracking-[0.24em] text-[#1f1d1b]/55 sm:text-[12px]">
              <li>
                <Link
                  href="/recipes"
                  className="transition-colors duration-500 ease-out hover:text-[#1f1d1b]"
                >
                  Recipes
                </Link>
              </li>
              <li>
                <Link
                  href="/living"
                  className="transition-colors duration-500 ease-out hover:text-[#1f1d1b]"
                >
                  Living
                </Link>
              </li>
              <li>
                <Link
                  href="/style"
                  className="transition-colors duration-500 ease-out hover:text-[#1f1d1b]"
                >
                  Style
                </Link>
              </li>
              <li>
                <Link
                  href="/practice"
                  className="transition-colors duration-500 ease-out hover:text-[#1f1d1b]"
                >
                  Practice
                </Link>
              </li>
              <li>
                <Link
                  href="/shop"
                  className="transition-colors duration-500 ease-out hover:text-[#1f1d1b]"
                >
                  Shop
                </Link>
              </li>
            </ul>
          </section>
        </div>
      )}
    </div>
  );
}
