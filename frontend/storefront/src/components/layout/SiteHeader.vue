<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useCartStore } from "@/stores/cart";
import { useAuthStore } from "@/stores/auth";

const { t } = useI18n();
const router = useRouter();
const cart = useCartStore();
const auth = useAuthStore();
const q = ref("");

function search() {
  router.push({ name: "products", query: q.value ? { search: q.value } : {} });
}
</script>

<template>
  <div class="bg-surface border-b border-black/5">
    <div class="container-x flex items-center gap-4 h-16">
      <router-link :to="{ name: 'home' }" class="flex items-center gap-2 shrink-0">
        <span class="grid place-items-center w-10 h-10 rounded-theme text-white font-extrabold text-lg"
              style="background: var(--c-primary)">س</span>
        <span class="font-extrabold text-xl hidden sm:block">{{ t("brand") }}</span>
      </router-link>

      <form @submit.prevent="search" class="flex-1 max-w-2xl">
        <div class="flex">
          <input v-model="q" :placeholder="t('common.search')"
                 class="w-full rounded-s-theme border border-black/10 bg-black/[0.03] px-4 py-2.5 outline-none focus:border-primary" />
          <button class="text-white px-5 rounded-e-theme font-bold" style="background: var(--c-primary)">🔍</button>
        </div>
      </form>

      <router-link :to="auth.isAuthenticated ? { name: 'dashboard' } : { name: 'login' }"
                   class="hidden md:flex flex-col items-center text-xs hover:text-primary">
        <span class="text-xl">👤</span>
        <span>{{ auth.isAuthenticated ? "حسابي" : "دخول" }}</span>
      </router-link>

      <router-link :to="{ name: 'cart' }" class="relative flex flex-col items-center text-xs hover:text-primary">
        <span class="text-xl">🛒</span>
        <span>{{ t("nav.cart") }}</span>
        <span v-if="cart.count"
              class="absolute -top-1 -left-1 text-[10px] font-bold text-white w-4 h-4 grid place-items-center rounded-full"
              style="background: var(--c-accent)">{{ cart.count }}</span>
      </router-link>
    </div>
  </div>
</template>
