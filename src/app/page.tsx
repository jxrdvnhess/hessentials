import Image from "next/image";
import type { Metadata } from "next";
import RightNow from "../components/RightNow";
import ImagePoemLine from "../components/ImagePoemLine";
import Symbol from "../components/Symbol";
import AurelianThisWeekPanel from "../components/AurelianThisWeekPanel";
import MemorialDayModule from "../components/MemorialDayModule";
import HomePracticeTeaser from "../components/HomePracticeTeaser";
import NewsletterSignup from "../components/NewsletterSignup";

export const metadata: Metadata = {
  title: "Hessentials",
  description:
    "Food, home, and style for people who want better defaults, not more options. Recipes, rooms, and small upgrades worth the time.",
  alternates: {
    canonical: "/",
  },
};

/**
 * Revalidate hourly so the Aurelian This Week panel's auto-computed
 * date range (`May 4–10, 2026`) rolls over within an hour of Monday
 * morning without requiring a redeploy. Editorial copy still rolls
 * with a push — see src/data/aurelian-weekly.ts.
 */
export const revalidate = 3600;

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

const GAP_HERO = "4vh"; // Hero → Image 01 — tightened so the image edge peeks within the first viewport (fold cue)
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

  // Type B — feature frame.
  // The inset margins + rounded corners are a desktop-only treatment.
  // On mobile, photographs go edge-to-edge with no card frame so the
  // figures and architecture inside read at real photographic scale
  // rather than thumb-scale inside a inset card.
  return (
    <div className="md:px-[6vw]">
      <div className="relative aspect-[4/5] w-full overflow-hidden md:aspect-auto md:h-[90vh] md:max-h-[1100px] md:rounded-[20px]">
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
    </div>
  );
}

export default function HomePage() {
  return (
    <>
      <main className="relative z-10 text-[#1f1d1b]">
      {/* ---------- Hero — H1 left, Aurelian This Week panel right (md+).
          §1.2 — min-h compressed to 42vh with items-end so the H1 sits
          near the bottom and Image 01 enters the viewport at ~30–40%
          of its height (first cut of a film, not a portrait).
          §1.3 — Aurelian This Week panel anchors the right side on md+;
          on mobile, the original "If you're new, start here / Aurelian"
          CTA cluster returns to the left column. */}
      {/* Fold cue (2026-04-29): md:min-h-[88vh] anchors the hero to
          most of the first viewport with items-end, so the H1 sits
          near the bottom and Image 01's top edge peeks below — a
          content cue that there's more to read, not a UI element.
          Mobile is content-driven (mobile-stacked Aurelian module
          already pushes the hero past viewport on phones); the
          eyebrow of that module serves as the mobile fold cue. */}
      {/* Mobile: items-start + tight top padding so H1 sits close to
          the sticky header and Aurelian This Week's headline lands
          above the fold on a 390x844 viewport. Desktop unchanged —
          items-end + 88vh anchor + 96px top padding still hold the
          existing composition. */}
      <section className="relative flex min-h-0 items-start px-6 pt-14 pb-4 sm:px-10 md:min-h-[88vh] md:items-end md:pt-24 md:px-16">
        <div className="fade-up delay-3 max-w-[520px]">
          <p className="mb-5 text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/55 sm:text-[12px] md:mb-10">
            Hessentials
          </p>
          <h1 className="font-serif text-[clamp(2.5rem,7vw,4.5rem)] font-normal leading-[1.02] tracking-[-0.02em] text-balance">
            Life, edited well.
          </h1>
          <p className="text-pretty mt-5 font-serif text-[clamp(1.125rem,1.9vw,1.5rem)] italic leading-[1.45] text-[#1f1d1b]/70 md:mt-8">
            Food, home, and style for people who want better defaults, not more options.
          </p>
          {/* Direct, blunt clarification. Tells the reader what they're getting. */}
          <p className="mt-3 max-w-[420px] text-[13px] leading-[1.55] text-[#1f1d1b]/55 sm:text-[13.5px] md:mt-6">
            Less to decide. More that works.
          </p>
          {/* Mobile Aurelian This Week — replaces the old "If you're
              new, start here / Aurelian — a short reading" CTA cluster
              so mobile visitors meet the same editorial moment desktop
              visitors do. Same content as the desktop aside, stacked
              under the hero copy. Tightened mt on mobile so the
              headline sits above the fold at 390x844. */}
          <AurelianThisWeekPanel layout="mobile-stacked" />
        </div>

        {/* Aurelian This Week — desktop right-side aside (md+). */}
        <AurelianThisWeekPanel layout="desktop-aside" />

        {/* Hero asymmetry mark — quiet "h" anchoring the upper-right
            quadrant. Hidden on md+ (the Aurelian panel now anchors that
            zone with real content). */}
        <div
          aria-hidden
          className="pointer-events-none absolute right-6 top-12 hidden opacity-25 sm:right-10 sm:block md:hidden"
        >
          <Symbol size="xs" />
        </div>
      </section>

      {/*
        Currently — elevated to the second section (was the fifth, sitting
        as a cream block below Image 03 on mobile and as a Image 03
        overlay on desktop). This is the highest-intent surface on the
        site — the editorial navigation into what's on rotation right
        now — so it reads first, before the photo arc and the seasonal
        feature. Visible at every breakpoint.

        Acceptance — Section 2 of the May 22 launch brief: at least one
        card visible by the second scroll gesture on 390x844.
      */}
      <section
        aria-label="Currently"
        className="px-6 pt-12 pb-4 sm:px-10 sm:pt-14 md:px-16 md:pt-16 md:pb-6"
      >
        <div className="mx-auto max-w-[480px]">
          <RightNow variant="default" />
        </div>
      </section>

      {/*
        Inline newsletter — sits between Currently and the seasonal
        feature so a mobile visitor meets the form before the photo arc
        opens. The footer instance still ships; this one closes the gap
        for visitors who never reach the close. No pop-up, no sticky
        bar (Section 3 of the May 22 brief).
      */}
      <section
        aria-label="Newsletter"
        className="border-t border-[#1f1d1b]/10 px-6 py-14 sm:px-10 sm:py-16 md:px-16 md:py-20"
      >
        <NewsletterSignup pillar="default" source="inline" />
      </section>

      {/*
        Memorial Day featured moment.

        Sits in the slot the archived Mother's Day module previously
        occupied. Replaced by the next seasonal moment when this one is
        archived.
      */}
      <div style={{ marginTop: GAP_HERO }}>
        <MemorialDayModule />
      </div>

      {/*
        Image 01 — Morning, two men at the table — Type A.

        The opening image of the cinematic arc. Crisp edge — no top
        gradient fade — so the seam between the Memorial Day module
        and the arc reads as a clean editorial transition.

        Inside the image: Some moments hold. — upper-left plaster wall,
        the undetailed area above and to the left of the older man.
      */}
      <section
        aria-hidden
        className="w-full"
        style={{ marginTop: GAP_IMG }}
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
          meets the architectural shadow under the eaves. The thesis
          standfirst pairs with it on desktop (§2.1) as a print
          pull-quote bracketed by hairlines; on mobile it renders as
          a cream pull-quote block immediately below the image. */}
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
              maxWidth: "min(34rem, 48%)",
              align: "right",
            }}
            size="lg"
            standfirst="Most of what you’ve been told to buy, cook, or follow isn’t that good."
          >
            Most don&rsquo;t.
          </ImagePoemLine>
        </Cinematic>
      </section>

      {/* ---------- Image 03 — Late afternoon, solo with notebook — Type B ----------
                  Currently was moved off this image into the second
                  section of the page (see Section 2 above). Image 03
                  keeps its brand-poetry moment unencumbered: poem line
                  only, no overlay block.
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
        </Cinematic>
      </section>

      {/* ---------- Practice statement teaser ----------
          The dinner photograph + "What was real, stayed." line that
          used to anchor the closer are baked into this teaser. With
          the PRACTICE eyebrow dropped, the section reads as the next
          beat in the photo arc — film-cut gap above (12px) instead
          of the cream-zone GAP_ZONE break the old The Edit roundup
          needed. Bottom keeps GAP_ZONE so the teaser breathes before
          the universal SiteFooter (rendered from layout.tsx) takes
          over the close. */}
      <section
        aria-label="Practice"
        style={{ marginTop: GAP_IMG, paddingBottom: GAP_ZONE }}
      >
        <HomePracticeTeaser />
      </section>
      </main>
    </>
  );
}
