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
    ];
  },
};

export default nextConfig;
