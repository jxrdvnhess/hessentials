import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mother's Day — Hessentials",
  description:
    "Most Mother's Day plans swing between overdone and forgettable. This is the third option.",
};

/**
 * Mother's Day — long-form editorial.
 *
 * Standalone seasonal piece (not part of the Living markdown system).
 * The brief specifies tight typographic control — section headers
 * restrained, two specific pull quotes, image at the section break
 * before "The table." — so this is rendered as explicit React markup
 * rather than markdown to keep that control intact.
 *
 * No sidebars, no related-content rail. The piece ends; the reader
 * either clicks something in the masthead nav or they don't.
 */
export default function MothersDayArticle() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        {/* ---------- Header ---------- */}
        <header className="mb-20 text-center md:mb-28">
          <p className="mb-10 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
            Mother&rsquo;s Day
          </p>
          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal italic leading-[1.06] tracking-[-0.022em] text-balance text-[#2b1f17]">
            Not a gift guide. A better way to get it right.
          </h1>
          <p className="text-pretty mx-auto mt-10 max-w-xl font-serif text-[clamp(1.125rem,1.6vw,1.3rem)] italic leading-[1.55] text-[#1f1d1b]/70">
            Most Mother&rsquo;s Day plans swing between overdone and
            forgettable. This is the third option.
          </p>
        </header>

        {/* ---------- Body ---------- */}
        <Body>
          <P>
            Most Mother&rsquo;s Day plans miss in the same predictable ways.
            They either try too hard &mdash; reservations, flowers, gifts
            stacked on top of each other &mdash; or they don&rsquo;t try at
            all and call it &ldquo;keeping it simple.&rdquo;
          </P>
          <P>Neither is thoughtful. One is loud. The other is lazy.</P>
          <P>
            There&rsquo;s a third option. It&rsquo;s quieter, more specific,
            and it tends to work better.
          </P>

          <SectionHeader>
            The problem isn&rsquo;t effort. It&rsquo;s attention.
          </SectionHeader>
          <P>
            Most people think this day is about effort. It&rsquo;s not.
            It&rsquo;s about whether you paid attention in the weeks leading
            up to it.
          </P>
          <P>
            The thing she ordered once on a trip and mentioned twice
            afterward. The book she keeps picking up at the store and
            putting back down. The chair she sits in to read that needs a
            better lamp. The morning routine that quietly breaks down
            before anyone else is awake.
          </P>
          <P>
            Mother&rsquo;s Day isn&rsquo;t a stage. It&rsquo;s a correction.
          </P>
          <P>If it feels generic, it is.</P>

          <SectionHeader>The binary that ruins the day.</SectionHeader>
          <P>
            Most plans fall into one of two categories. Overdone:
            reservations, crowded rooms, too many moving parts, a schedule
            someone has to manage. Underdone: &ldquo;just relax,&rdquo; but
            nothing has actually been handled, so the relaxing becomes its
            own kind of work.
          </P>
          <P>Both create work. Just in different ways.</P>
          <P>
            The third stance is simple. Remove friction. Add one or two
            things that feel considered. Stop there.
          </P>
          <P>
            A gift, if there is one, should feel like recognition rather
            than obligation. Something that improves a daily ritual.
            Something she mentioned once and forgot. A printed version of a
            recipe she makes from memory, typeset and archived. A well-made
            object that replaces a worn-out one she uses every morning. The
            book she put back at the store.
          </P>
          <P>
            What doesn&rsquo;t work is anything that could have been given
            to anyone else. Bundles. Panic purchases. The pre-built
            Mother&rsquo;s Day edit from a brand that does not know her.
          </P>

          <PullQuote>
            A good gift doesn&rsquo;t impress her. It tells her you were
            paying attention.
          </PullQuote>

          <SectionHeader>The table.</SectionHeader>

          {/* Image — placed at the section break, per brief. */}
          <figure className="my-12 -mx-6 sm:-mx-8 md:my-16 md:mx-0">
            <div className="relative aspect-[3/2] w-full overflow-hidden">
              <Image
                src="/mothers-day-table.jpg"
                alt=""
                fill
                sizes="(min-width: 768px) 672px, 100vw"
                quality={92}
                className="object-cover"
              />
            </div>
          </figure>

          <P>This is enough.</P>
          <P>
            Not a full production. Not a reservation you had to fight for.
            A table that&rsquo;s ready before she thinks to ask. Something
            warm. Something fresh. Bread, properly served. A seat she can
            walk into without adjusting anything.
          </P>
          <P>No chaos. No performance.</P>
          <P>
            The goal isn&rsquo;t to impress her. It&rsquo;s to make sitting
            down feel easy.
          </P>

          <SectionHeader>The invisible work.</SectionHeader>
          <P>
            This is what people skip, and it&rsquo;s the only part that
            matters.
          </P>
          <P>
            The kitchen is already handled before she walks in. The laundry
            isn&rsquo;t sitting where she&rsquo;ll see it. The small
            annoying thing she was going to do today &mdash; the one
            she&rsquo;s been carrying for two weeks &mdash; is already
            done. None of it is announced. None of it is pointed out. It
            just isn&rsquo;t waiting for her.
          </P>

          <PullQuote>
            Relief is a luxury. Most people overlook it because it
            doesn&rsquo;t photograph well.
          </PullQuote>

          <SectionHeader>
            Respond to the person, not the role.
          </SectionHeader>
          <P>
            There&rsquo;s no universal version of this day. The person who
            values control doesn&rsquo;t want surprises. The person
            who&rsquo;s overstimulated doesn&rsquo;t want noise. The person
            who loves beauty doesn&rsquo;t want more &mdash; she wants
            better. The person who values time doesn&rsquo;t want filler.
          </P>
          <P>
            Most people celebrate the role. The ones who get it right
            respond to the individual.
          </P>

          {/* Closing rule + final paragraphs. */}
          <hr
            aria-hidden
            className="mx-auto my-16 w-12 border-0 sm:my-20"
            style={{ height: "0.5px", backgroundColor: "rgba(31,29,27,0.3)" }}
          />

          <P>
            Most people will either do too much or not enough. If you remove
            what doesn&rsquo;t matter and get a few things right, it lands
            better than anything elaborate ever will.
          </P>
          <P>
            One good decision, executed well, beats five average ones.
          </P>
        </Body>

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
  // Generous line height, comfortable measure (~65-75 chars at this
  // type size and column width). Serif body throughout — same family
  // as the H1, slightly heavier weight than italic for read.
  return (
    <div className="font-serif text-[18px] leading-[1.75] text-[#1f1d1b]/85 sm:text-[19px] sm:leading-[1.7]">
      {children}
    </div>
  );
}

function P({ children }: { children: React.ReactNode }) {
  // Standard editorial paragraph spacing — a beat between paragraphs
  // that lets short standalone lines (e.g., "Mother's Day isn't a
  // stage. It's a correction.") read as deliberate punctuation.
  return <p className="mt-6 first:mt-0">{children}</p>;
}

function SectionHeader({ children }: { children: React.ReactNode }) {
  // Restrained per brief — italic serif, body-adjacent size. Not an
  // all-caps banner, not numbered. Generous space above to mark the
  // turn; modest space below so the next paragraph reads as the
  // section's first beat.
  return (
    <h2 className="text-balance mt-16 mb-6 font-serif text-[clamp(1.25rem,1.7vw,1.5rem)] font-normal italic leading-[1.3] text-[#2b1f17] sm:mt-20">
      {children}
    </h2>
  );
}

function PullQuote({ children }: { children: React.ReactNode }) {
  // Italic serif, larger than body, generous whitespace, no decorative
  // marks or rules. Same visual logic as the AurelianThisWeekPanel
  // excerpt on the homepage. Centered with restrained max-width so it
  // sits as a deliberate beat in the column.
  return (
    <blockquote className="mx-auto my-14 max-w-md text-center font-serif text-[clamp(1.375rem,2vw,1.5rem)] italic leading-[1.35] tracking-[-0.005em] text-[#2b1f17] sm:my-16">
      {children}
    </blockquote>
  );
}
