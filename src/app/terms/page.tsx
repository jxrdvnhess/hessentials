import fs from "node:fs/promises";
import path from "node:path";
import type { Metadata } from "next";
import { parseFrontmatter, markdownToHtml } from "../../lib/living";

const SLUG = "terms";
const UPDATED = "April 2026";

async function readDoc() {
  const filePath = path.join(process.cwd(), "content", "legal", `${SLUG}.md`);
  const source = await fs.readFile(filePath, "utf8");
  const { data, content } = parseFrontmatter(source);
  return {
    title: data.title || "Terms",
    html: markdownToHtml(content),
  };
}

export async function generateMetadata(): Promise<Metadata> {
  const { title } = await readDoc();
  return {
    title: `${title} — Hessentials`,
    description: "The terms of using Hessentials — written plainly.",
  };
}

export default async function TermsPage() {
  const { title, html } = await readDoc();

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        <header className="mb-20 text-center md:mb-28">
          <p className="mb-6 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/45 sm:text-[12px]">
            Legal
          </p>
          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal leading-[1.04] tracking-[-0.025em] text-balance">
            {title}
          </h1>
          <p className="mt-6 font-serif text-[15px] italic text-[#1f1d1b]/50 sm:text-[16px]">
            Updated {UPDATED}
          </p>
        </header>

        <div
          className="prose-editorial"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      </article>
    </main>
  );
}
