/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{vue,js}"],
  theme: {
    extend: {
      // Colors map to CSS variables so the whole UI is themeable at runtime
      // (the "full custom color" system) — change a var, everything updates.
      colors: {
        primary: "var(--c-primary)",
        secondary: "var(--c-secondary)",
        accent: "var(--c-accent)",
        surface: "var(--c-surface)",
        ink: "var(--c-ink)",
        muted: "var(--c-muted)",
      },
      fontFamily: {
        sans: ["Cairo", "system-ui", "sans-serif"],
      },
      borderRadius: {
        theme: "var(--c-radius)",
      },
    },
  },
  plugins: [],
};
