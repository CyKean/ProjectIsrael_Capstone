<template>
  <nav 
    class="fixed top-0 left-0 right-0 z-[1000] bg-white/95 backdrop-blur-sm shadow-sm font-poppins"
    :style="{ transform: 'translateY(0)' }"
  >
    <div class="max-w-[1920px] w-full mx-auto px-4 sm:px-6 md:px-8 lg:px-12 xl:px-24 2xl:px-32">
      <div class="relative flex justify-between items-center h-14 sm:h-16 md:h-20">
        <!-- Logo -->
        <a href="#" @click.prevent="scrollToSection('home')" class="relative z-[60]">
          <img 
            src="/public/images/logo/logo-wot-text.png"
            alt="Project Israel Logo" 
            class="h-8 w-8 sm:h-10 sm:w-10 md:h-12 md:w-12 transition-transform duration-300 hover:scale-110"
          />
        </a>
        
        <!-- Mobile Menu Button -->
        <button 
          @click="toggleMenu"
          class="lg:hidden z-[60] p-2 text-[#2E7D32] focus:outline-none transition-all duration-200"
          aria-label="Toggle menu"
          :aria-expanded="isMenuOpen"
        >
          <Menu v-if="!isMenuOpen" class="h-5 w-5 sm:h-6 sm:w-6 transition-transform duration-200" />
          <X v-else class="h-5 w-5 sm:h-6 sm:w-6 transition-transform duration-200" />
        </button>

        <!-- Mobile Menu Dropdown Container -->
        <transition
          enter-active-class="transition-all duration-300 ease-out"
          leave-active-class="transition-all duration-200 ease-in"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div 
            v-if="isMenuOpen"
            class="fixed top-20 right-4 z-[55] lg:hidden bg-white rounded-xl shadow-lg border border-gray-100 overflow-hidden w-64"
          >
            <div class="flex flex-col py-2 w-full">
              <a 
                v-for="link in navLinks" 
                :key="link.name"
                href="#"
                @click.prevent="scrollToSection(link.section); isMenuOpen = false"
                class="nav-link group relative w-full text-left py-3 px-4 transition-all duration-200"
                :class="currentSection === link.section 
                  ? 'bg-[#1B5E20]/10 text-[#1B5E20] font-semibold' 
                  : 'text-[#2E7D32] hover:bg-[#2E7D32]/10 hover:text-[#1B5E20]'"
              >
                <span class="text-base flex items-center">
                  {{ link.name }}
                  <span 
                    class="ml-2 h-1.5 w-1.5 rounded-full bg-[#1B5E20] transition-all duration-200"
                    :class="currentSection === link.section ? 'opacity-100' : 'opacity-0 group-hover:opacity-50'"
                  ></span>
                </span>
              </a>
            </div>
            
            <!-- Mobile Auth Buttons -->
            <div class="border-t border-gray-100 px-4 py-3 bg-gray-50">
              <button 
                @click="$emit('auth', 'login'); isMenuOpen = false"
                class="w-full px-4 py-2 rounded-lg text-[#2E7D32] border border-[#2E7D32] hover:bg-[#2E7D32] hover:text-white transition-all duration-200 font-medium text-sm flex items-center justify-center mb-2"
              >
                Login
              </button>
              <button 
                @click="$emit('auth', 'register'); isMenuOpen = false"
                class="w-full px-4 py-2 rounded-lg bg-[#2E7D32] text-white hover:bg-[#1B5E20] transition-all duration-200 font-medium text-sm flex items-center justify-center"
              >
                Sign up
              </button>
            </div>
          </div>
        </transition>

        <!-- Desktop Navigation -->
        <div class="hidden lg:flex items-center space-x-2 xl:space-x-4">
          <a
            v-for="link in navLinks"
            :key="link.name"
            href="#"
            @click.prevent="scrollToSection(link.section)"
            class="nav-link group relative px-3 py-2 rounded-lg transition-all duration-200"
            :class="currentSection === link.section 
              ? 'text-[#1B5E20] font-semibold' 
              : 'text-[#2E7D32] hover:text-[#1B5E20] hover:bg-[#2E7D32]/10'"
          >
            <span class="text-sm xl:text-base">
              {{ link.name }}
            </span>
            <span 
              class="absolute bottom-0 left-1/2 transform -translate-x-1/2 h-0.5 w-4 bg-[#1B5E20] transition-all duration-200"
              :class="currentSection === link.section ? 'opacity-100' : 'opacity-0 group-hover:opacity-50'"
            ></span>
          </a>
        </div>

        <!-- Desktop Auth Buttons -->
        <div class="hidden lg:flex gap-3 xl:gap-4 items-center">
          <button 
            @click="$emit('auth', 'login')"
            class="px-4 py-1.5 xl:px-5 xl:py-2 rounded-full text-[#2E7D32] border-2 border-[#2E7D32] hover:bg-[#2E7D32] hover:text-white transition-all duration-200 font-medium text-sm xl:text-base hover:shadow-md"
          >
            Login
          </button>
          <button 
            @click="$emit('auth', 'register')"
            class="px-4 py-1.5 xl:px-5 xl:py-2 rounded-full bg-[#2E7D32] text-white hover:bg-[#1B5E20] transition-all duration-200 font-medium text-sm xl:text-base hover:shadow-md"
          >
            Sign up
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Menu, X } from 'lucide-vue-next'

const emit = defineEmits(['auth'])
const isMenuOpen = ref(false)
const currentSection = ref('home')

// const navLinks = [
//   { name: 'HOME', section: 'home' },
//   { name: 'ABOUT', section: 'about' },
//   { name: 'CROPS', section: 'crops' }
// ]

const scrollToSection = (sectionId) => {
  const element = document.querySelector(`.${sectionId}-section`)
  if (element) {
    const navbarHeight = 80
    const elementPosition = element.getBoundingClientRect().top
    const offsetPosition = elementPosition + window.pageYOffset - navbarHeight

    window.scrollTo({
      top: offsetPosition,
      behavior: 'smooth'
    })

    currentSection.value = sectionId
  }
  closeMenu()
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const handleScroll = () => {
  const sections = ['home', 'about', 'crops']
  const navbarHeight = 80
  let closestSection = null
  let minDistance = Infinity

  sections.forEach(section => {
    const element = document.querySelector(`.${section}-section`)
    if (element) {
      const rect = element.getBoundingClientRect()
      const distance = Math.abs(rect.top - navbarHeight)
      
      if (distance < minDistance) {
        minDistance = distance
        closestSection = section
      }
    }
  })

  if (closestSection) {
    currentSection.value = closestSection
  }
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll() // Initialize current section
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

body {
  font-family: 'Poppins', sans-serif;
}

nav {
  will-change: transform;
  transform: translateY(0) !important;
  transition: none !important; /* Remove any transitions that might cause hiding */
}

.nav-link {
  position: relative;
  transition: color 0.3s ease;
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

@media (max-width: 1023px) {
  .nav-link {
    padding: 0.75rem 0;
  }
}
</style>