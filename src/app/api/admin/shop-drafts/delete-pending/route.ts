/**
 * Shop drafts — permanently remove a pending row.
 *
 * POST /api/admin/shop-drafts/delete-pending
 *   body: { directUrl: string }
 *
 * Removes the entry from `data/shop-import-pending.json` outright. Use
 * when an editorial decision rules a row out for good — the product
 * doesn't ship to the US, the brand has closed, the URL is dead, etc.
 *
 * This is distinct from `stage-pending` (which promotes the row to a
 * staged draft) and `rescrape-pending` (which leaves it pending). Once
 * deleted, a row only comes back if the bulk import script re-stages
 * it from the source CSV.
 *
 * Dev-only. Returns 403 in production.
 */

import fs from "node:fs/promises";
import path from "node:path";
import { NextRequest, NextResponse } from "next/server";

export const dynamic = "force-dynamic";

const PENDING_FILE = path.join(
  process.cwd(),
  "data",
  "shop-import-pending.json"
);

type PendingEntry = {
  directUrl: string;
  candidate?: { name?: string; brand?: string };
  [key: string]: unknown;
};

type PendingFile = { entries: PendingEntry[] };

async function readPending(): Promise<PendingFile> {
  try {
    const raw = await fs.readFile(PENDING_FILE, "utf8");
    return JSON.parse(raw) as PendingFile;
  } catch {
    return { entries: [] };
  }
}

async function writePending(data: PendingFile): Promise<void> {
  await fs.mkdir(path.dirname(PENDING_FILE), { recursive: true });
  await fs.writeFile(
    PENDING_FILE,
    JSON.stringify(data, null, 2) + "\n",
    "utf8"
  );
}

function isProd(): boolean {
  return process.env.NODE_ENV === "production";
}

export async function POST(req: NextRequest): Promise<NextResponse> {
  if (isProd()) {
    return NextResponse.json(
      { error: "Not available in production" },
      { status: 403 }
    );
  }

  let body: { directUrl?: string };
  try {
    body = (await req.json()) as { directUrl?: string };
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const directUrl = (body.directUrl ?? "").trim();
  if (!directUrl) {
    return NextResponse.json(
      { error: "directUrl is required" },
      { status: 400 }
    );
  }

  const pending = await readPending();
  const idx = pending.entries.findIndex((e) => e.directUrl === directUrl);
  if (idx < 0) {
    // Idempotent — already gone is success.
    return NextResponse.json({ ok: true, removed: 0 });
  }

  const [removed] = pending.entries.splice(idx, 1);
  await writePending(pending);

  return NextResponse.json({
    ok: true,
    removed: 1,
    directUrl,
    name: removed?.candidate?.name,
    brand: removed?.candidate?.brand,
  });
}
