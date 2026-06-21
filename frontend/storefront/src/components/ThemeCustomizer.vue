<script setup>
import { ref } from "vue";
import { useI18n } from "vue-i18n";
import { useThemeStore } from "@/stores/theme";

const { t } = useI18n();
const theme = useThemeStore();
const open = ref(false);

const PRESETS = [
  { primary: "#2563eb", accent: "#f59e0b" },
  { primary: "#16a34a", accent: "#facc15" },
  { primary: "#db2777", accent: "#22d3ee" },
  { primary: "#9333ea", accent: "#f97316" },
  { primary: "#dc2626", accent: "#fbbf24" },
  { primary: "#0891b2", accent: "#f43f5e" },
];

function applyPreset(p) {
  theme.primary = p.primary;
  theme.accent = p.accent;
  theme.apply();
}
</script>

<template>
  <!-- Floating control proving live "full custom color" theming -->
  <div class="fixed bottom-5 left-5 z-50">
    <button @click="open = !open"
            class="w-12 h-12 rounded-full text-white text-xl shadow-lg grid place-items-center"
            style="background: var(--c-primary)">🎨</button>

    <div v-if="open"
         class="absolute bottom-16 left-0 w-64 card p-4 shadow-2xl space-y-4 bg-surface">
      <div class="font-bold">{{ t("theme.customize") }}</div>

      <div class="flex flex-wrap gap-2">
        <button v-for="(p, i) in PRESETS" :key="i" @click="applyPreset(p)"
                class="w-8 h-8 rounded-full border-2 border-white shadow"
                :style="{ background: p.primary }" />
      </div>

      <label class="flex items-center justify-between text-sm">
        {{ t("theme.primary") }}
        <input type="color" :value="theme.primary"
               @input="theme.set('primary', $event.target.value)" class="w-10 h-8" />
      </label>
      <label class="flex items-center justify-between text-sm">
        {{ t("theme.accent") }}
        <input type="color" :value="theme.accent"
               @input="theme.set('accent', $event.target.value)" class="w-10 h-8" />
      </label>
      <label class="flex items-center justify-between text-sm">
        Radius
        <input type="range" min="0" max="28" :value="theme.radius"
               @input="theme.set('radius', Number($event.target.value))" />
      </label>

      <button @click="theme.reset()" class="w-full text-sm py-2 rounded-theme border border-black/10">
        {{ t("theme.reset") }}
      </button>
    </div>
  </div>
</template>
