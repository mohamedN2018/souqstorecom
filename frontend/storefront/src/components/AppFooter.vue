<script setup>
import { useI18n } from "vue-i18n";
const { t } = useI18n();
</script>

<template>
  <footer class="mt-16 text-white" style="background: var(--c-secondary)">
    <div class="container-x py-10 grid gap-8 md:grid-cols-4">
      <div>
        <h3 class="font-extrabold text-xl mb-2">{{ t("brand") }}</h3>
        <p class="opacity-70 text-sm">منصة سوق إلكتروني متعددة البائعين — تسوّق بثقة.</p>
      </div>
      <div>
        <h4 class="font-bold mb-3">روابط</h4>
        <ul class="space-y-2 text-sm opacity-80">
          <li><router-link :to="{ name: 'products' }">{{ t("nav.products") }}</router-link></li>
          <li><router-link :to="{ name: 'vendors' }">{{ t("nav.vendors") }}</router-link></li>
        </ul>
      </div>
      <div>
        <h4 class="font-bold mb-3">الدفع</h4>
        <p class="text-sm opacity-80">Paymob · Fawry · InstaPay · Visa · COD</p>
      </div>
      <div>
        <h4 class="font-bold mb-3">تواصل</h4>
        <p class="text-sm opacity-80">support@souqstore.test</p>
      </div>
    </div>
    <div class="border-t border-white/10 py-4 text-center text-xs opacity-60">
      © 2026 SouqStore — جميع الحقوق محفوظة
    </div>
  </footer>
</template>
