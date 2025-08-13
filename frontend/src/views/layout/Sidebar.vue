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
import axios from 'axios'
import { eventBus } from '../../eventBus'
import { sendPushNotification } from '../../utils/notify.js'
import { initWaterStream, onWaterLevelUpdate } from '../../utils/water.js'
import { getWeatherData, mapWeatherCode } from '../../utils/weather.js'
import api from '../../api/index.js'
import {
  getFirestore,
  collection,
  addDoc,
  getDocs,
  query,
  orderBy,
  limit,
  doc,
  setDoc,
  Timestamp,
  serverTimestamp,
  getDoc,
  updateDoc,
  deleteDoc,
  where,
  getDocsFromServer,
  onSnapshot
} from 'firebase/firestore'
import { useUserStore } from '../../utils/user.js'
import { onAuthStateChanged } from 'firebase/auth'
import { auth } from '../../api/firebase.js'

const db = getFirestore()
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
const unreadNotificationCount = computed(() => notifications.value.filter(n => n && !n.read).length);

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
    return localStorage.getItem(fullKey) === 'saved' || await this.checkFirestore(notificationKey);
  },

  // Check Firestore as fallback
  async checkFirestore(notificationKey) {
    try {
      const q = query(
        collection(db, 'notifications'),
        where('uniqueKey', '==', notificationKey),
        where('timestamp', '>=', startOfToday())
      );
      const snapshot = await getDocs(q);
      return !snapshot.empty;
    } catch (error) {
      console.error('Error checking notification:', error);
      return false;
    }
  },

  // Clean old localStorage entries (older than 1 day)
  cleanOldEntries() {
    const oneDayAgo = Date.now() - 24 * 60 * 60 * 1000;
    Object.keys(localStorage).forEach(key => {
      if (key.startsWith('notification-')) {
        const timestamp = parseInt(key.split('-').pop());
        if (timestamp && timestamp < oneDayAgo) {
          localStorage.removeItem(key);
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
  
  // Fallback to Firestore check
  try {
    const q = query(
      collection(db, 'notifications'),
      where('uniqueKey', '==', notificationKey),
      where('timestamp', '>=', startOfToday())
    );
    const snapshot = await getDocs(q);
    return !snapshot.empty;
  } catch (error) {
    console.error('Error checking notification:', error);
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
  // Generate consistent notification ID
  const notificationId = uniqueKey || `${severity}-${title}-${message}`.replace(/\s+/g, '-').toLowerCase();
  const todayKey = new Date().toISOString().split('T')[0];
  const storageKey = `${notificationId}-${todayKey}`;

  // Check if we've already processed this notification today
  const notificationState = notificationStorage.get(storageKey);
  
  // If already fully processed, skip everything
  if (notificationState === 'complete') {
    return;
  }

  // Show toast only if not shown today
  if (!notificationState) {
    showToastMessage(message, severity);
    notificationStorage.set(storageKey, 'toast-shown');
  }

  // Skip Firestore if already saved today
  if (notificationState === 'toast-shown' || notificationState === 'complete' || await wasNotificationSavedToday(notificationId)) {
    if (notificationState === 'toast-shown') {
      notificationStorage.set(storageKey, 'complete');
    }
    return;
  }

  try {
    // Determine notification type and format data accordingly
    let formattedData = {};
    const now = new Date();
    
    if (title.includes('Water') || message.includes('water level')) {
      // Water Level Alert (Type 1)
      formattedData = {
        type: 'water-level',
        level: contextData.waterLevel || 'Unknown',
        status: contextData.waterLevel <= 15 ? 'Critical' : 
               contextData.waterLevel <= 30 ? 'Warning' : 'Normal',
        priority: contextData.waterLevel <= 15 ? 'High Priority' : 
                 contextData.waterLevel <= 30 ? 'Warning' : 'Info',
        recommendation: contextData.waterLevel <= 15 ? 
          'Immediate water refill required' : 
          'Schedule water refill within 24 hours',
        timestamp: serverTimestamp()
      };
    } 
    else if (title.includes('Temperature') || title.includes('Humidity')) {
      // Humidity/Temperature Alert (Type 2)
      formattedData = {
        type: 'climate',
        temperature: contextData.temperature ? `${contextData.temperature}°C` : 'Unknown',
        humidity: contextData.humidity ? `${contextData.humidity}%` : 'Unknown',
        soilMoisture: contextData.soilMoisture ? `${contextData.soilMoisture}%` : 'Unknown',
        recommendation: contextData.humidity > 70 ? 
          'High humidity - fungal disease risk' :
          contextData.temperature > 30 ?
          'High temperature - plant stress likely' :
          'Normal conditions',
        timestamp: serverTimestamp()
      };
    }
    else if (title.includes('Soil') && !title.includes('pH')) {
      // Soil Moisture Alert (Type 3 & 5)
      formattedData = {
        type: 'soil-moisture',
        moisture: contextData.soilMoisture ? `${contextData.soilMoisture}%` : 'Unknown',
        temperature: contextData.temperature ? `${contextData.temperature}°C` : 'Unknown',
        humidity: contextData.humidity ? `${contextData.humidity}%` : 'Unknown',
        waterLevel: contextData.waterLevel ? `${contextData.waterLevel}%` : 'Unknown',
        recommendation: contextData.soilMoisture < 20 ? 
          'Soil is dry - irrigation required' :
          contextData.soilMoisture > 55 ?
          'Soil is oversaturated - risk of root rot' :
          'Soil moisture is optimal',
        timestamp: serverTimestamp()
      };
    }
    else if (title.includes('NPK') || title.includes('pH')) {
      // NPK/Soil pH Alert (Type 4)
      formattedData = {
        type: 'nutrients',
        nitrogen: contextData.nitrogen ? {
          value: contextData.nitrogen,
          level: contextData.nitrogen < 51 ? 'Low' : 
                contextData.nitrogen > 200 ? 'High' : 'Optimal'
        } : null,
        phosphorus: contextData.phosphorus ? {
          value: contextData.phosphorus,
          level: contextData.phosphorus < 21 ? 'Low' : 
                contextData.phosphorus > 60 ? 'High' : 'Optimal'
        } : null,
        potassium: contextData.potassium ? {
          value: contextData.potassium,
          level: contextData.potassium < 101 ? 'Low' : 
                contextData.potassium > 250 ? 'High' : 'Optimal'
        } : null,
        soilPh: contextData.soilPh ? {
          value: contextData.soilPh,
          condition: contextData.soilPh < 5.5 ? 'Acidic' : 
                    contextData.soilPh > 7.5 ? 'Alkaline' : 'Neutral'
        } : null,
        recommendation: getNutrientRecommendation(contextData),
        timestamp: serverTimestamp()
      };
    }
    else if (title.includes('Watering') && (title.includes('Started') || title.includes('Completed'))) {
      // Water Scheduling Alert (Type 6)
      formattedData = {
        type: 'schedule',
        date: contextData.date || formatDate(now),
        startTime: contextData.startTime || now.toLocaleTimeString(),
        endTime: contextData.endTime || (contextData.duration ? 
          new Date(now.getTime() + contextData.duration * 60000).toLocaleTimeString() : 'Unknown'),
        duration: contextData.duration ? `${contextData.duration} minutes` : 'Unknown',
        waterLevelAtStart: contextData.waterLevel ? `${contextData.waterLevel}%` : 'Unknown',
        zone: contextData.zone || 'Greenhouse 1',
        mode: contextData.mode || 'auto',
        motorStatus: contextData.motorStatus || 'unknown',
        remarks: contextData.remarks || 'No remarks',
        timestamp: serverTimestamp()
      };
    }
    else {
      // Default format for other notifications
      formattedData = {
        type: 'general',
        ...cleanFirestoreData(contextData),
        timestamp: serverTimestamp()
      };
    }

    // Prepare notification data
    const notificationData = {
      message,
      title,
      type: 'system',
      severity,
      read: false,
      timestamp: serverTimestamp(),
      formattedDate: formatDate(now),
      context: formattedData,
      uniqueKey: notificationId
    };

    // Save to Firestore
    await addDoc(collection(db, 'notifications'), notificationData);
    
    // Mark as complete in storage
    notificationStorage.set(storageKey, 'complete');
    
    // Send SMS if configured and critical
    if (user.value?.phoneNumber && severity === 'critical') {
      await sendSMS(user.value.phoneNumber, `[URGENT] ${title}: ${message}`);
    }
  } catch (error) {
    console.error('Failed to save notification:', error);
    if (notificationStorage.get(storageKey)) {
      notificationStorage.set(storageKey, 'toast-shown');
    }
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
  // Clear any existing listener
  if (unsubscribeWaterLevel.value) {
    unsubscribeWaterLevel.value();
  }

  const waterLevelQuery = query(
    collection(db, "water_level_readings"),
    orderBy("timestamp", "desc"),
    limit(1)
  );
  
  unsubscribeWaterLevel.value = onSnapshot(waterLevelQuery, (snapshot) => {
    if (!snapshot.empty) {
      const doc = snapshot.docs[0];
      const waterData = doc.data();
      console.log("Water level data:", waterData); // Debug log
      
      // Make sure we're getting the waterLevel field
      if (waterData && typeof waterData.waterLevel === 'number') {
        const level = waterData.waterLevel;
        console.log("Current water level:", level); // Debug log
        waterLevel.value = level;
        evaluateWaterLevel(level);
      } else {
        console.warn("Water level data missing or invalid:", waterData);
      }
    } else {
      console.log("No water level documents found");
    }
  }, (error) => {
    console.error("Water level listener error:", error);
  });
};

// Helper function to get latest sensor data
const getLatestSensorData = async () => {
  try {
    const sensorSnapshot = await getDocs(
      query(
        collection(db, "3sensor_readings", "esp32-2", "readings"),
        orderBy("timestamp", "desc"),
        limit(1)
      )
    );
    return sensorSnapshot.empty ? {} : sensorSnapshot.docs[0].data();
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
    const dateKey = new Date().toISOString().split('T')[0];
    const formattedDate = formatDate(new Date());
    const sensorData = await getLatestSensorData();

    const context = {
      date: formattedDate,
      waterLevel: level,
      timestamp: serverTimestamp()
    };

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
    else if (level >= 45 && level <= 55) {
      await sendNotification(
        `Water level is at ${Math.round(level)}%`,
        'Water Level Update',
        'info',
        `water-info-${dateKey}`,
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

      // Prepare the context with detailed temperature data
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
        recordedAt: serverTimestamp()
      };

      // Prepare the clean toast message (without min/max temps)
      const toastMessage = `${condition} expected on ${dayFormattedDate}`;

      await sendNotification(
        toastMessage, // Clean message for toast
        'Severe Weather Alert',
        'warning',
        `weather-${condition}-${dateKey}`,
        context      // Detailed data saved in context
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
  // Clean up previous listener
  if (unsubscribeCombinedListener.value) unsubscribeCombinedListener.value();

  // Queries for latest readings
  const waterQuery = query(
    collection(db, "water_level_readings"),
    orderBy("timestamp", "desc"),
    limit(1)
  );
  const sensor1Query = query(
    collection(db, "3sensor_readings", "esp32-1", "readings"),
    orderBy("timestamp", "desc"),
    limit(1)
  );
  const sensor2Query = query(
    collection(db, "3sensor_readings", "esp32-2", "readings"),
    orderBy("timestamp", "desc"),
    limit(1)
  );

  // Helper to fetch latest data from all sources
  const fetchLatestCombinedData = async () => {
    const [waterSnap, sensor1Snap, sensor2Snap] = await Promise.all([
      getDocs(waterQuery),
      getDocs(sensor1Query),
      getDocs(sensor2Query)
    ]);
    const waterData = !waterSnap.empty ? waterSnap.docs[0].data() : {};
    const sensor1Data = !sensor1Snap.empty ? sensor1Snap.docs[0].data() : {};
    const sensor2Data = !sensor2Snap.empty ? sensor2Snap.docs[0].data() : {};
    return { waterData, sensor1Data, sensor2Data };
  };

  // Listener callback
  const onAnyChange = async () => {
    const { waterData, sensor1Data, sensor2Data } = await fetchLatestCombinedData();
    await evaluateSensorRangesAndNotify({ waterData, sensor1Data, sensor2Data });
  };

  // Set up listeners for all three sources
  const unsubWater = onSnapshot(waterQuery, onAnyChange);
  const unsubSensor1 = onSnapshot(sensor1Query, onAnyChange);
  const unsubSensor2 = onSnapshot(sensor2Query, onAnyChange);

  // Store cleanup function
  unsubscribeCombinedListener.value = () => {
    unsubWater();
    unsubSensor1();
    unsubSensor2();
  };
};

// Unified evaluation function for all ranges and sources
const evaluateSensorRangesAndNotify = async ({ waterData, sensorData, source }) => {
  if (!sensorData) {
    console.warn('No sensor data provided');
    return;
  }

  const now = new Date();
  const dateKey = now.toISOString().split('T')[0];
  const formattedDate = formatDate(now);

  // Prepare base context data
  const context = {
    source,
    date: formattedDate,
    timestamp: serverTimestamp(),
    waterLevel: typeof waterData?.waterLevel === 'number' ? waterData.waterLevel : null,
    ...sensorData
  };

  // Temperature Alerts
  if (typeof sensorData.temperature === 'number') {
    if (sensorData.temperature > 30) {
      await sendNotification(
        `High temperature (${sensorData.temperature}°C) detected`,
        'Temperature Alert',
        'warning',
        `temp-high-${source}-${dateKey}`,
        context
      );
    } else if (sensorData.temperature < 18) {
      await sendNotification(
        `Low temperature (${sensorData.temperature}°C) detected`,
        'Temperature Alert',
        'warning',
        `temp-low-${source}-${dateKey}`,
        context
      );
    }
  }

  // Humidity Alerts
  if (typeof sensorData.humidity === 'number') {
    if (sensorData.humidity > 70) {
      await sendNotification(
        `High humidity (${sensorData.humidity}%) detected`,
        'Humidity Alert',
        'warning',
        `humidity-high-${source}-${dateKey}`,
        context
      );
    } else if (sensorData.humidity < 40) {
      await sendNotification(
        `Low humidity (${sensorData.humidity}%) detected`,
        'Humidity Alert',
        'warning',
        `humidity-low-${source}-${dateKey}`,
        context
      );
    }
  }

  // Soil Moisture Alerts
  if (typeof sensorData.soilMoisture === 'number') {
    if (sensorData.soilMoisture <= 10) {
      await sendNotification(
        `CRITICALLY LOW soil moisture (${sensorData.soilMoisture}%)`,
        '🚨 Soil Emergency',
        'critical',
        `soil-critical-${source}-${dateKey}`,
        context
      );
    } else if (sensorData.soilMoisture <= 20) {
      await sendNotification(
        `Low soil moisture (${sensorData.soilMoisture}%)`,
        'Soil Moisture Alert',
        'warning',
        `soil-low-${source}-${dateKey}`,
        context
      );
    } else if (sensorData.soilMoisture > 55) {
      await sendNotification(
        `High soil moisture (${sensorData.soilMoisture}%)`,
        'Soil Moisture Alert',
        'warning',
        `soil-high-${source}-${dateKey}`,
        context
      );
    }
  }

  // Soil pH Alerts
  if (typeof sensorData.soilPh === 'number') {
    if (sensorData.soilPh < 5.5) {
      await sendNotification(
        `Low soil pH (${sensorData.soilPh}) - Acidic conditions`,
        'Soil pH Alert',
        'warning',
        `ph-low-${source}-${dateKey}`,
        context
      );
    } else if (sensorData.soilPh > 7.5) {
      await sendNotification(
        `High soil pH (${sensorData.soilPh}) - Alkaline conditions`,
        'Soil pH Alert',
        'warning',
        `ph-high-${source}-${dateKey}`,
        context
      );
    }
  }

  // NPK Nutrient Alerts
  const nutrientChecks = [
    { name: 'nitrogen', low: 51, high: 200 },
    { name: 'phosphorus', low: 21, high: 60 },
    { name: 'potassium', low: 101, high: 250 }
  ];

  for (const nutrient of nutrientChecks) {
    const value = sensorData[nutrient.name];
    if (typeof value !== 'number') continue;

    if (value < nutrient.low) {
      await sendNotification(
        `Low ${nutrient.name} (${value}ppm) detected`,
        `${nutrient.name.charAt(0).toUpperCase() + nutrient.name.slice(1)} Alert`,
        'warning',
        `${nutrient.name}-low-${source}-${dateKey}`,
        context
      );
    } else if (value > nutrient.high) {
      await sendNotification(
        `High ${nutrient.name} (${value}ppm) detected`,
        `${nutrient.name.charAt(0).toUpperCase() + nutrient.name.slice(1)} Alert`,
        'warning',
        `${nutrient.name}-high-${source}-${dateKey}`,
        context
      );
    }
  }
};

// UPDATED SCHEDULE FUNCTIONS WITH PRECISE TIMING
const setupScheduleListener = () => {
  console.log('[DEBUG] Setting up schedule listeners...');
  
  // Clean up any existing listeners
  if (unsubscribeSchedules.value) {
    unsubscribeSchedules.value();
  }

  const unsubscribers = [];
  
  const setupSubcollectionListener = (subcollection, mode) => {
    console.log(`[DEBUG] Setting up ${mode} schedule listener...`);
    
    const q = query(
      collection(db, 'watering_schedules', 'schedules_root', subcollection),
      orderBy('scheduledTime', 'asc')
    );
    
    const unsubscribe = onSnapshot(q, (snapshot) => {
      console.log(`[DEBUG] ${mode} schedules updated: ${snapshot.docs.length} schedules`);
      
      const updatedSchedules = snapshot.docs.map(doc => {
        const data = doc.data();
        const schedule = {
          id: doc.id,
          mode: mode,
          ...data,
          daysArray: convertDaysFormat(data.days)
        };
        
        // Convert scheduledTime to milliseconds
        if (mode === 'one-time') {
          // One-time schedules: convert to timestamp
          schedule.scheduledTime = data.scheduledTime < 1e12 ? data.scheduledTime * 1000 : data.scheduledTime;
        } else {
          // Daily/Weekly schedules: convert to milliseconds since midnight
          if (data.scheduledTime >= 86400000) {
            // If it's a full timestamp, extract time of day
            const date = new Date(data.scheduledTime);
            schedule.scheduledTime = date.getHours() * 3600000 + 
                                   date.getMinutes() * 60000 + 
                                   date.getSeconds() * 1000;
          } else {
            // Already in milliseconds since midnight format
            schedule.scheduledTime = data.scheduledTime;
          }
        }
        
        return schedule;
      });

      processScheduleUpdates(updatedSchedules, mode, snapshot.docChanges());
    }, (error) => {
      console.error(`Error in ${mode} schedule listener:`, error);
      showToastMessage(`Error loading ${mode} schedules`, 'error');
    });
    
    unsubscribers.push(unsubscribe);
  };

  setupSubcollectionListener('one_time', 'one-time');
  setupSubcollectionListener('weekly', 'weekly');
  setupSubcollectionListener('daily', 'daily');

  unsubscribeSchedules.value = () => {
    console.log('[DEBUG] Cleaning up schedule listeners...');
    unsubscribers.forEach(unsub => unsub());
  };
  
  console.log('[DEBUG] Schedule listeners set up successfully');
};

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

// Add caching for sensor data to avoid frequent Firestore reads
let sensorDataCache = {
  data: null,
  lastFetch: 0,
  cacheDuration: 60000 // Cache for 1 minute
};

const getCachedSensorData = async () => {
  const now = Date.now();
  
  // Return cached data if it's still fresh
  if (sensorDataCache.data && (now - sensorDataCache.lastFetch) < sensorDataCache.cacheDuration) {
    console.log('[DEBUG] Using cached sensor data');
    return sensorDataCache.data;
  }
  
  // Fetch fresh data if cache is expired or empty
  try {
    console.log('[DEBUG] Fetching fresh sensor data');
    const freshData = await fetchSensorData();
    sensorDataCache.data = freshData;
    sensorDataCache.lastFetch = now;
    return freshData;
  } catch (error) {
    console.error('Error fetching sensor data:', error);
    // Return cached data if available, even if expired
    return sensorDataCache.data || {};
  }
};

const checkSchedules = async () => {
  const now = new Date();
  const currentDay = (now.getDay() + 6) % 7; // 0=Monday to 6=Sunday
  const currentTimeMs = now.getHours() * 3600000 + 
                       now.getMinutes() * 60000 + 
                       now.getSeconds() * 1000 + 
                       now.getMilliseconds();

  // console.log(`[DEBUG] Checking schedules at ${now.toLocaleTimeString()}, Day: ${currentDay}`);

  // Only fetch sensor data when we actually need to start a schedule
  let contextData = null;

  try {
    for (const schedule of schedulesCache.value) {
      if (!schedule.notifyWatering || schedule.completed) continue;

      const scheduleKey = `${schedule.id}-${currentDay}`;
      
      // Skip if we already processed this schedule today
      if (lastProcessedScheduleTimes.value[scheduleKey]) {
        const lastProcessed = new Date(lastProcessedScheduleTimes.value[scheduleKey]);
        const todayStart = new Date(now);
        todayStart.setHours(0, 0, 0, 0);
        
        if (lastProcessed >= todayStart) {
          continue; // Already processed today
        }
      }

      let shouldRunToday = false;
      let isTimeMatch = false;

      if (schedule.mode === 'daily') {
        shouldRunToday = true;
        // For daily schedules, check if the current time matches exactly
        isTimeMatch = Math.abs(currentTimeMs - schedule.scheduledTime) < 1000; // 1-second window
        
        // console.log(`[DEBUG] Daily schedule ${schedule.id}: shouldRun=${shouldRunToday}, timeMatch=${isTimeMatch}, scheduledTime=${formatTimeDebug(schedule.scheduledTime, 'daily')}, currentTime=${formatTimeDebug(currentTimeMs, 'daily')}`);
        
      } else if (schedule.mode === 'weekly') {
        shouldRunToday = schedule.daysArray?.includes(currentDay) ?? false;
        // For weekly schedules, check if today is the right day AND time matches exactly
        isTimeMatch = shouldRunToday && Math.abs(currentTimeMs - schedule.scheduledTime) < 1000; // 1-second window
        
        // console.log(`[DEBUG] Weekly schedule ${schedule.id}: shouldRun=${shouldRunToday}, timeMatch=${isTimeMatch}, days=${schedule.daysArray}, currentDay=${currentDay}, scheduledTime=${formatTimeDebug(schedule.scheduledTime, 'weekly')}, currentTime=${formatTimeDebug(currentTimeMs, 'weekly')}`);
        
      } else if (schedule.mode === 'one-time') {
        const scheduleDate = new Date(schedule.scheduledTime);
        shouldRunToday = scheduleDate.toDateString() === now.toDateString();
        isTimeMatch = shouldRunToday && Math.abs(now.getTime() - schedule.scheduledTime) < 1000; // 1-second window
        
        // console.log(`[DEBUG] One-time schedule ${schedule.id}: shouldRun=${shouldRunToday}, timeMatch=${isTimeMatch}, scheduledTime=${scheduleDate.toLocaleString()}, currentTime=${now.toLocaleString()}`);
      }

      // Check if schedule should start
      if (shouldRunToday && isTimeMatch && !activeSchedules.value[schedule.id]) {
        console.log(`[DEBUG] ✅ Activating ${schedule.mode} schedule ${schedule.id} at ${now.toLocaleTimeString()}`);
        
        // Only fetch sensor data when we actually need it (when starting a schedule)
        if (!contextData) {
          contextData = await getCachedSensorData();
        }
        
        // Mark this schedule as processed for today
        lastProcessedScheduleTimes.value[scheduleKey] = now.getTime();
        
        activeSchedules.value[schedule.id] = {
          startTime: now.getTime(),
          duration: schedule.duration,
          mode: schedule.mode,
          currentDay: currentDay,
          scheduleKey: scheduleKey
        };
        
        await processScheduleStart(schedule, currentDay, contextData);
        
        // Calculate precise end time
        const endTime = now.getTime() + (schedule.duration * 60000);
        
        // Set timer for schedule completion (all schedule types need this)
        const timeUntilEnd = endTime - now.getTime();
        scheduleTimers.value[schedule.id] = setTimeout(async () => {
          if (activeSchedules.value[schedule.id]) {
            console.log(`[DEBUG] ⏰ Completing ${schedule.mode} schedule ${schedule.id} at ${new Date().toLocaleTimeString()}`);
            await processScheduleEnd(schedule, currentDay);
            await saveToHistory(schedule, new Date(), currentDay);
            delete activeSchedules.value[schedule.id];
            delete scheduleTimers.value[schedule.id];
            
            // For one-time schedules, mark as completed in Firestore
            if (schedule.mode === 'one-time') {
              try {
                const scheduleRef = doc(db, 'watering_schedules', 'schedules_root', 'one_time', schedule.id);
                await updateDoc(scheduleRef, { completed: true });
                console.log(`[DEBUG] Marked one-time schedule ${schedule.id} as completed`);
              } catch (error) {
                console.error('Error marking one-time schedule as completed:', error);
              }
            }
          }
        }, timeUntilEnd);
      }
    }
  } catch (error) {
    console.error('Schedule check error:', error);
    showToastMessage('Error checking watering schedules', 'error');
  }
};

// Update getDayName to match your system (0=Monday)
const getDayName = (dayNumber) => {
  const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  return dayNames[dayNumber] || 'Unknown';
};

const fetchLatestContextData = async () => {
  // Get latest water level
  const waterSnap = await getDocs(
    query(collection(db, "water_level_readings"), orderBy("timestamp", "desc"), limit(1))
  );
  const waterLevel = !waterSnap.empty ? waterSnap.docs[0].data().waterLevel : null;

  // Get latest sensor readings (esp32-2 preferred, fallback to esp32-1)
  const sensorSnap2 = await getDocs(
    query(collection(db, "3sensor_readings", "esp32-2", "readings"), orderBy("timestamp", "desc"), limit(1))
  );
  const sensorSnap1 = await getDocs(
    query(collection(db, "3sensor_readings", "esp32-1", "readings"), orderBy("timestamp", "desc"), limit(1))
  );
  const sensorData = !sensorSnap2.empty ? sensorSnap2.docs[0].data() : (!sensorSnap1.empty ? sensorSnap1.docs[0].data() : {});

  return {
    waterLevel: waterLevel,
    soilMoisture: sensorData.soilMoisture ?? null,
    humidity: sensorData.humidity ?? null,
    temperature: sensorData.temperature ?? null
  };
};

const processScheduleStart = async (schedule, currentDay, contextData) => {
  const now = new Date();
  const formattedTime = now.toLocaleString('en-US', {
    weekday: 'short', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });

  try {
    let typeLabel = '';
    let message = '';
    
    if (schedule.mode === 'one-time') {
      typeLabel = 'One-time';
      message = `One-time watering started at ${formattedTime}`;
    } else if (schedule.mode === 'daily') {
      typeLabel = 'Daily';
      message = `Daily watering started at ${formattedTime}`;
    } else if (schedule.mode === 'weekly') {
      typeLabel = 'Weekly';
      const dayName = getDayName(currentDay);
      message = `Weekly watering (${dayName}) started at ${formattedTime}`;
    }

    const dateKey = now.toISOString().split('T')[0];
    const notificationKey = `schedule-start-${schedule.id}-${dateKey}`;
    
    // Update motor status first to include in context
    const motorSuccess = await updateMotorStatus(true, schedule.id);
    
    await sendNotification(
      message,
      `${typeLabel} Watering Started`,
      'info',
      notificationKey,
      {
        ...contextData,
        scheduleType: schedule.mode,
        duration: schedule.duration,
        day: currentDay,
        scheduleId: schedule.id,
        motorStatus: motorSuccess ? 'activated' : 'failed',
        zone: schedule.zone || 'Greenhouse 1',
        mode: 'auto',
        startTime: formattedTime,
        remarks: motorSuccess ? 'Motor activated successfully' : 'Motor activation failed'
      }
    );

    if (!motorSuccess) {
      showToastMessage('Warning: Motor may not have started properly', 'warning');
    }

  } catch (error) {
    console.error(`Error starting schedule ${schedule.id}:`, error);
    showToastMessage(`Failed to start ${schedule.mode} watering schedule`, 'error');
  }
};

const processScheduleEnd = async (schedule, currentDay) => {
  const now = new Date();
  const formattedTime = now.toLocaleString('en-US', {
    weekday: 'short', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit', second: '2-digit'
  });

  try {
    const contextData = await fetchLatestContextData();
    
    let typeLabel = '';
    let message = '';
    
    if (schedule.mode === 'one-time') {
      typeLabel = 'One-time';
      message = `One-time watering completed at ${formattedTime}`;
    } else if (schedule.mode === 'daily') {
      typeLabel = 'Daily';
      message = `Daily watering completed at ${formattedTime}`;
    } else if (schedule.mode === 'weekly') {
      typeLabel = 'Weekly';
      const dayName = getDayName(currentDay);
      message = `Weekly watering (${dayName}) completed at ${formattedTime}`;
    }

    const dateKey = now.toISOString().split('T')[0];
    const notificationKey = `schedule-end-${schedule.id}-${dateKey}`;
    
    // Update motor status first to include in context
    const motorSuccess = await updateMotorStatus(false, schedule.id);
    
    await sendNotification(
      message,
      `${typeLabel} Watering Completed`,
      'success',
      notificationKey,
      {
        ...contextData,
        scheduleType: schedule.mode,
        duration: schedule.duration,
        day: currentDay,
        scheduleId: schedule.id,
        motorStatus: motorSuccess ? 'deactivated' : 'failed to stop',
        zone: schedule.zone || 'Greenhouse 1',
        mode: 'auto',
        endTime: formattedTime,
        remarks: motorSuccess ? 'Motor deactivated successfully' : 'Motor failed to stop'
      }
    );

    if (!motorSuccess) {
      showToastMessage('Warning: Motor may not have stopped properly', 'warning');
    }

  } catch (error) {
    console.error(`Error completing schedule ${schedule.id}:`, error);
    showToastMessage(`Failed to complete ${schedule.mode} watering schedule`, 'error');
  }
};

const saveToHistory = async (schedule, endTime, day) => {
  try {
    const historyData = {
      scheduleId: schedule.id,
      mode: schedule.mode,
      originalScheduledTime: schedule.scheduledTime,
      actualStartTime: activeSchedules.value[schedule.id]?.startTime || endTime.getTime(),
      completedAt: endTime.getTime(),
      duration: schedule.duration,
      days: schedule.days,
      dayOfWeek: schedule.mode === 'weekly' ? day : null,
      notifyWatering: schedule.notifyWatering,  
      skipIfRain: schedule.skipIfRain,
      waterFlowRate: schedule.waterFlowRate,
      createdAt: serverTimestamp()
    };
    
    await addDoc(
      collection(db, 'watering_schedules', 'schedules_root', 'history'),
      historyData
    );
  } catch (error) {
    console.error('Error saving to history:', error);
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

const fetchNotifications = () => {
  try {
    // Create a query that only gets unread notifications
    const q = query(
      collection(db, "notifications"),
      where("read", "==", false) // Assuming you have a 'read' boolean field in your documents
    );

    // Set up real-time listener
    const unsubscribe = onSnapshot(q, (querySnapshot) => {
      notifications.value = querySnapshot.docs.map(doc => ({
        id: doc.id,
        ...doc.data()
      }));
      console.log('Unread notifications count:', notifications.value.length);
    });

    // Return the unsubscribe function in case you need to stop listening later
    return unsubscribe;
  } catch (err) {
    console.error("Error setting up notifications listener:", err);
  }
};

// Lifecycle Hooks
onMounted(async () => {
  await fetchNotifications()
  document.addEventListener('click', closeDropdown);
  window.addEventListener('resize', handleResize);

  // const todayKey = new Date().toDateString();
  // notificationHistory.value[todayKey] = [];
  // const now = new Date();
  // const midnight = new Date(now);
  // midnight.setHours(24, 0, 0, 0);
  // const msUntilMidnight = midnight - now;

  // setTimeout(() => {
  //   notificationTracker.value.dailyCache = {};
  //   notificationTracker.value.lastCleanup = null;
  // }, msUntilMidnight);

  notificationStorage.cleanExpired();
  
  // Set up daily cleanup
  const now = new Date();
  const midnight = new Date(now);
  midnight.setHours(24, 0, 0, 0);
  const msUntilMidnight = midnight - now;

  setTimeout(() => {
    notificationStorage.cleanExpired();
    // Set up the next midnight cleanup
    setInterval(() => {
      notificationStorage.cleanExpired();
    }, 24 * 60 * 60 * 1000); // 24 hours
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
    if (unsubscribeSoilMoisture) unsubscribeSoilMoisture();
    if (unsubscribeWaterLevel.value) unsubscribeWaterLevel.value();
    if (unsubscribeSchedules.value) unsubscribeSchedules.value();
    if (scheduleCheckInterval.value) clearInterval(scheduleCheckInterval.value);
    if (weatherInterval) clearInterval(weatherInterval);
    Object.values(scheduleTimers.value).forEach(timer => clearTimeout(timer));
    // Remove old sensor listeners if present
    if (unsubscribeSensorListeners?.value?.esp32_1) unsubscribeSensorListeners.value.esp32_1();
    if (unsubscribeSensorListeners?.value?.esp32_2) unsubscribeSensorListeners.value.esp32_2();
    // Remove unified combined listener
    if (unsubscribeCombinedListener.value) unsubscribeCombinedListener.value();
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