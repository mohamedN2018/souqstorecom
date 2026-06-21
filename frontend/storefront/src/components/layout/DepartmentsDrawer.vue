<script setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useUiStore } from "@/stores/ui";
import { useCatalogStore } from "@/stores/catalog";
import Icon from "@/components/Icon.vue";

const ui = useUiStore();
const catalog = useCatalogStore();
const router = useRouter();
const expanded = ref(null);

onMounted(() => catalog.loadCategories());

function go(slug) {
  ui.closeDrawer();
  router.push({ name: "products", query: { category: slug } });
}
</script>

<template>
  <!-- Amazon-style departments slide-out -->
  <teleport to="body">
    <transition name="overlay">
      <div v-if="ui.drawer" class="fixed inset-0 z-[60] bg-black/50" @click="ui.closeDrawer()" />
    </transition>
    <transition name="drawer">
      <aside v-if="ui.drawer"
             class="fixed top-0 bottom-0 right-0 z-[61] w-[85vw] max-w-sm bg-surface shadow-2xl flex flex-col">
        <div class="h-16 flex items-center gap-3 px-5 text-white shrink-0" style="background: var(--c-primary)">
          <Icon name="grid" class="w-6 h-6" />
          <span class="font-extrabold text-lg">كل الأقسام</span>
          <button @click="ui.closeDrawer()" class="mr-auto grid place-items-center w-9 h-9 rounded-lg hover:bg-white/15 transition" aria-label="إغلاق">
            <Icon name="x" />
          </button>
        </div>

        <nav class="flex-1 overflow-y-auto py-2">
          <div v-for="c in catalog.topCategories" :key="c.id" class="border-b border-black/5">
            <button @click="expanded === c.id ? (expanded = null) : (expanded = c.id)"
                    class="w-full flex items-center justify-between px-5 py-3.5 font-bold hover:bg-primary/5 transition">
              <span class="flex items-center gap-3">
                <span class="grid place-items-center w-8 h-8 rounded-lg bg-primary/8 text-primary"><Icon name="tag" class="w-4 h-4" /></span>
                {{ c.name }}
              </span>
              <Icon name="chevron-down" class="w-4 h-4 text-ink/40 transition-transform" :class="expanded === c.id ? 'rotate-180' : ''" />
            </button>
            <transition name="expand">
              <div v-if="expanded === c.id" class="bg-black/[0.02]">
                <button @click="go(c.slug)" class="w-full text-right px-12 py-2.5 text-sm font-semibold text-primary hover:bg-primary/5">
                  كل {{ c.name }}
                </button>
                <button v-for="s in catalog.subsOf(c.id)" :key="s.id" @click="go(s.slug)"
                        class="w-full text-right px-12 py-2.5 text-sm hover:bg-primary/5 text-ink/70">
                  {{ s.name }}
                </button>
              </div>
            </transition>
          </div>
        </nav>

        <div class="p-4 border-t border-black/5 shrink-0">
          <router-link :to="{ name: 'vendors' }" @click="ui.closeDrawer()"
                       class="flex items-center justify-center gap-2 font-bold text-primary py-2 rounded-xl hover:bg-primary/8 transition">
            <Icon name="store" class="w-5 h-5" /> تصفّح كل المتاجر
          </router-link>
        </div>
      </aside>
    </transition>
  </teleport>
</template>

<style scoped>
.overlay-enter-active, .overlay-leave-active { transition: opacity 0.25s ease; }
.overlay-enter-from, .overlay-leave-to { opacity: 0; }
.drawer-enter-active, .drawer-leave-active { transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
.drawer-enter-from, .drawer-leave-to { transform: translateX(100%); }
.expand-enter-active, .expand-leave-active { transition: all 0.2s ease; overflow: hidden; }
.expand-enter-from, .expand-leave-to { max-height: 0; opacity: 0; }
.expand-enter-to, .expand-leave-from { max-height: 500px; opacity: 1; }
</style>
