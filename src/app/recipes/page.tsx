import type { Metadata } from "next";
import RecipesFilter from "../../components/RecipesFilter";
import { recipes } from "../../data/recipes";

export const metadata: Metadata = {
  title: "Recipes — Hessentials",
  description: "Food that earns its place.",
};

// Quiet guidance tags — sentence case, functional, never stacked.
// Vocabulary: Weeknight · Make again · Beginner-safe · Pantry.
// Applied sparingly so they anchor scanning without becoming labels.
const RECIPE_CUES: Record<string, string> = {
  "mediterranean-shrimp-white-beans": "Weeknight",
  "sunday-rigatoni": "Make again",
  "tuscan-orzo": "Make again",
  "sourdough-with-olive-oil-and-garlic": "Beginner-safe",
  "yellow-coconut-vegetable-curry": "Pantry",
};

export default function RecipesIndexPage() {
  const filterable = recipes.map((entry) => ({
    slug: entry.slug,
    title: entry.recipe.title,
    description: entry.description,
    tags: entry.tags,
    cue: RECIPE_CUES[entry.slug],
  }));

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ----------
          The intro carries the curatorial framing. The previous "Start
          Here" block restated the same premise ("the few worth cooking")
          one frame too many — same editorial logic that killed "This
          stayed." It's been removed; recipes now flow straight from the
          intro into the filter list. */}
      <section className="mx-auto flex w-full max-w-3xl flex-col items-center px-6 pt-16 pb-16 text-center sm:px-10 md:pt-24 md:pb-20">
        {/* Hairline above the pillar eyebrow (§2.2). */}
        <span
          aria-hidden
          className="block w-20"
          style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
        />
        <p className="mt-6 mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
          Recipes
        </p>
        <p className="text-pretty mx-auto max-w-xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] italic leading-[1.4] text-[#1f1d1b]/80">
          Food that earns its place.
        </p>
        <p className="mx-auto mt-5 max-w-md font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
          Start with a few. Come back to the rest.
        </p>
      </section>

      {/* ---------- Filter + Grid ---------- */}
      <div className="pb-32 sm:pb-40">
        <RecipesFilter recipes={filterable} />
      </div>
    </main>
  );
}
