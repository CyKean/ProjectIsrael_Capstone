<template>
  <div class="h-screen flex bg-gradient-to-br from-green-50 to-emerald-100 font-poppins overflow-x-hidden">
    <Sidebar v-if="!$route.meta.hideSidebar" class="z-20" />
    
    <main class="flex-1 flex flex-col h-screen pt-[4.5rem] xs:pt-[5.5rem] sm:pt-[6.5rem] md:pt-[7rem] lg:pt-[7.5rem] transition-all duration-300">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component 
            :is="Component" 
            :key="$route.fullPath"
            class="router-component"
          />
        </keep-alive>
      </router-view>
    </main>

    <SessionTimeoutWarning />
  
  </div>
</template>

<script setup>
import Sidebar from './views/layout/Sidebar.vue'
import SessionTimeoutWarning from './components/SessionTimeoutWarning.vue'
import { useRoute } from 'vue-router'
import { useUserStore } from './utils/user'
import { watch } from 'vue'

const route = useRoute()
const userStore = useUserStore()

// Initialize user data
if (!userStore.user) {
  userStore.loadUser()
}

// Enhanced route watcher
watch(route, (newRoute, oldRoute) => {
  window.scrollTo(0, 0)
  document.documentElement.style.overflowX = 'hidden'
  
  if (newRoute.path === oldRoute?.path && JSON.stringify(newRoute.params) !== JSON.stringify(oldRoute?.params)) {
    window.location.reload()
  }
}, { immediate: true })
</script>