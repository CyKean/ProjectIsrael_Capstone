<template>
  <router-view></router-view>
</template>

<script setup>
import { useUserStore } from '../src/utils/user'
const userStore = useUserStore()
userStore.loadUser()

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
</style>

