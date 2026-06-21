import { defineStore } from "pinia";

const DEFAULT = {
  primary: "#2563eb",
  secondary: "#1e293b",
  accent: "#f59e0b",
  surface: "#ffffff",
  ink: "#0f172a",
  muted: "#64748b",
  radius: 14,
};

const VARMAP = {
  primary: "--c-primary",
  secondary: "--c-secondary",
  accent: "--c-accent",
  surface: "--c-surface",
  ink: "--c-ink",
  muted: "--c-muted",
};

export const useThemeStore = defineStore("theme", {
  state: () => ({
    ...DEFAULT,
    ...JSON.parse(localStorage.getItem("theme") || "{}"),
  }),
  actions: {
    apply() {
      const root = document.documentElement;
      for (const [key, varName] of Object.entries(VARMAP)) {
        root.style.setProperty(varName, this[key]);
      }
      root.style.setProperty("--c-radius", `${this.radius}px`);
      localStorage.setItem("theme", JSON.stringify(this.$state));
    },
    set(key, value) {
      this[key] = value;
      this.apply();
    },
    // Apply a vendor's theme (coming from the Vendor service) live.
    applyVendorTheme(t) {
      if (!t) return;
      this.primary = t.primary_color || this.primary;
      this.secondary = t.secondary_color || this.secondary;
      this.accent = t.accent_color || this.accent;
      if (t.rounded != null) this.radius = t.rounded;
      this.apply();
    },
    reset() {
      Object.assign(this, DEFAULT);
      this.apply();
    },
  },
});
