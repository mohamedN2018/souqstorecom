<script setup>
import { ref, watch, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { catalogApi } from "@/lib/api";
import ProductCard from "@/components/ProductCard.vue";

const { t } = useI18n();
const route = useRoute();
const router = useRouter();

const products = ref([]);
const categories = ref([]);
const count = ref(0);
const page = ref(1);
const loading = ref(false);

const filters = ref({
  category: route.query.category || "",
  search: route.query.search || "",
  min_price: "",
  max_price: "",
  ordering: "-created_at",
});

async function load() {
  loading.value = true;
  try {
    const params = { page: page.value };
    for (const [k, v] of Object.entries(filters.value)) if (v) params[k] = v;
    const { data } = await catalogApi.products(params);
    products.value = data.results;
    count.value = data.count;
  } finally {
    loading.value = false;
  }
}

function applyFilters() {
  page.value = 1;
  router.replace({ query: { ...filters.value } });
  load();
}

watch(() => route.query, (q) => {
  filters.value.category = q.category || "";
  filters.value.search = q.search || "";
  load();
});

onMounted(async () => {
  const { data } = await catalogApi.categories();
  categories.value = data;
  load();
});
</script>

<template>
  <div class="container-x py-8 grid lg:grid-cols-[260px_1fr] gap-6">
    <!-- FILTERS -->
    <aside class="card p-4 h-fit space-y-4 lg:sticky lg:top-20">
      <h3 class="font-extrabold">{{ t("common.filters") }}</h3>

      <div>
        <label class="text-sm font-semibold">الفئة</label>
        <select v-model="filters.category" @change="applyFilters"
                class="w-full mt-1 rounded-theme border border-black/10 px-2 py-2 bg-surface">
          <option value="">{{ t("common.all") }}</option>
          <option v-for="c in categories" :key="c.id" :value="c.slug">
            {{ c.parent ? "— " : "" }}{{ c.name }}
          </option>
        </select>
      </div>

      <div>
        <label class="text-sm font-semibold">{{ t("common.price") }}</label>
        <div class="flex gap-2 mt-1">
          <input v-model="filters.min_price" type="number" placeholder="من"
                 class="w-full rounded-theme border border-black/10 px-2 py-1" />
          <input v-model="filters.max_price" type="number" placeholder="إلى"
                 class="w-full rounded-theme border border-black/10 px-2 py-1" />
        </div>
      </div>

      <div>
        <label class="text-sm font-semibold">ترتيب</label>
        <select v-model="filters.ordering" @change="applyFilters"
                class="w-full mt-1 rounded-theme border border-black/10 px-2 py-2 bg-surface">
          <option value="-created_at">الأحدث</option>
          <option value="price">السعر: الأقل</option>
          <option value="-price">السعر: الأعلى</option>
          <option value="-rating_avg">الأعلى تقييماً</option>
          <option value="-sold_count">الأكثر مبيعاً</option>
        </select>
      </div>

      <button @click="applyFilters" class="btn-primary w-full">تطبيق</button>
    </aside>

    <!-- GRID -->
    <section>
      <div class="flex items-center justify-between mb-4">
        <h1 class="text-xl font-extrabold">{{ t("nav.products") }}</h1>
        <span class="text-sm text-ink/50">{{ count }} منتج</span>
      </div>

      <div v-if="loading" class="text-center py-20 text-ink/50">{{ t("common.loading") }}</div>
      <div v-else-if="!products.length" class="text-center py-20 text-ink/50">{{ t("common.empty") }}</div>
      <div v-else class="grid grid-cols-2 md:grid-cols-3 xl:grid-cols-4 gap-4">
        <ProductCard v-for="p in products" :key="p.id" :product="p" />
      </div>

      <!-- pagination -->
      <div v-if="count > 24" class="flex justify-center gap-2 mt-8">
        <button :disabled="page === 1" @click="page--; load()"
                class="px-4 py-2 card disabled:opacity-40">السابق</button>
        <span class="px-4 py-2 font-bold">{{ page }}</span>
        <button :disabled="page * 24 >= count" @click="page++; load()"
                class="px-4 py-2 card disabled:opacity-40">التالي</button>
      </div>
    </section>
  </div>
</template>
