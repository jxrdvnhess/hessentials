"use client";

import { FormEvent, useState } from "react";

type Status = "idle" | "submitting" | "success" | "error";

const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

/**
 * Newsletter signup — single email field, editorial restraint.
 *
 * Posts to /api/newsletter, which is currently a stub. To wire to a real
 * ESP (Substack, Beehiiv, ConvertKit, Buttondown, Klaviyo), see the
 * comments in src/app/api/newsletter/route.ts.
 */
export default function NewsletterSignup() {
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

  return (
    <div className="mx-auto flex max-w-md flex-col items-center gap-y-5 text-center">
      <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px]">
        Newsletter
      </p>

      <p className="font-serif text-[15px] italic leading-[1.45] text-[#1f1d1b]/65 sm:text-[16px]">
        A note when there&rsquo;s something to say.
      </p>

      {status === "success" ? (
        <p className="mt-1 font-serif text-[15px] italic leading-[1.45] text-[#1f1d1b]/75 sm:text-[16px]">
          Thank you. We&rsquo;ll be in touch.
        </p>
      ) : (
        <form
          onSubmit={handleSubmit}
          className="mt-1 flex w-full items-baseline gap-3 border-b border-[#1f1d1b]/20 pb-2 transition-colors duration-300 ease-out focus-within:border-[#1f1d1b]/55"
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
            className="flex-1 bg-transparent py-1 text-[15px] leading-[1.4] text-[#1f1d1b] placeholder:text-[#1f1d1b]/35 focus:outline-none sm:text-[16px]"
            required
          />
          <button
            type="submit"
            disabled={status === "submitting"}
            aria-label="Subscribe"
            className="text-[12px] uppercase tracking-[0.26em] text-[#1f1d1b]/65 transition-colors duration-300 ease-out hover:text-[#1f1d1b] disabled:opacity-40"
          >
            {status === "submitting" ? "…" : "→"}
          </button>
        </form>
      )}

      {status === "error" && (
        <p className="text-[11px] uppercase tracking-[0.22em] text-[#1f1d1b]/45">
          Something didn&rsquo;t go through. Try again.
        </p>
      )}
    </div>
  );
}
