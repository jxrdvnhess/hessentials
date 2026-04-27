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

export default function TheEdit() {
  const [items, setItems] = useState<EditItem[]>(INITIAL);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setItems(buildSelection());
  }, []);

  return (
    <ul className="grid grid-cols-1 gap-x-12 gap-y-8 sm:grid-cols-2 md:grid-cols-3 md:gap-x-16 md:gap-y-12">
      {items.map((item) => (
        <li key={`${item.category}-${item.href}-${item.title}`}>
          <Link
            href={item.href}
            className="group block border-t border-[#1f1d1b]/10 pt-5 transition-colors duration-500 ease-out hover:border-[#1f1d1b]/35"
          >
            <span className="flex items-baseline gap-3 font-serif text-[clamp(1.125rem,1.7vw,1.375rem)] font-normal leading-[1.25] tracking-[-0.01em] text-balance text-[#1f1d1b]/85 transition-colors duration-500 ease-out group-hover:text-[#1f1d1b]">
              <span className="flex-1">{item.title}</span>
              <span
                aria-hidden
                className="text-[12px] not-italic text-[#1f1d1b]/35 transition-colors duration-500 ease-out group-hover:text-[#1f1d1b]/75"
              >
                →
              </span>
            </span>
          </Link>
        </li>
      ))}
    </ul>
  );
}
