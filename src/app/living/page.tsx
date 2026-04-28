import type { Metadata } from "next";
import { getAllLivingArticles } from "../../lib/living";
import LivingFilter, {
  type LivingGroup,
  type LivingIndexArticle,
} from "../../components/LivingFilter";
import SectionDivider from "../../components/SectionDivider";

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
  "stop-using-overhead-lights-after-sunset": "Environment",
  "the-10-minute-reset": "Rituals",
  "stop-using-fabric-softener": "Rituals",
};

/**
 * Editor's pick — a small, deliberately mixed handful surfaced in a
 * "Start Here" rail above the main archive on the default ("All") view.
 * Ordered intentionally; not shuffled. The mix is intentional: one
 * systems piece, one environment piece, one behavioral piece, one
 * opinion piece — to signal the page's range, not its corrections.
 * Update sparingly — this is the page's point of view.
 */
const FEATURED_SLUGS = [
  "why-most-kitchens-are-set-up-wrong",
  "stop-using-overhead-lights-after-sunset",
  "the-10-minute-reset",
  "why-you-dont-cook-more",
  "why-tucson-is-the-best-town-in-the-southwest",
];

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
      <section className="mx-auto flex w-full max-w-3xl flex-col items-center px-6 pt-16 pb-12 text-center sm:px-10 md:pt-24">
        {/* Hairline above the pillar eyebrow (§2.2). */}
        <span
          aria-hidden
          className="block w-20"
          style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
        />
        <p className="mt-6 mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
          Living
        </p>
        <p className="text-pretty mx-auto max-w-2xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] italic leading-[1.4] text-[#1f1d1b]/80">
          Some things feel good. Some things work. They are not the same.
        </p>
        <p className="text-pretty mx-auto mt-6 max-w-xl font-serif text-[15px] leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
          What holds up. What doesn&rsquo;t. And how to tell the difference.
        </p>
      </section>

      {/* "h" motif transitioning from intro into the index (§2.1). */}
      <SectionDivider />

      {/* ---------- Filter + Grid (shuffled on every visit when "All") ---------- */}
      <div className="pb-32 sm:pb-40">
        <LivingFilter articles={projected} featuredSlugs={FEATURED_SLUGS} />
      </div>
    </main>
  );
}
