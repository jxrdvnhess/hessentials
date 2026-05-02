import type { Metadata, Viewport } from "next";
import { Playfair_Display, Inter } from "next/font/google";
import { GoogleAnalytics } from "@next/third-parties/google";
import SiteHeader from "../components/SiteHeader";
import FooterGate from "../components/FooterGate";
import JsonLd from "../components/JsonLd";
import { organizationSchema, websiteSchema } from "../lib/jsonLd";
import "./globals.css";

/**
 * Google Analytics is wired via @next/third-parties (Next's official
 * GA4 integration — script-tag injection, automatic pageview tracking
 * with App Router, no client-side useEffect needed).
 *
 * The measurement ID lives in NEXT_PUBLIC_GA_ID, set in the Vercel
 * project's environment variables. The conditional render below means
 * the script only loads when the env var is present — keeps localhost
 * out of production stats and prevents any tracking until the var is
 * configured.
 */
const GA_ID = process.env.NEXT_PUBLIC_GA_ID;

/**
 * Mobile-first viewport defaults.
 *
 * - `width=device-width, initial-scale=1` — render at the device's actual
 *   width on iPhone/iPad (without this, iOS Safari falls back to a 980px
 *   layout viewport and shrinks everything).
 * - `viewportFit: "cover"` — let layouts opt in to safe-area-inset paddings
 *   so the wordmark and menu drawer respect the iPhone notch / home bar.
 * - `themeColor` — matches the plaster background so the iOS status bar and
 *   tab bar tint with the brand instead of stark white.
 */
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover",
  themeColor: "#f8f6f3",
};

const serif = Playfair_Display({
  subsets: ["latin"],
  weight: ["400", "500"],
  variable: "--font-serif",
  display: "swap",
});

const sans = Inter({
  subsets: ["latin"],
  variable: "--font-sans",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "Hessentials — Choosing well, and standing by it.",
    // Every per-page title already includes "— Hessentials" (e.g.
    // "Recipes — Hessentials", "Pull-On Seersucker Swim Trunk —
    // Abercrombie — Hessentials"), so the template is a passthrough.
    // The previous template appended "| Hessentials" and produced
    // duplicates like "Recipes — Hessentials | Hessentials".
    template: "%s",
  },
  description:
    "Choosing well, and standing by it. Food, home, style, and the small decisions that make a life feel considered.",
  metadataBase: new URL("https://hessentials.co"),
  alternates: {
    canonical: "/",
  },
  openGraph: {
    title: "Hessentials",
    description: "This is what stayed.",
    url: "https://hessentials.co",
    siteName: "Hessentials",
    type: "website",
    locale: "en_US",
    images: [
      {
        url: "/og-image.png",
        width: 1200,
        height: 630,
        alt: "Hessentials — Choosing well, and standing by it.",
        type: "image/png",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "Hessentials",
    description: "This is what stayed.",
    images: ["/og-image.png"],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
    },
  },
  icons: {
    icon: [
      { url: "/favicon.ico", type: "image/x-icon" },
      { url: "/favicon-32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon-16.png", sizes: "16x16", type: "image/png" },
    ],
    apple: [{ url: "/apple-touch-icon.png", sizes: "180x180" }],
    other: [
      {
        rel: "icon",
        url: "/android-chrome-192.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        rel: "icon",
        url: "/android-chrome-512.png",
        sizes: "512x512",
        type: "image/png",
      },
    ],
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${sans.variable} ${serif.variable}`}>
      <body className="text-[#1f1d1b] antialiased">
        <SiteHeader />
        {children}
        <FooterGate />
        {/* Site-wide structured data — Organization (publisher
            identity) + WebSite (with SitelinksSearchBox potentialAction
            pointed at /search). Per-page schemas (Article, Recipe,
            Product) layer on top from each route. */}
        <JsonLd data={[organizationSchema(), websiteSchema()]} />
      </body>
      {GA_ID && <GoogleAnalytics gaId={GA_ID} />}
    </html>
  );
}
