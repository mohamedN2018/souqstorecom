<script setup>
import { computed, ref } from "vue";
import { useI18n } from "vue-i18n";
import { useCartStore } from "@/stores/cart";
import Icon from "@/components/Icon.vue";

const props = defineProps({ product: { type: Object, required: true } });
const { t } = useI18n();
const cart = useCartStore();

const discount = computed(() => props.product.discount_percent || 0);
const wished = ref(false);
const added = ref(false);

function add() {
  cart.add(props.product);
  added.value = true;
  setTimeout(() => (added.value = false), 1200);
}
</script>

<template>
  <div class="card overflow-hidden group flex flex-col">
    <router-link :to="{ name: 'product', params: { slug: product.slug } }" class="relative block overflow-hidden">
      <img :src="product.primary_image" :alt="product.name"
           loading="lazy"
           class="w-full aspect-square object-cover group-hover:scale-110 transition-transform duration-500 ease-out" />

      <!-- badges -->
      <div class="absolute top-2.5 inset-x-2.5 flex items-start justify-between pointer-events-none">
        <span v-if="discount"
              class="pill text-white shadow-md"
              style="background: var(--c-accent)">-{{ discount }}%</span>
        <span v-if="product.is_featured"
              class="pill text-white shadow-md ms-auto"
              style="background: var(--c-primary)">
          <Icon name="sparkles" class="w-3.5 h-3.5" /> مميز
        </span>
      </div>

      <!-- wishlist -->
      <button @click.prevent="wished = !wished"
              class="absolute bottom-2.5 left-2.5 grid place-items-center w-9 h-9 rounded-full bg-white/90 shadow-md opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0 transition"
              :class="wished ? 'text-rose-500' : 'text-ink/50 hover:text-rose-500'"
              aria-label="المفضلة">
        <Icon name="heart" class="w-5 h-5" :stroke="wished ? 0 : 1.8" :style="wished ? 'fill: currentColor' : ''" />
      </button>
    </router-link>

    <div class="p-3.5 flex flex-col gap-2 flex-1">
      <router-link :to="{ name: 'product', params: { slug: product.slug } }"
                   class="font-semibold text-sm leading-snug line-clamp-2 hover:text-primary min-h-[2.5rem]">
        {{ product.name }}
      </router-link>

      <div class="flex items-center gap-1 text-xs">
        <Icon name="star" class="w-3.5 h-3.5 text-amber-400" stroke="0" style="fill: currentColor" />
        <span class="font-bold">{{ product.rating_avg }}</span>
        <span class="text-ink/40">({{ product.rating_count }})</span>
      </div>

      <div class="mt-auto flex items-end justify-between gap-2 pt-1">
        <div class="leading-tight">
          <div class="flex items-baseline gap-1">
            <span class="font-extrabold text-lg text-primary">{{ Number(product.price).toLocaleString() }}</span>
            <span class="text-[11px] text-ink/50">{{ t("common.currency") }}</span>
          </div>
          <div v-if="product.compare_at_price" class="text-xs text-ink/40 line-through">
            {{ Number(product.compare_at_price).toLocaleString() }}
          </div>
        </div>
        <button @click="add"
                class="grid place-items-center w-10 h-10 rounded-xl text-white shadow-md active:scale-90 transition"
                :style="{ background: added ? '#16a34a' : 'var(--c-primary)' }"
                aria-label="أضف للسلة">
          <Icon :name="added ? 'check' : 'plus'" class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>
