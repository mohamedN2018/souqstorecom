<script setup>
import { ref } from "vue";
import { useRouter, useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const route = useRoute();
const auth = useAuthStore();

const email = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    const user = await auth.login(email.value, password.value);
    const next = route.query.next;
    const home =
      user.role === "admin" ? { name: "admin" }
      : user.role === "vendor" || user.role === "staff" ? { name: "dashboard" }
      : { name: "home" };
    router.push(next || home);
  } catch (e) {
    error.value = e.response?.data?.detail || "بيانات الدخول غير صحيحة";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="container-x py-12 flex justify-center">
    <div class="card p-8 w-full max-w-md space-y-5">
      <h1 class="text-2xl font-extrabold text-center">تسجيل الدخول</h1>

      <div v-if="error" class="bg-red-50 text-red-600 text-sm rounded-theme px-4 py-2">{{ error }}</div>

      <form @submit.prevent="submit" class="space-y-4">
        <div>
          <label class="text-sm font-semibold">البريد الإلكتروني</label>
          <input v-model="email" type="email" required
                 class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5 outline-none focus:border-primary" />
        </div>
        <div>
          <label class="text-sm font-semibold">كلمة السر</label>
          <input v-model="password" type="password" required
                 class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5 outline-none focus:border-primary" />
        </div>
        <button :disabled="loading" class="btn-primary w-full">
          {{ loading ? "..." : "دخول" }}
        </button>
      </form>

      <div class="text-center text-sm text-ink/60">
        ليس لديك حساب؟
        <router-link :to="{ name: 'register' }" class="text-primary font-bold">سجّل الآن</router-link>
      </div>
      <div class="text-center text-xs text-ink/40 border-t border-black/5 pt-3">
        تجريبي: customer1@souq.test / vendor1@souq.test — كلمة السر: Password123
      </div>
    </div>
  </div>
</template>
