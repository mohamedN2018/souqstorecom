<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useCartStore } from "@/stores/cart";
import { setLocale } from "@/i18n";

const { t, locale } = useI18n();
const router = useRouter();
const cart = useCartStore();
const q = ref("");

function search() {
  router.push({ name: "products", query: q.value ? { search: q.value } : {} });
}
function toggleLang() {
  setLocale(locale.value === "ar" ? "en" : "ar");
}
</script>

<template>
  <header class="sticky top-0 z-40 bg-surface/90 backdrop-blur border-b border-black/5">
    <div class="container-x flex items-center gap-4 h-16">
      <router-link :to="{ name: 'home' }" class="flex items-center gap-2 shrink-0">
        <span class="grid place-items-center w-9 h-9 rounded-theme text-white font-extrabold"
              style="background: var(--c-primary)">س</span>
        <span class="font-extrabold text-lg hidden sm:block">{{ t("brand") }}</span>
      </router-link>

      <form @submit.prevent="search" class="flex-1 max-w-xl">
        <input v-model="q" :placeholder="t('common.search')"
               class="w-full rounded-theme border border-black/10 bg-black/[0.03] px-4 py-2 outline-none focus:border-primary" />
      </form>

      <nav class="hidden md:flex items-center gap-5 font-semibold text-sm">
        <router-link :to="{ name: 'products' }" class="hover:text-primary">{{ t("nav.products") }}</router-link>
        <router-link :to="{ name: 'vendors' }" class="hover:text-primary">{{ t("nav.vendors") }}</router-link>
      </nav>

      <button @click="toggleLang" class="text-sm font-bold px-2 py-1 rounded-theme border border-black/10">
        {{ locale === "ar" ? "EN" : "ع" }}
      </button>

      <router-link :to="{ name: 'cart' }" class="relative">
        <span class="text-2xl">🛒</span>
        <span v-if="cart.count"
              class="absolute -top-2 -left-2 text-[11px] font-bold text-white w-5 h-5 grid place-items-center rounded-full"
              style="background: var(--c-accent)">{{ cart.count }}</span>
      </router-link>
    </div>
  </header>
</template>
