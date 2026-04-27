"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useEffect, useState } from "react";

type NavLink = { label: string; href: string };

type Props = { links: ReadonlyArray<NavLink> };

/**
 * MobileMenu — full-screen drawer for phones / small tablets.
 *
 * Restraint: a quiet "Menu" text trigger in the header bar (no hamburger
 * glyph). Tapping opens a full-screen overlay with the same plaster-tone
 * background and a vertical column of serif links. Closes on:
 *   - tapping a link (route change)
 *   - tapping "Close"
 *   - pressing Escape
 *   - the route changing for any other reason
 *
 * Hidden entirely from md+ breakpoints — desktop has its own inline nav.
 */
export default function MobileMenu({ links }: Props) {
  const [open, setOpen] = useState(false);
  const pathname = usePathname();

  // Always collapse the menu when the route changes.
  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setOpen(false);
  }, [pathname]);

  // Lock body scroll + listen for Escape while open.
  useEffect(() => {
    if (!open) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", onKey);
    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", onKey);
    };
  }, [open]);

  return (
    <>
      <button
        type="button"
        aria-label="Open menu"
        aria-expanded={open}
        aria-controls="site-mobile-menu"
        onClick={() => setOpen(true)}
        className="text-[10.5px] uppercase tracking-[0.26em] text-[#1f1d1b]/65 transition-colors duration-300 ease-out hover:text-[#1f1d1b] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/40 focus-visible:ring-offset-2 focus-visible:ring-offset-[#f8f6f3] md:hidden"
      >
        Menu
      </button>

      {open && (
        <div
          id="site-mobile-menu"
          role="dialog"
          aria-modal="true"
          aria-label="Site menu"
          className="fixed inset-0 z-50 bg-[#f8f6f3]/[0.97] backdrop-blur-md md:hidden"
          style={{
            paddingTop: "env(safe-area-inset-top)",
            paddingBottom: "env(safe-area-inset-bottom)",
          }}
        >
          <div className="flex h-full flex-col">
            <div className="flex items-center justify-between px-6 pt-5 sm:px-10 sm:pt-6">
              <span className="text-[10.5px] uppercase tracking-[0.28em] text-[#1f1d1b]/45">
                Hessentials
              </span>
              <button
                type="button"
                aria-label="Close menu"
                onClick={() => setOpen(false)}
                className="text-[10.5px] uppercase tracking-[0.26em] text-[#1f1d1b]/65 transition-colors duration-300 ease-out hover:text-[#1f1d1b] focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-[#1f1d1b]/40 focus-visible:ring-offset-2 focus-visible:ring-offset-[#f8f6f3]"
              >
                Close
              </button>
            </div>

            <nav
              aria-label="Primary"
              className="flex flex-1 flex-col items-center justify-center gap-7 px-6 pb-20"
            >
              {links.map(({ label, href }) => {
                const active =
                  pathname === href || pathname.startsWith(`${href}/`);
                return (
                  <Link
                    key={href}
                    href={href}
                    onClick={() => setOpen(false)}
                    className={[
                      "font-serif text-[clamp(1.75rem,7vw,2.25rem)] font-normal leading-none tracking-[-0.01em] transition-opacity duration-300 ease-out",
                      active
                        ? "opacity-100"
                        : "opacity-65 hover:opacity-100",
                    ].join(" ")}
                  >
                    {label}
                  </Link>
                );
              })}
            </nav>
          </div>
        </div>
      )}
    </>
  );
}
