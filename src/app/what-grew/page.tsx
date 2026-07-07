import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "What grew. — Hessentials",
  description:
    "In spring it was a plan on paper. By July, the conditions have answered.",
  alternates: {
    canonical: "/what-grew",
  },
};

/**
 * What grew. — long-form editorial.
 *
 * July cover story. The sequel to /half-revealed: June discovered which
 * rooms you actually live in; July walks out to the yard and reads what
 * the heat kept. Architecture mirrors /half-revealed exactly:
 * - Centered, max-w-2xl reading column
 * - Sentence-case H1 (matches the cover title exactly: "What grew.")
 * - Italic-serif standfirst (the cover dek runs as the deck)
 * - Local Body / P / PullQuote primitives, same reading rhythm
 * - One PullQuote: the pivot line that echoes the title
 * - Inline byline ("By Jordan Hess") — sentence case, no uppercase
 *
 * Rendering rules carried from the cover-essay house style:
 * - Sentence case preserved exactly in the H1 and throughout.
 * - Italics: the standfirst and the pull quote only (per Jordan's revision,
 *   emphasis is carried by isolated one-line paragraphs, not inline <em>).
 * - NO em dashes in body copy (Amendment II). The only em dash is the
 *   byline attribution ("— Jordan Hess"), a structural separator.
 * - Houston-July honesty: the heat does not lift at night, watering is at
 *   dusk, midday burns it off. No open-window / cool-evening imagery.
 * - This page is JSX, not markdown. Apostrophes are explicit &rsquo;
 *   entities (house typographic style); no smart-punctuation pipeline runs.
 */
export default function WhatGrewArticle() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        {/* ---------- Header ---------- */}
        <header className="mb-20 text-center md:mb-28">
          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal italic leading-[1.06] tracking-[-0.022em] text-balance text-[#2b1f17]">
            What grew.
          </h1>
          <p className="text-pretty mx-auto mt-10 max-w-xl font-serif text-[clamp(1.125rem,1.6vw,1.3rem)] italic leading-[1.55] text-[#1f1d1b]/70">
            In spring it was a plan on paper. By July, the conditions have
            answered.
          </p>
        </header>

        {/* ---------- Body ---------- */}
        <Body>
          <P>
            In spring you decide what the yard will be. You read the light
            generously, the way you read most plans at the start, and you
            put the thing you love where you want to see it rather than
            where it wants to stand. Spring lets you believe this will
            work, because nothing has been asked of it yet.
          </P>
          <P>July asks.</P>
          <P>
            By now the heat has been sitting on the yard for weeks and it
            does not lift at night. You water at dusk because anything you
            give it at noon is gone before it reaches the root. You have
            stopped checking the plan. You go out to see what is still
            standing.
          </P>
          <P>
            That is a different question than the one you asked in April,
            and a more honest one.
          </P>
          <P>
            Some of it thrived on neglect. The plant you pushed into the
            hard corner and forgot, the one you had no particular hope for,
            has taken the spot and held it through the worst of the heat.
            It never wanted the attention you were rationing. It wanted
            what that corner happened to have, and the corner had it, and
            that was the whole of the arrangement.
          </P>
          <P>Some of it you tended every day and it died anyway.</P>
          <P>Not because you neglected it.</P>
          <P>
            You gave it water and shade and the wrong ground, and no amount
            of tending stands in for the one thing it needed and could not
            get from you.
          </P>
          <P>Care is not a condition.</P>
          <P>It cannot substitute for one.</P>
          <P>A thing planted in the wrong conditions has not failed.</P>
          <P>It has told you the conditions were wrong.</P>
          <P>
            That is information, and it is the only kind the yard gives away
            for free. You can move it in the fall. You can stop planting it.
            What you cannot do is water it into loving a place it was never
            going to love.
          </P>
          <P>
            The habit you assumed would take discipline wanted only a place
            to happen, and it happens now without being asked. The one you
            scheduled and defended and set where you would see it never
            took.
          </P>
          <P>You know what actually grew by what you no longer manage.</P>
          <P>It runs on its own conditions.</P>
          <P>The season does not ask which you preferred.</P>

          <PullQuote>
            The question was never what you planted. It was what the ground
            would keep.
          </PullQuote>

          <P>
            The heat is not going anywhere. It will sit on the yard through
            September, and it will keep favoring what it favored. You can
            argue with that, or you can plant into it.
          </P>
          <P>You know the ground now.</P>
          <P>Spring could not tell you.</P>
          <P>July did.</P>
        </Body>

        {/* Inline byline — sentence case, no CSS uppercase transform.
            Attribution dash per Jordan's revision (structural separator,
            not body copy; note this differs from /half-revealed's "By"). */}
        <p className="mt-16 font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
          — Jordan Hess
        </p>

        {/* ---------- Bottom — quiet exit ---------- */}
        <nav
          aria-label="Onward"
          className="mx-auto mt-32 max-w-2xl text-center sm:mt-40 md:mt-48"
        >
          <Link
            href="/"
            className="inline-flex items-baseline gap-2 text-[10px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 transition-colors duration-500 ease-out hover:text-[#1f1d1b]/80 sm:text-[11px]"
          >
            <span aria-hidden>&larr;</span>
            Hessentials
          </Link>
        </nav>
      </article>
    </main>
  );
}

// ---------- Typography primitives ----------

function Body({ children }: { children: React.ReactNode }) {
  return (
    <div className="font-serif text-[18px] leading-[1.75] text-[#1f1d1b]/85 sm:text-[19px] sm:leading-[1.7]">
      {children}
    </div>
  );
}

function P({ children }: { children: React.ReactNode }) {
  return <p className="mt-6 first:mt-0">{children}</p>;
}

function PullQuote({ children }: { children: React.ReactNode }) {
  return (
    <blockquote className="mx-auto my-14 max-w-md text-center font-serif text-[clamp(1.375rem,2vw,1.5rem)] italic leading-[1.35] tracking-[-0.005em] text-[#2b1f17] sm:my-16">
      {children}
    </blockquote>
  );
}
