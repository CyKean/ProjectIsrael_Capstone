<template>
  <div class="bg-white rounded-2xl p-6 shadow-lg border border-blue-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
    <!-- Header -->
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center bg-blue-50 rounded-full px-2.5 py-1 shadow-inner space-x-1.5">
        <Waves class="w-4 h-4 text-blue-500" />
        <h3 class="text-sm font-semibold text-blue-700 tracking-wide">Water Level</h3>
      </div>
      <div class="bg-blue-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">LIVE</div>
    </div>

    <!-- Water Tank -->
    <div class="relative w-64 h-80 mx-auto mt-4">
      <div class="relative w-full h-full rounded-[2rem] border-[6px] border-blue-300 bg-white shadow-2xl overflow-hidden tank-style">

        <!-- Water Fill Area (shifted vertically by percentage) -->
        <!-- Water Fill Area -->
        <div class="absolute bottom-0 left-0 w-full h-full z-10 overflow-hidden">
          <div
            class="absolute top-0 left-0 w-full h-full transition-transform duration-700 ease-in-out"
            :style="{ transform: `translateY(${100 - waterLevel}%)` }"
          >
            <div class="relative w-[900%] h-full">
              <!-- Wave 1 -->
              <div class="absolute w-full h-full left-0 top-0 animate-long-wave-1">
                <svg viewBox="0 0 1200 300" preserveAspectRatio="none" class="w-full h-full">
                  <path
                    d="M0,0 C200,60 400,-60 600,0 C800,60 1000,-60 1200,0 L1200,300 L0,300 Z"
                    fill="#3B82F6" fill-opacity="0.6"
                  />
                </svg>
              </div>
              <!-- Wave 2 -->
              <div class="absolute w-full h-full left-0 top-0 animate-long-wave-2">
                <svg viewBox="0 0 1200 300" preserveAspectRatio="none" class="w-full h-full">
                  <path
                    d="M0,0 C200,50 400,-50 600,0 C800,50 1000,-50 1200,0 L1200,300 L0,300 Z"
                    fill="#60A5FA" fill-opacity="0.4"
                  />
                </svg>
              </div>
              <!-- Wave 3 -->
              <div class="absolute w-full h-full left-0 top-0 animate-long-wave-3">
                <svg viewBox="0 0 1200 300" preserveAspectRatio="none" class="w-full h-full">
                  <path
                    d="M0,0 C200,40 400,-40 600,0 C800,40 1000,-40 1200,0 L1200,300 L0,300 Z"
                    fill="#3B82F6" fill-opacity="0.2"
                  />
                </svg>
              </div>
            </div>
          </div>
        </div>


        <!-- Water Percentage -->
        <div class="absolute inset-0 flex items-center justify-center z-20">
          <div class="bg-white/80 backdrop-blur px-4 py-2 rounded-xl shadow-lg border border-blue-100">
            <span class="text-4xl font-bold text-blue-600">{{ waterLevel }}%</span>
          </div>
        </div>
      </div>

      <!-- Level Markers -->
      <div class="absolute top-2 bottom-2 -right-14 w-10 flex flex-col justify-between z-30">
        <div v-for="n in 5" :key="n" class="flex items-center gap-2">
          <div class="h-[2px] w-4 bg-blue-400 shadow-sm"></div>
          <span class="text-sm font-medium text-blue-600 bg-white/90 px-1 rounded">
            {{ 100 - (n - 1) * 25 }}%
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
const waterLevel = ref(80)
</script>

<style scoped>
@keyframes longWave1 {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
@keyframes longWave2 {
  0% { transform: translateX(0); }
  100% { transform: translateX(-60%); }
}
@keyframes longWave3 {
  0% { transform: translateX(0); }
  100% { transform: translateX(-70%); }
}

.animate-long-wave-1 {
  animation: longWave1 4s linear infinite;
}
.animate-long-wave-2 {
  animation: longWave2 7s linear infinite;
}
.animate-long-wave-3 {
  animation: longWave3 10s linear infinite;
}

.tank-style {
  background: linear-gradient(to top, #e0f2fe, #f8fafc);
  box-shadow:
    inset 0 0 15px rgba(59, 130, 246, 0.2),
    0 10px 20px rgba(0, 0, 0, 0.05);
  border-radius: 2rem;
}
</style>
