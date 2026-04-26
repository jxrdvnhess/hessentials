import fs from "node:fs/promises";
import path from "node:path";

export type Frontmatter = {
  title: string;
  slug: string;
  category?: string;
  section?: string;
  description?: string;
  date?: string;
  byline?: string;
};

export type LivingArticle = {
  slug: string;
  meta: Frontmatter;
  /** First paragraph plain text — used on the index when no description is set. */
  excerpt: string;
  /** Rendered HTML body. */
  html: string;
};

const CONTENT_DIR = path.join(process.cwd(), "content/living");

/* ---------- Frontmatter ---------- */

export function parseFrontmatter(source: string): {
  data: Record<string, string>;
  content: string;
} {
  const match = source.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!match) return { data: {}, content: source };

  const [, frontmatter, content] = match;
  const data: Record<string, string> = {};

  for (const line of frontmatter.split(/\r?\n/)) {
    const colon = line.indexOf(":");
    if (colon === -1) continue;
    const key = line.slice(0, colon).trim();
    let value = line.slice(colon + 1).trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    data[key] = value;
  }

  return { data, content: content ?? "" };
}

/* ---------- Markdown → HTML ---------- */

function escapeHtml(s: string): string {
  const map: Record<string, string> = {
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;",
  };
  return s.replace(/[&<>"']/g, (c) => map[c]);
}

function renderInline(text: string): string {
  let out = escapeHtml(text);

  // Bold first (greedy enough for **a**, but won't eat across runs)
  out = out.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

  // Italic
  out = out.replace(/(^|[^*])\*([^*\n]+)\*(?!\*)/g, "$1<em>$2</em>");
  out = out.replace(/(^|[^_])_([^_\n]+)_(?!_)/g, "$1<em>$2</em>");

  // Inline code
  out = out.replace(/`([^`]+)`/g, "<code>$1</code>");

  // Links [text](url)
  out = out.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2">$1</a>');

  // Soft break: two trailing spaces + newline → <br />
  out = out.replace(/  \r?\n/g, "<br />\n");

  return out;
}

const isHr = (line: string) => /^[-*_]{3,}\s*$/.test(line.trim());
const isHeading = (line: string) => /^#{1,6}\s+/.test(line);
const isUlItem = (line: string) => /^\s*[-*+]\s+/.test(line);
const isOlItem = (line: string) => /^\s*\d+\.\s+/.test(line);

export function markdownToHtml(md: string): string {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const blocks: string[] = [];
  let i = 0;

  while (i < lines.length) {
    const line = lines[i];

    if (line.trim() === "") {
      i++;
      continue;
    }

    if (isHr(line)) {
      blocks.push("<hr />");
      i++;
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const content = renderInline(heading[2].trim());
      blocks.push(`<h${level}>${content}</h${level}>`);
      i++;
      continue;
    }

    if (isUlItem(line)) {
      const items: string[] = [];
      while (i < lines.length && isUlItem(lines[i])) {
        const itemText = lines[i].replace(/^\s*[-*+]\s+/, "");
        items.push(`<li>${renderInline(itemText)}</li>`);
        i++;
      }
      blocks.push(`<ul>\n${items.join("\n")}\n</ul>`);
      continue;
    }

    if (isOlItem(line)) {
      const items: string[] = [];
      while (i < lines.length && isOlItem(lines[i])) {
        const itemText = lines[i].replace(/^\s*\d+\.\s+/, "");
        items.push(`<li>${renderInline(itemText)}</li>`);
        i++;
      }
      blocks.push(`<ol>\n${items.join("\n")}\n</ol>`);
      continue;
    }

    // Paragraph: collect until blank line or block element
    const paraLines: string[] = [];
    while (
      i < lines.length &&
      lines[i].trim() !== "" &&
      !isHr(lines[i]) &&
      !isHeading(lines[i]) &&
      !isUlItem(lines[i]) &&
      !isOlItem(lines[i])
    ) {
      paraLines.push(lines[i]);
      i++;
    }
    if (paraLines.length) {
      blocks.push(`<p>${renderInline(paraLines.join("\n"))}</p>`);
    }
  }

  return blocks.join("\n\n");
}

/* ---------- Excerpt ---------- */

function firstParagraph(md: string): string {
  const lines = md.replace(/\r\n/g, "\n").split("\n");
  const para: string[] = [];

  for (const line of lines) {
    const t = line.trim();
    if (t === "") {
      if (para.length) break;
      continue;
    }
    if (isHr(t) || isHeading(line) || isUlItem(line) || isOlItem(line)) {
      if (para.length) break;
      continue;
    }
    para.push(line);
  }

  return para.join(" ").replace(/\s+/g, " ").trim();
}

/* ---------- Public API ---------- */

async function readArticle(filename: string): Promise<LivingArticle> {
  const fileSlug = filename.replace(/\.md$/, "");
  const filePath = path.join(CONTENT_DIR, filename);
  const source = await fs.readFile(filePath, "utf8");
  const { data, content } = parseFrontmatter(source);

  const meta: Frontmatter = {
    title: data.title || fileSlug,
    slug: data.slug || fileSlug,
    category: data.category,
    section: data.section,
    description: data.description,
    date: data.date,
    byline: data.byline,
  };

  return {
    slug: fileSlug,
    meta,
    excerpt: meta.description || firstParagraph(content),
    html: markdownToHtml(content),
  };
}

export async function getAllLivingSlugs(): Promise<string[]> {
  try {
    const entries = await fs.readdir(CONTENT_DIR);
    return entries
      .filter((f) => f.endsWith(".md"))
      .map((f) => f.replace(/\.md$/, ""));
  } catch {
    return [];
  }
}

export async function getAllLivingArticles(): Promise<LivingArticle[]> {
  try {
    const entries = await fs.readdir(CONTENT_DIR);
    const articles = await Promise.all(
      entries
        .filter((f) => f.endsWith(".md"))
        .map((filename) => readArticle(filename))
    );
    return articles.sort((a, b) => a.meta.title.localeCompare(b.meta.title));
  } catch {
    return [];
  }
}

export async function getLivingArticleBySlug(
  slug: string
): Promise<LivingArticle | undefined> {
  try {
    return await readArticle(`${slug}.md`);
  } catch {
    return undefined;
  }
}
