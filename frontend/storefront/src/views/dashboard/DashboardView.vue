<script setup>
import { ref, onMounted, computed } from "vue";
import { catalogApi, vendorApi, staffApi } from "@/lib/api";
import { useAuthStore } from "@/stores/auth";
import { useCatalogStore } from "@/stores/catalog";
import { useThemeStore } from "@/stores/theme";
import { useProductFeed } from "@/composables/useProductFeed";
import DashboardShell from "@/components/dashboard/DashboardShell.vue";
import Icon from "@/components/Icon.vue";

const STAT_CARDS = [
  { key: "total", label: "المنتجات", icon: "package", color: "#4f46e5" },
  { key: "active", label: "نشطة", icon: "check", color: "#16a34a" },
  { key: "featured", label: "مميزة", icon: "sparkles", color: "#d97706" },
  { key: "sold", label: "إجمالي المبيعات", icon: "chart", color: "#e11d48" },
];

const auth = useAuthStore();
const catalog = useCatalogStore();
const theme = useThemeStore();

const tab = ref("overview");
const loading = ref(true);
const toast = ref("");
const store = ref(null);
const products = ref([]);
const isOwner = computed(() => auth.role === "vendor");

const nav = computed(() => {
  const items = [];
  if (isOwner.value || auth.can("view_analytics")) items.push({ key: "overview", label: "نظرة عامة", icon: "chart" });
  if (isOwner.value || auth.can("manage_products")) items.push({ key: "products", label: "المنتجات", icon: "package" });
  if (isOwner.value || auth.can("manage_products")) items.push({ key: "form", label: "إضافة منتج", icon: "plus" });
  if (isOwner.value) items.push({ key: "profile", label: "بيانات المتجر", icon: "store" });
  if (isOwner.value) items.push({ key: "appearance", label: "ألوان المتجر", icon: "palette" });
  if (isOwner.value) items.push({ key: "staff", label: "الموظفون", icon: "user" });
  return items;
});

const stats = computed(() => ({
  total: products.value.length,
  active: products.value.filter((p) => p.status === "active").length,
  featured: products.value.filter((p) => p.is_featured).length,
  sold: products.value.reduce((n, p) => n + (p.sold_count || 0), 0),
}));

function flash(m) { toast.value = m; setTimeout(() => (toast.value = ""), 2500); }

async function loadProducts() {
  const { data } = await catalogApi.myProducts();
  products.value = data.results || data;
}

onMounted(async () => {
  await catalog.loadCategories();
  if (isOwner.value) {
    try { store.value = (await vendorApi.myStore()).data; } catch { store.value = null; }
  }
  try { await loadProducts(); } catch { products.value = []; }
  loading.value = false;
});

// ---------- product form (add + edit) ----------
const blank = { id: null, name: "", category_id: "", price: "", compare_at_price: "", brand: "", short_description: "", is_featured: false };
const form = ref({ ...blank });
const editing = computed(() => !!form.value.id);
const saving = ref(false);
const subCategories = computed(() => catalog.categories.filter((c) => c.parent));

function newProduct() { form.value = { ...blank }; tab.value = "form"; }
function editProduct(p) {
  form.value = {
    id: p.id, name: p.name, category_id: "", price: p.price,
    compare_at_price: p.compare_at_price || "", brand: p.brand || "",
    short_description: p.short_description || "", is_featured: p.is_featured,
  };
  tab.value = "form";
}

async function saveProduct() {
  saving.value = true;
  try {
    const payload = { ...form.value, compare_at_price: form.value.compare_at_price || null };
    if (!payload.category_id) delete payload.category_id; // keep existing on edit
    if (editing.value) {
      await catalogApi.updateProduct(form.value.id, payload);
      flash("تم تحديث المنتج ✓");
    } else {
      await catalogApi.createProduct(payload);
      flash("تمت إضافة المنتج ✓ (ظهر مباشرة في المتجر)");
    }
    await loadProducts();
    form.value = { ...blank };
    tab.value = "products";
  } catch (e) {
    flash(e.response?.data?.name?.[0] || e.response?.data?.category_id?.[0] || "تعذّر الحفظ");
  } finally {
    saving.value = false;
  }
}

async function removeProduct(id) {
  await catalogApi.deleteProduct(id);
  products.value = products.value.filter((p) => p.id !== id);
  flash("تم حذف المنتج");
}

// ---------- profile ----------
const profile = ref({});
function syncProfile() { profile.value = { ...store.value }; }
async function saveProfile() {
  const { data } = await vendorApi.updateStore({
    name: profile.value.name, tagline: profile.value.tagline,
    city: profile.value.city, phone: profile.value.phone,
    description: profile.value.description,
  });
  store.value = data;
  flash("تم حفظ بيانات المتجر ✓");
}

// ---------- own theme ----------
const themeForm = ref({ primary_color: "#2563eb", accent_color: "#f59e0b", secondary_color: "#1e293b", rounded: 14 });
function syncTheme() { if (store.value?.theme) themeForm.value = { ...themeForm.value, ...store.value.theme }; }
function previewTheme() {
  theme.set("primary", themeForm.value.primary_color);
  theme.set("accent", themeForm.value.accent_color);
  theme.set("secondary", themeForm.value.secondary_color);
  theme.set("radius", Number(themeForm.value.rounded));
}
async function saveTheme() {
  const { data } = await vendorApi.updateTheme(themeForm.value);
  store.value = data; previewTheme();
  flash("تم حفظ ألوان متجرك ✓");
}

// ---------- staff ----------
const staff = ref([]);
const staffForm = ref({ full_name: "", email: "", password: "", permissions: [] });
const PERMS = [
  { key: "manage_products", label: "إدارة المنتجات" },
  { key: "view_orders", label: "عرض الطلبات" },
  { key: "manage_theme", label: "تعديل المظهر" },
  { key: "view_analytics", label: "عرض الإحصائيات" },
];
async function loadStaff() { const { data } = await staffApi.list(); staff.value = data.results || data; }
async function addStaff() {
  try {
    await staffApi.create(staffForm.value);
    staffForm.value = { full_name: "", email: "", password: "", permissions: [] };
    await loadStaff();
    flash("تمت إضافة الموظف ✓");
  } catch (e) { flash(e.response?.data?.email?.[0] || "تعذّر إضافة الموظف"); }
}
async function removeStaff(id) { await staffApi.remove(id); staff.value = staff.value.filter((s) => s.id !== id); }

function onSelect(key) {
  tab.value = key;
  if (key === "profile") syncProfile();
  if (key === "appearance") syncTheme();
  if (key === "staff") loadStaff();
  if (key === "form" && !editing.value) form.value = { ...blank };
}

// real-time
useProductFeed((ev) => {
  const vid = auth.user?.vendor_id || auth.user?.id;
  if (ev.product?.vendor_id && ev.product.vendor_id !== vid) return;
  if (ev.event === "product.created" && !products.value.find((p) => p.id === ev.product.id)) products.value.unshift(ev.product);
  else if (ev.event === "product.deleted") products.value = products.value.filter((p) => p.id !== ev.product.id);
});
</script>

<template>
  <DashboardShell :title="store?.name || 'لوحة المتجر'"
                  :subtitle="isOwner ? 'صاحب المتجر' : 'موظف'"
                  :nav="nav" :active="tab" @select="onSelect">
    <transition name="fade">
      <div v-if="toast" class="mb-4 bg-green-100 text-green-700 px-4 py-2 rounded-xl text-sm font-bold">{{ toast }}</div>
    </transition>

    <div v-if="loading" class="text-center py-20 text-ink/40">جاري التحميل...</div>

    <!-- pending approval banner -->
    <div v-else-if="isOwner && store && store.status === 'pending'" class="bg-amber-50 border border-amber-200 rounded-2xl p-6 mb-4">
      <h3 class="font-extrabold text-amber-700">⏳ متجرك قيد المراجعة</h3>
      <p class="text-sm text-amber-700/80 mt-1">سيتواصل معك فريق الإدارة قريباً. بعد الموافقة سيظهر متجرك ومنتجاتك في الموقع.</p>
    </div>

    <!-- no store -->
    <div v-else-if="isOwner && !store" class="bg-white rounded-2xl p-8 text-center">
      لا يوجد متجر مرتبط بحسابك.
      <router-link :to="{ name: 'vendor-register' }" class="text-primary font-bold">قدّم طلب فتح متجر</router-link>
    </div>

    <template v-else>
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
              <div class="text-2xl font-extrabold" :style="{ color: c.color }">
                {{ c.key === 'sold' ? stats.sold.toLocaleString() : stats[c.key] }}
              </div>
              <div class="text-xs text-ink/50">{{ c.label }}</div>
            </div>
          </div>
        </div>
        <div class="rounded-2xl p-6 flex flex-col sm:flex-row sm:items-center justify-between gap-4 text-white shadow-lg"
             style="background: linear-gradient(135deg, var(--c-primary), var(--c-accent));">
          <div>
            <h3 class="font-extrabold text-lg">أضف منتجاً جديداً</h3>
            <p class="text-sm opacity-90">يظهر فوراً في متجرك ولكل العملاء — مباشر بدون تحديث.</p>
          </div>
          <button @click="newProduct" class="bg-white text-ink font-bold px-5 py-2.5 rounded-xl flex items-center gap-2 hover:-translate-y-0.5 transition shrink-0">
            <Icon name="plus" class="w-5 h-5" /> منتج جديد
          </button>
        </div>
      </div>

      <!-- PRODUCTS -->
      <div v-else-if="tab === 'products'">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-extrabold flex items-center gap-2">منتجاتي ({{ products.length }})
            <span class="pill bg-green-100 text-green-600 text-[11px]"><span class="inline-block w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> مباشر</span>
          </h2>
          <button @click="newProduct" class="btn-primary text-sm"><Icon name="plus" class="w-4 h-4" /> إضافة</button>
        </div>
        <div v-if="!products.length" class="bg-white rounded-2xl p-8 text-center text-ink/50">لا منتجات بعد.</div>
        <div v-else class="grid sm:grid-cols-2 xl:grid-cols-3 gap-4">
          <div v-for="p in products" :key="p.id" class="bg-white rounded-2xl border border-black/5 overflow-hidden group">
            <div class="relative">
              <img :src="p.primary_image" class="w-full h-36 object-cover" />
              <span class="absolute top-2 right-2 text-[10px] font-bold px-2 py-1 rounded-full"
                    :class="p.status==='active' ? 'bg-green-100 text-green-700' : 'bg-amber-100 text-amber-700'">{{ p.status }}</span>
            </div>
            <div class="p-3">
              <div class="font-semibold text-sm line-clamp-1">{{ p.name }}</div>
              <div class="text-primary font-extrabold mt-1">{{ Number(p.price).toLocaleString() }} ج.م</div>
              <div class="flex gap-2 mt-3">
                <button @click="editProduct(p)" class="flex-1 flex items-center justify-center gap-1.5 bg-black/5 hover:bg-primary/10 hover:text-primary text-sm font-bold py-2 rounded-lg transition"><Icon name="edit" class="w-4 h-4" /> تعديل</button>
                <button @click="removeProduct(p.id)" class="grid place-items-center bg-red-50 text-red-600 hover:bg-red-100 py-2 px-3 rounded-lg transition" aria-label="حذف"><Icon name="trash" class="w-4 h-4" /></button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ADD / EDIT FORM + LIVE SIDE PANEL -->
      <div v-else-if="tab === 'form'" class="grid lg:grid-cols-[1fr_320px] gap-5 items-start">
        <div>
        <h2 class="text-lg font-extrabold mb-4">{{ editing ? "تعديل منتج" : "إضافة منتج جديد" }}</h2>
        <form @submit.prevent="saveProduct" class="bg-white rounded-2xl p-5 border border-black/5 grid sm:grid-cols-2 gap-4">
          <div class="sm:col-span-2"><label class="text-sm font-semibold">اسم المنتج</label>
            <input v-model="form.name" required class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2.5" /></div>
          <div><label class="text-sm font-semibold">الفئة {{ editing ? "(اتركها كما هي)" : "" }}</label>
            <select v-model="form.category_id" :required="!editing" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2.5 bg-white">
              <option value="">— اختر —</option>
              <option v-for="c in subCategories" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select></div>
          <div><label class="text-sm font-semibold">الماركة</label>
            <input v-model="form.brand" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2.5" /></div>
          <div><label class="text-sm font-semibold">السعر (ج.م)</label>
            <input v-model="form.price" type="number" required min="1" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2.5" /></div>
          <div><label class="text-sm font-semibold">السعر قبل الخصم</label>
            <input v-model="form.compare_at_price" type="number" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2.5" /></div>
          <div class="sm:col-span-2"><label class="text-sm font-semibold">وصف قصير</label>
            <input v-model="form.short_description" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2.5" /></div>
          <label class="sm:col-span-2 flex items-center gap-2 text-sm"><input v-model="form.is_featured" type="checkbox" /> منتج مميز</label>
          <button :disabled="saving" class="btn-primary sm:col-span-2">{{ saving ? "..." : (editing ? "حفظ التعديلات" : "إضافة المنتج") }}</button>
        </form>
        </div>

        <!-- LIVE side panel: products you added appear here instantly -->
        <aside class="bg-white rounded-2xl border border-black/5 lg:sticky lg:top-5 overflow-hidden">
          <div class="px-4 py-3 border-b border-black/5 flex items-center justify-between">
            <span class="font-extrabold text-sm">منتجاتك ({{ products.length }})</span>
            <span class="text-[11px] text-green-600 flex items-center gap-1">
              <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> مباشر
            </span>
          </div>
          <div class="max-h-[70vh] overflow-y-auto p-2">
            <div v-if="!products.length" class="text-center text-ink/40 text-sm py-8">أضف أول منتج ليظهر هنا فوراً.</div>
            <transition-group name="slidein" tag="div" class="space-y-2">
              <div v-for="p in products.slice(0, 30)" :key="p.id"
                   class="flex items-center gap-2 p-2 rounded-xl hover:bg-black/[0.03]">
                <img :src="p.primary_image" class="w-11 h-11 rounded-lg object-cover bg-black/5 shrink-0" />
                <div class="min-w-0 flex-1">
                  <div class="text-xs font-semibold line-clamp-1">{{ p.name }}</div>
                  <div class="text-primary font-bold text-xs">{{ Number(p.price).toLocaleString() }} ج.م</div>
                </div>
                <button @click="editProduct(p)" class="grid place-items-center w-7 h-7 rounded-lg text-ink/40 hover:text-primary hover:bg-primary/10" aria-label="تعديل"><Icon name="edit" class="w-4 h-4" /></button>
              </div>
            </transition-group>
          </div>
        </aside>
      </div>

      <!-- PROFILE -->
      <div v-else-if="tab === 'profile'" class="max-w-xl">
        <h2 class="text-lg font-extrabold mb-4">بيانات المتجر</h2>
        <div class="bg-white rounded-2xl p-5 border border-black/5 space-y-4">
          <div class="flex items-center gap-4">
            <img :src="store.logo_url" class="w-16 h-16 rounded-2xl object-cover bg-black/5" />
            <div><div class="font-extrabold">{{ store.name }}</div>
              <span class="text-xs font-bold px-2 py-0.5 rounded-full"
                    :class="store.status==='active' ? 'bg-green-100 text-green-700':'bg-amber-100 text-amber-700'">{{ store.status }}</span></div>
          </div>
          <div><label class="text-sm font-semibold">اسم المتجر</label><input v-model="profile.name" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2" /></div>
          <div><label class="text-sm font-semibold">الشعار</label><input v-model="profile.tagline" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2" /></div>
          <div class="grid grid-cols-2 gap-3">
            <div><label class="text-sm font-semibold">المدينة</label><input v-model="profile.city" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2" /></div>
            <div><label class="text-sm font-semibold">الهاتف</label><input v-model="profile.phone" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2" /></div>
          </div>
          <div><label class="text-sm font-semibold">وصف المتجر</label><textarea v-model="profile.description" rows="3" class="w-full mt-1 rounded-lg border border-black/10 px-3 py-2"></textarea></div>
          <button @click="saveProfile" class="btn-primary w-full">حفظ البيانات</button>
        </div>
      </div>

      <!-- APPEARANCE -->
      <div v-else-if="tab === 'appearance'" class="max-w-xl">
        <h2 class="text-lg font-extrabold mb-1">ألوان واجهة متجرك</h2>
        <p class="text-sm text-ink/50 mb-4">تتحكم في ألوان صفحة متجرك فقط — المعاينة فورية.</p>
        <div class="bg-white rounded-2xl p-5 border border-black/5 grid sm:grid-cols-2 gap-5">
          <label class="flex items-center justify-between">الأساسي <input type="color" v-model="themeForm.primary_color" @input="previewTheme" class="w-12 h-9" /></label>
          <label class="flex items-center justify-between">المميِّز <input type="color" v-model="themeForm.accent_color" @input="previewTheme" class="w-12 h-9" /></label>
          <label class="flex items-center justify-between">الثانوي <input type="color" v-model="themeForm.secondary_color" @input="previewTheme" class="w-12 h-9" /></label>
          <label class="flex items-center justify-between gap-2">الاستدارة <input type="range" min="0" max="28" v-model="themeForm.rounded" @input="previewTheme" /></label>
          <button @click="saveTheme" class="btn-primary sm:col-span-2">حفظ ألوان المتجر</button>
        </div>
      </div>

      <!-- STAFF -->
      <div v-else-if="tab === 'staff'" class="max-w-2xl space-y-5">
        <h2 class="text-lg font-extrabold">موظفو المتجر</h2>
        <div class="bg-white rounded-2xl p-5 border border-black/5">
          <h3 class="font-bold mb-3">إضافة موظف</h3>
          <form @submit.prevent="addStaff" class="grid sm:grid-cols-2 gap-3">
            <input v-model="staffForm.full_name" placeholder="الاسم" required class="rounded-lg border border-black/10 px-3 py-2" />
            <input v-model="staffForm.email" type="email" placeholder="البريد" required class="rounded-lg border border-black/10 px-3 py-2" />
            <input v-model="staffForm.password" type="password" placeholder="كلمة السر" required minlength="8" class="rounded-lg border border-black/10 px-3 py-2 sm:col-span-2" />
            <div class="sm:col-span-2">
              <div class="text-sm font-semibold mb-2">الصلاحيات</div>
              <div class="flex flex-wrap gap-3">
                <label v-for="p in PERMS" :key="p.key" class="flex items-center gap-1.5 text-sm">
                  <input type="checkbox" :value="p.key" v-model="staffForm.permissions" /> {{ p.label }}
                </label>
              </div>
            </div>
            <button class="btn-primary sm:col-span-2">إضافة الموظف</button>
          </form>
        </div>
        <div class="bg-white rounded-2xl border border-black/5 divide-y divide-black/5">
          <div v-if="!staff.length" class="p-6 text-center text-ink/40">لا موظفين بعد.</div>
          <div v-for="s in staff" :key="s.id" class="flex items-center gap-3 p-4">
            <span class="w-10 h-10 rounded-full bg-primary/10 text-primary grid place-items-center font-bold">{{ (s.email||'?')[0].toUpperCase() }}</span>
            <div class="flex-1"><div class="font-semibold text-sm">{{ s.full_name || s.email }}</div>
              <div class="text-xs text-ink/40">{{ (s.permissions||[]).join("، ") || "بدون صلاحيات" }}</div></div>
            <button @click="removeStaff(s.id)" class="text-red-500 text-sm">إزالة</button>
          </div>
        </div>
      </div>
    </template>
  </DashboardShell>
</template>

<style scoped>
/* New product slides in at the top of the live side panel */
.slidein-enter-active { transition: all 0.45s cubic-bezier(0.4, 0, 0.2, 1); }
.slidein-enter-from { opacity: 0; transform: translateY(-12px); background: rgb(34 197 94 / 0.12); }
.slidein-move { transition: transform 0.35s ease; }
</style>
