<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();

const form = ref({ full_name: "", email: "", password: "" });
const error = ref("");
const loading = ref(false);

async function submit() {
  error.value = "";
  loading.value = true;
  try {
    await auth.register({ ...form.value, role: "customer" });
    router.push({ name: "home" });
  } catch (e) {
    const d = e.response?.data;
    error.value = d?.email?.[0] || d?.password?.[0] || "تعذّر إنشاء الحساب";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="container-x py-12 flex justify-center">
    <div class="card p-8 w-full max-w-md space-y-5">
      <h1 class="text-2xl font-extrabold text-center">حساب جديد</h1>
      <div v-if="error" class="bg-red-50 text-red-600 text-sm rounded-theme px-4 py-2">{{ error }}</div>

      <form @submit.prevent="submit" class="space-y-4">
        <div>
          <label class="text-sm font-semibold">الاسم الكامل</label>
          <input v-model="form.full_name" required
                 class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5 outline-none focus:border-primary" />
        </div>
        <div>
          <label class="text-sm font-semibold">البريد الإلكتروني</label>
          <input v-model="form.email" type="email" required
                 class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5 outline-none focus:border-primary" />
        </div>
        <div>
          <label class="text-sm font-semibold">كلمة السر</label>
          <input v-model="form.password" type="password" required minlength="8"
                 class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5 outline-none focus:border-primary" />
        </div>
        <button :disabled="loading" class="btn-primary w-full">{{ loading ? "..." : "إنشاء الحساب" }}</button>
      </form>

      <div class="text-center text-sm text-ink/60">
        لديك حساب؟ <router-link :to="{ name: 'login' }" class="text-primary font-bold">دخول</router-link>
      </div>
      <div class="text-center text-sm border-t border-black/5 pt-3">
        تريد البيع؟ <router-link :to="{ name: 'vendor-register' }" class="text-primary font-bold">افتح متجرك</router-link>
      </div>
    </div>
  </div>
</template>
