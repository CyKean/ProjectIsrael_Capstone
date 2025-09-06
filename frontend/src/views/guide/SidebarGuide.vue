<template>
  <button class="start-tour" @click="startTour">
    <Eye class="w-4 h-4 mr-1" /> Start Tour
  </button>
</template>

<script setup>
import introJs from 'intro.js';
import 'intro.js/introjs.css';
import { Eye } from 'lucide-vue-next';

const startTour = () => {
  const tour = introJs();

  tour.setOptions({
    steps: [
      { element: document.querySelector('[data-intro-overview]'), intro: 'This is the Overview section.', position: 'bottom' },
      { element: document.querySelector('[data-intro-crop]'), intro: 'Use this for Crop Prediction.', position: 'bottom' },
      { element: document.querySelector('[data-intro-weather]'), intro: 'Weather forecast and monitoring.', position: 'bottom' },
      { element: document.querySelector('[data-intro-device]'), intro: 'Control your device here.', position: 'bottom' },
      { element: document.querySelector('[data-intro-soil]'), intro: 'Soil Analysis tools.', position: 'bottom' },
      { element: document.querySelector('[data-intro-sensor]'), intro: 'Check sensor data.', position: 'bottom' },
      { element: document.querySelector('[data-intro-wifi]'), intro: 'WiFi status indicator.', position: 'bottom' },
      { element: document.querySelector('[data-intro-recalibration]'), intro: 'Recalibration options here.', position: 'bottom', tooltipClass: 'small-intro-tooltip' },
      { element: document.querySelector('[data-intro-notification]'), intro: 'Notification alerts here.', position: 'bottom', tooltipClass: 'small-intro-tooltip' },
      { element: document.querySelector('[data-intro-profile]'), intro: 'Manage your user profile.', position: 'bottom', tooltipClass: 'small-intro-tooltip' }
    ],
    disableInteraction: true,
    showStepNumbers: false,
    showBullets: true,
    overlayOpacity: 0.4,
    exitOnOverlayClick: false,
    scrollToElement: false,
    nextLabel: 'Next',
    prevLabel: 'Back',
    doneLabel: 'Finish',
    skipLabel: '×'
  });

  tour.onafterchange(() => {
    const customTooltips = document.querySelectorAll('.introjs-tooltip.small-intro-tooltip');
    customTooltips.forEach(tooltip => {
      tooltip.style.width = '160px';
      tooltip.style.maxWidth = '160px';
      tooltip.style.minWidth = '160px';
      tooltip.style.padding = '5px 8px';
      tooltip.style.marginLeft = '10px';
      tooltip.style.boxSizing = 'border-box';
    });
  });

  tour.start();
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.start-tour {
  position: absolute;
  bottom: 50px;
  right: 250px;
  z-index: 50;
  background-color: #059669;
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
  background-color: #15803d;
  transform: scale(1.05);
}

:global(.introjs-tooltip) {
  max-width: 200px !important;
  padding: 10px 15px !important;
  font-size: 12px !important;
}

:global(.introjs-tooltip.small-intro-tooltip) {
  width: 160px !important;
  max-width: 160px !important;
  min-width: 160px !important;
  padding: 5px 8px !important;
  margin-left: 10px !important;
  box-sizing: border-box !important;
}

:global(.introjs-tooltip.small-intro-tooltip[style]) {
  max-width: 160px !important;
  min-width: 160px !important;
  padding: 5px 8px !important;
}

:global(.introjs-arrow) {
  transform: scale(0.8) !important;
}
</style>
