"use client";

/**
 * DrillDownHero — full-width grid of large clickable blocks below
 * the mosaic. Two registers:
 *
 *   - On `/shop`: blocks are pillars (Mens, Accessories, Grooming,
 *     Travel, Home). Click → `/shop/<pillar>`.
 *   - On `/shop/<pillar>`: blocks are subcategories under that
 *     pillar, prefixed by `All <pillar>`. Click → `/shop/<pillar>`
 *     for All, or `/shop/<pillar>/<sub>` for each sub.
 *
 * Each block is a slab of flat background with large serif type.
 * On hover, a single representative image fades in behind the type
 * — soft 30% opacity so the type still leads. No motion otherwise.
 */

import Image from "next/image";
import Link from "next/link";
import { useState } from "react";

export type DrillBlock = {
  /** Display label rendered inside the block. */
  label: string;
  /** Destination route. */
  href: string;
  /** Optional representative image for the hover state. */
  image?: string;
};

export default function DrillDownHero({
  blocks,
  eyebrow,
}: {
  blocks: DrillBlock[];
  /** Optional small uppercase label rendered above the grid. */
  eyebrow?: string;
}) {
  const [hovered, setHovered] = useState<string | null>(null);

  if (blocks.length === 0) return null;

  return (
    <section className="mx-auto w-full max-w-7xl px-6 py-24 sm:px-10 sm:py-32">
      {eyebrow && (
        <p className="mb-10 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
          {eyebrow}
        </p>
      )}
      <ul className="grid grid-cols-1 gap-px bg-[#1f1d1b]/8 sm:grid-cols-2 lg:grid-cols-3">
        {blocks.map((b) => {
          const isHover = hovered === b.href;
          return (
            <li key={b.href} className="relative">
              <Link
                href={b.href}
                onMouseEnter={() => setHovered(b.href)}
                onMouseLeave={() =>
                  setHovered((curr) => (curr === b.href ? null : curr))
                }
                className="relative flex aspect-[4/3] items-center justify-center overflow-hidden bg-[#f8f6f3] focus:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/40"
              >
                {/* Hover image — sits behind the label. Transition
                    uses opacity only; no transform / motion. */}
                {b.image && (
                  <Image
                    src={b.image}
                    alt=""
                    fill
                    sizes="(min-width: 1024px) 33vw, (min-width: 640px) 50vw, 100vw"
                    className={[
                      "object-cover transition-opacity duration-700 ease-out",
                      isHover ? "opacity-30" : "opacity-0",
                    ].join(" ")}
                  />
                )}
                <span
                  className="relative font-serif text-[clamp(2rem,4vw,3rem)] font-normal leading-[1.05] tracking-[-0.01em] text-[#1f1d1b] text-center"
                >
                  {b.label}
                </span>
              </Link>
            </li>
          );
        })}
      </ul>
    </section>
  );
}
