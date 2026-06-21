<script setup>
import { ref, onMounted } from "vue";
import { gsap } from "gsap";
import { useI18n } from "vue-i18n";
import { catalogApi } from "@/lib/api";
import { useCatalogStore } from "@/stores/catalog";
import { useProductFeed } from "@/composables/useProductFeed";
import ProductCard from "@/components/ProductCard.vue";
import ProductCarousel from "@/components/ProductCarousel.vue";
import PromoCarousel from "@/components/PromoCarousel.vue";
import CategorySidebar from "@/components/layout/CategorySidebar.vue";

const { t } = useI18n();
const catalog = useCatalogStore();

const featured = ref([]);
const bestSellers = ref([]);
const deals = ref([]);
const liveArrivals = ref([]);
const loading = ref(true);

const countdown = ref("00:00:00");
function startCountdown() {
  const end = new Date();
  end.setHours(23, 59, 59, 999);
  setInterval(() => {
    const diff = Math.max(0, end - new Date());
    const h = String(Math.floor(diff / 3.6e6)).padStart(2, "0");
    const m = String(Math.floor((diff % 3.6e6) / 6e4)).padStart(2, "0");
    const s = String(Math.floor((diff % 6e4) / 1e3)).padStart(2, "0");
    countdown.value = `${h}:${m}:${s}`;
  }, 1000);
}

onMounted(async () => {
  startCountdown();
  catalog.loadCategories();
  try {
    const [feat, best, deal] = await Promise.all([
      catalogApi.products({ featured: true, ordering: "-rating_avg" }),
      catalogApi.products({ ordering: "-sold_count" }),
      catalogApi.products({ ordering: "-created_at" }),
    ]);
    featured.value = feat.data.results.slice(0, 12);
    bestSellers.value = best.data.results.slice(0, 12);
    deals.value = deal.data.results.filter((p) => p.discount_percent > 0).slice(0, 12);
  } finally {
    loading.value = false;
  }
  gsap.from(".reveal", { y: 24, opacity: 0, duration: 0.6, stagger: 0.08, ease: "power2.out" });
});

// 🔴 Real-time: new products pop in live, no refresh.
useProductFeed((data) => {
  if (data.event === "product.created" && data.product) {
    liveArrivals.value.unshift(data.product);
    liveArrivals.value = liveArrivals.value.slice(0, 8);
  }
});
</script>

<template>
  <div class="container-x py-6 space-y-10">
    <!-- TOP: sidebar + offers carousel -->
    <section class="grid lg:grid-cols-[240px_1fr] gap-5">
      <CategorySidebar class="hidden lg:block reveal" />
      <PromoCarousel class="reveal" />
    </section>

    <!-- Live new arrivals (appears only when a vendor adds a product) -->
    <transition name="fade">
      <section v-if="liveArrivals.length" class="reveal">
        <div class="flex items-center gap-2 mb-3">
          <span class="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse"></span>
          <h2 class="text-xl font-extrabold">وصل حالاً 🔴 (مباشر)</h2>
        </div>
        <ProductCarousel :products="liveArrivals" />
      </section>
    </transition>

    <!-- FLASH DEALS -->
    <section class="reveal">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl md:text-2xl font-extrabold flex items-center gap-2">⚡ {{ t("home.flash") }}</h2>
        <span class="font-mono text-white px-3 py-1 rounded-lg tabular-nums" style="background: var(--c-accent)">{{ countdown }}</span>
      </div>
      <div v-if="loading" class="text-center py-10 text-ink/40">{{ t("common.loading") }}</div>
      <ProductCarousel v-else :products="deals" />
    </section>

    <!-- CATEGORIES GRID -->
    <section class="reveal">
      <h2 class="text-xl md:text-2xl font-extrabold mb-4">{{ t("home.categories") }}</h2>
      <div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <router-link v-for="c in catalog.topCategories" :key="c.id"
                     :to="{ name: 'products', query: { category: c.slug } }"
                     class="card p-4 flex flex-col items-center gap-2 hover:border-primary hover:-translate-y-1 transition text-center">
          <span class="w-12 h-12 grid place-items-center rounded-full text-2xl"
                style="background: color-mix(in srgb, var(--c-primary) 12%, transparent)">🛍️</span>
          <span class="text-xs font-bold">{{ c.name }}</span>
        </router-link>
      </div>
    </section>

    <!-- MOST ORDERED (replaces top vendors) -->
    <section class="reveal">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl md:text-2xl font-extrabold">🔥 الأكثر طلباً</h2>
        <router-link :to="{ name: 'products', query: { ordering: '-sold_count' } }" class="text-sm text-primary font-bold">عرض الكل</router-link>
      </div>
      <div v-if="loading" class="text-center py-10 text-ink/40">{{ t("common.loading") }}</div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <ProductCard v-for="p in bestSellers" :key="p.id" :product="p" />
      </div>
    </section>

    <!-- FEATURED -->
    <section class="reveal">
      <h2 class="text-xl md:text-2xl font-extrabold mb-4">{{ t("home.featured") }}</h2>
      <div v-if="loading" class="text-center py-10 text-ink/40">{{ t("common.loading") }}</div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <ProductCard v-for="p in featured" :key="p.id" :product="p" />
      </div>
    </section>
  </div>
</template>
