import type { Metadata } from "next";
import { notFound } from "next/navigation";
import Recipe from "../../../components/Recipe";
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
    </main>
  );
}
