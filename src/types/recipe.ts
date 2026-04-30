export type Ingredient = {
  /** e.g. "2 tbsp", "1", "3 sprigs", "to taste" */
  quantity?: string;
  /** e.g. "olive oil", "shallot, finely diced" */
  name: string;
  /** Optional inline aside, e.g. "(or substitute butter)" */
  note?: string;
  /**
   * Optional sub-heading. When any ingredient in the list carries a
   * `group`, the ingredients section renders with sub-headings
   * (e.g. "Coconut Rice", "Shrimp Curry"). Used only for recipes
   * with distinct components.
   */
  group?: string;
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
  /**
   * Short opening paragraph (one or two sentences) sitting between the
   * title block and the ingredients section. Editorial body text — the
   * recipe's quick framing in the writer's voice.
   */
  opening?: string;
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
