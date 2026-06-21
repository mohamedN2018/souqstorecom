<script setup>
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";
import { gsap } from "gsap";
import { useI18n } from "vue-i18n";
import { catalogApi } from "@/lib/api";
import { useCartStore } from "@/stores/cart";

const { t } = useI18n();
const route = useRoute();
const cart = useCartStore();

const product = ref(null);
const activeImage = ref("");
const activeVariant = ref(null);
const loading = ref(true);

async function load() {
  loading.value = true;
  const { data } = await catalogApi.product(route.params.slug);
  product.value = data;
  activeImage.value = data.images?.[0]?.url || "";
  activeVariant.value = data.variants?.find((v) => v.is_default) || data.variants?.[0] || null;
  loading.value = false;
  requestAnimationFrame(() =>
    gsap.from(".pd-anim", { y: 20, opacity: 0, duration: 0.6, stagger: 0.08, ease: "power2.out" })
  );
}

onMounted(load);
watch(() => route.params.slug, load);
</script>

<template>
  <div v-if="loading" class="container-x py-20 text-center text-ink/50">{{ t("common.loading") }}</div>

  <div v-else-if="product" class="container-x py-8">
    <div class="grid md:grid-cols-2 gap-8">
      <!-- gallery -->
      <div class="pd-anim">
        <img :src="activeImage" class="w-full aspect-square object-cover rounded-theme card" />
        <div class="flex gap-2 mt-3">
          <img v-for="(img, i) in product.images" :key="i" :src="img.url"
               @click="activeImage = img.url"
               class="w-16 h-16 object-cover rounded-lg cursor-pointer border-2"
               :class="activeImage === img.url ? 'border-primary' : 'border-transparent'" />
        </div>
      </div>

      <!-- info -->
      <div class="pd-anim space-y-4">
        <div class="text-sm text-primary font-semibold">{{ product.brand }}</div>
        <h1 class="text-2xl font-extrabold">{{ product.name }}</h1>
        <div class="flex items-center gap-2 text-amber-500">
          ★ {{ product.rating_avg }}
          <span class="text-ink/50 text-sm">({{ product.rating_count }} {{ t("product.reviews") }})</span>
          <span class="text-ink/40 text-sm">· {{ t("product.sold") }} {{ product.sold_count }}</span>
        </div>

        <div class="flex items-end gap-3">
          <span class="text-3xl font-extrabold text-primary">
            {{ Number(activeVariant?.price ?? product.price).toLocaleString() }}
            <span class="text-base">{{ t("common.currency") }}</span>
          </span>
          <span v-if="product.compare_at_price"
                class="text-ink/40 line-through">{{ Number(product.compare_at_price).toLocaleString() }}</span>
          <span v-if="product.discount_percent"
                class="text-white text-xs font-bold px-2 py-1 rounded-full" style="background: var(--c-accent)">
            -{{ product.discount_percent }}% {{ t("product.off") }}
          </span>
        </div>

        <!-- variants -->
        <div v-if="product.variants?.length > 1" class="space-y-2">
          <div class="text-sm font-semibold">الخيارات</div>
          <div class="flex flex-wrap gap-2">
            <button v-for="v in product.variants" :key="v.id" @click="activeVariant = v"
                    class="px-3 py-2 rounded-theme border text-sm"
                    :class="activeVariant?.id === v.id ? 'border-primary text-primary font-bold' : 'border-black/10'">
              {{ Object.values(v.attributes).join(" / ") }}
            </button>
          </div>
        </div>

        <p class="text-ink/70 leading-relaxed">{{ product.description }}</p>

        <div class="flex gap-3 pt-2">
          <button @click="cart.add({ ...product, primary_image: activeImage })" class="btn-primary flex-1">
            {{ t("product.add_to_cart") }} 🛒
          </button>
          <button class="px-5 py-2 rounded-theme font-bold text-white" style="background: var(--c-secondary)">
            {{ t("product.buy_now") }}
          </button>
        </div>
      </div>
    </div>

    <!-- reviews -->
    <section v-if="product.recent_reviews?.length" class="mt-12">
      <h2 class="text-xl font-extrabold mb-4">{{ t("product.reviews") }}</h2>
      <div class="grid md:grid-cols-2 gap-4">
        <div v-for="r in product.recent_reviews" :key="r.id" class="card p-4">
          <div class="flex items-center justify-between">
            <span class="font-bold">{{ r.customer_name }}</span>
            <span class="text-amber-500 text-sm">{{ "★".repeat(r.rating) }}</span>
          </div>
          <div class="font-semibold text-sm mt-1">{{ r.title }}</div>
          <p class="text-sm text-ink/60 mt-1">{{ r.body }}</p>
        </div>
      </div>
    </section>
  </div>
</template>
