import Image from "next/image";
import type { Metadata } from "next";
import RightNow from "../../components/RightNow";
import TheEdit from "../../components/TheEdit";

export const metadata: Metadata = {
  title: "Hessentials",
  description:
    "A system for choosing what holds. Food, home, style, and the small decisions that shape how life actually feels.",
};

/**
 * Homepage layout system — strict.
 *
 * IMAGE TYPES (two only)
 *   A — Full Bleed     100vh, edge-to-edge, no radius
 *   B — Feature Frame  90vh, inset 6% left/right, 20px corner radius
 *
 *   Dinner + Exit  → Type A
 *   Morning + Cleanup → Type B
 *
 * TEXT SYSTEMS (three only)
 *   Hero            left-aligned, max-w 520px, vertically centered
 *   Currently       overlay on Morning only, bottom-right, 64px from
 *                   edges, max-w 320px, subtle radial gradient
 *   Article Grid    The Edit, beige zone, 2-3 column structured
 *
 * SPACING TOKENS (locked)
 *   Image ↔ Image       24px
 *   Image ↔ Beige zone  140px
 */

const GAP_IMG = "24px"; // Image to image
const GAP_ZONE = "140px"; // Image to beige / beige to image

type CinematicProps = {
  src: string;
  alt: string;
  /** Type A — full bleed (100vh edge-to-edge). Type B — feature frame (90vh inset rounded). */
  type: "bleed" | "frame";
  /** Inline filter for subdued moments (Cleanup). */
  filter?: string;
  priority?: boolean;
  /** Overlay slot — used only on Morning for the Currently module. */
  children?: React.ReactNode;
};

function Cinematic({
  src,
  alt,
  type,
  filter,
  priority,
  children,
}: CinematicProps) {
  if (type === "bleed") {
    return (
      <div className="relative h-screen w-full overflow-hidden">
        <Image
          src={src}
          alt={alt}
          fill
          sizes="100vw"
          quality={92}
          priority={priority}
          className="object-cover"
          style={filter ? { filter } : undefined}
        />
        {children}
      </div>
    );
  }

  // Type B — feature frame
  return (
    <div className="px-[6vw]">
      <div className="relative h-[90vh] max-h-[1100px] w-full overflow-hidden rounded-[20px]">
        <Image
          src={src}
          alt={alt}
          fill
          sizes="88vw"
          quality={92}
          priority={priority}
          className="object-cover"
          style={filter ? { filter } : undefined}
        />
        {children}
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      {/* ---------- Hero — text only. Image 01 emerges inside this viewport. ---------- */}
      <section className="flex min-h-[65vh] items-center px-6 sm:px-10 md:px-16">
        <div className="fade-up delay-3 max-w-[520px]">
          <p className="mb-10 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px]">
            A more intentional way to live
          </p>
          <h1 className="font-serif text-[clamp(2.75rem,7vw,4.5rem)] font-normal leading-[1.02] tracking-[-0.02em] text-balance">
            Life, edited well.
          </h1>
          <p className="text-pretty mt-8 font-serif text-[clamp(1.25rem,1.9vw,1.5rem)] italic leading-[1.45] text-[#1f1d1b]/70">
            A system for choosing what holds.
          </p>
        </div>
      </section>

      {/*
        Image 01 — Dinner — Type A.

        This is the only place the strict GAP_ZONE rule is intentionally
        relaxed. The opening image must extend the hero, not begin a new
        section. So:

          - no top margin: the image touches the hero directly
          - top mask: the image's upper ~28% is faded to transparent
            via a linear-gradient mask, revealing the page's cream
            background through it

        The result: the seam between hero and image is cream-on-cream
        (invisible). Below the seam, the image gradually becomes itself.
        The headline sits in the upper cream area where it always was,
        unaffected. The viewer is already inside the world before they
        consciously scroll.
      */}
      <section
        aria-hidden
        className="w-full"
        style={{
          maskImage:
            "linear-gradient(to bottom, transparent 0%, transparent 4%, black 32%)",
          WebkitMaskImage:
            "linear-gradient(to bottom, transparent 0%, transparent 4%, black 32%)",
        }}
      >
        <Cinematic
          src="/home/hacienda-01-dinner.jpg"
          alt=""
          type="bleed"
          priority
        />
      </section>

      {/* ---------- Image 02 — Exit — Type A — image↔image gap above ---------- */}
      <section aria-hidden style={{ marginTop: GAP_IMG }}>
        <Cinematic
          src="/home/hacienda-02-exterior.jpg"
          alt=""
          type="bleed"
        />
      </section>

      {/* ---------- Image 03 — Morning — Type B — Currently overlaid ---------- */}
      <section aria-hidden style={{ marginTop: GAP_IMG }}>
        <Cinematic src="/home/hacienda-03-morning.jpg" alt="" type="frame">
          {/* Subtle radial darken at bottom-right for legibility */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0"
            style={{
              backgroundImage:
                "radial-gradient(ellipse 70% 60% at 100% 92%, rgba(20,18,16,0.58), rgba(20,18,16,0.22) 45%, transparent 75%)",
            }}
          />
          {/*
            Currently — bottom-right, 64px from edges, max-w 320px on
            tablet/desktop. Tightened to 32px / 280px on phones so the
            type doesn't clip the rounded frame's left edge.
          */}
          <div className="absolute bottom-8 right-8 max-w-[280px] sm:bottom-16 sm:right-16 sm:max-w-[320px]">
            <RightNow variant="light" />
          </div>
        </Cinematic>
      </section>

      {/* ---------- The Edit — beige zone — image↔beige gap above ---------- */}
      <section
        aria-label="The Edit"
        className="px-6 sm:px-10 md:px-16"
        style={{ marginTop: GAP_ZONE }}
      >
        <TheEdit />
      </section>

      {/* ---------- Image 04 — Cleanup — Type B — beige↔image gap above ---------- */}
      <section
        aria-hidden
        style={{ marginTop: GAP_ZONE, paddingBottom: GAP_ZONE }}
      >
        <Cinematic
          src="/home/hacienda-04-cleanup.jpg"
          alt=""
          type="frame"
          filter="brightness(0.86) saturate(0.93) contrast(1.02)"
        />
      </section>
    </main>
  );
}
