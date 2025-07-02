import type { Metadata } from "next";
import { Playfair_Display, Crimson_Text, Inter } from "next/font/google";
import "./globals.css";
import ThemeRoot from "./components/theme-root";

const playfairDisplay = Playfair_Display({
  variable: "--font-playfair",
  subsets: ["latin"],
  display: "swap",
});

const crimsonText = Crimson_Text({
  variable: "--font-crimson",
  subsets: ["latin"],
  weight: ["400", "600", "700"],
  display: "swap",
});

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "The New World Times",
  description:
    "Your customizable news source for breaking stories and in-depth coverage",
  icons: {
    icon: [
      { url: "/favicon.ico", sizes: "any" },
      {
        url: "/web-app-manifest-192x192.png",
        sizes: "192x192",
        type: "image/png",
      },
      {
        url: "/web-app-manifest-512x512.png",
        sizes: "512x512",
        type: "image/png",
      },
    ],
    apple: [
      {
        url: "/web-app-manifest-192x192.png",
        sizes: "192x192",
        type: "image/png",
      },
    ],
  },
  manifest: "/web-app-manifest-192x192.png",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      suppressHydrationWarning
      className="dark:bg-newspaper-gray-900"
    >
      <body
        className={`${playfairDisplay.variable} ${crimsonText.variable} ${inter.variable} antialiased dark:bg-newspaper-gray-900`}
      >
        <ThemeRoot>{children}</ThemeRoot>
      </body>
    </html>
  );
}
