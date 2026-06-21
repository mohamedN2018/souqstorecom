<script setup>
import { onMounted } from "vue";
import { useCatalogStore } from "@/stores/catalog";
import Icon from "@/components/Icon.vue";

const catalog = useCatalogStore();
onMounted(() => catalog.loadCategories());
</script>

<template>
  <aside class="card p-2 h-fit">
    <h3 class="font-extrabold flex items-center gap-2 px-3 py-2.5 text-sm">
      <Icon name="grid" class="w-5 h-5 text-primary" /> تسوّق حسب القسم
    </h3>
    <ul class="space-y-0.5">
      <li v-for="c in catalog.topCategories" :key="c.id">
        <router-link :to="{ name: 'products', query: { category: c.slug } }"
                     class="group flex items-center justify-between px-3 py-2.5 rounded-xl hover:bg-primary/8 hover:text-primary transition text-sm font-semibold">
          <span class="flex items-center gap-2.5">
            <span class="grid place-items-center w-8 h-8 rounded-lg bg-primary/8 text-primary group-hover:bg-primary group-hover:text-white transition">
              <Icon name="tag" class="w-4 h-4" />
            </span>
            {{ c.name }}
          </span>
          <Icon name="chevron-left" class="w-4 h-4 text-ink/30 group-hover:text-primary -scale-x-100" />
        </router-link>
      </li>
    </ul>
  </aside>
</template>
