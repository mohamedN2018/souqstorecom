<script setup>
import { ref, onMounted } from "vue";
import { gsap } from "gsap";
import { useI18n } from "vue-i18n";
import { catalogApi, vendorApi } from "@/lib/api";
import ProductCard from "@/components/ProductCard.vue";

const { t } = useI18n();
const categories = ref([]);
const featured = ref([]);
const vendors = ref([]);
const loading = ref(true);

// Flash-sale countdown
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
  try {
    const [cats, feat, vens] = await Promise.all([
      catalogApi.categories(),
      catalogApi.products({ featured: true, ordering: "-sold_count" }),
      vendorApi.list({ ordering: "-rating_avg" }),
    ]);
    categories.value = cats.data.filter((c) => !c.parent);
    featured.value = feat.data.results.slice(0, 12);
    vendors.value = vens.data.results.slice(0, 8);
  } finally {
    loading.value = false;
  }

  gsap.from(".hero-anim", { y: 30, opacity: 0, duration: 0.8, stagger: 0.12, ease: "power3.out" });
  gsap.from(".cat-chip", { scale: 0.8, opacity: 0, duration: 0.5, stagger: 0.05, delay: 0.3, ease: "back.out(1.6)" });
});
</script>

<template>
  <!-- HERO -->
  <section class="relative overflow-hidden text-white"
           style="background: linear-gradient(135deg, var(--c-primary), var(--c-secondary))">
    <div class="container-x py-16 md:py-24 relative z-10">
      <h1 class="hero-anim text-3xl md:text-5xl font-extrabold leading-tight max-w-2xl">
        {{ t("home.hero_title") }}
      </h1>
      <p class="hero-anim mt-4 text-lg opacity-90 max-w-xl">{{ t("home.hero_sub") }}</p>
      <router-link :to="{ name: 'products' }"
                   class="hero-anim inline-block mt-8 bg-white text-ink font-bold px-7 py-3 rounded-theme hover:-translate-y-1 transition"
                   style="color: var(--c-primary)">
        {{ t("home.shop_now") }} ←
      </router-link>
    </div>
    <div class="absolute -top-20 -left-20 w-80 h-80 rounded-full bg-white/10"></div>
    <div class="absolute -bottom-24 right-10 w-96 h-96 rounded-full bg-white/10"></div>
  </section>

  <!-- FLASH BAR -->
  <div class="text-white" style="background: var(--c-accent)">
    <div class="container-x py-3 flex items-center justify-center gap-3 font-bold">
      ⚡ {{ t("home.flash") }}
      <span class="font-mono bg-black/20 px-3 py-1 rounded-lg tabular-nums">{{ countdown }}</span>
    </div>
  </div>

  <div class="container-x py-10 space-y-12">
    <!-- CATEGORIES -->
    <section>
      <h2 class="text-2xl font-extrabold mb-5">{{ t("home.categories") }}</h2>
      <div class="flex flex-wrap gap-3">
        <router-link v-for="c in categories" :key="c.id"
                     :to="{ name: 'products', query: { category: c.slug } }"
                     class="cat-chip card px-4 py-3 font-semibold hover:text-primary hover:border-primary transition">
          {{ c.name }}
          <span class="text-xs text-ink/50">({{ c.products_count }})</span>
        </router-link>
      </div>
    </section>

    <!-- FEATURED -->
    <section>
      <h2 class="text-2xl font-extrabold mb-5">{{ t("home.featured") }}</h2>
      <div v-if="loading" class="text-center py-10 text-ink/50">{{ t("common.loading") }}</div>
      <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <ProductCard v-for="p in featured" :key="p.id" :product="p" />
      </div>
    </section>

    <!-- VENDORS -->
    <section>
      <h2 class="text-2xl font-extrabold mb-5">{{ t("home.top_vendors") }}</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <router-link v-for="v in vendors" :key="v.id"
                     :to="{ name: 'vendor', params: { slug: v.slug } }"
                     class="card p-4 flex items-center gap-3 hover:border-primary transition">
          <img :src="v.logo_url" class="w-12 h-12 rounded-full object-cover" />
          <div>
            <div class="font-bold text-sm">{{ v.name }}</div>
            <div class="text-xs text-amber-500">★ {{ v.rating_avg }}</div>
          </div>
        </router-link>
      </div>
    </section>
  </div>
</template>
