import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * The pause gate.
 *
 * While PAUSED is true, every public route is REWRITTEN (not redirected)
 * to /paused. The rewrite matters: the visitor's URL stays exactly what
 * they asked for, so a shared link to /recipes/caprese-chicken is still
 * that link the day the gate comes down. No redirect chains to unwind, no
 * canonical damage, nothing to clean up later.
 *
 * To take the site out of pause: set PAUSED to false below (or delete this
 * file and src/app/paused/). Nothing else in the app knows this exists.
 *
 * ── Getting in while it's closed ────────────────────────────────────────
 *   Visit  https://hessentials.co/?open=this-is-what-stayed
 *   once. That sets a cookie and the browser is let through from then on,
 *   on every route, for 30 days. There's no password screen and no visible
 *   affordance: a wrong or absent phrase just sees the sign.
 *
 *   To lock yourself back out (to check what the public sees, without an
 *   incognito window):  /?open=off
 *
 * ── What is NOT gated ───────────────────────────────────────────────────
 *   The matcher below excludes Next's build assets and image optimizer,
 *   plus anything with a file extension in /public (the wordmark PNGs the
 *   sign itself needs, favicons, og-image). Everything else — pages, API
 *   routes, /admin — sits behind the gate.
 */

const PAUSED = true;

/** The phrase that opens the door. Change it and the old link stops working. */
const BYPASS_PHRASE = "this-is-what-stayed";

const BYPASS_COOKIE = "hs_open";
/** Read by src/app/layout.tsx to render the sign without site chrome.
 *  Kept un-exported: Next only expects `middleware` and `config` here. */
const PAUSED_HEADER = "x-hs-paused";
const THIRTY_DAYS = 60 * 60 * 24 * 30;

export function middleware(request: NextRequest) {
  if (!PAUSED) return NextResponse.next();

  const { searchParams, pathname } = request.nextUrl;
  const open = searchParams.get("open");

  // Lock back out — clears the cookie, then shows the sign like anyone else.
  if (open === "off") {
    const response = showSign(request);
    response.cookies.delete(BYPASS_COOKIE);
    return response;
  }

  // The secret link. Strip the query and send the visitor on to the real
  // page so the phrase doesn't linger in the address bar or in analytics.
  if (open === BYPASS_PHRASE) {
    const clean = request.nextUrl.clone();
    clean.searchParams.delete("open");
    const response = NextResponse.redirect(clean);
    response.cookies.set(BYPASS_COOKIE, "1", {
      maxAge: THIRTY_DAYS,
      httpOnly: true,
      sameSite: "lax",
      secure: process.env.NODE_ENV === "production",
      path: "/",
    });
    return response;
  }

  // Already let in.
  if (request.cookies.get(BYPASS_COOKIE)?.value === "1") {
    return NextResponse.next();
  }

  // The sign itself must render, or the rewrite loops.
  if (pathname === "/paused") return NextResponse.next();

  return showSign(request);
}

/**
 * Rewrite to the sign, stamping PAUSED_HEADER on the request so the root
 * layout knows to drop the header, shop sub-nav and footer. The chrome is
 * suppressed server-side rather than by pathname, because a rewrite is
 * invisible to the client router — usePathname() still reports /recipes.
 */
function showSign(request: NextRequest) {
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set(PAUSED_HEADER, "1");
  return NextResponse.rewrite(new URL("/paused", request.url), {
    request: { headers: requestHeaders },
  });
}

export const config = {
  matcher: [
    /**
     * Everything except:
     *   _next/static, _next/image  — build output and the image optimizer
     *   *.<ext>                    — files served straight out of /public
     *                                (wordmark, favicons, og-image)
     */
    "/((?!_next/static|_next/image|.*\\.[\\w]+$).*)",
  ],
};
