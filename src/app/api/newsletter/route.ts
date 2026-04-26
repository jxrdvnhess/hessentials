import { NextResponse } from "next/server";

/**
 * Newsletter signup endpoint — Buttondown.
 *
 * Reads BUTTONDOWN_API_KEY from environment. Posts the email to
 * Buttondown's v1 subscribers endpoint and translates their response
 * into a clean ok / error contract for the front-end form.
 *
 * Behavior:
 *   - 201 Created           → ok
 *   - already subscribed    → ok (we don't out the user)
 *   - 400 invalid email     → 400
 *   - missing API key       → 500 (logged, not exposed)
 *   - any other failure     → 500
 */

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const BUTTONDOWN_ENDPOINT = "https://api.buttondown.email/v1/subscribers";

export async function POST(request: Request) {
  try {
    const body = (await request.json()) as { email?: unknown };
    const email =
      typeof body?.email === "string" ? body.email.trim().toLowerCase() : "";

    if (!email || !EMAIL_RE.test(email)) {
      return NextResponse.json({ error: "Invalid email" }, { status: 400 });
    }

    const apiKey = process.env.BUTTONDOWN_API_KEY;
    if (!apiKey) {
      console.error("[newsletter] BUTTONDOWN_API_KEY is not set");
      return NextResponse.json({ error: "Server error" }, { status: 500 });
    }

    const response = await fetch(BUTTONDOWN_ENDPOINT, {
      method: "POST",
      headers: {
        "content-type": "application/json",
        Authorization: `Token ${apiKey}`,
      },
      body: JSON.stringify({ email_address: email }),
    });

    if (response.ok) {
      return NextResponse.json({ ok: true });
    }

    // Buttondown returns 400 with an error code when the email already
    // exists. Treat that as success — the subscriber doesn't need to
    // know they were already on the list, and re-subscribing is a no-op.
    const text = await response.text().catch(() => "");
    const alreadyExists =
      response.status === 400 &&
      /already.*subscribed|already.*exists|duplicate/i.test(text);

    if (alreadyExists) {
      return NextResponse.json({ ok: true });
    }

    if (response.status === 400) {
      return NextResponse.json(
        { error: "Invalid email" },
        { status: 400 }
      );
    }

    console.error(
      "[newsletter] Buttondown error",
      response.status,
      text.slice(0, 300)
    );
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  } catch (err) {
    console.error("[newsletter] unhandled", err);
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  }
}
