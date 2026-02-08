import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // HackMate Dark Theme
        background: "#000000",
        foreground: "#ffffff",

        // Primary - Neon Green
        primary: {
          DEFAULT: "#00ff00",
          foreground: "#000000",
          dim: "#009900",
          bright: "#39ff14",
          glow: "rgba(0, 255, 0, 0.5)",
        },

        // Secondary
        secondary: {
          DEFAULT: "#0a0a0a",
          foreground: "#ffffff",
        },

        // Muted
        muted: {
          DEFAULT: "#111111",
          foreground: "#999999",
        },

        // Accent
        accent: {
          DEFAULT: "#1a1a1a",
          foreground: "#00ff00",
        },

        // Card
        card: {
          DEFAULT: "#0a0a0a",
          foreground: "#ffffff",
        },

        // Border
        border: "rgba(0, 255, 0, 0.2)",
        input: "rgba(0, 255, 0, 0.3)",
        ring: "rgba(0, 255, 0, 0.5)",

        // Severity colors
        severity: {
          critical: "#ff0000",
          high: "#ff6600",
          medium: "#ffcc00",
          low: "#0099ff",
          info: "#666666",
        },

        // Status colors
        status: {
          planning: "#0099ff",
          active: "#00ff00",
          completed: "#666666",
          hold: "#ffcc00",
        },
      },
      fontFamily: {
        mono: ['Fira Code', 'Consolas', 'Monaco', 'Courier New', 'monospace'],
        sans: ['Fira Code', 'monospace'],
      },
      boxShadow: {
        'glow-sm': '0 0 5px rgba(0, 255, 0, 0.3)',
        'glow-md': '0 0 10px rgba(0, 255, 0, 0.4)',
        'glow-lg': '0 0 20px rgba(0, 255, 0, 0.5)',
        'glow-xl': '0 0 30px rgba(0, 255, 0, 0.6)',
      },
      animation: {
        'pulse-glow': 'pulse-glow 2s ease-in-out infinite',
        'blink': 'blink 1s step-end infinite',
        'typing': 'typing 3.5s steps(40, end)',
        'scanline': 'scanline 10s linear infinite',
      },
      keyframes: {
        'pulse-glow': {
          '0%, 100%': { boxShadow: '0 0 5px rgba(0, 255, 0, 0.3)' },
          '50%': { boxShadow: '0 0 20px rgba(0, 255, 0, 0.6)' },
        },
        'blink': {
          '0%, 50%': { opacity: '1' },
          '51%, 100%': { opacity: '0' },
        },
        'typing': {
          'from': { width: '0' },
          'to': { width: '100%' },
        },
        'scanline': {
          '0%': { transform: 'translateY(0)' },
          '100%': { transform: 'translateY(10px)' },
        },
      },
    },
  },
  plugins: [],
};

export default config;
