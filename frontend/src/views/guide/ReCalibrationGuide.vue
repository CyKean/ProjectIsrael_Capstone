<template>
  <div>
    <button class="start-tour" @click="startTour">
      <Eye class="w-4 h-4 mr-1" /> Start Tour
    </button>
  </div>
</template>

<script setup>
import introJs from 'intro.js'
import 'intro.js/introjs.css'
import { Eye } from 'lucide-vue-next'

const startTour = () => {
  introJs().setOptions({
    steps: [
      { element: '[data-intro-page]', intro: 'This is the main recalibration page.', position: 'bottom' },
      { element: '[data-intro-esp32-1]', intro: 'ESP32-1 Sensor Configuration.', position: 'bottom' },
      { element: '[data-intro-esp32-2]', intro: 'ESP32-2 Sensor Configuration.', position: 'bottom' },
      { element: '[data-intro-esp32-3]', intro: 'ESP32-3 Sensor Configuration.', position: 'bottom' },
      { element: '[data-intro-global-actions]', intro: 'Manage all ESP32 configurations at once.', position: 'bottom' },
      { element: '[data-intro-save-all]', intro: 'Save all configurations.', position: 'top' },
      { element: '[data-intro-reset-all]', intro: 'Reset all ESP32 configurations.', position: 'top' },
      { element: '[data-intro-import-config]', intro: 'Import configurations from a file.', position: 'left' }
    ],
    showStepNumbers: false,
    exitOnOverlayClick: false,
    showBullets: true,
    scrollToElement: true,
    overlayOpacity: 0.4,
    nextLabel: 'Next',
    prevLabel: 'Back',
    doneLabel: 'Finish',
    skipLabel: '×'
  }).start()
}
</script>

<style scoped>
.start-tour {
  position: absolute;
  top: 138px;
  right: 2.5rem; /* right-10 */
  z-index: 50;
  background-color: #059669; /* Tailwind green-600 */
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transition: all 300ms ease;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 500;
}

.start-tour:hover {
  background-color: #047857; /* Tailwind green-700 */
  transform: scale(1.05);
}
</style>
