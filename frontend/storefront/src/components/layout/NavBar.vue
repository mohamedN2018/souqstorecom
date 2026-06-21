<script setup>
import { onMounted } from "vue";
import { useCatalogStore } from "@/stores/catalog";
import { useUiStore } from "@/stores/ui";

const catalog = useCatalogStore();
const ui = useUiStore();
onMounted(() => catalog.loadCategories());
</script>

<template>
  <nav class="text-white" style="background: var(--c-primary)">
    <div class="container-x flex items-center gap-1 h-11 overflow-x-auto no-scrollbar">
      <button @click="ui.openDrawer()"
              class="flex items-center gap-1.5 px-3 py-1.5 rounded-theme bg-white/15 hover:bg-white/25 font-bold whitespace-nowrap text-sm shrink-0">
        ☰ كل الأقسام
      </button>
      <router-link :to="{ name: 'products' }"
                   class="px-3 py-1.5 rounded-theme hover:bg-white/15 whitespace-nowrap text-sm">كل المنتجات</router-link>
      <router-link v-for="c in catalog.topCategories.slice(0, 8)" :key="c.id"
                   :to="{ name: 'products', query: { category: c.slug } }"
                   class="px-3 py-1.5 rounded-theme hover:bg-white/15 whitespace-nowrap text-sm">
        {{ c.name }}
      </router-link>
      <router-link :to="{ name: 'vendors' }"
                   class="px-3 py-1.5 rounded-theme hover:bg-white/15 whitespace-nowrap text-sm">المتاجر</router-link>
    </div>
  </nav>
</template>
