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

  <!-- Enhanced Notification Details Modal - REDUCED WIDTH -->
  <div v-if="showDetailsModal && selectedNotification" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-3xl w-full max-h-[90vh] overflow-hidden border border-gray-200">
      <!-- Modal Header -->
      <div class="px-6 py-4 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div 
              class="w-10 h-10 rounded-xl flex items-center justify-center shadow-sm flex-shrink-0"
              :class="getNotificationIcon(selectedNotification).bgColor"
            >
              <component 
                :is="getNotificationIcon(selectedNotification).icon" 
                class="h-5 w-5 text-white" 
              />
            </div>
            <div class="min-w-0">
              <h2 class="text-sm md:text-lg font-semibold text-gray-800">Notification Details</h2>
              <p class="text-xs md:text-sm text-gray-500">{{ formatTime(selectedNotification.time) }}</p>
            </div>
          </div>
          <button 
            @click="closeDetails"
            class="p-2 text-gray-400 rounded-lg transition-colors flex-shrink-0"
          >
            <X class="h-5 w-5" />
          </button>
        </div>
      </div>

      <!-- Modal Content - FIXED LAYOUT -->
      <div class="p-6 overflow-y-auto max-h-[calc(90vh-160px)] static">
        <div class="space-y-6 static">
          <!-- Title and Status -->
          <div class="space-y-3">
            <div class="flex items-start justify-between">
              <h3 class="text-md md:text-xl font-semibold text-gray-900 min-w-0 flex-1 pr-4">{{ selectedNotification.title }}</h3>
              <div class="flex items-center space-x-2 flex-shrink-0">
                <span 
                  class="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium whitespace-nowrap"
                  :class="getNotificationIcon(selectedNotification).badgeColor"
                >
                  {{ selectedNotification.category || selectedNotification.type }}
                </span>
                <div v-if="!selectedNotification.read && !selectedNotification.archived" class="flex items-center text-blue-600 text-xs font-medium whitespace-nowrap">
                  <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1 flex-shrink-0"></div>
                  Unread
                </div>
                <div v-if="selectedNotification.archived" class="flex items-center text-orange-600 text-xs font-medium whitespace-nowrap">
                  <Archive class="h-3 w-3 mr-1 flex-shrink-0" />
                  Archived
                </div>
              </div>
            </div>
          </div>

          <!-- Message -->
          <div class="space-y-2">
            <h4 class="text-xs md:text-sm font-medium text-gray-700">Message</h4>
            <p class="text-md text-gray-700 leading-relaxed font-medium">
              {{ selectedNotification.message }}
            </p>
          </div>

          <!-- Enhanced Detailed Analysis Container - COMPLETELY STABLE POSITIONING -->
          <div class="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-2xl border-2 border-indigo-100 shadow-lg relative">
            <div class="p-5 static">
              <div class="mb-4 static">
                <h4 class="text-sm md:text-lg font-bold text-gray-800 flex items-center static">
                  <div class="w-7 h-7 bg-indigo-500 rounded-full flex items-center justify-center mr-3 flex-shrink-0 static">
                    <Info class="h-4 w-4 text-white" />
                  </div>
                  <span class="min-w-0 static">Detailed Analysis & Context</span>
                </h4>
              </div>
              
              <!-- Weather Notifications -->
              <div v-if="isWeatherNotification(selectedNotification)" class="space-y-5 static">
                <div class="text-xs md:text-sm text-gray-600 bg-white/70 rounded-lg p-3 border border-indigo-200 static">
                  Weather forecast analysis for {{ selectedNotification.context?.forecast?.date || 'today' }}.
                </div>
                
                <!-- Current Weather Summary -->
                <div class="bg-blue-100 rounded-xl border-2 border-blue-300 shadow-sm static">
                  <div class="p-4 static">
                    <div class="flex items-center justify-between mb-3 static">
                      <div class="flex items-center space-x-2 min-w-0 flex-1 static">
                        <CloudRain class="h-5 w-5 text-blue-600 flex-shrink-0 static" />
                        <span class="text-base font-semibold text-blue-700 min-w-0 static">Current Weather Conditions</span>
                      </div>
                      <span class="text-sm md:text-lg font-bold text-blue-800 flex-shrink-0 ml-2 static">
                        {{ selectedNotification.context?.currentWeather?.condition || selectedNotification.context?.forecast?.condition || 'N/A' }}
                        <span v-if="selectedNotification.context?.currentWeather?.temperature">({{ selectedNotification.context.currentWeather.temperature }}°C)</span>
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Weather Parameters Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 static">
                  <!-- Humidity -->
                  <div class="bg-blue-50 rounded-xl border-2 border-blue-200 shadow-sm static">
                    <div class="p-3 md:p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Droplet class="h-4 w-4 text-blue-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-blue-700 static">Humidity</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-blue-800 mb-1 static">{{ selectedNotification.context?.currentWeather?.humidity || '--' }}%</p>
                      <p class="text-xs text-blue-600 leading-tight static">
                        {{ selectedNotification.context?.currentWeather?.humidity ? getHumidityDescription(selectedNotification.context.currentWeather.humidity) : 'No data' }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Pressure -->
                  <div class="bg-gray-50 rounded-xl border-2 border-gray-200 shadow-sm static">
                    <div class="p-3 md:p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Gauge class="h-4 w-4 text-gray-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-gray-700 static">Pressure</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-gray-800 mb-1 static">{{ selectedNotification.context?.currentWeather?.pressure || '--' }} hPa</p>
                      <p class="text-xs text-gray-600 leading-tight static">
                        {{ selectedNotification.context?.currentWeather?.pressure ? getPressureDescription(selectedNotification.context.currentWeather.pressure) : 'No data' }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Wind Speed -->
                  <div class="bg-green-50 rounded-xl border-2 border-green-200 shadow-sm static">
                    <div class="p-3 md:p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Wind class="h-4 w-4 text-green-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-green-700 static">Wind Speed</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-green-800 mb-1 static">{{ selectedNotification.context?.currentWeather?.windSpeed || '--' }} km/h</p>
                      <p class="text-xs text-green-600 leading-tight static">
                        {{ selectedNotification.context?.currentWeather?.windSpeed ? getWindDescription(selectedNotification.context.currentWeather.windSpeed) : 'No data' }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- UV Index -->
                  <div class="bg-yellow-50 rounded-xl border-2 border-yellow-200 shadow-sm static">
                    <div class="p-3 md:p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Sun class="h-4 w-4 text-yellow-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-yellow-700 static">UV Index</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-yellow-800 mb-1 static">{{ selectedNotification.context?.currentWeather?.uvIndex ? selectedNotification.context.currentWeather.uvIndex.toFixed(1) : '--' }}</p>
                      <p class="text-xs text-yellow-600 leading-tight static">
                        {{ selectedNotification.context?.currentWeather?.uvIndex ? getUVDescription(selectedNotification.context.currentWeather.uvIndex) : 'No data' }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <!-- Forecast -->
                <div v-if="selectedNotification.context?.forecast" class="bg-purple-100 rounded-xl border-2 border-purple-300 shadow-sm static">
                  <div class="p-4 static">
                    <div class="flex items-center justify-between mb-3 static">
                      <div class="flex items-center space-x-2 min-w-0 flex-1 static">
                        <CalendarClock class="h-5 w-5 text-purple-600 flex-shrink-0 static" />
                        <span class="text-base font-semibold text-purple-700 static">Weather Forecast</span>
                      </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4 mt-3 static">
                      <div class="bg-white/60 rounded-lg p-3 static">
                        <p class="text-xs md:text-sm text-purple-600 font-medium static">Max Temperature</p>
                        <p class="text-sm md:text-lg font-bold text-purple-800 static">{{ selectedNotification.context.forecast.temperatures.max }}°C</p>
                      </div>
                      <div class="bg-white/60 rounded-lg p-3 static">
                        <p class="text-xs md:text-sm text-purple-600 font-medium static">Min Temperature</p>
                        <p class="text-sm md:text-lg font-bold text-purple-800 static">{{ selectedNotification.context.forecast.temperatures.min }}°C</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Sensor and Agricultural Data Notifications - COMPLETELY STABLE -->
              <div v-else-if="selectedNotification.context?.type === 'water-level'" class="space-y-5 static">
                <div class="text-xs md:text-sm text-gray-600 bg-white/70 rounded-lg p-3 border border-indigo-200 static">
                  Water level status update for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                </div>
                
                <div class="bg-cyan-100 rounded-xl border-2 border-cyan-300 shadow-sm static">
                  <div class="p-4 static">
                    <div class="flex items-center space-x-2 mb-3 static">
                      <Gauge class="h-5 w-5 text-cyan-600 flex-shrink-0 static" />
                      <span class="text-base font-semibold text-cyan-700 static">Water Level Status</span>
                    </div>
                    <div class="text-center mb-3 static">
                      <span class="text-4xl md:text-5xl font-bold text-cyan-800 static">
                        {{ selectedNotification.context.level }}%
                      </span>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                      <div>
                        <p class="text-xs text-cyan-700 font-medium">Status</p>
                        <p class="text-sm font-semibold" :class="{
                          'text-red-600': selectedNotification.context.status === 'Critical',
                          'text-orange-600': selectedNotification.context.status === 'Warning',
                          'text-green-600': selectedNotification.context.status === 'Normal'
                        }">
                          {{ selectedNotification.context.status }}
                        </p>
                      </div>
                      <div>
                        <p class="text-xs text-cyan-700 font-medium">Priority</p>
                        <p class="text-sm font-semibold">
                          {{ selectedNotification.context.priority }}
                        </p>
                      </div>
                    </div>
                    <div class="mt-4">
                      <p class="text-xs md:text-sm text-cyan-700 leading-relaxed static">
                        {{ selectedNotification.context.recommendation }}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Climate Alert (Type 2) -->
              <div v-else-if="selectedNotification.context?.type === 'climate'" class="space-y-5 static">
                <div class="text-xs md:text-sm text-gray-600 bg-white/70 rounded-lg p-3 border border-indigo-200 static">
                  Environmental conditions for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                </div>
                
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 static">
                  <!-- Temperature -->
                  <div class="bg-red-50 rounded-xl border-2 border-red-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Thermometer class="h-4 w-4 text-red-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-red-700 static">Temperature</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-red-800 mb-1 static">
                        {{ selectedNotification.context.temperature }}
                      </p>
                      <p class="text-xs text-red-600 leading-tight static">
                        {{ getTemperatureDescription(parseFloat(selectedNotification.context.temperature.replace('°C',''))) }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Humidity -->
                  <div class="bg-blue-50 rounded-xl border-2 border-blue-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Droplet class="h-4 w-4 text-blue-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-blue-700 static">Humidity</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-blue-800 mb-1 static">
                        {{ selectedNotification.context.humidity }}
                      </p>
                      <p class="text-xs text-blue-600 leading-tight static">
                        {{ getHumidityDescription(parseFloat(selectedNotification.context.humidity.replace('%',''))) }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Soil Moisture -->
                  <div v-if="selectedNotification.context.soilMoisture" class="bg-amber-50 rounded-xl border-2 border-amber-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Droplet class="h-4 w-4 text-amber-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-amber-700 static">Soil Moisture</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-amber-800 mb-1 static">
                        {{ selectedNotification.context.soilMoisture }}
                      </p>
                      <p class="text-xs text-amber-600 leading-tight static">
                        {{ getMoistureDescription(parseFloat(selectedNotification.context.soilMoisture.replace('%',''))) }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div class="bg-emerald-100 rounded-xl border-2 border-emerald-300 shadow-sm static">
                  <div class="p-4 static">
                    <p class="text-xs md:text-sm text-emerald-800 font-medium leading-relaxed static">
                      {{ selectedNotification.context.recommendation }}
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- Soil Moisture Alert (Type 3 & 5) -->
              <div v-else-if="selectedNotification.context?.type === 'soil-moisture'" class="space-y-5 static">
                <div class="text-xs md:text-sm text-gray-600 bg-white/70 rounded-lg p-3 border border-indigo-200 static">
                  Soil conditions for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                </div>
                
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 static">
                  <!-- Soil Moisture -->
                  <div class="bg-amber-50 rounded-xl border-2 border-amber-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Droplet class="h-4 w-4 text-amber-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-amber-700 static">Soil Moisture</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-amber-800 mb-1 static">
                        {{ selectedNotification.context.moisture }}
                      </p>
                      <p class="text-xs text-amber-600 leading-tight static">
                        {{ getMoistureDescription(parseFloat(selectedNotification.context.moisture.replace('%',''))) }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Temperature -->
                  <div v-if="selectedNotification.context.temperature" class="bg-red-50 rounded-xl border-2 border-red-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Thermometer class="h-4 w-4 text-red-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-red-700 static">Temperature</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-red-800 mb-1 static">
                        {{ selectedNotification.context.temperature }}
                      </p>
                      <p class="text-xs text-red-600 leading-tight static">
                        {{ getTemperatureDescription(parseFloat(selectedNotification.context.temperature.replace('°C',''))) }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Water Level -->
                  <div v-if="selectedNotification.context.waterLevel" class="bg-cyan-50 rounded-xl border-2 border-cyan-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Gauge class="h-4 w-4 text-cyan-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-cyan-700 static">Water Level</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-cyan-800 mb-1 static">
                        {{ selectedNotification.context.waterLevel }}
                      </p>
                      <p class="text-xs text-cyan-600 leading-tight static">
                        {{ getWaterLevelDescription(parseFloat(selectedNotification.context.waterLevel.replace('%',''))) }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div class="bg-emerald-100 rounded-xl border-2 border-emerald-300 shadow-sm static">
                  <div class="p-4 static">
                    <p class="text-xs md:text-sm text-emerald-800 font-medium leading-relaxed static">
                      {{ selectedNotification.context.recommendation }}
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- NPK/Soil pH Alert (Type 4) -->
              <div v-else-if="selectedNotification.context?.type === 'nutrients'" class="space-y-5 static">
                <div class="text-xs md:text-sm text-gray-600 bg-white/70 rounded-lg p-3 border border-indigo-200 static">
                  Soil nutrient analysis for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                </div>
                
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 static">
                  <!-- Nitrogen -->
                  <div v-if="selectedNotification.context.nitrogen" class="bg-green-50 rounded-xl border-2 border-green-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Leaf class="h-4 w-4 text-green-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-green-700 static">Nitrogen (N)</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-green-800 mb-1 static">
                        {{ selectedNotification.context.nitrogen.value }} ppm
                      </p>
                      <p class="text-xs text-green-600 leading-tight static">
                        Level: {{ selectedNotification.context.nitrogen.level }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Phosphorus -->
                  <div v-if="selectedNotification.context.phosphorus" class="bg-orange-50 rounded-xl border-2 border-orange-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Sprout class="h-4 w-4 text-orange-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-orange-700 static">Phosphorus (P)</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-orange-800 mb-1 static">
                        {{ selectedNotification.context.phosphorus.value }} ppm
                      </p>
                      <p class="text-xs text-orange-600 leading-tight static">
                        Level: {{ selectedNotification.context.phosphorus.level }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Potassium -->
                  <div v-if="selectedNotification.context.potassium" class="bg-yellow-50 rounded-xl border-2 border-yellow-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Activity class="h-4 w-4 text-yellow-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-yellow-700 static">Potassium (K)</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-yellow-800 mb-1 static">
                        {{ selectedNotification.context.potassium.value }} ppm
                      </p>
                      <p class="text-xs text-yellow-600 leading-tight static">
                        Level: {{ selectedNotification.context.potassium.level }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Soil pH -->
                  <div v-if="selectedNotification.context.soilPh" class="bg-purple-50 rounded-xl border-2 border-purple-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Gauge class="h-4 w-4 text-purple-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-purple-700 static">Soil pH</span>
                      </div>
                      <p class="text-sm md:text-xl font-bold text-purple-800 mb-1 static">
                        {{ selectedNotification.context.soilPh.value }}
                      </p>
                      <p class="text-xs text-purple-600 leading-tight static">
                        Condition: {{ selectedNotification.context.soilPh.condition }}
                      </p>
                    </div>
                  </div>
                </div>
                
                <div class="bg-emerald-100 rounded-xl border-2 border-emerald-300 shadow-sm static">
                  <div class="p-4 static">
                    <p class="text-xs md:text-sm text-emerald-800 font-medium leading-relaxed static">
                      {{ selectedNotification.context.recommendation }}
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- Water Scheduling Alert (Type 6) -->
              <div v-else-if="selectedNotification.context?.scheduleId" class="space-y-5 static">
                <div class="text-xs md:text-sm text-gray-600 bg-white/70 rounded-lg p-3 border border-indigo-200 static">
                  {{ selectedNotification.message }}
                </div>
                
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 static">
                  <!-- Schedule Type -->
                  <div class="bg-blue-50 rounded-xl border-2 border-blue-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <CalendarClock class="h-4 w-4 text-blue-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-blue-700 static">Schedule Type</span>
                      </div>
                      <p class="text-sm md:text-lg font-bold text-blue-800 mb-1 static capitalize">
                        {{ selectedNotification.context.scheduleType }}
                        <span v-if="selectedNotification.context.scheduleType === 'weekly'">
                          ({{ getDayName(selectedNotification.context.day) }})
                        </span>
                      </p>
                    </div>
                  </div>
                  
                  <!-- Duration -->
                  <div class="bg-green-50 rounded-xl border-2 border-green-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Clock class="h-4 w-4 text-green-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-green-700 static">Duration</span>
                      </div>
                      <p class="text-sm md:text-lg font-bold text-green-800 mb-1 static">
                        {{ selectedNotification.context.duration }} minute{{ selectedNotification.context.duration !== 1 ? 's' : '' }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Start/End Time -->
                  <div class="bg-purple-50 rounded-xl border-2 border-purple-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <component :is="selectedNotification.title.includes('Started') ? Play : StopCircle" 
                                  class="h-4 w-4 text-purple-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-purple-700 static">
                          {{ selectedNotification.title.includes('Started') ? 'Start Time' : 'End Time' }}
                        </span>
                      </div>
                      <p class="text-sm md:text-lg font-bold text-purple-800 mb-1 static">
                        {{ formatTime(selectedNotification.time) }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Environmental Conditions -->
                  <div class="bg-cyan-50 rounded-xl border-2 border-cyan-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Thermometer class="h-4 w-4 text-cyan-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-cyan-700 static">Temperature</span>
                      </div>
                      <p class="text-sm md:text-lg font-bold text-cyan-800 mb-1 static">
                        {{ selectedNotification.context.temperature }}°C
                      </p>
                    </div>
                  </div>
                  
                  <div class="bg-blue-50 rounded-xl border-2 border-blue-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Droplet class="h-4 w-4 text-blue-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-blue-700 static">Humidity</span>
                      </div>
                      <p class="text-sm md:text-lg font-bold text-blue-800 mb-1 static">
                        {{ selectedNotification.context.humidity }}%
                      </p>
                    </div>
                  </div>
                  
                  <div class="bg-amber-50 rounded-xl border-2 border-amber-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Droplet class="h-4 w-4 text-amber-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-amber-700 static">Soil Moisture</span>
                      </div>
                      <p class="text-sm md:text-lg font-bold text-amber-800 mb-1 static">
                        {{ selectedNotification.context.soilMoisture }}%
                      </p>
                    </div>
                  </div>
                  
                  <div class="bg-indigo-50 rounded-xl border-2 border-indigo-200 shadow-sm static">
                    <div class="p-4 static">
                      <div class="flex items-center space-x-2 mb-2 static">
                        <Gauge class="h-4 w-4 text-indigo-600 flex-shrink-0 static" />
                        <span class="text-xs md:text-sm font-medium text-indigo-700 static">Water Level</span>
                      </div>
                      <p class="text-sm md:text-lg font-bold text-indigo-800 mb-1 static">
                        {{ selectedNotification.context.waterLevel }}%
                      </p>
                    </div>
                  </div>
                </div>
                
                <!-- Status Summary -->
                <div class="bg-emerald-100 rounded-xl border-2 border-emerald-300 shadow-sm static">
                  <div class="p-4 static">
                    <div class="flex items-center space-x-2 mb-2 static">
                      <Info class="h-4 w-4 text-emerald-600 flex-shrink-0 static" />
                      <span class="text-xs md:text-sm font-semibold text-emerald-700 static">Status Summary</span>
                    </div>
                    <p class="text-xs md:text-sm text-emerald-800 font-medium leading-relaxed static">
                      {{ selectedNotification.title.includes('Started') ? 
                        'Watering schedule started successfully' : 
                        'Watering schedule completed successfully' }}
                    </p>
                    <p v-if="selectedNotification.context.soilMoisture < 25" class="text-xs text-orange-600 mt-2 static">
                      Note: Soil moisture was low ({{ selectedNotification.context.soilMoisture }}%) during this watering
                    </p>
                    <p v-if="selectedNotification.context.waterLevel < 30" class="text-xs text-orange-600 mt-1 static">
                      Note: Water level was low ({{ selectedNotification.context.waterLevel }}%) during this watering
                    </p>
                  </div>
                </div>
              </div>
              
              <!-- General Notifications -->
              <div v-else class="space-y-4 static">
                <div class="text-xs md:text-sm text-gray-600 bg-white/70 rounded-lg p-3 border border-indigo-200 static">
                  {{ selectedNotification.context?.additionalInfo || getDynamicAdditionalInfo(selectedNotification) }}
                </div>
                <div class="bg-blue-50 rounded-xl border-2 border-blue-200 shadow-sm static">
                  <div class="p-4 static">
                    <div class="flex items-center space-x-2 mb-2 static">
                      <Info class="h-4 w-4 text-blue-600 flex-shrink-0 static" />
                      <span class="text-xs md:text-sm font-semibold text-blue-700 static">Status Information</span>
                    </div>
                    <p class="text-xs md:text-sm text-blue-800 font-medium leading-relaxed static">
                      {{ selectedNotification.context?.status || 'All systems operating within normal parameters' }}
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Enhanced Metadata - COMPLETELY STABLE -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Received Container -->
            <div class="bg-gradient-to-br from-emerald-50 to-teal-50 rounded-2xl border-2 border-emerald-200 shadow-lg">
              <div class="p-4">
                <div class="flex items-center space-x-2 mb-2">
                  <div class="w-6 h-6 bg-emerald-500 rounded-full flex items-center justify-center flex-shrink-0">
                    <CalendarClock class="h-3 w-3 text-white" />
                  </div>
                  <h4 class="text-xs md:text-sm font-bold text-emerald-700">Received</h4>
                </div>
                <p class="text-xs md:text-sm text-emerald-800 font-semibold leading-relaxed">{{ formatFullDate(selectedNotification.time) }}</p>
              </div>
            </div>
            
            <!-- Priority Container -->
            <div class="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl border-2 border-orange-200 shadow-lg">
              <div class="p-4">
                <div class="flex items-center space-x-2 mb-2">
                  <div class="w-6 h-6 bg-orange-500 rounded-full flex items-center justify-center flex-shrink-0">
                    <AlertTriangle class="h-3 w-3 text-white" />
                  </div>
                  <h4 class="text-xs md:text-sm font-bold text-orange-700">Priority</h4>
                </div>
                <p class="text-xs md:text-sm text-orange-800 font-semibold capitalize leading-relaxed">{{ selectedNotification.severity || 'Normal' }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Actions -->
      <div class="px-6 py-4 border-t border-gray-100 bg-gray-50 flex items-center justify-end space-x-3">
        <button 
          @click="closeDetails"
          class="px-4 py-2 bg-white text-gray-700 rounded-lg text-xs md:text-sm font-medium transition-colors border border-gray-200"
        >
          Close
        </button>
        <button 
          v-if="!selectedNotification.read && !selectedNotification.archived"
          @click="markAsReadAndClose(selectedNotification.id)"
          class="flex items-center px-4 py-2 bg-emerald-500 text-white rounded-lg text-xs md:text-sm font-medium transition-colors shadow-sm"
        >
          <Check class="h-4 w-4 mr-1.5 flex-shrink-0" />
          <span class="hidden md:block">Mark as Read</span>
        </button>
        <button 
          v-if="!selectedNotification.archived"
          @click="archiveCurrentNotification"
          :disabled="isArchiving"
          class="flex items-center px-4 py-2 bg-blue-500 text-white rounded-lg text-xs md:text-sm font-medium shadow-sm transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Archive v-if="!isArchiving" class="h-4 w-4 mr-1.5 flex-shrink-0" />
          <Loader2 v-else class="h-4 w-4 mr-1.5 animate-spin flex-shrink-0" />
          {{ isArchiving ? 'Archiving...' : 'Archive' }}
        </button>
        <button 
          v-if="selectedNotification.archived"
          @click="unarchiveCurrentNotification"
          :disabled="isUnarchiving"
          class="flex items-center px-4 py-2 bg-orange-500 text-white rounded-lg text-xs md:text-sm font-medium shadow-sm transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <ArchiveRestore v-if="!isUnarchiving" class="h-4 w-4 mr-1.5 flex-shrink-0" />
          <Loader2 v-else class="h-4 w-4 mr-1.5 animate-spin flex-shrink-0" />
          {{ isUnarchiving ? 'Unarchiving...' : 'Unarchive' }}
        </button>
      </div>
    </div>
  </div>

  <!-- Main Content -->
  <div class="flex-1 w-full px-2 sm:px-6 md:px-8 lg:px-10 xl:px-12 overflow-hidden">
    <!-- Main Container - Enhanced Design with proper alignment -->
     <div class="bg-white rounded-2xl shadow-md border border-emerald-100 w-full h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] overflow-hidden">
      <!-- Content Wrapper -->
      <div class="flex flex-col h-full">
        <!-- Enhanced Header Section -->
        <div class="p-4 md:p-5 border-b border-emerald-100 bg-gradient-to-r from-emerald-50 to-white">
          <!-- Header with improved layout -->
          <div class="flex items-center flex-col md:flex-row justify-between mb-5">
            <div class="flex items-center space-x-3">
              <div class="p-2.5 bg-emerald-500 rounded-xl shadow-sm">
                <component :is="showArchived ? Archive : Bell" class="h-3 w-3 md:h-5 md:w-5 text-white" />
              </div>
              <div>
                <h1 class="text-sm md:text-xl font-semibold text-gray-800">
                  {{ showArchived ? 'Archived Notifications' : 'Notifications' }}
                </h1>
                <p class="hidden md:block text-sm text-gray-500">
                  {{ showArchived ? 'View and manage your archived notifications' : 'Stay updated with your latest alerts and updates' }}
                </p>
              </div>
            </div>
            <div class="flex items-center overflow-x-auto space-x-4 md:space-x-2">
              <!-- Select Button -->
              <button 
                @click="toggleSelectMode"
                :disabled="isLoading"
                class="flex items-center px-2 md:px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                :class="isSelectMode 
                  ? 'bg-red-500 text-white' 
                  : 'bg-gray-100 text-gray-700'"
              >
                <Check class="h-4 w-4 mr-1.5" />
                <span class="hidden md:block">{{ isSelectMode ? 'Cancel Selection' : 'Select' }}</span>
              </button>

              <!-- Delete Selected Button -->
              <button 
                v-if="isSelectMode && selectedNotifications.size > 0"
                @click="deleteSelectedNotifications"
                :disabled="isLoading"
                class="flex items-center px-2 md:px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Trash2 class="h-4 w-4 mr-1.5" />
                <span class="hidden md:block">Delete Selected ({{ selectedNotifications.size }})</span>
              </button>

              <!-- Archive Toggle Button -->
              <button 
                @click="toggleArchiveView"
                :disabled="isLoading"
                class="flex items-center px-2 md:px-4 py-2 rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                :class="showArchived 
                  ? 'bg-orange-500 text-white' 
                  : 'bg-gray-100 text-gray-700'"
              >
                <component :is="showArchived ? Bell : Archive" class="h-4 w-4 mr-1.5" />
                <span class="hidden md:block">{{ showArchived ? 'Show Active' : 'Show Archived' }}</span>
              </button>
              
              <button 
                v-if="!showArchived"
                @click="markAllAsRead"
                :disabled="isLoading"
                class="flex items-center px-2 md:px-4 py-2 bg-emerald-500 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Check class="h-4 w-4 mr-1.5" />
                <span class="hidden md:block">Mark all read</span>
              </button>

              <button 
                v-if="!showArchived && !isSelectMode"
                @click="confirmDeleteAll"
                :disabled="isLoading || currentNotifications.length === 0"
                class="flex items-center px-2 md:px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Trash2 class="h-4 w-4 mr-1.5" />
                <span class="hidden md:block">Delete All</span>
              </button>

              <button 
                @click="goBack"
                class="flex items-center px-2 md:px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-sm font-medium transition-colors"
              >
                <ArrowLeft class="h-4 w-4 mr-1.5" />
                <span class="hidden md:block">Back</span>
              </button>
            </div>
          </div>

          <!-- Enhanced Filters and Search -->
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
            <!-- Filter Buttons - Fixed for single row layout -->
            <div class="flex items-center justify-start gap-1 sm:gap-2 overflow-x-auto scrollbar-hide min-w-0">
              <div class="flex items-center gap-1 sm:gap-2 flex-nowrap">
                <button 
                  v-for="filter in (showArchived ? archivedFilters : filters)" 
                  :key="filter.value"
                  @click="activeFilter = filter.value"
                  :disabled="isLoading"
                  :class="[
                    'px-2 sm:px-3 py-1.5 text-xs md:text-sm font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap flex-shrink-0',
                    activeFilter === filter.value 
                      ? 'bg-emerald-500 text-white shadow-sm' 
                      : 'bg-white text-gray-700 border border-gray-200'
                  ]"
                >
                  {{ filter.label }}
                </button>
              </div>
            </div>
            
            <!-- Search Bar - Reduced width and improved responsiveness -->
            <div class="relative w-full sm:w-80 md:w-72 lg:w-64 xl:w-80 max-w-sm flex-shrink-0">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search class="h-4 w-4 text-gray-400" />
              </div>
              <input 
                type="text"
                v-model="searchQuery"
                :disabled="isLoading"
                :placeholder="showArchived ? 'Search archived notifications...' : 'Search notifications...'"
                class="w-full pl-10 pr-4 py-2 text-xs md:text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
              />
            </div>
          </div>
        </div>

        <!-- Scrollable Notifications Content with fixed spacing -->
        <div class="flex-1 overflow-y-auto notification-scroll">
          <!-- Empty State -->
          <div v-if="!isLoading && filteredNotifications.length === 0" class="py-16 flex flex-col items-center justify-center">
            <div class="bg-gray-100 md:p-4 rounded-full mb-4">
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
          <div v-else-if="!isLoading">
            <!-- Group notifications by date -->
            <div v-for="group in paginatedGroups" :key="group.name" class="px-5 py-4">
              <div class="flex items-center mb-3 px-3 py-2 rounded-lg" 
                  :class="{
                    'bg-emerald-50': group.name === 'Today',
                    'bg-orange-50': group.name === 'Yesterday',
                    'bg-blue-50': group.name === 'A few days ago',
                    'bg-purple-50': group.name === 'A week ago',
                    'bg-indigo-50': group.name === 'A few weeks ago',
                    'bg-gray-50': group.name === 'A month ago'
                  }">
                <component 
                  :is="{
                    'Today': CalendarClock,
                    'Yesterday': CalendarDays,
                    'A few days ago': CalendarDays,
                    'A week ago': History,
                    'A few weeks ago': History,
                    'A month ago': History
                  }[group.name]" 
                  class="h-4 w-4 mr-2"
                  :class="{
                    'text-emerald-600': group.name === 'Today',
                    'text-orange-600': group.name === 'Yesterday',
                    'text-blue-600': group.name === 'A few days ago',
                    'text-purple-600': group.name === 'A week ago',
                    'text-indigo-600': group.name === 'A few weeks ago',
                    'text-gray-600': group.name === 'A month ago'
                  }" 
                />
                <span class="text-xs md:text-sm font-medium"
                      :class="{
                        'text-emerald-700': group.name === 'Today',
                        'text-orange-700': group.name === 'Yesterday',
                        'text-blue-700': group.name === 'A few days ago',
                        'text-purple-700': group.name === 'A week ago',
                        'text-indigo-700': group.name === 'A few weeks ago',
                        'text-gray-700': group.name === 'A month ago'
                      }">
                  {{ group.name }}
                </span>
              </div>
              
              <div class="space-y-2.5">
                <div 
                  v-for="notification in group.notifications" 
                  :key="notification.id"
                  @click="handleNotificationClick($event, notification)"
                  class="group p-3 rounded-xl border border-gray-100 bg-white transition-all duration-200 cursor-pointer"
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
                          :id="'notif-checkbox-' + notification.id"
                        >
                        <label :for="'notif-checkbox-' + notification.id" class="sr-only">
                          Select notification
                        </label>
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
                        <h3 class="text-xs md:text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                        <span class="text-[10px] text-xs text-gray-500 whitespace-nowrap -mr-20 md:ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                      </div>
                      <p class="text-xs md:text-sm text-gray-600 mb-2 line-clamp-2 font-medium">
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
                            class="flex items-center text-orange-600 text-xs font-medium bg-orange-50 px-2 py-1 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <component 
                              :is="unarchivingIds.has(notification.id) ? 'div' : Archive" 
                              :class="unarchivingIds.has(notification.id) ? 'animate-spin h-4 w-4 md:h-3 md:w-3 mr-1 border border-orange-600 border-t-transparent rounded-full' : 'h-3 w-3 mr-1'"
                            />
                            <span class="hidden md:block">{{ unarchivingIds.has(notification.id) ? 'Unarchiving...' : 'Archived' }}</span>
                          </button>
                          <!-- Green See Details Button -->
                          <button 
                            @click.stop="handleSeeDetails(notification)"
                            class="flex items-center px-2 py-1 text-xs font-medium text-emerald-600 bg-emerald-50 rounded-md transition-colors"
                          >
                            <Eye class="h-4 w-4 md:h-3 md:w-3 mr-1" />
                            <span class="hidden md:block">See Details</span>
                          </button>
                        </div>
                      </div>
                    </div>
                    <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        v-if="!notification.read && !showArchived"
                        @click.stop="markAsRead(notification.id)"
                        class="p-1.5 text-gray-400 rounded-lg transition-colors"
                        title="Mark as read"
                      >
                        <Check class="h-4 w-4" />
                      </button>
                      <button 
                        v-if="!showArchived"
                        @click.stop="archiveNotification(notification.id)"
                        class="p-1.5 text-gray-400 rounded-lg transition-colors"
                        title="Archive"
                      >
                        <Archive class="h-4 w-4" />
                      </button>
                      <button 
                        v-if="showArchived"
                        @click.stop="unarchiveNotification(notification.id)"
                        class="p-1.5 text-gray-400 rounded-lg transition-colors"
                        title="Unarchive"
                      >
                        <ArchiveRestore class="h-4 w-4" />
                      </button>
                      <button 
                        @click.stop="deleteNotification(notification.id)"
                        class="p-1.5 text-gray-400 rounded-lg transition-colors"
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
            <div v-if="paginatedGroups.length === 0 && filteredNotifications.length > 0" class="px-5 py-12 text-center">
              <Bell class="h-10 w-10 text-gray-300 mx-auto mb-3" />
              <p class="text-gray-500">No notifications on this page</p>
              <button 
                @click="currentPage = 1"
                class="mt-3 text-sm text-emerald-600"
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
                class="inline-flex items-center justify-center px-3 py-1.5 text-xs md:text-sm font-medium transition-colors rounded-lg
                  disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                  enabled:text-gray-700 enabled:border enabled:border-gray-200"
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
                    'relative inline-flex items-center justify-center w-8 h-8 text-xs md:text-sm transition-colors rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed',
                    page === currentPage
                      ? 'text-white bg-emerald-500 shadow-sm'
                      : page === '...'
                        ? 'cursor-default text-gray-400'
                        : 'text-gray-700 border border-gray-200'
                  ]"
                >
                  {{ page }}
                </button>
              </div>

              <button 
                @click="nextPage"
                :disabled="currentPage >= totalPages || totalPages === 0 || isLoading"
                class="inline-flex items-center justify-center px-3 py-1.5 text-xs md:text-sm font-medium transition-colors rounded-lg
                  disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                  enabled:text-gray-700 enabled:border enabled:border-gray-200"
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

  <!-- Add this modal near the other modals in the template -->
  <div v-if="showDeleteAllConfirmation" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl shadow-2xl max-w-md w-full p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-semibold text-gray-800">Confirm Delete All</h3>
        <button @click="showDeleteAllConfirmation = false" class="text-gray-400">
          <X class="w-5 w-5" />
        </button>
      </div>
      <p class="text-gray-600 mb-6">Are you sure you want to delete all {{ showArchived ? 'archived' : '' }} notifications? This action cannot be undone.</p>
      <div class="flex justify-end space-x-3">
        <button 
          @click="showDeleteAllConfirmation = false"
          class="px-4 py-2 bg-white text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200"
        >
          Cancel
        </button>
        <button 
          @click="deleteAllNotifications"
          :disabled="isDeletingAll"
          class="flex items-center px-4 py-2 bg-red-500 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Trash2 class="h-4 w-4 mr-1.5" />
          {{ isDeletingAll ? 'Deleting...' : 'Delete All' }}
        </button>
      </div>
    </div>
  </div>

  <!-- <Settings /> -->
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
  TrendingUp, TrendingDown, MapPin, Gauge, ArchiveRestore, Loader2
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
const unarchivingIds = ref(new Set())

// Notification details modal
const selectedNotifications = ref(new Set());
const selectedNotification = ref(null);
const showDetailsModal = ref(false);
const isSelectMode = ref(false);
const showDeleteAllConfirmation = ref(false)
const isDeletingAll = ref(false)
const notifications = ref([])
const archivedNotifications = ref([])
const NOTIF_COLLECTION = "notifications"
const isArchiving = ref(false);
const isUnarchiving = ref(false);

// Archive view toggle
const showArchived = ref(false)

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

// Current notifications based on view
const currentNotifications = computed(() => {
  return showArchived.value ? archivedNotifications.value : notifications.value
})

// Toast styles
const toastType = ref('info') 
const weatherModalData = ref(null);

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

// Filter notifications based on search and active filter
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

// Group notifications by date
const todayNotifications = computed(() =>
  filteredNotifications.value.filter(n => isToday(n.time))
)

const yesterdayNotifications = computed(() =>
  filteredNotifications.value.filter(n => isYesterday(n.time))
)

const fewDaysAgoNotifications = computed(() =>
  filteredNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 2 && daysAgo <= 6
  })
)

const weekAgoNotifications = computed(() =>
  filteredNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 7 && daysAgo <= 13
  })
)

const fewWeeksAgoNotifications = computed(() =>
  filteredNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 14 && daysAgo <= 29
  })
)

const monthAgoNotifications = computed(() =>
  filteredNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 30
  })
)

// Add to your component script
const getDayName = (dayIndex) => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[dayIndex] || 'Unknown day';
};

// Create paginated groups by slicing each group
const paginatedGroups = computed(() => {
  const allGroups = [
    { name: 'Today', notifications: todayNotifications.value },
    { name: 'Yesterday', notifications: yesterdayNotifications.value },
    { name: 'A few days ago', notifications: fewDaysAgoNotifications.value },
    { name: 'A week ago', notifications: weekAgoNotifications.value },
    { name: 'A few weeks ago', notifications: fewWeeksAgoNotifications.value },
    { name: 'A month ago', notifications: monthAgoNotifications.value }
  ].filter(group => group.notifications.length > 0)

  // Calculate how many items to show per page across all groups
  const itemsPerPageValue = itemsPerPage.value
  const startIndex = (currentPage.value - 1) * itemsPerPageValue
  let endIndex = startIndex + itemsPerPageValue
  let count = 0
  const result = []

  for (const group of allGroups) {
    const groupLength = group.notifications.length
    
    if (count + groupLength <= startIndex) {
      count += groupLength
      continue
    }

    const groupStart = Math.max(0, startIndex - count)
    const groupEnd = Math.min(groupLength, endIndex - count)
    
    if (groupStart < groupEnd) {
      result.push({
        name: group.name,
        notifications: group.notifications.slice(groupStart, groupEnd)
      })
      count += groupLength
    }

    if (count >= endIndex) break
  }

  return result
})

// Update total pages calculation
const totalPages = computed(() => {
  const totalItems = filteredNotifications.value.length
  return Math.ceil(totalItems / itemsPerPage.value) || 1
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
      pages.push('...', total - 3, total - 2, total - 1, total)
    } else {
      // Otherwise show ellipsis, current -1, current, current + 1, ellipsis
      pages.push('...', current - 1, current, current + 1, '...', total)
    }
  }

  return pages
})

// Date comparison helpers
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

// Notification handling methods
const handleNotificationClick = (event, notification) => {
  // Check if the click was directly on a button or input element
  if (event.target.closest('button') || event.target.closest('input')) {
    return;
  }

  if (isSelectMode.value) {
    toggleNotificationSelection(notification.id);
  }
};

const toggleSelectMode = () => {
  isSelectMode.value = !isSelectMode.value;
  if (!isSelectMode.value) {
    selectedNotifications.value = new Set();
  }
};

const toggleNotificationSelection = (id) => {
  const newSelection = new Set(selectedNotifications.value);
  if (newSelection.has(id)) {
    newSelection.delete(id);
  } else {
    newSelection.add(id);
  }
  selectedNotifications.value = newSelection;
};

// Updated delete selected notifications
const deleteSelectedNotifications = async () => {
  if (selectedNotifications.value.size === 0) return;

  try {
    isLoading.value = true;
    
    // Convert Set to Array
    const selectedIds = Array.from(selectedNotifications.value);
    
    // Create a batch operation
    const batch = writeBatch(db);
    
    selectedIds.forEach(id => {
      const docRef = doc(db, 'notifications', id);
      batch.delete(docRef);
    });
    
    await batch.commit();
    
    // Update local state
    notifications.value = notifications.value.filter(
      n => !selectedNotifications.value.has(n.id)
    );
    archivedNotifications.value = archivedNotifications.value.filter(
      n => !selectedNotifications.value.has(n.id)
    );
    
    window.showToast(
      `Deleted ${selectedNotifications.value.size} notification(s)`, 
      'success'
    );
    
    // Reset selection
    selectedNotifications.value = new Set();
    isSelectMode.value = false;
    
  } catch (error) {
    console.error('Error deleting notifications:', error);
    window.showToast('Failed to delete notifications', 'failed');
  } finally {
    isLoading.value = false;
  }
};

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
      window.showToast('No notifications to delete', 'info')
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
    
    window.showToast(`All notifications deleted successfully`, 'success')
  } catch (error) {
    console.error('Failed to delete all notifications:', error)
    window.showToast('Failed to delete all notifications', 'failed')
  } finally {
    isDeletingAll.value = false
  }
}

// Notification details methods
const openDetailsModal = (notification) => {
  selectedNotification.value = notification
  showDetailsModal.value = true
}

const handleSeeDetails = async (notification) => {
  try {
    // Mark as read if not already read
    if (!notification.read && !showArchived.value) {
      await markAsRead(notification.id);
    }
    // Open the details modal
    openDetailsModal(notification);
  } catch (error) {
    console.error('Error handling see details:', error);
    window.showToast('Failed to open notification details', 'failed');
  }
};

const closeDetails = () => {
  showDetailsModal.value = false
  selectedNotification.value = null
}

const markAsReadAndClose = async (id) => {
  try {
    await markAsRead(id);
    closeDetails();
  } catch (error) {
    console.error('Failed to mark as read:', error);
    window.showToast('Failed to mark as read', 'failed');
  }
};

const archiveNotificationAndClose = async (id) => {
  await archiveNotification(id)
  closeDetails()
}

const unarchiveNotificationAndClose = async (id) => {
  await unarchiveNotification(id)
  closeDetails()
}

// Archive view toggle
const toggleArchiveView = () => {
  showArchived.value = !showArchived.value
  activeFilter.value = 'all' // Reset filter when switching views
  currentPage.value = 1 // Reset to first page
}

// Notification type checks
const isWeatherNotification = (notification) => {
  return notification.type === 'weather' || 
         notification.category === 'weather' ||
         notification.title?.toLowerCase().includes('weather');
}

const isSoilNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
  return title.includes('soil') || title.includes('moisture') || 
         message.includes('soil') || message.includes('moisture') ||
         category.includes('soil') || type.includes('soil')
}

const isWaterNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
  return title.includes('water') || title.includes('level') || title.includes('irrigation') ||
         message.includes('water') || message.includes('level') || message.includes('irrigation') ||
         category.includes('water') || type.includes('water')
}

const isSystemNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
  return title.includes('system') || title.includes('device') || title.includes('sensor') ||
         message.includes('system') || message.includes('device') || message.includes('sensor') ||
         category.includes('system') || type.includes('system')
}

// Notification data methods
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

const getSystemData = (notification) => {
  return {
    uptime: Math.max(85, Math.min(100, 99.2 + Math.random() * 0.8 - 0.4)),
    dataPoints: Math.floor(1500 + Math.random() * 500),
    connectivity: Math.max(90, Math.min(100, 98 + Math.random() * 2 - 1)),
    power: Math.max(70, Math.min(100, 85 + Math.random() * 15 - 7.5))
  }
}

// Description methods
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

const getRainRating = (intensity) => {
  if (intensity >= 80) return 'Heavy'
  if (intensity >= 60) return 'Moderate'
  if (intensity >= 40) return 'Light'
  return 'Drizzle'
}

const getRainDescription = (intensity) => {
  const rating = getRainRating(intensity)
  if (rating === 'Heavy') return 'Expect significant rainfall with potential flooding'
  if (rating === 'Moderate') return 'Steady rain expected, plan accordingly'
  if (rating === 'Light') return 'Light precipitation, minimal impact expected'
  return 'Very light rain or drizzle'
}

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

// Enhanced notification type detection methods
const isSensorNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  const hasContext = notification.context && (
    notification.context.sensor1 || 
    notification.context.sensor2 || 
    notification.context.waterLevel !== undefined ||
    notification.context.source
  )
  
  return hasContext || 
         title.includes('soil') || title.includes('moisture') || title.includes('ph') ||
         title.includes('nitrogen') || title.includes('phosphorus') || title.includes('potassium') ||
         message.includes('soil') || message.includes('moisture') || message.includes('ph') ||
         message.includes('nitrogen') || message.includes('phosphorus') || message.includes('potassium') ||
         category.includes('soil') || category.includes('sensor') || type.includes('sensor')
}

// Helper method to safely get sensor values from context
const getSensorValue = (notification, parameter) => {
  if (!notification.context) return null
  
  // Check direct context properties first
  if (notification.context[parameter] !== undefined) {
    return notification.context[parameter]
  }
  
  // Check sensor1 data
  if (notification.context.sensor1 && notification.context.sensor1[parameter] !== undefined) {
    return notification.context.sensor1[parameter]
  }
  
  // Check sensor2 data
  if (notification.context.sensor2 && notification.context.sensor2[parameter] !== undefined) {
    return notification.context.sensor2[parameter]
  }
  
  return null
}

// Enhanced description methods for agricultural parameters
const getPhDescription = (ph) => {
  if (ph < 5.5) return 'Strongly acidic - nutrient availability poor'
  if (ph < 6.0) return 'Acidic - some nutrients may be limited'
  if (ph < 6.5) return 'Slightly acidic - good for most crops'
  if (ph <= 7.5) return 'Optimal range - excellent nutrient availability'
  if (ph <= 8.0) return 'Slightly alkaline - monitor nutrient uptake'
  return 'Highly alkaline - nutrients may be locked out'
}

const getNitrogenDescription = (nitrogen) => {
  if (nitrogen < 51) return 'Deficient - poor leafy growth expected'
  if (nitrogen < 100) return 'Low - consider nitrogen fertilization'
  if (nitrogen <= 200) return 'Adequate - good for vegetative growth'
  if (nitrogen <= 300) return 'High - monitor for excessive growth'
  return 'Excessive - may delay flowering/fruiting'
}

const getPhosphorusDescription = (phosphorus) => {
  if (phosphorus < 21) return 'Deficient - weak root & flower development'
  if (phosphorus < 40) return 'Low - consider phosphorus supplementation'
  if (phosphorus <= 60) return 'Adequate - good for root development'
  if (phosphorus <= 100) return 'High - excellent availability'
  return 'Excessive - may cause nutrient imbalances'
}

const getPotassiumDescription = (potassium) => {
  if (potassium < 101) return 'Deficient - poor stress resistance'
  if (potassium < 150) return 'Low - plants vulnerable to stress'
  if (potassium <= 250) return 'Adequate - good disease resistance'
  if (potassium <= 350) return 'High - excellent stress tolerance'
  return 'Excessive - may interfere with other nutrients'
}

// Comprehensive agricultural recommendation system
const getComprehensiveAgriculturalRecommendation = (notification) => {
  if (!notification.context) return 'No specific recommendations available at this time.'

  // Determine main parameter
  let mainParam = null
  if (notification.title?.toLowerCase().includes('moisture') || notification.category === 'soil' || notification.type === 'soil') {
    mainParam = 'soilMoisture'
  } else if (notification.title?.toLowerCase().includes('temperature') || notification.category === 'temperature') {
    mainParam = 'temperature'
  } else if (notification.title?.toLowerCase().includes('humidity') || notification.category === 'humidity') {
    mainParam = 'humidity'
  } else if (notification.title?.toLowerCase().includes('ph') || notification.category === 'ph') {
    mainParam = 'soilPh'
  } else if (notification.title?.toLowerCase().includes('nitrogen')) {
    mainParam = 'nitrogen'
  } else if (notification.title?.toLowerCase().includes('phosphorus')) {
    mainParam = 'phosphorus'
  } else if (notification.title?.toLowerCase().includes('potassium')) {
    mainParam = 'potassium'
  } else if (notification.context.waterLevel !== undefined) {
    mainParam = 'waterLevel'
  }

  // Only show recommendations for the main parameter
  const value = getSensorValue(notification, mainParam) ?? notification.context[mainParam]
  if (mainParam === 'soilMoisture') {
    if (value <= 10) return '🚨 EMERGENCY: Immediate irrigation required - crop stress imminent'
    if (value <= 20) return '⚠️ Schedule irrigation within 6-12 hours to prevent plant stress'
    if (value <= 30) return '💧 Consider irrigation within 24 hours depending on weather conditions'
    if (value > 70) return '⚠️ Soil oversaturated - suspend irrigation and improve drainage'
    return '✅ Soil moisture is within optimal range'
  }
  if (mainParam === 'temperature') {
    if (value < 15) return '🌡️ Cold conditions - consider row covers or greenhouse protection'
    if (value > 35) return '🌡️ High temperature stress - increase irrigation frequency and provide shade'
    return '✅ Temperature is optimal for crops'
  }
  if (mainParam === 'humidity') {
    if (value < 40) return '💨 Low humidity - increase irrigation frequency to prevent wilting'
    if (value > 80) return '💨 High humidity - improve ventilation to prevent fungal diseases'
    return '✅ Humidity is within acceptable range'
  }
  if (mainParam === 'soilPh') {
    if (value < 6.0) return '🧪 Soil too acidic - apply lime to raise pH for better nutrient uptake'
    if (value > 7.5) return '🧪 Soil too alkaline - apply sulfur or organic matter to lower pH'
    return '✅ Soil pH is optimal'
  }
  if (mainParam === 'nitrogen') {
    if (value < 75) return '🌱 Low nitrogen - apply nitrogen-rich fertilizer for better leaf growth'
    if (value > 250) return '⚠️ Excess nitrogen - reduce fertilization to prevent delayed maturity'
    return '✅ Nitrogen level is adequate'
  }
  if (mainParam === 'phosphorus') {
    if (value < 30) return '🌸 Low phosphorus - apply phosphorus fertilizer for root and flower development'
    if (value > 80) return '⚠️ Excess phosphorus - may interfere with micronutrient uptake'
    return '✅ Phosphorus level is adequate'
  }
  if (mainParam === 'potassium') {
    if (value < 120) return '💪 Low potassium - apply potassium fertilizer for disease resistance'
    if (value > 300) return '⚠️ Excess potassium - may cause magnesium deficiency'
    return '✅ Potassium level is adequate'
  }
  if (mainParam === 'waterLevel') {
    if (value <= 15) return '🚨 CRITICAL: Immediate water refill required - irrigation capacity severely limited'
    if (value <= 30) return '⚠️ Schedule water refill within 24 hours to maintain irrigation capacity'
    if (value >= 80) return '✅ Excellent water reserves - full irrigation schedule can proceed'
    return '💧 Water level is adequate'
  }
  return '✅ Current conditions are within acceptable ranges - continue regular monitoring'
}

// Action priority determination
const getActionPriority = (notification) => {
  if (!notification.context) return 'Monitor'
  
  const context = notification.context
  const severity = notification.severity?.toLowerCase()
  
  // Critical conditions
  if (severity === 'critical') return 'IMMEDIATE ACTION REQUIRED'
  
  const soilMoisture = getSensorValue(notification, 'soilMoisture')
  const temperature = getSensorValue(notification, 'temperature')
  const waterLevel = context.waterLevel
  
  if (waterLevel !== undefined && waterLevel <= 15) return 'IMMEDIATE ACTION REQUIRED'
  if (soilMoisture !== null && soilMoisture <= 10) return 'IMMEDIATE ACTION REQUIRED'
  if (temperature !== null && (temperature < 10 || temperature > 40)) return 'IMMEDIATE ACTION REQUIRED'
  
  // High priority conditions
  if (severity === 'warning') return 'High Priority - Act within 24 hours'
  if (waterLevel !== undefined && waterLevel <= 30) return 'High Priority - Act within 24 hours'
  if (soilMoisture !== null && soilMoisture <= 20) return 'High Priority - Act within 24 hours'
  
  // Medium priority conditions
  const ph = getSensorValue(notification, 'soilPh')
  const nitrogen = getSensorValue(notification, 'nitrogen')
  const phosphorus = getSensorValue(notification, 'phosphorus')
  const potassium = getSensorValue(notification, 'potassium')
  
  if (ph !== null && (ph < 5.5 || ph > 8.0)) return 'Medium Priority - Act within 3-7 days'
  if (nitrogen !== null && nitrogen < 50) return 'Medium Priority - Act within 3-7 days'
  if (phosphorus !== null && phosphorus < 20) return 'Medium Priority - Act within 3-7 days'
  if (potassium !== null && potassium < 100) return 'Medium Priority - Act within 3-7 days'
  
  return 'Low Priority - Monitor and plan'
}

// Weather-specific recommendations
const getWeatherRecommendation = (notification) => {
  if (!notification.context) return 'Monitor weather conditions and adjust agricultural activities accordingly.'
  
  const condition = notification.context.condition?.toLowerCase() || ''
  const forecast = notification.context.forecast
  const current = notification.context.current
  
  const recommendations = []
  
  // Severe weather recommendations
  if (condition.includes('heavy rain') || condition.includes('thunderstorm')) {
    recommendations.push('🌧️ Prepare for heavy rainfall - ensure proper drainage and secure equipment')
    recommendations.push('⚡ Risk of electrical storms - avoid outdoor electrical operations')
    recommendations.push('💧 Suspended irrigation may be possible due to natural precipitation')
  }
  
  if (condition.includes('rain shower')) {
    recommendations.push('🌦️ Light precipitation expected - reduce or suspend irrigation schedules')
    recommendations.push('🌱 Good conditions for nutrient uptake - consider liquid fertilizer application after rain')
  }
  
  // Temperature-based recommendations
  if (current?.temperature !== undefined) {
    if (current.temperature > 30) {
      recommendations.push('🌡️ High temperatures - increase irrigation frequency and provide shade protection')
    } else if (current.temperature < 15) {
      recommendations.push('🌡️ Cool temperatures - protect sensitive plants and adjust watering schedule')
    }
  }
  
  // Wind recommendations
  if (current?.windSpeed !== undefined && current.windSpeed > 20) {
    recommendations.push('💨 Strong winds expected - secure structures and protect young plants')
  }
  
  // UV recommendations
  if (current?.uvIndex !== undefined && current.uvIndex > 7) {
    recommendations.push('☀️ High UV levels - provide shade protection for sensitive crops')
  }
  
  // Humidity recommendations
  if (current?.humidity !== undefined) {
    if (current.humidity > 80) {
      recommendations.push('💨 High humidity - monitor for fungal diseases and improve ventilation')
    } else if (current.humidity < 40) {
      recommendations.push('💧 Low humidity - increase irrigation frequency to prevent plant stress')
    }
  }
  
  // Forecast-based recommendations
  if (forecast?.temperature_max !== undefined && forecast?.temperature_min !== undefined) {
    const tempRange = forecast.temperature_max - forecast.temperature_min
    if (tempRange > 15) {
      recommendations.push('🌡️ Large temperature variation expected - monitor plants for stress')
    }
  }
  
  if (recommendations.length === 0) {
    recommendations.push('✅ Weather conditions are favorable for normal agricultural operations')
  }
  
  return recommendations.join(' • ')
}

// Enhanced existing description methods with more detailed feedback
const getEnhancedHumidityDescription = (humidity) => {
  if (humidity >= 90) return 'Extremely humid - high disease risk'
  if (humidity >= 80) return 'Very humid - monitor for fungal issues'
  if (humidity >= 70) return 'High humidity - good for growth'
  if (humidity >= 60) return 'Moderate humidity - optimal conditions'
  if (humidity >= 50) return 'Comfortable humidity levels'
  if (humidity >= 40) return 'Moderate humidity - acceptable'
  if (humidity >= 30) return 'Low humidity - may cause stress'
  return 'Very low humidity - irrigation critical'
}

const getEnhancedTemperatureDescription = (temp) => {
  if (temp >= 40) return 'Extremely hot - emergency cooling needed'
  if (temp >= 35) return 'Very hot - heat stress likely'
  if (temp >= 30) return 'Hot - increase irrigation frequency'
  if (temp >= 25) return 'Warm - optimal for most crops'
  if (temp >= 20) return 'Moderate - good growing conditions'
  if (temp >= 15) return 'Cool - slower growth expected'
  if (temp >= 10) return 'Cold - protect sensitive plants'
  return 'Very cold - frost protection needed'
}

const getEnhancedMoistureDescription = (moisture) => {
  if (moisture >= 80) return 'Oversaturated - drainage issues likely'
  if (moisture >= 70) return 'Very moist - monitor for root problems'
  if (moisture >= 60) return 'High moisture - excellent conditions'
  if (moisture >= 50) return 'Optimal moisture - ideal for growth'
  if (moisture >= 40) return 'Adequate moisture - monitor regularly'
  if (moisture >= 30) return 'Moderate moisture - irrigation soon'
  if (moisture >= 20) return 'Low moisture - irrigation needed'
  if (moisture >= 10) return 'Very low - urgent irrigation required'
  return 'Critical drought - immediate action needed'
}

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

// Notification actions
const markAsRead = async (docId) => {
  try {
    const notifIndex = notifications.value.findIndex(n => n.id === docId);
    if (notifIndex !== -1) {
      // Update local state first for immediate UI feedback
      notifications.value[notifIndex].read = true;

      // Firestore update
      const notifRef = doc(db, NOTIF_COLLECTION, docId);
      await updateDoc(notifRef, { read: true });
    }
  } catch (err) {
    console.error("Failed to mark as read:", err);
    // Revert local state if Firestore update fails
    const notifIndex = notifications.value.findIndex(n => n.id === docId);
    if (notifIndex !== -1) {
      notifications.value[notifIndex].read = false;
    }
    throw err;
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

const archiveCurrentNotification = async () => {
  if (!selectedNotification.value) return;
  
  try {
    isArchiving.value = true;
    await archiveNotification(selectedNotification.value.id);
    window.showToast('Notification archived', 'success');
    closeDetails();
  } catch (error) {
    console.error('Failed to archive notification:', error);
    window.showToast('Failed to archive notification', 'failed');
  } finally {
    isArchiving.value = false;
  }
};

const unarchiveCurrentNotification = async () => {
  if (!selectedNotification.value) return;
  
  try {
    isUnarchiving.value = true;
    await unarchiveNotification(selectedNotification.value.id);
    window.showToast('Notification unarchived', 'success');
    closeDetails();
  } catch (error) {
    console.error('Failed to unarchive notification:', error);
    window.showToast('Failed to unarchive notification', 'failed');
  } finally {
    isUnarchiving.value = false;
  }
};

// Update the existing archive/unarchive methods to be more focused:
const archiveNotification = async (docId) => {
  try {
    const notifRef = doc(db, NOTIF_COLLECTION, docId);
    await updateDoc(notifRef, { 
      archived: true,
      read: true,
      archivedAt: new Date()
    });
  } catch (err) {
    console.error("❌ Failed to archive notification:", err);
    throw err; // Re-throw to be caught by the calling function
  }
};

const unarchiveNotification = async (docId) => {
  try {
    const notifRef = doc(db, NOTIF_COLLECTION, docId);
    await updateDoc(notifRef, { 
      archived: false,
      archivedAt: null
    });
  } catch (err) {
    console.error("❌ Failed to unarchive notification:", err);
    throw err; // Re-throw to be caught by the calling function
  }
};

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

const deleteNotification = async (docId) => {
  try {
    deletingIds.value.add(docId)
    
    // Remove from both active and archived arrays
    notifications.value = notifications.value.filter(n => n.id !== docId)
    archivedNotifications.value = archivedNotifications.value.filter(n => n.id !== docId)
    
    // Firestore delete
    await deleteDoc(doc(db, NOTIF_COLLECTION, docId))
    
    window.showToast('Notification deleted', 'success')
  } catch (err) {
    console.error("❌ Failed to delete notification:", err)
    window.showToast('Failed to delete notification', 'failed')
  } finally {
    deletingIds.value.delete(docId)
  }
}

// Format notification time
const formatTime = (time) => {
  if (!time) return 'Unknown time'
  const now = new Date()
  const diff = now - new Date(time)
  const mins = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (mins < 60) return `${mins} m${mins !== 1 ? 's' : ''} ago`
  if (hours < 24) return `${hours} h${hours !== 1 ? 's' : ''} ago`
  if (days < 7) return `${days} d${days !== 1 ? 's' : ''} ago`
  return new Date(time).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

// Notification icon system
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

// Navigation
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
    
    if (unsubscribeNotifications.value) {
      unsubscribeNotifications.value();
    }
    
    unsubscribeNotifications.value = onSnapshot(q, (snapshot) => {
      const allNotifications = [];
      
      snapshot.forEach((doc) => {
        const data = doc.data();
        allNotifications.push({
          ...data,
          id: doc.id,
          time: data.timestamp?.toDate?.() ?? new Date(),
          // Ensure context exists and has proper structure
          context: data.context || {}
        });
      });

      notifications.value = allNotifications.filter(n => !n.archived);
      archivedNotifications.value = allNotifications.filter(n => n.archived);
      
      const changes = snapshot.docChanges();
      const newAdditions = changes.filter(
        change => change.type === 'added' && 
                 change.doc.metadata.hasPendingWrites === false
      );
      
      if (newAdditions.length > 0 && !showArchived.value) {
        window.showToast(
          `${newAdditions.length} new notification${newAdditions.length > 1 ? 's' : ''}`,
          'info'
        );
      }
    }, (error) => {
      console.error('Error receiving notifications:', error);
      window.showToast('Error loading notifications', 'failed');
    });
    
  } catch (error) {
    console.error('Failed to setup notifications listener:', error);
    window.showToast('Failed to setup notifications', 'failed');
  } finally {
    isLoading.value = false;
  }
};

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

// Lifecycle hooks
onMounted(() => {
  loadUserPreferences() // Load user preferences on mount
  fetchNotifications()
  eventBus.on('notification-saved-success', fetchNotifications)
})

onUnmounted(() => {
  stopLoadingAnimation()
  if (unsubscribeNotifications.value) {
    unsubscribeNotifications.value()
  }
})

// Watchers
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

watch([activeFilter, searchQuery], () => {
  currentPage.value = 1
})
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

/* Hide scrollbar for filter buttons on mobile */
.scrollbar-hide {
  -ms-overflow-style: none;  /* Internet Explorer 10+ */
  scrollbar-width: none;  /* Firefox */
}
.scrollbar-hide::-webkit-scrollbar { 
  display: none;  /* Safari and Chrome */
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

/* Prevent any movement during scroll */
.static {
  position: static !important;
  transform: none !important;
  transition: none !important;
}

/* Ensure smooth scrolling without element movement */
.overflow-y-auto {
  scroll-behavior: smooth;
  -webkit-overflow-scrolling: touch;
}

/* Prevent layout shifts during scroll */
* {
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}
</style>