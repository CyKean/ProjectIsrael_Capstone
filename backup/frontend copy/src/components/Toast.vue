<template>
  <Transition name="toast">
    <div
      v-if="visible"
      :class="['fixed right-4 rounded-lg shadow-lg border p-4 flex items-center gap-3 z-[10001] max-w-md', styles.bg, styles.border]"
      :style="{ bottom: `${bottomOffset}px` }"
    >
      <div :class="[styles.iconBg, 'p-2 rounded-full']">
        <component :is="styles.icon" class="w-5 h-5" :class="styles.iconColor" />
      </div>
      <div>
        <p class="text-sm font-medium text-gray-800">{{ message }}</p>
      </div>
      <button @click="close" class="ml-auto text-gray-400 hover:text-gray-600">
        <X class="w-4 h-4" />
      </button>
    </div>
  </Transition>
</template>

<script setup>
import { X, CheckCircle, Info, AlertTriangle, XCircle } from 'lucide-vue-next'
const props = defineProps({
  message: String,
  severity: { type: String, default: 'info' },
  visible: Boolean,
  bottomOffset: { type: Number, default: 16 },
  styles: Object
})
const emit = defineEmits(['close'])
const close = () => emit('close')
</script>