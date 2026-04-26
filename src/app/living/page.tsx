import Link from "next/link";
import type { Metadata } from "next";
import { getAllLivingArticles, type LivingArticle } from "../../lib/living";

export const metadata: Metadata = {
  title: "Living — Hessentials",
  description:
    "Notes on rooms, rituals, plants, and the small decisions that shape a way of being at home.",
};

type Group = "Systems" | "Environment" | "Rituals";

const GROUPS: Record<string, Group> = {
  "the-one-pot-that-does-everything": "Systems",
  "ditch-the-coffee-machine-get-an-espresso-machine": "Systems",
  "why-most-kitchens-are-set-up-wrong": "Systems",
  "the-kitchen-setup-that-makes-you-cook-more": "Systems",
  "stop-buying-plush-blankets-use-cotton": "Environment",
  "youre-not-bad-with-plants": "Environment",
  "the-10-minute-reset-that-changes-your-evenings": "Rituals",
  "stop-using-fabric-softener": "Rituals",
};

const GROUP_ORDER: Group[] = ["Systems", "Environment", "Rituals"];

export default async function LivingIndexPage() {
  const articles = await getAllLivingArticles();

  const grouped: Record<Group, LivingArticle[]> = {
    Systems: [],
    Environment: [],
    Rituals: [],
  };
  for (const article of articles) {
    const group: Group = GROUPS[article.slug] ?? "Systems";
    grouped[group].push(article);
  }

  return (
    <main className="relative z-10 min-h-screen text-[#1f1d1b]">
      {/* ---------- Intro ---------- */}
      <section className="mx-auto w-full max-w-3xl px-6 pt-16 pb-12 text-center sm:px-10 md:pt-24">
        <p className="mb-8 text-[11px] uppercase tracking-[0.26em] text-[#1f1d1b]/45 sm:text-[12px]">
          Living
        </p>
        <p className="text-pretty mx-auto max-w-2xl font-serif text-[clamp(1.5rem,2.6vw,2rem)] italic leading-[1.4] text-[#1f1d1b]/80">
          Some things feel good. Some things work. They are not the same.
        </p>
      </section>

      {/* ---------- Groups ---------- */}
      <section className="mx-auto w-full max-w-6xl px-6 pb-32 sm:px-10 md:pb-40">
        {articles.length === 0 ? (
          <p className="text-center font-serif text-[18px] italic text-[#1f1d1b]/55">
            More entries arriving soon.
          </p>
        ) : (
          GROUP_ORDER.map((group) => {
            const list = grouped[group];
            if (list.length === 0) return null;
            return (
              <div key={group} className="mb-20 last:mb-0 sm:mb-24 md:mb-28">
                <div className="mb-12 flex items-center gap-4 sm:mb-14">
                  <span
                    aria-hidden
                    className="block h-px w-10 shrink-0 bg-[#1f1d1b]/15 sm:w-12"
                  />
                  <p className="text-[11px] uppercase tracking-[0.28em] text-[#1f1d1b]/35 sm:text-[12px]">
                    {group}
                  </p>
                  <span
                    aria-hidden
                    className="block h-px flex-1 bg-[#1f1d1b]/15"
                  />
                </div>

                <ul className="grid grid-cols-1 gap-x-12 gap-y-12 sm:grid-cols-2 sm:gap-x-14 sm:gap-y-16 md:gap-x-20">
                  {list.map((article) => (
                    <li key={article.slug}>
                      <Link
                        href={`/living/${article.slug}`}
                        className="group block transition-opacity duration-500 ease-out"
                      >
                        <h2 className="font-serif text-[clamp(1.5rem,2.6vw,2rem)] font-normal leading-[1.15] tracking-[-0.015em] text-balance text-[#1f1d1b] underline decoration-transparent decoration-[0.5px] underline-offset-[8px] transition-[text-decoration-color] duration-500 ease-out group-hover:decoration-[#1f1d1b]/30">
                          {article.meta.title}
                        </h2>

                        {article.excerpt && (
                          <p className="text-pretty mt-4 font-serif text-[16px] italic leading-[1.55] text-[#1f1d1b]/65 sm:text-[17px]">
                            {article.excerpt}
                          </p>
                        )}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            );
          })
        )}
      </section>
    </main>
  );
}
