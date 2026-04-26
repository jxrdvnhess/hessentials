import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Next 16 requires explicit allow-list of quality values used by next/image.
    // 75 = Next default. 90 = editorial moments. 95 = full-bleed hero imagery
    // where any softness is visible at scale (e.g. the home lifestyle image).
    qualities: [75, 90, 95],

    // Brand CDNs that serve shop product imagery. Listed explicitly so
    // unfamiliar hosts can't slip into next/image. Trim this list once shop
    // images are localized to /public/shop/ via scripts/download-shop-images.sh.
    remotePatterns: [
      { protocol: "https", hostname: "www.loewe.com" },
      { protocol: "https", hostname: "images.quince.com" },
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
};

export default nextConfig;
