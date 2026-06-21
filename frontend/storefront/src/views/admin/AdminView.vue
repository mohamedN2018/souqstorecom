<script setup>
import { ref, onMounted } from "vue";
import { adminApi, siteApi, vendorApi } from "@/lib/api";
import { useSiteStore } from "@/stores/site";
import DashboardShell from "@/components/dashboard/DashboardShell.vue";
import Icon from "@/components/Icon.vue";

const site = useSiteStore();
const tab = ref("overview");
const toast = ref("");

const stats = ref({});
const applications = ref([]);
const vendors = ref([]);
const settings = ref({ ...site.$state });

const nav = [
  { key: "overview", label: "نظرة عامة", icon: "chart" },
  { key: "applications", label: "طلبات المتاجر", icon: "inbox" },
  { key: "vendors", label: "كل المتاجر", icon: "store" },
  { key: "appearance", label: "مظهر الموقع", icon: "palette" },
];

const STAT_CARDS = [
  { key: "vendors_total", label: "إجمالي المتاجر", icon: "store", color: "#4f46e5" },
  { key: "vendors_active", label: "متاجر نشطة", icon: "check", color: "#16a34a" },
  { key: "vendors_pending", label: "بانتظار المراجعة", icon: "clock", color: "#d97706" },
  { key: "vendors_suspended", label: "موقوفة / مرفوضة", icon: "shield", color: "#e11d48" },
];

function flash(m) { toast.value = m; setTimeout(() => (toast.value = ""), 2500); }

// Resilient: one failing call never blanks the whole dashboard.
async function loadAll() {
  const [s, apps, v] = await Promise.allSettled([
    adminApi.stats(),
    adminApi.applications("pending"),
    vendorApi.list({ ordering: "-created_at" }),
  ]);
  if (s.status === "fulfilled") stats.value = s.value.data;
  if (apps.status === "fulfilled") applications.value = apps.value.data.results || apps.value.data;
  if (v.status === "fulfilled") vendors.value = v.value.data.results || v.value.data;
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
        <div v-for="c in STAT_CARDS" :key="c.key"
             class="bg-white rounded-2xl p-5 border border-black/5 shadow-sm flex items-center gap-4">
          <span class="grid place-items-center w-12 h-12 rounded-xl shrink-0"
                :style="{ background: `color-mix(in srgb, ${c.color} 12%, transparent)`, color: c.color }">
            <Icon :name="c.icon" class="w-6 h-6" />
          </span>
          <div class="min-w-0">
            <div class="text-2xl font-extrabold" :style="{ color: c.color }">{{ stats[c.key] ?? "—" }}</div>
            <div class="text-xs text-ink/50">{{ c.label }}</div>
          </div>
        </div>
      </div>
      <div class="bg-white rounded-2xl p-5 border border-black/5 shadow-sm">
        <h3 class="font-extrabold mb-3 flex items-center gap-2"><Icon name="inbox" class="w-5 h-5 text-primary" /> أحدث الطلبات</h3>
        <div v-if="!applications.length" class="text-ink/40 text-sm py-4 text-center">لا طلبات معلّقة حالياً.</div>
        <div v-for="a in applications.slice(0,5)" :key="a.id" class="flex items-center justify-between py-2.5 border-b border-black/5 last:border-0">
          <span class="font-semibold text-sm">{{ a.name }} <span class="text-xs text-ink/40">· {{ a.city }}</span></span>
          <button @click="tab = 'applications'" class="btn-ghost text-sm py-1.5">مراجعة</button>
        </div>
      </div>
    </div>

    <!-- APPLICATIONS -->
    <div v-else-if="tab === 'applications'" class="space-y-4">
      <h2 class="text-lg font-extrabold">طلبات فتح المتاجر ({{ applications.length }})</h2>
      <p class="text-sm text-ink/50">راجع كل طلب وتواصل مع صاحبه، ثم وافق أو ارفض.</p>
      <div v-if="!applications.length" class="bg-white rounded-2xl p-10 text-center text-ink/40 shadow-sm">
        <Icon name="check" class="w-10 h-10 mx-auto mb-2 text-green-500" />
        لا طلبات معلّقة حالياً.
      </div>
      <div v-for="a in applications" :key="a.id" class="bg-white rounded-2xl p-5 border border-black/5 shadow-sm flex flex-col sm:flex-row sm:items-center gap-4">
        <img :src="a.logo_url" class="w-14 h-14 rounded-xl object-cover bg-black/5 shrink-0" />
        <div class="flex-1 min-w-0">
          <div class="font-extrabold">{{ a.name }}</div>
          <div class="text-sm text-ink/50">{{ a.tagline }} · {{ a.city }}</div>
        </div>
        <div class="flex gap-2 shrink-0">
          <button @click="approve(a)" class="flex items-center gap-1.5 bg-green-600 hover:bg-green-700 text-white text-sm font-bold px-4 py-2 rounded-xl transition"><Icon name="check" class="w-4 h-4" /> موافقة</button>
          <button @click="reject(a)" class="flex items-center gap-1.5 bg-red-50 hover:bg-red-100 text-red-600 text-sm font-bold px-4 py-2 rounded-xl transition"><Icon name="x" class="w-4 h-4" /> رفض</button>
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
