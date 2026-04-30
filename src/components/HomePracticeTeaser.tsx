"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import Link from "next/link";
import ImagePoemLine from "./ImagePoemLine";

/**
 * Homepage Practice statement teaser.
 *
 * Replaces The Edit cream zone. Where The Edit was a six-tile roundup,
 * this is the opposite move: one Practice piece, full editorial weight,
 * standalone. Practice carries the brand's most distinctive editorial
 * voice — the curation IS the value, so giving it depth instead of
 * breadth is the point.
 *
 * Selection model
 *   Hand-picked rotation pool of five Practice articles, date-seeded
 *   so every visitor on the same calendar day sees the same feature.
 *   Rolls over at the visitor's local midnight. To change what's in
 *   rotation, edit FEATURED_PRACTICE — nothing else picks from the
 *   broader pillar.
 *
 * Layout
 *   Desktop: 7/5 split, image LEFT, text RIGHT (sibling to the
 *   Mother's Day module above so they read as one editorial language).
 *   Mobile: image-top stacked, text below on cream.
 *
 * Photography
 *   The dinner photograph (merida-moment-4) and the "What was real,
 *   stayed." line are the Practice slot's fixed visual identity — same
 *   image and poem line every day, regardless of which article is on
 *   rotation. The image used to anchor the homepage closer; promoting
 *   it here keeps that editorial weight while letting the headline
 *   carry the variety. The site closes via the universal SiteFooter
 *   (morning-merida) instead.
 */

type Featured = {
  slug: string;
  title: string;
  descriptor: string;
};

const FEATURED_PRACTICE: readonly Featured[] = [
  {
    slug: "i-stopped-drinking-at-30",
    title: "I Stopped Drinking at 30",
    descriptor:
      "a clear-eyed audit, not a sobriety crusade. the drink wasn't the variable.",
  },
  {
    slug: "practice-tarot-isnt-prediction",
    title: "Tarot isn't prediction. Here's what it is.",
    descriptor:
      "stop asking it what's going to happen. start asking it what's already true.",
  },
  {
    slug: "practice-1111-is-a-real-practice",
    title: "11:11 is a real practice. It just isn't what people say it is.",
    descriptor: "the number doesn't mean anything. the pause means everything.",
  },
  {
    slug: "practice-compliment-one-person-every-day",
    title: "Compliment one person every day. Make it specific.",
    descriptor: "not because they need it. because of what it does to you.",
  },
  {
    slug: "practice-go-to-mass-occasionally",
    title: "Go to Mass occasionally. Even if you're not Catholic.",
    descriptor:
      "one tradition's seriousness about the divine can deepen yours.",
  },
];

/** Fixed image for the slot (see component header). */
const PRACTICE_SLOT_IMAGE = "/home/merida-moment-4.jpg";

/* ---------- Date-seeded picker ---------- */

function hashStringToInt(input: string): number {
  let h = 0;
  for (let i = 0; i < input.length; i += 1) {
    h = ((h << 5) - h + input.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

function todayKey(): string {
  const d = new Date();
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

function pickFeaturedForDay(): Featured {
  const idx =
    hashStringToInt(`practice|${todayKey()}`) % FEATURED_PRACTICE.length;
  return FEATURED_PRACTICE[idx];
}

/* ---------- Component ---------- */

export default function HomePracticeTeaser() {
  // SSR returns the first item for stability; the client upgrades to
  // the date-seeded pick after mount. Avoids hydration mismatch when
  // client and server disagree on local date.
  const [featured, setFeatured] = useState<Featured>(FEATURED_PRACTICE[0]);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setFeatured(pickFeaturedForDay());
  }, []);

  const href = `/practice/${featured.slug}`;
  const headline = featured.title.toLowerCase();
  const descriptor = featured.descriptor;

  return (
    <section
      aria-labelledby="practice-teaser-headline"
      className="relative w-full"
    >
      <div className="mx-auto w-full max-w-[1400px] px-6 sm:px-10 md:px-16">
        {/* PRACTICE eyebrow + hairline removed so the dinner photo
            lands as the next beat in the cinematic arc, not a
            separately-labelled module. The article headline + URL
            carry the pillar identity now; the photo + line do the
            visual work. */}

        {/* Spread — image LEFT, text RIGHT on md+. Mirrors the Mother's
            Day module's 7/5 proportion so the two read as siblings. */}
        <div className="grid grid-cols-1 items-center gap-y-10 md:grid-cols-12 md:gap-x-12 lg:gap-x-16">
          {/* Image — fixed slot identity (merida-moment-4 + the
              "What was real, stayed." line that used to live on the
              homepage closer). The line sits in the upper-left
              plaster zone (clean wall area above and to the left of
              the older man), where it reads cleanly against the warm
              wall without crowding the figures or the pendants. */}
          <div className="md:col-span-7">
            <div className="relative aspect-[4/5] w-full overflow-hidden md:aspect-[4/3]">
              <Image
                src={PRACTICE_SLOT_IMAGE}
                alt=""
                fill
                sizes="(min-width: 768px) 58vw, 100vw"
                quality={92}
                className="object-cover"
              />
              <ImagePoemLine
                position={{
                  top: "10%",
                  left: "7%",
                  maxWidth: "min(24rem, 58%)",
                  align: "left",
                }}
                size="sm"
              >
                What was real, stayed.
              </ImagePoemLine>
            </div>
          </div>

          {/* Text */}
          <div className="md:col-span-5">
            <Link
              id="practice-teaser-headline"
              href={href}
              className="block font-serif text-[clamp(1.875rem,3vw,2.5rem)] italic leading-[1.16] tracking-[-0.01em] text-[#1f1d1b] transition-opacity duration-300 hover:opacity-70"
            >
              {headline}
            </Link>
            <p className="mt-6 max-w-[34rem] text-[14.5px] leading-[1.55] text-[#1f1d1b]/55 sm:text-[15px]">
              {descriptor}
            </p>
            <Link
              href={href}
              className="mt-10 inline-flex items-center gap-2 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/65 transition-colors duration-300 hover:text-[#1f1d1b] sm:text-[12px]"
            >
              Read
              <span aria-hidden>→</span>
            </Link>
          </div>
        </div>
      </div>
    </section>
  );
}
