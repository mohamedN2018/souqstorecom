<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

defineProps({
  title: { type: String, default: "لوحة التحكم" },
  subtitle: { type: String, default: "" },
  accent: { type: String, default: "var(--c-primary)" },
  nav: { type: Array, default: () => [] }, // [{ key, label, icon }]
  active: { type: String, default: "" },
});
const emit = defineEmits(["select"]);

const router = useRouter();
const auth = useAuthStore();
function logout() {
  auth.logout();
  router.push({ name: "home" });
}
</script>

<template>
  <div class="min-h-screen flex" style="background:#f1f5f9; color:#0f172a;">
    <!-- isolated sidebar -->
    <aside class="w-64 shrink-0 hidden md:flex flex-col text-white" :style="{ background: '#0f172a' }">
      <div class="h-16 flex items-center gap-2 px-5 border-b border-white/10">
        <span class="grid place-items-center w-9 h-9 rounded-lg font-extrabold" :style="{ background: accent }">س</span>
        <div>
          <div class="font-extrabold leading-tight">{{ title }}</div>
          <div class="text-[11px] opacity-60">{{ subtitle }}</div>
        </div>
      </div>
      <nav class="flex-1 p-3 space-y-1">
        <button v-for="item in nav" :key="item.key" @click="emit('select', item.key)"
                class="w-full text-right flex items-center gap-3 px-3 py-2.5 rounded-lg transition text-sm font-semibold"
                :class="active === item.key ? 'bg-white/15' : 'hover:bg-white/8 opacity-80'">
          <span class="text-lg">{{ item.icon }}</span> {{ item.label }}
        </button>
      </nav>
      <div class="p-3 border-t border-white/10 space-y-1">
        <router-link :to="{ name: 'home' }"
                     class="w-full flex items-center gap-2 px-3 py-2 rounded-lg hover:bg-white/8 text-sm">
          ← العودة للموقع
        </router-link>
        <button @click="logout" class="w-full text-right px-3 py-2 rounded-lg hover:bg-white/8 text-sm text-red-300">
          تسجيل الخروج
        </button>
      </div>
    </aside>

    <!-- main -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- isolated topbar -->
      <header class="h-16 bg-white border-b border-black/5 flex items-center justify-between px-5 sticky top-0 z-30">
        <div>
          <h1 class="font-extrabold text-lg">{{ title }}</h1>
          <p v-if="subtitle" class="text-xs text-ink/50">{{ subtitle }}</p>
        </div>
        <div class="flex items-center gap-3">
          <!-- mobile nav -->
          <select class="md:hidden rounded-lg border border-black/10 px-2 py-1 text-sm"
                  @change="emit('select', $event.target.value)">
            <option v-for="item in nav" :key="item.key" :value="item.key" :selected="active === item.key">{{ item.label }}</option>
          </select>
          <div class="text-right hidden sm:block">
            <div class="text-sm font-bold">{{ auth.user?.email }}</div>
            <div class="text-[11px] text-ink/50">{{ auth.role }}</div>
          </div>
          <span class="w-9 h-9 rounded-full grid place-items-center text-white font-bold" :style="{ background: accent }">
            {{ (auth.user?.email || '?')[0].toUpperCase() }}
          </span>
        </div>
      </header>

      <main class="flex-1 p-5 overflow-x-hidden">
        <slot />
      </main>
    </div>
  </div>
</template>
