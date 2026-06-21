import { defineStore } from "pinia";

// Marketplace cart — items can come from multiple vendors (grouped at checkout).
export const useCartStore = defineStore("cart", {
  state: () => ({
    items: JSON.parse(localStorage.getItem("cart") || "[]"),
  }),
  getters: {
    count: (s) => s.items.reduce((n, i) => n + i.qty, 0),
    total: (s) => s.items.reduce((n, i) => n + i.qty * Number(i.price), 0),
  },
  actions: {
    add(product, qty = 1) {
      const existing = this.items.find((i) => i.id === product.id);
      if (existing) {
        existing.qty += qty;
      } else {
        this.items.push({
          id: product.id,
          name: product.name,
          price: product.price,
          image: product.primary_image || (product.images?.[0]?.url ?? ""),
          vendor_id: product.vendor_id,
          qty,
        });
      }
      this.persist();
    },
    remove(id) {
      this.items = this.items.filter((i) => i.id !== id);
      this.persist();
    },
    setQty(id, qty) {
      const it = this.items.find((i) => i.id === id);
      if (it) it.qty = Math.max(1, qty);
      this.persist();
    },
    clear() {
      this.items = [];
      this.persist();
    },
    persist() {
      localStorage.setItem("cart", JSON.stringify(this.items));
    },
  },
});
