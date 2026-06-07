import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Half revealed. — Hessentials",
  description:
    "In January we are designing a house. In June we are discovering which rooms we actually live in.",
  alternates: {
    canonical: "/half-revealed",
  },
};

/**
 * Half revealed. — long-form editorial.
 *
 * Midyear Practice piece. Architecture mirrors /memorial-day:
 * - Centered, max-w-2xl reading column
 * - Sentence-case H1
 * - Italic-serif standfirst (the block lede also runs as the deck)
 * - Body uses local Body / P / PullQuote primitives so the reading
 *   rhythm matches the rest of the editorial series
 * - One PullQuote: the pivot line that echoes the title
 * - Inline byline ("By Jordan Hess") — sentence case, no uppercase
 *   transform, matching the Memorial Day render
 *
 * Rendering rules carried from the brief:
 * - Sentence case preserved exactly in the H1 and throughout.
 * - Italics in the copy are intentional editorial emphasis and render
 *   as italic serif (inline <em> and the standalone pivot line).
 * - There are NO em dashes and NO all-caps in this copy by design.
 *   None are introduced here.
 * - This page is JSX, not markdown. Apostrophes are explicit &rsquo;
 *   entities (house typographic style, matching /memorial-day); no
 *   smart-punctuation pipeline runs against this file.
 */
export default function HalfRevealedArticle() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        {/* ---------- Header ---------- */}
        <header className="mb-20 text-center md:mb-28">
          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal italic leading-[1.06] tracking-[-0.022em] text-balance text-[#2b1f17]">
            Half revealed.
          </h1>
          <p className="text-pretty mx-auto mt-10 max-w-xl font-serif text-[clamp(1.125rem,1.6vw,1.3rem)] italic leading-[1.55] text-[#1f1d1b]/70">
            In January we are designing a house. In June we are
            discovering which rooms we actually live in.
          </p>
        </header>

        {/* ---------- Body ---------- */}
        <Body>
          <P>
            By June the light stays late, and it fills the house
            differently than it did in winter. The windows are open.
            Something in the garden has grown past the point you planned
            for. You walk through the rooms near dusk, not looking for
            anything in particular, and you see them as they are.
          </P>
          <P>
            In January the house was a set of intentions. The chair
            angled toward the window for the reading you meant to do. The
            corner cleared for the practice you were going to keep. The
            table you imagined full. <em>January is imagination.</em>{" "}
            Everything in it is still possible, because nothing in it has
            happened yet.
          </P>
          <P>June is evidence.</P>
          <P>
            The chair, it turns out, is where you actually sit, though
            rarely for the reason you bought it. The corner stayed cleared
            and stayed empty. The table has its real history now, the
            nights that filled it and the nights it waited. None of this
            announced itself. It accumulated quietly, the way dust settles
            on the surfaces you stopped touching and keeps off the ones
            you reach for without thinking.
          </P>
          <P>
            This is not an audit. An audit asks whether you hit the
            number. A house only shows you where the year actually went.{" "}
            <em>
              What did you keep when no one was watching to see if you
              kept it.
            </em>
          </P>
          <P>
            Some things survived without your protection. A route your
            feet learned before you decided to walk it. A cup that
            migrated to the same spot every morning and stayed. A song you
            did not so much choose as fail to skip, a hundred mornings
            running. And a conversation that returns to you at odd hours,
            still unfinished, that you did not plan to keep and cannot put
            down. You never defended any of these. They earned the house
            by being used, which is the only test that holds.
          </P>
          <P>
            Other rooms were staged and never lived in, and you can tell
            by the stiffness. The shelf arranged for a version of yourself
            you admired from across a distance and never became. The
            discipline that fit someone else&rsquo;s hands. The plan that
            was correct in every respect except that it was never yours.
            These did not fail. They were never alive to begin with, and
            June is honest about the difference.
          </P>
          <P>
            And some things fit once and no longer do. A door you keep
            opening out of habit into a room you have already left. A fear
            that felt load-bearing in January and turns out to have been
            holding nothing up. Growth is seldom the addition you
            pictured. More often it is a subtraction you notice only when
            you reach for something and find you set it down months ago.
          </P>
          <P>
            Not all of it is light. Some rooms are quieter than they were,
            and you know why. Some hold a weight you were not carrying when
            the year began. And here and there, against everything you
            planned, a room you never thought to furnish has become the one
            you keep returning to. The year did not consult you. It rarely
            does.
          </P>

          <PullQuote>
            The year isn&rsquo;t half over. It&rsquo;s half revealed.
          </PullQuote>

          <P>
            The light goes. The rooms remain. Some are fuller than you
            expected. Some are emptier. Some have changed their purpose
            entirely.
          </P>
          <P>
            But they are no longer imagined rooms. They are yours.
          </P>
          <P>
            What you do with that knowledge is the rest of the year.
          </P>
        </Body>

        {/* Inline byline — sentence case, no CSS uppercase transform,
            matching the Memorial Day render. */}
        <p className="mt-16 font-serif text-[15px] italic leading-[1.55] text-[#1f1d1b]/55 sm:text-[16px]">
          By Jordan Hess
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
