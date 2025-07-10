<template>
  <nav class="fixed top-2 mx-4 left-0 right-0 bg-gradient-to-r from-[#00A572] to-[#008F61] backdrop-blur-md bg-opacity-95 shadow-lg z-50 rounded-xl border border-transparent border-t-[3px] border-t-orange-400">
    <div class="max-w-[1920px] mx-auto px-4 lg:px-6 py-2.5">
      <!-- Top row with logo and profile -->
      <div class="flex items-center justify-between">
        <!-- Logo and PROJECT ISRAEL text - positioned with padding-top -->
        <div class="flex items-center relative w-[180px]">
          <div class="bg-white rounded-full shadow-lg flex items-center justify-center overflow-hidden border-2 border-white/30 hover:border-white/50 transition-all duration-300" style="width: 2.8rem; height: 2.8rem;">
            <img
              src="/public/images/logo/logo-wot-text.png"
              alt="Project Israel"
              class="w-full h-full object-cover transform scale-[1.3] hover:scale-[1.8] transition-all duration-500 ease-out"
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
              to="/notifications"
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
                  : 'text-white hover:bg-white/10 hover:shadow-sm'
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
              class="absolute top-full left-0 mt-1 w-52 bg-white/95 backdrop-blur-md rounded-lg shadow-lg py-1.5 z-50 border border-white/20 transform transition-all duration-300"
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
  // Droplet, // Already imported
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

import { onAuthStateChanged } from 'firebase/auth'
import { auth } from '../../api/firebase.js'

const db = getFirestore()

const route = useRoute()
const router = useRouter()
const user = ref(null)
const isSensorDropdownOpen = ref(false)
const isProfileDropdownOpen = ref(false)
// Tooltip visibility states
const showWifiTooltip = ref(false)
const showWebSocketTooltip = ref(false)
const showRecalibrationTooltip = ref(false)
const showNotificationTooltip = ref(false)
const showProfileTooltip = ref(false)

// Notifications
const showNotifications = ref(false)
const notificationAnimation = ref('scale-95 opacity-0')

const isWebSocketConnected = ref(false)
const wsLatency = ref(0)
const wsUptime = ref('0m')
let wsStartTime = null
const wifiStrength = ref(100)
const wifiNetwork = ref('Unknown')
const ipAddress = ref('')

// Sample notifications data
const notifications = ref([])
const waterLevel = ref(0);
const sensorReadings = ref([]);

// Computed property for checking if user is on profile page
const isOnProfilePage = computed(() => {
  return route.name === 'UserProfile' || route.path === '/profile' || route.path.includes('/user-profile')
})

// Computed property for unread notification count
const unreadNotificationCount = computed(() => {
  return notifications.value.filter(n => n && !n.read).length;
});

// Provide the unread count to any child components that need it
provide('unreadNotificationCount', unreadNotificationCount);

const currentTime = ref(Date.now())
const savedSchedules = ref([])

const activeSchedules = new Map();
const notifiedStartIds = new Set()
const notifiedEndIds = new Set()
const processedSchedules = new Set()
const motorOnTriggered = new Set()
const motorOffTriggered = new Set()

// Keep track of previous states of schedules to detect changes for end notifications
const previousSchedulesMap = new Map();

// Toast handling
const showToast = ref(false)
const toastMessage = ref('')
const toastSeverity = ref('info')
const toastTimeout = ref(null)
const toastQueue = ref([]);
const isToastActive = ref(false);

const processingScheduleIds = ref(new Set());

const shownScheduleToasts = ref(new Set());
const motorOperationLock = ref(false);
const backendRequestQueue = ref([]);
const isProcessingQueue = ref(false);
const processedMotorRequests = ref(new Set());

const truncateText = (text, maxLength) => {
  if (!text) return '';
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength) + '...';
};

const sendSMS = async (phone, message) => {
  try {
    const response = await axios.post('http://127.0.0.1:8000/send-sms', {
      phone,
      message
    })
    console.log('✅ SMS sent:', response.data)
  } catch (error) {
    if (error.response) {
      console.error('❌ SMS send error:', error.response.data)
    } else {
      console.error('❌ SMS send error:', error)
    }
  }
}

// Function to navigate to recalibration page
const goToRecalibration = () => {
  isProfileDropdownOpen.value = false
  router.push('/app/recalibration')
}

// Function to navigate to FAQ page
const goToFAQ = () => {
  isProfileDropdownOpen.value = false
  router.push('/faq')
}

// Function to toggle profile dropdown
const toggleProfileDropdown = () => {
  isProfileDropdownOpen.value = !isProfileDropdownOpen.value
  if (isProfileDropdownOpen.value) {
    showProfileTooltip.value = false
  }
}

// const showToastMessage = (message, severity = 'info') => {
//   if (toastTimeout.value) clearTimeout(toastTimeout.value)

//   toastMessage.value = message
//   toastSeverity.value = severity
//   showToast.value = true

//   toastTimeout.value = setTimeout(() => {
//     showToast.value = false
//   }, 10000)
// }

// const processToastQueue = () => {
//   if (toastQueue.value.length === 0 || isToastActive.value) return;
  
//   isToastActive.value = true;
//   const nextToast = toastQueue.value.shift();
//   toastMessage.value = nextToast.message;
//   toastSeverity.value = nextToast.severity;
//   showToast.value = true;

//   setTimeout(() => {
//     showToast.value = false;
//     setTimeout(() => {
//       isToastActive.value = false;
//       processToastQueue();
//     }, 300); // Wait for exit animation
//   }, 10000);
// };

// Modified showToastMessage to use queue
// const showToastMessage = (message, severity = 'info') => {
//   toastQueue.value.push({ message, severity });
//   if (!isToastActive.value) {
//     processToastQueue();
//   }
// };

const processToastQueue = () => {
  if (toastQueue.value.length === 0 || isToastActive.value) return;
  
  isToastActive.value = true;
  const nextToast = toastQueue.value.shift();
  
  // Check if we've shown this toast before (even across refreshes)
  const toastKey = `toast-${nextToast.persistKey}`;
  if (nextToast.persistKey && localStorage.getItem(toastKey)) {
    isToastActive.value = false;
    processToastQueue();
    return;
  }
  
  toastMessage.value = nextToast.message;
  toastSeverity.value = nextToast.severity;
  showToast.value = true;

  // Mark as shown in localStorage
  if (nextToast.persistKey) {
    localStorage.setItem(toastKey, 'true');
  }

  setTimeout(() => {
    showToast.value = false;
    setTimeout(() => {
      isToastActive.value = false;
      processToastQueue();
    }, 300);
  }, 5000);
};

// Modified showToastMessage with persistence
const showToastMessage = (message, severity = 'info', persistKey = null) => {
  toastQueue.value.push({ message, severity, persistKey });
  if (!isToastActive.value) {
    processToastQueue();
  }
};

const toastStyles = computed(() => {
  switch (toastSeverity.value) {
    case 'success':
      return {
        icon: CheckCircle,
        iconColor: 'text-green-600',
        iconBg: 'bg-green-100',
        bg: 'bg-white',
        border: 'border-green-200'
      }
    case 'info':
      return {
        icon: Info,
        iconColor: 'text-blue-600',
        iconBg: 'bg-blue-100',
        bg: 'bg-white',
        border: 'border-blue-200'
      }
    case 'warning':
      return {
        icon: AlertTriangle,
        iconColor: 'text-yellow-600',
        iconBg: 'bg-yellow-100',
        bg: 'bg-white',
        border: 'border-yellow-200'
      }
    case 'critical':
      return {
        icon: XCircle,
        iconColor: 'text-red-600',
        iconBg: 'bg-red-100',
        bg: 'bg-white',
        border: 'border-red-200'
      }
    case 'failed':
      return {
        icon: XCircle,
        iconColor: 'text-gray-600',
        iconBg: 'bg-gray-100',
        bg: 'bg-white',
        border: 'border-gray-300'
      }
    default:
      return {
        icon: Info,
        iconColor: 'text-gray-600',
        iconBg: 'bg-gray-100',
        bg: 'bg-white',
        border: 'border-gray-300'
      }
  }
})

defineExpose({ showToastMessage })

const localNotifiedCache = {
  critical: null,
  warning: null,
  info: null,
}

const isSameDay = (d1, d2) =>
  d1.getFullYear() === d2.getFullYear() &&
  d1.getMonth() === d2.getMonth() &&
  d1.getDate() === d2.getDate()

const sendNotification = async (message, title, severity = 'info') => {
  // Default: show toast for non-critical notifications
  if (severity !== 'critical') {
    showToastMessage(message, severity)
  }

  let shouldSend = true

  if (severity === 'critical') {
    const today = new Date().toISOString().split('T')[0]

    const q = query(
      collection(db, 'notifications'),
      where('severity', '==', 'critical'),
      where('type', '==', 'water'),
      where('date', '==', today)
    )

    try {
      const snapshot = await getDocsFromServer(q)

      if (!snapshot.empty) {
        console.log('[DEBUG] Critical water notification already exists for today:', snapshot.docs[0].data())
        shouldSend = false
      } else {
        console.log('[DEBUG] No critical water notification found for today')
      }
    } catch (error) {
      console.error('❌ Error checking for existing notification:', error)
      shouldSend = false // Prevent duplicate on query error
    }
  }

  if (!shouldSend) return

  // Show toast only if allowed to send
  showToastMessage(message, severity)

  const notification = {
    id: Date.now().toString(),
    message,
    title,
    type: 'water',
    severity,
    read: false,
    date: new Date().toISOString().split('T')[0],
    timestamp: serverTimestamp(),
  }

  try {
    const docRef = await addDoc(collection(db, 'notifications'), notification)
    console.log('✅ Notification saved to Firestore:', docRef.id)

    const savedDoc = await getDoc(docRef)
    console.log('[DEBUG] Saved notification:', savedDoc.data())

    if (severity === 'critical') {
      const phone = '+639627080157'
      // await sendSMS(phone, `${title}: ${message}`) // Assuming sendSMS is defined elsewhere or re-added
    }
  } catch (error) {
    console.error('❌ Error saving notification:', error)
  }
}

const evaluateWaterLevel = (level) => {
  if (level <= 15) {
    sendNotification(
      'Water level is critically low! Immediate action required.',
      'Critical Water Level',
      'critical'
    )
  } else if (level <= 30 && level > 15) {
    sendNotification(
      'Water level is low (20–30%). Consider refilling soon.',
      'Low Water Level',
      'warning'
    )
  } else if (level === 50) {
    sendNotification(
      'Water level is at 50%. Monitoring status.',
      'Water Level Update',
      'info'
    )
  }
}

// const sendScheduleNotification = async (schedule, status) => { // `status` is 'started' or 'ended'
//   try {
//     const dateTimeFormatted = new Date(schedule.scheduledTime).toLocaleString('en-US', {
//       weekday: 'short',
//       // year: 'numeric', // Year might be too verbose for a quick notification
//       month: 'short',
//       day: 'numeric',
//       hour: '2-digit',
//       minute: '2-digit'
//     });

//     const eventType = status === 'started' ? 'watering_start' : 'watering_end';

//     const message =
//       status === 'started'
//         ? `The watering scheduled at ${dateTimeFormatted} is now starting.`
//         : `The watering scheduled at ${dateTimeFormatted} has ended.`;

//     // --- Duplicate Check ---
//     const notificationsRef = collection(db, 'notifications');
//     const q = query(notificationsRef,
//       where('scheduleId', '==', schedule.id),
//       where('eventType', '==', eventType)
//     );

//     const querySnapshot = await getDocs(q);
//     if (!querySnapshot.empty) {
//       console.log(`Notification for schedule ${schedule.id} (${eventType}) already exists. Skipping.`);
//       // Ensure local cache is also up-to-date if somehow missed
//       if (status === 'started') notifiedStartIds.add(schedule.id);
//       else notifiedEndIds.add(schedule.id);
//       return; // Exit if duplicate
//     }
//     // --- End Duplicate Check ---

//     const notification = {
//       title: 'Scheduled Watering',
//       message,
//       severity: 'info',
//       type: 'watering_schedule', // More specific type for this category of notification
//       scheduleId: schedule.id,   // Store the ID of the schedule this notification relates to
//       eventType: eventType,      // Store 'watering_start' or 'watering_end'
//       read: false,
//       timestamp: serverTimestamp()
//     };

//     await addDoc(collection(db, 'notifications'), notification);
//     showToastMessage(`Schedule ${status}: ${dateTimeFormatted}`);

//     // Update local notification caches after successful send
//     if (status === 'started') notifiedStartIds.add(schedule.id);
//     else notifiedEndIds.add(schedule.id);

//   } catch (error) {
//     console.error('Notification error:', error);
//   }
// };

// Enhanced sendScheduleNotification function with toast
const sendScheduleNotification = async (schedule, status) => {
  try {
    const dateTimeFormatted = new Date(schedule.scheduledTime).toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });

    const eventType = status === 'started' ? 'watering_start' : 'watering_end';
    const message = status === 'started'
      ? `The watering scheduled at ${dateTimeFormatted} is now starting.`
      : `The watering scheduled at ${dateTimeFormatted} has ended.`;

    // First show toast message
    showToastMessage(message, 'info', `schedule-${schedule.id}-${eventType}`);

    // Check for existing notification to prevent duplicates
    const notificationsRef = collection(db, 'notifications');
    const q = query(
      notificationsRef,
      where('scheduleId', '==', schedule.id),
      where('eventType', '==', eventType)
    );

    const querySnapshot = await getDocs(q);
    if (!querySnapshot.empty) {
      console.log(`Notification for schedule ${schedule.id} (${eventType}) already exists. Skipping.`);
      return;
    }

    // Save new notification
    await addDoc(notificationsRef, {
      title: 'Scheduled Watering',
      message,
      severity: 'info',
      type: 'watering_schedule',
      scheduleId: schedule.id,
      eventType,
      read: false,
      timestamp: serverTimestamp()
    });

    console.log(`Created ${status} notification for schedule ${schedule.id}`);

  } catch (error) {
    console.error('Notification error:', error);
    showToastMessage('Failed to save schedule notification', 'warning');
  }
};

const fetchNotifications = async () => {
  try {
    const querySnapshot = await getDocs(collection(db, "notifications"));
    notifications.value = querySnapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }));
    console.log('Fetched notifications:', notifications.value.length);
  } catch (err) {
    console.error("Error fetching notifications from Firebase:", err);
  }
};

// Set up real-time listener for notifications
const setupNotificationsListener = () => {
  const notificationsRef = collection(db, 'notifications');
  const q = query(notificationsRef, orderBy('timestamp', 'desc'));

  return onSnapshot(q, (snapshot) => {
    const notificationsList = [];
    snapshot.forEach((doc) => {
      notificationsList.push({
        id: doc.id,
        ...doc.data()
      });
    });
    notifications.value = notificationsList;
    console.log('Notifications updated:', notifications.value.length);
  }, (error) => {
    console.error('Error in notifications listener:', error);
  });
};

let unsubscribeNotifications = null;
let unsubscribeSchedules = null;

// const fetchWateringSchedules = () => {
//   const schedulesRef = collection(db, 'watering_schedules');
//   const schedulesQuery = query(schedulesRef, orderBy('scheduledTime', 'asc'));

//   if (unsubscribeSchedules) unsubscribeSchedules();

//   // Track processed schedule completions
//   const processedCompletions = new Set();
//   let isMotorOffOperationInProgress = false;

//   unsubscribeSchedules = onSnapshot(schedulesQuery, async (snapshot) => {
//     const schedules = [];
//     const now = Date.now();

//     // Process changes sequentially
//     for (const change of snapshot.docChanges()) {
//       const docSnap = change.doc;
//       const data = docSnap.data();
//       const scheduleId = docSnap.id;

//       // Convert timestamp if needed
//       if (data.scheduledTime && data.scheduledTime < 1e12) {
//         data.scheduledTime = data.scheduledTime * 1000;
//       }

//       // Handle completed schedules
//       if (change.type === 'modified' && data.completed === true) {
//         // Skip if already processed or operation in progress
//         if (processedCompletions.has(scheduleId) || isMotorOffOperationInProgress) {
//           continue;
//         }

//         processedCompletions.add(scheduleId);
//         isMotorOffOperationInProgress = true;

//         try {
//           const motorRef = doc(db, 'motor_status', 'current');
//           const motorSnapshot = await getDoc(motorRef);

//           if (motorSnapshot.exists()) {
//             const motorData = motorSnapshot.data();

//             // Only proceed if motor is actually ON
//             if (motorData.status === true) {
//               const nowDate = new Date();
//               const formattedTime = nowDate.toLocaleString('en-US', {
//                 weekday: 'short',
//                 month: 'short',
//                 day: 'numeric',
//                 hour: '2-digit',
//                 minute: '2-digit',
//                 hour12: true
//               });

//               // 1. Update motor status (single operation)
//               await updateDoc(motorRef, {
//                 status: false,
//                 timestamp: serverTimestamp(),
//                 formattedTime: formattedTime,
//                 user: 'system',
//                 device_id: 'main_motor'
//               });

//               // 2. Create SINGLE history log
//               const historyRef = collection(db, 'motor_status', 'history', 'logs');
//               await addDoc(historyRef, {
//                 status: false,
//                 timestamp: serverTimestamp(),
//                 device_id: 'main_motor',
//                 user: 'system',
//                 formattedTime: formattedTime,
//                 relatedSchedule: scheduleId
//               });

//               showToastMessage('Motor turned OFF after watering completed.');
//             }
//           }
//         } catch (err) {
//           console.error(`Error processing schedule completion ${scheduleId}:`, err);
//         } finally {
//           isMotorOffOperationInProgress = false;
//         }
//       }
//     }

//     // Update schedules list
//     snapshot.forEach((docSnap) => {
//       const data = docSnap.data();
//       const scheduleId = docSnap.id;

//       if (data.scheduledTime && data.scheduledTime < 1e12) {
//         data.scheduledTime = data.scheduledTime * 1000;
//       }

//       schedules.push({ id: scheduleId, ...data });
//     });

//     savedSchedules.value = schedules;
//   }, (error) => {
//     console.error("Error listening to watering schedules:", error);
//   });
// };

const fetchWateringSchedules = () => {
  const schedulesRef = collection(db, 'watering_schedules');
  const schedulesQuery = query(schedulesRef, orderBy('scheduledTime', 'asc'));

  if (unsubscribeSchedules) unsubscribeSchedules();

  unsubscribeSchedules = onSnapshot(schedulesQuery, async (snapshot) => {
    const schedules = [];
    const now = Date.now();
    const processedCompletions = new Set();

    // Track previous states to detect changes
    const previousStates = new Map(savedSchedules.value.map(s => [s.id, s.completed]));

    // Process each change
    for (const change of snapshot.docChanges()) {
      const docSnap = change.doc;
      const data = docSnap.data();
      const scheduleId = docSnap.id;

      // Convert timestamp if needed
      if (data.scheduledTime && data.scheduledTime < 1e12) {
        data.scheduledTime = data.scheduledTime * 1000;
      }

      // Handle schedule completion (end notification)
      if (data.completed === true && previousStates.get(scheduleId) === false) {
        if (processedCompletions.has(scheduleId)) continue;
        processedCompletions.add(scheduleId);

        try {
          // Send end notification
          await sendScheduleNotification({ ...data, id: scheduleId }, 'ended');
          
          // Turn off motor if needed
          await handleMotorStatus(false, scheduleId);
        } catch (err) {
          console.error(`Error processing completion for ${scheduleId}:`, err);
        }
      }

      schedules.push({ id: scheduleId, ...data });
    }

    savedSchedules.value = schedules;

    // Handle schedule starts (separate from completion handling)
    for (const schedule of schedules) {
      if (!schedule.notifyWatering || schedule.completed) continue;

      const isStarting = Math.abs(now - schedule.scheduledTime) <= 2000;
      
      if (isStarting && !notifiedStartIds.has(schedule.id)) {
        try {
          await sendScheduleNotification(schedule, 'started');
          notifiedStartIds.add(schedule.id);
          await handleMotorStatus(true, schedule.id);
        } catch (err) {
          console.error(`Error processing start for ${schedule.id}:`, err);
        }
      }
    }
  }, (error) => {
    console.error("Error listening to watering schedules:", error);
  });
};

// Centralized motor status handler
const handleMotorStatus = async (shouldBeOn, scheduleId = null) => {
  try {
    const motorRef = doc(db, 'motor_status', 'current');
    const motorSnapshot = await getDoc(motorRef);

    const nowDate = new Date();
    const formattedTime = nowDate.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });

    // Only update if needed
    if (!motorSnapshot.exists() || motorSnapshot.data().status !== shouldBeOn) {
      await updateDoc(motorRef, {
        status: shouldBeOn,
        timestamp: serverTimestamp(),
        formattedTime,
        user: 'system',
        device_id: 'main_motor'
      });
      console.log(`✅ Motor turned ${shouldBeOn ? 'ON' : 'OFF'} for schedule ${scheduleId}`);
    }

    // Check for existing history log before creating new one
    const historyQuery = query(
      collection(db, 'motor_status', 'history', 'logs'),
      where('relatedSchedule', '==', scheduleId),
      where('status', '==', shouldBeOn),
      limit(1)
    );
    
    const historySnapshot = await getDocs(historyQuery);
    if (historySnapshot.empty) {
      await addDoc(collection(db, 'motor_status', 'history', 'logs'), {
        status: shouldBeOn,
        timestamp: serverTimestamp(),
        device_id: 'main_motor',
        user: 'system',
        formattedTime,
        relatedSchedule: scheduleId
      });
      console.log(`📜 Motor ${shouldBeOn ? 'ON' : 'OFF'} event logged in history.`);
    }

  } catch (err) {
    console.error(`Error handling motor status for schedule ${scheduleId}:`, err);
    showToastMessage(`Failed to ${shouldBeOn ? 'start' : 'stop'} motor`, 'warning');
  }
};

const saveToLocalStorage = (notification) => {
  const existing = JSON.parse(localStorage.getItem('notifications') || '[]') // Corrected: localStorage.getItem
  // Prevent duplicates based on ID
  const exists = existing.find(n => n.id === notification.id)
  if (!exists) {
    existing.push(notification)
    localStorage.setItem('notifications', JSON.stringify(existing))
  }
}

const getSignalStrengthClass = (strength) => {
  if (strength >= 70) return 'bg-green-500'
  if (strength >= 40) return 'bg-yellow-500'
  return 'bg-red-500'
}

const menuItems = [
  { name: 'Overview', href: '/dashboard', icon: LayoutDashboard },
  { name: 'Crop Prediction', href: '/prediction', icon: Brain },
  { name: 'Weather', href: '/weather', icon: Cloud },
  { name: 'Device Control', href: '/control', icon: Cpu },
  { name: 'Soil Analysis', href: '/soil', icon: Sprout }
]

const sensorTypes = [
  { name: 'NPK Data', href: '/npkData', icon: Sprout },
  { name: 'Soil pH', href: '/soilph', icon: Beaker },
  { name: 'Soil Moisture', href: '/soil-moisture', icon: Droplets },
  { name: 'Temp/Humid', href: '/temperature-humidity', icon: Thermometer },
  { name: 'Water Level', href: '/water-level', icon: Gauge },
  { name: 'Motor Control', href: '/motor-control', icon: Power }
]

const toggleSensorDropdown = () => {
  isSensorDropdownOpen.value = !isSensorDropdownOpen.value
}

const isCurrentRoute = (path) => {
  return route.path === path
}

const isInSensorRoutes = computed(() => {
  return sensorTypes.some(sensor => route.path === sensor.href)
})

const closeDropdown = (e) => {
  if (!e.target.closest('.relative.group') && !e.target.closest('.relative.ml-4')) {
    isSensorDropdownOpen.value = false
    isProfileDropdownOpen.value = false
  }
}

const goToProfile = () => {
  isProfileDropdownOpen.value = false
  router.push({ name: 'UserProfile' })
}

let resizeTimeout
const handleResize = () => {
  clearTimeout(resizeTimeout)
  resizeTimeout = setTimeout(() => {
    if (window.innerWidth < 640) {
      isSensorDropdownOpen.value = false
      isProfileDropdownOpen.value = false
      showNotifications.value = false
      showWifiTooltip.value = false
      showWebSocketTooltip.value = false
      showRecalibrationTooltip.value = false
      showNotificationTooltip.value = false
      showProfileTooltip.value = false
    }
  }, 150)
}

const avatarOptions = ref([
  { id: 1, icon: '🌱', name: 'Seedling' },
  { id: 2, icon: '🌿', name: 'Herb' },
  { id: 3, icon: '🌾', name: 'Wheat' },
  { id: 4, icon: '🌽', name: 'Corn' },
  { id: 5, icon: '🥕', name: 'Carrot' },
  { id: 6, icon: '🍅', name: 'Tomato' },
  { id: 7, icon: '🥬', name: 'Lettuce' },
  { id: 8, icon: '🌻', name: 'Sunflower' },
  { id: 9, icon: '🌳', name: 'Tree' },
  { id: 10, icon: '🍃', name: 'Leaves' },
  { id: 11, icon: '🌵', name: 'Cactus' },
  { id: 12, icon: '🌸', name: 'Blossom' },
  { id: 13, icon: '🍄', name: 'Mushroom' },
  { id: 14, icon: '🌺', name: 'Hibiscus' },
  { id: 15, icon: '🌹', name: 'Rose' },
  { id: 16, icon: '🌷', name: 'Tulip' },
  { id: 17, icon: '🥦', name: 'Broccoli' },
  { id: 18, icon: '🌶️', name: 'Pepper' },
  { id: 19, icon: '🥒', name: 'Cucumber' },
  { id: 20, icon: '🍆', name: 'Eggplant' },
  { id: 21, icon: '🥔', name: 'Potato' },
  { id: 22, icon: '🧄', name: 'Garlic' },
  { id: 23, icon: '🧅', name: 'Onion' },
  { id: 24, icon: '🥜', name: 'Peanut' }
])

const fetchUserRealtime = () => {
  const uid = localStorage.getItem('uid') || sessionStorage.getItem('uid')
  if (!uid) {
    console.error('⚠️ No user ID found in local/session storage.')
    return
  }

  const userDocRef = doc(db, 'users', uid)

  const unsubscribe = onSnapshot(userDocRef, (docSnap) => {
    if (docSnap.exists()) {
      user.value = docSnap.data()
    } else {
      console.warn('User document not found.')
    }
  }, (error) => {
    console.error('Real-time fetch failed:', error)
  })

  return unsubscribe // Optional: in case you want to unsubscribe on unmount
}

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

const sendSmsAlert = async (phoneNumber, message) => {
  if (!phoneNumber) {
    console.warn('No phone number available for user to send SMS alert.');
    return;
  }
  try {
    // This requires a backend endpoint to handle the actual SMS sending logic
    // for security and to manage credentials.
    // await api.post('/send-sms', {
    //   phone: phoneNumber,
    //   message: message,
    // });
    console.log(`SMS alert sent to ${phoneNumber}`);
  } catch (error) {
    console.error('Error sending SMS alert via backend:', error);
  }
};

const saveWeatherAlertToFirebase = async (notificationDetails) => {
  try {
    // Check for existing notification for this date and type
    const notificationsRef = collection(db, 'notifications');
    const q = query(
      notificationsRef,
      where('date', '==', notificationDetails.date),
      where('type', '==', 'weather_alert')
    );
    
    const querySnapshot = await getDocs(q);
    if (!querySnapshot.empty) {
      console.log('Weather alert already exists for this date. Skipping save.');
      return false; // Return false to indicate duplicate
    }

    // If not found, save it
    await addDoc(notificationsRef, {
      ...notificationDetails,
      read: false,
      timestamp: serverTimestamp(),
    });
    console.log('Weather alert notification saved to Firebase.');
    return true; // Return true to indicate new notification
  } catch (error) {
    console.error('Error saving weather alert to Firebase:', error);
    return false;
  }
};


const thunderstormConditions = [
  'Thunderstorm',
  'Thunderstorm with Hail',
  'Severe Thunderstorm'
];

const severityMap = {
  'Heavy Rain': 1,
  'Rain Showers': 1,
  'Heavy Rain Showers': 2,
  'Violent Rain Showers': 3,
  'Thunderstorm': 4,
  'Thunderstorm with Hail': 5,
  'Severe Thunderstorm': 6
};

const getSeverityLevel = (condition) => {
  return severityMap[condition] || 0;
};


const checkWeatherForecastForAlerts = async () => {
  console.log('Checking weather forecast for alerts...');
  try {
    const weatherData = await getWeatherData();
    
    if (!weatherData || !weatherData.forecast) {
      console.warn('Could not retrieve weather forecast data.');
      return;
    }

    const today = new Date().toISOString().split('T')[0];
    const shownAlerts = JSON.parse(localStorage.getItem('shownWeatherAlerts') || '{}');
    const smsSentDates = new Set(JSON.parse(localStorage.getItem('smsSentDates') || '[]'));

    // Collect all severe weather alerts
    for (const day of weatherData.forecast.slice(0, 3)) {
      const condition = mapWeatherCode(day.condition_code);
      const dateStr = day.date.split('T')[0];
      
      if (isSevereWeather(condition)) {
        const weekday = new Date(dateStr).toLocaleDateString('en-US', { weekday: 'long' });
        const message = `Warning: ${condition} forecasted for ${weekday}.`;
        
        // Skip if we've already shown this alert today
        if (shownAlerts[dateStr] === today) continue;
        
        // Save notification to Firebase if it doesn't exist
        const notificationSaved = await saveWeatherAlertToFirebase({ 
          title: 'Severe Weather Alert', 
          message, 
          severity: 'warning', 
          type: 'weather_alert', 
          date: dateStr 
        });

        // Only show toast if notification was saved (new)
        if (notificationSaved) {
          showToastMessage(message, 'warning');
          shownAlerts[dateStr] = today; // Mark as shown today
          localStorage.setItem('shownWeatherAlerts', JSON.stringify(shownAlerts));
        }
        
        // Send SMS only for thunderstorm conditions and only once per day
        if (thunderstormConditions.includes(condition)) {
          const shouldSendSms = !smsSentDates.has(dateStr) && user.value?.phoneNumber;
          
          if (shouldSendSms) {
            await sendSmsAlert(user.value.phoneNumber, message);
            smsSentDates.add(dateStr);
            localStorage.setItem('smsSentDates', JSON.stringify([...smsSentDates]));
          }
        }
      }
    }
    
  } catch (error) {
    console.error('Failed to check weather forecast for alerts:', error);
    showToastMessage('Failed to check weather alerts', 'warning');
  }
};

// const checkWeatherForecastForAlerts = async () => {
//   console.log('Checking weather forecast for alerts...');
//   try {
//     const weatherData = await getWeatherData();
    
//     if (!weatherData || !weatherData.forecast) {
//       console.warn('Could not retrieve weather forecast data.');
//       return;
//     }

//     const today = new Date().toISOString().split('T')[0];
//     const notifiedDates = new Set(JSON.parse(localStorage.getItem('notifiedWeatherDates') || '[]'));

//     for (const day of weatherData.forecast.slice(0, 3)) {
//       // Map condition code to human-readable string
//       const condition = mapWeatherCode(day.condition_code);
//       const dateStr = day.date.split('T')[0]; // Extract date part only
      
//       if (isSevereWeather(condition)) {
//         // Skip if we've already notified for this date
//         if (notifiedDates.has(dateStr)) continue;
        
//         const weekday = new Date(dateStr).toLocaleDateString('en-US', { weekday: 'long' });
//         const message = `Warning: ${condition} forecasted for ${weekday}.`;
        
//         // Show toast immediately
//         showToastMessage(message, 'warning');
        
//         // Save to Firebase (with duplicate check)
//         await saveWeatherAlertToFirebase({ 
//           title: 'Severe Weather Alert', 
//           message, 
//           severity: 'warning', 
//           type: 'weather_alert', 
//           date: dateStr 
//         });
        
//         // Send SMS if user has phone number
//         if (user.value && user.value.phoneNumber) {
//           await sendSmsAlert(user.value.phoneNumber, message);
//         }
        
//         // Mark this date as notified
//         notifiedDates.add(dateStr);
//       }
//     }
    
//     // Save notified dates to localStorage
//   } catch (error) {
//     console.error('Failed to check weather forecast for alerts:', error);
//     showToastMessage('Failed to check weather alerts', 'warning');
//   }
// };

let userPhone = ref(null)

const evaluateSoilMoisture = (level) => {
  const today = new Date().toISOString().split('T')[0];
  
  if (level <= 10) {
    saveSoilMoistureAlertToFirebase({
      title: 'Critical Soil Moisture',
      message: `Soil moisture is critically low (${level}%)! Immediate watering required.`,
      severity: 'critical',
      type: 'soil_moisture',
      date: today
    });
  } else if (level <= 20) {
    saveSoilMoistureAlertToFirebase({
      title: 'Low Soil Moisture',
      message: `Soil moisture is low (${level}%). Consider watering soon.`,
      severity: 'warning',
      type: 'soil_moisture',
      date: today
    });
  }
}

const saveSoilMoistureAlertToFirebase = async (notificationDetails) => {
  try {
    // Check for existing notifications of same type and severity today
    const q = query(
      collection(db, 'notifications'),
      where('date', '==', notificationDetails.date),
      where('type', '==', 'soil_moisture'),
      where('severity', '==', notificationDetails.severity)
    );
    
    const querySnapshot = await getDocs(q);
    if (!querySnapshot.empty) {
      console.log(`${notificationDetails.severity} soil moisture alert already exists for today. Skipping save.`);
      return;
    }

    await addDoc(collection(db, 'notifications'), {
      ...notificationDetails,
      read: false,
      timestamp: serverTimestamp()
    });
    
    console.log('Soil moisture notification saved:', notificationDetails.severity);
    showToastMessage(notificationDetails.message, notificationDetails.severity);
    
    // Use the new SMS function for critical alerts
    if (notificationDetails.severity === 'critical' && user.value?.phoneNumber) {
      const smsMessage = `${notificationDetails.title}: ${notificationDetails.message}`;
      await sendSoilMoistureSmsAlert(user.value.phoneNumber, smsMessage);
    }
  } catch (error) {
    console.error('Error saving soil moisture alert:', error);
    showToastMessage('Failed to save soil moisture alert', 'warning');
  }
};

const sendSoilMoistureSmsAlert = async (phoneNumber, message) => {
  if (!phoneNumber) {
    console.warn('No phone number available to send soil moisture SMS alert');
    return;
  }
  
  try {
    // Replace with your actual SMS endpoint
    // const response = await axios.post('http://127.0.0.1:8000/send-sms', {
    //   phone: phoneNumber,
    //   message: message
    // });
        // await api.post('/send-sms', {
    //   phone: phoneNumber,
    //   message: message,
    // });

    console.log(`✅ SMS alert sent to ${phoneNumber}` );
    return true;
  } catch (error) {
    console.error('❌ Soil moisture SMS error:', error);
    showToastMessage('Failed to send soil moisture SMS', 'warning');
    return false;
  }
}

const setupSoilMoistureListener = () => {
  try {
    const soilMoistureQuery = query(
      collection(db, "3sensor_readings", "esp32-2", "readings"),
      orderBy("timestamp", "desc"),
      limit(1)
    );
    
    const unsubscribe = onSnapshot(soilMoistureQuery, (snapshot) => {
      if (!snapshot.empty) {
        const sensorData = snapshot.docs[0].data();
        const soilMoistureValue = sensorData.soilMoisture;
        
        console.log("🔄 Latest soil moisture reading:", soilMoistureValue);
        
        if (typeof soilMoistureValue === 'number') {
          evaluateSoilMoisture(soilMoistureValue);
        } else {
          console.warn("⚠️ Soil moisture value is not a number:", soilMoistureValue);
        }
      } else {
        console.log("ℹ️ No soil moisture data available yet.");
      }
    }, (error) => {
      console.error("❌ Soil moisture listener error:", error);
      showToastMessage('Soil moisture monitoring failed', 'warning');
    });
    
    return unsubscribe;  // Return the unsubscribe function
    
  } catch (err) {
    console.error("❌ Soil moisture setup error:", err);
    showToastMessage('Failed to setup soil moisture monitoring', 'warning');
    return () => {}; // Return dummy function for cleanup
  }
}

let unsubscribeSoilMoisture = null;
const previousScheduleStates = ref({});

onMounted(async () => {
  fetchUserRealtime()

  document.addEventListener('click', closeDropdown)
  window.addEventListener('resize', handleResize)
  handleResize()

  // Get IP Address
  try {
    const res = await fetch('https://api.ipify.org?format=json')
    const ipData = await res.json()
    ipAddress.value = ipData.ip
  } catch (error) {
    console.error('Error fetching IP:', error)
    ipAddress.value = 'Unknown'
  }

  // Network Info
  if ('connection' in navigator) {
    const conn = navigator.connection || navigator.mozConnection || navigator.webkitConnection

    const updateWifiInfo = () => {
      wifiStrength.value = conn.downlinkMax ? Math.min(conn.downlinkMax * 10, 100) : 70
      wifiNetwork.value = conn.effectiveType || 'WiFi'
    }

    updateWifiInfo()

    if (conn.addEventListener) {
      conn.addEventListener('change', updateWifiInfo)
    }
  }

  // Load notifications from localStorage
  const saved = localStorage.getItem('notifications')
  if (saved) {
    notifications.value = JSON.parse(saved)
  }

  await fetchNotifications()
  unsubscribeNotifications = setupNotificationsListener()

  // Watch watering schedules
  fetchWateringSchedules()
  checkWeatherForecastForAlerts();
  setInterval(checkWeatherForecastForAlerts, 3 * 60 * 60 * 1000); // Every 3 hours


  // Check for scheduled watering every second
  // setInterval(() => {
  //   currentTime.value = Date.now();
  //   const now = Date.now();

  //   savedSchedules.value.forEach(async (schedule) => {
  //     if (!schedule.notifyWatering || !schedule.scheduledTime || schedule.completed) return;

  //     const start = schedule.scheduledTime;
  //     const isStarting = Math.abs(now - start) <= 2000;

  //     if (isStarting && !notifiedStartIds.has(schedule.id)) {
  //       sendScheduleNotification(schedule, 'started');
  //       notifiedStartIds.add(schedule.id);

  //       try {
  //         const motorDocRef = doc(db, 'motor_status', 'current');
  //         const motorSnapshot = await getDoc(motorDocRef);

  //         const nowDate = new Date();
  //         const formattedTime = nowDate.toLocaleString('en-US', {
  //           weekday: 'short',
  //           month: 'short',
  //           day: 'numeric',
  //           hour: '2-digit',
  //           minute: '2-digit',
  //           hour12: true
  //         });

  //         if (!motorSnapshot.exists() || motorSnapshot.data().status === false) {
  //           // ✅ Turn ON the motor
  //           await updateDoc(motorDocRef, {
  //             status: true,
  //             timestamp: serverTimestamp(),
  //             formattedTime: formattedTime,
  //             user: 'system',
  //             device_id: 'main_motor'
  //           });
  //           console.log(`✅ Motor turned ON for schedule ${schedule.id}`);
  //         }

  //         // ✅ Always log to history (even if already ON)
  //         const historyRef = collection(db, 'motor_status', 'history', 'logs');
  //         await addDoc(historyRef, {
  //           status: true,
  //           scheduleId: schedule.id,
  //           triggeredBy: 'auto',
  //           timestamp: serverTimestamp(),
  //           device_id: 'main_motor',
  //           user: 'system',
  //           formattedTime: formattedTime
  //         });
  //         console.log(`📜 Motor ON event logged in history.`);

  //       } catch (err) {
  //         console.error(`❌ Error processing motor status for schedule ${schedule.id}:`, err);
  //       }
  //     }
  //   });
  // }, 1000);

  setInterval(async () => {
    const now = Date.now();
    const processedThisRun = new Set();

    for (const schedule of savedSchedules.value) {
      if (!schedule.notifyWatering || !schedule.scheduledTime || schedule.completed || 
          processedThisRun.has(schedule.id)) {
        continue;
      }

      processedThisRun.add(schedule.id);

      const start = schedule.scheduledTime;
      const isStarting = Math.abs(now - start) <= 2000;

      if (isStarting && !notifiedStartIds.has(schedule.id)) {
        try {
          // 1. Send notification (with built-in deduplication)
          await sendScheduleNotification(schedule, 'started');
          notifiedStartIds.add(schedule.id);

          // 2. Check if motor update is needed
          const motorDocRef = doc(db, 'motor_status', 'current');
          const motorSnapshot = await getDoc(motorDocRef);
          
          const nowDate = new Date();
          const formattedTime = nowDate.toLocaleString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          });

          // Only update if motor is not already ON
          if (!motorSnapshot.exists() || motorSnapshot.data().status === false) {
            await updateDoc(motorDocRef, {
              status: true,
              timestamp: serverTimestamp(),
              formattedTime,
              user: 'system',
              device_id: 'main_motor'
            });
            console.log(`✅ Motor turned ON for schedule ${schedule.id}`);
          }

          // 3. Create history log (with deduplication check)
          const historyQuery = query(
            collection(db, 'motor_status', 'history', 'logs'),
            where('scheduleId', '==', schedule.id),
            where('status', '==', true),
            limit(1)
          );
          
          const historySnapshot = await getDocs(historyQuery);
          if (historySnapshot.empty) {
            await addDoc(collection(db, 'motor_status', 'history', 'logs'), {
              status: true,
              timestamp: serverTimestamp(),
              device_id: 'main_motor',
              user: 'system',
              formattedTime,
              relatedSchedule: schedule.id
            });
            console.log(`📜 Motor ON event logged in history.`);
          }

        } catch (err) {
          console.error(`❌ Error processing schedule ${schedule.id}:`, err);
        }
      }
    }
  }, 1000);


  //   setInterval(async () => {
//   currentTime.value = Date.now();
//   const now = Date.now();
//   const processedThisRun = new Set();
//   let motorOperationLock = false; // Lock to prevent duplicate motor operations

//   // Process schedules sequentially
//   for (const schedule of savedSchedules.value) {
//     // Skip conditions
//     if (!schedule.notifyWatering || 
//         !schedule.scheduledTime || 
//         schedule.completed ||
//         processedThisRun.has(schedule.id) ||
//         processingScheduleIds.value.has(schedule.id)) {
//       continue;
//     }

//     // Mark as processed
//     processedThisRun.add(schedule.id);
//     processingScheduleIds.value.add(schedule.id);

//     const start = schedule.scheduledTime;
//     const isStarting = Math.abs(now - start) <= 2000;

//     if (isStarting && !notifiedStartIds.has(schedule.id)) {
//       try {
//         // 1. Send notification
//         sendScheduleNotification(schedule, 'started');
//         notifiedStartIds.add(schedule.id);

//         // 2. Prepare common data
//         const nowDate = new Date();
//         const formattedTime = nowDate.toLocaleString('en-US', {
//           weekday: 'short',
//           month: 'short',
//           day: 'numeric',
//           hour: '2-digit',
//           minute: '2-digit',
//           hour12: true
//         });

//         // 3. Check motor status (with lock to prevent duplicates)
//         if (!motorOperationLock) {
//           motorOperationLock = true;
          
//           const motorDocRef = doc(db, 'motor_status', 'current');
//           const motorSnapshot = await getDoc(motorDocRef);

//           // Only update if motor is not already ON
//           if (!motorSnapshot.exists() || motorSnapshot.data().status === false) {
//             await updateDoc(motorDocRef, {
//               status: true,
//               timestamp: serverTimestamp(),
//               formattedTime: formattedTime,
//               user: 'system',
//               device_id: 'main_motor'
//             });
//             console.log(`✅ Motor turned ON for schedule ${schedule.id}`);
//           }

//           // 4. Create SINGLE history log
//           const historyRef = collection(db, 'motor_status', 'history', 'logs');
//           await addDoc(historyRef, {
//             status: true,
//             scheduleId: schedule.id,
//             triggeredBy: 'auto',
//             timestamp: serverTimestamp(),
//             device_id: 'main_motor',
//             user: 'system',
//             formattedTime: formattedTime
//           });

//           // 5. Send SINGLE request to backend
//           try {
//             const response = await axios.post('http://localhost:8000/api/motor_status/', {
//               status: true,
//               device_id: 'main_motor',
//               user: 'system',
//               timestamp: nowDate.toISOString(),
//               formatted_time: formattedTime,
//               source: 'schedule'
//             });
//             console.log('📤 Motor status sent to backend');
//           } catch (apiErr) {
//             console.error('❌ Backend update error:', apiErr);
//           }
//         } else {
//           console.log('🔒 Motor operation already in progress, skipping duplicate');
//         }
//       } catch (err) {
//         console.error(`❌ Error processing schedule ${schedule.id}:`, err);
//       } finally {
//         motorOperationLock = false;
//         processingScheduleIds.value.delete(schedule.id);
//       }
//     }
//   }
// }, 1000);

  const user = await fetchUserRealtime(); 
  unsubscribeSoilMoisture = setupSoilMoistureListener();
})

// Clean up localStorage for old schedules periodically
setInterval(() => {
  const oneWeekAgo = Date.now() - 7 * 24 * 60 * 60 * 1000;
  Object.keys(localStorage).forEach(key => {
    if (key.startsWith('toast-') && 
        key.includes('-start') || key.includes('-end')) {
      const timestamp = parseInt(key.split('-').pop());
      if (timestamp && timestamp < oneWeekAgo) {
        localStorage.removeItem(key);
      }
    }
  });
}, 24 * 60 * 60 * 1000);

onBeforeUnmount(() => {
  // Clean up event listeners
  document.removeEventListener('click', closeDropdown)
  window.removeEventListener('resize', handleResize)
  clearTimeout(resizeTimeout)

  // Clean up Firestore listeners
  if (unsubscribeSchedules) unsubscribeSchedules();
  if (unsubscribeNotifications) unsubscribeNotifications();
  if (unsubscribeSoilMoisture) unsubscribeSoilMoisture();
  if (toastTimeout.value) clearTimeout(toastTimeout.value);
})

// Watch for route changes to close dropdowns
watch(() => route.path, () => {
  isSensorDropdownOpen.value = false
  isProfileDropdownOpen.value = false
  showNotifications.value = false
  showWifiTooltip.value = false
  showWebSocketTooltip.value = false
  showRecalibrationTooltip.value = false
  showNotificationTooltip.value = false
  showProfileTooltip.value = false
})
</script>

<style scoped>
.router-link-active {
  position: relative;
  transform: translateZ(0);
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