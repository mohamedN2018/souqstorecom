<script setup>
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useSiteStore } from "@/stores/site";
import { setLocale } from "@/i18n";
import Icon from "@/components/Icon.vue";

const { t, locale } = useI18n();
const auth = useAuthStore();
const site = useSiteStore();
const router = useRouter();

function toggleLang() {
  setLocale(locale.value === "ar" ? "en" : "ar");
}
function logout() {
  auth.logout();
  router.push({ name: "home" });
}
</script>

<template>
  <div class="text-white text-xs" style="background: var(--c-secondary)">
    <div class="container-x flex items-center justify-between gap-3 h-9">
      <div class="flex items-center gap-4 opacity-90 min-w-0">
        <span class="flex items-center gap-1.5 truncate">
          <Icon name="truck" class="w-3.5 h-3.5 shrink-0" />
          <span class="truncate">{{ site.announcement || "شحن مجاني للطلبات فوق 500 ج.م" }}</span>
        </span>
        <span class="hidden md:flex items-center gap-1.5 shrink-0">
          <Icon name="phone" class="w-3.5 h-3.5" /> الدعم: 19999
        </span>
      </div>
      <div class="flex items-center gap-2.5 sm:gap-3 shrink-0">
        <button @click="toggleLang" class="flex items-center gap-1.5 hover:opacity-80">
          <Icon name="globe" class="w-3.5 h-3.5" />{{ locale === "ar" ? "English" : "العربية" }}
        </button>
        <span class="opacity-30">|</span>
        <template v-if="auth.isAuthenticated">
          <router-link v-if="auth.isAdmin" :to="{ name: 'admin' }" class="font-bold flex items-center gap-1">
            <Icon name="shield" class="w-3.5 h-3.5" />لوحة الإدارة
          </router-link>
          <router-link v-else-if="auth.isVendor || auth.isStaff" :to="{ name: 'dashboard' }" class="font-bold flex items-center gap-1">
            <Icon name="store" class="w-3.5 h-3.5" />لوحة المتجر
          </router-link>
          <span class="opacity-30">|</span>
          <span class="opacity-90 hidden sm:inline">{{ auth.user?.email }}</span>
          <button @click="logout" class="flex items-center gap-1 hover:opacity-80">
            <Icon name="logout" class="w-3.5 h-3.5" />خروج
          </button>
        </template>
        <template v-else>
          <router-link :to="{ name: 'login' }" class="hover:opacity-80">دخول</router-link>
          <span class="opacity-30">|</span>
          <router-link :to="{ name: 'vendor-register' }" class="font-bold flex items-center gap-1 text-amber-300">
            <Icon name="store" class="w-3.5 h-3.5" />بيع معنا
          </router-link>
        </template>
      </div>
    </div>
  </div>
</template>
