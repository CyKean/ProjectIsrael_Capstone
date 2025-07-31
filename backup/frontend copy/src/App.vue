<template>
  <router-view></router-view>
  <ToastManager />
</template>

<script setup>
import { onMounted } from 'vue'
import { useUserStore } from '../src/utils/user'
import ToastManager from './components/ToastManager.vue'
const userStore = useUserStore()
userStore.loadUser()

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
</style>

