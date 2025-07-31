<template>
  <div v-if="userStore.showTimeoutWarning" class="session-timeout-warning">
    <div class="warning-content">
      <h3>Session Timeout Warning</h3>
      <p>You will be logged out due to inactivity in {{ countdown }} seconds.</p>
      <button @click="extendSession">Stay Logged In</button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onUnmounted } from 'vue'
import { useUserStore } from '../utils/user'

const userStore = useUserStore()
const countdown = ref(Math.floor(userStore.config.warningTimeout / 1000))
let countdownInterval = null

watch(() => userStore.showTimeoutWarning, (newVal) => {
  if (newVal) {
    countdown.value = Math.floor(userStore.config.warningTimeout / 1000)
    countdownInterval = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        clearInterval(countdownInterval)
      }
    }, 1000)
  } else {
    clearInterval(countdownInterval)
  }
})

onUnmounted(() => {
  clearInterval(countdownInterval)
})

function extendSession() {
  userStore.resetInactivityTimer()
}
</script>

<style scoped>
.session-timeout-warning {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* Highest z-index */
}

.warning-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  text-align: center;
  z-index: 10000; /* Even higher than the overlay */
}

button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background: #3aa876;
}
</style>