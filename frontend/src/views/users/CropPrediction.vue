<template>
  <!-- Container Wrapper with proper spacing -->
  <div class="flex-1 w-full px-2 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
    <!-- Main Container with adjusted width -->
    <div class="bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-green-100 w-[calc(100vw-15px)] md:w-[calc(100vw-20px)] h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] overflow-y-auto">
      <!-- Content Wrapper --> 
      <div class="p-2 md:p-4 sm:p-6">
        <!-- Clean Minimalist Metrics Section - With Loading State -->
        <div class="grid grid-cols-4 md:grid-cols-4 gap-1 md:gap-4 mb-4 md:mb-6">
          <!-- Total Predictions -->
          <div class="bg-white rounded-[1rem] md:rounded-xl p-2 md:p-5 border border-gray-100 shadow-sm">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center flex-col-reverse md:flex-row gap-2 md:gap-3">
                <ChartBarIcon class="h-3 w-3 md:h-5 md:w-5 text-purple-500" />
                <span class="text-[10px] md:text-sm font-medium text-purple-700 bg-purple-500/10 px-2 py-0.5 rounded-full">Total</span>
              </div>
            </div>
            <div v-if="!isStatsLoading" class="flex flex-col">
              <div class="text-2xl text-center md:text-left font-bold text-gray-900 mb-2">{{ totalRecommendations }}</div>
              <div class="flex items-center justify-center text-[7px] md:text-xs font-medium mt-1">
                <template v-if="percentageChange > 0">
                  <component
                    :is="isIncrease ? ArrowUpIcon : ArrowDownIcon"
                    :class="['w-3 h-3 mr-1', isIncrease ? 'text-green-600' : 'text-red-600']"
                  />
                  <span :class="[isIncrease ? 'text-green-600' : 'text-red-600']">
                    {{ isIncrease ? '+' : '-' }}{{ percentageChange }}% {{ isIncrease ? 'increase' : 'decrease' }}
                  </span>
                </template>
                <template v-else>
                  <MinusIcon class="w-3 h-3 mr-1 text-gray-500" />
                  <span class="text-gray-500">No significant change</span>
                </template>
              </div>
            </div>
            <div v-else class="animate-pulse">
              <div class="h-7 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div class="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>

          <!-- Planted -->
          <div class="bg-white rounded-[1rem] md:rounded-xl p-1 pt-2 md:p-5 border border-gray-100 shadow-sm">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center flex-col-reverse md:flex-row gap-1 md:gap-2 md:pt-4">
                <SproutIcon class="h-3 w-3 md:h-5 md:w-5 text-green-500" />
                <span class="text-[10px] md:text-sm font-medium text-green-700 bg-green-500/10 px-2 py-0.5 rounded-full">Planted</span>
              </div>
            </div>
            <div v-if="!isStatsLoading" class="flex flex-col">
              <div class="text-2xl text-center font-bold text-gray-900 mb-2">{{ plantedCount }}</div>
              <div class="flex items-center justify-center text-[7px] md:text-xs font-medium mt-1">
                <template v-if="plantedPercentageChange > 0">
                  <component
                    :is="plantedIsIncrease ? ArrowUpIcon : ArrowDownIcon"
                    :class="['w-3 h-3 mr-1', plantedIsIncrease ? 'text-green-600' : 'text-red-600']"
                  />
                  <span :class="[plantedIsIncrease ? 'text-green-600' : 'text-red-600']">
                    {{ plantedIsIncrease ? '+' : '-' }}{{ plantedPercentageChange }}% {{ plantedIsIncrease ? 'increase' : 'decrease' }}
                  </span>
                </template>
                <template v-else>
                  <MinusIcon class="w-3 h-3 mr-1 text-gray-500" />
                  <span class="text-gray-500">No significant change</span>
                </template>
              </div>
            </div>
            <div v-else class="animate-pulse">
              <div class="h-7 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div class="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>

          <!-- Success Rate -->
          <div class="bg-white rounded-[1rem] md:rounded-xl p-2 md:p-5 border border-gray-100 shadow-sm">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center flex-col-reverse md:flex-row gap-2">
                <ActivityIcon class="h-3 w-3 md:h-5 md:w-5 text-blue-500" />
                <span class="text-[10px] md:text-sm font-medium text-blue-700 bg-blue-500/10 px-2 py-0.5 rounded-full">Rate</span>
              </div>
            </div>
            <div v-if="!isStatsLoading" class="flex flex-col">
              <div class="text-xl md:text-2xl text-center font-bold text-gray-900 mb-2">{{ harvestSuccessRate }}%</div>
              <div class="flex items-center justify-center text-[7px] md:text-xs font-medium mt-1">
                <template v-if="harvestRatePercentageChange > 0">
                  <component
                    :is="harvestRateIsIncrease ? ArrowUpIcon : ArrowDownIcon"
                    :class="['w-3 h-3 mr-1', harvestRateIsIncrease ? 'text-green-600' : 'text-red-600']"
                  />
                  <span :class="[harvestRateIsIncrease ? 'text-green-600' : 'text-red-600']">
                    {{ harvestRateIsIncrease ? '+' : '-' }}{{ harvestRatePercentageChange }}% {{ harvestRateIsIncrease ? 'increase' : 'decrease' }}
                  </span>
                </template>
                <template v-else>
                  <MinusIcon class="w-3 h-3 mr-1 text-gray-500" />
                  <span class="text-gray-500">No significant change</span>
                </template>
              </div>
            </div>
            <div v-else class="animate-pulse">
              <div class="h-7 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div class="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>

          <!-- Ongoing -->
          <div class="bg-white rounded-[1rem] md:rounded-xl p-2 md:p-5 border border-gray-100 shadow-sm">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center flex-col-reverse md:flex-row gap-1">
                <ClipboardListIcon class="h-3 w-3 md:h-5 md:w-5 text-red-500" />
                <span class="text-[10px] md:text-sm font-medium text-red-700 bg-red-500/10 px-2 py-0.5 rounded-full">Active</span>
              </div>
            </div>
            <div v-if="!isStatsLoading" class="flex flex-col">
              <div class="text-2xl text-center font-bold text-gray-900 mb-2">{{ ongoingCount }}</div>
              <div class="flex items-center justify-center text-[7px] md:text-xs font-medium mt-1">
                <template v-if="ongoingPercentageChange > 0">
                  <component
                    :is="ongoingIsIncrease ? ArrowUpIcon : ArrowDownIcon"
                    :class="['w-3 h-3 mr-1', ongoingIsIncrease ? 'text-green-600' : 'text-red-600']"
                  />
                  <span :class="[ongoingIsIncrease ? 'text-green-600' : 'text-red-600']">
                    {{ ongoingIsIncrease ? '+' : '-' }}{{ ongoingPercentageChange }}% {{ ongoingIsIncrease ? 'increase' : 'decrease' }}
                  </span>
                </template>
                <template v-else>
                  <MinusIcon class="w-3 h-3 mr-1 text-gray-500" />
                  <span class="text-gray-500">No significant change</span>
                </template>
              </div>
            </div>
            <div v-else class="animate-pulse">
              <div class="h-7 bg-gray-200 rounded w-3/4 mb-2"></div>
              <div class="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>
        </div>

        <!-- Main Content Area -->
        <div class="space-y-6">
          <!-- Modified Prediction Form - Enhanced UI -->
          <div class="bg-white rounded-xl shadow-md py-5 px-3 sm:p-6 border border-gray-100 relative overflow-hidden">
            <!-- Background Pattern -->
            <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-green-50 to-transparent opacity-50 -z-10"></div>
                
            <!-- Enhanced Header -->
            <div class="mb-6">
              <h2 class="text-md md:text-xl font-semibold text-gray-800 flex items-center gap-2 tracking-wide">
                <ActivitySquareIcon class="w-5 h-5 text-green-500" />
                Crop Recommendations
              </h2>
              <p class="text-[10px] md:text-sm text-gray-500 mt-1">
                Real-time soil analysis and environmental parameters
              </p>
            </div>

            <!-- Form Fields Container -->
            <div class="space-y-4">
              <!-- Primary Measurements Section -->
              <div>
                <h3 class="text-xs md:text-sm font-medium text-gray-700 mb-4 flex items-center">
                  <span class="inline-block w-1.5 h-1.5 bg-green-500 rounded-full mr-2"></span>
                  Soil Composition Analysis
                </h3>
                <div class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-2 ">
                  <!-- Nitrogen Level -->
                  <div class="relative group">
                    <template v-if="!isSensorDataLoading">
                      <div class="absolute inset-0 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                      <div class="relative bg-white rounded-lg p-2 md:p-4 border border-gray-100 transition-all duration-300 hover:border-green-300 hover:shadow-md">
                        <div class="flex items-center gap-3 mb-3">
                          <div class="p-2 bg-green-50 rounded-lg">
                            <BeakerIcon class="w-3 h-3 md:w-4 md:h-4 text-green-600" />
                          </div>
                          <div>
                            <label class="block text-[10px] md:text-sm font-medium text-gray-500">Nitrogen (N)</label>
                            <div class="flex items-baseline gap-1 mt-0.5">
                              <span 
                                class="text-xl font-bold text-gray-900 bg-transparent w-auto focus:outline-none"
                              >
                                {{ nitrogen }}
                              </span>
                              <span class="text-[7px] md:text-xs text-gray-500">mg/kg</span>
                            </div>
                          </div>
                          </div>
                          <div class="h-1.5 w-full bg-gray-100 rounded-full">
                            <div 
                              class="h-1.5 bg-green-500 rounded-full transition-all duration-500"
                              :style="{ width: `${Math.min(100, (parseFloat(nitrogen || 0) / 200 * 100))}%` }"
                            ></div>
                          </div>
                      </div>
                    </template>
                    <div v-else class="relative bg-white rounded-lg p-4 border border-gray-100 animate-pulse">
                      <div class="flex items-center gap-3 mb-3">
                        <div class="p-2 bg-gray-200 rounded-lg w-8 h-8"></div>
                        <div>
                          <div class="h-4 bg-gray-200 rounded w-20 mb-1"></div>
                          <div class="flex items-baseline gap-1 mt-0.5">
                            <div class="h-6 bg-gray-200 rounded w-16"></div>
                            <div class="h-3 bg-gray-200 rounded w-8"></div>
                          </div>
                        </div>
                      </div>
                      <div class="h-1.5 w-full bg-gray-200 rounded-full"></div>
                    </div>
                  </div>

                  <!-- Phosphorus Level -->
                  <div class="relative group">
                    <template v-if="!isSensorDataLoading">
                      <div class="absolute inset-0 bg-gradient-to-r from-blue-50 to-sky-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                      <div class="relative bg-white rounded-lg p-2 md:p-4 border border-gray-100 transition-all duration-300 hover:border-blue-300 hover:shadow-md">
                        <div class="flex items-center gap-3 mb-3">
                          <div class="p-2 bg-blue-50 rounded-lg">
                            <TestTubesIcon class="w-3 h-3 md:w-4 md:h-4 text-blue-600" />
                          </div>
                          <div>
                            <label class="block text-[8.7px] md:text-sm font-medium text-gray-500">Phosphorus (P)</label>
                            <div class="flex items-baseline gap-1 mt-0.5">
                              <span 
                                class="text-xl font-bold text-gray-900 bg-transparent w-auto focus:outline-none"
                              >
                                {{ phosphorus }}
                              </span>
                              <span class="text-[7px] md:text-xs text-gray-500">mg/kg</span>
                            </div>
                          </div>
                        </div>
                        <div class="h-1.5 w-full bg-gray-100 rounded-full">
                          <div 
                            class="h-1.5 bg-blue-500 rounded-full transition-all duration-500"
                            :style="{ width: `${Math.min(100, (parseFloat(phosphorus || 0) / 200 * 100))}%` }"
                          ></div>
                        </div>
                      </div>
                    </template>
                    <div v-else class="relative bg-white rounded-lg p-4 border border-gray-100 animate-pulse">
                      <div class="flex items-center gap-3 mb-3">
                        <div class="p-2 bg-gray-200 rounded-lg w-8 h-8"></div>
                        <div>
                          <div class="h-4 bg-gray-200 rounded w-24 mb-1"></div>
                          <div class="flex items-baseline gap-1 mt-0.5">
                            <div class="h-6 bg-gray-200 rounded w-16"></div>
                            <div class="h-3 bg-gray-200 rounded w-8"></div>
                          </div>
                        </div>
                      </div>
                      <div class="h-1.5 w-full bg-gray-200 rounded-full"></div>
                    </div>
                  </div>

                  <!-- Potassium Level -->
                  <div class="relative group">
                    <template v-if="!isSensorDataLoading">
                      <div class="absolute inset-0 bg-gradient-to-r from-purple-50 to-violet-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                      <div class="relative bg-white rounded-lg p-2 md:p-4 border border-gray-100 transition-all duration-300 hover:border-purple-300 hover:shadow-md">
                        <div class="flex items-center gap-3 mb-3">
                          <div class="p-2 bg-purple-50 rounded-lg">
                            <BeakerIcon class="w-3 h-3 md:w-4 md:h-4 text-purple-600" />
                          </div>
                          <div>
                            <label class="block text-[9px] md:text-sm font-medium text-gray-500">Potassium (K)</label>
                            <div class="flex items-baseline gap-1 mt-0.5">
                              <span 
                                class="text-xl font-bold text-gray-900 bg-transparent w-auto focus:outline-none"
                              >
                                {{ potassium }}
                              </span>
                                <span class="text-[7px] md:text-xs text-gray-500">mg/kg</span>
                            </div>
                          </div>
                        </div>
                        <div class="h-1.5 w-full bg-gray-100 rounded-full">
                          <div 
                            class="h-1.5 bg-purple-500 rounded-full transition-all duration-500"
                            :style="{ width: `${Math.min(100, (parseFloat(potassium || 0) / 200 * 100))}%` }"
                          ></div>
                        </div>
                      </div>
                    </template>
                    <div v-else class="relative bg-white rounded-lg p-4 border border-gray-100 animate-pulse">
                      <div class="flex items-center gap-3 mb-3">
                        <div class="p-2 bg-gray-200 rounded-lg w-8 h-8"></div>
                        <div>
                          <div class="h-4 bg-gray-200 rounded w-24 mb-1"></div>
                          <div class="flex items-baseline gap-1 mt-0.5">
                            <div class="h-6 bg-gray-200 rounded w-16"></div>
                            <div class="h-3 bg-gray-200 rounded w-8"></div>
                          </div>
                        </div>
                      </div>
                      <div class="h-1.5 w-full bg-gray-200 rounded-full"></div>
                    </div>
                  </div>

                  <!-- pH Level -->
                  <div class="relative group">
                    <template v-if="!isSensorDataLoading">
                      <div class="absolute inset-0 bg-gradient-to-r from-amber-50 to-yellow-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                      <div class="relative bg-white rounded-lg p-3 md:p-4 border border-gray-100 transition-all duration-300 hover:border-amber-300 hover:shadow-md">
                        <div class="flex items-center gap-3 mb-3">
                          <div class="p-2 bg-amber-50 rounded-lg">
                            <DropletIcon class="w-3 h-3 md:w-4 md:h-4 text-amber-600" />
                          </div>
                          <div>
                            <label class="block text-[10px] md:text-sm font-medium text-gray-500">Soil pH</label>
                            <div class="flex items-baseline gap-1 mt-0.5">
                              <span 
                                class="text-xl font-bold text-gray-900 bg-transparent w-auto focus:outline-none"
                              >
                                {{ soilpH }}
                              </span>
                              <span class="text-[7px] md:text-xs text-gray-500">pH</span>
                            </div>
                          </div>
                        </div>
                        <div class="h-1.5 w-full bg-gray-100 rounded-full">
                          <div 
                            class="h-1.5 bg-amber-500 rounded-full transition-all duration-500"
                            :style="{ width: `${Math.min(100, (parseFloat(soilpH || 0) / 14 * 100))}%` }"
                          ></div>
                        </div>
                      </div>
                    </template>
                    <div v-else class="relative bg-white rounded-lg p-4 border border-gray-100 animate-pulse">
                      <div class="flex items-center gap-3 mb-3">
                        <div class="p-2 bg-gray-200 rounded-lg w-8 h-8"></div>
                        <div>
                          <div class="h-4 bg-gray-200 rounded w-16 mb-1"></div>
                          <div class="flex items-baseline gap-1 mt-0.5">
                            <div class="h-6 bg-gray-200 rounded w-16"></div>
                            <div class="h-3 bg-gray-200 rounded w-6"></div>
                          </div>
                        </div>
                      </div>
                      <div class="h-1.5 w-full bg-gray-200 rounded-full"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Environmental Parameters Section -->
              <div>
                <h3 class="text-xs md:text-sm font-medium text-gray-700 mb-4 flex items-center">
                  <span class="inline-block w-1.5 h-1.5 bg-blue-500 rounded-full mr-2"></span>
                  Environmental Parameters
                </h3>
                <div class="grid grid-cols-3 sm:grid-cols-3 gap-1">
                  <!-- Soil Moisture -->
                  <div class="relative group">
                    <template v-if="!isSensorDataLoading">
                      <div class="absolute inset-0 bg-gradient-to-r from-cyan-50 to-sky-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                        <div class="relative bg-white rounded-lg p-2 md:p-4 border border-gray-100 transition-all duration-300 hover:border-cyan-300 hover:shadow-md">
                        <div class="flex items-center gap-1 md:gap-3 mb-3">
                          <div class="p-1 bg-cyan-50 rounded-lg">
                            <WavesIcon class="w-2 h-2 md:w-4 md:h-4 text-cyan-600" />
                          </div>
                          <div>
                            <label class="block text-[7px] md:text-sm font-medium text-gray-500">Soil Moisture</label>
                            <div class="flex items-baseline gap-1 mt-0.5">
                              <span 
                                class="text-lg md:text-xl font-bold text-gray-900 bg-transparent w-auto focus:outline-none"
                              >
                                {{ soilMoisture }}
                              </span>
                              <span class="text-[9px] md:text-xs text-gray-500">%</span>
                            </div>
                          </div>
                        </div>
                        <div class="h-1.5 w-full bg-gray-100 rounded-full">
                          <div 
                            class="h-1.5 bg-cyan-500 rounded-full transition-all duration-500"
                            :style="{ width: `${Math.min(100, parseFloat(soilMoisture || 0))}%` }"
                          ></div>
                        </div>
                      </div>
                    </template>
                    <div v-else class="relative bg-white rounded-lg p-4 border border-gray-100 animate-pulse">
                      <div class="flex items-center gap-3 mb-3">
                        <div class="p-2 bg-gray-200 rounded-lg w-8 h-8"></div>
                        <div>
                          <div class="h-4 bg-gray-200 rounded w-28 mb-1"></div>
                          <div class="flex items-baseline gap-1 mt-0.5">
                            <div class="h-6 bg-gray-200 rounded w-16"></div>
                            <div class="h-3 bg-gray-200 rounded w-4"></div>
                          </div>
                        </div>
                      </div>
                      <div class="h-1.5 w-full bg-gray-200 rounded-full"></div>
                    </div>
                  </div>

                  <!-- Temperature -->
                  <div class="relative group">
                    <template v-if="!isSensorDataLoading">
                      <div class="absolute inset-0 bg-gradient-to-r from-orange-50 to-red-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                      <div class="relative bg-white rounded-lg p-2 md:p-4 border border-gray-100 transition-all duration-300 hover:border-orange-300 hover:shadow-md">
                        <div class="flex items-center gap-1 md:gap-3 mb-3">
                          <div class="p-1 md:p-2 bg-orange-50 rounded-lg">
                            <ThermometerIcon class="w-2 h-2 md:w-4 md:h-4 text-orange-600" />
                          </div>
                          <div>
                            <label class="block text-[7px] md:text-sm font-medium text-gray-500">Temperature</label>
                            <div class="flex items-baseline gap-1 mt-0.5">
                              <span 
                                class="text-lg md:text-xl font-bold text-gray-900 bg-transparent w-auto focus:outline-none"
                              >
                                {{ temperature }}
                              </span>
                              <span class="text-[9px] md:text-xs text-gray-500">°C</span>
                            </div>
                          </div>
                        </div>
                        <div class="h-1.5 w-full bg-gray-100 rounded-full">
                          <div 
                            class="h-1.5 bg-orange-500 rounded-full transition-all duration-500"
                            :style="{ width: `${Math.min(100, (parseFloat(temperature || 0) / 50 * 100))}%` }"
                          ></div>
                        </div>
                      </div>
                    </template>
                    <div v-else class="relative bg-white rounded-lg p-4 border border-gray-100 animate-pulse">
                      <div class="flex items-center gap-3 mb-3">
                        <div class="p-2 bg-gray-200 rounded-lg w-8 h-8"></div>
                        <div>
                          <div class="h-4 bg-gray-200 rounded w-24 mb-1"></div>
                          <div class="flex items-baseline gap-1 mt-0.5">
                            <div class="h-6 bg-gray-200 rounded w-16"></div>
                            <div class="h-3 bg-gray-200 rounded w-6"></div>
                          </div>
                        </div>
                      </div>
                      <div class="h-1.5 w-full bg-gray-200 rounded-full"></div>
                    </div>
                  </div>

                  <!-- Humidity -->
                  <div class="relative group">
                    <template v-if="!isSensorDataLoading">
                      <div class="absolute inset-0 bg-gradient-to-r from-teal-50 to-emerald-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                      <div class="relative bg-white rounded-lg p-2 md:p-4 border border-gray-100 transition-all duration-300 hover:border-teal-300 hover:shadow-md">
                        <div class="flex items-center gap-1 md:gap-3 mb-3">
                          <div class="p-1 md:p-2 bg-teal-50 rounded-lg">
                            <CloudIcon class="w-2 h-2 md:w-4 md:h-4 text-teal-600" />
                          </div>
                          <div>
                            <label class="block text-[7px] md:text-sm font-medium text-gray-500">Humidity</label>
                            <div class="flex items-baseline gap-1 mt-0.5">
                              <span 
                                class="text-lg md:text-xl font-bold text-gray-900 bg-transparent w-auto focus:outline-none"
                              >
                                {{ humidity }}
                              </span>
                              <span class="text-[8px] md:text-xs text-gray-500">%</span>
                            </div>
                          </div>
                        </div>
                        <div class="h-1.5 w-full bg-gray-100 rounded-full">
                          <div 
                            class="h-1.5 bg-teal-500 rounded-full transition-all duration-500"
                            :style="{ width: `${Math.min(100, parseFloat(humidity || 0))}%` }"
                          ></div>
                        </div>
                      </div>
                    </template>
                    <div v-else class="relative bg-white rounded-lg p-4 border border-gray-100 animate-pulse">
                      <div class="flex items-center gap-3 mb-3">
                        <div class="p-2 bg-gray-200 rounded-lg w-8 h-8"></div>
                        <div>
                          <div class="h-4 bg-gray-200 rounded w-20 mb-1"></div>
                          <div class="flex items-baseline gap-1 mt-0.5">
                            <div class="h-6 bg-gray-200 rounded w-16"></div>
                            <div class="h-3 bg-gray-200 rounded w-4"></div>
                          </div>
                        </div>
                      </div>
                      <div class="h-1.5 w-full bg-gray-200 rounded-full"></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Action Button -->
              <div class="flex justify-center mt-6 md:mt-8">
                <button 
                  type="submit"
                  @click="submitForm"
                  :disabled="isRecommending"
                  class="inline-flex items-center justify-center px-6 sm:px-8 py-3 text-xs md:text-base font-medium text-white bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl transition-all duration-300 hover:from-green-600 hover:to-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
                >
                  <template v-if="isRecommending">
                    <svg class="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    <span>Getting Recommendations...</span>
                  </template>
                  <template v-else>
                    <SproutIcon class="w-5 h-5" />
                    <span>Get Crop Recommendations</span>
                  </template>
                </button>
              </div>
            </div>
          </div>

          <!-- Table Section with Enhanced UI and Truly Fixed Height -->
          <div class="bg-white rounded-xl shadow-md p-2 md:p-5 sm:p-6 border border-gray-100 relative overflow-hidden">
            <!-- Background Pattern -->
            <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-blue-50 to-transparent opacity-50 -z-10"></div>
              
            <!-- Enhanced Filter Tabs -->
            <div class="border-b border-gray-100 mb-2 md:mb-6">
              <div class="flex gap-1 md:gap-4 overflow-x-auto scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-transparent pb-2">
                <button 
                  v-for="filter in filters" 
                  :key="filter.name"
                  :class="[
                    'px-2 py-2 md:px-4 md:py-2.5 text-xs md:text-sm font-medium transition-all duration-200 relative whitespace-nowrap',
                    activeFilter === filter.name 
                      ? 'text-green-600' 
                      : 'text-gray-500 hover:text-gray-700'
                  ]"
                  @click="activeFilter = filter.name"
                >
                  {{ filter.name }}
                  <div 
                    :class="[
                      'absolute bottom-0 left-0 w-full h-0.5 transition-all duration-200',
                      activeFilter === filter.name 
                        ? 'bg-green-500' 
                        : 'bg-transparent group-hover:bg-gray-100'
                    ]"
                  />
                </button>
              </div>
            </div>

            <!-- Enhanced Search and Actions -->
            <div class="flex flex-wrap justify-between items-center mb-2 md:mb-6 gap-2 md:gap-4">
              <div class="relative flex-1 max-w-md">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <SearchIcon class="w-3 h-3 md:h-4 md:w-4 text-gray-400" />
                </div>
                <input 
                  type="text"
                  v-model="searchQuery"
                  placeholder="Search predictions..."
                  class="w-full pl-8 md:pl-10 pr-4 py-2 text-xs md:text-sm bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all duration-200"
                />
              </div>
              <div class="flex items-center gap-2">
                <button 
                  class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                  @click="toggleGridView"
                  :class="{'bg-gray-100': isGridView}"
                  aria-label="Toggle grid view"
                >
                  <LayoutGridIcon class="h-4 w-4" />
                </button>
                <button 
                  class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg transition-colors duration-200"
                  @click="toggleFilterPanel"
                  :class="{'bg-gray-100': showFilterPanel}"
                  aria-label="Toggle filter panel"
                >
                  <FilterIcon class="h-4 w-4" />
                </button>
                 <!-- Add Export Dropdown Button -->
                <div class="relative inline-block">
                  <button 
                    class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg transition-colors duration-200 flex items-center gap-1"
                    @click.stop="toggleExportDropdown"
                  >
                    <DownloadIcon class="h-4 w-4" />
                    <span class="text-xs">Export</span>
                  </button>
                  
                  <!-- Export Dropdown -->
                  <transition
                    enter-active-class="transition ease-out duration-100"
                    enter-from-class="transform opacity-0 scale-95"
                    enter-to-class="transform opacity-100 scale-100"
                    leave-active-class="transition ease-in duration-75"
                    leave-from-class="transform opacity-100 scale-100"
                    leave-to-class="transform opacity-0 scale-95"
                  >
                    <div 
                      v-if="showExportDropdown"
                      class="absolute right-0 mt-2 w-40 origin-top-right bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none z-50"
                      role="menu"
                      aria-orientation="vertical"
                      aria-labelledby="menu-button"
                    >
                      <div class="py-1" role="none">
                        <button 
                          @click.stop="exportCropData('csv')"
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                          role="menuitem"
                        >
                          Export as CSV
                        </button>
                        <button 
                          @click.stop="exportCropData('pdf')"
                          class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 hover:text-gray-900"
                          role="menuitem"
                        >
                          Export as PDF
                        </button>
                      </div>
                    </div>
                  </transition>
                  
                </div>
                  <button 
                    @click="printTable"
                    class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg transition-colors duration-200 flex items-center gap-1"
                  >
                    <PrinterIcon class="h-4 w-4" />
                    <span class="text-xs">Print</span>
                  </button>
              </div>
            </div>

            <!-- Filter Panel -->
            <div 
              v-if="showFilterPanel" 
              class="bg-gray-50 rounded-lg p-4 mb-6 transition-all duration-300 ease-in-out"
            >
              <div class="flex justify-between items-center mb-4">
                <h3 class="text-sm font-medium text-gray-700">Advanced Filters</h3>
                <button 
                  @click="toggleFilterPanel"
                  class="text-gray-400 hover:text-gray-600"
                >
                  <XIcon class="h-4 w-4" />
                </button>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <!-- Success Rate Range -->
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-2">Success Rate</label>
                  <div class="flex items-center gap-2">
                    <input 
                      type="number" 
                      v-model="filterSuccessRateMin" 
                      min="0" 
                      max="100"
                      placeholder="Min" 
                      class="w-full px-3 py-2 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500"
                    />
                    <span class="text-gray-400">-</span>
                    <input 
                      type="number" 
                      v-model="filterSuccessRateMax" 
                      min="0" 
                      max="100"
                      placeholder="Max" 
                      class="w-full px-3 py-2 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500"
                    />
                  </div>
                </div>
                  
                <!-- Date Range -->
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-2">Date Range</label>
                  <div class="flex items-center gap-2">
                    <input 
                      type="date" 
                      v-model="filterDateStart" 
                      class="w-full px-3 py-2 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500"
                    />
                    <span class="text-gray-400">-</span>
                    <input 
                      type="date" 
                      v-model="filterDateEnd" 
                      class="w-full px-3 py-2 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500"
                    />
                  </div>
                </div>
                    
                <!-- Status Filter -->
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-2">Status</label>
                  <select 
                    v-model="filterStatus" 
                    class="w-full px-3 py-2 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500"
                  >
                    <option value="">All Statuses</option>
                    <option value="Planted">Planted</option>
                    <option value="Ongoing">Ongoing</option>
                    <option value="Harvested">Harvested</option>
                    <option value="Cancelled">Cancelled</option>
                  </select>
                </div>
              </div>
                  
              <div class="flex justify-end mt-4 gap-2">
                <button 
                  @click="resetFilters"
                  class="px-4 py-2 text-sm font-medium text-gray-600 bg-white rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                >
                  Reset
                </button>
                <button 
                  @click="applyFilters"
                  class="px-4 py-2 text-sm font-medium text-white bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg hover:from-green-600 hover:to-emerald-600 transition-colors"
                  >
                  Apply Filters
                </button>
              </div>
            </div>

            <!-- Grid View -->
            <div 
              v-if="isGridView" 
              class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 mb-6 transition-all duration-300 ease-in-out"
            > 
              <div 
                v-for="prediction in paginatedPredictions" 
                :key="prediction.id"
                class="bg-white rounded-lg border border-gray-200 p-4 hover:shadow-md transition-all duration-200 hover:-translate-y-1"
              >
                <div class="flex items-center gap-3 mb-3">
                  <div class="flex items-center justify-center w-10 h-10 rounded-lg bg-green-50 text-green-600">
                    <SproutIcon class="h-5 w-5" />
                  </div>
                  <div>
                    <h3 class="text-sm font-medium text-gray-900">{{ prediction.crop }}</h3>
                    <p class="text-xs text-gray-500">{{ prediction.date.split(',')[0] }}</p>
                  </div>
                </div>
                    
                <div class="space-y-2 mb-3">
                  <div class="flex justify-between items-center">
                    <span class="text-xs text-gray-600">Success Rate:</span>
                    <span class="text-xs font-medium text-gray-900">{{ prediction.successRate }}%</span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-1.5">
                    <div 
                      class="bg-green-500 h-1.5 rounded-full"
                      :style="{ width: `${prediction.successRate}%` }"
                    />
                  </div>
                </div>
                    
                <div class="flex items-center justify-between">
                  <span 
                    :class="[
                      'inline-flex items-center px-2 py-1 rounded-full text-xs font-medium',
                      getStatusClass(prediction.status)
                    ]"
                  >
                    <span 
                      :class="[
                        'w-1.5 h-1.5 rounded-full mr-1.5',
                        {
                          'bg-green-500': prediction.status === 'Planted',
                          'bg-blue-500': prediction.status === 'Ongoing',
                          'bg-red-500': prediction.status === 'Cancelled',
                          'bg-gray-500': prediction.status === 'Harvested'
                        }
                      ]"
                    />
                    {{ prediction.status }}
                  </span>
                    
                  <button 
                    @click="showDetails(prediction)"
                    class="inline-flex items-center justify-center px-3 py-1 text-xs font-medium text-white bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg hover:from-green-600 hover:to-emerald-600 transition-colors duration-200 gap-1"
                  >
                    <EyeIcon class="h-3 w-3" />
                    Details
                  </button>
                </div>
              </div>
              <!-- Skeleton for Grid View -->
              <template v-if="isPredictionsLoading">
                <div v-for="n in itemsPerPage" :key="`grid-skeleton-${n}`" class="bg-white rounded-lg border border-gray-200 p-4 animate-pulse">
                  <div class="flex items-center gap-3 mb-3">
                    <div class="w-10 h-10 rounded-lg bg-gray-200"></div>
                    <div>
                      <div class="h-4 bg-gray-200 rounded w-24 mb-1"></div>
                      <div class="h-3 bg-gray-200 rounded w-16"></div>
                    </div>
                  </div>
                  <div class="h-4 bg-gray-200 rounded w-full mb-2"></div>
                  <div class="h-3 bg-gray-200 rounded w-1/2 mb-3"></div>
                  <div class="flex items-center justify-between">
                    <div class="h-6 bg-gray-200 rounded-full w-20"></div>
                    <div class="h-8 bg-gray-200 rounded-lg w-24"></div>
                  </div>
                </div>
              </template>
            </div>

            <!-- Enhanced Table with Truly Fixed Height -->
            <div 
              v-if="!isGridView && !isPredictionsLoading"
              class="overflow-hidden rounded-lg border border-gray-100 transition-all duration-300 ease-in-out"
            >
              <div class="overflow-x-auto">
                <div class="overflow-y-auto" style="height: 370px"> <!-- Fixed height container -->
                  <table class="w-full">
                    <thead class="sticky top-0 bg-gray-50/95 backdrop-blur-sm z-10">
                      <tr>
                        <th 
                          v-for="header in tableHeaders" 
                          :key="header.key"
                          class="px-3 py-2 md:px-4 md:py-3.5 text-left text-[10px] md:text-xs font-medium text-gray-500 uppercase tracking-wider"
                        >
                          {{ header.label }}
                        </th>
                      </tr>
                    </thead>
                    <tbody class="divide-y divide-gray-100">
                      <tr 
                        v-for="prediction in paginatedPredictions" 
                        :key="prediction.id"
                        class="group hover:bg-gray-50/50 transition-colors duration-200"
                      >
                        <td class="px-3 py-1 md:px-4 md:py-3.5 whitespace-nowrap">
                          <div class="flex items-center gap-3">
                            <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-green-50 text-green-600">
                              <SproutIcon class="h-4 w-4" />
                            </div>
                            <span class="text-xs md:text-sm font-medium text-gray-900">
                              {{ prediction.crop }}
                            </span>
                          </div>
                        </td>
                        <td class="px-4 py-3.5 whitespace-nowrap">
                          <div class="flex flex-col">
                            <span class="text-sm font-medium text-gray-900">
                              {{ prediction.date.split(' at ')[0] }}  <!-- Date part -->
                            </span>
                            <span class="text-xs text-gray-500">
                              {{ prediction.date.split(' at ')[1] }}  <!-- Time part -->
                            </span>
                          </div>
                        </td>
                        <td class="px-4 py-3.5 whitespace-nowrap">
                          <div class="flex items-center gap-2">
                            <div class="w-16 bg-gray-100 rounded-full h-1.5">
                              <div 
                                class="bg-green-500 h-1.5 rounded-full"
                                :style="{ width: `${prediction.successRate}%` }"
                              />
                            </div>
                            <span class="text-sm font-medium text-gray-900">
                              {{ prediction.successRate }}%
                            </span>
                          </div>
                        </td>
                        <td class="px-4 py-3.5 whitespace-nowrap">
                          <span 
                            :class="[
                              'inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium',
                              getStatusClass(prediction.status)
                            ]"
                          >
                            <span 
                              :class="[
                                'w-1.5 h-1.5 rounded-full mr-1.5',
                                {
                                  'bg-green-500': prediction.status === 'Planted',
                                  'bg-blue-500': prediction.status === 'Ongoing',
                                  'bg-red-500': prediction.status === 'Cancelled',
                                  'bg-gray-500': prediction.status === 'Harvested'
                                }
                              ]"
                            />
                            {{ prediction.status }}
                          </span>
                        </td>
                        <td class="px-4 py-3.5 whitespace-nowrap">
                          <button 
                            @click="showDetails(prediction)"
                            class="inline-flex items-center justify-center px-3 py-1.5 text-xs font-medium text-white bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg hover:from-green-600 hover:to-emerald-600 transition-colors duration-200 gap-1.5"
                          >
                            <EyeIcon class="h-3.5 w-3.5" />
                            Show
                          </button>
                        </td>
                      </tr>
                      <!-- Placeholder rows to maintain height -->
                      <tr v-for="n in Math.max(0, itemsPerPage - paginatedPredictions.length)" :key="n">
                        <td colspan="6" class="px-4 py-3.5">&nbsp;</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
            <!-- Loading state for Table View -->
            <div v-if="!isGridView && isPredictionsLoading" class="overflow-hidden rounded-lg border border-gray-100">
              <div class="overflow-y-auto animate-pulse" style="height: 370px">
                <table class="w-full">
                  <thead class="sticky top-0 bg-gray-50/95 backdrop-blur-sm z-10">
                    <tr>
                      <th v-for="header in tableHeaders" :key="header.key" class="px-4 py-3.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="h-4 bg-gray-200 rounded w-3/4"></div>
                      </th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-gray-100">
                    <tr v-for="n in itemsPerPage" :key="`table-skeleton-${n}`">
                      <td v-for="header in tableHeaders" :key="`cell-skeleton-${header.key}-${n}`" class="px-4 py-3.5"><div class="h-5 bg-gray-200 rounded"></div></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Enhanced Pagination -->
            <div class="mt-6 flex flex-col sm:flex-row items-center justify-between gap-4">
              <!-- Items per page selector - full width on mobile -->
              <div class="w-full sm:w-auto flex items-center gap-2">
                <label class="text-xs md:text-sm text-gray-600 whitespace-nowrap">Items per page</label>
                <select 
                  v-model="itemsPerPage"
                  class="text-xs md:text-sm border border-gray-200 rounded-lg px-2 py-1 focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500 w-full sm:w-auto"
                >
                  <option value="6">6</option>
                  <option value="10">10</option>
                  <option value="20">20</option>
                </select>
              </div>
              
              <!-- Pagination controls - centered on mobile -->
              <div class="w-full sm:w-auto flex items-center justify-center gap-2">
                <button 
                  class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                  :disabled="currentPage === 1"
                  @click="currentPage--"
                  aria-label="Previous page"
                >
                  <ChevronLeftIcon class="h-4 w-4" />
                </button>
                
                <!-- Mobile-friendly page numbers with ellipsis -->
                <div class="flex items-center gap-1 overflow-x-auto py-1 max-w-[200px] sm:max-w-none">
                  <!-- Always show first page button if not on first page -->
                  <button 
                    v-if="currentPage > 1"
                    :class="[
                      'px-2 sm:px-3 py-1 text-xs sm:text-sm font-medium rounded-lg transition-colors duration-200',
                      currentPage === 1
                        ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white'
                        : 'text-gray-500 hover:bg-gray-50'
                    ]"
                    @click="currentPage = 1"
                  >
                    1
                  </button>
                  
                  <!-- Show ellipsis if current page is far from start -->
                  <span 
                    v-if="currentPage > 3"
                    class="px-1 text-gray-400"
                  >
                    ...
                  </span>
                  
                  <!-- Show previous page if not first page -->
                  <button 
                    v-if="currentPage > 2"
                    :class="[
                      'px-2 sm:px-3 py-1 text-xs sm:text-sm font-medium rounded-lg transition-colors duration-200',
                      'text-gray-500 hover:bg-gray-50'
                    ]"
                    @click="currentPage = currentPage - 1"
                  >
                    {{ currentPage - 1 }}
                  </button>
                  
                  <!-- Always show current page -->
                  <button 
                    :class="[
                      'px-2 sm:px-3 py-1 text-xs sm:text-sm font-medium rounded-lg transition-colors duration-200',
                      'bg-gradient-to-r from-green-500 to-emerald-500 text-white'
                    ]"
                  >
                    {{ currentPage }}
                  </button>
                  
                  <!-- Show next page if not last page -->
                  <button 
                    v-if="currentPage < totalPages - 1"
                    :class="[
                      'px-2 sm:px-3 py-1 text-xs sm:text-sm font-medium rounded-lg transition-colors duration-200',
                      'text-gray-500 hover:bg-gray-50'
                    ]"
                    @click="currentPage = currentPage + 1"
                  >
                    {{ currentPage + 1 }}
                  </button>
                  
                  <!-- Show ellipsis if current page is far from end -->
                  <span 
                    v-if="currentPage < totalPages - 2"
                    class="px-1 text-gray-400"
                  >
                    ...
                  </span>
                  
                  <!-- Always show last page button if not on last page -->
                  <button 
                    v-if="currentPage < totalPages"
                    :class="[
                      'px-2 sm:px-3 py-1 text-xs sm:text-sm font-medium rounded-lg transition-colors duration-200',
                      currentPage === totalPages
                        ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white'
                        : 'text-gray-500 hover:bg-gray-50'
                    ]"
                    @click="currentPage = totalPages"
                  >
                    {{ totalPages }}
                  </button>
                </div>
                
                <button 
                  class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                  :disabled="currentPage === totalPages"
                  @click="currentPage++"
                  aria-label="Next page"
                >
                  <ChevronRightIcon class="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Modal Overlay - Completely separate from the main content -->
  <div v-if="showModal" class="fixed inset-0 z-50 overflow-hidden">
    <!-- Backdrop with blur effect -->
    <div class="absolute inset-0 bg-black/50 backdrop-blur-[2px]" @click="closeModal"></div>
    
    <!-- Modal Content - Centered and above the backdrop -->
    <div class="absolute inset-0 flex items-center justify-center p-4">
      <div class="relative bg-white rounded-2xl shadow-xl max-w-xl w-full mx-auto h-full md:h-auto overflow-auto">
        <!-- Modal Header -->
        <div class="text-center p-6 pb-0">
          <h2 class="text-xl font-semibold text-gray-800">Crop Recommendations</h2>
          <p class="text-xs text-gray-500 mt-0.5">Based on your soil parameters</p>
        </div>

        <!-- Main Content Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-5 p-6">
          <!-- Left Column -->
          <div class="space-y-4">
            <!-- Primary Recommendation -->
            <div class="bg-gradient-to-br from-green-50 to-emerald-50/50 rounded-lg p-5">
              <div class="flex items-center gap-2 text-green-600 mb-3">
                <SproutIcon class="h-4 w-4" />
                <span class="text-xs font-medium">Recommended Crop</span>
              </div>
              <h3 class="text-xl font-bold text-green-700 mb-2">{{ recommendedCrop }}</h3>
              <div class="flex items-baseline gap-1 mb-2">
                <span class="text-2xl font-bold text-green-600">{{ successRate }}</span>
                <span class="text-sm font-medium text-green-600">%</span>
              </div>
              <p class="text-xs text-gray-600">
                This crop has a {{ successRate }}% chance of success based on your soil composition.
              </p>
            </div>

            <div class="bg-gradient-to-br from-amber-50 to-yellow-50/50 rounded-lg p-5">
              <div class="flex items-center gap-2 text-amber-600 mb-3">
                <FlaskIcon class="h-4 w-4" />
                <span class="text-xs font-medium">Recommended Fertilizer</span>
              </div>
              
              <div class="grid grid-cols-2 gap-2">
                <div class="text-xs text-amber-600">Type:</div>
                <div class="text-xs text-amber-700 text-right">{{ fertilizer.type }}</div>
                
                <div class="text-xs text-amber-600">Name:</div>
                <div class="text-xs text-amber-700 text-right">{{ fertilizer.name }}</div>
                
                <div class="text-xs text-amber-600">Amount:</div>
                <div class="text-xs text-amber-700 text-right">
                  {{ fertilizer.adjusted_amount }} {{ fertilizer.unit }}
                </div>
              </div>
              
              <div v-if="fertilizer.notes" class="mt-3 text-xs text-amber-600 italic">
                {{ fertilizer.notes }}
              </div>
            </div>

            <!-- Success Metrics -->
            <div class="bg-white rounded-lg p-4 border border-gray-100 shadow-sm">
              <div class="flex items-center gap-2 text-green-600 mb-3">
                <TrendingUpIcon class="h-4 w-4" />
                <span class="text-xs font-medium">Success Metrics</span>
              </div>
              <div class="space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-600">Soil Compatibility</span>
                  <span class="text-xs font-medium text-gray-900">{{ soilCompatibility }}%</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-1.5 mb-1">
                  <div 
                    class="bg-green-500 h-1.5 rounded-full"
                    :style="{ width: `${soilCompatibility}%` }"
                  />
                </div>
                
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-600">Growth Rate</span>
                  <span class="text-xs font-medium text-gray-900">{{ growthRate }}%</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-1.5 mb-1">
                  <div 
                    class="bg-blue-500 h-1.5 rounded-full"
                    :style="{ width: `${growthRate}%` }"
                  />
                </div>
                
                <div class="flex items-center justify-between">
                  <span class="text-xs text-gray-600">Yield Potential</span>
                  <span class="text-xs font-medium text-gray-900">{{ yieldPotential }}%</span>
                </div>
                <div class="w-full bg-gray-100 rounded-full h-1.5 mb-1">
                  <div 
                    class="bg-purple-500 h-1.5 rounded-full"
                    :style="{ width: `${yieldPotential}%` }"
                  />
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column - Alternative Options -->
          <div class="space-y-4">
            <!-- Alternative Options -->
            <div class="bg-white rounded-lg p-4 border border-gray-100 shadow-sm">
              <div class="flex items-center gap-2 text-green-600 mb-3">
                <ListIcon class="h-4 w-4" />
                <span class="text-xs font-medium">Alternative Options</span>
              </div>
              <div class="space-y-4">
                <div v-for="(option, index) in alternativeOptions" :key="index" class="space-y-2">
                  <!-- Crop Info -->
                  <div class="flex items-center justify-between">
                    <div>
                      <h4 class="text-sm font-medium text-gray-900">{{ option?.crop || 'N/A' }}</h4>
                      <p class="text-[10px] text-gray-500">Alternative crop</p>
                    </div>
                    <div class="text-right">
                      <div class="text-sm font-semibold text-gray-900">
                        {{ option?.confidence || 0 }}%
                      </div>
                    </div>
                  </div>
                  <!-- Progress Bar -->
                  <div class="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                    <div 
                      class="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all" 
                      :style="{ width: `${option?.confidence || 0}%` }"
                    ></div>
                  </div>
                  <!-- Fertilizer Info - Only show if fertilizer exists -->
                  <template v-if="option?.fertilizer">
                    <div class="mt-2 bg-amber-50 rounded-lg p-2">
                      <div class="text-[10px] font-medium text-amber-600 mb-1">Recommended Fertilizer:</div>
                      <div class="grid grid-cols-2 gap-1 text-[10px]">
                        <div class="text-amber-600">Type:</div>
                        <div class="text-amber-700 text-right">{{ option.fertilizer.type || 'N/A' }}</div>
                        
                        <div class="text-amber-600">Name:</div>
                        <div class="text-amber-700 text-right">{{ option.fertilizer.name || 'N/A' }}</div>
                        
                        <div class="text-amber-600">Amount:</div>
                        <div class="text-amber-700 text-right">
                          {{ option.fertilizer.adjusted_amount || 0 }} {{ option.fertilizer.unit || '' }}
                        </div>
                      </div>
                      <div v-if="option.fertilizer.notes" class="mt-1 text-[10px] text-amber-600 italic">
                        {{ option.fertilizer.notes }}
                      </div>
                    </div>
                  </template>
                  <div v-else class="mt-2 bg-amber-50 rounded-lg p-2 text-[10px] text-amber-600">
                    No specific fertilizer recommendation available
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="flex justify-end gap-2 p-6 pt-0">
          <button 
            @click="closeModal"
            class="px-4 py-2 text-xs md:text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
          >
            Close
          </button>
          <button 
            @click="saveRecommendation"
            :disabled="isSavingRecommendation"
            class="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-[10px] md:text-sm font-medium rounded-lg hover:from-green-600 hover:to-emerald-600 transition-colors flex items-center justify-center gap-1.5 shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
          >
            <template v-if="isSavingRecommendation">
              <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Saving...</span>
            </template>
            <template v-else>
              <DownloadIcon class="h-3.5 w-3.5" />
              <span>Save Recommendation</span>
            </template>
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- Details Modal - Using the same approach as the recommendation modal -->
  <div v-if="showDetailsModal" class="fixed inset-0 z-50 overflow-hidden">
    <!-- Backdrop with blur effect -->
    <div class="absolute inset-0 bg-black/50 backdrop-blur-[2px]" @click="closeDetailsModal"></div>
  
    <!-- Modal Content - Centered and above the backdrop -->
    <div class="absolute inset-0 flex items-center justify-center p-2 sm:p-4">
      <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-xl mx-auto h-full max-h-[95vh] sm:max-h-[90vh] flex flex-col overflow-hidden">
        
        <!-- Fixed Header with Green Background - Non-scrollable -->
        <div class="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 sm:px-6 py-4 sm:py-5 rounded-t-2xl flex-shrink-0">
          <h2 class="text-lg sm:text-xl font-semibold text-center">Crop Details</h2>
          <p class="text-xs sm:text-sm text-green-100 mt-1 text-center">Detailed information and management</p>
        </div>

        <!-- Scrollable Content Area -->
        <div class="flex-1 overflow-y-auto px-3 sm:px-4 py-4">
          <!-- Main Content Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 sm:gap-4">
            <!-- Left Column -->
            <div class="space-y-3 sm:space-y-4">
              <!-- Primary Recommendation -->
              <div class="bg-gradient-to-br from-green-50 to-emerald-50/50 rounded-lg p-3 sm:p-4">
                <div class="flex items-center gap-2 text-green-600 mb-2">
                  <SproutIcon class="h-4 w-4" />
                  <span class="text-xs font-medium">Recommended Crop</span>
                </div>
                <h3 class="text-lg sm:text-xl font-bold text-green-700 mb-1">{{ selectedPrediction?.crop }}</h3>
                <div class="flex items-baseline gap-1 mb-1">
                  <span class="text-xl sm:text-2xl font-bold text-green-600">{{ selectedPrediction?.successRate }}</span>
                  <span class="text-sm font-medium text-green-600">%</span>
                </div>
                <p class="text-xs text-gray-600">
                  Recommended on {{ new Date(selectedPrediction?.date).toLocaleString() }}
                </p>
              </div>

              <!-- Recommended Fertilizer -->
              <div class="bg-white rounded-lg p-3 sm:p-4 border border-gray-100 shadow-sm">
                <div class="flex items-center gap-2 text-green-600 mb-3">
                  <FlaskIcon class="h-4 w-4" />
                  <span class="text-xs font-medium">Recommended Fertilizer</span>
                </div>
                <div class="space-y-2">
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-700">Type:</span>
                    <span class="text-sm text-gray-600">{{ selectedPrediction?.fertilizer?.type || 'N/A' }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-700">Name:</span>
                    <span class="text-sm text-gray-600">{{ selectedPrediction?.fertilizer?.name || 'N/A' }}</span>
                  </div>
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-700">Amount:</span>
                    <span class="text-sm text-gray-600">
                      {{ selectedPrediction?.fertilizer?.adjusted_amount || 0 }} {{ selectedPrediction?.fertilizer?.unit || '' }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Success Metrics moved here (was in right column) -->
              <div class="bg-white rounded-lg p-3 sm:p-4 border border-gray-100 shadow-sm">
                <div class="flex items-center gap-2 text-green-600 mb-3">
                  <TrendingUpIcon class="h-4 w-4" />
                  <span class="text-xs font-medium">Success Metrics</span>
                </div>
                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-600">Soil Compatibility</span>
                    <span class="text-xs font-medium text-gray-900">{{ selectedPrediction?.soilCompatibility }}%</span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-1.5 mb-1">
                    <div 
                      class="bg-green-500 h-1.5 rounded-full transition-all duration-300"
                      :style="{ width: `${selectedPrediction?.soilCompatibility}%` }"
                    />
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-600">Growth Rate</span>
                    <span class="text-xs font-medium text-gray-900">{{ selectedPrediction?.growthRate }}%</span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-1.5 mb-1">
                    <div 
                      class="bg-blue-500 h-1.5 rounded-full transition-all duration-300"
                      :style="{ width: `${selectedPrediction?.growthRate}%` }"
                    />
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-600">Yield Potential</span>
                    <span class="text-xs font-medium text-gray-900">{{ selectedPrediction?.yieldPotential }}%</span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-1.5 mb-1">
                    <div 
                      class="bg-purple-500 h-1.5 rounded-full transition-all duration-300"
                      :style="{ width: `${selectedPrediction?.yieldPotential}%` }"
                    />
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-3 sm:space-y-4">
              <!-- Alternative Options with Fertilizers -->
              <div class="bg-white rounded-lg p-3 sm:p-4 border border-gray-100 shadow-sm">
                <div class="flex items-center gap-2 text-green-600 mb-3">
                  <ListIcon class="h-4 w-4" />
                  <span class="text-xs font-medium">Alternative Options</span>
                </div>
                <div class="space-y-4">
                  <div v-for="option in alternativeCrops" :key="option.crop" class="space-y-2">
                    <!-- Crop Info -->
                    <div class="flex items-center justify-between">
                      <div>
                        <h4 class="text-sm font-medium text-gray-900">{{ option.crop }}</h4>
                        <p class="text-[10px] text-gray-500">Alternative crop</p>
                      </div>
                      <div class="text-right">
                        <div class="text-sm font-semibold text-gray-900">
                          {{ option.confidence }}%
                        </div>
                      </div>
                    </div>
                    <!-- Progress Bar -->
                    <div class="h-1.5 w-full bg-gray-100 rounded-full overflow-hidden">
                      <div 
                        class="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all duration-300" 
                        :style="{ width: `${option.confidence}%` }"
                      ></div>
                    </div>
                    <!-- Fertilizer Info -->
                    <div class="bg-gray-50 rounded-lg p-2 mt-2">
                      <div class="text-[10px] font-medium text-gray-600 mb-1">Recommended Fertilizer:</div>
                      <div class="grid grid-cols-2 gap-1 text-[10px]">
                        <div class="text-gray-500">Type:</div>
                        <div class="text-gray-700 text-right">{{ option.fertilizer?.type || 'N/A' }}</div>
                        <div class="text-gray-500">Name:</div>
                        <div class="text-gray-700 text-right">{{ option.fertilizer?.name || 'N/A' }}</div>
                        <div class="text-gray-500">Amount:</div>
                        <div class="text-gray-700 text-right">
                          {{ option.fertilizer?.adjusted_amount || 0 }} {{ option.fertilizer?.unit || '' }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Status Management moved here (was in left column) -->
              <div class="bg-white rounded-lg p-3 sm:p-4 border border-gray-100 shadow-sm">
                <div class="flex items-center gap-2 text-green-600 mb-3">
                  <ActivityIcon class="h-4 w-4" />
                  <span class="text-xs font-medium">Status Management</span>
                </div>
                <div class="grid grid-cols-2 gap-2">
                  <button
                    v-for="status in ['Planted', 'Ongoing', 'Harvested', 'Cancelled']"
                    :key="status"
                    @click="updateStatus(status)"
                    :class="[
                      'px-2 sm:px-3 py-1.5 sm:py-2 rounded-lg text-xs font-medium transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-1',
                      editedStatus === status
                        ? getStatusButtonClass(status)
                        : 'bg-gray-50 text-gray-600 hover:bg-gray-100 focus:ring-gray-200'
                    ]"
                  >
                    {{ status }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Fixed Footer with Action Buttons - Non-scrollable -->
        <div class="bg-gray-50 px-3 sm:px-4 py-3 sm:py-4 rounded-b-2xl border-t border-gray-100 flex-shrink-0">
          <div class="flex justify-end gap-2 sm:gap-3">
            <button 
              @click="closeDetailsModal"
              class="px-3 sm:px-4 py-2 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200 focus:ring-offset-1"
            >
              Close
            </button>
            <button 
              class="px-3 sm:px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-sm font-medium rounded-lg hover:from-green-600 hover:to-emerald-600 transition-colors flex items-center gap-1.5 shadow-sm focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-offset-1 disabled:opacity-70 disabled:cursor-not-allowed"
              @click="saveChanges"
              :disabled="isSavingChanges"
            >
              <template v-if="isSavingChanges">
                <svg class="animate-spin -ml-1 mr-1 h-3.5 w-3.5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span>Saving...</span>
              </template>
              <template v-else>
                <SaveIcon class="h-3.5 w-3.5" />
                <span>Save Changes</span>
              </template>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
// Script section remains the same as in the previous version
import { ref, computed, onMounted, onUnmounted, onBeforeMount, reactive } from 'vue'
import { 
  ChartBarIcon,
  ClipboardListIcon,
  TrendingUpIcon,
  ActivityIcon,
  ActivitySquareIcon,
  BeakerIcon,
  TestTubesIcon,
  DropletIcon,
  WavesIcon,
  ThermometerIcon,
  CloudIcon,
  SproutIcon,
  XIcon,
  ListIcon,
  SearchIcon,
  FilterIcon,
  ChevronLeftIcon,
  ChevronRightIcon,
  LayoutGridIcon,
  InfoIcon,
  DownloadIcon,
  ArrowUpIcon,
  ArrowDownIcon,
  WarehouseIcon,
  CalendarIcon,
  EyeIcon,
  BeakerIcon as FlaskIcon,
  SaveIcon,
  TableIcon,
  MinusIcon,
  PrinterIcon,
} from 'lucide-vue-next'
import api from '../../api/index.js'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun } from 'docx'
import { saveAs } from 'file-saver'
import 'jspdf-autotable';

// Initialize all sensor data as reactive refs
const nitrogen = ref(0)
const phosphorus = ref(0)
const potassium = ref(0)
const soilpH = ref(0)
const soilMoisture = ref(0)
const temperature = ref(0)
const humidity = ref(0)

// Add new state for grid view and filter panel
const isGridView = ref(true)
const showFilterPanel = ref(false)

// Filter states
const filterSuccessRateMin = ref('')
const filterSuccessRateMax = ref('')
const filterDateStart = ref('')
const filterDateEnd = ref('')
const filterStatus = ref('')

const isSavingChanges = ref(false);

const showModal = ref(false)
const recommendedCrop = ref('')
const successRate = ref(0)
const soilCompatibility = ref(0)
const growthRate = ref(0)
const yieldPotential = ref(0)
const alternativeOptions = ref([])
const fertilizer = ref({
  type: '',
  name: '',
  base_amount: 0,
  adjusted_amount: 0,
  unit: ''
})

const predictions = ref([])
const filteredPredictionsCache = ref([]) // Cache for filtered predictions
const searchQuery = ref('')
const currentPage = ref(1)
const itemsPerPage = ref(6)
const activeFilter = ref('All')

const showDetailsModal = ref(false)
const selectedPrediction = ref(null)
const alternativeCrops = ref([])
const recommendedFertilizers = ref([])
const editedStatus = ref(null)

const isStatsLoading = ref(true); // For the top metric cards
const isPredictionsLoading = ref(true); // For the predictions table/grid
const isSensorDataLoading = ref(false); // For the NPK, pH, etc. input cards
const isSavingRecommendation = ref(false); // For the save recommendation button in the modal
const isRecommending = ref(false); // For the "Get Crop Recommendations" button

// Add these constants at the top of your script section
const MAX_VALUES = {
  nitrogen: 200, // mg/kg
  phosphorus: 200, // mg/kg
  potassium: 200, // mg/kg
  soilpH: 14, // pH scale
  soilMoisture: 100, // percentage
  temperature: 50, // °C
  humidity: 100 // percentage
}

// const printTable = () => {
//   const headers = printHeaders.value || [
//     { key: 'crop', label: 'Recommended Crop' },
//     { key: 'date', label: 'Date & Time' },
//     { key: 'successRate', label: 'Success Rate' },
//     { key: 'status', label: 'Status' }
//   ];

//   // Build the HTML content step by step to avoid template literal issues
//   let printContent = `<!DOCTYPE html><html><head>
//     <title>Crop Recommendations Report</title>
//     <style>
//       @page {
//         size: ${printSettings.paperSize} ${printSettings.orientation};
//         margin: ${printSettings.margin};
//       }
//       body {
//         font-family: Arial, sans-serif;
//         font-size: 12px;
//         margin: 0;
//         padding: 0;
//         -webkit-print-color-adjust: exact;
//         print-color-adjust: exact;
//       }
//       .print-page {
//         width: 100%;
//         height: 100%;
//         page-break-after: always;
//         margin-bottom: 0;
//       }
//       .print-page:last-child {
//         page-break-after: auto;
//       }
//       table {
//         width: 100%;
//         border-collapse: collapse;
//         margin: 0;
//       }
//       th, td {
//         border: 1px solid #ddd;
//         padding: 4px;
//         text-align: left;
//       }
//       th {
//         background-color: #f2f2f2;
//         font-weight: bold;
//       }
//       .header {
//         text-align: center;
//         margin-bottom: 10px;
//         padding-bottom: 5px;
//         border-bottom: 1px solid #ddd;
//       }
//       .footer {
//         text-align: center;
//         margin-top: 10px;
//         padding-top: 5px;
//         border-top: 1px solid #ddd;
//         font-size: 0.9em;
//         color: #666;
//       }
//     </style>
//     <script>
//       // Try to print directly to the default printer
//       function tryDirectPrint() {
//         try {
//           // First attempt: regular print (will show dialog)
//           window.print();
          
//           // If we reach here, the print was initiated
//           setTimeout(function() {
//             window.close();
//           }, 1000);
//         } catch (e) {
//           console.error('Print error:', e);
//           window.close();
//         }
//       }
      
//       // Auto-trigger print when the window loads
//       window.onload = function() {
//         setTimeout(tryDirectPrint, 100);
//       };
//     <` + `/script>
//   </head><body>`;

//   // Add page content
//   previewPages.value.forEach((page, index) => {
//     printContent += `<div class="print-page">`;
    
//     if (printSettings.includeHeader) {
//       printContent += `
//         <div class="header">
//           <h1>Crop Recommendations Report</h1>
//           <p>Page ${index + 1} of ${previewPages.value.length} • ${new Date().toLocaleDateString()}</p>
//         </div>`;
//     }
    
//     printContent += `
//       <table>
//         <thead>
//           <tr>`;
    
//     headers.forEach(header => {
//       printContent += `<th>${header.label}</th>`;
//     });
    
//     printContent += `
//           </tr>
//         </thead>
//         <tbody>`;
    
//     page.data.forEach(prediction => {
//       printContent += `
//           <tr>
//             <td>${prediction.crop}</td>
//             <td>${prediction.date.split(',')[1]?.trim() || prediction.date.split(',')[0]}</td>
//             <td>${prediction.successRate}%</td>
//             <td>${prediction.status}</td>
//           </tr>`;
//     });
    
//     printContent += `
//         </tbody>
//       </table>`;
    
//     if (printSettings.includeFooter) {
//       printContent += `
//         <div class="footer">
//           Confidential • AgriTech Dashboard
//         </div>`;
//     }
    
//     printContent += `</div>`;
//   });
  
//   printContent += `</body></html>`;
  
//   // Open print window with specific features that might help with printing
//   const printWindow = window.open('', '_blank', 'width=800,height=600,scrollbars=yes');
  
//   if (!printWindow) {
//     alert('Please allow popups for this site to enable printing.');
//     return;
//   }
  
//   // Write content to the window
//   printWindow.document.open();
//   printWindow.document.write(printContent);
//   printWindow.document.close();
// };

const printTable = () => {
  // Create a printable version of the table data
  const headers = [
    { key: 'crop', label: 'Recommended Crop' },
    { key: 'date', label: 'Date & Time' },
    { key: 'successRate', label: 'Success Rate' },
    { key: 'status', label: 'Status' }
  ];

  // Build the HTML content for printing
  let printContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Crop Recommendations Report</title>
      <meta name="robots" content="noindex">
      <style>
        /* Force print styles */
        @media print {
          @page {
            margin: 15mm;
            size: portrait;
          }
          
          body {
            font-family: Arial, sans-serif;
            font-size: 12pt;
            margin: 0;
            padding: 0;
            color: #000;
            background: #fff;
            width: 100%;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
          }
          
          h1 {
            text-align: center;
            margin-bottom: 10px;
            color: #000;
            font-size: 18pt;
            font-weight: bold;
          }
          
          .report-info {
            text-align: center;
            margin-bottom: 15px;
            border-bottom: 1px solid #000;
            padding-bottom: 10px;
            font-size: 10pt;
          }
          
          table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            page-break-inside: auto;
          }
          
          tr {
            page-break-inside: avoid;
            page-break-after: auto;
          }
          
          th, td {
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
            color: #000;
            background: #fff !important;
          }
          
          th {
            background-color: #f0f0f0 !important;
            font-weight: bold;
          }
          
          .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 10pt;
            color: #000;
          }
        }
        
        /* Screen styles */
        @media screen {
          body {
            font-family: Arial, sans-serif;
            font-size: 12px;
            margin: 15mm;
            padding: 0;
            background-color: white;
          }
          
          h1 {
            text-align: center;
            margin-bottom: 10px;
            color: #2d3748;
          }
          
          .report-info {
            text-align: center;
            margin-bottom: 15px;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 10px;
          }
          
          table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
          }
          
          th, td {
            border: 1px solid #cbd5e0;
            padding: 6px;
            text-align: left;
          }
          
          th {
            background-color: #f7fafc;
            font-weight: bold;
          }
          
          .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 10px;
            color: #718096;
          }
        }
      </style>
    </head>
    <body>
      <h1>Crop Recommendations Report</h1>
      <div class="report-info">
        Generated on: ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}
      </div>
      <table>
        <thead>
          <tr>
  `;
  
  // Add table headers
  headers.forEach(header => {
    printContent += `<th>${header.label}</th>`;
  });
  
  printContent += `
          </tr>
        </thead>
        <tbody>
  `;
  
  // Add table rows
  filteredPredictions.value.forEach(prediction => {
    printContent += `
          <tr>
            <td>${prediction.crop}</td>
            <td>${prediction.date.split(',')[1]?.trim() || prediction.date.split(',')[0]}</td>
            <td>${prediction.successRate}%</td>
            <td>${prediction.status}</td>
          </tr>
    `;
  });
  
  printContent += `
        </tbody>
      </table>
      <div class="footer">
        Confidential • AgriTech Dashboard • Page 1 of 1
      </div>
    </body>
    </html>
  `;
  
  // Create a blob and open it as a PDF-like document
  const blob = new Blob([printContent], { type: 'text/html' });
  const url = URL.createObjectURL(blob);
  
  // Open in a new window and trigger print
  const printWindow = window.open(url, '_blank');
  
  // Ensure the content is loaded before printing
  printWindow.onload = function() {
    // Small delay to ensure all content is rendered
    setTimeout(() => {
      printWindow.print();
      
      // Clean up after printing
      printWindow.onafterprint = function() {
        URL.revokeObjectURL(url);
        printWindow.close();
      };
    }, 500);
  };
};

// Alternative approach using iframe for more control
const printWithIframe = () => {
  // Create a hidden iframe
  const iframe = document.createElement('iframe');
  iframe.style.position = 'fixed';
  iframe.style.right = '0';
  iframe.style.bottom = '0';
  iframe.style.width = '0';
  iframe.style.height = '0';
  iframe.style.border = 'none';
  document.body.appendChild(iframe);
  
  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
  
  // Create print content
  const headers = [
    { key: 'crop', label: 'Recommended Crop' },
    { key: 'date', label: 'Date & Time' },
    { key: 'successRate', label: 'Success Rate' },
    { key: 'status', label: 'Status' }
  ];
  
  let printContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Crop Recommendations Report</title>
      <style>
        @media print {
          @page {
            margin: 15mm;
            size: portrait;
          }
          
          body {
            font-family: Arial, sans-serif;
            font-size: 12pt;
            margin: 0;
            padding: 0;
            color: #000;
            background: #fff;
            width: 100%;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
          }
          
          h1 {
            text-align: center;
            margin-bottom: 10px;
            color: #000;
            font-size: 18pt;
            font-weight: bold;
          }
          
          .report-info {
            text-align: center;
            margin-bottom: 15px;
            border-bottom: 1px solid #000;
            padding-bottom: 10px;
            font-size: 10pt;
          }
          
          table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            page-break-inside: auto;
          }
          
          th, td {
            border: 1px solid #000;
            padding: 8px;
            text-align: left;
            color: #000;
            background: #fff !important;
          }
          
          th {
            background-color: #f0f0f0 !important;
            font-weight: bold;
          }
          
          .footer {
            text-align: center;
            margin-top: 20px;
            font-size: 10pt;
            color: #000;
          }
        }
      </style>
    </head>
    <body>
      <h1>Crop Recommendations Report</h1>
      <div class="report-info">
        Generated on: ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}
      </div>
      <table>
        <thead>
          <tr>
  `;
  
  headers.forEach(header => {
    printContent += `<th>${header.label}</th>`;
  });
  
  printContent += `
          </tr>
        </thead>
        <tbody>
  `;
  
  filteredPredictions.value.forEach(prediction => {
    printContent += `
          <tr>
            <td>${prediction.crop}</td>
            <td>${prediction.date.split(',')[1]?.trim() || prediction.date.split(',')[0]}</td>
            <td>${prediction.successRate}%</td>
            <td>${prediction.status}</td>
          </tr>
    `;
  });
  
  printContent += `
        </tbody>
      </table>
      <div class="footer">
        Confidential • AgriTech Dashboard • Page 1 of 1
      </div>
    </body>
    </html>
  `;
  
  iframeDoc.open();
  iframeDoc.write(printContent);
  iframeDoc.close();
  
  // Wait for iframe to load and then print
  iframe.onload = function() {
    setTimeout(function() {
      iframe.contentWindow.focus();
      
      // Try to trigger print with a slight delay
      setTimeout(function() {
        iframe.contentWindow.print();
        
        // Remove iframe after printing
        setTimeout(function() {
          document.body.removeChild(iframe);
        }, 100);
      }, 500);
    }, 100);
  };
};


// Add this helper method to your script
const getIntensityClass = (value, max, color) => {
  const percentage = Math.min(100, (value / max) * 100)
  if (percentage > 80) return `bg-${color}-600`
  if (percentage > 60) return `bg-${color}-500`
  if (percentage > 40) return `bg-${color}-400`
  if (percentage > 20) return `bg-${color}-300`
  return `bg-${color}-200`
}

// Function to toggle grid view
const toggleGridView = () => {
  isGridView.value = !isGridView.value
}

// Function to toggle filter panel
const toggleFilterPanel = () => {
  showFilterPanel.value = !showFilterPanel.value
}

// Function to reset filters
const resetFilters = () => {
  filterSuccessRateMin.value = ''
  filterSuccessRateMax.value = ''
  filterDateStart.value = ''
  filterDateEnd.value = ''
  filterStatus.value = ''
  
  // Reset to original predictions
  filteredPredictionsCache.value = [...predictions.value]
  currentPage.value = 1
}

// Function to apply filters
const applyFilters = () => {
  let filtered = [...predictions.value]
  
  // Apply success rate filter
  if (filterSuccessRateMin.value !== '') {
    filtered = filtered.filter(p => p.successRate >= parseFloat(filterSuccessRateMin.value))
  }
  
  if (filterSuccessRateMax.value !== '') {
    filtered = filtered.filter(p => p.successRate <= parseFloat(filterSuccessRateMax.value))
  }
  
  // Apply date filter
  if (filterDateStart.value !== '') {
    const startDate = new Date(filterDateStart.value)
    filtered = filtered.filter(p => new Date(p.date) >= startDate)
  }
  
  if (filterDateEnd.value !== '') {
    const endDate = new Date(filterDateEnd.value)
    endDate.setHours(23, 59, 59, 999) // Set to end of day
    filtered = filtered.filter(p => new Date(p.date) <= endDate)
  }
  
  // Apply status filter
  if (filterStatus.value !== '') {
    filtered = filtered.filter(p => p.status === filterStatus.value)
  }
  
  // Update filtered predictions cache
  filteredPredictionsCache.value = filtered
  
  // Reset to first page
  currentPage.value = 1
}

// Greenhouse data - now all parameters are dynamic
const greenhouse1Data = ref({
  nitrogen: '32',
  phosphorus: '121',
  potassium: '114',
  ph: '5.3',
  moisture: '0.0',
  temperature: '27.1',
  humidity: '81.7',
})

const greenhouse2Data = ref({
  nitrogen: '92.15',
  phosphorus: '25.32',
  potassium: '83.76',
  ph: '6.98',
  moisture: '48.50',
  temperature: '30.75',
  humidity: '72.34'
})

const showExportDropdown = ref(false);

// Add these methods
const toggleExportDropdown = () => {
  showExportDropdown.value = !showExportDropdown.value;
};

const closeExportDropdown = () => {
  showExportDropdown.value = false;
};

const exportCropData = (format) => {
  // Prepare headers
  const headers = [
    'Recommended Crop',
    'Date',
    'Time',
    'Success Rate',
    'Status',
    'Soil Compatibility',
    'Growth Rate',
    'Yield Potential',
    'Fertilizer Type',
    'Fertilizer Name',
    'Fertilizer Amount'
  ];

  // Prepare rows
  const rows = filteredPredictions.value.map(prediction => [
    prediction.crop,
    prediction.date.split(',')[0],
    prediction.date.split(',')[1]?.trim() || '',
    `${prediction.successRate}%`,
    prediction.status,
    `${prediction.soilCompatibility}%`,
    `${prediction.growthRate}%`,
    `${prediction.yieldPotential}%`,
    prediction.fertilizer?.type || 'N/A',
    prediction.fertilizer?.name || 'N/A',
    prediction.fertilizer 
      ? `${prediction.fertilizer.adjusted_amount} ${prediction.fertilizer.unit}` 
      : 'N/A'
  ]);

  if (format === 'csv') {
    // CSV Export
    let csvContent = 'Crop Recommendations\n';
    csvContent += headers.join(',') + '\n';
    rows.forEach(row => {
      csvContent += row.map(val => `"${val}"`).join(',') + '\n';
    });
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    saveAs(blob, `crop_recommendations_${new Date().toISOString().split('T')[0]}.csv`);
    window.showToast && window.showToast('Crop recommendations exported as CSV', 'success');
  } else if (format === 'pdf') {
    // PDF Export
    const doc = new jsPDF();
    
    // Title
    doc.setFontSize(16);
    doc.text('Crop Recommendations', 14, 16);
    
    // Subtitle with date
    doc.setFontSize(10);
    doc.text(`Exported on: ${new Date().toLocaleString()}`, 14, 24);
    
    // Table
    autoTable(doc, {
      head: [headers],
      body: rows,
      startY: 30,
      styles: {
        fontSize: 8,
        cellPadding: 2,
        overflow: 'linebreak'
      },
      headStyles: {
        fillColor: [34, 197, 94], // green-500
        textColor: 255,
        fontSize: 9
      },
      alternateRowStyles: {
        fillColor: [243, 244, 246] // gray-100
      },
      columnStyles: {
        0: { cellWidth: 25 }, // Crop
        1: { cellWidth: 20 }, // Date
        2: { cellWidth: 15 }, // Time
        3: { cellWidth: 15 }, // Success Rate
        4: { cellWidth: 15 }, // Status
        5: { cellWidth: 15 }, // Soil Comp.
        6: { cellWidth: 15 }, // Growth Rate
        7: { cellWidth: 15 }, // Yield Pot.
        8: { cellWidth: 15 }, // Fert. Type
        9: { cellWidth: 20 }, // Fert. Name
        10: { cellWidth: 20 } // Fert. Amount
      }
    });
    
    doc.save(`crop_recommendations_${new Date().toISOString().split('T')[0]}.pdf`);
    window.showToast && window.showToast('Crop recommendations exported as PDF', 'success');
  }
  
  showExportDropdown.value = false;
};

// Close dropdown when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showExportDropdown.value = false;
  }
};

let esp32_1_unsubscribe = null;
let esp32_2_unsubscribe = null;
const streamActive = ref(false);
const lastStreamUpdate = ref(null);

onMounted(async () => {
  isStatsLoading.value = true;
  isSensorDataLoading.value = true;
  
  // Fetch initial data
  await fetchLatestSensorData();
  await fetchSavedRecommendations();
  await fetchRecommendationStats();

  // Set up polling for sensor data (every 10 seconds)
  const sensorPollingInterval = setInterval(fetchLatestSensorData, 10000);
  
  // Cleanup on unmount
  onUnmounted(() => {
    clearInterval(sensorPollingInterval);
    document.removeEventListener('click', handleClickOutside);
  });
});


onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});

const fetchLatestSensorData = async () => {
  try {
    isSensorDataLoading.value = true;
    const response = await api.get('/sensors/latest');
    const sensorData = response.data;
    
    // Update sensor values
    nitrogen.value = Number(sensorData.nitrogen);
    phosphorus.value = Number(sensorData.phosphorus);
    potassium.value = Number(sensorData.potassium);
    soilpH.value = Number(sensorData.soilPh);
    temperature.value = Number(sensorData.temperature);
    humidity.value = Number(sensorData.humidity);
    soilMoisture.value = Number(sensorData.soilMoisture);
    
  } catch (error) {
    console.error("❌ Error fetching sensor data:", error);
    window.showToast('Failed to fetch sensor data', 'failed');
  } finally {
    isSensorDataLoading.value = false;
  }
};

const normalizeFirestoreTimestamp = (timestamp) => {
  // Handle Firestore Timestamp objects
  if (timestamp instanceof Timestamp) {
    return timestamp.toDate();
  }
  
  // Handle string formats like "2025-04-04T15:16:15.872307"
  if (typeof timestamp === 'string') {
    // Try ISO format first
    if (timestamp.includes('T')) {
      return new Date(timestamp);
    }
    
    // Handle custom format like "July 1, 2025 at 7:39:41 PM UTC+8"
    const dateParts = timestamp.split(' at ');
    if (dateParts.length === 2) {
      return new Date(dateParts.join(' ').replace(' ', ' '));
    }
  }
  
  // Handle object format with seconds/nanoseconds
  if (timestamp && typeof timestamp === 'object' && timestamp.seconds) {
    return new Date(timestamp.seconds * 1000);
  }
  
  // Fallback to current date
  console.warn("Unknown timestamp format, using current date:", timestamp);
  return new Date();
};

const statsVersion = 'v8'

// Track stats with localStorage persistence
const stats = ref({
  current: {
    total: 0,
    planted: 0,
    ongoing: 0,
    harvested: 0,
    successRate: 0
  },
  baseline: {
    total: 0,
    planted: 0,
    ongoing: 0,
    harvested: 0,
    successRate: 0,
    timestamp: null
  }
})

const fetchStatsBaseline = async () => {
  try {
    const docSnap = await getDoc(statsDocRef);
    if (docSnap.exists()) {
      const data = docSnap.data();
      stats.value.baseline = {
        total: data.total || 0,
        planted: data.planted || 0,
        ongoing: data.ongoing || 0,
        harvested: data.harvested || 0,
        successRate: data.successRate || 0,
        timestamp: data.timestamp?.toDate() || null
      };
    }
    console.log("Loaded baseline stats from Firestore:", stats.value.baseline);
  } catch (error) {
    console.error("Error loading baseline stats:", error);
  }
};

const updateStatsBaseline = async (newStats) => {
  try {
    const now = new Date();
    const baselineData = {
      ...newStats,
      timestamp: now
    };
    
    await setDoc(statsDocRef, baselineData, { merge: true });
    stats.value.baseline = baselineData;
    console.log("Updated baseline stats in Firestore:", baselineData);
  } catch (error) {
    console.error("Error updating baseline stats:", error);
  }
};

// Calculate percentage change (always shows change if baseline exists)
const calculateChange = (current, baseline) => {
  if (baseline === 0 || !stats.value.baseline.timestamp) {
    return { value: 0, isIncrease: false }
  }
  const change = ((current - baseline) / baseline) * 100
  return {
    value: Math.abs(Math.round(change * 10) / 10), // 1 decimal place
    isIncrease: change > 0
  }
}

// Computed properties - FORCE display changes when baseline exists
const totalRecommendations = computed(() => stats.value.current.total)
const plantedCount = computed(() => stats.value.current.planted)
const ongoingCount = computed(() => stats.value.current.ongoing)
const harvestSuccessRate = computed(() => stats.value.current.successRate)

const percentageChange = computed(() => {
  const change = calculateChange(stats.value.current.total, stats.value.baseline.total)
  return stats.value.baseline.timestamp ? change.value : 0
})
const isIncrease = computed(() => 
  calculateChange(stats.value.current.total, stats.value.baseline.total).isIncrease
)

const plantedPercentageChange = computed(() => {
  const change = calculateChange(stats.value.current.planted, stats.value.baseline.planted)
  return stats.value.baseline.timestamp ? change.value : 0
})
const plantedIsIncrease = computed(() => 
  calculateChange(stats.value.current.planted, stats.value.baseline.planted).isIncrease
)

const harvestRatePercentageChange = computed(() => {
  const change = calculateChange(stats.value.current.successRate, stats.value.baseline.successRate)
  return stats.value.baseline.timestamp ? change.value : 0
})
const harvestRateIsIncrease = computed(() => 
  calculateChange(stats.value.current.successRate, stats.value.baseline.successRate).isIncrease
)

const ongoingPercentageChange = computed(() => {
  const change = calculateChange(stats.value.current.ongoing, stats.value.baseline.ongoing)
  return stats.value.baseline.timestamp ? change.value : 0
})
const ongoingIsIncrease = computed(() => 
  calculateChange(stats.value.current.ongoing, stats.value.baseline.ongoing).isIncrease
)

// Update stats and baseline
const updateStats = async (newStats) => {
  const now = new Date();
  
  // Always update current stats
  stats.value.current = newStats;
  
  // Set baseline on first run or when empty
  if (!stats.value.baseline.timestamp) {
    await updateStatsBaseline(newStats);
  }
  
  // Update baseline daily
  const hoursDiff = (now - stats.value.baseline.timestamp) / (1000 * 60 * 60);
  if (hoursDiff > 24) {
    await updateStatsBaseline(newStats);
  }
};

// Modify the fetchRecommendationStats to use our new system
const fetchRecommendationStats = async () => {
  try {
    isStatsLoading.value = true;
    
    const response = await api.get('/recommendations/stats');
    const statsData = response.data;
    
    stats.value.current = statsData.current;
    stats.value.baseline = statsData.baseline;
    
    console.log('Stats updated:', statsData);
    isStatsLoading.value = false;
  } catch (error) {
    console.error('Error fetching stats:', error);
    isStatsLoading.value = false;
  }
};

onMounted(() => {
  fetchRecommendationStats()
})

const selectedGreenhouse = ref(1)

const currentGreenhouseData = computed(() => {
  return selectedGreenhouse.value === 1 ? greenhouse1Data.value : greenhouse2Data.value
})

const selectGreenhouse = (greenhouse) => {
  selectedGreenhouse.value = greenhouse
}

const submitForm = async () => {
  isRecommending.value = true;
  const payload = {
    nitrogen: parseFloat(nitrogen.value),
    phosphorus: parseFloat(phosphorus.value),
    potassium: parseFloat(potassium.value),
    soilpH: parseFloat(soilpH.value),
    soilMoisture: parseFloat(soilMoisture.value),
    temperature: parseFloat(temperature.value),
    humidity: parseFloat(humidity.value),
  }

  console.log("Payload being sent to backend:", payload)

  try {
    const res = await api.post('/crop/recommend', payload)
    console.log("Payload sent to backend:", payload)
    console.log("Full response:", res.data) // Debug log

    const result = res.data

    // Handle both response formats (legacy and new ML format)
    if (result.recommendations) {
      // New ML format processing
      const primaryRecommendation = result.recommendations[0]
      
      recommendedCrop.value = primaryRecommendation.crop
      successRate.value = (primaryRecommendation.confidence * 100).toFixed(2) // Convert to percentage
      soilCompatibility.value = primaryRecommendation.soil_compatibility
      growthRate.value = primaryRecommendation.growth_rate
      yieldPotential.value = primaryRecommendation.yield_potential
      fertilizer.value = primaryRecommendation.fertilizer || {}
      
      // Process alternative options and filter out 0% confidence options
      alternativeOptions.value = result.recommendations.slice(1)
        .map(option => ({
          crop: option.crop,
          confidence: (option.confidence * 100).toFixed(2), // Convert to percentage
          fertilizer: option.fertilizer ? {
            type: option.fertilizer.type || '',
            name: option.fertilizer.name || '',
            base_amount: option.fertilizer.base_amount || 0,
            adjusted_amount: option.fertilizer.adjusted_amount || 0,
            unit: option.fertilizer.unit || '',
            notes: option.fertilizer.notes || ''
          } : null,
          soilCompatibility: option.soil_compatibility,
          growthRate: option.growth_rate,
          yieldPotential: option.yield_potential
        }))
    } else {
      // Legacy format processing (keep your existing logic as fallback)
      recommendedCrop.value = result.recommendedCrop
      successRate.value = result.successRate
      alternativeOptions.value = (result.alternativeOptions || [])
        .map(option => ({
          crop: option?.crop || 'Unknown Crop',
          confidence: option?.confidence || 0,
          fertilizer: option?.fertilizer ? {
            type: option.fertilizer.type || '',
            name: option.fertilizer.name || '',
            base_amount: option.fertilizer.base_amount || 0,
            adjusted_amount: option.fertilizer.adjusted_amount || 0,
            unit: option.fertilizer.unit || '',
            notes: option.fertilizer.notes || ''
          } : null
        }))
      soilCompatibility.value = result.soilCompatibility
      growthRate.value = result.growthRate
      yieldPotential.value = result.yieldPotential
      fertilizer.value = result.fertilizer || {}
    }

    showModal.value = true
  } catch (error) {
    console.error('Fetch error:', error)
    window.showToast('Failed to get crop recommendations','failed')
  } finally {
    isRecommending.value = false
  }
}

const saveRecommendation = async () => {
  try {
    isSavingRecommendation.value = true;
    
    const recommendationData = {
      recommendedCrop: recommendedCrop.value,
      successRate: parseFloat(successRate.value),
      soilCompatibility: parseFloat(soilCompatibility.value),
      growthRate: parseFloat(growthRate.value),
      yieldPotential: parseFloat(yieldPotential.value),
      fertilizer: fertilizer.value,
      alternativeOptions: alternativeOptions.value,
      soilData: {
        nitrogen: parseFloat(nitrogen.value),
        phosphorus: parseFloat(phosphorus.value),
        potassium: parseFloat(potassium.value),
        soilpH: parseFloat(soilpH.value),
        soilMoisture: parseFloat(soilMoisture.value),
        temperature: parseFloat(temperature.value),
        humidity: parseFloat(humidity.value)
      },
      status: "Recommended"
    };

    const response = await api.post('/save', recommendationData);
    
    console.log("Recommendation saved with ID: ", response.data.id);
    window.showToast('Recommendation saved successfully', 'success');
    closeModal();
    
    fetchSavedRecommendations();
    fetchRecommendationStats();
  } catch (error) {
    console.error('Error saving recommendation:', error);
    window.showToast('Failed to save recommendation', 'failed');
  } finally {
    isSavingRecommendation.value = false;
  }
};

const closeModal = () => {
  showModal.value = false
}

const filters = [
  { name: 'All' },
  { name: 'Planted' },
  { name: 'Ongoing' },
  { name: 'Cancelled' },
  { name: 'Harvested' }
]

const tableHeaders = [
  { key: 'crop', label: 'Recommended Crop' },
  { key: 'date', label: 'Date & Time' },
  { key: 'successRate', label: 'Success Rate' },
  { key: 'status', label: 'Status' },
  { key: 'actions', label: 'Actions' }
]

const fetchSavedRecommendations = async () => {
  try {
    isPredictionsLoading.value = true;

    const response = await api.get('/recommendations');
    const recommendations = response.data;

    // Process and format the data
    const formattedRecommendations = recommendations.map(rec => {
      // Handle date formatting - use the pre-formatted date from backend
      let dateDisplay = rec.date || "N/A";
      
      // If backend didn't format it, try to format it here
      if (dateDisplay === "N/A" && rec.timestamp) {
        try {
          // Handle ISO format timestamp
          const dateObj = new Date(rec.timestamp);
          if (!isNaN(dateObj.getTime())) {
            dateDisplay = dateObj.toLocaleString();
          }
        } catch (e) {
          console.error("Error parsing timestamp:", e);
        }
      }

      return {
        id: rec.id,
        crop: rec.recommendedCrop || rec.crop || "Unknown Crop",
        successRate: rec.successRate || 0,
        status: rec.status || 'Recommended',
        date: dateDisplay,
        timestamp: rec.timestamp ? new Date(rec.timestamp) : new Date(),
        soilCompatibility: rec.soilCompatibility || 0,
        growthRate: rec.growthRate || 0,
        yieldPotential: rec.yieldPotential || 0,
        alternativeOptions: rec.alternativeOptions || [],
        fertilizer: rec.fertilizer || {
          type: '',
          name: '',
          base_amount: 0,
          adjusted_amount: 0,
          unit: ''
        }
      };
    });

    predictions.value = formattedRecommendations;
    filteredPredictionsCache.value = [...formattedRecommendations];
    
    console.log("✅ Recommendations loaded:", predictions.value);
    isPredictionsLoading.value = false;
  } catch (error) {
    console.error("❌ Error fetching recommendations:", error);
    window.showToast('Failed to fetch crop recommendations', 'failed');
    isPredictionsLoading.value = false;
  }
};
 
const filteredPredictions = computed(() => {
  // Start with the filtered cache if it exists, otherwise use all predictions
  let result = filteredPredictionsCache.value.length > 0 ? filteredPredictionsCache.value : predictions.value

  if (activeFilter.value !== 'All') {
    result = result.filter(p => p.status === activeFilter.value)
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(p => p.crop.toLowerCase().includes(query))
  }

  return result
})

const paginatedPredictions = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  const end = start + itemsPerPage.value
  return filteredPredictions.value.slice(start, end)
})

const totalPages = computed(() => Math.ceil(filteredPredictions.value.length / itemsPerPage.value))

const getStatusClass = (status) => {
  const classes = {
    'Planted': 'bg-green-100 text-green-700',
    'Ongoing': 'bg-blue-100 text-blue-700',
    'Cancelled': 'bg-red-100 text-red-700',
    'Harvested': 'bg-gray-100 text-gray-700',
    'Recommended': ''
  }
  return classes[status]
}

const showDetails = (prediction) => {
  selectedPrediction.value = prediction
  editedStatus.value = prediction.status  
  // Sort alternatives by confidence or successRate (whichever you save)
  const sortedAlternatives = [...(prediction.alternativeOptions || [])].sort(
    (a, b) => (b.confidence || b.successRate || 0) - (a.confidence || a.successRate || 0)
  )

  alternativeCrops.value = sortedAlternatives

  // If fertilizers were included
  recommendedFertilizers.value = prediction.recommendedFertilizers || []

  showDetailsModal.value = true
}

const updateStatus = (status) => {
  editedStatus.value = status
}

const getStatusButtonClass = (status) => {
  switch (status) {
    case 'Planted':
      return 'bg-green-100 text-green-700'
    case 'Ongoing':
      return 'bg-blue-100 text-blue-700'
    case 'Harvested':
      return 'bg-gray-100 text-gray-700'
    case 'Cancelled':
      return 'bg-red-100 text-red-700'
    default:
      return 'bg-gray-50 text-gray-600'
  }
}

const closeDetailsModal = () => {
  showDetailsModal.value = false
  selectedPrediction.value = null
  alternativeCrops.value = []
  recommendedFertilizers.value = []
  editedStatus.value = null
}

const saveChanges = async () => {
  if (!selectedPrediction.value || !editedStatus.value) return;
  isSavingChanges.value = true;

  try {
    console.log("🔍 Debug - Status update details:", {
      documentId: selectedPrediction.value.id,
      newStatus: editedStatus.value,
      endpoint: `/api/recommendations/${selectedPrediction.value.id}/status`
    });

    // Test different payload formats
    const payload = { status: editedStatus.value };
    console.log("🔍 Debug - Payload being sent:", JSON.stringify(payload));

    const response = await api.post(
      `/recommendations/${selectedPrediction.value.id}/status`,
      payload,
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );

    console.log("✅ Status update successful:", response.data);
    
    // Update local state
    selectedPrediction.value.status = editedStatus.value;
    
    // Update in the main predictions array
    const index = predictions.value.findIndex(p => p.id === selectedPrediction.value.id);
    if (index !== -1) {
      predictions.value[index].status = editedStatus.value;
    }

    window.showToast('Status updated successfully', 'success');
    closeDetailsModal();
    
    // Refresh stats
    fetchRecommendationStats();
  } catch (error) {
    console.error('❌ Error updating status:', error);
    if (error.response) {
      console.error('❌ Error status:', error.response.status);
      console.error('❌ Error data:', error.response.data);
      console.error('❌ Error headers:', error.response.headers);
    }
    window.showToast('Failed to update status', 'failed');
  } finally {
    isSavingChanges.value = false;
  }
};

</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Smooth transitions */
* {
  transition: all 200ms ease-in-out;
}

.body {
  overflow-x: hidden; /* Prevent horizontal scroll */
}

/* Enhanced hover effects */
.hover\:shadow-md:hover {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Custom scrollbar styling */
.scrollbar-thin {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.scrollbar-thin::-webkit-scrollbar {
  height: 6px;
  width: 6px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.scrollbar-thumb-gray-200::-webkit-scrollbar-thumb {
  background-color: rgba(229, 231, 235, 0.8);
}

.scrollbar-thumb-gray-200:hover::-webkit-scrollbar-thumb {
  background-color: rgba(209, 213, 219, 1);
}

.overflow-x-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(156, 163, 175, 0.5) transparent;
}

.overflow-x-auto::-webkit-scrollbar {
  height: 6px;
}

.overflow-x-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-x-auto::-webkit-scrollbar-thumb {
  background-color: rgba(156, 163, 175, 0.5);
  border-radius: 3px;
}

.overflow-y-auto {
  scrollbar-width: thin;
  scrollbar-color: rgba(20, 83, 45, 0.5) transparent;
}

.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background-color: rgba(20, 83, 45, 0.5);
  border-radius: 9999px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background-color: rgba(20, 83, 45, 0.7);
}

/* Card animations *

/* Responsive adjustments */
@media (max-width: 640px) {
  .text-xl {
    font-size: 1.1rem;
  }
  
  .p-6 {
    padding: 1rem;
  }
}

/* Gradient animations */
.bg-gradient-to-r {
  background-size: 200% 200%;
  animation: gradientShift 8s ease infinite;
}

@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}
/* Add this to your style section */
.page-preview {
  page-break-after: always;
  margin-bottom: 1px !important; /* Tiny gap between pages */
}

.page-preview:last-child {
  page-break-after: auto;
  margin-bottom: 0 !important;
}
</style>