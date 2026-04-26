"use client";

import { useEffect, useRef, useState } from "react";
import type { Ingredient } from "../types/recipe";

type CopyShoppingListProps = {
  title: string;
  ingredients: Ingredient[];
  className?: string;
};

function formatShoppingList(title: string, ingredients: Ingredient[]) {
  const lines = ingredients.map((ing) => {
    const measure = ing.quantity ? `${ing.quantity} ` : "";
    const note = ing.note ? ` (${ing.note})` : "";
    return `☐ ${measure}${ing.name}${note}`;
  });
  return `${title}\n\n${lines.join("\n")}`;
}

export default function CopyShoppingList({
  title,
  ingredients,
  className,
}: CopyShoppingListProps) {
  const [copied, setCopied] = useState(false);
  const timeoutRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
    };
  }, []);

  const handleClick = async () => {
    const text = formatShoppingList(title, ingredients);

    try {
      await navigator.clipboard.writeText(text);
    } catch {
      // Fallback for environments without the Clipboard API.
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "absolute";
      textarea.style.left = "-9999px";
      document.body.appendChild(textarea);
      textarea.select();
      try {
        document.execCommand("copy");
      } catch {
        document.body.removeChild(textarea);
        return;
      }
      document.body.removeChild(textarea);
    }

    setCopied(true);
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
    timeoutRef.current = setTimeout(() => setCopied(false), 2200);
  };

  return (
    <button
      type="button"
      onClick={handleClick}
      aria-live="polite"
      className={[
        "cursor-pointer text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/55",
        "underline decoration-transparent decoration-[0.5px] underline-offset-[6px]",
        "transition-[color,text-decoration-color] duration-500 ease-out",
        "hover:text-[#1f1d1b] hover:decoration-[#1f1d1b]/30",
        "focus-visible:outline-none focus-visible:text-[#1f1d1b] focus-visible:decoration-[#1f1d1b]/40",
        "sm:text-[12px]",
        className ?? "",
      ].join(" ")}
    >
      {copied ? "Copied" : "Copy shopping list"}
    </button>
  );
}
