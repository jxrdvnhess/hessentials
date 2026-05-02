"use client";

/**
 * FooterGate — conditionally renders the public site footer.
 *
 * The admin surfaces under `/admin/*` are dev-only utilities for
 * editing shop data. The public footer (newsletter sign-up + the
 * "This is what stayed." closing) is editorial chrome that doesn't
 * belong on those pages — it adds visual noise and routes attention
 * away from the editing task.
 *
 * Implemented as a client wrapper so the root layout can stay a
 * server component. SiteFooter is already a client component, so
 * this adds no extra hydration cost.
 */

import { usePathname } from "next/navigation";
import SiteFooter from "./SiteFooter";

export default function FooterGate() {
  const pathname = usePathname();
  if (pathname?.startsWith("/admin")) return null;
  return <SiteFooter />;
}
