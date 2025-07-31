<template>
  <Transition name="modal" appear>
    <div class="fixed inset-0 bg-black/40 backdrop-blur-[2px] flex items-center justify-center z-50 p-4 modal-backdrop">
      <div class="bg-white rounded-3xl shadow-2xl max-w-sm w-full mx-4 overflow-hidden modal-popup">
        
        <!-- Content Container -->
        <div class="px-8 py-10 text-center">
          
          <!-- Modern Icon -->
          <div class="mb-6 flex justify-center">
            <div class="relative">
              <!-- Decorative circles -->
              <div class="flex items-center justify-center space-x-1">
                <div class="w-3 h-3 bg-gradient-to-br from-blue-400 to-blue-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                <div class="w-4 h-4 bg-gradient-to-br from-purple-400 to-purple-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                <div class="w-3 h-3 bg-gradient-to-br from-pink-400 to-pink-500 rounded-full animate-bounce" style="animation-delay: 0.3s"></div>
              </div>
              <div class="flex items-center justify-center space-x-1 mt-1">
                <div class="w-2 h-2 bg-gradient-to-br from-yellow-400 to-orange-400 rounded-full animate-bounce" style="animation-delay: 0.4s"></div>
                <div class="w-3 h-3 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full animate-bounce" style="animation-delay: 0.5s"></div>
                <div class="w-2 h-2 bg-gradient-to-br from-red-400 to-red-500 rounded-full animate-bounce" style="animation-delay: 0.6s"></div>
              </div>
            </div>
          </div>
          
          <!-- Green Heading -->
          <h2 class="text-2xl font-bold text-emerald-600 mb-3 tracking-tight animate-pulse-text">
            Goodbye for now!
          </h2>
          
          <!-- Subtitle -->
          <p class="text-gray-600 text-base leading-relaxed mb-8 font-medium">
            Are you sure you want to sign out of your account?
          </p>
          
          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-3">
            <button 
              @click="$emit('cancel')" 
              class="flex-1 px-6 py-3.5 bg-gray-50 hover:bg-gray-100 text-gray-700 font-semibold rounded-2xl transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-gray-200 focus:ring-offset-2 border border-gray-200 hover:border-gray-300 animate-slide-up"
            >
              Stay Here
            </button>
            <button 
              @click="$emit('confirm')" 
              class="flex-1 px-6 py-3.5 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white font-semibold rounded-2xl transition-all duration-200 ease-in-out transform hover:scale-105 active:scale-95 focus:outline-none focus:ring-2 focus:ring-red-300 focus:ring-offset-2 shadow-lg hover:shadow-xl animate-slide-up"
              style="animation-delay: 0.1s"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<style scoped>
/* Modal backdrop fade animation */
.modal-enter-active {
  animation: backdropFadeIn 0.3s ease-out;
}

.modal-leave-active {
  animation: backdropFadeOut 0.25s ease-in;
}

@keyframes backdropFadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes backdropFadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

/* Modal popup animation */
.modal-popup {
  animation: modalPopup 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55) forwards;
}

@keyframes modalPopup {
  0% {
    transform: scale(0.3) translateY(-50px) rotate(-5deg);
    opacity: 0;
  }
  50% {
    transform: scale(1.1) translateY(-10px) rotate(2deg);
    opacity: 0.8;
  }
  100% {
    transform: scale(1) translateY(0) rotate(0deg);
    opacity: 1;
  }
}

/* Bouncing dots animation */
@keyframes bounce {
  0%, 20%, 53%, 80%, 100% {
    transform: translate3d(0, 0, 0);
  }
  40%, 43% {
    transform: translate3d(0, -8px, 0);
  }
  70% {
    transform: translate3d(0, -4px, 0);
  }
  90% {
    transform: translate3d(0, -2px, 0);
  }
}

.animate-bounce {
  animation: bounce 2s infinite;
}

/* Pulsing text animation */
@keyframes pulseText {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.02);
  }
}

.animate-pulse-text {
  animation: pulseText 2s ease-in-out infinite;
}

/* Slide up animation for buttons */
@keyframes slideUp {
  from {
    transform: translateY(20px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.animate-slide-up {
  animation: slideUp 0.4s ease-out forwards;
}

/* Enhanced hover effects */
button:hover {
  transform: scale(1.05) !important;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
}

button:active {
  transform: scale(0.95) !important;
}

/* Subtle backdrop blur */
.backdrop-blur-\[2px\] {
  -webkit-backdrop-filter: blur(2px);
  backdrop-filter: blur(2px);
}

/* Responsive design */
@media (max-width: 640px) {
  .flex-col {
    flex-direction: column;
  }
}

/* Cross-browser compatibility */
* {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Enhanced focus states for accessibility */
button:focus-visible {
  outline: 2px solid transparent;
  outline-offset: 2px;
}

/* Smooth transitions for all interactive elements */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}
</style>