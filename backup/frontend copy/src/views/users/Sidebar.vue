<template>
  <div class="hidden md:flex md:flex-shrink-0 relative z-50">
    <div :class="[
      'flex flex-col bg-[#002B1D] transition-all duration-300 ease-in-out rounded-tr-3xl rounded-br-3xl relative h-screen',
      isCollapsed ? 'w-20' : 'w-[280px]'
    ]">
      <!-- Logo Section -->
      <router-link to="/profile" class="block">
        <div class="flex flex-col items-center px-6 py-4 border-b border-[#1a4d4f]">
          <div :class="['flex items-center justify-center transition-all duration-300', isCollapsed ? 'w-12 h-12' : 'w-20 h-20']">
            <img 
              src="/images/project-israel-logo-removebg-preview.png" 
              alt="Project Israel" 
              class="w-full h-full object-contain"
            />
          </div>
          <span class="text-white text-xl font-semibold mt-2" :class="[isCollapsed ? 'hidden' : 'block']">
            Project Israel
          </span>
        </div>
      </router-link>

      <!-- Toggle Button -->
      <button 
        @click="toggleSidebar"
        class="absolute -right-12 top-12 px-4 py-3 rounded-lg bg-[#002B1D] hover:bg-[#1a4d4f] text-gray-300 hover:text-[#8FE3CF] transition-colors shadow-lg z-50"
      >
        <Menu v-if="isCollapsed" class="h-5 w-5" />
        <PanelLeftClose v-else class="h-5 w-5" />
      </button>

      <!-- Navigation -->
      <nav class="flex-1 px-4 py-6 flex flex-col justify-between">
        <div>
          <div v-show="!isCollapsed" class="mb-6">
            <h3 class="text-sm font-semibold text-gray-400 uppercase tracking-wider px-2">
              MENU
            </h3>
          </div>
          
          <div class="space-y-2">
            <!-- Main Menu Items with Tooltips -->
            <div v-for="item in menuItems" 
                 :key="item.name" 
                 class="relative group"
            >
              <router-link 
                :to="item.href"
                :class="[
                  'flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-150',
                  isCollapsed ? 'justify-center' : '',
                  isCurrentRoute(item.href) ? 'bg-[#1a4d4f] text-white' : 'text-gray-300 hover:bg-[#1a4d4f] hover:text-white'
                ]"
              >
                <component 
                  :is="item.icon" 
                  :class="[
                    'flex-shrink-0 h-5 w-5',
                    isCurrentRoute(item.href) ? 'text-[#8FE3CF]' : 'text-gray-400 group-hover:text-[#8FE3CF]'
                  ]"
                />
                <span 
                  :class="['ml-4 transition-opacity duration-300', isCollapsed ? 'hidden' : 'block']"
                >
                  {{ item.name }}
                </span>
              </router-link>
              <!-- Tooltip -->
              <div
                v-if="isCollapsed"
                class="absolute left-full ml-2 px-3 py-2 bg-[#1a4d4f] text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50"
                style="top: 50%; transform: translateY(-50%);"
              >
                {{ item.name }}
              </div>
            </div>

            <!-- Sensor Data Section -->
            <div class="relative group">
              <button 
                @click="toggleSensorDropdown"
                :class="[
                  'w-full flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-150',
                  isSensorDropdownOpen || isInSensorRoutes ? 'bg-[#1a4d4f] text-white' : 'text-gray-300 hover:bg-[#1a4d4f] hover:text-white'
                ]"
              >
                <Database class="flex-shrink-0 h-5 w-5 text-gray-400 group-hover:text-[#8FE3CF]" />
                <span :class="['ml-4', isCollapsed ? 'hidden' : 'block']">Sensor Data</span>
                <ChevronDown 
                  v-if="!isCollapsed"
                  :class="['ml-auto h-5 w-5 transition-transform', isSensorDropdownOpen || isInSensorRoutes ? 'transform rotate-180' : '']"
                />
              </button>
              <!-- Tooltip for Sensor Data -->
              <div
                v-if="isCollapsed"
                class="absolute left-full ml-2 px-3 py-2 bg-[#1a4d4f] text-white text-sm rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 whitespace-nowrap z-50"
                style="top: 50%; transform: translateY(-50%);"
              >
                Sensor Data
              </div>

              <!-- Dropdown Content -->
              <div 
                v-show="!isCollapsed && (isSensorDropdownOpen || isInSensorRoutes)"
                class="mt-2 ml-4 space-y-1"
              >
                <router-link 
                  v-for="sensor in sensorTypes" 
                  :key="sensor.name"
                  :to="sensor.href"
                  :class="[
                    'flex items-center px-4 py-2 text-sm rounded-lg transition-colors duration-150',
                    isCurrentRoute(sensor.href) 
                      ? 'bg-[#1a4d4f] text-white' 
                      : 'text-gray-300 hover:bg-[#1a4d4f] hover:text-white'
                  ]"
                >
                  <component 
                    :is="sensor.icon" 
                    :class="[
                      'flex-shrink-0 h-4 w-4 mr-3',
                      isCurrentRoute(sensor.href) ? 'text-[#8FE3CF]' : 'text-gray-400'
                    ]"
                  />
                  {{ sensor.name }}
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </nav>

      <!-- Profile Section -->
      <div class="border-t border-[#1a4d4f] p-4">
        <div class="flex items-center gap-3">
          <div class="flex-shrink-0">
            <img 
              src="/images/profile-example.jpg" 
              class="w-10 h-10 rounded-full object-cover border-2 border-[#1a4d4f]" 
              alt="Profile" 
            />
          </div>
          <div v-if="!isCollapsed" class="flex-1 min-w-0">
            <p class="text-sm font-medium text-white truncate">John Doe</p>
            <p class="text-xs text-gray-400 truncate">Farmer</p>
          </div>
          <router-link 
            v-if="!isCollapsed"
            to="/profile" 
            class="p-2 rounded-lg hover:bg-[#1a4d4f] text-gray-300 hover:text-[#8FE3CF] transition-colors"
          >
            <Settings class="h-5 w-5" />
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { 
  LayoutDashboard,
  Brain,
  Cpu,
  Database,
  Sprout,
  Menu,
  PanelLeftClose,
  ChevronDown,
  Settings,
  Droplets,
  Thermometer,
  Gauge,
  Power
} from 'lucide-vue-next'

const route = useRoute()
const isCollapsed = ref(false)
const isSensorDropdownOpen = ref(false)

const menuItems = [
  { name: 'Overview', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Crop Prediction', href: '/prediction', icon: Brain },
  { name: 'Device Control', href: '/control', icon: Cpu },
  { name: 'Soil Analysis', href: '/soil', icon: Sprout },
]

const sensorTypes = [
  { name: 'Soil Moisture', href: '/soil-moisture', icon: Droplets },
  { name: 'Water Level', href: '/water-level', icon: Gauge },
  { name: 'Humidity', href: '/humidity', icon: Droplets },
  { name: 'Temperature', href: '/temperature', icon: Thermometer },
  { name: 'Motor Control', href: '/motor-control', icon: Power },
]

const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value
  if (isCollapsed.value) {
    isSensorDropdownOpen.value = false
  }
}

const toggleSensorDropdown = () => {
  isSensorDropdownOpen.value = !isSensorDropdownOpen.value
}

const isCurrentRoute = (path) => {
  return route.path === path
}

const isInSensorRoutes = computed(() => {
  return sensorTypes.some(sensor => route.path === sensor.href)
})

// Keep dropdown open when navigating to sensor routes
watch(() => route.path, (newPath) => {
  if (sensorTypes.some(sensor => sensor.href === newPath)) {
    isSensorDropdownOpen.value = true
  }
})
</script>

<style scoped>
/* Smooth transitions */
.router-link-active {
  position: relative;
}

.router-link-active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 2px;
  background-color: #8FE3CF;
  transform: scaleX(0);
  transition: transform 0.2s ease;
}

.router-link-active:hover::after {
  transform: scaleX(1);
}
</style>