<template>
  <Transition name="toast">
    <div
      v-if="visible"
      :class="['rounded-lg shadow-lg border p-2 md:p-4 flex items-center gap-3 max-w-md toast-content', styles.bg, styles.border, { 'mobile-toast': isMobile }]"
      :style="{ bottom: `${bottomOffset}px` }"
    >
      <div :class="[styles.iconBg, 'p-2 rounded-full']">
        <component :is="styles.icon" class="w-3 h-3 md:w-5 md:h-5" :class="styles.iconColor" />
      </div>
      <div class="flex-1 min-w-0">
        <p class="text-[10px] md:text-sm font-medium text-gray-800 break-words">{{ message }}</p>
      </div>
      <button @click="close" class="ml-auto text-gray-400 hover:text-gray-600 flex-shrink-0">
        <X class="w-4 h-4" />
      </button>
    </div>
  </Transition>
</template>

<script setup>
import { X, CheckCircle, Info, AlertTriangle, XCircle } from 'lucide-vue-next'
import { computed } from 'vue'

const props = defineProps({
  message: String,
  severity: { type: String, default: 'info' },
  visible: Boolean,
  bottomOffset: { type: Number, default: 16 },
  styles: Object
})

const emit = defineEmits(['close'])
const close = () => emit('close')

// Check if device is mobile
const isMobile = computed(() => {
  return window.innerWidth <= 768
})
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.9);
}

/* Mobile-specific styles */
@media (max-width: 768px) {
  .toast-content {
    width: calc(100vw - 1rem) !important;
    max-width: none !important;
    margin: 0 auto;
  }
  
  .toast-enter-from {
    transform: translateX(100%) translateY(20px);
  }
  
  .toast-leave-to {
    transform: translateX(100%) translateY(20px) scale(0.9);
  }
}

/* Ensure proper text wrapping */
.break-words {
  word-wrap: break-word;
  overflow-wrap: break-word;
}

.min-w-0 {
  min-width: 0;
}
</style>