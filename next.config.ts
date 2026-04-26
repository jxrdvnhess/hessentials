import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Next 16 requires explicit allow-list of quality values used by next/image.
    // 75 = Next default. 90 = editorial moments. 95 = full-bleed hero imagery
    // where any softness is visible at scale (e.g. the home lifestyle image).
    qualities: [75, 90, 95],
  },
};

export default nextConfig;
