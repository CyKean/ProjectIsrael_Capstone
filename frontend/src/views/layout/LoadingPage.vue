<template>
  <Transition name="fade">
    <div v-if="isVisible" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/40 backdrop-blur-[2px]">
      <div class="gradient-border relative w-[90%] max-w-md rounded-xl p-[3px]">
        <div class="relative w-full h-full rounded-xl bg-white/95 p-6 shadow-xl">
          <div class="flex flex-col items-center justify-center">
            <!-- Plant Illustration Container -->
            <div class="w-full flex justify-center mb-4">
              <div class="w-32 h-32 sm:w-36 sm:h-36 md:w-40 md:h-40 relative">
                <img 
                  src="/public/images/GIF/loading_plant.gif"
                  alt="Loading animation"
                  class="w-full h-full object-contain"
                />
              </div>
            </div>
            
            <!-- Loading Dots -->
            <div class="flex justify-center space-x-2.5 mb-4">
              <div v-for="index in 5" :key="index" class="loading-dot"></div>
            </div>

            <!-- Text Content - Dynamic -->
            <div class="text-center">
              <h3 class="text-xl font-bold text-[#2B5329] mb-2">{{ title }}</h3>
              <p class="text-sm leading-relaxed font-medium text-[#2B5329]/80 max-w-[280px] mx-auto">
                {{ message }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script>
export default {
  name: 'LoadingPage',
  props: {
    isVisible: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Loading'
    },
    message: {
      type: String,
      default: 'Please wait...'
    }
  }
}
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}

/* Loading dots animation */
.loading-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #2B5329;
  animation: dotPulse 1.4s infinite ease-in-out;
}

.loading-dot:nth-child(1) { animation-delay: 0s; }
.loading-dot:nth-child(2) { animation-delay: 0.2s; }
.loading-dot:nth-child(3) { animation-delay: 0.4s; }
.loading-dot:nth-child(4) { animation-delay: 0.6s; }
.loading-dot:nth-child(5) { animation-delay: 0.8s; }

@keyframes dotPulse {
  0%, 100% {
    transform: scale(0.3);
    opacity: 0.3;
  }
  50% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Gradient border animation */
.gradient-border {
  position: relative;
  background: linear-gradient(90deg, #FFB74D, #81C784);
  background-size: 200% 200%;
  animation: gradientBorder 2s linear infinite;
}

.gradient-border::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 0.75rem;
  padding: 3px;
  background: linear-gradient(90deg, #FFB74D, #81C784);
  background-size: 200% 200%;
  animation: gradientBorder 2s linear infinite;
  -webkit-mask: 
    linear-gradient(#fff 0 0) content-box, 
    linear-gradient(#fff 0 0);
  mask: 
    linear-gradient(#fff 0 0) content-box, 
    linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
}

@keyframes gradientBorder {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* Responsive adjustments */
@media (min-width: 640px) {
  .loading-dot {
    width: 9px;
    height: 9px;
  }
}

@media (min-width: 768px) {
  .loading-dot {
    width: 10px;
    height: 10px;
  }
}

/* Modal sizes on different screen sizes */
@media (max-width: 480px) {
  .gradient-border {
    width: 92%;
    max-width: 320px;
  }
}

@media (min-width: 481px) and (max-width: 768px) {
  .gradient-border {
    width: 88%;
    max-width: 380px;
  }
}

@media (min-width: 769px) {
  .gradient-border {
    width: 85%;
    max-width: 420px;
  }
}
</style>