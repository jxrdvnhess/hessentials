import type { Metadata } from "next";
import { Playfair_Display, Inter } from "next/font/google";
import PlasterBackground from "../components/PlasterBackground";
import SiteHeader from "../components/SiteHeader";
import SiteFooter from "../components/SiteFooter";
import "./globals.css";

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
  title:
    "Hessentials — A system for choosing what holds.",
  description:
    "A quieter approach. Choosing well, and standing by it. Food, home, style, and the small decisions that shape how life actually feels.",
  metadataBase: new URL("https://hessentials.co"),
  openGraph: {
    title: "Hessentials",
    description: "A system for choosing what holds.",
    type: "website",
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
        <PlasterBackground />
        <SiteHeader />
        {children}
        <SiteFooter />
      </body>
    </html>
  );
}
