<!-- <template>
  <button class="start-tour" @click="startTour">
    <Eye class="w-4 h-4 mr-1" /> Start Tour
  </button>
</template>

<script setup>
import introJs from 'intro.js'
import 'intro.js/introjs.css'
import { Eye } from 'lucide-vue-next'

const startTour = () => {
  introJs().setOptions({
    steps: [
      { element: '[data-intro-avatar]', intro: 'Choose your avatar here.', position: 'right' },
      { element: '[data-intro-personal-info]', intro: 'Edit your personal information here.', position: 'bottom' },
      { element: '[data-intro-security-settings]', intro: 'Manage your security settings.', position: 'bottom' },
      { element: '[data-intro-change-password]', intro: 'Change your password.', position: 'bottom' },
      { element: '[data-intro-change-pin]', intro: 'Change your PIN code.', position: 'bottom' },
      { element: '[data-intro-forgot-password]', intro: 'Recover your account if you forget your credentials.', position: 'bottom' },
      { element: '[data-intro-logout]', intro: 'Logout your account here.', position: 'bottom' }
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
  top: 180px;
  right: 2.5rem; /* right-10 */
  z-index: 1000;
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
  background-color: #047857;
  transform: scale(1.05);
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
</style> -->

<template>
  <button class="start-tour" @click="startTour">
    <Eye class="w-4 h-4 mr-1" /> Start Tour
  </button>
</template>

<script setup>
import introJs from 'intro.js'
import 'intro.js/introjs.css'
import { Eye } from 'lucide-vue-next'
import { onMounted } from 'vue'

const startTour = () => {
  // Add a small delay to ensure DOM is fully rendered
  setTimeout(() => {
    introJs().setOptions({
      steps: [
        { 
          element: document.querySelector('[data-intro-avatar]'), 
          intro: 'Choose your avatar here. Select from a variety of plant-themed characters to represent your profile.', 
          position: 'right' 
        },
        { 
          element: document.querySelector('[data-intro-personal-info]'), 
          intro: 'Edit your personal information here. Update your name and phone number to keep your account details current.', 
          position: 'bottom' 
        },
        { 
          element: document.querySelector('[data-intro-security-settings]'), 
          intro: 'Manage your security settings. Keep your account secure with these options.', 
          position: 'bottom' 
        },
        { 
          element: document.querySelector('[data-intro-change-password]'), 
          intro: 'Change your password. Ensure your account stays secure with a strong, updated password.', 
          position: 'bottom' 
        },
        { 
          element: document.querySelector('[data-intro-change-pin]'), 
          intro: 'Change your PIN code. Use a secure 4-digit PIN for quick access to your account.', 
          position: 'bottom' 
        },
        { 
          element: document.querySelector('[data-intro-forgot-password]'), 
          intro: 'Recover your account if you forget your credentials. Use OTP verification sent to your phone.', 
          position: 'bottom' 
        },
        { 
          element: document.querySelector('[data-intro-logout]'), 
          intro: 'Logout your account here. Securely sign out when you\'re done with your session.', 
          position: 'bottom' 
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
      skipLabel: '×',
      tooltipClass: 'custom-tour-tooltip',
      highlightClass: 'custom-tour-highlight'
    }).start()
  }, 100)
}

// Expose the method to parent components if needed
defineExpose({
  startTour
})
</script>

<style scoped>
.start-tour {
  position: fixed;
  top: 180px;
  right: 2.5rem;
  z-index: 1000;
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
  border: none;
  cursor: pointer;
}

.start-tour:hover {
  background-color: #047857;
  transform: scale(1.05);
}

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
</style>

<style>
/* Additional global styles for the tour */
.custom-tour-tooltip {
  font-family: 'Poppins', sans-serif;
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  max-width: 400px;
}

.custom-tour-tooltip .introjs-tooltip-title {
  color: #059669;
  font-weight: 600;
  font-size: 18px;
  margin-bottom: 8px;
}

.introjs-tooltiptext {
  font-size: 14px;
  line-height: 1.5;
}

.custom-tour-highlight {
  border: 2px solid #059669;
  box-shadow: 0 0 0 4px rgba(5, 150, 105, 0.2);
  border-radius: 12px;
}

.introjs-button {
  border-radius: 8px;
  font-family: 'Poppins', sans-serif;
  font-weight: 500;
  text-shadow: none;
  background-image: none;
  border: none;
  padding: 8px 16px;
  transition: all 0.2s ease;
}

.introjs-button.introjs-nextbutton {
  background-color: #059669;
  color: white;
}

.introjs-button.introjs-nextbutton:hover {
  background-color: #047857;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(5, 150, 105, 0.3);
}

.introjs-button.introjs-prevbutton {
  background-color: #e5e7eb;
  color: #374151;
}

.introjs-button.introjs-prevbutton:hover {
  background-color: #d1d5db;
}

.introjs-button.introjs-donebutton {
  background-color: #059669;
  color: white;
}

.introjs-button.introjs-donebutton:hover {
  background-color: #047857;
}

.introjs-bullets ul li a {
  background: #d1d5db;
}

.introjs-bullets ul li a.active {
  background: #059669;
}

.introjs-skipbutton {
  color: #6b7280;
  font-weight: 500;
}

.introjs-skipbutton:hover {
  color: #374151;
  background-color: #f3f4f6;
}
</style>