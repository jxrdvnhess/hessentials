"use client";

import { useEffect, useState } from "react";
import dailyIntents from "../data/dailyIntents.json";

type IntentsFile = {
  fallback: string;
  intents: Record<string, string>;
};

const data = dailyIntents as IntentsFile;

type Today = { date: string; intent: string };

function resolveToday(): Today {
  const now = new Date();
  const key = `${String(now.getMonth() + 1).padStart(2, "0")}-${String(
    now.getDate()
  ).padStart(2, "0")}`;
  const date = new Intl.DateTimeFormat("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  }).format(now);
  const intent = data.intents[key] ?? data.fallback;
  return { date, intent };
}

export default function DailyIntent() {
  // Date is resolved on the client so it reflects the visitor's local time,
  // not the server's. We render the fallback intent during SSR/hydration to
  // avoid layout shift, then settle on today's entry on mount.
  const [today, setToday] = useState<Today | null>(null);

  useEffect(() => {
    setToday(resolveToday());
  }, []);

  return (
    <div
      style={{ animationDelay: "3.1s" }}
      className="fade-up mx-auto mb-10 max-w-xl text-center sm:mb-12"
    >
      <p className="mb-4 text-[10px] uppercase tracking-[0.32em] text-[#1f1d1b]/55">
        {today ? `Daily intent · ${today.date}` : "Daily intent"}
      </p>
      <p className="font-serif text-[clamp(1.125rem,1.7vw,1.375rem)] italic leading-[1.55] text-[#1f1d1b]/70">
        {today?.intent ?? data.fallback}
      </p>
    </div>
  );
}
