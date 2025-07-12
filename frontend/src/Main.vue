<template>
  <div class="h-screen flex bg-gradient-to-br from-green-50 to-emerald-100 font-poppins overflow-x-hidden">
    <Sidebar v-if="!$route.meta.hideSidebar" class="z-20"/>
    
    <main class="flex-1 flex flex-col h-screen pt-32 transition-all duration-300">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" class="router-component" />
          </keep-alive>
        </router-view>
    </main>
  </div>
</template>

<script setup>
import Sidebar from './views/layout/Sidebar.vue'
import { watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

watch(route, () => {
  window.scrollTo(0, 0)
  document.documentElement.style.overflowX = 'hidden'
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

body {
  font-family: 'Poppins', sans-serif;
}

.router-component {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  main {
    margin-left: 0 !important;
    padding-top: 1rem; 
  }
}
</style>