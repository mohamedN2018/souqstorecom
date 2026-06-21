<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { gsap } from "gsap";
import Icon from "@/components/Icon.vue";

// Offline promo slides (gradients + text, no external images).
const slides = [
  { title: "تخفيضات الصيف الكبرى", sub: "خصومات تصل إلى 70% على آلاف المنتجات", cta: "تسوّق العروض", g: ["#2563eb", "#7c3aed"] },
  { title: "إلكترونيات بأفضل الأسعار", sub: "أحدث الموبايلات واللابتوبات مع ضمان", cta: "اكتشف الآن", g: ["#0891b2", "#0f766e"] },
  { title: "أزياء الموسم الجديد", sub: "تشكيلة حصرية من أرقى الماركات", cta: "تصفّح المجموعة", g: ["#db2777", "#9333ea"] },
  { title: "كل يوم عرض جديد", sub: "عروض فلاش لفترة محدودة — لا تفوّتها", cta: "عروض اليوم", g: ["#ea580c", "#dc2626"] },
];

const idx = ref(0);
let timer;

function go(i) {
  idx.value = (i + slides.length) % slides.length;
  gsap.fromTo(".promo-content", { opacity: 0, x: 30 }, { opacity: 1, x: 0, duration: 0.5, ease: "power2.out" });
}
function start() {
  timer = setInterval(() => go(idx.value + 1), 4500);
}
onMounted(start);
onBeforeUnmount(() => clearInterval(timer));
</script>

<template>
  <div class="relative overflow-hidden rounded-theme shadow-lg">
    <div class="h-60 md:h-[22rem] flex items-center text-white relative"
         :style="{ background: `linear-gradient(120deg, ${slides[idx].g[0]}, ${slides[idx].g[1]})` }">
      <div class="promo-content container-x relative z-10">
        <span class="pill bg-white/20 backdrop-blur mb-4">عرض حصري</span>
        <h2 class="text-3xl md:text-5xl font-extrabold max-w-lg leading-tight">{{ slides[idx].title }}</h2>
        <p class="mt-3 text-base md:text-lg opacity-90 max-w-md">{{ slides[idx].sub }}</p>
        <router-link :to="{ name: 'products' }"
                     class="inline-flex items-center gap-2 mt-6 bg-white font-bold px-7 py-3 rounded-2xl shadow-lg hover:-translate-y-1 transition"
                     :style="{ color: slides[idx].g[0] }">
          {{ slides[idx].cta }} <Icon name="arrow-left" class="w-5 h-5" />
        </router-link>
      </div>
      <!-- decorative blobs -->
      <div class="absolute -bottom-20 -left-16 w-72 h-72 rounded-full bg-white/10"></div>
      <div class="absolute -top-16 -right-10 w-52 h-52 rounded-full bg-white/10"></div>
    </div>

    <!-- arrows -->
    <button @click="go(idx - 1)" aria-label="السابق"
            class="absolute top-1/2 -translate-y-1/2 right-3 grid place-items-center w-11 h-11 rounded-full bg-white/20 hover:bg-white/35 backdrop-blur text-white transition">
      <Icon name="chevron-right" />
    </button>
    <button @click="go(idx + 1)" aria-label="التالي"
            class="absolute top-1/2 -translate-y-1/2 left-3 grid place-items-center w-11 h-11 rounded-full bg-white/20 hover:bg-white/35 backdrop-blur text-white transition">
      <Icon name="chevron-left" />
    </button>

    <!-- dots -->
    <div class="absolute bottom-3 left-1/2 -translate-x-1/2 flex gap-2">
      <button v-for="(s, i) in slides" :key="i" @click="go(i)"
              class="w-2.5 h-2.5 rounded-full transition"
              :class="i === idx ? 'bg-white w-6' : 'bg-white/50'" />
    </div>
  </div>
</template>
