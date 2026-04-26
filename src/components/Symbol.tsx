import Image from "next/image";

export type SymbolSize = "xs" | "sm" | "md" | "lg" | "xl" | "2xl";
export type SymbolVariant = "default" | "inverse";

type SymbolProps = {
  size?: SymbolSize;
  variant?: SymbolVariant;
  /** Set empty for decorative use (the wordmark already names the brand). */
  alt?: string;
  className?: string;
};

const WIDTH: Record<SymbolSize, string> = {
  xs: "w-4",
  sm: "w-6",
  md: "w-10",
  lg: "w-16",
  xl: "w-20",
  "2xl": "w-24",
};

/**
 * Hessentials monogram symbol. Quiet brand signature. The wordmark stays
 * primary; this is for footer marks, editorial end-marks, favicons, and
 * compact placements where the full wordmark would overweight the layout.
 */
export default function Symbol({
  size = "sm",
  variant = "default",
  alt = "",
  className,
}: SymbolProps) {
  const src =
    variant === "inverse"
      ? "/hessentials-symbol-inverse.png"
      : "/hessentials-symbol.png";

  return (
    <span
      className={["inline-block align-middle", WIDTH[size], className ?? ""]
        .filter(Boolean)
        .join(" ")}
    >
      <Image
        src={src}
        alt={alt}
        width={512}
        height={512}
        sizes="64px"
        className="block h-auto w-full"
      />
    </span>
  );
}
