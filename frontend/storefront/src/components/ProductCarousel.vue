<script setup>
import { ref } from "vue";
import ProductCard from "@/components/ProductCard.vue";

defineProps({ products: { type: Array, default: () => [] } });
const track = ref(null);

function scroll(dir) {
  track.value?.scrollBy({ left: dir * 320, behavior: "smooth" });
}
</script>

<template>
  <div class="relative">
    <div ref="track" class="flex gap-4 overflow-x-auto scroll-smooth pb-2"
         style="scrollbar-width: none;">
      <div v-for="p in products" :key="p.id" class="w-44 md:w-52 shrink-0">
        <ProductCard :product="p" />
      </div>
    </div>
    <button @click="scroll(-1)" class="hidden md:grid place-items-center absolute top-1/2 -translate-y-1/2 -right-3 w-9 h-9 rounded-full bg-surface card shadow">›</button>
    <button @click="scroll(1)" class="hidden md:grid place-items-center absolute top-1/2 -translate-y-1/2 -left-3 w-9 h-9 rounded-full bg-surface card shadow">‹</button>
  </div>
</template>
