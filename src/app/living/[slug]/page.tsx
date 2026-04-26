import type { Metadata } from "next";
import { notFound } from "next/navigation";
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

          {(meta.byline || meta.date) && (
            <p className="mt-10 text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/45">
              {[meta.byline, meta.date].filter(Boolean).join("  ·  ")}
            </p>
          )}
        </header>

        {/* ---------- Body ---------- */}
        <div
          className="prose-editorial"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      </article>
    </main>
  );
}
