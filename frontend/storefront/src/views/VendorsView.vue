<script setup>
import { ref, onMounted } from "vue";
import { vendorApi } from "@/lib/api";

const vendors = ref([]);
const loading = ref(true);

onMounted(async () => {
  const { data } = await vendorApi.list({ ordering: "-rating_avg" });
  vendors.value = data.results;
  loading.value = false;
});
</script>

<template>
  <div class="container-x py-8">
    <h1 class="text-2xl font-extrabold mb-6">المتاجر</h1>
    <div v-if="loading" class="text-center py-20 text-ink/50">جاري التحميل...</div>
    <div v-else class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
      <router-link v-for="v in vendors" :key="v.id"
                   :to="{ name: 'vendor', params: { slug: v.slug } }"
                   class="card overflow-hidden hover:-translate-y-1 transition">
        <img :src="v.banner_url" class="w-full h-28 object-cover" />
        <div class="p-4 flex items-center gap-3 -mt-8">
          <img :src="v.logo_url" class="w-14 h-14 rounded-full border-4 border-surface object-cover" />
          <div>
            <div class="font-bold">{{ v.name }}</div>
            <div class="text-xs text-ink/50">{{ v.city }} · ★ {{ v.rating_avg }} ({{ v.rating_count }})</div>
          </div>
        </div>
        <p class="px-4 pb-4 text-sm text-ink/60">{{ v.tagline }}</p>
      </router-link>
    </div>
  </div>
</template>
