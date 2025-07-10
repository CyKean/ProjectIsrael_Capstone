<template>
      <!-- Container Wrapper with proper spacing -->
      <div class="flex-1 w-full px-4 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
        <!-- Main Container with adjusted width -->
        <div class="bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-green-100 h-[calc(100vh-140px)] overflow-y-auto transition-all duration-300 ease-in-out hover:shadow-[0_12px_40px_rgb(0,0,0,0.12)]">
          <!-- Content Wrapper --> 
          <div class="p-4 sm:p-6">
            <!-- Clean Minimalist Metrics Section - With Loading State -->
            <div class="grid grid-cols-4 gap-4 mb-6">
              <!-- Total Predictions -->
              <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <ChartBarIcon class="h-5 w-5 text-purple-500" />
                    <span class="text-sm font-medium text-gray-700">Total</span>
                  </div>
                </div>
                <div v-if="!isStatsLoading" class="flex flex-col">
                  <div class="text-2xl font-bold text-gray-900 mb-2">{{ totalRecommendations }}</div>
                  <div 
                    :class="[
                      'text-xs font-medium',
                      isIncrease ? 'text-green-600' : 'text-red-600'
                    ]"
                  >
                    <!-- <span class="flex items-center">
                      <component
                        :is="isIncrease ? ArrowUpIcon : ArrowDownIcon"
                        class="w-3 h-3 mr-1"
                      />
                      {{ isIncrease ? '+' : '-' }}{{ percentageChange }}% {{ isIncrease ? 'increase' : 'decrease' }}
                    </span> -->
                  </div>
                </div>
                <div v-else class="animate-pulse">
                  <div class="h-7 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>

              <!-- Planted -->
              <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <SproutIcon class="h-5 w-5 text-green-500" />
                    <span class="text-sm font-medium text-gray-700">Planted</span>
                  </div>
                </div>
                <div v-if="!isStatsLoading" class="flex flex-col">
                  <div class="text-2xl font-bold text-gray-900 mb-2">{{ plantedCount }}</div>
                  <div 
                    :class="[
                      'text-xs font-medium',
                      plantedIsIncrease ? 'text-green-600' : 'text-red-600'
                    ]"
                  >
                    <!-- <span class="flex items-center">
                      <component
                        :is="plantedIsIncrease ? ArrowUpIcon : ArrowDownIcon"
                        class="w-3 h-3 mr-1"
                      />
                      {{ plantedIsIncrease ? '+' : '-' }}{{ plantedPercentageChange }}% {{ plantedIsIncrease ? 'increase' : 'decrease' }}
                    </span> -->
                  </div>
                </div>
                <div v-else class="animate-pulse">
                  <div class="h-7 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>

              <!-- Success Rate -->
              <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <ActivityIcon class="h-5 w-5 text-blue-500" />
                    <span class="text-sm font-medium text-gray-700">Rate</span>
                  </div>
                </div>
                <div v-if="!isStatsLoading" class="flex flex-col">
                  <div class="text-2xl font-bold text-gray-900 mb-2">{{ harvestSuccessRate }}%</div>
                  <div 
                    :class="[
                      'text-xs font-medium',
                      isIncrease ? 'text-green-600' : 'text-red-600'
                    ]"
                  >
                    <!-- <span class="flex items-center">
                      <component
                        :is="isIncrease ? ArrowUpIcon : ArrowDownIcon"
                        class="w-3 h-3 mr-1"
                      />
                      {{ isIncrease ? '+' : '-' }}{{ percentageChange }}% {{ isIncrease ? 'increase' : 'decrease' }}
                    </span> -->
                  </div>
                </div>
                <div v-else class="animate-pulse">
                  <div class="h-7 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>

              <!-- Ongoing -->
              <div class="bg-white rounded-xl p-5 border border-gray-100 shadow-sm">
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center gap-2">
                    <ClipboardListIcon class="h-5 w-5 text-red-500" />
                    <span class="text-sm font-medium text-gray-700">Active</span>
                  </div>
                </div>
                <div v-if="!isStatsLoading" class="flex flex-col">
                  <div class="text-2xl font-bold text-gray-900 mb-2">{{ ongoingCount }}</div>
                  <div 
                    :class="[
                      'text-xs font-medium',
                      ongoingIsIncrease ? 'text-green-600' : 'text-red-600'
                    ]"
                  >
                    <!-- <span class="flex items-center">
                      <component
                        :is="ongoingIsIncrease ? ArrowUpIcon : ArrowDownIcon"
                        class="w-3 h-3 mr-1"
                      />
                      {{ ongoingIsIncrease ? '+' : '-' }}{{ ongoingPercentageChange }}% {{ ongoingIsIncrease ? 'increase' : 'decrease' }}
                    </span> -->
                  </div>
                </div>
                <div v-else class="animate-pulse">
                  <div class="h-7 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div class="h-4 bg-gray-200 rounded w-1/2"></div>
                </div>
              </div>
            </div>

            <!-- Rest of the content remains the same -->
            <!-- Main Content Area -->
            <div class="space-y-6">
              <!-- Modified Prediction Form - Enhanced UI -->
              <div class="bg-white rounded-xl shadow-md p-5 sm:p-6 border border-gray-100 relative overflow-hidden">
                <!-- Background Pattern -->
                <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-green-50 to-transparent opacity-50 -z-10"></div>
                
                <!-- Enhanced Header -->
                <div class="mb-6">
                  <h2 class="text-xl font-semibold text-gray-800 flex items-center gap-2 tracking-wide">
                    <ActivitySquareIcon class="w-5 h-5 text-green-500" />
                    Crop Recommendations
                  </h2>
                  <p class="text-sm text-gray-500 mt-1">
                    Real-time soil analysis and environmental parameters
                  </p>
                </div>

                <!-- Form Fields Container -->
                <div class="space-y-6">
                  <!-- Primary Measurements Section -->
                  <div>
                    <h3 class="text-sm font-medium text-gray-700 mb-4 flex items-center">
                      <span class="inline-block w-1.5 h-1.5 bg-green-500 rounded-full mr-2"></span>
                      Soil Composition Analysis
                    </h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                      <!-- Nitrogen Level -->
                      <div class="relative group">
                        <template v-if="!isSensorDataLoading">
                          <div class="absolute inset-0 bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                          <div class="relative bg-white rounded-lg p-4 border border-gray-100 transition-all duration-300 hover:border-green-300 hover:shadow-md">
                            <div class="flex items-center gap-3 mb-3">
                              <div class="p-2 bg-green-50 rounded-lg">
                                <BeakerIcon class="w-4 h-4 text-green-600" />
                              </div>
                              <div>
                                <label class="block text-sm font-medium text-gray-500">Nitrogen (N)</label>
                                <div class="flex items-baseline gap-1 mt-0.5">
                                  <input 
                                    type="number"
                                    v-model="nitrogen"
                                    class="text-xl font-bold text-gray-900 bg-transparent w-20 focus:outline-none"
                                  />
                                  <span class="text-xs text-gray-500">mg/kg</span>
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
                          <div class="relative bg-white rounded-lg p-4 border border-gray-100 transition-all duration-300 hover:border-blue-300 hover:shadow-md">
                            <div class="flex items-center gap-3 mb-3">
                              <div class="p-2 bg-blue-50 rounded-lg">
                                <TestTubesIcon class="w-4 h-4 text-blue-600" />
                              </div>
                              <div>
                                <label class="block text-sm font-medium text-gray-500">Phosphorus (P)</label>
                                <div class="flex items-baseline gap-1 mt-0.5">
                                  <input 
                                    type="number"
                                    v-model="phosphorus"
                                    class="text-xl font-bold text-gray-900 bg-transparent w-20 focus:outline-none"
                                  />
                                  <span class="text-xs text-gray-500">mg/kg</span>
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
                          <div class="relative bg-white rounded-lg p-4 border border-gray-100 transition-all duration-300 hover:border-purple-300 hover:shadow-md">
                            <div class="flex items-center gap-3 mb-3">
                              <div class="p-2 bg-purple-50 rounded-lg">
                                <BeakerIcon class="w-4 h-4 text-purple-600" />
                              </div>
                              <div>
                                <label class="block text-sm font-medium text-gray-500">Potassium (K)</label>
                                <div class="flex items-baseline gap-1 mt-0.5">
                                  <input 
                                    type="number"
                                    v-model="potassium"
                                    class="text-xl font-bold text-gray-900 bg-transparent w-20 focus:outline-none"
                                  />
                                  <span class="text-xs text-gray-500">mg/kg</span>
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
                          <div class="relative bg-white rounded-lg p-4 border border-gray-100 transition-all duration-300 hover:border-amber-300 hover:shadow-md">
                            <div class="flex items-center gap-3 mb-3">
                              <div class="p-2 bg-amber-50 rounded-lg">
                                <DropletIcon class="w-4 h-4 text-amber-600" />
                              </div>
                              <div>
                                <label class="block text-sm font-medium text-gray-500">Soil pH</label>
                                <div class="flex items-baseline gap-1 mt-0.5">
                                  <input 
                                    type="number"
                                    v-model="soilpH"
                                    class="text-xl font-bold text-gray-900 bg-transparent w-20 focus:outline-none"
                                  />
                                  <span class="text-xs text-gray-500">pH</span>
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
                    <h3 class="text-sm font-medium text-gray-700 mb-4 flex items-center">
                      <span class="inline-block w-1.5 h-1.5 bg-blue-500 rounded-full mr-2"></span>
                      Environmental Parameters
                    </h3>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      <!-- Soil Moisture -->
                      <div class="relative group">
                        <template v-if="!isSensorDataLoading">
                          <div class="absolute inset-0 bg-gradient-to-r from-cyan-50 to-sky-50 rounded-xl transition-opacity opacity-0 group-hover:opacity-100"></div>
                          <div class="relative bg-white rounded-lg p-4 border border-gray-100 transition-all duration-300 hover:border-cyan-300 hover:shadow-md">
                            <div class="flex items-center gap-3 mb-3">
                              <div class="p-2 bg-cyan-50 rounded-lg">
                                <WavesIcon class="w-4 h-4 text-cyan-600" />
                              </div>
                              <div>
                                <label class="block text-sm font-medium text-gray-500">Soil Moisture</label>
                                <div class="flex items-baseline gap-1 mt-0.5">
                                  <input 
                                    type="number"
                                    v-model="soilMoisture"
                                    class="text-xl font-bold text-gray-900 bg-transparent w-20 focus:outline-none"
                                  />
                                  <span class="text-xs text-gray-500">%</span>
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
                          <div class="relative bg-white rounded-lg p-4 border border-gray-100 transition-all duration-300 hover:border-orange-300 hover:shadow-md">
                            <div class="flex items-center gap-3 mb-3">
                              <div class="p-2 bg-orange-50 rounded-lg">
                                <ThermometerIcon class="w-4 h-4 text-orange-600" />
                              </div>
                              <div>
                                <label class="block text-sm font-medium text-gray-500">Temperature</label>
                                <div class="flex items-baseline gap-1 mt-0.5">
                                  <input 
                                    type="number"
                                    v-model="temperature"
                                    class="text-xl font-bold text-gray-900 bg-transparent w-20 focus:outline-none"
                                  />
                                  <span class="text-xs text-gray-500">°C</span>
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
                          <div class="relative bg-white rounded-lg p-4 border border-gray-100 transition-all duration-300 hover:border-teal-300 hover:shadow-md">
                            <div class="flex items-center gap-3 mb-3">
                              <div class="p-2 bg-teal-50 rounded-lg">
                                <CloudIcon class="w-4 h-4 text-teal-600" />
                              </div>
                              <div>
                                <label class="block text-sm font-medium text-gray-500">Humidity</label>
                                <div class="flex items-baseline gap-1 mt-0.5">
                                  <input 
                                    type="number"
                                    v-model="humidity"
                                    class="text-xl font-bold text-gray-900 bg-transparent w-20 focus:outline-none"
                                  />
                                  <span class="text-xs text-gray-500">%</span>
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
                  <div class="flex justify-center mt-8">
                    <button 
                      type="submit"
                      @click="submitForm"
                      :disabled="isRecommending"
                      class="inline-flex items-center justify-center px-6 sm:px-8 py-3 text-base font-medium text-white bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl transition-all duration-300 hover:from-green-600 hover:to-emerald-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
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
              <div class="bg-white rounded-xl shadow-md p-5 sm:p-6 border border-gray-100 relative overflow-hidden">
                <!-- Background Pattern -->
                <div class="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-blue-50 to-transparent opacity-50 -z-10"></div>
                
                <!-- Enhanced Filter Tabs -->
                <div class="border-b border-gray-100 mb-6">
                  <div class="flex gap-4 overflow-x-auto scrollbar-thin scrollbar-thumb-gray-200 scrollbar-track-transparent pb-2">
                    <button 
                      v-for="filter in filters" 
                      :key="filter.name"
                      :class="[
                        'px-4 py-2.5 text-sm font-medium transition-all duration-200 relative whitespace-nowrap',
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
                <div class="flex flex-wrap justify-between items-center mb-6 gap-4">
                  <div class="relative flex-1 max-w-md">
                    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                      <SearchIcon class="h-4 w-4 text-gray-400" />
                    </div>
                    <input 
                      type="text"
                      v-model="searchQuery"
                      placeholder="Search predictions..."
                      class="w-full pl-10 pr-4 py-2 text-sm bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all duration-200"
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
                              class="px-4 py-3.5 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
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
                            <td class="px-4 py-3.5 whitespace-nowrap">
                              <div class="flex items-center gap-3">
                                <div class="flex items-center justify-center w-8 h-8 rounded-lg bg-green-50 text-green-600">
                                  <SproutIcon class="h-4 w-4" />
                                </div>
                                <span class="text-sm font-medium text-gray-900">
                                  {{ prediction.crop }}
                                </span>
                              </div>
                            </td>
                            <td class="px-4 py-3.5 whitespace-nowrap">
                              <div class="flex flex-col">
                                <span class="text-sm font-medium text-gray-900">
                                  {{ prediction.date.split(',')[1] }}
                                </span>
                                <span class="text-xs text-gray-500">
                                  {{ prediction.date.split(',')[0] }}
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
                <div class="mt-6 flex flex-wrap items-center justify-between gap-4">
                  <div class="flex items-center gap-2">
                    <label class="text-sm text-gray-600">Items per page</label>
                    <select 
                      v-model="itemsPerPage"
                      class="text-sm border border-gray-200 rounded-lg px-2 py-1 focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500"
                    >
                      <option value="5">5</option>
                      <option value="10">10</option>
                      <option value="20">20</option>
                    </select>
                  </div>
                  
                  <div class="flex items-center gap-2">
                    <button 
                      class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                      :disabled="currentPage === 1"
                      @click="currentPage--"
                    >
                      <ChevronLeftIcon class="h-4 w-4" />
                    </button>
                    
                    <div class="flex items-center gap-1">
                      <button 
                        v-for="page in totalPages"
                        :key="page"
                        :class="[
                          'px-3 py-1 text-sm font-medium rounded-lg transition-colors duration-200',
                          currentPage === page
                            ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white'
                            : 'text-gray-500 hover:bg-gray-50'
                        ]"
                        @click="currentPage = page"
                      >
                        {{ page }}
                      </button>
                    </div>
                    
                    <button 
                      class="p-2 text-gray-500 hover:text-gray-700 hover:bg-gray-50 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
                      :disabled="currentPage === totalPages"
                      @click="currentPage++"
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
        <div class="relative bg-white rounded-2xl shadow-xl max-w-xl w-full mx-auto">
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
          <div class="flex justify-end gap-2 p-6 pt-0 border-t border-gray-100">
            <button 
              @click="closeModal"
              class="px-4 py-2 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
            >
              Close
            </button>
            <button 
              @click="saveRecommendation"
              :disabled="isSavingRecommendation"
              class="px-4 py-2 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-sm font-medium rounded-lg hover:from-green-600 hover:to-emerald-600 transition-colors flex items-center justify-center gap-1.5 shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
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
      <div class="absolute inset-0 flex items-center justify-center p-4">
        <div class="relative bg-white rounded-2xl shadow-xl max-w-xl w-full mx-auto max-h-[90vh] overflow-y-auto">
          <!-- Modal Header -->
          <div class="text-center p-4 pb-0">
            <h2 class="text-lg font-semibold text-gray-800">Crop Details</h2>
            <p class="text-xs text-gray-500 mt-0.5">Detailed information and management</p>
          </div>

          <!-- Main Content Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 p-4">
            <!-- Left Column -->
            <div class="space-y-3">
              <!-- Primary Recommendation -->
              <div class="bg-gradient-to-br from-green-50 to-emerald-50/50 rounded-lg p-4">
                <div class="flex items-center gap-2 text-green-600 mb-2">
                  <SproutIcon class="h-4 w-4" />
                  <span class="text-xs font-medium">Recommended Crop</span>
                </div>
                <h3 class="text-lg font-bold text-green-700 mb-1">{{ selectedPrediction?.crop }}</h3>
                <div class="flex items-baseline gap-1 mb-1">
                  <span class="text-xl font-bold text-green-600">{{ selectedPrediction?.successRate }}</span>
                  <span class="text-sm font-medium text-green-600">%</span>
                </div>
                <p class="text-xs text-gray-600">
                  Recommended on {{ new Date(selectedPrediction?.date).toLocaleString() }}
                </p>
              </div>

              <!-- Recommended Fertilizer -->
              <div class="bg-white rounded-lg p-4 border border-gray-100 shadow-sm">
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

              <!-- Status Management -->
              <div class="bg-white rounded-lg p-3 border border-gray-100 shadow-sm">
                <div class="flex items-center gap-2 text-green-600 mb-2">
                  <ActivityIcon class="h-4 w-4" />
                  <span class="text-xs font-medium">Status Management</span>
                </div>
                <div class="grid grid-cols-2 gap-2">
                  <button
                    v-for="status in ['Planted', 'Ongoing', 'Harvested', 'Cancelled']"
                    :key="status"
                    @click="updateStatus(status)"
                    :class="[
                      'px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200',
                      editedStatus === status
                        ? getStatusButtonClass(status)
                        : 'bg-gray-50 text-gray-600 hover:bg-gray-100'
                    ]"
                  >
                    {{ status }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-3">
              <!-- Alternative Options with Fertilizers -->
              <div class="bg-white rounded-lg p-4 border border-gray-100 shadow-sm">
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
                        class="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all" 
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

              <!-- Success Metrics -->
              <div class="bg-white rounded-lg p-4 border border-gray-100 shadow-sm">
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
                      class="bg-green-500 h-1.5 rounded-full"
                      :style="{ width: `${selectedPrediction?.soilCompatibility}%` }"
                    />
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-600">Growth Rate</span>
                    <span class="text-xs font-medium text-gray-900">{{ selectedPrediction?.growthRate }}%</span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-1.5 mb-1">
                    <div 
                      class="bg-blue-500 h-1.5 rounded-full"
                      :style="{ width: `${selectedPrediction?.growthRate}%` }"
                    />
                  </div>
                  
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-600">Yield Potential</span>
                    <span class="text-xs font-medium text-gray-900">{{ selectedPrediction?.yieldPotential }}%</span>
                  </div>
                  <div class="w-full bg-gray-100 rounded-full h-1.5 mb-1">
                    <div 
                      class="bg-purple-500 h-1.5 rounded-full"
                      :style="{ width: `${selectedPrediction?.yieldPotential}%` }"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="flex justify-end gap-2 p-4 pt-3 border-t border-gray-100">
            <button 
              @click="closeDetailsModal"
              class="px-3 py-1.5 text-sm font-medium text-gray-600 rounded-lg hover:bg-gray-100 hover:text-gray-900 transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-gray-200"
            >
              Close
            </button>
            <button 
              class="px-3 py-1.5 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-sm font-medium rounded-lg hover:from-green-600 hover:to-emerald-600 transition-colors flex items-center gap-1.5 shadow-sm"
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
</template>

<script setup>
// Script section remains the same as in the previous version
import { ref, computed, onMounted, onUnmounted, onBeforeMount } from 'vue'
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
  TableIcon
} from 'lucide-vue-next'
import Sidebar from '../layout/Sidebar.vue'
// import Pagination from '../layout/Pagination.vue'
import api from '../../api/index.js'
import toastr from 'toastr'
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
    onSnapshot,
  } from 'firebase/firestore'
const db = getFirestore()

// Initialize all sensor data as reactive refs
const nitrogen = ref(0)
const phosphorus = ref(0)
const potassium = ref(0)
const soilpH = ref(0)
const soilMoisture = ref(0)
const temperature = ref(0)
const humidity = ref(0)

// Add new state for grid view and filter panel
const isGridView = ref(false)
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
const itemsPerPage = ref(5)
const activeFilter = ref('All')

const showDetailsModal = ref(false)
const selectedPrediction = ref(null)
const alternativeCrops = ref([])
const recommendedFertilizers = ref([])
const editedStatus = ref(null)

const totalRecommendations = ref(0)
const previousRecommendationCount = ref(0)
const percentageChange = ref(0)
const isIncrease = ref(true)

const plantedCount = ref(0)
const plantedPercentageChange = ref(0)
const plantedIsIncrease = ref(true)

const harvestSuccessRate = ref(0)
const harvestedCount = ref(0)
const previousSuccessRate = ref(0)

const ongoingCount = ref(0) // Ongoing Count
const ongoingPercentageChange = ref(0) // Ongoing Percentage Change
const ongoingIsIncrease = ref(true) // Ongoing Increase or Decrease


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

// onMounted(async () => {
//   isStatsLoading.value = true;
//   isSensorDataLoading.value = true; // Set loading for sensor data cards
//   await fetchLatestSensorDataFromFirebase()

//   // Step 2: Start listening for real-time updates
//   const eventSource = new EventSource('http://localhost:8000/api/stream')

//   eventSource.onmessage = (event) => {
//     const data = JSON.parse(event.data)

//     nitrogen.value = data.nitrogen
//     phosphorus.value = data.phosphorus
//     potassium.value = data.potassium
//     soilpH.value = data.soilPh
//     temperature.value = data.temperature
//     humidity.value = data.humidity
//     soilMoisture.value = data.soilMoisture

//     console.log("🔁 Real-time data:", data)
//   }

//   isPredictionsLoading.value = true;
//   fetchSavedRecommendations()
//   fetchRecommendationStats()
//   // isStatsLoading will be set to false within fetchRecommendationStats
// })

// // ✅ MODIFIED: Updated to fetch from new 3sensor_readings collection structure
// const fetchLatestSensorDataFromFirebase = async () => {
//   try {
//     // Fetch from esp32-1 (NPK + pH)
//     // isSensorDataLoading.value = true; // Already set in onMounted before calling this
//     const esp32_1_query = query(
//       collection(db, "3sensor_readings", "esp32-1", "readings"), 
//       orderBy("timestamp", "desc"), 
//       limit(1)
//     );
//     const esp32_1_snapshot = await getDocs(esp32_1_query);
    
//     if (!esp32_1_snapshot.empty) {
//       const esp32_1_data = esp32_1_snapshot.docs[0].data();
//       const timestamp = esp32_1_data.timestamp;
//       esp32_1_data.timestamp = timestamp instanceof Timestamp ? timestamp.toDate() : new Date(timestamp.seconds * 1000);
      
//       nitrogen.value = esp32_1_data.nitrogen;
//       phosphorus.value = esp32_1_data.phosphorus;
//       potassium.value = esp32_1_data.potassium;
//       soilpH.value = esp32_1_data.soilPh;
      
//       console.log("📥 ESP32-1 Data (NPK + pH):", esp32_1_data);
//     }

//     // Fetch from esp32-2 (Temperature, humidity, soil moisture)
//     const esp32_2_query = query(
//       collection(db, "3sensor_readings", "esp32-2", "readings"), 
//       orderBy("timestamp", "desc"), 
//       limit(1)
//     );
//     const esp32_2_snapshot = await getDocs(esp32_2_query);
    
//     if (!esp32_2_snapshot.empty) {
//       const esp32_2_data = esp32_2_snapshot.docs[0].data();
//       const timestamp = esp32_2_data.timestamp;
//       esp32_2_data.timestamp = timestamp instanceof Timestamp ? timestamp.toDate() : new Date(timestamp.seconds * 1000);
      
//       temperature.value = esp32_2_data.temperature;
//       humidity.value = esp32_2_data.humidity;
//       soilMoisture.value = esp32_2_data.soilMoisture;
      
//       console.log("📥 ESP32-2 Data (DHT21):", esp32_2_data);
//     }
//   } catch (err) {
//     console.error("❌ Error fetching from new Firebase collection:", err)
//   } finally {
//     isSensorDataLoading.value = false; // Set to false after fetching or if an error occurs
//   }
// }

let esp32_1_unsubscribe = null;
let esp32_2_unsubscribe = null;
const streamActive = ref(false);
const lastStreamUpdate = ref(null);

onMounted(async () => {
  isStatsLoading.value = true;
  isSensorDataLoading.value = true;
  
  // Setup Firebase real-time listeners
  fetchLatestSensorDataFromFirebase();

  // Start listening for SSE stream
  const eventSource = new EventSource('http://localhost:8000/api/stream');

  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      
      // Extract the actual sensor data from the "data" property
      const sensorData = data.data || {};
      
      // Convert to numbers and update values from stream
      if (sensorData.nitrogen !== undefined) nitrogen.value = Number(sensorData.nitrogen);
      if (sensorData.phosphorus !== undefined) phosphorus.value = Number(sensorData.phosphorus);
      if (sensorData.potassium !== undefined) potassium.value = Number(sensorData.potassium);
      if (sensorData.soilPh !== undefined) soilpH.value = Number(sensorData.soilPh);
      if (sensorData.temperature !== undefined) temperature.value = Number(sensorData.temperature);
      if (sensorData.humidity !== undefined) humidity.value = Number(sensorData.humidity);
      if (sensorData.soilMoisture !== undefined) soilMoisture.value = Number(sensorData.soilMoisture);
      
      // Mark stream as active
      streamActive.value = true;
      lastStreamUpdate.value = Date.now();
      console.log("🔁 Processed stream data:", sensorData);
    } catch (error) {
      console.error("Error processing stream data:", error);
    }
  };

  eventSource.onerror = (error) => {
    console.log("🚨 EventSource error:", error);
    console.log("🚨 Falling back to Firebase");
    streamActive.value = false;
    
    // Trigger Firebase update immediately on stream error
    fetchLatestSensorDataFromFirebase();
    
    // Attempt to reconnect after 5 seconds
    setTimeout(() => {
      if (eventSource.readyState === EventSource.CLOSED) {
        console.log("⏳ Attempting to reconnect to stream...");
        eventSource = new EventSource('http://localhost:8000/api/stream');
      }
    }, 5000);
  };

  // Set up stream health check
  const streamCheckInterval = setInterval(() => {
    if (lastStreamUpdate.value && (Date.now() - lastStreamUpdate.value) > 10000) {
      console.log("🔄 No stream data for 10 seconds, switching to Firebase");
      streamActive.value = false;
      fetchLatestSensorDataFromFirebase();
    }
  }, 5000);

  // Fetch other data
  isPredictionsLoading.value = true;
  fetchSavedRecommendations();
  fetchRecommendationStats();

  // Cleanup on unmount
  onUnmounted(() => {
    if (eventSource) eventSource.close();
    clearInterval(streamCheckInterval);
    if (esp32_1_unsubscribe) esp32_1_unsubscribe();
    if (esp32_2_unsubscribe) esp32_2_unsubscribe();
  });
});

const fetchLatestSensorDataFromFirebase = () => {
  try {
    isSensorDataLoading.value = true;
    
    // Clean up previous listeners if they exist
    if (esp32_1_unsubscribe) esp32_1_unsubscribe();
    if (esp32_2_unsubscribe) esp32_2_unsubscribe();

    // For esp32-1 (NPK + pH)
    const esp32_1_query = query(
      collection(db, "3sensor_readings", "esp32-1", "readings"), 
      orderBy("timestamp", "desc"), 
      limit(1)
    );
    
    esp32_1_unsubscribe = onSnapshot(esp32_1_query, (snapshot) => {
      if (!snapshot.empty) {
        const esp32_1_data = snapshot.docs[0].data();
        const timestamp = esp32_1_data.timestamp;
        
        // Convert to Date object if it's a Firestore Timestamp
        let dateObj;
        if (timestamp instanceof Timestamp) {
          dateObj = timestamp.toDate();
        } else if (timestamp.seconds) {
          // If it's an object with seconds and nanoseconds
          dateObj = new Date(timestamp.seconds * 1000);
        } else {
          // Otherwise, try to parse as string or use current date
          dateObj = new Date(timestamp);
        }
        
        // Only update if stream is inactive
        if (!streamActive.value) {
          nitrogen.value = Number(esp32_1_data.nitrogen);
          phosphorus.value = Number(esp32_1_data.phosphorus);
          potassium.value = Number(esp32_1_data.potassium);
          soilpH.value = Number(esp32_1_data.soilPh);
          console.log("📥 [Firebase Realtime] ESP32-1 Data (NPK + pH):", esp32_1_data);
        }
      }
    });

    // For esp32-2 (Temperature, humidity, soil moisture)
    const esp32_2_query = query(
      collection(db, "3sensor_readings", "esp32-2", "readings"), 
      orderBy("timestamp", "desc"), 
      limit(1)
    );
    
    esp32_2_unsubscribe = onSnapshot(esp32_2_query, (snapshot) => {
      if (!snapshot.empty) {
        const esp32_2_data = snapshot.docs[0].data();
        const timestamp = esp32_2_data.timestamp;
        let dateObj;
        if (timestamp instanceof Timestamp) {
          dateObj = timestamp.toDate();
        } else if (timestamp.seconds) {
          dateObj = new Date(timestamp.seconds * 1000);
        } else {
          dateObj = new Date(timestamp);
        }
        
        // Only update if stream is inactive
        if (!streamActive.value) {
          temperature.value = Number(esp32_2_data.temperature);
          humidity.value = Number(esp32_2_data.humidity);
          soilMoisture.value = Number(esp32_2_data.soilMoisture);
          console.log("📥 [Firebase Realtime] ESP32-2 Data (DHT21):", esp32_2_data);
        }
      }
    });
  } catch (err) {
    console.error("❌ Error setting up Firebase listeners:", err);
    toastr.error('Failed to connect to Firebase');
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

// Function to calculate percentage change between two periods
// Corrected calculatePercentageChange function
// const calculatePercentageChange = (currentCount, previousCount) => {
//   if (previousCount === 0) {
//     // Avoid division by zero - treat as 100% increase if we had 0 before
//     return {
//       percentageChange: currentCount > 0 ? 100 : 0,
//       isIncrease: currentCount > 0
//     };
//   }

//   const change = currentCount - previousCount;
//   const percentageChange = (change / previousCount) * 100;
  
//   return {
//     percentageChange: parseFloat(percentageChange.toFixed(1)),
//     isIncrease: change >= 0
//   };
// };

// Updated fetchRecommendationStats method
let statsUnsubscribe = null; // Store the unsubscribe function
let unsubscribeStats = null

// const fetchRecommendationStats = () => {
//   try {
//     isStatsLoading.value = true;
    
//     // Clean up previous listener if it exists
//     if (statsUnsubscribe) {
//       statsUnsubscribe();
//     }

//     const q = query(collection(db, 'crop_recommendations'), orderBy('timestamp', 'desc'));
    
//     // Set up real-time listener
//     statsUnsubscribe = onSnapshot(q, (snapshot) => {
//       try {
//         // Get current and previous period counts
//         const allDocs = snapshot.docs.map(doc => doc.data());
//         const currentPeriodCount = allDocs.length;
//         const previousPeriodCount = previousRecommendationCount.value || currentPeriodCount;

//         // Calculate for Total Recommendations
//         const totalChanges = calculatePercentageChange(currentPeriodCount, previousPeriodCount);
//         percentageChange.value = totalChanges.percentageChange;
//         isIncrease.value = totalChanges.isIncrease;
//         totalRecommendations.value = currentPeriodCount;
//         previousRecommendationCount.value = currentPeriodCount;

//         // Calculate for Planted
//         const plantedDocs = allDocs.filter(doc => doc.status === 'Planted');
//         const currentPlantedCount = plantedDocs.length;
//         const previousPlantedCount = plantedCount.value || currentPlantedCount;
        
//         const plantedChanges = calculatePercentageChange(currentPlantedCount, previousPlantedCount);
//         plantedPercentageChange.value = plantedChanges.percentageChange;
//         plantedIsIncrease.value = plantedChanges.isIncrease;
//         plantedCount.value = currentPlantedCount;

//         // Calculate for Ongoing
//         const ongoingDocs = allDocs.filter(doc => doc.status === 'Ongoing');
//         const currentOngoingCount = ongoingDocs.length;
//         const previousOngoingCount = ongoingCount.value || currentOngoingCount;
        
//         const ongoingChanges = calculatePercentageChange(currentOngoingCount, previousOngoingCount);
//         ongoingPercentageChange.value = ongoingChanges.percentageChange;
//         ongoingIsIncrease.value = ongoingChanges.isIncrease;
//         ongoingCount.value = currentOngoingCount;

//         // Calculate Success Rate (Harvested/Total)
//         const harvestedDocs = allDocs.filter(doc => doc.status === 'Harvested');
//         harvestedCount.value = harvestedDocs.length;
        
//         harvestSuccessRate.value = currentPeriodCount > 0
//           ? Math.round((harvestedCount.value / currentPeriodCount) * 100)
//           : 0;

//       } catch (error) {
//         console.error("❌ Error processing snapshot:", error);
//         toastr.error('Failed to process statistics update');
//       } finally {
//         isStatsLoading.value = false;
//       }
//     }, (error) => {
//       console.error("❌ Error with stats snapshot listener:", error);
//       toastr.error('Failed to connect to real-time statistics');
//       isStatsLoading.value = false;
//     });

//   } catch (error) {
//     console.error("❌ Error setting up stats listener:", error);
//     toastr.error('Failed to load statistics');
//     isStatsLoading.value = false;
//   }
// };

// Track previous counts in memory
// Track previous counts in component state
const previousCounts = ref({
  total: 0,
  planted: 0,
  ongoing: 0,
  harvested: 0,
  lastUpdated: null
})

const calculatePercentageChange = (current, previous) => {
  // If no previous data or counts are equal
  if (previous === 0 || current === previous) {
    return {
      percentage: 0,
      isIncrease: false
    }
  }

  const change = current - previous
  const percentage = (change / previous) * 100
  
  return {
    percentage: Math.abs(parseFloat(percentage.toFixed(1))),
    isIncrease: change > 0
  }
}

const fetchRecommendationStats = () => {
  try {
    isStatsLoading.value = true
    
    const q = query(collection(db, 'crop_recommendations'), orderBy('timestamp', 'desc'))
    
    return onSnapshot(q, (snapshot) => {
      const allDocs = snapshot.docs.map(doc => doc.data())
      const now = new Date()

      // Only update if data has changed significantly (more than 1 second old)
      if (!previousCounts.value.lastUpdated || 
          (now - previousCounts.value.lastUpdated) > 1000) {

        const currentTotal = allDocs.length
        const currentPlanted = allDocs.filter(d => d.status === 'Planted').length
        const currentOngoing = allDocs.filter(d => d.status === 'Ongoing').length
        const currentHarvested = allDocs.filter(d => d.status === 'Harvested').length

        // Calculate changes using previous counts
        const totalChange = calculatePercentageChange(currentTotal, previousCounts.value.total)
        const plantedChange = calculatePercentageChange(currentPlanted, previousCounts.value.planted)
        const ongoingChange = calculatePercentageChange(currentOngoing, previousCounts.value.ongoing)

        // Calculate success rate
        const successRate = currentTotal > 0 
          ? Math.round((currentHarvested / currentTotal) * 100)
          : 0

        // Update refs
        totalRecommendations.value = currentTotal
        percentageChange.value = totalChange.percentage
        isIncrease.value = totalChange.isIncrease

        plantedCount.value = currentPlanted
        plantedPercentageChange.value = plantedChange.percentage
        plantedIsIncrease.value = plantedChange.isIncrease

        ongoingCount.value = currentOngoing
        ongoingPercentageChange.value = ongoingChange.percentage
        ongoingIsIncrease.value = ongoingChange.isIncrease

        harvestSuccessRate.value = successRate

        // Update previous counts with current data
        previousCounts.value = {
          total: currentTotal,
          planted: currentPlanted,
          ongoing: currentOngoing,
          harvested: currentHarvested,
          lastUpdated: now
        }
      }

      isStatsLoading.value = false
    })

  } catch (error) {
    console.error('Error fetching stats:', error)
    isStatsLoading.value = false
  }
}

onMounted(() => {
  unsubscribeStats = fetchRecommendationStats()
})

onUnmounted(() => {
  if (unsubscribeStats) unsubscribeStats()
})

// Real-time listener version
const setupRealtimeListener = () => {
  const q = query(collection(db, 'crop_recommendations'), orderBy('timestamp', 'desc'))
  
  return onSnapshot(q, (snapshot) => {
    const allDocs = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data()
    }))

    // Current counts
    const currentTotal = allDocs.length
    const currentPlanted = allDocs.filter(d => d.status === 'Planted').length
    const currentOngoing = allDocs.filter(d => d.status === 'Ongoing').length
    const currentHarvested = allDocs.filter(d => d.status === 'Harvested').length

    // Calculate changes
    const totalChanges = calculatePercentageChange(currentTotal, previousCounts.value.total)
    const plantedChanges = calculatePercentageChange(currentPlanted, previousCounts.value.planted)
    const ongoingChanges = calculatePercentageChange(currentOngoing, previousCounts.value.ongoing)

    // Calculate success rate
    const successRate = currentTotal > 0 
      ? Math.round((currentHarvested / currentTotal) * 100)
      : 0

    // Update refs
    totalRecommendations.value = currentTotal
    percentageChange.value = totalChanges.percentage
    isIncrease.value = totalChanges.isIncrease

    plantedCount.value = currentPlanted
    plantedPercentageChange.value = plantedChanges.percentage
    plantedIsIncrease.value = plantedChanges.isIncrease

    ongoingCount.value = currentOngoing
    ongoingPercentageChange.value = ongoingChanges.percentage
    ongoingIsIncrease.value = ongoingChanges.isIncrease

    harvestSuccessRate.value = successRate

    // Update previous counts
    previousCounts.value = {
      total: currentTotal,
      planted: currentPlanted,
      ongoing: currentOngoing,
      harvested: currentHarvested
    }
  })
}

// Add cleanup in onUnmounted if using Composition API
onUnmounted(() => {
  if (statsUnsubscribe) {
    statsUnsubscribe();
  }
});

// const fetchRecommendationStats = async () => {
//   try {
//     isStatsLoading.value = true;
//     // Fetch all crop recommendation records
//     const snapshot = await getDocs(collection(db, 'crop_recommendations'), orderBy('timestamp', 'desc') )
//     const allDocs = snapshot.docs.map(doc => doc.data())

//     totalRecommendations.value = allDocs.length // Total count of all recommendations

//     // Calculate Harvested Count and Success Rate
//      const harvestedDocs = allDocs.filter(doc => doc.status === 'Harvested');
//     harvestedCount.value = harvestedDocs.length;

//     // Calculate success rate (harvested / total)
//     harvestSuccessRate.value = totalRecommendations.value > 0
//       ? Math.round((harvestedCount.value / totalRecommendations.value) * 100)
//       : 0;

//     // Calculate Planted Count and Percentage Change
//     const plantedDocs = allDocs.filter(doc => doc.status === 'Planted')
//     plantedCount.value = plantedDocs.length

//     // Calculate the percentage change for Planted recommendations
//     const plantedChanges = calculatePercentageChange(plantedDocs, 'Planted')

//     plantedPercentageChange.value = plantedChanges.percentageChange
//     plantedIsIncrease.value = plantedChanges.isIncrease

//     // Calculate Ongoing Count and Percentage Change
//     const ongoingDocs = allDocs.filter(doc => doc.status === 'Ongoing')
//     ongoingCount.value = ongoingDocs.length

//     const ongoingChanges = calculatePercentageChange(ongoingDocs, 'Ongoing')

//     ongoingPercentageChange.value = ongoingChanges.percentageChange
//     ongoingIsIncrease.value = ongoingChanges.isIncrease

//     // Calculate the percentage change for all recommendations
//     const recommendationChanges = calculatePercentageChange(allDocs)
//     percentageChange.value = recommendationChanges.percentageChange
//     isIncrease.value = recommendationChanges.isIncrease

//   } catch (error) {
//     console.error("❌ Error fetching recommendation stats:", error)
//   } finally {
//     isStatsLoading.value = false;
//   }
// }

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
    toastr.error('Failed to get crop recommendations')
  } finally {
    isRecommending.value = false
  }
}

const saveRecommendation = async () => {
  isSavingRecommendation.value = true;
  // Construct the document data matching your desired Firebase structure
  const recommendationData = {
    recommendedCrop: recommendedCrop.value,
    successRate: successRate.value,
    soilCompatibility: soilCompatibility.value,
    growthRate: growthRate.value,
    yieldPotential: yieldPotential.value,
    fertilizer: {
      type: fertilizer.value.type,
      name: fertilizer.value.name,
      base_amount: fertilizer.value.base_amount,
      adjusted_amount: fertilizer.value.adjusted_amount,
      unit: fertilizer.value.unit
    },
    alternativeOptions: alternativeOptions.value.map(alt => ({
      crop: alt.crop,
      confidence: alt.confidence,
      fertilizer: {
        type: alt.fertilizer.type,
        name: alt.fertilizer.name,
        base_amount: alt.fertilizer.base_amount,
        adjusted_amount: alt.fertilizer.adjusted_amount,
        unit: alt.fertilizer.unit
      }
    })),
    // Add soil reading data
    soilData: {
      nitrogen: nitrogen.value,
      phosphorus: phosphorus.value,
      potassium: potassium.value,
      soilpH: soilpH.value,
      soilMoisture: soilMoisture.value,
      temperature: temperature.value,
      humidity: humidity.value,
    },
    status: "Recommended", // Set default status
    timestamp: serverTimestamp() // Use Firebase server timestamp
  };

  try {
    // ✅ MODIFIED: Save soil reading to new collection structure
    // Save to esp32-1 for NPK + pH data
    const esp32_1_ref = await addDoc(collection(db, "3sensor_readings", "esp32-1", "readings"), {
      nitrogen: parseFloat(nitrogen.value),
      phosphorus: parseFloat(phosphorus.value),
      potassium: parseFloat(potassium.value),
      soilPh: parseFloat(soilpH.value),
      timestamp: serverTimestamp()
    });

    // Save to esp32-2 for environmental data
    const esp32_2_ref = await addDoc(collection(db, "3sensor_readings", "esp32-2", "readings"), {
      soilMoisture: parseFloat(soilMoisture.value),
      temperature: parseFloat(temperature.value),
      humidity: parseFloat(humidity.value),
      timestamp: serverTimestamp()
    });

    // Add a soilReadingId to the recommendationData.
    // You need to decide how to represent this. Using one of the IDs, e.g., from esp32-1:
    recommendationData.soilReadingId = esp32_1_ref.id;
    // If you need both, you could store them in an object or concatenate them,
    // but your target Firebase structure shows a single string for soilReadingId.

    // Now, save directly to the 'crop_recommendations' collection
    await addDoc(collection(db, "crop_recommendations"), recommendationData);
    
    console.log("✅ Saved recommendation directly to Firebase:", recommendationData);
    toastr.success('Recommendation Saved successfully')
    closeModal()
    fetchSavedRecommendations()
  } catch (error) {
    console.error('❌ Error saving recommendation:', error)
    toastr.error('Unexpected error, please try again')
  } finally {
    isSavingRecommendation.value = false;
  }
}


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

const fetchSavedRecommendations = () => {
  try {
    isPredictionsLoading.value = true;

    const q = query(collection(db, 'crop_recommendations'));

    const unsubscribe = onSnapshot(q, (querySnapshot) => {
      // Create an array of documents with normalized timestamps
      const docsWithTimestamps = querySnapshot.docs.map(doc => {
        const data = doc.data();
        let dateObj;
        let formattedDate = "N/A";

        // Handle different timestamp formats
        if (data.timestamp) {
          // Case 1: Firestore Timestamp object
          if (typeof data.timestamp.toDate === 'function') {
            try {
              dateObj = data.timestamp.toDate();
              formattedDate = dateObj.toLocaleString();
            } catch (e) {
              console.warn("Error converting Firestore timestamp:", e);
            }
          }
          // Case 2: Object with seconds/nanoseconds
          else if (data.timestamp.seconds && typeof data.timestamp.seconds === 'number') {
            dateObj = new Date(data.timestamp.seconds * 1000);
            formattedDate = dateObj.toLocaleString();
          }
          // Case 3: ISO string (e.g., "2025-04-04T15:16:15.872307")
          else if (typeof data.timestamp === 'string' && data.timestamp.includes('T')) {
            try {
              dateObj = new Date(data.timestamp);
              formattedDate = dateObj.toLocaleString();
            } catch (e) {
              console.warn("Error parsing ISO string:", e);
            }
          }
          // Case 4: Custom string format (e.g., "July 1, 2025 at 7:39:41 PM UTC+8")
          else if (typeof data.timestamp === 'string') {
            try {
              // Normalize the string to ISO format
              const normalized = data.timestamp
                .replace(' at ', ' ')
                .replace(' ', ' ')
                .replace(' UTC+8', ' GMT+0800');
              dateObj = new Date(normalized);
              formattedDate = dateObj.toLocaleString();
            } catch (e) {
              console.warn("Error parsing custom timestamp:", e);
            }
          }
        }

        // Fallback to current date if no valid timestamp
        if (!dateObj) {
          dateObj = new Date();
          formattedDate = dateObj.toLocaleString();
          console.warn("Using fallback date for document:", doc.id);
        }

        return {
          id: doc.id,
          crop: data.recommendedCrop,
          successRate: data.successRate,
          status: data.status || 'Recommended',
          date: formattedDate,
          timestamp: dateObj,  // Store as Date object for sorting
          soilCompatibility: data.soilCompatibility,
          growthRate: data.growthRate,
          yieldPotential: data.yieldPotential,
          alternativeOptions: data.alternativeOptions?.map(alt => ({
            ...alt,
            fertilizer: alt.fertilizer || {
              type: '',
              name: '',
              base_amount: 0,
              adjusted_amount: 0,
              unit: ''
            }
          })) || [],
          fertilizer: data.fertilizer || {
            type: '',
            name: '',
            base_amount: 0,
            adjusted_amount: 0,
            unit: ''
          }
        };
      });

      // Sort documents by timestamp (newest first)
      docsWithTimestamps.sort((a, b) => b.timestamp - a.timestamp);

      predictions.value = docsWithTimestamps;
      filteredPredictionsCache.value = [...docsWithTimestamps];
      
      console.log("✅ Sorted recommendations (newest first):", predictions.value);
      isPredictionsLoading.value = false;
    }, (error) => {
      console.error("❌ Error with onSnapshot listener:", error);
      toastr.error('Failed to fetch crop recommendations in real-time');
      isPredictionsLoading.value = false;
    });

    return unsubscribe;

  } catch (error) {
    console.error("❌ Error setting up onSnapshot for predictions:", error);
    toastr.error('Failed to set up real-time crop recommendation listener');
    isPredictionsLoading.value = false;
  }
};

// onMounted(fetchSavedRecommendations) // Already called in the main onMounted
 
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
  if (!selectedPrediction.value) return
   isSavingChanges.value = true;

  try {
    await api.post(`/crop/recommendations/${selectedPrediction.value.id}/status`, null, {
      params: { status: editedStatus.value }
    })

    selectedPrediction.value.status = editedStatus.value // update locally too

    // Optional: update in the main table
    const index = predictions.value.findIndex(p => p.id === selectedPrediction.value.id)
    if (index !== -1) predictions.value[index].status = editedStatus.value

    toastr.success('Status updated successfully')
    closeDetailsModal()
  } catch (err) {
    console.error('Error saving changes:', err)
    toastr.error('Failed to save changes')
  } finally {
    isSavingChanges.value = false;
  }
}

// const recommendationChanges = calculatePercentageChange(allDocs)
// percentageChange.value = recommendationChanges.percentageChange
// isIncrease.value = recommendationChanges.isIncrease

// const plantedChanges = calculatePercentageChange(plantedDocs, 'Planted')
// plantedPercentageChange.value = plantedChanges.percentageChange
// plantedIsIncrease.value = plantedChanges.isIncrease

// const ongoingChanges = calculatePercentageChange(ongoingDocs, 'Ongoing')
// ongoingPercentageChange.value = ongoingChanges.percentageChange
// ongoingIsIncrease.value = ongoingChanges.isIncrease
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

/* Card animations */
.bg-white {
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.bg-white:hover {
  transform: translateY(-2px);
}

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
</style>