// =============================================================================
// PARKED — not imported anywhere as of 2026-04-29.
//
// The plaster texture overlay was pulled site-wide because it was reading as
// wallpaper imitating what the footer photograph now does for real and
// competing with the photography. The site is flat brand cream now (var
// --cream-bg in globals.css). This component remains in the repo per the
// archive policy — the texture PNG (/public/soft-plaster-texture-with-
// plant-shadows.png) is also kept for possible future use in a specific
// editorial context. Delete this file if the next look-and-feel pass
// makes this clearly obsolete.
// =============================================================================

"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { usePathname } from "next/navigation";

/**
 * Plaster environment that lives in the root layout.
 *
 * Behavior:
 *  - `/`             → rises into place on every arrival (animation
 *                      re-fires); the homepage owns the brand arrival
 *  - other interior  → renders statically; persists across navigation
 *                      between non-home routes without remounting
 *
 * The animation re-fires on each `/` arrival because the wrapper's
 * `key` increments on every transition INTO `/`, forcing a remount.
 * For non-home interior routes the key stays stable, so navigation
 * between Recipes / Living / Aurelian / About doesn't disturb the
 * texture.
 */
export default function PlasterBackground() {
  const pathname = usePathname();
  const [homeArrivals, setHomeArrivals] = useState(0);

  useEffect(() => {
    if (pathname === "/") {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setHomeArrivals((n) => n + 1);
    }
  }, [pathname]);

  const isHome = pathname === "/";
  const key = isHome ? `home-${homeArrivals}` : "interior";

  return (
    <div
      key={key}
      aria-hidden
      className={[
        "pointer-events-none fixed inset-0 -z-10",
        isHome ? "plaster-rise" : "",
      ]
        .filter(Boolean)
        .join(" ")}
    >
      <Image
        src="/soft-plaster-texture-with-plant-shadows.png"
        alt=""
        fill
        priority
        sizes="100vw"
        className="object-cover object-center"
      />
    </div>
  );
}
