<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-85px)] mt-1 md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">
      
      <!-- Gradient header for visual appeal - CHANGED TO EMERALD (GREEN) -->
      <div class="bg-gradient-to-r from-emerald-50 to-white p-4 md:p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-sm md:text-xl font-semibold text-gray-800 mb-1">Soil pH Data Table</h1>
            <div class="hidden md:block flex items-center text-xs md:text-sm text-gray-500">
              <span class="text-emerald-600 font-medium">Soil pH</span>
              <ChevronRight class="h-3.5 w-3.5 mx-1 text-gray-400" />
              <span class="text-gray-600">Data Table</span>
            </div>
          </div>
          
          <!-- Controls aligned horizontally with improved styling -->
          <div class="flex md:block flex-row gap-2">
            <!-- Button group - wraps on mobile, nowrap on larger screens -->
            <div class="flex flex-col w-full items-center justify-center md:flex-row flex-wrap sm:flex-nowrap gap-2">
              <div class="relative flex-1 sm:w-56 md:w-72 min-w-0">
                <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-3 sm:h-4 w-3 sm:w-4 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search soil pH measurements..."
                  class="w-full pl-8 sm:pl-10 pr-3 sm:pr-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 text-xs sm:text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                  v-model="searchQuery"
                  @input="performSearch"
                />
              </div>
              
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

      <!-- Date Range Print Modal -->
      <div v-if="showPrintModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 z-50 flex items-center justify-center">
        <div class="bg-white rounded-lg shadow-xl p-6 w-96 max-w-[90%]">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-800">Select Date Range for Print</h3>
            <p class="text-sm text-gray-500 mt-1">Choose the date range for the soil moisture data you want to print</p>
          </div>
          
          <!-- Date Range Inputs -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
              <input 
                type="date" 
                v-model="printDateRange.start"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-1 focus:ring-green-500 focus:border-green-500"
              >
            </div>
            
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">End Date</label>
              <input 
                type="date" 
                v-model="printDateRange.end"
                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-1 focus:ring-green-500 focus:border-green-500"
              >
            </div>
          </div>

          <!-- Error Message -->
          <p v-if="printDateError" class="mt-2 text-sm text-red-600">{{ printDateError }}</p>
          
          <!-- Buttons -->
          <div class="mt-6 flex justify-end space-x-3">
            <button 
              @click="cancelPrint"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50"
            >
              Cancel
            </button>
            <button 
              @click="handlePrintWithDateRange"
              class="px-4 py-2 text-sm font-medium text-white bg-green-500 rounded-md hover:bg-green-600"
            >
              Print
            </button>
          </div>
        </div>
      </div>

      <!-- FIXED: Table and Graph Section - Always maintain consistent layout -->
      <div class="flex-1 overflow-y-auto md:overflow-hidden flex flex-col md:flex-row min-h-0">
        
        <!-- FIXED: Live Graph Container - Fixed width that doesn't expand -->
        <div class="w-full md:w-1/3 lg:w-1/3 md:max-w-[33.333%] border-r border-gray-200 bg-white p-4 md:overflow-y-auto flex-shrink-0">
          <div class="mb-3">
            <h3 class="text-xs md:text-sm font-semibold text-gray-700">Live Soil pH</h3>
            <p class="text-[10px] md:text-xs text-gray-500">Real-time monitoring</p>
          </div>
          
          <!-- Enhanced Combined Graph Container -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
            <!-- Graph Header with improved styling -->
            <div class="p-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full bg-orange-500 mr-1.5"></div>
                <span class="text-[10px] md:text-xs font-medium text-gray-700">pH Level</span>
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
                  <div class="w-1.5 h-1.5 rounded-full bg-orange-500 mr-1"></div>
                  <div class="text-xs font-bold text-orange-600">
                    {{ currentPhValue }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Enhanced Graph Footer with Stats -->
            <div class="border-t border-gray-100 p-3">
              <!-- pH Stats -->
              <div>
                <div class="flex items-center mb-2">
                  <div class="w-3 h-3 rounded-full bg-orange-500 mr-1.5"></div>
                  <div class="text-sm font-medium text-gray-700">Soil pH</div>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-orange-50/50 rounded-md p-2">
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Min</div>
                    <div class="text-sm font-semibold text-orange-600">{{ phStats.min }}</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Avg</div>
                    <div class="text-sm font-semibold text-orange-600">{{ phStats.avg }}</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Max</div>
                    <div class="text-sm font-semibold text-orange-600">{{ phStats.max }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Soil pH Status Information -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">pH Status Guide</h4>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-red-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Acidic</span>
                </div>
                <span class="text-xs text-gray-500">< 3.5 - 6.5</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-green-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Neutral</span>
                </div>
                <span class="text-xs text-gray-500">6.6 - 7.3</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Alkaline</span>
                </div>
                <span class="text-xs text-gray-500">7.4 - >9.0</span>
              </div>
            </div>
          </div>
          
          <!-- Optimal Ranges section -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Optimal Ranges</h4>
            <div class="space-y-3">
              <div>
                <div class="flex items-center mb-1">
                  <div class="w-2 h-2 rounded-full bg-orange-500 mr-1"></div>
                  <span class="text-xs font-medium text-gray-700">Soil pH</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full rounded-full" style="width: 100%; background: linear-gradient(to right, #dc2626 0%, #ea580c 16.67%, #eab308 33.33%, #16a34a 50%, #2563eb 66.67%, #9333ea 83.33%, #7c3aed 100%);"></div>
                </div>
                <div class="flex justify-between mt-1 text-[10px] text-gray-500">
                  <span>3.5</span>
                  <span>6.5</span>
                  <span>7.3</span>
                  <span>9.0</span>
                </div>
                <div class="flex justify-between mt-1 text-[9px] text-gray-400">
                  <span>Acidic</span>
                  <span>Neutral</span>
                  <span>Alkaline</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- FIXED: Table Container - Takes remaining space with consistent width -->
        <div class="w-full md:w-2/3 lg:w-2/3 flex flex-col min-w-0 flex-grow">
          
          <!-- Mobile Card View (shown on small screens) -->
          <div class="sm:hidden flex-1 overflow-auto bg-white p-3 space-y-3">
            <!-- Show loading state or empty state consistently -->
            <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mb-2"></div>
              <p class="text-gray-500 text-xs">Loading soil pH data...</p>
            </div>
            
            <div v-else-if="paginatedData.length === 0" class="flex flex-col items-center justify-center py-8">
              <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
              <p class="text-gray-500 text-xs font-medium">No soil pH data found</p>
              <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
            </div>
            
            <div v-else>
              <div v-for="(row, index) in paginatedData" :key="index" 
                  class="bg-gray-50 rounded-lg p-3 border border-gray-200 mb-2">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <div class="text-xs font-medium text-gray-900">{{ formatDateForDisplay(row.rawTimestamp) }}</div>
                    <div class="text-[10px] text-gray-500">{{ formatTimeForDisplay(row.rawTimestamp) }}</div>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Soil pH</div>
                    <div class="text-xs font-semibold text-orange-600">{{ row.soilPh }}</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">pH Status</div>
                    <span 
                      :class="[
                        'px-2 py-0.5 rounded-full text-[10px] font-medium',
                        row.phStatus === 'NEUTRAL' ? 'bg-green-100 text-green-800' :
                        row.phStatus === 'ACIDIC' ? 'bg-red-100 text-red-800' :
                        'bg-blue-100 text-blue-800'
                      ]"
                    >
                      {{ row.phStatus }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Desktop Table View (shown on medium screens and up) -->
          <div class="hidden sm:flex flex-1 flex-col min-h-0">
            
            <!-- FIXED: Always show table structure even when loading -->
            <div class="flex-1 overflow-y-auto">
              <table class="w-full min-w-full">
                <thead>
                  <tr>
                    
                    <th class="w-[20%] md:w-[25%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-orange-600">Soil pH</div>
                      <div class="text-gray-400 text-[10px]">pH LEVEL</div>
                    </th>
                    <th class="w-[20%] md:w-[25%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-orange-600">pH Status</div>
                      <div class="text-gray-400 text-[10px]">CONDITION</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-gray-600">Date</div>
                      <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-gray-600">Time</div>
                      <div class="text-gray-400 text-[10px]">HH:MM:SS</div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <!-- Loading state row -->
                  <tr v-if="isLoading">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mb-4"></div>
                        <p class="text-gray-500 text-lg font-medium">Loading soil pH data...</p>
                        <p class="text-gray-400 text-sm mt-1">Please wait while we fetch your data</p>
                      </div>
                    </td>
                  </tr>
                  
                  <!-- Data rows -->
                  <tr v-else-if="paginatedData.length > 0"
                      v-for="(row, index) in paginatedData" 
                      :key="index"
                      class="border-b border-gray-50 last:border-0">
                    
                    <td class="w-[25%] px-4 py-3.5 md:text-[15px] whitespace-nowrap border-b border-gray-200">
                      <div class="text-sm font-medium text-orange-600">{{ row.soilPh }}</div>
                    </td>
                    <td class="w-[25%] px-4 py-3.5 md:text-[15px] whitespace-nowrap border-b border-gray-200">
                      <span 
                        :class="[
                          'px-3 py-1 rounded-full text-xs font-medium',
                          row.phStatus === 'NEUTRAL' ? 'bg-green-100 text-green-800' :
                          row.phStatus === 'ACIDIC' ? 'bg-red-100 text-red-800' :
                          'bg-blue-100 text-blue-800'
                        ]"
                      >
                        {{ row.phStatus }}
                      </span>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 md:text-[15px] whitespace-nowrap border-b border-gray-200">
                      <div class="text-sm font-medium text-gray-700">{{ formatDateForDisplay(row.rawTimestamp) }}</div>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 md:text-[15px] whitespace-nowrap border-b border-gray-200">
                      <div class="text-sm font-medium text-gray-700">{{ formatTimeForDisplay(row.rawTimestamp) }}</div>
                    </td>
                  </tr>
                  
                  <!-- Empty state row -->
                  <tr v-else>
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <FileSearch class="h-16 w-16 text-gray-300 mb-4" />
                        <p class="text-gray-500 text-lg font-medium">No soil pH data found</p>
                        <p class="text-gray-400 text-sm mt-1">Try adjusting your search or filters</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
          <div class="border-t border-gray-200 py-2 px-3 bg-gray-50" v-if="!isLoading && paginatedData.length > 0">
              <div class="flex items-center justify-between">
                <div class="text-[10px] md:text-xs text-gray-600">
                  Showing {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, paginationInfo.totalItems) }}
                  of {{ paginationInfo.totalItems }}
                </div>
                <div class="flex items-center gap-1">
                  <button 
                    @click="prevPage"
                    :disabled="currentPage === 1"
                    class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-emerald-600"
                  >
                    <ChevronLeft class="w-3.5 h-3.5" />
                  </button>
                  
                  <div class="flex items-center gap-1">
                    <button
                      v-for="(page, index) in paginationNumbers"
                      :key="index"
                      @click="goToPage(page)"
                      :disabled="page === '...'"
                      :class="[
                        'px-2 py-1 text-[10px] md:text-xs rounded min-w-[20px]',
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
                    :disabled="currentPage >= paginationInfo.totalPages"
                    class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-emerald-600"
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

  <!-- Loading Page Component -->
  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Soil pH Data" 
    message="Please wait while we fetch the latest soil pH measurements"
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

// Utility functions for timestamp handling
const parseBackendTimestamp = (timestamp) => {
  if (!timestamp) return new Date();
  
  // If it's already a Date object, return it
  if (timestamp instanceof Date) {
    return timestamp;
  }
  
  // If it's an ISO string, parse it directly
  if (typeof timestamp === 'string') {
    const date = new Date(timestamp);
    if (!isNaN(date.getTime())) {
      return date;
    }
  }
  
  // If it's a number (Unix timestamp in seconds or milliseconds)
  if (typeof timestamp === 'number') {
    // Check if it's in milliseconds (13 digits) or seconds (10 digits)
    if (timestamp > 1e12) { // milliseconds
      return new Date(timestamp);
    } else { // seconds
      return new Date(timestamp * 1000);
    }
  }
  
  // If it's an object with _seconds (Firebase format)
  if (timestamp && typeof timestamp === 'object' && '_seconds' in timestamp) {
    return new Date(timestamp._seconds * 1000);
  }
  
  // Fallback to current time
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

// Reactive data
const soilPhData = ref([])
const isLoading = ref(true)
const chartCanvas = ref(null)
let chart = null;
const currentPhValue = ref('--')
const lastUpdated = ref('--')
const phStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})
let chartLabels = []
let chartValues = []
let combinedRealtimeData = []

const dataCache = ref(null)
let pollingInterval = null;
let lastProcessedTimestamp = 0;

let PRINT_CHART_DATA_LIMIT = 0;  

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
const currentPage = ref(1)

// UI state
const searchQuery = ref('')
const activeDropdown = ref(null)
const sortKey = ref('date')
const sortDirection = ref('desc')
const activeFilters = ref({})

const filters = ref({
  soilPh: { min: '', max: '' }
})

const filterFields = [
  { key: 'soilPh', label: 'Soil pH Level' }
]

const headers = [
  { key: 'id', label: 'ID' },
  { key: 'soilPh', label: 'Soil pH' },
  { key: 'phStatus', label: 'pH Status' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const exportFormats = ['csv', 'pdf']

// Print-related reactive data
const showPrintModal = ref(false)
const printDateRange = ref({
  start: '',
  end: ''
})
const printDateError = ref('')

// Main data fetching with pagination
const fetchSoilPhData = async (page = 1, limit = 20) => {
  try {
    isLoading.value = true;
    
    console.log(`Fetching page ${page} with limit ${limit}`);
    
    const response = await api.get(`/soil-ph/readings?page=${page}&limit=${limit}`);
    
    console.log('API Response:', response.data);
    
    const { data, pagination } = response.data;
    
    // Update pagination info
    paginationInfo.value = pagination;
    currentPage.value = pagination.currentPage;
    
    const processedData = Array.isArray(data) ? data.map((reading, index) => {
      try {
        // Use the utility function to parse timestamp
        const timestamp = parseBackendTimestamp(reading.timestamp);
        
        // Get soil pH value
        const soilPhValue = reading.soilPh !== undefined ? Number(reading.soilPh) : null;
        const soilPh = soilPhValue !== null ? soilPhValue.toFixed(1) : '--';
        const phStatus = calculatePhStatus(soilPhValue);

        return {
          id: reading.id || `page_${page}_index_${index}`,
          timestamp: timestamp.getTime() / 1000,
          soilPh: soilPh,
          phStatus: phStatus,
          date: formatDateForDisplay(reading.timestamp),
          time: formatTimeForDisplay(reading.timestamp),
          rawTimestamp: timestamp,
          deviceId: reading.device_id || reading.deviceId || 'esp32-1'
        };
      } catch (error) {
        console.error('Error processing reading:', reading, error);
        // Return fallback data with current timestamp
        const fallbackTimestamp = new Date();
        return {
          id: `fallback_${page}_${index}`,
          timestamp: fallbackTimestamp.getTime() / 1000,
          soilPh: '--',
          phStatus: 'UNKNOWN',
          date: formatDateForDisplay(fallbackTimestamp),
          time: formatTimeForDisplay(fallbackTimestamp),
          rawTimestamp: fallbackTimestamp,
          deviceId: 'esp32-1'
        };
      }
    }).filter(reading => reading !== null) : [];

    soilPhData.value = processedData;
    isLoading.value = false;
    
    // Initialize chart with current page data
    initializeChartData(processedData);
    
    console.log(`✅ Processed ${processedData.length} readings for page ${page}`);
    
  } catch (error) {
    console.error("❌ Error in fetchSoilPhData:", error);
    isLoading.value = false;
    
    // Fallback to empty data with default pagination
    soilPhData.value = [];
    paginationInfo.value = {
      currentPage: 1,
      totalPages: 1,
      totalItems: 0,
      itemsPerPage: limit
    };
  }
};

const setupRealtimeListener = () => {
  pollingInterval = setInterval(async () => {
    try {
      const response = await api.get(`/soil-ph/readings/realtime`);
      if (response.data && Array.isArray(response.data)) {
        processRealtimeData(response.data);
      }
    } catch (error) {
      console.error('Polling error:', error);
    }
  }, 5000);
  
  return () => {
    if (pollingInterval) {
      clearInterval(pollingInterval);
    }
  };
};

const processRealtimeData = (data) => {
  if (!Array.isArray(data) || data.length === 0) return;

  try {
    const processedData = data
      .filter(item => item && item.soilPh !== undefined && item.soilPh !== null && item.soilPh !== '--')
      .map((item, index) => {
        try {
          const timestamp = parseBackendTimestamp(item.timestamp);
          const value = Number(item.soilPh);
          
          if (isNaN(value)) return null;
          
          return {
            timestamp,
            value,
            deviceId: item.deviceId || 'esp32-1',
            soilPh: value.toFixed(1),
            phStatus: calculatePhStatus(value),
            date: formatDateForDisplay(item.timestamp),
            time: formatTimeForDisplay(item.timestamp),
            rawTimestamp: timestamp,
            id: `rt_${Date.now()}_${index}`
          };
        } catch {
          return null;
        }
      })
      .filter(item => item !== null);
    
    // Add new data to table (prepend to show newest first)
    if (processedData.length > 0) {
      soilPhData.value = [...processedData, ...soilPhData.value].slice(0, 100);
    }
    
    // Update chart data
    const chartDataPoints = processedData.map(item => ({
      timestamp: item.timestamp,
      value: item.value,
      deviceId: item.deviceId
    }));
    
    combinedRealtimeData = [...combinedRealtimeData, ...chartDataPoints];
    combinedRealtimeData.sort((a, b) => b.timestamp - a.timestamp);
    combinedRealtimeData = combinedRealtimeData.slice(0, 20);
    
    const chronologicalData = [...combinedRealtimeData].sort((a, b) => a.timestamp - b.timestamp);
    
    chartLabels = chronologicalData.map(item => 
      item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      })
    );
    
    chartValues = chronologicalData.map(item => item.value);
    
    if (combinedRealtimeData.length > 0) {
      const latestReading = combinedRealtimeData[0];
      currentPhValue.value = latestReading.value.toFixed(1);
      
      lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      });
      
      const values = combinedRealtimeData.map(item => item.value);
      phStats.value = {
        min: Math.min(...values).toFixed(1),
        max: Math.max(...values).toFixed(1),
        avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(1)
      };
    }
    
    updateChart();
    
  } catch (error) {
    console.error('Error in processRealtimeData:', error);
  }
};

const fetchStats = async () => {
  try {
    const response = await api.get(`/soil-ph/stats?hours=24`);
    const stats = response.data;
    
    phStats.value = {
      min: typeof stats.min === 'number' ? stats.min.toFixed(1) : '--',
      max: typeof stats.max === 'number' ? stats.max.toFixed(1) : '--',
      avg: typeof stats.avg === 'number' ? stats.avg.toFixed(1) : '--'
    };
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
};

const calculatePhStatus = (ph) => {
  if (ph === null || ph === undefined) return 'UNKNOWN';
  if (ph < 6.6) return 'ACIDIC';
  if (ph >= 6.6 && ph <= 7.3) return 'NEUTRAL';
  return 'ALKALINE';
}

// Chart functions
const initializeChartData = (data) => {
  // Sort data by timestamp (newest first) and take the first 20
  const sortedData = [...data]
    .filter(item => item.soilPh !== '--' && !isNaN(Number(item.soilPh)))
    .sort((a, b) => new Date(b.rawTimestamp) - new Date(a.rawTimestamp))
    .slice(0, 20)
    .sort((a, b) => new Date(a.rawTimestamp) - new Date(b.rawTimestamp)); // Sort chronologically for chart

  chartLabels = sortedData.map(item => 
    item.rawTimestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
  );
  
  chartValues = sortedData.map(item => Number(item.soilPh));
  combinedRealtimeData = sortedData.map(item => ({
    timestamp: item.rawTimestamp,
    value: Number(item.soilPh),
    deviceId: item.deviceId || 'esp32-1'
  }));
  
  if (sortedData.length > 0) {
    const latestReading = sortedData[sortedData.length - 1];
    currentPhValue.value = latestReading.soilPh;
    
    lastUpdated.value = latestReading.rawTimestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    });
  }
  
  initializeChart();
};

const initializeChart = () => {
  nextTick(() => {
    if (!chartCanvas.value) return;
    
    // Destroy existing chart
    if (chart && typeof chart.destroy === 'function') {
      try {
        chart.destroy();
      } catch (error) {
        console.error('Error destroying chart:', error);
      }
    }
    
    try {
      const ctx = chartCanvas.value.getContext('2d');
      
      // Calculate proper y-axis range
      const values = chartValues.filter(val => !isNaN(val));
      const minValue = values.length > 0 ? Math.min(...values) : 0;
      const maxValue = values.length > 0 ? Math.max(...values) : 14;
      const yMin = Math.max(0, Math.floor(minValue * 0.9));
      const yMax = Math.min(14, Math.ceil(maxValue * 1.1));
      
      chart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartLabels,
          datasets: [{
            label: 'Soil pH',
            data: chartValues,
            borderColor: '#f97316',
            backgroundColor: 'rgba(249, 115, 22, 0.15)',
            borderWidth: 2.5,
            tension: 0.4,
            fill: true,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#f97316',
            pointBorderWidth: 1.5
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: {
            duration: 0
          },
          interaction: {
            mode: 'index',
            intersect: false,
          },
          scales: {
            y: {
              beginAtZero: false,
              min: yMin,
              max: yMax,
              title: {
                display: true,
                text: 'pH Level',
                color: '#f97316',
                font: {
                  size: 11,
                  weight: '600'
                }
              },
              ticks: {
                font: {
                  size: 10
                },
                color: '#64748b',
                padding: 8
              },
              grid: {
                color: 'rgba(0, 0, 0, 0.04)',
                drawBorder: false
              }
            },
            x: {
              ticks: {
                font: {
                  size: 10
                },
                maxRotation: 0,
                padding: 8,
                color: '#64748b'
              },
              grid: {
                display: false,
                drawBorder: false
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              titleColor: '#334155',
              bodyColor: '#334155',
              borderColor: '#e2e8f0',
              borderWidth: 1,
              padding: 12,
              cornerRadius: 6,
              displayColors: true,
              boxWidth: 8,
              boxHeight: 8,
              usePointStyle: true,
              titleFont: {
                size: 12,
                weight: '600'
              },
              bodyFont: {
                size: 12
              },
              callbacks: {
                label: function(context) {
                  return `pH: ${context.raw.toFixed(1)}`;
                }
              }
            }
          }
        }
      });
    } catch (error) {
      console.error('Error initializing chart:', error);
    }
  });
};

const updateChart = () => {
  if (!chart) return;

  try {
    // Only update if we have data
    if (chartValues.length === 0) return;
    
    // Update chart data
    chart.data.labels = [...chartLabels];
    chart.data.datasets[0].data = [...chartValues];
    
    // Calculate proper min/max values for y-axis
    const values = chartValues.filter(val => !isNaN(val));
    const minValue = values.length > 0 ? Math.min(...values) : 0;
    const maxValue = values.length > 0 ? Math.max(...values) : 14;
    
    // Set y-axis range with some padding
    const yMin = Math.max(0, Math.floor(minValue * 0.9));
    const yMax = Math.min(14, Math.ceil(maxValue * 1.1));
    
    if (chart.options && chart.options.scales && chart.options.scales.y) {
      chart.options.scales.y.min = yMin;
      chart.options.scales.y.max = yMax;
    }
    
    // Update the chart
    chart.update();
  } catch (error) {
    console.error('Error updating chart:', error);
  }
};

// Pagination functions
const nextPage = async () => {
  if (currentPage.value < paginationInfo.value.totalPages) {
    await fetchSoilPhData(currentPage.value + 1, itemsPerPage.value);
  }
};

const prevPage = async () => {
  if (currentPage.value > 1) {
    await fetchSoilPhData(currentPage.value - 1, itemsPerPage.value);
  }
};

const goToPage = async (page) => {
  if (typeof page === 'number' && page >= 1 && page <= paginationInfo.value.totalPages) {
    await fetchSoilPhData(page, itemsPerPage.value);
  }
};

const paginationNumbers = computed(() => {
  const total = paginationInfo.value.totalPages;
  const current = currentPage.value;
  
  if (total <= 1) return [1];
  
  if (current === 1) {
    return [1, '..', total];
  } else if (current === total) {
    return [1, '..', total];
  } else {
    return [current, '...', total];
  }
});

// Client-side data processing (for current page)
const sortedByTimestampData = computed(() => {
  return [...soilPhData.value].sort((a, b) => {
    const aTime = a.rawTimestamp instanceof Date ? a.rawTimestamp.getTime() : new Date(a.rawTimestamp).getTime();
    const bTime = b.rawTimestamp instanceof Date ? b.rawTimestamp.getTime() : new Date(b.rawTimestamp).getTime();
    
    // Sort newest first (descending order)
    return bTime - aTime;
  });
});

const filteredData = computed(() => {
  let result = [...sortedByTimestampData.value]

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
  const startIndex = (currentPage.value - 1) * itemsPerPage.value
  const endIndex = startIndex + itemsPerPage.value
  return sortedData.value.slice(startIndex, endIndex)
})

const totalPages = computed(() => {
  return Math.ceil(sortedData.value.length / itemsPerPage.value)
})

// UI functions
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

const performSearch = async () => {
  if (searchQuery.value.trim()) {
    try {
      isLoading.value = true;
      const response = await api.get(`/soil-ph/readings/search?query=${encodeURIComponent(searchQuery.value)}&page=1&limit=${itemsPerPage.value}`);
      const { data, pagination } = response.data;
      
      // Process search results with proper timestamp handling
      const processedData = Array.isArray(data) ? data.map((reading, index) => {
        try {
          const timestamp = parseBackendTimestamp(reading.timestamp);
          const soilPhValue = reading.soilPh !== undefined ? Number(reading.soilPh) : null;
          const soilPh = soilPhValue !== null ? soilPhValue.toFixed(1) : '--';
          const phStatus = calculatePhStatus(soilPhValue);

          return {
            id: reading.id || `search_${index}`,
            timestamp: timestamp.getTime() / 1000,
            soilPh: soilPh,
            phStatus: phStatus,
            date: formatDateForDisplay(reading.timestamp),
            time: formatTimeForDisplay(reading.timestamp),
            rawTimestamp: timestamp,
            deviceId: reading.device_id || reading.deviceId || 'esp32-1'
          };
        } catch (error) {
          console.error('Error processing search result:', reading, error);
          return null;
        }
      }).filter(reading => reading !== null) : [];

      soilPhData.value = processedData;
      paginationInfo.value = pagination;
      currentPage.value = 1;
      isLoading.value = false;
    } catch (error) {
      console.error('Search error:', error);
      isLoading.value = false;
      currentPage.value = 1;
    }
  } else {
    // If search is cleared, fetch normal paginated data
    fetchSoilPhData(1, itemsPerPage.value);
  }
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
  currentPage.value = 1 
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

// Print functions with date range filtering
const openPrintModal = () => {
  // Set default date range (last 7 days)
  const endDate = new Date();
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - 7);
  
  printDateRange.value = {
    start: startDate.toISOString().split('T')[0],
    end: endDate.toISOString().split('T')[0]
  };
  
  printDateError.value = '';
  showPrintModal.value = true;
  activeDropdown.value = null;
}

const cancelPrint = () => {
  showPrintModal.value = false;
  printDateError.value = '';
}

const handlePrintWithDateRange = async () => {
  // Validate date range
  if (!printDateRange.value.start || !printDateRange.value.end) {
    printDateError.value = 'Please select both start and end dates';
    return;
  }

  const startDate = new Date(printDateRange.value.start);
  const endDate = new Date(printDateRange.value.end);
  endDate.setHours(23, 59, 59, 999); // Include entire end day

  if (startDate > endDate) {
    printDateError.value = 'Start date cannot be after end date';
    return;
  }

  try {
    isLoading.value = true;
    showPrintModal.value = false;
    
    // Fetch data for the selected date range
      const response = await api.get(`/soil-ph/readings/range?from_date=${printDateRange.value.start}&to_date=${printDateRange.value.end}`);
    
    const data = response.data.data || [];
    
    // Process the data for printing
    const soilPhRows = data.map((reading, index) => {
      try {
        const timestamp = parseBackendTimestamp(reading.timestamp);
        const soilPhValue = reading.soilPh !== undefined ? Number(reading.soilPh) : null;
        const soilPh = soilPhValue !== null ? soilPhValue.toFixed(1) : '--';
        const phStatus = calculatePhStatus(soilPhValue);

        return {
          id: reading.id || `print_${index}`,
          date: formatDateForDisplay(reading.timestamp),
          time: formatTimeForDisplay(reading.timestamp),
          device: reading.device_id || reading.deviceId || 'esp32-1',
          soilPh: soilPh,
          phStatus: phStatus,
          rawTimestamp: timestamp
        };
      } catch (error) {
        console.error('Error processing reading for print:', reading, error);
        return null;
      }
    }).filter(reading => reading !== null);

    if (soilPhRows.length === 0) {
      window.showToast('No data found for the selected date range', 'warning');
      isLoading.value = false;
      return;
    }

    // Sort by timestamp (newest first)
    soilPhRows.sort((a, b) => b.rawTimestamp - a.rawTimestamp);

    // Generate print content
    await generatePrintContent(soilPhRows, printDateRange.value);
    
  } catch (error) {
    console.error('Error fetching data for print:', error);
    window.showToast('Error fetching data for printing', 'error');
  } finally {
    isLoading.value = false;
  }
}

const generatePrintContent = async (soilPhRows, dateRange) => {
  const now = new Date();
  const formattedDate = now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });

  // Prepare chart data
  const printChartData = soilPhRows
    .filter(item => item.soilPh !== '--' && !isNaN(Number(item.soilPh)))
    .map(item => ({
      timestamp: item.rawTimestamp, 
      value: Number(item.soilPh)
    }))
    .sort((a, b) => a.timestamp - b.timestamp);

  // Calculate statistics with safe defaults
  const values = printChartData.map(item => item.value);
  const minValue = values.length > 0 ? Math.min(...values) : 0;
  const maxValue = values.length > 0 ? Math.max(...values) : 14;
  const avgValue = values.length > 0 ? values.reduce((sum, val) => sum + val, 0) / values.length : 0;

  let chartImage = '';
  
  // Generate chart if we have data
  if (printChartData.length > 0) {
    chartImage = await generateChartImage(printChartData, minValue, maxValue);
  }

  // Generate the print HTML
  generatePrintHTML(chartImage, soilPhRows, formattedDate, now, printChartData.length, minValue, maxValue, avgValue, dateRange);
}

const generateChartImage = async (chartData, minValue, maxValue) => {
  return new Promise((resolve) => {
    // Check if we have data to create a chart
    if (!chartData || chartData.length === 0) {
      resolve('');
      return;
    }

    try {
      const tempContainer = document.createElement('div');
      tempContainer.style.position = 'absolute';
      tempContainer.style.left = '-9999px';
      tempContainer.style.top = '-9999px';
      tempContainer.style.width = '800px';
      tempContainer.style.height = '400px';
      
      const tempCanvas = document.createElement('canvas');
      tempCanvas.width = 800;
      tempCanvas.height = 400;
      tempContainer.appendChild(tempCanvas);
      document.body.appendChild(tempContainer);

      const ctx = tempCanvas.getContext('2d');
      
      const tempChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.map(item => {
            return item.timestamp.toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              hour12: true
            });
          }),
          datasets: [{
            label: 'Soil pH',
            data: chartData.map(item => item.value),
            borderColor: '#f97316',
            backgroundColor: 'rgba(249, 115, 22, 0.15)',
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointRadius: 3,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#f97316',
            pointBorderWidth: 2
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
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              min: Math.max(0, Math.floor(minValue * 0.95)),
              max: Math.min(14, Math.ceil(maxValue * 1.05)),
              title: {
                display: true,
                text: 'pH Level',
                color: '#f97316',
                font: { size: 14, weight: '600' }
              },
              ticks: {
                font: { size: 12 },
                color: '#64748b'
              },
              grid: {
                color: 'rgba(100, 116, 139, 0.2)'
              }
            },
            x: {
              ticks: {
                font: { size: 10 },
                color: '#64748b',
                maxTicksLimit: 8,
                maxRotation: 45
              }
            }
          }
        }
      });

      setTimeout(() => {
        try {
          const chartImage = tempCanvas.toDataURL('image/png', 1.0);
          tempChart.destroy();
          document.body.removeChild(tempContainer);
          resolve(chartImage);
        } catch (error) {
          console.error('Error capturing chart:', error);
          document.body.removeChild(tempContainer);
          resolve('');
        }
      }, 500);
      
    } catch (error) {
      console.error('Error creating chart:', error);
      resolve('');
    }
  });
}

const generatePrintHTML = (chartImage, soilPhRows, formattedDate, now, chartRecordCount, minValue, maxValue, avgValue, dateRange) => {
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Soil pH Analysis Data - ${dateRange.start} to ${dateRange.end}</title>
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
          color: #f97316;
          font-size: 16px;
          font-weight: 600;
          margin: 5px 0;
        }
        .header .date {
          color: #6b7280;
          font-size: 14px;
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
        .chart-range {
          text-align: center;
          margin-bottom: 15px;
          font-size: 12px;
          color: #f97316;
          font-weight: 600;
          background-color: #fffbeb;
          padding: 8px;
          border-radius: 6px;
          border: 1px solid #fef3c7;
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
        .soil-ph { color: #f97316; font-weight: 500; }
        .status-neutral { color: #059669; }
        .status-acidic { color: #dc2626; }
        .status-alkaline { color: #2563eb; }
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
          color: #f97316;
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
        <h1>Soil pH Analysis Report</h1>
        <div class="date-range">Date Range: ${dateRange.start} to ${dateRange.end}</div>
        <div class="date">${formattedDate}</div>
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-item">
          <span class="summary-label">Date Range:</span>
          <span class="summary-value">${dateRange.start} to ${dateRange.end}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Total Records:</span>
          <span class="summary-value">${soilPhRows.length}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Chart Data Points:</span>
          <span class="summary-value">${chartRecordCount}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">pH Range:</span>
          <span class="summary-value">${minValue.toFixed(1)} - ${maxValue.toFixed(1)}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Average pH:</span>
          <span class="summary-value">${avgValue.toFixed(1)}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Report Generated:</span>
          <span class="summary-value">${now.toLocaleString()}</span>
        </div>
      </div>
      
      ${chartImage ? `
        <div class="section-header">Soil pH Trend Analysis</div>
        <div class="chart-title">Soil pH Levels Over Time</div>
        <div class="chart-info">Showing ${chartRecordCount} data points from selected date range</div>
        <div class="chart-range">pH Range: ${minValue.toFixed(1)} (Min) - ${maxValue.toFixed(1)} (Max) | Average: ${avgValue.toFixed(1)}</div>
        <img src="${chartImage}" class="chart-image" alt="Soil pH Chart" />
        
        <div class="stats-summary">
          <div class="stat-item">
            <h4>Soil pH Statistics</h4>
            <div class="stat-values">
              Min: ${minValue.toFixed(1)}<br>
              Avg: ${avgValue.toFixed(1)}<br>
              Max: ${maxValue.toFixed(1)}
            </div>
          </div>
          <div class="stat-item">
            <h4>Data Points</h4>
            <div class="stat-values">
              Total: ${chartRecordCount}<br>
              Date Range<br>
              ${dateRange.start} to ${dateRange.end}
            </div>
          </div>
          <div class="stat-item">
            <h4>pH Status</h4>
            <div class="stat-values">
              ${minValue < 6.6 ? 'Acidic' : minValue <= 7.3 ? 'Neutral' : 'Alkaline'} Range<br>
              Optimal: 6.6 - 7.3
            </div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">No chart data available for the selected date range</p>'}
      
      <div class="section-header">Detailed Soil pH Sensor Readings</div>
      <table>
        <thead>
          <tr>
            <th style="width: 10%">ID</th>
            <th style="width: 15%">Date</th>
            <th style="width: 12%">Time</th>
            <th style="width: 10%">Device</th>
            <th style="width: 15%">Soil pH</th>
            <th style="width: 15%">pH Status</th>
          </tr>
        </thead>
        <tbody>
          ${soilPhRows.map(row => `
            <tr>
              <td>${row.id}</td>
              <td>${row.date}</td>
              <td>${row.time}</td>
              <td>${row.device}</td>
              <td><span class="soil-ph">${row.soilPh}</span></td>
              <td>
                <span class="${
                  row.phStatus === 'NEUTRAL' ? 'status-neutral' :
                  row.phStatus === 'ACIDIC' ? 'status-acidic' : 'status-alkaline'
                }">${row.phStatus}</span>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by Soil pH Analysis System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
      </div>
    </body>
    </html>
  `;
  
  try {
    // Open print window with better error handling
    const printWindow = window.open('', '_blank', 'width=800,height=600');
    
    if (!printWindow) {
      throw new Error('Popup window was blocked. Please allow popups for this site.');
    }
    
    printWindow.document.write(tableContent);
    printWindow.document.close();
    
    // Wait for the window to load before printing
    printWindow.onload = function() {
      try {
        printWindow.focus();
        printWindow.print();
        
        // Close the window after printing (or if user cancels)
        setTimeout(() => {
          if (!printWindow.closed) {
            printWindow.close();
          }
        }, 500);
      } catch (printError) {
        console.error('Error during printing:', printError);
        window.showToast('Error during printing', 'error');
        printWindow.close();
      }
    };
    
  } catch (error) {
    console.error('Error opening print window:', error);
    window.showToast('Error opening print window. Please allow popups.', 'error');
    
    // Fallback: Try to print in current window
    try {
      const currentWindow = window.open();
      currentWindow.document.write(tableContent);
      currentWindow.document.close();
      currentWindow.print();
      setTimeout(() => currentWindow.close(), 500);
    } catch (fallbackError) {
      console.error('Fallback print also failed:', fallbackError);
      window.showToast('Print functionality is not available', 'error');
    }
  }
}

const exportData = async (format) => {
  try {
    isLoading.value = true
    console.log(`📤 Starting ${format.toUpperCase()} export...`)
    
    // For exports, fetch all data without pagination
    let allData = []
    
    try {
      console.log('🚀 Fetching all Soil pH data for export...')
      const response = await api.get('/soil-ph/readings/all')
      
      if (response.data && Array.isArray(response.data)) {
        allData = response.data.map((reading, index) => {
          const timestamp = parseBackendTimestamp(reading.timestamp)
          
          // Use soilPh field from backend, fallback to ph field
          const phValue = reading.soilPh !== undefined ? reading.soilPh : reading.ph
          const phNumber = parseFloat(phValue) || 0
          
          // Determine pH status
          let phStatus = 'Unknown'
          if (phValue !== '--' && !isNaN(phNumber)) {
            if (phNumber < 6.5) {
              phStatus = 'Acidic'
            } else if (phNumber >= 6.5 && phNumber <= 7.5) {
              phStatus = 'Neutral'
            } else if (phNumber > 7.5) {
              phStatus = 'Alkaline'
            }
          }
          
          return {
            id: reading.id || `export_${index}`,
            ph: phValue?.toFixed(2) || '--',
            phStatus: phStatus,
            date: formatDateForDisplay(reading.timestamp),
            time: formatTimeForDisplay(reading.timestamp),
            rawTimestamp: timestamp,
            deviceId: reading.device_id || 'esp32-1',
            timestampMs: timestamp.getTime()
          }
        })
        
        // Sort by timestamp (newest first)
        allData.sort((a, b) => b.timestampMs - a.timestampMs)
        
        console.log(`✅ Fetched ${allData.length} records for export`)
      }
    } catch (error) {
      console.error('❌ Error fetching all data for export:', error)
      // Fallback to current data if /all endpoint doesn't exist
      allData = sortedData.value
    }

    if (!allData.length) {
      window.showToast('No data available for export', 'warning')
      isLoading.value = false
      return
    }

    // Create export data with pH status
    const exportHeaders = ['Date', 'Time', 'pH Level', 'pH Status', 'Device']
    const exportRows = allData.map(row => [
      row.date || formatDateForDisplay(row.rawTimestamp),
      row.time || formatTimeForDisplay(row.rawTimestamp), 
      row.ph !== undefined ? row.ph : '--',
      row.phStatus !== undefined ? row.phStatus : 'Unknown',
      row.deviceId || 'esp32-1'
    ])

    const timestamp = new Date().toISOString().split('T')[0]

    if (format === 'csv') {
      let csvContent = exportHeaders.join(',') + '\n'
      exportRows.forEach(row => {
        csvContent += row.map(val => `"${val}"`).join(',') + '\n'
      })
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      saveAs(blob, `soil_ph_data_${timestamp}.csv`)
      window.showToast(`Exported ${allData.length} Soil pH records as CSV`, 'success')
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
      
      // Title section - more compact
      doc.setFontSize(16)
      doc.setTextColor(16, 163, 74)
      doc.text('Soil pH Data Report', pageWidth / 2, 20, { align: 'center' })
      
      doc.setFontSize(10)
      doc.setTextColor(100, 100, 100)
      doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, 27, { align: 'center' })
      doc.text(`Total Records: ${allData.length}`, pageWidth / 2, 33, { align: 'center' })
      
      // Add pH status summary - more compact
      const statusCounts = allData.reduce((acc, row) => {
        const status = row.phStatus || 'Unknown'
        acc[status] = (acc[status] || 0) + 1
        return acc
      }, {})
      
      doc.setFontSize(9)
      doc.setTextColor(75, 85, 99)
      
      let statusY = 40
      const statusEntries = Object.entries(statusCounts)
      let statusText = 'pH Status: '
      statusEntries.forEach(([status, count], index) => {
        const percentage = ((count / allData.length) * 100).toFixed(1)
        statusText += `${status} ${count} (${percentage}%)`
        if (index < statusEntries.length - 1) statusText += ' | '
      })
      
      // Single line for status summary to save space
      doc.text(statusText, pageWidth / 2, statusY, { align: 'center' })
      
      // FIXED: Start table much lower to utilize first page space
      let startY = 48 // Reduced from higher position
      
      console.log(`📄 Starting table at Y position: ${startY}mm on first page`)
      
      // Configure autoTable
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
          fillColor: [16, 163, 74],
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
          fillColor: [250, 250, 250]
        },
        columnStyles: {
          0: { cellWidth: tableWidth * 0.22 }, // Date
          1: { cellWidth: tableWidth * 0.18 }, // Time
          2: { cellWidth: tableWidth * 0.15 }, // pH Level
          3: { cellWidth: tableWidth * 0.25 }, // pH Status
          4: { cellWidth: tableWidth * 0.20 }  // Device
        },
        pageBreak: 'auto',
        showHead: 'everyPage',
        tableLineWidth: 0.1,
        theme: 'grid',
        didParseCell: function (data) {
          // Color code pH status cells
          if (data.column.index === 3 && data.section === 'body' && data.cell.raw) {
            const status = data.cell.raw.toString()
            if (status === 'Acidic') {
              data.cell.styles.fillColor = [254, 226, 226]
              data.cell.styles.textColor = [220, 38, 38]
            } else if (status === 'Neutral') {
              data.cell.styles.fillColor = [254, 252, 232]
              data.cell.styles.textColor = [202, 138, 4]
            } else if (status === 'Alkaline') {
              data.cell.styles.fillColor = [219, 234, 254]
              data.cell.styles.textColor = [37, 99, 235]
            }
          }
        },
        didDrawPage: function (data) {
          // Only add header on first page
          if (data.pageNumber === 1) {
            doc.setFontSize(16)
            doc.setTextColor(16, 163, 74)
            doc.text('Soil pH Data Report', pageWidth / 2, 20, { align: 'center' })
            
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
      
      doc.save(`soil_ph_report_${timestamp}.pdf`)
      window.showToast(`Exported ${allData.length} Soil pH records as PDF`, 'success')
    } else if (format === 'docs') {
      const tableRows = [
        new TableRow({
          children: exportHeaders.map(h => new TableCell({
            children: [new Paragraph({ children: [new TextRun({ text: h, bold: true })] })],
            shading: {
              fill: "2DA74B",
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
                if (cellText === 'Acidic') {
                  textRun.color = "FF0000"
                } else if (cellText === 'Neutral') {
                  textRun.color = "FFA500"
                } else if (cellText === 'Alkaline') {
                  textRun.color = "0000FF"
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
              text: 'Soil pH Data Report', 
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
      saveAs(buffer, `soil_ph_data_${timestamp}.docx`)
      window.showToast(`Exported ${allData.length} Soil pH records as DOCX`, 'success')
    }
    
  } catch (error) {
    console.error('❌ Export error:', error)
    window.showToast('Error exporting data. Please try again.', 'error')
  } finally {
    isLoading.value = false
    activeDropdown.value = null 
  }
}

watch([searchQuery, activeFilters, itemsPerPage], () => {
  currentPage.value = 1
})

let cleanupRealtime = null

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  
  // Always setup realtime listener, regardless of initial data
  cleanupRealtime = setupRealtimeListener();
  
  // Fetch first page of data with pagination
  fetchSoilPhData(1, itemsPerPage.value);
  fetchStats();
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  
  if (chart && typeof chart.destroy === 'function') {
    try {
      chart.destroy();
    } catch (error) {
      console.error('Error destroying chart:', error);
    }
  }
  
  if (pollingInterval) {
    clearInterval(pollingInterval);
  }
});
</script>
  
<style>
/* Your existing CSS styles remain exactly the same */
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

/* Table styling */
table {
  table-layout: fixed;
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
}

/* Fix table header and body alignment */
thead th, tbody td {
  box-sizing: border-box;
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