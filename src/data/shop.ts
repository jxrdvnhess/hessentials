/**
 * Hessentials Shop — curated edit, not a marketplace.
 *
 * Image paths point at /public/shop/<slug>.jpg. Drop the matching images in
 * that directory once they're sourced; the cards render a quiet plaster
 * placeholder until the image lands. URLs are best-effort brand product
 * pages — verify each before launch and replace any that have rotated.
 */

export type PriceTier = "$" | "$$" | "$$$";

export type ShopProduct = {
  slug: string;
  name: string;
  brand: string;
  reason: string;
  priceRange: PriceTier;
  /** External product page (or brand homepage as a safe fallback). */
  url: string;
  /** Local path under /public — drop the image here when sourced. */
  image: string;
};

export type ShopCategory = {
  slug: string;
  number: string;
  name: string;
  pov: string;
  products: ShopProduct[];
};

export const SHOP_INTRO = `This is not everything.\n\nIt’s what stayed.\n\nThings I’ve bought.\n\nUsed.\n\nKept.\n\nBecause they hold up in real life.`;

export const SHOP_CATEGORIES: ShopCategory[] = [
  {
    slug: "getting-dressed",
    number: "01",
    name: "Getting Dressed",
    pov: "This is what stays in rotation. Not what gets tried on.",
    products: [
      {
        slug: "prada-americas-cup-sneaker",
        name: "America’s Cup Leather Sneaker",
        brand: "Prada",
        reason: "You don’t rotate these. They stay in.",
        priceRange: "$$$",
        url: "https://www.prada.com/us/en/man/shoes/sneakers.html",
        image: "/shop/prada-americas-cup-sneaker.jpg",
      },
      {
        slug: "massimo-dutti-tailored-trouser",
        name: "Slim Fit Wool Trouser",
        brand: "Massimo Dutti",
        reason: "Reads more expensive than it is. By a lot.",
        priceRange: "$$",
        url: "https://www.massimodutti.com/us/men/clothing/trousers-c1473512.html",
        image: "/shop/massimo-dutti-tailored-trouser.jpg",
      },
      {
        slug: "club-monaco-ribbed-tank",
        name: "Ribbed Tank Top",
        brand: "Club Monaco",
        reason: "Layers cleanly. Holds its shape under everything.",
        priceRange: "$$",
        url: "https://www.clubmonaco.com",
        image: "/shop/club-monaco-ribbed-tank.jpg",
      },
      {
        slug: "quince-linen-pant",
        name: "European Linen Drawstring Pant",
        brand: "Quince",
        reason: "When you want to look put together without trying.",
        priceRange: "$",
        url: "https://www.quince.com/men/european-linen-drawstring-pant",
        image: "/shop/quince-linen-pant.jpg",
      },
      {
        slug: "goodfellow-chino-shorts",
        name: "7\" Chino Shorts",
        brand: "Goodfellow & Co.",
        reason: "Cheap in price. Not in how they wear.",
        priceRange: "$",
        url: "https://www.target.com/c/men-s-shorts/-/N-5xtdc",
        image: "/shop/goodfellow-chino-shorts.jpg",
      },
      {
        slug: "birkenstock-arizona-sandal",
        name: "Arizona Soft Footbed Sandal",
        brand: "Birkenstock",
        reason: "You stop noticing them after five minutes. That’s the point.",
        priceRange: "$$",
        url: "https://www.birkenstock.com/us/arizona-soft-footbed-suede-leather/arizona-softfootbedssfb-suedeleather-suedeleather-0-eva-u.html",
        image: "/shop/birkenstock-arizona-sandal.jpg",
      },
    ],
  },
  {
    slug: "in-transit",
    number: "02",
    name: "In Transit",
    pov: "What carries the day. Without becoming the problem.",
    products: [
      {
        slug: "prada-leather-duffle",
        name: "Leather Travel Duffle",
        brand: "Prada",
        reason: "Holds everything. Doesn’t feel like you packed too much.",
        priceRange: "$$$",
        url: "https://www.prada.com/us/en/man/bags/duffle-bags.html",
        image: "/shop/prada-leather-duffle.jpg",
      },
      {
        slug: "prada-belt-bag",
        name: "Re-Nylon and Leather Belt Bag",
        brand: "Prada",
        reason: "When you want to carry less but still need it close.",
        priceRange: "$$$",
        url: "https://www.prada.com/us/en/man/bags/belt-bags.html",
        image: "/shop/prada-belt-bag.jpg",
      },
      {
        slug: "johnston-murphy-xc4-backpack",
        name: "XC4 Leather Backpack",
        brand: "Johnston & Murphy",
        reason: "Looks like a briefcase. Carries like a backpack.",
        priceRange: "$$",
        url: "https://www.johnstonmurphy.com/xc4-leather-backpack",
        image: "/shop/johnston-murphy-xc4-backpack.jpg",
      },
      {
        slug: "away-carry-on",
        name: "The Carry-On",
        brand: "Away",
        reason: "It just works. Every time. That’s the whole job.",
        priceRange: "$$",
        url: "https://www.awaytravel.com/suitcases/carry-on",
        image: "/shop/away-carry-on.jpg",
      },
    ],
  },
  {
    slug: "daily-use",
    number: "03",
    name: "Daily Use",
    pov: "What stays out. What gets reached for.",
    products: [
      {
        slug: "prada-paradigme-eau-de-parfum",
        name: "Paradigme Eau de Parfum",
        brand: "Prada",
        reason: "Sits close. Doesn’t announce itself.",
        priceRange: "$$$",
        url: "https://www.sephora.com/brand/prada-beauty",
        image: "/shop/prada-paradigme-eau-de-parfum.jpg",
      },
      {
        slug: "aveda-pure-formance-grooming-system",
        name: "Pure-Formance Grooming Cream + Clay",
        brand: "Aveda",
        reason: "Hold without product crunch. Most others can’t say that.",
        priceRange: "$$",
        url: "https://www.aveda.com/products/8919/men",
        image: "/shop/aveda-pure-formance-grooming-system.jpg",
      },
    ],
  },
  {
    slug: "finishing-touches",
    number: "04",
    name: "Finishing Touches",
    pov: "Small things. They do most of the work.",
    products: [
      {
        slug: "ahlem-place-de-la-concorde",
        name: "Place de la Concorde",
        brand: "Ahlem",
        reason: "Hand-finished. People notice without knowing why.",
        priceRange: "$$$",
        url: "https://ahlemeyewear.com/products/place-de-la-concorde",
        image: "/shop/ahlem-place-de-la-concorde.jpg",
      },
      {
        slug: "mejuri-box-chain-necklace",
        name: "Box Chain Necklace",
        brand: "Mejuri",
        reason: "Disappears into the look. That’s what makes it work.",
        priceRange: "$$",
        url: "https://mejuri.com/shop/products/bold-box-chain-necklace",
        image: "/shop/mejuri-box-chain-necklace.jpg",
      },
    ],
  },
  {
    slug: "carry-and-keep",
    number: "05",
    name: "Carry & Keep",
    pov: "Bags that don’t need to perform. Just hold what they hold.",
    products: [
      {
        slug: "jcrew-medium-canvas-tote",
        name: "Medium Canvas Tote",
        brand: "J.Crew",
        reason: "You stop replacing it because you stop needing to.",
        priceRange: "$",
        url: "https://www.jcrew.com/c/mens_category/accessories/bags",
        image: "/shop/jcrew-medium-canvas-tote.jpg",
      },
      {
        slug: "baggu-standard-tote",
        name: "Standard Reusable Bag",
        brand: "Baggu",
        reason: "For days you don’t want to think about your bag.",
        priceRange: "$",
        url: "https://baggu.com/products/baggu-standard",
        image: "/shop/baggu-standard-tote.jpg",
      },
    ],
  },
];

export function getCategoryBySlug(slug: string): ShopCategory | undefined {
  return SHOP_CATEGORIES.find((c) => c.slug === slug);
}

export function getProductBySlug(
  slug: string
): { product: ShopProduct; category: ShopCategory } | undefined {
  for (const category of SHOP_CATEGORIES) {
    const product = category.products.find((p) => p.slug === slug);
    if (product) return { product, category };
  }
  return undefined;
}
