<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import { useSiteStore } from "@/stores/site";
import { vendorApi } from "@/lib/api";

const router = useRouter();
const auth = useAuthStore();
const site = useSiteStore();

const form = ref({ full_name: "", email: "", password: "", store_name: "", city: "", tagline: "" });
const accepted = ref(false);
const error = ref("");
const loading = ref(false);

onMounted(() => { if (!site.loaded) site.load(); });

async function submit() {
  error.value = "";
  if (!accepted.value) { error.value = "يجب الموافقة على شروط المنصة."; return; }
  loading.value = true;
  try {
    await auth.register({
      full_name: form.value.full_name, email: form.value.email,
      password: form.value.password, role: "vendor",
    });
    await vendorApi.register({
      name: form.value.store_name, tagline: form.value.tagline,
      city: form.value.city, email: form.value.email, terms_accepted: true,
    });
    router.push({ name: "dashboard" });
  } catch (e) {
    const d = e.response?.data;
    error.value = d?.email?.[0] || d?.terms_accepted?.[0] || d?.detail || "تعذّر إرسال الطلب";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="container-x py-12 flex justify-center">
    <div class="card p-8 w-full max-w-lg space-y-5">
      <div class="text-center">
        <h1 class="text-2xl font-extrabold">قدّم طلب فتح متجر 🏪</h1>
        <p class="text-sm text-ink/60 mt-1">يُراجع الطلب من قبل الإدارة وتتواصل معك قبل التفعيل.</p>
      </div>
      <div v-if="error" class="bg-red-50 text-red-600 text-sm rounded-theme px-4 py-2">{{ error }}</div>

      <form @submit.prevent="submit" class="grid sm:grid-cols-2 gap-4">
        <div class="sm:col-span-2"><label class="text-sm font-semibold">اسم المتجر</label>
          <input v-model="form.store_name" required class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5" /></div>
        <div><label class="text-sm font-semibold">اسم صاحب المتجر</label>
          <input v-model="form.full_name" required class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5" /></div>
        <div><label class="text-sm font-semibold">المدينة</label>
          <input v-model="form.city" class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5" /></div>
        <div class="sm:col-span-2"><label class="text-sm font-semibold">شعار المتجر (وصف قصير)</label>
          <input v-model="form.tagline" class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5" /></div>
        <div><label class="text-sm font-semibold">البريد الإلكتروني</label>
          <input v-model="form.email" type="email" required class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5" /></div>
        <div><label class="text-sm font-semibold">كلمة السر</label>
          <input v-model="form.password" type="password" required minlength="8" class="w-full mt-1 rounded-theme border border-black/10 px-3 py-2.5" /></div>

        <!-- terms -->
        <div class="sm:col-span-2">
          <div class="text-sm font-semibold mb-1">شروط المنصة</div>
          <div class="max-h-32 overflow-y-auto text-xs text-ink/60 bg-black/[0.03] rounded-theme p-3 leading-relaxed">
            {{ site.vendor_terms || "بالتقديم فإنك توافق على سياسات المنصة بشأن المنتجات والأسعار والإرجاع والعمولة، وأن متجرك يخضع لمراجعة الإدارة قبل التفعيل." }}
          </div>
          <label class="flex items-center gap-2 text-sm mt-2">
            <input type="checkbox" v-model="accepted" /> أوافق على شروط وأحكام المنصة
          </label>
        </div>

        <button :disabled="loading" class="btn-primary w-full sm:col-span-2">{{ loading ? "..." : "إرسال الطلب للمراجعة" }}</button>
      </form>
    </div>
  </div>
</template>
