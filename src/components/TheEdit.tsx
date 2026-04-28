"use client";

import { useEffect, useState } from "react";
import Link from "next/link";

type Category = "recipes" | "living" | "style" | "shop";

type EditItem = {
  title: string;
  href: string;
  category: Category;
};

/**
 * The Edit pool. Curated, magazine-feel titles spanning the four
 * Hessentials sections. Six items per render — one from each category,
 * plus two wildcards from anywhere.
 *
 * Aurelian is intentionally excluded. Aurelian content lives only on the
 * dedicated Aurelian page; surfacing it here would mix the editorial and
 * interpretive voices in a single section.
 */
const POOL: Record<Category, EditItem[]> = {
  recipes: [
    { title: "The 5 things I cook every week", href: "/recipes", category: "recipes" },
    { title: "Sunday rigatoni, the slow one", href: "/recipes/sunday-rigatoni", category: "recipes" },
    { title: "Tuscan orzo, fast and rich", href: "/recipes/tuscan-orzo", category: "recipes" },
    { title: "Caprese chicken, year-round", href: "/recipes/caprese-chicken", category: "recipes" },
    { title: "The breakfast I keep making", href: "/recipes/soft-scrambled-eggs-with-herbs", category: "recipes" },
  ],
  living: [
    { title: "Why you don't cook more", href: "/living/why-you-dont-cook-more", category: "living" },
    { title: "The 10-minute reset", href: "/living/the-10-minute-reset", category: "living" },
    { title: "Hosting without the production", href: "/living", category: "living" },
    { title: "Stop using fabric softener", href: "/living/stop-using-fabric-softener", category: "living" },
    { title: "The one pot that does everything", href: "/living/the-one-pot-that-does-everything", category: "living" },
  ],
  style: [
    { title: "Getting dressed without overthinking", href: "/style/the-uniform-is-not-boring", category: "style" },
    { title: "Texture is the outfit", href: "/style/texture-is-the-outfit", category: "style" },
    { title: "The 5-piece rule", href: "/style/the-5-piece-rule", category: "style" },
    { title: "The bag sets the tone", href: "/style/the-bag-sets-the-tone", category: "style" },
    { title: "The signature piece", href: "/style/the-signature-piece", category: "style" },
  ],
  shop: [
    { title: "I keep buying this", href: "/shop", category: "shop" },
    { title: "The closet edit", href: "/shop", category: "shop" },
    { title: "Pieces that earn their place", href: "/shop", category: "shop" },
    { title: "The kitchen, restocked", href: "/shop", category: "shop" },
  ],
};

const CATEGORIES: Category[] = ["recipes", "living", "style", "shop"];

function pickRandom<T>(items: readonly T[]): T {
  return items[Math.floor(Math.random() * items.length)];
}

function buildSelection(): EditItem[] {
  // One pick from each of the four categories.
  const base = CATEGORIES.map((c) => pickRandom(POOL[c]));
  // Two wildcards from anywhere, avoiding duplicates.
  const remaining = CATEGORIES.flatMap((c) =>
    POOL[c].filter((item) => !base.some((b) => b.href === item.href))
  );
  const w1 = pickRandom(remaining);
  const w2 = pickRandom(
    remaining.filter((item) => item.href !== w1.href)
  );
  return [...base, w1, w2];
}

// Stable initial selection for SSR — first item from each category, then
// second item from recipes and living as the two wildcards.
const INITIAL: EditItem[] = [
  POOL.recipes[0],
  POOL.living[0],
  POOL.style[0],
  POOL.shop[0],
  POOL.recipes[1],
  POOL.living[1],
];

/**
 * Six warm-tone gradients per spec §4.2. Cycled by SLOT POSITION
 * (card 1, 2, 3, 4, 5, 6 → palettes 1–6), not by article identity.
 *
 * Direction `135deg` (top-left lighter, bottom-right darker) is
 * intentional: title sits bottom-left, where the gradient has its
 * mid-tone, giving cream type maximal contrast without flat fill.
 */
const PALETTES: readonly string[] = [
  "linear-gradient(135deg, #d4a574 0%, #a06840 100%)", // amber
  "linear-gradient(135deg, #c4a888 0%, #6b4f3a 100%)", // taupe
  "linear-gradient(135deg, #6b5544 0%, #3d2a1f 100%)", // dark espresso
  "linear-gradient(135deg, #b8a285 0%, #8a6f4f 100%)", // tan
  "linear-gradient(135deg, #9c8264 0%, #4d3a26 100%)", // dark walnut
  "linear-gradient(135deg, #d4b896 0%, #b78659 100%)", // wheat
];

export default function TheEdit() {
  const [items, setItems] = useState<EditItem[]>(INITIAL);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setItems(buildSelection());
  }, []);

  return (
    <ul className="grid grid-cols-1 gap-x-8 gap-y-6 sm:grid-cols-2 md:grid-cols-3 md:gap-x-10 md:gap-y-10">
      {items.map((item, i) => (
        <li key={`${item.category}-${item.href}-${item.title}`}>
          <Link
            href={item.href}
            className="edit-tile group block transition-all duration-[400ms]"
          >
            <div
              className="
                edit-tile__block relative aspect-[5/3] cursor-pointer
                overflow-hidden rounded-[4px]
                md:aspect-auto md:h-[clamp(150px,16vw,200px)]
                transition-[transform,filter] duration-[400ms]
                ease-[cubic-bezier(0.22,1,0.36,1)]
                group-hover:-translate-y-0.5
                group-hover:brightness-105 group-hover:saturate-[1.05]
              "
              style={{ backgroundImage: PALETTES[i % PALETTES.length] }}
            >
              <div className="absolute inset-0 flex flex-col justify-end px-5 py-5 sm:px-6 sm:py-6 md:px-7 md:py-7">
                <div className="flex items-baseline justify-between gap-3.5">
                  <span
                    className="text-balance flex-1 font-serif text-[19px] font-normal italic leading-[1.22] tracking-[-0.005em] sm:text-[20px] md:text-[22px]"
                    style={{
                      color: "rgba(248, 246, 243, 0.97)",
                      textShadow: "0 1px 22px rgba(0,0,0,0.18)",
                    }}
                  >
                    {item.title}
                  </span>
                  <span
                    aria-hidden
                    className="flex-shrink-0 font-serif text-[16px] italic leading-none"
                    style={{ color: "rgba(248, 246, 243, 0.72)" }}
                  >
                    →
                  </span>
                </div>
              </div>
            </div>
          </Link>
        </li>
      ))}
    </ul>
  );
}
