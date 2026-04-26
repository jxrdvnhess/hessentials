"use client";

import Link from "next/link";
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type FormEvent,
  type KeyboardEvent,
} from "react";
import { searchIndex, type SearchItem } from "../data/searchIndex";

/**
 * Inline-expand search affordance for the global header.
 *
 * Restraint: a quiet glyph that opens an input flush to the nav. No modal,
 * no overlay. Results render in a thin dropdown anchored to the input.
 * Closes on Esc, click-outside, or selecting a result.
 */
export default function SiteSearch() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);
  const wrapRef = useRef<HTMLDivElement>(null);

  const results = useMemo<SearchItem[]>(
    () => (query ? searchIndex(query, 8) : []),
    [query]
  );

  const close = useCallback(() => {
    setOpen(false);
    setQuery("");
  }, []);

  useEffect(() => {
    if (!open) return;
    inputRef.current?.focus();

    const onKey = (e: globalThis.KeyboardEvent) => {
      if (e.key === "Escape") close();
    };
    const onClick = (e: MouseEvent) => {
      if (!wrapRef.current) return;
      if (!wrapRef.current.contains(e.target as Node)) close();
    };

    document.addEventListener("keydown", onKey);
    document.addEventListener("mousedown", onClick);
    return () => {
      document.removeEventListener("keydown", onKey);
      document.removeEventListener("mousedown", onClick);
    };
  }, [open, close]);

  const onSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Submit jumps to first result if there is one.
    if (results[0]) {
      window.location.assign(results[0].url);
      close();
    }
  };

  const onInputKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Escape") {
      e.preventDefault();
      close();
    }
  };

  return (
    <div ref={wrapRef} className="relative flex items-center">
      {/* Toggle glyph */}
      {!open && (
        <button
          type="button"
          aria-label="Search"
          onClick={() => setOpen(true)}
          className="flex h-7 w-7 items-center justify-center text-[#1f1d1b]/55 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/85 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/40 focus-visible:ring-offset-2 focus-visible:ring-offset-[#f8f6f3]"
        >
          <SearchGlyph />
        </button>
      )}

      {/* Inline input */}
      {open && (
        <form
          onSubmit={onSubmit}
          role="search"
          aria-label="Site search"
          className="flex items-center"
        >
          <span
            aria-hidden
            className="mr-2 flex h-4 w-4 items-center justify-center text-[#1f1d1b]/55"
          >
            <SearchGlyph />
          </span>
          <input
            ref={inputRef}
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={onInputKeyDown}
            placeholder="Search"
            aria-label="Search"
            spellCheck={false}
            autoComplete="off"
            className="w-[8.5rem] border-b border-[#1f1d1b]/25 bg-transparent pb-1 text-[12px] uppercase tracking-[0.22em] text-[#1f1d1b]/85 placeholder:text-[#1f1d1b]/35 focus:border-[#1f1d1b]/55 focus:outline-none sm:w-[12rem] md:w-[14rem]"
          />
          <button
            type="button"
            aria-label="Close search"
            onClick={close}
            className="ml-2 text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/45 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/75"
          >
            Close
          </button>
        </form>
      )}

      {/* Results dropdown */}
      {open && query && (
        <div
          role="listbox"
          aria-label="Search results"
          className="absolute right-0 top-full z-50 mt-3 w-[min(22rem,90vw)] border border-[#1f1d1b]/10 bg-[#f8f6f3] py-2 shadow-[0_8px_28px_-12px_rgba(31,29,27,0.18)]"
        >
          {results.length === 0 ? (
            <p className="px-4 py-3 text-[12px] text-[#1f1d1b]/45">
              No matches.
            </p>
          ) : (
            <ul>
              {results.map((item) => (
                <li key={`${item.section}-${item.url}-${item.title}`}>
                  <Link
                    href={item.url}
                    onClick={close}
                    className="block px-4 py-2.5 transition-colors duration-300 ease-out hover:bg-[#1f1d1b]/[0.04]"
                  >
                    <span className="block text-[10px] uppercase tracking-[0.22em] text-[#1f1d1b]/40">
                      {item.section}
                    </span>
                    <span className="mt-0.5 block font-serif text-[15px] leading-[1.3] text-[#1f1d1b]">
                      {item.title}
                    </span>
                    {item.description && (
                      <span className="mt-1 block text-[12px] leading-[1.45] text-[#1f1d1b]/55 line-clamp-1">
                        {item.description}
                      </span>
                    )}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

function SearchGlyph() {
  return (
    <svg
      aria-hidden
      viewBox="0 0 16 16"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.25"
      strokeLinecap="round"
      className="h-[15px] w-[15px]"
    >
      <circle cx="7" cy="7" r="4.75" />
      <line x1="10.6" y1="10.6" x2="13.5" y2="13.5" />
    </svg>
  );
}
