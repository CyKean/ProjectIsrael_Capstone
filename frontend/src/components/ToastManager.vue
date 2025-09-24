<template>
  <TransitionGroup name="toast-stack" tag="div" class="toast-container">
    <Toast
      v-for="(toast, idx) in toasts"
      :key="toast.id"
      :message="toast.message"
      :severity="toast.severity"
      :visible="toast.visible"
      :bottomOffset="getBottomOffset(idx)"
      :styles="getStyles(toast.severity)"
      @close="removeToast(toast.id)"
      :class="['toast-item', { 'mobile-toast': isMobile }]"
    />
  </TransitionGroup>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import Toast from './Toast.vue'
import { CheckCircle, Info, AlertTriangle, XCircle } from 'lucide-vue-next'

const toastSound = '/sounds/toast.wav';
const toasts = ref([])
const toastQueue = ref([])
const isProcessingQueue = ref(false)

// Check if device is mobile
const isMobile = computed(() => {
  return window.innerWidth <= 768
})

// Responsive bottom offset calculation
const getBottomOffset = (idx) => {
  if (isMobile.value) {
    // Smaller gap on mobile (8px base + 56px per toast)
    return 8 + idx * 52
  } else {
    // Original gap on desktop (16px base + 72px per toast)
    return 16 + idx * 72
  }
}

const getStyles = (severity) => {
  const styles = {
    success: {
      icon: CheckCircle,
      iconColor: 'text-green-600',
      iconBg: 'bg-green-100',
      bg: 'bg-white',
      border: 'border-green-200'
    },
    info: {
      icon: Info,
      iconColor: 'text-blue-600',
      iconBg: 'bg-blue-100',
      bg: 'bg-white',
      border: 'border-blue-200'
    },
    warning: {
      icon: AlertTriangle,
      iconColor: 'text-yellow-600',
      iconBg: 'bg-yellow-100',
      bg: 'bg-white',
      border: 'border-yellow-200'
    },
    critical: {
      icon: XCircle,
      iconColor: 'text-red-600',
      iconBg: 'bg-red-100',
      bg: 'bg-white',
      border: 'border-red-200'
    },
    failed: {
      icon: XCircle,
      iconColor: 'text-gray-600',
      iconBg: 'bg-gray-100',
      bg: 'bg-white',
      border: 'border-gray-300'
    }
  }
  return styles[severity] || styles.info
}

const playToastSound = () => {
  if (toastSound) {
    const audio = new Audio(toastSound)
    audio.play().catch(() => {})
  }
}

const processToastQueue = async () => {
  if (isProcessingQueue.value || toastQueue.value.length === 0) {
    return
  }

  isProcessingQueue.value = true

  while (toastQueue.value.length > 0) {
    const toastData = toastQueue.value.shift()
    
    const toast = {
      ...toastData,
      visible: true
    }
    
    toasts.value.push(toast)
    playToastSound()
    
    setTimeout(() => removeToast(toast.id), 5000)
    
    await new Promise(resolve => setTimeout(resolve, 200))
  }

  isProcessingQueue.value = false
}

import { useUserStore } from '../utils/user'

const userStore = useUserStore()
const user = computed(() => userStore.user)

// allowWhenLoggedOut: when true, toast will show even if there's no logged-in user
const showToast = (message, severity = 'info', allowWhenLoggedOut = false) => {
  if (!allowWhenLoggedOut && !user.value) {
    // Skip toasts when no user is logged in unless explicitly allowed
    console.log('⏩ Global toast skipped (no user logged in):', message)
    return
  }

  const id = Date.now() + Math.random()
  const toastData = {
    id,
    message,
    severity
  }
  
  toastQueue.value.push(toastData)
  processToastQueue()
}

const removeToast = (id) => {
  const idx = toasts.value.findIndex(t => t.id === id)
  if (idx !== -1) {
    toasts.value[idx].visible = false
    
    setTimeout(() => {
      const currentIdx = toasts.value.findIndex(t => t.id === id)
      if (currentIdx !== -1) {
        toasts.value.splice(currentIdx, 1)
      }
    }, 400)
  }
}

onMounted(() => {
  window.showToast = showToast
})

onUnmounted(() => {
  delete window.showToast
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  right: 0;
  bottom: 0;
  z-index: 10001;
  width: 100%;
  pointer-events: none;
}

.toast-item {
  position: absolute;
  right: 1rem;
  pointer-events: auto;
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  .toast-item {
    right: 0.5rem;
    left: 0.5rem;
    width: auto !important;
  }
}

.toast-stack-enter-active,
.toast-stack-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-stack-enter-from,
.toast-stack-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.95);
}

.toast-stack-move {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Mobile animation adjustments */
@media (max-width: 768px) {
  .toast-stack-enter-from,
  .toast-stack-leave-to {
    transform: translateX(100%) translateY(20px) scale(0.95);
  }
}
</style>