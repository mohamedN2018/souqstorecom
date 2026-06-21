import { onBeforeUnmount } from "vue";

/**
 * Live product feed over WebSocket (proxied to the catalog service).
 * Calls `onEvent({ event, product })` whenever a vendor creates/updates/deletes
 * a product — powering the "no refresh needed" real-time experience.
 */
export function useProductFeed(onEvent) {
  const proto = location.protocol === "https:" ? "wss" : "ws";
  let ws;
  let retry;

  function connect() {
    // Unique "/sqws" prefix (not "/ws") — another app on the shared edge
    // hijacks "/ws" for this domain. nginx/Vite rewrite "/sqws" → "/ws".
    ws = new WebSocket(`${proto}://${location.host}/sqws/products/`);
    ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data.event) onEvent(data);
      } catch {
        /* ignore */
      }
    };
    ws.onclose = () => {
      retry = setTimeout(connect, 2000); // auto-reconnect → "strong" real-time
    };
  }
  connect();

  onBeforeUnmount(() => {
    clearTimeout(retry);
    if (ws) {
      ws.onclose = null;
      ws.close();
    }
  });
}
