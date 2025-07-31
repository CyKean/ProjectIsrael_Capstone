<template>
  <TransitionGroup name="toast-stack" tag="div">
    <Toast
      v-for="(toast, idx) in toasts"
      :key="toast.id"
      :message="toast.message"
      :severity="toast.severity"
      :visible="toast.visible"
      :bottomOffset="16 + idx * 72"
      :styles="getStyles(toast.severity)"
      @close="removeToast(toast.id)"
      :style="{ position: 'fixed', right: '1rem', bottom: `${16 + idx * 72}px`, zIndex: 10001 }"
    />
  </TransitionGroup>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Toast from './Toast.vue'
import { CheckCircle, Info, AlertTriangle, XCircle } from 'lucide-vue-next'

const toastSound = '../../public/sounds/toast.wav'
const toasts = ref([]) // All currently visible toasts
const toastQueue = ref([]) // Queue for pending toasts
const isProcessingQueue = ref(false)

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
    
    // Add toast to visible toasts
    const toast = {
      ...toastData,
      visible: true
    }
    
    toasts.value.push(toast)
    playToastSound()
    
    // Set up auto-removal
    setTimeout(() => removeToast(toast.id), 5000)
    
    // Wait a bit before showing next toast to prevent simultaneous animations
    await new Promise(resolve => setTimeout(resolve, 200))
  }

  isProcessingQueue.value = false
}

const showToast = (message, severity = 'info') => {
  const id = Date.now() + Math.random()
  const toastData = {
    id,
    message,
    severity
  }
  
  // Add to queue instead of directly showing
  toastQueue.value.push(toastData)
  
  // Process the queue
  processToastQueue()
}

const removeToast = (id) => {
  const idx = toasts.value.findIndex(t => t.id === id)
  if (idx !== -1) {
    // Start the exit animation
    toasts.value[idx].visible = false
    
    // Wait for animation to complete before removing from array
    setTimeout(() => {
      const currentIdx = toasts.value.findIndex(t => t.id === id)
      if (currentIdx !== -1) {
        toasts.value.splice(currentIdx, 1)
      }
    }, 400) // Match the transition duration
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
</style>