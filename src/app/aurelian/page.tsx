import type { Metadata } from "next";
import BigThree from "../../components/BigThree";

export const metadata: Metadata = {
  title: "Aurelian — Hessentials",
  description:
    "Aurelian is the interpretive layer of Hessentials. Astrology used as a behavioral framework — timing, pressure, instinct, emotional regulation, and the gap between how someone appears and how they actually operate inside.",
};

const PATTERN_LIBRARY = [
  {
    name: "Fast Surface, Slow Interior",
    body:
      "This is the pattern of someone who appears ready before they actually are. The room reads confidence, or speed, or composure. Inside, they're still catching up to what the surface already showed.",
  },
  {
    name: "High Standards, Quiet Pressure",
    body:
      "This pattern creates competence that looks effortless from the outside. The cost is internal pressure no one sees because the person has learned to make strain look organized.",
  },
  {
    name: "Early Yes, Late Cost",
    body:
      "This is the pattern of agreeing in the moment and negotiating with yourself afterward. The room arrives faster than the inside does.",
  },
  {
    name: "Stable Until It Isn't",
    body:
      "This pattern can hold more than most people realize. The issue is not weakness. It's delayed response. By the time it shows on the outside, the threshold has already been crossed.",
  },
  {
    name: "Precision Under Pressure",
    body:
      "This pattern tries to create order before it feels safe to move. It can produce excellent judgment, but it can also turn every decision into a test of readiness.",
  },
  {
    name: "The Arrival Gap",
    body:
      "This is the distance between how someone is first experienced and what is actually happening underneath. Most relational confusion begins here.",
  },
] as const;

const NOTES = [
  "Most people do not struggle with decisions. They struggle with timing their decisions to their actual readiness.",
  "Being understood too quickly can feel just as exposing as being misunderstood.",
  "The first version people meet is not always the version making the decision.",
  "A pattern does not need to be dramatic to be expensive.",
  "Pressure often disguises itself as urgency.",
  "You can be clear and still not be ready.",
  "The body usually knows the cost before the mind admits the agreement was premature.",
  "Some people are not inconsistent. They are translating between systems inside themselves.",
  "The goal is not to become easier to read. The goal is to stop misreading yourself.",
] as const;

export default function AurelianPage() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Section 1: Top entrance ---------- */}
      <section className="mx-auto w-full max-w-[36rem] px-6 pt-16 text-center sm:pt-24 md:pt-28">
        <p className="mb-10 text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/45 sm:text-[12px]">
          Aurelian
        </p>

        <h1 className="font-serif text-[clamp(2.5rem,6vw,4.25rem)] font-normal leading-[1] tracking-[-0.025em] text-balance text-[#1f1d1b]">
          Aurelian
        </h1>

        <p className="mx-auto mt-10 max-w-[30rem] font-serif text-[clamp(1.125rem,1.6vw,1.25rem)] italic leading-[1.55] text-[#1f1d1b]/70">
          Astrology, used to read how you actually operate. Not how you
          describe yourself.
        </p>
      </section>

      {/* ---------- Section 2 + 3: Calculator ---------- */}
      <section
        id="big-three"
        aria-labelledby="big-three-heading"
        className="mx-auto w-full max-w-4xl px-6 pt-24 sm:px-10 md:pt-32"
      >
        <div className="mb-12 text-center md:mb-16">
          <h2
            id="big-three-heading"
            className="mb-10 font-serif text-[clamp(2rem,4vw,2.75rem)] font-normal leading-[1.05] tracking-[-0.02em] text-balance"
          >
            Your Big Three
          </h2>
          <p className="text-pretty mx-auto max-w-xl font-serif text-[18px] italic leading-[1.6] text-[#1f1d1b]/70 sm:text-[19px]">
            Sun is direction. Moon is inner rhythm. Rising is how the world
            meets you. Select what you know. Aurelian will read what&rsquo;s
            there.
          </p>
        </div>

        <BigThree />
      </section>

      {/* ---------- Section 5: Pattern Library ---------- */}
      <section
        id="pattern-library"
        aria-labelledby="pattern-library-heading"
        className="mx-auto w-full max-w-6xl px-6 pt-24 sm:px-10 md:pt-32"
      >
        <div className="text-center">
          <h2
            id="pattern-library-heading"
            className="font-serif text-[clamp(2rem,4vw,2.75rem)] font-normal leading-[1.05] tracking-[-0.02em] text-balance"
          >
            The Pattern Library
          </h2>
          <p className="mx-auto mt-6 max-w-xl text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/55 sm:text-[12px]">
            Short studies in behavior, timing, and pressure.
          </p>
        </div>

        <ul className="mx-auto mt-14 grid max-w-5xl grid-cols-1 gap-x-12 gap-y-12 sm:mt-16 sm:grid-cols-2 sm:gap-x-14 sm:gap-y-14 lg:grid-cols-3 lg:gap-x-16">
          {PATTERN_LIBRARY.map((entry) => (
            <li key={entry.name}>
              <p className="mb-2 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
                Pattern
              </p>
              <h3 className="mb-3 font-serif text-[clamp(1.25rem,2vw,1.5rem)] font-normal leading-[1.2] tracking-[-0.015em] text-[#1f1d1b]">
                {entry.name}
              </h3>
              <p className="text-pretty text-[15px] leading-[1.65] text-[#1f1d1b]/80 sm:text-[16px]">
                {entry.body}
              </p>
            </li>
          ))}
        </ul>
      </section>

      {/* ---------- Section 6: Notes from Aurelian ---------- */}
      <section
        id="notes"
        aria-labelledby="notes-heading"
        className="mx-auto w-full max-w-5xl px-6 pt-24 pb-32 text-center sm:px-10 md:pt-32 md:pb-40"
      >
        <h2
          id="notes-heading"
          className="font-serif text-[clamp(2rem,4vw,2.75rem)] font-normal leading-[1.05] tracking-[-0.02em] text-balance"
        >
          Notes from Aurelian
        </h2>
        <p className="mx-auto mt-6 max-w-lg text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/55 sm:text-[12px]">
          Field notes on timing, perception, pressure, and self-recognition.
        </p>

        <div className="mx-auto mt-14 grid max-w-4xl grid-cols-1 gap-x-12 gap-y-10 text-left text-[16px] leading-[1.65] text-[#1f1d1b]/80 sm:mt-16 sm:grid-cols-2 sm:gap-x-14 sm:gap-y-12 sm:text-[17px]">
          {NOTES.map((note) => (
            <p key={note} className="text-pretty">
              {note}
            </p>
          ))}
        </div>
      </section>
    </main>
  );
}
