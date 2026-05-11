import Image from "next/image";
import Link from "next/link";
import type { Metadata } from "next";
import Byline from "../../components/Byline";

export const metadata: Metadata = {
  title: "Memorial Day — Hessentials",
  description:
    "Most Memorial Day weekends swing between over-produced and never-happened. The good ones do something else.",
};

/**
 * Memorial Day — long-form editorial.
 *
 * Standalone seasonal piece, same architecture as /mothers-day:
 * - Centered, max-w-2xl reading column
 * - Eyebrow → italic-serif H1 → italic dek header
 * - Body uses the same P / SectionHeader / PullQuote primitives so
 *   the reading rhythm matches the rest of the holiday series
 * - One in-body figure at a section break (per the established
 *   pattern — image earns its place, not decorative)
 * - Closing rule, byline, quiet "← Hessentials" exit
 *
 * No sidebar, no related-content rail. The piece ends.
 */
export default function MemorialDayArticle() {
  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      <article className="mx-auto w-full max-w-2xl px-6 py-20 sm:px-8 md:py-28">
        {/* ---------- Header ---------- */}
        <header className="mb-20 text-center md:mb-28">
          <p className="mb-10 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
            Memorial Day
          </p>
          <h1 className="font-serif text-[clamp(2.25rem,5.5vw,3.75rem)] font-normal italic leading-[1.06] tracking-[-0.022em] text-balance text-[#2b1f17]">
            Not a cookout. The day your backyard starts working.
          </h1>
          <p className="text-pretty mx-auto mt-10 max-w-xl font-serif text-[clamp(1.125rem,1.6vw,1.3rem)] italic leading-[1.55] text-[#1f1d1b]/70">
            Most Memorial Day weekends swing between over-produced and
            never-happened. Neither makes the rest of the summer easier.
          </p>
        </header>

        {/* ---------- Body ---------- */}
        <Body>
          <P>
            Most Memorial Day weekends miss in the same two ways. The
            over-produced cookout &mdash; the marinades, the seven sides, the
            playlist, the host who hasn&rsquo;t sat down by four. Or the
            version where nothing was planned, the chairs are still stacked
            against the wall from October, and someone is sent for bagged
            ice at two-fifteen.
          </P>
          <P>Both feel like work. Neither feels good.</P>
          <P>
            There&rsquo;s a third option. Smaller. More deliberate. And it
            sets up the rest of the summer.
          </P>

          <SectionHeader>The weekend isn&rsquo;t the point.</SectionHeader>
          <P>
            For most of the year, the outside space is a default. A bag of
            charcoal under the table. A chair with the cushion still wet
            from March. A hose kinked since August. Memorial Day is the
            only weekend most people will walk it, notice all of that, and
            decide.
          </P>
          <P>
            Walk it now and the rest of the summer flows. Don&rsquo;t, and
            you&rsquo;ll keep eating inside through July.
          </P>
          <P>
            Treat the day as setup, not event. The afternoon is the
            byproduct.
          </P>

          <SectionHeader>What actually works.</SectionHeader>
          <P>
            Almost nothing about a good afternoon outside has to do with the
            food. It has to do with staging.
          </P>
          <P>
            Set the table before anyone arrives. Not as a flourish &mdash;
            as a release valve. Once it&rsquo;s set, the host is allowed to
            sit, and once the host sits, the room sits with them.
          </P>

          <PullQuote>
            A bare table on Memorial Day is a tell. People feel it before
            they can name it.
          </PullQuote>

          <P>
            Put the drinks and the trash at the edge of the space, not the
            center. Drinks at the edge so people serve themselves and stop
            pulling the host into refills. Trash at the edge so it&rsquo;s
            not the thing people see when they look up from their plate. If
            the can isn&rsquo;t visible from the table, the meal lasts an
            hour longer.
          </P>
          <P>
            Prep one thing the day before. Cold. Done. In a tray you can
            carry one-handed.
          </P>
          <P>
            Cook one thing the day of. Something with a clear finish line.
            Steaks come off when they come off. A whole fish comes off when
            it comes off. Skip the menu with eight finish times.
          </P>
          <P>Don&rsquo;t narrate the meal. The food is already on the table.</P>

          <SectionHeader>The table.</SectionHeader>

          {/* Image — placed at the section break, matching the
              Mother's Day piece's pacing. */}
          <figure className="my-12 -mx-6 sm:-mx-8 md:my-16 md:mx-0">
            <div className="relative aspect-[3/2] w-full overflow-hidden">
              <Image
                src="/memorial-day.jpg"
                alt=""
                fill
                sizes="(min-width: 768px) 672px, 100vw"
                quality={92}
                className="object-cover"
              />
            </div>
          </figure>

          <P>
            Outside, not in. Even if you have to drag the dining table
            through a sliding door. The whole afternoon decides itself in
            the first ten minutes, and ten minutes outdoors reads
            differently than ten minutes in the kitchen.
          </P>
          <P>
            One cloth on it, not three. One vessel of something fresh
            &mdash; herbs from the yard, lemons, a bowl of cherries. Plates
            already out. Glasses already out. Cloth napkins, folded once,
            stacked, not arranged.
          </P>
          <P>
            If anything looks staged, take one thing off.
          </P>

          <SectionHeader>The kit.</SectionHeader>
          <P>
            Six things earn the summer. Buy them once, store them together,
            stop thinking about them.
          </P>
          <P>
            Tongs with real spring. The bent stamped-metal pair from the
            grocery store folds under a steak. A pair with cast joints and
            proper tension lasts a decade. You&rsquo;ll know on the first
            use.
          </P>
          <P>
            One tray you can carry with one hand. Wood, melamine, or
            enameled steel. Not the wide thin plastic kind that flexes when
            it&rsquo;s full. The point of the tray is that it doesn&rsquo;t
            require you to walk twice.
          </P>
          <P>
            A pitcher you can pour without watching. Ceramic or thick glass
            with a real lip &mdash; not a spout that dribbles. An industrial
            aluminum-handled pitcher often beats the photogenic option.
          </P>
          <P>
            Cotton napkins. Not paper. They wash. The first three uses
            justify them.
          </P>
          <P>
            A vessel that holds ice. Galvanized bucket or enameled cooler,
            not the half-melted soft-bag situation that&rsquo;s sweating
            into the rug by hour three.
          </P>
          <P>
            One long-handled lighter with a working trigger. Lives in the
            same drawer all summer. Not matches. Not a gas-station Bic.
          </P>

          <SectionHeader>Why people give up on their own backyards.</SectionHeader>
          <P>
            It isn&rsquo;t laziness. It&rsquo;s access.
          </P>
          <P>
            Anything that requires walking back inside is the friction
            point. The cooler at the door instead of in the kitchen. The
            napkins on the table instead of in the drawer. The lighter
            beside the grill instead of on the counter. Those are not
            aesthetic decisions. They decide whether the afternoon happens
            or not.
          </P>

          <PullQuote>
            Placement beats intention. Every time.
          </PullQuote>

          <P>
            People assume they need more discipline to use their outside
            space. What they need is a shorter path between the chair and
            the next thing they want.
          </P>

          {/* Typographic break per brief — literal "———" rendered
              as the section divider, not a styled <hr>. Generous
              vertical space holds the same visual beat. */}
          <p
            aria-hidden
            className="my-16 text-center font-serif text-[#1f1d1b]/55 sm:my-20"
          >
            ———
          </p>

          <P>
            If you do this right, Memorial Day is not the event. It&rsquo;s
            the setup. The afternoon takes care of itself, and the backyard
            works through Labor Day.
          </P>
          <P>
            One day of staging buys a season of using the outside.
          </P>
        </Body>

        {/* Closing byline. */}
        <Byline />

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
