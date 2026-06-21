<script setup>
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import { useCartStore } from "@/stores/cart";

const props = defineProps({ product: { type: Object, required: true } });
const { t } = useI18n();
const cart = useCartStore();

const discount = computed(() => props.product.discount_percent || 0);
</script>

<template>
  <div class="card overflow-hidden group flex flex-col">
    <router-link :to="{ name: 'product', params: { slug: product.slug } }" class="relative block">
      <img :src="product.primary_image" :alt="product.name"
           loading="lazy"
           class="w-full aspect-square object-cover group-hover:scale-105 transition-transform duration-300" />
      <span v-if="discount"
            class="absolute top-2 left-2 text-xs font-bold text-white px-2 py-1 rounded-full"
            style="background: var(--c-accent)">-{{ discount }}%</span>
      <span v-if="product.is_featured"
            class="absolute top-2 right-2 text-xs font-bold text-white px-2 py-1 rounded-full"
            style="background: var(--c-primary)">⭐ مميز</span>
    </router-link>

    <div class="p-3 flex flex-col gap-2 flex-1">
      <router-link :to="{ name: 'product', params: { slug: product.slug } }"
                   class="font-semibold text-sm leading-snug line-clamp-2 hover:text-primary">
        {{ product.name }}
      </router-link>

      <div class="flex items-center gap-1 text-xs text-amber-500">
        ★ <span class="text-ink/60">{{ product.rating_avg }} ({{ product.rating_count }})</span>
      </div>

      <div class="mt-auto flex items-end justify-between">
        <div>
          <span class="font-extrabold text-primary">{{ Number(product.price).toLocaleString() }}</span>
          <span class="text-xs"> {{ t("common.currency") }}</span>
          <div v-if="product.compare_at_price" class="text-xs text-ink/40 line-through">
            {{ Number(product.compare_at_price).toLocaleString() }}
          </div>
        </div>
        <button @click="cart.add(product)"
                class="text-white text-xs font-bold px-3 py-2 rounded-theme active:scale-95 transition"
                style="background: var(--c-primary)">＋</button>
      </div>
    </div>
  </div>
</template>
