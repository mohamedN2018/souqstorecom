import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const routes = [
  { path: "/", name: "home", component: () => import("@/views/HomeView.vue") },
  { path: "/products", name: "products", component: () => import("@/views/ProductsView.vue") },
  { path: "/product/:slug", name: "product", component: () => import("@/views/ProductDetailView.vue") },
  { path: "/vendors", name: "vendors", component: () => import("@/views/VendorsView.vue") },
  { path: "/vendor/:slug", name: "vendor", component: () => import("@/views/VendorDetailView.vue") },
  { path: "/cart", name: "cart", component: () => import("@/views/CartView.vue") },

  { path: "/login", name: "login", component: () => import("@/views/auth/LoginView.vue") },
  { path: "/register", name: "register", component: () => import("@/views/auth/RegisterView.vue") },
  { path: "/sell", name: "vendor-register", component: () => import("@/views/auth/VendorRegisterView.vue") },

  // Isolated dashboards (own shell, no storefront chrome)
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("@/views/dashboard/DashboardView.vue"),
    meta: { dashboard: true, roles: ["vendor", "staff"] },
  },
  {
    path: "/admin",
    name: "admin",
    component: () => import("@/views/admin/AdminView.vue"),
    meta: { dashboard: true, roles: ["admin"] },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  if (to.meta.roles && !to.meta.roles.includes(auth.role)) {
    return { name: "login", query: { next: to.fullPath } };
  }
});

export default router;
