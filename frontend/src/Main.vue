<template>
  <div class="app-layout">
    <Sidebar v-if="!$route.meta.hideSidebar" />
    <router-view v-slot="{ Component }">
        <component :is="Component" class="router-component" />
    </router-view>
  </div>
</template>

<script setup>
import Sidebar from './views/layout/Sidebar.vue'
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

// Reset scroll position on route change
watch(route, () => {
  window.scrollTo(0, 0)
})
</script>

<style scoped>
.app-layout {
  display: flex;
  min-height: 100vh;
  width: 100vw; /* Use viewport width */
  background-color: #f5f7fa;
}

.main-content {
  flex: 1;
  padding: 0;
  margin-left: 280px; /* Sidebar width */
  width: calc(100vw - 280px); /* Full viewport width minus sidebar */
  min-height: 100vh;
  overflow-x: hidden; /* Prevent horizontal scroll */
}

.main-content.full-width {
  margin-left: 0;
  width: 100vw;
}

.router-component {
  width: 100%;
  max-width: 100%;
  margin: 0;
  padding: 0;
}

@media (max-width: 768px) {
  .main-content {
    margin-left: 0;
    width: 100vw;
  }
}
</style>