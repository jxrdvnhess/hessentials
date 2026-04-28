import Link from "next/link";
import { STYLE_ARTICLES, type StyleArticle } from "../data/style";
import SectionDivider from "./SectionDivider";

/**
 * Style index.
 *
 * The /style page is no longer a single shuffled grid. It now leads
 * with a curated "Start Here" set, then groups the remaining articles
 * into quiet thematic sections so the page reads as a system rather
 * than a list. Order is intentional — no shuffle.
 */

const START_HERE_SLUGS = [
  "the-5-piece-rule",
  "casual-is-not-a-free-pass",
  "the-signature-piece",
  "the-anti-trend-rule",
  "its-usually-the-small-things",
];

const GROUPS: { label: string; slugs: string[] }[] = [
  {
    label: "Getting Dressed",
    slugs: [
      "the-uniform-is-not-boring",
      "texture-is-the-outfit",
      "style-is-not-gendered",
    ],
  },
  {
    label: "Personal Signals",
    slugs: ["the-scent-people-remember", "the-bag-sets-the-tone"],
  },
  {
    label: "Home as Extension",
    slugs: [
      "the-entryway-test",
      "your-home-has-an-outfit-too",
      "people-can-feel-when-its-forced",
      "the-dinner-plate-is-a-style-object",
    ],
  },
];

/**
 * Light guidance tags. Applied sparingly — never to every article,
 * never competing with titles. A small scanning aid, nothing more.
 */
const TAGS: Record<string, string> = {
  "texture-is-the-outfit": "Daily default",
  "the-scent-people-remember": "Upgrade",
  "the-entryway-test": "Foundational",
};

const ARTICLES_BY_SLUG: Record<string, StyleArticle> = STYLE_ARTICLES.reduce(
  (acc, article) => {
    acc[article.slug] = article;
    return acc;
  },
  {} as Record<string, StyleArticle>
);

function ArticleCard({ article }: { article: StyleArticle }) {
  const tag = TAGS[article.slug];
  return (
    <li>
      <Link
        href={`/style/${article.slug}`}
        className="group block transition-opacity duration-500 ease-out"
      >
        {tag && (
          <span className="mb-3 block text-[10px] uppercase tracking-[0.24em] text-[#1f1d1b]/40">
            {tag}
          </span>
        )}
        <h2 className="font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30">
          {article.title}
        </h2>
        <p className="text-pretty mt-4 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[17px]">
          {article.subtitle}
        </p>
      </Link>
    </li>
  );
}

function ArticleGrid({ articles }: { articles: StyleArticle[] }) {
  // Tighter column gap (§2.4) + row hairlines on sm+ between rows.
  const cols = 2;
  return (
    <ul className="grid grid-cols-1 gap-x-10 gap-y-16 sm:grid-cols-2 sm:gap-x-12 md:gap-x-14 md:gap-y-20">
      {articles.flatMap((article, idx) => {
        const els = [];
        if (idx > 0 && idx % cols === 0) {
          els.push(
            <li
              key={`hr-${article.slug}`}
              aria-hidden
              className="hidden sm:col-span-2 sm:block"
            >
              <span
                className="block w-full"
                style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
              />
            </li>
          );
        }
        els.push(<ArticleCard key={article.slug} article={article} />);
        return els;
      })}
    </ul>
  );
}

export default function StyleIndex() {
  const startHere = START_HERE_SLUGS.map(
    (slug) => ARTICLES_BY_SLUG[slug]
  ).filter(Boolean);

  return (
    <div>
      {/* ---------- Start Here ---------- */}
      <section>
        <header className="mb-12 flex flex-col items-start md:mb-16">
          {/* Hairline above the eyebrow (§2.2). */}
          <span
            aria-hidden
            className="block w-20"
            style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
          />
          <p className="mt-5 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
            Start Here
          </p>
          <h2 className="text-balance mt-5 font-serif text-[clamp(1.5rem,2.4vw,1.875rem)] font-normal leading-[1.2] tracking-[-0.015em] text-[#1f1d1b]">
            The rules that change everything first.
          </h2>
          <p className="text-pretty mt-3 max-w-xl font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/60 sm:text-[17px]">
            If nothing else, start with these.
          </p>
        </header>
        <ArticleGrid articles={startHere} />
      </section>

      {/* ---------- Grouped sections ---------- */}
      {GROUPS.map((group) => {
        const articles = group.slugs
          .map((slug) => ARTICLES_BY_SLUG[slug])
          .filter(Boolean);
        if (articles.length === 0) return null;
        return (
          <section key={group.label}>
            {/* "h" motif marks the transition between groups (§2.1). */}
            <SectionDivider />
            <header className="mb-10 flex flex-col items-start md:mb-14">
              <span
                aria-hidden
                className="block w-20"
                style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
              />
              <p className="mt-5 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
                {group.label}
              </p>
            </header>
            <ArticleGrid articles={articles} />
          </section>
        );
      })}
    </div>
  );
}
