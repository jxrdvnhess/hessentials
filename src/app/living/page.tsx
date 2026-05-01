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

// Section is the canonical source of truth — read directly from each
// article's markdown frontmatter (`section: Systems | Environment |
// Rituals`). The article header and the index filter share the same
// value so a piece's eyebrow and its filter bucket can never drift.
// Articles without a section default to Systems.
const VALID_GROUPS: readonly LivingGroup[] = [
  "Systems",
  "Environment",
  "Rituals",
];

function asLivingGroup(value: string | undefined): LivingGroup {
  return VALID_GROUPS.includes(value as LivingGroup)
    ? (value as LivingGroup)
    : "Systems";
}

// Pillar pages treat all content equally — no curated subset is held
// up as the recommended entry point. The previous FEATURED_SLUGS const
// + Start Here rail was removed in the 2026-04-30 equal-treatment pass.
// Articles flow directly under the filter chips, in their natural
// (shuffled-on-mount) order.

export default async function LivingIndexPage() {
  const articles = await getAllLivingArticles();

  const projected: LivingIndexArticle[] = articles.map((article) => ({
    slug: article.slug,
    title: article.meta.title,
    excerpt: article.excerpt,
    group: asLivingGroup(article.meta.section),
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
        <LivingFilter articles={projected} />
      </div>
    </main>
  );
}
