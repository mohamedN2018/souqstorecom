<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useCartStore } from "@/stores/cart";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";

const { t } = useI18n();
const router = useRouter();
const cart = useCartStore();
const auth = useAuthStore();
const ui = useUiStore();
const q = ref("");

function search() {
  router.push({ name: "products", query: q.value ? { search: q.value } : {} });
}
</script>

<template>
  <div class="bg-surface/95 backdrop-blur border-b border-black/5">
    <div class="container-x flex items-center gap-3 md:gap-4 h-16">
      <!-- Departments (Amazon-style) -->
      <button @click="ui.openDrawer()"
              class="flex items-center gap-2 font-bold text-sm hover:text-primary shrink-0">
        <span class="text-xl">☰</span>
        <span class="hidden sm:block">الأقسام</span>
      </button>

      <router-link :to="{ name: 'home' }" class="flex items-center gap-2 shrink-0">
        <span class="grid place-items-center w-10 h-10 rounded-2xl text-white font-extrabold text-lg shadow-lg"
              style="background: linear-gradient(135deg, var(--c-primary), var(--c-secondary))">س</span>
        <span class="font-extrabold text-xl hidden lg:block">{{ t("brand") }}</span>
      </router-link>

      <!-- search -->
      <form @submit.prevent="search" class="flex-1 max-w-2xl">
        <div class="flex shadow-sm rounded-2xl overflow-hidden ring-1 ring-black/5 focus-within:ring-2 focus-within:ring-primary transition">
          <input v-model="q" :placeholder="t('common.search')"
                 class="w-full bg-black/[0.03] px-4 py-2.5 outline-none text-sm" />
          <button class="text-white px-5 font-bold" style="background: var(--c-primary)">🔍</button>
        </div>
      </form>

      <router-link :to="auth.isAuthenticated ? (auth.isAdmin ? { name: 'admin' } : auth.isVendor || auth.isStaff ? { name: 'dashboard' } : { name: 'home' }) : { name: 'login' }"
                   class="hidden md:flex flex-col items-center text-xs hover:text-primary shrink-0">
        <span class="text-xl">👤</span>
        <span>{{ auth.isAuthenticated ? "حسابي" : "دخول" }}</span>
      </router-link>

      <router-link :to="{ name: 'cart' }" class="relative flex flex-col items-center text-xs hover:text-primary shrink-0">
        <span class="text-xl">🛒</span>
        <span class="hidden sm:block">{{ t("nav.cart") }}</span>
        <span v-if="cart.count"
              class="absolute -top-1.5 -left-1.5 text-[10px] font-bold text-white w-5 h-5 grid place-items-center rounded-full shadow"
              style="background: var(--c-accent)">{{ cart.count }}</span>
      </router-link>
    </div>
  </div>
</template>
