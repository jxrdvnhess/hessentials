import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // Next 16 requires explicit allow-list of quality values used by next/image.
    // 75 is the Next default; 90 is for editorial moments (lifestyle imagery).
    qualities: [75, 90],
  },
};

export default nextConfig;
