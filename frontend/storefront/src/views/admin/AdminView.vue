<script setup>
import { ref, onMounted } from "vue";
import { adminApi, siteApi, vendorApi } from "@/lib/api";
import { useSiteStore } from "@/stores/site";
import DashboardShell from "@/components/dashboard/DashboardShell.vue";

const site = useSiteStore();
const tab = ref("overview");
const toast = ref("");

const stats = ref({});
const applications = ref([]);
const vendors = ref([]);
const settings = ref({ ...site.$state });

const nav = [
  { key: "overview", label: "نظرة عامة", icon: "📊" },
  { key: "applications", label: "طلبات المتاجر", icon: "📨" },
  { key: "vendors", label: "كل المتاجر", icon: "🏪" },
  { key: "appearance", label: "مظهر الموقع", icon: "🎨" },
];

function flash(m) { toast.value = m; setTimeout(() => (toast.value = ""), 2500); }

async function loadAll() {
  const [s, apps, v] = await Promise.all([
    adminApi.stats(),
    adminApi.applications("pending"),
    vendorApi.list({ ordering: "-created_at" }),
  ]);
  stats.value = s.data;
  applications.value = apps.data.results;
  vendors.value = v.data.results;
  settings.value = { ...site.$state };
}
onMounted(loadAll);

async function approve(v) {
  await adminApi.approve(v.id);
  applications.value = applications.value.filter((a) => a.id !== v.id);
  stats.value.vendors_pending--; stats.value.vendors_active++;
  flash(`تم تفعيل متجر "${v.name}" ✓`);
}
async function reject(v) {
  const reason = prompt("سبب الرفض (اختياري):") ?? "";
  await adminApi.reject(v.id, reason);
  applications.value = applications.value.filter((a) => a.id !== v.id);
  stats.value.vendors_pending--;
  flash(`تم رفض الطلب`);
}

async function saveSettings() {
  const { data } = await siteApi.update(settings.value);
  Object.assign(site.$state, data);
  site.applyGlobal();   // apply the new global theme everywhere immediately
  flash("تم حفظ إعدادات الموقع ✓");
}
</script>

<template>
  <DashboardShell title="لوحة الإدارة" subtitle="مدير المنصة" :nav="nav" :active="tab"
                  accent="#7c3aed" @select="tab = $event">
    <transition name="fade">
      <div v-if="toast" class="mb-4 bg-green-100 text-green-700 px-4 py-2 rounded-xl text-sm font-bold">{{ toast }}</div>
    </transition>

    <!-- OVERVIEW -->
    <div v-if="tab === 'overview'" class="space-y-6">
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="bg-white rounded-2xl p-5 border border-black/5">
          <div class="text-3xl font-extrabold">{{ stats.vendors_total ?? "—" }}</div>
          <div class="text-sm text-ink/50">إجمالي المتاجر</div>
        </div>
        <div class="bg-white rounded-2xl p-5 border border-black/5">
          <div class="text-3xl font-extrabold text-green-600">{{ stats.vendors_active ?? "—" }}</div>
          <div class="text-sm text-ink/50">متاجر نشطة</div>
        </div>
        <div class="bg-white rounded-2xl p-5 border border-black/5">
          <div class="text-3xl font-extrabold text-amber-500">{{ stats.vendors_pending ?? "—" }}</div>
          <div class="text-sm text-ink/50">بانتظار المراجعة</div>
        </div>
        <div class="bg-white rounded-2xl p-5 border border-black/5">
          <div class="text-3xl font-extrabold text-red-500">{{ stats.vendors_suspended ?? "—" }}</div>
          <div class="text-sm text-ink/50">موقوفة / مرفوضة</div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-5 border border-black/5">
        <h3 class="font-extrabold mb-3">أحدث الطلبات</h3>
        <div v-if="!applications.length" class="text-ink/40 text-sm">لا طلبات معلّقة.</div>
        <div v-for="a in applications.slice(0,5)" :key="a.id" class="flex items-center justify-between py-2 border-b border-black/5 last:border-0">
          <span class="font-semibold text-sm">{{ a.name }} <span class="text-xs text-ink/40">· {{ a.city }}</span></span>
          <button @click="tab = 'applications'" class="text-primary text-sm font-bold">مراجعة</button>
        </div>
      </div>
    </div>

    <!-- APPLICATIONS -->
    <div v-else-if="tab === 'applications'" class="space-y-4">
      <h2 class="text-lg font-extrabold">طلبات فتح المتاجر ({{ applications.length }})</h2>
      <p class="text-sm text-ink/50">راجع كل طلب وتواصل مع صاحبه، ثم وافق أو ارفض.</p>
      <div v-if="!applications.length" class="bg-white rounded-2xl p-8 text-center text-ink/40">لا طلبات معلّقة 🎉</div>
      <div v-for="a in applications" :key="a.id" class="bg-white rounded-2xl p-5 border border-black/5 flex items-center gap-4">
        <img :src="a.logo_url" class="w-14 h-14 rounded-xl object-cover bg-black/5" />
        <div class="flex-1">
          <div class="font-extrabold">{{ a.name }}</div>
          <div class="text-sm text-ink/50">{{ a.tagline }} · {{ a.city }}</div>
        </div>
        <div class="flex gap-2">
          <button @click="approve(a)" class="bg-green-600 text-white text-sm font-bold px-4 py-2 rounded-lg">موافقة</button>
          <button @click="reject(a)" class="bg-red-50 text-red-600 text-sm font-bold px-4 py-2 rounded-lg">رفض</button>
        </div>
      </div>
    </div>

    <!-- VENDORS -->
    <div v-else-if="tab === 'vendors'" class="space-y-3">
      <h2 class="text-lg font-extrabold">كل المتاجر</h2>
      <div class="bg-white rounded-2xl border border-black/5 divide-y divide-black/5">
        <div v-for="v in vendors" :key="v.id" class="flex items-center gap-3 p-4">
          <img :src="v.logo_url" class="w-10 h-10 rounded-lg object-cover bg-black/5" />
          <div class="flex-1">
            <div class="font-semibold text-sm">{{ v.name }}</div>
            <div class="text-xs text-ink/40">★ {{ v.rating_avg }} · {{ v.products_count }} منتج</div>
          </div>
          <span class="text-xs font-bold px-2 py-1 rounded-full"
                :class="{'bg-green-100 text-green-700': v.status==='active','bg-amber-100 text-amber-700': v.status==='pending','bg-red-100 text-red-700': v.status==='suspended'}">
            {{ v.status }}
          </span>
        </div>
      </div>
    </div>

    <!-- APPEARANCE (global theme — admin only) -->
    <div v-else-if="tab === 'appearance'" class="max-w-xl space-y-4">
      <h2 class="text-lg font-extrabold">مظهر الموقع العام</h2>
      <p class="text-sm text-ink/50">هذه الألوان تطبّق على واجهة الموقع كاملة — يتحكم بها المدير فقط.</p>
      <div class="bg-white rounded-2xl p-5 border border-black/5 space-y-4">
        <label class="flex items-center justify-between">اسم الموقع
          <input v-model="settings.site_name" class="border border-black/10 rounded-lg px-3 py-1.5 w-52" /></label>
        <label class="flex items-center justify-between">اللون الأساسي
          <input type="color" v-model="settings.primary_color" class="w-12 h-9" /></label>
        <label class="flex items-center justify-between">اللون الثانوي
          <input type="color" v-model="settings.secondary_color" class="w-12 h-9" /></label>
        <label class="flex items-center justify-between">اللون المميِّز
          <input type="color" v-model="settings.accent_color" class="w-12 h-9" /></label>
        <label class="flex items-center justify-between gap-3">الاستدارة
          <input type="range" min="0" max="28" v-model.number="settings.rounded" /></label>
        <div>
          <label class="text-sm font-semibold">شريط الإعلان</label>
          <input v-model="settings.announcement" class="w-full mt-1 border border-black/10 rounded-lg px-3 py-2" />
        </div>
        <div>
          <label class="text-sm font-semibold">شروط فتح المتجر</label>
          <textarea v-model="settings.vendor_terms" rows="4" class="w-full mt-1 border border-black/10 rounded-lg px-3 py-2"></textarea>
        </div>
        <button @click="saveSettings" class="btn-primary w-full">حفظ إعدادات الموقع</button>
      </div>
    </div>
  </DashboardShell>
</template>
