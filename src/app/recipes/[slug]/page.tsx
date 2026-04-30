import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Recipe from "../../../components/Recipe";
import JsonLd from "../../../components/JsonLd";
import { recipeSchema } from "../../../lib/jsonLd";
import { recipes, getRecipeBySlug } from "../../../data/recipes";

type Params = { slug: string };

export function generateStaticParams() {
  return recipes.map((entry) => ({ slug: entry.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug } = await params;
  const entry = getRecipeBySlug(slug);
  if (!entry) return {};

  return {
    title: `${entry.recipe.title} — Hessentials`,
    description: entry.recipe.dek ?? entry.description,
  };
}

export default async function RecipeDetailPage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  const entry = getRecipeBySlug(slug);
  if (!entry) notFound();

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <Recipe recipe={entry.recipe} />

      {/* ---------- Bottom — onward ---------- */}
      <nav
        aria-label="Continue reading"
        className="mx-auto mt-32 mb-24 max-w-2xl px-6 text-center sm:mt-40 sm:px-10 md:mt-48 md:mb-32"
      >
        <Link
          href="/recipes"
          className="inline-flex items-baseline gap-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/80 sm:text-[11px]"
        >
          <span aria-hidden>←</span>
          Recipes
        </Link>
        <p className="mt-6 font-serif text-[15px] italic leading-[1.6] text-[#1f1d1b]/50 sm:text-[16px]">
          More to come back to.
        </p>
      </nav>

      {/* Recipe structured data — surfaces in Google's recipe
          carousels with cook time, ingredients, and steps. */}
      <JsonLd
        data={recipeSchema({
          url: `/recipes/${entry.slug}`,
          recipe: entry.recipe,
          description: entry.description,
        })}
      />
    </main>
  );
}
