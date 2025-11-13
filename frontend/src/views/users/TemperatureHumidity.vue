<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-85px)] mt-1 md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">        <!-- Gradient header for visual appeal -->
      <!-- Gradient header for visual appeal -->
      <div class="bg-gradient-to-r from-emerald-50 to-white p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-sm md:text-xl font-semibold text-gray-800 mb-1">Temperature & Humidity Data Table</h1>
            <div class="flex items-center text-xs md:text-sm text-gray-500">
              <span class="text-emerald-600 font-medium">Temperature & Humidity</span>
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
                  placeholder="Search NPK measurements..."
                  class="w-full pl-8 sm:pl-10 pr-3 sm:pr-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 text-xs sm:text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                  v-model="searchQuery"
                  @input="performSearch"
                />
              </div>
              
              <!-- Items Per Page Selector -->
              <div class="relative flex-1 sm:flex-none">
                <select 
                  v-model="itemsPerPage"
                  @change="handleItemsPerPageChange"
                  class="w-full px-3 py-2 rounded-lg border border-gray-200 bg-white text-xs text-gray-700 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 shadow-sm"
                >
                  <option value="10">10/page</option>
                  <option value="20">20/page</option>
                  <option value="50">50/page</option>
                  <option value="100">100/page</option>
                </select>
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

                <!-- Print Button -->
                <div class="relative flex-1 sm:flex-none">
                  <button 
                    @click="openDateRangeModal"
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

      <!-- Table and Graph Section - Fixed flex container with proper width constraints -->
      <div class="flex-1 overflow-auto md:overflow-hidden flex flex-col md:flex-row min-h-0">
        <!-- Live Graph Container - FIXED: constrained width that doesn't expand -->
        <div class="w-full md:w-1/3 md:max-w-[33.333333%] md:min-w-[300px] lg:w-1/3 lg:max-w-[33.333333%] border-r border-gray-200 bg-white p-4 md:overflow-y-auto flex-shrink-0">
          <div class="mb-3">
            <h3 class="text-xs md:text-sm font-semibold text-gray-700">Live Temperature & Humidity</h3>
            <p class="text-[10px] md:text-xs text-gray-500">Real-time monitoring</p>
          </div>
          
          <!-- Enhanced Combined Graph Container with fixed dimensions -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4 max-w-full">
            <!-- Graph Header with improved styling -->
            <div class="p-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
              <div class="flex items-center gap-4">
                <div class="flex items-center">
                  <div class="w-3 h-3 rounded-full bg-red-500 mr-1.5"></div>
                  <span class="text-[10px] md:text-xs font-medium text-gray-700">Temp (°C)</span>
                </div>
                <div class="flex items-center">
                  <div class="w-3 h-3 rounded-full bg-blue-500 mr-1.5"></div>
                  <span class="text-[10px] md:text-xs font-medium text-gray-700">Humidity (%)</span>
                </div>
              </div>
              <div class="text-[10px] md:text-xs text-gray-500">
                Last updated: {{ lastUpdated }}
              </div>
            </div>
            
            <!-- Graph Canvas with fixed height and responsive width -->
            <div class="h-[280px] p-3 relative w-full max-w-full overflow-hidden">
              <canvas ref="chartCanvas" class="w-full h-full max-w-full"></canvas>
              
              <!-- Repositioned and Resized Current Values Indicator -->
              <div class="absolute top-3 left-3 bg-white/95 backdrop-blur-sm rounded-md px-2 py-1 shadow-sm border border-gray-100" style="max-width: 80px; z-index: 10;">
                <div class="text-[10px] font-medium text-gray-500 mb-0.5">Current</div>
                <div class="flex items-center mb-0.5">
                  <div class="w-1.5 h-1.5 rounded-full bg-red-500 mr-1"></div>
                  <div class="text-xs font-bold text-red-600">
                    {{ currentTempValue }}°C
                  </div>
                </div>
                <div class="flex items-center">
                  <div class="w-1.5 h-1.5 rounded-full bg-blue-500 mr-1"></div>
                  <div class="text-xs font-bold text-blue-600">
                    {{ currentHumidityValue }}%
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Enhanced Graph Footer with Stats -->
            <div class="border-t border-gray-100 p-3">
              <!-- Temperature Stats -->
              <div class="mb-3">
                <div class="flex items-center mb-2">
                  <div class="w-3 h-3 rounded-full bg-red-500 mr-1.5"></div>
                  <div class="text-sm font-medium text-gray-700">Temperature</div>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-red-50/50 rounded-md p-2">
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Min</div>
                    <div class="text-sm font-semibold text-red-600">{{ tempStats.min }}°C</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Avg</div>
                    <div class="text-sm font-semibold text-red-600">{{ tempStats.avg }}°C</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Max</div>
                    <div class="text-sm font-semibold text-red-600">{{ tempStats.max }}°C</div>
                  </div>
                </div>
              </div>
              
              <!-- Humidity Stats -->
              <div>
                <div class="flex items-center mb-2">
                  <div class="w-3 h-3 rounded-full bg-blue-500 mr-1.5"></div>
                  <div class="text-sm font-medium text-gray-700">Humidity</div>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-blue-50/50 rounded-md p-2">
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Min</div>
                    <div class="text-sm font-semibold text-blue-600">{{ humidityStats.min }}%</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Avg</div>
                    <div class="text-sm font-semibold text-blue-600">{{ humidityStats.avg }}%</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Max</div>
                    <div class="text-sm font-semibold text-blue-600">{{ humidityStats.max }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Optimal Ranges section (kept this as it's useful) -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4 max-w-full">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Optimal Ranges</h4>
            <div class="space-y-3">
              <div>
                <div class="flex items-center mb-1">
                  <div class="w-2 h-2 rounded-full bg-red-500 mr-1"></div>
                  <span class="text-xs font-medium text-gray-700">Temperature</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-green-200 via-green-500 to-yellow-500 rounded-full" style="width: 70%"></div>
                </div>
                <div class="flex justify-between mt-1 text-[10px] text-gray-500">
                  <span>20°C</span>
                  <span>25°C</span>
                  <span>30°C</span>
                </div>
              </div>
              
              <div>
                <div class="flex items-center mb-1">
                  <div class="w-2 h-2 rounded-full bg-blue-500 mr-1"></div>
                  <span class="text-xs font-medium text-gray-700">Humidity</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-blue-200 via-blue-500 to-indigo-500 rounded-full" style="width: 60%"></div>
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
        
        <!-- Table Container - FIXED: takes remaining space without expanding graph -->
        <div class="w-full md:w-2/3 md:flex-1 lg:w-2/3 lg:flex-1 flex flex-col min-w-0">
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
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Temperature</div>
                  <div class="text-xs font-semibold" :class="getTemperatureTextClass(row.temperature)">{{ row.temperature }}°C</div>
                </div>
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Humidity</div>
                  <div class="text-xs font-semibold" :class="getHumidityTextClass(row.humidity)">{{ row.humidity }}%</div>
                </div>
              </div>
            </div>
            
            <div v-if="paginatedData.length === 0 && !isLoading" 
                class="flex flex-col items-center justify-center py-8">
              <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
              <p class="text-gray-500 text-xs font-medium">No temperature & humidity data found</p>
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
                      <div class="text-red-600">Temperature</div>
                      <div class="text-gray-400 text-[10px]">(°C)</div>
                    </th>
                    <th class="w-[25%] py-3.5 px-4 text-left text-xs md:text-[15px] bg-gray-100 font-medium uppercase tracking-wider">
                      <div class="text-blue-600">Humidity</div>
                      <div class="text-gray-400 text-[10px]">(%)</div>
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
                    
                    <td class="w-[25%] px-4 py-3.5 md:text-[15px] whitespace-nowrap border-b border-gray-200">
                      <div class="text-sm font-medium" :class="getTemperatureTextClass(row.temperature)">
                        {{ row.temperature }}°C
                      </div>
                    </td>
                    <td class="w-[25%] px-4 py-3.5 md:text-[15px] whitespace-nowrap border-b border-gray-200">
                      <div class="text-sm font-medium" :class="getHumidityTextClass(row.humidity)">
                        {{ row.humidity }}%
                      </div>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 md:text-[15px] whitespace-nowrap border-b border-gray-200">
                      <div class="text-sm font-medium text-gray-700">{{ row.date }}</div>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 md:text-[15px] whitespace-nowrap border-b border-gray-200">
                      <div class="text-sm font-medium text-gray-700">{{ row.time }}</div>
                    </td>
                  </tr>
                  
                  <!-- Empty state when no data -->
                  <tr v-if="paginatedData.length === 0 && !isLoading">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <FileSearch class="h-16 w-16 text-gray-300 mb-4" />
                        <p class="text-gray-500 text-lg font-medium">No temperature & humidity data found</p>
                        <p class="text-gray-400 text-sm mt-1">Try adjusting your search or filters</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Pagination Section -->
          <div class="border-t border-gray-200 py-2 px-3 bg-gray-50 flex-shrink-0">
            <div class="flex items-center justify-between">
              <div class="text-[10px] md:text-xs text-gray-600">
                Showing {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, totalItems) }}
                of {{ totalItems }}
              </div>
              <div class="flex items-center gap-1">
                <button 
                  @click="prevPage"
                  :disabled="currentPage === 1"
                  class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600"
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
                        ? 'bg-green-500 text-white font-medium' 
                        : page === '...' 
                          ? 'text-gray-400 cursor-default' 
                          : 'text-gray-700 hover:text-green-600 hover:bg-gray-100'
                    ]"
                  >
                    {{ page }}
                  </button>
                </div>
                
                <button 
                  @click="nextPage"
                  :disabled="currentPage >= totalPages"
                  class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600"
                >
                  <ChevronRight class="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Date Range Selection Modal for Printing -->
    <div v-show="showDateRangeModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
        <!-- Modal Header -->
        <div class="bg-green-500 text-white px-6 py-4 rounded-t-lg">
          <h3 class="text-lg font-semibold">Select Date Range for Printing</h3>
        </div>
        
        <!-- Modal Body -->
        <div class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
            <input
              type="date"
              v-model="printStartDate"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
            <input
              type="date"
              v-model="printEndDate"
              class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500"
            />
          </div>
          
          <div class="text-xs text-gray-500">
            <p>• Select the date range for the data you want to print</p>
            <p>• Leave empty to print all available data</p>
          </div>
        </div>
        
        <!-- Modal Footer -->
        <div class="bg-gray-50 px-6 py-4 rounded-b-lg flex justify-end space-x-3">
          <button
            @click="showDateRangeModal = false"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Cancel
          </button>
          <button
            @click="confirmPrintWithDateRange"
            class="px-4 py-2 text-sm font-medium text-white bg-green-500 border border-transparent rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Generate Print
          </button>
        </div>
      </div>
    </div>

    <LoadingPage 
      :isVisible="isLoading" 
      title="Loading Temperature & Humidity Data" 
      message="Please wait while we fetch the latest temperature and humidity measurements"
    />
  </div>
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

const tempHumidityData = ref([])
const isLoading = ref(true)
const totalItems = ref(0)
const totalPages = ref(1)

const chartCanvas = ref(null)
const chart = ref(null)

const chartData = ref([])

const currentTempValue = ref('--')
const currentHumidityValue = ref('--')
const lastUpdated = ref('--')
const tempStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})
const humidityStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})

// Print date range modal
const showDateRangeModal = ref(false)
const printStartDate = ref('')
const printEndDate = ref('')

let pollingInterval = null
const POLLING_FREQUENCY = 5000 

let PRINT_CHART_DATA_LIMIT = 0 

// Open date range selection modal
const openDateRangeModal = () => {
  // Close any open dropdowns
  activeDropdown.value = null;
  
  // Set default dates (last 7 days)
  const endDate = new Date();
  const startDate = new Date();
  startDate.setDate(startDate.getDate() - 7);
  
  printEndDate.value = endDate.toISOString().split('T')[0];
  printStartDate.value = startDate.toISOString().split('T')[0];
  
  showDateRangeModal.value = true;
}

// Confirm print with selected date range
const confirmPrintWithDateRange = async () => {
  showDateRangeModal.value = false;
  isLoading.value = true;

  try {
    // Validate date inputs
    if (!printStartDate.value || !printEndDate.value) {
      window.showToast('Please select both start and end dates', 'warning');
      isLoading.value = false;
      return;
    }
    const startDate = new Date(printStartDate.value);
    const endDate = new Date(printEndDate.value);
    if (startDate > endDate) {
      window.showToast('Start date cannot be after end date', 'warning');
      isLoading.value = false;
      return;
    }

    // Fetch data from the correct endpoint with correct parameter names
    const response = await api.get('/temperature-humidity/readings/range', {
      params: {
        from_date: printStartDate.value,
        to_date: printEndDate.value
      }
    });
    const filteredData = response.data || [];

    if (filteredData.length === 0) {
      window.showToast('No data found for the selected date range.', 'warning');
      isLoading.value = false;
      return;
    }

    // Process and print the data
    await printTableWithDateRange(filteredData);

  } catch (error) {
    console.error('Error printing with date range:', error);
    window.showToast('Failed to generate print. Please check your date range.', 'error');
  } finally {
    isLoading.value = false;
  }
}

// Modified print function with date range
const printTableWithDateRange = async (filteredData) => {
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
  
  // Use the filteredData passed as parameter instead of fetching again
  const tempHumidityRows = filteredData.map((row, index) => ({
    id: index + 1,
    date: row.date,
    time: row.time,
    device: row.deviceId || 'N/A',
    temperature: row.temperature,
    humidity: row.humidity
  }));
  
  // Prepare chart data for printing
  const allForPrint = filteredData
    .filter(item => item.temperature !== '--' && item.humidity !== '--' && item.rawTimestamp)
    .map(item => ({
      timestamp: item.rawTimestamp,
      temperature: Number(item.temperature),
      humidity: Number(item.humidity)
    }))
    .sort((a, b) => a.timestamp - b.timestamp);
  
  console.log(`📊 Print chart will show ${allForPrint.length} records from selected date range`);
  
  const tempValues = allForPrint.map(item => item.temperature);
  const humidityValues = allForPrint.map(item => item.humidity);
  
  const tempMin = tempValues.length > 0 ? Math.min(...tempValues) : 0;
  const tempMax = tempValues.length > 0 ? Math.max(...tempValues) : 50;
  const tempAvg = tempValues.length > 0 ? 
    (tempValues.reduce((sum, val) => sum + val, 0) / tempValues.length) : 0;
  
  const humidityMin = humidityValues.length > 0 ? Math.min(...humidityValues) : 0;
  const humidityMax = humidityValues.length > 0 ? Math.max(...humidityValues) : 100;
  const humidityAvg = humidityValues.length > 0 ? 
    (humidityValues.reduce((sum, val) => sum + val, 0) / humidityValues.length) : 0;
  
  let chartImage = '';
  
  try {
    const ctx = tempCanvas.getContext('2d');
    
    if (allForPrint.length > 0) {
      const tempChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: allForPrint.map(item => {
            return item.timestamp.toLocaleDateString('en-US', {
              month: 'short',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
              hour12: true
            })
          }),
          datasets: [
            {
              label: 'Temperature (°C)',
              data: allForPrint.map(item => item.temperature),
              borderColor: '#ef4444',
              backgroundColor: 'rgba(239, 68, 68, 0.15)',
              borderWidth: 3,
              tension: 0.4,
              fill: true,
              pointRadius: 3,
              pointHoverRadius: 5,
              pointBackgroundColor: '#ffffff',
              pointBorderColor: '#ef4444',
              pointBorderWidth: 2,
              yAxisID: 'y-temperature'
            },
            {
              label: 'Humidity (%)',
              data: allForPrint.map(item => item.humidity),
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.15)',
              borderWidth: 3,
              tension: 0.4,
              fill: true,
              pointRadius: 3,
              pointHoverRadius: 5,
              pointBackgroundColor: '#ffffff',
              pointBorderColor: '#3b82f6',
              pointBorderWidth: 2,
              yAxisID: 'y-humidity'
            }
          ]
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
            'y-temperature': {
              type: 'linear',
              display: true,
              position: 'left',
              title: {
                display: true,
                text: 'Temperature (°C)',
                color: '#ef4444',
                font: {
                  size: 14,
                  weight: '600'
                }
              },
              beginAtZero: false,
              min: Math.max(0, Math.floor(tempMin * 0.95)),
              max: Math.ceil(tempMax * 1.05),
              ticks: {
                font: { size: 12 },
                color: '#ef4444',
                padding: 8
              },
              grid: {
                color: 'rgba(239, 68, 68, 0.1)'
              }
            },
            'y-humidity': {
              type: 'linear',
              display: true,
              position: 'right',
              title: {
                display: true,
                text: 'Humidity (%)',
                color: '#3b82f6',
                font: {
                  size: 14,
                  weight: '600'
                }
              },
              beginAtZero: false,
              min: Math.max(0, Math.floor(humidityMin * 0.95)),
              max: Math.min(100, Math.ceil(humidityMax * 1.05)),
              ticks: {
                font: { size: 12 },
                color: '#3b82f6',
                padding: 8
              },
              grid: {
                drawOnChartArea: false
              }
            },
            x: {
              ticks: {
                font: { size: 10 },
                color: '#64748b',
                maxTicksLimit: 10,
                maxRotation: 45
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
          
          generatePrintHTML(chartImage, tempHumidityRows, formattedDate, now, 
                           allForPrint.length, tempMin, tempMax, tempAvg, 
                           humidityMin, humidityMax, humidityAvg);
        } catch (error) {
          console.error('Error capturing chart:', error);
          document.body.removeChild(tempContainer);
          generatePrintHTML('', tempHumidityRows, formattedDate, now, 0, 0, 0, 0, 0, 0, 0);
        }
      }, 500);
    } else {
      document.body.removeChild(tempContainer);
      generatePrintHTML('', tempHumidityRows, formattedDate, now, 0, 0, 0, 0, 0, 0, 0);
    }
    
  } catch (error) {
    console.error('Error creating chart:', error);
    document.body.removeChild(tempContainer);
    generatePrintHTML('', tempHumidityRows, formattedDate, now, 0, 0, 0, 0, 0, 0, 0);
  }
}

const fetchDataForPrintAll = async () => {
  try {
    const params = new URLSearchParams();
    
    // For /readings/all endpoint, use simple date format
    if (printStartDate.value) {
      params.append('start_date', printStartDate.value);
    }
    
    if (printEndDate.value) {
      params.append('end_date', printEndDate.value);
    }
    
    console.log('🔍 Using /readings/all endpoint with params:', params.toString());
    
    const response = await api.get(`/temperature-humidity/readings/all?${params.toString()}`);
    const allReadings = response.data;
    
    console.log(`📊 /readings/all endpoint returned ${allReadings.length} readings`);
    
    const processedData = allReadings.map((reading, index) => {
      let formattedDate = '--';
      let formattedTime = '--';
      let rawTimestamp = null;

      try {
        if (reading.timestamp) {
          if (typeof reading.timestamp === 'string') {
            rawTimestamp = new Date(reading.timestamp);
          } else if (typeof reading.timestamp === 'object' && reading.timestamp.$date) {
            rawTimestamp = new Date(reading.timestamp.$date);
          } else if (reading.timestamp instanceof Date) {
            rawTimestamp = reading.timestamp;
          } else if (reading.timestamp._seconds) {
            rawTimestamp = new Date(reading.timestamp._seconds * 1000);
          }
        }

        if (rawTimestamp && !isNaN(rawTimestamp.getTime())) {
          formattedDate = rawTimestamp.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit'
          });

          formattedTime = rawTimestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          });
        }
      } catch (e) {
        console.error("Error formatting date:", e, reading.timestamp);
      }

      const temperature = reading.temperature !== undefined && reading.temperature !== null 
        ? Number(reading.temperature).toFixed(2) 
        : '--';
      
      const humidity = reading.humidity !== undefined && reading.humidity !== null 
        ? Number(reading.humidity).toFixed(2) 
        : '--';

      return {
        id: index + 1,
        temperature: temperature,
        humidity: humidity,
        date: formattedDate,
        time: formattedTime,
        rawTimestamp: rawTimestamp,
        deviceId: reading.device_id || 'esp32-2',
        soilMoisture: reading.soilMoisture || null
      };
    });

    return processedData;
  } catch (error) {
    console.error("❌ Error fetching data from /readings/all endpoint:", error);
    
    if (error.response) {
      console.error('Backend response error:', error.response.data);
    }
    
    window.showToast('Failed to fetch data for printing from all endpoint.', 'error');
    return [];
  }
}

const fetchDataForPrintRange = async () => {
  try {
    if (!printStartDate.value || !printEndDate.value) {
      console.error('❌ Both start and end dates are required for range endpoint');
      return [];
    }
    
    console.log('📅 Using range endpoint with dates:', printStartDate.value, 'to', printEndDate.value);
    
    // Remove the limit parameter from the URL
    const response = await api.get(`/temperature-humidity/readings/range?from_date=${printStartDate.value}&to_date=${printEndDate.value}`);
    const allReadings = response.data; // Now response.data is directly the array
    
    console.log(`📊 Range endpoint returned ${allReadings.length} readings`);
    
    if (allReadings.length === 0) {
      console.warn('⚠️ No data returned from range endpoint.');
    }
    
    const processedData = allReadings.map((reading, index) => {
      let formattedDate = '--';
      let formattedTime = '--';
      let rawTimestamp = null;

      try {
        if (reading.timestamp) {
          if (typeof reading.timestamp === 'string') {
            rawTimestamp = new Date(reading.timestamp);
          } else if (typeof reading.timestamp === 'object' && reading.timestamp.$date) {
            rawTimestamp = new Date(reading.timestamp.$date);
          } else if (reading.timestamp instanceof Date) {
            rawTimestamp = reading.timestamp;
          } else if (reading.timestamp._seconds) {
            rawTimestamp = new Date(reading.timestamp._seconds * 1000);
          }
        }

        if (rawTimestamp && !isNaN(rawTimestamp.getTime())) {
          formattedDate = rawTimestamp.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit'
          });

          formattedTime = rawTimestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          });
        }
      } catch (e) {
        console.error("Error formatting date:", e, reading.timestamp);
      }

      const temperature = reading.temperature !== undefined && reading.temperature !== null 
        ? Number(reading.temperature).toFixed(2) 
        : '--';
      
      const humidity = reading.humidity !== undefined && reading.humidity !== null 
        ? Number(reading.humidity).toFixed(2) 
        : '--';

      return {
        id: index + 1,
        temperature: temperature,
        humidity: humidity,
        date: formattedDate,
        time: formattedTime,
        rawTimestamp: rawTimestamp,
        deviceId: reading.device_id || 'esp32-2',
        soilMoisture: reading.soilMoisture || null
      };
    });

    return processedData;
  } catch (error) {
    console.error("❌ Error fetching data from range endpoint:", error);
    
    if (error.response) {
      console.error('Backend response error:', error.response.data);
      console.error('Status:', error.response.status);
    }
    
    // Don't show error toast here, let the fallback handle it
    console.log('🔄 Range endpoint failed, will try fallback...');
    throw error; // Re-throw to trigger fallback
  }
}

const generatePrintHTML = (chartImage, tempHumidityRows, formattedDate, now, 
                          chartRecordCount, tempMin, tempMax, tempAvg, 
                          humidityMin, humidityMax, humidityAvg) => {
  // Add date range info to summary
  const dateRangeText = printStartDate.value && printEndDate.value 
    ? `${printStartDate.value} to ${printEndDate.value}`
    : 'All available data';

  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Temperature & Humidity Data Report</title>
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
        .temperature { color: #ef4444; font-weight: 500; }
        .humidity { color: #3b82f6; font-weight: 500; }
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
          grid-template-columns: repeat(2, 1fr);
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
        .stat-item.temperature {
          border-left: 4px solid #ef4444;
        }
        .stat-item.humidity {
          border-left: 4px solid #3b82f6;
        }
        .stat-item h4 {
          margin: 0 0 10px 0;
          font-size: 14px;
          font-weight: 600;
        }
        .stat-item.temperature h4 {
          color: #ef4444;
        }
        .stat-item.humidity h4 {
          color: #3b82f6;
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
        <h1>Temperature & Humidity Data Report</h1>
        <div class="date">${formattedDate}</div>
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-item">
          <span class="summary-label">Date Range:</span>
          <span class="summary-value">${dateRangeText}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Total Records:</span>
          <span class="summary-value">${tempHumidityRows.length}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Chart Data Points:</span>
          <span class="summary-value">${chartRecordCount}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Report Generated:</span>
          <span class="summary-value">${now.toLocaleString()}</span>
        </div>
      </div>
      
      <div class="section-header">Temperature & Humidity Trend Analysis</div>
      ${chartImage ? `
        <div class="chart-title">Temperature & Humidity Levels Over Time</div>
        <div class="chart-info">Showing ${chartRecordCount} data points from selected date range</div>
        <img src="${chartImage}" class="chart-image" alt="Temperature & Humidity Chart" />
        
        <div class="stats-summary">
          <div class="stat-item temperature">
            <h4>Temperature Statistics</h4>
            <div class="stat-values">
              Min: ${tempMin.toFixed(2)}°C<br>
              Avg: ${tempAvg.toFixed(2)}°C<br>
              Max: ${tempMax.toFixed(2)}°C
            </div>
          </div>
          <div class="stat-item humidity">
            <h4>Humidity Statistics</h4>
            <div class="stat-values">
              Min: ${humidityMin.toFixed(2)}%<br>
              Avg: ${humidityAvg.toFixed(2)}%<br>
              Max: ${humidityMax.toFixed(2)}%
            </div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">No chart data available for the selected date range</p>'}
      
      <div class="section-header">Detailed Temperature & Humidity Sensor Readings</div>
      <table>
        <thead>
          <tr>
            <th style="width: 8%">ID</th>
            <th style="width: 15%">Date</th>
            <th style="width: 12%">Time</th>
            <th style="width: 10%">Device</th>
            <th style="width: 15%">Temperature</th>
            <th style="width: 15%">Humidity</th>
          </tr>
        </thead>
        <tbody>
          ${tempHumidityRows.map(row => `
            <tr>
              <td>${row.id}</td>
              <td>${row.date}</td>
              <td>${row.time}</td>
              <td>${row.device}</td>
              <td><span class="temperature">${row.temperature}°C</span></td>
              <td><span class="humidity">${row.humidity}%</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by Temperature & Humidity Monitoring System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
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

const paginationNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 1) return [1]
  
  if (current === 1) {
    return total <= 3 ? Array.from({length: total}, (_, i) => i + 1) : [1, 2, '...', total]
  } else if (current === total) {
    return total <= 3 ? Array.from({length: total}, (_, i) => i + 1) : [1, '...', total - 1, total]
  } else {
    if (total <= 5) {
      return Array.from({length: total}, (_, i) => i + 1)
    } else {
      return [1, '...', current - 1, current, current + 1, '...', total]
    }
  }
})

const dataCache = ref(null)

// New function to fetch all data for export/print
const fetchAllDataForExport = async () => {
  try {
    const response = await api.get('/temperature-humidity/readings?limit=0')
    const allReadings = response.data.data || response.data
    
    const processedData = allReadings.map((reading, index) => {
      let formattedDate = '--'
      let formattedTime = '--'
      let timestampSeconds = null
      let rawTimestamp = null

      try {
        if (reading.timestamp) {
          if (typeof reading.timestamp === 'object') {
            const sec = reading.timestamp._seconds ?? reading.timestamp.seconds
            const nsec = reading.timestamp._nanoseconds ?? reading.timestamp.nanoseconds
            if (sec !== undefined && sec !== null) {
              const s = Number(sec)
              const ns = Number(nsec) || 0
              if (!isNaN(s)) rawTimestamp = new Date(s * 1000 + ns / 1000000)
            }
          } else if (typeof reading.timestamp === 'number') {
            const num = Number(reading.timestamp)
            if (num > 1e12) {
              rawTimestamp = new Date(num)
            } else {
              rawTimestamp = new Date(num * 1000)
            }
          } else if (typeof reading.timestamp === 'string') {
            const parsed = new Date(reading.timestamp)
            if (!isNaN(parsed)) rawTimestamp = parsed
          }
        }

        if (rawTimestamp && !isNaN(rawTimestamp.getTime())) {
          formattedDate = rawTimestamp.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit'
          })

          formattedTime = rawTimestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          })

          timestampSeconds = rawTimestamp.getTime() / 1000
        }
      } catch (e) {
        console.error("Error formatting date:", e, reading.timestamp)
      }

      const temperature = reading.temperature !== undefined && reading.temperature !== null 
        ? Number(reading.temperature).toFixed(2) 
        : '--'
      
      const humidity = reading.humidity !== undefined && reading.humidity !== null 
        ? Number(reading.humidity).toFixed(2) 
        : '--'

      return {
        id: index + 1,
        timestamp: timestampSeconds,
        temperature: temperature,
        humidity: humidity,
        date: formattedDate,
        time: formattedTime,
        rawTimestamp: rawTimestamp,
        deviceId: reading.device_id,
        soilMoisture: reading.soilMoisture || null
      }
    })

    return processedData
  } catch (error) {
    console.error("❌ Error fetching all data for export:", error)
    return []
  }
}

// Function to fetch latest 20 records for chart only
const fetchLatestChartData = async () => {
  try {
    const response = await api.get('/temperature-humidity/readings?limit=20&sort=desc')
    const allReadings = response.data.data || response.data
    
    const processedData = allReadings.map((reading, index) => {
      let formattedDate = '--'
      let formattedTime = '--'
      let timestampSeconds = null
      let rawTimestamp = null

      try {
        if (reading.timestamp) {
          if (typeof reading.timestamp === 'object') {
            const sec = reading.timestamp._seconds ?? reading.timestamp.seconds
            const nsec = reading.timestamp._nanoseconds ?? reading.timestamp.nanoseconds
            if (sec !== undefined && sec !== null) {
              const s = Number(sec)
              const ns = Number(nsec) || 0
              if (!isNaN(s)) rawTimestamp = new Date(s * 1000 + ns / 1000000)
            }
          } else if (typeof reading.timestamp === 'number') {
            const num = Number(reading.timestamp)
            if (num > 1e12) {
              rawTimestamp = new Date(num)
            } else {
              rawTimestamp = new Date(num * 1000)
            }
          } else if (typeof reading.timestamp === 'string') {
            const parsed = new Date(reading.timestamp)
            if (!isNaN(parsed)) rawTimestamp = parsed
          }
        }

        if (rawTimestamp && !isNaN(rawTimestamp.getTime())) {
          formattedDate = rawTimestamp.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit'
          })

          formattedTime = rawTimestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          })

          timestampSeconds = rawTimestamp.getTime() / 1000
        }
      } catch (e) {
        console.error("Error formatting date:", e, reading.timestamp)
      }

      const temperature = reading.temperature !== undefined && reading.temperature !== null 
        ? Number(reading.temperature).toFixed(2) 
        : '--'
      
      const humidity = reading.humidity !== undefined && reading.humidity !== null 
        ? Number(reading.humidity).toFixed(2) 
        : '--'

      return {
        id: index + 1,
        timestamp: timestampSeconds,
        temperature: temperature,
        humidity: humidity,
        date: formattedDate,
        time: formattedTime,
        rawTimestamp: rawTimestamp,
        deviceId: reading.device_id,
        soilMoisture: reading.soilMoisture || null
      }
    })

    // Initialize chart data with the latest 20 records
    initializeChartData(processedData)
    
  } catch (error) {
    console.error("❌ Error fetching latest chart data:", error)
  }
}

// Updated fetch function with pagination - FOR TABLE DATA ONLY
const fetchTempHumidityData = async (page = 1, limit = 20) => {
  try {
    // isLoading.value = true
    
    const params = new URLSearchParams({
      page: page.toString(),
      limit: limit.toString()
    })
    
    // Add search query if provided
    if (searchQuery.value) {
      params.append('search', searchQuery.value)
    }
    
    // Use the correct endpoint with pagination parameters
    const response = await api.get(`/temperature-humidity/readings?${params.toString()}`)
    const result = response.data
    
    // DEBUG: show raw readings shapes so we can diagnose timestamp formats
    console.debug('DEBUG: raw readings sample (from /temperature-humidity/readings):', result.data?.slice(0, 5) || result.slice(0, 5))
    console.log(`📊 Temperature & humidity readings fetched: ${result.data?.length || result.length} (Page ${page}, Limit ${limit})`)
      
    const allReadings = result.data || result
    
    const processedData = allReadings.map((reading, index) => {
        // Handle timestamp --- use the timestamp from the DB only. Do NOT default to current time.
        let formattedDate = '--'
        let formattedTime = '--'
        let timestampSeconds = null
        let rawTimestamp = null

        try {
          if (reading.timestamp) {
              // Several possible timestamp shapes we may receive from backend:
              // - Firestore-like: { _seconds, _nanoseconds } or { seconds, nanoseconds }
              // - MongoDB $date: { $date: 167... } or { $date: { $numberLong: '...' } }
              // - Numeric seconds or milliseconds
              // - ISO string
              try {
                // If timestamp is a JSON string containing an object, parse it first
                if (typeof reading.timestamp === 'string' && reading.timestamp.trim().startsWith('{')) {
                  try {
                    reading.timestamp = JSON.parse(reading.timestamp)
                  } catch (e) {
                    // ignore parse error and continue
                    console.debug('DEBUG: failed to JSON.parse timestamp string', reading.timestamp)
                  }
                }

                if (typeof reading.timestamp === 'object') {
                  // Firestore-like
                  const sec = reading.timestamp._seconds ?? reading.timestamp.seconds
                  const nsec = reading.timestamp._nanoseconds ?? reading.timestamp.nanoseconds
                  if (sec !== undefined && sec !== null) {
                    const s = Number(sec)
                    const ns = Number(nsec) || 0
                    if (!isNaN(s)) rawTimestamp = new Date(s * 1000 + ns / 1000000)
                  } else if ('$date' in reading.timestamp) {
                    const d = reading.timestamp.$date
                    if (typeof d === 'number') {
                      rawTimestamp = new Date(d)
                    } else if (typeof d === 'string') {
                      const parsed = new Date(d)
                      if (!isNaN(parsed)) rawTimestamp = parsed
                    } else if (d && typeof d === 'object' && ('$numberLong' in d)) {
                      const ms = Number(d.$numberLong)
                      if (!isNaN(ms)) rawTimestamp = new Date(ms)
                    }
                  }
                  // Fallback: scan object (including nested objects) for numeric-looking properties
                  if (!rawTimestamp) {
                    const stack = [reading.timestamp]
                    const seen = new Set()
                    while (stack.length && !rawTimestamp) {
                      const obj = stack.pop()
                      if (!obj || typeof obj !== 'object') continue
                      if (seen.has(obj)) continue
                      seen.add(obj)
                      for (const val of Object.values(obj)) {
                        if (val == null) continue
                        if (typeof val === 'object') {
                          stack.push(val)
                          continue
                        }
                        const maybeNum = Number(val)
                        if (!isNaN(maybeNum)) {
                          // Heuristic: >1e12 is ms, >1e9 is seconds
                          if (maybeNum > 1e12) {
                            rawTimestamp = new Date(maybeNum)
                          } else if (maybeNum > 1e9) {
                            rawTimestamp = new Date(maybeNum * 1000)
                          }
                          if (rawTimestamp) break
                        }
                      }
                    }
                  }
                } else if (typeof reading.timestamp === 'number') {
                  // Could be seconds or milliseconds -- guess based on magnitude
                  const num = Number(reading.timestamp)
                  if (num > 1e12) {
                    // milliseconds
                    rawTimestamp = new Date(num)
                  } else {
                    // seconds
                    rawTimestamp = new Date(num * 1000)
                  }
                } else if (typeof reading.timestamp === 'string') {
                  const parsed = new Date(reading.timestamp)
                  if (!isNaN(parsed)) rawTimestamp = parsed
                }
              } catch (e) {
                console.warn('Unhandled timestamp shape', reading.timestamp, e)
              }
            }

            if (rawTimestamp && !isNaN(rawTimestamp.getTime())) {
            formattedDate = rawTimestamp.toLocaleDateString('en-US', {
              year: 'numeric',
              month: 'short',
              day: '2-digit'
            })

            formattedTime = rawTimestamp.toLocaleTimeString('en-US', {
              hour: '2-digit',
              minute: '2-digit',
              second: '2-digit',
              hour12: true
            })

            timestampSeconds = rawTimestamp.getTime() / 1000
          } else {
            // Keep placeholders when timestamp missing or invalid
            console.warn('Invalid or missing timestamp on reading:', reading)
          }
        } catch (e) {
          console.error("Error formatting date:", e, reading.timestamp)
        }

      const temperature = reading.temperature !== undefined && reading.temperature !== null 
        ? Number(reading.temperature).toFixed(2) 
        : '--'
      
      const humidity = reading.humidity !== undefined && reading.humidity !== null 
        ? Number(reading.humidity).toFixed(2) 
        : '--'

      return {
        id: (page - 1) * limit + index + 1, // Calculate ID based on pagination
        timestamp: timestampSeconds,
        temperature: temperature,
        humidity: humidity,
        date: formattedDate,
        time: formattedTime,
        rawTimestamp: rawTimestamp, // may be null if timestamp invalid
        deviceId: reading.device_id,
        soilMoisture: reading.soilMoisture || null
      }
    })

    dataCache.value = processedData
    
    // Update the main data array
    tempHumidityData.value = processedData
    
    // Update pagination info
    if (result.pagination) {
      totalItems.value = result.pagination.totalItems
      totalPages.value = result.pagination.totalPages
    } else {
      // Fallback if backend doesn't return pagination info
      totalItems.value = processedData.length
      totalPages.value = Math.ceil(processedData.length / limit)
    }
    
    // DEBUG: show processedData sample (after parsing)
    console.debug('DEBUG: processed readings sample:', processedData.slice(0, 5))
    isLoading.value = false
    
    // Set print chart data limit from current table data
    PRINT_CHART_DATA_LIMIT = processedData.length
    
  } catch (error) {
    console.error("❌ Error fetching temperature and humidity data:", error)
    isLoading.value = false
    
    if (dataCache.value) {
      tempHumidityData.value = dataCache.value
    }
  }
}

const setupPollingListener = () => {
  // Clear any existing interval
  if (pollingInterval) {
    clearInterval(pollingInterval)
  }
  
  // Fetch initial data separately
  fetchLatestChartData() // Fetch latest 20 records for chart
  fetchTempHumidityData(currentPage.value, itemsPerPage.value) // Fetch current page for table
  
  // Set up polling
  pollingInterval = setInterval(() => {
    fetchLatestChartData() // Always fetch latest 20 for chart
    fetchTempHumidityData(currentPage.value, itemsPerPage.value) // Fetch current page for table
  }, POLLING_FREQUENCY)
  
  // Return cleanup function
  return () => {
    if (pollingInterval) {
      clearInterval(pollingInterval)
      pollingInterval = null
    }
  }
}

// Additional helper functions with correct endpoints
const fetchFilteredData = async (deviceId = null, startDate = null, endDate = null) => {
  try {
    const params = new URLSearchParams()
    if (deviceId) params.append('device_id', deviceId)
    if (startDate) params.append('start_date', startDate.toISOString())
    if (endDate) params.append('end_date', endDate.toISOString())
    
    const url = `/temperature-humidity/readings?${params.toString()}`
    const response = await api.get(url)
    return response.data
    
  } catch (error) {
    console.error('Error fetching filtered data:', error)
    throw error
  }
}

const fetchStatistics = async (deviceId = null, hours = 24) => {
  try {
    const params = new URLSearchParams()
    if (deviceId) params.append('device_id', deviceId)
    params.append('hours', hours.toString())
    
    const url = `/temperature-humidity/stats?${params.toString()}`
    const response = await api.get(url)
    return response.data
    
  } catch (error) {
    console.error('Error fetching statistics:', error)
    throw error
  }
}

const fetchAvailableDevices = async () => {
  try {
    const response = await api.get('/temperature-humidity/devices')
    return response.data.devices
    
  } catch (error) {
    console.error('Error fetching devices:', error)
    throw error
  }
}

const fetchReadingsCount = async (deviceId = null) => {
  try {
    const params = new URLSearchParams()
    if (deviceId) params.append('device_id', deviceId)
    
    const url = `/temperature-humidity/count?${params.toString()}`
    const response = await api.get(url)
    return response.data.count
    
  } catch (error) {
    console.error('Error fetching readings count:', error)
    throw error
  }
}

const fetchTimeRange = async (deviceId = null) => {
  try {
    const params = new URLSearchParams()
    if (deviceId) params.append('device_id', deviceId)
    
    const url = `/temperature-humidity/time-range?${params.toString()}`
    const response = await api.get(url)
    return response.data
    
  } catch (error) {
    console.error('Error fetching time range:', error)
    throw error
  }
}

const initializeChartData = (data) => {
  // Ensure we pick the most recent 20 readings regardless of incoming order.
  // First, create a copy and sort by timestamp descending (newest first),
  // then take the first 20 (most recent), then sort those ascending for plotting oldest->newest.
  const dataSortedDesc = [...data].sort((a, b) => {
    const aT = a.timestamp == null ? -Infinity : a.timestamp
    const bT = b.timestamp == null ? -Infinity : b.timestamp
    return bT - aT
  })
  const recentData = dataSortedDesc.slice(0, 20)

  // Only include items that have valid rawTimestamp (timestamp saved in DB).
  const chartDataPoints = recentData
    .filter(item => item.temperature !== '--' && item.humidity !== '--' && item.rawTimestamp)
    .map(item => ({
      timestamp: item.rawTimestamp,
      temperature: Number(item.temperature),
      humidity: Number(item.humidity)
    }))
    .filter(pt => pt.timestamp instanceof Date && !isNaN(pt.timestamp.getTime()))
    .sort((a, b) => a.timestamp - b.timestamp) // Ensure oldest -> newest order for the chart

  chartData.value = chartDataPoints

  if (!chartDataPoints.length) {
    console.warn('DEBUG: initializeChartData -> no chart points available. recentData length=', recentData.length, 'filtered ->', recentData.filter(item=> item.temperature !== '--' && item.humidity !== '--').length)
    console.debug('DEBUG: recentData sample:', recentData.slice(0,5))
  }

  if (chartDataPoints.length > 0) {
    const latestReading = chartDataPoints[chartDataPoints.length - 1]
    currentTempValue.value = latestReading.temperature.toFixed(2)
    currentHumidityValue.value = latestReading.humidity.toFixed(2)
    
    const formattedTime = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    lastUpdated.value = formattedTime
    
    const tempValues = chartDataPoints.map(item => item.temperature)
    const humidityValues = chartDataPoints.map(item => item.humidity)
    
    tempStats.value = {
      min: Math.min(...tempValues).toFixed(2),
      max: Math.max(...tempValues).toFixed(2),
      avg: (tempValues.reduce((sum, val) => sum + val, 0) / tempValues.length).toFixed(2)
    }
    
    humidityStats.value = {
      min: Math.min(...humidityValues).toFixed(2),
      max: Math.max(...humidityValues).toFixed(2),
      avg: (humidityValues.reduce((sum, val) => sum + val, 0) / humidityValues.length).toFixed(2)
    }
  }
  
  initializeChart()
}

const initializeChart = () => {
  nextTick(() => {
    if (chartCanvas.value) {
      if (chart.value) {
        chart.value.destroy()
      }
      
      const ctx = chartCanvas.value.getContext('2d')
      
      // Format labels with proper error handling
      const labels = chartData.value.map(item => {
        try {
          if (item.timestamp instanceof Date && !isNaN(item.timestamp)) {
            return item.timestamp.toLocaleTimeString('en-US', {
              hour: '2-digit',
              minute: '2-digit',
              hour12: true
            })
          } else {
            // If timestamp is invalid, create a sequential time label
            const index = chartData.value.indexOf(item);
            const now = new Date();
            now.setMinutes(now.getMinutes() - (chartData.value.length - index - 1));
            return now.toLocaleTimeString('en-US', {
              hour: '2-digit',
              minute: '2-digit',
              hour12: true
            });
          }
        } catch (e) {
          console.error("Error formatting time:", e);
          return "--:--";
        }
      });
      
      chart.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: labels,
          datasets: [
            {
              label: 'Temperature (°C)',
              data: chartData.value.map(item => item.temperature),
              borderColor: '#ef4444', 
              backgroundColor: 'rgba(239, 68, 68, 0.15)', 
              borderWidth: 2.5,
              tension: 0.4,
              fill: true,
              pointRadius: 3,
              pointHoverRadius: 5,
              pointBackgroundColor: '#ffffff',
              pointBorderColor: '#ef4444',
              pointBorderWidth: 1.5,
              yAxisID: 'y-temperature'
            },
            {
              label: 'Humidity (%)',
              data: chartData.value.map(item => item.humidity),
              borderColor: '#3b82f6', 
              backgroundColor: 'rgba(59, 130, 246, 0.15)', 
              borderWidth: 2.5,
              tension: 0.4,
              fill: true,
              pointRadius: 3,
              pointHoverRadius: 5,
              pointBackgroundColor: '#ffffff',
              pointBorderColor: '#3b82f6',
              pointBorderWidth: 1.5,
              yAxisID: 'y-humidity'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: 'index',
            intersect: false,
          },
          animation: false,
          layout: {
            padding: {
              top: 10,
              left: 10,
              right: 10,
              bottom: 10
            }
          },
          scales: {
            'y-temperature': {
              type: 'linear',
              display: true,
              position: 'left',
              title: {
                display: true,
                text: 'Temperature (°C)',
                color: '#ef4444',
                font: {
                  size: 11,
                  weight: '600'
                },
                padding: {
                  bottom: 10
                }
              },
              beginAtZero: false,
              min: Math.max(0, Math.floor((parseFloat(tempStats.value.min) || 0) * 0.95)),
              max: Math.ceil((parseFloat(tempStats.value.max) || 50) * 1.05),
              ticks: {
                font: {
                  size: 10
                },
                color: '#ef4444',
                padding: 8
              },
              grid: {
                color: 'rgba(0, 0, 0, 0.04)',
                drawBorder: false
              }
            },
            'y-humidity': {
              type: 'linear',
              display: true,
              position: 'right',
              title: {
                display: true,
                text: 'Humidity (%)',
                color: '#3b82f6',
                font: {
                  size: 11,
                  weight: '600'
                },
                padding: {
                  bottom: 10
                }
              },
              beginAtZero: false,
              min: Math.max(0, Math.floor((parseFloat(humidityStats.value.min) || 0) * 0.95)),
              max: Math.min(100, Math.ceil((parseFloat(humidityStats.value.max) || 100) * 1.05)),
              ticks: {
                font: {
                  size: 10
                },
                color: '#3b82f6',
                padding: 8
              },
              grid: {
                drawOnChartArea: false,
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
                title: function(context) {
                  // Show full date and time in tooltip
                  const dataIndex = context[0].dataIndex;
                  const timestamp = chartData.value[dataIndex].timestamp;
                  
                  if (timestamp instanceof Date && !isNaN(timestamp)) {
                    return timestamp.toLocaleString('en-US', {
                      year: 'numeric',
                      month: 'short',
                      day: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    });
                  } else {
                    return "Time: N/A";
                  }
                },
                label: function(context) {
                  const label = context.dataset.label || '';
                  const value = context.raw !== null ? context.raw.toFixed(2) : '--';
                  return `${label}: ${value}`;
                }
              }
            }
          }
        }
      })
    }
  })
}

const updateChart = () => {
  // Check if chart exists and has data
  if (!chart.value || !chartData.value.length) {
    console.warn('Chart not available for update')
    return false // Return false instead of reinitializing
  }
  
  try {
    // Update chart labels and data
    chart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    
    chart.value.data.datasets[0].data = chartData.value.map(item => item.temperature)
    chart.value.data.datasets[1].data = chartData.value.map(item => item.humidity)
    
    // Safely update scales if they exist
    if (chart.value.options.scales && chart.value.options.scales['y-temperature']) {
      const tempMin = parseFloat(tempStats.value.min) || 0
      const tempMax = parseFloat(tempStats.value.max) || 50
      chart.value.options.scales['y-temperature'].min = Math.max(0, Math.floor(tempMin * 0.95))
      chart.value.options.scales['y-temperature'].max = Math.ceil(tempMax * 1.05)
    }
    
    if (chart.value.options.scales && chart.value.options.scales['y-humidity']) {
      const humidityMin = parseFloat(humidityStats.value.min) || 0
      const humidityMax = parseFloat(humidityStats.value.max) || 100
      chart.value.options.scales['y-humidity'].min = Math.max(0, Math.floor(humidityMin * 0.95))
      chart.value.options.scales['y-humidity'].max = Math.min(100, Math.ceil(humidityMax * 1.05))
    }
    
    // Update chart
    chart.value.update('none')
    return true
    
  } catch (error) {
    console.error('Error in updateChart:', error)
    // Don't reinitialize here - let the polling function handle it
    return false
  }
}

const getTemperatureTextClass = (temp) => {
  const temperature = parseFloat(temp)
  if (temperature >= 32) return 'text-red-600'
  if (temperature >= 28) return 'text-orange-600'
  if (temperature >= 24) return 'text-yellow-600'
  return 'text-green-600'
}

const getHumidityTextClass = (humidity) => {
  const humidityValue = parseFloat(humidity)
  if (humidityValue >= 70) return 'text-blue-600'
  if (humidityValue >= 60) return 'text-sky-600'
  if (humidityValue >= 40) return 'text-indigo-600'
  return 'text-purple-600'
}

const filters = ref({
  temperature: { min: '', max: '' },
  humidity: { min: '', max: '' }
})

const searchQuery = ref('')
const itemsPerPage = ref(20) 
const currentPage = ref(1)
const activeDropdown = ref(null)
// Default to sort by timestamp descending so the table shows newest -> oldest
const sortKey = ref('timestamp')
const sortDirection = ref('desc')
const activeFilters = ref({})

const filterFields = [
  { key: 'temperature', label: 'Temperature (°C)' },
  { key: 'humidity', label: 'Humidity (%)' }
]

const headers = [
  { key: 'id', label: 'ID' },
  { key: 'temperature', label: 'Temperature (°C)' },
  { key: 'humidity', label: 'Humidity (%)' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const exportFormats = ['csv', 'pdf']

// Updated computed properties for client-side operations on current page data
const filteredData = computed(() => {
  let result = [...tempHumidityData.value]

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
    
  // Treat null/undefined/empty as missing and push them to the end depending on sort direction
  if (aValue === '' || aValue === undefined || aValue === null) aValue = sortDirection.value === 'asc' ? -Infinity : Infinity
  if (bValue === '' || bValue === undefined || bValue === null) bValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortDirection.value === 'asc' 
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }
    return sortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
  })
})

const paginatedData = computed(() => {
  // Since we're fetching per page from server, just return the sorted data
  return sortedData.value
})

// Updated pagination functions
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchTempHumidityData(currentPage.value, itemsPerPage.value)
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchTempHumidityData(currentPage.value, itemsPerPage.value)
  }
}

const goToPage = (page) => {
  if (typeof page === 'number' && page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    fetchTempHumidityData(currentPage.value, itemsPerPage.value)
  }
}

const handleItemsPerPageChange = () => {
  currentPage.value = 1
  fetchTempHumidityData(currentPage.value, itemsPerPage.value)
}

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
  currentPage.value = 1
  fetchTempHumidityData(currentPage.value, itemsPerPage.value)
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

// Updated export function to fetch all data for export
const exportData = async (format) => {
  try {
    isLoading.value = true
    console.log(`📤 Starting ${format.toUpperCase()} export...`)
    
    // For exports, fetch ALL data without pagination
    let allData = []
    
    try {
      console.log('🚀 Fetching ALL Temperature & Humidity data for export...')
      const response = await api.get('/temperature-humidity/readings/all') // Adjust endpoint as needed
      
      console.log('📊 Backend response received:', {
        dataLength: response.data?.length,
        firstRecord: response.data?.[0]
      })
      
      if (response.data && Array.isArray(response.data)) {
        allData = response.data.map((reading, index) => {
          const timestamp = parseBackendTimestamp(reading.timestamp)
          
          return {
            id: reading.id || `export_${index}`,
            temperature: reading.temperature?.toFixed(2) || '--',
            humidity: reading.humidity?.toFixed(2) || '--',
            date: formatDateForDisplay(reading.timestamp),
            time: formatTimeForDisplay(reading.timestamp),
            rawTimestamp: timestamp,
            deviceId: reading.deviceId || 'esp32-2',
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
    const exportHeaders = headers.map(h => h.label)
    const exportRows = allData.map(row =>
      headers.map(header => {
        if (header.key === 'date') return formatDateForDisplay(row.rawTimestamp);
        if (header.key === 'time') return formatTimeForDisplay(row.rawTimestamp);
        return row[header.key] ?? ''
      })
    )

    const timestamp = new Date().toISOString().split('T')[0]

    if (format === 'csv') {
      let csvContent = exportHeaders.join(',') + '\n'
      exportRows.forEach(row => {
        csvContent += row.map(val => `"${val}"`).join(',') + '\n'
      })
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      saveAs(blob, `temperature_humidity_data_${timestamp}.csv`)
      window.showToast(`Exported ${allData.length} Temperature & Humidity records as CSV`, 'success')
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
      doc.text('Temperature & Humidity Data Report', pageWidth / 2, 20, { align: 'center' })
      
      doc.setFontSize(10)
      doc.setTextColor(100, 100, 100)
      doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, 27, { align: 'center' })
      doc.text(`Total Records: ${allData.length}`, pageWidth / 2, 33, { align: 'center' })
      
      // Statistics section - more compact
      doc.setFontSize(11)
      doc.setTextColor(30, 41, 59)
      doc.text('Current Readings & Statistics:', pageWidth / 2, 42, { align: 'center' })
      
      doc.setFontSize(9)
      doc.text(`Temperature: ${currentTempValue.value}°C | Min: ${tempStats.value.min}°C | Avg: ${tempStats.value.avg}°C | Max: ${tempStats.value.max}°C`, 
               pageWidth / 2, 48, { align: 'center' })
      doc.text(`Humidity: ${currentHumidityValue.value}% | Min: ${humidityStats.value.min}% | Avg: ${humidityStats.value.avg}% | Max: ${humidityStats.value.max}%`, 
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
        // Full width column distribution - adjust based on your actual headers
        columnStyles: {
          0: { cellWidth: tableWidth * 0.20 }, // Date
          1: { cellWidth: tableWidth * 0.15 }, // Time
          2: { cellWidth: tableWidth * 0.20 }, // Temperature
          3: { cellWidth: tableWidth * 0.20 }, // Humidity
          // 4: { cellWidth: tableWidth * 0.15 }, // Device
          // Add more columns if needed
        },
        pageBreak: 'auto',
        showHead: 'everyPage',
        tableLineWidth: 0.1,
        theme: 'grid',
        didDrawPage: function (data) {
          // Only add header on first page
          if (data.pageNumber === 1) {
            doc.setFontSize(16)
            doc.setTextColor(16, 185, 129)
            doc.text('Temperature & Humidity Data Report', pageWidth / 2, 20, { align: 'center' })
            
            doc.setFontSize(10)
            doc.setTextColor(100, 100, 100)
            doc.text(`Generated: ${new Date().toLocaleString()}`, pageWidth / 2, 27, { align: 'center' })
            doc.text(`Total Records: ${allData.length}`, pageWidth / 2, 33, { align: 'center' })
            
            // Statistics on first page only
            doc.setFontSize(11)
            doc.setTextColor(30, 41, 59)
            doc.text('Current Readings & Statistics:', pageWidth / 2, 42, { align: 'center' })
            
            doc.setFontSize(9)
            doc.text(`Temperature: ${currentTempValue.value}°C | Min: ${tempStats.value.min}°C | Avg: ${tempStats.value.avg}°C | Max: ${tempStats.value.max}°C`, 
                     pageWidth / 2, 48, { align: 'center' })
            doc.text(`Humidity: ${currentHumidityValue.value}% | Min: ${humidityStats.value.min}% | Avg: ${humidityStats.value.avg}% | Max: ${humidityStats.value.max}%`, 
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
      
      doc.save(`temperature_humidity_report_${timestamp}.pdf`)
      window.showToast(`Exported ${allData.length} Temperature & Humidity records as PDF`, 'success')
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
            children: row.map(cell =>
              new TableCell({
                children: [new Paragraph(cell ? cell.toString() : '')],
                width: { size: 20, type: 'pct' } // Equal width distribution
              })
            )
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
              text: 'Temperature & Humidity Data Report', 
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
      saveAs(buffer, `temperature_humidity_data_${timestamp}.docx`)
      window.showToast(`Exported ${allData.length} Temperature & Humidity records as DOCX`, 'success')
    }
    
  } catch (error) {
    console.error('❌ Export error:', error)
    window.showToast('Error exporting data. Please try again.', 'error')
  } finally {
    isLoading.value = false
    activeDropdown.value = null
  }
}

watch([searchQuery, activeFilters], () => {
  currentPage.value = 1
})

let unsubscribe = null

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  // Fetch initial data separately
  fetchLatestChartData() // For chart - latest 20 records
  fetchTempHumidityData(currentPage.value, itemsPerPage.value) // For table - current page
  
  // Then setup polling
  const cleanup = setupPollingListener()
  
  // Store cleanup function
  unsubscribe = cleanup
  
  const handleResize = () => {
    if (chart.value) {
      chart.value.resize()
    }
  }
  
  if (typeof ResizeObserver !== 'undefined') {
    const resizeObserver = new ResizeObserver(handleResize)
    if (chartCanvas.value) {
      resizeObserver.observe(chartCanvas.value.parentElement)
    }
  } else {
    window.addEventListener('resize', handleResize)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  
  if (chart.value) {
    chart.value.destroy()
  }
  
  // Clean up polling interval
  if (unsubscribe) {
    unsubscribe()
  }
  
  if (pollingInterval) {
    clearInterval(pollingInterval)
    pollingInterval = null
  }
  
  window.removeEventListener('resize', () => {})
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