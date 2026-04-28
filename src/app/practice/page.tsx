import type { Metadata } from "next";
import { getAllPracticeArticles } from "../../lib/practice";
import PracticeFilter, {
  type PracticeGroup,
  type PracticeIndexArticle,
} from "../../components/PracticeFilter";

export const metadata: Metadata = {
  title: "Practice — Hessentials",
  description:
    "Notes on the small returning things — what to do every day, what to do once a year, what to carry, what to ignore.",
};

/**
 * Editorial groupings keyed by article slug. The filter row narrows the
 * archive into the three buckets Practice sits in: Daily, Inner, Cyclical.
 * Articles without an explicit group default to Daily — review and add an
 * entry here when a new piece ships.
 */
const GROUPS: Record<string, PracticeGroup> = {
  // Daily — small, returnable, kept
  "practice-walking-is-not-slow-running": "Daily",
  "practice-compliment-one-person-every-day": "Daily",
  "practice-silence-five-minutes-no-app": "Daily",
  "practice-pick-one-stone-know-why": "Daily",
  "practice-the-single-object-you-carry": "Daily",
  // Inner — practices that work on the interior
  "practice-sound-baths-how-to-tell-which-ones-work": "Inner",
  "practice-1111-is-a-real-practice": "Inner",
  "practice-go-to-mass-occasionally": "Inner",
  "practice-tarot-isnt-prediction": "Inner",
  "practice-why-i-write-down-what-i-want": "Inner",
  // Cyclical — once a year, once a life
  "practice-the-annual-review-beats-resolutions": "Cyclical",
  "i-stopped-drinking-at-30": "Cyclical",
};

/**
 * Editor's pick — a deliberately mixed handful surfaced in a "Start Here"
 * rail above the main archive on the default ("All") view. One from each
 * bucket plus a fourth that sets the tone of the pillar. Update sparingly.
 */
const FEATURED_SLUGS = [
  "i-stopped-drinking-at-30",
  "practice-walking-is-not-slow-running",
  "practice-the-annual-review-beats-resolutions",
  "practice-1111-is-a-real-practice",
  "practice-why-i-write-down-what-i-want",
];

export default async function PracticeIndexPage() {
  const articles = await getAllPracticeArticles();

  const projected: PracticeIndexArticle[] = articles.map((article) => ({
    slug: article.slug,
    title: article.meta.title,
    excerpt: article.excerpt,
    group: GROUPS[article.slug] ?? "Daily",
  }));

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ---------- */}
      <section className="mx-auto w-full max-w-3xl px-6 pt-16 pb-12 text-center sm:px-10 md:pt-24">
        <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
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

      {/* ---------- Filter + Grid ---------- */}
      <div className="pb-32 sm:pb-40">
        <PracticeFilter articles={projected} featuredSlugs={FEATURED_SLUGS} />
      </div>
    </main>
  );
}
