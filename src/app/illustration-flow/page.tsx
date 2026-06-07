import Image from "next/image";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Illustration in flow — studies",
  robots: { index: false, follow: false },
};

/**
 * LOCAL BRAINSTORM — not linked in nav, noindex.
 *
 * Studies for weaving editorial drawings into the reading flow,
 * book-illustration style: art that illuminates the text instead of
 * stopping it. The opposite of the old full-bleed Mérida arc.
 *
 * Because these drawings dissolve into bare cream paper, they need no
 * frame and no hard crop — that's the whole advantage over the photos.
 * Every study below feathers the one drawing we have
 * (/half-revealed.jpg) into the page ground (#f8f6f3) so it floats on
 * the paper rather than sitting in a box.
 *
 * The drawing is a stand-in. Each real slot would get its own
 * drawing-of-evidence. This page is about PLACEMENT, not final art.
 *
 * Throwaway route — delete before anything ships.
 */

// On-cream treatment: the drawing's paper white-balanced to the brand
// ground (#f8f6f3) so it reads as ink on the page, not a sheet laid on
// top. This becomes the standard prep for every drawing.
const SRC = "/half-revealed-oncream.jpg";

// Feather the drawing's edges into the cream ground — "dissolves into
// the bare paper" rather than a framed photo.
const featherAll: React.CSSProperties = {
  WebkitMaskImage:
    "radial-gradient(118% 130% at 50% 42%, #000 60%, rgba(0,0,0,0) 100%)",
  maskImage:
    "radial-gradient(118% 130% at 50% 42%, #000 60%, rgba(0,0,0,0) 100%)",
};

const featherBleedRight: React.CSSProperties = {
  WebkitMaskImage:
    "linear-gradient(to right, rgba(0,0,0,0) 0%, #000 26%, #000 100%), radial-gradient(140% 150% at 50% 45%, #000 65%, rgba(0,0,0,0) 100%)",
  maskImage:
    "linear-gradient(to right, rgba(0,0,0,0) 0%, #000 26%, #000 100%), radial-gradient(140% 150% at 50% 45%, #000 65%, rgba(0,0,0,0) 100%)",
  WebkitMaskComposite: "source-in",
  maskComposite: "intersect",
};

function Note({ children }: { children: React.ReactNode }) {
  return (
    <p className="mx-auto mb-10 max-w-2xl border-l border-[#1f1d1b]/15 pl-4 text-[12.5px] leading-[1.6] text-[#1f1d1b]/50">
      {children}
    </p>
  );
}

function StudyLabel({ n, name }: { n: string; name: string }) {
  return (
    <p className="mx-auto mb-4 max-w-2xl text-[10.5px] uppercase tracking-[0.26em] text-[#1f1d1b]/40">
      Study {n} — {name}
    </p>
  );
}

function P({ children }: { children: React.ReactNode }) {
  return (
    <p className="mt-6 font-serif text-[18px] leading-[1.75] text-[#1f1d1b]/85 first:mt-0">
      {children}
    </p>
  );
}

function Caption({ children }: { children: React.ReactNode }) {
  return (
    <figcaption className="mt-3 text-center font-serif text-[13px] italic leading-[1.5] text-[#1f1d1b]/45">
      {children}
    </figcaption>
  );
}

function Divider() {
  return (
    <div
      aria-hidden
      className="mx-auto my-24 h-px w-10 bg-[#1f1d1b]/15 sm:my-32"
    />
  );
}

export default function IllustrationFlowStudies() {
  return (
    <main className="relative z-10 min-h-screen px-6 pb-40 pt-16 text-[#1f1d1b] sm:px-8">
      {/* ---------- Page intro ---------- */}
      <header className="mx-auto mb-20 max-w-2xl text-center">
        <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/45">
          Local brainstorm
        </p>
        <h1 className="mt-5 font-serif text-[clamp(2rem,4vw,2.75rem)] font-normal italic leading-[1.1] text-[#2b1f17]">
          Illustration in flow.
        </h1>
        <p className="mx-auto mt-6 max-w-xl font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/60">
          Five ways a drawing can sit inside the reading instead of
          stopping it. One drawing, used five ways — placement studies,
          not final art.
        </p>
      </header>

      {/* ========== STUDY 1 — The plate ========== */}
      <section>
        <StudyLabel n="1" name="The plate" />
        <Note>
          The base case. A drawing at full reading width, edges
          dissolved into the paper, a quiet caption, text resuming
          underneath. Reads like a plate in a well-set book — a breath,
          not a billboard.
        </Note>
        <article className="mx-auto max-w-2xl">
          <P>
            In January the house was a set of intentions. The chair
            angled toward the window for the reading you meant to do. The
            corner cleared for the practice you were going to keep. The
            table you imagined full.
          </P>
          <figure className="my-10">
            <Image
              src={SRC}
              alt=""
              width={1536}
              height={1024}
              style={featherAll}
              className="h-auto w-full"
              priority
            />
            <Caption>June is evidence.</Caption>
          </figure>
          <P>
            The chair, it turns out, is where you actually sit, though
            rarely for the reason you bought it. The corner stayed
            cleared and stayed empty. None of this announced itself. It
            accumulated quietly, the way dust settles on the surfaces you
            stopped touching.
          </P>
        </article>
      </section>

      <Divider />

      {/* ========== STUDY 2 — The margin vignette ========== */}
      <section>
        <StudyLabel n="2" name="The margin vignette" />
        <Note>
          A smaller drawing pulled into the outer margin beside the
          column. Because it dissolves into the paper it doesn&rsquo;t
          fight the text — it sits in the white space the way a marginal
          sketch sits in a notebook. Stacks above the text on mobile.
        </Note>
        <div className="mx-auto grid max-w-5xl grid-cols-1 items-center gap-x-12 gap-y-8 md:grid-cols-[1fr_minmax(0,34rem)]">
          <Image
            src={SRC}
            alt=""
            width={1536}
            height={1024}
            style={featherAll}
            className="order-1 h-auto w-full md:order-none"
          />
          <article>
            <P>
              Some things survived without your protection. A route your
              feet learned before you decided to walk it. A cup that
              migrated to the same spot every morning and stayed.
            </P>
            <P>
              You never defended any of these. They earned the house by
              being used, which is the only test that holds.
            </P>
          </article>
        </div>
      </section>

      <Divider />

      {/* ========== STUDY 4 — The soft bleed ========== */}
      <section>
        <StudyLabel n="4" name="The soft bleed" />
        <Note>
          The reformed full-bleed. The drawing runs off one page edge
          but feathers into cream on the inner side — wide and
          atmospheric without the cinematic drama, because nothing is
          framed or hard-cropped. The honest version of the old arc.
        </Note>
        <figure className="relative">
          <div className="ml-auto w-[min(100%,1100px)]">
            <Image
              src={SRC}
              alt=""
              width={1536}
              height={1024}
              style={featherBleedRight}
              className="h-auto w-full"
            />
          </div>
          <figcaption className="mx-auto mt-6 max-w-2xl text-center font-serif text-[13px] italic leading-[1.5] text-[#1f1d1b]/45">
            The light goes. The rooms remain.
          </figcaption>
        </figure>
      </section>

      <Divider />

      {/* ========== STUDY 5 — The opening pairing ========== */}
      <section>
        <StudyLabel n="5" name="The opening pairing" />
        <Note>
          A drawing beside the opening lines of a piece — a chapter head.
          Image and first words arrive together, so the drawing reads as
          part of the writing rather than decoration bolted above it.
        </Note>
        <div className="mx-auto grid max-w-5xl grid-cols-1 items-end gap-x-12 gap-y-8 md:grid-cols-2">
          <article>
            <p className="text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/40">
              Practice — Reflection
            </p>
            <h2 className="mt-5 font-serif text-[clamp(1.875rem,3.2vw,2.5rem)] font-normal italic leading-[1.12] text-[#2b1f17]">
              Half revealed.
            </h2>
            <p className="mt-5 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/70">
              In January we are designing a house. In June we are
              discovering which rooms we actually live in.
            </p>
          </article>
          <Image
            src={SRC}
            alt=""
            width={1536}
            height={1024}
            style={featherAll}
            className="h-auto w-full"
          />
        </div>
      </section>

      <footer className="mx-auto mt-32 max-w-2xl text-center text-[12px] leading-[1.6] text-[#1f1d1b]/40">
        Same drawing in all five. Tell me which placements feel right and
        I&rsquo;ll fold the keepers into the homepage flow — and we can
        spec the real drawings each slot needs.
      </footer>
    </main>
  );
}
