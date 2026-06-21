<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import Icon from "@/components/Icon.vue";

defineProps({
  title: { type: String, default: "لوحة التحكم" },
  subtitle: { type: String, default: "" },
  accent: { type: String, default: "var(--c-primary)" },
  nav: { type: Array, default: () => [] }, // [{ key, label, icon }]  icon = Icon name
  active: { type: String, default: "" },
});
const emit = defineEmits(["select"]);

const router = useRouter();
const auth = useAuthStore();
const mobileNav = ref(false);

function logout() {
  auth.logout();
  router.push({ name: "home" });
}
function pick(key) {
  emit("select", key);
  mobileNav.value = false;
}
</script>

<template>
  <div class="min-h-screen flex" style="background:#0b1120;">
    <!-- ============ SIDEBAR (desktop) ============ -->
    <aside class="w-[260px] shrink-0 hidden md:flex flex-col text-slate-300 sticky top-0 h-screen"
           style="background: linear-gradient(180deg,#0f172a,#0b1120);">
      <div class="h-[68px] flex items-center gap-3 px-5 border-b border-white/5">
        <span class="grid place-items-center w-10 h-10 rounded-xl text-white font-extrabold shadow-lg"
              :style="{ background: `linear-gradient(135deg, ${accent}, color-mix(in srgb, ${accent} 60%, #000))` }">س</span>
        <div class="min-w-0">
          <div class="font-extrabold text-white leading-tight truncate">{{ title }}</div>
          <div class="text-[11px] opacity-50">{{ subtitle }}</div>
        </div>
      </div>

      <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
        <button v-for="item in nav" :key="item.key" @click="pick(item.key)"
                class="group w-full flex items-center gap-3 px-3 py-2.5 rounded-xl transition text-sm font-semibold"
                :class="active === item.key ? 'text-white shadow-lg' : 'hover:bg-white/5 text-slate-400 hover:text-white'"
                :style="active === item.key ? { background: `linear-gradient(135deg, ${accent}, color-mix(in srgb, ${accent} 70%, #000))` } : {}">
          <Icon :name="item.icon" class="w-5 h-5 shrink-0" />
          <span class="truncate">{{ item.label }}</span>
        </button>
      </nav>

      <div class="p-3 border-t border-white/5 space-y-1">
        <router-link :to="{ name: 'home' }"
                     class="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl hover:bg-white/5 text-sm text-slate-400 hover:text-white transition">
          <Icon name="external" class="w-5 h-5" /> العودة للموقع
        </router-link>
        <button @click="logout"
                class="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl hover:bg-red-500/10 text-sm text-red-300 transition">
          <Icon name="logout" class="w-5 h-5" /> تسجيل الخروج
        </button>
      </div>
    </aside>

    <!-- ============ MOBILE DRAWER ============ -->
    <teleport to="body">
      <transition name="ov">
        <div v-if="mobileNav" class="md:hidden fixed inset-0 z-[80] bg-black/50" @click="mobileNav = false" />
      </transition>
      <transition name="dr">
        <aside v-if="mobileNav"
               class="md:hidden fixed top-0 bottom-0 right-0 z-[81] w-72 flex flex-col text-slate-300"
               style="background: linear-gradient(180deg,#0f172a,#0b1120);">
          <div class="h-16 flex items-center justify-between px-5 border-b border-white/5">
            <span class="font-extrabold text-white">{{ title }}</span>
            <button @click="mobileNav = false" class="grid place-items-center w-9 h-9 rounded-lg hover:bg-white/10"><Icon name="x" /></button>
          </div>
          <nav class="flex-1 p-3 space-y-1 overflow-y-auto">
            <button v-for="item in nav" :key="item.key" @click="pick(item.key)"
                    class="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-semibold"
                    :class="active === item.key ? 'text-white' : 'text-slate-400'"
                    :style="active === item.key ? { background: accent } : {}">
              <Icon :name="item.icon" class="w-5 h-5" /> {{ item.label }}
            </button>
          </nav>
          <div class="p-3 border-t border-white/5 space-y-1">
            <router-link :to="{ name: 'home' }" class="flex items-center gap-2.5 px-3 py-2.5 rounded-xl hover:bg-white/5 text-sm"><Icon name="external" class="w-5 h-5" /> العودة للموقع</router-link>
            <button @click="logout" class="w-full flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-red-300 text-sm"><Icon name="logout" class="w-5 h-5" /> خروج</button>
          </div>
        </aside>
      </transition>
    </teleport>

    <!-- ============ MAIN ============ -->
    <div class="flex-1 flex flex-col min-w-0" style="background:#f1f5f9; color:#0f172a;">
      <header class="h-[68px] bg-white/90 backdrop-blur border-b border-black/5 flex items-center justify-between gap-3 px-4 md:px-6 sticky top-0 z-30">
        <div class="flex items-center gap-3 min-w-0">
          <button @click="mobileNav = true" class="md:hidden grid place-items-center w-10 h-10 rounded-xl bg-black/5" aria-label="القائمة">
            <Icon name="menu" />
          </button>
          <div class="min-w-0">
            <h1 class="font-extrabold text-base md:text-lg truncate">{{ title }}</h1>
            <p v-if="subtitle" class="text-xs text-ink/50 truncate">{{ subtitle }}</p>
          </div>
        </div>
        <div class="flex items-center gap-3 shrink-0">
          <div class="text-left hidden sm:block">
            <div class="text-sm font-bold truncate max-w-[160px]">{{ auth.user?.email }}</div>
            <div class="text-[11px] text-ink/50">{{ auth.role }}</div>
          </div>
          <span class="w-10 h-10 rounded-xl grid place-items-center text-white font-bold shadow-md shrink-0"
                :style="{ background: `linear-gradient(135deg, ${accent}, color-mix(in srgb, ${accent} 65%, #000))` }">
            {{ (auth.user?.email || '?')[0].toUpperCase() }}
          </span>
        </div>
      </header>

      <main class="flex-1 p-4 md:p-6 overflow-x-hidden">
        <slot />
      </main>
    </div>
  </div>
</template>

<style scoped>
.ov-enter-active, .ov-leave-active { transition: opacity 0.25s ease; }
.ov-enter-from, .ov-leave-to { opacity: 0; }
.dr-enter-active, .dr-leave-active { transition: transform 0.3s cubic-bezier(0.4,0,0.2,1); }
.dr-enter-from, .dr-leave-to { transform: translateX(100%); }
</style>
