"use client";

import { FormEvent, useState } from "react";

type Status = "idle" | "submitting" | "success" | "error";
type Variant = "default" | "light";

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

type NewsletterSignupProps = {
  /** "default" — ink on cream (footer band). "light" — cream on dark image (overlay usage). */
  variant?: Variant;
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
}: NewsletterSignupProps = {}) {
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
        A note when there&rsquo;s something to say.
      </p>

      {status === "success" ? (
        <p className={`mt-1 font-serif text-[15px] italic leading-[1.45] sm:text-[16px] ${successMsg}`}>
          Thank you. We&rsquo;ll be in touch.
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
