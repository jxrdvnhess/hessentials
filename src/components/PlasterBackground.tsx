"use client";

import { useEffect, useState } from "react";
import Image from "next/image";
import { usePathname } from "next/navigation";

/**
 * Plaster environment that lives in the root layout.
 *
 * Behavior:
 *  - `/`             → not rendered (Enter Page)
 *  - `/home`         → rises into place on every arrival (animation re-fires)
 *  - other interior  → renders statically; persists across navigation
 *                      between non-home routes without remounting
 *
 * The animation re-fires on each `/home` arrival because the wrapper's
 * `key` increments on every transition INTO `/home`, forcing a remount.
 * For non-home interior routes the key stays stable, so navigation
 * between Recipes / Living / Aurelian / About doesn't disturb the texture.
 */
export default function PlasterBackground() {
  const pathname = usePathname();
  const [homeArrivals, setHomeArrivals] = useState(0);

  useEffect(() => {
    if (pathname === "/home") {
      setHomeArrivals((n) => n + 1);
    }
  }, [pathname]);

  if (pathname === "/") return null;

  const isHome = pathname === "/home";
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
