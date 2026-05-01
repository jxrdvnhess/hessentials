export type ShopItem = {
  name: string;
  brand: string;
  reason: string;
  priceRange: "$" | "$$" | "$$$";
  alt: string;
  /**
   * Direct buy link for the primary product. Brand-owned site preferred;
   * reliable retailer (Nordstrom, etc.) acceptable as fallback.
   * Required — per Hessentials STYLE rule, products without a buyable
   * URL must not be referenced.
   */
  url: string;
  /** Direct buy link for the alternative recommendation. */
  altUrl?: string;
};

export type StyleSection =
  | { type: "intro"; heading: string; body: string }
  | { type: "essay"; heading: string; body: string }
  | { type: "callout"; label: string; body: string }
  | { type: "practical"; heading: string; items: string[] }
  | { type: "shop"; heading: string; note: string; items: ShopItem[] };

export type StyleArticle = {
  slug: string;
  category: "Style";
  eyebrow: string;
  title: string;
  subtitle: string;
  dek: string;
  author: string;
  tone: string[];
  heroStyle: string;
  sections: StyleSection[];
  tags: string[];
};

const TONE = ["editorial", "personal", "practical", "slightly sassy"];
const AUTHOR = "J.D.H.";

export const STYLE_ARTICLES: StyleArticle[] = [
  {
    slug: "the-uniform-is-not-boring",
    category: "Style",
    eyebrow: "Personal Style",
    title: "The uniform is not boring.",
    subtitle:
      "It is what happens when you finally stop letting your closet emotionally terrorize you.",
    dek: "A uniform is not about repetition. It is about relief.",
    author: AUTHOR,
    tone: TONE,
    heroStyle:
      "minimal editorial outfit flatlay, warm ivory plaster background, charcoal and camel tones, soft shadow, no clutter",
    sections: [
      {
        type: "intro",
        heading: "Getting dressed should not feel like a negotiation.",
        body: `There is a very specific kind of exhaustion that comes from standing in front of a full closet and still feeling like nothing makes sense.

That is not a lack of clothes. That is a lack of decisions.

A uniform fixes that. Not in a restrictive way, but in a "thank God, I already know what works" way. It removes the daily spiral. It gives you something to fall back on that actually holds up.`,
      },
      {
        type: "essay",
        heading: "A uniform is just your taste, edited.",
        body: `I do not believe in having more options than you can confidently choose from.

For me, a uniform is simple: a good pant, a clean top, one strong layer, and a shoe that makes sense. The variation comes from texture, proportion, and small shifts, not from reinventing yourself every morning like it is a personal rebrand.

The mistake people make is thinking a uniform has to be boring. It does not. It just cannot look like you panicked.

If your outfit cannot survive a last-minute dinner plan or running into someone you know, it was never a strong outfit to begin with. A uniform handles real life.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "Your closet should not require a full staff meeting every time you leave the house.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Pick one color family you already trust and build inside of it.",
          "Create three outfits using pieces you already own before buying anything new.",
          "Pay attention to what you reach for twice in one week. That is your real style.",
          "Replace the worst version of your most-worn item first.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Fewer pieces. Better decisions. These earn their place.",
        items: [
          {
            name: "Heavyweight Structured Tee",
            brand: "Buck Mason",
            reason:
              "Holds shape, does not collapse after one wear, works under everything.",
            priceRange: "$$",
            alt: "COS for a slightly more minimal cut",
            url: "https://www.buckmason.com/collections/heavyweight-tees",
            altUrl: "https://www.cos.com/en_usd/men/men-tops/men-t-shirts.html",
          },
          {
            name: "Relaxed Tailored Trouser",
            brand: "COS",
            reason:
              "Gives structure without feeling stiff. Instantly elevates anything basic.",
            priceRange: "$$",
            alt: "Lululemon for a softer, more flexible version",
            url: "https://www.cos.com/en_usd/men/men-trousers.html",
            altUrl: "https://shop.lululemon.com/c/mens-pants",
          },
          {
            name: "Soft Structured Jacket",
            brand: "Alo",
            reason:
              "Adds polish without trying too hard. This is where personality can live.",
            priceRange: "$$",
            alt: "Theory if you want it sharper",
            url: "https://www.aloyoga.com/collections/mens-jackets-and-hoodies",
            altUrl: "https://www.theory.com/men/jackets-coats/",
          },
          {
            name: "Minimal Leather Sneaker",
            brand: "Common Projects",
            reason:
              "Clean, consistent, never distracting. Works across almost everything.",
            priceRange: "$$$",
            alt: "New Balance 990 if you want comfort first",
            url: "https://www.nordstrom.com/sr?keyword=common+projects+achilles",
            altUrl: "https://www.newbalance.com/pd/made-in-usa-990v6/M990V6-43094-PMG-NA.html",
          },
        ],
      },
    ],
    tags: ["wardrobe", "uniform", "personal style", "essentials"],
  },
  {
    slug: "casual-is-not-a-free-pass",
    category: "Style",
    eyebrow: "Everyday Dressing",
    title: "Casual is not a free pass.",
    subtitle: "It only looks effortless.",
    dek: "There is a very specific middle ground. Relaxed, but not undone.",
    author: AUTHOR,
    tone: TONE,
    heroStyle:
      "editorial casual outfit, knit polo, relaxed trouser, suede shoe, warm plaster background",
    sections: [
      {
        type: "intro",
        heading: "Casual is not a free pass.",
        body: `I fully support comfort. I do not support giving up and calling it casual.

There is a very specific middle ground I care about. You look relaxed, but not undone. Comfortable, but still intentional. Like you got dressed without making it a whole thing, but you absolutely made a decision.`,
      },
      {
        type: "essay",
        heading: "The difference is small, but it is everything.",
        body: `Elevated casual is usually one upgrade away from average.

A knit instead of a basic tee. A real pant instead of something that gave up at the waistband. A shoe that looks chosen, not default.

The goal is not to impress anyone. It is to feel like yourself in a slightly sharper way. That is what makes it repeatable.

Also, if the outfit only works when you are standing perfectly still, it is not a good outfit. It needs to survive errands, sitting, walking, real life. That is the test.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If it is comfortable but has no shape, it is not elevated. It is just soft.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Replace one cotton tee with a knit version.",
          "Swap one pair of joggers for a relaxed trouser.",
          "Keep your colors quiet and let texture do the work.",
          "Choose shoes that look intentional, even if they are simple.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Small upgrades. Big difference.",
        items: [
          {
            name: "Knit Polo or Tee",
            brand: "Reiss",
            reason:
              "Immediately sharper than a basic tee without feeling dressed up.",
            priceRange: "$$",
            alt: "Abercrombie for a more accessible version",
            url: "https://www.reiss.com/us/en/category/mens-tops",
            altUrl: "https://www.abercrombie.com/shop/us/mens-tops",
          },
          {
            name: "Relaxed Trouser",
            brand: "COS",
            reason:
              "Gives structure without stiffness. Works across multiple outfits.",
            priceRange: "$$",
            alt: "Aritzia for a softer drape",
            url: "https://www.cos.com/en_usd/men/men-trousers.html",
            altUrl: "https://www.aritzia.com/us/en/clothing/pants",
          },
          {
            name: "Suede Everyday Shoe",
            brand: "Clarks",
            reason: "Adds texture and intention without being loud.",
            priceRange: "$$",
            alt: "Birkenstock Boston Suede for a more relaxed version",
            url: "https://www.clarks.com/c/mens-shoes/suede",
            altUrl: "https://www.birkenstock.com/us/boston-soft-footbed-suede-leather/boston-suede-suedeleather-softfootbed-eva-u_46.html",
          },
          {
            name: "Soft Overshirt",
            brand: "Alex Mill",
            reason:
              "The easiest layer to throw on that still looks considered.",
            priceRange: "$$",
            alt: "J.Crew for a simpler option",
            url: "https://www.alexmill.com/collections/men-shirts",
            altUrl: "https://www.jcrew.com/c/mens/categories/clothing/shirts",
          },
        ],
      },
    ],
    tags: ["casual style", "everyday", "wardrobe"],
  },
  {
    slug: "texture-is-the-outfit",
    category: "Style",
    eyebrow: "Taste Notes",
    title: "Texture is the outfit.",
    subtitle: "Color gets attention. Texture gets respect.",
    dek: "The easiest way to look more considered is to stop adding color and start adding depth.",
    author: AUTHOR,
    tone: TONE,
    heroStyle:
      "editorial still life, knit, suede, linen, stone textures, warm neutral palette",
    sections: [
      {
        type: "intro",
        heading: "This is where things quietly get better.",
        body: `I will always care more about texture than color.

Color is fun. Texture is what makes something feel like it has a point of view.

A neutral outfit with the right materials will always feel more elevated than something loud that does not know what it is doing.`,
      },
      {
        type: "essay",
        heading: "Texture is how you make simple look intentional.",
        body: `This applies to everything. Clothes, homes, tables, even food.

When everything is smooth and flat, it feels unfinished. When you layer texture, things start to feel grounded. A knit with a trouser. Linen on a table. Wood next to ceramic. Suede with cotton.

You do not need more things. You need better contrast between the things you already have.

That is why texture is such an easy upgrade. It does not require a full reset. It just requires paying attention.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "When something feels off, it is usually missing texture, not more color.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Build one outfit using only two colors but at least three textures.",
          "Add linen or woven elements to your table instead of more decor.",
          "Swap one flat fabric for something with structure or weight.",
          "Layer matte and soft finishes instead of adding brightness.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Less color. More depth.",
        items: [
          {
            name: "Textured Knit Sweater",
            brand: "Everlane",
            reason: "Adds depth instantly without complicating the outfit.",
            priceRange: "$$",
            alt: "Naadam for a softer, more premium feel",
            url: "https://www.everlane.com/collections/mens-sweaters",
            altUrl: "https://naadam.co/collections/mens-cashmere-sweaters",
          },
          {
            name: "Suede Loafer",
            brand: "Tod’s",
            reason: "Brings texture and polish without being formal.",
            priceRange: "$$$",
            alt: "Vince for a more accessible version",
            url: "https://www.tods.com/us-en/Men/Shoes/Gommino-and-City-Gommino/c/211-Tods/",
            altUrl: "https://www.vince.com/men/shoes",
          },
          {
            name: "Linen Napkin Set",
            brand: "Food52",
            reason: "Transforms a table without adding clutter.",
            priceRange: "$$",
            alt: "Zara Home for a simpler option",
            url: "https://food52.com/shop/categories/napkins",
            altUrl: "https://www.zarahome.com/us/dining-room/napkins-c1020528.html",
          },
          {
            name: "Matte Ceramic Dishware",
            brand: "Fable",
            reason: "Soft finish makes everything feel more considered.",
            priceRange: "$$",
            alt: "Crate & Barrel for a classic version",
            url: "https://fablehome.co/collections/dinnerware",
            altUrl: "https://www.crateandbarrel.com/dining-and-entertaining/dinnerware-place-settings/1",
          },
        ],
      },
    ],
    tags: ["texture", "style", "home", "wardrobe"],
  },
  {
    slug: "the-5-piece-rule",
    category: "Style",
    eyebrow: "Outfit Systems",
    title: "The 5-piece rule.",
    subtitle: "If something feels off, it’s usually because something is missing.",
    dek: "Most bad outfits are not wrong. They are just unfinished.",
    author: AUTHOR,
    tone: TONE,
    heroStyle:
      "editorial outfit breakdown, five components laid out on plaster background",
    sections: [
      {
        type: "intro",
        heading: "This is where outfits quietly fall apart.",
        body: `You know that feeling when something is not working, but you cannot figure out why?

It is usually not the whole outfit. It is one missing layer of intention.`,
      },
      {
        type: "essay",
        heading: "Every outfit has five parts. If one is missing, you feel it.",
        body: `I think about outfits in five parts: base, structure, texture, contrast, and finish.

The base is the easiest to overlook. A clean tee, a fitted knit, a simple shirt — the layer everything else sits on. If the base is wrong, nothing on top of it works.

The structure is the piece that gives the outfit a silhouette. A trouser, a jacket, a skirt with shape. Something that holds a line. Without structure, an outfit reads soft.

The texture is what keeps it from feeling flat. A heavyweight knit. A suede. A raw cotton. The eye needs at least one weight that is different from the others, or the whole outfit reads thin.

The contrast is the one element that breaks the palette without breaking the outfit. A black shoe with a tan-on-tan look. A pale top with darker pants. A leather where everything else is fabric. Without contrast, an outfit looks like a uniform — in the bad way.

The finish is the last detail. A watch, a bag, a hat, a pair of sunglasses. The thing that signals you finished getting dressed. An outfit without a finish reads like you got close.

Most "off" outfits are missing one of these. Identify which, add it, walk out the door.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If your outfit feels off, do not change everything. Add one missing piece.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Start with a base layer you trust.",
          "Add one structured piece.",
          "Introduce one texture.",
          "Break the palette slightly.",
          "Finish with a shoe or accessory that makes sense.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Each piece plays a role. Nothing extra.",
        items: [
          {
            name: "Structured Base Tee",
            brand: "Buck Mason",
            reason: "Holds the outfit together from the start.",
            priceRange: "$$",
            alt: "COS for a cleaner silhouette",
            url: "https://www.buckmason.com/collections/heavyweight-tees",
            altUrl: "https://www.cos.com/en_usd/men/men-tops/men-t-shirts.html",
          },
          {
            name: "Tailored Trouser",
            brand: "Theory",
            reason: "Gives shape instantly.",
            priceRange: "$$$",
            alt: "Uniqlo for a budget version",
            url: "https://www.theory.com/men/pants",
            altUrl: "https://www.uniqlo.com/us/en/men/pants/smart-pants",
          },
          {
            name: "Textured Layer",
            brand: "Alex Mill",
            reason:
              "A heavyweight overshirt or knit that adds the weight an outfit needs to stop reading flat.",
            priceRange: "$$",
            alt: "Everlane for a more accessible version",
            url: "https://www.alexmill.com/collections/men-shirt-jackets-overshirts",
            altUrl: "https://www.everlane.com/collections/mens-shirts",
          },
          {
            name: "Contrast Shoe",
            brand: "Common Projects Black Achilles",
            reason:
              "A clean black shoe is the easiest contrast piece in any neutral outfit. Breaks the palette without making noise.",
            priceRange: "$$$",
            alt: "Veja V-10 in black for a softer alternative",
            url: "https://www.nordstrom.com/sr?keyword=common+projects+black+achilles",
            altUrl: "https://www.veja-store.com/en_us/men-v-10",
          },
          {
            name: "Minimal Accessory",
            brand: "Mejuri",
            reason:
              "A watch, a chain, a single ring. The piece that tells the room you finished getting dressed.",
            priceRange: "$$",
            alt: "Madewell for a more accessible price point",
            url: "https://mejuri.com/shop/categories/all-jewelry",
            altUrl: "https://www.madewell.com/jewelry",
          },
        ],
      },
    ],
    tags: ["outfits", "styling system"],
  },
  {
    slug: "its-usually-the-small-things",
    category: "Style",
    eyebrow: "Taste Notes",
    title: "It's usually the small things.",
    subtitle: "Some people look better and no one can explain why.",
    dek: "It is not more effort. It is better awareness.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "close-up details: cuff, shoe, fabric, layered neutrals",
    sections: [
      {
        type: "intro",
        heading: "This is where taste actually lives.",
        body: `No one compliments "good sleeve length."

And yet… it changes everything.`,
      },
      {
        type: "essay",
        heading: "The five details that do most of the work.",
        body: `Pant break. A full break (fabric pooling on the shoe) reads sloppy on most cuts. A half-break — fabric kissing the top of the shoe — is the one to ask the tailor for. A no-break only works on a slim ankle and a clean shoe; otherwise it looks short.

Sleeve length. The cuff should sit where the heel of the hand meets the wrist. Shorter reads outgrown. Longer reads borrowed. Get a tailor to set this once and you will stop noticing it forever.

Fabric weight. A light cotton tee under a heavy wool coat reads off because the proportions of the materials do not match. Match weight to weight: heavyweight knit with a real trouser, lightweight knit with a softer cotton. The eye registers this even when the brain does not.

Clean shoes. The single fastest way to look better. Brush the suede. Wipe the leather. Replace the laces when they fray. A great outfit on dirty shoes reads as careless. A simple outfit on cared-for shoes reads as intentional.

Crisp cuffs and collars. A wrinkled collar undoes the whole shirt. Steam, do not iron — faster, fewer creases, no scorching. A handheld steamer is one of the most underrated style tools there is.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If it looks off and you cannot explain why, it is almost always a detail. Fix the detail before changing the outfit.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Take a full-length photo of yourself in your most-worn outfit. Check sleeve length and pant break.",
          "Brush or wipe your shoes before walking out the door. Two minutes, every time.",
          "Steam — do not iron — your shirt collar and cuffs. Five seconds each.",
          "Find a tailor and get one pair of pants hemmed correctly. Use that as your reference for everything else.",
          "Replace any frayed lace, broken zipper, or missing button. These are visible, even from across a room.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Small tools. Big difference.",
        items: [
          {
            name: "Handheld Garment Steamer",
            brand: "Steamery Cirrus 2",
            reason:
              "Powerful enough for wool, fast enough to use before walking out. Lives near the door, gets used daily.",
            priceRange: "$$",
            alt: "Conair Turbo Extreme for an everyday version",
            url: "https://www.amazon.com/STEAMERY-Cirrus-NO-2-Steamer-Black/dp/B07NF9GTBF",
            altUrl: "https://www.target.com/s?searchTerm=conair+turbo+extreme+steamer",
          },
          {
            name: "Suede Brush + Eraser Kit",
            brand: "Jason Markk",
            reason:
              "Brings suede shoes back from one wear. The single most cost-effective shoe-care purchase you can make.",
            priceRange: "$",
            alt: "Kiwi for a basic alternative",
            url: "https://jasonmarkk.com/products/premium-suede-cleaning-kit",
            altUrl: "https://www.target.com/s?searchTerm=kiwi+shoe+polish",
          },
          {
            name: "Leather Conditioner",
            brand: "Saphir Renovateur",
            reason:
              "Twice a year on every leather shoe and bag. Doubles their lifespan and keeps them from cracking.",
            priceRange: "$$",
            alt: "Bickmore Bick 4 for a more accessible option",
            url: "https://saphir.com/products/renovateur",
            altUrl: "https://bickmore.com/products/bick-4-leather-conditioner-8oz",
          },
        ],
      },
    ],
    tags: ["details", "fit", "style"],
  },
  {
    slug: "the-anti-trend-rule",
    category: "Style",
    eyebrow: "Philosophy",
    title: "The anti-trend rule.",
    subtitle: "If it only works right now, it never really worked.",
    dek: "Trends are information. They are not instruction.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "minimal wardrobe, timeless neutrals",
    sections: [
      {
        type: "intro",
        heading: "You are always slightly late to trends.",
        body: `By the time a trend reaches you, it has already been on the runway, on the people who shop runways, on Pinterest, on the early adopters, and on the brands knocking it off. You are arriving in the last 20%.

That is not a problem. It is a signal. The trend is no longer telling you something new.`,
      },
      {
        type: "essay",
        heading: "Borrow, do not follow.",
        body: `Trends are useful as a read on what feels right in the moment. They are not useful as a shopping list.

The test is simple: would you wear this in three years?

If the answer is yes, the trend is just confirming taste you already had. Buy it, wear it, integrate it. You were going to land there anyway.

If the answer is no, you are paying for the look of belonging. That is the most expensive way to dress, because the receipt is permanent and the relevance is not.

Take the wide-leg trouser cycle. Wide-leg pants come back every decade. People who already liked a wider leg buy them and they look like themselves. People who do not, buy them, feel slightly costumed for a season, and then donate them. Same trend. Two completely different outcomes, decided by whether the piece was already on-brand for the person.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If you are buying it because everyone else is, you have already missed the moment that mattered.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Before buying anything trending, ask: would I wear this in three years? If no, skip it.",
          "Spend a month not opening any fashion content. Notice what you actually reach for.",
          "Identify two pieces you bought because of a trend and never wore. That is your data.",
          "If you want a trend in your wardrobe, take it in the cheapest version possible. Save the budget for pieces that hold up.",
          "Keep a short list of pieces you want to be wearing in five years. Buy from that list, not from your feed.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Pieces that have outlasted every trend cycle they have been part of.",
        items: [
          {
            name: "Classic White Button-Down",
            brand: "Toteme",
            reason:
              "Has been in style since shirts existed and will be in style after most of us. Never needs to prove itself.",
            priceRange: "$$$",
            alt: "Everlane Relaxed Oxford for an everyday version",
            url: "https://toteme-studio.com/collections/shirts",
            altUrl: "https://www.everlane.com/collections/mens-shirts",
          },
          {
            name: "Straight-Leg Denim",
            brand: "AGOLDE 90s",
            reason:
              "Cut that pre-dates the trend and outlasts it. A jean that holds up across years and silhouettes.",
            priceRange: "$$",
            alt: "Levi's 501 — the original, still correct",
            url: "https://agolde.com/collections/womens-90s-jean",
            altUrl: "https://www.levi.com/US/en_US/jeans-by-fit-number/men/jeans/501/c/levi_jeans_by_fit_number_men_jeans_501",
          },
          {
            name: "Crewneck Cashmere",
            brand: "Naadam",
            reason:
              "Has never not worked. Buy in a color you wear, not the one you are seeing online.",
            priceRange: "$$",
            alt: "Uniqlo 100% Cashmere for a more accessible option",
            url: "https://naadam.co/collections/mens-cashmere-sweaters",
            altUrl: "https://www.uniqlo.com/us/en/men/sweaters/cashmere",
          },
        ],
      },
    ],
    tags: ["trends", "philosophy", "wardrobe"],
  },
  {
    slug: "the-signature-piece",
    category: "Style",
    eyebrow: "Identity",
    title: "The signature piece.",
    subtitle: "Pick one thing. Wear it until it becomes the thing people associate with you.",
    dek: "Style is not built on variety. It is built on repetition done well.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "hero jacket focus",
    sections: [
      {
        type: "intro",
        heading: "Think about the people whose style you actually remember.",
        body: `You do not remember their full wardrobe. You remember one thing.

A specific jacket. A particular shoe. A watch they wear every day. The same scent, room after room. That is the move.`,
      },
      {
        type: "essay",
        heading: "How to find yours.",
        body: `A signature piece is not chosen. It is noticed.

It is the thing you reach for without thinking. The piece you have already worn this week and want to wear again. The one that makes you feel like yourself the second it is on. If you have to talk yourself into it, it is not the one.

Pick from a category that earns repetition. A jacket. A shoe. A watch. A scent. A bag. These are pieces you can wear again and again without anyone clocking it as a uniform — they read as your taste settling in.

Avoid pieces that demand a moment. A statement coat that needs the right outfit underneath is not a signature piece. That is a costume. A signature piece works on a Tuesday at noon as well as it works at dinner.

Then commit. The mistake people make is buying their signature piece and then immediately diluting it by buying three alternates. Do not. The whole idea is repetition. Wear it until it has a patina, then wear it more.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If you have it in three colors, none of them is your signature piece.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Look at the last week of photos on your phone. Notice what you are wearing more than once. Start there.",
          "Choose a category that earns repetition. Outerwear, footwear, accessory, scent.",
          "If you are between two pieces, pick the one you would wear tomorrow without checking the weather or the calendar.",
          "Wear it for thirty days straight. If you stop reaching for it, it was not the one.",
          "When the first one wears out, replace it with the same piece. Do not upgrade. Do not switch.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Three categories that earn repetition. Pick one.",
        items: [
          {
            name: "Workwear-Cut Chore Coat",
            brand: "Margaret Howell",
            reason:
              "Heavyweight cotton, structured but unfussy. Reads casual or considered depending on what is under it. Gets better with wear.",
            priceRange: "$$$",
            alt: "Alex Mill for the same shape at half the price",
            url: "https://www.margarethowell.co.uk/men/clothing",
            altUrl: "https://www.alexmill.com/collections/men-shirt-jackets-overshirts",
          },
          {
            name: "Suede Loafer",
            brand: "Tod’s Gommino",
            reason:
              "A shoe people will start to associate with you. Quiet enough to wear daily, distinct enough to register.",
            priceRange: "$$$",
            alt: "Sezane for a softer, more accessible version",
            url: "https://www.tods.com/us-en/Men/Shoes/Gommino-and-City-Gommino/c/211-Tods/",
            altUrl: "https://www.sezane.com/us/category/shoes-1",
          },
          {
            name: "Field Watch",
            brand: "Hamilton Khaki",
            reason:
              "An everyday watch that does not announce itself. Reads as personal, not as a status piece.",
            priceRange: "$$",
            alt: "Timex Marlin for a vintage-feel alternative",
            url: "https://www.hamiltonwatch.com/en-us/h69439931-khaki-field-mechanical.html",
            altUrl: "https://www.timex.com/marlin-collection/",
          },
        ],
      },
    ],
    tags: ["signature", "identity", "wardrobe"],
  },
  {
    slug: "the-entryway-test",
    category: "Style",
    eyebrow: "Home",
    title: "The entryway test.",
    subtitle: "Your home is making an argument before you say a word.",
    dek: "Stand at your front door, walk in, and ask three questions.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "warm entry vignette",
    sections: [
      {
        type: "intro",
        heading: "The first six feet decide the rest of the house.",
        body: `Whatever someone walks into first becomes the lens for everything else they see. If your entry is hectic, the rest of your home reads as hectic too — even if it is not.

The good news: an entry is small. You can fix it in a weekend.`,
      },
      {
        type: "essay",
        heading: "Three questions. That is the test.",
        body: `Stand outside your door. Walk in like a guest. Then answer these:

One — is there a place to put my keys, my phone, and one bag without thinking? If the answer is "the floor" or "anywhere I can find a spot," you have a function problem. A small tray and a hook fix it.

Two — is the first light I see warm? Overhead lights and cool LEDs are interrogation lighting. A single warm lamp on a table changes the whole reading of the room.

Three — is there one thing here worth looking at? Not a lot of things. One. A piece of art, a vase with branches, a stack of books with weight. The eye needs somewhere to land that is not utility.

If the entry passes all three, the house does too. If it fails any of them, fix that one before fixing anything else.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "An entry needs a lamp before it needs anything else. If yours has overhead light only, start there.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Add a small table or floating shelf if you do not have one. Twelve inches is enough.",
          "Put a tray on it. Keys, wallet, glasses. Everything off the surface, into the tray.",
          "Plug in a warm-bulb table lamp. 2700K, no cooler.",
          "Hang one piece of art at eye level. Skip the gallery wall.",
          "Remove anything that does not belong: shoes you do not wear, mail piles, that one box.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Small footprint. High return.",
        items: [
          {
            name: "Ceramic Table Lamp",
            brand: "Cedar & Moss",
            reason:
              "Warm, soft, weighted. The single object that does the most work in an entryway.",
            priceRange: "$$",
            alt: "CB2 for a cleaner profile",
            url: "https://cedarandmoss.com/collections/table-lamps",
            altUrl: "https://www.cb2.com/lighting/table-lamps/1",
          },
          {
            name: "Wall-Mounted Brass Hook",
            brand: "Schoolhouse",
            reason:
              "One real hook, not a row of plastic ones. Holds a coat or a bag without making the wall busy.",
            priceRange: "$",
            alt: "Rejuvenation for similar quality",
            url: "https://www.schoolhouse.com/collections/hooks-hardware",
            altUrl: "https://www.rejuvenation.com/products/category/hardware/wall-hooks",
          },
          {
            name: "Catchall Tray",
            brand: "Hawkins New York",
            reason:
              "Stops the surface from becoming a junk drawer. A tray turns mess into a vignette.",
            priceRange: "$$",
            alt: "Crate & Barrel for a basic version",
            url: "https://hawkinsnewyork.com/collections/trays",
            altUrl: "https://www.crateandbarrel.com/decorating-and-accessories/trays/1",
          },
          {
            name: "Floor-Length Mirror",
            brand: "West Elm",
            reason:
              "If your entry is small, a leaning mirror doubles the light and gives you one last check before you leave.",
            priceRange: "$$",
            alt: "IKEA Hovet for the same effect at a fraction of the price",
            url: "https://www.westelm.com/shop/decor/decorative-mirrors/full-length-mirrors/",
            altUrl: "https://www.ikea.com/us/en/p/hovet-mirror-aluminum-40507196/",
          },
        ],
      },
    ],
    tags: ["entryway", "home", "first impressions"],
  },
  {
    slug: "the-scent-people-remember",
    category: "Style",
    eyebrow: "Personal",
    title: "The scent people remember.",
    subtitle: "Worn close, repeated often, never announced.",
    dek: "Most people pick the wrong scent for the wrong reason. The right one becomes part of how people think of you.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "fragrance still life",
    sections: [
      {
        type: "intro",
        heading: "People remember how you smell more than they remember what you wore.",
        body: `Scent attaches to memory in a way that almost nothing else does. Years later, someone catches a note of cedar or vanilla in a doorway and thinks of you.

That is the move. Not loud. Not new every season. One scent, worn close, repeated until it becomes shorthand for you.`,
      },
      {
        type: "essay",
        heading: "Close, not projecting.",
        body: `The mistake most people make is buying a fragrance that fills a room.

A scent that announces itself is doing the work of saying "I am here." A scent that sits close to the skin is doing the work of being remembered. The first reads as performance. The second reads as identity.

Pick something with sillage you can control. Eau de toilette over eau de parfum if you tend to over-spray. Wood, musk, or skin-adjacent notes over heavy florals or sweet gourmands if you want it to read as personal rather than purchased.

Day and evening can be the same scent or two different ones — that is preference, not rule. What matters is that you wear them long enough for people to associate them with you. Six months minimum before you swap. Otherwise you are just trying things on.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If your scent enters the room before you do, it is too much.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Sample for a week before you commit. A scent on a card is not a scent on your skin.",
          "Spray once on the chest, once on the wrist. Stop there. Two sprays is the ceiling.",
          "Wear the same scent for 30 days. If you stop noticing it, that is correct — others still do.",
          "Avoid fragrances designed for a specific season. The right one works in any temperature.",
          "If three people have asked what you are wearing in the last year, that is your scent. Stop searching.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Three scents that read as personal, not promotional.",
        items: [
          {
            name: "Santal 33",
            brand: "Le Labo",
            reason:
              "Recognizable without trying. Wood, leather, a little cardamom. Wears close. Has aged into a quiet classic.",
            priceRange: "$$$",
            alt: "Maison Margiela Replica 'Jazz Club' for similar warmth at half the price",
            url: "https://www.lelabofragrances.com/santal-33-147.html",
            altUrl: "https://www.sephora.com/product/replica-jazz-club-P385350",
          },
          {
            name: "Vetiver",
            brand: "Guerlain",
            reason:
              "Earthy, slightly green, almost ascetic. The kind of scent people associate with one specific person.",
            priceRange: "$$$",
            alt: "Goldfield & Banks 'Velvet Splendour' for a softer take",
            url: "https://www.sephora.com/product/vetiver-eau-de-toilette-P380901",
            altUrl: "https://goldfieldbanks.com/products/velvet-splendour",
          },
          {
            name: "Eau de Cologne",
            brand: "Chanel Les Eaux de Chanel",
            reason:
              "An everyday, lower-projection option. Citrus, clean, never overdone. Good for the day before a meeting.",
            priceRange: "$$",
            alt: "Acqua di Parma Colonia for a more affordable classic",
            url: "https://www.chanel.com/us/fragrance/c/7x1x1x37/les-eaux-de-chanel/",
            altUrl: "https://www.acquadiparma.com/default/en/colonia/COLONIAEDCRP.html",
          },
        ],
      },
    ],
    tags: ["scent", "fragrance", "signature"],
  },
  {
    slug: "your-home-has-an-outfit-too",
    category: "Style",
    eyebrow: "Home",
    title: "Your home has an outfit too.",
    subtitle: "And some rooms are not dressed well.",
    dek: "If you can edit a closet, you can edit a room. Same instinct, bigger scale.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "warm modern classic room",
    sections: [
      {
        type: "intro",
        heading: "Walk into a room and read it like an outfit.",
        body: `Most rooms that feel off are not under-decorated. They are over-everything-d.

Too many colors. Too many finishes. Too many objects fighting for the same shelf. The fix is the same one you already use on yourself in the morning: edit first, then add.`,
      },
      {
        type: "essay",
        heading: "The four parts of a dressed room.",
        body: `Think of a room the way you think of an outfit: base, structure, texture, finish.

The base is the largest piece — the sofa, the rug, the bed. This is your trouser. Get it neutral, get it durable, get it in a color you can live with for ten years. Loud bases age fast.

The structure is the case goods — coffee table, console, dresser, dining table. This is your jacket. It gives the room a silhouette. Wood, metal, stone. Something with weight.

The texture is the soft layer — pillows, throws, curtains, linens. This is your knit. It is what keeps a clean room from feeling like a showroom. Linen, wool, mohair, raw cotton. Mix at least three.

The finish is the small layer — lamps, art, ceramics, books, the one strange object you found on a trip. This is your watch and your shoe. Get this part wrong and the whole outfit looks generic.

If a room feels like nothing, you are usually missing texture or finish. If a room feels chaotic, you have too much finish and not enough base.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "Loud rooms are usually rooms with no base. They are all accessories.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Remove three objects from the room. Live with the absence for a week before deciding if anything goes back.",
          "Identify your base, structure, texture, and finish. If one is missing, add only there.",
          "Replace one synthetic textile (poly throw, plastic-feel rug) with a natural one. Linen, wool, cotton.",
          "Switch off the overhead. Light the room with two lamps and see what is actually there.",
          "Move the loudest object out of the room for a day. If you do not miss it, it was not earning its place.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "One layer at a time. Most rooms are missing one of the four.",
        items: [
          {
            name: "Linen-Blend Sofa",
            brand: "Article",
            reason:
              "A neutral, low-arm linen sofa is the home equivalent of a relaxed trouser. Quiet enough to live with, structured enough to anchor a room.",
            priceRange: "$$$",
            alt: "Sundays for a softer, more handmade feel",
            url: "https://www.article.com/category/sofas",
            altUrl: "https://sundays-company.com/collections/sofas",
          },
          {
            name: "Solid Wood Coffee Table",
            brand: "Crate & Barrel",
            reason:
              "Real wood with weight. Adds a finish you cannot fake with veneer or particleboard.",
            priceRange: "$$",
            alt: "West Elm for more design variety",
            url: "https://www.crateandbarrel.com/furniture/coffee-tables/1",
            altUrl: "https://www.westelm.com/shop/furniture/all-coffee-tables/",
          },
          {
            name: "Heavyweight Linen Throw",
            brand: "The Citizenry",
            reason:
              "Reads as texture before color. Gets better the more it crumples, which is the whole point.",
            priceRange: "$$",
            alt: "H&M Home for an everyday version",
            url: "https://www.the-citizenry.com/collections/throws",
            altUrl: "https://www2.hm.com/en_us/home/shop-by-product/throws.html",
          },
          {
            name: "Ceramic Table Lamp",
            brand: "Cedar & Moss",
            reason:
              "Warm light at eye level. The single fastest way to make a room feel finished.",
            priceRange: "$$",
            alt: "CB2 for a cleaner profile",
            url: "https://cedarandmoss.com/collections/table-lamps",
            altUrl: "https://www.cb2.com/lighting/table-lamps/1",
          },
        ],
      },
    ],
    tags: ["home", "interior", "rooms"],
  },
  {
    slug: "people-can-feel-when-its-forced",
    category: "Style",
    eyebrow: "Hosting",
    title: "People can feel when it's forced.",
    subtitle: "Atmosphere is built, not added.",
    dek: "Hosting is not what happens at dinner. It is what happens in the two hours before.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "warm dinner scene",
    sections: [
      {
        type: "intro",
        heading: "The night is set before anyone arrives.",
        body: `If you are still working when your first guest walks in, the night is already off.

People do not remember the menu. They remember whether they could exhale when they walked in. That is not luck. That is staging.`,
      },
      {
        type: "essay",
        heading: "Atmosphere is built, not added.",
        body: `Three things do most of the work: light, sound, pacing. In that order.

Light is the easiest to get wrong and the easiest to fix. Turn off the overheads. Lamps and candles only. If a room cannot be lit by lamps and candles, that is a furniture problem, not a dimmer problem.

Sound has to be on before the doorbell rings. Not loud. Present. A room without music feels like a waiting room, and your guest will register it before they realize why.

Pacing is what people remember and never name. Drinks get poured, not asked about. The first thing on the table is already there when they sit down. Dinner lands when people are ready to sit, not when the timer says so. If you are still standing twenty minutes after a guest arrived, you are working, not hosting.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If you are still in the kitchen when the first guest arrives, the night is already behind.",
      },
      {
        type: "essay",
        heading: "What not to do.",
        body: `Skip the welcome speech. No one needs a tour.

Do not ask what people want to drink. Pour something good. They can ask for something else.

Plated apps look like a wedding. Put a board down and let people approach it.

Do not apologize for anything. Not the food, not the apartment, not the playlist. The host sets the tone — if you are anxious, the room is anxious.`,
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Turn off every overhead light an hour before people arrive.",
          "Start the playlist thirty minutes early so it is part of the room, not announced.",
          "Have one thing already on the table when guests walk in — olives, a bowl of nuts, anything.",
          "Pour the first drink without asking.",
          "Sit down within the first fifteen minutes. If you cannot, your menu is too ambitious.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Atmosphere first. Food second.",
        items: [
          {
            name: "Tuberose or Wood Candle",
            brand: "Diptyque",
            reason:
              "One candle in the right place changes a whole room. Light it before guests arrive so the scent is in the air, not arriving with it.",
            priceRange: "$$$",
            alt: "P.F. Candle Co. for an everyday version",
            url: "https://www.diptyqueparis.com/en_us/p/tubereuse-tuberose-candle-190g.html",
            altUrl: "https://pfcandleco.com/collections/candles",
          },
          {
            name: "Smart Dimmers",
            brand: "Lutron Caséta",
            reason:
              "The single biggest atmosphere upgrade in any home. If your overhead lights cannot dim, they should not be on.",
            priceRange: "$$",
            alt: "Leviton Decora for a simpler install",
            url: "https://www.casetawireless.com/us/en/products/dimmers-switches/diva-smart-dimmer-switch",
            altUrl: "https://www.leviton.com/products/residential/lighting-controls/decora-dimmers-fan-controls",
          },
          {
            name: "Compact Speaker",
            brand: "Sonos Era 100",
            reason:
              "Sounds intentional, looks intentional, gets out of the way. Hide it on a shelf, not on the counter.",
            priceRange: "$$$",
            alt: "Marshall Stanmore III for warmer character",
            url: "https://www.sonos.com/en-us/shop/era-100",
            altUrl: "https://www.marshall.com/us/en/product/stanmore-iii?pid=1006014",
          },
          {
            name: "Universal Wine Glass",
            brand: "Zalto Universal",
            reason:
              "One shape, all wine. Stops the cabinet from filling up with single-purpose stems.",
            priceRange: "$$$",
            alt: "Schott Zwiesel Pure for an everyday version",
            url: "https://www.amazon.com/Zalto-DenkArt-Universal-Hand-Blown-Crystal/dp/B08DH1F81Q",
            altUrl: "https://www.crateandbarrel.com/search?query=schott+zwiesel+pure",
          },
        ],
      },
    ],
    tags: ["hosting", "atmosphere", "dinner"],
  },
  {
    slug: "the-dinner-plate-is-a-style-object",
    category: "Style",
    eyebrow: "Food",
    title: "The dinner plate is a style object.",
    subtitle: "Same food, different plate, completely different meal.",
    dek: "Plating is not garnish. It is the difference between food someone eats and food someone remembers.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "plated dinner",
    sections: [
      {
        type: "intro",
        heading: "The same dish lands differently on the right plate.",
        body: `A bowl of pasta covered edge-to-edge looks like a cafeteria. The same pasta, in the center of a wider plate, with one swipe of olive oil and a torn basil leaf, looks like dinner.

Same food. Same effort. The plate is doing the work.`,
      },
      {
        type: "essay",
        heading: "Three things ruin most plates.",
        body: `One — the food covers the entire surface. A plate needs negative space the way a room needs empty walls. The eye reads the white as intention. Without it, dinner looks like a pile.

Two — everything is the same color. A bowl of beige food, no matter how good it tastes, photographs and presents flat. One green element, one acid, one finish. That is the rule.

Three — there is no finish. A plate without a final touch looks unfinished because it is. A drizzle of oil, a crack of pepper, a sprinkle of flake salt, a sprig of something fresh. Five seconds of work that signals "this was on purpose."

Use a plate one size larger than you think. Center the food. Leave a clean rim. Then add the green, the acid, and the finish in that order.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If the plate is full to the edge, the food is not the problem. The plate is too small.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Switch to one size larger plates than you currently use. Most home dinnerware is undersized.",
          "Plate from the center. Leave at least an inch of rim showing.",
          "Add one green: parsley, basil, dill, chive. Torn, not chopped.",
          "Finish with oil. A swirl of good olive oil makes anything look intentional.",
          "Add one texture: crunch, crumble, flake salt. The eye needs a final note.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Bigger plates. Better finishes.",
        items: [
          {
            name: "Wide-Rim White Dinnerware",
            brand: "Fable",
            reason:
              "Slightly oversized, slightly off-white, made to leave space around the food. Makes home cooking look composed.",
            priceRange: "$$",
            alt: "Crate & Barrel for a thinner-rim alternative",
            url: "https://fablehome.co/collections/dinnerware",
            altUrl: "https://www.crateandbarrel.com/dining-and-entertaining/dinnerware-place-settings/1",
          },
          {
            name: "Olive Oil Bottle with Pour Spout",
            brand: "Brightland",
            reason:
              "Quality oil and a real spout. Both matter. A drizzle is the easiest finish there is.",
            priceRange: "$$",
            alt: "California Olive Ranch in a refilled bottle",
            url: "https://brightland.co/collections/olive-oil",
            altUrl: "https://www.californiaoliveranch.com/collections/olive-oil",
          },
          {
            name: "Flake Salt",
            brand: "Maldon",
            reason:
              "Adds finish, adds texture, adds intention. A pinch on top of almost anything makes it look plated.",
            priceRange: "$",
            alt: "Jacobsen for an American-made version",
            url: "https://www.williams-sonoma.com/products/maldon-salt/",
            altUrl: "https://www.williams-sonoma.com/m/products/jacobsen-salt-company-flake-finishing-sea-salt/",
          },
          {
            name: "Linen Napkins",
            brand: "Hawkins New York",
            reason:
              "Reads as 'this was set, not thrown together.' A small upgrade with outsized effect.",
            priceRange: "$$",
            alt: "Crate & Barrel for a more accessible price point",
            url: "https://hawkinsnewyork.com/collections/linens-and-textiles",
            altUrl: "https://www.crateandbarrel.com/dining-and-entertaining/cloth-napkins/1",
          },
        ],
      },
    ],
    tags: ["food", "plating", "table"],
  },
  {
    slug: "style-is-not-gendered",
    category: "Style",
    eyebrow: "Philosophy",
    title: "Style is not gendered.",
    subtitle: "The rules read the same on everyone.",
    dek: "Fit, proportion, and texture do not care who is wearing them.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "mixed styling silhouettes",
    sections: [
      {
        type: "intro",
        heading: "The rules are the rules.",
        body: `A well-cut trouser is well-cut on anyone. A bad fit is a bad fit. Texture reads the same on every body.

The reason fashion makes this complicated is that fashion sells more clothes when you buy two of everything. Style does not work that way.`,
      },
      {
        type: "essay",
        heading: "What actually changes is the silhouette, not the system.",
        body: `Take one piece — a black, low-rise, slightly cropped wool trouser. Cut wide at the bottom.

On a smaller frame, it works with a fitted knit and a flat shoe. The proportion is the trouser doing the volume and the top staying close.

On a larger frame, the same trouser works with a heavier knit and a shoe with a little weight. Same trouser. Same rule. The proportion just resets relative to the body.

Nothing changes about the standard. Fit first. Then texture. Then proportion. Then finish.

The piece is not what differs. The combination differs. That is what people mean when they say someone has style — they understand combination, regardless of which side of the store they shop on.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "Stop shopping by department. Shop by silhouette.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Pick one piece you love. Try it on with three different combinations of weight, length, and shoe.",
          "Stop reading sizing as identity. A small in one brand is a medium in another. The number is information, not meaning.",
          "If a piece only works one way, it is not a strong piece. Strong pieces hold up across silhouettes.",
          "Ignore the gender label on a tag once. See what happens.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Pieces that hold their shape across bodies.",
        items: [
          {
            name: "Wide-Leg Wool Trouser",
            brand: "COS",
            reason:
              "A real trouser cut wide enough to be the silhouette. Reads as intentional on anyone wearing it.",
            priceRange: "$$",
            alt: "Toteme for a more elevated version",
            url: "https://www.cos.com/en_usd/search/?text=wide+leg+wool+trouser",
            altUrl: "https://toteme-studio.com/collections/trousers",
          },
          {
            name: "Heavyweight Crewneck Knit",
            brand: "Naadam",
            reason:
              "Weight matters more than cut here. A real knit drapes; a thin one looks like an afterthought.",
            priceRange: "$$",
            alt: "Uniqlo for an everyday version",
            url: "https://naadam.co/collections/cashmere-sweaters",
            altUrl: "https://www.uniqlo.com/us/en/men/sweaters/cashmere",
          },
          {
            name: "Leather Derby or Loafer",
            brand: "Margaret Howell",
            reason:
              "A clean, slightly weighted shoe finishes any silhouette without committing to a category.",
            priceRange: "$$$",
            alt: "G.H. Bass Weejuns for the original at half the price",
            url: "https://www.margarethowell.co.uk/men/shoes",
            altUrl: "https://www.ghbass.com/collections/the-original-weejuns",
          },
        ],
      },
    ],
    tags: ["philosophy", "fit", "proportion"],
  },
  {
    slug: "the-bag-sets-the-tone",
    category: "Style",
    eyebrow: "Accessories",
    title: "The bag sets the tone.",
    subtitle: "Your bag is either holding your day or becoming the first problem in it.",
    dek: "A good bag is structure. A bad bag is the reason you are late.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "minimal carry bag",
    sections: [
      {
        type: "intro",
        heading: "A bag is read before you say anything.",
        body: `Walk into a meeting, a restaurant, a flight. Your bag arrives before you do.

If it looks slumped, overstuffed, and spilling charging cables, the read is "scattered." If it stands up on its own, closes cleanly, and has one job, the read is "in control." Same person, same outfit, completely different impression.`,
      },
      {
        type: "essay",
        heading: "Structure over slouch.",
        body: `Most of the bags people own do not stand up. That is the whole problem.

A bag with no structure becomes a sack. The contents shift, the shape collapses, and you spend ten minutes a day rummaging. A structured bag — leather, canvas with a base, anything that holds a silhouette — keeps the contents organized by virtue of its shape. You stop hunting for things because there are fewer places they can be.

Pick the material to match the day. Leather reads more considered and lasts longer. Canvas reads more relaxed and washes. Nylon is for travel, not a Tuesday meeting. Match material to context the same way you match shoes to occasion.

Then commit to one bag for the week. Most people own four or five bags and rotate them, which means they re-pack constantly and lose things in the process. Pick one. Use it. Empty it on Friday. Repack on Monday. That is the system.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If your bag does not stand up on its own, neither does your day.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Empty your current bag onto a table. Cull anything you have not used in two weeks.",
          "Use a small pouch inside the bag for cords and chargers. They are the chaos source.",
          "Pick one bag and use it for seven days. No swapping.",
          "If your bag has a logo, ask whether it is doing more than the bag is.",
          "Replace your slumped tote first. That is the bag costing you the most every day.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Three bags that hold their shape across price tiers.",
        items: [
          {
            name: "Classic Easy Tote",
            brand: "Cuyana",
            reason:
              "Italian leather, double handles, room for a 16-inch laptop. Softens with use without going slack. Reads as intentional in any room — the bag people start associating with you after a year.",
            priceRange: "$$$",
            alt: "Madewell Transport for a more accessible version",
            url: "https://cuyana.com/products/classic-easy-tote",
            altUrl: "https://www.madewell.com/p/womens/accessories/bags/totes/the-medium-transport-tote/F5788/",
          },
          {
            name: "Waxed Canvas Carryall",
            brand: "Filson Field Bag",
            reason:
              "For days when leather is too much. Structured base, real hardware, ages well, never apologizes.",
            priceRange: "$$",
            alt: "L.L.Bean Boat & Tote (zip-top) for the same logic at a third of the cost",
            url: "https://www.filson.com/products/small-rugged-twill-field-bag-tan-1",
            altUrl: "https://www.llbean.com/llb/shop/37037?page=boat-and-tote-bag-zip-top",
          },
          {
            name: "Compact Crossbody",
            brand: "Polène Numéro Dix",
            reason:
              "When you need to carry less, not more. Structured shell, clean closure, reads as a deliberate edit.",
            priceRange: "$$$",
            alt: "Mansur Gavriel Mini Tote for a softer-shape alternative",
            url: "https://eng.polene-paris.com/collections/numero-dix",
            altUrl: "https://www.mansurgavriel.com/collections/small-tote",
          },
        ],
      },
    ],
    tags: ["bags", "accessories", "carry"],
  },
];

export function getAllStyleSlugs(): string[] {
  return STYLE_ARTICLES.map((a) => a.slug);
}

export function getStyleArticleBySlug(
  slug: string
): StyleArticle | undefined {
  return STYLE_ARTICLES.find((a) => a.slug === slug);
}
