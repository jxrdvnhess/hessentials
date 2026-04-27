import type { MetadataRoute } from "next";

/**
 * Build-time robots.txt generator. Served by Next.js at /robots.txt.
 *
 * Allows everything by default, with two exceptions:
 *   - /api/ — server endpoints (newsletter signup, aurelian refine).
 *     There's nothing crawlable here, just JSON. No reason for bots to
 *     hit it; disallowing keeps logs cleaner.
 *   - /_next/ — Next.js internal build assets.
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: ["/api/", "/_next/"],
      },
    ],
    sitemap: "https://hessentials.co/sitemap.xml",
    host: "https://hessentials.co",
  };
}
