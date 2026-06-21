<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useCartStore } from "@/stores/cart";
import { useAuthStore } from "@/stores/auth";
import { useUiStore } from "@/stores/ui";
import Icon from "@/components/Icon.vue";

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
  <div class="glass border-b border-black/5">
    <div class="container-x flex items-center gap-3 md:gap-5 h-[68px]">
      <!-- Departments (Amazon-style) -->
      <button @click="ui.openDrawer()"
              class="grid place-items-center w-10 h-10 rounded-xl bg-black/5 hover:bg-primary/10 hover:text-primary transition shrink-0"
              aria-label="الأقسام">
        <Icon name="menu" />
      </button>

      <router-link :to="{ name: 'home' }" class="flex items-center gap-2.5 shrink-0">
        <span class="grid place-items-center w-11 h-11 rounded-2xl text-white font-extrabold text-xl shadow-lg"
              style="background: linear-gradient(135deg, var(--c-primary), var(--c-accent))">س</span>
        <span class="font-extrabold text-xl hidden lg:block tracking-tight">{{ t("brand") }}</span>
      </router-link>

      <!-- search -->
      <form @submit.prevent="search" class="flex-1 max-w-2xl">
        <div class="group flex items-center bg-black/[0.04] rounded-2xl ring-1 ring-black/5 focus-within:ring-2 focus-within:ring-primary focus-within:bg-white transition">
          <span class="grid place-items-center w-11 h-11 text-ink/40 group-focus-within:text-primary">
            <Icon name="search" />
          </span>
          <input v-model="q" :placeholder="t('common.search')"
                 class="w-full bg-transparent py-3 outline-none text-sm" />
          <button class="m-1 text-white px-5 py-2 rounded-xl font-bold text-sm shrink-0"
                  style="background: var(--c-primary)">{{ t("common.search") }}</button>
        </div>
      </form>

      <router-link :to="auth.isAuthenticated ? (auth.isAdmin ? { name: 'admin' } : auth.isVendor || auth.isStaff ? { name: 'dashboard' } : { name: 'home' }) : { name: 'login' }"
                   class="hidden md:flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-black/5 transition shrink-0">
        <Icon name="user" class="w-6 h-6 text-ink/70" />
        <span class="flex flex-col leading-tight text-xs">
          <span class="text-ink/50">{{ auth.isAuthenticated ? "مرحباً" : "أهلاً بك" }}</span>
          <span class="font-bold">{{ auth.isAuthenticated ? "حسابي" : "سجّل دخول" }}</span>
        </span>
      </router-link>

      <router-link :to="{ name: 'cart' }"
                   class="relative flex items-center gap-2 px-3 py-2 rounded-xl hover:bg-black/5 transition shrink-0">
        <span class="relative">
          <Icon name="cart" class="w-6 h-6 text-ink/70" />
          <span v-if="cart.count"
                class="absolute -top-2 -left-2 text-[10px] font-bold text-white min-w-[18px] h-[18px] px-1 grid place-items-center rounded-full shadow"
                style="background: var(--c-accent)">{{ cart.count }}</span>
        </span>
        <span class="hidden sm:flex flex-col leading-tight text-xs">
          <span class="text-ink/50">السلة</span>
          <span class="font-bold">{{ cart.count }} منتج</span>
        </span>
      </router-link>
    </div>
  </div>
</template>
