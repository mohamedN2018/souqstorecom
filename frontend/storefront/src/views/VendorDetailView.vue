<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRoute } from "vue-router";
import { vendorApi, catalogApi } from "@/lib/api";
import { useThemeStore } from "@/stores/theme";
import ProductCard from "@/components/ProductCard.vue";

const route = useRoute();
const theme = useThemeStore();
const vendor = ref(null);
const products = ref([]);
const loading = ref(true);

onMounted(async () => {
  const { data } = await vendorApi.detail(route.params.slug);
  vendor.value = data;
  // Apply this store's custom theme live — demonstrates per-vendor theming.
  theme.applyVendorTheme(data.theme);

  const res = await catalogApi.products({ vendor: data.id, ordering: "-sold_count" });
  products.value = res.data.results;
  loading.value = false;
});

// Restore the global theme when leaving the store page.
onUnmounted(() => theme.reset());
</script>

<template>
  <div v-if="vendor">
    <div class="h-48 md:h-64 relative" :style="{ background: 'linear-gradient(135deg, var(--c-primary), var(--c-secondary))' }">
      <img v-if="vendor.banner_url" :src="vendor.banner_url" class="w-full h-full object-cover opacity-80" />
    </div>
    <div class="container-x -mt-12 relative">
      <div class="card p-5 flex items-center gap-4">
        <img :src="vendor.logo_url" class="w-20 h-20 rounded-2xl object-cover border-4 border-surface" />
        <div class="flex-1">
          <h1 class="text-xl font-extrabold">{{ vendor.name }}</h1>
          <p class="text-sm text-ink/60">{{ vendor.tagline }}</p>
          <div class="text-xs text-ink/50 mt-1">
            ★ {{ vendor.rating_avg }} ({{ vendor.rating_count }}) · {{ vendor.city }} · {{ vendor.products_count }} منتج
          </div>
        </div>
        <span class="text-xs font-bold text-white px-3 py-1 rounded-full self-start" style="background: var(--c-accent)">
          مطبّق ثيم المتجر 🎨
        </span>
      </div>
    </div>

    <div class="container-x py-8">
      <h2 class="text-lg font-extrabold mb-4">منتجات المتجر</h2>
      <div v-if="loading" class="text-center py-16 text-ink/50">جاري التحميل...</div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-5 gap-4">
        <ProductCard v-for="p in products" :key="p.id" :product="p" />
      </div>
    </div>
  </div>
</template>
