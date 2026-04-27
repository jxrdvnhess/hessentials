"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { STYLE_ARTICLES, type StyleArticle } from "../data/style";
import { shuffleArray } from "../lib/shuffle";

/**
 * Style index list.
 *
 * /style has no filter row — every visit is effectively the "All" view —
 * so we shuffle the article list on every page visit. Server-side render
 * keeps the declared order (deterministic, hydration-safe); the client
 * re-orders on first paint after mount.
 */
export default function StyleIndex() {
  const [articles, setArticles] = useState<StyleArticle[]>(STYLE_ARTICLES);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setArticles(shuffleArray(STYLE_ARTICLES));
  }, []);

  return (
    <ul className="grid grid-cols-1 gap-x-12 gap-y-16 sm:grid-cols-2 sm:gap-x-14 md:gap-x-20 md:gap-y-20">
      {articles.map((article) => (
        <li key={article.slug}>
          <Link
            href={`/style/${article.slug}`}
            className="group block transition-opacity duration-500 ease-out"
          >
            <h2 className="font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30">
              {article.title}
            </h2>

            <p className="text-pretty mt-4 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[17px]">
              {article.subtitle}
            </p>
          </Link>
        </li>
      ))}
    </ul>
  );
}
