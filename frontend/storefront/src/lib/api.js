import axios from "axios";

// Same-origin: Vite (dev) / nginx (prod) proxy this prefix to the gateway.
// NOTE: the whole backend lives under ONE unique prefix "/gw" (API, WebSocket
// AND media) because the shared platform/edge hijacks the bare "/api", "/ws"
// and "/media" paths for another app. The web nginx / Vite proxy strip "/gw"
// before reaching the gateway. See rewriteMedia() below for image URLs.
const api = axios.create({
  baseURL: "/gw/api/v1",
  timeout: 15000,
});

// Attach JWT if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Backend stores image URLs as "/media/...". Since the edge hijacks "/media",
// rewrite them to "/gw/media/..." everywhere in one place — no component edits.
export function rewriteMedia(value) {
  if (typeof value === "string") {
    return value.startsWith("/media/") ? "/gw" + value : value;
  }
  if (Array.isArray(value)) return value.map(rewriteMedia);
  if (value && typeof value === "object") {
    for (const k in value) value[k] = rewriteMedia(value[k]);
    return value;
  }
  return value;
}
api.interceptors.response.use((res) => {
  if (res.data) res.data = rewriteMedia(res.data);
  return res;
});

export default api;

export const catalogApi = {
  categories: () => api.get("/catalog/categories/"),
  products: (params) => api.get("/catalog/products/", { params }),
  product: (slug) => api.get(`/catalog/products/${slug}/`),
  // reviews + checkout
  reviews: (slug) => api.get(`/catalog/products/${slug}/reviews/`),
  addReview: (slug, data) => api.post(`/catalog/products/${slug}/reviews/`, data),
  checkout: (items) => api.post("/catalog/checkout/", { items }),
  // vendor product management
  myProducts: () => api.get("/catalog/manage/products/"),
  createProduct: (data) => api.post("/catalog/manage/products/", data),
  updateProduct: (id, data) => api.patch(`/catalog/manage/products/${id}/`, data),
  deleteProduct: (id) => api.delete(`/catalog/manage/products/${id}/`),
};

export const vendorApi = {
  list: (params) => api.get("/vendors/", { params }),
  detail: (slug) => api.get(`/vendors/${slug}/`),
  register: (data) => api.post("/vendors/register/", data),
  myStore: () => api.get("/vendors/me/"),
  updateStore: (data) => api.patch("/vendors/me/", data),
  updateTheme: (data) => api.patch("/vendors/me/theme/", data),
};

export const authApi = {
  login: (data) => api.post("/auth/login/", data),
  register: (data) => api.post("/auth/register/", data),
  me: () => api.get("/auth/me/"),
};

// Store staff (vendor owner manages employees)
export const staffApi = {
  list: () => api.get("/auth/staff/"),
  create: (data) => api.post("/auth/staff/", data),
  update: (id, data) => api.patch(`/auth/staff/${id}/`, data),
  remove: (id) => api.delete(`/auth/staff/${id}/`),
};

// Global site settings (admin edits, everyone reads)
export const siteApi = {
  get: () => api.get("/site/settings/"),
  update: (data) => api.patch("/site/settings/", data),
};

// Platform admin
export const adminApi = {
  applications: (status) => api.get("/vendors/admin/applications/", { params: status ? { status } : {} }),
  stats: () => api.get("/vendors/admin/stats/"),
  approve: (id) => api.post(`/vendors/admin/${id}/approve/`),
  reject: (id, reason) => api.post(`/vendors/admin/${id}/reject/`, { reason }),
};
