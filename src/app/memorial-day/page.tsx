import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Memorial Day — Hessentials",
  description:
    "Memorial Day arrives after the season has already started. The day the calendar catches up.",
};

/**
 * Memorial Day — long-form editorial.
 *
 * Standalone seasonal piece. Architecture mirrors /mothers-day:
 * - Centered, max-w-2xl reading column
 * - Sentence-case H1 (no eyebrow — H1 opens with "Memorial Day.")
 * - Italic-serif standfirst
 * - Body uses local P / SectionHeader / PullQuote primitives so the
 *   reading rhythm matches the rest of the editorial series
 * - Section headers sentence case with periods, never CSS-uppercased
 * - Two pull quotes (red/white/blue + closing)
 * - Literal "———" typographic break before the close
 * - Inline byline ("By Jordan Hess") — sentence case, no uppercase
 *   transform per brief. Diverges from the shared Byline component
 *   on purpose so Mother's Day's existing render is untouched.
 *
 * No in-body figure: the new body does not have a "table" anchor, so
 * an image inside the column would feel arbitrary. The homepage
 * MemorialDayModule carries the image.
 *
 * Rendering note: this page is JSX, not markdown. Em dashes are
 * explicit &mdash; entities and apostrophes are &rsquo; — no
 * smart-punctuation pipeline runs against this file.
 */
export default function MemorialDayArticle() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        {/* ---------- Header ---------- */}
        <header className="mb-20 text-center md:mb-28">
          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal italic leading-[1.06] tracking-[-0.022em] text-balance text-[#2b1f17]">
            Memorial Day. Not the start of summer.
          </h1>
          <p className="text-pretty mx-auto mt-10 max-w-xl font-serif text-[clamp(1.125rem,1.6vw,1.3rem)] italic leading-[1.55] text-[#1f1d1b]/70">
            The day the calendar catches up.
          </p>
        </header>

        {/* ---------- Body ---------- */}
        <Body>
          <P>
            Memorial Day arrives after the season has already started. The
            pool has been open for two weeks in Atlanta. The grass has been
            cut three times in the Northeast. In Houston, every door has
            been propped open for a month. The calendar&rsquo;s start date
            isn&rsquo;t a real start date. It&rsquo;s just a date.
          </P>
          <P>
            What the weekend actually is: the first day you&rsquo;ll host
            the season you&rsquo;ve already been living in.
          </P>
          <P>That distinction is the whole article.</P>

          <SectionHeader>The day moves where the weather is.</SectionHeader>
          <P>
            Some Memorial Days happen on the patio. Some happen entirely
            inside, with the AC set to seventy-two and the back doors
            swinging open every twenty minutes. Both are correct.
          </P>
          <P>
            The mistake is fighting the weather. A 98&deg; afternoon in
            Houston is not a patio day no matter how committed you are to
            the cookout idea. Set up inside. Let the grill be a quick
            out-and-back. Keep the windows open so the day still smells
            like outside. Fresh flowers on every surface that catches
            light.
          </P>
          <P>
            The opposite move works in a year when the weather is kind.
            Move the dining room outside. Pull a rug onto the patio if you
            have one. Let the inside of the house go quiet for the
            afternoon.
          </P>
          <P>
            Either way, the day reads as one decision. Pick the room
            before you pick anything else.
          </P>

          <SectionHeader>If there&rsquo;s a pool, that&rsquo;s the anchor.</SectionHeader>
          <P>
            Stage the pool first. Set up there harder than you set up
            anywhere else. A real bar with ice, glasses, and three or four
            things people can pour without asking. A platter of light
            bites that doesn&rsquo;t need refrigeration for two hours.
            Towels stacked somewhere visible, not buried in a closet
            anyone has to ask about.
          </P>
          <P>
            Trash cans where people would already look for one. Beside the
            bar. Near the chairs. Not tucked behind a hedge for aesthetic
            reasons that cost you the floor on cleanup.
          </P>
          <P>
            The point is that the pool becomes a place the host
            doesn&rsquo;t have to host. Guests serve themselves. They use
            the towels. They sort their own trash. The kitchen becomes
            yours again, which is how you cook a meal worth eating
            without a sweat ring on your shirt by four.
          </P>

          <SectionHeader>The spread.</SectionHeader>
          <P>
            No tradition required. Pick the meats that are exciting to you
            this year and cook them however the setting allows. Brisket if
            you have the patience. Whole fish if you trust your
            fishmonger. A pile of bone-in chicken thighs if the day is
            moving inside and you need a roast that takes care of itself.
            The point is to be inspired, not loyal to a script.
          </P>
          <P>
            The one fixed thing on the table is beans. Baked beans,
            always. A second pot of something with beans in it if the
            spread is large. Beans hold for hours, feed twelve from a
            single pot, and reward whatever you cooked alongside them.
            There is no version of this menu where beans are optional.
          </P>

          <SectionHeader>
            Red, white, and blue, where guests won&rsquo;t expect it.
          </SectionHeader>
          <P>
            The palette is the day&rsquo;s only required nod. The trick
            is where you place it.
          </P>
          <P>
            Not bunting. Not paper flags in the centerpiece. Not the
            tablecloth. The work happens in the accents nobody will name
            out loud but everyone will register.
          </P>
          <P>
            A single navy linen napkin folded into a stack of cream ones.
            A bowl of cherries set beside white peonies and a small
            ceramic vase the color of the deep end. The pitcher you pour
            iced tea from in a glazed cobalt. A red enamel pot of beans
            on a trivet that&rsquo;s nothing special.
          </P>

          <PullQuote>
            The palette as a wink, not a costume.
          </PullQuote>

          <P>
            The day reads as Memorial Day without ever announcing itself.
          </P>

          <SectionHeader>The kit.</SectionHeader>
          <P>
            Six things earn the summer. Buy them once, store them
            together, stop thinking about them.
          </P>
          <P>
            Tongs with real spring. The stamped-metal pair from the
            grocery store folds under a steak. A pair with cast joints
            and proper tension lasts a decade. You&rsquo;ll know on the
            first use.
          </P>
          <P>
            One tray you can carry with one hand. Wood, melamine, or
            enameled steel. Not the wide thin plastic kind that flexes
            under a full load.
          </P>
          <P>
            A pitcher you can pour without watching. Ceramic or thick
            glass with a real lip, not a spout that dribbles. The good
            cobalt-glazed ones do double duty as the day&rsquo;s accent
            piece.
          </P>
          <P>
            Cotton napkins. Not paper. They wash. A short stack in solid
            colors with one or two navies and reds tucked in will carry
            every spring and summer event through Labor Day.
          </P>
          <P>
            A vessel that holds ice. Galvanized bucket or enameled
            cooler, not the soft-bag situation that&rsquo;s sweating
            into the rug by three.
          </P>
          <P>
            One long-handled lighter with a working trigger. Lives in the
            same drawer all summer. Not matches. Not a gas-station Bic.
          </P>
          <P>
            And one more thing, if there&rsquo;s a pool: a stack of clean
            cotton towels in plain sight. Bigger than a hand towel,
            smaller than a beach towel. Refilled before the first guest
            arrives.
          </P>

          <SectionHeader>Why this works.</SectionHeader>
          <P>It isn&rsquo;t discipline. It&rsquo;s access.</P>
          <P>
            Anything that requires walking back inside is the friction
            point. The drinks staged at the pool rather than in a cooler
            with a closed lid. The napkins on the table rather than in a
            drawer. The trash where the guest already expects to find
            one. The towel within arm&rsquo;s reach of the chair.
          </P>

          <PullQuote>
            Placement beats intention. Every time.
          </PullQuote>

          <P>
            People assume they need more rigor to use their outside
            space. What they need is a shorter path between the chair and
            the next thing they want.
          </P>

          {/* Typographic break per brief — literal "———" rendered as
              the section divider, not a styled <hr>. */}
          <p
            aria-hidden
            className="my-16 text-center font-serif text-[#1f1d1b]/55 sm:my-20"
          >
            ———
          </p>

          <P>
            Memorial Day isn&rsquo;t the event. It&rsquo;s the setup.
            Stage the day well and the afternoon takes care of itself.
            The backyard, or the kitchen, or the pool, works through
            Labor Day.
          </P>
          <P>One day of staging buys a season.</P>
        </Body>

        {/* Inline byline — sentence case, no CSS uppercase transform
            per brief. Intentionally diverges from the shared Byline
            component (BY JORDAN HESS small caps) so Mother's Day's
            existing render is unaffected. */}
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

function SectionHeader({ children }: { children: React.ReactNode }) {
  // Sentence case in the source text, no CSS text-transform: uppercase.
  // Italic serif at a body-adjacent size — restrained section turn,
  // not an all-caps banner.
  return (
    <h2 className="text-balance mt-16 mb-6 font-serif text-[clamp(1.25rem,1.7vw,1.5rem)] font-normal italic leading-[1.3] text-[#2b1f17] sm:mt-20">
      {children}
    </h2>
  );
}

function PullQuote({ children }: { children: React.ReactNode }) {
  return (
    <blockquote className="mx-auto my-14 max-w-md text-center font-serif text-[clamp(1.375rem,2vw,1.5rem)] italic leading-[1.35] tracking-[-0.005em] text-[#2b1f17] sm:my-16">
      {children}
    </blockquote>
  );
}
