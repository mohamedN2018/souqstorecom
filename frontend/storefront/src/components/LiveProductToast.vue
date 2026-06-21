<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useProductFeed } from "@/composables/useProductFeed";

const router = useRouter();
const toasts = ref([]);

// When ANY vendor adds a product, surface it live across the storefront.
useProductFeed((ev) => {
  if (ev.event !== "product.created" || !ev.product) return;
  const id = `${ev.product.id}-${toasts.value.length}`;
  toasts.value.push({ id, product: ev.product });
  setTimeout(() => dismiss(id), 6000);
});

function dismiss(id) {
  toasts.value = toasts.value.filter((t) => t.id !== id);
}
function open(p) {
  dismiss(p.id);
  router.push({ name: "product", params: { slug: p.product.slug } });
}
</script>

<template>
  <teleport to="body">
    <div class="fixed bottom-5 left-5 z-[70] space-y-3 w-72">
      <transition-group name="toast">
        <button v-for="t in toasts" :key="t.id" @click="open(t)"
                class="w-full flex items-center gap-3 bg-surface shadow-2xl rounded-2xl p-3 border border-black/5 text-right hover:-translate-y-0.5 transition">
          <img :src="t.product.primary_image" class="w-14 h-14 rounded-xl object-cover bg-black/5 shrink-0" />
          <div class="min-w-0">
            <div class="flex items-center gap-1.5 text-[11px] font-bold text-red-500">
              <span class="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span> منتج جديد الآن
            </div>
            <div class="font-semibold text-sm line-clamp-1">{{ t.product.name }}</div>
            <div class="text-primary font-bold text-sm">{{ Number(t.product.price).toLocaleString() }} ج.م</div>
          </div>
        </button>
      </transition-group>
    </div>
  </teleport>
</template>

<style scoped>
.toast-enter-active, .toast-leave-active { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
.toast-enter-from { opacity: 0; transform: translateX(-30px); }
.toast-leave-to { opacity: 0; transform: translateX(-30px); }
</style>
