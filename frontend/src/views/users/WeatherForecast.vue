<template>
  <div class="flex-1 w-full px-2 xs:px-3 sm:px-4 md:px-6 lg:px-8 xl:px-10 overflow-hidden">
    <div class="bg-white rounded-[12px] xs:rounded-[14px] sm:rounded-[16px] md:rounded-[18px] lg:rounded-[20px] shadow-sm xs:shadow-md sm:shadow-lg border border-green-100 h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] overflow-y-auto">
      <div class="p-3 xs:p-4 sm:p-5 md:p-6 pb-0">
        <h1 class="text-xl xs:text-2xl sm:text-3xl font-bold text-gray-800 mb-1 xs:mb-1.5 sm:mb-2">Weather Forecasting</h1>
        <div class="flex items-center text-sm xs:text-base text-gray-500">
          <span class="text-green-600">Weather Forecast</span>
          <ChevronRight class="h-4 w-4 xs:h-4 xs:w-4 sm:h-5 sm:w-5 mx-1 xs:mx-1" />
          <span>Overview</span>
        </div>
      </div>

      <div class="p-3 xs:p-4 sm:p-5 md:p-6 lg:p-8">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 xs:gap-4 sm:gap-5 md:gap-6 mb-4 sm:mb-5 md:mb-6">
          <!-- Current Weather card (unchanged) -->
          <div class="bg-white rounded-lg xs:rounded-xl sm:rounded-2xl p-3 xs:p-4 sm:p-5 md:p-6 shadow-sm xs:shadow-md sm:shadow-lg border border-emerald-100 transition-all duration-300 hover:shadow-xl hover:-translate-y-1 overflow-hidden flex flex-col">
            <div class="flex justify-between items-start mb-2 xs:mb-3 sm:mb-4">
              <div class="flex items-center justify-between w-full">
                <div class="bg-emerald-50 rounded-full px-2 py-1 xs:px-2.5 xs:py-1.5 sm:px-3 sm:py-1.5 flex items-center space-x-1 xs:space-x-1.5 sm:space-x-2 shadow-inner">
                  <CloudSun class="w-4 h-4 xs:w-4 xs:h-4 sm:w-5 sm:h-5 text-emerald-500" />
                  <h3 class="text-sm xs:text-sm font-semibold text-emerald-700 tracking-wide">Current Weather</h3>
                </div>
                <div class="bg-emerald-500 text-white text-xs xs:text-xs font-bold px-1.5 py-0.5 rounded-full shadow-sm xs:shadow-md">
                  LIVE
                </div>
              </div>
            </div>

            <template v-if="isLoading">
              <div class="animate-pulse">
                <div class="flex items-center justify-between mb-3 xs:mb-4 sm:mb-5 md:mb-6">
                  <div>
                    <div class="h-8 xs:h-10 sm:h-12 w-16 xs:w-20 sm:w-24 bg-gray-200 rounded-md mb-1"></div>
                    <div class="h-3 xs:h-3.5 sm:h-4 w-20 xs:w-24 sm:w-32 bg-gray-200 rounded-md"></div>
                  </div>
                  <div class="h-8 xs:h-10 sm:h-12 w-8 xs:w-10 sm:w-12 bg-gray-200 rounded-full"></div>
                </div>
                <div class="mt-auto grid grid-cols-2 gap-2 xs:gap-3 sm:gap-4 flex-grow">
                  <div v-for="i in 4" :key="`detail-skeleton-${i}`" class="bg-gray-100 rounded-md xs:rounded-lg sm:rounded-xl p-2 xs:p-3 sm:p-4 h-12 xs:h-14 sm:h-16">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center">
                        <div class="h-3.5 xs:h-4 sm:h-5 w-3.5 xs:w-4 sm:w-5 bg-gray-200 rounded-full mr-1.5 xs:mr-2 sm:mr-3"></div>
                        <div class="h-3 xs:h-3.5 sm:h-4 w-12 xs:w-16 sm:w-20 bg-gray-200 rounded"></div>
                      </div>
                      <div class="h-3.5 xs:h-4 sm:h-5 w-8 xs:w-10 sm:w-12 bg-gray-200 rounded"></div>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <template v-else>
              <div class="flex items-center justify-between mb-3 xs:mb-4 sm:mb-5">
                <div>
                  <div class="flex items-end space-x-1 mt-2 xs:mt-3 sm:mt-4">
                    <p class="text-4xl xs:text-5xl sm:text-6xl font-bold text-emerald-900">{{ weather?.temperature_c }}</p>
                    <p class="text-2xl xs:text-3xl font-semibold text-emerald-700 mb-1 xs:mb-2">°C</p>
                  </div>
                  <p class="text-sm xs:text-base sm:text-lg mt-1 xs:mt-2 text-emerald-600">{{ weather?.weather_condition }}</p>
                </div>
                <div class="weather-icon-wrapper">
                  <component 
                    :is="getWeatherIcon(weather?.weather_condition)"
                    :class="['h-8 w-8 xs:h-10 xs:w-10 sm:h-12 sm:w-12 transform transition-transform hover:scale-110', getWeatherIconColor(weather?.weather_condition)]"
                  />
                </div>
              </div>

              <div class="mt-auto grid grid-cols-2 gap-2 xs:gap-3 sm:gap-4 flex-grow">
                <div class="bg-teal-50 rounded-lg xs:rounded-xl sm:rounded-2xl p-2 xs:p-3 sm:p-4 md:p-5 flex flex-col justify-center h-16 xs:h-18 sm:h-20 shadow-sm hover:shadow-md transition-all duration-300">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <Waves class="h-3.5 w-3.5 xs:h-3.5 xs:w-3.5 sm:h-4 sm:w-4 md:h-5 md:w-5 text-teal-500 mr-1 xs:mr-1.5 sm:mr-2 md:mr-2.5 flex-shrink-0" />
                      <span class="text-xs xs:text-sm sm:text-base md:text-sm font-medium text-teal-700 truncate">Pressure</span>
                    </div>
                    <span class="text-sm xs:text-base sm:text-lg md:text-l font-semibold text-teal-800 ml-1">{{ weather?.pressure }}</span>
                  </div>
                </div>
                <div class="bg-cyan-50 rounded-lg xs:rounded-xl sm:rounded-2xl p-2 xs:p-3 sm:p-4 md:p-5 flex flex-col justify-center h-16 xs:h-18 sm:h-20 shadow-sm hover:shadow-md transition-all duration-300">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <Droplet class="h-3.5 w-3.5 xs:h-3.5 xs:w-3.5 sm:h-4 sm:w-4 md:h-5 md:w-5 text-cyan-500 mr-1 xs:mr-1.5 sm:mr-2 md:mr-2.5 flex-shrink-0" />
                      <span class="text-xs xs:text-sm sm:text-base md:text-sm font-medium text-cyan-700 truncate">Humidity</span>
                    </div>
                    <span class="text-sm xs:text-base sm:text-lg md:text-l font-semibold text-cyan-800 ml-1">{{ weather?.humidity }}%</span>
                  </div>
                </div>
                <div class="bg-green-50 rounded-lg xs:rounded-xl sm:rounded-2xl p-2 xs:p-3 sm:p-4 md:p-5 flex flex-col justify-center h-16 xs:h-18 sm:h-20 shadow-sm hover:shadow-md transition-all duration-300">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <Wind class="h-3.5 w-3.5 xs:h-3.5 xs:w-3.5 sm:h-4 sm:w-4 md:h-5 md:w-5 text-green-500 mr-1 xs:mr-1.5 sm:mr-2 md:mr-2.5 flex-shrink-0" />
                      <span class="text-xs xs:text-sm sm:text-base md:text-sm font-medium text-green-700 truncate">Wind</span>
                    </div>
                    <span class="text-sm xs:text-base sm:text-lg md:text-l font-semibold text-green-800 ml-1">{{ weather?.wind_speed }} km/h</span>
                  </div>
                </div>
                <div class="bg-amber-50 rounded-lg xs:rounded-xl sm:rounded-2xl p-2 xs:p-3 sm:p-4 md:p-5 flex flex-col justify-center h-16 xs:h-18 sm:h-20 shadow-sm hover:shadow-md transition-all duration-300">
                  <div class="flex items-center justify-between">
                    <div class="flex items-center min-w-0">
                      <Sun class="h-3.5 w-3.5 xs:h-3.5 xs:w-3.5 sm:h-4 sm:w-4 md:h-5 md:w-5 text-amber-500 mr-1 xs:mr-1.5 sm:mr-2 md:mr-2.5 flex-shrink-0" />
                      <span class="text-sm font-medium text-amber-700 truncate">UV Index</span>
                    </div>
                    <span class="text-sm xs:text-base sm:text-lg md:text-l font-semibold text-amber-800 ml-1">{{ weather?.uv_index }}</span>
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- Map card (unchanged) -->
          <div class="bg-gradient-to-br from-emerald-50 to-emerald-100 rounded-lg xs:rounded-xl sm:rounded-2xl overflow-hidden shadow-sm xs:shadow-md relative group hover:shadow-md transition-all duration-300 transform hover:-translate-y-1 md:col-span-1 lg:col-span-1">
            <div class="absolute inset-0 bg-grid-emerald-500/5"></div>
            <div class="relative h-full p-2 xs:p-3 sm:p-4 md:p-5 lg:p-6">
              <div class="flex justify-between items-start mb-2 xs:mb-3 sm:mb-4">
                <div class="bg-white px-2 py-0.5 xs:px-2.5 xs:py-1 sm:px-3 sm:py-1 rounded-full shadow-sm flex items-center">
                  <Map class="w-3 h-3 xs:w-3 xs:h-3 sm:w-4 sm:h-4 text-emerald-600 mr-0.5 xs:mr-1" />
                  <h2 class="text-sm xs:text-sm font-bold text-emerald-700">Map</h2>
                </div>
                <div class="flex space-x-1 xs:space-x-1.5 sm:space-x-2">
                  <button class="bg-white p-1 xs:p-1.5 rounded-full shadow-sm hover:bg-emerald-50 transition-colors">
                    <RefreshCw class="h-3 w-3 xs:h-3 xs:w-3 sm:h-4 sm:w-4 text-emerald-600" />
                  </button>
                  <button class="bg-white p-1 xs:p-1.5 rounded-full shadow-sm hover:bg-emerald-50 transition-colors">
                    <MoreVertical class="h-3 w-3 xs:h-3 xs:w-3 sm:h-4 sm:w-4 text-emerald-600" />
                  </button>
                </div>
              </div>

              <div class="mt-2 xs:mt-3 sm:mt-4 h-[calc(100%-2.5rem)] xs:h-[calc(100%-3rem)] rounded-md xs:rounded-lg sm:rounded-xl overflow-hidden relative border border-white/60 shadow-inner">
                <div id="weather-map" class="w-full h-[240px] md:h-[320px] rounded-xl"></div>
              </div>
            </div>
          </div>

          <!-- Nearby (unchanged) -->
          <div class="bg-white rounded-lg xs:rounded-xl sm:rounded-2xl p-2 xs:p-3 sm:p-4 md:p-5 lg:p-6 border border-gray-100 shadow-sm xs:shadow-md hover:shadow-md transition-all duration-300">
            <div class="flex justify-between items-center mb-2 xs:mb-3 sm:mb-4">
              <div class="bg-emerald-50 rounded-full px-2 py-1 xs:px-2.5 xs:py-1.5 sm:px-3 sm:py-1.5 flex items-center space-x-1 xs:space-x-1.5 sm:space-x-2 shadow-inner mb-2">
                <Globe class="w-4 h-4 xs:w-4 xs:h-4 sm:w-5 sm:h-5 text-emerald-500" />
                <h3 class="text-sm xs:text-sm font-semibold text-emerald-700 tracking-wide">Near Barangay</h3>
              </div>
            </div>
            <template v-if="isLoading">
              <div class="space-y-1 xs:space-y-1.5 sm:space-y-2 animate-pulse">
                <div v-for="i in 5" :key="`city-skeleton-${i}`" class="flex items-center justify-between p-1.5 xs:p-2 sm:p-2.5 rounded-md xs:rounded-lg sm:rounded-xl bg-gray-50">
                  <div class="flex items-center">
                    <div class="h-5 w-5 xs:h-6 xs:w-6 sm:h-7 sm:w-7 md:h-8 md:w-8 bg-gray-200 rounded-full mr-1.5 xs:mr-2 sm:mr-3"></div>
                    <div>
                      <div class="h-3 xs:h-3.5 sm:h-4 w-14 xs:w-16 sm:w-20 md:w-24 bg-gray-200 rounded mb-0.5 xs:mb-1"></div>
                      <div class="h-2.5 xs:h-3 w-10 xs:w-12 sm:w-14 md:w-16 bg-gray-200 rounded"></div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="h-3 xs:h-3.5 sm:h-4 w-12 xs:w-14 sm:w-16 md:w-20 bg-gray-200 rounded mb-0.5 xs:mb-1"></div>
                    <div class="h-2.5 xs:h-3 w-8 xs:w-10 sm:w-12 md:w-14 bg-gray-200 rounded"></div>
                  </div>
                </div>
              </div>
            </template>
            <template v-else>
              <div class="space-y-1 xs:space-y-1.5 sm:space-y-2">
                <div v-for="(city, index) in popularCities" :key="city.name" 
                     class="flex items-center justify-between p-1.5 xs:p-2 sm:p-2.5 rounded-md xs:rounded-lg sm:rounded-xl hover:bg-emerald-50 transition-all duration-200 cursor-pointer group"
                     :class="{'bg-emerald-50/50': index === 0}">
                  <div class="flex items-center min-w-0 flex-1">
                    <div class="bg-white rounded-full p-1 xs:p-1.5 sm:p-2 shadow-sm mr-2 xs:mr-2.5 sm:mr-3 group-hover:bg-emerald-100 transition-colors flex-shrink-0">
                      <component :is="getWeatherIcon(city.condition)" class="h-3 w-3 xs:h-3.5 xs:w-3.5 sm:h-4 sm:w-4 text-emerald-600" />
                    </div>
                    <div class="min-w-0 flex-1">
                      <div class="text-xs xs:text-sm sm:text-sm font-medium text-gray-800 truncate">{{ city.name }}</div>
                      <div class="text-xs xs:text-xs sm:text-xs text-gray-500">{{ city.temperature }}°C</div>
                    </div>
                  </div>
                  <div class="text-right flex-shrink-0 ml-2">
                    <div class="text-xs xs:text-xs sm:text-xs font-medium truncate max-w-[4rem] xs:max-w-[5rem] sm:max-w-[6rem]" :class="getConditionColor(city.condition)">
                      {{ city.condition }}
                    </div>
                    <div class="text-xs xs:text-xs sm:text-xs text-gray-500">{{ city.time }}</div>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-4 gap-3 xs:gap-4 sm:gap-5 md:gap-6">
          <!-- Forecast list (unchanged) -->
          <div class="bg-white rounded-lg xs:rounded-xl sm:rounded-2xl p-2 xs:p-3 sm:p-4 md:p-5 lg:p-6 border border-gray-100 shadow-sm xs:shadow-md hover:shadow-md transition-all duration-300 flex flex-col">
            <div class="flex justify-between items-center mb-3 xs:mb-7 sm:mb-8 flex-shrink-0">
              <h3 class="text-base xs:text-lg sm:text-l font-bold text-gray-800 flex items-center">
                <CalendarDays class="w-4 h-4 xs:w-5 xs:h-5 sm:w-6 sm:h-6 mr-1 xs:mr-1.5 sm:mr-2 text-emerald-500" />
                Forecast
              </h3>
              <div class="flex rounded-full bg-gray-100 p-0.5">
                <button
                  class="px-2 py-0.5 xs:px-2.5 xs:py-1 sm:px-3 sm:py-1 rounded-full text-xs xs:text-sm font-medium"
                  :class="selectedDays === 7 ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200'"
                  @click="selectedDays = 7"
                >
                  7 Days
                </button>
                <button
                  class="px-2 py-0.5 xs:px-2.5 xs:py-1 sm:px-3 sm:py-1 rounded-full text-xs xs:text-sm font-medium"
                  :class="selectedDays === 10 ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-600 hover:bg-gray-200'"
                  @click="selectedDays = 10"
                >
                  10 Days
                </button>
              </div>
            </div>

            <template v-if="isLoading">
              <div class="space-y-1.5 xs:space-y-2 sm:space-y-3 mt-2 xs:mt-3 sm:mt-4 animate-pulse flex-1">
                <div v-for="i in selectedDays" :key="`forecast-skeleton-${i}`" class="flex items-center justify-between p-2 xs:p-2.5 sm:p-3 rounded-md xs:rounded-lg sm:rounded-xl bg-gray-50">
                  <div class="flex items-center">
                    <div class="h-5 w-5 xs:h-6 xs:w-6 sm:h-7 sm:w-7 md:h-8 md:w-8 bg-gray-200 rounded-full mr-1.5 xs:mr-2 sm:mr-3"></div>
                    <div class="h-3 xs:h-3.5 sm:h-4 w-12 xs:w-14 sm:w-16 md:w-20 bg-gray-200 rounded"></div>
                  </div>
                  <div class="h-3 xs:h-3.5 sm:h-4 w-14 xs:w-16 sm:w-18 md:w-24 bg-gray-200 rounded"></div>
                </div>
              </div>
            </template>

            <template v-else>
              <div 
                class="space-y-1.5 xs:space-y-2 sm:space-y-3 mt-2 xs:mt-3 sm:mt-4 flex-1"
                :class="{
                  'overflow-y-auto max-h-[400px] xs:max-h-[450px] sm:max-h-[500px] md:max-h-[550px] lg:max-h-[600px] pr-2': selectedDays === 10,
                  'overflow-visible': selectedDays === 7
                }"
              >
                <div
                  v-for="day in forecast.slice(0, selectedDays)"
                  :key="day.date"
                  class="flex items-center justify-between p-2 xs:p-2.5 sm:p-3 rounded-md xs:rounded-lg sm:rounded-xl hover:bg-emerald-50 transition-all duration-200 cursor-pointer border border-transparent hover:border-emerald-100 flex-shrink-0"
                >
                  <div class="flex items-center">
                    <div class="bg-white rounded-full p-1 xs:p-1.5 sm:p-2 shadow-sm mr-1.5 xs:mr-2 sm:mr-3">
                      <component :is="getWeatherIcon(day.condition_code)" class="h-4 w-4 xs:h-4 xs:w-4 sm:h-5 sm:w-5 md:h-6 md:w-6 text-emerald-600" />
                    </div>
                    <div class="text-sm xs:text-sm font-medium text-gray-800">
                      {{ Number(day.temperature_max).toFixed(1) }}° / {{ Number(day.temperature_min).toFixed(1) }}°
                    </div>
                  </div>
                  <div class="text-xs xs:text-sm text-gray-600">
                    {{ new Date(day.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}
                  </div>
                </div>
              </div>
            </template>
          </div>

          <!-- Today's Forecast -->
          <div class="bg-white rounded-lg xs:rounded-xl sm:rounded-2xl p-2 xs:p-3 sm:p-4 md:p-5 border border-gray-100 shadow-sm xs:shadow-md hover:shadow-md transition-all duration-300 lg:col-span-3">
            <div class="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 mb-2 xs:mb-3">
              <div class="flex items-center">
                <h2 class="text-base xs:text-lg sm:text-l md:text-xl font-bold text-gray-800">Today's Forecast</h2>
                <span class="ml-3 text-[8px] md:text-xs text-emerald-700 bg-emerald-100 px-2 py-0.5 rounded-full">
                  {{ currentDate }}
                </span>
              </div>
              <div class="inline-flex sm:flex items-center gap-1 rounded-full bg-gray-100 p-0.5 w-auto self-start sm:self-auto sm:ml-auto mt-1">
                <button 
                  @click="setActiveTab('summary')" 
                  class="px-3 py-1 rounded-full text-xs xs:text-sm font-medium transition-all duration-200"
                  :class="activeTab === 'summary' ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-700 hover:bg-gray-200'"
                >
                  Summary
                </button>
                <button 
                  @click="setActiveTab('hourly')" 
                  class="px-3 py-1 rounded-full text-xs xs:text-sm font-medium transition-all duration-200"
                  :class="activeTab === 'hourly' ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-700 hover:bg-gray-200'"
                >
                  Hourly
                </button>
                <button 
                  @click="setActiveTab('details')" 
                  class="px-3 py-1 rounded-full text-xs xs:text-sm font-medium transition-all duration-200"
                  :class="activeTab === 'details' ? 'bg-emerald-500 text-white shadow-sm' : 'text-gray-700 hover:bg-gray-200'"
                >
                  Details
                </button>
              </div>
            </div>
            
            <template v-if="isLoading">
              <div class="animate-pulse h-full">
                <div v-if="activeTab === 'summary'" class="h-full">
                  <div class="relative w-full h-32 xs:h-40 sm:h-52 bg-gray-200 rounded-md xs:rounded-lg mb-2 xs:mb-3"></div>
                  <div class="h-4 xs:h-5 sm:h-6 w-24 xs:w-32 sm:w-48 bg-gray-200 rounded mb-2 xs:mb-3"></div>
                  <div class="grid grid-cols-5 grid-rows-2 sm:grid-cols-10 sm:grid-rows-1 gap-1 summary-grid-height">
                    <div v-for="i in 10" :key="`summary-skeleton-${i}`" class="flex flex-col h-full items-center">
                      <div class="h-3 w-3 xs:h-4 xs:w-4 sm:h-5 sm:w-5 bg-gray-200 rounded-full mb-0.5 xs:mb-1"></div>
                      <div class="flex-grow w-full bg-gray-100 rounded-md"></div>
                      <div class="h-2.5 xs:h-3 w-6 xs:w-8 bg-gray-200 rounded mt-0.5 xs:mt-1"></div>
                      <div class="h-2.5 xs:h-3 w-8 xs:w-10 bg-gray-200 rounded mt-0.5 xs:mt-1"></div>
                    </div>
                  </div>
                </div>
                <div v-else-if="activeTab === 'hourly'" class="space-y-1.5 xs:space-y-2 sm:space-y-3">
                  <div v-for="i in 5" :key="`hourly-skeleton-${i}`" class="flex items-center justify-between p-2 xs:p-2.5 sm:p-3 rounded-md xs:rounded-lg sm:rounded-xl bg-gray-50">
                    <div class="flex items-center space-x-2 xs:space-x-3 sm:space-x-4">
                      <div class="h-3 xs:h-3.5 sm:h-4 w-10 xs:w-12 sm:w-16 bg-gray-200 rounded"></div>
                      <div class="h-5 w-5 xs:h-6 xs:w-6 sm:h-7 sm:w-7 md:h-8 md:w-8 bg-gray-200 rounded-full"></div>
                      <div class="h-3 xs:h-3.5 sm:h-4 w-8 xs:w-10 sm:w-12 bg-gray-200 rounded"></div>
                    </div>
                    <div class="flex items-center space-x-2 xs:space-x-3 sm:space-x-4 md:space-x-6">
                      <div class="h-3 xs:h-3.5 sm:h-4 w-8 xs:w-10 sm:w-12 bg-gray-200 rounded"></div>
                      <div class="h-3 xs:h-3.5 sm:h-4 w-10 xs:w-12 sm:w-16 bg-gray-200 rounded"></div>
                      <div class="h-3 xs:h-3.5 sm:h-4 w-14 xs:w-16 sm:w-20 bg-gray-200 rounded"></div>
                    </div>
                  </div>
                </div>
                <div v-else-if="activeTab === 'details'" class="grid grid-cols-2 gap-2 xs:gap-3 sm:gap-4">
                  <div v-for="i in 4" :key="`details-tab-skeleton-${i}`" class="bg-gray-100 rounded-md xs:rounded-lg sm:rounded-xl p-2 xs:p-3 sm:p-4 h-20 xs:h-24 sm:h-28 md:h-32">
                    <div class="h-3.5 xs:h-4 sm:h-5 w-3/4 bg-gray-200 rounded mb-1.5 xs:mb-2 sm:mb-3"></div>
                    <div class="space-y-1 xs:space-y-1.5 sm:space-y-2">
                      <div class="h-3 xs:h-3.5 sm:h-4 w-full bg-gray-200 rounded"></div>
                      <div class="h-3 xs:h-3.5 sm:h-4 w-5/6 bg-gray-200 rounded"></div>
                    </div>
                  </div>
                </div>
              </div>
            </template>

            <template v-else>
              <div v-if="activeTab === 'summary'" class="min-h-[30rem] md:h-full">
                <div class="relative w-full h-32 xs:h-40 sm:h-52">
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
                      <div class="chart-temp-label whitespace-nowrap leading-none text-[5px] md:text-[13px] sm:text-xs mb-0.5 xs:mb-1 text-emerald-600 font-semibold">{{ temp }}°C</div>
                      <div class="w-2 h-2 xs:w-2.5 xs:h-2.5 rounded-full bg-white border-2 border-emerald-500 shadow-sm xs:shadow-md"></div>
                    </div>
                  </div>
                </div>

                <div class="flex items-center mb-2 xs:mb-3 mt-1 xs:mt-2 px-1 bg-emerald-50/30 py-1 xs:py-1.5 rounded-md xs:rounded-lg">
                  <Droplet class="h-4 w-4 xs:h-4 sm:h-5 sm:w-5 text-emerald-600 mr-1 xs:mr-1.5 sm:mr-2" />
                  <h3 class="text-sm xs:text-sm font-medium text-emerald-700">Precipitation Chance</h3>
                </div>

                <div class="grid grid-cols-5 grid-rows-2 sm:grid-cols-10 sm:grid-rows-1 gap-1 summary-grid-height">
                  <div v-for="(hour, index) in hourlyForecast.slice(0, 10)" :key="`forecast-${index}`" class="flex flex-col h-full">
                    <div class="bg-emerald-50 p-1 rounded-full mb-0.5 xs:mb-1 mx-auto">
                      <component :is="getWeatherIcon(hour.condition)" class="h-3 w-3 xs:h-3 xs:w-3 sm:h-4 sm:w-4 text-emerald-600" />
                    </div>
                    <div class="w-full px-0.5 flex flex-col">
                      <div class="bg-emerald-50 rounded-md relative overflow-hidden h-24 xs:h-28 sm:h-32 md:h-40 lg:h-48">
                        <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-emerald-500 to-emerald-300 transition-all duration-500" :style="{ height: `${hour.rainChance}%` }"></div>
                      </div>
                      <div class="precip-label text-[10px] sm:text-xs font-medium text-emerald-600 text-center mt-0.5">{{ hour.rainChance }}%</div>
                      <div class="text-[6px] md:text-xs text-gray-500 text-center mt-0.5">{{ hour.time }}</div>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else-if="activeTab === 'hourly'" class="min-h-[30rem]">
                <div class="hourly-scroll space-y-1.5 xs:space-y-2 sm:space-y-3">
                  <div
                    v-for="(hour, index) in hourlyForecast"
                    :key="`hourly-${index}`"
                    class="grid grid-cols-12 items-center gap-1 p-2 xs:p-2.5 sm:p-3 rounded-md xs:rounded-lg sm:rounded-xl hover:bg-emerald-50 transition-all duration-200 cursor-pointer border border-transparent hover:border-emerald-100"
                  >
                    <div class="col-span-2 md:col-span-2 text-[8px] md:text-md xs:text-[10px] sm:text-sm font-medium text-gray-700">
                      {{ hour.time }}
                    </div>
                    <div class="col-span-1 sm:col-span-1">
                      <div class="bg-white rounded-full p-1 xs:p-1.5 sm:p-2 shadow-sm inline-flex items-center justify-center">
                        <component
                          :is="getWeatherIcon(hour.condition)"
                          class="h-2 w-2 xs:h-4 xs:w-4 sm:h-5 sm:w-5 md:h-8 md:w-8"
                          :class="getWeatherIconColor(hour.condition)"
                        />
                      </div>
                    </div>
                    <div class="col-span-2 sm:col-span-2 text-[10px] md:text-md xs:text-sm sm:text-base font-medium text-gray-800">
                      {{ hour.temp }}°C
                    </div>
                    <div class="col-span-2 sm:col-span-2 flex items-center">
                      <Droplet class="h-3 w-3 md:h-8 md:h-8 text-emerald-500 mr-1" />
                      <span class="text-[12px] md:text-lg text-gray-700">{{ hour.rainChance }}%</span>
                    </div>
                    <div class="col-span-3 sm:col-span-2 flex items-center">
                      <Wind class="h-3 w-3 md:h-8 md:h-8 text-teal-500 mr-1" />
                      <span class="text-[10px] md:text-lg text-gray-700">{{ getRandomWindSpeed() }} km/h</span>
                    </div>
                    <div
                      class="col-span-2 sm:col-span-3 min-w-0 text-right md:text-lg xs:text-[12px] text-[9px] font-medium leading-snug sm:whitespace-nowrap"
                      :class="getConditionColor(hour.condition)"
                      :title="hour.condition"
                    >
                      {{ hour.condition }}
                    </div>
                  </div>
                </div>
              </div>

              <div v-else-if="activeTab === 'details'" class="h-full">
                <div class="md:grid md:grid-cols-2 gap-2 xs:gap-3 sm:gap-4">
                  <div class="space-y-2 xs:space-y-3 sm:space-y-4">
                    <div class="bg-emerald-50/50 rounded-md xs:rounded-lg sm:rounded-xl p-2 xs:p-3 sm:p-4">
                      <h3 class="text-sm xs:text-sm font-semibold text-emerald-800 mb-1.5 xs:mb-2 sm:mb-3 flex items-center"><CloudRain class="h-4 w-4 xs:h-4 xs:w-4 sm:h-5 sm:w-5 mr-1 xs:mr-1.5 sm:mr-2 text-emerald-600" />Precipitation</h3>
                      <div class="space-y-1 xs:space-y-1.5 sm:space-y-2">
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Hourly Value</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ weather.precipitation?.toFixed(1) ?? '--' }} mm</span></div>
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Chance of Rain</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ hourlyForecast[0]?.rainChance ?? '--' }}%</span></div>
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Humidity</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ weather.humidity ?? '--' }}%</span></div>
                      </div>
                    </div>
                    <div class="bg-emerald-50/50 rounded-md xs:rounded-lg sm:rounded-xl p-2 xs:p-3 sm:p-4">
                      <h3 class="text-sm xs:text-sm font-semibold text-emerald-800 mb-1.5 xs:mb-2 sm:mb-3 flex items-center"><Wind class="h-4 w-4 xs:h-4 xs:w-4 sm:h-5 sm:w-5 mr-1 xs:mr-1.5 sm:mr-2 text-emerald-600" />Wind</h3>
                      <div class="space-y-1 xs:space-y-1.5 sm:space-y-2">
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Speed</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ weather.wind_speed ?? '--' }} km/h</span></div>
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Direction</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ getCompassDirection(weather.wind_direction ?? '--') }}</span></div>
                      </div>
                    </div>
                  </div>
                  <div class="space-y-2 xs:space-y-3 sm:space-y-4">
                    <div class="bg-emerald-50/50 rounded-md xs:rounded-lg sm:rounded-xl p-2 xs:p-3 sm:p-4">
                      <h3 class="text-sm xs:text-sm font-semibold text-emerald-800 mb-1.5 xs:mb-2 sm:mb-3 flex items-center"><Sun class="h-4 w-4 xs:h-4 xs:w-4 sm:h-5 sm:w-5 mr-1 xs:mr-1.5 sm:mr-2 text-emerald-600" />Sun & Moon</h3>
                      <div class="space-y-1 xs:space-y-1.5 sm:space-y-2">
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Sunrise</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ sunriseDisplay }}</span></div>
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Sunset</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ sunsetDisplay }}</span></div>
                      </div>
                    </div>
                    <div class="bg-emerald-50/50 rounded-md xs:rounded-lg sm:rounded-xl p-2 xs:p-3 sm:p-4">
                      <h3 class="text-sm xs:text-sm font-semibold text-emerald-800 mb-1.5 xs:mb-2 sm:mb-3 flex items-center"><Thermometer class="h-4 w-4 xs:h-4 xs:w-4 sm:h-5 sm:w-5 mr-1 xs:mr-1.5 sm:mr-2 text-emerald-600" />Temperature</h3>
                      <div class="space-y-1 xs:space-y-1.5 sm:space-y-2">
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Current</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ weather.temperature_c ?? '--' }}°C</span></div>
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">High / Low</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ forecast[0]?.temperature_max ?? '--' }}° / {{ forecast[0]?.temperature_min ?? '--' }}°</span></div>
                        <div class="flex justify-between items-center"><span class="text-xs xs:text-sm text-gray-600">Pressure</span><span class="mobile-value text-sm xs:text-sm font-medium text-gray-800">{{ weather.pressure ?? '--' }} hPa</span></div>
                      </div>
                    </div>
                  </div>
                  <div class="col-span-2 bg-emerald-50/50 rounded-md xs:rounded-lg sm:rounded-xl p-2 xs:p-3 sm:p-4">
                    <h3 class="text-sm xs:text-sm font-semibold text-emerald-800 mb-1.5 xs:mb-2 sm:mb-3 flex items-center"><Wind class="h-4 w-4 xs:h-4 xs:w-4 sm:h-5 sm:w-5 mr-1 xs:mr-1.5 sm:mr-2 text-emerald-600" />Air Quality</h3>
                    <div class="flex items-center justify-between">
                      <div>
                        <div class="text-lg xs:text-xl sm:text-2xl font-bold text-emerald-700">{{ airQual?.pm2_5?.toFixed(1) ?? '--' }} µg/m³</div>
                        <div class="text-xs xs:text-sm text-emerald-600">PM₂.₅ Concentration</div>
                      </div>
                      <div class="w-2/3 xs:w-3/4 h-2 xs:h-3 bg-gray-200 rounded-full overflow-hidden">
                        <div class="h-full bg-gradient-to-r from-emerald-500 to-emerald-300" :style="{ width: `${Math.min((airQual?.pm2_5 / 50) * 100, 100)}%` }"></div>
                      </div>
                    </div>
                    <div class="mt-1 xs:mt-2 text-xs xs:text-sm text-gray-600">Air quality index based on PM₂.₅ levels.</div>
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
  MoreVertical,
  RefreshCw,
  Sun,
  Thermometer,
  Waves,
  Wind,
  CloudSnow, 
} from 'lucide-vue-next'
import { getWeatherData, getWeatherDataForPopularCities } from '../../utils/weather';
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
const isLoading = ref(true);
const sunriseDisplay = computed(() => formatTimeHM(sunData.value?.sunrise))
const sunsetDisplay  = computed(() => formatTimeHM(sunData.value?.sunset))
let intervalId = null;

const svgWidth = 1000
const svgHeight = 200
const paddingTop = 10
const paddingBottom = 10

const minTemp = computed(() =>
  hourlyTemps.value.length ? Math.min(...hourlyTemps.value) : 0
)
const maxTemp = computed(() =>
  hourlyTemps.value.length ? Math.max(...hourlyTemps.value) : 1
)

const temperatureToYpx = (temp) => {
  if (maxTemp.value === minTemp.value) return svgHeight / 2
  return (
    svgHeight - paddingBottom -
    ((temp - minTemp.value) / (maxTemp.value - minTemp.value)) *
    (svgHeight - paddingTop - paddingBottom)
  )
}

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

/* Area fill ends flat (no curved cap) */
const areaPath = computed(() => {
  const points = hourlyTemps.value.map((t, i) => {
    const x = (i / (hourlyTemps.value.length - 1)) * svgWidth
    const y = temperatureToYpx(t)
    return [x, y]
  })
  if (points.length < 2) return ''

  const [firstX, firstY] = points[0]
  let path = `M${firstX},${svgHeight} L${firstX},${firstY}`
  for (let i = 1; i < points.length; i++) {
    const [x1, y1] = points[i - 1]
    const [x2, y2] = points[i]
    const cx = (x1 + x2) / 2
    path += ` Q${x1},${y1} ${cx},${(y1 + y2) / 2}`
  }
  const [lastX, lastY] = points[points.length - 1]
  path += ` T${lastX},${lastY} L${lastX},${svgHeight} L${firstX},${svgHeight} Z`
  return path
})

function getCompassDirection(degree) {
  const directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
  const index = Math.round(degree / 45) % 8;
  return directions[index];
}

const pathRef = ref(null)
onMounted(() => {
  if (pathRef.value) {
    const length = pathRef.value.getTotalLength()
    pathRef.value.style.strokeDasharray = length
    pathRef.value.style.strokeDashoffset = length
    pathRef.value.getBoundingClientRect()
    pathRef.value.style.transition = 'stroke-dashoffset 1s ease-in-out'
    pathRef.value.style.strokeDashoffset = '0'
  }
})

const currentDate = computed(() => {
  const today = new Date()
  return today.toLocaleDateString('en-US', {
    weekday: 'long',
    month: 'long',
    day: 'numeric',
    year: 'numeric'
  })
})

const setActiveTab = (tab) => {
  activeTab.value = tab
}

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
      return Cloud
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

const getConditionColor = (condition) => {
  const conditionLower = condition.toLowerCase()
  
  if (conditionLower.includes('rain') || conditionLower.includes('drizzle')) {
    return 'text-emerald-600'
  } else if (conditionLower.includes('thunder')) {
    return 'text-purple-600'
  } else if (conditionLower.includes('sunny') || conditionLower.includes('clear')) {
    return 'text-amber-600'
  } else if (conditionLower.includes('cloudy') || conditionLower.includes('overcast')) {
    return 'text-gray-600'
  } else {
    return 'text-emerald-600'
  }
}

const getWeatherIconColor = (condition) => {
  if (!condition) return 'text-gray-300'
  const conditionLower = condition.toLowerCase()

  if (conditionLower.includes('rain') || conditionLower.includes('drizzle')) {
    return 'text-emerald-500'
  } else if (conditionLower.includes('thunder')) {
    return 'text-purple-600'
  } else if (conditionLower.includes('sunny') || conditionLower.includes('clear')) {
    return 'text-amber-400'
  } else if (conditionLower.includes('cloudy') || conditionLower.includes('overcast')) {
    return 'text-gray-400'
  } else {
    return 'text-emerald-500'
  }
}

const getRandomWindSpeed = () => Math.floor(Math.random() * 8) + 4

function formatTimeHM(iso) {
  if (!iso) return '--:--'
  const parts = iso.split('T')
  if (parts.length !== 2) return '--:--'
  const [hour, minute] = parts[1].split(':')
  let hours = parseInt(hour)
  const isAM = hours < 12
  hours = hours % 12 || 12
  const ampm = isAM ? 'AM' : 'PM'
  return `${hours}:${minute.padStart(2, '0')} ${ampm}`
}

const MAPTILER_KEY = import.meta.env.VITE_MAPTILER_API 

function updateReactive(target, source) {
  Object.keys(source).forEach(key => { target[key] = source[key] })
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

// Silent background updates
const updateWeatherSilently = async () => {
  try {
    const data = await getWeatherData();

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

/* MapLibre attribution, smaller */
:deep(.maplibregl-ctrl-attrib){font-size:10px!important;line-height:1.2!important;padding:2px 4px!important;background-color:rgba(255,255,255,.8)!important;border-radius:4px!important;max-width:200px!important}
:deep(.maplibregl-ctrl-attrib a){font-size:10px!important;color:#374151!important;text-decoration:none!important}
:deep(.maplibregl-ctrl-attrib-button){width:16px!important;height:16px!important;font-size:10px!important}

/* Grid background pattern */
.bg-grid-emerald-500\/5 {
  background-image: linear-gradient(to right, rgba(16, 185, 129, 0.05) 1px, transparent 1px),
                    linear-gradient(to bottom, rgba(16, 185, 129, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
}

/* Animations */
@keyframes pulse{0%,100%{opacity:.8}50%{opacity:.4}}
.animate-pulse{animation:pulse 3s cubic-bezier(.4,0,.6,1) infinite}
@keyframes ping{75%,100%{transform:scale(2);opacity:0}}
.animate-ping{animation:ping 2s cubic-bezier(0,0,.2,1) infinite}

/* Chart animations */
.temperature-path{stroke-dasharray:1000;stroke-dashoffset:1000;animation:dash 2s ease-in-out forwards;stroke-linecap:round}
.temperature-area{opacity:0;animation:fadeIn 2s ease-in-out forwards;animation-delay:.5s}
@keyframes dash{to{stroke-dashoffset:0}}
@keyframes fadeIn{to{opacity:1}}

/* Icon float */
@keyframes float{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-6px) rotate(2deg)}}
.weather-icon-wrapper{position:relative;transition:all .3s ease}
.weather-icon-wrapper svg{animation:float 3s ease-in-out infinite}

/* Custom scrollbar */
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:rgba(16,185,129,.05);border-radius:4px}
::-webkit-scrollbar-thumb{background:rgba(16,185,129,.3);border-radius:4px;transition:background-color 200ms}
::-webkit-scrollbar-thumb:hover{background:rgba(16,185,129,.5)}
*{transition:all 200ms ease-in-out;scrollbar-width:thin;scrollbar-color:rgba(16,185,129,.3) rgba(16,185,129,.05)}

/* Ensure the forecast card fills available space */
.lg\:col-span-3{height:100%;display:flex;flex-direction:column}

/* Summary bars min-height */
.summary-grid-height{height:auto;min-height:160px}
@media (min-width:640px){.summary-grid-height{min-height:200px}}
@media (min-width:768px){.summary-grid-height{min-height:240px;height:auto}}

/* Mobile readability */
@media (max-width:640px){
  .chart-temp-label{font-size:10px;line-height:1}
  .precip-label{font-size:10px}
  .mobile-value{font-size:12px}
}

/* Scrollable Hourly:
   - Mobile (default): NOT scrollable (overflow visible)
   - Desktop (>= sm): scrollable with max-height
*/
.hourly-scroll{
  overflow: visible;
  max-height: none;
  padding-right: 0;
  margin-right: 0;
}
@media (min-width: 640px){ /* sm and up = desktop/tablet */
  .hourly-scroll{
    overflow-y: auto;
    max-height: 28rem;
    padding-right: .25rem;
    margin-right: -.25rem; /* preserve visual alignment */
  }
}
@media (min-width: 768px){
  .hourly-scroll{ max-height: 32rem; }
}
@media (min-width: 1024px){
  .hourly-scroll{ max-height: 36rem; }
}

/* keep the rest of your styles as-is */
</style>