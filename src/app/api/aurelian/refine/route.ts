import { NextRequest, NextResponse } from "next/server";
import {
  RECOGNITION_SYSTEM_PROMPT,
  buildRecognitionUserPrompt,
} from "../../../../lib/aurelianRecognition";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ANTHROPIC_URL = "https://api.anthropic.com/v1/messages";
const ANTHROPIC_VERSION = "2023-06-01";
const MODEL = "claude-sonnet-4-6";
const TIMEOUT_MS = 12_000;

type RefineRequest = {
  reading?: {
    pattern?: string;
    synthesis?: string;
    realLife?: string;
    watchPoint?: string;
    [key: string]: unknown;
  };
  signs?: {
    sun?: string;
    moon?: string;
    rising?: string;
  };
};

function extractJsonObject(raw: string): Record<string, unknown> | null {
  // Strip optional markdown fences and find the first JSON object literal.
  const fenced = raw.match(/```(?:json)?\s*([\s\S]*?)\s*```/);
  const candidate = fenced ? fenced[1] : raw;
  const objectMatch = candidate.match(/\{[\s\S]*\}/);
  if (!objectMatch) return null;
  try {
    return JSON.parse(objectMatch[0]);
  } catch {
    return null;
  }
}

export async function POST(req: NextRequest) {
  let body: RefineRequest;
  try {
    body = (await req.json()) as RefineRequest;
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const { reading, signs } = body;
  if (!reading || typeof reading !== "object") {
    return NextResponse.json({ error: "Missing reading" }, { status: 400 });
  }

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) {
    // No API key configured — return the reading unchanged so the UX is
    // identical with or without the refinement layer.
    return NextResponse.json({ reading, refined: false });
  }

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
        max_tokens: 2048,
        temperature: 0.4,
        system: RECOGNITION_SYSTEM_PROMPT,
        messages: [
          {
            role: "user",
            content: buildRecognitionUserPrompt(reading, signs ?? {}),
          },
        ],
      }),
      signal: controller.signal,
    });
    clearTimeout(timeout);

    if (!upstream.ok) {
      return NextResponse.json({ reading, refined: false });
    }

    const data = (await upstream.json()) as {
      content?: Array<{ type: string; text?: string }>;
    };
    const text = data.content?.find((c) => c.type === "text")?.text ?? "";
    const refined = extractJsonObject(text);
    if (!refined) {
      return NextResponse.json({ reading, refined: false });
    }

    const refinedReading = {
      ...reading,
      pattern:
        typeof refined.pattern === "string"
          ? refined.pattern
          : reading.pattern,
      synthesis:
        typeof refined.synthesis === "string"
          ? refined.synthesis
          : reading.synthesis,
      realLife:
        typeof refined.realLife === "string"
          ? refined.realLife
          : reading.realLife,
      watchPoint:
        typeof refined.watchPoint === "string"
          ? refined.watchPoint
          : reading.watchPoint,
    };

    return NextResponse.json({ reading: refinedReading, refined: true });
  } catch {
    clearTimeout(timeout);
    return NextResponse.json({ reading, refined: false });
  }
}
