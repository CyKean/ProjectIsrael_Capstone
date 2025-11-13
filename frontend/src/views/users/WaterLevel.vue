<template>
   <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-85px)] mt-1 md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">        <!-- Gradient header for visual appeal -->
      <!-- Gradient header for visual appeal -->
      <div class="bg-gradient-to-r from-emerald-50 to-white p-4 md:p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-sm md:text-xl font-semibold text-gray-800 mb-1">Water Level Data Table</h1>
            <div class="flex items-center text-xs md:text-sm text-gray-500">
              <span class="text-emerald-600 font-medium">Water Level</span>
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
                  placeholder="Search water level measurements..."
                  class="w-full pl-8 sm:pl-10 pr-3 sm:pr-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 text-xs sm:text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                  v-model="searchQuery"
                  @input="handleSearch"
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
                      <div class="flex gap-2">
                        <button 
                          @click="applyFilters"
                          class="flex-1 px-3 sm:px-4 py-1.5 sm:py-2 bg-green-500 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-green-600 transition-colors"
                        >
                          Apply
                        </button>
                        <button 
                          @click="clearFilters"
                          class="flex-1 px-3 sm:px-4 py-1.5 sm:py-2 bg-gray-500 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-gray-600 transition-colors"
                        >
                          Clear
                        </button>
                      </div>
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

                <!-- Print Button -->
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
      <div class="flex-1 overflow-auto md:overflow-hidden flex flex-col md:flex-row">
        <!-- Live Graph Container - FIXED: Add explicit width constraints and overflow handling -->
        <div class="w-full md:w-1/3 lg:w-1/3 md:max-w-[33.333%] border-r border-gray-200 bg-white p-4 md:overflow-y-auto flex-shrink-0">
          <div class="mb-3">
            <h3 class="text-xs md:text-sm font-semibold text-gray-700">Live Water Level</h3>
            <p class="text-[10px] md:text-xs text-gray-500">Real-time monitoring</p>
          </div>
          
          <!-- Enhanced Combined Graph Container - FIXED: Add container constraints -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4 max-w-full">
            <!-- Graph Header with improved styling -->
            <div class="p-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full bg-blue-500 mr-1.5"></div>
                <span class="text-[10px] md:text-xs font-medium text-gray-700">Level (%)</span>
              </div>
              <div class="text-[10px] md:text-xs text-gray-500">
                Last updated: {{ lastUpdated }}
              </div>
            </div>
            
            <!-- Graph Canvas with current values overlay - FIXED: Add strict size constraints -->
            <div class="h-[280px] p-3 relative w-full overflow-hidden">
              <canvas 
                ref="chartCanvas" 
                class="w-full h-full max-w-full"
                :style="{ maxWidth: '100%', maxHeight: '280px' }"
              ></canvas>
              
              <!-- Repositioned and Resized Current Values Indicator -->
              <div class="absolute top-3 left-3 bg-white/95 backdrop-blur-sm rounded-md px-2 py-1 shadow-sm border border-gray-100" style="max-width: 80px; z-index: 10;">
                <div class="text-[10px] font-medium text-gray-500 mb-0.5">Current</div>
                <div class="flex items-center">
                  <div class="w-1.5 h-1.5 rounded-full bg-blue-500 mr-1"></div>
                  <div class="text-xs font-bold text-blue-600">
                    {{ currentWaterLevelValue }}%
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Enhanced Graph Footer with Stats -->
            <div class="border-t border-gray-100 p-3">
              <!-- Water Level Stats -->
              <div>
                <div class="flex items-center mb-2">
                  <div class="w-3 h-3 rounded-full bg-blue-500 mr-1.5"></div>
                  <div class="text-sm font-medium text-gray-700">Water Level</div>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-blue-50/50 rounded-md p-2">
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Min</div>
                    <div class="text-sm font-semibold text-blue-600">{{ waterLevelStats.min }}%</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Avg</div>
                    <div class="text-sm font-semibold text-blue-600">{{ waterLevelStats.avg }}%</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Max</div>
                    <div class="text-sm font-semibold text-blue-600">{{ waterLevelStats.max }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Water Status Guide -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Water Drum Status Guide</h4>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-emerald-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Full</span>
                </div>
                <span class="text-xs text-gray-500">80% - 100%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Sufficient</span>
                </div>
                <span class="text-xs text-gray-500">40% - 80%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-yellow-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Low</span>
                </div>
                <span class="text-xs text-gray-500">20% - 40%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-red-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Empty</span>
                </div>
                <span class="text-xs text-gray-500">< 20%</span>
              </div>
            </div>
          </div>
          
          <!-- Water Level Indicators -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Water Drum Capacity</h4>
            <div class="space-y-3">
              <div>
                <div class="flex items-center mb-1">
                  <div class="w-2 h-2 rounded-full bg-blue-500 mr-1"></div>
                  <span class="text-xs font-medium text-gray-700">Current Water Level</span>
                </div>
                <div class="h-4 bg-gray-100 rounded-full overflow-hidden relative">
                  <div class="absolute inset-0 flex">
                    <div class="h-full bg-red-500 w-[20%] flex items-center justify-center">
                      <span class="text-[8px] text-white font-bold">Empty</span>
                    </div>
                    <div class="h-full bg-yellow-500 w-[20%] flex items-center justify-center">
                      <span class="text-[8px] text-white font-bold">Low</span>
                    </div>
                    <div class="h-full bg-blue-500 w-[40%] flex items-center justify-center">
                      <span class="text-[8px] text-white font-bold">Sufficient</span>
                    </div>
                    <div class="h-full bg-emerald-500 w-[20%] flex items-center justify-center">
                      <span class="text-[8px] text-white font-bold">Full</span>
                    </div>
                  </div>
                </div>
                <div class="flex justify-between mt-1 text-[10px] text-gray-500">
                  <span>0%</span>
                  <span>20%</span>
                  <span>40%</span>
                  <span>80%</span>
                  <span>100%</span>
                </div>
              </div>
              <div class="mt-3 text-xs text-gray-600">
                <p class="mb-1"><span class="font-medium">Refill needed:</span> When water level drops below 20%</p>
                <p><span class="font-medium">Optimal usage:</span> Keep water level between 40% - 80%</p>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Table Container - FIXED: Add explicit flex constraints -->
        <div class="w-full md:w-2/3 lg:w-2/3 md:max-w-[66.666%] flex flex-col flex-grow min-w-0">
          <!-- Mobile Card View (shown on small screens) -->
          <div class="sm:hidden flex-1 overflow-auto bg-white p-3 space-y-3">
            <div v-for="(row, index) in displayedData" :key="row.id" 
                class="bg-gray-50 rounded-lg p-3 border border-gray-200">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <div class="text-xs font-medium text-gray-900">{{ row.date }}</div>
                  <div class="text-[10px] text-gray-500">{{ row.time }}</div>
                </div>
                <div class="text-[10px] text-gray-400">#{{ row.id }}</div>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Water Level</div>
                  <div class="text-xs font-semibold text-blue-600">{{ row.waterLevel }}%</div>
                </div>
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Status</div>
                  <span 
                    :class="[
                      'px-2 py-0.5 rounded-full text-[10px] font-medium',
                      row.status === 'FULL' ? 'bg-emerald-100 text-emerald-800' :
                      row.status === 'SUFFICIENT' ? 'bg-blue-100 text-blue-800' :
                      row.status === 'LOW' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ row.status }}
                  </span>
                </div>
              </div>
            </div>
            
            <div v-if="displayedData.length === 0 && !isLoading" 
                class="flex flex-col items-center justify-center py-8">
              <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
              <p class="text-gray-500 text-xs font-medium">No water level data found</p>
              <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
            </div>

            <!-- Loading state for mobile -->
            <div v-if="isLoading" class="flex flex-col items-center justify-center py-8">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-green-500 mb-2"></div>
              <p class="text-gray-500 text-xs font-medium">Loading data...</p>
            </div>
          </div>

          <!-- Desktop Table View (shown on medium screens and up) -->
          <div class="hidden sm:flex flex-1 flex-col min-h-0">
            <!-- Single Table Structure for Perfect Alignment -->
            <div class="flex-1 overflow-auto">
              <table class="w-full min-w-[600px] table-fixed">
                <thead class="sticky top-0 z-10 bg-gray-300 border-b border-gray-200">
                <tr>
                  
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-emerald-600">Water Status</div>
                    <div class="text-gray-400 text-[10px]">CONDITION</div>
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-blue-600">Water Level</div>
                    <div class="text-gray-400 text-[10px]">PERCENTAGE (%)</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-gray-600">Date</div>
                    <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-gray-600">Time</div>
                    <div class="text-gray-400 text-[10px]">HH:MM:SS AM/PM</div>
                  </th>
                </tr>
              </thead>
                
                <!-- Table Body -->
                <tbody class="bg-white divide-y divide-gray-50">
                  <tr 
                    v-for="(row, index) in displayedData" 
                    :key="row.id"
                    class="hover:bg-gray-50/50 transition-colors"
                  >
                    
                    <td class="w-[25%] px-4 py-3.5 whitespace-nowrap md:text-[15px] border-b border-gray-200">
                      <span 
                        :class="[
                          'px-3 py-1 rounded-full text-xs font-medium',
                          row.status === 'FULL' ? 'bg-emerald-100 text-emerald-800' :
                          row.status === 'SUFFICIENT' ? 'bg-blue-100 text-blue-800' :
                          row.status === 'LOW' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-red-100 text-red-800'
                        ]"
                      >
                        {{ row.status }}
                      </span>
                    </td>
                    <td class="w-[25%] px-4 py-3.5 whitespace-nowrap md:text-[15px] border-b border-gray-200">
                      <div class="text-sm font-medium text-blue-600">
                        {{ row.waterLevel }}%
                      </div>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 whitespace-nowrap md:text-[15px] border-b border-gray-200">
                      <div class="text-sm font-medium text-gray-700">{{ row.date }}</div>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 whitespace-nowrap md:text-[15px] border-b border-gray-200">
                      <div class="text-sm font-medium text-gray-700">{{ row.time }}</div>
                    </td>
                  </tr>
                  
                  <!-- Empty state when no data -->
                  <tr v-if="displayedData.length === 0 && !isLoading">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <FileSearch class="h-16 w-16 text-gray-300 mb-4" />
                        <p class="text-gray-500 text-lg font-medium">No water level data found</p>
                        <p class="text-gray-400 text-sm mt-1">Try adjusting your search or filters</p>
                      </div>
                    </td>
                  </tr>

                  <!-- Loading state -->
                  <tr v-if="isLoading">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500 mb-4"></div>
                        <p class="text-gray-500 text-lg font-medium">Loading water level data...</p>
                        <p class="text-gray-400 text-sm mt-1">Please wait while we fetch the latest readings</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Pagination Section -->
          <div class="border-t border-gray-200 py-2 px-3 bg-gray-50">
            <div class="flex items-center justify-between">
              <div class="text-[10px] md:text-xs text-gray-600">
                <span v-if="!isLoading">
                  Showing {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, totalItems) }}
                  of {{ totalItems }} entries
                </span>
                <span v-else>Loading...</span>
              </div>
              <div class="flex items-center gap-1">
                <button 
                  @click="prevPage"
                  :disabled="currentPage === 1 || isFetching"
                  class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600 transition-colors"
                >
                  <ChevronLeft class="w-3.5 h-3.5" />
                </button>
                
                <div class="flex items-center gap-1">
                  <button
                    v-for="(pageNum, index) in paginationNumbers"
                    :key="index"
                    @click="goToPage(pageNum)"
                    :disabled="pageNum === '...' || isFetching"
                    :class="[
                      'px-2 py-1 text-[10px] md:text-xs rounded min-w-[20px] transition-colors',
                      pageNum === currentPage 
                        ? 'bg-green-500 text-white font-medium' 
                        : pageNum === '...' 
                          ? 'text-gray-400 cursor-default' 
                          : 'text-gray-700 hover:text-green-600 hover:bg-gray-100'
                    ]"
                  >
                    {{ pageNum }}
                  </button>
                </div>
                
                <button 
                  @click="nextPage"
                  :disabled="currentPage >= totalPages || isFetching"
                  class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600 transition-colors"
                >
                  <ChevronRight class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- Print Modal -->
  <div v-if="showPrintModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50 p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto">
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-800">Print Water Level Data</h3>
          <button @click="closePrintModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>
        
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Date Range</label>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs text-gray-500 mb-1">From Date</label>
                <input
                  type="date"
                  v-model="printStartDate"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm"
                />
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">To Date</label>
                <input
                  type="date"
                  v-model="printEndDate"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm"
                />
              </div>
            </div>
          </div>

          <!-- <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Print Options</label>
            <div class="space-y-2">
              <label class="flex items-center">
                <input
                  type="checkbox"
                  v-model="printOptions.includeChart"
                  class="rounded border-gray-300 text-green-600 focus:ring-green-500"
                />
                <span class="ml-2 text-sm text-gray-700">Include Water Level Chart</span>
              </label>
              <label class="flex items-center">
                <input
                  type="checkbox"
                  v-model="printOptions.includeStats"
                  class="rounded border-gray-300 text-green-600 focus:ring-green-500"
                />
                <span class="ml-2 text-sm text-gray-700">Include Statistics</span>
              </label>
              <label class="flex items-center">
                <input
                  type="checkbox"
                  v-model="printOptions.includeGuide"
                  class="rounded border-gray-300 text-green-600 focus:ring-green-500"
                />
                <span class="ml-2 text-sm text-gray-700">Include Status Guide</span>
              </label>
            </div>
          </div> -->

          <div class="bg-yellow-50 border border-yellow-200 rounded-md p-3">
            <div class="flex">
              <div class="flex-shrink-0">
                <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
              </div>
              <div class="ml-3">
                <p class="text-sm text-yellow-700">
                  This will fetch all data within the selected date range. For large date ranges, this may take a moment.
                </p>
              </div>
            </div>
          </div>
        </div>

        <div class="flex gap-3 mt-6">
          <button
            @click="closePrintModal"
            class="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="generatePrintReport"
            :disabled="isPrinting || !printStartDate || !printEndDate"
            class="flex-1 px-4 py-2 text-sm font-medium text-white bg-green-600 border border-transparent rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="isPrinting">Generating...</span>
            <span v-else>Generate Report</span>
          </button>
        </div>
      </div>
    </div>
  </div>

  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Water Level Data" 
    message="Please wait while we fetch the latest water level measurements"
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

// Reactive data
const waterLevelData = ref([])
const isLoading = ref(true)
const isFetching = ref(false)
const totalItems = ref(0)
const totalPages = ref(1)

// Print modal state
const showPrintModal = ref(false)
const isPrinting = ref(false)
const printStartDate = ref('')
const printEndDate = ref('')
const printOptions = ref({
  includeChart: true,
  includeStats: true,
  includeGuide: true
})

// Chart related
const chartCanvas = ref(null)
const chart = ref(null)
const chartData = ref([])
const currentWaterLevelValue = ref('--')
const lastUpdated = ref('--')
const waterLevelStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})

// UI state
const searchQuery = ref('')
const itemsPerPage = ref(20)
const currentPage = ref(1)
const activeDropdown = ref(null)
const sortKey = ref('timestamp')
const sortDirection = ref('desc')
const activeFilters = ref({})

// Filters
const filters = ref({
  waterLevel: { min: '', max: '' }
})

const filterFields = [
  { key: 'waterLevel', label: 'Water Level (%)' }
]

const headers = [
  { key: 'id', label: 'ID' },
  { key: 'status', label: 'Water Status' },
  { key: 'waterLevel', label: 'Water Level (%)' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const exportFormats = ['csv', 'pdf']

// Polling
let pollingInterval = null
const POLLING_FREQUENCY = 5000 

// Computed properties
const displayedData = computed(() => {
  let result = [...waterLevelData.value]

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  // Apply numeric filters
  Object.keys(activeFilters.value).forEach(key => {
    const { min, max } = activeFilters.value[key]
    if (min !== '' && max !== '') {
      result = result.filter(row => {
        const value = parseFloat(row[key])
        return value >= min && value <= max
      })
    } else if (min !== '') {
      result = result.filter(row => {
        const value = parseFloat(row[key])
        return value >= min
      })
    } else if (max !== '') {
      result = result.filter(row => {
        const value = parseFloat(row[key])
        return value <= max
      })
    }
  })

  // Apply sorting
  if (sortKey.value) {
    result.sort((a, b) => {
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
  }

  return result
})

const paginationNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 1) return [1]
  
  if (total <= 5) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }
  
  if (current <= 3) {
    return [1, 2, 3, '...', total]
  } else if (current >= total - 2) {
    return [1, '...', total - 2, total - 1, total]
  } else {
    return [1, '...', current - 1, current, current + 1, '...', total]
  }
})

// Set default dates for print modal
const setDefaultPrintDates = () => {
  const endDate = new Date()
  const startDate = new Date()
  startDate.setDate(startDate.getDate() - 7)
  
  printEndDate.value = endDate.toISOString().split('T')[0]
  printStartDate.value = startDate.toISOString().split('T')[0]
}

// Print Modal Functions
const openPrintModal = () => {
  setDefaultPrintDates()
  showPrintModal.value = true
  activeDropdown.value = null
}

const closePrintModal = () => {
  showPrintModal.value = false
  isPrinting.value = false
}

// Main Print Function
const generatePrintReport = async () => {
   if (!printStartDate.value || !printEndDate.value) {
    alert('Please select both start and end dates')
    return
  }

  isPrinting.value = true

  try {
    console.log('📅 Using workaround for date range:', printStartDate.value, 'to', printEndDate.value)
    
    // Get ALL data and filter client-side as temporary solution
    const response = await api.get('/water-level/readings/all')
    const allData = response.data || []
    
    console.log(`📊 Retrieved ${allData.length} total records`)
    
    // Filter by date range client-side
    const startDate = new Date(printStartDate.value)
    const endDate = new Date(printEndDate.value)
    endDate.setHours(23, 59, 59, 999) // Include entire end day
    
    const filteredData = allData.filter(reading => {
      if (!reading.timestamp) return false
      
      const readingDate = new Date(reading.timestamp)
      return readingDate >= startDate && readingDate <= endDate
    })
    
    console.log(`📅 Filtered to ${filteredData.length} records in date range`)
    
    if (filteredData.length === 0) {
      alert('No water level data found for the selected date range.')
      isPrinting.value = false
      return
    }

    // Process the data for printing (same as before)
    const processedData = filteredData.map(reading => {
      let timestamp
      try {
        if (reading.timestamp) {
          timestamp = new Date(reading.timestamp)
        } else {
          timestamp = new Date()
        }
      } catch (e) {
        console.warn('Error parsing timestamp:', e)
        timestamp = new Date()
      }

      const waterLevelValue = reading.waterLevel !== undefined ? reading.waterLevel : 
                             reading.value !== undefined ? reading.value : 0

      return {
        id: reading.id || `print-${Math.random().toString(36).substr(2, 9)}`,
        waterLevel: Number(waterLevelValue).toFixed(2),
        status: calculateWaterStatus(Number(waterLevelValue)),
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
        rawTimestamp: timestamp
      }
    })

    // Generate the print content
    await generatePrintContent(processedData)

  } catch (error) {
    console.error('❌ Error generating print report:', error)
    alert('Error generating report. Please try again.')
  } finally {
    isPrinting.value = false
    closePrintModal()
  }
}

// Generate chart image for print
const generateChartImage = async (printData) => {
  return new Promise((resolve) => {
    const tempCanvas = document.createElement('canvas')
    tempCanvas.width = 800
    tempCanvas.height = 400
    const tempContainer = document.createElement('div')
    tempContainer.appendChild(tempCanvas)
    tempContainer.style.position = 'absolute'
    tempContainer.style.left = '-9999px'
    document.body.appendChild(tempContainer)

    const ctx = tempCanvas.getContext('2d')
    
    // Prepare chart data
    const chartData = printData
      .map(item => ({
        timestamp: item.rawTimestamp,
        value: parseFloat(item.waterLevel)
      }))
      .sort((a, b) => a.timestamp - b.timestamp)
      .slice(-50) // Limit to last 50 points for readability

    const labels = chartData.map(item => 
      item.timestamp.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    )

    const data = chartData.map(item => item.value)

    const chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Water Level (%)',
          data: data,
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderWidth: 2,
          tension: 0.4,
          fill: true
        }]
      },
      options: {
        responsive: false,
        animation: false,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Water Level Trend'
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            title: {
              display: true,
              text: 'Water Level (%)'
            }
          }
        }
      }
    })

    setTimeout(() => {
      const imageData = tempCanvas.toDataURL('image/png', 1.0)
      chart.destroy()
      document.body.removeChild(tempContainer)
      resolve(imageData)
    }, 500)
  })
}

// Generate the actual print content
const generatePrintContent = async (printData) => {
  const now = new Date()
  const formattedDate = now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })

  // Calculate statistics
  const waterLevelValues = printData.map(item => parseFloat(item.waterLevel)).filter(val => !isNaN(val))
  const waterLevelMin = waterLevelValues.length > 0 ? Math.min(...waterLevelValues) : 0
  const waterLevelMax = waterLevelValues.length > 0 ? Math.max(...waterLevelValues) : 0
  const waterLevelAvg = waterLevelValues.length > 0 ? 
    (waterLevelValues.reduce((sum, val) => sum + val, 0) / waterLevelValues.length) : 0

  // Create chart image if needed
  let chartImage = ''
  if (printOptions.value.includeChart && printData.length > 0) {
    chartImage = await generateChartImage(printData)
  }

  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Water Level Data Report</title>
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
        .header .date-range {
          color: #6b7280;
          font-size: 14px;
          margin-bottom: 5px;
        }
        .header .generated-date {
          color: #9ca3af;
          font-size: 12px;
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
        .summary {
          margin: 25px 0;
          padding: 20px;
          background-color: #f0fdf4;
          border-radius: 8px;
          border-left: 4px solid #10b981;
          box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }
        .summary-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
          gap: 15px;
          margin-top: 15px;
        }
        .summary-item {
          background: white;
          padding: 15px;
          border-radius: 6px;
          text-align: center;
          box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .summary-label {
          font-size: 12px;
          color: #6b7280;
          margin-bottom: 5px;
        }
        .summary-value {
          font-size: 18px;
          font-weight: bold;
          color: #065f46;
        }
        .chart-container {
          text-align: center;
          margin: 25px 0;
        }
        .chart-image {
          max-width: 100%;
          height: auto;
          border: 1px solid #e5e7eb;
          border-radius: 8px;
          padding: 15px;
          background: white;
        }
        .chart-title {
          font-size: 16px;
          font-weight: 600;
          color: #374151;
          margin-bottom: 15px;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          margin: 25px 0;
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
        }
        tr:nth-child(even) {
          background-color: #f9fafb;
        }
        .status-full { color: #059669; font-weight: 500; }
        .status-sufficient { color: #3b82f6; font-weight: 500; }
        .status-low { color: #d97706; font-weight: 500; }
        .status-empty { color: #dc2626; font-weight: 500; }
        .guide {
          margin: 25px 0;
          padding: 20px;
          background-color: #f8fafc;
          border-radius: 8px;
          border: 1px solid #e2e8f0;
        }
        .guide-item {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
          padding: 8px 0;
        }
        .guide-color {
          width: 16px;
          height: 16px;
          border-radius: 50%;
          margin-right: 12px;
        }
        .guide-text {
          font-size: 14px;
          color: #374151;
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
          body { margin: 0.5in; }
          .no-print { display: none; }
          .header { page-break-after: avoid; }
          table { page-break-inside: auto; }
          tr { page-break-inside: avoid; }
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Water Level Data Report</h1>
        <div class="date-range">
          Date Range: ${printStartDate.value} to ${printEndDate.value}
        </div>
        <div class="generated-date">
          Generated on: ${formattedDate}
        </div>
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-label">Total Records</div>
            <div class="summary-value">${printData.length}</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Date Range</div>
            <div class="summary-value">${printData.length > 0 ? printData[printData.length-1].date + ' to ' + printData[0].date : 'N/A'}</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Time Range</div>
            <div class="summary-value">${printData.length > 0 ? printData[printData.length-1].time + ' to ' + printData[0].time : 'N/A'}</div>
          </div>
        </div>
      </div>

      ${printOptions.value.includeStats ? `
        <div class="section-header">Water Level Statistics</div>
        <div class="summary-grid">
          <div class="summary-item">
            <div class="summary-label">Minimum Level</div>
            <div class="summary-value">${waterLevelMin.toFixed(2)}%</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Average Level</div>
            <div class="summary-value">${waterLevelAvg.toFixed(2)}%</div>
          </div>
          <div class="summary-item">
            <div class="summary-label">Maximum Level</div>
            <div class="summary-value">${waterLevelMax.toFixed(2)}%</div>
          </div>
        </div>
      ` : ''}

      ${printOptions.value.includeChart && chartImage ? `
        <div class="section-header">Water Level Trend</div>
        <div class="chart-container">
          <div class="chart-title">Water Level Over Time</div>
          <img src="${chartImage}" class="chart-image" alt="Water Level Chart" />
        </div>
      ` : ''}

      ${printOptions.value.includeGuide ? `
        <div class="section-header">Water Level Status Guide</div>
        <div class="guide">
          <div class="guide-item">
            <div class="guide-color" style="background-color: #10b981;"></div>
            <div class="guide-text">Full (80% - 100%) - Optimal water level</div>
          </div>
          <div class="guide-item">
            <div class="guide-color" style="background-color: #3b82f6;"></div>
            <div class="guide-text">Sufficient (40% - 80%) - Good water level</div>
          </div>
          <div class="guide-item">
            <div class="guide-color" style="background-color: #f59e0b;"></div>
            <div class="guide-text">Low (20% - 40%) - Monitor closely</div>
          </div>
          <div class="guide-item">
            <div class="guide-color" style="background-color: #ef4444;"></div>
            <div class="guide-text">Empty (0% - 20%) - Refill needed</div>
          </div>
        </div>
      ` : ''}

      <div class="section-header">Detailed Water Level Readings</div>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Date</th>
            <th>Time</th>
            <th>Water Level</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          ${printData.map(row => `
            <tr>
              <td>${row.id}</td>
              <td>${row.date}</td>
              <td>${row.time}</td>
              <td>${row.waterLevel}%</td>
              <td class="status-${row.status.toLowerCase()}">${row.status}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by Water Level Monitoring System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
      </div>
    </body>
    </html>
  `

  // Open print dialog
  const iframe = document.createElement('iframe')
  iframe.style.position = 'absolute'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = 'none'
  iframe.style.left = '-9999px'
  document.body.appendChild(iframe)

  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document
  iframeDoc.open()
  iframeDoc.write(tableContent)
  iframeDoc.close()

  iframe.onload = function() {
    try {
      iframe.contentWindow.focus()
      iframe.contentWindow.print()
      setTimeout(() => {
        document.body.removeChild(iframe)
      }, 100)
    } catch (error) {
      console.error('Print error:', error)
      document.body.removeChild(iframe)
      // Fallback: open in new window
      const printWindow = window.open('', '_blank')
      printWindow.document.write(tableContent)
      printWindow.document.close()
      printWindow.focus()
      printWindow.print()
    }
  }
}

const fetchWaterLevelDataRange = async (startDate, endDate) => {
  try {
    const response = await api.get('/water-level/readings/range', {
      params: {
        from_date: startDate,
        to_date: endDate
      }
    });
    
    if (response.data) {
      waterLevelData.value = response.data;
      totalItems.value = response.data.length; // Assuming you want to set total items based on the response
      totalPages.value = 1; // Since this is a range query, we can set total pages to 1
    } else {
      alert('No data found for the specified date range.');
    }
  } catch (error) {
    console.error('Error fetching water level data range:', error);
    alert('Error fetching data. Please try again later.');
  }
};

// Main data fetching function
const fetchWaterLevelData = async (page = currentPage.value, limit = itemsPerPage.value) => {
  try {
    console.log(`💧 Fetching water level data - Page: ${page}, Limit: ${limit}`)
    isFetching.value = true
    if (page === 1) {
      // isLoading.value = true
    }

    const response = await api.get(`/water-level/readings`, {
      params: {
        page: page,
        limit: limit
      }
    })

    console.log('📊 Full API Response:', response)
    
    let data = []
    let paginationInfo = {}
    
    // Handle different response structures
    if (response.data) {
      if (response.data.data && Array.isArray(response.data.data)) {
        data = response.data.data
        paginationInfo = response.data.pagination || {}
      } else if (Array.isArray(response.data)) {
        data = response.data
        paginationInfo = {
          currentPage: page,
          totalPages: Math.ceil(data.length / limit),
          totalItems: data.length,
          itemsPerPage: limit
        }
      }
    }

    console.log('📊 Processed data:', data)
    console.log('📊 Pagination info:', paginationInfo)

    if (!Array.isArray(data)) {
      console.error('❌ Expected array but got:', typeof data, data)
      throw new Error('Invalid data format received from API')
    }

    // Process the data for display
    const processedData = data.map((reading, index) => {
      let timestamp
      try {
        if (reading.timestamp) {
          timestamp = new Date(reading.timestamp)
        } else {
          timestamp = new Date()
        }
      } catch (e) {
        console.warn('Error parsing timestamp:', e)
        timestamp = new Date()
      }

      const waterLevelValue = reading.waterLevel !== undefined ? reading.waterLevel : 
                             reading.value !== undefined ? reading.value : 0

      return {
        id: reading.id || `wl-${(page - 1) * limit + index + 1}`,
        timestamp: timestamp.getTime(),
        waterLevel: Number(waterLevelValue).toFixed(2),
        status: calculateWaterStatus(Number(waterLevelValue)),
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
        deviceId: reading.device_id || reading.deviceId || 'unknown'
      }
    })

    // Update reactive data
    waterLevelData.value = processedData
    
    // Update pagination info
    totalItems.value = paginationInfo.totalItems || data.length
    totalPages.value = paginationInfo.totalPages || Math.ceil(totalItems.value / limit) || 1
    
    console.log(`✅ Successfully loaded ${processedData.length} water level readings`)
    console.log(`📄 Page ${currentPage.value} of ${totalPages.value}, Total items: ${totalItems.value}`)

    // Update chart with first page data
    if (page === 1 && processedData.length > 0) {
      updateChartWithData(processedData)
    }

  } catch (error) {
    console.error('❌ Error fetching water level data:', error)
    waterLevelData.value = []
    totalItems.value = 0
    totalPages.value = 1
  } finally {
    isLoading.value = false
    isFetching.value = false
  }
}

// Chart functions
const updateChartWithData = (data) => {
  if (!data || data.length === 0) return

  const chartDataPoints = data.slice(0, 20).map(item => ({
    timestamp: item.rawTimestamp,
    value: parseFloat(item.waterLevel)
  })).sort((a, b) => a.timestamp - b.timestamp)

  chartData.value = chartDataPoints

  if (chartDataPoints.length > 0) {
    const latestReading = chartDataPoints[chartDataPoints.length - 1]
    currentWaterLevelValue.value = latestReading.value.toFixed(2)
    
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    
    const values = chartDataPoints.map(item => item.value).filter(val => !isNaN(val))
    if (values.length > 0) {
      waterLevelStats.value = {
        min: Math.min(...values).toFixed(2),
        max: Math.max(...values).toFixed(2),
        avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2)
      }
    }
  }

  initializeChart()
}

const initializeChart = () => {
  nextTick(() => {
    if (!chartCanvas.value || chartData.value.length === 0) return

    if (chart.value) {
      chart.value.destroy()
    }

    const ctx = chartCanvas.value.getContext('2d')
    chart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.value.map(item => 
          item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          })
        ),
        datasets: [{
          label: 'Water Level (%)',
          data: chartData.value.map(item => item.value),
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.15)',
          borderWidth: 2.5,
          tension: 0.4,
          fill: true,
          pointRadius: 3,
          pointHoverRadius: 5,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#3b82f6',
          pointBorderWidth: 1.5
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false }
        },
        scales: {
          y: {
            beginAtZero: true,
            max: 100,
            title: {
              display: true,
              text: 'Level (%)',
              color: '#3b82f6'
            }
          },
          x: {
            ticks: {
              maxRotation: 45
            }
          }
        }
      }
    })
  })
}

// Pagination functions
const nextPage = async () => {
  if (currentPage.value < totalPages.value && !isFetching.value) {
    currentPage.value++
    await fetchWaterLevelData(currentPage.value, itemsPerPage.value)
    scrollToTop()
  }
}

const prevPage = async () => {
  if (currentPage.value > 1 && !isFetching.value) {
    currentPage.value--
    await fetchWaterLevelData(currentPage.value, itemsPerPage.value)
    scrollToTop()
  }
}

const goToPage = async (pageNum) => {
  if (typeof pageNum === 'number' && pageNum >= 1 && pageNum <= totalPages.value && !isFetching.value) {
    currentPage.value = pageNum
    await fetchWaterLevelData(currentPage.value, itemsPerPage.value)
    scrollToTop()
  }
}

const scrollToTop = () => {
  const tableContainer = document.querySelector('.overflow-auto')
  if (tableContainer) {
    tableContainer.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// Search and filter functions
const handleSearch = () => {
  // Search is handled locally by the computed property
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

const clearFilters = () => {
  filters.value = {
    waterLevel: { min: '', max: '' }
  }
  activeFilters.value = {}
  activeDropdown.value = null
}

// UI functions
const toggleDropdown = (dropdownName) => {
  activeDropdown.value = activeDropdown.value === dropdownName ? null : dropdownName
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    activeDropdown.value = null
  }
}

const setSortKey = (key) => {
  if (sortKey.value === key) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDirection.value = 'desc'
  }
  activeDropdown.value = null
}

// Utility functions
const calculateWaterStatus = (level) => {
  if (level >= 80) return 'FULL'
  if (level >= 40) return 'SUFFICIENT'
  if (level >= 20) return 'LOW'
  return 'EMPTY'
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

// Updated export function
const exportData = async (format) => {
  try {
    isLoading.value = true
    console.log(`📤 Starting ${format.toUpperCase()} export...`)
    
    // For exports, fetch ALL data without pagination
    let allData = []
    
    try {
      console.log('🚀 Fetching ALL Water Level data for export...')
      const response = await api.get('/water-level/readings/all')
      
      console.log('📊 Backend response received:', {
        dataLength: response.data?.length,
        firstRecord: response.data?.[0]
      })
      
      if (response.data && Array.isArray(response.data)) {
        allData = response.data.map((reading, index) => {
          const timestamp = parseBackendTimestamp(reading.timestamp)
          
          const waterLevelValue = reading.waterLevel !== undefined ? reading.waterLevel : 
                               reading.value !== undefined ? reading.value : 0

          return {
            id: reading.id || `export_${index}`,
            waterLevel: Number(waterLevelValue).toFixed(2),
            status: calculateWaterStatus(Number(waterLevelValue)),
            date: formatDateForDisplay(reading.timestamp),
            time: formatTimeForDisplay(reading.timestamp),
            rawTimestamp: timestamp,
            deviceId: reading.deviceId || 'unknown',
            timestampMs: timestamp.getTime()
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
    const exportHeaders = ['Date', 'Time', 'Water Level (%)', 'Status', 'Device']
    const exportRows = allData.map(row => [
      row.date || '--',
      row.time || '--', 
      row.waterLevel !== undefined ? row.waterLevel : '--',
      row.status || 'Unknown',
      row.deviceId || 'unknown'
    ])

    const timestamp = new Date().toISOString().split('T')[0]

    if (format === 'csv') {
      let csvContent = exportHeaders.join(',') + '\n'
      exportRows.forEach(row => {
        csvContent += row.map(val => `"${val}"`).join(',') + '\n'
      })
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      saveAs(blob, `water_level_data_${timestamp}.csv`)
      window.showToast(`Exported ${allData.length} Water Level records as CSV`, 'success')
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
      doc.text('Water Level Data Report', pageWidth / 2, 20, { align: 'center' })
      
      doc.setFontSize(10)
      doc.setTextColor(100, 100, 100)
      doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, 27, { align: 'center' })
      doc.text(`Total Records: ${allData.length}`, pageWidth / 2, 33, { align: 'center' })
      
      // Water level status summary
      const statusCounts = allData.reduce((acc, row) => {
        const status = row.status || 'Unknown'
        acc[status] = (acc[status] || 0) + 1
        return acc
      }, {})
      
      doc.setFontSize(9)
      doc.setTextColor(75, 85, 99)
      let statusText = 'Water Status: '
      const statusEntries = Object.entries(statusCounts)
      statusEntries.forEach(([status, count], index) => {
        const percentage = ((count / allData.length) * 100).toFixed(1)
        statusText += `${status} ${count} (${percentage}%)`
        if (index < statusEntries.length - 1) statusText += ' | '
      })
      
      // Status summary on first page only
      doc.text(statusText, pageWidth / 2, 40, { align: 'center' })
      
      // Current reading and statistics
      doc.setFontSize(11)
      doc.setTextColor(30, 41, 59)
      doc.text('Current Reading & Statistics:', pageWidth / 2, 48, { align: 'center' })
      
      const waterLevelValues = allData.map(item => parseFloat(item.waterLevel)).filter(val => !isNaN(val))
      const waterLevelMin = waterLevelValues.length > 0 ? Math.min(...waterLevelValues) : 0
      const waterLevelMax = waterLevelValues.length > 0 ? Math.max(...waterLevelValues) : 0
      const waterLevelAvg = waterLevelValues.length > 0 ? 
        (waterLevelValues.reduce((sum, val) => sum + val, 0) / waterLevelValues.length) : 0
      
      doc.setFontSize(9)
      doc.text(`Current: ${currentWaterLevelValue.value}% | Min: ${waterLevelMin.toFixed(2)}% | Avg: ${waterLevelAvg.toFixed(2)}% | Max: ${waterLevelMax.toFixed(2)}%`, 
               pageWidth / 2, 54, { align: 'center' })
      
      let startY = 60
      
      console.log(`📄 Starting table at Y position: ${startY}mm on first page`)
      
      // Configure autoTable for ALL data with full width
      const tableConfig = {
        head: [exportHeaders],
        body: exportRows,
        startY: startY,
        margin: { left: margin, right: margin },
        tableWidth: tableWidth,
        styles: { 
          fontSize: 8,
          cellPadding: 3,
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
          cellPadding: 4
        },
        bodyStyles: {
          cellPadding: 3,
          lineWidth: 0.1,
          minCellHeight: 6
        },
        alternateRowStyles: {
          fillColor: [240, 253, 244]
        },
        // Full width column distribution
        columnStyles: {
          0: { cellWidth: tableWidth * 0.22 }, // Date
          1: { cellWidth: tableWidth * 0.18 }, // Time
          2: { cellWidth: tableWidth * 0.20 }, // Water Level
          3: { cellWidth: tableWidth * 0.25 }, // Status
          // 4: { cellWidth: tableWidth * 0.15 }  // Device
        },
        pageBreak: 'auto',
        showHead: 'everyPage',
        tableLineWidth: 0.1,
        theme: 'grid',
        didParseCell: function (data) {
          // Color code water status cells
          if (data.column.index === 3 && data.section === 'body' && data.cell.raw) {
            const status = data.cell.raw.toString()
            if (status === 'FULL') {
              data.cell.styles.fillColor = [220, 252, 231] // green-100
              data.cell.styles.textColor = [22, 163, 74]   // green-600
            } else if (status === 'SUFFICIENT') {
              data.cell.styles.fillColor = [219, 234, 254] // blue-100
              data.cell.styles.textColor = [37, 99, 235]   // blue-600
            } else if (status === 'LOW') {
              data.cell.styles.fillColor = [254, 249, 195] // yellow-100
              data.cell.styles.textColor = [161, 98, 7]    // yellow-600
            } else if (status === 'EMPTY') {
              data.cell.styles.fillColor = [254, 226, 226] // red-100
              data.cell.styles.textColor = [220, 38, 38]   // red-600
            }
          }
        },
        didDrawPage: function (data) {
          // Only add header on first page
          if (data.pageNumber === 1) {
            doc.setFontSize(16)
            doc.setTextColor(16, 185, 129)
            doc.text('Water Level Data Report', pageWidth / 2, 20, { align: 'center' })
            
            doc.setFontSize(10)
            doc.setTextColor(100, 100, 100)
            doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, 27, { align: 'center' })
            doc.text(`Total Records: ${allData.length}`, pageWidth / 2, 33, { align: 'center' })
            
            // Status summary on first page only
            doc.setFontSize(9)
            doc.setTextColor(75, 85, 99)
            doc.text(statusText, pageWidth / 2, 40, { align: 'center' })
            
            // Current reading and statistics on first page only
            doc.setFontSize(11)
            doc.setTextColor(30, 41, 59)
            doc.text('Current Reading & Statistics:', pageWidth / 2, 48, { align: 'center' })
            
            doc.setFontSize(9)
            doc.text(`Current: ${currentWaterLevelValue.value}% | Min: ${waterLevelMin.toFixed(2)}% | Avg: ${waterLevelAvg.toFixed(2)}% | Max: ${waterLevelMax.toFixed(2)}%`, 
                     pageWidth / 2, 54, { align: 'center' })
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
      
      doc.save(`water_level_report_${timestamp}.pdf`)
      window.showToast(`Exported ${allData.length} Water Level records as PDF`, 'success')
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
                if (cellText === 'FULL') {
                  textRun.color = "16A34A" // Green
                } else if (cellText === 'SUFFICIENT') {
                  textRun.color = "2563EB" // Blue
                } else if (cellText === 'LOW') {
                  textRun.color = "CA8A04" // Yellow
                } else if (cellText === 'EMPTY') {
                  textRun.color = "DC2626" // Red
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
              text: 'Water Level Data Report', 
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
      saveAs(buffer, `water_level_data_${timestamp}.docx`)
      window.showToast(`Exported ${allData.length} Water Level records as DOCX`, 'success')
    }
    
  } catch (error) {
    console.error('❌ Export error:', error)
    window.showToast('Error exporting data. Please try again.', 'error')
  } finally {
    isLoading.value = false
    activeDropdown.value = null
  }
}

// Polling setup
const setupPollingListener = () => {
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
  
  fetchWaterLevelData(1, itemsPerPage.value)
  pollingInterval = setInterval(() => {
    fetchWaterLevelData(currentPage.value, itemsPerPage.value)
  }, POLLING_FREQUENCY)
  
  return () => {
    if (pollingInterval) {
      clearInterval(pollingInterval)
      pollingInterval = null
    }
  }
}

// Watchers
watch(itemsPerPage, (newLimit) => {
  currentPage.value = 1
  fetchWaterLevelData(1, newLimit)
})

watch(currentPage, (newPage) => {
  if (!isFetching.value) {
    fetchWaterLevelData(newPage, itemsPerPage.value)
  }
})

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  setupPollingListener()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
  if (chart.value) {
    chart.value.destroy()
  }
})
</script>
  
<style>
/* Core styles */
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