<template>
      <!-- Container Wrapper -->
      <div class="flex-1 w-full px-4 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
        <!-- Main Container -->
        <div class="bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-green-100 h-[calc(100vh-140px)] overflow-y-auto transition-all duration-300 ease-in-out hover:shadow-[0_12px_40px_rgb(0,0,0,0.12)]">
          <!-- Title Section - Styled like Soil Analysis Measurements with breadcrumb -->
          <div class="p-6 pb-0">
            <h1 class="text-2xl font-bold text-gray-800 mb-2">Weather Forecasting</h1>
            <div class="flex items-center text-sm text-gray-500">
              <span class="text-green-600">Weather Forecast</span>
              <ChevronRight class="h-4 w-4 mx-1" />
              <span>Overview</span>
            </div>
          </div>
          
          <!-- Content Wrapper -->
          <div class="p-6 md:p-8">
            <!-- Top Section: Current Weather & Map -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
              <!-- Current Weather Card -->
              <div class="bg-white rounded-2xl p-6 shadow-lg border border-emerald-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 overflow-hidden flex flex-col">
                <div class="flex justify-between items-start mb-5">
                  <div class="flex items-center justify-between w-full">
                    <div class="bg-emerald-50 rounded-full px-3 py-1.5 flex items-center space-x-2 shadow-inner">
                      <CloudSun class="w-5 h-5 text-emerald-500" />
                      <h3 class="text-sm font-semibold text-emerald-700 tracking-wide">Current Weather Today</h3>
                    </div>
                    <div class="bg-emerald-500 text-white text-[10px] font-bold px-2 py-0.5 rounded-full shadow-md">
                      LIVE
                    </div>
                  </div>
                </div>

                <!-- Loading Skeleton for Current Weather -->
                <template v-if="isLoading">
                  <div class="animate-pulse">
                    <div class="flex items-center justify-between mb-6">
                      <div>
                        <div class="h-12 w-24 bg-gray-200 rounded-md mb-1"></div>
                        <div class="h-4 w-32 bg-gray-200 rounded-md"></div>
                      </div>
                      <div class="h-14 w-14 bg-gray-200 rounded-full"></div>
                    </div>
                    <div class="mt-auto grid grid-cols-2 gap-4 flex-grow">
                      <div v-for="i in 4" :key="`detail-skeleton-${i}`" class="bg-gray-100 rounded-xl p-4 h-16">
                        <div class="flex items-center justify-between">
                          <div class="flex items-center">
                            <div class="h-6 w-6 bg-gray-200 rounded-full mr-3"></div>
                            <div class="h-4 w-20 bg-gray-200 rounded"></div>
                          </div>
                          <div class="h-6 w-10 bg-gray-200 rounded"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>

                <!-- Actual Current Weather Content -->
                <template v-else>
                  <div class="flex items-center justify-between mb-6">
                    <div>
                      <div class="flex items-end space-x-1">
                        <p class="text-5xl font-bold text-emerald-900">{{ weather?.temperature_c }}</p>
                        <p class="text-2xl font-semibold text-emerald-700 mb-1">°C</p>
                      </div>
                      <p class="text-base mt-1 text-emerald-600">{{weather?.weather_condition}}</p>
                    </div>
                    <div class="weather-icon-wrapper">
                      <component 
                          :is="getWeatherIcon(weather?.weather_condition)"
                          :class="['h-14 w-14 transform transition-transform hover:scale-110', getWeatherIconColor(weather?.weather_condition)]"
                        />
                    </div>
                  </div>

                  <div class="mt-auto grid grid-cols-2 gap-4 flex-grow">
                    <div class="bg-teal-50 rounded-xl p-4 flex items-center justify-between h-full shadow-sm hover:shadow transition-all duration-300">
                      <div class="flex items-center">
                        <Waves class="h-6 w-6 text-teal-500 mr-3" />
                        <span class="text-sm font-medium text-teal-700">Pressure</span>
                      </div>
                      <span class="text-lg font-semibold text-teal-800">{{ weather?.pressure }}</span>
                    </div>
                    <div class="bg-cyan-50 rounded-xl p-4 flex items-center justify-between h-full shadow-sm hover:shadow transition-all duration-300">
                      <div class="flex items-center">
                        <Droplet class="h-6 w-6 text-cyan-500 mr-3" />
                        <span class="text-sm font-medium text-cyan-700">Humidity</span>
                      </div>
                      <span class="text-lg font-semibold text-cyan-800">{{ weather?.humidity }}%</span>
                    </div>
                    <div class="bg-green-50 rounded-xl p-4 flex items-center justify-between h-full shadow-sm hover:shadow transition-all duration-300">
                      <div class="flex items-center">
                        <Wind class="h-6 w-6 text-green-500 mr-3" />
                        <span class="text-sm font-medium text-green-700">Wind Speed</span>
                      </div>
                      <span class="text-lg font-semibold text-green-800">{{ weather?.wind_speed }} km/h</span>
                    </div>
                    <div class="bg-amber-50 rounded-xl p-4 flex items-center justify-between h-full shadow-sm hover:shadow transition-all duration-300">
                      <div class="flex items-center">
                        <Sun class="h-6 w-6 text-amber-500 mr-3" />
                        <span class="text-sm font-medium text-amber-700">UV Index</span>
                      </div>
                      <span class="text-lg font-semibold text-amber-800">{{ weather?.uv_index }}</span>
                    </div>
                  </div>
                </template>
              </div>
              
              <!-- Map Card -->
              <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-2xl overflow-hidden shadow-sm relative group hover:shadow-md transition-all duration-300 transform hover:-translate-y-1">
                <div class="absolute inset-0 bg-grid-emerald-500/5"></div>
                <div class="relative h-full p-6">
                  <div class="flex justify-between items-start mb-4">
                    <div class="bg-white px-3 py-1 rounded-full shadow-sm flex items-center">
                      <Map class="w-3.5 h-3.5 text-emerald-600 mr-1" />
                      <h2 class="text-sm font-bold text-emerald-700">Map</h2>
                    </div>
                    <div class="flex space-x-2">
                      <button class="bg-white p-1.5 rounded-full shadow-sm hover:bg-emerald-50 transition-colors">
                        <RefreshCw class="h-3.5 w-3.5 text-emerald-600" />
                      </button>
                      <button class="bg-white p-1.5 rounded-full shadow-sm hover:bg-emerald-50 transition-colors">
                        <MoreVertical class="h-3.5 w-3.5 text-emerald-600" />
                      </button>
                    </div>
                  </div>

                  <!-- Actual Interactive Map -->
                  <div class="mt-4 h-[calc(100%-3rem)] rounded-xl overflow-hidden relative border border-white/60 shadow-inner">
                    <div id="weather-map" class="w-full h-full rounded-xl z-10"></div>
                  </div>
                </div>
              </div>

              <!-- Popular Cities Card -->
              <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300">
                <div class="flex justify-between items-center mb-4">
                  <h2 class="text-lg font-bold text-gray-800 flex items-center">
                    <Globe class="w-5 h-5 mr-2 text-emerald-500" />
                    Near Barangay
                  </h2>
                </div>
                
                <!-- Loading Skeleton for Popular Cities -->
                <template v-if="isLoading">
                  <div class="space-y-1 animate-pulse">
                    <div v-for="i in 5" :key="`city-skeleton-${i}`" class="flex items-center justify-between p-2.5 rounded-xl bg-gray-50">
                      <div class="flex items-center">
                        <div class="h-8 w-8 bg-gray-200 rounded-full mr-3"></div>
                        <div>
                          <div class="h-4 w-24 bg-gray-200 rounded mb-1"></div>
                          <div class="h-3 w-16 bg-gray-200 rounded"></div>
                        </div>
                      </div>
                      <div class="text-right">
                        <div class="h-4 w-16 bg-gray-200 rounded mb-1"></div>
                        <div class="h-3 w-12 bg-gray-200 rounded"></div>
                      </div>
                    </div>
                  </div>
                </template>

                <!-- Actual Popular Cities Content -->
                <template v-else>
                  <div class="space-y-1">
                    <div v-for="(city, index) in popularCities" :key="city.name" 
                         class="flex items-center justify-between p-2.5 rounded-xl hover:bg-emerald-50 transition-all duration-200 cursor-pointer group"
                         :class="{'bg-emerald-50/50': index === 0}">
                      <div class="flex items-center">
                        <div class="bg-white rounded-full p-2 shadow-sm mr-3 group-hover:bg-emerald-100 transition-colors">
                          <component :is="getWeatherIcon(city.condition)" class="h-4 w-4 text-emerald-600" />
                        </div>
                        <div>
                          <div class="text-sm font-medium text-gray-800">{{ city.name }}</div>
                          <div class="text-xs text-gray-500">{{ city.temperature }}°C</div>
                        </div>
                      </div>
                      <div class="text-right">
                        <div class="text-xs font-medium" :class="getConditionColor(city.condition)">
                          {{ city.condition }}
                        </div>
                        <div class="text-[10px] text-gray-500">{{ city.time }}</div>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>

            <!-- Bottom Section: Forecast & Chart -->
            <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
              <!-- 7-Day Forecast Card - Enhanced with better spacing -->
              <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300">
                <div class="flex justify-between items-center mb-4">
                  <h2 class="text-lg font-bold text-gray-800 flex items-center">
                    <CalendarDays class="w-5 h-5 mr-2 text-emerald-500" />
                    Forecast
                  </h2>
                  <div class="flex rounded-full bg-gray-100 p-0.5">
                    <button
                      class="px-3 py-1 rounded-full text-xs font-medium"
                      :class="selectedDays === 7 ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200'"
                      @click="selectedDays = 7"
                    >
                      7 Days
                    </button>
                    <button
                      class="px-3 py-1 rounded-full text-xs font-medium"
                      :class="selectedDays === 10 ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200'"
                      @click="selectedDays = 10"
                    >
                      10 Days
                    </button>
                  </div>
                </div>

                <!-- Loading Skeleton for 7-Day Forecast -->
                <template v-if="isLoading">
                  <div class="space-y-3 mt-4 animate-pulse">
                    <div v-for="i in selectedDays" :key="`forecast-skeleton-${i}`" class="flex items-center justify-between p-3 rounded-xl bg-gray-50">
                      <div class="flex items-center">
                        <div class="h-8 w-8 bg-gray-200 rounded-full mr-3"></div>
                        <div class="h-4 w-20 bg-gray-200 rounded"></div>
                      </div>
                      <div class="h-4 w-24 bg-gray-200 rounded"></div>
                    </div>
                  </div>
                </template>

                <!-- Actual 7-Day Forecast Content -->
                <template v-else>
                  <div class="space-y-3 mt-4">
                    <div
                      v-for="day in forecast.slice(0, selectedDays)"
                      :key="day.date"
                      class="flex items-center justify-between p-3 rounded-xl hover:bg-emerald-50 transition-all duration-200 cursor-pointer border border-transparent hover:border-emerald-100"
                    >
                      <div class="flex items-center">
                        <div class="bg-white rounded-full p-2 shadow-sm mr-3">
                          <component :is="getWeatherIcon(day.condition_code)" class="h-5 w-5 text-emerald-600" />
                        </div>
                        <div class="text-sm font-medium text-gray-800">
                          {{ Number(day.temperature_max).toFixed(1) }}° / {{ Number(day.temperature_min).toFixed(1) }}°
                        </div>
                      </div>
                      <div class="text-xs text-gray-600">
                        {{ new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                      </div>
                    </div>
                  </div>
                </template>
              </div>

              
              <!-- Today's Forecast Card with Tab Functionality -->
              <div class="bg-white rounded-2xl p-5 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 lg:col-span-3">
                <!-- Header with tabs -->
                <div class="flex justify-between items-center mb-3">
                  <div class="flex items-center">
                    <h2 class="text-lg font-bold text-gray-800">Today's Forecast</h2>
                    <span class="ml-2 text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">{{ currentDate }}</span>
                  </div>
                  <div class="flex rounded-full bg-gray-100 p-0.5">
                    <button 
                      @click="setActiveTab('summary')" 
                      class="px-3 py-1 rounded-full text-xs font-medium transition-all duration-200"
                      :class="activeTab === 'summary' ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200'"
                    >
                      Summary
                    </button>
                    <button 
                      @click="setActiveTab('hourly')" 
                      class="px-3 py-1 rounded-full text-xs font-medium transition-all duration-200"
                      :class="activeTab === 'hourly' ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200'"
                    >
                      Hourly
                    </button>
                    <button 
                      @click="setActiveTab('details')" 
                      class="px-3 py-1 rounded-full text-xs font-medium transition-all duration-200"
                      :class="activeTab === 'details' ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200'"
                    >
                      Details
                    </button>
                  </div>
                </div>
                
                <!-- Loading Skeleton for Today's Forecast Tabs -->
                <template v-if="isLoading">
                  <div class="animate-pulse h-full">
                    <div v-if="activeTab === 'summary'" class="h-full">
                      <div class="relative w-full h-52 bg-gray-200 rounded-lg mb-3"></div>
                      <div class="h-6 w-48 bg-gray-200 rounded mb-3"></div>
                      <div class="grid grid-cols-10 gap-1 h-[48%]">
                        <div v-for="i in 10" :key="`summary-skeleton-${i}`" class="flex flex-col h-full items-center">
                          <div class="h-6 w-6 bg-gray-200 rounded-full mb-1"></div>
                          <div class="flex-grow w-full bg-gray-100 rounded-md"></div>
                          <div class="h-3 w-8 bg-gray-200 rounded mt-1"></div>
                          <div class="h-3 w-10 bg-gray-200 rounded mt-1"></div>
                        </div>
                      </div>
                    </div>
                    <div v-else-if="activeTab === 'hourly'" class="space-y-3">
                      <div v-for="i in 5" :key="`hourly-skeleton-${i}`" class="flex items-center justify-between p-3 rounded-xl bg-gray-50">
                        <div class="flex items-center space-x-4">
                          <div class="h-4 w-16 bg-gray-200 rounded"></div>
                          <div class="h-8 w-8 bg-gray-200 rounded-full"></div>
                          <div class="h-4 w-12 bg-gray-200 rounded"></div>
                        </div>
                        <div class="flex items-center space-x-6">
                          <div class="h-4 w-10 bg-gray-200 rounded"></div>
                          <div class="h-4 w-16 bg-gray-200 rounded"></div>
                          <div class="h-4 w-20 bg-gray-200 rounded"></div>
                        </div>
                      </div>
                    </div>
                    <div v-else-if="activeTab === 'details'" class="grid grid-cols-2 gap-4">
                      <div v-for="i in 4" :key="`details-tab-skeleton-${i}`" class="bg-gray-100 rounded-xl p-4 h-32">
                        <div class="h-5 w-3/4 bg-gray-200 rounded mb-3"></div>
                        <div class="space-y-2">
                          <div class="h-4 w-full bg-gray-200 rounded"></div>
                          <div class="h-4 w-5/6 bg-gray-200 rounded"></div>
                        </div>
                      </div>
                    </div>
                  </div>
                </template>

                <!-- Actual Today's Forecast Content -->
                <template v-else>
                  <div v-if="activeTab === 'summary'" class="h-full">
                    <div class="relative w-full h-52">
                      <svg class="w-full h-full" viewBox="0 0 1000 200" preserveAspectRatio="none">
                        <line x1="0" y1="50" x2="1000" y2="50" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="5,5" />
                        <line x1="0" y1="100" x2="1000" y2="100" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="5,5" />
                        <line x1="0" y1="150" x2="1000" y2="150" stroke="#e5e7eb" stroke-width="1" stroke-dasharray="5,5" />
                        <path :d="temperaturePath" fill="none" stroke="url(#lineGradient)" stroke-width="3" stroke-linecap="round" ref="pathRef" />
                        <path :d="areaPath" fill="url(#areaGradient)" />
                        <defs>
                          <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stop-color="#10b981" />
                            <stop offset="50%" stop-color="#059669" />
                            <stop offset="100%" stop-color="#10b981" />
                          </linearGradient>
                          <linearGradient id="areaGradient" x1="0%" y1="0%" x2="0%" y2="100%">
                            <stop offset="0%" stop-color="rgba(16, 185, 129, 0.3)" />
                            <stop offset="100%" stop-color="rgba(16, 185, 129, 0.05)" />
                          </linearGradient>
                        </defs>
                      </svg>
                      <div class="absolute top-0 left-0 w-full h-full pointer-events-none">
                        <div v-for="(temp, index) in hourlyTemps" :key="index" class="absolute flex flex-col items-center" :style="{ left: `calc(${(index / (hourlyTemps.length - 1)) * 100}% - 6px)`, bottom: `${((temp - minTemp) / (maxTemp - minTemp)) * 80 + 10}%` }">
                          <div class="text-[10px] mb-1 text-emerald-600 font-semibold">{{ temp }}°C</div>
                          <div class="w-2.5 h-2.5 rounded-full bg-white border-2 border-emerald-500 shadow-md"></div>
                        </div>
                      </div>
                    </div>
                    <div class="flex items-center mb-3 mt-2 px-1 bg-emerald-50/30 py-2 rounded-lg">
                      <Droplet class="h-4 w-4 text-emerald-600 mr-2.5" />
                      <h3 class="text-sm font-medium text-emerald-700">Precipitation Chance</h3>
                    </div>
                    <div class="grid grid-cols-10 gap-1 h-[48%]">
                      <div v-for="(hour, index) in hourlyForecast.slice(0, 10)" :key="`forecast-${index}`" class="flex flex-col h-full">
                        <div class="bg-emerald-50 p-1.5 rounded-full mb-1 mx-auto">
                          <component :is="getWeatherIcon(hour.condition)" class="h-3.5 w-3.5 text-emerald-600" />
                        </div>
                        <div class="flex-grow w-full px-0.5 flex flex-col">
                          <div class="flex-grow bg-emerald-50 rounded-md relative overflow-hidden">
                            <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-emerald-500 to-emerald-300 transition-all duration-500" :style="{ height: `${hour.rainChance}%` }"></div>
                          </div>
                          <div class="text-[10px] font-medium text-emerald-600 text-center mt-0.5">{{ hour.rainChance }}%</div>
                          <div class="text-[10px] text-gray-500 text-center mt-0.5">{{ hour.time }}</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else-if="activeTab === 'hourly'" class="h-full overflow-auto">
                    <div class="space-y-3">
                      <div v-for="(hour, index) in hourlyForecast" :key="`hourly-${index}`" class="flex items-center justify-between p-3 rounded-xl hover:bg-emerald-50 transition-all duration-200 border border-transparent hover:border-emerald-100">
                        <div class="flex items-center space-x-4">
                          <div class="w-16 text-sm font-medium text-gray-700">{{ hour.time }}</div>
                          <div class="bg-white rounded-full p-2 shadow-sm">
                            <component :is="getWeatherIcon(hour.condition)" class="h-6 w-6" :class="getWeatherIconColor(hour.condition)" />
                          </div>
                          <div class="text-sm font-medium text-gray-800">{{ hour.temp }}°C</div>
                        </div>
                        <div class="flex items-center space-x-6">
                          <div class="flex items-center">
                            <Droplet class="h-4 w-4 text-emerald-500 mr-1.5" />
                            <span class="text-sm text-gray-700">{{ hour.rainChance }}%</span>
                          </div>
                          <div class="flex items-center">
                            <Wind class="h-4 w-4 text-teal-500 mr-1.5" />
                            <span class="text-sm text-gray-700">{{ getRandomWindSpeed() }} km/h</span>
                          </div>
                          <div class="w-20 text-sm font-medium" :class="getConditionColor(hour.condition)">
                            {{ hour.condition }}
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else-if="activeTab === 'details'" class="h-full">
                    <div class="grid grid-cols-2 gap-4">
                      <div class="space-y-4">
                        <div class="bg-emerald-50/50 rounded-xl p-4">
                          <h3 class="text-sm font-semibold text-emerald-800 mb-3 flex items-center"><CloudRain class="h-4 w-4 mr-2 text-emerald-600" />Precipitation</h3>
                          <div class="space-y-2">
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Hourly Value</span><span class="text-sm font-medium text-gray-800">{{ weather.precipitation?.toFixed(1) ?? '--' }} mm</span></div>
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Chance of Rain</span><span class="text-sm font-medium text-gray-800">{{ hourlyForecast[0]?.rainChance ?? '--' }}%</span></div>
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Humidity</span><span class="text-sm font-medium text-gray-800">{{ weather.humidity ?? '--' }}%</span></div>
                          </div>
                        </div>
                        <div class="bg-emerald-50/50 rounded-xl p-4">
                          <h3 class="text-sm font-semibold text-emerald-800 mb-3 flex items-center"><Wind class="h-4 w-4 mr-2 text-emerald-600" />Wind</h3>
                          <div class="space-y-2">
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Speed</span><span class="text-sm font-medium text-gray-800">{{ weather.wind_speed ?? '--' }} km/h</span></div>
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Direction</span><span class="text-sm font-medium text-gray-800">{{ getCompassDirection(weather.wind_direction ?? '--') }}</span></div>
                          </div>
                        </div>
                      </div>
                      <div class="space-y-4">
                        <div class="bg-emerald-50/50 rounded-xl p-4">
                          <h3 class="text-sm font-semibold text-emerald-800 mb-3 flex items-center"><Sun class="h-4 w-4 mr-2 text-emerald-600" />Sun & Moon</h3>
                          <div class="space-y-2">
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Sunrise</span><span class="text-sm font-medium text-gray-800">{{ sunriseDisplay }}</span></div>
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Sunset</span><span class="text-sm font-medium text-gray-800">{{ sunsetDisplay }}</span></div>
                          </div>
                        </div>
                        <div class="bg-emerald-50/50 rounded-xl p-4">
                          <h3 class="text-sm font-semibold text-emerald-800 mb-3 flex items-center"><Thermometer class="h-4 w-4 mr-2 text-emerald-600" />Temperature</h3>
                          <div class="space-y-2">
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Current</span><span class="text-sm font-medium text-gray-800">{{ weather.temperature_c ?? '--' }}°C</span></div>
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">High / Low</span><span class="text-sm font-medium text-gray-800">{{ forecast[0]?.temperature_max ?? '--' }}° / {{ forecast[0]?.temperature_min ?? '--' }}°</span></div>
                            <div class="flex justify-between items-center"><span class="text-xs text-gray-600">Pressure</span><span class="text-sm font-medium text-gray-800">{{ weather.pressure ?? '--' }} hPa</span></div>
                          </div>
                        </div>
                      </div>
                      <div class="col-span-2 bg-emerald-50/50 rounded-xl p-4">
                        <h3 class="text-sm font-semibold text-emerald-800 mb-3 flex items-center"><Wind class="h-4 w-4 mr-2 text-emerald-600" />Air Quality</h3>
                        <div class="flex items-center justify-between">
                          <div>
                            <div class="text-2xl font-bold text-emerald-700">{{ airQual?.pm2_5?.toFixed(1) ?? '--' }} µg/m³</div>
                            <div class="text-xs text-emerald-600">PM₂.₅ Concentration</div>
                          </div>
                          <div class="w-3/4 h-3 bg-gray-200 rounded-full overflow-hidden">
                            <div class="h-full bg-gradient-to-r from-emerald-500 to-emerald-300" :style="{ width: `${Math.min((airQual?.pm2_5 / 50) * 100, 100)}%` }"></div>
                          </div>
                        </div>
                        <div class="mt-2 text-xs text-gray-600">Air quality index based on PM₂.₅ levels.</div>
                      </div>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </div>
        </div>
      </div>
</template>

<script setup>
import { ref, onMounted, computed, onBeforeUnmount } from 'vue'
import { 
  Calendar as CalendarIcon,
  CalendarDays,
  ChevronRight,
  Cloud,
  CloudDrizzle,
  CloudLightning,
  CloudRain,
  CloudSun,
  Droplet,
  Globe,
  Map,
  Minus,
  MoreVertical,
  Plus,
  RefreshCw,
  Snowflake,   // ✅ Add this for cold weather
  Sun,
  Thermometer,
  Waves,
  Wind,
  CloudSnow, 
} from 'lucide-vue-next'
import { getWeatherData, getWeatherDataForPopularCities, mapWeatherCode  } from '../../utils/weather';
import Sidebar from '../layout/Sidebar.vue'
import api from '../../api/index.js'
import maplibregl from 'maplibre-gl'
import 'maplibre-gl/dist/maplibre-gl.css'

const activeTab = ref('summary')
const popularCities = ref([]);
const hourlyForecast = ref([])
const weather = ref({})
const forecast = ref([])
const selectedDays = ref(7);
const sunData = ref([])
const airQual = ref([])
const hourlyTemps = computed(() => hourlyForecast.value.map(h => h.temp))
const isLoading = ref(true); // Added for loading state
const sunriseDisplay = computed(() => formatTimeHM(sunData.value?.sunrise))
const sunsetDisplay  = computed(() => formatTimeHM(sunData.value?.sunset))
let intervalId = null;
let lastWeatherSnapshot = null;

const svgWidth = 1000
const svgHeight = 200
const paddingTop = 10
const paddingBottom = 10

// Calculate min and max temperatures
const minTemp = computed(() =>
  hourlyTemps.value.length ? Math.min(...hourlyTemps.value) : 0
)
const maxTemp = computed(() =>
  hourlyTemps.value.length ? Math.max(...hourlyTemps.value) : 1
)

// Map temperature to Y coordinate
const temperatureToYpx = (temp) => {
  if (maxTemp.value === minTemp.value) return svgHeight / 2
  return (
    svgHeight - paddingBottom -
    ((temp - minTemp.value) / (maxTemp.value - minTemp.value)) *
    (svgHeight - paddingTop - paddingBottom)
  )
}

// Create SVG path for line
const temperaturePath = computed(() => {
  const points = hourlyTemps.value.map((t, i) => {
    const x = (i / (hourlyTemps.value.length - 1)) * svgWidth
    const y = temperatureToYpx(t)
    return [x, y]
  })

  if (points.length < 2) return ''

  let path = `M${points[0][0]},${points[0][1]}`
  for (let i = 1; i < points.length; i++) {
    const [x1, y1] = points[i - 1]
    const [x2, y2] = points[i]
    const cx = (x1 + x2) / 2
    path += ` Q${x1},${y1} ${cx},${(y1 + y2) / 2}`
  }
  const [lastX, lastY] = points[points.length - 1]
  path += ` T${lastX},${lastY}`
  return path
})

// Create path for area under the curve
const areaPath = computed(() => {
  const points = hourlyTemps.value.map((t, i) => {
    const x = (i / (hourlyTemps.value.length - 1)) * svgWidth
    const y = temperatureToYpx(t)
    return [x, y]
  })
  if (points.length < 2) return ''

  let path = `M${points[0][0]},${svgHeight} L${points[0][0]},${points[0][1]}`
  for (let i = 1; i < points.length; i++) {
    const [x1, y1] = points[i - 1]
    const [x2, y2] = points[i]
    const cx = (x1 + x2) / 2
    path += ` Q${x1},${y1} ${cx},${(y1 + y2) / 2}`
  }
  const [lastX, lastY] = points[points.length - 1]
  path += ` T${lastX},${lastY}`
  path += ` L${lastX},${svgHeight} Z`
  return path
})

function getCompassDirection(degree) {
  const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  const index = Math.round(degree / 45) % 8;
  return directions[index];
}

// Animate path
const pathRef = ref(null)
onMounted(() => {
  if (pathRef.value) {
    const length = pathRef.value.getTotalLength()
    pathRef.value.style.strokeDasharray = length
    pathRef.value.style.strokeDashoffset = length
    pathRef.value.getBoundingClientRect() // force reflow
    pathRef.value.style.transition = 'stroke-dashoffset 1s ease-in-out'
    pathRef.value.style.strokeDashoffset = '0'
  }
})

const currentDate = computed(() => {
  const today = new Date()
  const weekday = today.toLocaleDateString('en-US', { weekday: 'short' })  // "Sat"
  const day = today.getDate()                                              // 3
  return `${weekday} ${day}`
})

// Function to set the active tab
const setActiveTab = (tab) => {
  activeTab.value = tab
}

// Function to return the appropriate weather icon based on condition
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
      return Cloud // fallback for fog since lucide doesn't have Fog icon
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
      return CloudSnow
    case 'Thunderstorm':
    case 'Thunderstorm with Hail':
    case 'Severe Thunderstorm':
      return CloudLightning
    default:
      return Cloud
  }
}

// Function to get text color based on weather condition
const getConditionColor = (condition) => {
  const conditionLower = condition.toLowerCase()
  
  if (conditionLower.includes('rain') || conditionLower.includes('drizzle')) {
    return 'text-emerald-600' // Updated to emerald for consistency
  } else if (conditionLower.includes('thunder')) {
    return 'text-purple-600'
  } else if (conditionLower.includes('sunny') || conditionLower.includes('clear')) {
    return 'text-amber-600'
  } else if (conditionLower.includes('cloudy')) {
    return 'text-gray-600'
  } else {
    return 'text-emerald-600'
  }
}

// Function to get weather icon colors
const getWeatherIconColor = (condition) => {
  if (!condition) return 'text-gray-300'
  const conditionLower = condition.toLowerCase()

  if (conditionLower.includes('rain') || conditionLower.includes('drizzle')) {
    return 'text-emerald-500'
  } else if (conditionLower.includes('thunder')) {
    return 'text-purple-600'
  } else if (conditionLower.includes('sunny') || conditionLower.includes('clear')) {
    return 'text-amber-400'
  } else if (conditionLower.includes('cloudy')) {
    return 'text-gray-400'
  } else {
    return 'text-emerald-500'
  }
}

// Helper function to generate random wind speed for hourly view
const getRandomWindSpeed = () => {
  return Math.floor(Math.random() * 8) + 4
}

function formatTimeHM(iso) {
  if (!iso) return '--:--'
  const parts = iso.split('T')
  if (parts.length !== 2) return '--:--'
  const [hour, minute] = parts[1].split(':')
  let hours = parseInt(hour)
  const isAM = hours < 12
  hours = hours % 12 || 12 // Convert 0-23 to 1-12 format
  const ampm = isAM ? 'AM' : 'PM'
  return `${hours}:${minute.padStart(2, '0')} ${ampm}`
}

const MAPTILER_KEY = import.meta.env.VITE_MAPTILER_API 

// const loadWeather = async () => {
//   isLoading.value = true;
//   try {
//     const data = await getWeatherData();
//     console.log("Weather Data:", data)
//     weather.value = data.current;
//     forecast.value = data.forecast;
//     sunData.value = data.sunData;
//     airQual.value = data.airQuality;    

//     if (data && data.hourlyForecast && Array.isArray(data.hourlyForecast)) {
//       hourlyForecast.value = data.hourlyForecast.slice(0, 10)
//     } else {
//       console.error("hourlyForecast is missing or not an array", data)
//       hourlyForecast.value = Array(10).fill({ time: '--:--', temp: '--', condition: 'Cloud', rainChance: 0 }); // Fallback
//     }
//     popularCities.value = await getWeatherDataForPopularCities();
//   } catch (error) {
//     console.error('Failed to load weather:', error);
//     // Set fallback data for display on error
//     weather.value = { temperature_c: '--', weather_condition: 'Error', pressure: '--', humidity: '--', wind_speed: '--', uv_index: '--', precipitation: 0 };
//     forecast.value = Array(10).fill({ date: new Date().toISOString(), condition_code: 'Cloud', temperature_max: '--', temperature_min: '--' });
//     hourlyForecast.value = Array(10).fill({ time: '--:--', temp: '--', condition: 'Cloud', rainChance: 0 });
//   } finally {
//     isLoading.value = false; 
//   }
// };

// onMounted(async () => {
//   await loadWeather(); 
//   intervalId = setInterval(loadWeather, 600000);

//   const map = new maplibregl.Map({
//     container: 'weather-map',
//     style: `https://api.maptiler.com/maps/hybrid/style.json?key=${MAPTILER_KEY}`, // 🛰️ Satellite + Labels
//     center: [121.2151274080352, 13.405165290699628],
//     zoom: 14
//   })

//   map.addControl(new maplibregl.NavigationControl())

//   new maplibregl.Marker({ color: '#059669' })
//     .setLngLat([121.2151274080352, 13.405165290699628])
//     .setPopup(new maplibregl.Popup().setText('📍 Your Location'))
//     .addTo(map)
// })

function updateReactive(target, source) {
  Object.keys(source).forEach(key => {
    target[key] = source[key];
  });
}

const loadWeatherInitially = async () => {
  isLoading.value = true;
  try {
    const data = await getWeatherData();
    updateReactive(weather.value, data.current);
    forecast.value = data.forecast;
    sunData.value = data.sunData;
    airQual.value = data.airQuality;
    hourlyForecast.value = data.hourlyForecast.slice(0, 10);
    popularCities.value = await getWeatherDataForPopularCities();
  } catch (error) {
    console.error('Initial weather load failed:', error);
  } finally {
    isLoading.value = false;
  }
};

// ⏱️ Silent background updates (no loading)
const updateWeatherSilently = async () => {
  try {
    const data = await getWeatherData();

    // Only update values if changed
    if (JSON.stringify(data.current) !== JSON.stringify(weather.value)) {
      updateReactive(weather.value, data.current);
    }
    forecast.value = data.forecast;
    sunData.value = data.sunData;
    airQual.value = data.airQuality;
    hourlyForecast.value = data.hourlyForecast.slice(0, 10);
    popularCities.value = await getWeatherDataForPopularCities();
  } catch (error) {
    console.warn('Silent update failed:', error);
  }
};

onMounted(async () => {
  await loadWeatherInitially();
  intervalId = setInterval(updateWeatherSilently, 60 * 1000); // Every minute

  const map = new maplibregl.Map({
    container: 'weather-map',
    style: `https://api.maptiler.com/maps/hybrid/style.json?key=${MAPTILER_KEY}`,
    center: [121.2151274080352, 13.405165290699628],
    zoom: 14
  });

  map.addControl(new maplibregl.NavigationControl());

  new maplibregl.Marker({ color: '#059669' })
    .setLngLat([121.2151274080352, 13.405165290699628])
    .setPopup(new maplibregl.Popup().setText('📍 Your Location'))
    .addTo(map);
});

onBeforeUnmount(() => {
  clearInterval(intervalId);
});

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Grid background pattern */
.bg-grid-emerald-500\/5 {
  background-image: linear-gradient(to right, rgba(16, 185, 129, 0.05) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(16, 185, 129, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
}

.bg-grid-emerald-500\/10 {
  background-image: linear-gradient(to right, rgba(16, 185, 129, 0.1) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(16, 185, 129, 0.1) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* Animations */
@keyframes pulse {
  0%, 100% { opacity: 0.8; }
  50% { opacity: 0.4; }
}

.animate-pulse {
  animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes ping {
  75%, 100% {
    transform: scale(2);
    opacity: 0;
  }
}

.animate-ping {
  animation: ping 2s cubic-bezier(0, 0, 0.2, 1) infinite;
}

/* Temperature chart animations */
.temperature-path {
  stroke-dasharray: 1000;
  stroke-dashoffset: 1000;
  animation: dash 2s ease-in-out forwards;
  stroke-linecap: round;
}

.temperature-area {
  opacity: 0;
  animation: fadeIn 2s ease-in-out forwards;
  animation-delay: 0.5s;
}

@keyframes dash {
  to {
    stroke-dashoffset: 0;
  }
}

@keyframes fadeIn {
  to {
    opacity: 1;
  }
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
  transition: all 0.3s ease;
}

.weather-icon-wrapper svg {
  animation: float 3s ease-in-out infinite;
}

/* Custom scrollbar styling */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(16, 185, 129, 0.05);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: rgba(16, 185, 129, 0.3);
  border-radius: 4px;
  transition: background-color 200ms;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(16, 185, 129, 0.5);
}

/* Smooth transitions */
* {
  transition: all 200ms ease-in-out;
}

/* Firefox scrollbar styling */
* {
  scrollbar-width: thin;
  scrollbar-color: rgba(16, 185, 129, 0.3) rgba(16, 185, 129, 0.05);
}

/* Media queries for better responsiveness */
@media (max-width: 1280px) {
  .grid-cols-10 {
    grid-template-columns: repeat(5, minmax(0, 1fr));
  }
  
  .h-\[38\%\] {
    height: 33%;
  }
  
  .h-\[48\%\] {
    height: 58%;
  }
}

@media (max-width: 768px) {
  .grid-cols-10 {
    grid-template-columns: repeat(5, minmax(0, 1fr));
  }
  
  .text-\[10px\] {
    font-size: 0.65rem;
  }
}

@media (max-width: 640px) {
  .p-5 {
    padding: 0.75rem;
  }
  
  .h-\[38\%\] {
    height: 30%;
  }
  
  .h-\[48\%\] {
    height: 63%;
  }
  
  .grid-cols-10 {
    grid-template-columns: repeat(5, minmax(0, 1fr));
    grid-template-rows: repeat(2, minmax(0, 1fr));
    gap: 0.5rem;
  }
}

/* Ensure the forecast card fills available space */
.lg\:col-span-3 {
  height: 100%;
  display: flex;
  flex-direction: column;
}

/* Make sure precipitation bars are responsive */
@supports (height: 100%) {
  .flex-grow {
    min-height: 0;
  }
}

</style>