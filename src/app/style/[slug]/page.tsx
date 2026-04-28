import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import {
  STYLE_ARTICLES,
  getStyleArticleBySlug,
  type ShopItem,
  type StyleSection,
} from "../../../data/style";

type Params = { slug: string };

export function generateStaticParams() {
  return STYLE_ARTICLES.map((a) => ({ slug: a.slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug } = await params;
  const article = getStyleArticleBySlug(slug);
  if (!article) return {};
  return {
    title: `${article.title} — Hessentials`,
    description: article.dek,
  };
}

/* ---------- Section renderers ---------- */

function paragraphs(body: string): string[] {
  return body.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean);
}

function IntroSection({
  section,
}: {
  section: Extract<StyleSection, { type: "intro" }>;
}) {
  return (
    <section aria-label="Intro">
      <h2 className="mb-8 font-serif text-[clamp(1.5rem,2.6vw,1.875rem)] font-normal leading-[1.2] tracking-[-0.015em] text-balance">
        {section.heading}
      </h2>
      <div className="space-y-6 text-[18px] leading-[1.75] text-[#1f1d1b]/85">
        {paragraphs(section.body).map((p, i) => (
          <p key={i} className="text-pretty">
            {p}
          </p>
        ))}
      </div>
    </section>
  );
}

function EssaySection({
  section,
}: {
  section: Extract<StyleSection, { type: "essay" }>;
}) {
  return (
    <section aria-label="Essay">
      <h2 className="mb-8 font-serif text-[clamp(1.625rem,2.8vw,2rem)] font-normal leading-[1.2] tracking-[-0.02em] text-balance">
        {section.heading}
      </h2>
      <div className="space-y-6 text-[18px] leading-[1.75] text-[#1f1d1b]/85">
        {paragraphs(section.body).map((p, i) => (
          <p key={i} className="text-pretty">
            {p}
          </p>
        ))}
      </div>
    </section>
  );
}

function CalloutSection({
  section,
}: {
  section: Extract<StyleSection, { type: "callout" }>;
}) {
  return (
    <aside
      aria-label={section.label}
      className="mx-auto max-w-xl text-center"
    >
      <p className="mb-6 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/45 sm:text-[12px]">
        {section.label}
      </p>
      <p className="text-pretty font-serif text-[clamp(1.375rem,2.6vw,1.875rem)] italic leading-[1.45] text-[#1f1d1b]/85">
        {section.body}
      </p>
    </aside>
  );
}

function PracticalSection({
  section,
}: {
  section: Extract<StyleSection, { type: "practical" }>;
}) {
  return (
    <section aria-label={section.heading}>
      <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
        {section.heading}
      </p>
      <ol className="space-y-5 text-[17px] leading-[1.7] text-[#1f1d1b]/85 sm:text-[18px]">
        {section.items.map((item, i) => (
          <li
            key={i}
            className="grid grid-cols-[3rem_1fr] gap-x-4 sm:grid-cols-[3.5rem_1fr]"
          >
            <span className="pt-[0.2em] font-serif text-[15px] leading-none tracking-[-0.01em] text-[#1f1d1b]/40 sm:text-[16px]">
              {String(i + 1).padStart(2, "0")}
            </span>
            <span className="text-pretty">{item}</span>
          </li>
        ))}
      </ol>
    </section>
  );
}

function ShopItemRow({ item }: { item: ShopItem }) {
  const linkClass =
    "underline decoration-[#1f1d1b]/20 underline-offset-[5px] transition-colors hover:decoration-[#1f1d1b]/60";

  return (
    <div>
      <div className="mb-3 flex items-baseline justify-between gap-6">
        <h3 className="font-serif text-[clamp(1.125rem,1.8vw,1.375rem)] font-normal leading-[1.25] tracking-[-0.01em] text-[#1f1d1b]">
          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className={linkClass}
          >
            {item.name}
          </a>
        </h3>
        <span
          aria-label="Price range"
          className="shrink-0 font-serif text-[14px] tracking-[0.04em] text-[#1f1d1b]/55"
        >
          {item.priceRange}
        </span>
      </div>
      <p className="mb-3 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/55">
        {item.brand}
      </p>
      <p className="mb-3 text-pretty leading-[1.7] text-[#1f1d1b]/85">
        {item.reason}
      </p>
      <p className="text-[14px] italic leading-[1.65] text-[#1f1d1b]/55 sm:text-[15px]">
        Alternative —{" "}
        {item.altUrl ? (
          <a
            href={item.altUrl}
            target="_blank"
            rel="noopener noreferrer"
            className={linkClass}
          >
            {item.alt}
          </a>
        ) : (
          item.alt
        )}
      </p>
    </div>
  );
}

function ShopSection({
  section,
}: {
  section: Extract<StyleSection, { type: "shop" }>;
}) {
  return (
    <section aria-label={section.heading}>
      <p className="mb-3 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
        {section.heading}
      </p>
      <p className="mb-12 text-pretty font-serif text-[17px] italic leading-[1.6] text-[#1f1d1b]/65 sm:text-[18px]">
        {section.note}
      </p>
      <div className="space-y-12">
        {section.items.map((item, i) => (
          <div
            key={`${item.brand}-${item.name}-${i}`}
            className={
              i > 0
                ? "border-t border-[#1f1d1b]/15 pt-12"
                : ""
            }
          >
            <ShopItemRow item={item} />
          </div>
        ))}
      </div>
    </section>
  );
}

function EmDash() {
  return (
    <div
      aria-hidden
      className="my-20 text-center font-serif text-[18px] text-[#1f1d1b]/30 sm:my-24"
    >
      —
    </div>
  );
}

/* ---------- Page ---------- */

export default async function StyleArticlePage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  const article = getStyleArticleBySlug(slug);
  if (!article) notFound();

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        {/* ---------- Article header ---------- */}
        <header className="mb-20 text-center md:mb-28">
          <p className="mb-10 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
            {article.eyebrow}
          </p>

          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal leading-[1.04] tracking-[-0.025em] text-balance">
            {article.title}
          </h1>

          <p className="text-pretty mx-auto mt-8 max-w-xl font-serif text-[clamp(1.125rem,1.8vw,1.375rem)] italic leading-[1.5] text-[#1f1d1b]/70">
            {article.subtitle}
          </p>

          <p className="text-pretty mx-auto mt-8 max-w-xl text-[15px] leading-[1.65] text-[#1f1d1b]/60 sm:text-[16px]">
            {article.dek}
          </p>

          <p className="mt-10 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/45">
            By {article.author}
          </p>
        </header>

        {/* ---------- Body sections ---------- */}
        <div>
          {article.sections.map((section, i) => (
            <div key={`${section.type}-${i}`}>
              {i > 0 && <EmDash />}
              {section.type === "intro" && <IntroSection section={section} />}
              {section.type === "essay" && <EssaySection section={section} />}
              {section.type === "callout" && (
                <CalloutSection section={section} />
              )}
              {section.type === "practical" && (
                <PracticalSection section={section} />
              )}
              {section.type === "shop" && <ShopSection section={section} />}
            </div>
          ))}
        </div>

        {/* ---------- Tags ---------- */}
        {article.tags.length > 0 && (
          <footer className="mt-32 text-center md:mt-40">
            <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
              {article.tags.join(" · ")}
            </p>
          </footer>
        )}

        {/* ---------- Bottom — onward ---------- */}
        <nav
          aria-label="Continue reading"
          className="mx-auto mt-32 max-w-2xl text-center sm:mt-40 md:mt-48"
        >
          <Link
            href="/style"
            className="inline-flex items-baseline gap-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/80 sm:text-[11px]"
          >
            <span aria-hidden>←</span>
            Style
          </Link>
          <p className="mt-6 font-serif text-[15px] italic leading-[1.6] text-[#1f1d1b]/50 sm:text-[16px]">
            More worth wearing.
          </p>
        </nav>
      </article>
    </main>
  );
}
