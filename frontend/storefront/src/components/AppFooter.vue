<script setup>
import { useI18n } from "vue-i18n";
import Icon from "@/components/Icon.vue";
const { t } = useI18n();

const features = [
  { icon: "truck", text: "شحن لكل المحافظات" },
  { icon: "shield", text: "دفع آمن 100%" },
  { icon: "package", text: "إرجاع مجاني" },
  { icon: "phone", text: "دعم 24/7" },
];
</script>

<template>
  <footer class="mt-20 text-white" style="background: var(--c-secondary)">
    <!-- feature strip -->
    <div class="border-b border-white/10">
      <div class="container-x py-6 grid grid-cols-2 md:grid-cols-4 gap-4">
        <div v-for="f in features" :key="f.text" class="flex items-center gap-3">
          <span class="grid place-items-center w-10 h-10 rounded-xl bg-white/10 shrink-0">
            <Icon :name="f.icon" class="w-5 h-5" />
          </span>
          <span class="text-sm font-semibold">{{ f.text }}</span>
        </div>
      </div>
    </div>

    <div class="container-x py-12 grid gap-8 md:grid-cols-4">
      <div class="md:col-span-1">
        <div class="flex items-center gap-2.5 mb-3">
          <span class="grid place-items-center w-10 h-10 rounded-2xl text-white font-extrabold text-lg"
                style="background: linear-gradient(135deg, var(--c-primary), var(--c-accent))">س</span>
          <h3 class="font-extrabold text-xl">{{ t("brand") }}</h3>
        </div>
        <p class="opacity-70 text-sm leading-relaxed">منصة سوق إلكتروني متعددة البائعين — تسوّق بثقة من آلاف المنتجات وأفضل المتاجر.</p>
      </div>
      <div>
        <h4 class="font-bold mb-3">روابط سريعة</h4>
        <ul class="space-y-2.5 text-sm opacity-75">
          <li><router-link :to="{ name: 'products' }" class="hover:opacity-100 hover:text-primary transition">{{ t("nav.products") }}</router-link></li>
          <li><router-link :to="{ name: 'vendors' }" class="hover:opacity-100 hover:text-primary transition">{{ t("nav.vendors") }}</router-link></li>
          <li><router-link :to="{ name: 'vendor-register' }" class="hover:opacity-100 hover:text-primary transition">انضم كبائع</router-link></li>
        </ul>
      </div>
      <div>
        <h4 class="font-bold mb-3">طرق الدفع</h4>
        <div class="flex flex-wrap gap-2">
          <span v-for="p in ['Paymob','Fawry','InstaPay','Visa','COD']" :key="p"
                class="pill bg-white/10 text-xs">{{ p }}</span>
        </div>
      </div>
      <div>
        <h4 class="font-bold mb-3">النشرة البريدية</h4>
        <p class="text-sm opacity-75 mb-3">اشترك ليصلك كل جديد وأقوى العروض.</p>
        <form @submit.prevent class="flex bg-white/10 rounded-xl overflow-hidden ring-1 ring-white/10">
          <input placeholder="بريدك الإلكتروني" class="bg-transparent px-3 py-2.5 text-sm outline-none w-full placeholder:text-white/40" />
          <button class="px-4 text-white font-bold" style="background: var(--c-primary)">
            <Icon name="arrow-left" class="w-5 h-5" />
          </button>
        </form>
      </div>
    </div>
    <div class="border-t border-white/10 py-4 text-center text-xs opacity-60">
      © 2026 {{ t("brand") }} — جميع الحقوق محفوظة
    </div>
  </footer>
</template>
