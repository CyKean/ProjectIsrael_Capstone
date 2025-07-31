<template>
  <nav class="fixed top-2 mx-4 left-0 right-0 bg-gradient-to-r from-[#00A572] to-[#008F61] backdrop-blur-md bg-opacity-95 shadow-lg z-50 rounded-xl border border-transparent border-t-[3px] border-t-orange-400 ">
    <div class="max-w-[1920px] mx-auto px-4 lg:px-6 py-2.5">
      <!-- Top row with logo and profile -->
      <div class="flex items-center justify-between">
        <!-- Logo and PROJECT ISRAEL text - positioned with padding-top -->
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

        <!-- User Profile Section with Connection Status and Notification Icons -->
        <div class="flex items-center group w-[180px] justify-end">
          <span class="text-xs text-white mr-2 hidden md:block opacity-90 group-hover:opacity-100 transition-opacity">{{ user?.email }}</span>

          <!-- WebSocket Connection Status -->
          <div class="relative mr-2">
            <button
              class="relative flex items-center justify-center h-7 w-7 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-300"
              @mouseenter="showWebSocketTooltip = true"
              @mouseleave="showWebSocketTooltip = false"
            >
              <div class="flex items-center justify-center size-full rounded-full" :class="isWebSocketConnected ? 'bg-green-500/20' : ''">
                <Zap class="h-3.5 w-3.5 text-white" />
              </div>
            </button>

            <!-- Enhanced WebSocket Tooltip - Minimalist Design -->
            <div
              v-show="showWebSocketTooltip"
              class="absolute right-0 top-full mt-2 w-52 bg-white/95 backdrop-blur-md rounded-lg shadow-lg overflow-hidden z-50 transition-all duration-200 border border-gray-100 transform origin-top-right"
              :class="showWebSocketTooltip ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
            >
              <div class="p-3">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center">
                    <div class="w-2 h-2 rounded-full mr-2" :class="isWebSocketConnected ? 'bg-green-500' : 'bg-red-500'"></div>
                    <h3 class="font-medium text-sm text-gray-800">WebSocket</h3>
                  </div>
                  <Zap class="h-4 w-4 text-[#00A572]" />
                </div>

                <div v-if="isWebSocketConnected" class="space-y-2.5">
                  <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-500">Status</span>
                    <span class="font-medium text-gray-800">Connected</span>
                  </div>

                  <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-500">Latency</span>
                    <span class="font-medium text-gray-800">{{ wsLatency }}ms</span>
                  </div>

                  <div class="flex justify-between items-center text-xs">
                    <span class="text-gray-500">Uptime</span>
                    <span class="font-medium text-gray-800">{{ wsUptime }}</span>
                  </div>

                </div>

                <div v-else class="flex items-center justify-center py-2">
                  <span class="text-xs text-red-500 font-medium">Disconnected</span>
                </div>
              </div>
            </div>
          </div>

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

            <!-- Enhanced WiFi Tooltip - Minimalist Design -->
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

          <!-- Notification Icon with Enhanced Minimalist Badge -->
          <div class="relative">
            <router-link
              to="/app/notifications"
              class="relative flex items-center justify-center h-8 w-8 rounded-full bg-white/10 hover:bg-white/20 transition-all duration-300 text-white group/bell"
              :class="{ 'bg-white/30': $route.path === '/notifications' }"
              @mouseenter="showNotificationTooltip = true"
              @mouseleave="showNotificationTooltip = false"
            >
              <Bell class="h-4 w-4 transition-transform duration-200 group-hover/bell:scale-110" />

              <!-- Enhanced Minimalist Notification Badge - Completely Static -->
              <div
                v-if="unreadNotificationCount > 0"
                class="notification-badge-static absolute -top-1 -right-1 min-w-[16px] h-4 flex items-center justify-center rounded-full bg-red-500 text-white shadow-md border border-white/30"
              >
                <span class="text-[9px] font-semibold leading-none px-0.5">
                  {{ unreadNotificationCount > 99 ? '99+' : unreadNotificationCount }}
                </span>
              </div>
            </router-link>

            <!-- Ultra Small Notification Tooltip - Compact and Readable -->
            <!-- Custom Small Notification Tooltip -->
            <div
              v-show="showNotificationTooltip"
              class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 bg-green-100 text-green-900 font-medium text-[10px] rounded-md whitespace-nowrap z-50 transition-all duration-200 shadow-sm"
              :class="showNotificationTooltip ? 'opacity-100' : 'opacity-0'"
            >
              Notifications
              <!-- Custom small tooltip arrow -->
              <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-green-100"></div>
            </div>

            <!-- Notification Panel -->
            <!-- <div
              v-show="showNotifications"
              class="absolute right-0 top-full mt-2 w-80 origin-top-right bg-white rounded-lg shadow-lg overflow-hidden z-50 border border-gray-100 transform transition-all duration-200"
              :class="notificationAnimation"
            >
              <div class="p-3 bg-gradient-to-r from-[#00A572] to-[#008F61] text-white">
                <div class="flex items-center justify-between">
                  <div class="flex items-center gap-2">
                    <Bell class="h-4 w-4" />
                    <h3 class="font-medium">Notifications</h3>
                  </div>
                  <div class="flex items-center gap-2">
                    <span
                      v-if="notifications && notifications.length"
                      class="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-orange-500 text-[10px] font-bold text-white"
                    >
                      {{ notifications.filter(n => n && !n.read).length }}
                    </span>

                    <button
                      @click.stop="markAllAsRead"
                      class="text-xs px-1.5 py-0.5 bg-white/10 hover:bg-white/20 rounded-md transition-colors"
                      title="Mark all as read"
                    >
                      <Check class="h-3 w-3" />
                    </button>
                  </div>
                </div>
              </div>

              <div class="max-h-[350px] overflow-y-auto">
                <div v-if="notifications.filter(n => n).length === 0" class="p-4 text-center text-gray-500">
                  <BellOff class="h-6 w-6 mx-auto mb-2 text-gray-400" />
                  <p class="text-sm">No notifications</p>
                </div>

                <div v-else>
                  <div v-if="todayNotifications.filter(n => n).length > 0">
                    <div class="px-3 py-1.5 bg-gray-50 border-y border-gray-100">
                      <span class="text-xs font-medium text-gray-500">Today</span>
                    </div>
                    <div
                      v-for="notification in todayNotifications.filter(n => n)"
                      :key="notification.id"
                      class="p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer"
                      :class="{ 'bg-blue-50/50': notification && !notification.read }"
                      @click="markAsRead(notification.id)"
                    >
                      <div class="flex items-start gap-3">
                        <div
                          class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
                          :class="getNotificationTypeClass(notification.type).bgColor"
                        >
                          <component
                            :is="getNotificationTypeClass(notification.type).icon"
                            class="h-4 w-4 text-white"
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium text-gray-900 mb-0.5">{{ notification.title }}</p>
                          <p class="text-xs text-gray-500 mb-1">{{ notification.message }}</p>
                          <div class="flex items-center justify-between">
                            <span class="text-xs text-gray-400">{{ formatTime(notification.time) }}</span>
                            <div v-if="notification && !notification.read" class="h-2 w-2 rounded-full bg-blue-500"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div v-if="earlierNotifications.filter(n => n).length > 0">
                    <div class="px-3 py-1.5 bg-gray-50 border-y border-gray-100">
                      <span class="text-xs font-medium text-gray-500">Earlier</span>
                    </div>
                    <div
                      v-for="notification in earlierNotifications.filter(n => n)"
                      :key="notification.id"
                      class="p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors cursor-pointer"
                      :class="{ 'bg-blue-50/50': notification && !notification.read }"
                      @click="markAsRead(notification.id)"
                    >
                      <div class="flex items-start gap-3">
                        <div
                          class="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center"
                          :class="getNotificationTypeClass(notification.type).bgColor"
                        >
                          <component
                            :is="getNotificationTypeClass(notification.type).icon"
                            class="h-4 w-4 text-white"
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <p class="text-sm font-medium text-gray-900 mb-0.5">{{ notification.title }}</p>
                          <p class="text-xs text-gray-500 mb-1">{{ notification.message }}</p>
                          <div class="flex items-center justify-between">
                            <span class="text-xs text-gray-400">{{ formatTime(notification.time) }}</span>
                            <div v-if="notification && !notification.read" class="h-2 w-2 rounded-full bg-blue-500"></div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="p-2 bg-gray-50 border-t border-gray-100 flex justify-between items-center">
                <a href="/notifications" class="text-xs text-[#00A572] font-medium hover:underline">
                  View all notifications
                </a>
                <button
                  @click.stop="showNotifications = false"
                  class="text-xs px-2 py-1 text-gray-500 hover:bg-gray-200 rounded transition-colors"
                >
                  Close
                </button>
              </div>
            </div> -->
          </div>

          <!-- Profile Dropdown - Modified Section -->
          <div class="relative ml-4">
            <button
              class="relative cursor-pointer group/profile"
              @click="toggleProfileDropdown"
              @mouseenter="showProfileTooltip = true"
              @mouseleave="showProfileTooltip = false"
            >
              <!-- Profile Image with Ultra Clean Design -->
              <div class="relative">
                <div
                  class="w-8 h-8 rounded-full overflow-hidden transition-all duration-300 ease-out group-hover/profile:scale-[1.02]"
                  :class="[
                    isOnProfilePage || isProfileDropdownOpen
                      ? 'ring-1 ring-green-400/60 ring-offset-1 ring-offset-white/20'
                      : 'ring-1 ring-white/15 hover:ring-white/25',
                    user?.avatar?.icon ? 'bg-white flex items-center justify-center' : '' // Add background for emoji
                  ]"
                >
                  <span v-if="user?.avatar?.icon" class="text-lg leading-none select-none">{{ user.avatar.icon }}</span>
                  <img v-else-if="user?.profilePicture"
                       :src="user.profilePicture"
                       class="w-full h-full object-cover transition-all duration-300"
                       :class="isOnProfilePage || isProfileDropdownOpen ? 'brightness-[1.02] saturate-[1.05]' : ''"
                       alt="Profile"/>
                  <img v-else
                       src="/public/images/profile.jpg"
                       class="w-full h-full object-cover transition-all duration-300"
                       alt="Profile"/>

                  <!-- Ultra Subtle Active Overlay -->
                  <div
                    v-if="isOnProfilePage || isProfileDropdownOpen"
                    class="absolute inset-0 bg-gradient-to-br from-green-400/8 via-transparent to-transparent"
                  ></div>
                </div>

                <!-- Micro Active Indicator -->
                <div
                  v-if="isOnProfilePage || isProfileDropdownOpen"
                  class="absolute -bottom-px -right-px w-2 h-2 bg-green-400 rounded-full border border-white/40 shadow-sm"
                ></div>
              </div>

              <!-- Small Profile Tooltip -->
              <div
                v-show="showProfileTooltip && !isProfileDropdownOpen"
                class="absolute top-full left-1/2 transform -translate-x-1/2 mt-1 px-2 py-0.5 bg-green-100 text-green-800 text-[10px] font-medium rounded-md whitespace-nowrap z-50 transition-all duration-200 shadow-sm"
                :class="showProfileTooltip ? 'opacity-100' : 'opacity-0'"
              >
                Profile
                <!-- Custom small tooltip arrow -->
                <div class="absolute bottom-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-green-100"></div>
              </div>
            </button>

            <!-- Profile Dropdown Menu -->
            <div
              v-show="isProfileDropdownOpen"
              class="absolute right-0 top-full mt-2 w-48 bg-white/95 backdrop-blur-md rounded-lg shadow-lg overflow-hidden z-50 border border-gray-100 transform transition-all duration-200"
              :class="isProfileDropdownOpen ? 'scale-100 opacity-100' : 'scale-95 opacity-0'"
            >
              <!-- Profile Header -->
              <div class="p-3 bg-gradient-to-r from-[#00A572] to-[#008F61] text-white">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full overflow-hidden bg-white/20">
                    <span v-if="user?.avatar?.icon" class="text-lg leading-none select-none flex items-center justify-center w-full h-full">{{ user.avatar.icon }}</span>
                    <img v-else-if="user?.profilePicture"
                         :src="user.profilePicture"
                         class="w-full h-full object-cover"
                         alt="Profile"/>
                    <img v-else
                         src="/public/images/profile.jpg"
                         class="w-full h-full object-cover"
                         alt="Profile"/>
                  </div>
                  <div class="flex-1 min-w-0">
                    <p class="text-sm font-medium" :title="user?.name || 'Unknown User'">{{ truncateText(user?.name || 'Unknown User', 13) }}</p>
                    <p class="text-xs text-white/80" :title="user?.phoneNumber || '+63...........'">{{ truncateText(user?.phoneNumber || '+63...........', 15) }}</p>
                  </div>
                </div>
              </div>

              <!-- Dropdown Options -->
              <div class="py-1">
                <!-- Profile Option -->
                <button
                  @click="goToProfile"
                  class="w-full flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-[#E8F5E9] hover:text-[#00A572] transition-all duration-200"
                  :class="isOnProfilePage ? 'bg-[#E8F5E9] text-[#00A572] font-medium' : ''"
                >
                  <svg class="h-4 w-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
                  </svg>
                  Profile
                </button>

                <!-- Recalibration Option -->
                <button
                  @click="goToRecalibration"
                  class="w-full flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-[#E8F5E9] hover:text-[#00A572] transition-all duration-200"
                  :class="$route.path === '/app/recalibration' ? 'bg-[#E8F5E9] text-[#00A572] font-medium' : ''"
                >
                  <Cog class="h-4 w-4 mr-3" />
                  Recalibration
                </button>

                <!-- FAQ Option -->
                <button
                  @click="goToFAQ"
                  class="w-full flex items-center px-3 py-2 text-sm text-gray-700 hover:bg-[#E8F5E9] hover:text-[#00A572] transition-all duration-200"
                  :class="$route.path === '/faq' ? 'bg-[#E8F5E9] text-[#00A572] font-medium' : ''"
                >
                  <svg class="h-4 w-4 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  FAQ
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation items centered -->
      <div class="flex items-center justify-center mt-1.5">
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
    </div>
  </nav>
  

  <!-- Spacer for content below navbar -->
  <div class="h-20"></div>

  <!-- Click outside handlers -->
  <div
    v-if="showNotifications"
    class="fixed inset-0 z-40"
    @click="showNotifications = false"
  ></div>
  
  <div
    v-if="isProfileDropdownOpen"
    class="fixed inset-0 z-40"
    @click="isProfileDropdownOpen = false"
  ></div>
  
  <Transition name="toast">
    <div
      v-if="showToast"
      :class="[
        'fixed bottom-4 right-4 rounded-lg shadow-lg border p-4 flex items-center gap-3 z-[10001] max-w-md',
        toastStyles.bg,
        toastStyles.border
      ]"
    >
      <div :class="[toastStyles.iconBg, 'p-2 rounded-full']">
        <component :is="toastStyles.icon" class="w-5 h-5" :class="toastStyles.iconColor" />
      </div>
      <div>
        <p class="text-sm font-medium text-gray-800">{{ toastMessage }}</p>
      </div>
      <button
        @click="showToast = false"
        class="ml-auto text-gray-400 hover:text-gray-600"
      >
        <X class="w-4 h-4" />
      </button>
    </div>
  </Transition>

</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  LayoutDashboard, Brain, Cpu, Database, Sprout, ChevronDown,
  Droplets, Thermometer, Gauge, Power, Cloud, Bell, Wifi, Zap,
  CheckCircle, Info, AlertTriangle, XCircle, X, Cog, Beaker
} from 'lucide-vue-next'
import api from '../../api/index.js'
import {
  getFirestore, collection, addDoc, query, orderBy, limit,
  doc, getDoc, updateDoc, serverTimestamp, onSnapshot
} from 'firebase/firestore'
import { useUserStore } from '../../utils/user.js'
import { auth } from '../../api/firebase.js'

const db = getFirestore()
const route = useRoute()
const router = useRouter()
const userStore = useUserStore();
const user = computed(() => userStore.user)

// UI State
const isSensorDropdownOpen = ref(false)
const isProfileDropdownOpen = ref(false)
const showWifiTooltip = ref(false)
const showWebSocketTooltip = ref(false)
const showNotificationTooltip = ref(false)
const showProfileTooltip = ref(false)
const showNotifications = ref(false)
const isWebSocketConnected = ref(false)
const wifiStrength = ref(100)
const wifiNetwork = ref('Unknown')
const ipAddress = ref('')

// Notification State
const notifications = ref([])
const waterLevel = ref(0)
const showToast = ref(false)
const toastMessage = ref('')
const toastSeverity = ref('info')
const toastQueue = ref([])
const isToastActive = ref(false)

// Tracking State
const sentNotifications = ref(new Set())
const processingNotifications = ref(new Set())
const lastSmsSentTime = ref(0)
const SMS_RATE_LIMIT_MS = 60000 // 1 minute
let unsubscribeWaterLevel = null
let unsubscribeSoilMoisture = null

// Utility Functions
const truncateText = (text, maxLength) => text?.length <= maxLength ? text : text?.substring(0, maxLength) + '...'
const getSignalStrengthClass = (strength) => strength >= 70 ? 'bg-green-500' : strength >= 40 ? 'bg-yellow-500' : 'bg-red-500'
const isCurrentRoute = (path) => route.path === path
const isInSensorRoutes = computed(() => sensorTypes.some(sensor => route.path === sensor.href))
const isOnProfilePage = computed(() => route.name === 'UserProfile' || route.path.includes('/profile'))
const unreadNotificationCount = computed(() => notifications.value.filter(n => n && !n.read).length)

// SMS Functions
const formatPhoneNumber = (phone) => {
  if (!phone) return null;
  const cleaned = phone.toString().replace(/\D/g, '');
  
  // Philippine numbers
  if (cleaned.length === 11 && cleaned.startsWith('0')) return `+63${cleaned.substring(1)}`;
  if (cleaned.length === 10 && cleaned.startsWith('9')) return `+63${cleaned}`;
  if (cleaned.length === 12 && cleaned.startsWith('63')) return `+${cleaned}`;
  
  // International numbers
  if (cleaned.startsWith('+') && cleaned.length >= 11) return phone;
  
  console.warn('Unrecognized phone format:', phone);
  return null;
};

const sendSMS = async (phone, message) => {
  if (!phone) {
    console.warn('No phone number provided');
    return false;
  }

  // Rate limiting
  const now = Date.now();
  if (now - lastSmsSentTime.value < SMS_RATE_LIMIT_MS) {
    console.warn('SMS rate limit exceeded');
    return false;
  }

  const formattedPhone = formatPhoneNumber(phone);
  if (!formattedPhone) {
    console.error('Invalid phone number:', phone);
    return false;
  }

  try {
    console.log('Sending SMS:', { number: formattedPhone, message });
    const response = await api.post('/sms/send-sms', { 
      number: formattedPhone,
      message 
    }, { timeout: 10000 });

    console.log('SMS sent successfully');
    lastSmsSentTime.value = now;
    return true;
  } catch (error) {
    console.error('SMS failed:', {
      status: error.response?.status,
      data: error.response?.data,
      message: error.message
    });
    showToastMessage('Failed to send SMS', 'warning');
    return false;
  }
};

// Notification System
const generateNotificationId = (type, identifier) => `${type}-${identifier}`;

const toastStyles = computed(() => ({
  success: { icon: CheckCircle, iconColor: 'text-green-600', iconBg: 'bg-green-100', bg: 'bg-white', border: 'border-green-200' },
  info: { icon: Info, iconColor: 'text-blue-600', iconBg: 'bg-blue-100', bg: 'bg-white', border: 'border-blue-200' },
  warning: { icon: AlertTriangle, iconColor: 'text-yellow-600', iconBg: 'bg-yellow-100', bg: 'bg-white', border: 'border-yellow-200' },
  critical: { icon: XCircle, iconColor: 'text-red-600', iconBg: 'bg-red-100', bg: 'bg-white', border: 'border-red-200' },
  failed: { icon: XCircle, iconColor: 'text-gray-600', iconBg: 'bg-gray-100', bg: 'bg-white', border: 'border-gray-300' }
})[toastSeverity.value] || toastStyles.value.info);

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

const showToastMessage = (message, severity = 'info') => {
  toastQueue.value.push({ message, severity });
  if (!isToastActive.value) processToastQueue();
};

const sendNotification = async (message, title, severity = 'info', uniqueKey = null) => {
  const notificationId = uniqueKey || generateNotificationId(severity, message);
  
  if (sentNotifications.value.has(notificationId)) {
    console.log('Skipping duplicate:', notificationId);
    return;
  }
  if (processingNotifications.value.has(notificationId)) {
    console.log('Already processing:', notificationId);
    return;
  }

  processingNotifications.value.add(notificationId);

  try {
    // Show toast
    showToastMessage(message, severity);

    // Save to Firestore
    await addDoc(collection(db, 'notifications'), {
      id: notificationId,
      message,
      title,
      type: 'system',
      severity,
      read: false,
      timestamp: serverTimestamp(),
    });

    sentNotifications.value.add(notificationId);
    
    // Send SMS based on rules
    if (user.value?.phoneNumber) {
      if (severity === 'critical') {
        await sendSMS(user.value.phoneNumber, `[URGENT] ${title}: ${message}`);
      } else if (severity === 'warning' && user.value.notifyWarnings !== false) {
        await sendSMS(user.value.phoneNumber, `[Warning] ${title}: ${message}`);
      }
    }
  } catch (error) {
    console.error('Notification error:', error);
  } finally {
    processingNotifications.value.delete(notificationId);
  }
};

// Water Level Monitoring
const setupWaterLevelListener = () => {
  if (unsubscribeWaterLevel) unsubscribeWaterLevel();

  const waterLevelQuery = query(
    collection(db, "water_level_readings"),
    orderBy("timestamp", "desc"),
    limit(1)
  );
  
  unsubscribeWaterLevel = onSnapshot(waterLevelQuery, (snapshot) => {
    if (!snapshot.empty) {
      const data = snapshot.docs[0].data();
      const level = data.waterLevel ?? data.level ?? data.value;
      
      if (typeof level === 'number') {
        waterLevel.value = level;
        evaluateWaterLevel(level);
      }
    }
  }, (error) => {
    console.error("Water level error:", error);
  });
};

const evaluateWaterLevel = async (level) => {
  console.log(`Water level: ${level}%`);
  
  if (typeof level !== 'number' || level < 0 || level > 100) {
    console.warn('Invalid water level:', level);
    return;
  }

  try {
    if (level <= 15) {
      await sendNotification(
        `Water level CRITICALLY LOW (${level}%)! Take action now.`,
        '🚨 Emergency Alert',
        'critical',
        `water-critical-${Math.floor(level)}`
      );
    } 
    else if (level <= 30) {
      await sendNotification(
        `Water level low (${level}%). Consider refilling.`,
        'Low Water Alert',
        'warning',
        `water-warning-${Math.floor(level)}`
      );
    }
    else if (level === 50) {
      await sendNotification(
        'Water level at 50%',
        'Water Update',
        'info',
        'water-info-50'
      );
    }
  } catch (error) {
    console.error('Water alert failed:', error);
  }
};

// Soil Moisture Monitoring
const setupSoilMoistureListener = () => {
  if (unsubscribeSoilMoisture) unsubscribeSoilMoisture();

  const soilQuery = query(
    collection(db, "3sensor_readings", "esp32-2", "readings"),
    orderBy("timestamp", "desc"),
    limit(1)
  );
  
  unsubscribeSoilMoisture = onSnapshot(soilQuery, (snapshot) => {
    if (!snapshot.empty) {
      const data = snapshot.docs[0].data();
      if (typeof data.soilMoisture === 'number') {
        evaluateSoilMoisture(data.soilMoisture);
      }
    }
  });
};

const evaluateSoilMoisture = async (level) => {
  try {
    if (level <= 10) {
      await sendNotification(
        `Soil CRITICALLY DRY (${level}%)! Watering needed.`,
        '🚨 Soil Alert',
        'critical',
        `soil-critical-${Math.floor(level)}`
      );
    } 
    else if (level <= 20) {
      await sendNotification(
        `Soil dry (${level}%). Consider watering.`,
        'Soil Alert',
        'warning',
        `soil-warning-${Math.floor(level)}`
      );
    }
  } catch (error) {
    console.error('Soil alert failed:', error);
  }
};

// Navigation Functions
const goToRecalibration = () => {
  isProfileDropdownOpen.value = false;
  router.push('/app/recalibration');
};

const goToFAQ = () => {
  isProfileDropdownOpen.value = false;
  router.push('/faq');
};

const toggleProfileDropdown = () => {
  isProfileDropdownOpen.value = !isProfileDropdownOpen.value;
  if (isProfileDropdownOpen.value) showProfileTooltip.value = false;
};

const goToProfile = () => {
  isProfileDropdownOpen.value = false;
  router.push({ name: 'UserProfile' });
};

const toggleSensorDropdown = () => {
  isSensorDropdownOpen.value = !isSensorDropdownOpen.value;
};

// UI Handlers
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

// Lifecycle Hooks
onMounted(async () => {
  document.addEventListener('click', closeDropdown);
  window.addEventListener('resize', handleResize);

  // Get IP
  try {
    const res = await fetch('https://api.ipify.org?format=json');
    ipAddress.value = (await res.json()).ip;
  } catch {
    ipAddress.value = 'Unknown';
  }

  // Network info
  if ('connection' in navigator) {
    const conn = navigator.connection;
    const updateWifi = () => {
      wifiStrength.value = conn.downlinkMax ? Math.min(conn.downlinkMax * 10, 100) : 70;
      wifiNetwork.value = conn.effectiveType || 'WiFi';
    };
    updateWifi();
    conn.addEventListener?.('change', updateWifi);
  }

  // Wait for user auth before setting up listeners
  const unwatch = watch(() => user.value, (newUser) => {
    if (newUser) {
      unwatch();
      setupWaterLevelListener();
      setupSoilMoistureListener();
    }
  }, { immediate: true });
});

onBeforeUnmount(() => {
  document.removeEventListener('click', closeDropdown);
  window.removeEventListener('resize', handleResize);
  if (unsubscribeWaterLevel) unsubscribeWaterLevel();
  if (unsubscribeSoilMoisture) unsubscribeSoilMoisture();
});

watch(() => route.path, () => {
  isSensorDropdownOpen.value = false;
  isProfileDropdownOpen.value = false;
  showNotifications.value = false;
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
</style>