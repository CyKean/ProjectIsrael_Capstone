<template>
  <!-- Container Wrapper with proper spacing -->
  <div class="flex-1 w-full px-2 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
    <!-- Main Container with adjusted width -->
    <div class=" bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-green-100 w-[calc(100vw-15px)] h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] overflow-x-hidden">
      <!-- Content Wrapper -->
      <div class="p-2 md:p-6">
        <!-- Find the Top Metrics Cards section and replace it with this updated version -->

        <!-- Top Metrics Cards - Conditional Rendering -->
        <div v-if="!isLoading" class="grid grid-cols-3 sm:grid-cols-3 lg:grid-cols-7 gap-2 md:gap-4 mb-4 md:mb-8">
          <!-- Nitrogen Level Card -->
          <div class="group bg-white rounded-xl p-3 md:p-4 border-2 border-green-100 shadow-lg transition-all duration-300 hover:border-green-400 hover:shadow-xl hover:-translate-y-1">
            <div class="flex items-center justify-between mb-2">
              <Leaf class="h-5 w-5 text-green-500 transition-transform duration-300 group-hover:scale-110" />
              <span class="text-[9px] md:text-xs font-semibold text-green-600 bg-green-100 px-2 py-0.5 rounded-full">N</span>
            </div>
            <div class="text-xl font-bold text-green-700">{{ nitrogen }}</div>
            <div class="text-[7.5px] md:text-xs text-green-600">Nitrogen (mg/kg)</div>
          </div>

          <!-- Phosphorus Level Card -->
          <div class="group bg-white rounded-xl p-3 md:p-4 border-2 border-blue-100 shadow-lg transition-all duration-300 hover:border-blue-400 hover:shadow-xl hover:-translate-y-1">
            <div class="flex items-center justify-between mb-2">
              <TestTube class="h-5 w-5 text-blue-500 transition-transform duration-300 group-hover:scale-110" />
              <span class="text-[9px] md:text-xs font-semibold text-blue-600 bg-blue-100 px-2 py-0.5 rounded-full">P</span>
            </div>
            <div class="text-xl font-bold text-blue-700">{{ phosphorus }}</div>
            <div class="text-[7.5px] md:text-xs text-blue-600">Phosphorus (mg/kg)</div>
          </div>

          <!-- Potassium Level Card -->
          <div class="group bg-white rounded-xl p-3 md:p-4 border-2 border-purple-100 shadow-lg transition-all duration-300 hover:border-purple-400 hover:shadow-xl hover:-translate-y-1">
            <div class="flex items-center justify-between mb-2">
              <TestTubes class="h-5 w-5 text-purple-500 transition-transform duration-300 group-hover:scale-110" />
              <span class="text-[9px] md:text-xs font-semibold text-purple-600 bg-purple-100 px-2 py-0.5 rounded-full">K</span>
            </div>
            <div class="text-xl font-bold text-purple-700">{{ potassium }}</div>
            <div class="text-[7.5px] md:text-xs text-purple-600">Potassium (mg/kg)</div>
          </div>

          <!-- Soil pH Level Card -->
          <div class="group bg-white rounded-xl p-3 md:p-4 border-2 border-orange-100 shadow-lg transition-all duration-300 hover:border-orange-400 hover:shadow-xl hover:-translate-y-1">
            <div class="flex items-center justify-between mb-2">
              <Beaker class="h-5 w-5 text-orange-500 transition-transform duration-300 group-hover:scale-110" />
              <span class="text-[9px] md:text-xs font-semibold text-orange-600 bg-orange-100 px-2 py-0.5 rounded-full">pH</span>
            </div>
            <div class="text-xl font-bold text-orange-700">{{ soilpH }}</div>
            <div class="text-[7.5px] md:text-xs text-orange-600">Soil pH Level</div>
          </div>

          <!-- Soil Moisture Card -->
          <div class="group bg-white rounded-xl p-3 md:p-4 border-2 border-emerald-100 shadow-lg transition-all duration-300 hover:border-emerald-400 hover:shadow-xl hover:-translate-y-1">
            <div class="flex items-center justify-between mb-2">
              <Sprout class="h-5 w-5 text-emerald-500 transition-transform duration-300 group-hover:scale-110" />
              <span class="text-[9px] md:text-xs font-semibold text-emerald-600 bg-emerald-100 px-2 py-0.5 rounded-full">SM</span>
            </div>
            <div class="text-xl font-bold text-emerald-700">{{ soilMoisture }}</div>
            <div class="text-[7.5px] md:text-xs text-emerald-600">Soil Moisture</div>
          </div>

          <!-- Temperature Card -->
          <div class="group bg-white rounded-xl p-3 md:p-4 border-2 border-red-100 shadow-lg transition-all duration-300 hover:border-red-400 hover:shadow-xl hover:-translate-y-1">
            <div class="flex items-center justify-between mb-2">
              <Thermometer class="h-5 w-5 text-red-500 transition-transform duration-300 group-hover:scale-110" />
              <span class="text-[9px] md:text-xs font-semibold text-red-600 bg-red-100 px-2 py-0.5 rounded-full">Temp</span>
            </div>
            <div class="text-xl font-bold text-red-700">{{ temperature }}</div>
            <div class="text-[7.5px] md:text-xs text-red-600">Temperature (°C)</div>
          </div>

          <!-- Humidity Card -->
          <div class="group bg-white rounded-xl p-3 md:p-4 border-2 border-sky-100 shadow-lg transition-all duration-300 hover:border-sky-400 hover:shadow-xl hover:-translate-y-1">
            <div class="flex items-center justify-between mb-2">
              <Droplets class="h-5 w-5 text-sky-500 transition-transform duration-300 group-hover:scale-110" />
              <span class="text-[9px] md:text-xs font-semibold text-sky-600 bg-sky-100 px-2 py-0.5 rounded-full">RH</span>
            </div>
            <div class="text-xl font-bold text-sky-700">{{ humidity }}</div>
            <div class="text-[7.5px] md:text-xs text-sky-600">Humidity (%)</div>
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
            <!-- <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-blue-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
              <div class="flex justify-between items-center mb-4">
                <div class="flex items-center bg-blue-50 rounded-full px-2.5 py-1 shadow-inner space-x-1.5">
                  <Waves class="w-4 h-4 text-blue-500" />
                  <h3 class="text-xs md:text-sm font-semibold text-blue-700 tracking-wide">Water Level</h3>
                </div>
                <div class="bg-blue-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">LIVE</div>
              </div>

              <div class="relative w-64 h-80 mx-auto mt-4">
                <div class="relative w-[80%] h-full md:w-full md:h-full rounded-[2rem] border-[6px] border-blue-300 bg-white shadow-2xl overflow-hidden tank-style">
                  <div class="absolute bottom-0 left-0 w-full h-full z-10 overflow-hidden">
                    <div
                      class="absolute top-0 left-0 w-full h-full transition-transform duration-700 ease-in-out"
                      :style="{ transform: `translateY(${100 - waterLevel}%)` }"
                    >
                      <div class="relative w-[900%] h-full">
                        <div class="absolute w-full h-full left-0 top-0 animate-long-wave-1">
                          <svg viewBox="0 0 1200 300" preserveAspectRatio="none" class="w-full h-full">
                            <path
                              d="M0,0 C200,60 400,-60 600,0 C800,60 1000,-60 1200,0 L1200,300 L0,300 Z"
                              fill="#3B82F6" fill-opacity="0.6"
                            />
                          </svg>
                        </div>
                        <div class="absolute w-full h-full left-0 top-0 animate-long-wave-2">
                          <svg viewBox="0 0 1200 300" preserveAspectRatio="none" class="w-full h-full">
                            <path
                              d="M0,0 C200,50 400,-50 600,0 C800,50 1000,-50 1200,0 L1200,300 L0,300 Z"
                              fill="#60A5FA" fill-opacity="0.4"
                            />
                          </svg>
                        </div>
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

                  <div class="absolute inset-0 flex items-center justify-center z-20">
                    <div class="bg-white/80 backdrop-blur px-4 py-2 rounded-xl shadow-lg border border-blue-100">
                      <span v-if="!isChartsLoading" class="text-4xl font-bold text-blue-600">{{ waterLevel }}%</span>
                      <span v-else class="text-4xl font-bold text-blue-600">
                        <div class="h-8 w-16 bg-gray-300 rounded animate-pulse"></div>
                      </span>
                    </div>
                  </div>
                </div>

                <div class="absolute top-2 bottom-2 left-1/2 -translate-x-[-5rem] md:-translate-x-[-8rem] md:-right-14 w-10 flex flex-col justify-between z-30">
                  <div v-for="n in 5" :key="n" class="flex items-center gap-2">
                    <div class="h-[2px] w-4 bg-blue-400 shadow-sm"></div>
                    <span class="text-sm font-medium text-blue-600 bg-white/90 px-1 rounded">
                      {{ 100 - (n - 1) * 25 }}%
                    </span>
                  </div>
                </div>
              </div>
            </div> -->

            <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-blue-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300">
              <!-- Header -->
              <div class="flex justify-between items-center mb-4">
                <div class="flex items-center bg-blue-50 rounded-full px-2.5 py-1 shadow-inner space-x-1.5">
                  <Waves class="w-4 h-4 text-blue-500" />
                  <h3 class="text-xs md:text-sm font-semibold text-blue-700 tracking-wide">Water Level</h3>
                </div>
                <div class="bg-blue-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">LIVE</div>
              </div>

              <!-- Water Tank Container -->
              <div class="flex justify-center items-start md:mt-8">
                <!-- Level Markers - Left Side -->
                <div class="h-80 flex flex-col justify-between pt-2 pb-2 mr-2 z-30">
                  <div v-for="n in 5" :key="n" class="flex items-center gap-2">
                    <span class="text-xs md:text-sm font-medium text-blue-600 bg-white/90 px-1 rounded whitespace-nowrap">
                      {{ 100 - (n - 1) * 25 }}%
                    </span>
                    <div class="h-[2px] w-4 bg-blue-400 shadow-sm"></div>
                  </div>
                </div>

                <!-- Water Tank -->
                <div class="relative w-64 h-80">
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
                </div>

              </div>
            </div>

            <!-- Motor Status Card with Loading State -->
            <div v-if="!isChartsLoading" class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-purple-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
              <!-- Header section -->
              <div class="flex flex-col items-start space-y-2 mb-4">
                <div class="flex items-center justify-between w-full">
                  <div class="bg-purple-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                    <Power class="w-4 h-4 text-purple-500" />
                    <h3 class="text-xs md:text-sm font-semibold text-purple-700 tracking-wide">Motor Status</h3>
                  </div>
                  <div class="bg-purple-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                    WEEKLY
                  </div>
                </div>
                <div class="w-full">
                  <p class="text-[10px] md:text-xs text-purple-600 font-medium bg-purple-100 px-3 py-1 rounded-full shadow-sm inline-block">
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
                  <div class="text-[10px] md:text-xs text-purple-700 mb-1">ON</div>
                  <div class="text-md md:text-lg font-bold text-purple-800">{{ motorOnPercentage.toFixed(1) }}%</div>
                </div>
                
                <!-- OFF Percentage Label -->
                <div class="absolute top-1/2 right-0 -translate-y-1/2 translate-x-1/2 text-center w-16 bg-purple-200 rounded-md border-2 border-purple-500">
                  <div class="text-[10px] md:text-xs text-purple-700 mb-1">OFF</div>
                  <div class="text-md md:text-lg font-bold text-purple-800">{{ (100 - motorOnPercentage).toFixed(1) }}%</div>
                </div>
                
              </div>

              <!-- Status Information -->
              <div class="mt-6 text-center">
                <p class="text-sm md:text-base font-semibold text-purple-600">
                  Motor was <span class="text-purple-700 font-bold">ON</span> for <span class="text-purple-700 font-bold">{{ motorOnPercentage.toFixed(1) }}%</span> of the week
                </p>
                <p class="text-xs md:text-sm text-purple-600 mt-1">
                  Total runtime: {{ (motorOnPercentage * 1.68).toFixed(1) }} hours
                </p>
              </div>

              <!-- Weekly Breakdown -->
              <div class="mt-4">
                <h4 class="text-[10px] md:text-xs font-semibold text-purple-700 mb-2">Weekly Breakdown</h4>
                <div class="grid grid-cols-4 md:grid-cols-7 gap-2 md:gap-1">
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
            <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-blue-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 overflow-hidden">
              <div class="flex justify-between items-start mb-4">
                <div class="flex items-center justify-between w-full">
                  <div class="bg-sky-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                    <CloudSun class="w-4 h-4 text-sky-500" />
                    <h3 class="text-xs md:text-sm font-semibold text-sky-700 tracking-wide">Weather Forecast</h3>
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
                <div class="grid grid-cols-4 md:grid-cols-7 gap-1">
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
            <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-emerald-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
              <!-- Header section with adjusted text sizes and spacing -->
              <div class="flex flex-col items-start space-y-2 mb-4">
                <div class="flex items-center justify-between w-full">
                  <div class="bg-emerald-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                    <Sprout class="w-4 h-4 text-emerald-500" />
                    <h3 class="text-xs md:text-sm font-semibold text-emerald-700 tracking-wide">Soil Moisture</h3>
                  </div>
                  <div class="bg-emerald-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                    LIVE
                  </div>
                </div>
                <div class="w-full">
                  <p class="text-[10px] md:text-xs text-emerald-600 font-medium bg-emerald-100 px-3 py-1 rounded-full shadow-sm inline-block">
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
                      class="ml-2 text-[10px] md:text-sm font-medium"
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
                      class="text-[10px] md:text-xs font-medium"
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
              <div class="bg-white rounded-xl p-2 md:p-4 border border-emerald-100">
                <div class="h-[200px] md:h-[180px]">
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
            <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-sky-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
              <!-- Header section with adjusted text sizes and spacing -->
              <div class="flex flex-col items-start space-y-2 mb-4">
                <div class="flex items-center justify-between w-full">
                  <div class="bg-sky-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                    <Droplets class="w-4 h-4 text-sky-500" />
                    <h3 class="text-xs md:text-sm font-semibold text-sky-700 tracking-wide">Humidity</h3>
                  </div>
                  <div class="bg-sky-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                    LIVE
                  </div>
                </div>
                <div class="w-full">
                  <p class="text-[10px] md:text-xs text-sky-600 font-medium bg-sky-100 px-3 py-1 rounded-full shadow-sm inline-block">
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
                      class="ml-2 text-[10px] md:text-sm font-medium"
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
                      class="text-[10px] md:text-xs font-medium"
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
              <div class="bg-white rounded-xl p-2 md:p-4 border border-sky-100">
                <div class="h-[200px] md:h-[180px]">
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
            <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-red-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
              <!-- Header section with adjusted text sizes and spacing -->
              <div class="flex flex-col items-start space-y-2 mb-4">
                <div class="flex items-center justify-between w-full">
                  <div class="bg-red-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                    <Thermometer class="w-4 h-4 text-red-500" />
                    <h3 class="text-xs md:text-sm font-semibold text-red-700 tracking-wide">Temperature</h3>
                  </div>
                  <div class="bg-red-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                    LIVE
                  </div>
                </div>
                <div class="w-full">
                  <p class="text-[10px] md:text-xs text-red-600 font-medium bg-red-100 px-3 py-1 rounded-full shadow-sm inline-block">
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
                      class="ml-2 text-xs md:text-sm font-medium"
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
                      class="text-[10px] md:text-xs font-medium"
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
              <div class="bg-white rounded-xl p-2 md:p-4 border border-red-100">
                <div class="h-[200px] md:h-[180px]">
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
            <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-orange-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
              <!-- Header section with adjusted text sizes and spacing -->
              <div class="flex flex-col items-start space-y-2 mb-4">
                <div class="flex items-center justify-between w-full">
                  <div class="bg-orange-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                    <Beaker class="w-4 h-4 text-orange-500" />
                    <h3 class="text-xs md:text-sm font-semibold text-orange-700 tracking-wide">Soil pH</h3>
                  </div>
                  <div class="bg-orange-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                    LIVE
                  </div>
                </div>
                <div class="w-full">
                  <p class="text-[10px] md:text-xs text-orange-600 font-medium bg-orange-100 px-3 py-1 rounded-full shadow-sm inline-block">
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
                      class="ml-2 text-xs md:text-sm font-medium"
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
                        class="text-[10px] md:text-xs font-medium"
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
              <div class="bg-white rounded-xl p-2 md:p-4 border border-orange-100">
                <div class="h-[200px] md:h-[180px]">
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
          <div class="bg-white rounded-2xl p-4 md:p-6 shadow-lg border border-green-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1">
            <!-- Enhanced Header section with adjusted text sizes and spacing -->
            <div class="flex flex-col items-start space-y-2 mb-6">
              <div class="flex items-center justify-between w-full">
                <div class="bg-green-50 rounded-full px-2.5 py-1 flex items-center space-x-1.5 shadow-inner">
                  <FlaskConical class="w-4 h-4 text-green-500" />
                  <h3 class="text-xs md:text-sm font-semibold text-green-700 tracking-wide">NPK Levels</h3>
                </div>
                <div class="bg-green-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                  WEEKLY
                </div>
              </div>
              <div class="w-full">
                <p class="text-[10px] md:text-xs text-green-600 font-medium bg-green-100 px-3 py-1 rounded-full shadow-sm inline-block">
                  {{ npkTimeRange }}
                </p>
              </div>
            </div>

            <!-- Enhanced Circular Progress Section -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-2 md:gap-6 mb-2 md:mb-8">
              <div
                v-for="(npk, index) in normalizedNpkLevels"
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
                        :stroke-dashoffset="getDashOffset(npk.percentage)"
                        stroke-linecap="round"
                        fill="transparent"
                        r="56"
                        cx="64"
                        cy="64"
                      >
                        <animate
                          attributeName="stroke-dashoffset"
                          :from="circumference"
                          :to="getDashOffset(npk.percentage)"
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
                        {{ npk.percentage.toFixed(1) }}%
                      </span>
                      <span :class="`text-sm font-medium text-${npk.color}-600 mt-1`">
                        {{ npk.title }}
                      </span>
                      <span :class="`text-xs text-${npk.color}-500 mt-1`">
                        {{ npk.displayValue }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Enhanced Chart Container -->
            <div class="bg-white rounded-xl p-2 md:p-4 border border-green-100 transition-all duration-300 hover:shadow-md">
              <div class="h:[400px] md:h-[300px]">
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
import { getWeatherData } from '../../utils/weather';
import api from '../../api/index.js'

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

const soilMoistureChartInstance = ref(null);
const humidityChartInstance = ref(null);
const temperatureChartInstance = ref(null);
const soilPhChartInstance = ref(null);
const performanceChartInstance = ref(null);

const performanceChartRef = ref(null);
const soilMoistureChartRef = ref(null);
const humidityChartRef = ref(null);
const temperatureChartRef = ref(null);
const soilPhChartRef = ref(null);

const motorStatus = ref(false);
const motorOnPercentage = ref(0); 

const circumference = 2 * Math.PI * 48; 

const weatherData = ref({})
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

const totalNpk = computed(() => avgNitrogen.value + avgPhosphorus.value + avgPotassium.value);

const normalizedNpkLevels = computed(() => {
  if (!npkReadings.value || npkReadings.value.length === 0) {
    return [
      { title: 'Nitrogen', value: 0, displayValue: '0 mg/kg', color: 'green', percentage: 0 },
      { title: 'Phosphorus', value: 0, displayValue: '0 mg/kg', color: 'blue', percentage: 0 },
      { title: 'Potassium', value: 0, displayValue: '0 mg/kg', color: 'purple', percentage: 0 }
    ];
  }

  const latest = npkReadings.value[npkReadings.value.length - 1];
  
  const nitrogenVal = latest.nitrogen || 0;
  const phosphorusVal = latest.phosphorus || 0;
  const potassiumVal = latest.potassium || 0;
  
  const total = nitrogenVal + phosphorusVal + potassiumVal;
  
  const nitrogenPercent = total > 0 ? (nitrogenVal / total) * 100 : 0;
  const phosphorusPercent = total > 0 ? (phosphorusVal / total) * 100 : 0;
  const potassiumPercent = total > 0 ? (potassiumVal / total) * 100 : 0;

  return [
    {
      title: 'Nitrogen',
      value: nitrogenVal,
      percentage: nitrogenPercent,
      displayValue: `${nitrogenVal} mg/kg`,
      color: 'green',
    },
    {
      title: 'Phosphorus',
      value: phosphorusVal,
      percentage: phosphorusPercent,
      displayValue: `${phosphorusVal} mg/kg`,
      color: 'blue',
    },
    {
      title: 'Potassium',
      value: potassiumVal,
      percentage: potassiumPercent,
      displayValue: `${potassiumVal} mg/kg`,
      color: 'purple',
    },
  ];
});

const npkLevels = ref([
  {
    title: 'Nitrogen',
    value: 0,
    displayValue: '0 mg/kg',
    color: 'green',
  },
  {
    title: 'Phosphorus',
    value: 0,
    displayValue: '0 mg/kg',
    color: 'blue',
  },
  {
    title: 'Potassium',
    value: 0,
    displayValue: '0 mg/kg',
    color: 'purple',
  },
]);

const updateNpkLevels = () => {
  if (!npkReadings.value || npkReadings.value.length === 0) {
    console.log('No NPK readings available');
    return;
  }
  
  const latest = npkReadings.value[npkReadings.value.length - 1];
  
  npkLevels.value = [
    {
      title: 'Nitrogen',
      value: latest.nitrogen || 0,
      displayValue: `${latest.nitrogen || 0} mg/kg`,
      color: 'green',
    },
    {
      title: 'Phosphorus',
      value: latest.phosphorus || 0,
      displayValue: `${latest.phosphorus || 0} mg/kg`,
      color: 'blue',
    },
    {
      title: 'Potassium',
      value: latest.potassium || 0,
      displayValue: `${latest.potassium || 0} mg/kg`,
      color: 'purple',
    },
  ];
  
  console.log('Updated NPK levels:', npkLevels.value);
};

watch(npkReadings, () => {
  updateNpkLevels();
}, { deep: true });

const getDashOffset = (value) => {
  const numericValue = Number(value) || 0;
  
  const normalizedValue = Math.min(Math.max(numericValue, 0), 100);
  
  return circumference - (normalizedValue / 100) * circumference;
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

const API_BASE = 'http://localhost:8000/api';

const setupEventSource = () => {
  try {
    streamConnection.value = new EventSource(`${API_BASE}/stream`);
    
    streamConnection.value.onmessage = (event) => {
      streamDataReceived.value = true;
      lastStreamUpdate.value = new Date();
      
      if (streamTimeout.value) clearTimeout(streamTimeout.value);
      
      const data = JSON.parse(event.data);
      console.log("📡 Received real-time data:", data);

      // Update metrics from stream data
      if (data.type === 'esp32-1') {
        nitrogen.value = data.data.nitrogen || 0;
        phosphorus.value = data.data.phosphorus || 0;
        potassium.value = data.data.potassium || 0;
        soilpH.value = data.data.soilPh || 7.0;
      } 
      else if (data.type === 'esp32-2') {
        temperature.value = data.data.temperature || 0;
        humidity.value = data.data.humidity || 0;
        soilMoisture.value = data.data.soilMoisture || 0;
      }
      else if (data.type === 'esp32-3') {
        waterLevel.value = data.data.waterLevel || 0;
      }

      updateChartDataFromStream(data);
    };

    streamConnection.value.onerror = (e) => {
      console.error("❌ SSE Error:", e);
      if (!streamDataReceived.value) {
        console.log("⚡ Stream error, falling back to regular API");
        fetchLatestSensorData();
        fetchLatestWaterLevel();
      }
    };

  } catch (error) {
    console.error("❌ Error setting up EventSource:", error);
    fetchLatestSensorData();
    fetchLatestWaterLevel();
  }
};

const fetchLatestSensorData = async () => {
  try {
    const response = await api.get('/sensor-data/latest');
    const data = response.data;
    
    // Update all device data
    if (data['esp32-1']) {
      nitrogen.value = data['esp32-1'].nitrogen || 0;
      phosphorus.value = data['esp32-1'].phosphorus || 0;
      potassium.value = data['esp32-1'].potassium || 0;
      soilpH.value = data['esp32-1'].soilPh || 7.0;
    }
    
    if (data['esp32-2']) {
      temperature.value = data['esp32-2'].temperature || 0;
      humidity.value = data['esp32-2'].humidity || 0;
      soilMoisture.value = data['esp32-2'].soilMoisture || 0;
    }
    
  } catch (error) {
    console.error("❌ Error fetching sensor data:", error);
  }
};

const fetchLatestWaterLevel = async () => {
  try {
    const response = await api.get('/water-level/latest');
    waterLevel.value = response.data.waterLevel || 0;
    console.log("💧 Latest Water Level:", waterLevel.value);
  } catch (error) {
    console.error("❌ Error fetching water level:", error);
  }
};

const fetchMotorStatusData = async () => {
  try {
    // Get current motor status
    const statusResponse = await api.get('/motor-status/current');
    motorStatus.value = statusResponse.data.status || false;

    // Get history logs
    const historyResponse = await api.get('/motor-status/history?week_only=true');
    const logs = historyResponse.data;

    // Ensure logs is an array
    if (!Array.isArray(logs)) {
      console.warn('Motor history API did not return an array:', logs);
      weeklyData.value = [];
      motorOnPercentage.value = 0;
      return;
    }

    // Filter this week's logs
    const now = new Date();
    const startOfWeek = new Date(now);
    startOfWeek.setDate(now.getDate() - now.getDay());
    startOfWeek.setHours(0, 0, 0, 0);

    const thisWeekLogs = logs.filter(log => {
      const ts = new Date(log.timestamp || now);
      return ts >= startOfWeek;
    });

    // Compute % of time ON per day
    const dailyOnCounts = Array(7).fill(0);
    const dailyTotalLogs = Array(7).fill(0);

    thisWeekLogs.forEach(log => {
      const ts = new Date(log.timestamp || now);
      const dayIndex = ts.getDay();
      dailyTotalLogs[dayIndex]++;
      if (log.status === true) {
        dailyOnCounts[dayIndex]++;
      }
    });

    const dayLabels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const dailyPercentages = dailyOnCounts.map((onCount, index) => ({
      label: dayLabels[index],
      percentage: dailyTotalLogs[index] > 0 ? (onCount / dailyTotalLogs[index]) * 100 : 0
    }));

    weeklyData.value = dailyPercentages;

    // Calculate overall weekly ON percentage
    const totalOnLogsForWeek = dailyOnCounts.reduce((sum, count) => sum + count, 0);
    const totalLogsForWeek = dailyTotalLogs.reduce((sum, count) => sum + count, 0);
    
    motorOnPercentage.value = totalLogsForWeek > 0 ? (totalOnLogsForWeek / totalLogsForWeek) * 100 : 0;

  } catch (error) {
    console.error('Error fetching motor status and history:', error);
    weeklyData.value = [];
    motorOnPercentage.value = 0;
  }
};

const fetchAllSensorData = async () => {
  try {
    const response = await api.get('/sensor-data/all');
    const data = response.data;
    
    console.log('Fetched all sensor data:', data); // Debug log
    
    // Process NPK data (esp32-1)
    if (data.npkData && Array.isArray(data.npkData)) {
      const npkReadingsData = data.npkData.map(item => ({
        id: `npk-${item.timestamp}`,
        deviceId: 'esp32-1',
        nitrogen: Number(item.nitrogen) || 0,
        phosphorus: Number(item.phosphorus) || 0,
        potassium: Number(item.potassium) || 0,
        soilPh: Number(item.soilPh) || 7.0,
        timestamp: new Date(item.timestamp)
      }));
      
      // Update all relevant refs
      soilPhReadings.value = npkReadingsData;
      npkReadings.value = npkReadingsData;
      
      // Set latest values for display
      if (npkReadingsData.length > 0) {
        const latest = npkReadingsData[npkReadingsData.length - 1];
        nitrogen.value = latest.nitrogen;
        phosphorus.value = latest.phosphorus;
        potassium.value = latest.potassium;
        soilpH.value = latest.soilPh;
        
        console.log('Latest NPK values:', {
          nitrogen: nitrogen.value,
          phosphorus: phosphorus.value,
          potassium: potassium.value,
          soilPh: soilpH.value
        });
      }
    } else {
      console.warn('No NPK data found in response');
    }
    
    // Process Environmental data (esp32-2)
    if (data.envData && Array.isArray(data.envData)) {
      const envReadings = data.envData.map(item => ({
        id: `env-${item.timestamp}`,
        deviceId: 'esp32-2',
        temperature: Number(item.temperature) || 0,
        humidity: Number(item.humidity) || 0,
        soilMoisture: Number(item.soilMoisture) || 0,
        timestamp: new Date(item.timestamp)
      }));
      
      // Update all relevant refs
      soilMoistureReadings.value = envReadings;
      humidityReadings.value = envReadings;
      temperatureReadings.value = envReadings;
      
      // Set latest values for display
      if (envReadings.length > 0) {
        const latest = envReadings[envReadings.length - 1];
        temperature.value = latest.temperature;
        humidity.value = latest.humidity;
        soilMoisture.value = latest.soilMoisture;
        
        console.log('Latest environmental values:', {
          temperature: temperature.value,
          humidity: humidity.value,
          soilMoisture: soilMoisture.value
        });
      }
    } else {
      console.warn('No environmental data found in response');
    }
    
    // Process Water data (esp32-3)
    if (data.waterData && Array.isArray(data.waterData)) {
      const waterReadings = data.waterData.map(item => ({
        id: `water-${item.timestamp}`,
        deviceId: 'esp32-3',
        waterLevel: Number(item.waterLevel) || 0,
        timestamp: new Date(item.timestamp)
      }));
      
      // Set latest water level
      if (waterReadings.length > 0) {
        const latestWaterLevel = waterReadings[waterReadings.length - 1].waterLevel;
        waterLevel.value = Math.min(Math.max(latestWaterLevel, 0), 100); // Ensure between 0-100
        console.log('Water level set to:', waterLevel.value);
      } else {
        console.warn('No water level readings found');
      }
    } else {
      console.warn('No water data found in response');
    }
    
    return true;
  } catch (error) {
    console.error('Error fetching all sensor data:', error);
    return false;
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
  if (!performanceChartRef.value || !npkReadings.value.length) return;
  
  try {
    if (performanceChartInstance.value) {
      performanceChartInstance.value.destroy();
    }

    // Get the last 20 readings for better visibility
    const recentReadings = npkReadings.value.slice(-20);
    const labels = recentReadings.map(r => formatTimeLabel(r.timestamp));
    const nitrogenData = recentReadings.map(r => r.nitrogen || 0);
    const phosphorusData = recentReadings.map(r => r.phosphorus || 0);
    const potassiumData = recentReadings.map(r => r.potassium || 0);

    // Find the maximum value to set appropriate Y-axis scale
    const maxValue = Math.max(
      Math.max(...nitrogenData),
      Math.max(...phosphorusData),
      Math.max(...potassiumData),
      50 // Minimum scale of 50
    );

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
            pointRadius: 3,
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
            pointRadius: 3,
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
            pointRadius: 3,
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
            callbacks: {
              label: function(context) {
                return `${context.dataset.label}: ${context.parsed.y} mg/kg`;
              }
            }
          }
        },
        interaction: { intersect: false, mode: 'index' },
        scales: {
          x: {
            grid: { display: false },
            ticks: { 
              maxTicksLimit: 6,
              callback: function(value, index, values) {
                return index % 3 === 0 ? this.getLabelForValue(value) : '';
              }
            }
          },
          y: {
            beginAtZero: true,
            suggestedMax: maxValue * 1.1, // Add 10% padding
            ticks: {
              callback: v => v + ' mg/kg'
            },
            grid: { color: 'rgba(0, 0, 0, 0.1)' }
          }
        }
      }
    });
  } catch (error) {
    console.error("Error initializing NPK chart:", error);
  }
};

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
  if (soilMoistureChartRef.value && soilMoistureReadings.value.length > 0) {
    initSoilMoistureChart();
  }
  
  if (humidityChartRef.value && humidityReadings.value.length > 0) {
    initHumidityChart();
  }
  
  if (temperatureChartRef.value && temperatureReadings.value.length > 0) {
    initTemperatureChart();
  }
  
  if (soilPhChartRef.value && soilPhReadings.value.length > 0) {
    initSoilPhChart();
  }
  
  if (performanceChartRef.value && npkReadings.value.length > 0) {
    initNpkChart();
  }
};

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

// const debugData = () => {
//   console.log('NPK Readings:', npkReadings.value);
//   console.log('NPK Levels:', npkLevels.value);
//   console.log('Water Level:', waterLevel.value);
//   console.log('Soil Moisture Readings:', soilMoistureReadings.value);
//   console.log('Humidity Readings:', humidityReadings.value);
//   console.log('Temperature Readings:', temperatureReadings.value);
// };

// const debugApiResponse = async () => {
//   try {
//     const response = await api.get('/sensor-data/all');
//     console.log('API Response:', response.data);
    
//     if (response.data.npkData) {
//       console.log('NPK Data:', response.data.npkData);
//       console.log('Latest NPK:', response.data.npkData[response.data.npkData.length - 1]);
//     }
    
//     if (response.data.waterData) {
//       console.log('Water Data:', response.data.waterData);
//       console.log('Latest Water:', response.data.waterData[response.data.waterData.length - 1]);
//     }
//   } catch (error) {
//     console.error('Debug API Error:', error);
//   }
// };

onMounted(async () => {
  isLoading.value = true;
  isWeatherLoading.value = true;
  isChartsLoading.value = true;

  try {
    setupEventSource();

    await Promise.all([
      loadWeather(),
      fetchAllSensorData(),
      fetchMotorStatusData(),
      fetchLatestWaterLevel()
    ]);

    updateNpkLevels();

    isChartsLoading.value = false;
    await nextTick();
    
    setTimeout(() => {
      initAllCharts();
      
      // debugData();
      // debugApiResponse();
    }, 100);

  } catch (error) {
    console.error("Initialization error:", error);
  } finally {
    isLoading.value = false;
    isWeatherLoading.value = false;
  }
});

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

const maxNpk = computed(() => Math.max(
  ...(nitrogenData.value || [0]),
  ...(phosphorusData.value || [0]),
  ...(potassiumData.value || [0])
));

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
  firestoreListenersUnsubscribers.value.forEach(unsubscribe => unsubscribe());
  firestoreListenersUnsubscribers.value = [];
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
/* @media (max-width: 640px) {
  .grid {
    grid-template-columns: 1fr;
  }
  
  .chart-container {
    height: 250px;
  }
} */

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