import { CURRENT_READING } from "../data/aurelian-weekly";

/**
 * Aurelian — This Week.
 *
 * A non-interactive weekly reading that sits alongside the Big Three
 * tool. The Big Three reads the person; this reads the week. Both
 * apply the same framework, and they coexist on the page.
 *
 * Editorial container: max-w-[36rem] for a single readable column,
 * centered. Eyebrow naming the section, italic serif headline below,
 * body paragraphs in the same prose treatment used in the Notes
 * section so the Aurelian voice is consistent across blocks.
 */
export default function AurelianWeekly() {
  const { range, headline, paragraphs } = CURRENT_READING;

  return (
    <section
      id="this-week"
      aria-labelledby="this-week-heading"
      className="mx-auto w-full max-w-[36rem] px-6 pt-24 sm:px-10 md:pt-32"
    >
      <div className="flex flex-col items-center text-center">
        {/* Hairline above the section eyebrow (§2.2). */}
        <span
          aria-hidden
          className="block w-20"
          style={{ height: "0.5px", backgroundColor: "#c8bfae" }}
        />
        <p className="mt-6 text-[11px] uppercase tracking-[0.3em] text-[#1f1d1b]/55 sm:text-[12px]">
          This Week
        </p>
        <p className="mt-3 text-[10.5px] uppercase tracking-[0.26em] text-[#1f1d1b]/40 sm:text-[11px]">
          {range}
        </p>

        <h2
          id="this-week-heading"
          className="text-balance mt-10 font-serif text-[clamp(1.625rem,3vw,2.125rem)] font-normal italic leading-[1.25] tracking-[-0.015em] text-[#1f1d1b]"
        >
          {headline}
        </h2>
      </div>

      <div className="mx-auto mt-12 max-w-[34rem] space-y-6 text-[16px] leading-[1.7] text-[#1f1d1b]/85 sm:mt-14 sm:space-y-7 sm:text-[17px]">
        {paragraphs.map((p, i) => (
          <p key={i} className="text-pretty">
            {p}
          </p>
        ))}
      </div>
    </section>
  );
}
