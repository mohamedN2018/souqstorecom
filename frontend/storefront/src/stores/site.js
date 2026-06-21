import { defineStore } from "pinia";
import { siteApi } from "@/lib/api";
import { useThemeStore } from "@/stores/theme";

// Global marketplace settings (name, announcement, theme, vendor terms).
// The theme here is controlled ONLY by the platform admin.
export const useSiteStore = defineStore("site", {
  state: () => ({
    site_name: "سوق ستور",
    primary_color: "#2563eb",
    secondary_color: "#1e293b",
    accent_color: "#f59e0b",
    rounded: 14,
    announcement: "",
    vendor_terms: "",
    loaded: false,
  }),
  actions: {
    async load() {
      try {
        const { data } = await siteApi.get();
        Object.assign(this.$state, data, { loaded: true });
        this.applyGlobal();
      } catch {
        this.loaded = true;
      }
    },
    // Apply the admin-defined global theme as the site default.
    applyGlobal() {
      const theme = useThemeStore();
      theme.primary = this.primary_color;
      theme.secondary = this.secondary_color;
      theme.accent = this.accent_color;
      theme.radius = this.rounded;
      theme.setGlobalDefault({
        primary: this.primary_color,
        secondary: this.secondary_color,
        accent: this.accent_color,
        radius: this.rounded,
      });
      theme.apply();
    },
  },
});
