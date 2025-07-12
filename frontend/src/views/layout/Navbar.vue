<template>
  <nav 
    class="fixed top-0 left-0 right-0 z-[1000] bg-white/95 backdrop-blur-sm shadow-sm font-poppins"
    :style="{ transform: 'translateY(0)' }"
  >
    <div class="max-w-[1920px] w-full mx-auto px-6 sm:px-12 md:px-16 lg:px-24">
      <div class="relative flex justify-between items-center h-16 sm:h-20 md:h-24">
        <!-- Logo -->
        <a href="#" @click.prevent="scrollToSection('home')" class="relative z-[60]">
          <img 
            src="/public/images/logo/logo-wot-text.png"
            alt="Project Israel Logo" 
            class="h-10 w-10 sm:h-18 sm:w-18 md:h-20 md:w-20 transition-transform duration-300 hover:scale-110"
          />
        </a>
        
        <!-- Mobile Menu Button -->
        <button 
          @click="toggleMenu"
          class="lg:hidden z-[60] p-2 text-[#2E7D32]"
          aria-label="Toggle menu"
        >
          <Menu v-if="!isMenuOpen" class="h-6 w-6" />
          <X v-else class="h-6 w-6" />
        </button>

        <!-- Mobile Menu Overlay -->
        <div 
          v-if="isMenuOpen"
          class="fixed inset-0 bg-white/95 backdrop-blur-sm z-[55] lg:hidden flex flex-col items-center justify-center pt-24"
        >
          <div class="flex flex-col items-center space-y-8">
            <a 
              v-for="link in navLinks" 
              :key="link.name"
              href="#"
              @click.prevent="scrollToSection(link.section)"
              class="nav-link group relative text-xl"
            >
              <span :class="currentSection === link.section ? 'text-[#1B5E20] font-bold' : 'text-[#2E7D32] hover:text-[#1B5E20]'">
                {{ link.name }}
              </span>
              <span :class="['nav-dot', currentSection === link.section && 'active']"></span>
            </a>
          </div>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden lg:flex items-center space-x-7">
          <a
            v-for="link in navLinks"
            :key="link.name"
            href="#"
            @click.prevent="scrollToSection(link.section)"
            class="nav-link group relative px-3 py-2"
          >
            <span :class="currentSection === link.section ? 'text-[#1B5E20] font-bold' : 'text-[#2E7D32] hover:text-[#1B5E20]'">
              {{ link.name }}
            </span>
            <span :class="['nav-dot', currentSection === link.section && 'active']"></span>
          </a>
        </div>

        <!-- Desktop Auth Buttons -->
        <div class="hidden lg:flex gap-7 items-center pr-10">
          <button 
            @click="$emit('auth', 'login')"
            class="px-6 py-2 rounded-full text-[#2E7D32] border-2 border-[#2E7D32] hover:bg-[#2E7D32] hover:text-white transition-colors duration-300 font-medium"
          >
            Login
          </button>
          <button 
            @click="$emit('auth', 'register')"
            class="px-6 py-2 rounded-full bg-[#2E7D32] text-white hover:bg-[#1B5E20] transition-colors duration-300 font-medium"
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