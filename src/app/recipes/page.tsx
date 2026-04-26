import type { Metadata } from "next";
import RecipesFilter from "../../components/RecipesFilter";
import { recipes } from "../../data/recipes";

export const metadata: Metadata = {
  title: "Recipes — Hessentials",
  description: "Food that earns its place.",
};

export default function RecipesIndexPage() {
  const filterable = recipes.map((entry) => ({
    slug: entry.slug,
    title: entry.recipe.title,
    description: entry.description,
    tags: entry.tags,
  }));

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
      </section>

      {/* ---------- Filter + Grid ---------- */}
      <div className="pb-32 sm:pb-40">
        <RecipesFilter recipes={filterable} />
      </div>
    </main>
  );
}
