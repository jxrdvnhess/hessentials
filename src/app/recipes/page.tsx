import type { Metadata } from "next";
import Link from "next/link";
import RecipesFilter from "../../components/RecipesFilter";
import { recipes } from "../../data/recipes";

export const metadata: Metadata = {
  title: "Recipes — Hessentials",
  description: "Food that earns its place.",
};

// Recipes that work even when you're not trying that hard:
// minimal ingredients or simple technique, forgiving execution,
// strong flavor payoff. Excluded from the default "All" grid to
// avoid immediate repetition.
const FEATURED_SLUGS = [
  "orzo-with-spinach-garlic-and-parmesan",
  "thai-basil-ground-chicken",
  "chili-crisp-egg-and-rice-bowl",
  "simple-arugula-salad",
] as const;

// Quiet guidance tags — sentence case, functional, never stacked.
// Vocabulary: Weeknight · Make again · Beginner-safe · Pantry.
// Applied sparingly so they anchor scanning without becoming labels.
const RECIPE_CUES: Record<string, string> = {
  "mediterranean-shrimp-white-beans": "Weeknight",
  "garlic-butter-chicken-with-crispy-potatoes": "Weeknight",
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

  const featured = FEATURED_SLUGS.map((slug) =>
    filterable.find((r) => r.slug === slug)
  ).filter((r): r is NonNullable<typeof r> => Boolean(r));

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ---------- */}
      <section className="mx-auto w-full max-w-3xl px-6 pt-16 pb-10 text-center sm:px-10 md:pt-24">
        <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
          Recipes
        </p>
        <p className="text-pretty mx-auto max-w-xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] italic leading-[1.4] text-[#1f1d1b]/80">
          Food that earns its place.
        </p>
        <p className="mx-auto mt-5 max-w-md font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
          Start with a few. Come back to the rest.
        </p>
      </section>

      {/* ---------- Start Here ---------- */}
      <section className="mx-auto w-full max-w-6xl px-6 pt-8 pb-16 sm:px-10 sm:pt-12 sm:pb-24">
        <div className="mx-auto mb-12 max-w-3xl text-center sm:mb-16">
          <p className="mb-5 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
            Start here
          </p>
          <h2 className="text-pretty mx-auto max-w-xl font-serif text-[clamp(1.25rem,2.2vw,1.625rem)] leading-[1.25] tracking-[-0.01em] text-[#1f1d1b]">
            If you cook nothing else from here, cook these
          </h2>
          <p className="mx-auto mt-4 max-w-md font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
            Simple, reliable, and worth repeating.
          </p>
        </div>

        <ul className="mx-auto grid w-full max-w-5xl grid-cols-1 gap-x-12 gap-y-14 sm:grid-cols-2 sm:gap-x-14 md:gap-x-20 md:gap-y-16">
          {featured.map((recipe) => (
            <li key={recipe.slug}>
              <Link
                href={`/recipes/${recipe.slug}`}
                className="group block transition-opacity duration-500 ease-out"
              >
                <h3 className="font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30">
                  {recipe.title}
                </h3>
                <p className="text-pretty mt-4 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[17px]">
                  {recipe.description}
                </p>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      {/* ---------- The Rest ---------- */}
      <section className="mx-auto w-full max-w-3xl px-6 pt-8 pb-12 text-center sm:px-10 sm:pt-12 sm:pb-16">
        <p className="mb-5 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
          The rest
        </p>
        <p className="mx-auto max-w-md font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
          More to come back to.
        </p>
      </section>

      {/* ---------- Filter + Grid ---------- */}
      <div className="pb-32 sm:pb-40">
        <RecipesFilter
          recipes={filterable}
          deferSlugs={FEATURED_SLUGS as unknown as readonly string[]}
        />
      </div>
    </main>
  );
}
