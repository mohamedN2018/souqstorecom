import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// In dev the gateway is reachable on the docker network as http://gateway:80.
const GATEWAY = process.env.GATEWAY_URL || "http://localhost:18080";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) },
  },
  server: {
    host: "0.0.0.0",
    port: 5173,
    watch: { usePolling: true }, // reliable file watching inside Docker on Windows
    // The browser reaches us on host port 5280 (mapped to 5173). The HMR
    // websocket must therefore connect back on 5280, otherwise live-reload
    // silently fails and you'd have to refresh manually.
    hmr: { clientPort: 5280 },
    // Same-origin proxy → no CORS, browser only ever talks to the dev server.
    proxy: {
      "/api": { target: GATEWAY, changeOrigin: true },
      "/media": { target: GATEWAY, changeOrigin: true },
      "/ws": { target: GATEWAY, ws: true, changeOrigin: true },
    },
  },
});
