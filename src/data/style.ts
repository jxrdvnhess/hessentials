export type ShopItem = {
  name: string;
  brand: string;
  reason: string;
  priceRange: "$" | "$$" | "$$$";
  alt: string;
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
const AUTHOR = "Jordan Hess";

export const STYLE_ARTICLES: StyleArticle[] = [
  {
    slug: "the-uniform-is-not-boring",
    category: "Style",
    eyebrow: "Personal Style",
    title: "The Uniform Is Not Boring",
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
          },
          {
            name: "Relaxed Tailored Trouser",
            brand: "COS",
            reason:
              "Gives structure without feeling stiff. Instantly elevates anything basic.",
            priceRange: "$$",
            alt: "Lululemon for a softer, more flexible version",
          },
          {
            name: "Soft Structured Jacket",
            brand: "Alo",
            reason:
              "Adds polish without trying too hard. This is where personality can live.",
            priceRange: "$$",
            alt: "Theory if you want it sharper",
          },
          {
            name: "Minimal Leather Sneaker",
            brand: "Common Projects",
            reason:
              "Clean, consistent, never distracting. Works across almost everything.",
            priceRange: "$$$",
            alt: "New Balance 990 if you want comfort first",
          },
        ],
      },
    ],
    tags: ["wardrobe", "uniform", "personal style", "essentials"],
  },
  {
    slug: "elevated-casual-is-a-discipline",
    category: "Style",
    eyebrow: "Everyday Dressing",
    title: "Elevated Casual Is a Discipline",
    subtitle: "Effortless is built. Not accidental.",
    dek: "Casual is where taste either shows up quietly or completely leaves the building.",
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
          },
          {
            name: "Relaxed Trouser",
            brand: "COS",
            reason:
              "Gives structure without stiffness. Works across multiple outfits.",
            priceRange: "$$",
            alt: "Aritzia for a softer drape",
          },
          {
            name: "Suede Everyday Shoe",
            brand: "Clarks",
            reason: "Adds texture and intention without being loud.",
            priceRange: "$$",
            alt: "Birkenstock Boston Suede for a more relaxed version",
          },
          {
            name: "Soft Overshirt",
            brand: "Alex Mill",
            reason:
              "The easiest layer to throw on that still looks considered.",
            priceRange: "$$",
            alt: "J.Crew for a simpler option",
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
    title: "Texture Is the Outfit",
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
          },
          {
            name: "Suede Loafer",
            brand: "Tod’s",
            reason: "Brings texture and polish without being formal.",
            priceRange: "$$$",
            alt: "Vince for a more accessible version",
          },
          {
            name: "Linen Napkin Set",
            brand: "Food52",
            reason: "Transforms a table without adding clutter.",
            priceRange: "$$",
            alt: "Zara Home for a simpler option",
          },
          {
            name: "Matte Ceramic Dishware",
            brand: "Fable",
            reason: "Soft finish makes everything feel more considered.",
            priceRange: "$$",
            alt: "Crate & Barrel for a classic version",
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
    title: "The 5-Piece Rule",
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
        heading: "Every outfit needs structure.",
        body: `I think about outfits in five parts: base, structure, texture, contrast, and finish.

If one is missing, the whole thing feels slightly off. Not bad. Just not right.

This is why some outfits look good in theory but feel wrong in real life. They are incomplete.`,
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
          },
          {
            name: "Tailored Trouser",
            brand: "Theory",
            reason: "Gives shape instantly.",
            priceRange: "$$$",
            alt: "Quince for a budget version",
          },
          {
            name: "Textured Layer",
            brand: "Alex Mill",
            reason: "Adds depth without noise.",
            priceRange: "$$",
            alt: "Everlane",
          },
          {
            name: "Minimal Accessory",
            brand: "Mejuri",
            reason: "Finishes without distracting.",
            priceRange: "$$",
            alt: "Quince",
          },
        ],
      },
    ],
    tags: ["outfits", "styling system"],
  },
  {
    slug: "the-details-that-change-everything",
    category: "Style",
    eyebrow: "Taste Notes",
    title: "The Details That Change Everything",
    subtitle: "This is why some people look better and no one can explain why.",
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
        heading: "Most people skip this part.",
        body: `Pant break, sleeve length, fabric weight, clean shoes.

These are small things that quietly control the entire outcome.

You do not need better outfits. You need better attention.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If it looks off and you cannot explain why, it is probably a detail.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Check your sleeve length in the mirror.",
          "Clean your shoes before leaving the house.",
          "Notice fabric weight differences.",
          "Adjust one small thing before changing the outfit.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Small upgrades. Noticeable difference.",
        items: [
          {
            name: "Garment Steamer",
            brand: "Conair",
            reason: "Wrinkles instantly ruin intention.",
            priceRange: "$",
            alt: "Rowenta",
          },
          {
            name: "Leather Care Kit",
            brand: "Jason Markk",
            reason: "Clean shoes change everything.",
            priceRange: "$$",
            alt: "Kiwi",
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
    title: "The Anti-Trend Rule",
    subtitle: "If it only works right now, it never really worked.",
    dek: "Trends are data. Not direction.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "minimal wardrobe, timeless neutrals",
    sections: [
      {
        type: "intro",
        heading: "You are always slightly late to trends.",
        body: `By the time you see it everywhere, it is already over.`,
      },
      {
        type: "essay",
        heading: "Borrow, don’t follow.",
        body: `Trends can be useful. They show what people are responding to.

But your job is to filter, not adopt.

If it does not look like you, it will never feel right.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If it feels like you are trying something on, you probably are.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Ignore trends for one month.",
          "Rewear your strongest outfits.",
          "Notice what still feels good.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Timeless > temporary.",
        items: [
          {
            name: "Classic White Shirt",
            brand: "Toteme",
            reason: "Never needs to prove itself.",
            priceRange: "$$$",
            alt: "Everlane",
          },
        ],
      },
    ],
    tags: ["trends", "style philosophy"],
  },
  {
    slug: "the-signature-piece",
    category: "Style",
    eyebrow: "Identity",
    title: "The Signature Piece",
    subtitle: "The thing people start associating with you.",
    dek: "Repetition builds identity.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "hero jacket focus",
    sections: [
      {
        type: "intro",
        heading: "You do not need variety. You need recognition.",
        body: `This is where style becomes identity.`,
      },
      {
        type: "essay",
        heading: "Pick something and commit.",
        body: `A jacket, a shoe, a watch, a scent.

Not ten. One.

That is how people remember you.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If everything changes, nothing sticks.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Identify one item you love wearing repeatedly.",
          "Wear it more, not less.",
          "Build around it.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Choose something you won’t get tired of.",
        items: [
          {
            name: "Sherpa Jacket",
            brand: "Alo",
            reason: "Recognizable, wearable, not loud.",
            priceRange: "$$",
            alt: "Abercrombie",
          },
        ],
      },
    ],
    tags: ["signature", "identity"],
  },
  {
    slug: "the-entryway-test",
    category: "Style",
    eyebrow: "Home",
    title: "The Entryway Test",
    subtitle: "Your house starts talking before you do.",
    dek: "Make sure it says something intentional.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "warm entry vignette",
    sections: [
      {
        type: "intro",
        heading: "First impressions are fast.",
        body: `People decide how they feel about your space immediately.`,
      },
      {
        type: "essay",
        heading: "It does not need to be big.",
        body: `It needs a landing moment. Light, texture, and function.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "Your entry needs a lamp before anything else.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Add one warm light source.",
          "Create a key drop.",
          "Remove clutter.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Simple, intentional.",
        items: [
          {
            name: "Ceramic Table Lamp",
            brand: "CB2",
            reason: "Soft light changes everything.",
            priceRange: "$$",
            alt: "Target",
          },
        ],
      },
    ],
    tags: ["entryway", "home"],
  },
  {
    slug: "signature-scent-is-branding",
    category: "Style",
    eyebrow: "Personal",
    title: "Signature Scent Is Branding",
    subtitle: "People remember how you smell.",
    dek: "You just don’t realize it.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "fragrance still life",
    sections: [
      {
        type: "intro",
        heading: "Scent is memory.",
        body: `This matters more than people admit.`,
      },
      {
        type: "essay",
        heading: "Recognition over volume.",
        body: `It should sit close, not announce itself.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If your scent enters before you, it’s too much.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Choose one daytime scent.",
          "Choose one evening scent.",
          "Wear both consistently.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Close, intentional, memorable.",
        items: [
          {
            name: "Santal 33",
            brand: "Le Labo",
            reason: "Recognizable without trying.",
            priceRange: "$$$",
            alt: "Maison Margiela Replica",
          },
        ],
      },
    ],
    tags: ["scent", "fragrance"],
  },
  {
    slug: "your-home-has-an-outfit-too",
    category: "Style",
    eyebrow: "Home",
    title: "Your Home Has an Outfit Too",
    subtitle: "And some rooms are not dressed well.",
    dek: "Same system. Bigger scale.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "warm modern classic room",
    sections: [
      {
        type: "intro",
        heading: "It is the same instinct.",
        body: `You already know how to do this.`,
      },
      {
        type: "essay",
        heading: "Translate it.",
        body: `Base, structure, texture, finish.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If everything is loud, nothing is working.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Remove three items.",
          "Add one texture.",
          "Adjust lighting.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Edit first, then add.",
        items: [
          {
            name: "Linen Throw Pillow",
            brand: "H&M Home",
            reason: "Softens everything instantly.",
            priceRange: "$",
            alt: "The Citizenry",
          },
        ],
      },
    ],
    tags: ["home", "interior"],
  },
  {
    slug: "hosting-is-a-performance",
    category: "Style",
    eyebrow: "Hosting",
    title: "Hosting Is a Performance",
    subtitle: "In a calm, controlled way.",
    dek: "A good night is designed.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "warm dinner scene",
    sections: [
      {
        type: "intro",
        heading: "People remember the feeling.",
        body: `Not the menu.`,
      },
      {
        type: "essay",
        heading: "Design the night.",
        body: `Light, sound, pacing.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "Overhead lighting ruins everything.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Lower lighting.",
          "Start music early.",
          "Set the table simply.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Atmosphere first.",
        items: [
          {
            name: "Candle Set",
            brand: "Diptyque",
            reason: "Softens the entire room.",
            priceRange: "$$$",
            alt: "P.F. Candle Co.",
          },
        ],
      },
    ],
    tags: ["hosting"],
  },
  {
    slug: "the-dinner-plate-is-a-style-object",
    category: "Style",
    eyebrow: "Food",
    title: "The Dinner Plate Is a Style Object",
    subtitle: "Yes, it matters.",
    dek: "Presentation changes everything.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "plated dinner",
    sections: [
      {
        type: "intro",
        heading: "This is not extra.",
        body: `It is the point.`,
      },
      {
        type: "essay",
        heading: "Edit the plate.",
        body: `Space, color, texture.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If it’s all one color, it’s not done.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Use white plates.",
          "Add green.",
          "Finish with oil or crunch.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Simple upgrades.",
        items: [
          {
            name: "White Dinnerware",
            brand: "Fable",
            reason: "Makes everything look better.",
            priceRange: "$$",
            alt: "Crate & Barrel",
          },
        ],
      },
    ],
    tags: ["food", "plating"],
  },
  {
    slug: "style-is-not-gendered",
    category: "Style",
    eyebrow: "Philosophy",
    title: "Style Is Not Gendered",
    subtitle: "The rules are the same.",
    dek: "Only the expression changes.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "mixed styling silhouettes",
    sections: [
      {
        type: "intro",
        heading: "This is simpler than people make it.",
        body: `Fit, proportion, texture.`,
      },
      {
        type: "essay",
        heading: "Same system.",
        body: `Different expression.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "Good taste translates.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Focus on fit first.",
          "Then texture.",
          "Then proportion.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Universal pieces.",
        items: [
          {
            name: "Relaxed Trouser",
            brand: "COS",
            reason: "Works across styles and identities.",
            priceRange: "$$",
            alt: "Uniqlo",
          },
        ],
      },
    ],
    tags: ["inclusive", "style"],
  },
  {
    slug: "the-bag-sets-the-tone",
    category: "Style",
    eyebrow: "Accessories",
    title: "The Bag Sets the Tone",
    subtitle: "If it looks chaotic, everything feels chaotic.",
    dek: "Structure matters more than you think.",
    author: AUTHOR,
    tone: TONE,
    heroStyle: "minimal carry bag",
    sections: [
      {
        type: "intro",
        heading: "Your bag tells the story.",
        body: `Before you even speak.`,
      },
      {
        type: "essay",
        heading: "Structure creates calm.",
        body: `A good bag removes friction.`,
      },
      {
        type: "callout",
        label: "Jordan’s Rule",
        body: "If your bag is chaos, your day will be too.",
      },
      {
        type: "practical",
        heading: "Try This First",
        items: [
          "Empty your bag.",
          "Rebuild with intention.",
          "Remove duplicates.",
        ],
      },
      {
        type: "shop",
        heading: "Shop the Idea",
        note: "Clean, functional, repeatable.",
        items: [
          {
            name: "Leather Tote",
            brand: "Cuyana",
            reason: "Structured without trying too hard.",
            priceRange: "$$",
            alt: "Everlane",
          },
        ],
      },
    ],
    tags: ["bags", "accessories"],
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
