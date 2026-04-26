import Image from "next/image";

export type WordmarkSize = "small" | "nav" | "medium" | "large" | "hero";

type WordmarkProps = {
  /**
   * Visual scale.
   *  - small  → footer / compact placements
   *  - nav    → global site header (responsive, anchors the bar)
   *  - medium → page header
   *  - large  → entry screen
   *  - hero   → arrival / brand-moment placement
   */
  size?: WordmarkSize;
  /** Use for above-the-fold instances (e.g., the entry screen). */
  priority?: boolean;
  /** Override accessible name. Defaults to "Hessentials". */
  alt?: string;
  /** Additive utility classes — layout, animation, spacing. Don't override width. */
  className?: string;
};

/**
 * Each size scales fluidly via clamp() — min/preferred/max — so the wordmark
 * stays proportional with surrounding type at every viewport.
 */
const WIDTH_BY_SIZE: Record<WordmarkSize, string> = {
  small: "w-[clamp(112px,11vw,140px)]",
  nav: "w-[clamp(140px,14vw,200px)]",
  medium: "w-[clamp(160px,18vw,220px)]",
  large: "w-[clamp(280px,72vw,440px)]",
  hero: "w-[clamp(320px,78vw,520px)]",
};

const SIZES_HINT_BY_SIZE: Record<WordmarkSize, string> = {
  small: "(min-width: 1280px) 140px, 11vw",
  nav: "(min-width: 1280px) 200px, 14vw",
  medium: "(min-width: 1280px) 220px, 18vw",
  large: "(min-width: 1024px) 440px, 72vw",
  hero: "(min-width: 1024px) 520px, 78vw",
};

export default function Wordmark({
  size = "medium",
  priority = false,
  alt = "Hessentials",
  className,
}: WordmarkProps) {
  return (
    <span
      className={[
        "inline-block align-middle opacity-90 transition-opacity duration-500 ease-out hover:opacity-100",
        WIDTH_BY_SIZE[size],
        className ?? "",
      ].join(" ")}
    >
      <Image
        src="/hessentials-wordmark.png"
        alt={alt}
        width={1200}
        height={400}
        priority={priority}
        sizes={SIZES_HINT_BY_SIZE[size]}
        className="block h-auto w-full"
      />
    </span>
  );
}
