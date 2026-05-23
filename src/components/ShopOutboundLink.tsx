"use client";

import type { ReactNode } from "react";
import { trackShopClick } from "../lib/analytics";

type Props = {
  href: string;
  /**
   * Label for the analytics destination. Distinct from `href` because
   * affiliate networks often rewrite URLs at click time; the brand is
   * the stable identifier in GA4 reports.
   */
  brand?: string;
  className?: string;
  children: ReactNode;
};

/**
 * Outbound link to a retail destination from a Shop product detail
 * page. Fires `shop_click` (Section 5 of the May 22 launch brief)
 * before navigation so the event lands in GA4 even when the browser
 * unloads the page on a same-tab click.
 *
 * Renders a plain anchor — same shape as the previous element it
 * replaced, no JS framework navigation, target="_blank" preserved.
 */
export default function ShopOutboundLink({
  href,
  brand,
  className,
  children,
}: Props) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className={className}
      onClick={() => {
        trackShopClick({
          surface: "shop_outbound",
          destination: brand ?? href,
        });
      }}
    >
      {children}
    </a>
  );
}
