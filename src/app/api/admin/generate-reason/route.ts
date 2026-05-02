/**
 * Generate a Hessentials shop reason line via the Anthropic API.
 *
 * POST /api/admin/generate-reason
 *   body: {
 *     name, brand, category, subcategory?, url
 *   }
 *
 * Re-fetches the source URL to get a fresh description (the page text
 * may have changed since the import preview), then calls Claude with
 * the voice rules system prompt. Returns:
 *
 *   { reason: string, refined: true }
 *
 * Soft fail: if no `ANTHROPIC_API_KEY` is configured, or the upstream
 * call fails, returns `{ reason: "", refined: false }` so the UI can
 * surface a quiet message rather than blowing up.
 *
 * Dev-only — 403 in production. The reason this isn't safe to expose
 * publicly is rate / cost: production users could spam it.
 */

import { NextRequest, NextResponse } from "next/server";
import { extractProduct } from "../../../../lib/shopImport/extract";
import {
  REASON_SYSTEM_PROMPT,
  buildReasonUserPrompt,
} from "../../../../lib/shopImport/voiceRules";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
const ANTHROPIC_VERSION = "2023-06-01";
/** Sonnet for voice fidelity. Switch to Haiku once the prompt is dialed. */
const MODEL = "claude-sonnet-4-6";
const TIMEOUT_MS = 15_000;

type GenerateBody = {
  name?: string;
  brand?: string;
  category?: string;
  subcategory?: string;
  url?: string;
  /** Optional override — when the form already has a description, skip the re-fetch. */
  description?: string;
};

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

/** Strip wrapping quotes / smart quotes / leading bullets. */
function tidy(raw: string): string {
  let out = raw.trim();
  // Drop leading "Reason:" or similar prefixes the model occasionally adds.
  out = out.replace(/^(reason|line|copy)\s*[:\-—]\s*/i, "");
  // Strip wrapping quotes (straight or smart).
  out = out.replace(/^["'“”‘’]+|["'“”‘’]+$/g, "");
  // Drop a leading bullet.
  out = out.replace(/^[-•*]\s+/, "");
  return out.trim();
}

export async function POST(req: NextRequest): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json({ error: "Not available" }, { status: 403 });
  }

  let body: GenerateBody;
  try {
    body = (await req.json()) as GenerateBody;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const name = (body.name ?? "").trim();
  const brand = (body.brand ?? "").trim();
  const category = (body.category ?? "").trim();
  const subcategory = (body.subcategory ?? "").trim();
  const url = (body.url ?? "").trim();

  if (!name || !brand || !category || !url) {
    return NextResponse.json(
      {
        error: "name, brand, category, and url are all required",
      },
      { status: 400 }
    );
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    return NextResponse.json({
      reason: "",
      refined: false,
      error:
        "ANTHROPIC_API_KEY is not set. Add it to .env.local and restart the dev server.",
    });
  }

  // Pull a fresh description from the source page unless the caller
  // supplied one (the import form already has it from the preview).
  let description = (body.description ?? "").trim();
  if (!description) {
    try {
      const extracted = await extractProduct(url);
      description = extracted.description;
    } catch {
      // Description is nice-to-have; the model can produce a workable
      // line from name + brand + category alone.
    }
  }

  const userPrompt = buildReasonUserPrompt({
    name,
    brand,
    category,
    subcategory: subcategory || undefined,
    description,
    url,
  });

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const upstream = await fetch(ANTHROPIC_URL, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-api-key": apiKey,
        "anthropic-version": ANTHROPIC_VERSION,
      },
      body: JSON.stringify({
        model: MODEL,
        max_tokens: 256,
        // Lower temperature keeps voice tight; the few-shot exemplars
        // do most of the steering.
        temperature: 0.5,
        system: REASON_SYSTEM_PROMPT,
        messages: [{ role: "user", content: userPrompt }],
      }),
      signal: controller.signal,
    });
    clearTimeout(timeout);

    if (!upstream.ok) {
      const errText = await upstream.text().catch(() => "");
      return NextResponse.json(
        {
          reason: "",
          refined: false,
          error: `Anthropic ${upstream.status}: ${errText.slice(0, 200)}`,
        },
        { status: 502 }
      );
    }

    const data = (await upstream.json()) as {
      content?: Array<{ type: string; text?: string }>;
    };
    const raw = data.content?.find((c) => c.type === "text")?.text ?? "";
    const reason = tidy(raw);
    if (!reason) {
      return NextResponse.json({
        reason: "",
        refined: false,
        error: "Empty response from model.",
      });
    }
    return NextResponse.json({ reason, refined: true });
  } catch (e) {
    clearTimeout(timeout);
    return NextResponse.json(
      {
        reason: "",
        refined: false,
        error: e instanceof Error ? e.message : String(e),
      },
      { status: 502 }
    );
  }
}
