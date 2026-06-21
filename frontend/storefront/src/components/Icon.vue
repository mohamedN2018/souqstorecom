<script setup>
/*
  Local inline-SVG icon set (Lucide-style strokes). Fully offline — no icon
  font / CDN. Use: <Icon name="cart" /> ; size via class (w-5 h-5) or :size.
  Icons inherit currentColor so they theme automatically.
*/
import { computed } from "vue";

const props = defineProps({
  name: { type: String, required: true },
  size: { type: [Number, String], default: null },
  stroke: { type: [Number, String], default: 1.8 },
});

// Each entry is the inner markup of a 24×24 viewBox (stroke, no fill).
const PATHS = {
  menu: '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
  search: '<circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
  cart: '<circle cx="9" cy="21" r="1.6"/><circle cx="18" cy="21" r="1.6"/><path d="M2.5 3h2l2.2 12.4a2 2 0 0 0 2 1.6h8.4a2 2 0 0 0 2-1.6L21.5 7H6"/>',
  user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
  heart: '<path d="M20.8 5.6a5.5 5.5 0 0 0-7.8 0L12 6.6l-1-1a5.5 5.5 0 1 0-7.8 7.8l1 1L12 21l7.8-6.6 1-1a5.5 5.5 0 0 0 0-7.8z"/>',
  star: '<path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 18.4 6.1 21l1.2-6.5L2.5 9.9l6.6-.9z"/>',
  "chevron-left": '<polyline points="15 18 9 12 15 6"/>',
  "chevron-right": '<polyline points="9 18 15 12 9 6"/>',
  "chevron-down": '<polyline points="6 9 12 15 18 9"/>',
  "arrow-left": '<line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/>',
  "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
  zap: '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
  flame: '<path d="M12 22a7 7 0 0 0 7-7c0-4-3-6-3.5-9C13 8 10 8 10 11c0 1.5 1 2.5 1 3.5A2.5 2.5 0 0 1 6 14c0-3 3-5 3-9 0 0-2 1-3 4a8 8 0 0 0-1 4 7 7 0 0 0 7 9z"/>',
  store: '<path d="M3 9l1.5-5h15L21 9M4 9v10a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1V9M3 9h18"/>',
  truck: '<path d="M1 4h13v11H1z"/><path d="M14 8h4l3 3v4h-7"/><circle cx="6" cy="18.5" r="1.8"/><circle cx="17" cy="18.5" r="1.8"/>',
  phone: '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3 19.5 19.5 0 0 1-6-6 19.8 19.8 0 0 1-3-8.6A2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.6a2 2 0 0 1-.5 2.1L8.1 9.6a16 16 0 0 0 6 6l1.2-1.2a2 2 0 0 1 2.1-.5c.8.3 1.7.6 2.6.7a2 2 0 0 1 1.7 2z"/>',
  globe: '<circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c2.5 2.6 3.9 6 4 9.5-.1 3.5-1.5 6.9-4 9.5-2.5-2.6-3.9-6-4-9.5.1-3.5 1.5-6.9 4-9.5z"/>',
  logout: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>',
  plus: '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
  minus: '<line x1="5" y1="12" x2="19" y2="12"/>',
  check: '<polyline points="20 6 9 17 4 12"/>',
  x: '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>',
  grid: '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/>',
  sparkles: '<path d="M12 3l1.6 4.4L18 9l-4.4 1.6L12 15l-1.6-4.4L6 9l4.4-1.6z"/><path d="M19 14l.8 2.2L22 17l-2.2.8L19 20l-.8-2.2L16 17l2.2-.8z"/>',
  shield: '<path d="M12 2.5l8 3v6c0 5-3.4 8.5-8 10-4.6-1.5-8-5-8-10v-6z"/>',
  tag: '<path d="M20.5 13.5l-7 7a2 2 0 0 1-2.8 0l-7.2-7.2A2 2 0 0 1 3 11.9V4a1 1 0 0 1 1-1h7.9a2 2 0 0 1 1.4.6l7.2 7.2a2 2 0 0 1 0 2.7z"/><circle cx="7.5" cy="7.5" r="1.3"/>',
  package: '<path d="M21 16V8a2 2 0 0 0-1-1.7l-8-4.6a2 2 0 0 0-2 0l-8 4.6A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.7l8 4.6a2 2 0 0 0 2 0l8-4.6A2 2 0 0 0 21 16z"/><polyline points="3.3 7 12 12 20.7 7"/><line x1="12" y1="22" x2="12" y2="12"/>',
  clock: '<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/>',
  filter: '<polygon points="22 3 2 3 10 12.5 10 19 14 21 14 12.5 22 3"/>',
  chart: '<line x1="3" y1="21" x2="21" y2="21"/><rect x="5" y="11" width="3.5" height="7" rx="1"/><rect x="10.25" y="6" width="3.5" height="12" rx="1"/><rect x="15.5" y="13" width="3.5" height="5" rx="1"/>',
  palette: '<circle cx="12" cy="12" r="9.5"/><circle cx="8" cy="9" r="1.1"/><circle cx="12" cy="7.5" r="1.1"/><circle cx="16" cy="9" r="1.1"/><circle cx="16.5" cy="13.5" r="1.1"/><path d="M12 21.5c1.4 0 2-1 2-2s-.6-1.5-.6-2.2c0-.8.7-1.3 1.6-1.3H17"/>',
  edit: '<path d="M11 4H5a2 2 0 0 0-2 2v13a2 2 0 0 0 2 2h13a2 2 0 0 0 2-2v-6"/><path d="M18.5 2.5a2.1 2.1 0 0 1 3 3L12 15l-4 1 1-4z"/>',
  trash: '<polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>',
  settings: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.6 1.6 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.6 1.6 0 0 0-2.7 1.1V21a2 2 0 0 1-4 0v-.1a1.6 1.6 0 0 0-2.7-1.1l-.1.1A2 2 0 1 1 4.5 17l.1-.1A1.6 1.6 0 0 0 3.5 14H3a2 2 0 0 1 0-4h.1A1.6 1.6 0 0 0 4.6 7.3l-.1-.1A2 2 0 1 1 7.3 4.5l.1.1A1.6 1.6 0 0 0 10 3.5V3a2 2 0 0 1 4 0v.1a1.6 1.6 0 0 0 2.7 1.1l.1-.1A2 2 0 1 1 19.5 7l-.1.1a1.6 1.6 0 0 0 1.1 2.7H21a2 2 0 0 1 0 4h-.1a1.6 1.6 0 0 0-1.5 1z"/>',
  inbox: '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.5 5.5h13L22 12v6a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2v-6z"/>',
  eye: '<path d="M1.5 12S5 5 12 5s10.5 7 10.5 7-3.5 7-10.5 7S1.5 12 1.5 12z"/><circle cx="12" cy="12" r="3"/>',
  dollar: '<line x1="12" y1="1.5" x2="12" y2="22.5"/><path d="M17 5.5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>',
  external: '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
};

const inner = computed(() => PATHS[props.name] || "");
const dim = computed(() => (props.size ? `${props.size}px` : null));
</script>

<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="none"
    :stroke="'currentColor'"
    :stroke-width="stroke"
    stroke-linecap="round"
    stroke-linejoin="round"
    :width="dim"
    :height="dim"
    :class="dim ? '' : 'w-5 h-5'"
    aria-hidden="true"
    v-html="inner"
  />
</template>
