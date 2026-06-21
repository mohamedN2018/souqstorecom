<script setup>
import { onMounted } from "vue";
import { useCatalogStore } from "@/stores/catalog";
import { useUiStore } from "@/stores/ui";
import Icon from "@/components/Icon.vue";

const catalog = useCatalogStore();
const ui = useUiStore();
onMounted(() => catalog.loadCategories());
</script>

<template>
  <nav class="text-white shadow-sm" style="background: var(--c-secondary)">
    <div class="container-x flex items-center gap-1.5 h-12 overflow-x-auto no-scrollbar">
      <button @click="ui.openDrawer()"
              class="flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-white/15 hover:bg-white/25 font-bold whitespace-nowrap text-sm shrink-0 transition">
        <Icon name="grid" class="w-4 h-4" /> كل الأقسام
      </button>
      <router-link :to="{ name: 'products' }"
                   class="px-3.5 py-1.5 rounded-full hover:bg-white/15 whitespace-nowrap text-sm font-semibold transition">
        كل المنتجات
      </router-link>
      <router-link :to="{ name: 'products', query: { ordering: '-sold_count' } }"
                   class="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full hover:bg-white/15 whitespace-nowrap text-sm font-semibold transition">
        <Icon name="flame" class="w-4 h-4" /> الأكثر مبيعاً
      </router-link>
      <router-link v-for="c in catalog.topCategories.slice(0, 8)" :key="c.id"
                   :to="{ name: 'products', query: { category: c.slug } }"
                   class="px-3.5 py-1.5 rounded-full hover:bg-white/15 whitespace-nowrap text-sm font-semibold transition">
        {{ c.name }}
      </router-link>
      <router-link :to="{ name: 'vendors' }"
                   class="flex items-center gap-1.5 px-3.5 py-1.5 rounded-full hover:bg-white/15 whitespace-nowrap text-sm font-semibold transition">
        <Icon name="store" class="w-4 h-4" /> المتاجر
      </router-link>
    </div>
  </nav>
</template>
