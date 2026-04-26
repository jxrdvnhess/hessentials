import fs from "node:fs/promises";
import path from "node:path";
import type { Metadata } from "next";
import { parseFrontmatter, markdownToHtml } from "../../lib/living";

async function readAbout() {
  const filePath = path.join(process.cwd(), "content", "about.md");
  const source = await fs.readFile(filePath, "utf8");
  const { data, content } = parseFrontmatter(source);
  return {
    title: data.title || "About",
    html: markdownToHtml(content),
  };
}

export async function generateMetadata(): Promise<Metadata> {
  const { title } = await readAbout();
  return {
    title: `${title} — Hessentials`,
    description:
      "Hessentials is about choosing well — a curated system for living with more intention.",
  };
}

export default async function AboutPage() {
  const { title, html } = await readAbout();

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        <header className="mb-20 text-center md:mb-28">
          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal leading-[1.04] tracking-[-0.025em] text-balance">
            {title}
          </h1>
        </header>

        <div
          className="prose-editorial"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      </article>
    </main>
  );
}
