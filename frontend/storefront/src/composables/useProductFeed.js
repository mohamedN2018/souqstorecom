import { onBeforeUnmount } from "vue";
import { rewriteMedia } from "@/lib/api";

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
    // WebSocket under the unique "/sqstore/rt" namespace (avoids the generic
    // "/ws" hijacked by other apps). nginx/Vite map "/sqstore/rt" → "/ws".
    ws = new WebSocket(`${proto}://${location.host}/sqstore/rt/products/`);
    ws.onmessage = (e) => {
      try {
        const data = rewriteMedia(JSON.parse(e.data));
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
