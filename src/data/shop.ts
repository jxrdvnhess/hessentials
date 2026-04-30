/**
 * Hessentials Shop — curated edit, not a marketplace.
 *
 * Single flat array of products. Categories are tags, not sections — the
 * filter row on the shop page narrows the grid without rearranging it.
 *
 * IMAGE SOURCING:
 * Images are hosted locally under /public/shop. Convention is one slug per
 * product, indexed sequentially:
 *   - /shop/<slug>-1.jpg   primary card image
 *   - /shop/<slug>-2.jpg   second view (gallery)
 *   - /shop/<slug>-3.jpg   …and so on
 * The first entry of `images` should match `image` (the primary used on the
 * grid + OG metadata). Single-image products may keep `image` only and skip
 * the `images` array — the renderer falls back gracefully.
 */

/**
 * Display price for a Shop product.
 *
 * Values are either a single retail price ("$95") or a tight range
 * when retail varies by size, length, or finish ("$1,400–$1,800").
 *
 * Tier markers ($ / $$ / $$$ / $$$$) were retired — the brand stance
 * is clarity, and tier markers were a soft hedge. Prices update with
 * the inventory; ranges should stay tight.
 */
export type PriceTier = string;

export type ShopCategory =
  | "Apparel"
  | "Footwear"
  | "Bags"
  | "Watches & Jewelry"
  | "Eyewear"
  | "Travel"
  | "Home"
  | "Grooming"
  | "Provisions";

/** Categories in display order — used by the filter row. */
export const SHOP_CATEGORIES: readonly ShopCategory[] = [
  "Apparel",
  "Footwear",
  "Bags",
  "Watches & Jewelry",
  "Eyewear",
  "Travel",
  "Home",
  "Grooming",
  "Provisions",
];

/**
 * How to read the live price off the source `url`. When unset, the
 * pricing layer leaves the static `priceRange` in place — that's the
 * default for every existing listing until the audit pass classifies
 * it. See `src/lib/pricing/fetchPrice.ts`.
 */
export type ExtractionMethod = "json-ld" | "shopify" | "html" | "manual";

export type ShopProduct = {
  slug: string;
  name: string;
  brand: string;
  category: ShopCategory;
  reason: string;
  /**
   * Manual / last-known-good price. Always rendered when no
   * `extractionMethod` is set, or as the fallback when a live fetch
   * fails. Curated by Jordan; live fetches override at runtime.
   */
  priceRange: PriceTier;
  /** External product page. Doubles as the source for live pricing. */
  url: string;
  /** Renderable image URL (typically `/shop/<slug>-1.jpg`). */
  image: string;
  /**
   * Optional gallery. When present, the detail page renders a carousel.
   * The first entry should match `image` (used on the grid + metadata).
   */
  images?: string[];
  /**
   * Optional live-pricing strategy. Omit (or set to "manual") to keep
   * the static `priceRange`. The audit pass fills these in per source
   * domain.
   */
  extractionMethod?: ExtractionMethod;
  /**
   * CSS selector pointing at the priced element. Required when
   * `extractionMethod === "html"`, ignored otherwise. Supports a small
   * subset of CSS — see `extractors/html.ts` for the grammar.
   */
  htmlPriceSelector?: string;
  /**
   * Plausibility floor. Variants below this dollar amount are dropped
   * before display — the typical case is a Shopify shop that lists
   * sample swatches or replacement parts as full variants. Set this
   * just below the lowest legitimate variant of the actual product.
   */
  priceFloor?: number;
};

export const SHOP_INTRO = "Bought. Used. Kept.";

/**
 * Curated, non-grouped order. Categories alternate intentionally — the grid
 * should read like a spread, not a sorted list.
 */
export const SHOP_PRODUCTS: ShopProduct[] = [
  {
    slug: "loewe-goya-thin-briefcase",
    name: "Goya Thin Briefcase",
    brand: "Loewe",
    category: "Bags",
    reason: "Soft calfskin. The bag for not announcing the day.",
    priceRange: "$4,200–$4,500",
    url: "https://www.loewe.com/usa/en/men/bags/portfolio-and-briefcases/goya-thin-briefcase-in-soft-grained-calfskin/337.12.P57-1100.html",
    image: "/shop/loewe-goya-thin-briefcase-1.jpg",
    images: [
      "/shop/loewe-goya-thin-briefcase-1.jpg",
      "/shop/loewe-goya-thin-briefcase-2.jpg",
      "/shop/loewe-goya-thin-briefcase-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 1000,
  },
  {
    slug: "omega-aqua-terra-small-seconds",
    name: "Seamaster Aqua Terra 150M Small Seconds",
    brand: "Omega",
    category: "Watches & Jewelry",
    reason: "The dress watch you can swim in.",
    priceRange: "$12,000",
    url: "https://www.omegawatches.com/en-us/watch-omega-seamaster-aqua-terra-150m-co-axial-master-chronometer-small-seconds-41-mm-22022412103001",
    image: "/shop/omega-aqua-terra-small-seconds-1.jpg",
    images: [
      "/shop/omega-aqua-terra-small-seconds-1.jpg",
      "/shop/omega-aqua-terra-small-seconds-2.jpg",
      "/shop/omega-aqua-terra-small-seconds-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 5000,
  },
  {
    slug: "bedsure-waffle-blanket",
    name: "Cotton Waffle Weave Blanket",
    brand: "Bedsure",
    category: "Home",
    reason: "Cotton, not synthetic. Cool in summer, warm enough otherwise.",
    priceRange: "$35–$55",
    url: "https://bedsurehome.com/products/cotton-waffle-weave-blanket?variant=40158662000742",
    image: "/shop/bedsure-waffle-blanket-1.jpg",
    images: [
      "/shop/bedsure-waffle-blanket-1.jpg",
      "/shop/bedsure-waffle-blanket-2.jpg",
      "/shop/bedsure-waffle-blanket-3.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 15,
  },
  {
    slug: "massimo-dutti-linen-double-collar-tee",
    name: "Linen-Cotton Double-Collar T-Shirt",
    brand: "Massimo Dutti",
    category: "Apparel",
    reason: "Wears like a shirt. Reads like a tee.",
    priceRange: "$69–$89",
    url: "https://www.massimodutti.com/us/linen-and-cotton-doublecollar-tshirt-l00659198?pelement=59486681",
    image: "/shop/massimo-dutti-linen-double-collar-tee-1.jpg",
    images: [
      "/shop/massimo-dutti-linen-double-collar-tee-1.jpg",
      "/shop/massimo-dutti-linen-double-collar-tee-2.jpg",
      "/shop/massimo-dutti-linen-double-collar-tee-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 25,
  },
  {
    slug: "lv-hippo-coffee-table",
    name: "Hippo Coffee Table",
    brand: "LV Furniture Collection",
    category: "Home",
    reason: "Substantial. Anchors the room without raising its voice.",
    priceRange: "$1,800–$2,400",
    url: "https://lvfurniturecollection.com/products/hippo-coffee-table?country=US&currency=USD&variant=45139005243523",
    image: "/shop/lv-hippo-coffee-table-1.jpg",
    images: [
      "/shop/lv-hippo-coffee-table-1.jpg",
      "/shop/lv-hippo-coffee-table-2.jpg",
      "/shop/lv-hippo-coffee-table-3.jpg",
      "/shop/lv-hippo-coffee-table-4.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 800,
  },
  {
    slug: "birkenstock-arizona-eva",
    name: "Arizona EVA",
    brand: "Birkenstock",
    category: "Footwear",
    reason: "For pools, beaches, kitchens. Anywhere you don’t want to think.",
    priceRange: "$45",
    url: "https://www.birkenstock.com/us/arizona-eva/arizona-eva-eva-0-eva-u_3716.html",
    image: "/shop/birkenstock-arizona-eva-1.jpg",
    images: [
      "/shop/birkenstock-arizona-eva-1.jpg",
      "/shop/birkenstock-arizona-eva-2.jpg",
      "/shop/birkenstock-arizona-eva-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 20,
  },
  {
    slug: "ahlem-louxor",
    name: "Louxor",
    brand: "Ahlem",
    category: "Eyewear",
    reason: "Hand-finished in France. People notice without knowing why.",
    priceRange: "$480–$540",
    url: "https://www.ahlemeyewear.com/products/louxor-1?variant=44903388545273",
    image: "/shop/ahlem-louxor-1.jpg",
    images: [
      "/shop/ahlem-louxor-1.jpg",
      "/shop/ahlem-louxor-2.jpg",
      "/shop/ahlem-louxor-3.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 200,
  },
  {
    slug: "prada-linen-duffel",
    name: "Linen-Blend Drawstring Duffel",
    brand: "Prada",
    category: "Bags",
    reason: "Looks unstructured. Holds more than it should.",
    priceRange: "$2,800–$3,400",
    url: "https://www.prada.com/us/en/p/linen-blend-drawstring-duffel-bag/2VY011_2CX9_F0018_V_OOO",
    image: "/shop/prada-linen-duffel-1.jpg",
    images: [
      "/shop/prada-linen-duffel-1.jpg",
      "/shop/prada-linen-duffel-2.jpg",
      "/shop/prada-linen-duffel-3.jpg",
      "/shop/prada-linen-duffel-4.jpg",
      "/shop/prada-linen-duffel-5.jpg",
      "/shop/prada-linen-duffel-6.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 800,
  },
  {
    slug: "crazy-water-sampler",
    name: "Mineral Water Sampler",
    brand: "Crazy Water",
    category: "Provisions",
    reason: "Texas mineral water from Mineral Wells. Four numbered strengths.",
    priceRange: "$30–$45",
    url: "https://drinkcrazywater.myshopify.com/collections/water/products/crazy-water-sampler",
    image: "/shop/crazy-water-sampler.jpg",
    extractionMethod: "shopify",
    priceFloor: 15,
  },
  {
    slug: "tag-heuer-aquaracer-quartz",
    name: "Aquaracer Professional 200 Quartz 40mm",
    brand: "Tag Heuer",
    category: "Watches & Jewelry",
    reason: "A real watch, finished correctly, without the chronograph tax.",
    priceRange: "$2,000–$2,400",
    url: "https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-aquaracer/40-mm-quartz/CBP1112.BA0627.html",
    image: "/shop/tag-heuer-aquaracer-quartz-1.jpg",
    images: [
      "/shop/tag-heuer-aquaracer-quartz-1.jpg",
      "/shop/tag-heuer-aquaracer-quartz-2.jpg",
      "/shop/tag-heuer-aquaracer-quartz-3.jpg",
      "/shop/tag-heuer-aquaracer-quartz-4.jpg",
      "/shop/tag-heuer-aquaracer-quartz-5.jpg",
      "/shop/tag-heuer-aquaracer-quartz-6.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 800,
  },
  {
    slug: "aveda-pureformance-clay",
    name: "Pure-Formance Grooming Clay",
    brand: "Aveda",
    category: "Grooming",
    reason: "Hold without product crunch. Most others can’t say that.",
    priceRange: "$30",
    url: "https://www.aveda.com/product/17776/16733/styling/mens-styling/aveda-men-pure-formance-grooming-clay?size=2.5_fl_oz%2F75_ml",
    image: "/shop/aveda-pureformance-clay-1.jpg",
    images: [
      "/shop/aveda-pureformance-clay-1.jpg",
      "/shop/aveda-pureformance-clay-2.jpg",
      "/shop/aveda-pureformance-clay-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 12,
  },
  {
    slug: "massimo-dutti-tapered-jeans",
    name: "Tapered Fit Jeans",
    brand: "Massimo Dutti",
    category: "Apparel",
    reason: "Tapered without being skinny. The cut that actually lasts.",
    priceRange: "$89–$109",
    url: "https://www.massimodutti.com/us/tapered-fit-jeans-l00451110?pelement=57966404",
    image: "/shop/massimo-dutti-tapered-jeans-1.jpg",
    images: [
      "/shop/massimo-dutti-tapered-jeans-1.jpg",
      "/shop/massimo-dutti-tapered-jeans-2.jpg",
      "/shop/massimo-dutti-tapered-jeans-3.jpg",
      "/shop/massimo-dutti-tapered-jeans-4.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 30,
  },
  {
    slug: "tiffany-venetian-link-bracelet",
    name: "Venetian Link Bracelet",
    brand: "Tiffany & Co.",
    category: "Watches & Jewelry",
    reason: "Sterling silver. The kind people inherit.",
    priceRange: "$375–$575",
    url: "https://www.tiffany.com/jewelry/bracelets/sterling-silver-bracelets-117817401.html",
    image: "/shop/tiffany-venetian-link-bracelet-1.jpg",
    images: [
      "/shop/tiffany-venetian-link-bracelet-1.jpg",
      "/shop/tiffany-venetian-link-bracelet-2.jpg",
      "/shop/tiffany-venetian-link-bracelet-3.jpg",
      "/shop/tiffany-venetian-link-bracelet-4.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 150,
  },
  {
    slug: "prada-renylon-belt-bag",
    name: "Re-Nylon and Saffiano Leather Belt Bag",
    brand: "Prada",
    category: "Bags",
    reason: "When you want to carry less but still want it close.",
    priceRange: "$1,650–$1,950",
    url: "https://www.prada.com/us/en/p/re-nylon-and-saffiano-leather-belt-bag/2VL977_2DMG_F0002_V_WOO",
    image: "/shop/prada-renylon-belt-bag-1.jpg",
    images: [
      "/shop/prada-renylon-belt-bag-1.jpg",
      "/shop/prada-renylon-belt-bag-2.jpg",
      "/shop/prada-renylon-belt-bag-3.jpg",
      "/shop/prada-renylon-belt-bag-4.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 600,
  },
  {
    slug: "pacific-coast-down-pillow",
    name: "Down Sleeping Pillow",
    brand: "Pacific Coast",
    category: "Home",
    reason: "Holds shape through the night. Most pillows don’t.",
    priceRange: "$80–$110",
    url: "https://www.amazon.com/Pacific-Coast-Standard-Sleeping-Downproof/dp/B0DPV65G7Y?th=1",
    image: "/shop/pacific-coast-down-pillow-1.jpg",
    images: [
      "/shop/pacific-coast-down-pillow-1.jpg",
      "/shop/pacific-coast-down-pillow-2.jpg",
    ],
    // Amazon aggressively blocks server-side fetches. Stays on manual
    // priceRange — keep this updated by hand or move to a non-Amazon
    // source if one exists.
  },
  {
    slug: "massimo-dutti-cotton-slim-pants",
    name: "Cotton Blend Slim Fit Pants",
    brand: "Massimo Dutti",
    category: "Apparel",
    reason: "Reads more expensive than it is. Wears like it, too.",
    priceRange: "$79–$99",
    url: "https://www.massimodutti.com/us/cotton-blend-slim-fit-pants-l00101001?pelement=58445844",
    image: "/shop/massimo-dutti-cotton-slim-pants-1.jpg",
    images: [
      "/shop/massimo-dutti-cotton-slim-pants-1.jpg",
      "/shop/massimo-dutti-cotton-slim-pants-2.jpg",
      "/shop/massimo-dutti-cotton-slim-pants-3.jpg",
      "/shop/massimo-dutti-cotton-slim-pants-4.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 25,
  },
  {
    slug: "birkenstock-arizona-leather",
    name: "Arizona Soft Footbed (Oiled Leather)",
    brand: "Birkenstock",
    category: "Footwear",
    reason: "You stop noticing them after five minutes. That’s the point.",
    priceRange: "$135–$155",
    url: "https://www.birkenstock.com/us/arizona-soft-footbed-natural-leather-oiled/arizona-core-oiledleather-softfootbed-eva-u_5326.html",
    image: "/shop/birkenstock-arizona-leather-1.jpg",
    images: [
      "/shop/birkenstock-arizona-leather-1.jpg",
      "/shop/birkenstock-arizona-leather-2.jpg",
      "/shop/birkenstock-arizona-leather-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 50,
  },
  {
    slug: "johnston-murphy-rhodes-backpack",
    name: "Rhodes Leather Backpack",
    brand: "Johnston & Murphy",
    category: "Bags",
    reason: "Looks like a briefcase. Carries like a backpack.",
    priceRange: "$245–$295",
    url: "https://www.johnstonmurphy.com/p/leather-goods-backpacks-briefcases/rhodes-backpack/14510.html?dwvar_14510_color=Tan%20Full%20Grain",
    image: "/shop/johnston-murphy-rhodes-backpack-1.jpg",
    images: [
      "/shop/johnston-murphy-rhodes-backpack-1.jpg",
      "/shop/johnston-murphy-rhodes-backpack-2.jpg",
      "/shop/johnston-murphy-rhodes-backpack-3.jpg",
      "/shop/johnston-murphy-rhodes-backpack-4.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 100,
  },
  {
    slug: "aveda-pureformance-cream",
    name: "Pure-Formance Grooming Cream",
    brand: "Aveda",
    category: "Grooming",
    reason: "Softer hold. Same trick — finish doesn’t read as done.",
    priceRange: "$30",
    url: "https://www.aveda.com/product/17776/16732/styling/mens-styling/aveda-men-pure-formance-grooming-cream?size=4.2_fl_oz%2F125_ml",
    image: "/shop/aveda-pureformance-cream-1.jpg",
    images: [
      "/shop/aveda-pureformance-cream-1.jpg",
      "/shop/aveda-pureformance-cream-2.jpg",
      "/shop/aveda-pureformance-cream-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 12,
  },
  {
    slug: "ahlem-haussmann",
    name: "Haussmann",
    brand: "Ahlem",
    category: "Eyewear",
    reason: "The frame that suits more faces than it should.",
    priceRange: "$480–$540",
    url: "https://www.ahlemeyewear.com/products/haussman?variant=44220169715961",
    image: "/shop/ahlem-haussmann-1.jpg",
    images: [
      "/shop/ahlem-haussmann-1.jpg",
      "/shop/ahlem-haussmann-2.jpg",
      "/shop/ahlem-haussmann-3.jpg",
      "/shop/ahlem-haussmann-4.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 200,
  },
  {
    slug: "away-the-large",
    name: "The Large",
    brand: "Away",
    category: "Travel",
    reason: "Checked. Heavy-duty. Doesn’t pretend to be cute.",
    priceRange: "$375–$425",
    url: "https://www.awaytravel.com/products/large-navy-blue",
    image: "/shop/away-the-large-1.jpg",
    images: [
      "/shop/away-the-large-1.jpg",
      "/shop/away-the-large-2.jpg",
      "/shop/away-the-large-3.jpg",
      "/shop/away-the-large-4.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 150,
  },
  {
    slug: "massimo-dutti-cotton-tee",
    name: "100% Cotton Short-Sleeve T-Shirt",
    brand: "Massimo Dutti",
    category: "Apparel",
    reason: "Heavyweight cotton. The base layer for everything.",
    priceRange: "$39",
    url: "https://www.massimodutti.com/us/100-cotton-short-sleeve-tshirt-l01418212?pelement=56718135",
    image: "/shop/massimo-dutti-cotton-tee-1.jpg",
    images: [
      "/shop/massimo-dutti-cotton-tee-1.jpg",
      "/shop/massimo-dutti-cotton-tee-2.jpg",
      "/shop/massimo-dutti-cotton-tee-3.jpg",
      "/shop/massimo-dutti-cotton-tee-4.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 15,
  },
  {
    slug: "goodfellow-flat-front-shorts",
    name: "5\" Flat Front Shorts",
    brand: "Goodfellow & Co.",
    category: "Apparel",
    reason: "Cheap in price. Not in how they wear.",
    priceRange: "$20–$28",
    url: "https://www.target.com/p/men-s-5-flat-front-shorts-goodfellow-co/-/A-94965145?preselect=94886502",
    image: "/shop/goodfellow-flat-front-shorts-1.jpg",
    images: [
      "/shop/goodfellow-flat-front-shorts-1.jpg",
      "/shop/goodfellow-flat-front-shorts-2.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 10,
  },
  {
    slug: "prada-renylon-backpack",
    name: "Re-Nylon and Saffiano Leather Backpack",
    brand: "Prada",
    category: "Bags",
    reason: "Prada nylon is a uniform. This is the carry version.",
    priceRange: "$2,400–$2,800",
    url: "https://www.prada.com/us/en/p/re-nylon-and-saffiano-leather-backpack/2VZ048_2DMG_F0002_V_OOO",
    image: "/shop/prada-renylon-backpack-1.jpg",
    images: [
      "/shop/prada-renylon-backpack-1.jpg",
      "/shop/prada-renylon-backpack-2.jpg",
      "/shop/prada-renylon-backpack-3.jpg",
      "/shop/prada-renylon-backpack-4.jpg",
      "/shop/prada-renylon-backpack-5.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 800,
  },
  {
    slug: "uniqlo-oxford-oversized-shirt",
    name: "Oxford Oversized Shirt (Striped)",
    brand: "Uniqlo",
    category: "Apparel",
    reason: "Oversized without losing structure. Layers over everything.",
    priceRange: "$40",
    url: "https://www.uniqlo.com/us/en/products/E484905-000/00?colorDisplayCode=01&sizeDisplayCode=003",
    image: "/shop/uniqlo-oxford-oversized-shirt-1.jpg",
    images: [
      "/shop/uniqlo-oxford-oversized-shirt-1.jpg",
      "/shop/uniqlo-oxford-oversized-shirt-2.jpg",
      "/shop/uniqlo-oxford-oversized-shirt-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 15,
  },
  {
    slug: "abercrombie-premium-ribbed-tank",
    name: "Premium Ribbed Tank",
    brand: "Abercrombie",
    category: "Apparel",
    reason: "Holds shape under everything. Worth it for that alone.",
    priceRange: "$25–$32",
    url: "https://www.abercrombie.com/shop/us/p/premium-ribbed-tank-61149838?categoryId=73458",
    image: "/shop/abercrombie-premium-ribbed-tank-1.jpg",
    images: [
      "/shop/abercrombie-premium-ribbed-tank-1.jpg",
      "/shop/abercrombie-premium-ribbed-tank-2.jpg",
      "/shop/abercrombie-premium-ribbed-tank-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 10,
  },
  {
    slug: "prada-renylon-duffle",
    name: "Re-Nylon and Saffiano Leather Duffle",
    brand: "Prada",
    category: "Bags",
    reason: "Built to take a beating. Doesn’t read like it has.",
    priceRange: "$2,100–$2,500",
    url: "https://www.prada.com/us/en/p/re-nylon-and-saffiano-leather-duffle-bag/2VC013_2DMH_F0002_V_XOO",
    image: "/shop/prada-renylon-duffle-1.jpg",
    images: [
      "/shop/prada-renylon-duffle-1.jpg",
      "/shop/prada-renylon-duffle-2.jpg",
      "/shop/prada-renylon-duffle-3.jpg",
      "/shop/prada-renylon-duffle-4.jpg",
      "/shop/prada-renylon-duffle-5.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 800,
  },
  {
    slug: "away-bigger-carry-on",
    name: "The Bigger Carry-On",
    brand: "Away",
    category: "Travel",
    reason: "Hits the size limit on purpose. Holds a week.",
    priceRange: "$295–$345",
    url: "https://www.awaytravel.com/products/bigger-carry-on-navy-blue",
    image: "/shop/away-bigger-carry-on-1.jpg",
    images: [
      "/shop/away-bigger-carry-on-1.jpg",
      "/shop/away-bigger-carry-on-2.jpg",
      "/shop/away-bigger-carry-on-3.jpg",
      "/shop/away-bigger-carry-on-4.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 100,
  },
  {
    slug: "clayton-crume-canvas-tote",
    name: "Canvas Market Tote",
    brand: "Clayton & Crume",
    category: "Bags",
    reason: "Heavy canvas, leather handles. Outlasts replacing.",
    priceRange: "$145–$195",
    url: "https://claytonandcrume.com/products/canvas-market-tote?country=US&currency=USD&variant=47093690171559",
    image: "/shop/clayton-crume-canvas-tote-1.jpg",
    images: [
      "/shop/clayton-crume-canvas-tote-1.jpg",
      "/shop/clayton-crume-canvas-tote-2.jpg",
      "/shop/clayton-crume-canvas-tote-3.jpg",
      "/shop/clayton-crume-canvas-tote-4.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 50,
  },
  {
    slug: "abercrombie-seersucker-swim-trunk",
    name: "Pull-On Seersucker Swim Trunk",
    brand: "Abercrombie",
    category: "Apparel",
    reason: "Seersucker, not slick nylon. The pool trunk that reads thought-out.",
    priceRange: "$55–$75",
    url: "https://www.abercrombie.com/shop/us/p/pull-on-seersucker-swim-trunk-58989323",
    image: "/shop/Abercrombie-Seersucker-Swim-Trunk-1.jpg",
    images: [
      "/shop/Abercrombie-Seersucker-Swim-Trunk-1.jpg",
      "/shop/Abercrombie-Seersucker-Swim-Trunk-2.jpg",
      "/shop/Abercrombie-Seersucker-Swim-Trunk-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 20,
  },
  {
    slug: "clayton-daybook",
    name: "Daybook",
    brand: "Clayton & Crume",
    category: "Home",
    reason: "Full-grain leather, brass snap, refillable. The notebook you keep.",
    priceRange: "$245–$295",
    url: "https://claytonandcrume.com/products/daybook",
    image: "/shop/clayton-daybook-1.jpg",
    images: [
      "/shop/clayton-daybook-1.jpg",
      "/shop/clayton-daybook-2.jpg",
      "/shop/clayton-daybook-3.jpg",
      "/shop/clayton-daybook-4.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 80,
  },
  {
    slug: "ibex-wool-dryer-puffs",
    name: "Wool Dryer Puffs",
    brand: "Ibex",
    category: "Home",
    reason:
      "Merino wool, US-made. Replaces dryer sheets and never runs out.",
    priceRange: "$25–$35",
    url: "https://ibex.com/products/wool-dryer-puffs",
    image: "/shop/ibex-dryer-puffs-1.jpg",
    images: [
      "/shop/ibex-dryer-puffs-1.jpg",
      "/shop/ibex-dryer-puffs-2.jpg",
      "/shop/ibex-dryer-puffs-3.jpg",
      "/shop/ibex-dryer-puffs-4.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 10,
  },
  {
    slug: "ysl-l-homme-edt",
    name: "L’Homme Eau de Toilette",
    brand: "YSL",
    category: "Grooming",
    reason: "Bergamot and cedar. The dependable cologne that wears close.",
    priceRange: "$95–$160",
    url: "https://www.yslbeautyus.com/fragrance/mens-fragrances/lhomme/lhomme-eau-de-toilette-spray/284YSL.html",
    image: "/shop/ysl-l-homme-1.jpg",
    extractionMethod: "json-ld",
    priceFloor: 35,
  },
  {
    slug: "ysl-myslf-edp",
    name: "MYSLF Eau de Parfum",
    brand: "YSL",
    category: "Grooming",
    reason:
      "Orange blossom, vetiver. The brighter one — for when L’Homme is too quiet.",
    priceRange: "$115–$185",
    url: "https://www.yslbeautyus.com/fragrance/mens-fragrances/myslf/myslf-eau-de-parfum/WW-51115YSL.html",
    image: "/shop/ysl-MYSLF-1.jpg",
    images: ["/shop/ysl-MYSLF-1.jpg", "/shop/ysl-MYSLF-2.jpg"],
    extractionMethod: "json-ld",
    priceFloor: 40,
  },
  {
    slug: "prada-paradigme-edp",
    name: "Paradigme Eau de Parfum",
    brand: "Prada",
    category: "Grooming",
    reason: "Mate and ambergris. Reads as the wearer, not the brand.",
    priceRange: "$250–$300",
    url: "https://www.prada.com/us/en/p/paradigme-edp-100-ml/2A1451_2H0Q_F0Z99_P_ML100",
    image: "/shop/prada-Paradigme-1.jpg",
    images: [
      "/shop/prada-Paradigme-1.jpg",
      "/shop/prada-Paradigme-2.jpg",
      "/shop/prada-Paradigme-3.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 100,
  },
  {
    slug: "kiehls-avocado-eye-cream",
    name: "Creamy Eye Treatment with Avocado",
    brand: "Kiehl’s",
    category: "Grooming",
    reason: "Avocado oil, no fuss. Forty years on the counter for a reason.",
    priceRange: "$45",
    url: "https://www.kiehls.com/skincare/eye-creams-and-serums/avocado-eye-cream/258.html",
    image: "/shop/kiehls-avocado-eye-cream-1.jpg",
    images: [
      "/shop/kiehls-avocado-eye-cream-1.jpg",
      "/shop/kiehls-avocado-eye-cream-2.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 18,
  },
  {
    slug: "louis-vuitton-dopp-kit",
    name: "Dopp Kit (Damier Graphite)",
    brand: "Louis Vuitton",
    category: "Bags",
    reason:
      "Damier Graphite canvas. Travels with the bag, not buried inside it.",
    priceRange: "$720–$820",
    url: "https://us.louisvuitton.com/eng-us/products/dopp-kit-toilet-pouch-damier-graphite-canvas-nvprod1420096v/N40127",
    image: "/shop/louis-vuitton-dopp-kit-1.jpg",
    images: [
      "/shop/louis-vuitton-dopp-kit-1.jpg",
      "/shop/louis-vuitton-dopp-kit-2.jpg",
      "/shop/louis-vuitton-dopp-kit-3.jpg",
      "/shop/louis-vuitton-dopp-kit-4.jpg",
    ],
    // Louis Vuitton aggressively blocks server-side fetches; this may
    // fail and fall back to the static priceRange. Admin page will
    // surface the error if so.
    extractionMethod: "json-ld",
    priceFloor: 250,
  },
  {
    slug: "prada-symbole-sunglasses",
    name: "Symbole Sunglasses",
    brand: "Prada",
    category: "Eyewear",
    reason: "Triangle, not logo. Prada that doesn’t need to introduce itself.",
    priceRange: "$475–$590",
    url: "https://www.prada.com/us/en/p/prada-symbole-sunglasses/SPRB17_E16K_FE08Z_C_054",
    image: "/shop/Prada-Symbole-sunglasses-1.jpg",
    images: [
      "/shop/Prada-Symbole-sunglasses-1.jpg",
      "/shop/Prada-Symbole-sunglasses-2.jpg",
      "/shop/Prada-Symbole-sunglasses-3.jpg",
      "/shop/Prada-Symbole-sunglasses-4.jpg",
    ],
    extractionMethod: "json-ld",
    priceFloor: 200,
  },
  {
    slug: "dr-bronner-tea-tree-bar-soap",
    name: "Tea Tree Pure-Castile Bar Soap",
    brand: "Dr. Bronner’s",
    category: "Grooming",
    reason: "Tea tree, real oils, no fillers. Soap the way it used to be.",
    priceRange: "$7",
    url: "https://www.drbronner.com/products/tea-tree-pure-castile-bar-soap",
    image: "/shop/dr-bronners-pure-castile-tea-tree-1.jpg",
    images: [
      "/shop/dr-bronners-pure-castile-tea-tree-1.jpg",
      "/shop/dr-bronners-pure-castile-tea-tree-2.jpg",
      "/shop/dr-bronners-pure-castile-tea-tree-3.jpg",
    ],
    extractionMethod: "shopify",
    priceFloor: 3,
  },
];

export function getProductBySlug(slug: string): ShopProduct | undefined {
  return SHOP_PRODUCTS.find((p) => p.slug === slug);
}

export function getProductsByCategory(category: ShopCategory): ShopProduct[] {
  return SHOP_PRODUCTS.filter((p) => p.category === category);
}
