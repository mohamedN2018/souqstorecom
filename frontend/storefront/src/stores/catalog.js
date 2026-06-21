import { defineStore } from "pinia";
import { catalogApi } from "@/lib/api";

// Small cache so the category tree is fetched once and shared across the UI.
export const useCatalogStore = defineStore("catalog", {
  state: () => ({ categories: [], loaded: false }),
  getters: {
    topCategories: (s) => s.categories.filter((c) => !c.parent),
    subsOf: (s) => (id) => s.categories.filter((c) => c.parent === id),
  },
  actions: {
    async loadCategories() {
      if (this.loaded) return;
      const { data } = await catalogApi.categories();
      this.categories = data;
      this.loaded = true;
    },
  },
});
