import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";
import RightNow from "../../components/RightNow";
import TheEdit from "../../components/TheEdit";
import HomeFooterOverlay, {
  HomeFooterMobile,
} from "../../components/HomeFooterOverlay";
import ImagePoemLine from "../../components/ImagePoemLine";
import Symbol from "../../components/Symbol";

export const metadata: Metadata = {
  title: "Hessentials",
  description:
    "Food, home, and style for people who want better defaults, not more options. Recipes, rooms, and small upgrades worth the time.",
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
 *                   edges, max-w 320px, localized scrim under block
 *   Article Grid    The Edit, beige zone, 2-3 column structured
 *
 * IMAGE ARC PACING (post 2026-04-28 design refinement)
 *   The four images now stack near-flush as a cinematic sequence. Poem
 *   lines moved off the cream gaps and into the images themselves at
 *   art-directed low-detail zones (see ImagePoemLine). Hero → Image 01
 *   keeps a modest cream gap so the hero has room to breathe. Between
 *   images: 12px — a film cut, not a section break.
 */

const GAP_HERO = "8vh"; // Hero → Image 01 — modest cream breath before the arc
const GAP_IMG = "12px"; // Image ↔ Image — film cut
const GAP_ZONE = "96px"; // Image ↔ The Edit — beige zone, compressed from 140px

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
  /** Overlay slot — used for in-image poem lines, the Currently module, and footer overlays. */
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
      <div className="relative aspect-[3/4] w-full overflow-hidden md:aspect-auto md:h-screen">
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
      <div className="relative aspect-[4/5] w-full overflow-hidden rounded-[20px] md:aspect-auto md:h-[90vh] md:max-h-[1100px]">
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
      {/* ---------- Hero — text only. Image 01 emerges below this viewport. ----------
          The right side of the hero used to read as accidental empty space. A
          single small "h" mark in the upper-right anchors the asymmetry without
          adding content (per §1.4). */}
      <section className="relative flex min-h-[52vh] items-center px-6 pt-16 sm:px-10 md:min-h-[65vh] md:px-16 md:pt-0">
        <div className="fade-up delay-3 max-w-[520px]">
          <p className="mb-10 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px]">
            Hessentials
          </p>
          <h1 className="font-serif text-[clamp(2.75rem,7vw,4.5rem)] font-normal leading-[1.02] tracking-[-0.02em] text-balance">
            Life, edited well.
          </h1>
          <p className="text-pretty mt-8 font-serif text-[clamp(1.25rem,1.9vw,1.5rem)] italic leading-[1.45] text-[#1f1d1b]/70">
            Food, home, and style for people who want better defaults, not more options.
          </p>
          {/* Direct, blunt clarification. Tells the reader what they're getting. */}
          <p className="mt-6 max-w-[420px] text-[13px] leading-[1.55] text-[#1f1d1b]/55 sm:text-[13.5px]">
            Less to decide. More that works.
          </p>
          {/* Single, named entry point. Hero must answer "what do I do next" within three seconds.
              The label is italic serif (not an uppercase eyebrow) so it reads like a quiet
              hand on the shoulder rather than a section header. */}
          <div className="mt-10 max-w-[480px]">
            <p className="font-serif text-[12px] italic leading-none text-[#1f1d1b]/55 sm:text-[13px]">
              If you&rsquo;re new, start here
            </p>
            <Link
              href="/aurelian"
              className="group mt-3 inline-flex flex-wrap items-baseline gap-x-2"
            >
              <span className="font-serif text-[clamp(1.0625rem,1.5vw,1.25rem)] italic leading-[1.35] text-[#1f1d1b]/85 transition-opacity duration-300 ease-out group-hover:opacity-65">
                Aurelian &mdash; a short reading on how you operate
              </span>
              <span aria-hidden className="text-[12px] not-italic text-[#1f1d1b]/45">
                →
              </span>
            </Link>
          </div>
        </div>

        {/* Hero asymmetry mark — quiet "h" anchoring the upper-right
            quadrant. Tonal-cream tint via opacity so it reads as
            present-but-not-announced against the plaster background. */}
        <div
          aria-hidden
          className="pointer-events-none absolute right-6 top-12 hidden opacity-25 sm:right-10 sm:block md:right-16 md:top-16"
        >
          <Symbol size="xs" />
        </div>
      </section>

      {/*
        Image 01 — Morning, two men at the table — Type A.

        The opening image extends the hero rather than beginning a new
        section:

          - small cream breath above (GAP_HERO ~ 8vh)
          - top mask: the image's upper ~28% is faded to transparent
            via a linear-gradient mask, revealing the page's cream
            background through it

        The result: the seam between hero and image is cream-on-cream
        (invisible). Below the seam, the image gradually becomes itself.
        The viewer is already inside the world before they consciously
        scroll.

        Inside the image: Some moments hold. — upper-left plaster wall,
        the undetailed area above and to the left of the older man.
      */}
      <section
        aria-hidden
        className="w-full"
        style={{
          marginTop: GAP_HERO,
          maskImage:
            "linear-gradient(to bottom, transparent 0%, transparent 4%, black 32%)",
          WebkitMaskImage:
            "linear-gradient(to bottom, transparent 0%, transparent 4%, black 32%)",
        }}
      >
        <Cinematic
          src="/home/merida-moment-1.jpg"
          alt=""
          type="bleed"
          quality={95}
          priority
        >
          <ImagePoemLine
            position={{
              top: "14%",
              left: "6%",
              maxWidth: "min(34rem, 48%)",
              align: "left",
            }}
            size="lg"
          >
            Some moments hold.
          </ImagePoemLine>
        </Cinematic>
      </section>

      {/* ---------- Image 02 — Midday poolside — Type A — film-cut gap above ----------
          Inside: Most don't. — upper-right where the pink-clay wall
          meets the architectural shadow under the eaves. */}
      <section aria-hidden style={{ marginTop: GAP_IMG }}>
        <Cinematic
          src="/home/merida-moment-2.jpg"
          alt=""
          type="bleed"
        >
          <ImagePoemLine
            position={{
              top: "10%",
              right: "6%",
              maxWidth: "min(30rem, 42%)",
              align: "right",
            }}
            size="lg"
          >
            Most don&rsquo;t.
          </ImagePoemLine>
        </Cinematic>
      </section>

      {/* ---------- Image 03 — Late afternoon, solo with notebook — Type B ----------
                  Desktop: full Currently overlay, anchored bottom-right,
                  with a localized scrim that darkens only the area beneath
                  the Currently block (per §3.1).
                  Mobile:  bigger portrait crop with the full Currently
                  block in a cream section below the image — the image
                  keeps its brand-poetry moment.
                  Inside: You learn the difference. — upper-left wall area
                  where the pink-clay wall catches the gold light, above
                  and to the left of the seated man. */}
      <section aria-hidden style={{ marginTop: GAP_IMG }}>
        <Cinematic
          src="/home/merida-moment-3.jpg"
          alt=""
          type="frame"
          quality={95}
        >
          <ImagePoemLine
            position={{
              top: "12%",
              left: "6%",
              maxWidth: "min(32rem, 46%)",
              align: "left",
            }}
            size="lg"
          >
            You learn the difference.
          </ImagePoemLine>

          {/* DESKTOP: localized scrim under the Currently block + Currently overlay.
              The scrim is bounded to the lower-right column where the
              type actually sits — not a full-image darken — so the rest
              of the composition stays clean. Per §3.1: transparent →
              ~40% black, sized to the column where the text lives. The
              new merida_moment_3.jpg has a brighter doorway behind the
              block, so the scrim is a touch heavier than spec to keep
              the article links legible. */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 hidden md:block"
            style={{
              backgroundImage:
                "linear-gradient(to bottom right, transparent 30%, rgba(20,18,16,0.32) 65%, rgba(20,18,16,0.5) 100%)",
              maskImage:
                "radial-gradient(ellipse 60% 70% at 100% 100%, black 0%, black 45%, transparent 90%)",
              WebkitMaskImage:
                "radial-gradient(ellipse 60% 70% at 100% 100%, black 0%, black 45%, transparent 90%)",
            }}
          />
          <div className="absolute right-16 bottom-16 hidden max-w-[320px] md:block">
            <RightNow variant="light" />
          </div>

          {/* MOBILE: image stays clean. All Start Here + Currently labels
              live in the cream block below so the cream block reads as a
              single, guided composition rather than splitting an eyebrow
              across the seam. */}
        </Cinematic>
      </section>

      {/* MOBILE-ONLY: full Start Here + Currently block as a clean cream
          section below the morning image. */}
      <section
        aria-label="Start here and Currently"
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
        <div className="mb-12 max-w-[520px] sm:mb-14 md:mb-16">
          {/* Quiet edge line. A single, confident truth that frames the
              section without raising its voice. Generous spacing below
              so it reads as a quiet aside, not a heading. */}
          <p className="font-serif text-[clamp(0.95rem,1.2vw,1.0625rem)] italic leading-[1.55] text-[#1f1d1b]/55">
            Most of what you&rsquo;ve been told to buy, cook, or follow isn&rsquo;t that good.
          </p>
          {/* Section eyebrow with the new hairline above it (§2.2).
              80px wide, 0.5px, tonal cream — anchors the label as an
              architectural moment, not a floating tag. */}
          <span
            aria-hidden
            className="mt-14 block w-20"
            style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
          />
          <p className="mt-6 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px]">
            The Edit
          </p>
          <p className="text-balance mt-4 font-serif text-[clamp(1.125rem,1.6vw,1.375rem)] italic leading-[1.4] text-[#1f1d1b]/70">
            The pieces that hold up. Read one. Use it tonight.
          </p>
        </div>
        <TheEdit />
      </section>

      {/*
        Image 04 — Night, dinner conversation — Type B — closes the page.

        The footer (newsletter + brand mark + tagline + legal) is overlaid
        on this image instead of rendering on a separate cream slab below.
        The page lands inside the world it built. Each footer row reveals
        on scroll using the same staggered fade-up pattern as Currently
        on Image 03 — keeps the homepage cinematic from top to bottom.

        The global SiteFooter is suppressed on /home (see SiteFooter.tsx).
        Bottom padding is intentionally minimal here so the image is the
        last thing on the page.

        Inside the image: What was real, stayed. — upper-center wall
        behind the table, in the soft pendant glow.
      */}
      <section
        aria-label="Site footer"
        style={{ marginTop: GAP_ZONE, paddingBottom: "24px" }}
      >
        <Cinematic
          src="/home/merida-moment-4.jpg"
          alt=""
          type="frame"
          filter="brightness(0.92) saturate(0.96) contrast(1.02)"
        >
          <ImagePoemLine
            position={{
              top: "10%",
              left: "50%",
              transform: "translateX(-50%)",
              maxWidth: "min(36rem, 70%)",
              align: "center",
            }}
            size="lg"
          >
            What was real, stayed.
          </ImagePoemLine>

          {/* DESKTOP: bottom darken + full footer overlay. */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 hidden md:block"
            style={{
              backgroundImage:
                "linear-gradient(to bottom, transparent 35%, rgba(20,18,16,0.32) 65%, rgba(20,18,16,0.62) 100%)",
            }}
          />
          <HomeFooterOverlay />

          {/* MOBILE: bottom darken + brand-close whisper.
              Just the wordmark eyebrow + tagline italic — the cleanup
              image keeps its identity as the brand close. The full
              footer (newsletter, symbol, legal) lives in the cream
              block below. */}
          <div
            aria-hidden
            className="pointer-events-none absolute inset-0 md:hidden"
            style={{
              backgroundImage:
                "linear-gradient(to bottom, transparent 50%, rgba(20,18,16,0.28) 75%, rgba(20,18,16,0.65) 100%)",
            }}
          />
          <div className="absolute inset-x-0 bottom-9 flex flex-col items-center text-center md:hidden">
            <p className="text-[11px] uppercase tracking-[0.3em] text-[#f8f6f3]/85">
              Hessentials
            </p>
            <p className="mt-3 font-serif text-[16px] italic leading-[1.4] text-[#f8f6f3]/85">
              This is what stayed.
            </p>
          </div>
        </Cinematic>

        {/* MOBILE-ONLY: cream footer block below the cleanup image
            (newsletter + symbol + legal — the wordmark whisper above
            already lives on the image). */}
        <HomeFooterMobile />
      </section>
    </main>
  );
}
