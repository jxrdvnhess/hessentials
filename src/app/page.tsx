import { redirect } from "next/navigation";

/**
 * Root → /home.
 *
 * The previous wordmark + Enter splash gateway lived here; it's been
 * replaced by the cinematic splash morph that fires on /home itself
 * (first visit only, cookie-gated). `/` now collapses to the canonical
 * homepage URL.
 *
 * The next.config.ts redirect catches this at the edge before this
 * file ever runs; this file is a defense-in-depth fallback for any
 * direct invocation of the route handler.
 */
export default function RootPage() {
  redirect("/home");
}
