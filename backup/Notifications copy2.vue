<template>
    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-black/20 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="bg-white rounded-2xl shadow-2xl border-2 border-transparent bg-gradient-to-r from-yellow-200 via-emerald-200 to-green-300 p-0.5 max-w-md mx-4">
        <div class="bg-white rounded-2xl p-8 text-center">
          <!-- Notification Icon Animation -->
          <div class="mb-6 relative">
            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-emerald-400 to-green-500 rounded-2xl flex items-center justify-center shadow-lg">
              <Bell class="h-10 w-10 text-white animate-bounce" />
            </div>
            <!-- Notification Badge -->
            <div class="absolute -top-1 -right-1 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
              <span class="text-white text-xs font-bold">!</span>
            </div>
          </div>
          
          <!-- Loading Dots -->
          <div class="flex justify-center space-x-2 mb-6">
            <div 
              v-for="i in 5" 
              :key="i"
              class="w-2 h-2 rounded-full transition-all duration-300"
              :class="loadingDotIndex === i - 1 ? 'bg-emerald-500 scale-125' : 'bg-gray-300'"
            ></div>
          </div>
          
          <!-- Loading Text -->
          <h3 class="text-xl font-semibold text-gray-800 mb-2">Loading Notifications</h3>
          <p class="text-gray-600 text-sm">Please wait while we fetch your latest alerts and updates</p>
        </div>
      </div>
    </div>

    <!-- Enhanced Notification Details Modal -->
    <div v-if="selectedNotification" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-2xl w-full max-h-[85vh] overflow-hidden border border-gray-200">
        <!-- Modal Header -->
        <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-3">
              <div 
                class="w-10 h-10 rounded-xl flex items-center justify-center shadow-sm"
                :class="getNotificationIcon(selectedNotification).bgColor"
              >
                <component 
                  :is="getNotificationIcon(selectedNotification).icon" 
                  class="h-5 w-5 text-white" 
                />
              </div>
              <div>
                <h2 class="text-lg font-semibold text-gray-800">Notification Details</h2>
                <p class="text-sm text-gray-500">{{ formatTime(selectedNotification.time) }}</p>
              </div>
            </div>
            <button 
              @click="closeDetails"
              class="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <X class="h-5 w-5" />
            </button>
          </div>
        </div>

        <!-- Modal Content -->
        <div class="p-6 overflow-y-auto max-h-[calc(85vh-160px)]">
          <div class="space-y-5">
            <!-- Title and Status -->
            <div>
              <div class="flex items-start justify-between mb-3">
                <h3 class="text-lg font-semibold text-gray-900">{{ selectedNotification.title }}</h3>
                <div class="flex items-center space-x-2">
                  <span 
                    class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium"
                    :class="getNotificationIcon(selectedNotification).badgeColor"
                  >
                    {{ selectedNotification.category || selectedNotification.type }}
                  </span>
                  <div v-if="!selectedNotification.read" class="flex items-center text-blue-600 text-xs font-medium">
                    <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                    Unread
                  </div>
                  <div v-if="selectedNotification.archived" class="flex items-center text-orange-600 text-xs font-medium">
                    <Archive class="h-3 w-3 mr-1" />
                    Archived
                  </div>
                </div>
              </div>
            </div>

            <!-- Message - Back to Dark Gray -->
            <div>
              <h4 class="text-sm font-medium text-gray-700 mb-2">Message</h4>
              <p class="text-gray-700 leading-relaxed font-medium">
                {{ selectedNotification.message }}
              </p>
            </div>

            <!-- Enhanced Detailed Analysis Container -->
            <div class="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-2xl p-4 border-2 border-indigo-100 shadow-lg">
              <h4 class="text-sm font-bold text-gray-800 mb-3 flex items-center">
                <div class="w-6 h-6 bg-indigo-500 rounded-full flex items-center justify-center mr-2">
                  <Info class="h-3 w-3 text-white" />
                </div>
                Detailed Analysis
              </h4>
              
              <!-- Weather Notifications -->
              <!-- Enhanced Weather Notifications Section -->
              <div v-if="isWeatherNotification(selectedNotification)" class="space-y-4">
                <p class="text-xs text-gray-600 mb-3 bg-white/60 rounded-lg p-2 border border-indigo-200">
                  Current weather conditions and forecast data for your location.
                </p>
                
                <!-- Current Weather Summary -->
                <div class="bg-blue-100 rounded-xl p-4 border-2 border-blue-300 shadow-sm">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center space-x-2">
                      <CloudRain class="h-4 w-4 text-blue-600" />
                      <span class="text-sm font-medium text-blue-700">Current Weather</span>
                    </div>
                    <span class="text-base font-bold text-blue-800">
                      {{ weatherModalData?.weatherCondition || 'Loading...' }}
                      <span v-if="weatherModalData?.temperature">({{ weatherModalData.temperature }}°C)</span>
                    </span>
                  </div>
                </div>

                <div class="grid grid-cols-2 gap-3">
                  <!-- Humidity -->
                  <div class="bg-blue-50 rounded-xl p-3 border-2 border-blue-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Droplet class="h-3 w-3 text-blue-600" />
                      <span class="text-xs font-medium text-blue-700">Humidity</span>
                    </div>
                    <p class="text-lg font-bold text-blue-800">{{ weatherModalData?.humidity || '--' }}%</p>
                    <p class="text-xs text-blue-600 mt-1">
                      {{ weatherModalData?.humidity ? getHumidityDescription(weatherModalData.humidity) : 'No data' }}
                    </p>
                  </div>
                  
                  <!-- Pressure -->
                  <div class="bg-gray-50 rounded-xl p-3 border-2 border-gray-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Gauge class="h-3 w-3 text-gray-600" />
                      <span class="text-xs font-medium text-gray-700">Pressure</span>
                    </div>
                    <p class="text-lg font-bold text-gray-800">{{ weatherModalData?.pressure || '--' }} hPa</p>
                    <p class="text-xs text-gray-600 mt-1">
                      {{ weatherModalData?.pressure ? getPressureDescription(weatherModalData.pressure) : 'No data' }}
                    </p>
                  </div>
                  
                  <!-- Wind Speed -->
                  <div class="bg-green-50 rounded-xl p-3 border-2 border-green-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Wind class="h-3 w-3 text-green-600" />
                      <span class="text-xs font-medium text-green-700">Wind Speed</span>
                    </div>
                    <p class="text-lg font-bold text-green-800">{{ weatherModalData?.windSpeed || '--' }} km/h</p>
                    <p class="text-xs text-green-600 mt-1">
                      {{ weatherModalData?.windSpeed ? getWindDescription(weatherModalData.windSpeed) : 'No data' }}
                    </p>
                  </div>
                  
                  <!-- UV Index -->
                  <div class="bg-yellow-50 rounded-xl p-3 border-2 border-yellow-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Sun class="h-3 w-3 text-yellow-600" />
                      <span class="text-xs font-medium text-yellow-700">UV Index</span>
                    </div>
                    <p class="text-lg font-bold text-yellow-800">{{ weatherModalData?.uvIndex || '--' }}</p>
                    <p class="text-xs text-yellow-600 mt-1">
                      {{ weatherModalData?.uvIndex ? getUVDescription(weatherModalData.uvIndex) : 'No data' }}
                    </p>
                  </div>
                </div>
                
                <!-- Rain Forecast -->
                <div class="bg-green-100 rounded-xl p-4 border-2 border-green-300 shadow-sm">
                  <div class="flex items-center justify-between mb-2">
                    <div class="flex items-center space-x-2">
                      <CloudRain class="h-4 w-4 text-green-600" />
                      <span class="text-sm font-medium text-green-700">Rain Forecast</span>
                    </div>
                    <span class="text-base font-bold text-green-800">{{ weatherModalData?.rainIntensity || '--' }}%</span>
                  </div>
                  <div class="flex items-center space-x-3 mb-3">
                    <div class="flex-1">
                      <div class="flex justify-between text-xs text-green-600 mb-2">
                        <span>Light</span>
                        <span>Heavy</span>
                      </div>
                      <div class="w-full bg-green-200 rounded-full h-3">
                        <div 
                          class="bg-green-600 h-3 rounded-full transition-all duration-300"
                          :style="{ width: `${weatherModalData?.rainIntensity || 0}%` }"
                        ></div>
                      </div>
                    </div>
                    <span class="text-sm font-bold text-green-800">
                      {{ weatherModalData?.rainIntensity ? getRainRating(weatherModalData.rainIntensity) : '--' }}
                    </span>
                  </div>
                  <p class="text-sm text-green-700 font-medium">
                    {{ weatherModalData?.rainIntensity ? getRainDescription(weatherModalData.rainIntensity) : 'No rain data available' }}
                  </p>
                </div>
              </div>
              
              <!-- Soil Moisture Notifications -->
              <div v-else-if="isSoilNotification(selectedNotification)" class="space-y-4">
                <p class="text-xs text-gray-600 mb-3 bg-white/60 rounded-lg p-2 border border-indigo-200">
                  Soil moisture levels are critical for optimal plant growth. This analysis provides insights into current soil conditions and irrigation status.
                </p>
                
                <div class="grid grid-cols-2 gap-3">
                  <div class="bg-amber-50 rounded-xl p-3 border-2 border-amber-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Droplet class="h-3 w-3 text-amber-600" />
                      <span class="text-xs font-medium text-amber-700">Soil Moisture</span>
                    </div>
                    <p class="text-lg font-bold text-amber-800">{{ getSoilData(selectedNotification).moistureLevel }}%</p>
                    <p class="text-xs text-amber-600 mt-1">{{ getMoistureDescription(getSoilData(selectedNotification).moistureLevel) }}</p>
                  </div>
                  
                  <div class="bg-blue-50 rounded-xl p-3 border-2 border-blue-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Droplet class="h-3 w-3 text-blue-600" />
                      <span class="text-xs font-medium text-blue-700">Humidity</span>
                    </div>
                    <p class="text-lg font-bold text-blue-800">{{ getSoilData(selectedNotification).humidity }}%</p>
                    <p class="text-xs text-blue-600 mt-1">{{ getHumidityDescription(getSoilData(selectedNotification).humidity) }}</p>
                  </div>
                  
                  <div class="bg-green-50 rounded-xl p-3 border-2 border-green-200 shadow-sm col-span-2">
                    <div class="flex items-center space-x-2 mb-1">
                      <Thermometer class="h-3 w-3 text-green-600" />
                      <span class="text-xs font-medium text-green-700">Soil Temperature</span>
                    </div>
                    <p class="text-lg font-bold text-green-800">{{ getSoilData(selectedNotification).temperature }}°C</p>
                    <p class="text-xs text-green-600 mt-1">{{ getTemperatureDescription(getSoilData(selectedNotification).temperature) }}</p>
                  </div>
                </div>
                
                <!-- Auto Irrigation Status -->
                <div class="bg-emerald-100 rounded-xl p-4 border-2 border-emerald-300 shadow-sm">
                  <div class="flex items-center space-x-2 mb-2">
                    <Sprout class="h-4 w-4 text-emerald-600" />
                    <span class="text-sm font-medium text-emerald-700">Irrigation Status</span>
                  </div>
                  <p class="text-sm text-emerald-800 font-bold">🚿 AUTO IRRIGATION IS BEING TRIGGERED SINCE SOIL MOISTURE IS LOW</p>
                  <p class="text-xs text-emerald-600 mt-1">System automatically activated to maintain optimal growing conditions</p>
                </div>
              </div>
              
              <!-- Water Level Notifications -->
              <div v-else-if="isWaterNotification(selectedNotification)" class="space-y-4">
                <p class="text-xs text-gray-600 mb-3 bg-white/60 rounded-lg p-2 border border-indigo-200">
                  Water management system status and reservoir levels. Critical for maintaining optimal irrigation capacity.
                </p>
                
                <div class="grid grid-cols-2 gap-3">
                  <div class="bg-cyan-50 rounded-xl p-3 border-2 border-cyan-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Gauge class="h-3 w-3 text-cyan-600" />
                      <span class="text-xs font-medium text-cyan-700">Water Level</span>
                    </div>
                    <p class="text-lg font-bold text-cyan-800">{{ getWaterData(selectedNotification).level }}%</p>
                    <p class="text-xs text-cyan-600 mt-1">{{ getWaterLevelDescription(getWaterData(selectedNotification).level) }}</p>
                  </div>
                  
                  <div class="bg-blue-50 rounded-xl p-3 border-2 border-blue-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Activity class="h-3 w-3 text-blue-600" />
                      <span class="text-xs font-medium text-blue-700">Flow Rate</span>
                    </div>
                    <p class="text-lg font-bold text-blue-800">{{ getWaterData(selectedNotification).flowRate }} L/min</p>
                    <p class="text-xs text-blue-600 mt-1">{{ getFlowRateDescription(getWaterData(selectedNotification).flowRate) }}</p>
                  </div>
                </div>
                
                <!-- Watering Capacity Estimation -->
                <div class="bg-blue-100 rounded-xl p-4 border-2 border-blue-300 shadow-sm">
                  <div class="flex items-center space-x-2 mb-2">
                    <Droplet class="h-4 w-4 text-blue-600" />
                    <span class="text-sm font-medium text-blue-700">Irrigation Capacity</span>
                  </div>
                  <div class="grid grid-cols-2 gap-3">
                    <div class="bg-white/60 rounded-lg p-2">
                      <p class="text-xs text-blue-600 font-medium">Estimated Sessions</p>
                      <p class="text-base font-bold text-blue-800">{{ getWateringCapacity(selectedNotification).sessions }}</p>
                    </div>
                    <div class="bg-white/60 rounded-lg p-2">
                      <p class="text-xs text-blue-600 font-medium">Coverage Area</p>
                      <p class="text-base font-bold text-blue-800">{{ getWateringCapacity(selectedNotification).coverage }}</p>
                    </div>
                  </div>
                  <p class="text-sm text-blue-700 font-medium mt-2">{{ getWateringRecommendation(selectedNotification) }}</p>
                </div>
              </div>
              
              <!-- System Notifications -->
              <div v-else-if="isSystemNotification(selectedNotification)" class="space-y-4">
                <p class="text-xs text-gray-600 mb-3 bg-white/60 rounded-lg p-2 border border-indigo-200">
                  System performance metrics and operational status. Monitoring ensures all agricultural systems function optimally.
                </p>
                
                <div class="grid grid-cols-2 gap-3">
                  <div class="bg-green-50 rounded-xl p-3 border-2 border-green-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Activity class="h-3 w-3 text-green-600" />
                      <span class="text-xs font-medium text-green-700">System Uptime</span>
                    </div>
                    <p class="text-lg font-bold text-green-800">{{ getSystemData(selectedNotification).uptime }}%</p>
                    <p class="text-xs text-green-600 mt-1">{{ getUptimeDescription(getSystemData(selectedNotification).uptime) }}</p>
                  </div>
                  
                  <div class="bg-blue-50 rounded-xl p-3 border-2 border-blue-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Database class="h-3 w-3 text-blue-600" />
                      <span class="text-xs font-medium text-blue-700">Data Points</span>
                    </div>
                    <p class="text-lg font-bold text-blue-800">{{ getSystemData(selectedNotification).dataPoints }}</p>
                    <p class="text-xs text-blue-600 mt-1">{{ getDataPointsDescription(getSystemData(selectedNotification).dataPoints) }}</p>
                  </div>
                  
                  <div class="bg-purple-50 rounded-xl p-3 border-2 border-purple-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Wifi class="h-3 w-3 text-purple-600" />
                      <span class="text-xs font-medium text-purple-700">Connectivity</span>
                    </div>
                    <p class="text-lg font-bold text-purple-800">{{ getSystemData(selectedNotification).connectivity }}%</p>
                    <p class="text-xs text-purple-600 mt-1">{{ getConnectivityDescription(getSystemData(selectedNotification).connectivity) }}</p>
                  </div>
                  
                  <div class="bg-yellow-50 rounded-xl p-3 border-2 border-yellow-200 shadow-sm">
                    <div class="flex items-center space-x-2 mb-1">
                      <Battery class="h-3 w-3 text-yellow-600" />
                      <span class="text-xs font-medium text-yellow-700">Power Status</span>
                    </div>
                    <p class="text-lg font-bold text-yellow-800">{{ getSystemData(selectedNotification).power }}%</p>
                    <p class="text-xs text-yellow-600 mt-1">{{ getPowerDescription(getSystemData(selectedNotification).power) }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Default/Other Notifications -->
              <div v-else class="space-y-3">
                <p class="text-sm text-gray-600 bg-white/60 rounded-lg p-3 border border-indigo-200">
                  {{ getDynamicAdditionalInfo(selectedNotification) }}
                </p>
                <div class="bg-blue-50 rounded-xl p-4 border-2 border-blue-200 shadow-sm">
                  <div class="flex items-center space-x-2 mb-2">
                    <Info class="h-4 w-4 text-blue-600" />
                    <span class="text-sm font-semibold text-blue-700">Status</span>
                  </div>
                  <p class="text-sm text-blue-800 font-medium">All systems operating within normal parameters</p>
                </div>
              </div>
            </div>

            <!-- Enhanced Metadata with Curved Containers -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Received Container -->
              <div class="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl p-4 border-2 border-emerald-200 shadow-lg">
                <div class="flex items-center space-x-2 mb-2">
                  <div class="w-6 h-6 bg-emerald-500 rounded-full flex items-center justify-center">
                    <CalendarClock class="h-3 w-3 text-white" />
                  </div>
                  <h4 class="text-sm font-bold text-emerald-700">Received</h4>
                </div>
                <p class="text-sm text-emerald-800 font-semibold">{{ formatFullDate(selectedNotification.time) }}</p>
              </div>
              
              <!-- Priority Container -->
              <div class="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-4 border-2 border-orange-200 shadow-lg">
                <div class="flex items-center space-x-2 mb-2">
                  <div class="w-6 h-6 bg-orange-500 rounded-full flex items-center justify-center">
                    <AlertTriangle class="h-3 w-3 text-white" />
                  </div>
                  <h4 class="text-sm font-bold text-orange-700">Priority</h4>
                </div>
                <p class="text-sm text-orange-800 font-semibold capitalize">{{ selectedNotification.severity || 'Normal' }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal Actions - Updated for Archive/Unarchive -->
        <div class="px-6 py-4 border-t border-gray-100 bg-gray-50 flex items-center justify-end space-x-3">
          <button 
            @click="closeDetails"
            class="px-4 py-2 bg-white hover:bg-gray-50 text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200"
          >
            Close
          </button>
          <button 
            v-if="!selectedNotification.read && !selectedNotification.archived"
            @click="markAsReadAndClose(selectedNotification.id)"
            class="flex items-center px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-sm font-medium transition-colors shadow-sm"
          >
            <Check class="h-4 w-4 mr-1.5" />
            Mark as Read
          </button>
          <button 
            v-if="!selectedNotification.archived"
            @click="archiveNotificationAndClose(selectedNotification.id)"
            class="flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg text-sm font-medium shadow-sm transition-colors duration-200 hover:bg-blue-600"
          >
            <Archive class="h-4 w-4 mr-1.5" />
            Archive
          </button>
          <button 
            v-if="selectedNotification.archived"
            @click="unarchiveNotificationAndClose(selectedNotification.id)"
            class="flex items-center px-4 py-2 bg-orange-500 text-white rounded-lg text-sm font-medium shadow-sm transition-colors duration-200 hover:bg-orange-600"
          >
            <ArchiveRestore class="h-4 w-4 mr-1.5" />
            Unarchive
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
      <!-- Container Wrapper -->
      <div class="flex-1 w-full px-4 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
        <!-- Main Container - Enhanced Design -->
        <div class="bg-white rounded-2xl shadow-md border border-emerald-100 h-[calc(100vh-140px)] overflow-hidden">
          <!-- Content Wrapper -->
          <div class="flex flex-col h-full">
            <!-- Enhanced Header Section -->
            <div class="p-5 border-b border-emerald-100 bg-gradient-to-r from-emerald-50 to-white">
              <!-- Header with improved layout -->
              <div class="flex items-center justify-between mb-5">
                <div class="flex items-center space-x-3">
                  <div class="p-2.5 bg-emerald-500 rounded-xl shadow-sm">
                    <component :is="showArchived ? Archive : Bell" class="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <h1 class="text-xl font-semibold text-gray-800">
                      {{ showArchived ? 'Archived Notifications' : 'Notifications' }}
                    </h1>
                    <p class="text-sm text-gray-500">
                      {{ showArchived ? 'View and manage your archived notifications' : 'Stay updated with your latest alerts and updates' }}
                    </p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <!-- Select Button -->
                  <button 
                    @click="toggleSelectMode"
                    :disabled="isLoading"
                    class="flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    :class="isSelectMode 
                      ? 'bg-red-500 hover:bg-red-600 text-white' 
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-700'"
                  >
                    <Check class="h-4 w-4 mr-1.5" />
                    {{ isSelectMode ? 'Cancel Selection' : 'Select' }}
                  </button>

                  <!-- Delete Selected Button -->
                  <button 
                    v-if="isSelectMode && selectedNotifications.size > 0"
                    @click="deleteSelectedNotifications"
                    :disabled="isLoading"
                    class="flex items-center px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Trash2 class="h-4 w-4 mr-1.5" />
                    Delete Selected ({{ selectedNotifications.size }})
                  </button>

                  <!-- Archive Toggle Button -->
                  <button 
                    @click="toggleArchiveView"
                    :disabled="isLoading"
                    class="flex items-center px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                    :class="showArchived 
                      ? 'bg-orange-500 hover:bg-orange-600 text-white' 
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-700'"
                  >
                    <component :is="showArchived ? Bell : Archive" class="h-4 w-4 mr-1.5" />
                    {{ showArchived ? 'Show Active' : 'Show Archived' }}
                  </button>
                  
                  <button 
                    v-if="!showArchived"
                    @click="markAllAsRead"
                    :disabled="isLoading"
                    class="flex items-center px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Check class="h-4 w-4 mr-1.5" />
                    Mark all read
                  </button>

                  <button 
                    v-if="!showArchived && !isSelectMode"
                    @click="confirmDeleteAll"
                    :disabled="isLoading || currentNotifications.length === 0"
                    class="flex items-center px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Trash2 class="h-4 w-4 mr-1.5" />
                    Delete All
                  </button>

                  <button 
                    @click="goBack"
                    class="flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors"
                  >
                    <ArrowLeft class="h-4 w-4 mr-1.5" />
                    Back
                  </button>
                </div>
              </div>

              <!-- Enhanced Filters and Search -->
              <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                <!-- Filter Buttons - Updated for archived view -->
                <div class="flex items-center justify-start gap-2 flex-wrap">
                  <button 
                    v-for="filter in (showArchived ? archivedFilters : filters)" 
                    :key="filter.value"
                    @click="activeFilter = filter.value"
                    :disabled="isLoading"
                    :class="[
                      'px-3 py-1.5 text-sm font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap',
                      activeFilter === filter.value 
                        ? 'bg-emerald-500 text-white shadow-sm' 
                        : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
                    ]"
                  >
                    {{ filter.label }}
                  </button>
                </div>
                
                <!-- Search Bar - Reduced width and improved responsiveness -->
                <div class="relative w-full sm:w-80 md:w-72 lg:w-64 xl:w-80 max-w-sm">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search class="h-4 w-4 text-gray-400" />
                  </div>
                  <input 
                    type="text"
                    v-model="searchQuery"
                    :disabled="isLoading"
                    :placeholder="showArchived ? 'Search archived notifications...' : 'Search notifications...'"
                    class="w-full pl-10 pr-4 py-2 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                </div>
              </div>
            </div>

            <!-- Scrollable Notifications Content with fixed spacing -->
            <div class="flex-1 overflow-y-auto notification-scroll">
              <!-- Empty State -->
              <div v-if="!isLoading && currentNotifications.length === 0" class="py-16 flex flex-col items-center justify-center">
                <div class="bg-gray-100 p-4 rounded-full mb-4">
                  <component :is="showArchived ? Archive : BellOff" class="h-8 w-8 text-gray-400" />
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-1">
                  {{ showArchived ? 'No archived notifications' : 'No notifications' }}
                </h3>
                <p class="text-sm text-gray-500 text-center">
                  {{ searchQuery 
                    ? 'No results found for your search.' 
                    : showArchived 
                      ? 'You don\'t have any archived notifications yet.' 
                      : 'You don\'t have any notifications yet.' 
                  }}
                </p>
              </div>

              <!-- Notifications - Enhanced Design with Consistent Spacing -->
              <div v-else-if="!isLoading" class="divide-y divide-gray-100">
                <!-- Today's Notifications -->
                <div v-if="todayNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-emerald-50 px-3 py-2 rounded-lg">
                    <CalendarClock class="h-4 w-4 text-emerald-600 mr-2" />
                    <span class="text-sm font-medium text-emerald-700">Today</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in todayNotifications" 
                      :key="notification.id"
                      @click="isSelectMode && !$event.target.closest('button') ? toggleNotificationSelection(notification.id) : null"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm cursor-pointer"
                      :class="{ 
                        'bg-blue-50/30 border-blue-200': !notification.read && !showArchived,
                        'bg-orange-50/30 border-orange-200': showArchived,
                        'ring-2 ring-emerald-500': isSelectMode && selectedNotifications.has(notification.id)
                      }"
                    >
                      <div class="flex items-start gap-3">
                        <!-- Checkbox for select mode -->
                        <div v-if="isSelectMode" class="flex-shrink-0 mt-1" @click.stop>
                          <input 
                            type="checkbox" 
                            :checked="selectedNotifications.has(notification.id)"
                            @click.stop="toggleNotificationSelection(notification.id)"
                            class="h-4 w-4 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500"
                          >
                        </div>
                        
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationIcon(notification).bgColor"
                        >
                          <component 
                            :is="getNotificationIcon(notification).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2 font-medium">
                            {{ notification.message }}
                          </p>
                          <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                              <span 
                                class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                                :class="getNotificationIcon(notification).badgeColor"
                              >
                                {{ notification.category || notification.type }}
                              </span>
                              <div v-if="!notification.read && !showArchived" class="flex items-center text-blue-600 text-xs font-medium">
                                <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                                Unread
                              </div>
                              <button 
                                v-if="showArchived"
                                @click.stop="handleQuickUnarchive(notification.id)"
                                :disabled="unarchivingIds.has(notification.id)"
                                class="flex items-center text-orange-600 hover:text-orange-700 text-xs font-medium bg-orange-50 hover:bg-orange-100 px-2 py-1 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                <component 
                                  :is="unarchivingIds.has(notification.id) ? 'div' : Archive" 
                                  :class="unarchivingIds.has(notification.id) ? 'animate-spin h-3 w-3 mr-1 border border-orange-600 border-t-transparent rounded-full' : 'h-3 w-3 mr-1'"
                                />
                                {{ unarchivingIds.has(notification.id) ? 'Unarchiving...' : 'Archived' }}
                              </button>
                              <!-- Green See Details Button -->
                              <button 
                                @click.stop="showDetails(notification)"
                                class="flex items-center px-2 py-1 text-xs font-medium text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 rounded-md transition-colors"
                              >
                                <Eye class="h-3 w-3 mr-1" />
                                See Details
                              </button>
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read && !showArchived"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="!showArchived"
                            @click.stop="archiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-indigo-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Archive"
                          >
                            <Archive class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="showArchived"
                            @click.stop="unarchiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-orange-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Unarchive"
                          >
                            <ArchiveRestore class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Yesterday's Notifications -->
                <div v-if="yesterdayNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-orange-50 px-3 py-2 rounded-lg">
                    <CalendarDays class="h-4 w-4 text-orange-600 mr-2" />
                    <span class="text-sm font-medium text-orange-700">Yesterday</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in yesterdayNotifications" 
                      :key="notification.id"
                      @click="isSelectMode && !$event.target.closest('button') ? toggleNotificationSelection(notification.id) : null"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm cursor-pointer"
                      :class="{ 
                        'bg-blue-50/30 border-blue-200': !notification.read && !showArchived,
                        'bg-orange-50/30 border-orange-200': showArchived,
                        'ring-2 ring-emerald-500': isSelectMode && selectedNotifications.has(notification.id)
                      }"
                    >
                      <div class="flex items-start gap-3">
                        <!-- Checkbox for select mode -->
                        <div v-if="isSelectMode" class="flex-shrink-0 mt-1" @click.stop>
                          <input 
                            type="checkbox" 
                            :checked="selectedNotifications.has(notification.id)"
                            @click.stop="toggleNotificationSelection(notification.id)"
                            class="h-4 w-4 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500"
                          >
                        </div>
                        
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationIcon(notification).bgColor"
                        >
                          <component 
                            :is="getNotificationIcon(notification).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2 font-medium">
                            {{ notification.message }}
                          </p>
                          <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                              <span 
                                class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                                :class="getNotificationIcon(notification).badgeColor"
                              >
                                {{ notification.category || notification.type }}
                              </span>
                              <div v-if="!notification.read && !showArchived" class="flex items-center text-blue-600 text-xs font-medium">
                                <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                                Unread
                              </div>
                              <button 
                                v-if="showArchived"
                                @click.stop="handleQuickUnarchive(notification.id)"
                                :disabled="unarchivingIds.has(notification.id)"
                                class="flex items-center text-orange-600 hover:text-orange-700 text-xs font-medium bg-orange-50 hover:bg-orange-100 px-2 py-1 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                <component 
                                  :is="unarchivingIds.has(notification.id) ? 'div' : Archive" 
                                  :class="unarchivingIds.has(notification.id) ? 'animate-spin h-3 w-3 mr-1 border border-orange-600 border-t-transparent rounded-full' : 'h-3 w-3 mr-1'"
                                />
                                {{ unarchivingIds.has(notification.id) ? 'Unarchiving...' : 'Archived' }}
                              </button>
                              <!-- Green See Details Button -->
                              <button 
                                @click.stop="showDetails(notification)"
                                class="flex items-center px-2 py-1 text-xs font-medium text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 rounded-md transition-colors"
                              >
                                <Eye class="h-3 w-3 mr-1" />
                                See Details
                              </button>
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read && !showArchived"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="!showArchived"
                            @click.stop="archiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-indigo-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Archive"
                          >
                            <Archive class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="showArchived"
                            @click.stop="unarchiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-orange-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Unarchive"
                          >
                            <ArchiveRestore class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- A Few Days Ago Notifications (2-6 days) -->
                <div v-if="fewDaysAgoNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-blue-50 px-3 py-2 rounded-lg">
                    <CalendarDays class="h-4 w-4 text-blue-600 mr-2" />
                    <span class="text-sm font-medium text-blue-700">A few days ago</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in fewDaysAgoNotifications" 
                      :key="notification.id"
                      @click="isSelectMode && !$event.target.closest('button') ? toggleNotificationSelection(notification.id) : null"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm cursor-pointer"
                      :class="{ 
                        'bg-blue-50/30 border-blue-200': !notification.read && !showArchived,
                        'bg-orange-50/30 border-orange-200': showArchived,
                        'ring-2 ring-emerald-500': isSelectMode && selectedNotifications.has(notification.id)
                      }"
                    >
                      <div class="flex items-start gap-3">
                        <!-- Checkbox for select mode -->
                        <div v-if="isSelectMode" class="flex-shrink-0 mt-1" @click.stop>
                          <input 
                            type="checkbox" 
                            :checked="selectedNotifications.has(notification.id)"
                            @click.stop="toggleNotificationSelection(notification.id)"
                            class="h-4 w-4 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500"
                          >
                        </div>
                        
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationIcon(notification).bgColor"
                        >
                          <component 
                            :is="getNotificationIcon(notification).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2 font-medium">
                            {{ notification.message }}
                          </p>
                          <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                              <span 
                                class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                                :class="getNotificationIcon(notification).badgeColor"
                              >
                                {{ notification.category || notification.type }}
                              </span>
                              <div v-if="!notification.read && !showArchived" class="flex items-center text-blue-600 text-xs font-medium">
                                <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                                Unread
                              </div>
                              <button 
                                v-if="showArchived"
                                @click.stop="handleQuickUnarchive(notification.id)"
                                :disabled="unarchivingIds.has(notification.id)"
                                class="flex items-center text-orange-600 hover:text-orange-700 text-xs font-medium bg-orange-50 hover:bg-orange-100 px-2 py-1 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                <component 
                                  :is="unarchivingIds.has(notification.id) ? 'div' : Archive" 
                                  :class="unarchivingIds.has(notification.id) ? 'animate-spin h-3 w-3 mr-1 border border-orange-600 border-t-transparent rounded-full' : 'h-3 w-3 mr-1'"
                                />
                                {{ unarchivingIds.has(notification.id) ? 'Unarchiving...' : 'Archived' }}
                              </button>
                              <!-- Green See Details Button -->
                              <button 
                                @click.stop="showDetails(notification)"
                                class="flex items-center px-2 py-1 text-xs font-medium text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 rounded-md transition-colors"
                              >
                                <Eye class="h-3 w-3 mr-1" />
                                See Details
                              </button>
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read && !showArchived"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="!showArchived"
                            @click.stop="archiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-indigo-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Archive"
                          >
                            <Archive class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="showArchived"
                            @click.stop="unarchiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-orange-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Unarchive"
                          >
                            <ArchiveRestore class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- A Week Ago Notifications (7-13 days) -->
                <div v-if="weekAgoNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-purple-50 px-3 py-2 rounded-lg">
                    <History class="h-4 w-4 text-purple-600 mr-2" />
                    <span class="text-sm font-medium text-purple-700">A week ago</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in weekAgoNotifications" 
                      :key="notification.id"
                      @click="isSelectMode && !$event.target.closest('button') ? toggleNotificationSelection(notification.id) : null"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm cursor-pointer"
                      :class="{ 
                        'bg-blue-50/30 border-blue-200': !notification.read && !showArchived,
                        'bg-orange-50/30 border-orange-200': showArchived,
                        'ring-2 ring-emerald-500': isSelectMode && selectedNotifications.has(notification.id)
                      }"
                    >
                      <div class="flex items-start gap-3">
                        <!-- Checkbox for select mode -->
                        <div v-if="isSelectMode" class="flex-shrink-0 mt-1" @click.stop>
                          <input 
                            type="checkbox" 
                            :checked="selectedNotifications.has(notification.id)"
                            @click.stop="toggleNotificationSelection(notification.id)"
                            class="h-4 w-4 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500"
                          >
                        </div>
                        
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationIcon(notification).bgColor"
                        >
                          <component 
                            :is="getNotificationIcon(notification).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2 font-medium">
                            {{ notification.message }}
                          </p>
                          <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                              <span 
                                class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                                :class="getNotificationIcon(notification).badgeColor"
                              >
                                {{ notification.category || notification.type }}
                              </span>
                              <div v-if="!notification.read && !showArchived" class="flex items-center text-blue-600 text-xs font-medium">
                                <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                                Unread
                              </div>
                              <button 
                                v-if="showArchived"
                                @click.stop="handleQuickUnarchive(notification.id)"
                                :disabled="unarchivingIds.has(notification.id)"
                                class="flex items-center text-orange-600 hover:text-orange-700 text-xs font-medium bg-orange-50 hover:bg-orange-100 px-2 py-1 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                <component 
                                  :is="unarchivingIds.has(notification.id) ? 'div' : Archive" 
                                  :class="unarchivingIds.has(notification.id) ? 'animate-spin h-3 w-3 mr-1 border border-orange-600 border-t-transparent rounded-full' : 'h-3 w-3 mr-1'"
                                />
                                {{ unarchivingIds.has(notification.id) ? 'Unarchiving...' : 'Archived' }}
                              </button>
                              <!-- Green See Details Button -->
                              <button 
                                @click.stop="showDetails(notification)"
                                class="flex items-center px-2 py-1 text-xs font-medium text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 rounded-md transition-colors"
                              >
                                <Eye class="h-3 w-3 mr-1" />
                                See Details
                              </button>
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read && !showArchived"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="!showArchived"
                            @click.stop="archiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-indigo-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Archive"
                          >
                            <Archive class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="showArchived"
                            @click.stop="unarchiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-orange-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Unarchive"
                          >
                            <ArchiveRestore class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- A Few Weeks Ago Notifications (14-29 days) -->
                <div v-if="fewWeeksAgoNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-indigo-50 px-3 py-2 rounded-lg">
                    <History class="h-4 w-4 text-indigo-600 mr-2" />
                    <span class="text-sm font-medium text-indigo-700">A few weeks ago</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in fewWeeksAgoNotifications" 
                      :key="notification.id"
                      @click="isSelectMode && !$event.target.closest('button') ? toggleNotificationSelection(notification.id) : null"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm cursor-pointer"
                      :class="{ 
                        'bg-blue-50/30 border-blue-200': !notification.read && !showArchived,
                        'bg-orange-50/30 border-orange-200': showArchived,
                        'ring-2 ring-emerald-500': isSelectMode && selectedNotifications.has(notification.id)
                      }"
                    >
                      <div class="flex items-start gap-3">
                        <!-- Checkbox for select mode -->
                        <div v-if="isSelectMode" class="flex-shrink-0 mt-1" @click.stop>
                          <input 
                            type="checkbox" 
                            :checked="selectedNotifications.has(notification.id)"
                            @click.stop="toggleNotificationSelection(notification.id)"
                            class="h-4 w-4 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500"
                          >
                        </div>
                        
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationIcon(notification).bgColor"
                        >
                          <component 
                            :is="getNotificationIcon(notification).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2 font-medium">
                            {{ notification.message }}
                          </p>
                          <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                              <span 
                                class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                                :class="getNotificationIcon(notification).badgeColor"
                              >
                                {{ notification.category || notification.type }}
                              </span>
                              <div v-if="!notification.read && !showArchived" class="flex items-center text-blue-600 text-xs font-medium">
                                <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                                Unread
                              </div>
                              <button 
                                v-if="showArchived"
                                @click.stop="handleQuickUnarchive(notification.id)"
                                :disabled="unarchivingIds.has(notification.id)"
                                class="flex items-center text-orange-600 hover:text-orange-700 text-xs font-medium bg-orange-50 hover:bg-orange-100 px-2 py-1 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                <component 
                                  :is="unarchivingIds.has(notification.id) ? 'div' : Archive" 
                                  :class="unarchivingIds.has(notification.id) ? 'animate-spin h-3 w-3 mr-1 border border-orange-600 border-t-transparent rounded-full' : 'h-3 w-3 mr-1'"
                                />
                                {{ unarchivingIds.has(notification.id) ? 'Unarchiving...' : 'Archived' }}
                              </button>
                              <!-- Green See Details Button -->
                              <button 
                                @click.stop="showDetails(notification)"
                                class="flex items-center px-2 py-1 text-xs font-medium text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 rounded-md transition-colors"
                              >
                                <Eye class="h-3 w-3 mr-1" />
                                See Details
                              </button>
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read && !showArchived"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="!showArchived"
                            @click.stop="archiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-indigo-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Archive"
                          >
                            <Archive class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="showArchived"
                            @click.stop="unarchiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-orange-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Unarchive"
                          >
                            <ArchiveRestore class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- A Month Ago Notifications (30+ days) -->
                <div v-if="monthAgoNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-gray-50 px-3 py-2 rounded-lg">
                    <History class="h-4 w-4 text-gray-600 mr-2" />
                    <span class="text-sm font-medium text-gray-700">A month ago</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in monthAgoNotifications" 
                      :key="notification.id"
                      @click="isSelectMode && !$event.target.closest('button') ? toggleNotificationSelection(notification.id) : null"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm cursor-pointer"
                      :class="{ 
                        'bg-blue-50/30 border-blue-200': !notification.read && !showArchived,
                        'bg-orange-50/30 border-orange-200': showArchived,
                        'ring-2 ring-emerald-500': isSelectMode && selectedNotifications.has(notification.id)
                      }"
                    >
                      <div class="flex items-start gap-3">
                        <!-- Checkbox for select mode -->
                        <div v-if="isSelectMode" class="flex-shrink-0 mt-1" @click.stop>
                          <input 
                            type="checkbox" 
                            :checked="selectedNotifications.has(notification.id)"
                            @click.stop="toggleNotificationSelection(notification.id)"
                            class="h-4 w-4 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500"
                          >
                        </div>
                        
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationIcon(notification).bgColor"
                        >
                          <component 
                            :is="getNotificationIcon(notification).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2 font-medium">
                            {{ notification.message }}
                          </p>
                          <div class="flex items-center justify-between">
                            <div class="flex items-center gap-2">
                              <span 
                                class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                                :class="getNotificationIcon(notification).badgeColor"
                              >
                                {{ notification.category || notification.type }}
                              </span>
                              <div v-if="!notification.read && !showArchived" class="flex items-center text-blue-600 text-xs font-medium">
                                <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                                Unread
                              </div>
                              <button 
                                v-if="showArchived"
                                @click.stop="handleQuickUnarchive(notification.id)"
                                :disabled="unarchivingIds.has(notification.id)"
                                class="flex items-center text-orange-600 hover:text-orange-700 text-xs font-medium bg-orange-50 hover:bg-orange-100 px-2 py-1 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                              >
                                <component 
                                  :is="unarchivingIds.has(notification.id) ? 'div' : Archive" 
                                  :class="unarchivingIds.has(notification.id) ? 'animate-spin h-3 w-3 mr-1 border border-orange-600 border-t-transparent rounded-full' : 'h-3 w-3 mr-1'"
                                />
                                {{ unarchivingIds.has(notification.id) ? 'Unarchiving...' : 'Archived' }}
                              </button>
                              <!-- Green See Details Button -->
                              <button 
                                @click.stop="showDetails(notification)"
                                class="flex items-center px-2 py-1 text-xs font-medium text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 rounded-md transition-colors"
                              >
                                <Eye class="h-3 w-3 mr-1" />
                                See Details
                              </button>
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read && !showArchived"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="!showArchived"
                            @click.stop="archiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-indigo-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Archive"
                          >
                            <Archive class="h-4 w-4" />
                          </button>
                          <button 
                            v-if="showArchived"
                            @click.stop="unarchiveNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-orange-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Unarchive"
                          >
                            <ArchiveRestore class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- No notifications in current view -->
                <div v-if="paginatedNotifications.length === 0 && filteredNotifications.length > 0" class="px-5 py-12 text-center">
                  <Bell class="h-10 w-10 text-gray-300 mx-auto mb-3" />
                  <p class="text-gray-500">No notifications on this page</p>
                  <button 
                    @click="currentPage = 1"
                    class="mt-3 text-sm text-emerald-600 hover:text-emerald-700"
                  >
                    Go to first page
                  </button>
                </div>
              </div>
            </div>

            <!-- Enhanced Pagination Footer with Items Per Page Selector -->
            <div class="px-5 py-4 border-t border-gray-100 bg-gradient-to-r from-white to-emerald-50/30">
              <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                  <div class="flex items-center">
                    <span class="text-sm text-gray-600 mr-2">Show</span>
                    <select 
                      v-model="itemsPerPage" 
                      @change="handleItemsPerPageChange"
                      :disabled="isLoading"
                      class="bg-white border border-gray-200 text-gray-700 rounded-lg px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
                        {{ option }}
                      </option>
                    </select>
                    <span class="text-sm text-gray-600 ml-2">per page</span>
                  </div>
                  
                  <div class="hidden sm:flex items-center">
                    <span class="text-sm text-gray-600 mr-2">|</span>
                    <span class="text-sm text-gray-600">
                      Showing <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, filteredNotifications.length) }}</span> of <span class="font-medium">{{ filteredNotifications.length }}</span>
                    </span>
                  </div>
                </div>
                
                <!-- Smart Pagination with Enhanced Design -->
                <div class="flex items-center gap-2">
                  <button 
                    @click="prevPage"
                    :disabled="currentPage === 1 || isLoading"
                    class="inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium transition-colors rounded-lg
                      disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                      enabled:text-gray-700 enabled:hover:text-emerald-600 enabled:hover:bg-emerald-50 enabled:border enabled:border-gray-200"
                  >
                    <ChevronLeft class="w-4 h-4 mr-1" />
                    Prev
                  </button>

                  <div class="flex items-center gap-1">
                    <button
                      v-for="page in displayedPages"
                      :key="page"
                      @click="goToPage(page)"
                      :disabled="isLoading"
                      :class="[
                        'relative inline-flex items-center justify-center w-8 h-8 text-sm transition-colors rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed',
                        page === currentPage
                          ? 'text-white bg-emerald-500 shadow-sm'
                          : page === '...'
                            ? 'cursor-default text-gray-400'
                            : 'text-gray-700 hover:text-emerald-600 hover:bg-emerald-50 border border-gray-200'
                      ]"
                    >
                      {{ page }}
                    </button>
                  </div>

                  <button 
                    @click="nextPage"
                    :disabled="currentPage >= totalPages || totalPages === 0 || isLoading"
                    class="inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium transition-colors rounded-lg
                      disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                      enabled:text-gray-700 enabled:hover:text-emerald-600 enabled:hover:bg-emerald-50 enabled:border enabled:border-gray-200"
                  >
                    Next
                    <ChevronRight class="w-4 h-4 ml-1" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    <Transition name="toast">
      <div
        v-if="showToast"
        :class="[
          'fixed bottom-4 right-4 rounded-lg shadow-lg border p-4 flex items-center gap-3 z-[10001] max-w-md',
          toastStyles[toastType].bg,
          toastStyles[toastType].border
        ]"
      >
        <div :class="[toastStyles[toastType].iconBg, 'p-2 rounded-full']">
          <component :is="toastStyles[toastType].icon" class="w-5 h-5" :class="toastStyles[toastType].iconColor" />
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

    <!-- Add this modal near the other modals in the template -->
    <div v-if="showDeleteAllConfirmation" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-800">Confirm Delete All</h3>
          <button @click="showDeleteAllConfirmation = false" class="text-gray-400 hover:text-gray-600">
            <X class="w-5 h-5" />
          </button>
        </div>
        <p class="text-gray-600 mb-6">Are you sure you want to delete all {{ showArchived ? 'archived' : '' }} notifications? This action cannot be undone.</p>
        <div class="flex justify-end space-x-3">
          <button 
            @click="showDeleteAllConfirmation = false"
            class="px-4 py-2 bg-white hover:bg-gray-50 text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200"
          >
            Cancel
          </button>
          <button 
            @click="deleteAllNotifications"
            :disabled="isDeletingAll"
            class="flex items-center px-4 py-2 bg-red-500 hover:bg-red-600 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Trash2 class="h-4 w-4 mr-1.5" />
            {{ isDeletingAll ? 'Deleting...' : 'Delete All' }}
          </button>
        </div>
      </div>
    </div>

    <Settings />
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { eventBus } from '../../eventBus'
import {
  Bell, BellOff, Check, ArrowLeft, Search, ChevronLeft, ChevronRight,
  AlertTriangle, Info, AlertCircle, Droplet, Leaf, BarChart, Cog, Trash2,
  CalendarClock, CalendarDays, History, Eye, Archive, X, CloudRain, 
  Thermometer, Wind, Sun, Cloud, Zap, Sprout, TreePine, Wheat, 
  Activity, Database, Wifi, WifiOff, Battery, BatteryLow, Settings2,
  TrendingUp, TrendingDown, MapPin, Gauge, ArchiveRestore
} from 'lucide-vue-next'
import Sidebar from '../layout/Sidebar.vue'
import Settings from '../layout/Settings.vue'
import {
  getFirestore,
  collection,
  getDocs,
  query,
  orderBy,
  doc,
  updateDoc,
  deleteDoc,
  getDoc,
  setDoc,
  onSnapshot,
  writeBatch
} from 'firebase/firestore'
import { getCurrentInstance } from 'vue'
import { getWeatherData, mapWeatherCode } from '../../utils/weather.js';

// Firestore DB reference
const db = getFirestore()

// Loading state
const isLoading = ref(true)
const loadingDotIndex = ref(0)
let loadingInterval = null
const showToast = ref(false)
const toastMessage = ref('')
const toastTimeout = ref(null)
const toastQueue = ref([]);
const isToastActive = ref(false);
const deletingIds = ref(new Set())
const archivingIds = ref(new Set())
// const unarchivingIds = ref(new Set())

// Notification details modal
const selectedNotification = ref(null)
const showDeleteAllConfirmation = ref(false)
const isDeletingAll = ref(false)
const notifications = ref([])

// Archive view toggle
const showArchived = ref(false)

// Replace your current toastStyles computed with this:
const toastType = ref('info') 
// Add to your script setup
const weatherModalData = ref(null);

watch(selectedNotification, async (newVal) => {
  if (newVal && isWeatherNotification(newVal)) {
    weatherModalData.value = await fetchWeatherForModal(newVal);
  } else {
    weatherModalData.value = null;
  }
});

watch(notifications, (newVal) => {
  const ids = newVal.map(n => n.id)
  const duplicates = ids.filter((id, index) => ids.indexOf(id) !== index)
  if (duplicates.length) {
    console.error('Duplicate notification IDs detected:', duplicates)
  }
}, { deep: true })

const toastStyles = {
  success: {
    bg: 'bg-green-50',
    border: 'border-green-200',
    iconBg: 'bg-green-100',
    icon: Check,
    iconColor: 'text-green-600'
  },
  error: {
    bg: 'bg-red-50',
    border: 'border-red-200',
    iconBg: 'bg-red-100',
    icon: AlertTriangle,
    iconColor: 'text-red-600'
  },
  info: {
    bg: 'bg-blue-50',
    border: 'border-blue-200',
    iconBg: 'bg-blue-100',
    icon: Info,
    iconColor: 'text-blue-600'
  }
}

const showToastMessage = (message, type = 'info') => {
  toastMessage.value = message
  toastType.value = type
  showToast.value = true
  
  if (toastTimeout.value) {
    clearTimeout(toastTimeout.value)
  }
  
  toastTimeout.value = setTimeout(() => {
    showToast.value = false
  }, 3000)
}

// Filters
const filters = [
  { label: 'All', value: 'all' },
  { label: 'Unread', value: 'unread' },
  { label: 'System', value: 'system' },
  { label: 'Alerts', value: 'alert' },
  { label: 'Data', value: 'data' }
]

// Archived filters (no unread filter for archived)
const archivedFilters = [
  { label: 'All', value: 'all' },
  { label: 'System', value: 'system' },
  { label: 'Alerts', value: 'alert' },
  { label: 'Data', value: 'data' }
]

const activeFilter = ref('all')
const searchQuery = ref('')
const currentPage = ref(1)

// Items per page options and default value
const itemsPerPageOptions = [4, 10, 15, 20, 25, 30]
const itemsPerPage = ref(4) // Default is 4

// Store user preference in localStorage
const loadUserPreferences = () => {
  try {
    const savedItemsPerPage = localStorage.getItem('notificationsPerPage')
    if (savedItemsPerPage) {
      const parsedValue = parseInt(savedItemsPerPage)
      if (itemsPerPageOptions.includes(parsedValue)) {
        itemsPerPage.value = parsedValue
      }
    }
  } catch (error) {
    console.error('Error loading user preferences:', error)
  }
}

const saveUserPreferences = () => {
  try {
    localStorage.setItem('notificationsPerPage', itemsPerPage.value.toString())
  } catch (error) {
    console.error('Error saving user preferences:', error)
  }
}

const handleItemsPerPageChange = () => {
  currentPage.value = 1 // Reset to first page when changing items per page
  saveUserPreferences() // Save user preference
}

// const notifications = ref([])
const archivedNotifications = ref([])
const NOTIF_COLLECTION = "notifications"

// Add this after the existing loading states
const unarchivingIds = ref(new Set())

// Toggle archive view
const toggleArchiveView = () => {
  showArchived.value = !showArchived.value
  activeFilter.value = 'all' // Reset filter when switching views
  currentPage.value = 1 // Reset to first page
}

// Current notifications based on view
const currentNotifications = computed(() => {
  return showArchived.value ? archivedNotifications.value : notifications.value
})

const selectedNotifications = ref(new Set());
const isSelectMode = ref(false);

const handleNotificationClick = (id, event) => {
  if (isSelectMode.value && !event.target.closest('button')) {
    toggleNotificationSelection(id)
  } else if (!isSelectMode.value) {
    const notification = currentNotifications.value.find(n => n.id === id)
    if (notification) showDetails(notification)
  }
}

// Toggle select mode
const toggleSelectMode = () => {
  isSelectMode.value = !isSelectMode.value
  if (!isSelectMode.value) {
    selectedNotifications.value = new Set()
  }
}

// Toggle selection of a notification
const toggleNotificationSelection = (id) => {
  const newSelection = new Set(selectedNotifications.value)
  if (newSelection.has(id)) {
    newSelection.delete(id)
  } else {
    newSelection.add(id)
  }
  selectedNotifications.value = newSelection
}

const confirmDeleteAll = () => {
  showDeleteAllConfirmation.value = true
}

const deleteAllNotifications = async () => {
  try {
    isDeletingAll.value = true
    showDeleteAllConfirmation.value = false
    
    // Get all documents in the collection
    const q = query(collection(db, NOTIF_COLLECTION))
    const querySnapshot = await getDocs(q)
    
    if (querySnapshot.empty) {
      showToastMessage('No notifications to delete', 'info')
      return
    }

    // Use batch delete for better performance
    const batch = writeBatch(db)
    querySnapshot.forEach((doc) => {
      batch.delete(doc.ref)
    })

    await batch.commit()
    
    // Clear local state
    notifications.value = []
    archivedNotifications.value = []
    
    showToastMessage(`All notifications deleted successfully`, 'success')
  } catch (error) {
    console.error('Failed to delete all notifications:', error)
    showToastMessage('Failed to delete all notifications', 'error')
  } finally {
    isDeletingAll.value = false
  }
}

const deleteSelectedNotifications = async () => {
  if (selectedNotifications.value.size === 0) return

  try {
    isLoading.value = true
    const deletePromises = Array.from(selectedNotifications.value).map(id => 
      deleteDoc(doc(db, 'notifications', id)))
    
    await Promise.all(deletePromises)
    
    // Update local state
    notifications.value = notifications.value.filter(
      n => !selectedNotifications.value.has(n.id)
    )
    archivedNotifications.value = archivedNotifications.value.filter(
      n => !selectedNotifications.value.has(n.id)
    )
    
    showToastMessage(
      `${selectedNotifications.value.size} notification(s) deleted`, 
      'success'
    )
    selectedNotifications.value = new Set()
    isSelectMode.value = false
    
  } catch (error) {
    console.error('Error deleting notifications:', error)
    showToastMessage('Failed to delete notifications', 'error')
  } finally {
    isLoading.value = false
  }
}

// Notification details methods
const showDetails = (notification) => {
  selectedNotification.value = notification
}

const closeDetails = () => {
  selectedNotification.value = null
}

const markAsReadAndClose = async (id) => {
  await markAsRead(id)
  closeDetails()
}

const archiveNotificationAndClose = async (id) => {
  await archiveNotification(id)
  closeDetails()
}

const unarchiveNotificationAndClose = async (id) => {
  await unarchiveNotification(id)
  closeDetails()
}

// Modified archiveNotification with loading and toast
const archiveNotification = async (docId) => {
  try {
    archivingIds.value.add(docId);
    
    const notifIndex = notifications.value.findIndex(n => n.id === docId);
    if (notifIndex === -1) {
      throw new Error('Notification not found in local state');
    }

    const notification = notifications.value[notifIndex];
    
    const updateData = {
      archived: true,
      read: true,
      archivedAt: new Date()
    };

    const notifRef = doc(db, NOTIF_COLLECTION, docId);
    await updateDoc(notifRef, updateData);

    const updatedNotification = {
      ...notification,
      ...updateData
    };

    archivedNotifications.value.unshift(updatedNotification);
    notifications.value.splice(notifIndex, 1);

    showToastMessage('Notification archived', 'success');
  } catch (err) {
    console.error("❌ Failed to archive notification:", err);
    showToastMessage(`Failed to archive notification: ${err.message}`, 'error');
  } finally {
    archivingIds.value.delete(docId);
  }
};

// Modified unarchiveNotification with loading and toast
const unarchiveNotification = async (docId) => {
  try {
    unarchivingIds.value.add(docId)
    
    const notifIndex = archivedNotifications.value.findIndex(n => n.id === docId)
    if (notifIndex !== -1) {
      const notification = archivedNotifications.value[notifIndex]
      notification.archived = false

      // Move back to active notifications array
      notifications.value.unshift(notification)
      archivedNotifications.value.splice(notifIndex, 1)

      // Firestore update
      const notifRef = doc(db, NOTIF_COLLECTION, docId)
      await updateDoc(notifRef, { 
        archived: false,
        archivedAt: null
      })
      
      showToastMessage('Notification unarchived', 'success')
    }
  } catch (err) {
    console.error("❌ Failed to unarchive notification:", err)
    showToastMessage('Failed to unarchive notification', 'error')
  } finally {
    unarchivingIds.value.delete(id)
  }
}

// Add this function with the other notification methods
const handleQuickUnarchive = async (id) => {
  try {
    unarchivingIds.value.add(id)
    
    const notifIndex = archivedNotifications.value.findIndex(n => n.id === id)
    if (notifIndex !== -1) {
      const notification = archivedNotifications.value[notifIndex]
      notification.archived = false

      // Move back to active notifications array
      notifications.value.unshift(notification)
      archivedNotifications.value.splice(notifIndex, 1)

      // Firestore update
      const notifRef = doc(db, NOTIF_COLLECTION, id)
      await updateDoc(notifRef, { 
        archived: false,
        archivedAt: null
      })
      
      // Show success feedback and redirect after a short delay
      setTimeout(() => {
        showArchived.value = false
        activeFilter.value = 'all'
        currentPage.value = 1
      }, 500)
    }
  } catch (err) {
    console.error("❌ Failed to unarchive notification:", err)
  } finally {
    unarchivingIds.value.delete(id)
  }
}

const isWeatherNotification = (notification) => {
  return notification.type === 'weather' || 
         notification.category === 'weather' ||
         notification.title?.toLowerCase().includes('weather');
};

// Check if notification is soil-related
const isSoilNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
  return title.includes('soil') || title.includes('moisture') || 
         message.includes('soil') || message.includes('moisture') ||
         category.includes('soil') || type.includes('soil')
}

// Check if notification is water-related
const isWaterNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
  return title.includes('water') || title.includes('level') || title.includes('irrigation') ||
         message.includes('water') || message.includes('level') || message.includes('irrigation') ||
         category.includes('water') || type.includes('water')
}

// Check if notification is system-related
const isSystemNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
  return title.includes('system') || title.includes('device') || title.includes('sensor') ||
         message.includes('system') || message.includes('device') || message.includes('sensor') ||
         category.includes('system') || type.includes('system')
}

const fetchWeatherForModal = async (notification) => {
  try {
    const weather = await getWeatherData();
    return {
      humidity: weather.current.humidity,
      pressure: weather.current.pressure,
      windSpeed: weather.current.wind_speed,
      uvIndex: weather.current.uv_index,
      rainIntensity: weather.current.rainChance,
      temperature: weather.current.temperature_c,
      weatherCondition: weather.current.weather_condition
    };
  } catch (error) {
    console.error("Failed to fetch weather data:", error);
    return null;
  }
};

// Generate soil data with humidity
const getSoilData = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  
  let baseMoisture = 45
  let baseTemp = 22
  let baseHumidity = 65
  
  if (title.includes('low') || message.includes('low')) {
    baseMoisture = 15
    baseHumidity = 45
  } else if (title.includes('critical') || message.includes('critical')) {
    baseMoisture = 8
    baseHumidity = 35
  }
  
  return {
    moistureLevel: Math.max(5, Math.min(100, baseMoisture + Math.random() * 10 - 5)),
    temperature: Math.round((baseTemp + Math.random() * 6 - 3) * 10) / 10,
    humidity: Math.max(30, Math.min(100, Math.round(baseHumidity + Math.random() * 10 - 5)))
  }
}

// Generate water data
const getWaterData = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  
  let baseLevel = 75
  let baseFlow = 45
  
  if (title.includes('low') || message.includes('low')) {
    baseLevel = 25
    baseFlow = 15
  } else if (title.includes('critical') || message.includes('critical')) {
    baseLevel = 10
    baseFlow = 5
  }
  
  return {
    level: Math.max(0, Math.min(100, baseLevel + Math.random() * 10 - 5)),
    flowRate: Math.max(0, Math.round((baseFlow + Math.random() * 10 - 5) * 10) / 10)
  }
}

// Generate watering capacity estimation
const getWateringCapacity = (notification) => {
  const waterLevel = getWaterData(notification).level
  
  let sessions = 0
  let coverage = '0 m²'
  
  if (waterLevel >= 80) {
    sessions = Math.floor(12 + Math.random() * 6) // 12-18 sessions
    coverage = '500-800 m²'
  } else if (waterLevel >= 60) {
    sessions = Math.floor(8 + Math.random() * 4) // 8-12 sessions
    coverage = '300-500 m²'
  } else if (waterLevel >= 40) {
    sessions = Math.floor(4 + Math.random() * 4) // 4-8 sessions
    coverage = '150-300 m²'
  } else if (waterLevel >= 20) {
    sessions = Math.floor(2 + Math.random() * 2) // 2-4 sessions
    coverage = '50-150 m²'
  } else {
    sessions = Math.floor(1 + Math.random()) // 1-2 sessions
    coverage = '10-50 m²'
  }
  
  return { sessions, coverage }
}

// Generate watering recommendation
const getWateringRecommendation = (notification) => {
  const waterLevel = getWaterData(notification).level
  
  if (waterLevel >= 80) {
    return 'Excellent water reserves. Full irrigation capacity available for extended operations.'
  } else if (waterLevel >= 60) {
    return 'Good water levels. Sufficient for regular irrigation schedule with some reserve.'
  } else if (waterLevel >= 40) {
    return 'Moderate water levels. Consider prioritizing critical areas for irrigation.'
  } else if (waterLevel >= 20) {
    return 'Low water levels. Immediate refill recommended. Limit irrigation to essential areas only.'
  } else {
    return 'Critical water shortage. Emergency refill required. Suspend all non-essential irrigation.'
  }
}

// Generate system data
const getSystemData = (notification) => {
  return {
    uptime: Math.max(85, Math.min(100, 99.2 + Math.random() * 0.8 - 0.4)),
    dataPoints: Math.floor(1500 + Math.random() * 500),
    connectivity: Math.max(90, Math.min(100, 98 + Math.random() * 2 - 1)),
    power: Math.max(70, Math.min(100, 85 + Math.random() * 15 - 7.5))
  }
}

// Description functions for weather data
const getHumidityDescription = (humidity) => {
  if (humidity >= 80) return 'Very humid conditions'
  if (humidity >= 60) return 'Moderate humidity'
  if (humidity >= 40) return 'Comfortable levels'
  return 'Low humidity'
}

const getPressureDescription = (pressure) => {
  if (pressure >= 1020) return 'High pressure system'
  if (pressure >= 1000) return 'Normal pressure'
  return 'Low pressure system'
}

const getWindDescription = (windSpeed) => {
  if (windSpeed >= 25) return 'Strong winds'
  if (windSpeed >= 15) return 'Moderate winds'
  if (windSpeed >= 5) return 'Light breeze'
  return 'Calm conditions'
}

const getUVDescription = (uvIndex) => {
  if (uvIndex >= 8) return 'Very high exposure'
  if (uvIndex >= 6) return 'High UV levels'
  if (uvIndex >= 3) return 'Moderate exposure'
  return 'Low UV levels'
}

// Description functions for soil data
const getMoistureDescription = (moisture) => {
  if (moisture >= 60) return 'Optimal moisture'
  if (moisture >= 40) return 'Adequate levels'
  if (moisture >= 20) return 'Needs watering'
  return 'Critical - water immediately'
}

const getTemperatureDescription = (temp) => {
  if (temp >= 25) return 'Warm soil conditions'
  if (temp >= 18) return 'Optimal temperature'
  if (temp >= 10) return 'Cool conditions'
  return 'Cold soil'
}

// Description functions for water data
const getWaterLevelDescription = (level) => {
  if (level >= 80) return 'Excellent water supply'
  if (level >= 50) return 'Adequate reserves'
  if (level >= 25) return 'Monitor closely'
  return 'Critical - refill needed'
}

const getFlowRateDescription = (flow) => {
  if (flow >= 40) return 'Strong flow rate'
  if (flow >= 20) return 'Normal flow'
  if (flow >= 10) return 'Reduced flow'
  return 'Very low flow'
}

// Description functions for system data
const getUptimeDescription = (uptime) => {
  if (uptime >= 99) return 'Excellent reliability'
  if (uptime >= 95) return 'Good performance'
  if (uptime >= 90) return 'Acceptable uptime'
  return 'Needs attention'
}

const getDataPointsDescription = (points) => {
  return `${points} readings collected today`
}

const getConnectivityDescription = (connectivity) => {
  if (connectivity >= 95) return 'Strong connection'
  if (connectivity >= 85) return 'Good connectivity'
  if (connectivity >= 70) return 'Fair connection'
  return 'Poor connectivity'
}

const getPowerDescription = (power) => {
  if (power >= 90) return 'Full power'
  if (power >= 75) return 'Good battery level'
  if (power >= 50) return 'Moderate charge'
  return 'Low battery - charge soon'
}

// Get rain rating based on intensity
const getRainRating = (notification) => {
  const intensity = getWeatherData(notification).rainIntensity
  
  if (intensity >= 80) return 'Heavy'
  if (intensity >= 60) return 'Moderate'
  if (intensity >= 40) return 'Light'
  return 'Drizzle'
}

const getRainDescription = (notification) => {
  const rating = getRainRating(notification)
  if (rating === 'Heavy') return 'Expect significant rainfall with potential flooding'
  if (rating === 'Moderate') return 'Steady rain expected, plan accordingly'
  if (rating === 'Light') return 'Light precipitation, minimal impact expected'
  return 'Very light rain or drizzle'
}

// Generate dynamic additional information for non-weather notifications
const getDynamicAdditionalInfo = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
  if (title.includes('system') || type.includes('system')) {
    return 'System performance metrics show normal operation. All services are running optimally with 99.9% uptime recorded in the last 24 hours.'
  }
  
  if (title.includes('sensor') || message.includes('sensor')) {
    return 'Sensor readings indicate stable environmental conditions. Data collection is proceeding normally with all monitoring devices responding correctly.'
  }
  
  if (title.includes('crop') || title.includes('plant')) {
    return 'Crop monitoring data shows healthy growth patterns. Soil conditions are optimal for current growth stage with adequate nutrient levels detected.'
  }
  
  if (title.includes('water') || title.includes('irrigation')) {
    return 'Water management systems are functioning properly. Current water levels are within acceptable ranges for optimal crop irrigation.'
  }
  
  return `Detailed analysis of ${notification.title || 'this notification'} indicates normal operational parameters. All associated systems are functioning within expected ranges.`
}

// Format full date for details modal
const formatFullDate = (time) => {
  if (!time) return 'Unknown date'
  return new Date(time).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Loading animation
const startLoadingAnimation = () => {
  loadingInterval = setInterval(() => {
    loadingDotIndex.value = (loadingDotIndex.value + 1) % 5
  }, 300)
}

const stopLoadingAnimation = () => {
  if (loadingInterval) {
    clearInterval(loadingInterval)
    loadingInterval = null
  }
}

// Enhanced Back Navigation Function
const goBack = () => {
  try {
    // Check if there's history to go back to
    if (window.history.length > 1) {
      // Use Vue Router's go method to go back in history
      if (window.history.state && window.history.state.back) {
        window.history.back()
      } else {
        // Fallback: Use Vue Router's go method
        const router = getCurrentInstance()?.appContext.app.config.globalProperties.$router
        if (router) {
          router.go(-1)
        } else {
          // Final fallback: Use browser's native back
          window.history.back()
        }
      }
    } else {
      // If no history, fallback to dashboard
      const router = getCurrentInstance()?.appContext.app.config.globalProperties.$router
      if (router) {
        router.push('/dashboard')
      } else {
        // If router is not available, try to navigate using window.location
        window.location.href = '/dashboard'
      }
    }
  } catch (error) {
    console.error('Error navigating back:', error)
    // Fallback to dashboard on any error
    try {
      const router = getCurrentInstance()?.appContext.app.config.globalProperties.$router
      if (router) {
        router.push('/dashboard')
      } else {
        window.location.href = '/dashboard'
      }
    } catch (fallbackError) {
      console.error('Fallback navigation also failed:', fallbackError)
    }
  }
}

// Fetch notifications from Firebase
const unsubscribeNotifications = ref(null)

const fetchNotifications = () => {
  try {
    isLoading.value = true;
    
    const q = query(
      collection(db, 'notifications'),
      orderBy('timestamp', 'desc')
    );
    
    // Unsubscribe from any existing listener
    if (unsubscribeNotifications.value) {
      unsubscribeNotifications.value();
    }
    
    unsubscribeNotifications.value = onSnapshot(q, (snapshot) => {
      // Process all documents in the snapshot (not just changes)
      const allNotifications = snapshot.docs.map(doc => {
        const data = doc.data();
        return {
          ...data,
          id: doc.id,
          time: data.timestamp?.toDate?.() ?? new Date()
        };
      });

      // Filter duplicates (shouldn't be needed with Firestore IDs but just in case)
      const uniqueNotifications = allNotifications.filter(
        (notification, index, self) =>
          index === self.findIndex(n => n.id === notification.id)
      );

      // Split into active and archived
      notifications.value = uniqueNotifications.filter(n => !n.archived);
      archivedNotifications.value = uniqueNotifications.filter(n => n.archived);
      
      // Only show new notification toast for actual additions
      const changes = snapshot.docChanges();
      if (changes.some(change => change.type === 'added' && change.doc.metadata.hasPendingWrites === false)) {
        const newCount = changes.filter(
          change => change.type === 'added' && change.doc.metadata.hasPendingWrites === false
        ).length;
        
        if (newCount > 0 && !showArchived.value) {
          showToastMessage(`${newCount} new notification${newCount > 1 ? 's' : ''}`, 'info');
        }
      }
    }, (error) => {
      console.error('Error receiving notifications:', error);
      showToastMessage('Error loading notifications', 'error');
    });
    
  } catch (error) {
    console.error('Failed to setup notifications listener:', error);
    showToastMessage('Failed to setup notifications', 'error');
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  loadUserPreferences() // Load user preferences on mount
  fetchNotifications()
  eventBus.on('notification-saved-success', fetchNotifications)
  fetchWeatherForModal()
})

onUnmounted(() => {
  stopLoadingAnimation()
  if (unsubscribeNotifications.value) {
    unsubscribeNotifications.value()
  }
})

// Computed: Filtered notifications
const filteredNotifications = computed(() => {
  let result = [...currentNotifications.value]

  if (activeFilter.value === 'unread' && !showArchived.value) {
    result = result.filter(n => !n.read)
  } else if (activeFilter.value === 'system') {
    result = result.filter(n => n.type === 'system')
  } else if (activeFilter.value === 'alert') {
    result = result.filter(n => ['warning', 'critical'].includes(n.severity))
  } else if (activeFilter.value === 'data') {
    result = result.filter(n => n.type === 'data')
  }

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(n =>
      n.title?.toLowerCase().includes(query) ||
      n.message?.toLowerCase().includes(query)
    )
  }

  return result
})

// Smart Pagination logic
const totalPages = computed(() =>
  Math.ceil(filteredNotifications.value.length / itemsPerPage.value) || 1
)

const paginatedNotifications = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredNotifications.value.slice(start, start + itemsPerPage.value)
})

// Smart pagination display logic
const displayedPages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const pages = []

  if (total <= 7) {
    // If 7 or fewer pages, show all
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // Always show first page
    pages.push(1)

    if (current <= 3) {
      // If near start, show 2-5 then ellipsis
      pages.push(2, 3, 4, 5, '...', total)
    } else if (current >= total - 2) {
      // If near end, show ellipsis then last 4
      pages.push('...', total - 4, total - 3, total - 2, total - 1, total)
    } else {
      // Otherwise show ellipsis, current -1, current, current + 1, ellipsis
      pages.push('...', current - 1, current, current + 1, '...', total)
    }
  }

  return pages
})

// Pagination methods
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const goToPage = (page) => {
  if (typeof page === 'number') {
    currentPage.value = page
  }
}

watch([activeFilter, searchQuery], () => {
  currentPage.value = 1
})

// Enhanced date comparison helpers
const isSameDay = (dateA, dateB) => {
  return (
    dateA?.getFullYear() === dateB.getFullYear() &&
    dateA?.getMonth() === dateB.getMonth() &&
    dateA?.getDate() === dateB.getDate()
  )
}

const isToday = (date) => {
  if (!date) return false
  const today = new Date()
  return isSameDay(date, today)
}

const isYesterday = (date) => {
  if (!date) return false
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  return isSameDay(date, yesterday)
}

const getDaysAgo = (date) => {
  if (!date) return 0
  const now = new Date()
  const diffTime = Math.abs(now - new Date(date))
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

// Enhanced notification grouping by time periods
const todayNotifications = computed(() =>
  paginatedNotifications.value.filter(n => isToday(n.time))
)

const yesterdayNotifications = computed(() =>
  paginatedNotifications.value.filter(n => isYesterday(n.time))
)

// A few days ago (2-6 days)
const fewDaysAgoNotifications = computed(() =>
  paginatedNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 2 && daysAgo <= 6
  })
)

// A week ago (7-13 days)
const weekAgoNotifications = computed(() =>
  paginatedNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 7 && daysAgo <= 13
  })
)

// A few weeks ago (14-29 days)
const fewWeeksAgoNotifications = computed(() =>
  paginatedNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 14 && daysAgo <= 29
  })
)

// A month ago (30+ days)
const monthAgoNotifications = computed(() =>
  paginatedNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 30
  })
)

const markAsRead = async (docId) => {
  try {
    const notifIndex = notifications.value.findIndex(n => n.id === docId);
    if (notifIndex !== -1) {
      notifications.value[notifIndex].read = true;

      // Firestore update
      const notifRef = doc(db, NOTIF_COLLECTION, docId);
      await updateDoc(notifRef, { read: true });
    }
  } catch (err) {
    console.error("❌ Failed to mark as read:", err);
  }
};

const markAllAsRead = async () => {
  try {
    const updates = notifications.value.map(async (n) => {
      if (!n.read) {
        n.read = true;
        const notifRef = doc(db, NOTIF_COLLECTION, n.id);
        return updateDoc(notifRef, { read: true });
      }
    });
    await Promise.all(updates);
  } catch (err) {
    console.error("❌ Failed to mark all as read:", err);
  }
};

// Format notification time
const formatTime = (time) => {
  if (!time) return 'Unknown time'
  const now = new Date()
  const diff = now - new Date(time)
  const mins = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (mins < 60) return `${mins} min${mins !== 1 ? 's' : ''} ago`
  if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`
  if (days < 7) return `${days} day${days !== 1 ? 's' : ''} ago`
  return new Date(time).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

// Enhanced notification icon system based on content and category
const getNotificationIcon = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
  // Weather-related notifications
  if (title.includes('weather') || title.includes('rain') || title.includes('storm') || 
      message.includes('weather') || message.includes('rain') || message.includes('storm') ||
      category.includes('weather') || type.includes('weather')) {
    if (title.includes('severe') || message.includes('severe') || title.includes('storm') || message.includes('storm')) {
      return { bgColor: 'bg-red-500', badgeColor: 'bg-red-100 text-red-800', icon: Zap }
    }
    if (title.includes('rain') || message.includes('rain')) {
      return { bgColor: 'bg-blue-500', badgeColor: 'bg-blue-100 text-blue-800', icon: CloudRain }
    }
    if (title.includes('wind') || message.includes('wind')) {
      return { bgColor: 'bg-gray-500', badgeColor: 'bg-gray-100 text-gray-800', icon: Wind }
    }
    if (title.includes('temperature') || message.includes('temperature') || title.includes('heat') || message.includes('heat')) {
      return { bgColor: 'bg-orange-500', badgeColor: 'bg-orange-100 text-orange-800', icon: Thermometer }
    }
    return { bgColor: 'bg-sky-500', badgeColor: 'bg-sky-100 text-sky-800', icon: Cloud }
  }
  
  // Water and soil related notifications
  if (title.includes('water') || title.includes('moisture') || title.includes('irrigation') ||
      message.includes('water') || message.includes('moisture') || message.includes('irrigation') ||
      category.includes('water') || category.includes('soil') || type.includes('water')) {
    if (title.includes('level') || message.includes('level')) {
      return { bgColor: 'bg-cyan-500', badgeColor: 'bg-cyan-100 text-cyan-800', icon: Gauge }
    }
    if (title.includes('soil') || message.includes('soil')) {
      return { bgColor: 'bg-amber-600', badgeColor: 'bg-amber-100 text-amber-800', icon: Sprout }
    }
    return { bgColor: 'bg-cyan-500', badgeColor: 'bg-cyan-100 text-cyan-800', icon: Droplet }
  }
  
  // Crop and plant related notifications
  if (title.includes('crop') || title.includes('plant') || title.includes('harvest') || title.includes('growth') ||
      message.includes('crop') || message.includes('plant') || message.includes('harvest') || message.includes('growth') ||
      category.includes('crop') || category.includes('plant') || type.includes('crop')) {
    if (title.includes('prediction') || message.includes('prediction') || title.includes('forecast') || message.includes('forecast')) {
      return { bgColor: 'bg-green-600', badgeColor: 'bg-green-100 text-green-800', icon: TrendingUp }
    }
    if (title.includes('wheat') || message.includes('wheat') || title.includes('grain') || message.includes('grain')) {
      return { bgColor: 'bg-yellow-600', badgeColor: 'bg-yellow-100 text-yellow-800', icon: Wheat }
    }
    return { bgColor: 'bg-green-500', badgeColor: 'bg-green-100 text-green-800', icon: Leaf }
  }
  
  // System and device related notifications
  if (title.includes('system') || title.includes('device') || title.includes('sensor') || title.includes('connection') ||
      message.includes('system') || message.includes('device') || message.includes('sensor') || message.includes('connection') ||
      category.includes('system') || type.includes('system')) {
    if (title.includes('offline') || message.includes('offline') || title.includes('disconnected') || message.includes('disconnected')) {
      return { bgColor: 'bg-red-500', badgeColor: 'bg-red-100 text-red-800', icon: WifiOff }
    }
    if (title.includes('battery') || message.includes('battery') || title.includes('power') || message.includes('power')) {
      if (title.includes('low') || message.includes('low')) {
        return { bgColor: 'bg-orange-500', badgeColor: 'bg-orange-100 text-orange-800', icon: BatteryLow }
      }
      return { bgColor: 'bg-green-500', badgeColor: 'bg-green-100 text-green-800', icon: Battery }
    }
    if (title.includes('data') || message.includes('data') || title.includes('reading') || message.includes('reading')) {
      return { bgColor: 'bg-indigo-500', badgeColor: 'bg-indigo-100 text-indigo-800', icon: Database }
    }
    if (title.includes('connection') || message.includes('connection') || title.includes('network') || message.includes('network')) {
      return { bgColor: 'bg-blue-500', badgeColor: 'bg-blue-100 text-blue-800', icon: Wifi }
    }
    return { bgColor: 'bg-purple-500', badgeColor: 'bg-purple-100 text-purple-800', icon: Settings2 }
  }
  
  // Alert and warning notifications
  if (notification.severity === 'critical' || title.includes('critical') || message.includes('critical') ||
      title.includes('urgent') || message.includes('urgent')) {
    return { bgColor: 'bg-red-600', badgeColor: 'bg-red-100 text-red-800', icon: AlertCircle }
  }
  
  if (notification.severity === 'warning' || title.includes('warning') || message.includes('warning') ||
      title.includes('alert') || message.includes('alert') || type.includes('alert')) {
    return { bgColor: 'bg-orange-500', badgeColor: 'bg-orange-100 text-orange-800', icon: AlertTriangle }
  }
  
  // Data and analytics notifications
  if (title.includes('analysis') || title.includes('report') || title.includes('trend') ||
      message.includes('analysis') || message.includes('report') || message.includes('trend') ||
      category.includes('data') || type.includes('data')) {
    if (title.includes('increase') || message.includes('increase') || title.includes('up') || message.includes('up')) {
      return { bgColor: 'bg-green-500', badgeColor: 'bg-green-100 text-green-800', icon: TrendingUp }
    }
    if (title.includes('decrease') || message.includes('decrease') || title.includes('down') || message.includes('down')) {
      return { bgColor: 'bg-red-500', badgeColor: 'bg-red-100 text-red-800', icon: TrendingDown }
    }
    return { bgColor: 'bg-indigo-500', badgeColor: 'bg-indigo-100 text-indigo-800', icon: BarChart }
  }
  
  // Location and GPS related
  if (title.includes('location') || title.includes('gps') || title.includes('position') ||
      message.includes('location') || message.includes('gps') || message.includes('position')) {
    return { bgColor: 'bg-blue-500', badgeColor: 'bg-blue-100 text-blue-800', icon: MapPin }
  }
  
  // Success notifications
  if (title.includes('success') || title.includes('completed') || title.includes('finished') ||
      message.includes('success') || message.includes('completed') || message.includes('finished') ||
      type.includes('success')) {
    return { bgColor: 'bg-green-500', badgeColor: 'bg-green-100 text-green-800', icon: Check }
  }
  
  // Info notifications
  if (type.includes('info') || category.includes('info')) {
    return { bgColor: 'bg-blue-500', badgeColor: 'bg-blue-100 text-blue-800', icon: Info }
  }
  
  // Default fallback
  return { bgColor: 'bg-gray-500', badgeColor: 'bg-gray-100 text-gray-800', icon: Bell }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Enhanced scrollbar styling */
.notification-scroll::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

.notification-scroll::-webkit-scrollbar-track {
  background: rgba(20, 83, 45, 0.05);
  border-radius: 4px;
}

.notification-scroll::-webkit-scrollbar-thumb {
  background: rgba(20, 83, 45, 0.2);
  border-radius: 4px;
  transition: background-color 200ms;
}

.notification-scroll::-webkit-scrollbar-thumb:hover {
  background: rgba(20, 83, 45, 0.4);
}

/* Firefox scrollbar styling */
.notification-scroll {
  scrollbar-width: thin;
  scrollbar-color: rgba(20, 83, 45, 0.2) rgba(20, 83, 45, 0.05);
}

/* Line clamp utilities */
.line-clamp-1 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

/* Focus styles */
:focus-visible {
  outline: 2px solid #10b981;
  outline-offset: 2px;
}

/* Enhanced responsive design for filter buttons */
@media (max-width: 1024px) {
  .flex.flex-col.lg\\:flex-row.lg\\:items-center.lg\\:justify-between {
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .p-5 {
    padding: 1rem;
  }
  
  .px-5 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .py-4 {
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
  }
  
  .gap-3 {
    gap: 0.5rem;
  }
  
  /* Ensure filter buttons wrap nicely on mobile */
  .flex.items-center.justify-start.gap-2.flex-wrap {
    justify-content: flex-start;
  }
}

@media (max-width: 640px) {
  .text-xl {
    font-size: 1.125rem;
  }
  
  .px-3 {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  
  .py-1\.5 {
    padding-top: 0.25rem;
    padding-bottom: 0.25rem;
  }
  
  .w-8, .h-8 {
    width: 1.75rem;
    height: 1.75rem;
  }
  
  /* Stack filter buttons vertically on very small screens if needed */
  .flex.items-center.justify-start.gap-2.flex-wrap {
    gap: 0.5rem;
  }
}

/* Animation for unread indicator */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.bg-blue-500 {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Print styles */
@media print {
  .shadow-sm,
  .shadow-md,
  .hover\:shadow-lg {
    box-shadow: none !important;
  }
  
  .bg-gradient-to-r,
  .bg-gradient-to-br {
    background: white !important;
  }
  
  .border {
    border-color: #e5e7eb !important;
  }
}

/* Additional responsive improvements */
@media (min-width: 1280px) {
  .relative.w-full.sm\\:w-80.md\\:w-72.lg\\:w-64.xl\\:w-80.max-w-sm {
    width: 20rem; /* 320px */
  }
}

@media (max-width: 480px) {
  /* Very small screens - ensure buttons don't get too cramped */
  .flex.items-center.justify-start.gap-2.flex-wrap button {
    min-width: fit-content;
    flex-shrink: 0;
  }
}
</style>