"use client";

import { createContext, useContext, useEffect, useState } from "react";
import { usePathname } from "next/navigation";

const SESSION_FLAG = "hessentials-arrived";

export type ArrivalPhase = "pending" | "first" | "subsequent";

const ArrivalContext = createContext<ArrivalPhase>("pending");

/**
 * Resolves once per session:
 *  - pending: not yet known (initial render, or user is still on `/`)
 *  - first:   user has crossed into a non-`/` route for the first time
 *  - subsequent: user already crossed before; freeze entry animations
 */
export default function ArrivalProvider({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [phase, setPhase] = useState<ArrivalPhase>("pending");

  useEffect(() => {
    if (pathname === "/") return;
    if (typeof window === "undefined") return;

    if (sessionStorage.getItem(SESSION_FLAG)) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setPhase("subsequent");
    } else {
      setPhase("first");
      sessionStorage.setItem(SESSION_FLAG, "true");
    }
  }, [pathname]);

  return (
    <ArrivalContext.Provider value={phase}>{children}</ArrivalContext.Provider>
  );
}

export function useArrivalPhase(): ArrivalPhase {
  return useContext(ArrivalContext);
}
