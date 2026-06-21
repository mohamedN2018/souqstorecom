<script setup>
import { ref, onMounted } from "vue";
import { gsap } from "gsap";
import { useI18n } from "vue-i18n";
import { catalogApi, vendorApi } from "@/lib/api";
import { useCatalogStore } from "@/stores/catalog";
import { useProductFeed } from "@/composables/useProductFeed";
import ProductCard from "@/components/ProductCard.vue";
import ProductCarousel from "@/components/ProductCarousel.vue";
import PromoCarousel from "@/components/PromoCarousel.vue";
import CategorySidebar from "@/components/layout/CategorySidebar.vue";
import Icon from "@/components/Icon.vue";

const { t } = useI18n();
const catalog = useCatalogStore();

const featured = ref([]);
const bestSellers = ref([]);
const deals = ref([]);
const vendors = ref([]);
const liveArrivals = ref([]);
const loading = ref(true);

const trust = [
  { icon: "truck", title: "شحن سريع", sub: "توصيل لكل المحافظات" },
  { icon: "shield", title: "دفع آمن", sub: "حماية كاملة لبياناتك" },
  { icon: "package", title: "إرجاع مجاني", sub: "خلال 14 يوم" },
  { icon: "phone", title: "دعم 24/7", sub: "فريق جاهز لمساعدتك" },
];

const catGradients = [
  ["#4f46e5", "#7c3aed"], ["#0891b2", "#0e7490"], ["#db2777", "#9333ea"],
  ["#ea580c", "#dc2626"], ["#16a34a", "#0d9488"], ["#2563eb", "#1d4ed8"],
  ["#d97706", "#b45309"], ["#7c3aed", "#c026d3"],
];

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
  // Resilient: each section loads independently — one failing request never
  // blanks the whole page.
  const [feat, best, deal, vens] = await Promise.allSettled([
    catalogApi.products({ featured: true, ordering: "-rating_avg" }),
    catalogApi.products({ ordering: "-sold_count" }),
    catalogApi.products({ ordering: "-created_at" }),
    vendorApi.list({ ordering: "-rating_avg" }),
  ]);
  if (feat.status === "fulfilled") featured.value = feat.value.data.results.slice(0, 12);
  if (best.status === "fulfilled") bestSellers.value = best.value.data.results.slice(0, 12);
  if (deal.status === "fulfilled") deals.value = deal.value.data.results.filter((p) => p.discount_percent > 0).slice(0, 12);
  if (vens.status === "fulfilled") vendors.value = vens.value.data.results.slice(0, 12);
  loading.value = false;
  gsap.from(".reveal", { y: 24, opacity: 0, duration: 0.6, stagger: 0.06, ease: "power2.out" });
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
  <div class="container-x py-6 space-y-12">
    <!-- HERO: sidebar + offers carousel -->
    <section class="grid lg:grid-cols-[260px_1fr] gap-5">
      <CategorySidebar class="hidden lg:block reveal" />
      <PromoCarousel class="reveal" />
    </section>

    <!-- TRUST STRIP -->
    <section class="reveal grid grid-cols-2 lg:grid-cols-4 gap-3">
      <div v-for="b in trust" :key="b.title"
           class="card p-4 flex items-center gap-3">
        <span class="grid place-items-center w-11 h-11 rounded-xl shrink-0 text-primary"
              style="background: color-mix(in srgb, var(--c-primary) 10%, transparent)">
          <Icon :name="b.icon" class="w-5 h-5" />
        </span>
        <div class="leading-tight">
          <div class="font-bold text-sm">{{ b.title }}</div>
          <div class="text-xs text-ink/50">{{ b.sub }}</div>
        </div>
      </div>
    </section>

    <!-- Live new arrivals (appears only when a vendor adds a product) -->
    <transition name="fade">
      <section v-if="liveArrivals.length" class="reveal">
        <div class="flex items-center gap-2 mb-4">
          <span class="relative flex w-3 h-3">
            <span class="absolute inline-flex w-full h-full rounded-full bg-red-500 opacity-60 animate-ping"></span>
            <span class="relative inline-flex w-3 h-3 rounded-full bg-red-500"></span>
          </span>
          <h2 class="section-title text-xl md:text-2xl">وصل حالاً <span class="pill bg-red-500/10 text-red-500">مباشر</span></h2>
        </div>
        <ProductCarousel :products="liveArrivals" />
      </section>
    </transition>

    <!-- FLASH DEALS -->
    <section class="reveal">
      <div class="flex items-center justify-between mb-5 flex-wrap gap-3">
        <h2 class="section-title text-xl md:text-2xl">
          <span class="grid place-items-center w-9 h-9 rounded-xl text-white" style="background: var(--c-accent)">
            <Icon name="zap" class="w-5 h-5" />
          </span>
          عروض اليوم
        </h2>
        <span class="flex items-center gap-2 text-sm">
          <span class="text-ink/50">ينتهي خلال</span>
          <span class="font-mono text-white px-3 py-1.5 rounded-xl tabular-nums tracking-widest shadow-md" style="background: var(--c-secondary)">{{ countdown }}</span>
        </span>
      </div>
      <div v-if="loading" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div v-for="i in 6" :key="i" class="card overflow-hidden">
          <div class="skeleton aspect-square"></div>
          <div class="p-3 space-y-2"><div class="skeleton h-4 rounded"></div><div class="skeleton h-4 w-2/3 rounded"></div></div>
        </div>
      </div>
      <ProductCarousel v-else :products="deals" />
    </section>

    <!-- CATEGORIES GRID -->
    <section class="reveal">
      <h2 class="section-title text-xl md:text-2xl mb-5">
        <Icon name="grid" class="w-6 h-6 text-primary" /> تسوّق حسب القسم
      </h2>
      <div class="grid grid-cols-3 md:grid-cols-4 lg:grid-cols-8 gap-3">
        <router-link v-for="(c, i) in catalog.topCategories" :key="c.id"
                     :to="{ name: 'products', query: { category: c.slug } }"
                     class="card p-4 flex flex-col items-center gap-2.5 hover:-translate-y-1.5 transition text-center">
          <span class="grid place-items-center w-14 h-14 rounded-2xl text-white shadow-md"
                :style="{ background: `linear-gradient(135deg, ${catGradients[i % catGradients.length][0]}, ${catGradients[i % catGradients.length][1]})` }">
            <Icon name="tag" class="w-6 h-6" />
          </span>
          <span class="text-xs font-bold line-clamp-1">{{ c.name }}</span>
          <span class="text-[10px] text-ink/40">{{ c.products_count }} منتج</span>
        </router-link>
      </div>
    </section>

    <!-- MOST ORDERED -->
    <section class="reveal">
      <div class="flex items-center justify-between mb-5">
        <h2 class="section-title text-xl md:text-2xl">
          <Icon name="flame" class="w-6 h-6 text-accent" /> الأكثر طلباً
        </h2>
        <router-link :to="{ name: 'products', query: { ordering: '-sold_count' } }" class="btn-ghost text-sm py-2">
          عرض الكل <Icon name="chevron-left" class="w-4 h-4" />
        </router-link>
      </div>
      <div v-if="loading" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div v-for="i in 6" :key="i" class="card overflow-hidden">
          <div class="skeleton aspect-square"></div>
          <div class="p-3 space-y-2"><div class="skeleton h-4 rounded"></div><div class="skeleton h-4 w-2/3 rounded"></div></div>
        </div>
      </div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <ProductCard v-for="p in bestSellers" :key="p.id" :product="p" />
      </div>
    </section>

    <!-- STORES -->
    <section class="reveal">
      <div class="flex items-center justify-between mb-5">
        <h2 class="section-title text-xl md:text-2xl">
          <Icon name="store" class="w-6 h-6 text-primary" /> تسوّق من متاجرنا
        </h2>
        <router-link :to="{ name: 'vendors' }" class="btn-ghost text-sm py-2">
          كل المتاجر <Icon name="chevron-left" class="w-4 h-4" />
        </router-link>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        <router-link v-for="v in vendors" :key="v.id"
                     :to="{ name: 'vendor', params: { slug: v.slug } }"
                     class="card p-4 flex flex-col items-center gap-2 text-center hover:-translate-y-1.5 transition">
          <img :src="v.logo_url" class="w-16 h-16 rounded-full object-cover ring-2 ring-primary/15" />
          <div class="font-bold text-sm line-clamp-1">{{ v.name }}</div>
          <div class="flex items-center gap-1 text-xs">
            <Icon name="star" class="w-3.5 h-3.5 text-amber-400" stroke="0" style="fill: currentColor" />
            <span class="font-bold">{{ v.rating_avg }}</span>
          </div>
          <span class="pill bg-primary/8 text-primary">{{ v.products_count }} منتج</span>
        </router-link>
      </div>
    </section>

    <!-- FEATURED -->
    <section class="reveal">
      <h2 class="section-title text-xl md:text-2xl mb-5">
        <Icon name="sparkles" class="w-6 h-6 text-primary" /> {{ t("home.featured") }}
      </h2>
      <div v-if="loading" class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div v-for="i in 6" :key="i" class="card overflow-hidden">
          <div class="skeleton aspect-square"></div>
          <div class="p-3 space-y-2"><div class="skeleton h-4 rounded"></div><div class="skeleton h-4 w-2/3 rounded"></div></div>
        </div>
      </div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <ProductCard v-for="p in featured" :key="p.id" :product="p" />
      </div>
    </section>
  </div>
</template>
