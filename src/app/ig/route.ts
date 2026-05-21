import { NextResponse } from "next/server";

/**
 * /ig → / with Instagram bio UTM tags.
 *
 * Why a route handler instead of a next.config.ts redirect:
 *   Next.js config-level redirects strip literal query params from
 *   the destination when the source has no params of its own
 *   (the destination's `?utm_source=...` got dropped on the way
 *   through). A route handler controls the Location header
 *   directly, so the UTMs survive.
 *
 * Why this exists at all:
 *   Instagram's bio link surfaces the raw URL when a profile has
 *   only one link, ignoring the custom "Title." A UTM-tagged URL
 *   reads as cluttered noise in that space ("hessentials.co?utm_source
 *   =instagram&utm_m..."). Redirecting through /ig keeps the bio
 *   link clean ("hessentials.co/ig") while still tagging the traffic
 *   server-side — so GA can distinguish bio taps from Story taps
 *   (utm_medium=bio vs utm_medium=story).
 *
 * Status:
 *   307 (temporary) rather than 308 so we can tweak the UTM params
 *   later without permanent browser caching working against us.
 */
export function GET(request: Request) {
  const destination = new URL(
    "/?utm_source=instagram&utm_medium=bio",
    request.url,
  );
  return NextResponse.redirect(destination, 307);
}
