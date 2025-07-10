<template>
      <!-- Container Wrapper with proper spacing -->
      <div class="flex-1 w-full px-4 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
        <!-- Main Container with adjusted width -->
        <div class="bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-green-100 h-[calc(100vh-140px)] overflow-y-auto transition-all duration-300 ease-in-out hover:shadow-[0_12px_40px_rgb(0,0,0,0.12)]">
          <!-- Content Wrapper -->
          <div class="p-6">
            <!-- Find the Top Metrics Cards section and replace it with this updated version -->
  
            <!-- Top Metrics Cards - Conditional Rendering -->
            <div v-if="!isLoading" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-4 mb-8">
              <!-- Nitrogen Level Card -->
              <div class="group bg-white rounded-xl p-4 border-2 border-green-100 shadow-lg transition-all duration-300 hover:border-green-400 hover:shadow-xl hover:-translate-y-1">
                <div class="flex items-center justify-between mb-2">
                  <Leaf class="h-5 w-5 text-green-500 transition-transform duration-300 group-hover:scale-110" />
                  <span class="text-xs font-semibold text-green-600 bg-green-100 px-2 py-0.5 rounded-full">N</span>
                </div>
                <div class="text-xl font-bold text-green-700">{{ nitrogen }}</div>
                <div class="text-xs text-green-600">Nitrogen (mg/kg)</div>
              </div>

              <!-- Phosphorus Level Card -->
              <div class="group bg-white rounded-xl p-4 border-2 border-blue-100 shadow-lg transition-all duration-300 hover:border-blue-400 hover:shadow-xl hover:-translate-y-1">
                <div class="flex items-center justify-between mb-2">
                  <TestTube class="h-5 w-5 text-blue-500 transition-transform duration-300 group-hover:scale-110" />
                  <span class="text-xs font-semibold text-blue-600 bg-blue-100 px-2 py-0.5 rounded-full">P</span>
                </div>
                <div class="text-xl font-bold text-blue-700">{{ phosphorus }}</div>
                <div class="text-xs text-blue-600">Phosphorus (mg/kg)</div>
              </div>

              <!-- Potassium Level Card -->
              <div class="group bg-white rounded-xl p-4 border-2 border-purple-100 shadow-lg transition-all duration-300 hover:border-purple-400 hover:shadow-xl hover:-translate-y-1">
                <div class="flex items-center justify-between mb-2">
                  <TestTubes class="h-5 w-5 text-purple-500 transition-transform duration-300 group-hover:scale-110" />
                  <span class="text-xs font-semibold text-purple-600 bg-purple-100 px-2 py-0.5 rounded-full">K</span>
                </div>
                <div class="text-xl font-bold text-purple-700">{{ potassium }}</div>
                <div class="text-xs text-purple-600">Potassium (mg/kg)</div>
              </div>

              <!-- Soil pH Level Card -->
              <div class="group bg-white rounded-xl p-4 border-2 border-orange-100 shadow-lg transition-all duration-300 hover:border-orange-400 hover:shadow-xl hover:-translate-y-1">
                <div class="flex items-center justify-between mb-2">
                  <Beaker class="h-5 w-5 text-orange-500 transition-transform duration-300 group-hover:scale-110" />
                  <span class="text-xs font-semibold text-orange-600 bg-orange-100 px-2 py-0.5 rounded-full">pH</span>
                </div>
                <div class="text-xl font-bold text-orange-700">{{ soilpH }}</div>
                <div class="text-xs text-orange-600">Soil pH Level</div>
              </div>

              <!-- Soil Moisture Card -->
              <div class="group bg-white rounded-xl p-4 border-2 border-emerald-100 shadow-lg transition-all duration-300 hover:border-emerald-400 hover:shadow-xl hover:-translate-y-1">
                <div class="flex items-center justify-between mb-2">
                  <Sprout class="h-5 w-5 text-emerald-500 transition-transform duration-300 group-hover:scale-110" />
                  <span class="text-xs font-semibold text-emerald-600 bg-emerald-100 px-2 py-0.5 rounded-full">SM</span>
                </div>
                <div class="text-xl font-bold text-emerald-700">{{ soilMoisture }}</div>
                <div class="text-xs text-emerald-600">Soil Moisture</div>
              </div>

              <!-- Temperature Card -->
              <div class="group bg-white rounded-xl p-4 border-2 border-red-100 shadow-lg transition-all duration-300 hover:border-red-400 hover:shadow-xl hover:-translate-y-1">
                <div class="flex items-center justify-between mb-2">
                  <Thermometer class="h-5 w-5 text-red-500 transition-transform duration-300 group-hover:scale-110" />
                  <span class="text-xs font-semibold text-red-600 bg-red-100 px-2 py-0.5 rounded-full">Temp</span>
                </div>
                <div class="text-xl font-bold text-red-700">{{ temperature }}</div>
                <div class="text-xs text-red-600">Temperature (°C)</div>
              </div>

              <!-- Humidity Card -->
              <div class="group bg-white rounded-xl p-4 border-2 border-sky-100 shadow-lg transition-all duration-300 hover:border-sky-400 hover:shadow-xl hover:-translate-y-1">
                <div class="flex items-center justify-between mb-2">
                  <Droplets class="h-5 w-5 text-sky-500 transition-transform duration-300 group-hover:scale-110" />
                  <span class="text-xs font-semibold text-sky-600 bg-sky-100 px-2 py-0.5 rounded-full">RH</span>
                </div>
                <div class="text-xl font-bold text-sky-700">{{ humidity }}</div>
                <div class="text-xs text-sky-600">Humidity (%)</div>
              </div>
            </div>
            <!-- Loading Skeleton for Top Metrics Cards -->
            <div v-else class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-7 gap-4 mb-8">
              <div v-for="i in 7" :key="i" class="bg-white rounded-xl p-4 border-2 border-gray-200 shadow-lg">
                <div class="flex items-center justify-between mb-2">
                  <div class="h-5 w-5 bg-gray-300 rounded animate-pulse"></div>
                  <div class="h-5 w-6 bg-gray-300 rounded-full animate-pulse"></div>
                </div>
                <div class="h-7 bg-gray-300 rounded animate-pulse w-3/4 mb-1"></div>
                <div class="h-4 bg-gray-300 rounded animate-pulse w-full"></div>
              </div>
            </div>

            <!-- Charts Section -->
            <div class="grid grid-cols-1 gap-8">
              <!-- First Row - Water Level, Motor Status, and Weather -->
              <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <!-- Enhanced Water Level Card -->
                <div class="bg-white rounded-2xl p-6 shadow-lg border border-blue-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
                  <!-- Header -->
                  <div class="flex justify-between items-center mb-4">
                    <div class="flex items-center bg-blue-50 rounded-full px-2.5 py-1 shadow-inner space-x-1.5">
                      <Waves class="w-4 h-4 text-blue-500" />
                      <h3 class="text-sm font-semibold text-blue-700 tracking-wide">Water Level</h3>
                    </div>
                    <div class="bg-blue-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">LIVE</div>
                  </div>

                  <!-- Water Tank -->
                  <div class="relative w-64 h-80 mx-auto mt-4">
                    <div class="relative w-full h-full rounded-[2rem] border-[6px] border-blue-300 bg-white shadow-2xl overflow-hidden tank-style">
                      <!-- Water Fill Area -->
                      <div class="absolute bottom-0 left-0 w-full h-full z-10 overflow-hidden">
                        <div
                          class="absolute top-0 left-0 w-full h-full transition-transform duration-700 ease-in-out"
                          :style="{ transform: `translateY(${100 - waterLevel}%)` }"
                        >
                          <div class="relative w-[900%] h-full">
                            <!-- Wave 1 -->
                            <div class="absolute w-full h-full left-0 top-0 animate-long-wave-1">
                              <svg viewBox="0 0 1200 300" preserveAspectRatio="none" class="w-full h-full">
                                <path
                                  d="M0,0 C200,60 400,-60 600,0 C800,60 1000,-60 1200,0 L1200,300 L0,300 Z"
                                  fill="#3B82F6" fill-opacity="0.6"
                                />
                              </svg>
                            </div>
                            <!-- Wave 2 -->
                            <div class="absolute w-full h-full left-0 top-0 animate-long-wave-2">
                              <svg viewBox="0 0 1200 300" preserveAspectRatio="none" class="w-full h-full">
                                <path
                                  d="M0,0 C200,50 400,-50 600,0 C800,50 1000,-50 1200,0 L1200,300 L0,300 Z"
                                  fill="#60A5FA" fill-opacity="0.4"
                                />
                              </svg>
                            </div>
                            <!-- Wave 3 -->
                            <div class="absolute w-full h-full left-0 top-0 animate-long-wave-3">
                              <svg viewBox="0 0 1200 300" preserveAspectRatio="none" class="w-full h-full">
                                <path
                                  d="M0,0 C200,40 400,-40 600,0 C800,40 1000,-40 1200,0 L1200,300 L0,300 Z"
                                  fill="#3B82F6" fill-opacity="0.2"
                                />
                              </svg>
                            </div>
                          </div>
                        </div>
                      </div>

                      <!-- Water Percentage -->
                      <div class="absolute inset-0 flex items-center justify-center z-20">
                        <div class="bg-white/80 backdrop-blur px-4 py-2 rounded-xl shadow-lg border border-blue-100">
                          <span v-if="!isChartsLoading" class="text-4xl font-bold text-blue-600">{{ waterLevel }}%</span>
                          <span v-else class="text-4xl font-bold text-blue-600">
                            <div class="h-8 w-16 bg-gray-300 rounded animate-pulse"></div>
                          </span>
                        </div>
                      </div>
                    </div>

                    <!-- Level Markers -->
                    <div class="absolute top-2 bottom-2 -right-14 w-10 flex flex-col justify-between z-30">
                      <div v-for="n in 5" :key="n" class="flex items-center gap-2">
                        <div class="h-[2px] w-4 bg-blue-400 shadow-sm"></div>
                        <span class="text-sm font-medium text-blue-600 bg-white/90 px-1 rounded">
                          {{ 100 - (n - 1) * 25 }}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Motor Status Card with Loading State -->
                <div v-if="!isChartsLoading" class="bg-white rounded-2xl p-6 shadow-lg border border-purple-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
                  <!-- Header section -->
                  <div class="flex flex-col items-start space-y-2 mb-4">
                    <div class="flex items-center justify-between w-full">
                      <div class="bg-purple-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                        <Power class="w-4 h-4 text-purple-500" />
                        <h3 class="text-sm font-semibold text-purple-700 tracking-wide">Motor Status</h3>
                      </div>
                      <div class="bg-purple-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                        WEEKLY
                      </div>
                    </div>
                    <div class="w-full">
                      <p class="text-xs text-purple-600 font-medium bg-purple-100 px-3 py-1 rounded-full shadow-sm inline-block">
                        Last 7 Days Overview
                      </p>
                    </div>
                  </div>
                  
                  <!-- Circular Display with ON/OFF percentages -->
                  <div class="relative w-48 h-48 mx-auto mt-4">
                    <svg class="w-full h-full" viewBox="0 0 100 100">
                      <!-- Background circle -->
                      <circle cx="50" cy="50" r="45" fill="none" stroke="#f3e8ff" stroke-width="8" />
                      
                      <!-- ON percentage arc (purple) -->
                      <circle 
                        cx="50" 
                        cy="50" 
                        r="45" 
                        fill="none" 
                        stroke="#e9d5ff" 
                        stroke-width="8" 
                        stroke-linecap="round"
                        :stroke-dasharray="circumference"
                        :stroke-dashoffset="circumference - (circumference * motorOnPercentage / 100)"
                        transform="rotate(-90 50 50)"
                      />
                      
                      <!-- OFF percentage arc (light purple) -->
                      <circle 
                        cx="50" 
                        cy="50" 
                        r="45" 
                        fill="none" 
                        stroke="#a855f7" 
                        stroke-width="8" 
                        stroke-linecap="round"
                        :stroke-dasharray="circumference"
                        :stroke-dashoffset="(circumference * motorOnPercentage / 100) - circumference"
                        transform="rotate(-90 50 50)"
                        stroke-dashoffset="0"
                      />
                    </svg>
                    
                    <!-- Center Power Button -->
                    <div 
                      class="absolute inset-6 rounded-full shadow-lg overflow-hidden cursor-default transition-all duration-300 power-button"
                      :class="motorStatus ? 'power-on' : 'power-off'"
                    >
                      <div class="absolute inset-0 bg-gradient-to-br from-purple-400 to-purple-600"></div>
                      <div class="absolute inset-0 flex items-center justify-center">
                        <Power :class="['w-14 h-14 transition-all duration-300', motorStatus ? 'text-white' : 'text-purple-200']" />
                      </div>
                      <div v-if="motorStatus" class="absolute inset-0 bg-purple-500 animate-pulse opacity-30"></div>
                    </div>
                    
                    <!-- ON Percentage Label -->
                    <div class="absolute top-1/2 left-0 -translate-y-1/2 -translate-x-1/2 text-center w-16 bg-purple-200 rounded-md border-2 border-purple-500">
                      <div class="text-xs text-purple-700 mb-1">ON</div>
                      <div class="text-lg font-bold text-purple-800">{{ motorOnPercentage.toFixed(1) }}%</div>
                    </div>
                    
                    <!-- OFF Percentage Label -->
                    <div class="absolute top-1/2 right-0 -translate-y-1/2 translate-x-1/2 text-center w-16 bg-purple-200 rounded-md border-2 border-purple-500">
                      <div class="text-xs text-purple-700 mb-1">OFF</div>
                      <div class="text-lg font-bold text-purple-800">{{ (100 - motorOnPercentage).toFixed(1) }}%</div>
                    </div>
                    
                  </div>

                  <!-- Status Information -->
                  <div class="mt-6 text-center">
                    <p class="text-base font-semibold text-purple-700">
                      Motor was <span class="text-purple-500">ON</span> for <span class="text-purple-500">{{ motorOnPercentage.toFixed(1) }}%</span> of the week
                    </p>
                    <p class="text-sm text-purple-600 mt-1">
                      Total runtime: {{ (motorOnPercentage * 1.68).toFixed(1) }} hours
                    </p>
                  </div>

                  <!-- Weekly Breakdown -->
                  <div class="mt-4">
                    <h4 class="text-xs font-semibold text-purple-700 mb-2">Weekly Breakdown</h4>
                    <div class="grid grid-cols-7 gap-1">
                      <div v-for="(day, index) in weeklyData" :key="index" class="flex flex-col items-center">
                        <div class="w-full bg-purple-100 rounded-full overflow-hidden">
                          <div 
                            class="bg-purple-500 h-1" 
                            :style="{ width: `${day.percentage}%` }"
                          ></div>
                        </div>
                        <span class="text-[10px] text-purple-600 mt-1">{{ day.label }}</span>
                      </div>
                    </div>
                  </div>
                </div>
                <div v-else class="h-full flex items-center justify-center bg-gray-50 rounded-lg">
                  <div class="text-center">
                    <svg class="animate-spin h-8 w-8 text-purple-500 mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <p class="text-sm text-gray-500">Loading motor status...</p>
                  </div>
                </div>

                <!-- Enhanced Weather Card with Colored Icons -->
                <div class="bg-white rounded-2xl p-6 shadow-lg border border-blue-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 overflow-hidden">
                  <div class="flex justify-between items-start mb-4">
                    <div class="flex items-center justify-between w-full">
                      <div class="bg-sky-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                        <CloudSun class="w-4 h-4 text-sky-500" />
                        <h3 class="text-sm font-semibold text-sky-700 tracking-wide">Weather Forecast</h3>
                      </div>
                      <div class="bg-sky-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">LIVE</div>
                    </div>
                  </div>

                  <!-- Current Weather -->
                  <div class="flex items-center justify-between mb-4">
                    <template v-if="!isWeatherLoading">
                      <div>
                        <div class="flex items-end space-x-1">
                          <p class="text-4xl font-bold text-gray-900">{{ weather?.temperature_c ?? '0' }}</p>
                          <p class="text-xl font-semibold text-gray-600 mb-1">°C</p>
                        </div>
                        <p class="text-base mt-1 text-gray-600">{{ weather?.weather_condition ?? '--' }}</p>
                      </div>
                      <div class="weather-icon-wrapper">
                        <component 
                          :is="getWeatherIcon(weather?.weather_condition)"
                          :class="['h-14 w-14 transform transition-transform hover:scale-110', getWeatherIconColor(weatherData[0]?.weather)]"
                        />
                      </div>
                    </template>
                    <template v-else>
                      <div class="flex items-center justify-between w-full animate-pulse">
                        <div>
                          <div class="h-10 w-24 bg-gray-300 rounded"></div>
                          <div class="h-6 w-32 bg-gray-300 rounded mt-2"></div>
                        </div>
                        <div class="h-14 w-14 bg-gray-300 rounded-full"></div>
                      </div>
                    </template>
                  </div>

                  <!-- Weather Details -->
                  <div v-if="!isWeatherLoading" class="grid grid-cols-2 gap-3 mb-4">
                    <div v-for="(detail, index) in weatherDetails" :key="index" class="bg-gray-50 rounded-lg p-2 transition-all duration-300 hover:bg-gray-100">
                      <div class="flex items-center space-x-2">
                        <component :is="detail.icon" :class="['h-4 w-4', getDetailIconColor(detail.label)]" />
                        <div>
                          <p class="text-xs text-gray-500">{{ detail.label }}</p>
                          <p class="text-sm font-semibold text-gray-900">{{ detail.value }}</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else class="grid grid-cols-2 gap-3 mb-4 animate-pulse">
                    <div v-for="i in 4" :key="`detail-skeleton-${i}`" class="bg-gray-200 rounded-lg p-2 h-16">
                      <!-- Skeleton content for detail item -->
                    </div>
                  </div>

                  <!-- 7-Day Forecast -->
                  <div v-if="!isWeatherLoading">
                    <h4 class="text-xs font-semibold mb-2 text-gray-900">7-Day Forecast</h4>
                    <div class="grid grid-cols-7 gap-1">
                      <div 
                        v-for="(day, index) in forecast" 
                        :key="index" 
                        class="flex flex-col items-center p-1 rounded-lg transition-all duration-300 hover:bg-gray-50"
                      >
                        <span class="text-[10px] mb-1 text-gray-600">
                          {{ new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' }) }}
                        </span>
                        <component 
                          :is="getWeatherIcon(day.temperature_max || 'Clear')" 
                          class="h-6 w-6 mb-1 text-yellow-500"
                        />
                        <span class="text-xs font-bold text-gray-900">
                          {{ typeof day.temperature_max === 'number' ? `${day.temperature_max.toFixed(1)}°` : 'N/A' }}
                        </span>
                      </div>
                    </div>
                  </div>
                  <div v-else class="animate-pulse">
                    <div class="h-4 w-24 bg-gray-300 rounded mb-2"></div>
                    <div class="grid grid-cols-7 gap-1">
                      <div v-for="i in 7" :key="`forecast-skeleton-${i}`" class="flex flex-col items-center p-1 rounded-lg bg-gray-200 h-20">
                        <div class="h-3 w-8 bg-gray-300 rounded mb-1.5"></div>
                        <div class="h-6 w-6 bg-gray-300 rounded-full mb-1.5"></div>
                        <div class="h-3 w-8 bg-gray-300 rounded"></div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Second Row - Soil Moisture and Humidity -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Enhanced Soil Moisture Card -->
                <div class="bg-white rounded-2xl p-6 shadow-lg border border-emerald-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
                  <!-- Header section with adjusted text sizes and spacing -->
                  <div class="flex flex-col items-start space-y-2 mb-4">
                    <div class="flex items-center justify-between w-full">
                      <div class="bg-emerald-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                        <Sprout class="w-4 h-4 text-emerald-500" />
                        <h3 class="text-sm font-semibold text-emerald-700 tracking-wide">Soil Moisture</h3>
                      </div>
                      <div class="bg-emerald-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                        LIVE
                      </div>
                    </div>
                    <div class="w-full">
                      <p class="text-xs text-emerald-600 font-medium bg-emerald-100 px-3 py-1 rounded-full shadow-sm inline-block">
                        {{ soilMoistureTimeRange }}
                      </p>
                    </div>
                  </div>

                  <!-- Current Value with Enhanced Styling -->
                  <div class="flex items-center space-x-3 mb-6">
                    <div class="flex-1">
                      <div class="flex items-baseline">
                        <span class="text-3xl font-bold text-emerald-600">{{ soilMoisture ?? '0.0' }}%</span>
                        <span
                          class="ml-2 text-sm font-medium"
                          :class="getSoilMoistureStatus(latestSoilMoisture).color"
                        >
                          {{ getSoilMoistureStatus(latestSoilMoisture).label }}
                        </span>
                      </div>
                      <div class="flex items-center mt-1" v-if="soilMoistureChange">
                        <component
                          :is="soilMoistureChange.direction === 'up' ? ArrowUp : ArrowDown"
                          class="w-4 h-4 mr-1"
                          :class="soilMoistureChange.direction === 'up' ? 'text-emerald-500' : 'text-red-500'"
                        />
                        <span
                          class="text-xs font-medium"
                          :class="soilMoistureChange.direction === 'up' ? 'text-emerald-600' : 'text-red-600'"
                        >
                          {{ soilMoistureChange.percent }}% {{ soilMoistureChange.direction === 'up' ? 'increase' : 'decrease' }} from yesterday
                        </span>
                      </div>
                    </div>
                    <div class="bg-emerald-50 p-3 rounded-2xl">
                      <Droplets class="w-8 h-8 text-emerald-500" />
                    </div>
                  </div>

                  <!-- Enhanced Chart Container -->
                  <div class="bg-white rounded-xl p-4 border border-emerald-100">
                    <div class="h-[180px]">
                      <canvas v-if="!isChartsLoading" ref="soilMoistureChartRef"></canvas>
                      <div v-else class="h-full flex items-center justify-center bg-gray-50 rounded-lg">
                        <div class="text-center">
                          <svg class="animate-spin h-8 w-8 text-emerald-500 mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <p class="text-sm text-gray-500">Loading chart...</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Enhanced Humidity Card -->
                <div class="bg-white rounded-2xl p-6 shadow-lg border border-sky-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
                  <!-- Header section with adjusted text sizes and spacing -->
                  <div class="flex flex-col items-start space-y-2 mb-4">
                    <div class="flex items-center justify-between w-full">
                      <div class="bg-sky-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                        <Droplets class="w-4 h-4 text-sky-500" />
                        <h3 class="text-sm font-semibold text-sky-700 tracking-wide">Humidity</h3>
                      </div>
                      <div class="bg-sky-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                        LIVE
                      </div>
                    </div>
                    <div class="w-full">
                      <p class="text-xs text-sky-600 font-medium bg-sky-100 px-3 py-1 rounded-full shadow-sm inline-block">
                        {{ humidityTimeRange }}
                      </p>
                    </div>
                  </div>

                  <!-- Current Value with Enhanced Styling -->
                  <div class="flex items-center space-x-3 mb-6">
                    <div class="flex-1">
                      <div class="flex items-baseline">
                        <span class="text-3xl font-bold text-sky-600">{{ humidity % 100 ?? '0.0'}}</span>
                        <span
                          class="ml-2 text-sm font-medium"
                          :class="getHumidityStatus(latestHumidity).color"
                        >
                          {{ getHumidityStatus(latestHumidity).label }}
                        </span>
                      </div>
                      <div class="flex items-center mt-1" v-if="humidityChange">
                        <component
                          :is="humidityChange.direction === 'up' ? ArrowUp : ArrowDown"
                          class="w-4 h-4 mr-1"
                          :class="humidityChange.direction === 'up' ? 'text-emerald-500' : 'text-red-500'"
                        />
                        <span
                          class="text-xs font-medium"
                          :class="humidityChange.direction === 'up' ? 'text-emerald-600' : 'text-red-600'"
                        >
                          {{ humidityChange.percent }}% {{ humidityChange.direction === 'up' ? 'increase' : 'decrease' }} from yesterday
                        </span>
                      </div>
                    </div>
                    <div class="bg-sky-50 p-3 rounded-2xl">
                      <Cloud class="w-8 h-8 text-sky-500" />
                    </div>
                  </div>

                  <!-- Enhanced Chart Container -->
                  <div class="bg-white rounded-xl p-4 border border-sky-100">
                    <div class="h-[180px]">
                      <canvas v-if="!isChartsLoading" ref="humidityChartRef"></canvas>
                      <div v-else class="h-full flex items-center justify-center bg-gray-50 rounded-lg">
                        <div class="text-center">
                          <svg class="animate-spin h-8 w-8 text-sky-500 mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <p class="text-sm text-gray-500">Loading chart...</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Third Row - Temperature and Soil pH -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Enhanced Temperature Card -->
                <div class="bg-white rounded-2xl p-6 shadow-lg border border-red-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
                  <!-- Header section with adjusted text sizes and spacing -->
                  <div class="flex flex-col items-start space-y-2 mb-4">
                    <div class="flex items-center justify-between w-full">
                      <div class="bg-red-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                        <Thermometer class="w-4 h-4 text-red-500" />
                        <h3 class="text-sm font-semibold text-red-700 tracking-wide">Temperature</h3>
                      </div>
                      <div class="bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                        LIVE
                      </div>
                    </div>
                    <div class="w-full">
                      <p class="text-xs text-red-600 font-medium bg-red-100 px-3 py-1 rounded-full shadow-sm inline-block">
                        {{ temperatureTimeRange }}
                      </p>
                    </div>
                  </div>

                  <!-- Current Value with Enhanced Styling -->
                  <div class="flex items-center space-x-3 mb-6">
                    <div class="flex-1">
                      <div class="flex items-baseline">
                        <span class="text-3xl font-bold text-red-600">{{ temperature ?? '0.0' }}°C</span>
                        <span
                          class="ml-2 text-sm font-medium"
                          :class="getTemperatureStatus(latestTemperature).color"
                        >
                          {{ getTemperatureStatus(latestTemperature).label }}
                        </span>
                      </div>
                      <div class="flex items-center mt-1" v-if="temperatureChange">
                        <component
                          :is="temperatureChange.direction === 'up' ? ArrowUp : ArrowDown"
                          class="w-4 h-4 mr-1"
                          :class="temperatureChange.direction === 'up' ? 'text-emerald-500' : 'text-red-500'"
                        />
                        <span
                          class="text-xs font-medium"
                          :class="temperatureChange.direction === 'up' ? 'text-emerald-600' : 'text-red-600'"
                        >
                          {{ temperatureChange.percent }}°C {{ temperatureChange.direction === 'up' ? 'increase' : 'decrease' }} from yesterday
                        </span>
                      </div>
                    </div>
                    <div class="bg-red-50 p-3 rounded-2xl">
                      <Sun class="w-8 h-8 text-red-500" />
                    </div>
                  </div>

                  <!-- Enhanced Chart Container -->
                  <div class="bg-white rounded-xl p-4 border border-red-100">
                    <div class="h-[180px]">
                      <canvas v-if="!isChartsLoading" ref="temperatureChartRef"></canvas>
                      <div v-else class="h-full flex items-center justify-center bg-gray-50 rounded-lg">
                        <div class="text-center">
                          <svg class="animate-spin h-8 w-8 text-red-500 mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <p class="text-sm text-gray-500">Loading chart...</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Enhanced Soil pH Card -->
                <div class="bg-white rounded-2xl p-6 shadow-lg border border-orange-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
                  <!-- Header section with adjusted text sizes and spacing -->
                  <div class="flex flex-col items-start space-y-2 mb-4">
                    <div class="flex items-center justify-between w-full">
                      <div class="bg-orange-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                        <Beaker class="w-4 h-4 text-orange-500" />
                        <h3 class="text-sm font-semibold text-orange-700 tracking-wide">Soil pH</h3>
                      </div>
                      <div class="bg-orange-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                        LIVE
                      </div>
                    </div>
                    <div class="w-full">
                      <p class="text-xs text-orange-600 font-medium bg-orange-100 px-3 py-1 rounded-full shadow-sm inline-block">
                        {{ soilPhTimeRange }}
                      </p>
                    </div>
                  </div>

                  <!-- Current Value with Enhanced Styling -->
                  <div class="flex items-center space-x-3 mb-6">
                    <div class="flex-1">
                      <div class="flex items-baseline">
                        <span class="text-3xl font-bold text-orange-600">{{ soilpH ?? '0.0' }}</span>
                        <span
                          class="ml-2 text-sm font-medium"
                          :class="getPhStatus(latestSoilPh).color"
                        >
                          {{ getPhStatus(latestSoilPh).label }}
                        </span>
                      </div>
                      <div class="flex items-center mt-1">
                        <template v-if="soilPhChange">
                          <component
                            :is="soilPhChange.direction === 'up' ? ArrowUp : ArrowDown"
                            class="w-4 h-4 mr-1"
                            :class="soilPhChange.direction === 'up' ? 'text-emerald-500' : 'text-red-500'"
                          />
                          <span
                            class="text-xs font-medium"
                            :class="soilPhChange.direction === 'up' ? 'text-emerald-600' : 'text-red-600'"
                          >
                            {{ soilPhChange.percent }}% {{ soilPhChange.direction === 'up' ? 'increase' : 'decrease' }} from yesterday
                          </span>
                        </template>
                        <span v-else class="text-xs text-gray-500">Change from yesterday: N/A</span>
                      </div>
                    </div>
                    <div class="bg-orange-50 p-3 rounded-2xl">
                      <FlaskConical class="w-8 w-8 text-orange-500" />
                    </div>
                  </div>

                  <!-- Enhanced Chart Container -->
                  <div class="bg-white rounded-xl p-4 border border-orange-100">
                    <div class="h-[180px]">
                      <canvas v-if="!isChartsLoading" ref="soilPhChartRef"></canvas>
                      <div v-else class="h-full flex items-center justify-center bg-gray-50 rounded-lg">
                        <div class="text-center">
                          <svg class="animate-spin h-8 w-8 text-orange-500 mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                          </svg>
                          <p class="text-sm text-gray-500">Loading chart...</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Fourth Row - Overall Performance -->
              <div class="bg-white rounded-2xl p-6 shadow-lg border border-green-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
                <!-- Enhanced Header section with adjusted text sizes and spacing -->
                <div class="flex flex-col items-start space-y-2 mb-6">
                  <div class="flex items-center justify-between w-full">
                    <div class="bg-green-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                      <FlaskConical class="w-4 h-4 text-green-500" />
                      <h3 class="text-sm font-semibold text-green-700 tracking-wide">NPK Levels</h3>
                    </div>
                    <div class="bg-green-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                      WEEKLY
                    </div>
                  </div>
                  <div class="w-full">
                    <p class="text-xs text-green-600 font-medium bg-green-100 px-3 py-1 rounded-full shadow-sm inline-block">
                      {{ npkTimeRange }}
                    </p>
                  </div>
                </div>

                <!-- Enhanced Circular Progress Section -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                  <div
                    v-for="(npk, index) in npkLevels"
                    :key="index"
                    :class="`p-4 rounded-xl border border-${npk.color}-100 bg-${npk.color}-50/30 backdrop-blur-sm transition-all duration-300 hover:shadow-lg hover:scale-105`"
                  >
                    <div class="text-center">
                      <div class="relative inline-flex items-center justify-center">
                        <svg class="w-32 h-32 transform -rotate-90">
                          <!-- Background circle -->
                          <circle
                            stroke-width="12"
                            :stroke="npk.title === 'Nitrogen' ? '#4ADE80' : npk.title === 'Phosphorus' ? '#60A5FA' : '#A78BFA'"
                            fill="transparent"
                            r="56"
                            cx="64"
                            cy="64"
                            opacity="0.2"
                          />

                          <!-- Foreground animated circle -->
                          <circle
                            stroke-width="12"
                            :stroke="npk.title === 'Nitrogen' ? '#4ADE80' : npk.title === 'Phosphorus' ? '#60A5FA' : '#A78BFA'"
                            :stroke-dasharray="circumference"
                            :stroke-dashoffset="getDashOffset(npk.value)"
                            stroke-linecap="round"
                            fill="transparent"
                            r="56"
                            cx="64"
                            cy="64"
                          >
                            <animate
                              attributeName="stroke-dashoffset"
                              :from="circumference"
                              :to="getDashOffset(npk.value)"
                              dur="1.5s"
                              fill="freeze"
                              calcMode="spline"
                              keySplines="0.4 0 0.2 1"
                            />
                          </circle>
                        </svg>

                        <!-- Text inside circle -->
                        <div class="absolute inset-0 flex flex-col items-center justify-center">
                          <span :class="`text-3xl font-bold text-${npk.color}-700`">
                            {{ Number(npk.value?.value || 0).toFixed(1) }}%
                          </span>
                          <span :class="`text-sm font-medium text-${npk.color}-600 mt-1`">
                            {{ npk.title }}
                          </span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Enhanced Chart Container -->
                <div class="bg-white rounded-xl p-4 border border-green-100 transition-all duration-300 hover:shadow-md">
                  <div class="h-[300px]">
                    <canvas v-if="!isChartsLoading" ref="performanceChartRef"></canvas>
                    <div v-else class="h-full flex items-center justify-center bg-gray-50 rounded-lg">
                      <div class="text-center">
                        <svg class="animate-spin h-8 w-8 text-green-500 mx-auto mb-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                          <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        <p class="text-sm text-gray-500">Loading chart...</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, nextTick, watch } from 'vue';
import { Chart, registerables } from 'chart.js';
import { 
  Sprout,
  Thermometer, 
  Droplets,
  Waves, 
  Power,
  Leaf,
  TestTube,
  TestTubes,
  Beaker,
  CloudSun,
  Cloud, 
  CloudRain, 
  Sun, 
  CloudLightning,
  CloudDrizzle,
  Wind,
  ArrowUp,
  ArrowDown,
  FlaskConical
} from 'lucide-vue-next';
import Sidebar from '../layout/Sidebar.vue'
import { getWeatherData } from '../../utils/weather';
import api from '../../api/index'
import { eventBus } from '../../eventBus';
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
    onSnapshot 
} from 'firebase/firestore'

const db = getFirestore()
Chart.register(...registerables);

const isLoading = ref(true);
const isChartsLoading = ref(true);
const isWeatherLoading = ref(true);
const streamDataReceived = ref(false);
const streamTimeout = ref(null);
const streamConnection = ref(null);
const lastStreamUpdate = ref(null);
const usingFirebaseFallback = ref(false);
const waterLevel = ref(0);

// Refs for chart instances
const soilMoistureChartInstance = ref(null);
const humidityChartInstance = ref(null);
const temperatureChartInstance = ref(null);
const soilPhChartInstance = ref(null);
const performanceChartInstance = ref(null);

// Refs for chart DOM elements
const performanceChartRef = ref(null);
const soilMoistureChartRef = ref(null);
const humidityChartRef = ref(null);
const temperatureChartRef = ref(null);
const soilPhChartRef = ref(null);

// Update the motorStatus and motorStatusPercentage variables
const motorStatus = ref(false);
const motorOnPercentage = ref(0); 

const circumference = 2 * Math.PI * 48; // Used for NPK progress rings and motor status ring
const dashOffset = computed(() => circumference * (1 - motorOnPercentage.value / 100));

const weatherData = ref({})
const npkData = ref({})
const weather = ref(null)
const forecast = ref([])

const nitrogen = ref(null)
const phosphorus = ref(null)
const potassium = ref(null)
const soilpH = ref(null)
const temperature = ref(null)
const humidity = ref(null)
const soilMoisture = ref(null)

// Refs for chart-specific data
const soilMoistureReadings = ref([]);
const humidityReadings = ref([]);
const temperatureReadings = ref([]);
const soilPhReadings = ref([]);
const npkReadings = ref([]);

let intervalId = null;
const firestoreListenersUnsubscribers = ref([]);
const weeklyData = ref([])

// Step 1: Calculate average values
const avgNitrogen = computed(() => {
  if (!npkReadings.value || npkReadings.value.length === 0) return 0;
  const total = npkReadings.value.reduce((sum, r) => sum + (r.nitrogen || 0), 0);
  return total / npkReadings.value.length;
});

const avgPhosphorus = computed(() => {
  if (!npkReadings.value || npkReadings.value.length === 0) return 0;
  const total = npkReadings.value.reduce((sum, r) => sum + (r.phosphorus || 0), 0);
  return total / npkReadings.value.length;
});

const avgPotassium = computed(() => {
  if (!npkReadings.value || npkReadings.value.length === 0) return 0;
  const total = npkReadings.value.reduce((sum, r) => sum + (r.potassium || 0), 0);
  return total / npkReadings.value.length;
});

// Step 2: Normalize so total = 100%
const totalNpk = computed(() => avgNitrogen.value + avgPhosphorus.value + avgPotassium.value);

const npkLevels = [
  {
    title: 'Nitrogen',
    value: computed(() =>
      totalNpk.value > 0 ? (avgNitrogen.value / totalNpk.value) * 100 : 0
    ),
    color: 'green',
  },
  {
    title: 'Phosphorus',
    value: computed(() =>
      totalNpk.value > 0 ? (avgPhosphorus.value / totalNpk.value) * 100 : 0
    ),
    color: 'blue',
  },
  {
    title: 'Potassium',
    value: computed(() =>
      totalNpk.value > 0 ? (avgPotassium.value / totalNpk.value) * 100 : 0
    ),
    color: 'purple',
  },
];

const getDashOffset = (val) => {
  const value = typeof val === 'object' && 'value' in val ? val.value : val;
  return circumference - (value / 100) * circumference;
};

const lineChartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    x: {
      display: true,
      grid: {
        display: false
      }
    },
    y: {
      display: true,
      beginAtZero: true,
      max: 100,
      ticks: {
        stepSize: 10
      }
    }
  },
  elements: {
    line: {
      tension: 0.4
    },
    point: {
      radius: 4
    }
  }
};

const loadWeather = async () => {
  try {
    const data = await getWeatherData();
    weather.value = data.current;
    forecast.value = data.forecast.slice(0, 7);
  } catch (error) {
    console.error('Failed to load weather:', error);
  }
};

const setupEventSource = () => {
  try {
    streamConnection.value = new EventSource('http://localhost:8000/api/stream');
    
    streamConnection.value.onmessage = (event) => {
      streamDataReceived.value = true;
      lastStreamUpdate.value = new Date();
      
      // Reset the timeout since we received data
      if (streamTimeout.value) clearTimeout(streamTimeout.value);
      
      const data = JSON.parse(event.data);
      console.log("📡 Received real-time data:", data);

      // Update metrics from stream data
      if (data.type === 'esp32-1') {
        nitrogen.value = data.data.nitrogen;
        phosphorus.value = data.data.phosphorus;
        potassium.value = data.data.potassium;
        soilpH.value = data.data.soilPh;
      } 
      else if (data.type === 'esp32-2') {
        temperature.value = data.data.temperature;
        humidity.value = data.data.humidity;
        soilMoisture.value = data.data.soilMoisture;
      }
      else if (data.type === 'esp32-3') {
        waterLevel.value = data.data.waterLevel;
      }

      // Update chart data if needed
      updateChartDataFromStream(data);
    };

    streamConnection.value.onerror = (e) => {
      console.error("❌ SSE Error:", e);
      if (!streamDataReceived.value && !usingFirebaseFallback.value) {
        console.log("⚡ Stream error, falling back to Firebase");
        usingFirebaseFallback.value = true;
        fetchLatestSensorDataFromFirebase();
        fetchLatestWaterLevel();
      }
    };

  } catch (error) {
    console.error("❌ Error setting up EventSource:", error);
    if (!usingFirebaseFallback.value) {
      usingFirebaseFallback.value = true;
      fetchLatestSensorDataFromFirebase();
      fetchLatestWaterLevel();
    }
  }
};

const updateChartDataFromStream = (data) => {
  if (!data || !data.timestamp) return;

  const newReading = {
    timestamp: new Date(data.timestamp),
    ...data.data
  };

  // Add to appropriate chart dataset
  if (data.type === 'esp32-1') {
    soilPhReadings.value = [...soilPhReadings.value.slice(-14), newReading];
    npkReadings.value = [...npkReadings.value.slice(-14), newReading];
  }
  else if (data.type === 'esp32-2') {
    soilMoistureReadings.value = [...soilMoistureReadings.value.slice(-14), newReading];
    humidityReadings.value = [...humidityReadings.value.slice(-14), newReading];
    temperatureReadings.value = [...temperatureReadings.value.slice(-14), newReading];
  }
};

const fetchLatestSensorDataFromFirebase = async () => {
  // Only run if we're in fallback mode
  if (!usingFirebaseFallback.value) return;
  
  let devicesLoaded = 0;
  const totalDevices = 2;

  const setLoadedIfComplete = () => {
    devicesLoaded++;
    if (devicesLoaded >= totalDevices) {
      isLoading.value = false;
    }
  };

  // For esp32-1 (NPK + pH)
  try {
    const esp32_1_query = query(
      collection(db, "3sensor_readings", "esp32-1", "readings"), 
      orderBy("timestamp", "desc"), 
      limit(1)
    );
    
    const unsubscribeEsp32_1 = onSnapshot(esp32_1_query, (snapshot) => {
      if (!snapshot.empty) {
        const esp32_1_data = snapshot.docs[0].data();
        nitrogen.value = esp32_1_data.nitrogen;
        phosphorus.value = esp32_1_data.phosphorus;
        potassium.value = esp32_1_data.potassium;
        soilpH.value = esp32_1_data.soilPh;
      }
      setLoadedIfComplete();
    }, (error) => {
      console.error("❌ Error fetching real-time ESP32-1 data:", error);
      setLoadedIfComplete();
    });
    
    firestoreListenersUnsubscribers.value.push(unsubscribeEsp32_1);
  } catch (err) {
    console.error("❌ Error setting up ESP32-1 snapshot:", err);
    setLoadedIfComplete();
  }

  // For esp32-2 (Temperature, humidity, soil moisture)
  try {
    const esp32_2_query = query(
      collection(db, "3sensor_readings", "esp32-2", "readings"), 
      orderBy("timestamp", "desc"), 
      limit(1)
    );
    
    const unsubscribeEsp32_2 = onSnapshot(esp32_2_query, (snapshot) => {
      if (!snapshot.empty) {
        const esp32_2_data = snapshot.docs[0].data();
        temperature.value = esp32_2_data.temperature;
        humidity.value = esp32_2_data.humidity;
        soilMoisture.value = esp32_2_data.soilMoisture;
      }
      setLoadedIfComplete();
    }, (error) => {
      console.error("❌ Error fetching real-time ESP32-2 data:", error);
      setLoadedIfComplete();
    });
    
    firestoreListenersUnsubscribers.value.push(unsubscribeEsp32_2);
  } catch (err) {
    console.error("❌ Error setting up ESP32-2 snapshot:", err);
    setLoadedIfComplete();
  }
};

const fetchLatestWaterLevel = () => {
  try {
    const q = query(
      collection(db, "water_level_readings"),
      orderBy("timestamp", "desc"),
      limit(1)
    );

    // Using onSnapshot for real-time updates
    const unsubscribe = onSnapshot(q, (snapshot) => {
      if (!snapshot.empty) {
        const latestDoc = snapshot.docs[0];
        const data = latestDoc.data();
        waterLevel.value = data.waterLevel || 0;
        console.log("💧 Latest Water Level from esp32-3:", waterLevel.value);
      }
    }, (error) => {
      console.error("❌ Error listening to water level updates:", error);
    });

    // Return the unsubscribe function in case you want to stop listening later
    return unsubscribe;
    
  } catch (error) {
    console.error("❌ Error setting up water level listener:", error);
    // Return a no-op function if initialization fails
    return () => {};
  }
};

const fetchMotorStatusData = async () => {
  try {
    // Get current motor status
    const currentDoc = await getDoc(doc(db, 'motor_status', 'current'))
    if (currentDoc.exists()) {
      const data = currentDoc.data()
      motorStatus.value = data.status || false
    }

    // Get history logs
    const historySnapshot = await getDocs(collection(db, 'motor_status', 'history', 'logs'))
    const logs = []
    historySnapshot.forEach(doc => logs.push(doc.data()))

    // Filter this week's logs
    const now = new Date()
    const startOfWeek = new Date(now)
    startOfWeek.setDate(now.getDate() - now.getDay()) // Sunday

    const thisWeekLogs = logs.filter(log => {
      const ts = log.timestamp?.toDate?.() || new Date(log.timestamp)
      return ts >= startOfWeek
    })

    // Compute % of time ON per day
    const dailyOnCounts = Array(7).fill(0);
    const dailyTotalLogs = Array(7).fill(0);

    thisWeekLogs.forEach(log => {
      const ts = log.timestamp?.toDate?.() || new Date(log.timestamp)
      const dayIndex = ts.getDay() // 0 for Sunday, 1 for Monday, etc.
      dailyTotalLogs[dayIndex]++;
      if (log.status === true) {
        dailyOnCounts[dayIndex]++;
      }
    })

    const dayLabels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
    const dailyPercentages = dailyOnCounts.map((onCount, index) => ({
      label: dayLabels[index],
      percentage: dailyTotalLogs[index] > 0 ? (onCount / dailyTotalLogs[index]) * 100 : 0
    }))

    weeklyData.value = dailyPercentages;

    // Calculate overall weekly ON percentage
    const totalOnLogsForWeek = dailyOnCounts.reduce((sum, count) => sum + count, 0);
    const totalLogsForWeek = dailyTotalLogs.reduce((sum, count) => sum + count, 0);
    
    motorOnPercentage.value = totalLogsForWeek > 0 ? (totalOnLogsForWeek / totalLogsForWeek) * 100 : 0;

  } catch (error) {
    console.error('Error fetching motor status and history:', error)
  }
}

const mapSnapshotToReadings = (snapshot, deviceId) => {
  return snapshot.docs.map(doc => {
    const data = doc.data();
    let timestamp;
    
    if (data.timestamp?.toDate) {
      timestamp = data.timestamp.toDate();
    } else if (data.timestamp?.seconds) {
      timestamp = new Date(data.timestamp.seconds * 1000);
    } else if (data.timestamp instanceof Date) {
      timestamp = data.timestamp;
    } else {
      console.warn('Unknown timestamp format in document:', doc.id);
      timestamp = new Date(); // fallback to current time
    }

    return {
      id: doc.id,
      deviceId,
      ...data,
      timestamp: timestamp
    };
  }).filter(reading => {
    // Filter out any readings that might have invalid data
    return (
      reading.timestamp instanceof Date && 
      !isNaN(reading.timestamp.getTime())
    );
  });
};

const fetchDeviceChartData = async (deviceId, timeRange, targetRefs) => {
  const now = new Date();
  let startDate;
  const minDataPoints = 15; // Minimum data points we want to display
  const maxAttempts = 5; // Maximum extension attempts to prevent infinite loops
  let currentRangeHours = timeRange === '24h' ? 24 : 7 * 24;
  let attempts = 0;
  let readings = [];
  let sufficientData = false;
  
  // Only extend time range if we need more data points
  while (!sufficientData && attempts < maxAttempts) {
    try {
      startDate = new Date(now.getTime() - currentRangeHours * 60 * 60 * 1000);
      
      const queryRef = query(
        collection(db, '3sensor_readings', deviceId, 'readings'),
        where('timestamp', '>=', Timestamp.fromDate(startDate)),
        orderBy('timestamp', 'asc')
      );
      
      const snapshot = await getDocs(queryRef);
      readings = mapSnapshotToReadings(snapshot, deviceId);
      
      // Check if we have enough data points
      if (readings.length >= minDataPoints) {
        sufficientData = true;
      } else {
        // Double the time range for next attempt
        currentRangeHours *= 2;
        attempts++;
      }
    } catch (error) {
      console.error(`Error fetching ${timeRange} data for ${deviceId}:`, error);
      break;
    }
  }
  
  // Sort readings by timestamp and take the last minDataPoints
  readings.sort((a, b) => a.timestamp - b.timestamp);
  if (readings.length > minDataPoints) {
    readings = readings.slice(-minDataPoints);
  }
  
  // Update all target refs with the fetched readings
  targetRefs.forEach(ref => {
    ref.value = readings;
  });

  // Set up real-time listener using the final range
  try {
    const finalQueryRef = query(
      collection(db, '3sensor_readings', deviceId, 'readings'),
      where('timestamp', '>=', Timestamp.fromDate(startDate)),
      orderBy('timestamp', 'asc')
    );
    
    const unsubscribe = onSnapshot(finalQueryRef, (snapshot) => {
      const updatedReadings = mapSnapshotToReadings(snapshot, deviceId);
      
      // Sort and take last minDataPoints
      updatedReadings.sort((a, b) => a.timestamp - b.timestamp);
      let finalReadings = updatedReadings;
      if (updatedReadings.length > minDataPoints) {
        finalReadings = updatedReadings.slice(-minDataPoints);
      }
      
      targetRefs.forEach(ref => {
        ref.value = finalReadings;
      });
    });

    firestoreListenersUnsubscribers.value.push(unsubscribe);
    return readings;
  } catch (error) {
    console.error(`Error setting up real-time listener for ${deviceId}:`, error);
    return readings;
  }
};

const formatTimeLabel = (timestamp) => {
  const date = timestamp?.toDate?.() || new Date(timestamp);
  return date.toLocaleString('en-US', { 
    month: 'short', 
    day: 'numeric', 
    hour: '2-digit', 
    minute: '2-digit',
    hour12: true 
  });
};

const formatDateLabel = (timestamp) => {
  const date = timestamp?.toDate?.() || new Date(timestamp);
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
};

const isInitialChartRender = ref(true);
const isInitialRender = ref(true);

const getFixedPercentageChartOptions = (title) => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20,
          boxWidth: 12
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: ${context.parsed.y}%`;
          }
        }
      }
    },
    scales: {
      y: {
        min: 0,
        max: 100,
        ticks: {
          stepSize: 20,
          callback: function(value) {
            return `${value}%`;
          },
          color: '#6B7280'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#6B7280',
          maxRotation: 0,
          autoSkip: true,
          maxTicksLimit: 6,
          callback: function(value, index, values) {
            // Only show every 3rd label to prevent overcrowding
            return index % 3 === 0 ? this.getLabelForValue(value) : '';
          }
        }
      }
    },
    elements: {
      line: {
        tension: 0.4
      },
      point: {
        radius: 4,
        hoverRadius: 6
      }
    }
  };
};

const initSoilMoistureChart = () => {
  if (!soilMoistureChartRef.value) return;
  try {
    if (soilMoistureChartInstance.value) {
      soilMoistureChartInstance.value.destroy();
    }

    const labels = soilMoistureReadings.value.map(r => formatTimeLabel(r.timestamp));
    const data = soilMoistureReadings.value.map(r => r.soilMoisture || 0);

    soilMoistureChartInstance.value = new Chart(soilMoistureChartRef.value.getContext('2d'), {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Soil Moisture (%)',
          data,
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.1)',
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointBackgroundColor: '#10b981',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.parsed.y}%`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
          },
          y: {
            min: 0,
            max: 100,
            ticks: {
              stepSize: 20,
              callback: (value) => `${value}%`,
              autoSkip: false
            },
          }
        },
        interaction: { mode: 'nearest', axis: 'x', intersect: false },
        elements: { point: { radius: 0, hoverRadius: 8 } },
        animation: { duration: 0 }
      }
    });
  } catch (error) {
    console.error("Error initializing soil moisture chart:", error);
  }
};

const initHumidityChart = () => {
  if (!humidityChartRef.value) return;
  try {
    if (humidityChartInstance.value) {
      humidityChartInstance.value.destroy();
    }

    const labels = humidityReadings.value.map(r => formatTimeLabel(r.timestamp));
    const data = humidityReadings.value.map(r => r.humidity || 0);

    humidityChartInstance.value = new Chart(humidityChartRef.value.getContext('2d'), {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Humidity (%)',
          data,
          borderColor: '#0ea5e9',
          backgroundColor: 'rgba(14, 165, 233, 0.1)',
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointBackgroundColor: '#0ea5e9',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.parsed.y}%`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
          },
          y: {
            min: 0,
            max: 100,
            ticks: {
              stepSize: 20,
              callback: (value) => `${value}%`,
              autoSkip: false
            },
          }
        },
        interaction: { mode: 'nearest', axis: 'x', intersect: false },
        elements: { point: { radius: 0, hoverRadius: 8 } },
        animation: { duration: 0 }
      }
    });
  } catch (error) {
    console.error("Error initializing humidity chart:", error);
  }
};

const initTemperatureChart = () => {
  if (!temperatureChartRef.value) return;
  try {
    if (temperatureChartInstance.value) {
      temperatureChartInstance.value.destroy();
    }

    const labels = temperatureReadings.value.map(r => formatTimeLabel(r.timestamp));
    const data = temperatureReadings.value.map(r => r.temperature || 0);
    const maxY = Math.max(...data, 30);

    temperatureChartInstance.value = new Chart(temperatureChartRef.value.getContext('2d'), {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Temperature (°C)',
          data,
          borderColor: '#ef4444',
          backgroundColor: 'rgba(239, 68, 68, 0.1)',
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointBackgroundColor: '#ef4444',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.parsed.y}°C`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
          },
          y: {
            min: Math.min(...data, 10) - 5,
            max: maxY + 5,
            ticks: {
              callback: (value) => `${value}°C`,
              autoSkip: false
            },
          }
        },
        interaction: { mode: 'nearest', axis: 'x', intersect: false },
        elements: { point: { radius: 0, hoverRadius: 8 } },
        animation: { duration: 0 }
      }
    });
  } catch (error) {
    console.error("Error initializing temperature chart:", error);
  }
};

const initSoilPhChart = () => {
  if (!soilPhChartRef.value) return;  
  try {
    if (soilPhChartInstance.value) {
      soilPhChartInstance.value.destroy();
    }

    const labels = soilPhReadings.value.map(r => formatTimeLabel(r.timestamp));
    const data = soilPhReadings.value.map(r => r.soilPh || 0);
    const minY = Math.min(...data, 1); 
    const maxY = Math.max(...data, 7); 

    soilPhChartInstance.value = new Chart(soilPhChartRef.value.getContext('2d'), {
      type: 'line',
      data: {
        labels,
        datasets: [{
          label: 'Soil pH',
          data,
          borderColor: '#f97316',
          backgroundColor: (context) => {
            const chart = context.chart;
            const {ctx, chartArea} = chart;
            if (!chartArea) return null; // This fixes the error
            return createLinearGradient(ctx, chartArea);
          },
          fill: true,
          tension: 0.4,
          borderWidth: 3,
          pointRadius: 4,
          pointBackgroundColor: '#f97316',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.parsed.y}`
            }
          }
        },
        scales: {
          x: {
            grid: { display: false },
          },
          y: {
            min: minY - 1,
            max: maxY + 1,
            ticks: {
              callback: (value) => value,
              autoSkip: false
            },
          }
        },
        interaction: { mode: 'nearest', axis: 'x', intersect: false },
        elements: { point: { radius: 0, hoverRadius: 8 } },
        animation: { duration: 0 }
      }
    });

    // Helper function for gradient background
    function createLinearGradient(ctx, chartArea) {
      const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
      gradient.addColorStop(0, 'rgba(249, 115, 22, 0.1)');
      gradient.addColorStop(1, 'rgba(249, 115, 22, 0.3)');
      return gradient;
    }
  } catch (error) {
    console.error("Error initializing soil pH chart:", error);
  }
};

const initNpkChart = () => {
  if (!performanceChartRef.value) return;
  
  const readings = npkReadings.value;
  if (readings.length === 0) return;
  
  const labels = readings.map(r => formatTimeLabel(r.timestamp));
  const nitrogenData = readings.map(r => r.nitrogen || 0);
  const phosphorusData = readings.map(r => r.phosphorus || 0);
  const potassiumData = readings.map(r => r.potassium || 0);

  try {
    if (performanceChartInstance.value) {
      performanceChartInstance.value.destroy();
    }

    performanceChartInstance.value = new Chart(performanceChartRef.value.getContext('2d'), {
      type: 'line',
      data: {
        labels,
        datasets: [
          {
            label: 'Nitrogen (mg/kg)',
            data: nitrogenData,
            borderColor: '#4ADE80',
            backgroundColor: 'rgba(74, 222, 128, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointRadius: 4,
            pointBackgroundColor: '#4ADE80',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2
          },
          {
            label: 'Phosphorus (mg/kg)',
            data: phosphorusData,
            borderColor: '#60A5FA',
            backgroundColor: 'rgba(96, 165, 250, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointRadius: 4,
            pointBackgroundColor: '#60A5FA',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2
          },
          {
            label: 'Potassium (mg/kg)',
            data: potassiumData,
            borderColor: '#A78BFA',
            backgroundColor: 'rgba(167, 139, 250, 0.1)',
            fill: true,
            tension: 0.4,
            borderWidth: 3,
            pointRadius: 4,
            pointBackgroundColor: '#A78BFA',
            pointBorderColor: '#ffffff',
            pointBorderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { 
            display: true, 
            position: 'top',
            labels: {
              usePointStyle: true,
              boxWidth: 10,
              padding: 20
            }
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'white',
            titleColor: '#374151',
            bodyColor: '#374151',
            borderColor: '#E5E7EB',
            borderWidth: 1,
            padding: 12,
            displayColors: true
          }
        },
        interaction: { intersect: false, mode: 'index' },
        scales: {
          x: {
            grid: { display: false },
            ticks: { 
              color: '#6B7280',
              autoSkip: false
            }
          },
          y: {
            beginAtZero: true,
            ticks: {
              color: '#6B7280',
              callback: v => v + ' mg/kg'
            },
            grid: { color: '#E5E7EB' }
          }
        }
      }
    });
  } catch (error) {
    console.error("Error initializing NPK chart:", error);
  }
};

const getChartOptions = (title, unit, maxY, beginAtZero = true, minY = 0) => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'top',
        labels: {
          usePointStyle: true,
          padding: 20
        }
      },
      tooltip: {
        callbacks: {
          label: function(context) {
            return `${context.dataset.label}: ${context.parsed.y}${unit}`;
          }
        }
      }
    },
    scales: {
      y: {
        beginAtZero,
        min: minY,
        max: maxY,
        ticks: {
          callback: value => `${value}${unit}`,
          color: '#6B7280'
        },
        grid: {
          color: 'rgba(0, 0, 0, 0.05)'
        }
      },
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#6B7280'
        }
      }
    }
  };
};

// Watchers for chart data
watch(soilMoistureReadings, () => {
  if (soilMoistureChartRef.value) initSoilMoistureChart();
}, { deep: true });

watch(humidityReadings, () => {
  if (humidityChartRef.value) initHumidityChart();
}, { deep: true });

watch(temperatureReadings, () => {
  if (temperatureChartRef.value) initTemperatureChart();
}, { deep: true });

watch(soilPhReadings, () => {
  if (soilPhChartRef.value) initSoilPhChart();
}, { deep: true });

watch(npkReadings, () => {
  if (performanceChartRef.value) initNpkChart();
}, { deep: true });

const initAllCharts = () => {
  initSoilMoistureChart();
  initHumidityChart();
  initTemperatureChart();
  initSoilPhChart();
  initNpkChart();
};

// Destroy all charts
const destroyAllCharts = () => {
  [soilMoistureChartInstance, humidityChartInstance, 
   temperatureChartInstance, soilPhChartInstance, 
   performanceChartInstance].forEach(chart => {
    if (chart.value) {
      chart.value.destroy();
      chart.value = null;
    }
  });
};

onMounted(async () => {
  isLoading.value = true;
  isWeatherLoading.value = true;
  isChartsLoading.value = true;

  // Set up real-time data stream
  setupEventSource();

  // Set fallback timeout (10 seconds)
  streamTimeout.value = setTimeout(() => {
    if (!streamDataReceived.value) {
      console.log("⚡ No stream data received, falling back to Firebase");
      usingFirebaseFallback.value = true;
      fetchLatestSensorDataFromFirebase();
      fetchLatestWaterLevel();
    }
  }, 10000);

  // Set up stream monitor
  const streamMonitorInterval = setInterval(() => {
    if (lastStreamUpdate.value && (new Date() - lastStreamUpdate.value) > 30000) {
      console.log("⚠️ No stream data for 30 seconds, switching to Firebase");
      usingFirebaseFallback.value = true;
      streamConnection.value?.close();
      fetchLatestSensorDataFromFirebase();
      fetchLatestWaterLevel();
      clearInterval(streamMonitorInterval);
    }
  }, 5000);

  // Load initial data
  try {
    await Promise.all([
      loadWeather(),
      fetchDeviceChartData('esp32-2', '24h', [soilMoistureReadings, humidityReadings, temperatureReadings]),
      fetchDeviceChartData('esp32-1', '24h', [soilPhReadings]),
      fetchDeviceChartData('esp32-1', '7d', [npkReadings]),
      fetchMotorStatusData()
    ]);

    // Initialize charts
    isChartsLoading.value = false;
    await nextTick();
    initAllCharts();

  } catch (error) {
    console.error("Initialization error:", error);
  } finally {
    isLoading.value = false;
    isWeatherLoading.value = false;
  }
});

// const getTimeRangeLabel = (readings, isWeekly = false) => {
//   if (readings.length === 0) return isWeekly ? 'No Data' : 'No Recent Data';
  
//   const first = readings[0].timestamp;
//   const last = readings[readings.length - 1].timestamp;
  
//   // Calculate difference in milliseconds
//   const diffMs = Math.abs(last - first);
  
//   if (isWeekly) {
//     const diffDays = Math.ceil(diffMs / (1000 * 60 * 60 * 24));
//     if (diffDays <= 7) return 'Last 7 Days';
//     if (diffDays <= 14) return 'Last 14 Days';
//     return `Last ${diffDays} Days`;
//   }
  
//   // Convert to hours, minutes, seconds
//   const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
//   const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
  
//   if (diffMs < 60000) {
//     // Less than 1 minute
//     const seconds = Math.floor(diffMs / 1000);
//     return `Last ${seconds} Second${seconds !== 1 ? 's' : ''}`;
//   } else if (diffMs < 3600000) {
//     // Less than 1 hour
//     return `Last ${diffMinutes} Minute${diffMinutes !== 1 ? 's' : ''}`;
//   } else if (diffMs < 86400000) {
//     // Less than 24 hours
//     if (diffMinutes === 0) {
//       return `Last ${diffHours} Hour${diffHours !== 1 ? 's' : ''}`;
//     }
//     return `Last ${diffHours}:${diffMinutes.toString().padStart(2, '0')} Hours`;
//   } else {
//     // More than 24 hours
//     const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
//     const remainingHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    
//     if (remainingHours === 0) {
//       return `Last ${diffDays} Day${diffDays !== 1 ? 's' : ''}`;
//     }
//     return `Last ${diffDays} Day${diffDays !== 1 ? 's' : ''} ${remainingHours} Hour${remainingHours !== 1 ? 's' : ''}`;
//   }
// };

const getTimeRangeLabel = (readings, isWeekly = false) => {
  if (!readings || readings.length === 0) return isWeekly ? 'No Data' : 'No Recent Data';
  
  const first = new Date(readings[0].timestamp);
  const last = new Date(readings[readings.length - 1].timestamp);
  
  // Calculate difference in milliseconds
  const diffMs = Math.abs(last - first);
  
  // Convert to days, hours, minutes
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  const diffHours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  const diffMinutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
  
  if (isWeekly) {
    if (diffDays <= 7) return 'Last 7 Days';
    if (diffDays <= 14) return 'Last 14 Days';
    return `Last ${diffDays} Days`;
  }
  
  // Format the time range based on the actual duration
  if (diffDays > 0) {
    if (diffHours > 0) {
      return `Last ${diffDays} Day${diffDays !== 1 ? 's' : ''} ${diffHours} Hour${diffHours !== 1 ? 's' : ''}`;
    }
    return `Last ${diffDays} Day${diffDays !== 1 ? 's' : ''}`;
  }
  
  if (diffHours > 0) {
    if (diffMinutes > 0) {
      return `Last ${diffHours} Hour${diffHours !== 1 ? 's' : ''} ${diffMinutes} Min${diffMinutes !== 1 ? 's' : ''}`;
    }
    return `Last ${diffHours} Hour${diffHours !== 1 ? 's' : ''}`;
  }
  
  if (diffMinutes > 0) {
    return `Last ${diffMinutes} Min${diffMinutes !== 1 ? 's' : ''}`;
  }
  
  const diffSeconds = Math.floor(diffMs / 1000);
  return `Last ${diffSeconds} Sec${diffSeconds !== 1 ? 's' : ''}`;
};


const soilMoistureTimeRange = computed(() => 
  getTimeRangeLabel(soilMoistureReadings.value));

const humidityTimeRange = computed(() => 
  getTimeRangeLabel(humidityReadings.value));

const temperatureTimeRange = computed(() => 
  getTimeRangeLabel(temperatureReadings.value));

const soilPhTimeRange = computed(() => 
  getTimeRangeLabel(soilPhReadings.value));

const npkTimeRange = computed(() => 
  getTimeRangeLabel(npkReadings.value, true));

function getChange(current, previous) {
  const currentVal = parseFloat(current);
  const previousVal = parseFloat(previous);

  if (isNaN(currentVal) || isNaN(previousVal)) {
    return null;
  }

  if (previousVal === 0) {
    if (currentVal === 0) {
      return { direction: 'up', percent: '0.0' };
    }
    return null;
  }

  const diff = currentVal - previousVal;
  const percent = (diff / previousVal) * 100;

  if (isNaN(percent) || !isFinite(percent)) {
    return null;
  }

  return {
    direction: diff >= 0 ? 'up' : 'down',
    percent: Math.abs(percent).toFixed(1)
  };
}

const createChangeComputed = (readingsRef, key) => {
  return computed(() => {
    if (!readingsRef.value || readingsRef.value.length < 2) {
      return null;
    }
    const currentVal = readingsRef.value[readingsRef.value.length - 1]?.[key];
    const previousVal = readingsRef.value[0]?.[key];
    return getChange(currentVal, previousVal);
  });
};

const soilMoistureChange = createChangeComputed(soilMoistureReadings, 'soilMoisture');
const humidityChange = createChangeComputed(humidityReadings, 'humidity');
const temperatureChange = createChangeComputed(temperatureReadings, 'temperature');
const soilPhChange = createChangeComputed(soilPhReadings, 'soilPh');

const latestSoilMoisture = computed(() => soilMoisture.value ?? (soilMoistureReadings.value.length > 0 ? soilMoistureReadings.value[soilMoistureReadings.value.length - 1].soilMoisture : null));
const latestHumidity = computed(() => humidity.value ?? (humidityReadings.value.length > 0 ? humidityReadings.value[humidityReadings.value.length - 1].humidity : null));
const latestTemperature = computed(() => temperature.value ?? (temperatureReadings.value.length > 0 ? temperatureReadings.value[temperatureReadings.value.length - 1].temperature : null));
const latestSoilPh = computed(() => soilpH.value ?? (soilPhReadings.value.length > 0 ? soilPhReadings.value[soilPhReadings.value.length - 1].soilPh : null));

const nitrogenData = computed(() => npkReadings.value.map(r => r.nitrogen || 0));
const phosphorusData = computed(() => npkReadings.value.map(r => r.phosphorus || 0));
const potassiumData = computed(() => npkReadings.value.map(r => r.potassium || 0));

function getSoilMoistureStatus(value) {
  const val = Number(value);
  if (isNaN(val)) {
    return { label: 'No Data', color: 'text-gray-500' };
  }

  if (val <= 30) return { label: 'Too Dry', color: 'text-red-500' };
  if (val <= 55) return { label: 'Moist (Optimal)', color: 'text-emerald-500' };
  if (val <= 75) return { label: 'Wet', color: 'text-yellow-500' };
  return { label: 'Too Wet', color: 'text-blue-500' };
}

function getHumidityStatus(value) {
  const val = Number(value);
  if (isNaN(val)) {
    return { label: 'No Data', color: 'text-gray-500' };
  }

  if (val <= 30) return { label: 'Very Dry', color: 'text-red-500' };
  if (val <= 50) return { label: 'Comfortable', color: 'text-emerald-500' };
  if (val <= 70) return { label: 'Humid', color: 'text-yellow-500' };
  return { label: 'Very Humid', color: 'text-blue-500' };
}

function getTemperatureStatus(value) {
  const val = Number(value);
  if (isNaN(val)) {
    return { label: 'No Data', color: 'text-gray-500' };
  }

  if (val < 20) return { label: 'Too Cold', color: 'text-blue-500' };
  if (val <= 25) return { label: 'Cool', color: 'text-yellow-500' };
  if (val <= 32) return { label: 'Optimal', color: 'text-emerald-500' };
  return { label: 'Too Hot', color: 'text-red-500' };
}

function getPhStatus(value) {
  const val = Number(value);
  if (isNaN(val)) {
    return { label: 'No Data', color: 'text-gray-500' };
  }

  if (val < 3.5) return { label: 'Extremely Acidic', color: 'text-red-600' };
  if (val <= 6.5) return { label: 'Acidic', color: 'text-orange-500' };
  if (val <= 7.3) return { label: 'Neutral (Optimal)', color: 'text-emerald-500' };
  if (val <= 9.0) return { label: 'Alkaline', color: 'text-blue-500' };
  return { label: 'Extremely Alkaline', color: 'text-purple-600' };
}

// Get highest value among all NPK
const maxNpk = computed(() => Math.max(
  ...(nitrogenData.value || [0]),
  ...(phosphorusData.value || [0]),
  ...(potassiumData.value || [0])
));

// Round up to nearest multiple of 10 (for clean y-axis)
const maxY = computed(() => Math.ceil(maxNpk.value / 10) * 10);

const getMaxY = (data, step = 10) => {
  const max = Math.max(...data);
  return Math.ceil(max / step) * step;
};

onBeforeUnmount(() => {
  if (streamConnection.value) {
    streamConnection.value.close();
  }
  
  if (streamTimeout.value) {
    clearTimeout(streamTimeout.value);
  }
  
  try {
    destroyAllCharts();
  } catch (e) {
    console.warn('Error while destroying chart:', e);
  }

  clearInterval(intervalId);
  // Unsubscribe from all Firestore listeners
  firestoreListenersUnsubscribers.value.forEach(unsubscribe => unsubscribe());
  firestoreListenersUnsubscribers.value = []; // Clear the array
  console.log("🚫 Unsubscribed from all Firestore listeners.");
})

const weatherDetails = computed(() => [
  {
    label: 'Humidity',
    value: `${weather.value?.humidity}%`,
    icon: Droplets,
  },
  {
    label: 'Wind',
    value: `${weather.value?.wind_speed} m/s`,
    icon: Wind,
  },
  {
    label: 'Precipitation',
    value: `${weather.value?.precipitation} mm`,
    icon: CloudRain,
  },
  {
    label: 'UV Index',
    value: weather.value?.uv_index?.toFixed(1),
    icon: Sun,
  },
]);

// Add new helper function for weather icon colors
const getWeatherIconColor = (weather) => {
  switch (weather) {
    case 'sunny':
      return 'text-amber-400';
    case 'partly-cloudy':
      return 'text-blue-400';
    case 'cloudy':
      return 'text-gray-400';
    case 'rainy':
      return 'text-blue-500';
    case 'stormy':
      return 'text-indigo-600';
    case 'drizzle':
      return 'text-blue-400';
    default:
      return 'text-blue-500';
  }
};

const getWeatherIcon = (condition) => {
  switch (condition) {
    case 'Clear':
    case 'Mainly Clear':
      return Sun
    case 'Partly Cloudy':
      return CloudSun
    case 'Overcast':
      return Cloud
    case 'Fog':
    case 'Depositing Rime Fog':
      return Wind
    case 'Light Drizzle':
    case 'Moderate Drizzle':
    case 'Dense Drizzle':
      return CloudDrizzle
    case 'Light Rain':
    case 'Moderate Rain':
    case 'Heavy Rain':
    case 'Rain Showers':
    case 'Heavy Rain Showers':
    case 'Violent Rain Showers':
      return CloudRain
    case 'Light Snowfall':
    case 'Moderate Snowfall':
    case 'Heavy Snowfall':
      return Cloud
    case 'Thunderstorm':
    case 'Thunderstorm with Hail':
    case 'Severe Thunderstorm':
      return CloudLightning
    default:
      return Cloud
  }
}

// Add new helper function for detail icon colors
const getDetailIconColor = (label) => {
  switch (label) {
    case 'Humidity':
      return 'text-blue-500';
    case 'Wind Speed':
      return 'text-teal-500';
    case 'Precipitation':
      return 'text-indigo-500';
    case 'UV Index':
      return 'text-amber-500';
    default:
      return 'text-gray-500';
  }
};

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Enhanced scrollbar styling */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: rgba(20, 83, 45, 0.1);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(20, 83, 45, 0.5);
  border-radius: 4px;
  transition: background-color 200ms;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(20, 83, 45, 0.7);
}

/* Smooth transitions */
* {
  transition: all 200ms ease-in-out;
}

/* Ensure proper layout on different browsers */
@supports (-webkit-touch-callout: none) {
  .h-screen {
    height: -webkit-fill-available;
  }
}

/* Firefox scrollbar styling */
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(20, 83, 45, 0.5) rgba(20, 83, 45, 0.1);
}

/* Weather card styles */
.weather-card-gradient {
  background: linear-gradient(
    135deg,
    rgba(186, 230, 253, 0.2) 0%,
    rgba(147, 197, 253, 0.3) 100%
  );
}

/* Glassmorphism effects */
.glass-effect {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}

/* Weather icon animations */
@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0);
  }
  50% {
    transform: translateY(-6px) rotate(2deg);
  }
}

.weather-icon-wrapper {
  position: relative;
  padding: 1rem;
  border-radius: 50%;
  background: rgba(243, 244, 246, 0.5);
  transition: all 0.3s ease;
}

.weather-icon-wrapper:hover {
  background: rgba(243, 244, 246, 0.8);
  transform: translateY(-2px);
}

.weather-icon-wrapper svg {
  animation: float 3s ease-in-out infinite;
}

/* Temperature gradient text */
.temperature-text {
  background: linear-gradient(135deg, #f97316, #ef4444);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Water tank styles */
.water-tank-container {
  perspective: 1200px;
}

.water-tank {
  transform: rotateX(12deg) rotateY(-22deg);
  transform-style: preserve-3d;
  transition: all 0.4s ease;
}

.water-tank:hover {
  transform: rotateX(15deg) rotateY(-28deg) scale(1.05);
  filter: drop-shadow(0 20px 30px rgba(59, 130, 246, 0.1));
}

/* Power button styles */
.power-button-container {
  perspective: 1000px;
}

.power-button {
  transform: translateZ(0) rotateX(10deg);
  transform-style: preserve-3d;
  transition: all 0.4s ease;
}

.power-button:hover {
  transform: translateZ(10px) rotateX(15deg) scale(1.05);
}

.power-button:active {
  transform: translateZ(0) rotateX(10deg) scale(0.95);
}

.power-on {
  box-shadow: 
    0 0 0 2px rgba(168, 85, 247, 0.5),
    0 0 20px 5px rgba(168, 85, 247, 0.5),
    0 0 0 4px rgba(168, 85, 247, 0.3);
}

.power-off {
  box-shadow: 
    0 0 0 2px rgba(168, 85, 247, 0.3),
    0 0 15px 2px rgba(168, 85, 247, 0.2),
    0 0 0 4px rgba(168, 85, 247, 0.1);
}

@keyframes pulse {
  0%, 100% {
    opacity: 0.3;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Chart container styles */
.chart-container {
  position: relative;
  transition: all 0.3s ease;
}

.chart-container:hover {
  transform: scale(1.02);
}

/* Enhanced tooltip styling */
.chartjs-tooltip {
  background-color: rgba(255, 255, 255, 0.95) !important;
  backdrop-filter: blur(8px);
  border-radius: 8px !important;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
}

/* NPK Levels card styles */
.npk-card {
  transition: all 0.3s ease;
}

.npk-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
}

/* Responsive design adjustments */
@media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 250px;
  }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Accessibility improvements */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

/* Focus styles for better keyboard navigation */
:focus-visible {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Print styles for better readability when printed */
@media print {
  body {
    font-size: 12pt;
  }

  .chart-container {
    break-inside: avoid;
  }

  .no-print {
    display: none;
  }
}

@keyframes longWave1 {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
@keyframes longWave2 {
  0% { transform: translateX(0); }
  100% { transform: translateX(-60%); }
}
@keyframes longWave3 {
  0% { transform: translateX(0); }
  100% { transform: translateX(-70%); }
}

.animate-long-wave-1 {
  animation: longWave1 4s linear infinite;
}
.animate-long-wave-2 {
  animation: longWave2 7s linear infinite;
}
.animate-long-wave-3 {
  animation: longWave3 10s linear infinite;
}

.tank-style {
  background: linear-gradient(to top, #e0f2fe, #f8fafc);
  box-shadow:
    inset 0 0 15px rgba(59, 130, 246, 0.2),
    0 10px 20px rgba(0, 0, 0, 0.05);
  border-radius: 2rem;
}

html, body {
  width: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* Make sure all containers expand to full width */
.w-full {
  width: 100%;
}

/* Remove any horizontal padding that might constrain width */
.px-0 {
  padding-left: 0;
  padding-right: 0;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .main-content {
    padding-left: 0;
    padding-right: 0;
  }
  
  .grid-cols-7 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

/* Smooth transitions for layout changes */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}
</style>