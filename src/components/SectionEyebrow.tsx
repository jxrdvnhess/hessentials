import type { ReactNode } from "react";

type SectionEyebrowProps = {
  /** The eyebrow text — typically all-caps, letter-spaced. */
  children: ReactNode;
  /** Anchor the block left, center, or right. Default "center". */
  align?: "left" | "center" | "right";
  /** Pass-through className for outer wrapper. */
  className?: string;
};

/**
 * All-caps section eyebrow with the new hairline above (per §2.2).
 *
 * The hairline (80px wide, 0.5px, tonal cream `#c8bfae`) anchors the
 * label as an architectural moment instead of a floating tag. The label
 * itself uses the same uppercase-tracked treatment as before; only the
 * scaffolding above it is new.
 *
 * Pass any inline-aware children — typically a short string ("RECIPES",
 * "START HERE", "THIS WEEK"). For more complex labels (e.g., an
 * additional tagline below the eyebrow line), wrap the children in a
 * fragment.
 */
export default function SectionEyebrow({
  children,
  align = "center",
  className = "",
}: SectionEyebrowProps) {
  const alignClass =
    align === "left"
      ? "items-start text-left"
      : align === "right"
      ? "items-end text-right"
      : "items-center text-center";

  return (
    <div className={`flex flex-col ${alignClass} ${className}`}>
      <span
        aria-hidden
        className="block w-20"
        style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
      />
      <p className="mt-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]">
        {children}
      </p>
    </div>
  );
}
