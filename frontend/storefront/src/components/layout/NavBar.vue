<script setup>
import { onMounted } from "vue";
import { useCatalogStore } from "@/stores/catalog";

const catalog = useCatalogStore();
onMounted(() => catalog.loadCategories());
</script>

<template>
  <nav class="text-white" style="background: var(--c-primary)">
    <div class="container-x flex items-center gap-1 h-11 overflow-x-auto">
      <router-link :to="{ name: 'home' }"
                   class="px-3 py-1.5 rounded-theme hover:bg-white/15 font-bold whitespace-nowrap text-sm">
        🏠 الرئيسية
      </router-link>
      <router-link :to="{ name: 'products' }"
                   class="px-3 py-1.5 rounded-theme hover:bg-white/15 whitespace-nowrap text-sm">
        كل المنتجات
      </router-link>
      <router-link v-for="c in catalog.topCategories.slice(0, 8)" :key="c.id"
                   :to="{ name: 'products', query: { category: c.slug } }"
                   class="px-3 py-1.5 rounded-theme hover:bg-white/15 whitespace-nowrap text-sm">
        {{ c.name }}
      </router-link>
      <router-link :to="{ name: 'vendors' }"
                   class="px-3 py-1.5 rounded-theme hover:bg-white/15 whitespace-nowrap text-sm">
        المتاجر
      </router-link>
    </div>
  </nav>
</template>
