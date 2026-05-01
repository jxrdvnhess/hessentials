import type { Metadata } from "next";
import { getAllPracticeArticles } from "../../lib/practice";
import PracticeFilter, {
  type PracticeGroup,
  type PracticeIndexArticle,
} from "../../components/PracticeFilter";
import SectionDivider from "../../components/SectionDivider";

export const metadata: Metadata = {
  title: "Practice — Hessentials",
  description:
    "Notes on the small returning things — what to do every day, what to do once a year, what to carry, what to ignore.",
};

// Section is the canonical source of truth — read directly from each
// article's markdown frontmatter (`section: Daily | Inner | Cyclical`).
// The article header and the index filter share the same value so a
// piece's eyebrow and its filter bucket can never drift. Articles
// without a section default to Daily.
const VALID_GROUPS: readonly PracticeGroup[] = [
  "Daily",
  "Inner",
  "Cyclical",
];

function asPracticeGroup(value: string | undefined): PracticeGroup {
  return VALID_GROUPS.includes(value as PracticeGroup)
    ? (value as PracticeGroup)
    : "Daily";
}

// Pillar pages treat all content equally — no curated subset is held
// up as the recommended entry point. The previous FEATURED_SLUGS const
// + Start Here rail was removed in the 2026-04-30 equal-treatment pass.
// Articles flow directly under the filter chips, in their natural
// (shuffled-on-mount) order.

export default async function PracticeIndexPage() {
  const articles = await getAllPracticeArticles();

  const projected: PracticeIndexArticle[] = articles.map((article) => ({
    slug: article.slug,
    title: article.meta.title,
    excerpt: article.excerpt,
    group: asPracticeGroup(article.meta.section),
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
          Practice
        </p>
        <p className="text-pretty mx-auto max-w-2xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] italic leading-[1.4] text-[#1f1d1b]/80">
          The small returning things are the ones that hold the life.
        </p>
        <p className="text-pretty mx-auto mt-6 max-w-xl font-serif text-[15px] leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
          What to do every day. What to do once a year. What to carry. What
          to ignore.
        </p>
      </section>

      {/* "h" motif transitioning from intro into the index (§2.1). */}
      <SectionDivider />

      {/* ---------- Filter + Grid ---------- */}
      <div className="pb-32 sm:pb-40">
        <PracticeFilter articles={projected} />
      </div>
    </main>
  );
}
