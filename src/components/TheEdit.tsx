import Link from "next/link";

type Category = "recipes" | "living" | "style" | "practice" | "shop";

type EditItem = {
  title: string;
  href: string;
  category: Category;
};

/**
 * The Edit — homepage curated set.
 *
 * Hardcoded six-item editorial roundup, in order. Not randomized, not
 * pool-driven — Jordan curates this directly. The pillar mix (Recipes 1,
 * Living 2, Style 1, Practice 1, Shop 1) is intentional. Item titles are
 * editorial-piece headlines, not specific recipe titles. No terminal
 * punctuation on any item — parallel structure across the set.
 *
 * To rotate items: edit this list. Don't reintroduce randomization or
 * a wildcard slot.
 */
const EDIT_ITEMS: EditItem[] = [
  {
    title: "The breakfast I keep making",
    href: "/recipes/soft-scrambled-eggs-with-herbs",
    category: "recipes",
  },
  {
    title: "The 10-minute reset",
    href: "/living/the-10-minute-reset",
    category: "living",
  },
  {
    title: "The 5-piece rule",
    href: "/style/the-5-piece-rule",
    category: "style",
  },
  {
    title: "Tarot isn't prediction",
    href: "/practice/tarot-isnt-prediction",
    category: "practice",
  },
  {
    title: "Pieces that earn their place",
    href: "/shop",
    category: "shop",
  },
  {
    title: "Stop using fabric softener",
    href: "/living/stop-using-fabric-softener",
    category: "living",
  },
];

const CATEGORY_LABEL: Record<Category, string> = {
  recipes: "Recipes",
  living: "Living",
  style: "Style",
  practice: "Practice",
  shop: "Shop",
};

/**
 * The Edit — type-only editorial cards.
 *
 * Magazine table-of-contents register. Each card is a hairline above,
 * a small uppercase category eyebrow, an italic display title, and a
 * right-aligned arrow. No background gradients, no oversized type, no
 * fixed-aspect tile sizing — the section reads as a list of pieces,
 * not a stack of CTA panels.
 *
 * Layout:
 *   - Mobile (<sm)  : single column, full-width
 *   - Desktop (sm+) : two columns, breathing room between
 *
 * The whole section should fit close to one viewport on desktop, and
 * one or two scroll-flicks on mobile.
 */
export default function TheEdit() {
  return (
    <ul className="grid grid-cols-1 gap-x-12 sm:grid-cols-2 sm:gap-x-16 md:gap-x-20">
      {EDIT_ITEMS.map((item) => (
        <li key={`${item.category}-${item.href}-${item.title}`}>
          <Link
            href={item.href}
            className="
              group block border-t border-[#1f1d1b]/15 py-5 transition-colors
              duration-500 ease-out hover:border-[#1f1d1b]/40
              sm:py-6
            "
          >
            <p className="text-[10px] uppercase leading-none tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[10.5px]">
              {CATEGORY_LABEL[item.category]}
            </p>
            <div className="mt-3 flex items-baseline justify-between gap-4">
              <span
                className="
                  text-balance flex-1 font-serif text-[20px] font-normal italic
                  leading-[1.25] tracking-[-0.005em] text-[#2b1f17]/90
                  transition-colors duration-500 ease-out
                  group-hover:text-[#2b1f17]
                  sm:text-[22px] md:text-[24px]
                "
              >
                {item.title}
              </span>
              <span
                aria-hidden
                className="
                  shrink-0 font-serif text-[14px] not-italic leading-none
                  text-[#1f1d1b]/35
                  transition-colors duration-500 ease-out
                  group-hover:text-[#1f1d1b]/70
                "
              >
                &rarr;
              </span>
            </div>
          </Link>
        </li>
      ))}
    </ul>
  );
}
