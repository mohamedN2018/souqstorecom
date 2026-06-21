<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import TopBar from "@/components/layout/TopBar.vue";
import SiteHeader from "@/components/layout/SiteHeader.vue";
import NavBar from "@/components/layout/NavBar.vue";
import AppFooter from "@/components/AppFooter.vue";

const route = useRoute();
// Dashboards are fully isolated — no storefront chrome.
const isDashboard = computed(() => route.meta.dashboard === true);
</script>

<template>
  <!-- Isolated dashboard: render only the routed view (it brings its own shell) -->
  <router-view v-if="isDashboard" />

  <!-- Storefront -->
  <div v-else class="min-h-screen flex flex-col">
    <header class="sticky top-0 z-40 shadow-sm">
      <TopBar />
      <SiteHeader />
      <NavBar />
    </header>
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}
.fade-leave-to {
  opacity: 0;
}
</style>
