<template>
  <div class="min-h-screen w-full flex items-center justify-center bg-white p-4">
    <div 
      :class="['text-center max-w-2xl mx-auto', { 'slide-out': isLeaving }]"
    >
      <!-- Lottie Animation Container -->
      <div class="w-full max-w-md mx-auto my-4">
        <dotlottie-player
          src="https://lottie.host/3ca23ce0-55bb-4468-90dd-96d072542932/BJ5CK7fZ2k.lottie"
          background="transparent"
          speed="1"
          style="width: 100%; height: 300px;"
          loop
          autoplay
        ></dotlottie-player>
      </div>

      <h2 class="text-3xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-[#4CAF50] to-[#FF9800] inline-block text-transparent bg-clip-text">
        PAGE NOT FOUND
      </h2>
      
      <p class="text-gray-600 text-base md:text-sm mb-8 max-w-lg mx-auto">
        Looks like you're a little off track, but don't worry, every field has its path.
        Let us guide you back to precision!
      </p>

      <button 
        @click="handleGoBack"
        class="inline-flex items-center px-5 py-2 bg-[#4CAF50] text-white rounded-lg hover:bg-[#45a049] transition-colors duration-300 text-base font-medium"
      >
        Go Back
        <ArrowRight class="ml-2 h-5 w-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ArrowRight } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

// Add this to your index.html or main entry file
if (typeof window !== 'undefined') {
  import('https://unpkg.com/@dotlottie/player-component@2.7.12/dist/dotlottie-player.mjs')
}

const router = useRouter()
const isLeaving = ref(false)

const handleGoBack = () => {
  isLeaving.value = true
  setTimeout(() => {
    router.back()
  }, 500) // Match this with the CSS transition duration
}
</script>

<style scoped>
dotlottie-player {
  margin: 0 auto;
}

/* Slide out animation */
.slide-out {
  animation: slideRight 0.5s ease-in-out forwards;
}

@keyframes slideRight {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}

/* Ensure animations work across different browsers */
@supports (-webkit-appearance:none) {
  @-webkit-keyframes slideRight {
    from {
      opacity: 1;
      -webkit-transform: translateX(0);
    }
    to {
      opacity: 0;
      -webkit-transform: translateX(100%);
    }
  }
}

/* Optimize for mobile devices */
@media (max-width: 768px) {
  .slide-out {
    animation-duration: 0.3s;
  }
}
</style>

