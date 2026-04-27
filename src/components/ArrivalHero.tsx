"use client";

import { useEffect, useRef, useState } from "react";
import Wordmark from "./Wordmark";

export default function ArrivalHero() {
  const ref = useRef<HTMLElement>(null);
  const [revealed, setRevealed] = useState(false);

  useEffect(() => {
    const node = ref.current;
    if (!node) return;

    if (
      typeof window !== "undefined" &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    ) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setRevealed(true);
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setRevealed(true);
          observer.disconnect();
        }
      },
      { threshold: 0.25 }
    );

    observer.observe(node);
    return () => observer.disconnect();
  }, []);

  return (
    <section
      ref={ref}
      id="begin"
      aria-label="Arrival"
      className={[
        "arrival-hero relative grid min-h-[100vh] place-items-center overflow-hidden bg-[#f8f6f3]",
        revealed ? "is-revealed" : "",
      ].join(" ")}
    >
      <div
        aria-hidden="true"
        className="arrival-bg pointer-events-none absolute inset-0"
      />
      <div className="arrival-wordmark relative z-10 mb-[10vh]">
        <Wordmark size="hero" priority />
      </div>
    </section>
  );
}
