<template>
  <div class="min-h-screen bg-white relative overflow-hidden font-poppins home-section">
    <Navbar @auth="handleAuth" />

    <div class="relative z-10">
      <transition name="page-transition" mode="out-in" @before-leave="beforeLeave" @enter="enter" @after-enter="afterEnter">
        <div :key="transitionKey" class="page-content" :style="contentStyle">
          <!-- <Navbar @auth="handleAuth" /> -->
          <!-- Wave Container -->
          <div class="absolute bottom-0 left-0 right-0 w-full h-[200px] sm:h-[300px] z-0 overflow-hidden px-6 sm:px-12 md:px-16 lg:px-24" style="pointer-events: none;">
            <div class="wave wave-orange"></div>
            <div class="wave wave-green"></div>
          </div>

          <!-- Falling Leaves Animation -->
          <div class="absolute inset-0 pointer-events-none z-10 overflow-hidden">
            <div v-for="i in (isMobile ? 10 : 20)" :key="`leaf1-${i}`" 
                 class="leaf absolute animate-fall"
                 :style="{
                   left: `${Math.random() * 100}%`,
                   top: `${Math.random() * -200}%`,
                   animationDuration: `${20 + Math.random() * 20}s`,
                   animationDelay: `${Math.random() * -40}s`,
                   transform: `scale(${isMobile ? 0.6 : 1})`
                 }">
              <img 
                src="/public/images/leaves-plants/fall-leaf1.png" 
                alt="" 
                class="w-16 sm:w-24 h-16 sm:h-24 opacity-60"
              />
            </div>
            
            <div v-for="i in (isMobile ? 10 : 20)" :key="`leaf2-${i}`" 
                 class="leaf absolute animate-fall"
                 :style="{
                   left: `${Math.random() * 100}%`,
                   top: `${Math.random() * -200}%`,
                   animationDuration: `${20 + Math.random() * 20}s`,
                   animationDelay: `${Math.random() * -40}s`,
                   transform: `scale(${isMobile ? 0.6 : 1})`
                 }">
              <img 
                src="/public/images/leaves-plants/fall-leaf2.png" 
                alt="" 
                class="w-20 sm:w-28 h-20 sm:h-28 opacity-60"
              />
            </div>
          </div>

          <!-- Main Content -->
          <div class="container mx-auto px-8 sm:px-12 md:px-20 lg:px-32 xl:px-40 2xl:px-48 min-h-screen relative z-20 flex items-center">
            <div class="flex flex-col lg:flex-row items-center justify-between w-full pt-20 sm:pt-24 lg:pt-0">
              <!-- Left Content -->
              <div class="lg:w-1/2 text-left lg:text-left mb-8 lg:mb-0 pl-6 sm:pl-10 md:pl-16 lg:pl-20 xl:pl-24 2xl:pl-28">
                <h1 class="text-[#2E7D32] text-3xl xs:text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-extrabold mb-4 font-poppins tracking-wide relative">
                  PROJECT ISRAEL
                  <!-- Plant decorations with improved responsive visibility -->
                  <img 
                    src="/public/images/leaves-plants/plant-decoration.png" 
                    alt=""
                    class="absolute top-0 left-[1%] w-4 xs:w-5 sm:w-6 md:w-8 h-4 xs:h-5 sm:h-6 md:h-8 -mt-4 hidden sm:block pointer-events-none"
                  />
                  <img 
                    src="/public/images/leaves-plants/plant-decoration.png" 
                    alt=""
                    class="absolute top-0 left-[35%] w-4 xs:w-5 sm:w-6 md:w-8 h-4 xs:h-5 sm:h-6 md:h-8 -mt-4 hidden sm:block pointer-events-none"
                  />
                  <img 
                    src="/public/images/leaves-plants/plant-decoration.png" 
                    alt=""
                    class="absolute top-0 left-[75%] w-4 xs:w-5 sm:w-6 md:w-8 h-4 xs:h-5 sm:h-6 md:h-8 -mt-4 hidden sm:block pointer-events-none"
                  />
                </h1>
                
                <h2 class="text-[#FFA000] text-lg text-left xs:text-xl sm:text-2xl md:text-3xl font-extrabold mb-4 font-poppins tracking-wide">
                  GROW SMART & WATER WISELY
                </h2>
                
                <p class="text-gray-700 text-left text-xs xs:text-sm sm:text-base font-medium mb-8 font-poppins max-w-full mx-auto lg:mx-0">
                  Your Guide to Precision Agriculture and Sustainability
                </p>

                <!-- Button with improved mobile spacing -->
                <div class="relative inline-block">
                  <button 
                    @click="showAuthModal = true" 
                    class="px-3 sm:px-4 py-2 sm:py-3 rounded-full text-sm xs:text-base sm:text-lg font-bold text-white transition-all duration-300 ease-in-out bg-gradient-to-r from-[#2E7D32] to-[#D4C5A8] hover:shadow-xl hover:scale-105 hover:from-[#1B5E20] hover:to-[#E6D5B8] transform hover:-translate-y-1 flex items-center whitespace-nowrap cursor-pointer z-30 relative"
                    style="pointer-events: auto;"
                  >
                    GET STARTED
                    <span class="ml-2 inline-flex items-center justify-center bg-white rounded-full p-1 h-6 w-6 xs:h-7 xs:w-7 sm:h-8 sm:w-8">
                      <ArrowRight class="h-3 w-3 xs:h-4 xs:w-4 sm:h-5 sm:w-5 text-[#2E7D32]" />
                    </span>
                  </button>
                  <!-- Decorative leaves -->
                  <div class="absolute -top-4 -left-2 animate-pop-scale hidden sm:block pointer-events-none">
                    <img src="/public/images/leaves-plants/leaf-decoration.png" alt="" class="w-5 sm:w-7 h-5 sm:h-7 transform -rotate-45" />
                  </div>
                  <div class="absolute -top-5 left-1/2 -translate-x-1/2 animate-pop-scale hidden sm:block pointer-events-none" style="animation-delay: 0.2s">
                    <img src="/public/images/leaves-plants/leaf-decoration.png" alt="" class="w-5 sm:w-7 h-5 sm:h-7" />
                  </div>
                  <div class="absolute -top-4 -right-2 animate-pop-scale hidden sm:block pointer-events-none" style="animation-delay: 0.4s">
                    <img src="/public/images/leaves-plants/leaf-decoration.png" alt="" class="w-5 sm:w-7 h-5 sm:h-7 transform rotate-45" />
                  </div>
                </div>
              </div>

              <!-- Right Content with Half Circle and Basket -->
              <div class="lg:w-1/2 relative pointer-events-none">
                <div class="relative h-[250px] xs:h-[300px] sm:h-[400px] md:h-[500px] lg:h-[700px] w-full">
                  <div class="absolute right-0 transform translate-x-[15%] bottom-0">
                    <div class="relative">
                      <!-- Half circle with smoother responsive scaling -->
                      <div class="w-[250px] h-[250px] xs:w-[300px] xs:h-[300px] sm:w-[400px] sm:h-[400px] md:w-[500px] md:h-[500px] lg:w-[700px] lg:h-[700px] bg-[#4CAF50] rounded-full transform translate-y-1/2">
                        <!-- Basket image with improved responsive positioning -->
                        <img 
                          src="/public/images/vege-basket.png" 
                          alt="Vegetable Basket" 
                          class="absolute top-[27%] left-1/2 transform -translate-x-1/2 -translate-y-[65%] w-[85%] sm:w-[90%] max-w-[650px] z-20"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>

    <!-- Enhanced Authentication Modal -->
    <Teleport to="body">
      <div v-if="showAuthModal" class="modal-overlay">
        <!-- Backdrop -->
        <div 
          class="modal-backdrop"
          @click="closeModal"
        ></div>
        
        <!-- Modal Container -->
        <div class="modal-container">
          <!-- Close Button -->
          <button 
            @click="closeModal"
            class="modal-close-btn"
          >
            <svg class="w-4 h-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>

          <!-- Modal Content -->
          <div class="modal-content">
            <!-- Icon with gradient background -->
            <div class="modal-icon">
              <div class="modal-icon-bg"></div>
              <div class="modal-icon-main">
                <svg class="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                </svg>
              </div>
            </div>
            
            <!-- Title and Description -->
            <h2 class="modal-title">
              Welcome Back!
            </h2>
            <p class="modal-description">
              Choose how you'd like to continue with Project Israel
            </p>
            
            <!-- Action Buttons -->
            <div class="modal-buttons">
              <!-- Login Button -->
              <button 
                class="modal-btn-primary"
                @click="handleModalAuth('login')"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3v-1m0-4h14"></path>
                </svg>
                <span>Sign In</span>
              </button>
              
              <!-- Register Button -->
              <button 
                class="modal-btn-secondary"
                @click="handleModalAuth('register')"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
                </svg>
                <span>Create Account</span>
              </button>
            </div>

            <!-- Divider -->
            <div class="modal-divider">
              <div class="modal-divider-line"></div>
              <span class="modal-divider-text">OR</span>
              <div class="modal-divider-line"></div>
            </div>

            <!-- Guest Access -->
            <button 
              class="modal-guest-btn"
              @click="closeModal"
            >
              Continue as Guest
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowRight, LockIcon } from 'lucide-vue-next'
// import Footer from '../layout/Footer.vue'
import Navbar from '../layout/Navbar.vue'
// import About from './About.vue'
// import OrganicSection from './OrganicSection.vue'

const router = useRouter()
const isMobile = ref(window.innerWidth < 640)
const transitionKey = ref(0)
const contentStyle = ref({})
const showAuthModal = ref(false)

const beforeLeave = (el) => {
  const { left } = el.getBoundingClientRect()
  el.style.left = left + 'px'
  el.style.position = 'absolute'
}

const enter = (el) => {
  const { left } = el.getBoundingClientRect()
  el.style.left = `${left + 50}px` 
  el.style.opacity = 0
}

const afterEnter = (el) => {
  el.style.left = ''
  el.style.position = ''
  el.style.opacity = ''
}

const handleAuth = (type) => {
  transitionKey.value++
  contentStyle.value = { position: 'relative', left: '0px', transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)' }
  
  setTimeout(() => {
    router.push(`/${type}`)
  }, 500)
}

const handleModalAuth = (type) => {
  closeModal()
  setTimeout(() => {
    handleAuth(type)
  }, 300)
}

const closeModal = () => {
  showAuthModal.value = false
}

onMounted(() => {
  window.addEventListener('resize', () => {
    isMobile.value = window.innerWidth < 640
  })
})

onUnmounted(() => {
  window.removeEventListener('resize', () => {
    isMobile.value = window.innerWidth < 640
  })
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 99999;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-backdrop {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}

.modal-container {
  position: relative;
  width: 100%;
  max-width: 24rem;
  background: white;
  border-radius: 1.5rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
  border: 1px solid rgba(229, 231, 235, 1);
  overflow: hidden;
  z-index: 100000;
}

.modal-close-btn {
  position: absolute;
  top: 1rem;
  right: 1rem;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  background-color: rgba(243, 244, 246, 1);
  transition: background-color 0.2s;
  z-index: 100001;
}

.modal-close-btn:hover {
  background-color: rgba(229, 231, 235, 1);
}

.modal-content {
  padding: 2rem;
  text-align: center;
}

.modal-icon {
  margin-bottom: 1.5rem;
  position: relative;
  margin-left: auto;
  margin-right: auto;
  width: 4rem;
  height: 4rem;
}

.modal-icon-bg {
  position: absolute;
  inset: 0;
  background: linear-gradient(to bottom right, #2E7D32, #4CAF50);
  border-radius: 1rem;
  transform: rotate(3deg);
  opacity: 0.2;
}

.modal-icon-main {
  position: relative;
  width: 100%;
  height: 100%;
  background: linear-gradient(to bottom right, #2E7D32, #4CAF50);
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: rgba(17, 24, 39, 1);
  margin-bottom: 0.75rem;
}

.modal-description {
  color: rgba(75, 85, 99, 1);
  font-size: 0.875rem;
  margin-bottom: 2rem;
  line-height: 1.625;
}

.modal-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.modal-btn-primary {
  width: 100%;
  padding: 1rem 1.5rem;
  background: linear-gradient(to right, #2E7D32, #4CAF50);
  color: white;
  font-weight: 600;
  border-radius: 1rem;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.modal-btn-primary:hover {
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  transform: scale(1.02);
}

.modal-btn-secondary {
  width: 100%;
  padding: 1rem 1.5rem;
  background: white;
  border: 2px solid #2E7D32;
  color: #2E7D32;
  font-weight: 600;
  border-radius: 1rem;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.modal-btn-secondary:hover {
  background: #2E7D32;
  color: white;
  transform: scale(1.02);
}

.modal-divider {
  display: flex;
  align-items: center;
  margin: 1.5rem 0;
}

.modal-divider-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(209, 213, 219, 1), transparent);
}

.modal-divider-text {
  padding: 0 1rem;
  font-size: 0.75rem;
  color: rgba(107, 114, 128, 1);
  font-weight: 500;
}

.modal-guest-btn {
  font-size: 0.875rem;
  color: rgba(107, 114, 128, 1);
  font-weight: 500;
  transition: color 0.3s;
}

.modal-guest-btn:hover {
  color: #2E7D32;
}

/* Navigation Styles */
.nav-link {
  padding: 0.5rem 0;
  font-weight: 500;
  position: relative;
}

.nav-dot {
  position: absolute;
  left: 50%;
  bottom: 0;
  width: 6px;
  height: 6px;
  background-color: #2E7D32;
  border-radius: 9999px;
  transform: translateX(-50%) scale(0);
  transition: transform 0.3s ease-out;
}

.nav-dot.active {
  transform: translateX(-50%) scale(1);
}

/* Base wave styles */
.wave {
  position: absolute;
  width: 200%;
  height: 100%;
  bottom: 0;
  left: 0;
  background-repeat: repeat-x;
  background-position: 0 bottom;
  transform-origin: center bottom;
  will-change: transform;
}

.wave-orange {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 800 88.7' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M800 56.9c-155.5 0-204.9-50-405.5-49.9-200 0-250 49.9-394.5 49.9v31.8h800v-31.8z' fill='%23FFD8A8'/%3E%3C/svg%3E");
  animation: wave-right 8s cubic-bezier(0.36, 0, 0.64, 1) infinite;
  animation-delay: 0s;
  opacity: .8;
  height: 120px;
  z-index: 2;
}

.wave-green {
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 800 88.7' fill='none' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M800 56.9c-155.5 0-204.9-50-405.5-49.9-200 0-250 49.9-394.5 49.9v31.8h800v-31.8z' fill='%23C8E6C9'/%3E%3C/svg%3E");
  animation: wave-left 8s cubic-bezier(0.36, 0, 0.64, 1) infinite;
  animation-delay: -4s;
  opacity: .9;
  height: 140px;
  z-index: 1;
}

@keyframes wave-right {
  0% {
    transform: translateX(0) translateZ(0) scaleY(1);
  }
  50% {
    transform: translateX(-25%) translateZ(0) scaleY(0.98);
  }
  100% {
    transform: translateX(-50%) translateZ(0) scaleY(1);
  }
}

@keyframes wave-left {
  0% {
    transform: translateX(-50%) translateZ(0) scaleY(1);
  }
  50% {
    transform: translateX(-25%) translateZ(0) scaleY(0.98);
  }
  100% {
    transform: translateX(0) translateZ(0) scaleY(1);
  }
}

@keyframes fall {
  0% {
    transform: translateY(-100%) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0;
  }
}

.animate-fall {
  animation: fall linear infinite;
  will-change: transform, opacity;
}

@keyframes pop-scale {
  0% { 
    transform: scale(0.8) rotate(var(--leaf-rotation, 0deg));
    opacity: 0.8;
  }
  50% { 
    transform: scale(1.2) rotate(var(--leaf-rotation, 0deg));
    opacity: 1;
  }
  100% {
    transform: scale(0.8) rotate(var(--leaf-rotation, 0deg));
    opacity: 0.8;
  }
}

.animate-pop-scale {
  animation: pop-scale 2s ease-in-out infinite;
}

/* Mobile Menu Styles */
@media (max-width: 768px) {
  .nav-link {
    padding: 0.5rem 0;
  }
  
  .nav-dot {
    bottom: 0;
  }
}

/* Page transition styles */
.page-transition-enter-active,
.page-transition-leave-active {
  transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute;
  width: 100%;
}

.page-transition-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.page-transition-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Optimize animations for mobile devices */
@media (prefers-reduced-motion: reduce) {
  .animate-fall,
  .animate-pop-scale,
  .wave {
    animation: none;
  }
}

/* Improve performance on mobile */
@media (max-width: 640px) {
  .wave {
    animation-duration: 12s; /* Slower waves on mobile */
  }
  
  .leaf {
    display: none; /* Hide some leaves on mobile for better performance */
  }
}

/* Ensure smooth scaling on different devices */
@media (max-width: 360px) {
  .text-3xl {
    font-size: 1.75rem;
  }
  
  .container {
    padding-left: 2rem;
    padding-right: 2rem;
  }
}

/* Add support for ultra-wide screens */
@media (min-width: 2000px) {
  .container {
    max-width: 1920px;
  }
}
</style>