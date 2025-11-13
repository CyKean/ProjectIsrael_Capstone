<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-85px)] mt-1 md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">        <!-- Gradient header for visual appeal -->      <!-- Gradient header for visual appeal -->
      <div class="bg-gradient-to-r from-emerald-50 to-white p-4 md:p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-sm md:text-xl font-semibold text-gray-800 mb-1">Soil Moisture Data Table</h1>
            <div class="flex items-center text-xs md:text-sm text-gray-500">
              <span class="text-emerald-600 font-medium">Soil Moisture</span>
              <ChevronRight class="h-3.5 w-3.5 mx-1 text-gray-400" />
              <span class="text-gray-600">Data Table</span>
            </div>
          </div>
          
          <!-- Controls aligned horizontally with improved styling -->
          <div class="flex md:block flex-row gap-2">
            <!-- Button group - wraps on mobile, nowrap on larger screens -->
            <div class="flex flex-col md:flex-row flex-wrap sm:flex-nowrap gap-2">
              <div class="relative flex-1 sm:w-56 md:w-72 min-w-0">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-3 sm:h-4 w-3 sm:w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search soil moisture data..."
                  class="w-full pl-8 sm:pl-10 pr-3 sm:pr-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 text-xs sm:text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                  v-model="searchQuery"
                  @input="performSearch"
                />
              </div>
              <!-- Filter Button -->
              <div class="flex flex-row gap-2">
                <div class="relative flex-1 sm:flex-none">
                  <button 
                    @click.stop="toggleDropdown('filter')"
                    class="w-full flex items-center justify-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 bg-white text-xs sm:text-sm text-gray-700 hover:text-green-600 transition-colors shadow-sm"
                  >
                    <Filter class="h-3 sm:h-4 w-3 sm:w-4 text-gray-500" />
                    <span class="hidden md:block">Filter</span>
                    <ChevronDown class="h-3 sm:h-4 w-3 sm:w-4 text-gray-400" :class="{ 'transform rotate-180': activeDropdown === 'filter' }" />
                  </button>
                  
                  <div 
                    v-show="activeDropdown === 'filter'"
                    class="fixed sm:absolute left-2 sm:left-auto sm:right-0 mt-2 w-[calc(100%-1rem)] sm:w-64 md:w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                    @click.stop
                  >
                    <div class="p-3 sm:p-4 space-y-3 sm:space-y-4 max-h-[60vh] sm:max-h-[400px] md:w-[320px] overflow-y-auto">
                      <div v-for="field in filterFields" :key="field.key" class="space-y-1.5 sm:space-y-2">
                        <label class="block text-xs sm:text-sm font-medium text-gray-700">{{ field.label }}</label>
                        <div class="flex items-center gap-2">
                          <input
                            v-model="filters[field.key].min"
                            type="number"
                            placeholder="Min"
                            class="w-full px-2 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-green-500 focus:border-green-500"
                          />
                          <span class="text-gray-400">-</span>
                          <input
                            v-model="filters[field.key].max"
                            type="number"
                            placeholder="Max"
                            class="w-full px-2 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-green-500 focus:border-green-500"
                          />
                        </div>
                      </div>
                      <button 
                        @click="applyFilters"
                        class="w-full px-3 sm:px-4 py-1.5 sm:py-2 bg-green-500 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-green-600 transition-colors"
                      >
                        Apply Filters
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Sort Button -->
                <div class="relative flex-1 sm:flex-none">
                  <button 
                    @click.stop="toggleDropdown('sort')"
                    class="w-full flex items-center justify-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 bg-white text-xs sm:text-sm text-gray-700 hover:text-green-600 transition-colors shadow-sm"
                  >
                    <ArrowUpDown class="h-3 sm:h-4 w-3 sm:w-4 text-gray-500" />
                    <span class="hidden md:block">Sort</span>
                    <ChevronDown class="h-3 sm:h-4 w-3 sm:w-4 text-gray-400" :class="{ 'transform rotate-180': activeDropdown === 'sort' }" />
                  </button>
                  
                  <div 
                    v-show="activeDropdown === 'sort'"
                    class="fixed sm:absolute left-2 sm:left-auto right-2 sm:right-0 mt-2 w-[calc(100%-1rem)] sm:w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                    @click.stop
                  >
                    <div class="py-1">
                      <button
                        v-for="header in headers"
                        :key="header.key"
                        @click="setSortKey(header.key)"
                        class="w-full px-3 sm:px-4 py-1.5 sm:py-2 text-left text-xs sm:text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between"
                      >
                        {{ header.label }}
                        <ArrowUpDown v-if="sortKey === header.key" class="h-3 w-3 text-green-500" />
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Export Button -->
                <div class="relative flex-1 sm:flex-none">
                  <button 
                    @click.stop="toggleDropdown('export')"
                    class="w-full flex items-center justify-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg bg-green-500 text-white text-xs sm:text-sm font-medium hover:bg-green-600 transition-colors shadow-sm"
                  >
                    <Download class="h-3 sm:h-4 w-3 sm:w-4" />
                    <span class="hidden md:block">Export</span>
                    <ChevronDown class="h-3 sm:h-4 w-3 sm:w-4" :class="{ 'transform rotate-180': activeDropdown === 'export' }" />
                  </button>
                  
                  <div 
                    v-show="activeDropdown === 'export'"
                    class="fixed sm:absolute left-2 sm:left-auto right-2 sm:right-0 mt-2 w-[calc(100%-1rem)] sm:w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                    @click.stop
                  >
                    <div class="py-1">
                      <button
                        v-for="format in exportFormats"
                        :key="format"
                        @click="exportData(format)"
                        class="w-full px-3 sm:px-4 py-1.5 sm:py-2 text-left text-xs sm:text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                      >
                        <span v-if="format === 'csv'" class="mr-2 text-green-500"><FileText class="h-3 sm:h-4 w-3 sm:w-4" /></span>
                        <span v-else-if="format === 'pdf'" class="mr-2 text-red-500"><FileText class="h-3 sm:h-4 w-3 sm:w-4" /></span>
                        Export as {{ format.toUpperCase() }}
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Print Button - Updated with Modal Approach -->
                <div class="relative flex-1 sm:flex-none">
                  <button 
                    @click="openPrintModal"
                    class="w-full flex items-center justify-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 bg-white text-xs sm:text-sm text-gray-700 hover:text-green-600 transition-colors shadow-sm"
                  >
                    <Printer class="h-3 sm:h-4 w-3 sm:w-4 text-gray-500" />
                    <span class="hidden md:block">Print</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Table and Graph Section - Flex container for side-by-side layout -->
      <div class="flex-1 overflow-y-auto md:overflow-hidden flex flex-col md:flex-row min-h-0">
        <!-- Live Graph Container - Smaller width compared to table, now scrollable -->
        <div class="w-full md:w-1/3 lg:w-1/3 md:max-w-[33.333%] border-r border-gray-200 bg-white p-4 md:overflow-y-auto flex-shrink-0">
          <div class="mb-3">
            <h3 class="text-sm font-semibold text-gray-700">Live Soil Moisture</h3>
            <p class="text-xs text-gray-500">Latest 20 readings - Real-time monitoring</p>
          </div>
          
          <!-- Enhanced Combined Graph Container -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
            <!-- Graph Header with improved styling -->
            <div class="p-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full bg-emerald-500 mr-1.5"></div>
                <span class="text-[10px] md:text-xs font-medium text-gray-700">Moisture (%)</span>
              </div>
              <div class="text-[10px] md:text-xs text-gray-500">
                Last updated: {{ lastUpdated }}
              </div>
            </div>
            
            <!-- Graph Canvas with current values overlay -->
            <div class="h-[280px] p-3 relative">
              <canvas ref="chartCanvas" class="w-full h-full"></canvas>
              
              <!-- Repositioned and Resized Current Values Indicator -->
              <div class="absolute top-3 left-3 bg-white/95 backdrop-blur-sm rounded-md px-2 py-1 shadow-sm border border-gray-100" style="max-width: 80px; z-index: 10;">
                <div class="text-[10px] font-medium text-gray-500 mb-0.5">Current</div>
                <div class="flex items-center">
                  <div class="w-1.5 h-1.5 rounded-full bg-emerald-500 mr-1"></div>
                  <div class="text-xs font-bold text-emerald-600">
                    {{ currentMoistureValue }}%
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Enhanced Graph Footer with Stats -->
            <div class="border-t border-gray-100 p-3">
              <!-- Moisture Stats -->
              <div>
                <div class="flex items-center mb-2">
                  <div class="w-3 h-3 rounded-full bg-emerald-500 mr-1.5"></div>
                  <div class="text-sm font-medium text-gray-700">Soil Moisture</div>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-emerald-50/50 rounded-md p-2">
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Min</div>
                    <div class="text-sm font-semibold text-emerald-600">{{ moistureStats.min }}%</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Avg</div>
                    <div class="text-sm font-semibold text-emerald-600">{{ moistureStats.avg }}%</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Max</div>
                    <div class="text-sm font-semibold text-emerald-600">{{ moistureStats.max }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Soil Status Information -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Soil Status Guide</h4>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-emerald-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Wet</span>
                </div>
                <span class="text-xs text-gray-500">≥ 70%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-yellow-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Medium</span>
                </div>
                <span class="text-xs text-gray-500">30% - 70%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-red-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Dry</span>
                </div>
                <span class="text-xs text-gray-500">< 30%</span>
              </div>
            </div>
          </div>
          
          <!-- Optimal Ranges section -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Optimal Ranges</h4>
            <div class="space-y-3">
              <div>
                <div class="flex items-center mb-1">
                  <div class="w-2 h-2 rounded-full bg-emerald-500 mr-1"></div>
                  <span class="text-xs font-medium text-gray-700">Soil Moisture</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-red-300 via-yellow-300 to-emerald-500 rounded-full" style="width: 70%"></div>
                </div>
                <div class="flex justify-between mt-1 text-[10px] text-gray-500">
                  <span>30%</span>
                  <span>50%</span>
                  <span>70%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
       <!-- Table Container - Larger width with FIXED ALIGNMENT -->
        <div class="w-full md:w-2/3 lg:w-2/3 flex flex-col">
          <!-- Mobile Card View (shown on small screens) -->
          <div class="sm:hidden flex-1 overflow-auto bg-white p-3 space-y-3">
            <div v-for="(row, index) in paginatedData" :key="index" 
                class="bg-gray-50 rounded-lg p-3 border border-gray-200">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <div class="text-xs font-medium text-gray-900">{{ row.date }}</div>
                  <div class="text-[10px] text-gray-500">{{ row.time }}</div>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Soil Moisture</div>
                  <div class="text-xs font-semibold text-blue-600">{{ row.soilMoisture }}%</div>
                </div>
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Status</div>
                  <span 
                    :class="[
                      'px-2 py-0.5 rounded-full text-[10px] font-medium',
                      row.soilStatus === 'WET' ? 'bg-emerald-100 text-emerald-800' :
                      row.soilStatus === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ row.soilStatus }}
                  </span>
                </div>
              </div>
            </div>
            
            <div v-if="paginatedData.length === 0 && !isLoading" 
                class="flex flex-col items-center justify-center py-8">
              <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
              <p class="text-gray-500 text-xs font-medium">No soil moisture data found</p>
              <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
            </div>
          </div>

          <!-- Desktop Table View (shown on medium screens and up) -->
          <div class="hidden sm:flex flex-1 flex-col min-h-0">
            <!-- Single Table Structure for Perfect Alignment -->
            <div class="flex-1 overflow-auto">
              <table class="w-full min-w-[600px] table-fixed">
                <!-- Fixed Header -->
                <thead class="sticky top-0 z-10 bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th class="w-[25%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                      <div class="text-blue-600">Soil Moisture</div>
                      <div class="text-gray-400 text-[10px]">PERCENTAGE (%)</div>
                    </th>
                    <th class="w-[25%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                      <div class="text-emerald-600">Soil Status</div>
                      <div class="text-gray-400 text-[10px]">CONDITION</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                      <div class="text-gray-600">Date</div>
                      <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                      <div class="text-gray-600">Time</div>
                      <div class="text-gray-400 text-[10px]">HH:MM:SS</div>
                    </th>
                  </tr>
                </thead>
                
                <!-- Table Body -->
                <tbody class="bg-white divide-y divide-gray-50">
                  <tr 
                    v-for="(row, index) in paginatedData" 
                    :key="index"
                    class="hover:bg-gray-50/50 transition-colors"
                  >
                    <td class="w-[25%] px-4 py-3.5 whitespace-nowrap md:text-[15px] border-b border-gray-200">
                      <div class="text-sm font-medium text-blue-600">
                        {{ row.soilMoisture }}
                      </div>
                    </td>
                    <td class="w-[25%] px-4 py-3.5 whitespace-nowrap md:text-[15px] border-b border-gray-200">
                      <span 
                        :class="[
                          'px-3 py-1 rounded-full text-xs font-medium',
                          row.soilStatus === 'WET' ? 'bg-emerald-100 text-emerald-800' :
                          row.soilStatus === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        ]"
                      >
                        {{ row.soilStatus }}
                      </span>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 whitespace-nowrap md:text-[15px] border-b border-gray-200">
                      <div class="text-sm font-medium text-gray-700">{{ row.date }}</div>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 whitespace-nowrap md:text-[15px] border-b border-gray-200">
                      <div class="text-sm font-medium text-gray-700">{{ row.time }}</div>
                    </td>
                  </tr>
                  
                  <!-- Empty state when no data -->
                  <tr v-if="paginatedData.length === 0 && !isLoading">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <FileSearch class="h-16 w-16 text-gray-300 mb-4" />
                        <p class="text-gray-500 text-lg font-medium">No soil moisture data found</p>
                        <p class="text-gray-400 text-sm mt-1">Try adjusting your search or filters</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Pagination with new style -->
          <div class="border-t border-gray-200 py-2 px-3 bg-gray-50">
            <div class="flex items-center justify-between">
              <div class="text-[10px] md:text-xs text-gray-600">
                Showing {{ (paginationInfo.currentPage - 1) * paginationInfo.itemsPerPage + 1 }} - 
                {{ Math.min(paginationInfo.currentPage * paginationInfo.itemsPerPage, paginationInfo.totalItems) }}
                of {{ paginationInfo.totalItems }}
              </div>
              <div class="flex items-center gap-1">
                <button 
                  @click="prevPage"
                  :disabled="!paginationInfo.hasPrev"
                  class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-emerald-600"
                >
                  <ChevronLeft class="w-3.5 h-3.5" />
                </button>
                
                <div class="flex items-center gap-1">
                  <button
                    v-for="(page, index) in displayedPages"
                    :key="index"
                    @click="goToPage(page)"
                    :disabled="page === '...'"
                    :class="[
                      'px-2 py-1 text-[10px] md:text-xs rounded min-w-[20px]',
                      page === paginationInfo.currentPage 
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
                  :disabled="!paginationInfo.hasNext"
                  class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-emerald-600"
                >
                  <ChevronRight class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Date Range Print Modal -->
      <div v-if="showPrintModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 z-50 flex items-center justify-center p-4">
        <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
          <!-- Modal Header -->
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-800">Select Date Range for Print</h3>
            <p class="text-sm text-gray-500 mt-1">Choose the date range for the soil moisture data you want to print</p>
          </div>
          
          <!-- Date Range Inputs -->
          <div class="px-6 py-4 space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
              <input 
                type="date" 
                v-model="printDateRange.start"
                class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
              <input 
                type="date" 
                v-model="printDateRange.end"
                class="w-full px-3 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm"
              >
            </div>

            <!-- Quick Date Range Buttons -->
            <!-- <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Quick Select</label>
              <div class="grid grid-cols-3 gap-2">
                <button
                  @click="setQuickDateRange('today')"
                  class="px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
                >
                  Today
                </button>
                <button
                  @click="setQuickDateRange('week')"
                  class="px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
                >
                  This Week
                </button>
                <button
                  @click="setQuickDateRange('month')"
                  class="px-3 py-2 text-xs bg-gray-100 hover:bg-gray-200 rounded-lg text-gray-700 transition-colors"
                >
                  This Month
                </button>
              </div>
            </div> -->

            <!-- Error Message -->
            <p v-if="printDateError" class="text-sm text-red-600 bg-red-50 p-2 rounded-lg">{{ printDateError }}</p>
          </div>
          
          <!-- Modal Footer -->
          <div class="px-6 py-4 border-t border-gray-200 bg-gray-50 rounded-b-lg">
            <div class="flex justify-end space-x-3">
              <button 
                @click="cancelPrint"
                class="px-4 py-2.5 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              <button 
                @click="handlePrintWithDateRange"
                :disabled="!printDateRange.start || !printDateRange.end"
                class="px-4 py-2.5 text-sm font-medium text-white bg-green-500 rounded-lg hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
              >
                <Printer class="h-4 w-4" />
                Print Selected Range
              </button>
            </div>
          </div>
        </div>
      </div>
      
    </div>
  </div>

  <!-- Loading Page Component -->
  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Soil Moisture Data" 
    message="Please wait while we fetch the latest soil moisture measurements"
  />
</template>
  
<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Search, Filter, Download, ChevronDown, ChevronRight, ChevronLeft, ArrowUpDown, FileText, FileSearch, Printer } from 'lucide-vue-next'
import LoadingPage from '../layout/LoadingPage.vue'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun } from 'docx'
import { saveAs } from 'file-saver'
import api from '../../api/index'

import Chart from 'chart.js/auto'

const soilMoistureData = ref([])
const isLoading = ref(true)

// Chart related variables - COMPLETELY NON-REACTIVE
const chartCanvas = ref(null)

// Use regular variables (not reactive) for chart instance and data
let chartInstance = null
let chartDataArray = []
let chartLabelsArray = []

const currentMoistureValue = ref('--')
const lastUpdated = ref('--')
const moistureStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})

// Add flags to prevent recursive updates and overlapping calls
let isUpdatingChart = false
let isPolling = false

let pollingInterval = null
const POLLING_FREQUENCY = 5000 

// Pagination state
const paginationInfo = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20,
  hasNext: false,
  hasPrev: false
})

const itemsPerPage = ref(20)

// Print date range state
const printDateRange = ref({
  start: '',
  end: ''
})

// Modal state
const showPrintModal = ref(false)
const printDateError = ref('')

// Modal methods
const openPrintModal = () => {
  // Initialize with default range (last 7 days) if not set
  if (!printDateRange.value.start || !printDateRange.value.end) {
    initializePrintDateRange()
  }
  showPrintModal.value = true
  printDateError.value = ''
}

const cancelPrint = () => {
  showPrintModal.value = false
  printDateError.value = ''
}

const handlePrintWithDateRange = async () => {
  // Validate dates
  if (!printDateRange.value.start || !printDateRange.value.end) {
    printDateError.value = 'Please select both start and end dates'
    return
  }

  const startDate = new Date(printDateRange.value.start)
  const endDate = new Date(printDateRange.value.end)

  if (startDate > endDate) {
    printDateError.value = 'Start date cannot be after end date'
    return
  }

  // Close modal and proceed with printing
  showPrintModal.value = false
  printDateError.value = ''
  
  isLoading.value = true

  try {
    const data = await fetchDataForDateRange(printDateRange.value.start, printDateRange.value.end)
    
    if (data.length === 0) {
      alert('No soil moisture data found for the selected date range.')
      isLoading.value = false
      return
    }

    await generatePrintForDateRange(data, printDateRange.value.start, printDateRange.value.end)

  } catch (error) {
    console.error('Error printing date range:', error)
    alert('Error generating print. Please try again.')
  } finally {
    isLoading.value = false
  }
}

// Initialize print date range with default values (last 7 days)
const initializePrintDateRange = () => {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - 7)
  
  printDateRange.value = {
    start: start.toISOString().split('T')[0],
    end: end.toISOString().split('T')[0]
  }
}

// Quick date range functions
const setQuickDateRange = (range) => {
  const today = new Date()
  const start = new Date()
  
  switch (range) {
    case 'today':
      start.setDate(today.getDate())
      break
    case 'week':
      start.setDate(today.getDate() - 7)
      break
    case 'month':
      start.setMonth(today.getMonth() - 1)
      break
  }
  
  printDateRange.value = {
    start: start.toISOString().split('T')[0],
    end: today.toISOString().split('T')[0]
  }
  printDateError.value = ''
}

// Fetch data for the table (paginated)
const fetchSoilMoistureData = async (page = 1, limit = 20) => {
  try {
    console.log(`🌱 Fetching table data - Page: ${page}, Limit: ${limit}`);

    const response = await api.get(`/soil-moisture?page=${page}&limit=${limit}`, {
      headers: {
        'Accept': 'application/json',
      }
    })

    console.log('📊 Table API Response:', response)
    
    let data, paginationData
    if (response && typeof response === 'object') {
      if (response.data !== undefined) {
        // Handle paginated response structure
        if (response.data.data && response.data.pagination) {
          data = response.data.data;
          paginationData = response.data.pagination;
        } else {
          // Fallback to non-paginated response
          data = response.data;
          paginationData = {
            currentPage: page,
            totalPages: Math.ceil(data.length / limit),
            totalItems: data.length,
            itemsPerPage: limit,
            hasNext: page < Math.ceil(data.length / limit),
            hasPrev: page > 1
          };
        }
      } else {
        data = [];
        paginationData = {
          currentPage: page,
          totalPages: 0,
          totalItems: 0,
          itemsPerPage: limit,
          hasNext: false,
          hasPrev: false
        };
      }
    }

    console.log('📊 Table data received:', data.length, 'items')

    if (!Array.isArray(data)) {
      console.error('❌ Expected array but got:', typeof data, data)
      throw new Error(`Expected array but got: ${typeof data}`)
    }

    const processedData = data.map((reading, index) => {
      let timestamp
      if (reading.timestamp) {
        if (typeof reading.timestamp === 'string') {
          timestamp = new Date(reading.timestamp)
        } else if (reading.timestamp instanceof Date) {
          timestamp = reading.timestamp
        } else {
          console.warn('Unknown timestamp format:', reading.timestamp)
          timestamp = new Date()
        }
      } else {
        timestamp = new Date()
      }

      const soilMoistureValue = reading.soilMoisture

      return {
        id: reading.id || `${(page - 1) * limit + index + 1}`,
        timestamp: timestamp.getTime() / 1000,
        soilMoisture: Number(soilMoistureValue).toFixed(2),
        soilStatus: calculateSoilStatus(Number(soilMoistureValue)),
        date: timestamp.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: '2-digit'
        }),
        time: timestamp.toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        }),
        rawTimestamp: timestamp, 
        deviceId: reading.deviceId || 'esp32-2'
      }
    })

    // Update the table data only
    soilMoistureData.value = processedData
    
    // Store pagination info
    paginationInfo.value = paginationData;
    
    isLoading.value = false
    
    console.log(`✅ Successfully loaded ${processedData.length} table records for page ${page}`)

  } catch (error) {
    console.error("❌ Error fetching table data:", error)
    isLoading.value = false
  }
}

// Fetch data for the chart (always latest 20 readings)
const fetchChartData = async () => {
  try {
    const response = await api.get('/soil-moisture/recent?limit=20', {
      headers: {
        'Accept': 'application/json',
      }
    });

    if (!response?.data) {
      return;
    }

    // Process data
    const newChartData = Array.isArray(response.data) ? response.data : [];
    if (newChartData.length === 0) {
      return;
    }

    // Process data without Vue reactivity
    const processedData = newChartData
      .map(reading => ({
        timestamp: new Date(reading.timestamp || Date.now()),
        value: Number(reading.soilMoisture) || 0
      }))
      .sort((a, b) => a.timestamp - b.timestamp);

    // Update stats
    if (processedData.length > 0) {
      const values = processedData.map(item => item.value);
      const latestReading = processedData[processedData.length - 1];

      currentMoistureValue.value = latestReading.value.toFixed(2);
      lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      });

      moistureStats.value = {
        min: Math.min(...values).toFixed(2),
        max: Math.max(...values).toFixed(2),
        avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2)
      };
    }

    // Update chart arrays directly (non-reactive)
    chartDataArray = processedData.map(item => item.value);
    chartLabelsArray = processedData.map(item => 
      item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    );

    console.log('📊 Chart data updated:', chartDataArray.length, 'points');

    // Update chart safely
    if (!chartInstance) {
      console.log('🔄 Initializing chart for the first time');
      nextTick(() => {
        initializeChart();
      });
    } else {
      console.log('🔄 Updating existing chart');
      safeUpdateChart();
    }

  } catch (error) {
    console.error('Error fetching chart data:', error);
  }
};

// Safe chart update with protection against recursion
const safeUpdateChart = () => {
  if (isUpdatingChart || !chartInstance) {
    console.log('Chart update skipped - already updating or chart not ready');
    return;
  }

  isUpdatingChart = true;

  try {
    console.log('🔄 Starting chart update');
    
    // Update chart data directly - no Vue reactivity involved
    chartInstance.data.labels = [...chartLabelsArray];
    chartInstance.data.datasets[0].data = [...chartDataArray];

    // Update chart with no animation
    chartInstance.update('none');
    
    console.log('✅ Chart updated successfully');
    
  } catch (error) {
    console.error('Error updating chart:', error);
  } finally {
    isUpdatingChart = false;
  }
};

// Initialize chart when component mounts
const initializeChart = () => {
  if (!chartCanvas.value) {
    console.log('Chart canvas not ready, retrying...');
    setTimeout(initializeChart, 100);
    return;
  }

  try {
    // Destroy existing chart if it exists
    if (chartInstance) {
      console.log('Destroying existing chart');
      chartInstance.destroy();
      chartInstance = null;
    }

    const ctx = chartCanvas.value.getContext('2d');
    
    console.log('🔄 Creating new chart with data:', chartDataArray.length, 'points');
    
    // Create chart with initial data
    chartInstance = new Chart(ctx, {
      type: 'line',
      data: {
        labels: [...chartLabelsArray],
        datasets: [{
          label: 'Soil Moisture (%)',
          data: [...chartDataArray],
          borderColor: '#10b981',
          backgroundColor: 'rgba(16, 185, 129, 0.15)',
          borderWidth: 2.5,
          tension: 0.4,
          fill: true,
          pointRadius: 3,
          pointHoverRadius: 5,
          pointBackgroundColor: '#10b981',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 2
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 0
        },
        interaction: {
          intersect: false,
          mode: 'index'
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: true,
            mode: 'index',
            intersect: false,
            callbacks: {
              label: function(context) {
                return `Moisture: ${context.parsed.y}%`;
              },
              title: function(context) {
                return `Time: ${context[0].label}`;
              }
            }
          }
        },
        scales: {
          x: {
            display: true,
            title: {
              display: true,
              text: 'Time',
              color: '#6b7280',
              font: {
                size: 12
              }
            },
            grid: {
              display: false
            },
            ticks: {
              maxTicksLimit: 8,
              callback: function(value, index, values) {
                // Show fewer labels for better performance
                return index % Math.ceil(values.length / 6) === 0 ? this.getLabelForValue(value) : '';
              }
            }
          },
          y: {
            display: true,
            title: {
              display: true,
              text: 'Moisture (%)',
              color: '#6b7280',
              font: {
                size: 12
              }
            },
            min: 0,
            max: 100,
            grid: {
              color: 'rgba(0, 0, 0, 0.04)'
            },
            ticks: {
              callback: function(value) {
                return value + '%';
              }
            }
          }
        }
      }
    });

    console.log('✅ Chart initialized successfully');

  } catch (error) {
    console.error('Error initializing chart:', error);
    isUpdatingChart = false;
  }
};

// Combined polling function with debouncing
const setupPollingListener = () => {
  let intervalId = null;
  
  const poll = async () => {
    if (isPolling) {
      return; // Skip if already polling
    }
    
    isPolling = true;
    
    try {
      await fetchSoilMoistureData(paginationInfo.value.currentPage, itemsPerPage.value);
      await fetchChartData();
    } catch (error) {
      console.error('Polling error:', error);
    } finally {
      isPolling = false;
    }
  };

  // Initial fetch
  console.log('🔄 Starting initial data fetch');
  poll();
  
  // Set up interval with longer delay to prevent overlap
  intervalId = setInterval(poll, POLLING_FREQUENCY + 1000);
  
  // Return cleanup function
  return () => {
    if (intervalId) {
      clearInterval(intervalId);
    }
    isPolling = false;
    isUpdatingChart = false;
  };
};

// Update pagination functions to only fetch table data
const nextPage = async () => {
  if (paginationInfo.value.hasNext) {
    const nextPage = paginationInfo.value.currentPage + 1;
    isLoading.value = true;
    await fetchSoilMoistureData(nextPage, itemsPerPage.value);
  }
}

const prevPage = async () => {
  if (paginationInfo.value.hasPrev) {
    const prevPage = paginationInfo.value.currentPage - 1;
    isLoading.value = true;
    await fetchSoilMoistureData(prevPage, itemsPerPage.value);
  }
}

const goToPage = async (page) => {
  if (typeof page === 'number' && page >= 1 && page <= paginationInfo.value.totalPages) {
    isLoading.value = true;
    await fetchSoilMoistureData(page, itemsPerPage.value);
  }
}

// Fetch data for date range printing
const fetchDataForDateRange = async (startDate, endDate) => {
  try {
    console.log(`📅 Fetching data for date range: ${startDate} to ${endDate}`)
    
    // Convert dates to proper format for API
    const start = new Date(startDate)
    const end = new Date(endDate)
    end.setHours(23, 59, 59, 999) // Include entire end date
    
    // Fetch all data and filter client-side
    const response = await api.get('/soil-moisture/all', {
      headers: {
        'Accept': 'application/json',
      }
    })

    let allData = []
    if (response && response.data) {
      allData = Array.isArray(response.data) ? response.data : []
    }

    // Filter data by date range
    const filteredData = allData.filter(reading => {
      const readingDate = new Date(reading.timestamp)
      return readingDate >= start && readingDate <= end
    })

    // Sort by timestamp descending
    filteredData.sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))

    console.log(`✅ Found ${filteredData.length} records in date range`)

    return filteredData

  } catch (error) {
    console.error('❌ Error fetching data for date range:', error)
    return []
  }
}

// Print current page (original functionality)
const printCurrentPage = () => {
  printTable()
}

// Original print table function (for current page)
const printTable = async () => {
  const tempContainer = document.createElement('div');
  tempContainer.style.width = '800px';
  tempContainer.style.height = '400px';
  tempContainer.style.position = 'absolute';
  tempContainer.style.left = '-9999px';
  tempContainer.style.backgroundColor = 'white';
  tempContainer.style.padding = '20px';
  
  const tempCanvas = document.createElement('canvas');
  tempCanvas.width = 800;
  tempCanvas.height = 400;
  tempContainer.appendChild(tempCanvas);
  document.body.appendChild(tempContainer);
  
  const now = new Date();
  const formattedDate = now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });
  
  // Use current table data for the table in print
  const soilMoistureRows = soilMoistureData.value.map(row => ({
    id: row.id,
    date: row.date,
    time: row.time,
    device: row.deviceId || 'N/A',
    soilMoisture: row.soilMoisture,
    soilStatus: row.soilStatus
  }));
  
  // Use chart data arrays for the chart in print
  const printChartData = chartDataArray.map((value, index) => ({
    timestamp: new Date(Date.now() - (chartDataArray.length - index - 1) * 60000), // Approximate timestamps
    value: value
  }));
  
  console.log(`📊 Print chart will show ${printChartData.length} latest records from chart data`);
  
  // Calculate statistics from chart data
  const printChartValues = printChartData.map(item => item.value);
  const overallMin = printChartValues.length > 0 ? Math.min(...printChartValues) : 0;
  const overallMax = printChartValues.length > 0 ? Math.max(...printChartValues) : 100;
  const overallAvg = printChartValues.length > 0 ? 
    (printChartValues.reduce((sum, val) => sum + val, 0) / printChartValues.length) : 0;
  
  let chartImage = '';
  
  try {
    const ctx = tempCanvas.getContext('2d');
    
    // Calculate dynamic y-axis scaling
    const dataRange = overallMax - overallMin;
    const yAxisPadding = dataRange * 0.1;
    const yMin = Math.max(0, Math.floor(overallMin - yAxisPadding));
    const yMax = Math.min(100, Math.ceil(overallMax + yAxisPadding));
    
    const tempChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartLabelsArray,
        datasets: [{
          label: 'Soil Moisture (%) - Latest 20 Readings',
          data: chartDataArray, 
          borderColor: '#10b981', 
          backgroundColor: 'rgba(16, 185, 129, 0.15)', 
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 2,
          pointHoverRadius: 4,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#10b981',
          pointBorderWidth: 1.5
        }]
      },
      options: {
        responsive: false,
        maintainAspectRatio: false,
        animation: false, 
        plugins: {
          legend: { 
            display: true,
            position: 'top',
            labels: {
              usePointStyle: true,
              padding: 20,
              font: { size: 14 }
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `Moisture: ${context.raw.toFixed(1)}%`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            min: yMin,
            max: yMax,
            title: {
              display: true,
              text: 'Moisture (%)',
              color: '#10b981',
              font: {
                size: 14,
                weight: '600'
              }
            },
            ticks: {
              font: { size: 12 },
              color: '#64748b',
              stepSize: calculateStepSize(dataRange),
              callback: function(value) {
                return value + '%';
              }
            },
            grid: {
              color: 'rgba(100, 116, 139, 0.2)'
            }
          },
          x: {
            ticks: {
              font: { size: 9 },
              color: '#64748b',
              maxTicksLimit: 10,
              maxRotation: 45,
              callback: function(value, index, values) {
                return index % Math.ceil(values.length / 10) === 0 ? this.getLabelForValue(value) : '';
              }
            },
            grid: {
              display: false
            }
          }
        }
      }
    });
    
    setTimeout(async () => {
      try {
        chartImage = tempCanvas.toDataURL('image/png', 1.0);
        
        tempChart.destroy();
        document.body.removeChild(tempContainer);
        
        generatePrintHTML(chartImage, soilMoistureRows, formattedDate, now, printChartData.length, overallMin, overallMax, overallAvg);
      } catch (error) {
        console.error('Error capturing chart:', error);
        document.body.removeChild(tempContainer);
        generatePrintHTML('', soilMoistureRows, formattedDate, now, 0, 0, 0, 0);
      }
    }, 500);
    
  } catch (error) {
    console.error('Error creating chart:', error);
    document.body.removeChild(tempContainer);
    generatePrintHTML('', soilMoistureRows, formattedDate, now, 0, 0, 0, 0);
  }
};

// Generate print for date range
const generatePrintForDateRange = async (data, startDate, endDate) => {
  const tempContainer = document.createElement('div')
  tempContainer.style.width = '800px'
  tempContainer.style.height = '400px'
  tempContainer.style.position = 'absolute'
  tempContainer.style.left = '-9999px'
  tempContainer.style.backgroundColor = 'white'
  tempContainer.style.padding = '20px'
  
  const tempCanvas = document.createElement('canvas')
  tempCanvas.width = 800
  tempCanvas.height = 400
  tempContainer.appendChild(tempCanvas)
  document.body.appendChild(tempContainer)
  
  const now = new Date()
  const formattedDate = now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
  
  // Process data for printing
  const soilMoistureRows = data.map((reading, index) => {
    const timestamp = new Date(reading.timestamp)
    return {
      id: reading.id || `${index + 1}`,
      date: timestamp.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: '2-digit'
      }),
      time: timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      }),
      device: reading.deviceId || 'N/A',
      soilMoisture: Number(reading.soilMoisture).toFixed(2),
      soilStatus: calculateSoilStatus(Number(reading.soilMoisture)),
      rawTimestamp: timestamp
    }
  })
  
  // Prepare chart data
  const printChartData = data
    .map(reading => ({
      timestamp: new Date(reading.timestamp),
      value: Number(reading.soilMoisture)
    }))
    .sort((a, b) => a.timestamp - b.timestamp)
  
  console.log(`📊 Print chart will show ${printChartData.length} records from date range`)
  
  // Calculate statistics
  const printChartValues = printChartData.map(item => item.value)
  const overallMin = printChartValues.length > 0 ? Math.min(...printChartValues) : 0
  const overallMax = printChartValues.length > 0 ? Math.max(...printChartValues) : 100
  const overallAvg = printChartValues.length > 0 ? 
    (printChartValues.reduce((sum, val) => sum + val, 0) / printChartValues.length) : 0
  
  let chartImage = ''
  
  try {
    const ctx = tempCanvas.getContext('2d')
    
    // Calculate dynamic y-axis scaling
    const dataRange = overallMax - overallMin
    const yAxisPadding = dataRange * 0.1
    const yMin = Math.max(0, Math.floor(overallMin - yAxisPadding))
    const yMax = Math.min(100, Math.ceil(overallMax + yAxisPadding))
    
    const tempChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: printChartData.map(item => {
          return item.timestamp.toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          })
        }),
        datasets: [{
          label: 'Soil Moisture (%)',
          data: printChartData.map(item => item.value), 
          borderColor: '#10b981', 
          backgroundColor: 'rgba(16, 185, 129, 0.15)', 
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 2,
          pointHoverRadius: 4,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#10b981',
          pointBorderWidth: 1.5
        }]
      },
      options: {
        responsive: false,
        maintainAspectRatio: false,
        animation: false, 
        plugins: {
          legend: { 
            display: true,
            position: 'top',
            labels: {
              usePointStyle: true,
              padding: 20,
              font: { size: 14 }
            }
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `Moisture: ${context.raw.toFixed(1)}%`
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            min: yMin,
            max: yMax,
            title: {
              display: true,
              text: 'Moisture (%)',
              color: '#10b981',
              font: {
                size: 14,
                weight: '600'
              }
            },
            ticks: {
              font: { size: 12 },
              color: '#64748b',
              stepSize: calculateStepSize(dataRange),
              callback: function(value) {
                return value + '%'
              }
            },
            grid: {
              color: 'rgba(100, 116, 139, 0.2)'
            }
          },
          x: {
            ticks: {
              font: { size: 9 },
              color: '#64748b',
              maxTicksLimit: 10,
              maxRotation: 45,
              callback: function(value, index, values) {
                return index % Math.ceil(values.length / 10) === 0 ? this.getLabelForValue(value) : ''
              }
            },
            grid: {
              display: false
            }
          }
        }
      }
    })
    
    setTimeout(async () => {
      try {
        chartImage = tempCanvas.toDataURL('image/png', 1.0)
        
        tempChart.destroy()
        document.body.removeChild(tempContainer)
        
        generatePrintHTML(chartImage, soilMoistureRows, formattedDate, now, printChartData.length, overallMin, overallMax, overallAvg, startDate, endDate)
      } catch (error) {
        console.error('Error capturing chart:', error)
        document.body.removeChild(tempContainer)
        generatePrintHTML('', soilMoistureRows, formattedDate, now, 0, 0, 0, 0, startDate, endDate)
      }
    }, 500)
    
  } catch (error) {
    console.error('Error creating chart:', error)
    document.body.removeChild(tempContainer)
    generatePrintHTML('', soilMoistureRows, formattedDate, now, 0, 0, 0, 0, startDate, endDate)
  }
}

// Helper function to calculate appropriate step size for y-axis
function calculateStepSize(dataRange) {
  if (dataRange <= 10) return 1;
  if (dataRange <= 20) return 2;
  if (dataRange <= 50) return 5;
  if (dataRange <= 100) return 10;
  return 20;
}

// Updated print HTML generator with date range info
const generatePrintHTML = (chartImage, soilMoistureRows, formattedDate, now, chartRecordCount, printMin, printMax, printAvg, startDate = '', endDate = '') => {
  const dateRangeText = startDate && endDate 
    ? `Date Range: ${new Date(startDate).toLocaleDateString()} - ${new Date(endDate).toLocaleDateString()}`
    : 'Current Page Data'
  
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Soil Moisture Analysis Data</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          margin: 20px;
          color: #333;
          line-height: 1.4;
        }
        .header {
          text-align: center;
          margin-bottom: 25px;
          padding-bottom: 15px;
          border-bottom: 2px solid #10b981;
        }
        .header h1 {
          color: #065f46;
          margin: 0 0 8px 0;
          font-size: 24px;
        }
        .header .date {
          color: #6b7280;
          font-size: 14px;
        }
        .date-range {
          text-align: center;
          margin: 10px 0;
          padding: 8px;
          background-color: #f0fdf4;
          border-radius: 6px;
          font-size: 14px;
          font-weight: 500;
          color: #065f46;
        }
        .section-header {
          margin: 30px 0 18px 0;
          padding: 12px 15px;
          background-color: #f9fafb;
          border-left: 4px solid #10b981;
          border-radius: 4px;
          font-size: 17px;
          font-weight: bold;
          color: #065f46;
        }
        .chart-info {
          text-align: center;
          margin-bottom: 10px;
          font-size: 12px;
          color: #6b7280;
          font-style: italic;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          margin: 15px 0 25px 0;
          font-size: 12px;
          box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        th, td {
          border: 1px solid #e5e7eb;
          padding: 10px 12px;
          text-align: left;
        }
        th {
          background-color: #f3f4f6;
          font-weight: 600;
          color: #374151;
          border-bottom: 2px solid #d1d5db;
          font-size: 12px;
        }
        td {
          color: #4b5563;
          border-color: #e5e7eb;
        }
        tr:nth-child(even) {
          background-color: #f9fafb;
        }
        .soil-moisture { color: #10b981; font-weight: 500; }
        .status-wet { color: #059669; }
        .status-medium { color: #d97706; }
        .status-dry { color: #dc2626; }
        .summary {
          margin: 25px 0;
          padding: 20px;
          background-color: #f0fdf4;
          border-radius: 8px;
          border-left: 4px solid #10b981;
          box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .summary h3 {
          margin-top: 0;
          color: #065f46;
          font-size: 18px;
          border-bottom: 1px solid #bbf7d0;
          padding-bottom: 10px;
        }
        .summary-item {
          display: flex;
          justify-content: space-between;
          margin-bottom: 10px;
          padding: 8px 0;
        }
        .summary-label {
          font-weight: 600;
          color: #374151;
        }
        .summary-value {
          color: #059669;
          font-weight: 500;
        }
        .chart-image {
          width: 100%;
          max-width: 800px;
          margin: 15px auto;
          display: block;
          page-break-inside: avoid;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 15px;
          background: white;
          box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .chart-title {
          font-size: 16px;
          font-weight: 600;
          color: #374151;
          margin-bottom: 15px;
          text-align: center;
          padding: 10px;
          background-color: #f9fafb;
          border-radius: 4px;
        }
        .stats-summary {
          display: grid;
          grid-template-columns: repeat(3, 1fr);
          gap: 15px;
          margin: 20px 0;
          text-align: center;
        }
        .stat-item {
          padding: 15px;
          background-color: #f8fafc;
          border-radius: 8px;
          border: 1px solid #e2e8f0;
        }
        .stat-item h4 {
          margin: 0 0 10px 0;
          font-size: 14px;
          font-weight: 600;
          color: #10b981;
        }
        .stat-values {
          font-size: 12px;
          color: #64748b;
        }
        .footer {
          margin-top: 30px;
          font-size: 12px;
          color: #9ca3af;
          text-align: center;
          padding-top: 15px;
          border-top: 1px solid #e5e7eb;
        }
        @media print {
          body { margin: 0.5in; padding: 0; }
          .no-print { display: none; }
          .header { page-break-after: avoid; }
          table { page-break-inside: auto; }
          tr { page-break-inside: avoid; page-break-after: auto; }
          .chart-image { page-break-inside: avoid; }
        }
        @page { size: portrait; margin: 0.5in; }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Soil Moisture Analysis Report</h1>
        <div class="date">${formattedDate}</div>
      </div>
      
      <div class="date-range">
        ${dateRangeText}
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-item">
          <span class="summary-label">Total Records:</span>
          <span class="summary-value">${soilMoistureRows.length}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Chart Data Points:</span>
          <span class="summary-value">${chartRecordCount}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Date Range:</span>
          <span class="summary-value">${soilMoistureRows.length > 0 ? soilMoistureRows[soilMoistureRows.length-1].date + ' to ' + soilMoistureRows[0].date : 'N/A'}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Report Generated:</span>
          <span class="summary-value">${now.toLocaleString()}</span>
        </div>
      </div>
      
      <div class="section-header">Soil Moisture Trend Analysis</div>
      ${chartImage ? `
        <div class="chart-title">Soil Moisture Levels Over Time</div>
        <div class="chart-info">Showing ${chartRecordCount} data points</div>
        <img src="${chartImage}" class="chart-image" alt="Soil Moisture Chart" />
        
        <div class="stats-summary">
          <div class="stat-item">
            <h4>Soil Moisture</h4>
            <div class="stat-values">
              Min: ${printMin.toFixed(2)}%<br>
              Avg: ${printAvg.toFixed(2)}%<br>
              Max: ${printMax.toFixed(2)}%
            </div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">Chart could not be generated</p>'}
      
      <div class="section-header">Detailed Soil Moisture Sensor Readings</div>
      <table>
        <thead>
          <tr>
            <th style="width: 10%">ID</th>
            <th style="width: 15%">Date</th>
            <th style="width: 12%">Time</th>
            <th style="width: 10%">Device</th>
            <th style="width: 15%">Soil Moisture</th>
            <th style="width: 15%">Soil Status</th>
          </tr>
        </thead>
        <tbody>
          ${soilMoistureRows.map(row => `
            <tr>
              <td>${row.id}</td>
              <td>${row.date}</td>
              <td>${row.time}</td>
              <td>${row.device}</td>
              <td><span class="soil-moisture">${row.soilMoisture}%</span></td>
              <td>
                <span class="${
                  row.soilStatus === 'WET' ? 'status-wet' :
                  row.soilStatus === 'MEDIUM' ? 'status-medium' : 'status-dry'
                }">${row.soilStatus}</span>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by Soil Moisture Analysis System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
      </div>
    </body>
    </html>
  `;
  
  const iframe = document.createElement('iframe');
  iframe.style.position = 'absolute';
  iframe.style.width = '0';
  iframe.style.height = '0';
  iframe.style.border = 'none';
  iframe.style.left = '-9999px';
  document.body.appendChild(iframe);
  
  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
  
  iframeDoc.open();
  iframeDoc.write(tableContent);
  iframeDoc.close();
  
  iframe.onload = function() {
    try {
      iframe.contentWindow.focus();
      iframe.contentWindow.print();
      
      setTimeout(() => {
        document.body.removeChild(iframe);
      }, 100);
    } catch (error) {
      console.error('Print error:', error);
      document.body.removeChild(iframe);
      
      const printWindow = window.open('', '_blank');
      printWindow.document.write(tableContent);
      printWindow.document.close();
      printWindow.focus();
      printWindow.print();
    }
  };
};

// Existing computed properties and methods
const displayedPages = computed(() => {
  const total = paginationInfo.value.totalPages
  const current = paginationInfo.value.currentPage
  
  if (total <= 1) return [1]
  
  if (current === 1) {
    return [1, '..', total]
  } else if (current === total) {
    return [1, '..', total]
  } else {
    return [current, '...', total]
  }
})

const calculateSoilStatus = (moisture) => {
  if (moisture >= 70) return 'WET'
  if (moisture >= 30 && moisture < 70) return 'MEDIUM'
  return 'DRY'
}

const filters = ref({
  soilMoisture: { min: '', max: '' }
})

const searchQuery = ref('')
const activeDropdown = ref(null)
const sortKey = ref('date')
const sortDirection = ref('desc')
const activeFilters = ref({})

const filterFields = [
  { key: 'soilMoisture', label: 'Soil Moisture (%)' }
]

const headers = [
  { key: 'id', label: 'ID' },
  { key: 'soilMoisture', label: 'Soil Moisture (%)' },
  { key: 'soilStatus', label: 'Soil Status' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const exportFormats = ['csv', 'pdf']

// Client-side filtering for current page data
const filteredData = computed(() => {
  let result = [...soilMoistureData.value]

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  Object.keys(activeFilters.value).forEach(key => {
    const { min, max } = activeFilters.value[key]
    if (min !== '' && max !== '') {
      result = result.filter(row => row[key] >= min && row[key] <= max)
    } else if (min !== '') {
      result = result.filter(row => row[key] >= min)
    } else if (max !== '') {
      result = result.filter(row => row[key] <= max)
    }
  })

  return result
})

const sortedData = computed(() => {
  if (!sortKey.value) return filteredData.value

  return [...filteredData.value].sort((a, b) => {
    let aValue = a[sortKey.value]
    let bValue = b[sortKey.value]
    
    if (aValue === '' || aValue === undefined) aValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    if (bValue === '' || bValue === undefined) bValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortDirection.value === 'asc' 
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }
    
    return sortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
  })
})

const paginatedData = computed(() => {
  return sortedData.value
})

const totalPages = computed(() => {
  return paginationInfo.value.totalPages
})

const toggleDropdown = (dropdownName) => {
  if (activeDropdown.value === dropdownName) {
    activeDropdown.value = null
  } else {
    activeDropdown.value = dropdownName
  }
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    activeDropdown.value = null
  }
}

const performSearch = () => {
  // Client-side search only for current page
}

const applyFilters = () => {
  const newFilters = {}

  Object.keys(filters.value).forEach(key => {
    const min = parseFloat(filters.value[key].min)
    const max = parseFloat(filters.value[key].max)
    
    if (!isNaN(min) || !isNaN(max)) {
      newFilters[key] = {
        min: isNaN(min) ? '' : min,
        max: isNaN(max) ? '' : max
      }
    }
  })

  activeFilters.value = newFilters
  activeDropdown.value = null
}

const setSortKey = (key) => {
  if (sortKey.value === key) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDirection.value = 'asc' 
  }
  activeDropdown.value = null 
}

// Add these utility functions at the top of your script section
const parseBackendTimestamp = (timestamp) => {
  if (!timestamp) return new Date();
  
  if (timestamp instanceof Date) {
    return timestamp;
  }
  
  if (typeof timestamp === 'string') {
    const date = new Date(timestamp);
    if (!isNaN(date.getTime())) {
      return date;
    }
  }
  
  if (typeof timestamp === 'number') {
    if (timestamp > 1e12) {
      return new Date(timestamp);
    } else {
      return new Date(timestamp * 1000);
    }
  }
  
  if (timestamp && typeof timestamp === 'object' && '_seconds' in timestamp) {
    return new Date(timestamp._seconds * 1000);
  }
  
  console.warn('Unable to parse timestamp, using current time:', timestamp);
  return new Date();
};

const formatDateForDisplay = (timestamp) => {
  const date = parseBackendTimestamp(timestamp);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: '2-digit'
  });
};

const formatTimeForDisplay = (timestamp) => {
  const date = parseBackendTimestamp(timestamp);
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: true
  });
};

// Now the exportData function
const exportData = async (format) => {
  try {
    isLoading.value = true
    console.log(`📤 Starting ${format.toUpperCase()} export...`)
    
    // For exports, fetch ALL data without pagination
    let allData = []
    
    try {
      console.log('🚀 Fetching ALL Soil Moisture data for export...')
      const response = await api.get('/soil-moisture/all')
      
      console.log('📊 Backend response received:', {
        dataLength: response.data?.length,
        firstRecord: response.data?.[0]
      })
      
      if (response.data && Array.isArray(response.data)) {
        allData = response.data.map((reading, index) => {
          const timestamp = parseBackendTimestamp(reading.timestamp)
          
          // Use soilMoisture field from backend
          const moistureValue = reading.soilMoisture !== undefined ? reading.soilMoisture : reading.moisture
          
          return {
            id: reading.id || `export_${index}`,
            moisture: moistureValue?.toFixed(2) || '--',
            date: formatDateForDisplay(reading.timestamp),
            time: formatTimeForDisplay(reading.timestamp),
            rawTimestamp: timestamp,
            deviceId: reading.deviceId || 'esp32-2',
            timestampMs: timestamp.getTime(),
            status: calculateSoilStatus(moistureValue || 0)
          }
        })
        
        // Sort by timestamp (newest first)
        allData.sort((a, b) => b.timestampMs - a.timestampMs)
        
        console.log(`✅ Fetched ALL ${allData.length} records for export`)
      }
    } catch (error) {
      console.error('❌ Error fetching ALL data for export:', error)
      console.error('Error details:', error.response?.data)
      
      // Don't fall back to current page data - show error instead
      window.showToast('Error fetching all data for export', 'error')
      isLoading.value = false
      return
    }

    if (!allData.length) {
      window.showToast('No data available for export', 'warning')
      isLoading.value = false
      return
    }

    console.log(`📊 Exporting ALL ${allData.length} records`)

    // Create export data with ALL records
    const exportHeaders = ['Date', 'Time', 'Moisture (%)', 'Status', 'Device']
    const exportRows = allData.map(row => [
      row.date || '--',
      row.time || '--', 
      row.moisture !== undefined ? row.moisture : '--',
      row.status || 'Unknown',
      row.deviceId || 'esp32-2'
    ])

    const timestamp = new Date().toISOString().split('T')[0]

    if (format === 'csv') {
      let csvContent = exportHeaders.join(',') + '\n'
      exportRows.forEach(row => {
        csvContent += row.map(val => `"${val}"`).join(',') + '\n'
      })
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      saveAs(blob, `soil_moisture_data_${timestamp}.csv`)
      window.showToast(`Exported ${allData.length} Soil Moisture records as CSV`, 'success')
    } else if (format === 'pdf') {
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      })
      
      const pageWidth = doc.internal.pageSize.getWidth()
      const pageHeight = doc.internal.pageSize.getHeight()
      const margin = 10
      const tableWidth = pageWidth - (margin * 2)
      
      // Title section
      doc.setFontSize(16)
      doc.setTextColor(16, 185, 129)
      doc.text('Soil Moisture Data Report', pageWidth / 2, 20, { align: 'center' })
      
      doc.setFontSize(10)
      doc.setTextColor(100, 100, 100)
      doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, 27, { align: 'center' })
      doc.text(`Total Records: ${allData.length}`, pageWidth / 2, 33, { align: 'center' })
      
      // Add moisture status summary
      const statusCounts = allData.reduce((acc, row) => {
        const status = row.status || 'Unknown'
        acc[status] = (acc[status] || 0) + 1
        return acc
      }, {})
      
      doc.setFontSize(9)
      doc.setTextColor(75, 85, 99)
      let statusText = 'Moisture Status: '
      const statusEntries = Object.entries(statusCounts)
      statusEntries.forEach(([status, count], index) => {
        const percentage = ((count / allData.length) * 100).toFixed(1)
        statusText += `${status} ${count} (${percentage}%)`
        if (index < statusEntries.length - 1) statusText += ' | '
      })
      
      // Status summary on first page only
      doc.text(statusText, pageWidth / 2, 40, { align: 'center' })
      
      let startY = 48
      
      // Configure autoTable for ALL data
      const tableConfig = {
        head: [exportHeaders],
        body: exportRows,
        startY: startY,
        margin: { left: margin, right: margin },
        tableWidth: tableWidth,
        styles: { 
          fontSize: 8,
          cellPadding: 2,
          overflow: 'linebreak',
          textColor: [51, 51, 51],
          lineColor: [200, 200, 200],
          lineWidth: 0.1,
          minCellHeight: 6,
          cellWidth: 'wrap'
        },
        headStyles: {
          fillColor: [16, 185, 129],
          textColor: 255,
          fontStyle: 'bold',
          fontSize: 9,
          cellPadding: 3
        },
        bodyStyles: {
          cellPadding: 2,
          lineWidth: 0.1,
          minCellHeight: 6
        },
        alternateRowStyles: {
          fillColor: [240, 253, 244]
        },
        columnStyles: {
          0: { cellWidth: tableWidth * 0.22 }, // Date
          1: { cellWidth: tableWidth * 0.18 }, // Time
          2: { cellWidth: tableWidth * 0.20 }, // Moisture
          3: { cellWidth: tableWidth * 0.25 }, // Status
          4: { cellWidth: tableWidth * 0.15 }  // Device
        },
        pageBreak: 'auto',
        showHead: 'everyPage',
        tableLineWidth: 0.1,
        theme: 'grid',
        didParseCell: function (data) {
          // Color code moisture status cells
          if (data.column.index === 3 && data.section === 'body' && data.cell.raw) {
            const status = data.cell.raw.toString()
            if (status === 'Dry' || status === 'Very Dry') {
              data.cell.styles.fillColor = [254, 226, 226]
              data.cell.styles.textColor = [220, 38, 38]
            } else if (status === 'Optimal' || status === 'Adequate') {
              data.cell.styles.fillColor = [220, 252, 231]
              data.cell.styles.textColor = [22, 163, 74]
            } else if (status === 'Wet' || status === 'Very Wet') {
              data.cell.styles.fillColor = [219, 234, 254]
              data.cell.styles.textColor = [37, 99, 235]
            }
          }
        },
        didDrawPage: function (data) {
          // Only add header on first page
          if (data.pageNumber === 1) {
            doc.setFontSize(16)
            doc.setTextColor(16, 185, 129)
            doc.text('Soil Moisture Data Report', pageWidth / 2, 20, { align: 'center' })
            
            doc.setFontSize(10)
            doc.setTextColor(100, 100, 100)
            doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, 27, { align: 'center' })
            doc.text(`Total Records: ${allData.length}`, pageWidth / 2, 33, { align: 'center' })
            
            // Status summary on first page only
            doc.setFontSize(9)
            doc.setTextColor(75, 85, 99)
            doc.text(statusText, pageWidth / 2, 40, { align: 'center' })
          }
          
          // Footer on every page
          doc.setFontSize(8)
          doc.setTextColor(150, 150, 150)
          doc.text(
            `Page ${data.pageNumber} - ${allData.length} total records`,
            pageWidth / 2,
            pageHeight - 10,
            { align: 'center' }
          )
        }
      }
      
      // Generate the table
      autoTable(doc, tableConfig)
      
      doc.save(`soil_moisture_report_${timestamp}.pdf`)
      window.showToast(`Exported ${allData.length} Soil Moisture records as PDF`, 'success')
    } else if (format === 'docs') {
      const tableRows = [
        new TableRow({
          children: exportHeaders.map(h => new TableCell({
            children: [new Paragraph({ children: [new TextRun({ text: h, bold: true })] })],
            shading: {
              fill: "10B981",
              color: "FFFFFF"
            }
          }))
        }),
        ...exportRows.map(row =>
          new TableRow({
            children: row.map((cell, index) => {
              const cellText = cell ? cell.toString() : ''
              const textRun = new TextRun({ text: cellText, size: 20 })
              
              if (index === 3 && cellText) {
                if (cellText === 'Dry' || cellText === 'Very Dry') {
                  textRun.color = "FF0000"
                } else if (cellText === 'Optimal' || cellText === 'Adequate') {
                  textRun.color = "16A34A"
                } else if (cellText === 'Wet' || cellText === 'Very Wet') {
                  textRun.color = "2563EB"
                }
              }
              
              return new TableCell({
                children: [new Paragraph({ children: [textRun] })],
                width: { size: 20, type: 'pct' }
              })
            })
          })
        )
      ]
      
      const docxDoc = new Document({
        sections: [{
          properties: {
            page: {
              margin: {
                top: 1000,
                right: 1000,
                bottom: 1000,
                left: 1000,
              }
            }
          },
          children: [
            new Paragraph({ 
              text: 'Soil Moisture Data Report', 
              heading: 'Heading1',
              alignment: 'center'
            }),
            new Paragraph({
              text: `Generated: ${new Date().toLocaleString()} | Total Records: ${allData.length}`,
              alignment: 'center'
            }),
            new Paragraph({ text: '' }),
            new Table({ 
              width: {
                size: 100,
                type: 'pct'
              },
              rows: tableRows 
            })
          ]
        }]
      })
      const buffer = await Packer.toBlob(docxDoc)
      saveAs(buffer, `soil_moisture_data_${timestamp}.docx`)
      window.showToast(`Exported ${allData.length} Soil Moisture records as DOCX`, 'success')
    }
    
  } catch (error) {
    console.error('❌ Export error:', error)
    window.showToast('Error exporting data. Please try again.', 'error')
  } finally {
    isLoading.value = false
    activeDropdown.value = null
  }
}

let unsubscribe = null

onMounted(async () => {
  try {
    // Add event listeners
    document.addEventListener('click', handleClickOutside);
    
    // Initialize print date range
    initializePrintDateRange();
    
    // Wait for the next tick to ensure DOM is ready
    await nextTick();
    
    // Start data polling
    const cleanup = setupPollingListener();
    unsubscribe = cleanup;
    
  } catch (error) {
    console.error('Error during component mount:', error);
  }
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  
  if (chartInstance) {
    chartInstance.destroy();
    chartInstance = null;
  }
  
  if (unsubscribe) {
    unsubscribe();
  }
  
  // Reset flags
  isPolling = false;
  isUpdatingChart = false;
});
</script>
  
<style>
/* Your existing CSS styles remain the same */
.relative {
  position: relative;
}

[v-show] {
  transition: opacity 0.2s;
}

.relative:hover {
  z-index: 50;
}

/* Remove all hover animations from the main container */
.main-container {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.bg-white {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.rounded-lg {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.shadow-lg {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.border {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.border-gray-100 {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.h-\[calc100vh-140px\] {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.flex {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.flex-col {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.bg-gradient-to-r {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.from-emerald-50 {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.to-white {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.from-white {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

.to-emerald-50 {
  transition: none !important;
  animation: none !important;
  transform: none !important;
}

/* Text styling for better readability */
* {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Button styling - transition only colors not position */
button {
  transition: color 0.2s ease, background-color 0.2s ease, border-color 0.2s ease;
  transform: none !important;
}

/* FIXED TABLE ALIGNMENT STYLES */
table {
  table-layout: fixed;
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

/* Ensure consistent column widths */
table.table-fixed {
  table-layout: fixed;
}

/* Fix table header and body alignment */
thead th, tbody td {
  box-sizing: border-box;
  vertical-align: middle;
}

/* Ensure consistent padding and alignment */
thead th {
  position: sticky;
  top: 0;
  background-color: #f9fafb;
  z-index: 10;
}

tbody td {
  background-color: white;
}

/* Responsive styles */
@media (max-width: 1200px) {
  th, td {
    padding-left: 0.75rem !important;
    padding-right: 0.75rem !important;
  }
}

@media (max-width: 992px) {
  th, td {
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
  }
}

@media (max-width: 768px) {
  .overflow-x-auto {
    -webkit-overflow-scrolling: touch;
  }

  th, td {
    padding-left: 0.5rem !important;
    padding-right: 0.5rem !important;
    font-size: 0.875rem;
  }

  th div, td div {
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

@media (max-width: 640px) {
  .flex-col {
    row-gap: 0.5rem;
  }

  th, td {
    padding-left: 0.25rem !important;
    padding-right: 0.25rem !important;  
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  table {
    font-size: 0.75rem;
  }

  th, td {
    padding-left: 0.25rem !important;
    padding-right: 0.25rem !important;
  }
}
</style>