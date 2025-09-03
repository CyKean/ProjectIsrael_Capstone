
<template>
  <!-- Loading Overlay -->
  <div v-if="isLoading" class="fixed inset-0 bg-black/20 backdrop-blur-sm z-50 flex items-center justify-center">
    <div class="bg-white rounded-2xl shadow-2xl border-2 border-transparent bg-gradient-to-r from-yellow-200 via-emerald-200 to-green-300 p-0.5 max-w-md mx-4">
      <div class="bg-white rounded-2xl p-6 sm:p-8 text-center">
        <!-- Notification Icon Animation -->
        <div class="mb-4 sm:mb-6 relative">
          <div class="w-16 h-16 sm:w-20 sm:h-20 mx-auto bg-gradient-to-br from-emerald-400 to-green-500 rounded-2xl flex items-center justify-center shadow-lg">
            <Bell class="h-8 w-8 sm:h-10 sm:w-10 text-white animate-bounce" />
          </div>
          <!-- Notification Badge -->
          <div class="absolute -top-1 -right-1 w-5 h-5 sm:w-6 sm:h-6 bg-red-500 rounded-full flex items-center justify-center">
            <span class="text-white text-xs font-bold">!</span>
          </div>
        </div>
        
        <!-- Loading Dots -->
        <div class="flex justify-center space-x-2 mb-4 sm:mb-6">
          <div 
            v-for="i in 5" 
            :key="i"
            class="w-2 h-2 rounded-full transition-all duration-300"
            :class="loadingDotIndex === i - 1 ? 'bg-emerald-500 scale-125' : 'bg-gray-300'"
          ></div>
        </div>
        
        <!-- Loading Text -->
        <h3 class="text-lg sm:text-xl font-semibold text-gray-800 mb-2">Loading Notifications</h3>
        <p class="text-gray-600 text-sm">Please wait while we fetch your latest alerts and updates</p>
      </div>
    </div>
  </div>

  <!-- Enhanced Notification Details Modal - MOBILE RESPONSIVE -->
  <div v-if="showDetailsModal && selectedNotification" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-2 sm:p-4">
    <div class="bg-white rounded-xl sm:rounded-2xl shadow-2xl w-full max-w-4xl max-h-[95vh] sm:max-h-[90vh] overflow-hidden border border-gray-200">
      <!-- Modal Header -->
      <div class="px-3 sm:px-6 py-3 sm:py-4 border-b border-gray-100 bg-gradient-to-r from-gray-50 to-white">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-2 sm:space-x-3 min-w-0 flex-1">
            <div 
              class="w-8 h-8 sm:w-10 sm:h-10 rounded-lg sm:rounded-xl flex items-center justify-center shadow-sm flex-shrink-0"
              :class="getNotificationIcon(selectedNotification).bgColor"
            >
              <component 
                :is="getNotificationIcon(selectedNotification).icon" 
                class="h-4 w-4 sm:h-5 sm:w-5 text-white" 
              />
            </div>
            <div class="min-w-0 flex-1">
              <h2 class="text-sm sm:text-lg font-semibold text-gray-800 truncate">Notification Details</h2>
              <p class="text-xs sm:text-sm text-gray-500 truncate">{{ formatTime(selectedNotification.time) }}</p>
            </div>
          </div>
          <button 
            @click="closeDetails"
            class="p-1.5 sm:p-2 text-gray-400 rounded-lg transition-colors flex-shrink-0"
          >
            <X class="h-4 w-4 sm:h-5 sm:w-5" />
          </button>
        </div>
      </div>

      <!-- Modal Content - MOBILE RESPONSIVE LAYOUT -->
      <div class="overflow-y-auto max-h-[calc(95vh-140px)] sm:max-h-[calc(90vh-160px)]">
        <div class="p-3 sm:p-6">
          <div class="space-y-4 sm:space-y-6">
            <!-- Title and Status -->
            <div class="space-y-3">
              <div class="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-2">
                <h3 class="text-base sm:text-xl font-semibold text-gray-900 min-w-0">{{ selectedNotification.title }}</h3>
                <div class="flex items-center flex-wrap gap-2">
                  <span 
                    class="inline-flex items-center px-2 sm:px-2.5 py-1 rounded-full text-xs font-medium whitespace-nowrap"
                    :class="getNotificationIcon(selectedNotification).badgeColor"
                  >
                    {{ selectedNotification.category || selectedNotification.type }}
                  </span>
                  
                  <div v-if="selectedNotification.archived" class="flex items-center text-orange-600 text-xs font-medium whitespace-nowrap">
                    <Archive class="h-3 w-3 mr-1 flex-shrink-0" />
                    Archived
                  </div>
                </div>
              </div>
            </div>

            <!-- Message -->
            <div class="space-y-2">
              <h4 class="text-xs sm:text-sm font-medium text-gray-700">Message</h4>
              <p class="text-sm sm:text-md text-gray-700 leading-relaxed font-medium">
                {{ selectedNotification.message }}
              </p>
            </div>

            <!-- Enhanced Detailed Analysis Container - MOBILE RESPONSIVE -->
            <div class="bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 rounded-xl sm:rounded-2xl border-2 border-indigo-100 shadow-lg">
              <div class="p-3 sm:p-5">
                <div class="mb-3 sm:mb-4">
                  <h4 class="text-sm sm:text-lg font-bold text-gray-800 flex items-center">
                    <div class="w-6 h-6 sm:w-7 sm:h-7 bg-indigo-500 rounded-full flex items-center justify-center mr-2 sm:mr-3 flex-shrink-0">
                      <Info class="h-3 w-3 sm:h-4 sm:w-4 text-white" />
                    </div>
                    <span class="text-sm sm:text-lg">Detailed Analysis & Context</span>
                  </h4>
                </div>

                <!-- 1. Low Water Alert -->
                <div v-if="selectedNotification.context?.type === 'water-level'" class="space-y-3 sm:space-y-5">
                  <div class="text-xs sm:text-sm text-gray-600 bg-white/70 rounded-lg p-2 sm:p-3 border border-indigo-200">
                    Water level status for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                  </div>
                  
                  <!-- Water Level Status -->
                  <div class="bg-cyan-100 rounded-lg sm:rounded-xl border-2 border-cyan-300 shadow-sm">
                    <div class="p-3 sm:p-4 text-center">
                      <div class="flex items-center justify-center space-x-2 mb-3">
                        <Gauge class="h-4 w-4 sm:h-5 sm:w-5 text-cyan-600 flex-shrink-0" />
                        <span class="text-sm sm:text-base font-semibold text-cyan-700">Water Level Status</span>
                      </div>
                      <div class="text-center mb-3">
                        <span class="text-3xl sm:text-5xl font-bold text-cyan-800">
                          {{ selectedNotification.context.waterLevel || '--' }}%
                        </span>
                      </div>
                      <p class="text-xs sm:text-sm text-cyan-700 font-medium">
                        {{ getWaterLevelDescription(selectedNotification.context.waterLevel) }}
                      </p>
                    </div>
                  </div>

                  <!-- Status and Priority -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-4">
                    <div class="bg-blue-50 rounded-lg sm:rounded-xl border-2 border-blue-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <AlertTriangle class="h-3 w-3 sm:h-4 sm:w-4 text-blue-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-blue-700">Status</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-blue-800 mb-1">
                          {{ selectedNotification.context.status || '--' }}
                        </p>
                      </div>
                    </div>
                    
                    <div class="bg-orange-50 rounded-lg sm:rounded-xl border-2 border-orange-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <AlertCircle class="h-3 w-3 sm:h-4 sm:w-4 text-orange-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-orange-700">Priority</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-orange-800 mb-1">
                          {{ selectedNotification.context.priority || '--' }}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Agricultural Recommendation -->
                  <div class="bg-emerald-100 rounded-lg sm:rounded-xl border-2 border-emerald-300 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-3 w-3 sm:h-4 sm:w-4 text-emerald-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-emerald-700">Agricultural Recommendation</span>
                      </div>
                      <p class="text-xs sm:text-sm text-emerald-800 font-medium leading-relaxed">
                        {{ selectedNotification.context.recommendation || getWateringRecommendation(selectedNotification) }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 2. Humidity/Temperature Alert -->
                <div v-else-if="selectedNotification.context?.type === 'humidity-temperature'" class="space-y-3 sm:space-y-5">
                  <div class="text-xs sm:text-sm text-gray-600 bg-white/70 rounded-lg p-2 sm:p-3 border border-indigo-200">
                    Environmental conditions for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                  </div>
                  
                  <!-- Key Metrics Display -->
                  <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 sm:gap-4">
                    <!-- Humidity -->
                    <div class="bg-blue-50 rounded-lg sm:rounded-xl border-2 border-blue-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Droplet class="h-3 w-3 sm:h-4 sm:w-4 text-blue-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-blue-700">Humidity</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-blue-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.humidity) || '--' }}%
                        </p>
                      </div>
                    </div>
                    
                    <!-- Temperature -->
                    <div class="bg-red-50 rounded-lg sm:rounded-xl border-2 border-red-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Thermometer class="h-3 w-3 sm:h-4 sm:w-4 text-red-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-red-700">Temperature</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-red-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.temperature) || '--' }}°C
                        </p>
                      </div>
                    </div>
                    
                    <!-- Soil Moisture -->
                    <div class="bg-amber-50 rounded-lg sm:rounded-xl border-2 border-amber-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Droplet class="h-3 w-3 sm:h-4 sm:w-4 text-amber-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-amber-700">Soil Moisture</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-amber-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.soilMoisture) || '--' }}%
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Agricultural Recommendation -->
                  <div class="bg-emerald-100 rounded-lg sm:rounded-xl border-2 border-emerald-300 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-3 w-3 sm:h-4 sm:w-4 text-emerald-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-emerald-700">Agricultural Recommendation</span>
                      </div>
                      <p class="text-xs sm:text-sm text-emerald-800 font-medium leading-relaxed">
                        {{ selectedNotification.context.recommendation || getTempHumidityRecommendation(selectedNotification) }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 3. Low Soil Alert -->
                <div v-else-if="selectedNotification.context?.type === 'low-soil'" class="space-y-3 sm:space-y-5">
                  <div class="text-xs sm:text-sm text-gray-600 bg-white/70 rounded-lg p-2 sm:p-3 border border-indigo-200">
                    Soil conditions for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                  </div>
                  
                  <!-- All Sensor Data Display -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-4">
                    <!-- Soil Moisture -->
                    <div class="bg-amber-50 rounded-lg sm:rounded-xl border-2 border-amber-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Droplet class="h-3 w-3 sm:h-4 sm:w-4 text-amber-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-amber-700">Soil Moisture</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-amber-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.soilMoisture) || '--' }}%
                        </p>
                      </div>
                    </div>
                    
                    <!-- Temperature -->
                    <div class="bg-red-50 rounded-lg sm:rounded-xl border-2 border-red-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Thermometer class="h-3 w-3 sm:h-4 sm:w-4 text-red-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-red-700">Temperature</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-red-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.temperature) || '--' }}°C
                        </p>
                      </div>
                    </div>
                    
                    <!-- Humidity -->
                    <div class="bg-blue-50 rounded-lg sm:rounded-xl border-2 border-blue-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Droplet class="h-3 w-3 sm:h-4 sm:w-4 text-blue-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-blue-700">Humidity</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-blue-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.humidity) || '--' }}%
                        </p>
                      </div>
                    </div>
                    
                    <!-- Nitrogen -->
                    <div class="bg-green-50 rounded-lg sm:rounded-xl border-2 border-green-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Leaf class="h-3 w-3 sm:h-4 sm:w-4 text-green-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-green-700">Nitrogen (N)</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-green-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.nitrogen) || '--' }} ppm
                        </p>
                        <p class="text-xs text-green-600 leading-tight">
                          Level: {{ getNitrogenLevel(parseFloat(getFormattedValue(selectedNotification.context.nitrogen))) }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Phosphorus -->
                    <div class="bg-orange-50 rounded-lg sm:rounded-xl border-2 border-orange-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Sprout class="h-3 w-3 sm:h-4 sm:w-4 text-orange-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-orange-700">Phosphorus (P)</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-orange-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.phosphorus) || '--' }} ppm
                        </p>
                        <p class="text-xs text-orange-600 leading-tight">
                          Level: {{ getPhosphorusLevel(parseFloat(getFormattedValue(selectedNotification.context.phosphorus))) }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Potassium -->
                    <div class="bg-yellow-50 rounded-lg sm:rounded-xl border-2 border-yellow-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Activity class="h-3 w-3 sm:h-4 sm:w-4 text-yellow-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-yellow-700">Potassium (K)</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-yellow-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.potassium) || '--' }} ppm
                        </p>
                        <p class="text-xs text-yellow-600 leading-tight">
                          Level: {{ getPotassiumLevel(parseFloat(getFormattedValue(selectedNotification.context.potassium))) }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Soil pH -->
                    <div class="bg-purple-50 rounded-lg sm:rounded-xl border-2 border-purple-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Gauge class="h-3 w-3 sm:h-4 sm:w-4 text-purple-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-purple-700">Soil pH</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-purple-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.soilPh) || '--' }}
                        </p>
                        <p class="text-xs text-purple-600 leading-tight">
                          Condition: {{ getPhDescription(parseFloat(getFormattedValue(selectedNotification.context.soilPh))) }}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Agricultural Recommendation -->
                  <div class="bg-emerald-100 rounded-lg sm:rounded-xl border-2 border-emerald-300 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-3 w-3 sm:h-4 sm:w-4 text-emerald-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-emerald-700">Agricultural Recommendation</span>
                      </div>
                      <p class="text-xs sm:text-sm text-emerald-800 font-medium leading-relaxed">
                        {{ selectedNotification.context.recommendation || getComprehensiveAgriculturalRecommendation(selectedNotification) }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 4. NPK / Soil pH Alert -->
                <div v-else-if="selectedNotification.context?.type === 'npk-ph'" class="space-y-3 sm:space-y-5">
                  <div class="text-xs sm:text-sm text-gray-600 bg-white/70 rounded-lg p-2 sm:p-3 border border-indigo-200">
                    Soil nutrient analysis for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                  </div>
                  
                  <!-- NPK Values -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2 sm:gap-4">
                    <!-- Nitrogen -->
                    <div class="bg-green-50 rounded-lg sm:rounded-xl border-2 border-green-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Leaf class="h-3 w-3 sm:h-4 sm:w-4 text-green-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-green-700">Nitrogen (N)</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-green-800 mb-1">
                          {{ selectedNotification.context.nitrogen?.value || '--' }} ppm
                        </p>
                        <p class="text-xs text-green-600 leading-tight">
                          Level: {{ selectedNotification.context.nitrogen?.level || '--' }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Phosphorus -->
                    <div class="bg-orange-50 rounded-lg sm:rounded-xl border-2 border-orange-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Sprout class="h-3 w-3 sm:h-4 sm:w-4 text-orange-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-orange-700">Phosphorus (P)</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-orange-800 mb-1">
                          {{ selectedNotification.context.phosphorus?.value || '--' }} ppm
                        </p>
                        <p class="text-xs text-orange-600 leading-tight">
                          Level: {{ selectedNotification.context.phosphorus?.level || '--' }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Potassium -->
                    <div class="bg-yellow-50 rounded-lg sm:rounded-xl border-2 border-yellow-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Activity class="h-3 w-3 sm:h-4 sm:w-4 text-yellow-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-yellow-700">Potassium (K)</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-yellow-800 mb-1">
                          {{ selectedNotification.context.potassium?.value || '--' }} ppm
                        </p>
                        <p class="text-xs text-yellow-600 leading-tight">
                          Level: {{ selectedNotification.context.potassium?.level || '--' }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Soil pH -->
                    <div class="bg-purple-50 rounded-lg sm:rounded-xl border-2 border-purple-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Gauge class="h-3 w-3 sm:h-4 sm:w-4 text-purple-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-purple-700">Soil pH</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-purple-800 mb-1">
                          {{ selectedNotification.context.soilPh?.value || '--' }}
                        </p>
                        <p class="text-xs text-purple-600 leading-tight">
                          Condition: {{ selectedNotification.context.soilPh?.condition || '--' }}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Agricultural Recommendation -->
                  <div class="bg-emerald-100 rounded-lg sm:rounded-xl border-2 border-emerald-300 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-3 w-3 sm:h-4 sm:w-4 text-emerald-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-emerald-700">Agricultural Recommendation</span>
                      </div>
                      <p class="text-xs sm:text-sm text-emerald-800 font-medium leading-relaxed">
                        {{ selectedNotification.context.recommendation || getSoilNutrientRecommendation(selectedNotification) }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 5. Soil Moisture Notification -->
                <div v-else-if="selectedNotification.context?.type === 'soil-moisture'" class="space-y-3 sm:space-y-5">
                  <div class="text-xs sm:text-sm text-gray-600 bg-white/70 rounded-lg p-2 sm:p-3 border border-indigo-200">
                    Soil moisture status for {{ selectedNotification.context.date || formatFullDate(selectedNotification.time) }}.
                  </div>
                  
                  <!-- Soil Moisture -->
                  <div class="bg-amber-100 rounded-lg sm:rounded-xl border-2 border-amber-300 shadow-sm">
                    <div class="p-3 sm:p-4 text-center">
                      <div class="flex items-center justify-center space-x-2 mb-3">
                        <Droplet class="h-4 w-4 sm:h-5 sm:w-5 text-amber-600 flex-shrink-0" />
                        <span class="text-sm sm:text-base font-semibold text-amber-700">Soil Moisture Level</span>
                      </div>
                      <div class="text-center mb-3">
                        <span class="text-3xl sm:text-5xl font-bold text-amber-800">
                          {{ getFormattedValue(selectedNotification.context.soilMoisture) || '--' }}%
                        </span>
                      </div>
                      <p class="text-xs sm:text-sm text-amber-700 font-medium">
                        {{ getMoistureDescription(parseFloat(getFormattedValue(selectedNotification.context.soilMoisture))) }}
                      </p>
                    </div>
                  </div>

                  <!-- Motor Status and Water Level -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-4">
                    <!-- Motor Status -->
                    <div class="bg-green-50 rounded-lg sm:rounded-xl border-2 border-green-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Zap class="h-3 w-3 sm:h-4 sm:w-4 text-green-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-green-700">Motor Status</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-green-800 mb-1">
                          {{ selectedNotification.context.motorStatus || 'Auto' }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Water Level -->
                    <div class="bg-cyan-50 rounded-lg sm:rounded-xl border-2 border-cyan-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Gauge class="h-3 w-3 sm:h-4 sm:w-4 text-cyan-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-cyan-700">Water Level</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-cyan-800 mb-1">
                          {{ getFormattedValue(selectedNotification.context.waterLevel) || '--' }}%
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Time of Last Activation -->
                  <div v-if="selectedNotification.context.lastActivation" class="bg-blue-50 rounded-lg sm:rounded-xl border-2 border-blue-200 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Clock class="h-3 w-3 sm:h-4 sm:w-4 text-blue-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-medium text-blue-700">Last Auto Activation</span>
                      </div>
                      <p class="text-sm sm:text-base font-bold text-blue-800 mb-1">
                        {{ formatTime(selectedNotification.context.lastActivation) }}
                      </p>
                    </div>
                  </div>
                  
                  <!-- Agricultural Recommendation -->
                  <div class="bg-emerald-100 rounded-lg sm:rounded-xl border-2 border-emerald-300 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-3 w-3 sm:h-4 sm:w-4 text-emerald-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-emerald-700">Agricultural Recommendation</span>
                      </div>
                      <p class="text-xs sm:text-sm text-emerald-800 font-medium leading-relaxed">
                        {{ selectedNotification.context.recommendation || getSoilMoistureRecommendation(selectedNotification) }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 6. Water Scheduling Alert -->
                <div v-else-if="selectedNotification.context?.type === 'watering-schedule'" class="space-y-3 sm:space-y-5">
                  <div class="text-xs sm:text-sm text-gray-600 bg-white/70 rounded-lg p-2 sm:p-3 border border-indigo-200">
                    Watering schedule details for {{ selectedNotification.context.scheduleDate || formatFullDate(selectedNotification.time) }}.
                  </div>
                  
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-4">
                    <!-- Schedule Type -->
                    <div class="bg-blue-50 rounded-lg sm:rounded-xl border-2 border-blue-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <CalendarClock class="h-3 w-3 sm:h-4 sm:w-4 text-blue-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-blue-700">Schedule Type</span>
                        </div>
                        <p class="text-base sm:text-lg font-bold text-blue-800 mb-1 capitalize">
                          {{ selectedNotification.context.scheduleType }}
                          <span v-if="selectedNotification.context.scheduleType === 'weekly'">
                            ({{ getDayName(selectedNotification.context.dayOfWeek) }})
                          </span>
                        </p>
                      </div>
                    </div>
                    
                    <!-- Duration -->
                    <div class="bg-green-50 rounded-lg sm:rounded-xl border-2 border-green-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Clock class="h-3 w-3 sm:h-4 sm:w-4 text-green-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-green-700">Duration</span>
                        </div>
                        <p class="text-base sm:text-lg font-bold text-green-800 mb-1">
                          {{ selectedNotification.context.duration }} minute{{ selectedNotification.context.duration !== 1 ? 's' : '' }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Start/End Time -->
                    <div class="bg-purple-50 rounded-lg sm:rounded-xl border-2 border-purple-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <component :is="selectedNotification.title.includes('Started') ? Play : StopCircle" 
                                    class="h-3 w-3 sm:h-4 sm:w-4 text-purple-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-purple-700">
                            {{ selectedNotification.title.includes('Started') ? 'Start Time' : 'End Time' }}
                          </span>
                        </div>
                        <p class="text-base sm:text-lg font-bold text-purple-800 mb-1">
                          {{ selectedNotification.context.startTime || selectedNotification.context.endTime || formatTime(selectedNotification.time) }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Water Level at Start -->
                    <div class="bg-cyan-50 rounded-lg sm:rounded-xl border-2 border-cyan-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Gauge class="h-3 w-3 sm:h-4 sm:w-4 text-cyan-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-cyan-700">Water Level at Start</span>
                        </div>
                        <p class="text-base sm:text-lg font-bold text-cyan-800 mb-1">
                          {{ selectedNotification?.context?.environment?.waterLevel || selectedNotification?.context?.waterLevelAtStart || '--' }}%
                        </p>
                      </div>
                    </div>
                    
                    <!-- Zone/Area -->
                    <div class="bg-indigo-50 rounded-lg sm:rounded-xl border-2 border-indigo-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <MapPin class="h-3 w-3 sm:h-4 sm:w-4 text-indigo-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-indigo-700">Watering Zone</span>
                        </div>
                        <p class="text-base sm:text-lg font-bold text-indigo-800 mb-1">
                          {{ selectedNotification.context.zone || 'Greenhouse 1' }}
                        </p>
                      </div>
                    </div>
                    
                    <!-- Mode -->
                    <div class="bg-amber-50 rounded-lg sm:rounded-xl border-2 border-amber-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <Settings2 class="h-3 w-3 sm:h-4 sm:w-4 text-amber-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-amber-700">Mode</span>
                        </div>
                        <p class="text-base sm:text-lg font-bold text-amber-800 mb-1 capitalize">
                          {{ selectedNotification.context.mode || 'auto' }}
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Status Summary -->
                  <div class="bg-emerald-100 rounded-lg sm:rounded-xl border-2 border-emerald-300 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-3 w-3 sm:h-4 sm:w-4 text-emerald-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-emerald-700">Status Summary</span>
                      </div>
                      <p class="text-xs sm:text-sm text-emerald-800 font-medium leading-relaxed">
                        {{ selectedNotification.context.remarks || getWateringScheduleRemarks(selectedNotification) }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- 7. Weather Alert -->
                <div v-else-if="selectedNotification.context?.type === 'weather-alert'" class="space-y-3 sm:space-y-5">
                  <div class="text-xs sm:text-sm text-gray-600 bg-white/70 rounded-lg p-2 sm:p-3 border border-indigo-200">
                    Weather forecast for {{ selectedNotification.context.forecast?.date || formatFullDate(selectedNotification.time) }}.
                  </div>
                  
                  <!-- Weather Condition -->
                  <div class="bg-blue-100 rounded-lg sm:rounded-xl border-2 border-blue-300 shadow-sm">
                    <div class="p-3 sm:p-4 text-center">
                      <div class="flex items-center justify-center space-x-2 mb-3">
                        <CloudRain class="h-4 w-4 sm:h-5 sm:w-5 text-blue-600 flex-shrink-0" />
                        <span class="text-sm sm:text-base font-semibold text-blue-700">Weather Condition</span>
                      </div>
                      <div class="text-center mb-3">
                        <span class="text-3xl sm:text-5xl font-bold text-blue-800">
                          {{ selectedNotification.context.forecast?.condition || '--' }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Temperature Range -->
                  <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-4">
                    <!-- Min Temperature -->
                    <div class="bg-indigo-50 rounded-lg sm:rounded-xl border-2 border-indigo-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <ThermometerSnowflake class="h-3 w-3 sm:h-4 sm:w-4 text-indigo-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-indigo-700">Min Temperature</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-indigo-800 mb-1">
                          {{ selectedNotification.context.forecast?.temperatures?.min || '--' }}°C
                        </p>
                      </div>
                    </div>
                    
                    <!-- Max Temperature -->
                    <div class="bg-red-50 rounded-lg sm:rounded-xl border-2 border-red-200 shadow-sm">
                      <div class="p-3 sm:p-4">
                        <div class="flex items-center space-x-2 mb-2">
                          <ThermometerSun class="h-3 w-3 sm:h-4 sm:w-4 text-red-600 flex-shrink-0" />
                          <span class="text-xs sm:text-sm font-medium text-red-700">Max Temperature</span>
                        </div>
                        <p class="text-lg sm:text-xl font-bold text-red-800 mb-1">
                          {{ selectedNotification.context.forecast?.temperatures?.max || '--' }}°C
                        </p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Current Weather -->
                  <div class="bg-gray-50 rounded-lg sm:rounded-xl border-2 border-gray-200 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-3">
                        <Thermometer class="h-3 w-3 sm:h-4 sm:w-4 text-gray-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-gray-700">Current Weather</span>
                      </div>
                      <div class="grid grid-cols-2 sm:grid-cols-4 gap-2">
                        <div>
                          <p class="text-xs text-gray-500">Temperature</p>
                          <p class="text-sm font-bold text-gray-800">{{ selectedNotification.context.currentWeather?.temperature || '--' }}°C</p>
                        </div>
                        <div>
                          <p class="text-xs text-gray-500">Humidity</p>
                          <p class="text-sm font-bold text-gray-800">{{ selectedNotification.context.currentWeather?.humidity || '--' }}%</p>
                        </div>
                        <div>
                          <p class="text-xs text-gray-500">Wind Speed</p>
                          <p class="text-sm font-bold text-gray-800">{{ selectedNotification.context.currentWeather?.windSpeed || '--' }} km/h</p>
                        </div>
                        <div>
                          <p class="text-xs text-gray-500">Pressure</p>
                          <p class="text-sm font-bold text-gray-800">{{ selectedNotification.context.currentWeather?.pressure || '--' }} hPa</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Agricultural Recommendation -->
                  <div class="bg-emerald-100 rounded-lg sm:rounded-xl border-2 border-emerald-300 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-3 w-3 sm:h-4 sm:w-4 text-emerald-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-emerald-700">Agricultural Recommendation</span>
                      </div>
                      <p class="text-xs sm:text-sm text-emerald-800 font-medium leading-relaxed">
                        {{ selectedNotification.context.recommendation || getWeatherRecommendation(selectedNotification) }}
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Default/Unknown Notification Type -->
                <div v-else class="space-y-3 sm:space-y-5">
                  <div class="text-xs sm:text-sm text-gray-600 bg-white/70 rounded-lg p-2 sm:p-3 border border-indigo-200">
                    Notification details for {{ formatFullDate(selectedNotification.time) }}.
                  </div>
                  
                  <div class="bg-gray-50 rounded-lg sm:rounded-xl border-2 border-gray-200 shadow-sm">
                    <div class="p-3 sm:p-4">
                      <div class="flex items-center space-x-2 mb-2">
                        <Info class="h-3 w-3 sm:h-4 sm:w-4 text-gray-600 flex-shrink-0" />
                        <span class="text-xs sm:text-sm font-semibold text-gray-700">Notification Context</span>
                      </div>
                      <pre class="text-xs text-gray-700 overflow-auto p-2 bg-white rounded border border-gray-200 max-h-40">{{ JSON.stringify(selectedNotification.context, null, 2) }}</pre>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Notification Metadata -->
            <div class="bg-gray-50 rounded-xl sm:rounded-2xl border border-gray-200 p-3 sm:p-5">
              <h4 class="text-xs sm:text-sm font-semibold text-gray-700 mb-3 sm:mb-4 flex items-center">
                <div class="w-5 h-5 sm:w-6 sm:h-6 bg-gray-400 rounded-full flex items-center justify-center mr-2 sm:mr-3 flex-shrink-0">
                  <Database class="h-2.5 w-2.5 sm:h-3 sm:w-3 text-white" />
                </div>
                <span class="text-xs sm:text-sm">Notification Metadata</span>
              </h4>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 sm:gap-4">
                <div>
                  <p class="text-xs text-gray-500">Notification ID</p>
                  <p class="text-xs font-medium text-gray-800 break-all">{{ selectedNotification.notificationId || selectedNotification._id }}</p>
                </div>
                <div>
                  <p class="text-xs text-gray-500">Source</p>
                  <p class="text-xs font-medium text-gray-800">{{ selectedNotification.context?.source || 'System' }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal Footer -->
      <div class="px-3 sm:px-6 py-3 sm:py-4 border-t border-gray-100 bg-gray-50 flex flex-col sm:flex-row items-center justify-between gap-2">
        <div class="flex items-center space-x-2 text-xs text-gray-500">
          <Database class="h-3 w-3" />
          <span>{{ selectedNotification._id }}</span>
        </div>
        <div class="flex items-center space-x-2">
          <button 
            @click="selectedNotification.archived ? unarchiveCurrentNotification() : archiveCurrentNotification()" 
            class="px-3 sm:px-4 py-1.5 sm:py-2 text-xs sm:text-sm font-medium text-orange-700 bg-orange-100 hover:bg-orange-200 rounded-lg transition-colors flex items-center"
          >
            <Archive class="h-3 w-3 sm:h-4 sm:w-4 mr-1" />
            {{ selectedNotification.archived ? 'Unarchive' : 'Archive' }}
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Main Content - COMPLETELY MOBILE RESPONSIVE -->
  <div class="flex-1 w-full px-2 sm:px-4 md:px-6 lg:px-8 xl:px-10 2xl:px-12 overflow-hidden">
    <!-- Main Container - Mobile Responsive Design -->
     <div class="bg-white rounded-xl sm:rounded-2xl shadow-md border border-emerald-100 w-full h-[calc(100vh-80px)] sm:h-[calc(100vh-90px)] md:h-[calc(100vh-130px)] overflow-hidden">
      <!-- Content Wrapper -->
      <div class="flex flex-col h-full">
        <!-- Enhanced Header Section - MOBILE RESPONSIVE -->
        <div class="p-3 sm:p-4 md:p-5 border-b border-emerald-100 bg-gradient-to-r from-emerald-50 to-white">
          <!-- Header with improved mobile layout -->
          <div class="flex flex-col space-y-3 sm:space-y-4 md:space-y-5">
            <!-- Title and Icon - Mobile First -->
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2 sm:space-x-3">
                <div class="p-2 sm:p-2.5 bg-emerald-500 rounded-lg sm:rounded-xl shadow-sm">
                  <component :is="showArchived ? Archive : Bell" class="h-4 w-4 sm:h-5 sm:w-5 text-white" />
                </div>
                <div>
                  <h1 class="text-base sm:text-lg md:text-xl font-semibold text-gray-800">
                    {{ showArchived ? 'Archived Notifications' : 'Notifications' }}
                  </h1>
                  <p class="hidden sm:block text-xs sm:text-sm text-gray-500">
                    {{ showArchived ? 'View and manage your archived notifications' : 'Stay updated with your latest alerts and updates' }}
                  </p>
                </div>
              </div>
              
              <!-- Back Button - Always visible on mobile -->
              <button 
                @click="goBack"
                class="flex items-center px-2 sm:px-3 md:px-4 py-2 bg-gray-100 text-gray-700 rounded-lg text-xs sm:text-sm font-medium transition-colors"
              >
                <ArrowLeft class="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-1.5" />
                <span class="hidden sm:block">Back</span>
              </button>
            </div>
            
            <!-- Action Buttons - Mobile Responsive Layout -->
            <div class="flex flex-wrap items-center gap-2 overflow-x-auto pb-1">
              <!-- Select Button -->
              <button 
                @click="toggleSelectMode"
                :disabled="isLoading"
                class="flex items-center px-2 sm:px-3 md:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                :class="isSelectMode 
                  ? 'bg-red-500 text-white' 
                  : 'bg-gray-100 text-gray-700'"
              >
                <Check class="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-1.5" />
                <span class="hidden md:block">{{ isSelectMode ? 'Cancel' : 'Select' }}</span>
              </button>

              <!-- Delete Selected Button -->
              <button 
                v-if="isSelectMode && selectedNotifications.size > 0"
                @click="deleteSelectedNotifications"
                :disabled="isLoading"
                class="flex items-center px-2 sm:px-3 md:px-4 py-2 bg-red-500 text-white rounded-lg text-xs sm:text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                <Trash2 class="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-1.5" />
                <span class="hidden md:block">Delete ({{ selectedNotifications.size }})</span>
                <span class="block md:hidden">({{ selectedNotifications.size }})</span>
              </button>

              <!-- Archive Toggle Button -->
              <button 
                @click="toggleArchiveView"
                :disabled="isLoading"
                class="flex items-center px-2 sm:px-3 md:px-4 py-2 rounded-lg text-xs sm:text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
                :class="showArchived 
                  ? 'bg-orange-500 text-white' 
                  : 'bg-gray-100 text-gray-700'"
              >
                <component :is="showArchived ? Bell : Archive" class="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-1.5" />
                <span class="hidden md:block">{{ showArchived ? 'Active' : 'Archived' }}</span>
              </button>
              
              <button 
                v-if="!showArchived"
                @click="markAllAsRead"
                :disabled="isLoading"
                class="flex items-center px-2 sm:px-3 md:px-4 py-2 bg-emerald-500 text-white rounded-lg text-xs sm:text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                <Check class="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-1.5" />
                <span class="hidden md:block">Mark All</span>
              </button>

              <button 
                v-if="!showArchived && !isSelectMode"
                @click="confirmDeleteAll"
                :disabled="isLoading || currentNotifications.length === 0"
                class="flex items-center px-2 sm:px-3 md:px-4 py-2 bg-red-500 text-white rounded-lg text-xs sm:text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap"
              >
                <Trash2 class="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-1.5" />
                <span class="hidden md:block">Delete All</span>
              </button>
            </div>

            <!-- Enhanced Filters and Search - Mobile Responsive -->
            <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-3 sm:gap-4">
              <!-- Filter Buttons - Mobile optimized scrollable -->
              <div class="flex items-center justify-start gap-1 sm:gap-2 overflow-x-auto scrollbar-hide min-w-0 pb-1">
                <div class="flex items-center gap-1 sm:gap-2 flex-nowrap">
                  <button 
                    v-for="filter in (showArchived ? archivedFilters : filters)" 
                    :key="filter.value"
                    @click="activeFilter = filter.value"
                    :disabled="isLoading"
                    :class="[
                      'px-2 sm:px-3 py-1.5 text-xs sm:text-sm font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed whitespace-nowrap flex-shrink-0',
                      activeFilter === filter.value 
                        ? 'bg-emerald-500 text-white shadow-sm' 
                        : 'bg-white text-gray-700 border border-gray-200'
                    ]"
                  >
                    {{ filter.label }}
                  </button>
                </div>
              </div>
              
              <!-- Search Bar - Mobile responsive -->
              <div class="relative w-full sm:w-80 md:w-72 lg:w-64 xl:w-80 max-w-sm flex-shrink-0">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <Search class="h-3 w-3 sm:h-4 sm:w-4 text-gray-400" />
                </div>
                <input 
                  type="text"
                  v-model="searchQuery"
                  :disabled="isLoading"
                  :placeholder="showArchived ? 'Search archived...' : 'Search notifications...'"
                  class="w-full pl-8 sm:pl-10 pr-4 py-2 text-xs sm:text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- Scrollable Notifications Content - Mobile Responsive -->
        <div class="flex-1 overflow-y-auto notification-scroll">
          <!-- Empty State -->
          <div v-if="!isLoading && filteredNotifications.length === 0" class="py-12 sm:py-16 flex flex-col items-center justify-center px-4">
            <div class="bg-gray-100 p-3 sm:p-4 rounded-full mb-4">
              <component :is="showArchived ? Archive : BellOff" class="h-6 w-6 sm:h-8 sm:w-8 text-gray-400" />
            </div>
            <h3 class="text-base sm:text-lg font-medium text-gray-900 mb-1">
              {{ showArchived ? 'No archived notifications' : 'No notifications' }}
            </h3>
            <p class="text-xs sm:text-sm text-gray-500 text-center max-w-sm">
              {{ searchQuery 
                ? 'No results found for your search.' 
                : showArchived 
                  ? 'You don\'t have any archived notifications yet.' 
                  : 'You don\'t have any notifications yet.' 
              }}
            </p>
          </div>

          <!-- Notifications - Mobile Responsive Design -->
          <div v-else-if="!isLoading">
            <!-- Group notifications by date -->
            <div v-for="group in paginatedGroups" :key="group.name" class="px-3 sm:px-4 md:px-5 py-3 sm:py-4">
              <div class="flex items-center mb-2 sm:mb-3 px-2 sm:px-3 py-2 rounded-lg" 
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
                  class="h-3 w-3 sm:h-4 sm:w-4 mr-2"
                  :class="{
                    'text-emerald-600': group.name === 'Today',
                    'text-orange-600': group.name === 'Yesterday',
                    'text-blue-600': group.name === 'A few days ago',
                    'text-purple-600': group.name === 'A week ago',
                    'text-indigo-600': group.name === 'A few weeks ago',
                    'text-gray-600': group.name === 'A month ago'
                  }" 
                />
                <span class="text-xs sm:text-sm font-medium"
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
              
              <div class="space-y-2 sm:space-y-2.5">
                <div 
                  v-for="notification in group.notifications" 
                  :key="notification.id"
                  @click="handleNotificationClick($event, notification)"
                  class="group p-3 sm:p-3 rounded-lg sm:rounded-xl border border-gray-100 bg-white transition-all duration-200 cursor-pointer"
                  :class="{ 
                    'bg-blue-50/30 border-blue-200': !notification.read && !showArchived,
                    'bg-orange-50/30 border-orange-200': showArchived,
                    'ring-2 ring-emerald-500': isSelectMode && selectedNotifications.has(notification.id)
                  }"
                >
                  <div class="flex items-start gap-2 sm:gap-3">
                    <!-- Checkbox for select mode -->
                    <div v-if="isSelectMode" class="flex-shrink-0 mt-1" @click.stop>
                        <input 
                          type="checkbox" 
                          :checked="selectedNotifications.has(notification.id)"
                          @click.stop="toggleNotificationSelection(notification.id)"
                          class="h-3 w-3 sm:h-4 sm:w-4 text-emerald-600 rounded border-gray-300 focus:ring-emerald-500"
                          :id="'notif-checkbox-' + notification.id"
                        >
                        <label :for="'notif-checkbox-' + notification.id" class="sr-only">
                          Select notification
                        </label>
                    </div>
                    
                    <div 
                      class="flex-shrink-0 w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center shadow-sm"
                      :class="getNotificationIcon(notification).bgColor"
                    >
                      <component 
                        :is="getNotificationIcon(notification).icon" 
                        class="h-3 w-3 sm:h-4 sm:w-4 text-white" 
                      />
                    </div>
                    <div class="flex-1 min-w-0">
                      <div class="flex items-start justify-between mb-1">
                        <h3 class="text-xs sm:text-sm font-medium text-gray-900 line-clamp-1 pr-2">{{ notification.title }}</h3>
                        <span class="text-xs text-gray-500 whitespace-nowrap bg-gray-50 px-1.5 py-0.5 rounded flex-shrink-0"> {{ formatTimeForDisplay(notification.time) }}</span>
                      </div>
                      <p class="text-xs sm:text-sm text-gray-600 mb-2 line-clamp-2 font-medium">
                        {{ notification.message }}
                      </p>
                      
                      <!-- Mobile optimized action buttons -->
                      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                        <div class="flex items-center flex-wrap gap-1 sm:gap-2">
                          <span 
                            class="inline-flex items-center px-1.5 sm:px-2 py-0.5 rounded-md text-xs font-medium"
                            :class="getNotificationIcon(notification).badgeColor"
                          >
                            {{ notification.category || notification.type }}
                          </span>
                          <div v-if="!notification.read && !showArchived" class="flex items-center text-blue-600 text-xs font-medium">
                            <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                            Unread
                          </div>
                        </div>
                        
                        <!-- Action buttons - Mobile responsive -->
                        <div class="flex items-center gap-1 sm:gap-2">
                          <button 
                            v-if="showArchived"
                            @click.stop="handleQuickUnarchive(notification.id)"
                            :disabled="unarchivingIds.has(notification.id)"
                            class="flex items-center text-orange-600 text-xs font-medium bg-orange-50 px-2 py-1 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                          >
                            <component 
                              :is="unarchivingIds.has(notification.id) ? 'div' : Archive" 
                              :class="unarchivingIds.has(notification.id) ? 'animate-spin h-3 w-3 mr-1 border border-orange-600 border-t-transparent rounded-full' : 'h-3 w-3 mr-1'"
                            />
                            <span class="hidden sm:block">{{ unarchivingIds.has(notification.id) ? 'Unarchiving...' : 'Archived' }}</span>
                          </button>
                          <!-- Green See Details Button -->
                          <button 
                            @click.stop="handleSeeDetails(notification)"
                            class="flex items-center px-2 py-1 text-xs font-medium text-emerald-600 bg-emerald-50 rounded-md transition-colors"
                          >
                            <Eye class="h-3 w-3 mr-1" />
                            <span class=" sm:block">Details</span>
                          </button>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Hover action buttons - Hidden on mobile, shown on hover for larger screens -->
                    <div class="hidden sm:flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
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
                        @click.stop="archiveNotificationAndClose(notification.id)"
                        class="p-1.5 text-gray-400 rounded-lg transition-colors"
                        title="Archive"
                      >
                        <Archive class="h-4 w-4" />
                      </button>
                      <button 
                        v-if="showArchived"
                        @click.stop="unarchiveNotificationAndClose(notification.id)"
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
            <div v-if="paginatedGroups.length === 0 && filteredNotifications.length > 0" class="px-3 sm:px-5 py-8 sm:py-12 text-center">
              <Bell class="h-8 w-8 sm:h-10 sm:w-10 text-gray-300 mx-auto mb-3" />
              <p class="text-sm sm:text-base text-gray-500 mb-2">No notifications on this page</p>
              <button 
                @click="currentPage = 1"
                class="text-xs sm:text-sm text-emerald-600 font-medium"
              >
                Go to first page
              </button>
            </div>
          </div>
        </div>

        <!-- Enhanced Pagination Footer - Mobile Responsive -->
        <div class="border-t border-gray-200 py-2 sm:py-3 px-3 sm:px-4 bg-gray-50">
          <div class="flex flex-col-reverse md:flex-row sm:flex-row items-center justify-between gap-2 sm:gap-4">
            <!-- Items per page selector - Mobile: moved to top, Desktop: left side -->
            <div class="flex sm:hidden items-center order-1 w-full justify-center">
              <span class="text-xs text-gray-600 mr-2">Show</span>
              <select 
                v-model="itemsPerPage" 
                @change="handleItemsPerPageChange"
                :disabled="isLoading"
                class="bg-white border border-gray-200 text-gray-700 rounded px-2 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
              <span class="text-xs text-gray-600 ml-2">per page</span>
            </div>
            
            <!-- Desktop items per page selector -->
            <div class="hidden sm:flex items-center">
              <span class="text-xs text-gray-600 mr-2">Show</span>
              <select 
                v-model="itemsPerPage" 
                @change="handleItemsPerPageChange"
                :disabled="isLoading"
                class="bg-white border border-gray-200 text-gray-700 rounded px-1.5 py-1 text-xs focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
                  {{ option }}
                </option>
              </select>
              <span class="text-xs text-gray-600 ml-2">per page</span>
            </div>
            
            <div class="flex flex-row items-center">
              <!-- Results info - Mobile: order-2, Desktop: center -->
              <div class="text-xs text-gray-600 order-2 sm:order-none">
                Showing {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, filteredNotifications.length) }}
                of {{ filteredNotifications.length }}
              </div>
              
              <!-- Pagination controls - Mobile: order-3, Desktop: right -->
              <div class="flex items-center gap-1 order-3 sm:order-none">
                <button 
                  @click="prevPage"
                  :disabled="currentPage === 1 || isLoading"
                  class="p-1.5 text-gray-700 hover:text-emerald-600 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <ChevronLeft class="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                </button>
                
                <div class="flex items-center gap-0.5">
                  <button
                    v-for="page in paginationNumbers"
                    :key="page"
                    @click="goToPage(page)"
                    :disabled="page === '...' || isLoading"
                    :class="[
                      'px-1.5 sm:px-2 py-1 text-xs rounded min-w-[20px] sm:min-w-[24px] transition-colors',
                      page === currentPage 
                        ? 'bg-emerald-500 text-white font-medium' 
                        : page === '...' 
                          ? 'text-gray-400 cursor-default' 
                          : 'text-gray-700 hover:text-emerald-600 hover:bg-gray-100'
                    ]"
                  >
                    {{ page }}
                  </button>
                </div>
                
                <button 
                  @click="nextPage"
                  :disabled="currentPage >= totalPages || totalPages === 0 || isLoading"
                  class="p-1.5 text-gray-700 hover:text-emerald-600 rounded disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <ChevronRight class="w-3 h-3 sm:w-3.5 sm:h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Delete All Confirmation Modal - Mobile Responsive -->
  <div v-if="showDeleteAllConfirmation" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-xl sm:rounded-2xl shadow-2xl max-w-md w-full p-4 sm:p-6">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-base sm:text-lg font-semibold text-gray-800">Confirm Delete All</h3>
        <button @click="showDeleteAllConfirmation = false" class="text-gray-400 p-1">
          <X class="w-4 h-4 sm:w-5 sm:h-5" />
        </button>
      </div>
      <p class="text-sm sm:text-base text-gray-600 mb-6">Are you sure you want to delete all {{ showArchived ? 'archived' : '' }} notifications? This action cannot be undone.</p>
      <div class="flex flex-col sm:flex-row justify-end gap-2 sm:gap-3">
        <button 
          @click="showDeleteAllConfirmation = false"
          class="px-4 py-2 bg-white text-gray-700 rounded-lg text-xs sm:text-sm font-medium transition-colors border border-gray-200"
        >
          Cancel
        </button>
        <button 
          @click="deleteAllNotifications"
          :disabled="isDeletingAll"
          class="flex items-center justify-center px-4 py-2 bg-red-500 text-white rounded-lg text-xs sm:text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Trash2 class="h-3 w-3 sm:h-4 sm:w-4 mr-1.5" />
          {{ isDeletingAll ? 'Deleting...' : 'Delete All' }}
        </button>
      </div>
    </div>
  </div>

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
import { getCurrentInstance } from 'vue'
import { getWeatherData, mapWeatherCode } from '../../utils/weather.js';
import api from '../../api/index'

const isLoading = ref(true)
const loadingDotIndex = ref(0)
let loadingInterval = null
const unarchivingIds = ref(new Set())

const selectedNotifications = ref(new Set());
const selectedNotification = ref(null);
const showDetailsModal = ref(false);
const isSelectMode = ref(false);
const showDeleteAllConfirmation = ref(false)
const isDeletingAll = ref(false)
const notifications = ref([])
const archivedNotifications = ref([])
const isArchiving = ref(false);
const isUnarchiving = ref(false);

const showArchived = ref(false)

const filters = [
  { label: 'All', value: 'all' },
  { label: 'Unread', value: 'unread' },
  { label: 'System', value: 'system' },
  { label: 'Alerts', value: 'alert' },
  { label: 'Data', value: 'data' }
]

const archivedFilters = [
  { label: 'All', value: 'all' },
  { label: 'System', value: 'system' },
  { label: 'Alerts', value: 'alert' },
  { label: 'Data', value: 'data' }
]

const activeFilter = ref('all')
const searchQuery = ref('')
const currentPage = ref(1)

const itemsPerPageOptions = [4, 10, 15, 20, 25, 30]
const itemsPerPage = ref(4) 

const currentNotifications = computed(() => {
  return showArchived.value ? archivedNotifications.value : notifications.value;
});

const paginationNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 1) return [1]
  
  if (total <= 5) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  
  if (current === 1) {
    return [1, '...', total]
  } else if (current === total) {
    return [1, '...', total - 1, total]
  } else if (current === 2) {
    return [1, 2, '...', total]
  } else if (current === total - 1) {
    return [ total - 2, total - 1, total]
  } else {
    return [ current - 1, current, current + 1, '...', total]
  }
})

const toastType = ref('info') 
const weatherModalData = ref(null);

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
  currentPage.value = 1 
  saveUserPreferences() 
}

const filteredNotifications = computed(() => {
  let result = [...currentNotifications.value];
  
  if (activeFilter.value === 'unread' && !showArchived.value) {
    result = result.filter(n => !n.read);
  } else if (activeFilter.value === 'system') {
    result = result.filter(n => n.type === 'system');
  } else if (activeFilter.value === 'alert') {
    result = result.filter(n => ['warning', 'critical'].includes(n.severity));
  } else if (activeFilter.value === 'data') {
    result = result.filter(n => n.type === 'data');
  }

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(n =>
      n.title?.toLowerCase().includes(query) ||
      n.message?.toLowerCase().includes(query)
    );
  }

  return result;
});

const todayNotifications = computed(() =>
  filteredNotifications.value.filter(n => isToday(n.time))
);

const yesterdayNotifications = computed(() =>
  filteredNotifications.value.filter(n => isYesterday(n.time))
);

const fewDaysAgoNotifications = computed(() =>
  filteredNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time);
    return daysAgo >= 2 && daysAgo <= 6;
  })
);

const weekAgoNotifications = computed(() =>
  filteredNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time);
    return daysAgo >= 7 && daysAgo <= 13;
  })
);

const fewWeeksAgoNotifications = computed(() =>
  filteredNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time);
    return daysAgo >= 14 && daysAgo <= 29;
  })
);

const monthAgoNotifications = computed(() =>
  filteredNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time);
    return daysAgo >= 30;
  })
);

const getDayName = (dayIndex) => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
  return days[dayIndex] || 'Unknown day';
};

const paginatedGroups = computed(() => {
  const allGroups = [
    { name: 'Today', notifications: todayNotifications.value },
    { name: 'Yesterday', notifications: yesterdayNotifications.value },
    { name: 'A few days ago', notifications: fewDaysAgoNotifications.value },
    { name: 'A week ago', notifications: weekAgoNotifications.value },
    { name: 'A few weeks ago', notifications: fewWeeksAgoNotifications.value },
    { name: 'A month ago', notifications: monthAgoNotifications.value }
  ].filter(group => group.notifications.length > 0)

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

const totalPages = computed(() => {
  const totalItems = filteredNotifications.value.length
  return Math.ceil(totalItems / itemsPerPage.value) || 1
})

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

const displayedPages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const pages = []

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    pages.push(1)

    if (current <= 3) {
      pages.push(2, 3, 4, 5, '...', total)
    } else if (current >= total - 2) {
      pages.push('...', total - 3, total - 2, total - 1, total)
    } else {
      pages.push('...', current - 1, current, current + 1, '...', total)
    }
  }

  return pages
})

const ensureDate = (dateValue) => {
  if (!dateValue) return new Date();
  
  if (dateValue instanceof Date) {
    return dateValue;
  }
  
  if (typeof dateValue === 'string' || typeof dateValue === 'number') {
    return new Date(dateValue);
  }
  
  if (typeof dateValue === 'object' && dateValue._seconds) {
    return new Date(dateValue._seconds * 1000 + (dateValue._nanoseconds || 0) / 1000000);
  }
  
  return new Date();
};

const isSameDay = (dateA, dateB) => {
  const validDateA = ensureDate(dateA);
  const validDateB = ensureDate(dateB);
  
  return (
    validDateA.getFullYear() === validDateB.getFullYear() &&
    validDateA.getMonth() === validDateB.getMonth() &&
    validDateA.getDate() === validDateB.getDate()
  );
};

const isToday = (date) => {
  if (!date) return false;
  const today = new Date();
  return isSameDay(date, today);
};

const isYesterday = (date) => {
  if (!date) return false;
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  return isSameDay(date, yesterday);
};

const getDaysAgo = (date) => {
  if (!date) return 0;
  const validDate = ensureDate(date);
  const now = new Date();
  const diffTime = Math.abs(now - validDate);
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
};

const handleNotificationClick = (event, notification) => {
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

const deleteSelectedNotifications = async () => {
  if (selectedNotifications.value.size === 0) return;

  try {
    isLoading.value = true;
    
    const selectedIds = Array.from(selectedNotifications.value);
    
    await api.post('/notifications/delete-multiple', { ids: selectedIds });
    
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

const openDetailsModal = (notification) => {
  selectedNotification.value = notification
  showDetailsModal.value = true
}

const handleSeeDetails = async (notification) => {
  try {
    if (!notification.read && !showArchived.value) {
      await markAsRead(notification.id);
    }
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

const toggleArchiveView = () => {
  showArchived.value = !showArchived.value
  activeFilter.value = 'all' 
  currentPage.value = 1 
}

const isLowSoilMoistureNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  return title.includes('low soil moisture') || message.includes('low soil moisture') || 
         title.includes('dry soil') || message.includes('dry soil')
}

const isLowSoilNutrientNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  return title.includes('low soil nutrient') || title.includes('soil nutrient alert') || 
         title.includes('nutrient deficiency') || title.includes('soil alert')
}

const isSingleParameterAlert = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  return title.includes('humidity alert') || title.includes('temperature alert') || 
         title.includes('potassium alert') || title.includes('nitrogen alert') ||
         title.includes('phosphorus alert') || title.includes('soil ph alert') ||
         title.includes('ph alert')
}

const getParameterName = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  if (title.includes('humidity')) return 'Humidity'
  if (title.includes('temperature')) return 'Temperature'
  if (title.includes('potassium')) return 'Potassium'
  if (title.includes('nitrogen')) return 'Nitrogen'
  if (title.includes('phosphorus')) return 'Phosphorus'
  if (title.includes('soil ph') || title.includes('ph')) return 'Soil pH'
  return 'Parameter'
}

const getParameterValue = (notification) => {
  const param = getParameterName(notification).toLowerCase()
  if (param.includes('humidity')) return notification.context.humidity
  if (param.includes('temperature')) return notification.context.temperature
  if (param.includes('potassium')) return notification.context.potassium
  if (param.includes('nitrogen')) return notification.context.nitrogen
  if (param.includes('phosphorus')) return notification.context.phosphorus
  if (param.includes('ph')) return notification.context.soilPh
  return null
}

const getParameterUnit = (notification) => {
  const param = getParameterName(notification).toLowerCase()
  if (param.includes('humidity')) return '%'
  if (param.includes('temperature')) return '°C'
  if (param.includes('potassium') || param.includes('nitrogen') || param.includes('phosphorus')) return ' ppm'
  if (param.includes('ph')) return ''
  return ''
}

const getParameterAlertClass = (notification) => {
  const param = getParameterName(notification).toLowerCase()
  
  if (param.includes('humidity')) {
    return {
      bg: 'bg-blue-100 rounded-lg sm:rounded-xl border-2 border-blue-300 shadow-sm',
      icon: Droplet,
      iconColor: 'text-blue-600',
      text: 'text-blue-700',
      valueColor: 'text-blue-800'
    }
  }
  if (param.includes('temperature')) {
    return {
      bg: 'bg-red-100 rounded-lg sm:rounded-xl border-2 border-red-300 shadow-sm',
      icon: Thermometer,
      iconColor: 'text-red-600',
      text: 'text-red-700',
      valueColor: 'text-red-800'
    }
  }
  if (param.includes('potassium')) {
    return {
      bg: 'bg-yellow-100 rounded-lg sm:rounded-xl border-2 border-yellow-300 shadow-sm',
      icon: Activity,
      iconColor: 'text-yellow-600',
      text: 'text-yellow-700',
      valueColor: 'text-yellow-800'
    }
  }
  if (param.includes('nitrogen')) {
    return {
      bg: 'bg-green-100 rounded-lg sm:rounded-xl border-2 border-green-300 shadow-sm',
      icon: Leaf,
      iconColor: 'text-green-600',
      text: 'text-green-700',
      valueColor: 'text-green-800'
    }
  }
  if (param.includes('phosphorus')) {
    return {
      bg: 'bg-orange-100 rounded-lg sm:rounded-xl border-2 border-orange-300 shadow-sm',
      icon: Sprout,
      iconColor: 'text-orange-600',
      text: 'text-orange-700',
      valueColor: 'text-orange-800'
    }
  }
  if (param.includes('ph')) {
    return {
      bg: 'bg-purple-100 rounded-lg sm:rounded-xl border-2 border-purple-300 shadow-sm',
      icon: Gauge,
      iconColor: 'text-purple-600',
      text: 'text-purple-700',
      valueColor: 'text-purple-800'
    }
  }
  
  return {
    bg: 'bg-gray-100 rounded-lg sm:rounded-xl border-2 border-gray-300 shadow-sm',
    icon: Info,
    iconColor: 'text-gray-600',
    text: 'text-gray-700',
    valueColor: 'text-gray-800'
  }
}

const getParameterAlertDescription = (notification) => {
  const param = getParameterName(notification)
  return `${param} status update`
}

const getParameterStatusDescription = (notification) => {
  const param = getParameterName(notification).toLowerCase()
  const value = parseFloat(getFormattedValue(getParameterValue(notification)))
  
  if (param.includes('humidity')) {
    if (value >= 80) return 'Very High Humidity'
    if (value >= 60) return 'High Humidity'
    if (value >= 40) return 'Normal Humidity'
    return 'Low Humidity'
  }
  if (param.includes('temperature')) {
    if (value >= 30) return 'High Temperature'
    if (value >= 20) return 'Optimal Temperature'
    if (value >= 10) return 'Low Temperature'
    return 'Very Low Temperature'
  }
  if (param.includes('potassium')) {
    if (value >= 250) return 'High Potassium'
    if (value >= 150) return 'Optimal Potassium'
    if (value >= 100) return 'Low Potassium'
    return 'Very Low Potassium'
  }
  if (param.includes('nitrogen')) {
    if (value >= 200) return 'High Nitrogen'
    if (value >= 100) return 'Optimal Nitrogen'
    if (value >= 50) return 'Low Nitrogen'
    return 'Very Low Nitrogen'
  }
  if (param.includes('phosphorus')) {
    if (value >= 60) return 'High Phosphorus'
    if (value >= 40) return 'Optimal Phosphorus'
    if (value >= 20) return 'Low Phosphorus'
    return 'Very Low Phosphorus'
  }
  if (param.includes('ph')) {
    if (value >= 7.5) return 'Alkaline Soil'
    if (value >= 6.5) return 'Neutral Soil'
    if (value >= 5.5) return 'Slightly Acidic'
    return 'Acidic Soil'
  }
  
  return 'Parameter Status'
}

const getParameterImpact = (notification) => {
  const param = getParameterName(notification).toLowerCase()
  const value = parseFloat(getFormattedValue(getParameterValue(notification)))
  
  if (param.includes('humidity')) {
    if (value >= 80) return 'High humidity increases fungal disease risk and can reduce pollination effectiveness.'
    if (value >= 60) return 'Moderate humidity supports good plant growth but monitor for potential disease development.'
    if (value >= 40) return 'Optimal humidity levels for most crops, promoting healthy growth and development.'
    return 'Low humidity can cause plant stress, reduced growth, and increased water requirements.'
  }
  if (param.includes('temperature')) {
    if (value >= 30) return 'High temperatures can cause heat stress, reduced photosynthesis, and flower abortion.'
    if (value >= 20) return 'Optimal temperature range for most crops, supporting healthy growth and development.'
    if (value >= 10) return 'Cool temperatures may slow plant growth and development rates.'
    return 'Very low temperatures can damage plant tissues and halt growth completely.'
  }
  if (param.includes('potassium')) {
    if (value >= 250) return 'Excess potassium can interfere with magnesium and calcium uptake.'
    if (value >= 150) return 'Adequate potassium supports disease resistance, water regulation, and fruit quality.'
    if (value >= 100) return 'Low potassium may reduce plant vigor and stress tolerance.'
    return 'Potassium deficiency severely impacts fruit quality, disease resistance, and overall plant health.'
  }
  if (param.includes('nitrogen')) {
    if (value >= 200) return 'Excess nitrogen promotes vegetative growth at expense of fruiting and can delay maturity.'
    if (value >= 100) return 'Optimal nitrogen levels support healthy leaf development and protein synthesis.'
    if (value >= 50) return 'Nitrogen deficiency results in stunted growth and yellowing of older leaves.'
    return 'Severe nitrogen deficiency causes complete growth arrest and significant yield reduction.'
  }
  if (param.includes('phosphorus')) {
    if (value >= 60) return 'Excess phosphorus can inhibit micronutrient uptake, particularly zinc and iron.'
    if (value >= 40) return 'Adequate phosphorus supports root development, flowering, and energy transfer.'
    if (value >= 20) return 'Phosphorus deficiency results in poor root development and purplish leaf discoloration.'
    return 'Severe phosphorus deficiency severely limits plant growth and reproductive development.'
  }
  if (param.includes('ph')) {
    if (value >= 7.5) return 'Alkaline soil conditions can limit availability of iron, manganese, and phosphorus.'
    if (value >= 6.5) return 'Neutral pH provides optimal nutrient availability for most crops.'
    if (value >= 5.5) return 'Slightly acidic conditions are suitable for many crops but may limit some nutrients.'
    return 'Acidic soil conditions can increase aluminum toxicity and limit phosphorus and calcium availability.'
  }
  
  return 'This parameter affects crop growth and development in various ways depending on its level.'
}

const getParameterRecommendation = (notification) => {
  const param = getParameterName(notification).toLowerCase()
  const value = parseFloat(getFormattedValue(getParameterValue(notification)))
  
  if (param.includes('humidity')) {
    if (value >= 80) return 'Improve ventilation, space plants appropriately, and consider fungicide applications to prevent disease.'
    if (value >= 60) return 'Monitor for disease symptoms and ensure good air circulation around plants.'
    if (value >= 40) return 'Maintain current practices as humidity levels are optimal for crop growth.'
    return 'Increase irrigation frequency, use mulch to conserve soil moisture, and consider shade structures.'
  }
  if (param.includes('temperature')) {
    if (value >= 30) return 'Provide shade, increase irrigation frequency, and consider misting systems for cooling.'
    if (value >= 20) return 'Maintain current practices as temperatures are in the optimal range for growth.'
    if (value >= 10) return 'Use row covers or cold frames to protect plants and extend the growing season.'
    return 'Implement frost protection measures and consider moving sensitive plants to protected areas.'
  }
  
  return 'Monitor this parameter regularly and adjust management practices based on crop requirements.'
}

const getSoilMoistureRecommendation = (notification) => {
  const moisture = parseFloat(getFormattedValue(notification.context.soilMoisture))
  
  if (moisture < 20) return 'Critical soil moisture level. Immediate irrigation required. Auto irrigation system activated.'
  if (moisture < 30) return 'Low soil moisture. Schedule irrigation soon. Monitor plant water stress indicators.'
  if (moisture < 40) return 'Moderate soil moisture. Maintain regular irrigation schedule.'
  if (moisture < 60) return 'Adequate soil moisture for most crops. Continue normal irrigation practices.'
  return 'Sufficient soil moisture. No additional irrigation needed at this time.'
}

const getSoilNutrientRecommendation = (notification) => {
  const recommendations = []
  const context = notification.context || {}
  
  const nitrogen = parseFloat(getFormattedValue(context.nitrogen))
  if (nitrogen < 50) recommendations.push('Apply nitrogen fertilizer to address deficiency')
  else if (nitrogen > 200) recommendations.push('Reduce nitrogen application to prevent excessive vegetative growth')
  
  const phosphorus = parseFloat(getFormattedValue(context.phosphorus))
  if (phosphorus < 20) recommendations.push('Apply phosphorus fertilizer to support root development')
  else if (phosphorus > 60) recommendations.push('Monitor for micronutrient deficiencies due to high phosphorus')
  
  const potassium = parseFloat(getFormattedValue(context.potassium))
  if (potassium < 100) recommendations.push('Apply potassium fertilizer to improve stress tolerance')
  else if (potassium > 250) recommendations.push('High potassium levels may affect magnesium availability')
  
  const ph = parseFloat(getFormattedValue(context.soilPh))
  if (ph < 5.5) recommendations.push('Apply lime to raise soil pH and improve nutrient availability')
  else if (ph > 7.5) recommendations.push('Apply sulfur or acidifying fertilizers to lower soil pH')
  
  if (recommendations.length === 0) {
    return 'Soil nutrient levels are within optimal ranges. Continue regular monitoring and maintenance fertilization.'
  }
  
  return recommendations.join('. ') + '.'
}

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
    sessions = Math.floor(12 + Math.random() * 6) 
    coverage = '500-800 m²'
  } else if (waterLevel >= 60) {
    sessions = Math.floor(8 + Math.random() * 4) 
    coverage = '300-500 m²'
  } else if (waterLevel >= 40) {
    sessions = Math.floor(4 + Math.random() * 4) 
    coverage = '150-300 m²'
  } else if (waterLevel >= 20) {
    sessions = Math.floor(2 + Math.random() * 2) 
    coverage = '50-150 m²'
  } else {
    sessions = Math.floor(1 + Math.random()) 
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

const isTempHumidityNotification = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  
  return (title.includes('temperature') || title.includes('humidity') || 
          message.includes('temperature') || message.includes('humidity')) &&
         !isWeatherNotification(notification) 
}
const getFormattedValue = (value) => {
  if (!value) return null
  if (typeof value === 'number') return value.toFixed(1)
  
  const numericMatch = value.toString().match(/(\d+\.?\d*)/)
  return numericMatch ? parseFloat(numericMatch[1]).toFixed(1) : null
}

const getTempHumidityRecommendation = (notification) => {
  const context = notification.context || {}
  
  const humidity = parseFloat(getFormattedValue(context.humidity))
  const temperature = parseFloat(getFormattedValue(context.temperature))
  const soilMoisture = parseFloat(getFormattedValue(context.soilMoisture))
  
  let recommendations = []
  
  if (humidity >= 80) {
    recommendations.push('High humidity – fungal disease risk')
  } else if (humidity >= 60) {
    recommendations.push('Moderate humidity – good growing conditions')
  } else if (humidity >= 40) {
    recommendations.push('Normal humidity levels')
  } else {
    recommendations.push('Low humidity – increase irrigation frequency')
  }
  
  if (temperature >= 30) {
    recommendations.push('High temperature – provide shade protection')
  } else if (temperature >= 25) {
    recommendations.push('Warm temperature – optimal for growth')
  } else if (temperature >= 18) {
    recommendations.push('Moderate temperature – normal conditions')
  } else {
    recommendations.push('Cool temperature – protect sensitive plants')
  }
  
  if (soilMoisture) {
    if (soilMoisture < 20) {
      recommendations.push('Low soil moisture – irrigation needed')
    } else if (soilMoisture > 70) {
      recommendations.push('High soil moisture – improve drainage')
    }
  }
  
  return recommendations.join(' • ')
}

const getNitrogenLevel = (value) => {
  if (!value) return '--'
  if (value < 50) return 'Low'
  if (value < 100) return 'Moderate'
  if (value <= 200) return 'Adequate'
  if (value <= 300) return 'High'
  return 'Excessive'
}

const getPhosphorusLevel = (value) => {
  if (!value) return '--'
  if (value < 20) return 'Low'
  if (value < 40) return 'Moderate'
  if (value <= 60) return 'Adequate'
  if (value <= 100) return 'High'
  return 'Excessive'
}

const getPotassiumLevel = (value) => {
  if (!value) return '--'
  if (value < 100) return 'Low'
  if (value < 150) return 'Moderate'
  if (value <= 250) return 'Adequate'
  if (value <= 350) return 'High'
  return 'Excessive'
}

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

const getSensorValue = (notification, parameter) => {
  if (!notification.context) return null
  
  if (notification.context[parameter] !== undefined) {
    return notification.context[parameter]
  }
  
  if (notification.context.sensor1 && notification.context.sensor1[parameter] !== undefined) {
    return notification.context.sensor1[parameter]
  }
  
  if (notification.context.sensor2 && notification.context.sensor2[parameter] !== undefined) {
    return notification.context.sensor2[parameter]
  }
  
  return null
}

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

const getComprehensiveAgriculturalRecommendation = (notification) => {
  if (!notification.context) return 'No specific recommendations available at this time.'

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

const getActionPriority = (notification) => {
  if (!notification.context) return 'Monitor'
  
  const context = notification.context
  const severity = notification.severity?.toLowerCase()
  
  if (severity === 'critical') return 'IMMEDIATE ACTION REQUIRED'
  
  const soilMoisture = getSensorValue(notification, 'soilMoisture')
  const temperature = getSensorValue(notification, 'temperature')
  const waterLevel = context.waterLevel
  
  if (waterLevel !== undefined && waterLevel <= 15) return 'IMMEDIATE ACTION REQUIRED'
  if (soilMoisture !== null && soilMoisture <= 10) return 'IMMEDIATE ACTION REQUIRED'
  if (temperature !== null && (temperature < 10 || temperature > 40)) return 'IMMEDIATE ACTION REQUIRED'
  
  if (severity === 'warning') return 'High Priority - Act within 24 hours'
  if (waterLevel !== undefined && waterLevel <= 30) return 'High Priority - Act within 24 hours'
  if (soilMoisture !== null && soilMoisture <= 20) return 'High Priority - Act within 24 hours'
  
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

const getWeatherRecommendation = (notification) => {
  if (!notification.context) return 'Monitor weather conditions and adjust agricultural activities accordingly.'
  
  const condition = notification.context.condition?.toLowerCase() || ''
  const forecast = notification.context.forecast
  const current = notification.context.current
  
  const recommendations = []
  
  if (condition.includes('heavy rain') || condition.includes('thunderstorm')) {
    recommendations.push('🌧️ Prepare for heavy rainfall - ensure proper drainage and secure equipment')
    recommendations.push('⚡ Risk of electrical storms - avoid outdoor electrical operations')
    recommendations.push('💧 Suspended irrigation may be possible due to natural precipitation')
  }
  
  if (condition.includes('rain shower')) {
    recommendations.push('🌦️ Light precipitation expected - reduce or suspend irrigation schedules')
    recommendations.push('🌱 Good conditions for nutrient uptake - consider liquid fertilizer application after rain')
  }
  
  if (current?.temperature !== undefined) {
    if (current.temperature > 30) {
      recommendations.push('🌡️ High temperatures - increase irrigation frequency and provide shade protection')
    } else if (current.temperature < 15) {
      recommendations.push('🌡️ Cool temperatures - protect sensitive plants and adjust watering schedule')
    }
  }
  
  if (current?.windSpeed !== undefined && current.windSpeed > 20) {
    recommendations.push('💨 Strong winds expected - secure structures and protect young plants')
  }
  
  if (current?.uvIndex !== undefined && current.uvIndex > 7) {
    recommendations.push('☀️ High UV levels - provide shade protection for sensitive crops')
  }
  
  if (current?.humidity !== undefined) {
    if (current.humidity > 80) {
      recommendations.push('💨 High humidity - monitor for fungal diseases and improve ventilation')
    } else if (current.humidity < 40) {
      recommendations.push('💧 Low humidity - increase irrigation frequency to prevent plant stress')
    }
  }
  
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

const markAsRead = async (id) => {
  if (!validateNotificationId(id, 'markAsRead')) return;
  
  try {
    const notifIndex = notifications.value.findIndex(n => n.id === id);
    if (notifIndex !== -1) {
      notifications.value = notifications.value.map((n, index) => 
        index === notifIndex ? { ...n, read: true } : n
      );
    }
    
    await api.patch(`/notifications/${id}`, { read: true });
    
    window.showToast('Marked as read', 'success');
    
  } catch (err) {
    console.error("Failed to mark as read:", err);
    
    const notifIndex = notifications.value.findIndex(n => n.id === id);
    if (notifIndex !== -1) {
      notifications.value = notifications.value.map((n, index) => 
        index === notifIndex ? { ...n, read: false } : n
      );
    }
    
    window.showToast('Failed to mark as read', 'failed');
  }
};

const markAllAsRead = async () => {
  try {
    const unreadNotifications = notifications.value.filter(n => !n.read);
    
    if (unreadNotifications.length === 0) {
      window.showToast('No unread notifications', 'info');
      return;
    }
    
    notifications.value = notifications.value.map(n => ({ ...n, read: true }));
    
    await api.post('/notifications/mark-all-read');
    window.showToast(`Marked ${unreadNotifications.length} notifications as read`, 'success');
    
  } catch (err) {
    console.error("❌ Failed to mark all as read:", err);
    fetchNotifications(); 
    window.showToast('Failed to mark all as read', 'failed');
  }
};

const archiveNotification = async (id) => {
  if (!validateNotificationId(id, 'archive')) return;
  
  try {
    const notif = notifications.value.find(n => n.id === id);
    if (notif) {
      notif.archived = true;
      notif.read = true;
      
      await api.patch(`/notifications/${id}`, { 
        archived: true,
        read: true,
        archivedAt: new Date().toISOString()
      });
      
      notifications.value = notifications.value.filter(n => n.id !== id);
      archivedNotifications.value.push(notif);
      
      // window.showToast('Notification archived', 'success');
    }
  } catch (err) {
    console.error("❌ Failed to archive notification:", err);
    fetchNotifications(); 
    window.showToast('Failed to archive notification', 'failed');
  }
};

const unarchiveNotification = async (id) => {
  if (!validateNotificationId(id, 'unarchive')) return;
  
  try {
    const notif = archivedNotifications.value.find(n => n.id === id);
    if (notif) {
      notif.archived = false;
      
      await api.patch(`/notifications/${id}`, { 
        archived: false,
        archivedAt: null
      });
      
      archivedNotifications.value = archivedNotifications.value.filter(n => n.id !== id);
      notifications.value.unshift(notif);
      
      // window.showToast('Notification unarchived', 'success');
    }
  } catch (err) {
    console.error("❌ Failed to unarchive notification:", err);
    fetchNotifications();
    window.showToast('Failed to unarchive notification', 'failed');
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

const handleQuickUnarchive = async (id) => {
  try {
    unarchivingIds.value.add(id);
    
    const notifIndex = archivedNotifications.value.findIndex(n => n.id === id);
    if (notifIndex !== -1) {
      const notification = archivedNotifications.value[notifIndex];
      notification.archived = false;

      notifications.value.unshift(notification);
      archivedNotifications.value.splice(notifIndex, 1);

      await api.patch(`/notifications/${id}`, { 
        archived: false,
        archivedAt: null
      });
    }
  } catch (err) {
    console.error("❌ Failed to unarchive notification:", err);
  } finally {
    unarchivingIds.value.delete(id);
  }
};

const deleteNotification = async (id) => {
  if (!validateNotificationId(id, 'delete')) return;
  
  try {
    notifications.value = notifications.value.filter(n => n.id !== id);
    archivedNotifications.value = archivedNotifications.value.filter(n => n.id !== id);
    
    await api.delete(`/notifications/${id}`);
    window.showToast('Notification deleted', 'success');
    
  } catch (err) {
    console.error("❌ Failed to delete notification:", err);
    window.showToast('Failed to delete notification', 'failed');
  }
};

const deleteAllNotifications = async () => {
  try {
    isDeletingAll.value = true;
    showDeleteAllConfirmation.value = false;
    
    const count = notifications.value.length + archivedNotifications.value.length;
    
    await api.delete('/notifications');
    
    notifications.value = [];
    archivedNotifications.value = [];
    
    window.showToast(`Deleted ${count} notifications`, 'success');
    
  } catch (error) {
    console.error('Failed to delete all notifications:', error);
    window.showToast('Failed to delete all notifications', 'failed');
  } finally {
    isDeletingAll.value = false;
  }
};

const getUnreadCount = async () => {
  try {
    const response = await api.get('/notifications/unread/count');
    return response.data.unread_count || 0;
  } catch (error) {
    console.error('Error getting unread count:', error);
    return 0;
  }
};

const formatTime = (time) => {
  if (!time) return 'Unknown time';
  
  let notificationTime;
  
  if (typeof time === 'string' || typeof time === 'number') {
    notificationTime = new Date(time);
  } else if (time instanceof Date) {
    notificationTime = time;
  } else if (time._seconds) {
    notificationTime = new Date(time._seconds * 1000);
  } else {
    return 'Invalid time';
  }
  
  if (isNaN(notificationTime.getTime())) {
    return 'Invalid time';
  }
  
  const now = new Date();
  
  // TEMPORARY FIX: Adjust for the 4-hour discrepancy
  // Remove this line once the backend issue is fixed
  const adjustedNotificationTime = new Date(notificationTime.getTime() - (-8 * 60 * 60000));
  
  const diff = now - adjustedNotificationTime;
  const mins = Math.floor(diff / 60000);
  const hours = Math.floor(diff / 3600000);
  const days = Math.floor(diff / 86400000);

  if (mins < 1) return 'Just now';
  if (mins < 60) return `${mins} min ago`;
  if (hours < 24) return `${hours} hr ago`;
  if (days < 7) return `${days} day${days !== 1 ? 's' : ''} ago`;
  
  return adjustedNotificationTime.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });
};

const formatTimeForDisplay = (time) => {
  if (!time) return 'Unknown time';
  
  const date = new Date(time);
  if (isNaN(date.getTime())) return 'Invalid time';
  
  const relativeTime = formatTime(time);
  
  
  return `${relativeTime} `;
};

const getNotificationIcon = (notification) => {
  const title = notification.title?.toLowerCase() || ''
  const message = notification.message?.toLowerCase() || ''
  const category = notification.category?.toLowerCase() || ''
  const type = notification.type?.toLowerCase() || ''
  
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
  
  if (notification.severity === 'critical' || title.includes('critical') || message.includes('critical') ||
      title.includes('urgent') || message.includes('urgent')) {
    return { bgColor: 'bg-red-600', badgeColor: 'bg-red-100 text-red-800', icon: AlertCircle }
  }
  
  if (notification.severity === 'warning' || title.includes('warning') || message.includes('warning') ||
      title.includes('alert') || message.includes('alert') || type.includes('alert')) {
    return { bgColor: 'bg-orange-500', badgeColor: 'bg-orange-100 text-orange-800', icon: AlertTriangle }
  }
  
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
  
  if (title.includes('location') || title.includes('gps') || title.includes('position') ||
      message.includes('location') || message.includes('gps') || message.includes('position')) {
    return { bgColor: 'bg-blue-500', badgeColor: 'bg-blue-100 text-blue-800', icon: MapPin }
  }
  
  if (title.includes('success') || title.includes('completed') || title.includes('finished') ||
      message.includes('success') || message.includes('completed') || message.includes('finished') ||
      type.includes('success')) {
    return { bgColor: 'bg-green-500', badgeColor: 'bg-green-100 text-green-800', icon: Check }
  }
  
  if (type.includes('info') || category.includes('info')) {
    return { bgColor: 'bg-blue-500', badgeColor: 'bg-blue-100 text-blue-800', icon: Info }
  }
  
  return { bgColor: 'bg-gray-500', badgeColor: 'bg-gray-100 text-gray-800', icon: Bell }
}

const goBack = () => {
  try {
    if (window.history.length > 1) {
      if (window.history.state && window.history.state.back) {
        window.history.back()
      } else {
        const router = getCurrentInstance()?.appContext.app.config.globalProperties.$router
        if (router) {
          router.go(-1)
        } else {
          window.history.back()
        }
      }
    } else {
      const router = getCurrentInstance()?.appContext.app.config.globalProperties.$router
      if (router) {
        router.push('/dashboard')
      } else {
        window.location.href = '/dashboard'
      }
    }
  } catch (error) {
    console.error('Error navigating back:', error)
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

const unsubscribeNotifications = ref(null)

const isValidId = (id) => {
  return id && id !== 'undefined' && id !== 'null' && id !== '' && !id.startsWith('temp-');
};

const generateTempId = (index) => {
  return `temp-${Date.now()}-${Math.random().toString(36).substr(2, 9)}-${index}`;
};

const standardizeNotification = (notif) => {
  let notificationId = notif._id || notif.id || notif.documentId || notif.firebaseId || notif.uniqueKey;
  
  if (!isValidId(notificationId)) {
    notificationId = generateTempId();
  }
  
  return {
    ...notif,
    id: notificationId, 
    _id: notificationId, 
    time: notif.timestamp || notif.time || new Date(),
    originalId: notif._id || notif.id,
    read: Boolean(notif.read),
    archived: Boolean(notif.archived),
    timestamp: notif.timestamp ? new Date(notif.timestamp) : new Date()
  };
};

const fetchNotifications = async () => {
  try {
    // isLoading.value = true;
    console.log('Starting to fetch notifications...');
    
    const response = await api.get('/notifications');
    console.log('API response received:', response.status);
    
    if (response.data && Array.isArray(response.data)) {
      console.log('Raw data from API:', response.data.length, 'items');
      
      const processedNotifications = response.data.map(standardizeNotification);
      console.log('Processed notifications:', processedNotifications.length);
      
      const uniqueNotifications = [];
      const seenIds = new Set();
      
      for (const notif of processedNotifications) {
        if (!notif.id || !isValidId(notif.id)) {
          notif.id = generateTempId();
          notif._id = notif.id;
        }
        
        if (!seenIds.has(notif.id)) {
          seenIds.add(notif.id);
          uniqueNotifications.push(notif);
        }
      }
      
      console.log('Unique notifications:', uniqueNotifications.length);
      
      notifications.value = uniqueNotifications.filter(n => !n.archived);
      archivedNotifications.value = uniqueNotifications.filter(n => n.archived);
      
      console.log('Active notifications:', notifications.value.length);
      console.log('Archived notifications:', archivedNotifications.value.length);
      
      if (notifications.value.length > 0) {
        const sample = notifications.value[0];
        console.log('Sample notification fields:', Object.keys(sample));
        console.log('Sample notification:', {
          id: sample.id,
          time: sample.time,
          title: sample.title,
          message: sample.message
        });
      }
    }
    
  } catch (error) {
    console.error('Failed to fetch notifications:', error);
    window.showToast('Error loading notifications', 'failed');
  } finally {
    isLoading.value = false;
  }
};

const setupNotificationPolling = (unsubscribeFunctions) => {
  const notificationInterval = setInterval(fetchNotifications, 1000);
  fetchNotifications(); // Initial fetch
  unsubscribeFunctions.push(() => clearInterval(notificationInterval));
}

const validateNotificationId = (id, operation = 'operation') => {
  if (!isValidId(id)) {
    console.warn(`Skipping ${operation} for invalid ID:`, id);
    return false;
  }
  return true;
};

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

const checkForIdIssues = () => {
  const allNotifications = [...notifications.value, ...archivedNotifications.value];
  const invalidIds = allNotifications.filter(n => !n._id || !isValidId(n._id));
  const duplicateIds = allNotifications.map(n => n._id).filter((id, index, array) => array.indexOf(id) !== index);
  
  if (invalidIds.length > 0) {
    console.error('Notifications with invalid IDs:', invalidIds);
  }
  
  if (duplicateIds.length > 0) {
    console.warn('Duplicate IDs found:', duplicateIds);
  }
  
  return { invalidIds, duplicateIds };
};

const unsubscribeFunctions = ref([])

onMounted(() => {
  loadUserPreferences()
  setupNotificationPolling(unsubscribeFunctions.value)
  fetchNotifications().then(() => {
    checkForIdIssues();
  });
  eventBus.on('notification-saved-success', fetchNotifications)
})

onUnmounted(() => {
  stopLoadingAnimation()
  if (unsubscribeNotifications.value) {
    unsubscribeNotifications.value()
  }
  unsubscribeFunctions.value.forEach(unsubscribe => unsubscribe())
  unsubscribeFunctions.value = []

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