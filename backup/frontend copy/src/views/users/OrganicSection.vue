<template>
  <section class="organic-section relative bg-white overflow-hidden py-8 md:py-16 crops-section">
    <!-- Background Decorative Elements with responsive adjustments -->
    <div class="absolute inset-0 w-full overflow-hidden">
      <!-- Left side decoration - Hidden on mobile -->
      <div class="hidden md:block absolute left-0 h-full w-[250px] lg:w-[400px] overflow-hidden">
        <div class="absolute inset-0 bg-[#4CAF50] border-2 border-orange-200"
             style="clip-path: path('M 0,0 L 380,0 C 360,50 360,50 380,100 L 0,100 Z');">
          <div class="grid grid-cols-4 md:grid-cols-6 gap-1 md:gap-2 p-2 md:p-4 h-full">
            <div v-for="i in 48" :key="`left-${i}`" 
                 class="w-1 md:w-1.5 h-1 md:h-1.5 rounded-full bg-white/20"></div>
          </div>
          <div class="absolute right-0 h-full w-0.5 bg-[#FFD700]"></div>
        </div>
      </div>

      <!-- Right side decoration - Hidden on mobile -->
      <div class="hidden md:block absolute right-0 h-full w-[250px] lg:w-[400px] overflow-hidden">
        <div class="absolute inset-0 bg-[#4CAF50] border-2 border-orange-200"
             style="clip-path: path('M 20,0 L 400,0 L 400,100 L 20,100 C 40,50 40,50 20,0 Z');">
          <div class="grid grid-cols-4 md:grid-cols-6 gap-1 md:gap-2 p-2 md:p-4 h-full">
            <div v-for="i in 48" :key="`right-${i}`" 
                 class="w-1 md:w-1.5 h-1 md:h-1.5 rounded-full bg-white/20"></div>
          </div>
          <div class="absolute left-0 h-full w-0.5 bg-[#FFD700]"></div>
        </div>
      </div>
    </div>

    <!-- Main Content with improved responsive spacing -->
    <div class="container mx-auto max-w-7xl px-4 relative z-10 -mt-4 md:-mt-10">
      <div class="text-center mb-8 md:mb-16">
        <h2 class="text-3xl sm:text-4xl md:text-5xl font-bold mb-3 mt-10 md:mb-8 bg-gradient-to-r from-green-500 to-orange-500 text-transparent bg-clip-text font-poppins">
          ORGANIC CROPS
        </h2>
        <div class="inline-block mt-4 md:mt-8 px-4 md:px-6 py-2 bg-orange-100 rounded-lg">
          <p class="text-orange-600 text-base md:text-lg font-medium font-poppins">
            100% Fresh from our Greenhouse - Naturally Grown with Care and Love
          </p>
        </div>
      </div>

      <!-- Carousel Container with improved responsive handling -->
      <div class="relative pt-8 pb-12 px-2 sm:px-4 md:px-8 -mt-2 md:-mt-4">
        <div class="overflow-hidden">
          <div class="flex transition-transform duration-500 ease-in-out"
               :style="{ transform: `translateX(-${currentSlide * (100 / itemsPerView)}%)` }">
            <div v-for="crop in crops" 
                 :key="crop.name"
                 class="w-full sm:w-1/2 lg:w-1/4 flex-shrink-0 p-2 md:px-3">
              <div class="bg-white rounded-2xl shadow-lg transform transition-all duration-300 hover:scale-[1.02] border-2 border-[#4CAF50]">
                <!-- Image Container with responsive sizing -->
                <div class="relative rounded-xl overflow-visible aspect-square">
                  <img :src="crop.image" 
                       :alt="crop.name"
                       class="w-full h-full object-cover transition-transform duration-300 hover:scale-110 rounded-t-xl" />
                  
                  <!-- Responsive Organic Badge -->
                  <div class="absolute -bottom-3 -right-3 md:-bottom-4 md:-right-4 w-24 h-24 md:w-32 md:h-32 transform rotate-[-15deg] transition-transform hover:rotate-0 hover:scale-110 z-10">
                    <img src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/organic-badge-No9lws1YZjeLFUM5mOFGsAPbjPoRqz.png"
                         alt="100% Organic Badge"
                         class="w-full h-full object-contain drop-shadow-lg" />
                  </div>
                </div>
                
                <!-- Crop Name with responsive text -->
                <div class="p-3 md:p-4 bg-[#4CAF50] rounded-b-xl">
                  <h3 class="text-lg md:text-xl font-bold text-center text-white font-poppins">
                    {{ crop.name }}
                  </h3>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Navigation Buttons with improved mobile touch areas -->
        <button @click="prevSlide" 
                :disabled="currentSlide === 0"
                class="absolute left-0 top-1/2 -translate-y-1/2 w-8 h-8 md:w-10 md:h-10 
                       bg-[#4CAF50] text-white rounded-full flex items-center justify-center 
                       hover:bg-[#45a049] transition-colors disabled:opacity-50 disabled:cursor-not-allowed
                       focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#4CAF50] z-20
                       touch-manipulation">
          <svg xmlns="http://www.w3.org/2000/svg" 
               class="h-5 w-5 md:h-6 md:w-6" 
               fill="none" 
               viewBox="0 0 24 24" 
               stroke="currentColor">
            <path stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="2" 
                  d="M15 19l-7-7 7-7" />
          </svg>
        </button>

        <button @click="nextSlide" 
                :disabled="isLastSlide"
                class="absolute right-0 top-1/2 -translate-y-1/2 w-8 h-8 md:w-10 md:h-10 
                       bg-[#4CAF50] text-white rounded-full flex items-center justify-center 
                       hover:bg-[#45a049] transition-colors disabled:opacity-50 disabled:cursor-not-allowed
                       focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#4CAF50] z-20
                       touch-manipulation">
          <svg xmlns="http://www.w3.org/2000/svg" 
               class="h-5 w-5 md:h-6 md:w-6" 
               fill="none" 
               viewBox="0 0 24 24" 
               stroke="currentColor">
            <path stroke-linecap="round" 
                  stroke-linejoin="round" 
                  stroke-width="2" 
                  d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  </section>
</template>

<script setup>
// Script remains the same as it already handles responsiveness well
import { ref, computed, onMounted } from 'vue'

const crops = [
  {
    name: 'EGGPLANT',
    image: '/public/images/crops/eggplant.png'
  },
  {
    name: 'CARROTS',
    image: '/public/images/crops/carrots.png'
  },
  {
    name: 'CABBAGE',
    image: '/public/images/crops/cabbage.png'
  },
  {
    name: 'TOMATOES',
    image: '/public/images/crops/tomatoes.png'
  },
  {
    name: 'LETTUCE',
    image: '/public/images/crops/lettuce.png'
  }
]

const currentSlide = ref(0)
const windowWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 1024)

const itemsPerView = computed(() => {
  if (windowWidth.value >= 1024) return 4
  if (windowWidth.value >= 640) return 2
  return 1
})

const isLastSlide = computed(() => {
  return currentSlide.value >= crops.length - itemsPerView.value
})

const nextSlide = () => {
  if (!isLastSlide.value) {
    currentSlide.value++
  }
}

const prevSlide = () => {
  if (currentSlide.value > 0) {
    currentSlide.value--
  }
}

onMounted(() => {
  if (typeof window !== 'undefined') {
    const handleResize = () => {
      windowWidth.value = window.innerWidth
      // Ensure current slide is valid for new viewport
      if (currentSlide.value > crops.length - itemsPerView.value) {
        currentSlide.value = Math.max(0, crops.length - itemsPerView.value)
      }
    }

    window.addEventListener('resize', handleResize)
    handleResize() // Initial check

    // Cleanup
    return () => {
      window.removeEventListener('resize', handleResize)
    }
  }
})
</script>

<style scoped>
/* Import Poppins font */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Apply Poppins to all elements */
* {
  font-family: 'Poppins', sans-serif;
}

.organic-section {
  min-height: min-content;
}

/* Ensure smooth transitions */
* {
  transition: all 0.3s ease-in-out;
}

/* Fix for Safari border-radius clipping */
.rounded-2xl {
  transform: translateZ(0);
  mask-image: radial-gradient(white, black);
  -webkit-mask-image: -webkit-radial-gradient(white, black);
}

/* Add touch-friendly improvements for mobile */
@media (hover: none) {
  .touch-manipulation {
    touch-action: manipulation;
  }
}

/* Improve performance on mobile devices */
@media (max-width: 640px) {
  .transition-transform {
    will-change: transform;
  }
}
</style>