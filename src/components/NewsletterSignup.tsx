"use client";

import { FormEvent, useState } from "react";
import { usePathname } from "next/navigation";
import { trackNewsletterSignup } from "../lib/analytics";

type Status = "idle" | "submitting" | "success" | "error";
type Variant = "default" | "light";

/**
 * Pillar key controls the tagline copy. "default" carries the site-wide
 * line (used on /, fallback routes, and anywhere the inference rule
 * doesn't match). Everything else swaps in pillar-specific editorial
 * copy. The component infers this from the current pathname when no
 * `pillar` prop is provided, so route changes update the tagline
 * automatically. Pass the prop explicitly to force a tagline (e.g. for
 * previews).
 *
 * Aurelian's line is in his own register (no "Sent when…" closer) —
 * the persona writes differently from the Hessentials house voice.
 */
type Pillar =
  | "default"
  | "recipes"
  | "living"
  | "style"
  | "practice"
  | "shop"
  | "aurelian"
  | "about";

const PILLAR_TAGLINES: Record<Pillar, string> = {
  default:
    "What stayed. What didn’t. The reasoning behind it. Sent when it’s worth a note.",
  recipes:
    "Recipes I keep making, what to skip, the upgrades that hold up. Sent when it’s worth it.",
  living:
    "Rooms, routines, and the difference between feeling good and being good. Sent when something earns it.",
  style:
    "What stays in rotation. What doesn’t. Sent when something deserves the hanger.",
  practice:
    "Practice without doctrine. Without ‘manifest.’ Sent when something works.",
  shop:
    "Pieces that earned their place. The edits I keep coming back to. Sent when something’s worth keeping.",
  aurelian:
    "From Aurelian. When the pattern is worth naming.",
  about:
    "Hessentials, when it’s ready. Sent when there’s something to show.",
};

/** Map a pathname to its pillar key. Falls through to "default" for
 *  routes that don't match a specific pillar (homepage, legal pages,
 *  error pages, anything else). */
function pillarFromPath(pathname: string | null): Pillar {
  if (!pathname) return "default";
  if (pathname === "/shop" || pathname.startsWith("/shop/")) return "shop";
  if (pathname === "/recipes" || pathname.startsWith("/recipes/")) return "recipes";
  if (pathname === "/living" || pathname.startsWith("/living/")) return "living";
  if (pathname === "/style" || pathname.startsWith("/style/")) return "style";
  if (pathname === "/practice" || pathname.startsWith("/practice/")) return "practice";
  if (pathname === "/aurelian" || pathname.startsWith("/aurelian/")) return "aurelian";
  if (pathname === "/about" || pathname.startsWith("/about/")) return "about";
  return "default";
}

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

type NewsletterSignupProps = {
  /** "default" — ink on cream (footer band). "light" — cream on dark image (overlay usage). */
  variant?: Variant;
  /**
   * Optional pillar override. When omitted, the component infers from
   * the current pathname. Pass this when the footer is rendered above
   * a route the inference rule doesn't cover.
   */
  pillar?: Pillar;
  /**
   * Analytics surface label — passed to the `newsletter_signup` event
   * on successful submit so we can distinguish the inline homepage
   * module from the footer instance in GA4. Defaults to "footer"
   * because that's the older, more common placement.
   */
  source?: "footer" | "inline" | string;
};

/**
 * Newsletter signup — single email field, editorial restraint.
 *
 * Posts to /api/newsletter, which is currently a stub. To wire to a real
 * ESP (Substack, Beehiiv, ConvertKit, Buttondown, Klaviyo), see the
 * comments in src/app/api/newsletter/route.ts.
 */
export default function NewsletterSignup({
  variant = "default",
  pillar,
  source = "footer",
}: NewsletterSignupProps = {}) {
  const pathname = usePathname();
  const resolvedPillar: Pillar = pillar ?? pillarFromPath(pathname);
  const tagline_copy = PILLAR_TAGLINES[resolvedPillar];
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<Status>("idle");

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!EMAIL_RE.test(email.trim())) {
      setStatus("error");
      return;
    }

    setStatus("submitting");
    try {
      const response = await fetch("/api/newsletter", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });

      if (response.ok) {
        setStatus("success");
        setEmail("");
        // Fire newsletter_signup on submit-success only (never on focus
        // or form_start). source distinguishes the inline homepage
        // module from the footer instance in GA4. Marked as a Key
        // Event in property a393214688p535310595.
        trackNewsletterSignup(source);
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  };

  const light = variant === "light";

  // Light variant uses cream tones at the same opacity values so the
  // overlay reads against a darkened image with the same hierarchy.
  const eyebrow = light
    ? "text-[#f8f6f3]/65"
    : "text-[#1f1d1b]/55";
  const tagline = light
    ? "text-[#f8f6f3]/70"
    : "text-[#1f1d1b]/65";
  const successMsg = light
    ? "text-[#f8f6f3]/85"
    : "text-[#1f1d1b]/75";
  const formBorder = light
    ? "border-[#f8f6f3]/30 focus-within:border-[#f8f6f3]/65"
    : "border-[#1f1d1b]/20 focus-within:border-[#1f1d1b]/55";
  const inputColor = light
    ? "text-[#f8f6f3] placeholder:text-[#f8f6f3]/45"
    : "text-[#1f1d1b] placeholder:text-[#1f1d1b]/35";
  const buttonColor = light
    ? "text-[#f8f6f3]/70 hover:text-[#f8f6f3]"
    : "text-[#1f1d1b]/65 hover:text-[#1f1d1b]";
  const errorMsg = light
    ? "text-[#f8f6f3]/55"
    : "text-[#1f1d1b]/45";

  return (
    <div className="mx-auto flex max-w-md flex-col items-center gap-y-5 text-center">
      <p className={`text-[11px] uppercase tracking-[0.28em] sm:text-[12px] ${eyebrow}`}>
        Newsletter
      </p>

      <p className={`font-serif text-[15px] italic leading-[1.45] sm:text-[16px] ${tagline}`}>
        {tagline_copy}
      </p>

      {status === "success" ? (
        <p className={`mt-1 font-serif text-[15px] italic leading-[1.45] sm:text-[16px] ${successMsg}`}>
          You&rsquo;re in. Next note lands when there&rsquo;s something to say.
        </p>
      ) : (
        <form
          onSubmit={handleSubmit}
          className={`mt-1 flex w-full items-baseline gap-3 border-b pb-2 transition-colors duration-300 ease-out ${formBorder}`}
        >
          <label htmlFor="newsletter-email" className="sr-only">
            Email address
          </label>
          <input
            id="newsletter-email"
            type="email"
            autoComplete="email"
            inputMode="email"
            placeholder="email address"
            value={email}
            onChange={(e) => {
              setEmail(e.target.value);
              if (status === "error") setStatus("idle");
            }}
            disabled={status === "submitting"}
            className={`flex-1 bg-transparent py-1 text-[15px] leading-[1.4] focus:outline-none sm:text-[16px] ${inputColor}`}
            required
          />
          <button
            type="submit"
            disabled={status === "submitting"}
            aria-label="Subscribe"
            className={`text-[12px] uppercase tracking-[0.26em] transition-colors duration-300 ease-out disabled:opacity-40 ${buttonColor}`}
          >
            {status === "submitting" ? "…" : "→"}
          </button>
        </form>
      )}

      {status === "error" && (
        <p className={`text-[11px] uppercase tracking-[0.22em] ${errorMsg}`}>
          Something didn&rsquo;t go through. Try again.
        </p>
      )}
    </div>
  );
}
