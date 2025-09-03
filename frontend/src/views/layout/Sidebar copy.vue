<template>
  <nav class="fixed top-2 mx-1 left-0 right-0 bg-gradient-to-r from-[#00A572] to-[#008F61] backdrop-blur-md bg-opacity-95 shadow-lg z-50 rounded-xl border border-transparent border-t-[3px] border-t-orange-400">
    <div class="max-w-[1920px] mx-auto px-4 lg:px-6 py-2.5">
      <!-- Top row with logo and profile -->
      <div class="flex items-center justify-between">
        <!-- Logo and PROJECT ISRAEL text -->
        <div class="flex items-center relative w-[180px]">
          <div class="bg-white rounded-full shadow-lg flex items-center justify-center overflow-hidden border-2 border-white/30 hover:border-white/50 transition-all duration-300" style="width: 2.8rem; height: 2.8rem;">
            <img
              src="/public/images/logo/logo-wot-text.png"
              alt="Project Israel"
              class="w-8 h-8 object-cover transform scale-[1.3] hover:scale-[1.8] transition-all duration-500 ease-out"
              style="transform-origin: center;"
            />
          </div>
          <div class="ml-2.5 flex flex-col">
            <span class="text-white font-bold text-sm leading-tight">PROJECT</span>
            <span class="text-orange-400 font-bold text-sm leading-tight">ISRAEL</span>
          </div>
        </div>

        <!-- Mobile menu button (hidden on larger screens) -->
        <div class="md:hidden flex items-center">
          <button
            @click="toggleMobileMenu"
            class="inline-flex items-center justify-center p-2 rounded-md text-white hover:text-white hover:bg-white/10 focus:outline-none transition duration-150 ease-in-out"
            aria-label="Toggle menu"
          >
            <svg
              class="h-6 w-6"
              :class="{ 'hidden': isMobileMenuOpen, 'block': !isMobileMenuOpen }"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg
              class="h-6 w-6"
              :class="{ 'hidden': !isMobileMenuOpen, 'block': isMobileMenuOpen }"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <!-- User Profile Section - Hidden on mobile -->
        <div class="hidden md:flex items-center group w-[180px] justify-end">
          <span class="text-xs text-white mr-2 opacity-90 group-hover:opacity-100 transition-opacity">{{ user?.email }}</span>

          <!-- WiFi Connection Status -->
          <div class="relative mr-2">
            <button
              class="relative flex items-center justify-center h-7 w-7 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-300"
              @mouseenter="showWifiTooltip = true"
              @mouseleave="showWifiTooltip = false"
            >
              <div class="flex items-center justify-center size-full rounded-full" :class="wifiStrength > 0 ? 'bg-green-500/20' : ''">
                <Wifi class="h-3.5 w-3.5 text-white" />
              </div>
            </button>

            <!-- WiFi Tooltip -->
            <div
              v-show="showWifiTooltip"
              class="absolute right-0 top-full mt-2 w-52 bg-white/95 backdrop-blur-md rounded-lg shadow-lg overflow-hidden z-50 transition-all duration-200 border border-gray-100 transform origin-top-right"
              :class="showWifiTooltip ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
            >
              <div class="p-3">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center">
                    <div class="w-2 h-2 rounded-full mr-2" :class="wifiStrength > 0 ? 'bg-green-500' : 'bg-red-500'"></div>
                    <h3 class="font-medium text-sm text-gray-800">WiFi Status</h3>
                  </div>
                  <Wifi class="h-4 w-4 text-[#00A572]" />
                </div>

                <div v-if="wifiStrength > 0" class="space-y-2.5">
                  <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-500">Network</span>
                    <span class="font-medium text-gray-800">{{ wifiNetwork }}</span>
                  </div>

                  <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-500">IP Address</span>
                    <span class="font-medium text-gray-800">{{ ipAddress }}</span>
                  </div>

                  <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-500">Signal</span>
                    <span class="font-medium text-gray-800">{{ wifiStrength }}%</span>
                  </div>

                  <!-- Signal Strength Bar -->
                  <div class="mt-1.5">
                    <div class="w-full h-1 bg-gray-100 rounded-full overflow-hidden">
                      <div
                        class="h-full rounded-full transition-all duration-500 ease-out"
                        :class="getSignalStrengthClass(wifiStrength)"
                        :style="{ width: `${wifiStrength}%` }"
                      ></div>
                    </div>
                  </div>
                </div>

                <div v-else class="flex items-center justify-center py-2">
                  <span class="text-xs text-red-500 font-medium">Disconnected</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Recalibration Button -->
          <div class="relative mr-2">
            <button
              @click="goToRecalibration"
              class="relative flex items-center justify-center h-7 w-7 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-300"
              :class="$route.path === '/app/recalibration' ? 'bg-white/30' : ''"
              @mouseenter="showRecalibrationTooltip = true"
              @mouseleave="showRecalibrationTooltip = false"
            >
              <div class="flex items-center justify-center size-full rounded-full" :class="$route.path === '/recalibration' ? 'bg-green-500/20' : ''">
                <Cog class="h-3.5 w-3.5 text-white" />
              </div>
            </button>

            <!-- Recalibration Tooltip -->
            <div
              v-show="showRecalibrationTooltip"
              class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 bg-green-100 text-green-800 text-[10px] font-medium rounded-md whitespace-nowrap z-50 transition-all duration-200 shadow-sm"
              :class="showRecalibrationTooltip ? 'opacity-100' : 'opacity-0'"
            >
              Recalibration
              <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-green-100"></div>
            </div>
          </div>

          <!-- Notification Icon -->
          <div class="relative">
            <router-link
              to="/app/notifications"
              class="relative flex items-center justify-center h-8 w-8 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-300 text-white group/bell"
              :class="{ 'bg-white/30': $route.path === '/notifications' }"
              @mouseenter="showNotificationTooltip = true"
              @mouseleave="showNotificationTooltip = false"
            >
              <Bell class="h-4 w-4 transition-transform duration-200 group-hover/bell:scale-110" />

              <!-- Notification Badge -->
              <div
                v-if="unreadNotificationCount > 0"
                class="notification-badge-static absolute -top-1 -right-1 min-w-[16px] h-4 flex items-center justify-center rounded-full bg-red-500 text-white shadow-md border border-white/30"
              >
                <span class="text-[9px] font-semibold leading-none px-0.5">
                  {{ unreadNotificationCount > 99 ? '99+' : unreadNotificationCount }}
                </span>
              </div>
            </router-link>

            <!-- Notification Tooltip -->
            <div
              v-show="showNotificationTooltip"
              class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 bg-green-100 text-green-900 font-medium text-[10px] rounded-md whitespace-nowrap z-50 transition-all duration-200 shadow-sm"
              :class="showNotificationTooltip ? 'opacity-100' : 'opacity-0'"
            >
              Notifications
              <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-green-100"></div>
            </div>
          </div>

          <!-- Profile Button -->
          <div class="relative ml-4">
            <button
              class="relative cursor-pointer group/profile"
              @click="goToProfile"
              @mouseenter="showProfileTooltip = true"
              @mouseleave="showProfileTooltip = false"
            >
              <div class="relative">
                <div
                  class="w-8 h-8 rounded-full overflow-hidden transition-all duration-300 ease-out group-hover/profile:scale-[1.02]"
                  :class="[
                    isOnProfilePage
                      ? 'ring-1 ring-green-400/60 ring-offset-1 ring-offset-white/20'
                      : 'ring-1 ring-white/15 hover:ring-white/25',
                    user?.avatar?.icon ? 'bg-white flex items-center justify-center' : ''
                  ]"
                >
                  <span v-if="user?.avatar?.icon" class="text-lg leading-none select-none">{{ user.avatar.icon }}</span>
                  <img v-else-if="user?.profilePicture"
                       :src="user.profilePicture"
                       class="w-full h-full object-cover transition-all duration-300"
                       :class="isOnProfilePage ? 'brightness-[1.02] saturate-[1.05]' : ''"
                       alt="Profile"/>
                  <img v-else
                       src="/public/images/profile.jpg"
                       class="w-full h-full object-cover transition-all duration-300"
                       alt="Profile"/>

                  <div
                    v-if="isOnProfilePage"
                    class="absolute inset-0 bg-gradient-to-br from-green-400/8 via-transparent to-transparent"
                  ></div>
                </div>

                <!-- Active Indicator -->
                <div
                  v-if="isOnProfilePage"
                  class="absolute -bottom-px -right-px w-2 h-2 bg-green-400 rounded-full border border-white/40 shadow-sm"
                ></div>
              </div>

              <!-- Profile Tooltip -->
              <div
                v-show="showProfileTooltip"
                class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 bg-green-100 text-green-800 text-[10px] font-medium rounded-md whitespace-nowrap z-50 transition-all duration-200 shadow-sm"
                :class="showProfileTooltip ? 'opacity-100' : 'opacity-0'"
              >
                Profile
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-green-100"></div>
              </div>
            </button>
          </div>
        </div>
      </div>

      <!-- Navigation items - Desktop version (always shown on desktop) -->
      <div class="hidden md:flex items-center justify-center mt-1.5">
        <div class="flex items-center space-x-1 sm:space-x-2 md:space-x-3 flex-wrap gap-y-1">
          <router-link
            v-for="item in menuItems"
            :key="item.name"
            :to="item.href"
            :class="[
              'flex items-center px-2.5 sm:px-3 py-1.5 text-xs sm:text-sm font-medium rounded-lg transition-all duration-300 hover:scale-105',
              isCurrentRoute(item.href)
                ? 'bg-white text-[#00A572] shadow-md'
                : 'text-white hover:bg-white/10 hover:shadow-sm'
            ]"
          >
            <component
              :is="item.icon"
              class="h-3.5 w-3.5 mr-1.5 transition-transform duration-300 group-hover:rotate-12"
            />
            <span class="whitespace-nowrap">{{ item.name }}</span>
          </router-link>

          <div class="relative group">
            <button
              @click="toggleSensorDropdown"
              :class="[
                'flex items-center px-2.5 sm:px-3 py-1.5 text-xs sm:text-sm font-medium rounded-lg transition-all duration-300 hover:scale-105',
                isSensorDropdownOpen || isInSensorRoutes
                  ? 'bg-white text-[#00A572] shadow-md'
                  : 'text-white hover:shadow-sm hover:bg-white/10'
              ]"
            >
              <Database class="h-3.5 w-3.5 mr-1.5" />
              <span class="whitespace-nowrap">Sensor Data</span>
              <ChevronDown
                :class="['ml-1.5 h-3 w-3 transition-transform duration-300',
                  isSensorDropdownOpen ? 'transform rotate-180' : ''
                ]"
              />
            </button>
            <div
              v-show="isSensorDropdownOpen"
              class="absolute top-full left-0 mt-1 w-52 bg-white/95 backdrop-blur-md rounded-lg shadow-lg py-1.5 dropdown-link border border-white/20 transform transition-all duration-300 z-[9999]"
            >
              <router-link
                v-for="sensor in sensorTypes"
                :key="sensor.name"
                :to="sensor.href"
                :class="[
                  'flex items-center px-3 py-1.5 text-sm transition-all duration-200 hover:scale-[1.02]',
                  isCurrentRoute(sensor.href)
                    ? 'bg-[#E8F5E9] text-[#00A572] font-medium'
                    : 'text-gray-700 hover:bg-[#E8F5E9] hover:text-[#00A572]'
                ]"
              >
                <component :is="sensor.icon" class="h-3.5 w-3.5 mr-2" />
                {{ sensor.name }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile Navigation Dropdown (shown only when mobile menu is open) -->
      <Transition name="slide-down">
        <div v-if="isMobileMenuOpen" class="md:hidden mt-1.5">
          <div class="flex flex-col space-y-1 max-h-[70vh] overflow-y-auto">
            <!-- Main Navigation Links -->
            <router-link
              v-for="item in menuItems"
              :key="item.name"
              :to="item.href"
              :class="[
                'flex items-center px-2.5 py-1.5 text-sm font-medium rounded-lg transition-all duration-300',
                isCurrentRoute(item.href)
                  ? 'bg-white text-[#00A572] shadow-md'
                  : 'text-white hover:bg-white/10 hover:shadow-sm'
              ]"
              @click="isMobileMenuOpen = false"
            >
              <component :is="item.icon" class="h-3.5 w-3.5 mr-1.5" />
              <span class="whitespace-nowrap">{{ item.name }}</span>
            </router-link>

            <!-- Sensor Data Dropdown -->
            <div class="relative group">
              <button
                @click="toggleSensorDropdown"
                :class="[
                  'flex items-center px-2.5 py-1.5 text-sm font-medium rounded-lg transition-all duration-300',
                  isSensorDropdownOpen || isInSensorRoutes
                    ? 'bg-white text-[#00A572] shadow-md'
                    : 'text-white hover:shadow-sm hover:bg-white/10'
                ]"
              >
                <Database class="h-3.5 w-3.5 mr-1.5" />
                <span class="whitespace-nowrap">Sensor Data</span>
                <ChevronDown
                  :class="['ml-1.5 h-3 w-3 transition-transform duration-300',
                    isSensorDropdownOpen ? 'transform rotate-180' : ''
                  ]"
                />
              </button>
              
              <!-- Sensor Data Dropdown Content -->
              <Transition name="slide-down">
                <div
                  v-if="isSensorDropdownOpen"
                  class="mt-1 w-full bg-white/95 backdrop-blur-md rounded-lg shadow-lg py-1.5 border border-white/20"
                >
                  <div class="max-h-[200px] overflow-y-auto">
                    <router-link
                      v-for="sensor in sensorTypes"
                      :key="sensor.name"
                      :to="sensor.href"
                      :class="[
                        'flex items-center px-3 py-1.5 text-sm transition-all duration-200 hover:scale-[1.02]',
                        isCurrentRoute(sensor.href)
                          ? 'bg-[#E8F5E9] text-[#00A572] font-medium'
                          : 'text-gray-700 hover:bg-[#E8F5E9] hover:text-[#00A572]'
                      ]"
                      @click="isMobileMenuOpen = false; isSensorDropdownOpen = false"
                    >
                      <component :is="sensor.icon" class="h-3.5 w-3.5 mr-2" />
                      {{ sensor.name }}
                    </router-link>
                  </div>
                </div>
              </Transition>
            </div>

            <!-- Profile Section for Mobile -->
            <div class="pt-2 border-t border-white/10 mt-2">
              <div class="flex items-center justify-between px-2.5 py-1.5">
                <span class="text-xs text-white opacity-90">{{ user?.email }}</span>
              </div>

              <!-- WiFi Connection Status -->
              <button
                @click="goToWifi"
                class="flex items-center w-full px-2.5 py-1.5 text-sm font-medium rounded-lg transition-all duration-300 text-white hover:bg-white/10 hover:shadow-sm"
              >
                <div class="flex items-center justify-center size-7 rounded-full mr-1.5" :class="wifiStrength > 0 ? 'bg-green-500/20' : ''">
                  <Wifi class="h-3.5 w-3.5 text-white" />
                </div>
                <span class="whitespace-nowrap">WiFi Status</span>
                <span class="ml-auto text-xs" :class="wifiStrength > 0 ? 'text-green-400' : 'text-red-400'">
                  {{ wifiStrength > 0 ? `${wifiStrength}%` : 'Disconnected' }}
                </span>
              </button>

              <!-- Recalibration Button -->
              <button
                @click="goToRecalibration"
                class="flex items-center w-full px-2.5 py-1.5 text-sm font-medium rounded-lg transition-all duration-300 text-white hover:bg-white/10 hover:shadow-sm"
                :class="{ 'bg-white/10': $route.path === '/(link of the calibration link)' }"
              >
                <div class="flex items-center justify-center size-7 rounded-full mr-1.5" :class="$route.path === '/recalibration' ? 'bg-green-500/20' : ''">
                  <Cog class="h-3.5 w-3.5 text-white" />
                </div>
                <span class="whitespace-nowrap">Recalibration</span>
              </button>

              <!-- Notification Button -->
              <router-link
                to="/app/notifications"
                class="flex items-center w-full px-2.5 py-1.5 text-sm font-medium rounded-lg transition-all duration-300 text-white hover:bg-white/10 hover:shadow-sm"
                :class="{ 'bg-white/10': $route.path === '/notifications' }"
                @click="isMobileMenuOpen = false"
              >
                <div class="relative flex items-center justify-center size-7 rounded-full mr-1.5">
                  <Bell class="h-3.5 w-3.5 text-white" />
                  <div
                    v-if="unreadNotificationCount > 0"
                    class="absolute -top-1 -right-1 min-w-[14px] h-3.5 flex items-center justify-center rounded-full bg-red-500 text-white text-[8px] px-0.5"
                  >
                    {{ unreadNotificationCount > 99 ? '99+' : unreadNotificationCount }}
                  </div>
                </div>
                <span class="whitespace-nowrap">Notifications</span>
              </router-link>

              <!-- Profile Button -->
              <button
                @click="goToProfile"
                class="flex items-center w-full px-2.5 py-1.5 text-sm font-medium rounded-lg transition-all duration-300 text-white hover:bg-white/10 hover:shadow-sm"
                :class="{ 'bg-white/10': isOnProfilePage }"
              >
                <div class="relative size-7 rounded-full overflow-hidden mr-1.5">
                  <span v-if="user?.avatar?.icon" class="flex items-center justify-center size-full text-lg">{{ user.avatar.icon }}</span>
                  <img v-else-if="user?.profilePicture"
                       :src="user.profilePicture"
                       class="w-full h-full object-cover"
                       alt="Profile"/>
                  <img v-else
                       src="/public/images/profile.jpg"
                       class="w-full h-full object-cover"
                       alt="Profile"/>
                </div>
                <span class="whitespace-nowrap">Profile</span>
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </nav>

  <!-- Spacer for content below navbar -->
  <div class="h-20"></div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick, provide } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  LayoutDashboard,
  Brain,
  Cpu,
  Database,
  Sprout,
  ChevronDown,
  Droplets,
  Thermometer,
  Gauge,
  Power,
  Cloud,
  Bell,
  BellOff,
  Wifi,
  Zap,
  Check,
  AlertCircle,
  Leaf,
  BarChart,
  Cog,
  Beaker,
  CheckCircle,
  Info,
  AlertTriangle,
  XCircle,
  X,
  CloudLightning
} from 'lucide-vue-next'
import { sendPushNotification } from '../../utils/notify.js'
import { initWaterStream, onWaterLevelUpdate } from '../../utils/water.js'
import { getWeatherData, mapWeatherCode } from '../../utils/weather.js'
import api from '../../api/index.js'
import { useUserStore } from '../../utils/user.js'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore();
const user = computed(() => userStore.user)
const isSensorDropdownOpen = ref(false)
const isProfileDropdownOpen = ref(false)
const showWifiTooltip = ref(false)
const showWebSocketTooltip = ref(false)
const showRecalibrationTooltip = ref(false)
const showNotificationTooltip = ref(false)
const showProfileTooltip = ref(false)
const showNotifications = ref(false)
const wifiStrength = ref(100)
const wifiNetwork = ref('Unknown')
const ipAddress = ref('')
const notifications = ref([])
const waterLevel = ref(0);
const savedSchedules = ref([])
const showToast = ref(false)
const toastMessage = ref('')
const toastSeverity = ref('info')
const toastTimeout = ref(null)
const toastQueue = ref([]);
const isToastActive = ref(false);
const processingScheduleIds = ref(new Set());
let unsubscribeUserListener = null;
let unsubscribeSoilMoisture = null;
let unsubscribeFunctions = []
const schedulesCache = ref([]);
const scheduleTimers = ref({});
const unsubscribeSchedules = ref(null);
const scheduleCheckInterval = ref(null);
const activeSchedules = ref({});
const activeSystemSchedules = ref({}); 
const immediateCheckTimeout = ref(null);
const lastProcessedScheduleTimes = ref({});
const activeWateringSchedules = ref({});
const lastNotificationDates = ref({});
const notificationHistory = ref({}); // Tracks notifications by day
const notificationCooldowns = ref(new Map()); 
const toastMessagesShown = ref({});

const toastHistory = ref({});


// Reactive state
const isMobileMenuOpen = ref(false);
const isMobile = ref(window.innerWidth < 768);

// Add these near your other refs
const sentNotifications = ref(new Set());
const processingNotifications = ref(new Set());

// Methods
const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value;
  if (isMobileMenuOpen.value) {
    isSensorDropdownOpen.value = false;
  }
};

const closeMobileMenu = () => {
  if (isMobile.value) {
    isMobileMenuOpen.value = false;
  }
};

const closeMobileMenuAndDropdown = () => {
  isMobileMenuOpen.value = false;
  isSensorDropdownOpen.value = false;
};

// Helper function to generate unique notification IDs
const generateNotificationId = (type, identifier) => {
  return `${type}-${identifier}`;
};

// Utility Functions
const truncateText = (text, maxLength) => {
  if (!text) return '';
  return text.length <= maxLength ? text : text.substring(0, maxLength) + '...';
};

const getSignalStrengthClass = (strength) => {
  if (strength >= 70) return 'bg-green-500'
  if (strength >= 40) return 'bg-yellow-500'
  return 'bg-red-500'
}

const isCurrentRoute = (path) => route.path === path
const isInSensorRoutes = computed(() => sensorTypes.some(sensor => route.path === sensor.href))
const isOnProfilePage = computed(() => route.name === 'UserProfile' || route.path === '/profile' || route.path.includes('/user-profile'))

// UI Functions
const closeDropdown = (e) => {
  if (!e.target.closest('.relative.group') && !e.target.closest('.relative.ml-4')) {
    isSensorDropdownOpen.value = false;
    isProfileDropdownOpen.value = false;
  }
};

const handleResize = () => {
  if (window.innerWidth < 640) {
    isSensorDropdownOpen.value = false;
    isProfileDropdownOpen.value = false;
    showNotifications.value = false;
    showWifiTooltip.value = false;
    showWebSocketTooltip.value = false;
    showRecalibrationTooltip.value = false;
    showNotificationTooltip.value = false;
    showProfileTooltip.value = false;
  }
};

// Menu Items
const menuItems = [
  { name: 'Overview', href: '/app/dashboard', icon: LayoutDashboard },
  { name: 'Crop Prediction', href: '/app/prediction', icon: Brain },
  { name: 'Weather', href: '/app/weather', icon: Cloud },
  { name: 'Device Control', href: '/app/control', icon: Cpu },
  { name: 'Soil Analysis', href: '/app/soil', icon: Sprout }
];

const sensorTypes = [
  { name: 'NPK Data', href: '/app/npkData', icon: Sprout },
  { name: 'Soil pH', href: '/app/soilph', icon: Beaker },
  { name: 'Soil Moisture', href: '/app/soil-moisture', icon: Droplets },
  { name: 'Temp/Humid', href: '/app/temperature-humidity', icon: Thermometer },
  { name: 'Water Level', href: '/app/water-level', icon: Gauge },
  { name: 'Motor Control', href: '/app/motor-control', icon: Power }
];

const notificationTracker = {
  // Check if notification was saved today (using localStorage)
  async wasSavedToday(notificationKey) {
    const todayKey = new Date().toISOString().split('T')[0];
    const fullKey = `notification-${notificationKey}-${todayKey}`;
    return localStorage.getItem(fullKey) === 'saved' || await this.checkMongoDB(notificationKey);
  },

  // Check MongoDB as fallback
  async checkMongoDB(notificationKey) {
    try {
      // Call the API to check if notification exists today
      const response = await api.get('/notifications/check-today', {
        params: { uniqueKey: notificationKey }
      });
      return response.data.exists;
    } catch (error) {
      console.error('Error checking notification in MongoDB:', error);
      return false;
    }
  },

  // Clean old localStorage entries (older than 1 day)
  cleanOldEntries() {
    const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('notification-')) {
        // Extract timestamp from key format: notification-{key}-{date}
        const parts = key.split('-');
        if (parts.length >= 3) {
          const datePart = parts[parts.length - 1];
          // Try to parse the date
          try {
            const keyDate = new Date(datePart);
            if (keyDate.getTime() < oneDayAgo) {
              localStorage.removeItem(key);
            }
          } catch (e) {
            // If date parsing fails, remove the key
            localStorage.removeItem(key);
          }
        }
      }
    });
  }
};

const cleanNotificationCache = () => {
  const today = new Date().toDateString();
  if (notificationTracker.lastCleanup === today) return;
  
  notificationTracker.savedToday.clear();
  notificationTracker.lastCleanup = today;
};

const wasNotificationSavedToday = async (notificationKey) => {
  const todayKey = new Date().toISOString().split('T')[0];
  const storageKey = `${notificationKey}-${todayKey}`;
  
  // First check localStorage
  const state = notificationStorage.get(storageKey);
  if (state === 'complete') {
    return true;
  }
  
  // Fallback to MongoDB check via API
  try {
    const response = await api.get('/notifications/check-today', {
      params: { uniqueKey: notificationKey }
    });
    return response.data.exists;
  } catch (error) {
    console.error('Error checking notification in MongoDB:', error);
    return false;
  }
};

const markNotificationSaved = (notificationKey) => {
  const todayKey = new Date().toISOString().split('T')[0];
  const fullKey = `notification-${notificationKey}-${todayKey}`;
  localStorage.setItem(fullKey, 'saved');
};

const startOfToday = () => {
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate());
};

const formatNotificationContext = (type, sensorData, additionalData = {}) => {
  const baseContext = {
    timestamp: new Date(),
    source: 'system',
    ...additionalData
  };

  switch (type) {
    case 'water-level':
      return {
        ...baseContext,
        waterLevel: sensorData.waterData?.waterLevel,
        status: sensorData.waterData?.waterLevel <= 15 ? 'Critical' : 
                sensorData.waterData?.waterLevel <= 30 ? 'Warning' : 'Normal',
        priority: sensorData.waterData?.waterLevel <= 15 ? 'High' : 
                 sensorData.waterData?.waterLevel <= 30 ? 'Medium' : 'Low',
        recommendation: sensorData.waterData?.waterLevel <= 15 ? 
          'Immediate water refill required' :
          sensorData.waterData?.waterLevel <= 30 ? 
          'Schedule water refill within 24 hours' :
          'Water level adequate'
      };

    case 'humidity-temperature':
      return {
        ...baseContext,
        humidity: sensorData.sensor2Data?.humidity,
        temperature: sensorData.sensor2Data?.temperature,
        soilMoisture: sensorData.sensor2Data?.soilMoisture,
        recommendation: sensorData.sensor2Data?.humidity > 70 ? 
          'High humidity - fungal disease risk' :
          sensorData.sensor2Data?.temperature > 30 ? 
          'High temperature - plant stress risk' :
          sensorData.sensor2Data?.temperature < 18 ?
          'Low temperature - growth may slow' :
          'Conditions optimal'
      };

    case 'soil-moisture':
      return {
        ...baseContext,
        soilMoisture: sensorData.sensor2Data?.soilMoisture,
        motorStatus: additionalData.motorStatus || 'Unknown',
        lastActivation: additionalData.lastActivation || 'N/A',
        waterLevel: sensorData.waterData?.waterLevel,
        recommendation: sensorData.sensor2Data?.soilMoisture <= 20 ? 
          'Soil is dry - irrigation required' :
          sensorData.sensor2Data?.soilMoisture > 55 ?
          'Soil is oversaturated - reduce watering' :
          'Soil moisture optimal'
      };

    case 'npk-ph':
      return {
        ...baseContext,
        nitrogen: {
          value: sensorData.sensor1Data?.nitrogen,
          level: sensorData.sensor1Data?.nitrogen < 51 ? 'Low' :
                 sensorData.sensor1Data?.nitrogen > 200 ? 'High' : 'Optimal'
        },
        phosphorus: {
          value: sensorData.sensor1Data?.phosphorus,
          level: sensorData.sensor1Data?.phosphorus < 21 ? 'Low' :
                 sensorData.sensor1Data?.phosphorus > 60 ? 'High' : 'Optimal'
        },
        potassium: {
          value: sensorData.sensor1Data?.potassium,
          level: sensorData.sensor1Data?.potassium < 101 ? 'Low' :
                 sensorData.sensor1Data?.potassium > 250 ? 'High' : 'Optimal'
        },
        soilPh: {
          value: sensorData.sensor1Data?.soilPh,
          condition: sensorData.sensor1Data?.soilPh < 5.5 ? 'Acidic' :
                    sensorData.sensor1Data?.soilPh > 7.5 ? 'Alkaline' : 'Neutral'
        },
        recommendation: getNutrientRecommendation(sensorData.sensor1Data)
      };

    case 'watering-schedule':
      return {
        ...baseContext,
        scheduleDate: additionalData.scheduleDate,
        startTime: additionalData.startTime,
        endTime: additionalData.endTime,
        duration: additionalData.duration,
        waterLevelAtStart: sensorData.waterData?.waterLevel,
        zone: additionalData.zone || 'Greenhouse 1',
        mode: additionalData.mode || 'auto',
        motorActivationSuccess: additionalData.motorSuccess || false,
        remarks: additionalData.motorSuccess ? 
          'Motor activated successfully' : 'Motor activation failed'
      };

    case 'weather-alert':
      return {
        ...baseContext,
        forecast: additionalData.forecast,
        currentWeather: additionalData.currentWeather,
        recommendation: additionalData.condition?.includes('Rain') ?
          'Rain expected - consider delaying watering' :
          additionalData.condition?.includes('Thunderstorm') ?
          'Thunderstorm warning - secure equipment' :
          'Normal weather conditions'
      };

    default:
      return baseContext;
  }
};

const formatDate = (date) => {
  return date.toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
    weekday: 'short'
  });
};

// SMS Function
const sendSMS = async (phone, message) => {
  if (!phone) {
    console.warn('No phone number provided for SMS');
    return false;
  }

  // Format the phone number first
  const formattedPhone = formatPhoneNumber(phone);
  if (!formattedPhone) {
    console.error('Invalid phone number format:', phone);
    return false;
  }

  try {
    console.log('Sending SMS with:', { 
      number: formattedPhone,  // Use the formatted number
      message 
    });

    const response = await api.post('/sms/send-sms', { 
      number: formattedPhone,  // Use the formatted number
      message 
    });

    console.log('✅ SMS sent successfully:', response.data);
    return true;
  } catch (error) {
    console.error('❌ SMS send error:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    showToastMessage('Failed to send SMS notification', 'warning');
    return false;
  }
};

// Improved phone number formatter
const formatPhoneNumber = (phone) => {
  if (!phone) return null;
  
  // Remove all non-digit characters
  const cleaned = phone.toString().replace(/\D/g, '');
  
  // Handle Philippine numbers (most common case)
  if (cleaned.length === 11 && cleaned.startsWith('0')) {
    return `+63${cleaned.substring(1)}`;
  }
  if (cleaned.length === 10 && cleaned.startsWith('9')) {
    return `+63${cleaned}`;
  }
  if (cleaned.length === 12 && cleaned.startsWith('63')) {
    return `+${cleaned}`;
  }
  
  // Handle international numbers
  if (cleaned.length >= 11 && cleaned.startsWith('1')) { // US/Canada
    return `+${cleaned}`;
  }
  
  // If already in international format with +
  if (phone.startsWith('+') && cleaned.length >= 11) {
    return phone;
  }
  
  console.warn('Unrecognized phone number format:', phone);
  return null;
};

// Navigation Functions
const goToRecalibration = () => {
  isProfileDropdownOpen.value = false
  router.push('/app/recalibration')
}

const goToFAQ = () => {
  isProfileDropdownOpen.value = false
  router.push('/faq')
}

const toggleProfileDropdown = () => {
  isProfileDropdownOpen.value = !isProfileDropdownOpen.value
  if (isProfileDropdownOpen.value) showProfileTooltip.value = false
}

const goToProfile = () => {
  isProfileDropdownOpen.value = false
  router.push({ name: 'UserProfile' })
}

const toggleSensorDropdown = () => {
  isSensorDropdownOpen.value = !isSensorDropdownOpen.value
}

const processToastQueue = () => {
  if (toastQueue.value.length === 0 || isToastActive.value) return;
  
  isToastActive.value = true;
  const nextToast = toastQueue.value.shift();
  toastMessage.value = nextToast.message;
  toastSeverity.value = nextToast.severity;
  showToast.value = true;

  setTimeout(() => {
    showToast.value = false;
    setTimeout(() => {
      isToastActive.value = false;
      processToastQueue();
    }, 300);
  }, 5000);
};

const showToastMessage = (message, severity = 'info', persistKey = null) => {
  
  window.showToast(message, severity)
}

const notificationStorage = {
  set(key, value, ttl = 24 * 60 * 60 * 1000) {
    const now = new Date();
    const item = {
      value: value,
      expiry: now.getTime() + ttl,
    };
    localStorage.setItem(`notif_${key}`, JSON.stringify(item));
  },

  get(key) {
    const itemStr = localStorage.getItem(`notif_${key}`);
    if (!itemStr) return null;
    
    const item = JSON.parse(itemStr);
    const now = new Date();
    
    // If expired, delete and return null
    if (now.getTime() > item.expiry) {
      localStorage.removeItem(`notif_${key}`);
      return null;
    }
    
    return item.value;
  },

  has(key) {
    return this.get(key) !== null;
  },

  cleanExpired() {
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('notif_')) {
        this.get(key.replace('notif_', '')); // This will auto-clean expired items
      }
    });
  }
};

// Fix the cleanExpired method to not use 'this'
notificationStorage.cleanExpired = function() {
  Object.keys(localStorage).forEach(key => {
    if (key.startsWith('notif_')) {
      notificationStorage.get(key.replace('notif_', ''));
    }
  });
};

// Notification Functions
const sendNotification = async (message, title, severity = 'info', uniqueKey = null, contextData = {}) => {
  try {
    // Create a reliable unique key
    const notificationId = uniqueKey || `ntf-${severity}-${title}-${message}`
      .replace(/\s+/g, '-')
      .replace(/[^a-zA-Z0-9_-]/g, '')
      .toLowerCase();
    
    // Check if we've already processed this notification in the last minute
    const existingState = notificationStorage.get(notificationId);
    
    if (existingState === 'completed') {
      console.log('⏩ Notification already completed:', notificationId);
      return { success: true, skipped: true, reason: 'already_completed' };
    }

    // Show toast only if not shown recently
    if (existingState !== 'toast_shown') {
      showToastMessage(message, severity);
      notificationStorage.set(notificationId, 'toast_shown', 60000); // 1 minute TTL for toast
    } else {
      console.log('⏩ Toast already shown, only saving notification:', notificationId);
    }

    // Save notification to database
    const response = await api.post('/notifications', {
      message,
      title,
      severity,
      uniqueKey: uniqueKey,
      contextData: {
        ...contextData,
        notificationId: notificationId,
        processedAt: new Date().toISOString()
      },
      type: 'watering_schedule'
    });
    
    console.log('✅ Notification saved successfully:', response.data);
    
    // Mark as completed in storage with longer TTL (24 hours)
    notificationStorage.set(notificationId, 'completed', 24 * 60 * 60 * 1000);
    
    // Send SMS if configured
    if (user.value?.phoneNumber) {
      try {
        await sendSMS(
          user.value.phoneNumber,
          `[${title}] ${message}`
        );
        console.log('✅ SMS sent successfully');
      } catch (smsError) {
        console.error('❌ Failed to send SMS:', smsError);
      }
    }
    
    return { 
      success: true, 
      id: response.data.id,
      alreadyShown: existingState === 'toast_shown'
    };
    
  } catch (error) {
    console.error('❌ Failed to save notification:', error);
    
    if (error.response) {
      console.error('Error response:', error.response.data);
      console.error('Error status:', error.response.status);
    }
    
    return { 
      success: false, 
      error: error.message 
    };
  }
};

const getNutrientRecommendation = (data) => {
  if (!data) return 'No recommendation available';
  
  let recommendations = [];
  
  // Nitrogen recommendations
  if (data.nitrogen < 51) {
    recommendations.push('Apply nitrogen-rich fertilizer');
  } else if (data.nitrogen > 200) {
    recommendations.push('Reduce nitrogen application');
  }
  
  // Phosphorus recommendations
  if (data.phosphorus < 21) {
    recommendations.push('Add phosphorus fertilizer');
  } else if (data.phosphorus > 60) {
    recommendations.push('Reduce phosphorus input');
  }
  
  // Potassium recommendations
  if (data.potassium < 101) {
    recommendations.push('Supplement with potassium');
  } else if (data.potassium > 250) {
    recommendations.push('Reduce potassium fertilization');
  }
  
  // pH recommendations
  if (data.soilPh < 5.5) {
    recommendations.push('Apply lime to reduce acidity');
  } else if (data.soilPh > 7.5) {
    recommendations.push('Use sulfur to lower pH');
  }
  
  return recommendations.length > 0 ? 
    recommendations.join('. ') + '.' : 
    'Nutrient levels are optimal';
};

// Add this with your other refs
const unsubscribeWaterLevel = ref(null);

const setupWaterLevelListener = () => {
  const pollWaterLevel = async () => {
    try {
      const response = await api.get('/sensors/water-level/latest')
      if (response.data && typeof response.data.waterLevel === 'number') {
        waterLevel.value = response.data.waterLevel
        evaluateWaterLevel(response.data.waterLevel)
      }
    } catch (error) {
      console.error('Water level fetch error:', error)
    }
  }
  
  const waterLevelInterval = setInterval(pollWaterLevel, 30000)
  pollWaterLevel()
  unsubscribeFunctions.push(() => clearInterval(waterLevelInterval))
}

// Helper function to get latest sensor data
const getLatestSensorData = async () => {
  try {
    const response = await api.get('/sensors/combined/latest');
    return response.data.sensor2Data || {};
  } catch (error) {
    console.error("Error fetching sensor data:", error);
    return {};
  }
};

const evaluateWaterLevel = async (level) => {
  if (typeof level !== 'number' || level < 0 || level > 100) {
    console.warn(`Invalid water level value: ${level}`);
    return;
  }

  try {
    const sensorData = await fetchLatestContextData();
    const dateKey = new Date().toISOString().split('T')[0];
    const formattedDate = formatDate(new Date());

    const context = formatNotificationContext('water-level', sensorData, {
      date: formattedDate,
      waterLevel: level
    });

    if (level <= 15) {
      await sendNotification(
        `Water level is CRITICALLY LOW (${level}%)! Immediate action required.`,
        '🚨 Water Emergency',
        'critical',
        `water-critical-${dateKey}`,
        context
      );
    } 
    else if (level <= 30) {
      await sendNotification(
        `Water level is low (${level}%). Consider refilling soon.`,
        'Low Water Warning',
        'warning',
        `water-warning-${dateKey}`,
        context
      );
    }
  } catch (error) {
    console.error('Water level alert error:', error);
  }
};

const sendScheduleNotification = async (schedule, status) => {
  const dateTimeFormatted = new Date(schedule.scheduledTime).toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  const message = status === 'started'
    ? `The watering scheduled at ${dateTimeFormatted} is now starting.`
    : `The watering scheduled at ${dateTimeFormatted} has ended.`;

  const notificationId = `schedule-${schedule.id}-${status}`;

  try {
    await sendNotification(
      message,
      'Scheduled Watering',
      'info',
      notificationId
    );

    // Send SMS if enabled
    if (user.value?.phoneNumber && user.value.notifySchedules) {
      await sendSMS(
        user.value.phoneNumber,
        `[Schedule] ${status === 'started' ? 'Started' : 'Completed'}: ${message}`
      );
    }
  } catch (error) {
    console.error('Schedule notification error:', error);
  }
};

// Weather Alert Functions
const isSevereWeather = (condition) => {
  if (!condition) return false;
  const severeConditions = [
    'Heavy Rain',
    'Rain Showers',
    'Heavy Rain Showers',
    'Violent Rain Showers',
    'Thunderstorm',
    'Thunderstorm with Hail',
    'Severe Thunderstorm',
  ];
  return severeConditions.includes(condition);
};

const checkWeatherForecastForAlerts = async () => {
  try {
    const weatherData = await getWeatherData();
    if (!weatherData?.forecast) return;

    const now = new Date();
    const dateKey = now.toISOString().split('T')[0];
    const formattedDate = formatDate(now);

    for (const day of weatherData.forecast.slice(0, 3)) {
      const condition = mapWeatherCode(day.condition_code);
      if (!isSevereWeather(condition)) continue;

      const dayDate = new Date(day.date);
      const dayFormattedDate = formatDate(dayDate);

      const context = {
        forecast: {
          date: dayFormattedDate,
          condition,
          temperatures: {
            current: day.temperature,
            min: day.temperature_min,
            max: day.temperature_max,
            unit: '°C'
          },
          precipitation: day.precipitation,
          humidity: day.humidity
        },
        currentWeather: {
          temperature: weatherData.current?.temperature_c,
          humidity: weatherData.current?.humidity,
          pressure: weatherData.current?.pressure,
          windSpeed: weatherData.current?.wind_speed,
          uvIndex: weatherData.current?.uv_index
        },
        recordedAt: new Date()  // Changed from serverTimestamp()
      };

      const toastMessage = `${condition} expected on ${dayFormattedDate}`;

      await sendNotification(
        toastMessage,
        'Severe Weather Alert',
        'warning',
        `weather-${condition}-${dateKey}`,
        context
      );
    }
  } catch (error) {
    console.error('Weather alert error:', error);
    showToastMessage('Failed to check weather alerts', 'error');
  }
};

// Enhanced data cleaner
const cleanFirestoreData = (data) => {
  if (data === null || data === undefined) return null;
  
  if (typeof data !== 'object') return data;
  
  if (Array.isArray(data)) {
    return data.map(item => cleanFirestoreData(item));
  }

  const cleaned = {};
  Object.keys(data).forEach(key => {
    const value = data[key];
    if (value !== undefined) {
      cleaned[key] = cleanFirestoreData(value);
    }
  });
  return cleaned;
};

const unsubscribeCombinedListener = ref(null);

const setupCombinedRealtimeListener = () => {
  const pollSensorData = async () => {
    try {
      const response = await api.get('/sensors/combined/latest')
      await evaluateSensorRangesAndNotify(response.data)
    } catch (error) {
      console.error('Sensor data fetch error:', error)
    }
  }
  
  const sensorInterval = setInterval(pollSensorData, 60000)
  pollSensorData()
  unsubscribeFunctions.push(() => clearInterval(sensorInterval))
}


// Unified evaluation function for all ranges and sources
const evaluateSensorRangesAndNotify = async (sensorDataResponse) => {
  const { waterData, sensor1Data, sensor2Data } = sensorDataResponse;
  const sensorData = { waterData, sensor1Data, sensor2Data };
  const source = "esp32-2";

  if (!sensorData) {
    console.warn('No sensor data provided');
    return;
  }

  const now = new Date();
  const dateKey = now.toISOString().split('T')[0];
  const formattedDate = formatDate(now);

  // Temperature Alerts
  if (typeof sensor2Data?.temperature === 'number') {
    if (sensor2Data.temperature > 30) {
      const context = formatNotificationContext('humidity-temperature', sensorData, {
        source,
        date: formattedDate
      });

      await sendNotification(
        `High temperature (${sensor2Data.temperature}°C) detected`,
        'Temperature Alert',
        'warning',
        `temp-high-${source}-${dateKey}`,
        context
      );
    } else if (sensor2Data.temperature < 18) {
      const context = formatNotificationContext('humidity-temperature', sensorData, {
        source,
        date: formattedDate
      });

      await sendNotification(
        `Low temperature (${sensor2Data.temperature}°C) detected`,
        'Temperature Alert',
        'warning',
        `temp-low-${source}-${dateKey}`,
        context
      );
    }
  }

  // Humidity Alerts
  if (typeof sensor2Data?.humidity === 'number') {
    if (sensor2Data.humidity > 70) {
      const context = formatNotificationContext('humidity-temperature', sensorData, {
        source,
        date: formattedDate
      });

      await sendNotification(
        `High humidity (${sensor2Data.humidity}%) detected`,
        'Humidity Alert',
        'warning',
        `humidity-high-${source}-${dateKey}`,
        context
      );
    } else if (sensor2Data.humidity < 40) {
      const context = formatNotificationContext('humidity-temperature', sensorData, {
        source,
        date: formattedDate
      });

      await sendNotification(
        `Low humidity (${sensor2Data.humidity}%) detected`,
        'Humidity Alert',
        'warning',
        `humidity-low-${source}-${dateKey}`,
        context
      );
    }
  }

  // Soil Moisture Alerts
  if (typeof sensor2Data?.soilMoisture === 'number') {
    if (sensor2Data.soilMoisture <= 10) {
      const context = formatNotificationContext('soil-moisture', sensorData, {
        source,
        date: formattedDate,
        motorStatus: 'Auto OFF',
        lastActivation: 'N/A'
      });

      await sendNotification(
        `CRITICALLY LOW soil moisture (${sensor2Data.soilMoisture}%)`,
        '🚨 Soil Emergency',
        'critical',
        `soil-critical-${source}-${dateKey}`,
        context
      );
    } else if (sensor2Data.soilMoisture <= 20) {
      const context = formatNotificationContext('soil-moisture', sensorData, {
        source,
        date: formattedDate,
        motorStatus: 'Auto OFF',
        lastActivation: 'N/A'
      });

      await sendNotification(
        `Low soil moisture (${sensor2Data.soilMoisture}%)`,
        'Soil Moisture Alert',
        'warning',
        `soil-low-${source}-${dateKey}`,
        context
      );
    }
  }

  // Soil pH Alerts
  if (sensor1Data && typeof sensor1Data.soilPh === 'number') {
    if (sensor1Data.soilPh < 5.5) {
      const context = formatNotificationContext('npk-ph', sensorData, {
        source: 'esp32-1',
        date: formattedDate
      });

      await sendNotification(
        `Low soil pH (${sensor1Data.soilPh}) - Acidic conditions`,
        'Soil pH Alert',
        'warning',
        `ph-low-esp32-1-${dateKey}`,
        context
      );
    } else if (sensor1Data.soilPh > 7.5) {
      const context = formatNotificationContext('npk-ph', sensorData, {
        source: 'esp32-1',
        date: formattedDate
      });

      await sendNotification(
        `High soil pH (${sensor1Data.soilPh}) - Alkaline conditions`,
        'Soil pH Alert',
        'warning',
        `ph-high-esp32-1-${dateKey}`,
        context
      );
    }
  }

  // NPK Nutrient Alerts
  if (sensor1Data) {
    const nutrientChecks = [
      { name: 'nitrogen', low: 51, high: 200 },
      { name: 'phosphorus', low: 21, high: 60 },
      { name: 'potassium', low: 101, high: 250 }
    ];

    for (const nutrient of nutrientChecks) {
      const value = sensor1Data[nutrient.name];
      if (typeof value !== 'number') continue;

      if (value < nutrient.low) {
        const context = formatNotificationContext('npk-ph', sensorData, {
          source: 'esp32-1',
          date: formattedDate
        });

        await sendNotification(
          `Low ${nutrient.name} (${value}ppm) detected`,
          `${nutrient.name.charAt(0).toUpperCase() + nutrient.name.slice(1)} Alert`,
          'warning',
          `${nutrient.name}-low-esp32-1-${dateKey}`,
          context
        );
      } else if (value > nutrient.high) {
        const context = formatNotificationContext('npk-ph', sensorData, {
          source: 'esp32-1',
          date: formattedDate
        });

        await sendNotification(
          `High ${nutrient.name} (${value}ppm) detected`,
          `${nutrient.name.charAt(0).toUpperCase() + nutrient.name.slice(1)} Alert`,
          'warning',
          `${nutrient.name}-high-esp32-1-${dateKey}`,
          context
        );
      }
    }
  }
};

const setupScheduleListener = () => {
  const pollSchedules = async () => {
    try {
      const response = await api.get('/schedules/active')
      processScheduleUpdates(response.data, 'all', [])
    } catch (error) {
      console.error('Schedule fetch error:', error)
    }
  }
  
  const scheduleInterval = setInterval(pollSchedules, 30000)
  pollSchedules()
  unsubscribeFunctions.push(() => clearInterval(scheduleInterval))
}

const processScheduleUpdates = (updatedSchedules, mode, changes) => {
  schedulesCache.value = schedulesCache.value.filter(s => s.mode !== mode);
  
  updatedSchedules.forEach(schedule => {
    schedulesCache.value.push(schedule);
  });
  
  schedulesCache.value.sort((a, b) => a.scheduledTime - b.scheduledTime);

  // Special handling for one-time schedules
  if (mode === 'one-time') {
    changes.forEach(change => {
      if (change.type === 'modified') {
        const newData = change.doc.data();
        const oldData = change.doc.metadata.hasPendingWrites ? 
          schedulesCache.value.find(s => s.id === change.doc.id) : null;
        
        if (newData.completed === true && (!oldData || oldData.completed !== true)) {
          const schedule = {
            id: change.doc.id,
            mode: 'one-time',
            ...newData,
            scheduledTime: newData.scheduledTime < 1e12 ? newData.scheduledTime * 1000 : newData.scheduledTime
          };
          
          if (activeSchedules.value[schedule.id]) {
            processScheduleEnd(schedule, activeSchedules.value[schedule.id].currentDay);
            saveToHistory(schedule, new Date(), activeSchedules.value[schedule.id].currentDay);
            delete activeSchedules.value[schedule.id];
            if (scheduleTimers.value[schedule.id]) {
              clearTimeout(scheduleTimers.value[schedule.id]);
              delete scheduleTimers.value[schedule.id];
            }
          }
        }
      }
    });
  }
};

const scheduleProcessingStatus = ref({});

let sensorDataCache = {
  data: null,
  lastFetch: 0,
  cacheDuration: 60000
};

const lastWateringNotifications = ref(new Map());

const getCachedSensorData = async () => {
  const now = Date.now();
  if (sensorDataCache.data && (now - sensorDataCache.lastFetch) < sensorDataCache.cacheDuration) {
    return sensorDataCache.data;
  }
  
  try {
    const response = await api.get('/sensors/combined/latest');
    sensorDataCache.data = response.data;
    sensorDataCache.lastFetch = now;
    return response.data;
  } catch (error) {
    console.error('Error fetching sensor data:', error);
    return sensorDataCache.data || {};
  }
};

const checkSchedules = async () => {
  try {
    const now = new Date();
    const currentDay = (now.getDay() + 6) % 7; 
    const currentTime = now.getHours() * 3600000 + now.getMinutes() * 60000 + now.getSeconds() * 1000;
    
    for (const schedule of schedulesCache.value) {
      if (!schedule.notifyWatering || schedule.completed) continue;
      
      const scheduleKey = `${schedule.id}-${currentDay}`;
      
      if (processingSchedules.value.has(scheduleKey)) {
        continue;
      }
      
      if (lastProcessedScheduleTimes.value[scheduleKey]) {
        const lastProcessed = new Date(lastProcessedScheduleTimes.value[scheduleKey]);
        const todayStart = new Date(now);
        todayStart.setHours(0, 0, 0, 0);
        
        if (lastProcessed >= todayStart) {
          continue;
        }
      }
      
      let shouldRun = false;
      let timeMatch = false;
      
      if (schedule.mode === 'daily') {
        shouldRun = true;
        timeMatch = Math.abs(currentTime - schedule.scheduledTime) < 2000;
      } else if (schedule.mode === 'weekly') {
        shouldRun = schedule.daysArray?.includes(currentDay) ?? false;
        timeMatch = shouldRun && Math.abs(currentTime - schedule.scheduledTime) < 2000;
      } else if (schedule.mode === 'one-time') {
        const scheduleDate = new Date(schedule.scheduledTime);
        shouldRun = scheduleDate.toDateString() === now.toDateString();
        timeMatch = shouldRun && Math.abs(now.getTime() - schedule.scheduledTime) < 2000;
      }
      
      if (shouldRun && timeMatch && !activeSchedules.value[schedule.id]) {
        console.log(`✅ Starting ${schedule.mode} schedule ${schedule.id}`);
        processingSchedules.value.add(scheduleKey);
        lastProcessedScheduleTimes.value[scheduleKey] = now.getTime();
        processScheduleStart(schedule, currentDay);
      }
    }
  } catch (error) {
    console.error('Schedule check error:', error);
  }
};

const sendWateringNotification = async (message, title, scheduleId, eventType, contextData = {}) => {
  const now = new Date();
  const notificationKey = `watering-${scheduleId}-${eventType}-${now.toISOString().split('T')[0]}`;
  
  const lastSent = lastWateringNotifications.value.get(notificationKey);
  if (lastSent && (now - lastSent) < 60000) { 
    console.log(`⏩ Watering notification already sent recently: ${notificationKey}`);
    return { success: true, skipped: true };
  }
  
  const result = await sendNotification(
    message,
    title,
    eventType === 'start' ? 'info' : 'success',
    notificationKey,
    contextData
  );
  
  if (result.success) {
    lastWateringNotifications.value.set(notificationKey, now.getTime());
  }
  
  return result;
};

const getDayName = (dayNumber) => {
  const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  return dayNames[dayNumber] || 'Unknown';
};

const fetchLatestContextData = async () => {
  try {
    const response = await api.get('/sensors/combined/latest')
    return response.data
  } catch (error) {
    console.error('Error fetching sensor data:', error)
    return {}
  }
}

const motorControlLocks = ref(new Map());
const lastMotorCommand = ref({
  status: null,
  scheduleId: null,
  timestamp: 0
});

const processingSchedules = ref(new Set());
const lastMotorCommands = ref(new Map());

const updateMotorStatus = async (status, scheduleId, actionType = 'schedule') => {
  const commandKey = `${status ? 'on' : 'off'}-${scheduleId}-${actionType}`;
  const now = Date.now();
  
  if (lastMotorCommands.value.has(commandKey)) {
    const lastSent = lastMotorCommands.value.get(commandKey);
    if (now - lastSent < 10000) {
      console.log(`⏩ Skipping duplicate motor command (recently sent): ${commandKey}`);
      return true;
    }
  }
  
  if (motorControlLocks.value.has(commandKey)) {
    console.log(`⏩ Motor command already in progress: ${commandKey}`);
    return true;
  }
  
  motorControlLocks.value.set(commandKey, true);
  lastMotorCommands.value.set(commandKey, now);
  
  try {
    console.log(`⚡ Turning motor ${status ? 'ON' : 'OFF'} for ${actionType}: ${scheduleId}`);
    
    const response = await api.post('/devices/motor/control', {
      status: status ? 'on' : 'off',
      scheduleId: scheduleId || 'system-command'
    });
    
    try {
      console.log(`📡 Sending motor status to ESP32 via /api/motor_status/`);
      const motorStatusResponse = await api.post('/motor_status/', {
        status: status,
        device_id: 'main_motor',
        user: 'system',
        timestamp: new Date().toISOString(),
        formatted_time: new Date().toLocaleString('en-US', {
          weekday: 'short',
          month: 'short',
          day: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        }),
        source: `schedule-${scheduleId || 'system'}-${actionType}`
      });
      
      console.log(`✅ Motor status sent to ESP32:`, motorStatusResponse.data);
    } catch (motorStatusError) {
      console.warn('⚠️ Failed to send motor status to ESP32, but continuing:', motorStatusError.message);
    } 
    
    if (response.data && response.data.status === 'success') {
      console.log(`✅ Motor ${status ? 'started' : 'stopped'} successfully`);
      return true;
    }
    
    console.warn('Motor control returned non-success status:', response.data);
    return false;
    
  } catch (error) {
    console.error('Motor control failed:', error);
    return false;
  } finally {
    setTimeout(() => {
      motorControlLocks.value.delete(commandKey);
    }, 10000);
  }
};

const markScheduleCompleted = async (scheduleId) => {
  try {
    console.log(`📝 Marking schedule ${scheduleId} as completed`);
    
    const response = await api.put(`/schedules/${scheduleId}/complete`);
    
    if (response.data && response.data.status === 'success') {
      console.log(`✅ Schedule ${scheduleId} marked as completed`);
      return true;
    }
    
    return false;
  } catch (error) {
    console.error('Error marking schedule as completed:', error);
    return false;
  }
};

const processScheduleStart = async (schedule, currentDay) => {
  const scheduleId = schedule.id;
  const scheduleKey = `${schedule.id}-${currentDay}`;
  
  if (scheduleProcessingStatus.value[scheduleId] === 'processing') {
    console.log(`⏩ Schedule ${scheduleId} is already being processed`);
    processingSchedules.value.delete(scheduleKey);
    return;
  }
  
  scheduleProcessingStatus.value[scheduleId] = 'processing';
  const startTime = Date.now();
  
  try {
    const sensorData = await getCachedSensorData();
    
    const now = new Date();
    const formattedTime = now.toLocaleString('en-US', {
      weekday: 'short', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
    
    let typeLabel, message;
    switch (schedule.mode) {
      case 'one-time':
        typeLabel = 'One-time';
        message = `One-time watering started at ${formattedTime}`;
        break;
      case 'daily':
        typeLabel = 'Daily';
        message = `Daily watering started at ${formattedTime}`;
        break;
      case 'weekly':
        typeLabel = 'Weekly';
        const dayName = getDayName(currentDay);
        message = `Weekly watering (${dayName}) started at ${formattedTime}`;
        break;
      default:
        typeLabel = 'Scheduled';
        message = `Watering started at ${formattedTime}`;
    }
    
    console.log(`⚡ Turning motor ON for schedule ${scheduleId}`);
    const motorSuccess = await updateMotorStatus(true, scheduleId, 'schedule-start');
    
    if (motorSuccess) {
      console.log(`✅ Motor started for schedule ${scheduleId}`);
    } else {
      console.error(`❌ Failed to start motor for schedule ${scheduleId}`);
    }
    
    const context = formatNotificationContext('watering-schedule', sensorData, {
      scheduleType: schedule.mode,
      duration: schedule.duration,
      scheduleId: scheduleId,
      motorStatus: motorSuccess ? 'on' : 'off',
      startTime: formattedTime,
      startTimestamp: startTime,
      dayOfWeek: currentDay,
      action: 'start',
      motorSuccess: motorSuccess,
      zone: 'Greenhouse 1',
      mode: 'auto',
      waterLevelAtStart: sensorData.waterData?.waterLevel
    });
    
    const notificationResult = await sendWateringNotification(
      message,
      `${typeLabel} Watering Started`,
      scheduleId,
      'start',
      context
    );
    
    if (notificationResult.success) {
      console.log('✅ Start notification saved successfully');
    } else if (notificationResult.skipped) {
      console.log('⏩ Start notification skipped (duplicate)');
    } else {
      console.error('❌ Failed to save start notification');
    }
    
    activeSchedules.value[scheduleId] = {
      startTime: startTime,
      duration: schedule.duration,
      mode: schedule.mode,
      currentDay: currentDay,
      motorStarted: motorSuccess,
      notificationSent: notificationResult.success,
      contextData: context
    };
    
    if (scheduleTimers.value[scheduleId]) {
      clearTimeout(scheduleTimers.value[scheduleId]);
    }
    
    scheduleTimers.value[scheduleId] = setTimeout(() => {
      processScheduleEnd(schedule, currentDay, startTime);
    }, schedule.duration * 60000);
    
  } catch (error) {
    console.error(`❌ Error starting schedule ${scheduleId}:`, error);
  } finally {
    processingSchedules.value.delete(scheduleKey);
  }
};

const processScheduleEnd = async (schedule, currentDay, startTime) => {
  const scheduleId = schedule.id;
  const scheduleKey = `${schedule.id}-${currentDay}`;
  
  try {
    const sensorData = await getCachedSensorData();
    const endTime = Date.now();
    
    const now = new Date();
    const formattedTime = now.toLocaleString('en-US', {
      weekday: 'short', month: 'short', day: 'numeric',
      hour: '2-digit', minute: '2-digit', second: '2-digit'
    });
    
    let typeLabel, message;
    switch (schedule.mode) {
      case 'one-time':
        typeLabel = 'One-time';
        message = `One-time watering completed at ${formattedTime}`;
        break;
      case 'daily':
        typeLabel = 'Daily';
        message = `Daily watering completed at ${formattedTime}`;
        break;
      case 'weekly':
        typeLabel = 'Weekly';
        const dayName = getDayName(currentDay);
        message = `Weekly watering (${dayName}) completed at ${formattedTime}`;
        break;
      default:
        typeLabel = 'Scheduled';
        message = `Watering completed at ${formattedTime}`;
    }
    
    console.log(`🛑 Stopping motor for schedule ${scheduleId}`);
    const motorSuccess = await updateMotorStatus(false, scheduleId, 'schedule-end');
    
    if (motorSuccess) {
      console.log(`✅ Motor stopped for schedule ${scheduleId}`);
    } else {
      console.error(`❌ Failed to stop motor for schedule ${scheduleId}`);
    }
    
    const context = formatNotificationContext('watering-schedule', sensorData, {
      scheduleType: schedule.mode,
      duration: schedule.duration,
      scheduleId: scheduleId,
      motorStatus: motorSuccess ? 'off' : 'unknown',
      endTime: formattedTime,
      endTimestamp: endTime,
      startTimestamp: startTime,
      totalDuration: endTime - startTime,
      dayOfWeek: currentDay,
      action: 'end',
      motorSuccess: motorSuccess,
      zone: 'Greenhouse 1',
      mode: 'auto',
      waterLevelAtStart: sensorData.waterData?.waterLevel,
      remarks: motorSuccess ? 'Motor deactivated successfully' : 'Motor deactivation failed'
    });
    
    const notificationResult = await sendWateringNotification(
      message,
      `${typeLabel} Watering Completed`,
      scheduleId,
      'end',
      context
    );
    
    if (notificationResult.success) {
      console.log('✅ End notification saved successfully');
    } else if (notificationResult.skipped) {
      console.log('⏩ End notification skipped (duplicate)');
    } else {
      console.error('❌ Failed to save end notification');
    }
    
    if (schedule.mode === 'one-time') {
      console.log('📝 Marking one-time schedule as completed...');
      const completionSuccess = await markScheduleCompleted(scheduleId);
      
      if (completionSuccess) {
        console.log(`✅ Schedule ${scheduleId} marked as completed`);
      } else {
        console.error(`❌ Failed to mark schedule ${scheduleId} as completed`);
      }
    }
    
    console.log(`✅ Schedule ${scheduleId} completed successfully`);
    
  } catch (error) {
    console.error(`❌ Error completing schedule ${scheduleId}:`, error);
  } finally {
    delete activeSchedules.value[scheduleId];
    delete scheduleTimers.value[scheduleId];
    delete scheduleProcessingStatus.value[scheduleId];
    processingSchedules.value.delete(scheduleKey);
  }
};

const saveToHistory = async (schedule, startTime, endTime, day) => {
  try {
    console.log('💾 Saving schedule to history:', schedule.id);
    
    const historyData = {
      scheduleId: schedule.id,
      mode: schedule.mode,
      originalScheduledTime: schedule.scheduledTime,
      actualStartTime: startTime,
      completedAt: endTime,
      duration: schedule.duration,
      days: schedule.days || {},
      dayOfWeek: schedule.mode === 'weekly' ? day : null,
      notifyWatering: schedule.notifyWatering !== false,
      skipIfRain: schedule.skipIfRain || false,
      waterFlowRate: schedule.waterFlowRate || 'medium'
    };
    
    console.log('📤 Sending history data to schedules_root:', historyData);
    
    const response = await api.post('/schedules/history', historyData);
    
    if (response.data && response.data.status === 'success') {
      console.log('✅ Schedule saved to history in schedules_root document');
      
      setTimeout(async () => {
        try {
          const historyResponse = await api.get('/schedules/history?limit=5');
          if (historyResponse.data && Array.isArray(historyResponse.data)) {
            const recentEntry = historyResponse.data.find(entry => 
              entry.scheduleId === schedule.id && entry.completedAt === endTime
            );
            if (recentEntry) {
              console.log('✅ Schedule history verified in schedules_root');
            } else {
              console.warn('⚠️ Schedule history not found in recent entries');
            }
          }
        } catch (verifyError) {
          console.warn('Could not verify schedule history:', verifyError);
        }
      }, 1000);
      
      return true;
    }
    
    return false;
  } catch (error) {
    console.error('❌ Error saving to schedule history:', error);
    
    // Log detailed error information
    if (error.response) {
      console.error('Error response:', error.response.data);
      console.error('Error status:', error.response.status);
    }
    
    return false;
  }
};

// Helper functions
const convertDaysFormat = (daysObject) => {
  if (!daysObject) return [];
  return Object.entries(daysObject)
    .filter(([_, value]) => value === true)
    .map(([key, _]) => parseInt(key));
};

// Enhanced initialization with better timing precision
const initScheduleSystem = () => {
  console.log('[DEBUG] Initializing schedule system...');
  
  // Clear any existing interval first
  if (scheduleCheckInterval.value) {
    clearInterval(scheduleCheckInterval.value);
  }
  
  // Clear any existing immediate timeout
  if (immediateCheckTimeout.value) {
    clearTimeout(immediateCheckTimeout.value);
  }
  
  // Check schedules every second for precise timing
  scheduleCheckInterval.value = setInterval(() => {
    checkSchedules();
  }, 1000); // Check every second for precise timing
  
  // Initial immediate check after a short delay to ensure everything is loaded
  immediateCheckTimeout.value = setTimeout(() => {
    console.log('[DEBUG] Running initial schedule check...');
    checkSchedules();
  }, 1000);
  
  console.log('[DEBUG] Schedule system initialized');
};

// Helper function to format time for debugging
const formatTimeDebug = (timeMs, mode) => {
  if (mode === 'one-time') {
    return new Date(timeMs).toLocaleString();
  } else {
    const hours = Math.floor(timeMs / 3600000);
    const minutes = Math.floor((timeMs % 3600000) / 60000);
    const seconds = Math.floor((timeMs % 60000) / 1000);
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }
};

// Function to invalidate sensor data cache when needed
const invalidateSensorDataCache = () => {
  sensorDataCache.lastFetch = 0;
  console.log('[DEBUG] Sensor data cache invalidated');
};

const unreadNotificationCount = ref(0);
let pollingInterval = null;

// Your existing fetch function with auto-update enhancement
const fetchNotifications = async () => {
  try {
    const endpoints = [
      '/notifications_unread_count', 
      '/unread-count'
    ];
    
    for (const endpoint of endpoints) {
      try {
        const response = await api.get(endpoint);
        
        // Only update if count changed
        if (response.data.count !== unreadNotificationCount.value) {
          unreadNotificationCount.value = response.data.count;
        }
        
        return; // Stop if one works
      } catch (error) {
      }
    }
    
    // If all fail, use default
    unreadNotificationCount.value = 0;
    
  } catch (error) {
    unreadNotificationCount.value = 0;
  }
};

// Simple polling function for real-time updates
const startPolling = () => {
  // Clear any existing interval
  if (pollingInterval) {
    clearInterval(pollingInterval);
  }
  
  // Fetch immediately
  fetchNotifications();
  
  // Then poll every 5 seconds for real-time updates
  pollingInterval = setInterval(() => {
    fetchNotifications();
  }, 5000); // 5 seconds
};

// Stop polling
const stopPolling = () => {
  if (pollingInterval) {
    clearInterval(pollingInterval);
    pollingInterval = null;
  }
};

// Lifecycle Hooks
onMounted(async () => {
  await fetchNotifications()
  document.addEventListener('click', closeDropdown);
  window.addEventListener('resize', handleResize);

  startPolling();

  notificationStorage.cleanExpired();
  
  // Set up daily cleanup
  const now = new Date();
  const midnight = new Date(now);
  midnight.setHours(24, 0, 0, 0);
  const msUntilMidnight = midnight - now;

  setTimeout(() => {
    notificationStorage.cleanExpired();
    setInterval(() => {
      notificationStorage.cleanExpired();
    }, 24 * 60 * 60 * 1000); 
  }, msUntilMidnight);

  // Get IP Address
  try {
    const res = await fetch('https://api.ipify.org?format=json');
    const ipData = await res.json();
    ipAddress.value = ipData.ip;
  } catch (error) {
    ipAddress.value = 'Unknown';
  }

  // Network Info
  if ('connection' in navigator) {
    const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    const updateWifiInfo = () => {
      wifiStrength.value = conn.downlinkMax ? Math.min(conn.downlinkMax * 10, 100) : 70;
      wifiNetwork.value = conn.effectiveType || 'WiFi';
    };
    updateWifiInfo();
    if (conn.addEventListener) conn.addEventListener('change', updateWifiInfo);
  }

  // Setup listeners
  setupWaterLevelListener();
  setupScheduleListener(); // This loads the initial schedules

  // Check weather every 3 hours
  checkWeatherForecastForAlerts();
  const weatherInterval = setInterval(checkWeatherForecastForAlerts, 3 * 60 * 60 * 1000);

  // Initialize the schedule system with precise checking
  initScheduleSystem();

  // --- MODIFICATION: Use unified sensor & water listener ---
  setupCombinedRealtimeListener();

  // Store interval for cleanup
  onBeforeUnmount(() => {
    document.removeEventListener('click', closeDropdown);
    window.removeEventListener('resize', handleResize);
    
    // Remove all Firebase-specific cleanup
    if (scheduleCheckInterval.value) clearInterval(scheduleCheckInterval.value);
    if (weatherInterval) clearInterval(weatherInterval);
    Object.values(scheduleTimers.value).forEach(timer => clearTimeout(timer));
    stopPolling();

  });

});

watch(() => route.path, () => {
  isSensorDropdownOpen.value = false;
  isProfileDropdownOpen.value = false;
  showNotifications.value = false;
  showWifiTooltip.value = false;
  showWebSocketTooltip.value = false;
  showRecalibrationTooltip.value = false;
  showNotificationTooltip.value = false;
  showProfileTooltip.value = false;
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
.router-link-active {
  position: relative;
  transform: translateZ(0);
}

.dropdown-link {
  z-index: 9999;
}

.router-link-active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: -1px;
  height: 1px;
  background: linear-gradient(to right, white, transparent);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.router-link-active:hover::after {
  transform: scaleX(1);
}

/* Ensure notification badge styling is consistent */
.notification-badge {
  /* These styles will override any inline styles */
  min-width: 16px !important;
  height: 16px !important;
  background-color: #ef4444 !important; /* Tailwind red-500 */
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
}

/* Completely static notification badge - no animations */
.notification-badge-static {
  min-width: 16px !important;
  height: 16px !important;
  background-color: #ef4444 !important; /* Tailwind red-500 */
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1) !important;
  /* Explicitly disable all animations and transitions */
  animation: none !important;
  transition: none !important;
  transform: none !important;
}

.notification-badge-static:hover {
  /* Remove hover effects that might cause movement */
  transform: none !important;
  animation: none !important;
}

@media (max-width: 1024px) {
  nav {
    top: 3px;
    margin-left: 1rem;
    margin-right: 1rem;
  }
}

@media (max-width: 768px) {
  nav {
    top: 2px;
    margin-left: 0.5rem;
    margin-right: 0.5rem;
  }
}

@media (max-width: 640px) {
  nav {
    margin-left: 0.25rem;
    margin-right: 0.25rem;
  }
}

nav {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-10px); }
  to { opacity: 1; transform: translateY(0); }
}

@supports (-webkit-backdrop-filter: none) or (backdrop-filter: none) {
  nav {
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
  }
}

html {
  scroll-behavior: smooth;
}

@supports (-webkit-touch-callout: none) {
  nav {
    transform: translateZ(0);
    -webkit-font-smoothing: antialiased;
  }
}

@-moz-document url-prefix() {
  nav {
    will-change: transform;
    backface-visibility: hidden;
  }
}

* {
  -webkit-tap-highlight-color: transparent;
}

:focus-visible {
  outline: 2px solid white;
  outline-offset: 2px;
}

@media print {
  nav {
    display: none;
  }
}

/* Toast animation styles */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
/* Transition effects */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
  overflow: hidden;
}

.slide-down-enter-from,
.slide-down-leave-to {
  max-height: 0;
  opacity: 0;
  transform: translateY(-10px);
}

/* Smooth transitions for dropdowns */
.dropdown-link {
  transition: all 0.3s ease;
}

/* Ensure dropdowns appear above other content */
.z-\[9999\] {
  z-index: 9999;
}

/* Mobile menu transitions */
.md\:hidden {
  transition: opacity 0.3s ease, visibility 0.3s ease;
}
</style>