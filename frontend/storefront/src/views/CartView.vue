<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import { useCartStore } from "@/stores/cart";
import { useAuthStore } from "@/stores/auth";
import { catalogApi } from "@/lib/api";

const { t } = useI18n();
const router = useRouter();
const cart = useCartStore();
const auth = useAuthStore();

const placing = ref(false);
const done = ref(false);

async function checkout() {
  if (!auth.isAuthenticated) {
    router.push({ name: "login", query: { next: "/cart" } });
    return;
  }
  placing.value = true;
  try {
    // Records a purchase per item → unlocks verified reviews. (Order service stand-in.)
    await catalogApi.checkout(cart.items.map((i) => ({ product_id: i.id, qty: i.qty })));
    cart.clear();
    done.value = true;
  } finally {
    placing.value = false;
  }
}
</script>

<template>
  <div class="container-x py-8">
    <h1 class="text-2xl font-extrabold mb-6">{{ t("nav.cart") }}</h1>

    <div v-if="done" class="card p-10 text-center space-y-3">
      <div class="text-4xl">✅</div>
      <h2 class="text-xl font-extrabold">تم تأكيد طلبك!</h2>
      <p class="text-ink/60">يمكنك الآن تقييم المنتجات التي اشتريتها من صفحة كل منتج.</p>
      <router-link :to="{ name: 'products' }" class="btn-primary inline-block">متابعة التسوق</router-link>
    </div>

    <div v-else-if="!cart.items.length" class="text-center py-20 text-ink/50">
      السلة فارغة 🛒
      <div class="mt-4"><router-link :to="{ name: 'products' }" class="btn-primary inline-block">{{ t("home.shop_now") }}</router-link></div>
    </div>

    <div v-else class="grid lg:grid-cols-[1fr_320px] gap-6">
      <div class="space-y-3">
        <div v-for="it in cart.items" :key="it.id" class="card p-3 flex items-center gap-3">
          <img :src="it.image" class="w-20 h-20 object-cover rounded-theme" />
          <div class="flex-1">
            <div class="font-semibold text-sm">{{ it.name }}</div>
            <div class="text-primary font-bold">{{ Number(it.price).toLocaleString() }} {{ t("common.currency") }}</div>
          </div>
          <div class="flex items-center gap-2">
            <button @click="cart.setQty(it.id, it.qty - 1)" class="w-8 h-8 card">−</button>
            <span class="w-8 text-center font-bold">{{ it.qty }}</span>
            <button @click="cart.setQty(it.id, it.qty + 1)" class="w-8 h-8 card">＋</button>
          </div>
          <button @click="cart.remove(it.id)" class="text-red-500 px-2">✕</button>
        </div>
      </div>

      <aside class="card p-5 h-fit space-y-4 lg:sticky lg:top-32">
        <h3 class="font-extrabold">ملخص الطلب</h3>
        <div class="flex justify-between"><span>الإجمالي</span>
          <span class="font-extrabold text-primary">{{ cart.total.toLocaleString() }} {{ t("common.currency") }}</span>
        </div>
        <button :disabled="placing" @click="checkout" class="btn-primary w-full">
          {{ placing ? "..." : "إتمام الشراء" }}
        </button>
        <button @click="cart.clear()" class="w-full text-sm py-2 rounded-theme border border-black/10">تفريغ السلة</button>
      </aside>
    </div>
  </div>
</template>
