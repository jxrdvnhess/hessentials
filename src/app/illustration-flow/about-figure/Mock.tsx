import Image from "next/image";
import AboutEssay from "../../../components/AboutEssay";

/**
 * Shared layout for the About still-figure mocks (baseline + scenes
 * A/B/C). Essay left on the site's plaster ground; the drawing right,
 * CSS sticky, still. No JS, no motion. Mobile: essay alone.
 */
export default function Mock({
  src,
  width,
  height,
}: {
  src: string;
  width: number;
  height: number;
}) {
  return (
    <main className="relative z-10 text-[#1f1d1b]">
      <section
        aria-label="About Hessentials — still figure mock"
        className="mx-auto w-full max-w-6xl px-7 sm:px-10 md:grid md:grid-cols-[minmax(0,53%)_minmax(0,1fr)] md:gap-x-[5vw]"
      >
        <div className="pb-[35vh] pt-[26vh]">
          <AboutEssay variant="inline" />
        </div>

        <div aria-hidden className="hidden md:block">
          <div className="sticky top-0 flex h-screen items-end justify-center pb-[7vh]">
            <Image
              src={src}
              alt=""
              width={width}
              height={height}
              priority
              className="h-[76vh] w-auto max-w-full object-contain opacity-90"
            />
          </div>
        </div>
      </section>
    </main>
  );
}
