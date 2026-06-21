import { defineStore } from "pinia";
import { authApi } from "@/lib/api";

function decodeJwt(token) {
  try {
    return JSON.parse(atob(token.split(".")[1]));
  } catch {
    return {};
  }
}

export const useAuthStore = defineStore("auth", {
  state: () => ({
    access: localStorage.getItem("access") || "",
    refresh: localStorage.getItem("refresh") || "",
    user: JSON.parse(localStorage.getItem("user") || "null"),
  }),
  getters: {
    isAuthenticated: (s) => !!s.access,
    role: (s) => s.user?.role || "",
    isVendor: (s) => s.user?.role === "vendor",
    isStaff: (s) => s.user?.role === "staff",
    isAdmin: (s) => s.user?.role === "admin",
    permissions: (s) => s.user?.permissions || [],
    can: (s) => (perm) => s.user?.role === "vendor" || (s.user?.permissions || []).includes(perm),
  },
  actions: {
    async login(email, password) {
      const { data } = await authApi.login({ email, password });
      this._setTokens(data.access, data.refresh);
      const claims = decodeJwt(data.access);
      this.user = {
        id: claims.user_id,
        email: claims.email,
        role: claims.role,
        vendor_id: claims.vendor_id,
        permissions: claims.permissions || [],
      };
      localStorage.setItem("user", JSON.stringify(this.user));
      return this.user;
    },
    async register({ email, password, full_name, role = "customer" }) {
      await authApi.register({ email, password, full_name, role });
      return this.login(email, password);
    },
    _setTokens(access, refresh) {
      this.access = access;
      this.refresh = refresh;
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
    },
    logout() {
      this.access = this.refresh = "";
      this.user = null;
      ["access", "refresh", "user"].forEach((k) => localStorage.removeItem(k));
    },
  },
});
