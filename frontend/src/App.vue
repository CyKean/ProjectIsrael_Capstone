<template>
  <router-view></router-view>
  <ToastManager />
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useUserStore } from '../src/utils/user'
import ToastManager from './components/ToastManager.vue'

const userStore = useUserStore()
const isAppInitialized = ref(false)

onMounted(async () => {
  // Only initialize once in the main App component
  await userStore.loadUser()
  isAppInitialized.value = true
})
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
</style>