import { createRouter, createWebHistory } from "vue-router";

const routes = [
  { path: "/", name: "home", component: () => import("@/views/HomeView.vue") },
  { path: "/products", name: "products", component: () => import("@/views/ProductsView.vue") },
  { path: "/product/:slug", name: "product", component: () => import("@/views/ProductDetailView.vue") },
  { path: "/vendors", name: "vendors", component: () => import("@/views/VendorsView.vue") },
  { path: "/vendor/:slug", name: "vendor", component: () => import("@/views/VendorDetailView.vue") },
  { path: "/cart", name: "cart", component: () => import("@/views/CartView.vue") },
];

export default createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
});
