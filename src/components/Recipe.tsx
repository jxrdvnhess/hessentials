import Image from "next/image";
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

        {ingredients.length > 0 && (
          <div className="mt-6 flex justify-center">
            <CopyShoppingList title={title} ingredients={ingredients} />
          </div>
        )}

        {byline && (
          <p className="mt-10 text-[11px] uppercase tracking-[0.24em] text-[#1f1d1b]/45">
            {byline}
          </p>
        )}
      </header>

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

          <ul className="space-y-3.5 md:sticky md:top-16">
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
        </section>

        {/* Method */}
        <section aria-labelledby="recipe-method" className="md:col-span-7">
          <h2
            id="recipe-method"
            className="mb-12 text-[11px] uppercase leading-none tracking-[0.26em] text-[#1f1d1b]/55 sm:text-[12px]"
          >
            Method
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

            {notes && (
              <aside
                aria-label="Notes"
                className="mx-auto max-w-2xl text-center"
              >
                <p className="mb-6 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
                  Notes
                </p>
                <p className="text-pretty font-serif text-[18px] italic leading-[1.65] text-[#1f1d1b]/70 sm:text-[19px]">
                  {notes}
                </p>
              </aside>
            )}
          </div>
        </>
      )}

      {/* ---------- Origin / Heritage ---------- */}
      {origin && (
        <>
          <p
            aria-hidden
            className="mx-auto mt-36 mb-16 text-center font-serif text-[18px] text-[#1f1d1b]/30 md:mt-48 md:mb-20"
          >
            —
          </p>

          <aside
            aria-label="Origin"
            className="mx-auto max-w-2xl text-center"
          >
            {origin.heading && (
              <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
                {origin.heading}
              </p>
            )}
            <p className="text-pretty mx-auto max-w-xl font-serif text-[18px] italic leading-[1.65] text-[#1f1d1b]/70 sm:text-[19px]">
              {origin.body}
            </p>
            {origin.image && (
              <figure className="mx-auto mt-16 md:mt-20">
                <Image
                  src={origin.image.src}
                  alt={origin.image.alt}
                  width={origin.image.width}
                  height={origin.image.height}
                  sizes="(min-width: 1024px) 720px, 100vw"
                  className="h-auto w-full"
                />
              </figure>
            )}
          </aside>
        </>
      )}
    </article>
  );
}
