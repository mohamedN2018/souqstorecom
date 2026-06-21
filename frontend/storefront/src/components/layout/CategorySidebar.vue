<script setup>
import { onMounted } from "vue";
import { useCatalogStore } from "@/stores/catalog";

const catalog = useCatalogStore();
onMounted(() => catalog.loadCategories());
</script>

<template>
  <aside class="card p-4 h-fit">
    <h3 class="font-extrabold mb-3 flex items-center gap-2">☰ الأقسام</h3>
    <ul class="space-y-1">
      <li v-for="c in catalog.topCategories" :key="c.id">
        <router-link :to="{ name: 'products', query: { category: c.slug } }"
                     class="flex items-center justify-between px-2 py-2 rounded-theme hover:bg-primary/10 hover:text-primary transition text-sm font-semibold">
          <span>{{ c.name }}</span>
          <span class="text-xs text-ink/40">{{ c.products_count }}</span>
        </router-link>
      </li>
    </ul>
  </aside>
</template>
