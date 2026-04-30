import Image from "next/image";
import Byline from "./Byline";
import CopyShoppingList from "./CopyShoppingList";
import type { Recipe as RecipeData, RecipeMeta } from "../types/recipe";

type RecipeProps = {
  recipe: RecipeData;
  className?: string;
};

type MetaItem = { key: string; node: React.ReactNode };

function MetaLine({ meta }: { meta?: RecipeMeta }) {
  const items: MetaItem[] = [];
  if (meta?.serves) items.push({ key: "serves", node: meta.serves });
  if (meta?.time) items.push({ key: "time", node: meta.time });
  if (meta?.yields) items.push({ key: "yields", node: meta.yields });

  if (items.length === 0) return null;

  return (
    <ul className="flex flex-wrap items-center justify-center gap-x-5 gap-y-2 text-[11px] uppercase leading-none tracking-[0.24em] text-[#1f1d1b]/55 sm:text-[12px]">
      {items.map((item, i) => (
        <li key={item.key} className="flex items-center gap-x-5">
          {i > 0 && (
            <span aria-hidden className="text-[#1f1d1b]/30">
              ·
            </span>
          )}
          {item.node}
        </li>
      ))}
    </ul>
  );
}

export default function Recipe({ recipe, className }: RecipeProps) {
  const {
    eyebrow,
    title,
    dek,
    opening,
    meta,
    image,
    byline,
    ingredients,
    method,
    serve,
    variations,
    notes,
    origin,
  } = recipe;

  const hasClosing =
    Boolean(serve) ||
    Boolean(variations && variations.length > 0) ||
    Boolean(notes);

  // Auto-detect rendering mode for ingredients. When NO ingredient has
  // a quantity, we drop the quantity column entirely (the new minimal
  // recipes are guidance, not specifications — quantities aren't part
  // of the model). When ANY ingredient has a `group`, we render with
  // sub-headings (e.g. "Coconut Rice", "Shrimp Curry") for recipes
  // with distinct components.
  const hasQuantities = ingredients.some((ing) => Boolean(ing.quantity));
  const hasGroups = ingredients.some((ing) => Boolean(ing.group));

  // Group ingredients in declared order, preserving the position of the
  // first ungrouped block (rendered before any grouped sections).
  const ingredientGroups = hasGroups
    ? ingredients.reduce<Array<{ heading: string | null; items: typeof ingredients }>>(
        (acc, ing) => {
          const heading = ing.group ?? null;
          const last = acc[acc.length - 1];
          if (last && last.heading === heading) {
            last.items.push(ing);
          } else {
            acc.push({ heading, items: [ing] });
          }
          return acc;
        },
        []
      )
    : null;

  // Multi-paragraph notes — split on blank lines.
  const notesParagraphs = notes
    ? notes.split(/\n\s*\n/).map((p) => p.trim()).filter(Boolean)
    : [];

  return (
    <article
      className={[
        "mx-auto w-full max-w-5xl px-6 py-24 text-[#1f1d1b] sm:px-10 md:py-36",
        className ?? "",
      ].join(" ")}
    >
      {/* ---------- Header ---------- */}
      <header className="mx-auto max-w-3xl text-center">
        {eyebrow && (
          <p className="mb-12 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
            {eyebrow}
          </p>
        )}

        <h1 className="font-serif text-[clamp(2.75rem,7.5vw,5.5rem)] font-normal leading-[0.98] tracking-[-0.025em] text-balance">
          {title}
        </h1>

        {dek && (
          <p className="text-pretty mx-auto mt-12 max-w-2xl font-serif text-[clamp(1.125rem,1.7vw,1.375rem)] italic leading-[1.55] text-[#1f1d1b]/70">
            {dek}
          </p>
        )}

        {meta && (
          <div className="mt-16">
            <MetaLine meta={meta} />
          </div>
        )}

        {/* CopyShoppingList only appears when ingredients carry
            quantities — for the new minimal recipes (no quantities,
            guidance not specifications), the shopping-list widget
            would copy noise, so we suppress it. */}
        {hasQuantities && ingredients.length > 0 && (
          <div className="mt-6 flex justify-center">
            <CopyShoppingList title={title} ingredients={ingredients} />
          </div>
        )}

        {/* Top-of-recipe byline removed per Authorship brief —
            byline now sits at the bottom of the recipe as a
            signature. See <Byline /> at the end of this article. */}
      </header>

      {/* ---------- Opening paragraph ---------- */}
      {opening && (
        <p className="text-pretty mx-auto mt-16 max-w-2xl text-center font-serif text-[18px] leading-[1.7] text-[#1f1d1b]/80 sm:mt-20 sm:text-[19px]">
          {opening}
        </p>
      )}

      {/* ---------- Hero image ---------- */}
      {image && (
        <figure className="mx-auto mt-24 md:mt-32">
          <Image
            src={image.src}
            alt={image.alt}
            width={image.width}
            height={image.height}
            sizes="(min-width: 1024px) 960px, 100vw"
            className="h-auto w-full"
          />
        </figure>
      )}

      {/* ---------- Body ---------- */}
      <div className="mx-auto mt-32 grid max-w-4xl gap-20 md:mt-44 md:grid-cols-12 md:gap-24">
        {/* Ingredients */}
        <section
          aria-labelledby="recipe-ingredients"
          className="md:col-span-5"
        >
          <h2
            id="recipe-ingredients"
            className="mb-12 text-[11px] uppercase leading-none tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]"
          >
            Ingredients
          </h2>

          <div className="md:sticky md:top-16">
            {ingredientGroups ? (
              // Grouped — render each group with its sub-heading.
              <div className="space-y-10">
                {ingredientGroups.map((group, gi) => (
                  <div key={`${group.heading ?? "ungrouped"}-${gi}`}>
                    {group.heading && (
                      <h3 className="mb-5 font-serif text-[16px] italic leading-none text-[#1f1d1b]/85 sm:text-[17px]">
                        {group.heading}
                      </h3>
                    )}
                    <ul className="space-y-3">
                      {group.items.map((ing, i) => (
                        <li
                          key={`${ing.name}-${i}`}
                          className="text-[16px] leading-[1.6] text-[#1f1d1b]/85 sm:text-[17px]"
                        >
                          {ing.name}
                          {ing.note && (
                            <span className="text-[#1f1d1b]/50">
                              {" "}
                              {ing.note}
                            </span>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
              </div>
            ) : hasQuantities ? (
              // Quantified — original two-column layout (italic
              // quantity beside name).
              <ul className="space-y-3.5">
                {ingredients.map((ing, i) => (
                  <li
                    key={`${ing.name}-${i}`}
                    className="grid grid-cols-[5.5rem_1fr] gap-x-8 text-[16px] leading-[1.6] sm:grid-cols-[6.5rem_1fr] sm:text-[17px]"
                  >
                    <span className="font-serif italic text-[#1f1d1b]/50">
                      {ing.quantity ?? ""}
                    </span>
                    <span>
                      {ing.name}
                      {ing.note && (
                        <span className="text-[#1f1d1b]/50"> {ing.note}</span>
                      )}
                    </span>
                  </li>
                ))}
              </ul>
            ) : (
              // Minimal — flat list, no quantity column. Recipes are
              // guidance, not specifications.
              <ul className="space-y-3">
                {ingredients.map((ing, i) => (
                  <li
                    key={`${ing.name}-${i}`}
                    className="text-[16px] leading-[1.6] text-[#1f1d1b]/85 sm:text-[17px]"
                  >
                    {ing.name}
                    {ing.note && (
                      <span className="text-[#1f1d1b]/50"> {ing.note}</span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>
        </section>

        {/* Steps */}
        <section aria-labelledby="recipe-steps" className="md:col-span-7">
          <h2
            id="recipe-steps"
            className="mb-12 text-[11px] uppercase leading-none tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]"
          >
            Steps
          </h2>

          <ol className="space-y-14 sm:space-y-16">
            {method.map((step, i) => (
              <li
                key={i}
                className="grid grid-cols-[3rem_1fr] gap-x-6 sm:grid-cols-[3.75rem_1fr] sm:gap-x-8"
              >
                <span className="pt-[0.35em] font-serif text-[20px] leading-none tracking-[-0.01em] text-[#1f1d1b]/40 sm:text-[22px]">
                  {String(i + 1).padStart(2, "0")}
                </span>
                <p className="text-[17px] leading-[1.75] text-[#1f1d1b]/85 sm:text-[18px]">
                  {step}
                </p>
              </li>
            ))}
          </ol>
        </section>
      </div>

      {/* ---------- Closing block: To Serve / Variations / Notes ---------- */}
      {hasClosing && (
        <>
          <p
            aria-hidden
            className="mx-auto mt-36 mb-16 text-center font-serif text-[18px] text-[#1f1d1b]/30 md:mt-48 md:mb-20"
          >
            —
          </p>

          <div className="space-y-20 sm:space-y-24">
            {serve && (
              <aside
                aria-label="Serving"
                className="mx-auto max-w-xl text-center"
              >
                <p className="mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
                  To Serve
                </p>
                <p className="text-pretty font-serif text-[18px] italic leading-[1.65] text-[#1f1d1b]/70 sm:text-[19px]">
                  {serve}
                </p>
              </aside>
            )}

            {variations && variations.length > 0 && (
              <aside
                aria-label="Variations"
                className="mx-auto max-w-2xl text-center"
              >
                <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
                  Variations
                </p>
                <ul className="space-y-3">
                  {variations.map((v, i) => (
                    <li
                      key={i}
                      className="text-pretty font-serif text-[17px] italic leading-[1.6] text-[#1f1d1b]/70 sm:text-[18px]"
                    >
                      {v}
                    </li>
                  ))}
                </ul>
              </aside>
            )}

            {notesParagraphs.length > 0 && (
              <aside
                aria-label="Notes"
                className="mx-auto max-w-2xl text-center"
              >
                <p className="mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
                  Notes
                </p>
                <div className="space-y-5">
                  {notesParagraphs.map((para, i) => (
                    <p
                      key={i}
                      className="text-pretty font-serif text-[18px] italic leading-[1.65] text-[#1f1d1b]/70 sm:text-[19px]"
                    >
                      {para}
                    </p>
                  ))}
                </div>
              </aside>
            )}
          </div>
        </>
      )}

      {/* Closing byline. */}
      <Byline author={byline} />

      {/* ---------- Origin / Heritage ----------
          Sits beneath the byline as a quiet bottom-of-page marker. The
          image carries the meaning on its own — no caption, no eyebrow,
          no narration. The alt text is enough for screen readers. The
          recipe ends at the byline; this image is the heritage marker
          and that's the end of the page. */}
      {origin?.image && (
        <aside aria-label="Origin" className="mx-auto mt-16 max-w-sm text-center sm:mt-20">
          <figure>
            <Image
              src={origin.image.src}
              alt={origin.image.alt}
              width={origin.image.width}
              height={origin.image.height}
              sizes="(min-width: 768px) 384px, 100vw"
              className="h-auto w-full"
            />
          </figure>
        </aside>
      )}
    </article>
  );
}
