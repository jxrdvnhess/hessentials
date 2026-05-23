/**
 * Analytics — thin wrapper around the GA4 gtag() global injected by
 * @next/third-parties (see src/app/layout.tsx). Each helper is a no-op
 * when gtag isn't loaded — true on first paint, on the local dev box
 * without NEXT_PUBLIC_GA_ID set, and when an ad blocker swallows the
 * script. That keeps every call site free of "is gtag here yet?" gating.
 *
 * Event names are the contract. Don't rename without updating the GA4
 * property's Key Events (property a393214688p535310595).
 *
 *   newsletter_signup — fires on a successful newsletter POST.
 *                       Fired by both the footer form and the inline
 *                       homepage module. Submit-success only — never
 *                       focus, never form_start.
 *
 *   article_read      — fires once per page at 75% scroll depth on
 *                       Practice / Living / Style article templates.
 *                       Built-in enhanced-measurement only fires its
 *                       `scroll` event at 90%, so we run our own.
 *
 *   shop_click        — fires on click from a Currently card whose
 *                       URL points to /shop/*, or any other tracked
 *                       outbound Shop link. The before-and-after
 *                       metric for elevating Currently.
 */

type GtagFn = (
  command: "event" | "config" | "set",
  ...params: unknown[]
) => void;

declare global {
  interface Window {
    gtag?: GtagFn;
    dataLayer?: unknown[];
  }
}

function emit(event: string, params?: Record<string, unknown>): void {
  if (typeof window === "undefined") return;
  if (typeof window.gtag !== "function") return;
  try {
    if (params) {
      window.gtag("event", event, params);
    } else {
      window.gtag("event", event);
    }
  } catch {
    // Swallow — analytics should never break a user flow.
  }
}

export function trackNewsletterSignup(source: "footer" | "inline" | string): void {
  emit("newsletter_signup", { source });
}

export function trackArticleRead(params: {
  pillar: "living" | "style" | "practice";
  slug: string;
}): void {
  emit("article_read", params);
}

export function trackShopClick(params: {
  surface: "currently" | "shop_outbound" | string;
  destination?: string;
}): void {
  emit("shop_click", params);
}
