<template>
  <router-view></router-view>
</template>

<script setup>
import { useUserStore } from '../src/utils/user'
const userStore = useUserStore()
userStore.loadUser()

</script>
