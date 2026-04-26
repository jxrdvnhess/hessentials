/**
 * Hessentials Shop — curated edit, not a marketplace.
 *
 * Single flat array of products. Categories are tags, not sections — the
 * filter row on the shop page narrows the grid without rearranging it.
 *
 * IMAGE SOURCING (current state):
 * Each `image` field holds the brand CDN URL directly. next.config.ts allows
 * those hostnames via `remotePatterns`. The shop renders without any local
 * asset step. Trade-off: brand CDN URLs occasionally rot — when one breaks,
 * its card falls back to the brand-name placeholder until the URL is updated.
 *
 * To localize later (recommended once the catalog stabilizes):
 *   1. Run `bash scripts/download-shop-images.sh` to populate /public/shop/.
 *   2. Replace each `image` value with `/shop/<slug>.jpg`.
 *   3. Optional: trim `remotePatterns` from next.config.ts.
 */

export type PriceTier = "$" | "$$" | "$$$" | "$$$$";

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

export type ShopProduct = {
  slug: string;
  name: string;
  brand: string;
  category: ShopCategory;
  reason: string;
  priceRange: PriceTier;
  /** External product page. */
  url: string;
  /** Renderable image URL — CDN today, /shop/<slug>.jpg once localized. */
  image: string;
};

export const SHOP_INTRO = "Things worth keeping.";

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
    priceRange: "$$$$",
    url: "https://www.loewe.com/usa/en/men/bags/portfolio-and-briefcases/goya-thin-briefcase-in-soft-grained-calfskin/337.12.P57-1100.html",
    image:
      "https://www.loewe.com/dw/image/v2/BBPC_PRD/on/demandware.static/-/Sites-Loewe_master/default/dwca31ef16/images_rd/337.12.P57/337.12.P57-1100/337.12.P57_1100_1F.jpg?sw=850&q=100",
  },
  {
    slug: "quince-linen-pants",
    name: "100% Linen Pants",
    brand: "Quince",
    category: "Apparel",
    reason: "Linen that doesn’t punish you for sitting down in it.",
    priceRange: "$",
    url: "https://www.quince.com/men/men-s-100-linen-pants?color=flax",
    image:
      "https://images.quince.com/7eAGPP7q4CFhsOk9DqpQli/05c1649b0521c6e2d686e4e1c71723b9/M-PNT-16-FLAX-33489_EDITED.jpg?w=1200&q=80&fm=jpg",
  },
  {
    slug: "omega-aqua-terra-small-seconds",
    name: "Seamaster Aqua Terra 150M Small Seconds",
    brand: "Omega",
    category: "Watches & Jewelry",
    reason: "The dress watch you can swim in.",
    priceRange: "$$$$",
    url: "https://www.omegawatches.com/en-us/watch-omega-seamaster-aqua-terra-150m-co-axial-master-chronometer-small-seconds-41-mm-22022412103001",
    image:
      "https://www.omegawatches.com/media/catalog/product/o/m/omega-seamaster-aqua-terra-150m-co-axial-master-chronometer-small-seconds-41-mm-22022412103001-bdacfe.png?w=450",
  },
  {
    slug: "bedsure-waffle-blanket",
    name: "Cotton Waffle Weave Blanket",
    brand: "Bedsure",
    category: "Home",
    reason: "Cotton, not synthetic. Cool in summer, warm enough otherwise.",
    priceRange: "$",
    url: "https://bedsurehome.com/products/cotton-waffle-weave-blanket?variant=40158662000742",
    image: "https://m.media-amazon.com/images/I/91UYXcDdHnL._AC_SL1500_.jpg",
  },
  {
    slug: "prada-court-leather-sneakers",
    name: "Court Leather Sneakers",
    brand: "Prada",
    category: "Footwear",
    reason: "The sneaker you keep wearing once you stop trying to look young.",
    priceRange: "$$$$",
    url: "https://www.prada.com/us/en/p/court-leather-sneakers/2EE483_070_F0009_F_G000",
    image:
      "https://www.prada.com/content/dam/pradabkg_products/2/2EE/2EE483/070F0009/2EE483_070_F0009_F_G000_SLR.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg",
  },
  {
    slug: "massimo-dutti-linen-double-collar-tee",
    name: "Linen-Cotton Double-Collar T-Shirt",
    brand: "Massimo Dutti",
    category: "Apparel",
    reason: "The tee that knows it’s not just a tee.",
    priceRange: "$$",
    url: "https://www.massimodutti.com/us/linen-and-cotton-doublecollar-tshirt-l00659198?pelement=59486681",
    image:
      "https://static.massimodutti.net/assets/public/dcac/dcf9/610443679566/3bdbbec2edff/00659198700-o6/00659198700-o6.jpg?ts=1777020874502&w=1600&f=auto",
  },
  {
    slug: "lv-hippo-coffee-table",
    name: "Hippo Coffee Table",
    brand: "LV Furniture Collection",
    category: "Home",
    reason: "Substantial. Anchors the room without raising its voice.",
    priceRange: "$$$$",
    url: "https://lvfurniturecollection.com/products/hippo-coffee-table?country=US&currency=USD&variant=45139005243523",
    image:
      "https://lvfurniturecollection.com/cdn/shop/files/hippo-coffee-table_6f30515d-913e-4667-9ad5-f86d1c03fe6b.png?v=1770254572&width=1946",
  },
  {
    slug: "birkenstock-arizona-eva",
    name: "Arizona EVA",
    brand: "Birkenstock",
    category: "Footwear",
    reason: "For pools, beaches, kitchens. Anywhere you don’t want to think.",
    priceRange: "$",
    url: "https://www.birkenstock.com/us/arizona-eva/arizona-eva-eva-0-eva-u_3716.html",
    image:
      "https://www.birkenstock.com/dw/image/v2/BLZD_PRD/on/demandware.static/-/Sites-master-catalog-amer/default/dw6172c109/129421/129421.jpg?sw=1148&sh=1148&sm=fit&q=80",
  },
  {
    slug: "ahlem-louxor",
    name: "Louxor",
    brand: "Ahlem",
    category: "Eyewear",
    reason: "Hand-finished in France. People notice without knowing why.",
    priceRange: "$$$",
    url: "https://www.ahlemeyewear.com/products/louxor-1?variant=44903388545273",
    image:
      "https://www.ahlemeyewear.com/cdn/shop/files/Louxor_SUN_WEB_greyGold_01_WEB_grey_1500x1002_crop_center.jpg?v=1714675082",
  },
  {
    slug: "quince-mesh-sweater-polo",
    name: "Mesh Stitch Cotton Sweater Polo",
    brand: "Quince",
    category: "Apparel",
    reason: "The polo that doesn’t look like a polo.",
    priceRange: "$",
    url: "https://www.quince.com/men/mens-mesh-stitch-organic-cotton-short-sleeve-sweater-polo?color=speckled-beige&gender=men",
    image:
      "https://images.quince.com/6RzIOSVBe0PjasL3JJi9AI/cd7704af61a8d52f303161d209d947d4/M-LKT-93-SPKBG-03_EDITED.jpg?w=1200&q=80&fm=jpg",
  },
  {
    slug: "prada-linen-duffel",
    name: "Linen-Blend Drawstring Duffel",
    brand: "Prada",
    category: "Bags",
    reason: "Looks unstructured. Holds more than it should.",
    priceRange: "$$$$",
    url: "https://www.prada.com/us/en/p/linen-blend-drawstring-duffel-bag/2VY011_2CX9_F0018_V_OOO",
    image:
      "https://www.prada.com/content/dam/pradabkg_products/2/2VY/2VY011/2CX9F0018/2VY011_2CX9_F0018_V_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg",
  },
  {
    slug: "crazy-water-sampler",
    name: "Mineral Water Sampler",
    brand: "Crazy Water",
    category: "Provisions",
    reason: "Texas mineral water from Mineral Wells. Four numbered strengths.",
    priceRange: "$",
    url: "https://drinkcrazywater.myshopify.com/collections/water/products/crazy-water-sampler",
    image:
      "https://drinkcrazywater.myshopify.com/cdn/shop/products/sampler_large.png?v=1509477709",
  },
  {
    slug: "tag-heuer-aquaracer-quartz",
    name: "Aquaracer Professional 200 Quartz 40mm",
    brand: "Tag Heuer",
    category: "Watches & Jewelry",
    reason: "A real watch, finished correctly, without the chronograph tax.",
    priceRange: "$$$$",
    url: "https://www.tagheuer.com/us/en/timepieces/collections/tag-heuer-aquaracer/40-mm-quartz/CBP1112.BA0627.html",
    image:
      "https://www.tagheuer.com/on/demandware.static/-/Sites-tagheuer-master/default/dwced42cf4/TAG_Heuer_Aquaracer/CBP1112.BA0627/CBP1112.BA0627_Soldier.png?impolicy=TrimRatioResize&width=1254&ratioHeight=5&ratioWidth=4&expansion=true",
  },
  {
    slug: "aveda-pureformance-clay",
    name: "Pure-Formance Grooming Clay",
    brand: "Aveda",
    category: "Grooming",
    reason: "Hold without product crunch. Most others can’t say that.",
    priceRange: "$$",
    url: "https://www.aveda.com/product/17776/16733/styling/mens-styling/aveda-men-pure-formance-grooming-clay?size=2.5_fl_oz%2F75_ml",
    image:
      "https://www.aveda.com/media/images/products/355x600/white/av_sku_A3TX01_34069_355x600_0.jpg",
  },
  {
    slug: "massimo-dutti-tapered-jeans",
    name: "Tapered Fit Jeans",
    brand: "Massimo Dutti",
    category: "Apparel",
    reason: "Tapered without being skinny. The cut that actually lasts.",
    priceRange: "$$",
    url: "https://www.massimodutti.com/us/tapered-fit-jeans-l00451110?pelement=57966404",
    image:
      "https://static.massimodutti.net/assets/public/21d8/ffc7/26214fef9b7f/09b197e25617/00451110806-o8/00451110806-o8.jpg?ts=1770972782296&w=1600&f=auto",
  },
  {
    slug: "tiffany-venetian-link-bracelet",
    name: "Venetian Link Bracelet",
    brand: "Tiffany & Co.",
    category: "Watches & Jewelry",
    reason: "Sterling silver. The kind people inherit.",
    priceRange: "$$$",
    url: "https://www.tiffany.com/jewelry/bracelets/sterling-silver-bracelets-117817401.html",
    image:
      "https://media.tiffany.com/is/image/tco/60150727_BLT_ALT3X1?hei=1230&wid=1230&fmt=jpg",
  },
  {
    slug: "quince-silk-sleep-mask",
    name: "Mulberry Silk Sleep Mask",
    brand: "Quince",
    category: "Travel",
    reason: "Real silk. Twelve dollars. The math is fine.",
    priceRange: "$",
    url: "https://www.quince.com/home/sleep-mask?color=navy",
    image:
      "https://images.quince.com/5IpMYbOpVBkz3wH1MZMWJ9/25563122b08b520366aeb5d6f1f3db90/eye_mask_1_navy.jpg?w=1200&q=80&fm=jpg",
  },
  {
    slug: "prada-renylon-belt-bag",
    name: "Re-Nylon and Saffiano Leather Belt Bag",
    brand: "Prada",
    category: "Bags",
    reason: "When you want to carry less but still want it close.",
    priceRange: "$$$$",
    url: "https://www.prada.com/us/en/p/re-nylon-and-saffiano-leather-belt-bag/2VL977_2DMG_F0002_V_WOO",
    image:
      "https://www.prada.com/content/dam/pradanux_products/2/2VL/2VL977/2DMGF0002/2VL977_2DMG_F0002_V_WOO_SLF.png/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg",
  },
  {
    slug: "pacific-coast-down-pillow",
    name: "Down Sleeping Pillow",
    brand: "Pacific Coast",
    category: "Home",
    reason: "Holds shape through the night. Most pillows don’t.",
    priceRange: "$$",
    url: "https://www.amazon.com/Pacific-Coast-Standard-Sleeping-Downproof/dp/B0DPV65G7Y?th=1",
    image:
      "https://encrypted-tbn3.gstatic.com/shopping?q=tbn:ANd9GcR0x7j0UnChScpFZasLpeJ_lNMm26PoSOladxNb7CMzTfPRvGlhXqLcX8ElmiJPGT33RMY_n8av0qcahg6r1Bpic8E3jS-ilcFXGXUmwSzcR7XW8R5JSOpU_w",
  },
  {
    slug: "massimo-dutti-cotton-slim-pants",
    name: "Cotton Blend Slim Fit Pants",
    brand: "Massimo Dutti",
    category: "Apparel",
    reason: "Reads more expensive than it is. Wears like it, too.",
    priceRange: "$$",
    url: "https://www.massimodutti.com/us/cotton-blend-slim-fit-pants-l00101001?pelement=58445844",
    image:
      "https://static.massimodutti.net/assets/public/0b67/83b3/c1f84fd3b74f/e1f1c5ab126a/00101001401-o6/00101001401-o6.jpg?ts=1773142882443&w=1600&f=auto",
  },
  {
    slug: "birkenstock-arizona-leather",
    name: "Arizona Soft Footbed (Oiled Leather)",
    brand: "Birkenstock",
    category: "Footwear",
    reason: "You stop noticing them after five minutes. That’s the point.",
    priceRange: "$$",
    url: "https://www.birkenstock.com/us/arizona-soft-footbed-natural-leather-oiled/arizona-core-oiledleather-softfootbed-eva-u_5326.html",
    image:
      "https://www.birkenstock.com/dw/image/v2/BLZD_PRD/on/demandware.static/-/Sites-master-catalog-amer/default/dw4dfcde85/452761/452761.jpg?sw=1148&sh=1148&sm=fit&q=80",
  },
  {
    slug: "johnston-murphy-rhodes-backpack",
    name: "Rhodes Leather Backpack",
    brand: "Johnston & Murphy",
    category: "Bags",
    reason: "Looks like a briefcase. Carries like a backpack.",
    priceRange: "$$",
    url: "https://www.johnstonmurphy.com/p/leather-goods-backpacks-briefcases/rhodes-backpack/14510.html?dwvar_14510_color=Tan%20Full%20Grain",
    image:
      "https://www.johnstonmurphy.com/dw/image/v2/AANO_PRD/on/demandware.static/-/Sites-genesco-master/default/dw64925262/large/4611736_master.jpg?sw=1200&sh=1130&strip=false",
  },
  {
    slug: "aveda-pureformance-cream",
    name: "Pure-Formance Grooming Cream",
    brand: "Aveda",
    category: "Grooming",
    reason: "Softer hold. Same trick — finish doesn’t read as done.",
    priceRange: "$$",
    url: "https://www.aveda.com/product/17776/16732/styling/mens-styling/aveda-men-pure-formance-grooming-cream?size=4.2_fl_oz%2F125_ml",
    image:
      "https://www.aveda.com/media/images/products/355x600/white/av_sku_A3TW01_34068_355x600_0.jpg",
  },
  {
    slug: "ahlem-haussmann",
    name: "Haussmann",
    brand: "Ahlem",
    category: "Eyewear",
    reason: "The frame that suits more faces than it should.",
    priceRange: "$$$",
    url: "https://www.ahlemeyewear.com/products/haussman?variant=44220169715961",
    image:
      "https://www.ahlemeyewear.com/cdn/shop/files/Haussmann_SUN_Champagne_01_WEB_grey_2d6e74b6-308e-46f5-9ece-376eab17439b_1500x1002_crop_center.jpg?v=1736543132",
  },
  {
    slug: "away-the-large",
    name: "The Large",
    brand: "Away",
    category: "Travel",
    reason: "Checked. Heavy-duty. Doesn’t pretend to be cute.",
    priceRange: "$$$",
    url: "https://www.awaytravel.com/products/large-navy-blue",
    image:
      "https://www.awaytravel.com/cdn/shop/files/872a3683-1382-44ea-b173-efa206cdd7d8_6a783a90-fdc2-4fab-ac47-a720cdc93b8e.jpg?v=1773689166&width=1200",
  },
  {
    slug: "massimo-dutti-cotton-tee",
    name: "100% Cotton Short-Sleeve T-Shirt",
    brand: "Massimo Dutti",
    category: "Apparel",
    reason: "Heavyweight cotton. The base layer for everything.",
    priceRange: "$",
    url: "https://www.massimodutti.com/us/100-cotton-short-sleeve-tshirt-l01418212?pelement=56718135",
    image:
      "https://static.massimodutti.net/assets/public/deb2/11c0/a0d24d6e8786/3f0d9377fc33/01418212712-o7/01418212712-o7.jpg?ts=1770630992252&w=1600&f=auto",
  },
  {
    slug: "goodfellow-flat-front-shorts",
    name: "5\" Flat Front Shorts",
    brand: "Goodfellow & Co.",
    category: "Apparel",
    reason: "Cheap in price. Not in how they wear.",
    priceRange: "$",
    url: "https://www.target.com/p/men-s-5-flat-front-shorts-goodfellow-co/-/A-94965145?preselect=94886502",
    image:
      "https://target.scene7.com/is/image/Target/GUEST_4f30aa05-e862-4b91-82fb-b14c368bda9d?wid=1200&hei=1200&qlt=80",
  },
  {
    slug: "prada-renylon-backpack",
    name: "Re-Nylon and Saffiano Leather Backpack",
    brand: "Prada",
    category: "Bags",
    reason: "Prada nylon is a uniform. This is the carry version.",
    priceRange: "$$$$",
    url: "https://www.prada.com/us/en/p/re-nylon-and-saffiano-leather-backpack/2VZ048_2DMG_F0002_V_OOO",
    image:
      "https://www.prada.com/content/dam/pradabkg_products/2/2VZ/2VZ048/2DMGF0002/2VZ048_2DMG_F0002_V_OOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg",
  },
  {
    slug: "uniqlo-oxford-oversized-shirt",
    name: "Oxford Oversized Shirt (Striped)",
    brand: "Uniqlo",
    category: "Apparel",
    reason: "Oversized without losing structure. Layers over everything.",
    priceRange: "$",
    url: "https://www.uniqlo.com/us/en/products/E484905-000/00?colorDisplayCode=01&sizeDisplayCode=003",
    image:
      "https://image.uniqlo.com/UQ/ST3/WesternCommon/imagesgoods/484905/sub/goods_484905_sub14_3x4.jpg",
  },
  {
    slug: "abercrombie-premium-ribbed-tank",
    name: "Premium Ribbed Tank",
    brand: "Abercrombie",
    category: "Apparel",
    reason: "Holds shape under everything. Worth it for that alone.",
    priceRange: "$",
    url: "https://www.abercrombie.com/shop/us/p/premium-ribbed-tank-61149838?categoryId=73458",
    image:
      "https://img.abercrombie.com/is/image/anf/KIC_124-5764-00037-900_model1?policy=product-extra-large",
  },
  {
    slug: "prada-renylon-duffle",
    name: "Re-Nylon and Saffiano Leather Duffle",
    brand: "Prada",
    category: "Bags",
    reason: "Built to take a beating. Doesn’t read like it has.",
    priceRange: "$$$$",
    url: "https://www.prada.com/us/en/p/re-nylon-and-saffiano-leather-duffle-bag/2VC013_2DMH_F0002_V_XOO",
    image:
      "https://www.prada.com/content/dam/pradabkg_products/2/2VC/2VC013/2DMHF0002/2VC013_2DMH_F0002_V_XOO_SLF.jpg/_jcr_content/renditions/cq5dam.web.hebebed.2400.2400.jpg",
  },
  {
    slug: "away-bigger-carry-on",
    name: "The Bigger Carry-On",
    brand: "Away",
    category: "Travel",
    reason: "Hits the size limit on purpose. Holds a week.",
    priceRange: "$$",
    url: "https://www.awaytravel.com/products/bigger-carry-on-navy-blue",
    image:
      "https://www.awaytravel.com/cdn/shop/files/215cd47b-8e23-4546-9a91-b5035b4d078c_9d00a95f-e0b6-4b8f-8ee6-ce6393f1b82e.jpg?v=1773689166&width=1200",
  },
  {
    slug: "clayton-crume-canvas-tote",
    name: "Canvas Market Tote",
    brand: "Clayton & Crume",
    category: "Bags",
    reason: "Heavy canvas, leather handles. Outlasts replacing.",
    priceRange: "$$",
    url: "https://claytonandcrume.com/products/canvas-market-tote?country=US&currency=USD&variant=47093690171559",
    image:
      "https://claytonandcrume.com/cdn/shop/files/CanvasMarketTote_1_1_e83c0901-e7be-49f1-972a-34e98cc9d5f9.jpg?v=1761077812&width=1200",
  },
];

export function getProductBySlug(slug: string): ShopProduct | undefined {
  return SHOP_PRODUCTS.find((p) => p.slug === slug);
}

export function getProductsByCategory(category: ShopCategory): ShopProduct[] {
  return SHOP_PRODUCTS.filter((p) => p.category === category);
}
