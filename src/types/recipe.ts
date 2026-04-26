export type Ingredient = {
  /** e.g. "2 tbsp", "1", "3 sprigs", "to taste" */
  quantity?: string;
  /** e.g. "olive oil", "shallot, finely diced" */
  name: string;
  /** Optional inline aside, e.g. "(or substitute butter)" */
  note?: string;
};

export type RecipeMeta = {
  serves?: string;
  time?: string;
  yields?: string;
};

export type RecipeImage = {
  src: string;
  alt: string;
  width: number;
  height: number;
};

export type RecipeOrigin = {
  /** Small uppercase label above the body — e.g. "From My Family Kitchen". */
  heading?: string;
  /** A short paragraph framing the origin or heritage of the dish. */
  body: string;
  /** Optional supporting image — a recipe card, a photograph, a scan. */
  image?: RecipeImage;
};

export type Recipe = {
  /** Small uppercase label above the title — e.g. "Recipe" or a series. */
  eyebrow?: string;
  title: string;
  /** One-line editorial dek beneath the title. */
  dek?: string;
  meta?: RecipeMeta;
  image?: RecipeImage;
  byline?: string;
  ingredients: Ingredient[];
  /** Method steps as plain strings; component handles numbering & spacing. */
  method: string[];
  /** A short, single-line serving suggestion. */
  serve?: string;
  /** Optional alternates — each rendered as its own quiet line. */
  variations?: string[];
  /** Optional closing notes paragraph. */
  notes?: string;
  /** Optional origin / heritage block — story plus an optional image. */
  origin?: RecipeOrigin;
};
