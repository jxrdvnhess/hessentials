import { execSync } from "node:child_process";
import path from "node:path";

/**
 * Article metadata helpers — build-time-only.
 *
 * Two responsibilities:
 *
 *   1. Surface a publish-date / modified-date pair for each markdown
 *      article. The brief calls for `datePublished` + `dateModified` on
 *      every Article schema. As of the May 22 launch push, no
 *      `content/living/*.md` or `content/practice/*.md` file carries a
 *      `date:` field in its frontmatter — adding one per article is an
 *      editorial pass. Until then, we fall back to git's record of when
 *      the file was first added (datePublished) and last modified
 *      (dateModified). Frontmatter, when set, wins.
 *
 *   2. Compose a meta description in the 120–160 character range. Some
 *      pieces carry an intentionally short editorial dek (e.g.
 *      "The number doesn't mean anything. The pause means everything."
 *      — 61 chars). That dek belongs at the top of the page, but for
 *      the search snippet we want a longer, fuller editorial line —
 *      typically the article's opening paragraph trimmed at a sentence
 *      boundary.
 *
 * All work happens at build time inside the Next.js server runtime
 * (`generateMetadata` is server-side; the data layer is too). Shelling
 * out to `git` is safe in Vercel's build environment.
 */

/* ---------- Git-derived dates ---------- */

/**
 * Cache results so each file is shelled out at most once per build.
 * The data layer reads the same article in two contexts (the page +
 * the schema), and `git log` is the most expensive call in this module.
 */
type DatePair = { published?: string; modified?: string };
const dateCache = new Map<string, DatePair>();

function safeGit(command: string): string | undefined {
  try {
    const out = execSync(command, {
      cwd: process.cwd(),
      stdio: ["ignore", "pipe", "ignore"],
      encoding: "utf8",
    }).trim();
    return out || undefined;
  } catch {
    // Not in a git context (e.g. tarball deploy), or the file isn't
    // tracked. Return undefined — the schema field stays absent rather
    // than reporting a wrong date.
    return undefined;
  }
}

/**
 * Quote a path so it survives any spaces or punctuation when handed to
 * `git log`. We don't accept arbitrary user input here, but the path
 * goes through a shell, so this is belt-and-suspenders.
 */
function shellQuote(value: string): string {
  return `'${value.replace(/'/g, `'\\''`)}'`;
}

/**
 * Git first-commit author date for `filePath`. Returns ISO 8601 (with
 * offset). `--diff-filter=A` is "added" — the original create commit.
 * `--follow` carries the lookup across renames so a slug change does
 * not lose the original publish date.
 */
function gitFirstCommitDate(filePath: string): string | undefined {
  const quoted = shellQuote(filePath);
  return safeGit(
    `git log --diff-filter=A --follow --format=%aI -- ${quoted} | tail -n 1`
  );
}

/**
 * Git most-recent author date for `filePath`. Used as `dateModified`.
 */
function gitLastCommitDate(filePath: string): string | undefined {
  const quoted = shellQuote(filePath);
  return safeGit(`git log -1 --format=%aI -- ${quoted}`);
}

/**
 * Resolve publish + modified dates for a markdown article. Frontmatter
 * wins; otherwise git fills the gap.
 */
export function resolveArticleDates({
  filePath,
  frontmatterDate,
  frontmatterUpdated,
}: {
  filePath: string;
  frontmatterDate?: string;
  frontmatterUpdated?: string;
}): DatePair {
  const cacheKey = path.resolve(filePath);
  const cached = dateCache.get(cacheKey);
  if (cached) {
    // Cache returns the git-derived pair; layer the frontmatter
    // overrides on top (in case different callers pass different
    // frontmatter — currently they don't, but cheap to be correct).
    return {
      published: frontmatterDate ?? cached.published,
      modified: frontmatterUpdated ?? cached.modified ?? frontmatterDate ?? cached.published,
    };
  }

  const gitPublished = gitFirstCommitDate(filePath);
  const gitModified = gitLastCommitDate(filePath);
  const pair: DatePair = {
    published: gitPublished,
    modified: gitModified,
  };
  dateCache.set(cacheKey, pair);

  return {
    published: frontmatterDate ?? pair.published,
    modified: frontmatterUpdated ?? pair.modified ?? frontmatterDate ?? pair.published,
  };
}

/* ---------- Meta description composer ---------- */

const META_TARGET_MIN = 120;
const META_TARGET_MAX = 165;

function squashWhitespace(s: string): string {
  return s.replace(/\s+/g, " ").trim();
}

/**
 * Trim a string to roughly META_TARGET_MAX characters, ending at the
 * last sentence boundary inside the window so the snippet reads as a
 * full thought rather than a mid-sentence cut.
 *
 * If the input fits inside the window already, returns it as-is.
 */
function trimToSentence(text: string, maxLen: number = META_TARGET_MAX): string {
  const cleaned = squashWhitespace(text);
  if (cleaned.length <= maxLen) return cleaned;

  // Look for sentence-ending punctuation followed by space or end,
  // within the first `maxLen` chars. Prefer the latest one that lands
  // inside the window — gives the fullest sentence that still fits.
  const window = cleaned.slice(0, maxLen + 1);
  const sentenceEnd = window.match(/.*[.!?](?=\s|$)/);
  if (sentenceEnd) return sentenceEnd[0].trim();

  // No sentence break inside the window — cut at the last word boundary
  // and append an ellipsis. Better than cutting mid-word.
  const lastSpace = cleaned.lastIndexOf(" ", maxLen);
  const safeCut = lastSpace > 0 ? lastSpace : maxLen;
  return cleaned.slice(0, safeCut).trim() + "…";
}

/**
 * Build a meta description from the candidate strings supplied. Returns
 * the first candidate that lands in 120–165 chars after sentence-trim,
 * otherwise the trimmed version of whichever candidate gives the best
 * fit. Empty / missing candidates are skipped.
 *
 * Caller order is the editorial preference order — pass the values
 * most appropriate as a snippet first. For an article: explicit
 * description, then opening / standfirst, then body first paragraph.
 *
 * Per the May 22 brief, a meta description that is too short reads as
 * an auto-truncated title placeholder. This composer's job is to make
 * sure that does not happen on any template.
 */
export function buildMetaDescription(
  ...candidates: Array<string | undefined>
): string | undefined {
  // First pass: any candidate that already lives in the target window
  // is taken as-is — these are the writer's intentional editorial
  // lengths.
  for (const c of candidates) {
    if (!c) continue;
    const cleaned = squashWhitespace(c);
    if (cleaned.length >= META_TARGET_MIN && cleaned.length <= META_TARGET_MAX) {
      return cleaned;
    }
  }

  // Second pass: any candidate longer than the target — trim it to a
  // sentence boundary inside the window.
  for (const c of candidates) {
    if (!c) continue;
    const cleaned = squashWhitespace(c);
    if (cleaned.length > META_TARGET_MAX) {
      return trimToSentence(cleaned);
    }
  }

  // Fall-through: no candidate hits the window. Pick the longest
  // non-empty candidate — better an honest short editorial line than a
  // padded one.
  let best: string | undefined;
  for (const c of candidates) {
    if (!c) continue;
    const cleaned = squashWhitespace(c);
    if (!best || cleaned.length > best.length) best = cleaned;
  }
  return best;
}

/**
 * Pull the first plain-text paragraph out of a markdown source. Strips
 * frontmatter, ATX headings, list markers, and HR rules. Used by
 * articles whose `description` frontmatter is shorter than ideal for a
 * search snippet — the opening paragraph is editorial copy too, and
 * usually carries the right register and length.
 */
export function firstParagraphOf(markdown: string): string {
  // Drop frontmatter block if still present.
  const body = markdown.replace(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/, "");
  const lines = body.replace(/\r\n/g, "\n").split("\n");
  const para: string[] = [];

  for (const line of lines) {
    const t = line.trim();
    if (t === "") {
      if (para.length) break;
      continue;
    }
    if (/^#{1,6}\s+/.test(t)) {
      if (para.length) break;
      continue;
    }
    if (/^[-*_]{3,}\s*$/.test(t)) {
      if (para.length) break;
      continue;
    }
    if (/^\s*[-*+]\s+/.test(line) || /^\s*\d+\.\s+/.test(line)) {
      if (para.length) break;
      continue;
    }
    para.push(line);
  }

  return squashWhitespace(para.join(" "));
}
