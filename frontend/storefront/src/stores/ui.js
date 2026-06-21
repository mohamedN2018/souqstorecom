import { defineStore } from "pinia";

// Small UI state shared across the storefront (drawers, overlays).
export const useUiStore = defineStore("ui", {
  state: () => ({ drawer: false }),
  actions: {
    openDrawer() { this.drawer = true; },
    closeDrawer() { this.drawer = false; },
    toggleDrawer() { this.drawer = !this.drawer; },
  },
});
