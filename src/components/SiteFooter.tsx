"use client";

import { usePathname } from "next/navigation";
import Symbol from "./Symbol";

export default function SiteFooter() {
  const pathname = usePathname();
  // No footer on the Enter Page — gateway stays clean.
  if (pathname === "/") return null;

  const year = new Date().getFullYear();

  return (
    <footer
      aria-label="Site"
      className="border-t border-[#1f1d1b]/10 px-6 py-14 text-center sm:px-10 md:px-16 md:py-16"
    >
      <div className="mx-auto flex max-w-3xl flex-col items-center gap-y-5">
        <Symbol size="md" alt="Hessentials" />

        <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/50 sm:text-[12px]">
          Hessentials
        </p>

        <p className="font-serif text-[15px] italic leading-[1.4] text-[#1f1d1b]/55 sm:text-[16px]">
          Less, but better.
        </p>

        <p className="mt-2 text-[10px] uppercase tracking-[0.24em] text-[#1f1d1b]/35 sm:text-[11px]">
          © {year}
        </p>
      </div>
    </footer>
  );
}
