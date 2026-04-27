import Image from "next/image";
import type { Metadata } from "next";
import RightNow from "../../components/RightNow";
import TheEdit from "../../components/TheEdit";
import HomeFooterOverlay, {
  HomeFooterMobile,
} from "../../components/HomeFooterOverlay";

export const metadata: Metadata = {
  title: "Hessentials",
  description:
    "Choosing well, and standing by it. Food, home, style, and the small decisions that make a life feel considered.",
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
  /**
   * Quality tier — how aggressively to compress the image variants Next/Image
   * generates. Higher = sharper on retina/4K, larger file. The narrative
   * anchors (Dinner, Morning) get 95; secondary scenes (Exit, Cleanup)
   * settle at 92. Allowed values are pre-declared in next.config.ts.
   */
  quality?: 90 | 92 | 95;
  /** Overlay slot — used only on Morning for the Currently module. */
  children?: React.ReactNode;
};

function Cinematic({
  src,
  alt,
  type,
  filter,
  priority,
  quality = 92,
  children,
}: CinematicProps) {
  // Hacienda source images are 1537×1023 (3:2 landscape). On a portrait
  // phone, h-screen / h-[90vh] crops the landscape composition into a
  // narrow vertical strip — most of the room is sliced off the sides.
  // On mobile we size by the source aspect ratio so the FULL composition
  // shows; on desktop we keep the viewport-pinned cinematic sizing
  // (where the aspect roughly matches anyway).
  if (type === "bleed") {
    return (
      <div className="relative aspect-[3/2] w-full overflow-hidden md:aspect-auto md:h-screen">
        <Image
          src={src}
          alt={alt}
          fill
          sizes="100vw"
          quality={quality}
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
      <div className="relative aspect-[3/2] w-full overflow-hidden rounded-[20px] md:aspect-auto md:h-[90vh] md:max-h-[1100px]">
        <Image
          src={src}
          alt={alt}
          fill
          sizes="88vw"
          quality={quality}
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
            Hessentials
          </p>
          <h1 className="font-serif text-[clamp(2.75rem,7vw,4.5rem)] font-normal leading-[1.02] tracking-[-0.02em] text-balance">
            Life, edited well.
          </h1>
          <p className="text-pretty mt-8 font-serif text-[clamp(1.25rem,1.9vw,1.5rem)] italic leading-[1.45] text-[#1f1d1b]/70">
            This is what I kept coming back to.
          </p>
          {/* 02 — Micro-intro. Quiet continuation of the hero, not a new section. */}
          <p className="mt-6 max-w-[420px] text-[13px] leading-[1.55] text-[#1f1d1b]/55 sm:text-[13.5px]">
            Most of what&rsquo;s here just stayed. What didn&rsquo;t, didn&rsquo;t.
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
          quality={95}
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

      {/* ---------- Image 03 — Morning — Type B
                  Desktop: Currently overlay anchored bottom-right.
                  Mobile:  clean image (no overlay), then Currently as
                           a separate cream section below the image —
                           overlay text wasn't readable on a portrait-
                           cropped image. */}
      <section aria-hidden style={{ marginTop: GAP_IMG }}>
        <Cinematic
          src="/home/hacienda-03-morning.jpg"
          alt=""
          type="frame"
          quality={95}
        >
          {/* DESKTOP-ONLY: radial darken + RightNow overlay. */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 hidden md:block"
            style={{
              backgroundImage:
                "radial-gradient(ellipse 70% 60% at 100% 92%, rgba(20,18,16,0.58), rgba(20,18,16,0.22) 45%, transparent 75%)",
            }}
          />
          <div className="absolute right-16 bottom-16 hidden max-w-[320px] md:block">
            <RightNow variant="light" />
          </div>
        </Cinematic>
      </section>

      {/* MOBILE-ONLY: Currently as a clean cream section below the
          morning image. Same content, properly composed for a phone. */}
      <section
        aria-label="Currently"
        className="block px-6 pt-12 pb-2 sm:px-10 md:hidden"
      >
        <div className="mx-auto max-w-[420px]">
          <RightNow variant="default" />
        </div>
      </section>

      {/* ---------- The Edit — beige zone — image↔beige gap above ---------- */}
      <section
        aria-label="The Edit"
        className="px-6 sm:px-10 md:px-16"
        style={{ marginTop: GAP_ZONE }}
      >
        <TheEdit />
      </section>

      {/*
        Image 04 — Cleanup — Type B — closes the page.

        The footer (newsletter + brand mark + tagline + legal) is overlaid
        on this image instead of rendering on a separate cream slab below.
        The page lands inside the world it built. Each footer row reveals
        on scroll using the same staggered fade-up pattern as Currently
        on Image 03 — keeps the homepage cinematic from top to bottom.

        The global SiteFooter is suppressed on /home (see SiteFooter.tsx).
        Bottom padding is intentionally minimal here so the image is the
        last thing on the page.
      */}
      <section
        aria-label="Site footer"
        style={{ marginTop: GAP_ZONE, paddingBottom: "24px" }}
      >
        <Cinematic
          src="/home/hacienda-04-cleanup.jpg"
          alt=""
          type="frame"
          filter="brightness(0.78) saturate(0.92) contrast(1.02)"
        >
          {/* DESKTOP-ONLY: bottom darken + footer overlay. */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 hidden md:block"
            style={{
              backgroundImage:
                "linear-gradient(to bottom, transparent 35%, rgba(20,18,16,0.32) 65%, rgba(20,18,16,0.62) 100%)",
            }}
          />
          <HomeFooterOverlay />
        </Cinematic>

        {/* MOBILE-ONLY: cream footer block below the cleanup image. */}
        <HomeFooterMobile />
      </section>
    </main>
  );
}
