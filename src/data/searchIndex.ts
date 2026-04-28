/**
 * Build-time search index for the global site search.
 *
 * Combined from the structured data sources (recipes, style, shop, aurelian's
 * pattern library) plus a hand-maintained list for Living, whose articles are
 * authored as markdown and aren't trivially importable in a client component.
 *
 * Keep this file simple: title, section, url, optional description. The
 * matcher is a substring check, ranked title-first.
 */

import { recipes } from "./recipes";
import { STYLE_ARTICLES } from "./style";
import { SHOP_PRODUCTS } from "./shop";

export type SearchSection =
  | "Recipes"
  | "Living"
  | "Style"
  | "Practice"
  | "Shop"
  | "Aurelian";

export type SearchItem = {
  title: string;
  section: SearchSection;
  url: string;
  description?: string;
};

/* ---------- Living (markdown-authored, hardcoded for indexing) ---------- */

const LIVING_ITEMS: SearchItem[] = [
  {
    title: "Why you don't cook more",
    section: "Living",
    url: "/living/why-you-dont-cook-more",
  },
  {
    title: "Why Most Kitchens Are Set Up Wrong",
    section: "Living",
    url: "/living/why-most-kitchens-are-set-up-wrong",
  },
  {
    title: "The 10-minute reset",
    section: "Living",
    url: "/living/the-10-minute-reset",
  },
  {
    title: "You're Not Bad with Plants",
    section: "Living",
    url: "/living/youre-not-bad-with-plants",
  },
  {
    title: "The One Pot That Does Everything",
    section: "Living",
    url: "/living/the-one-pot-that-does-everything",
  },
  {
    title: "Stop Buying Plush Blankets. Use Cotton.",
    section: "Living",
    url: "/living/stop-buying-plush-blankets-use-cotton",
  },
  {
    title: "Ditch the Coffee Machine. Get an Espresso Machine.",
    section: "Living",
    url: "/living/ditch-the-coffee-machine-get-an-espresso-machine",
  },
  {
    title: "Stop Using Fabric Softener",
    section: "Living",
    url: "/living/stop-using-fabric-softener",
  },
];

/* ---------- Practice (markdown-authored, hardcoded for indexing) ---------- */

const PRACTICE_ITEMS: SearchItem[] = [
  {
    title: "I Stopped Drinking at 30",
    section: "Practice",
    url: "/practice/i-stopped-drinking-at-30",
    description:
      "A clear-eyed audit, not a sobriety crusade. The drink wasn't the variable. The structure was.",
  },
  {
    title: "Why I write down what I want and carry it with me",
    section: "Practice",
    url: "/practice/practice-why-i-write-down-what-i-want",
    description:
      "Most of what people call wanting something doesn't survive a folded page in pen.",
  },
  {
    title: "Sound baths and how to tell which ones work",
    section: "Practice",
    url: "/practice/practice-sound-baths-how-to-tell-which-ones-work",
    description: "Most of them don't. Here's what you're listening for.",
  },
  {
    title: "11:11 is a real practice. It just isn't what people say it is.",
    section: "Practice",
    url: "/practice/practice-1111-is-a-real-practice",
    description:
      "The number doesn't mean anything. The pause means everything.",
  },
  {
    title: "Compliment one person every day. Make it specific.",
    section: "Practice",
    url: "/practice/practice-compliment-one-person-every-day",
    description:
      "Not because they need it. Because of what it does to you.",
  },
  {
    title: "Pick one stone. Know why.",
    section: "Practice",
    url: "/practice/practice-pick-one-stone-know-why",
    description: "Not for healing. For commitment.",
  },
  {
    title: "Walking is not slow running.",
    section: "Practice",
    url: "/practice/practice-walking-is-not-slow-running",
    description: "One is for the body. The other is for the rest of you.",
  },
  {
    title: "Go to Mass occasionally. Even if you're not Catholic.",
    section: "Practice",
    url: "/practice/practice-go-to-mass-occasionally",
    description:
      "One tradition's seriousness about the divine can deepen yours.",
  },
  {
    title: "Tarot isn't prediction. Here's what it is.",
    section: "Practice",
    url: "/practice/practice-tarot-isnt-prediction",
    description:
      "Stop asking it what's going to happen. Start asking it what's already true.",
  },
  {
    title: "The single object you carry.",
    section: "Practice",
    url: "/practice/practice-the-single-object-you-carry",
    description: "Not jewelry. Not a talisman. An anchor.",
  },
  {
    title: "Silence. Five minutes. No app.",
    section: "Practice",
    url: "/practice/practice-silence-five-minutes-no-app",
    description:
      "The thing every meditation app is selling you a worse version of.",
  },
  {
    title: "The annual review beats resolutions.",
    section: "Practice",
    url: "/practice/practice-the-annual-review-beats-resolutions",
    description:
      "Looking back is the practice. Looking forward is the byproduct.",
  },
];

/* ---------- Aurelian (Pattern Library, currently inline on page) ---------- */

const AURELIAN_ITEMS: SearchItem[] = [
  {
    title: "Aurelian",
    section: "Aurelian",
    url: "/aurelian",
    description:
      "The interpretive layer of Hessentials. Astrology used as behavioral framework — timing, pressure, instinct.",
  },
  {
    title: "Your Big Three",
    section: "Aurelian",
    url: "/aurelian#big-three",
    description: "Sun is direction. Moon is inner rhythm. Rising is how the world meets you.",
  },
  {
    title: "Fast Surface, Slow Interior",
    section: "Aurelian",
    url: "/aurelian#pattern-library",
    description: "Appears ready before they actually are.",
  },
  {
    title: "High Standards, Quiet Pressure",
    section: "Aurelian",
    url: "/aurelian#pattern-library",
    description: "Competence that looks effortless. The cost is internal.",
  },
  {
    title: "Early Yes, Late Cost",
    section: "Aurelian",
    url: "/aurelian#pattern-library",
    description: "Agreeing in the moment and negotiating with yourself afterward.",
  },
  {
    title: "Stable Until It Isn't",
    section: "Aurelian",
    url: "/aurelian#pattern-library",
    description: "Holds more than most realize. The issue is delayed response.",
  },
  {
    title: "Precision Under Pressure",
    section: "Aurelian",
    url: "/aurelian#pattern-library",
    description: "Tries to create order before it feels safe to move.",
  },
  {
    title: "The Arrival Gap",
    section: "Aurelian",
    url: "/aurelian#pattern-library",
    description:
      "The distance between how someone is first experienced and what is actually happening underneath.",
  },
];

/* ---------- Compose ---------- */

const RECIPE_ITEMS: SearchItem[] = recipes.map((r) => ({
  title: r.recipe.title,
  section: "Recipes",
  url: `/recipes/${r.slug}`,
  description: r.description,
}));

const STYLE_ITEMS: SearchItem[] = STYLE_ARTICLES.map((a) => ({
  title: a.title,
  section: "Style",
  url: `/style/${a.slug}`,
  description: a.dek || a.subtitle,
}));

const SHOP_ITEMS: SearchItem[] = SHOP_PRODUCTS.map((p) => ({
  title: p.name,
  section: "Shop" as const,
  url: "/shop",
  description: `${p.brand} — ${p.reason}`,
}));

export const SEARCH_INDEX: SearchItem[] = [
  ...RECIPE_ITEMS,
  ...LIVING_ITEMS,
  ...STYLE_ITEMS,
  ...PRACTICE_ITEMS,
  ...SHOP_ITEMS,
  ...AURELIAN_ITEMS,
];

/* ---------- Search ---------- */

export function searchIndex(query: string, limit = 8): SearchItem[] {
  const q = query.trim().toLowerCase();
  if (!q) return [];

  const titleHits: SearchItem[] = [];
  const descHits: SearchItem[] = [];

  for (const item of SEARCH_INDEX) {
    if (item.title.toLowerCase().includes(q)) {
      titleHits.push(item);
    } else if (item.description?.toLowerCase().includes(q)) {
      descHits.push(item);
    }
  }

  return [...titleHits, ...descHits].slice(0, limit);
}
