import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Next 16 requires explicit allow-list of quality values used by next/image.
    // Quality tiers, by context:
    //   75 = Next default. Index/grid thumbnails where compression is invisible.
    //   85 = Shop product cards, recipe hero crops.
    //   90 = Editorial moments — wordmark, symbol, secondary hero images.
    //   92 = Mid-tier hero (Exit, Cleanup) — softer on retina than 95.
    //   95 = Anchor full-bleed imagery (Dinner, Morning) — full retina/4K crisp.
    qualities: [75, 85, 90, 92, 95],

    // Brand CDNs that serve shop product imagery. Listed explicitly so
    // unfamiliar hosts can't slip into next/image. Trim this list once shop
    // images are localized to /public/shop/ via scripts/download-shop-images.sh.
    remotePatterns: [
      { protocol: "https", hostname: "www.loewe.com" },
      { protocol: "https", hostname: "www.omegawatches.com" },
      { protocol: "https", hostname: "m.media-amazon.com" },
      { protocol: "https", hostname: "www.prada.com" },
      { protocol: "https", hostname: "static.massimodutti.net" },
      { protocol: "https", hostname: "lvfurniturecollection.com" },
      { protocol: "https", hostname: "www.birkenstock.com" },
      { protocol: "https", hostname: "www.ahlemeyewear.com" },
      { protocol: "https", hostname: "drinkcrazywater.myshopify.com" },
      { protocol: "https", hostname: "www.tagheuer.com" },
      { protocol: "https", hostname: "www.aveda.com" },
      { protocol: "https", hostname: "media.tiffany.com" },
      { protocol: "https", hostname: "www.johnstonmurphy.com" },
      { protocol: "https", hostname: "www.awaytravel.com" },
      { protocol: "https", hostname: "target.scene7.com" },
      { protocol: "https", hostname: "image.uniqlo.com" },
      { protocol: "https", hostname: "img.abercrombie.com" },
      { protocol: "https", hostname: "claytonandcrume.com" },
      { protocol: "https", hostname: "encrypted-tbn3.gstatic.com" },
    ],
  },

  /**
   * Permanent redirects for slugs that were renamed during the voice pass.
   * Keeps any external links, search-engine results, and past sends working.
   * 308 (permanent) so SEO equity transfers to the new URL.
   */
  async redirects() {
    return [
      // /home → / — the homepage moved to the canonical / URL so visitors
      // land on hessentials.co (not hessentials.co/home). Any legacy
      // links to /home bounce here. Non-permanent for now in case we
      // need to walk this back; promote to permanent once stable.
      {
        source: "/home",
        destination: "/",
        permanent: false,
      },
      // /recipes/garlic-butter-chicken-with-crispy-potatoes — retired in
      // the 2026-04-30 library editorial pass (thematic overlap with the
      // pesto-caprese chicken recipe and other chicken-on-a-plate
      // variants). 301 to the recipes index so any external links bounce
      // cleanly.
      {
        source: "/recipes/garlic-butter-chicken-with-crispy-potatoes",
        destination: "/recipes",
        permanent: true,
      },
      {
        source: "/living/the-10-minute-reset-that-changes-your-evenings",
        destination: "/living/the-10-minute-reset",
        permanent: true,
      },
      {
        source: "/living/the-kitchen-setup-that-makes-you-cook-more",
        destination: "/living/why-you-dont-cook-more",
        permanent: true,
      },
      {
        source: "/style/elevated-casual-is-a-discipline",
        destination: "/style/casual-is-not-a-free-pass",
        permanent: true,
      },
      {
        source: "/style/the-details-that-change-everything",
        destination: "/style/its-usually-the-small-things",
        permanent: true,
      },
      {
        source: "/style/hosting-is-a-performance",
        destination: "/style/people-can-feel-when-its-forced",
        permanent: true,
      },
      {
        source: "/style/signature-scent-is-branding",
        destination: "/style/the-scent-people-remember",
        permanent: true,
      },
      // Prada Court Leather Sneakers retired 2026-04-30 (pre-order
      // listing without a fetchable price). Replacement sneakers are
      // pending. Bouncing to the Shop index in the meantime.
      {
        source: "/shop/prada-court-leather-sneakers",
        destination: "/shop",
        permanent: true,
      },
      // Practice slug rename pass (2026-05-01): stripped the duplicate
      // `practice-` prefix from every Practice article slug. The pillar
      // already namespaces the URL — repeating it in the slug was noise.
      // 308 (permanent) so SEO equity transfers to the canonical paths.
      {
        source: "/practice/practice-1111-is-a-real-practice",
        destination: "/practice/1111-is-a-real-practice",
        permanent: true,
      },
      {
        source: "/practice/practice-compliment-one-person-every-day",
        destination: "/practice/compliment-one-person-every-day",
        permanent: true,
      },
      {
        source: "/practice/practice-go-to-mass-occasionally",
        destination: "/practice/go-to-mass-occasionally",
        permanent: true,
      },
      {
        source: "/practice/practice-pick-one-stone-know-why",
        destination: "/practice/pick-one-stone-know-why",
        permanent: true,
      },
      {
        source: "/practice/practice-silence-five-minutes-no-app",
        destination: "/practice/silence-five-minutes-no-app",
        permanent: true,
      },
      {
        source: "/practice/practice-sound-baths-how-to-tell-which-ones-work",
        destination: "/practice/sound-baths-how-to-tell-which-ones-work",
        permanent: true,
      },
      {
        source: "/practice/practice-tarot-isnt-prediction",
        destination: "/practice/tarot-isnt-prediction",
        permanent: true,
      },
      {
        source: "/practice/practice-the-annual-review-beats-resolutions",
        destination: "/practice/the-annual-review-beats-resolutions",
        permanent: true,
      },
      {
        source: "/practice/practice-the-single-object-you-carry",
        destination: "/practice/the-single-object-you-carry",
        permanent: true,
      },
      {
        source: "/practice/practice-walking-is-not-slow-running",
        destination: "/practice/walking-is-not-slow-running",
        permanent: true,
      },
      {
        source: "/practice/practice-why-i-write-down-what-i-want",
        destination: "/practice/why-i-write-down-what-i-want",
        permanent: true,
      },
    ];
  },
};

export default nextConfig;
