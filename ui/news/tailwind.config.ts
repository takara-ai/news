import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: "class",
  theme: {
    extend: {
      fontFamily: {
        serif: ["var(--font-crimson)", "Georgia", "Times New Roman", "serif"],
        display: ["var(--font-playfair)", "Georgia", "serif"],
        sans: ["var(--font-inter)", "Arial", "sans-serif"],
        chomsky: ["var(--font-chomsky)", "serif"],
      },
      fontSize: {
        headline: ["3rem", { lineHeight: "1.1", letterSpacing: "-0.02em" }],
        subheadline: ["2rem", { lineHeight: "1.2", letterSpacing: "-0.01em" }],
        article: ["1.125rem", { lineHeight: "1.8" }],
        byline: ["0.875rem", { lineHeight: "1.4", letterSpacing: "0.05em" }],
        caption: ["0.8125rem", { lineHeight: "1.4" }],
      },
      colors: {
        newspaper: {
          black: "#1a1a1a",
          gray: {
            50: "#f9fafb",
            100: "#f3f4f6",
            200: "#e5e7eb",
            300: "#d1d5db",
            400: "#9ca3af",
            500: "#6b7280",
            600: "#4b5563",
            700: "#374151",
            800: "#1f2937",
            900: "#111827",
          },
        },
      },
      spacing: {
        "18": "4.5rem",
        "88": "22rem",
      },
      lineHeight: {
        newspaper: "1.8",
      },
      typography: {
        DEFAULT: {
          css: {
            color: "inherit",
            h1: {
              color: "inherit",
            },
            h2: {
              color: "inherit",
            },
            h3: {
              color: "inherit",
            },
            h4: {
              color: "inherit",
            },
            h5: {
              color: "inherit",
            },
            h6: {
              color: "inherit",
            },
            p: {
              color: "inherit",
            },
            strong: {
              color: "inherit",
            },
            a: {
              color: "inherit",
            },
          },
        },
      },
    },
  },
  plugins: [require("@tailwindcss/typography")],
};

export default config;
