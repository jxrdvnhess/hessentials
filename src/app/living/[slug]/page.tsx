import type { Metadata } from "next";
import Link from "next/link";
import { notFound } from "next/navigation";
import Byline from "../../../components/Byline";
import JsonLd from "../../../components/JsonLd";
import { articleSchema } from "../../../lib/jsonLd";
import {
  getAllLivingSlugs,
  getLivingArticleBySlug,
} from "../../../lib/living";

type Params = { slug: string };

export async function generateStaticParams() {
  const slugs = await getAllLivingSlugs();
  return slugs.map((slug) => ({ slug }));
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { slug } = await params;
  const article = await getLivingArticleBySlug(slug);
  if (!article) return {};

  return {
    title: `${article.meta.title} — Hessentials`,
    description: article.excerpt,
  };
}

export default async function LivingArticlePage({
  params,
}: {
  params: Promise<Params>;
}) {
  const { slug } = await params;
  const article = await getLivingArticleBySlug(slug);
  if (!article) notFound();

  const { meta, html } = article;
  const eyebrow = meta.section ? `Living — ${meta.section}` : "Living";

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Top — back link ----------
          Mirrors the Shop product detail return link. Pillar
          attribution is the source of truth. */}
      <div className="mx-auto w-full max-w-7xl px-6 pt-10 sm:px-10 md:px-16 md:pt-12">
        <Link
          href="/living"
          className="inline-flex items-baseline gap-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/80 sm:text-[11px]"
        >
          <span aria-hidden>←</span>
          Living
        </Link>
      </div>

      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        {/* ---------- Header ---------- */}
        <header className="mb-20 text-center md:mb-28">
          <p className="mb-10 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
            {eyebrow}
          </p>

          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal leading-[1.04] tracking-[-0.025em] text-balance">
            {meta.title}
          </h1>

          {meta.description && (
            <p className="text-pretty mx-auto mt-10 max-w-xl font-serif text-[clamp(1.125rem,1.6vw,1.3rem)] italic leading-[1.55] text-[#1f1d1b]/70">
              {meta.description}
            </p>
          )}

          {/* Top-of-article byline + date were removed per the
              Authorship brief — bylines belong at the end as a
              signature, not at the top as journalism-style attribution.
              See <Byline /> below. */}
        </header>

        {/* ---------- Body ---------- */}
        <div
          className="prose-editorial"
          dangerouslySetInnerHTML={{ __html: html }}
        />

        {/* Closing byline — sits just below the final paragraph,
            generous whitespace before the "Continue reading" nav. */}
        <Byline author={meta.byline} />

        {/* ---------- Bottom — onward ---------- */}
        <nav
          aria-label="Continue reading"
          className="mx-auto mt-32 max-w-2xl text-center sm:mt-40 md:mt-48"
        >
          <Link
            href="/living"
            className="inline-flex items-baseline gap-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/80 sm:text-[11px]"
          >
            <span aria-hidden>←</span>
            Living
          </Link>
          <p className="mt-6 font-serif text-[15px] italic leading-[1.6] text-[#1f1d1b]/50 sm:text-[16px]">
            More worth reading.
          </p>
        </nav>
      </article>

      {/* Article structured data — strengthens eligibility for Top
          Stories / article rich results, and gives Google a clean
          author + publisher + datePublished signal. */}
      <JsonLd
        data={articleSchema({
          url: `/living/${article.slug}`,
          headline: meta.title,
          description: meta.description ?? article.excerpt,
          datePublished: meta.date,
          byline: meta.byline,
        })}
      />
    </main>
  );
}
