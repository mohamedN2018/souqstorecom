<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import TopBar from "@/components/layout/TopBar.vue";
import SiteHeader from "@/components/layout/SiteHeader.vue";
import NavBar from "@/components/layout/NavBar.vue";
import AppFooter from "@/components/AppFooter.vue";
import DepartmentsDrawer from "@/components/layout/DepartmentsDrawer.vue";
import LiveProductToast from "@/components/LiveProductToast.vue";
import { useHeaderScroll } from "@/composables/useHeaderScroll";

const route = useRoute();
// Dashboards are fully isolated — no storefront chrome.
const isDashboard = computed(() => route.meta.dashboard === true);

// Scroll down → keep only the NavBar; scroll up → reveal the whole header.
const { collapsed } = useHeaderScroll();
</script>

<template>
  <!-- Isolated dashboard: render only the routed view (it brings its own shell) -->
  <router-view v-if="isDashboard" />

  <!-- Storefront -->
  <div v-else class="min-h-screen flex flex-col">
    <header class="sticky top-0 z-40">
      <!-- collapsible top rows: smoothly fold to 0 height on scroll-down -->
      <div class="grid transition-[grid-template-rows] duration-300 ease-out"
           :style="{ gridTemplateRows: collapsed ? '0fr' : '1fr' }">
        <div class="overflow-hidden">
          <TopBar />
          <SiteHeader />
        </div>
      </div>
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

    <!-- Amazon-style departments drawer + live new-product toasts -->
    <DepartmentsDrawer />
    <LiveProductToast />
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
