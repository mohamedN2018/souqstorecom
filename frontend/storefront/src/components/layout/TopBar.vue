<script setup>
import { useI18n } from "vue-i18n";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useSiteStore } from "@/stores/site";
import { setLocale } from "@/i18n";

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
    <div class="container-x flex items-center justify-between h-9">
      <div class="flex items-center gap-4 opacity-90">
        <span>{{ site.announcement || "🚚 شحن مجاني للطلبات فوق 500 ج.م" }}</span>
        <span class="hidden sm:inline">📞 الدعم: 19999</span>
      </div>
      <div class="flex items-center gap-3">
        <button @click="toggleLang" class="hover:opacity-80">{{ locale === "ar" ? "English" : "العربية" }}</button>
        <span class="opacity-40">|</span>
        <template v-if="auth.isAuthenticated">
          <router-link v-if="auth.isAdmin" :to="{ name: 'admin' }" class="font-bold">لوحة الإدارة</router-link>
          <router-link v-else-if="auth.isVendor || auth.isStaff" :to="{ name: 'dashboard' }" class="font-bold">لوحة المتجر</router-link>
          <span class="opacity-40">|</span>
          <span class="opacity-90">{{ auth.user?.email }}</span>
          <button @click="logout" class="hover:opacity-80">خروج</button>
        </template>
        <template v-else>
          <router-link :to="{ name: 'login' }" class="hover:opacity-80">دخول</router-link>
          <span class="opacity-40">|</span>
          <router-link :to="{ name: 'vendor-register' }" class="font-bold">بيع معنا</router-link>
        </template>
      </div>
    </div>
  </div>
</template>
