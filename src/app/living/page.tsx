import type { Metadata } from "next";
import { getAllLivingArticles } from "../../lib/living";
import LivingFilter, {
  type LivingGroup,
  type LivingIndexArticle,
} from "../../components/LivingFilter";

export const metadata: Metadata = {
  title: "Living — Hessentials",
  description:
    "Notes on rooms, rituals, plants, and the small decisions that change how home feels.",
};

/**
 * Editorial groupings keyed by article slug. The interactive filter row
 * lives in <LivingFilter />; this map decides which bucket each piece
 * belongs to so the filter ("Systems" / "Environment" / "Rituals") can
 * narrow the list. Articles without an explicit group default to
 * Systems — review and add an entry here when a new piece ships.
 */
const GROUPS: Record<string, LivingGroup> = {
  "the-one-pot-that-does-everything": "Systems",
  "ditch-the-coffee-machine-get-an-espresso-machine": "Systems",
  "why-most-kitchens-are-set-up-wrong": "Systems",
  "why-you-dont-cook-more": "Systems",
  "stop-buying-plush-blankets-use-cotton": "Environment",
  "youre-not-bad-with-plants": "Environment",
  "the-10-minute-reset": "Rituals",
  "stop-using-fabric-softener": "Rituals",
};

export default async function LivingIndexPage() {
  const articles = await getAllLivingArticles();

  const projected: LivingIndexArticle[] = articles.map((article) => ({
    slug: article.slug,
    title: article.meta.title,
    excerpt: article.excerpt,
    group: GROUPS[article.slug] ?? "Systems",
  }));

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ---------- */}
      <section className="mx-auto w-full max-w-3xl px-6 pt-16 pb-12 text-center sm:px-10 md:pt-24">
        <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
          Living
        </p>
        <p className="text-pretty mx-auto max-w-2xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] italic leading-[1.4] text-[#1f1d1b]/80">
          Some things feel good. Some things work. They are not the same.
        </p>
      </section>

      {/* ---------- Filter + Grid (shuffled on every visit when "All") ---------- */}
      <div className="pb-32 sm:pb-40">
        <LivingFilter articles={projected} />
      </div>
    </main>
  );
}
