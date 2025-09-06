<!-- <template>
  <button class="start-tour" @click="startTour">
    <Eye class="w-4 h-4 mr-2" /> Start Tour
  </button>
</template>

<script setup>
import { Eye } from 'lucide-vue-next'
import introJs from 'intro.js'
import 'intro.js/introjs.css'

const scrollToElement = (selector) => {
  const el = document.querySelector(selector)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

const startTour = () => {
  // Scroll all important elements into view
  scrollToElement('[data-intro-soil]')
  scrollToElement('[data-intro-environment]')
  scrollToElement('[data-intro-recommendation-button]')
  scrollToElement('[data-intro-history-table]')
  
  // Wait for layout & scroll to settle
  setTimeout(() => {
    // Force browser to reflow layout
    window.dispatchEvent(new Event('resize'))
    
    // Optional: allow the layout to repaint
    requestAnimationFrame(() => {
      const tour = introJs()
      tour.setOptions({
        steps: [
          {
            element: '[data-intro-soil-composition]',
            intro: 'This section shows your soil composition—NPK, pH, and moisture levels.',
            position: 'bottom'
          },
          {
            element: '[data-intro-environment]',
            intro: 'These are environmental conditions like temperature, humidity, and rainfall.',
            position: 'top'
          },
          {
            element: '[data-intro-recommendation-button]',
            intro: 'Click this to generate your crop recommendation based on the latest data.',
            position: 'bottom'
          },
          {
            element: '[data-intro-history-table]',
            intro: 'Here you can view all your past recommendations and update their status.',
            position: 'top'
          }
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
      })
      
      // Ensure layout is refreshed before starting
      tour.onbeforechange(() => {
        setTimeout(() => tour.refresh(), 100)
      })
      
      tour.start()
    })
  }, 600)
}
</script>

<style scoped>
[data-intro-soil],
[data-intro-environment],
[data-intro-recommendation-button],
[data-intro-history-table] {
  will-change: transform;
  position: relative;
  z-index: 10;
}

.start-tour {
  @apply fixed top-24 right-6 z-50 bg-green-600 text-white px-4 py-2 rounded-full flex items-center gap-2 shadow-lg hover:bg-green-700 transition-all duration-300 hover:scale-105;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 500;
}

/* Import Poppins font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Global intro.js styling overrides */
:global(.introjs-overlay) {
  background-color: rgba(0, 0, 0, 0.4) !important;
}

:global(.introjs-helperLayer) {
  background: transparent !important;
  border: 3px solid #10b981 !important;
  border-radius: 12px !important;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04), 0 0 0 1px rgba(16, 185, 129, 0.3) !important;
  animation: floatHighlight 2s ease-in-out infinite alternate !important;
}

/* Main tooltip container - INCREASED WIDTH */
:global(.introjs-tooltip) {
  background: white !important;
  border: 2px solid #10b981 !important;
  border-radius: 12px !important;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15) !important;
  font-family: 'Poppins', sans-serif !important;
  font-size: 14px !important;
  max-width: 400px !important;
  min-width: 350px !important;
  padding: 0 !important;
  position: relative !important;
  overflow: hidden !important;
}

/* Green header div */
:global(.introjs-tooltip::before) {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  z-index: 1;
}

/* Tooltip content area */
:global(.introjs-tooltip-text) {
  color: #374151 !important;
  line-height: 1.6 !important;
  margin: 24px 28px 20px 28px !important;
  font-weight: 400 !important;
  font-size: 14px !important;
  padding-top: 6px !important;
}

/* Close button with GREEN CIRCLE background */
:global(.introjs-skipbutton) {
  position: absolute !important;
  top: 12px !important;
  right: 14px !important;
  background: #10b981 !important;
  border: none !important;
  color: white !important;
  cursor: pointer !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  line-height: 1 !important;
  padding: 0 !important;
  width: 24px !important;
  height: 24px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 50% !important;
  transition: all 0.2s ease !important;
  z-index: 2 !important;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3) !important;
}

:global(.introjs-skipbutton:hover) {
  background: #059669 !important;
  transform: scale(1.1) !important;
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.4) !important;
}

/* Progress indicators */
:global(.introjs-bullets) {
  text-align: center !important;
  margin: 0 28px 24px 28px !important;
  padding: 0 !important;
}

:global(.introjs-bullets ul) {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 6px !important;
  list-style: none !important;
  margin: 0 !important;
  padding: 0 !important;
}

:global(.introjs-bullets ul li) {
  display: inline-block !important;
  margin: 0 !important;
}

/* Gray dots for inactive steps */
:global(.introjs-bullets ul li a) {
  background: #d1d5db !important;
  border-radius: 50% !important;
  cursor: pointer !important;
  display: block !important;
  height: 8px !important;
  text-indent: -999em !important;
  width: 8px !important;
  transition: all 0.3s ease !important;
  border: none !important;
}

/* Orange line for active step */
:global(.introjs-bullets ul li a.active) {
  background: #f97316 !important;
  border-radius: 4px !important;
  width: 20px !important;
  height: 8px !important;
}

:global(.introjs-bullets ul li a:hover) {
  background: #9ca3af !important;
}

:global(.introjs-bullets ul li a.active:hover) {
  background: #ea580c !important;
}

/* Button container - IMPROVED SPACING */
:global(.introjs-tooltipbuttons) {
  display: flex !important;
  justify-content: space-between !important;
  gap: 16px !important;
  margin: 0 28px 28px 28px !important;
  padding: 0 !important;
}

/* Button styling - CENTERED TEXT AND PROPER SIZING */
:global(.introjs-button) {
  background: #f97316 !important;
  border: none !important;
  border-radius: 8px !important;
  color: white !important;
  cursor: pointer !important;
  font-family: 'Poppins', sans-serif !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  padding: 12px 24px !important;
  transition: all 0.3s ease !important;
  text-rendering: optimizeLegibility !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  letter-spacing: 0.025em !important;
  text-shadow: none !important;
  outline: none !important;
  min-width: 100px !important;
  flex: 1 !important;
  text-align: center !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

:global(.introjs-button:hover) {
  transform: scale(1.05) !important;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4) !important;
}

:global(.introjs-button:focus) {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.3) !important;
}

/* Next and Done buttons (Green) */
:global(.introjs-nextbutton) {
  background: #10b981 !important;
}

:global(.introjs-nextbutton:hover) {
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
}

:global(.introjs-nextbutton:focus) {
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3) !important;
}

:global(.introjs-donebutton) {
  background: #10b981 !important;
}

:global(.introjs-donebutton:hover) {
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
}

:global(.introjs-donebutton:focus) {
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3) !important;
}

/* Back button (Orange) */
:global(.introjs-prevbutton) {
  background: #f97316 !important;
}

.guide-container {
  position: fixed;
  bottom: 24px;  /* Moves it to the bottom */
  right: 24px;
  z-index: 9999;
}

.guide-button {
  display: flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 9999px; /* Makes it extra round */
  padding: 12px 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.guide-button:hover {
  transform: scale(1.05);
}

/* Arrow styling */
:global(.introjs-arrow) {
  border-top-color: #10b981 !important;
  border-bottom-color: #10b981 !important;
  border-left-color: #10b981 !important;
  border-right-color: #10b981 !important;
}

:global(.introjs-arrow.top) {
  border-bottom-color: white !important;
}

:global(.introjs-arrow.bottom) {
  border-top-color: white !important;
}

:global(.introjs-arrow.left) {
  border-right-color: white !important;
}

:global(.introjs-arrow.right) {
  border-left-color: white !important;
}

/* Floating animation */
@keyframes floatHighlight {
  0% {
    transform: translateY(0px) scale(1);
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04), 0 0 0 1px rgba(16, 185, 129, 0.3);
  }
  100% {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 30px 35px -5px rgba(0, 0, 0, 0.15), 0 15px 15px -5px rgba(0, 0, 0, 0.08), 0 0 0 1px rgba(16, 185, 129, 0.5);
  }
}

@media (max-width: 768px) {
  .guide-button {
    padding: 10px 16px;
    font-size: 12px;
  }
}

</style> -->

<template>
  <button class="start-tour" @click="startTour">
    <Eye class="w-4 h-4 mr-2" /> Start Tour
  </button>
</template>

<script setup>
import { Eye } from 'lucide-vue-next'
import introJs from 'intro.js'
import 'intro.js/introjs.css'

const scrollToElement = (selector) => {
  const el = document.querySelector(selector)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth', block: 'center' })
  }
}

const startTour = () => {
  // Scroll all important elements into view
  scrollToElement('[data-intro-soil]')
  scrollToElement('[data-intro-environment]')
  scrollToElement('[data-intro-recommendation-button]')
  scrollToElement('[data-intro-history-table]')
  
  // Wait for layout & scroll to settle
  setTimeout(() => {
    // Force browser to reflow layout
    window.dispatchEvent(new Event('resize'))
    
    // Optional: allow the layout to repaint
    requestAnimationFrame(() => {
      const tour = introJs()
      tour.setOptions({
        steps: [
          {
            element: '[data-intro-soil-composition]',
            intro: 'This section shows your soil composition—NPK, pH, and moisture levels.',
            position: 'bottom'
          },
          {
            element: '[data-intro-environment]',
            intro: 'These are environmental conditions like temperature, humidity, and rainfall.',
            position: 'top'
          },
          {
            element: '[data-intro-recommendation-button]',
            intro: 'Click this to generate your crop recommendation based on the latest data.',
            position: 'bottom'
          },
          {
            element: '[data-intro-history-table]',
            intro: 'Here you can view all your past recommendations and update their status.',
            position: 'top'
          }
        ],
        showStepNumbers: false,
        exitOnOverlayClick: false,
        showBullets: true,
        scrollToElement: true,
        overlayOpacity: 0.8, // Increased to make background very dark
        nextLabel: 'Next',
        prevLabel: 'Back',
        doneLabel: 'Finish',
        skipLabel: '×'
      })
      
      // Ensure layout is refreshed before starting
      tour.onbeforechange(() => {
        setTimeout(() => tour.refresh(), 100)
      })
      
      tour.start()
    })
  }, 600)
}
</script>

<style scoped>
[data-intro-soil],
[data-intro-environment],
[data-intro-recommendation-button],
[data-intro-history-table] {
  will-change: transform;
  position: relative;
  z-index: 10;
}

.start-tour {
  @apply fixed top-24 right-6 z-50 bg-green-600 text-white px-4 py-2 rounded-full flex items-center gap-2 shadow-lg hover:bg-green-700 transition-all duration-300 hover:scale-105;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 500;
}

/* Import Poppins font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* Global intro.js styling overrides - DARK BACKGROUND */
:global(.introjs-overlay) {
  background-color: rgba(75, 72, 72, 0.85) !important; /* Very dark background */
}

/* Make the highlighted element stand out more */
:global(.introjs-helperLayer) {
  background: transparent !important;
  border: 3px solid #10b981 !important;
  border-radius: 12px !important;
  box-shadow: 
    0 0 0 1000px rgba(0, 0, 0, 0.4), /* This creates the dark overlay effect */
    0 20px 25px -5px rgba(0, 0, 0, 0.3), 
    0 10px 10px -5px rgba(0, 0, 0, 0.2),
    0 0 0 2px rgba(16, 185, 129, 0.8) !important;
  animation: floatHighlight 2s ease-in-out infinite alternate !important;
}

/* Force the highlighted element to be brighter */
:global(.introjs-showElement) {
  filter: brightness(1.2) !important;
  transform: scale(1.02) !important;
  transition: all 0.3s ease !important;
}

/* Main tooltip container */
:global(.introjs-tooltip) {
  background: white !important;
  border: 2px solid #10b981 !important;
  border-radius: 12px !important;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3) !important;
  font-family: 'Poppins', sans-serif !important;
  font-size: 14px !important;
  max-width: 400px !important;
  min-width: 350px !important;
  padding: 0 !important;
  position: relative !important;
  overflow: hidden !important;
  z-index: 10001 !important;
}

/* Green header div */
:global(.introjs-tooltip::before) {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(90deg, #10b981 0%, #059669 100%);
  z-index: 1;
}

/* Tooltip content area */
:global(.introjs-tooltip-text) {
  color: #374151 !important;
  line-height: 1.6 !important;
  margin: 24px 28px 20px 28px !important;
  font-weight: 400 !important;
  font-size: 14px !important;
  padding-top: 6px !important;
}

/* Close button with GREEN CIRCLE background */
:global(.introjs-skipbutton) {
  position: absolute !important;
  top: 12px !important;
  right: 14px !important;
  background: #10b981 !important;
  border: none !important;
  color: white !important;
  cursor: pointer !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  line-height: 1 !important;
  padding: 0 !important;
  width: 24px !important;
  height: 24px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  border-radius: 50% !important;
  transition: all 0.2s ease !important;
  z-index: 2 !important;
  box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3) !important;
}

:global(.introjs-skipbutton:hover) {
  background: #059669 !important;
  transform: scale(1.1) !important;
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.4) !important;
}

/* Progress indicators */
:global(.introjs-bullets) {
  text-align: center !important;
  margin: 0 28px 24px 28px !important;
  padding: 0 !important;
}

:global(.introjs-bullets ul) {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
  gap: 6px !important;
  list-style: none !important;
  margin: 0 !important;
  padding: 0 !important;
}

:global(.introjs-bullets ul li) {
  display: inline-block !important;
  margin: 0 !important;
}

/* Gray dots for inactive steps */
:global(.introjs-bullets ul li a) {
  background: #d1d5db !important;
  border-radius: 50% !important;
  cursor: pointer !important;
  display: block !important;
  height: 8px !important;
  text-indent: -999em !important;
  width: 8px !important;
  transition: all 0.3s ease !important;
  border: none !important;
}

/* Orange line for active step */
:global(.introjs-bullets ul li a.active) {
  background: #f97316 !important;
  border-radius: 4px !important;
  width: 20px !important;
  height: 8px !important;
}

:global(.introjs-bullets ul li a:hover) {
  background: #9ca3af !important;
}

:global(.introjs-bullets ul li a.active:hover) {
  background: #ea580c !important;
}

/* Button container - IMPROVED SPACING */
:global(.introjs-tooltipbuttons) {
  display: flex !important;
  justify-content: space-between !important;
  gap: 16px !important;
  margin: 0 28px 28px 28px !important;
  padding: 0 !important;
}

/* Button styling - CENTERED TEXT AND PROPER SIZING */
:global(.introjs-button) {
  background: #f97316 !important;
  border: none !important;
  border-radius: 8px !important;
  color: white !important;
  cursor: pointer !important;
  font-family: 'Poppins', sans-serif !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  padding: 12px 24px !important;
  transition: all 0.3s ease !important;
  text-rendering: optimizeLegibility !important;
  -webkit-font-smoothing: antialiased !important;
  -moz-osx-font-smoothing: grayscale !important;
  letter-spacing: 0.025em !important;
  text-shadow: none !important;
  outline: none !important;
  min-width: 100px !important;
  flex: 1 !important;
  text-align: center !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

:global(.introjs-button:hover) {
  transform: scale(1.05) !important;
  box-shadow: 0 4px 12px rgba(249, 115, 22, 0.4) !important;
}

:global(.introjs-button:focus) {
  outline: none !important;
  box-shadow: 0 0 0 2px rgba(249, 115, 22, 0.3) !important;
}

/* Next and Done buttons (Green) */
:global(.introjs-nextbutton) {
  background: #10b981 !important;
}

:global(.introjs-nextbutton:hover) {
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
}

:global(.introjs-nextbutton:focus) {
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3) !important;
}

:global(.introjs-donebutton) {
  background: #10b981 !important;
}

:global(.introjs-donebutton:hover) {
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4) !important;
}

:global(.introjs-donebutton:focus) {
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.3) !important;
}

/* Back button (Orange) */
:global(.introjs-prevbutton) {
  background: #f97316 !important;
}

.guide-container {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
}

.guide-button {
  display: flex;
  align-items: center;
  gap: 10px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 9999px;
  padding: 12px 20px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.guide-button:hover {
  transform: scale(1.05);
}

/* Arrow styling */
:global(.introjs-arrow) {
  border-top-color: #10b981 !important;
  border-bottom-color: #10b981 !important;
  border-left-color: #10b981 !important;
  border-right-color: #10b981 !important;
}

:global(.introjs-arrow.top) {
  border-bottom-color: white !important;
}

:global(.introjs-arrow.bottom) {
  border-top-color: white !important;
}

:global(.introjs-arrow.left) {
  border-right-color: white !important;
}

:global(.introjs-arrow.right) {
  border-left-color: white !important;
}

/* Floating animation */
@keyframes floatHighlight {
  0% {
    transform: translateY(0px) scale(1);
    box-shadow: 
      0 0 0 9999px rgba(0, 0, 0, 0.85),
      0 20px 25px -5px rgba(0, 0, 0, 0.3), 
      0 10px 10px -5px rgba(0, 0, 0, 0.2),
      0 0 0 2px rgba(16, 185, 129, 0.8);
  }
  100% {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 
      0 0 0 9999px rgba(0, 0, 0, 0.85),
      0 30px 35px -5px rgba(0, 0, 0, 0.4), 
      0 15px 15px -5px rgba(0, 0, 0, 0.3),
      0 0 0 2px rgba(16, 185, 129, 1);
  }
}

@media (max-width: 768px) {
  .guide-button {
    padding: 10px 16px;
    font-size: 12px;
  }
}
</style>