"use client";

import { useMemo } from "react";
import { generateStyleReading } from "../lib/aurelian-style";
import type { Selection } from "../data/aurelian";

type Props = {
  sun: Selection;
  moon: Selection;
  rising: Selection;
};

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

function PracticalList({ items }: { items: readonly string[] }) {
  return (
    <ul className="mt-5 space-y-2.5 text-[15.5px] leading-[1.65] text-[#1f1d1b]/80 sm:text-[16.5px]">
      {items.map((item) => (
        <li key={item} className="relative pl-5">
          <span
            aria-hidden
            className="absolute left-0 top-0 text-[#1f1d1b]/35"
          >
            —
          </span>
          {item}
        </li>
      ))}
    </ul>
  );
}

export default function AurelianStyle({ sun, moon, rising }: Props) {
  const reading = useMemo(
    () => generateStyleReading({ sun, moon, rising }),
    [sun, moon, rising]
  );

  if (!reading) return null;

  const {
    opening,
    partialNote,
    naturalSignal,
    comfortLayer,
    expressionLayer,
    styleTension,
    recommendations,
    hessentialsDirection,
  } = reading;

  return (
    <section
      aria-label="How this shows up in style"
      className="mx-auto mt-32 max-w-[34rem] sm:mt-44"
    >
      {/* ---------- Title + Opening ---------- */}
      <h2 className="text-center font-serif text-[clamp(1.75rem,3.4vw,2.375rem)] font-normal leading-[1.1] tracking-[-0.02em] text-[#1f1d1b]">
        How This Shows Up in Style
      </h2>

      <p className="mx-auto mt-8 max-w-[28rem] text-center font-serif italic leading-[1.6] text-[#1f1d1b]/65">
        {opening}
      </p>

      {partialNote && (
        <p className="mx-auto mt-6 max-w-[26rem] text-center text-[12.5px] uppercase tracking-[0.22em] leading-[1.7] text-[#1f1d1b]/40 sm:text-[13px]">
          {partialNote}
        </p>
      )}

      <EmDash />

      {/* ---------- Placement layers ---------- */}
      <div className="space-y-14 sm:space-y-16">
        {naturalSignal && (
          <div>
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              Natural Signal — {naturalSignal.signName} Rising
            </p>
            <p className="text-pretty font-serif italic leading-[1.7] text-[#1f1d1b]/85">
              {naturalSignal.description}
            </p>
            <p className="mt-6 text-[12px] uppercase tracking-[0.22em] text-[#1f1d1b]/45 sm:text-[12.5px]">
              In practice, this favors
            </p>
            <PracticalList items={naturalSignal.favors} />
          </div>
        )}

        {comfortLayer && (
          <div>
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              What Actually Feels Right — {comfortLayer.signName} Moon
            </p>
            <p className="text-pretty font-serif italic leading-[1.7] text-[#1f1d1b]/85">
              {comfortLayer.description}
            </p>
            <p className="mt-6 text-[12px] uppercase tracking-[0.22em] text-[#1f1d1b]/45 sm:text-[12.5px]">
              In practice, this means
            </p>
            <PracticalList items={comfortLayer.favors} />
          </div>
        )}

        {expressionLayer && (
          <div>
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              What You&rsquo;re Expressing Over Time — {expressionLayer.signName} Sun
            </p>
            <p className="text-pretty font-serif italic leading-[1.7] text-[#1f1d1b]/85">
              {expressionLayer.description}
            </p>
            <p className="mt-6 text-[12px] uppercase tracking-[0.22em] text-[#1f1d1b]/45 sm:text-[12.5px]">
              In practice
            </p>
            <PracticalList items={expressionLayer.favors} />
          </div>
        )}
      </div>

      {/* ---------- Style Tension ---------- */}
      {styleTension && (
        <>
          <EmDash />
          <section aria-label="Style tension">
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              Style Tension
            </p>
            <p className="font-serif text-[clamp(1.25rem,2vw,1.5rem)] italic leading-[1.35] tracking-[-0.01em] text-[#1f1d1b]">
              {styleTension.pattern}
            </p>
            <p className="mt-6 text-pretty leading-[1.85] text-[#1f1d1b]/85">
              {styleTension.paragraph}
            </p>
          </section>
        </>
      )}

      {/* ---------- What Actually Works ---------- */}
      {recommendations.length > 0 && (
        <>
          <EmDash />
          <section aria-label="What actually works">
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              What Actually Works
            </p>
            <PracticalList items={recommendations} />
          </section>
        </>
      )}

      {/* ---------- Hessentials Style Direction ---------- */}
      {hessentialsDirection && (
        <>
          <EmDash />
          <section aria-label="Hessentials style direction">
            <p className="mb-4 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              Hessentials Style Direction
            </p>
            <p className="text-pretty leading-[1.85] text-[#1f1d1b]/85">
              {hessentialsDirection}
            </p>
          </section>
        </>
      )}
    </section>
  );
}
