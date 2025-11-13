<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-85px)] mt-1 md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">
      <!-- Gradient header for visual appeal -->
      <div class="bg-gradient-to-r from-green-50 to-white p-4 md:p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-sm md:text-xl font-semibold text-gray-800 mb-1">NPK Data Table</h1>
            <div class="flex items-center text-xs md:text-sm text-gray-500">
              <span class="text-green-600 font-medium">NPK Analysis</span>
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
            <p class="text-sm text-gray-500 mt-1">Choose the date range for the NPK data you want to print</p>
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

      <!-- Table and Graph Section - Flex container for side-by-side layout -->
      <div class="flex-1 overflow-y-auto md:overflow-hidden flex flex-col md:flex-row min-h-0">
        <!-- Live Graph Container - Three Separate Charts -->
        <div class="w-full md:w-1/3 md:max-w-sm lg:w-1/3 lg:max-w-md xl:max-w-lg border-r border-gray-200 bg-white p-4 overflow-y-auto flex-shrink-0">
          <div class="mb-3 flex items-center justify-between">
            <div>
              <h3 class="text-xs md:text-sm font-semibold text-gray-700">Live NPK Analysis</h3>
              <p class="text-[10px] md:text-xs text-gray-500">Real-time soil monitoring</p>
            </div>
            
            <!-- Minimalist Last Updated Status -->
            <div class="text-right">
              <div class="flex items-center gap-1.5 text-[10px] md:text-xs text-gray-500 mb-0.5">
                <Clock class="h-3 w-3" />
                <span>Last Updated</span>
                <div class="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></div>
              </div>
              <div class="text-xs md:text-sm font-mono font-semibold text-gray-800">
                {{ lastUpdated || '--:--:-- --' }}
              </div>
              <div class="text-[10px] md:text-xs text-gray-400">
                {{ currentDate }}
              </div>
            </div>
          </div>
          
          <!-- Nitrogen Graph -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
            <div class="p-3 border-b border-gray-100 bg-green-50 flex justify-between items-center">
              <div class="flex items-center gap-2">
                <div class="w-3 h-3 rounded-full bg-green-500"></div>
                <span class="text-xs md:text-sm font-semibold text-green-700">Nitrogen (mg/kg)</span>
              </div>
              <div class="text-[10px] md:text-xs text-gray-500">
                Current: <span class="font-bold text-green-600">{{ currentNitrogenValue }}</span>
              </div>
            </div>
            
            <div class="h-[180px] p-3 relative">
              <canvas ref="nitrogenChartCanvas" class="w-full h-full"></canvas>
            </div>
            
            <div class="border-t border-gray-100 p-3 bg-green-50/30">
              <div class="grid grid-cols-3 gap-2">
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Min</div>
                  <div class="text-sm font-semibold text-green-600">{{ nitrogenStats.min }}</div>
                </div>
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Avg</div>
                  <div class="text-sm font-semibold text-green-600">{{ nitrogenStats.avg }}</div>
                </div>
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Max</div>
                  <div class="text-sm font-semibold text-green-600">{{ nitrogenStats.max }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Phosphorus Graph -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
            <div class="p-3 border-b border-gray-100 bg-blue-50 flex justify-between items-center">
              <div class="flex items-center gap-2">
                <div class="w-3 h-3 rounded-full bg-blue-500"></div>
                <span class="text-xs md:text-sm font-semibold text-blue-700">Phosphorus (mg/kg)</span>
              </div>
              <div class="text-[10px] md:text-xs text-gray-500">
                Current: <span class="font-bold text-blue-600">{{ currentPhosphorusValue }}</span>
              </div>
            </div>
            
            <div class="h-[180px] p-3 relative">
              <canvas ref="phosphorusChartCanvas" class="w-full h-full"></canvas>
            </div>
            
            <div class="border-t border-gray-100 p-3 bg-blue-50/30">
              <div class="grid grid-cols-3 gap-2">
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Min</div>
                  <div class="text-sm font-semibold text-blue-600">{{ phosphorusStats.min }}</div>
                </div>
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Avg</div>
                  <div class="text-sm font-semibold text-blue-600">{{ phosphorusStats.avg }}</div>
                </div>
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Max</div>
                  <div class="text-sm font-semibold text-blue-600">{{ phosphorusStats.max }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Potassium Graph -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
            <div class="p-3 border-b border-gray-100 bg-purple-50 flex justify-between items-center">
              <div class="flex items-center gap-2">
                <div class="w-3 h-3 rounded-full bg-purple-500"></div>
                <span class="text-xs md:text-sm font-semibold text-purple-700">Potassium (mg/kg)</span>
              </div>
              <div class="text-[10px] md:text-xs text-gray-500">
                Current: <span class="font-bold text-purple-600">{{ currentPotassiumValue }}</span>
              </div>
            </div>
            
            <div class="h-[180px] p-3 relative">
              <canvas ref="potassiumChartCanvas" class="w-full h-full"></canvas>
            </div>
            
            <div class="border-t border-gray-100 p-3 bg-purple-50/30">
              <div class="grid grid-cols-3 gap-2">
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Min</div>
                  <div class="text-sm font-semibold text-purple-600">{{ potassiumStats.min }}</div>
                </div>
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Avg</div>
                  <div class="text-sm font-semibold text-purple-600">{{ potassiumStats.avg }}</div>
                </div>
                <div class="flex flex-col items-center p-2 bg-white rounded shadow-sm">
                  <div class="text-xs text-gray-500 mb-1">Max</div>
                  <div class="text-sm font-semibold text-purple-600">{{ potassiumStats.max }}</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Optimal Ranges section -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-3">Optimal NPK Ranges</h4>
            <div class="space-y-4">
              <div>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center">
                    <div class="w-2 h-2 rounded-full bg-green-500 mr-2"></div>
                    <span class="text-xs font-medium text-gray-700">Nitrogen</span>
                  </div>
                  <span class="text-xs md:text-sm text-green-600 font-medium">20-60 mg/kg</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-green-200 via-green-500 to-green-600 rounded-full" style="width: 70%"></div>
                </div>
              </div>
              
              <div>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center">
                    <div class="w-2 h-2 rounded-full bg-blue-500 mr-2"></div>
                    <span class="text-xs font-medium text-gray-700">Phosphorus</span>
                  </div>
                  <span class="text-xs text-blue-600 font-medium">50-150 mg/kg</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-blue-200 via-blue-500 to-blue-600 rounded-full" style="width: 60%"></div>
                </div>
              </div>
              
              <div>
                <div class="flex items-center justify-between mb-2">
                  <div class="flex items-center">
                    <div class="w-2 h-2 rounded-full bg-purple-500 mr-2"></div>
                    <span class="text-xs font-medium text-gray-700">Potassium</span>
                  </div>
                  <span class="text-xs text-purple-600 font-medium">80-160 mg/kg</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full bg-gradient-to-r from-purple-200 via-purple-500 to-purple-600 rounded-full" style="width: 65%"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Table Container - Larger width -->
        <div class="flex-1 md:w-full md:w-2/3 lg:w-2/3 flex flex-col">
          <!-- Loading overlay for pagination -->
          <div v-if="isFetching" class="absolute inset-0 bg-white bg-opacity-70 flex items-center justify-center z-20">
            <div class="bg-white rounded-lg shadow-lg p-4 flex items-center gap-3">
              <div class="animate-spin rounded-full h-6 w-6 border-b-2 border-green-500"></div>
              <span class="text-sm text-gray-600">Loading data...</span>
            </div>
          </div>

          <!-- Mobile View (shown on small screens) -->
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
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Nitrogen</div>
                    <div class="text-xs font-semibold" :class="getNitrogenTextClass(row.nitrogen)">{{ row.nitrogen }} mg/kg</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Phosphorus</div>
                    <div class="text-xs font-semibold" :class="getPhosphorusTextClass(row.phosphorus)">{{ row.phosphorus }} mg/kg</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Potassium</div>
                    <div class="text-xs font-semibold" :class="getPotassiumTextClass(row.potassium)">{{ row.potassium }} mg/kg</div>
                  </div>
                </div>
              </div>
              
              <div v-if="paginatedData.length === 0 && !isLoading && !isFetching" 
                  class="flex flex-col items-center justify-center py-8">
                <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
                <p class="text-gray-500 text-xs font-medium">No NPK data found</p>
                <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
              </div>
            </div>

            <!-- Desktop Table View (shown on medium screens and up) -->
            <div class="hidden sm:flex flex-1 flex-col min-h-0">
              <!-- Fixed Header with enhanced styling -->
              <div class="w-full border-b border-gray-200 sticky top-0 z-10 bg-gray-50">
                <table class="min-w-full">
                  <thead>
                    <tr>
                      <th class="w-[20%] py-2.5 px-3 text-left text-[9px] md:text-[15px] font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-green-600">Nitrogen</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="w-[20%] py-2.5 px-3 text-left text-[9px] md:text-[15px] font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-blue-600">Phosphorus</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="w-[20%] py-2.5 px-3 text-left text-[9px] md:text-[15px] font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-purple-600">Potassium</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="w-[15%] py-2.5 px-3 text-left text-[9px] md:text-[15px] font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-gray-600">Date</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">MMM DD, YYYY</div>
                      </th>
                      <th class="w-[15%] py-2.5 px-3 text-left text-[9px] md:text-[15px] font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-gray-600">Time</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">HH:MM:SS</div>
                      </th>
                    </tr>
                  </thead>
                </table>
              </div>
              
              <!-- Scrollable Body with enhanced styling -->
              <div class="flex-1 overflow-y-auto bg-white">
                <table class="min-w-full">
                  <tbody class="divide-y divide-gray-100">
                    <tr 
                      v-for="(row, index) in paginatedData" 
                      :key="index"
                      class="hover:bg-gray-50 transition-colors"
                    >
                      <td class="w-[20%] py-3 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-[15px] font-semibold" :class="getNitrogenTextClass(row.nitrogen)">
                          {{ row.nitrogen }}
                        </div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-[15px] font-semibold" :class="getPhosphorusTextClass(row.phosphorus)">
                          {{ row.phosphorus }}
                        </div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-[15px] font-semibold" :class="getPotassiumTextClass(row.potassium)">
                          {{ row.potassium }}
                        </div>
                      </td>
                      <td class="w-[15%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-[15px] font-medium text-gray-700">{{ row.date }}</div>
                      </td>
                      <td class="w-[15%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-[15px] font-medium text-gray-700">{{ row.time }}</div>
                      </td>
                    </tr>
                    
                    <tr v-if="paginatedData.length === 0 && !isLoading && !isFetching">
                      <td colspan="6" class="px-4 py-8 text-center">
                        <div class="flex flex-col items-center justify-center">
                          <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
                          <p class="text-gray-500 text-xs font-medium">No NPK data found</p>
                          <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
        </div>
      </div>

      <!-- Fixed Pagination Section with enhanced styling -->
      <div class="border-t border-gray-200 py-2 px-3 bg-gray-50">
        <div class="flex items-center justify-between">
          <div class="text-[10px] md:text-xs text-gray-600">
            Showing {{ showingText }}
          </div>
          <div class="flex items-center gap-1">
            <button 
              @click="prevPage"
              :disabled="currentPage === 1 || isFetching"
              class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600"
            >
              <ChevronLeft class="w-3.5 h-3.5" />
            </button>
            
            <div class="flex items-center gap-1">
              <button
                v-for="(page, index) in paginationNumbers"
                :key="index"
                @click="goToPage(page)"
                :disabled="page === '...' || isFetching"
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
              :disabled="currentPage >= totalPages || isFetching"
              class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600"
            >
              <ChevronRight class="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Loading Page Component -->
  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading NPK Data" 
    message="Please wait while we fetch the latest soil nutrient measurements"
  />
</template>
  
<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Search, Filter, Download, ChevronDown, ChevronRight, ChevronLeft, ArrowUpDown, FileText, FileSearch, Clock, Printer } from 'lucide-vue-next'
import LoadingPage from '../layout/LoadingPage.vue'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun } from 'docx'
import { saveAs } from 'file-saver'
import api from '../../api/index.js'
import Chart from 'chart.js/auto'
import html2canvas from 'html2canvas';

// Data state
const npkData = ref([])
const chartData = ref([]) // Separate data for charts
const isLoading = ref(true)
const isFetching = ref(false)
const isFetchingCharts = ref(false)
const chartsInitialized = ref(false)

// Chart references
const nitrogenChartCanvas = ref(null)
const phosphorusChartCanvas = ref(null)
const potassiumChartCanvas = ref(null)
const nitrogenChart = ref(null)
const phosphorusChart = ref(null)
const potassiumChart = ref(null)

// Current values and stats
const currentNitrogenValue = ref('--')
const currentPhosphorusValue = ref('--')
const currentPotassiumValue = ref('--')
const lastUpdated = ref('--')
const currentDate = ref('')
const nitrogenStats = ref({ min: '--', max: '--', avg: '--' })
const phosphorusStats = ref({ min: '--', max: '--', avg: '--' })
const potassiumStats = ref({ min: '--', max: '--', avg: '--' })

// Pagination state
const totalItems = ref(0)
const totalPagesFromAPI = ref(0)
const itemsPerPage = ref(20)
const currentPage = ref(1)

// Polling system
const pollingInterval = ref(null)
const pollingEnabled = ref(true)
const pollingIntervalTime = ref(10000) // 10 seconds
const isUpdating = ref(false)
const dataCache = ref(null)
let PRINT_CHART_DATA_LIMIT = 0;

// Table controls
const searchQuery = ref('')
const activeDropdown = ref(null)
const sortKey = ref('date')
const sortDirection = ref('desc')
const activeFilters = ref({})

const filters = ref({
  nitrogen: { min: '', max: '' },
  phosphorus: { min: '', max: '' },
  potassium: { min: '', max: '' }
})

const filterFields = [
  { key: 'nitrogen', label: 'Nitrogen (mg/kg)' },
  { key: 'phosphorus', label: 'Phosphorus (mg/kg)' },
  { key: 'potassium', label: 'Potassium (mg/kg)' }
]

const headers = [
  { key: 'nitrogen', label: 'Nitrogen (mg/kg)' },
  { key: 'phosphorus', label: 'Phosphorus (mg/kg)' },
  { key: 'potassium', label: 'Potassium (mg/kg)' },
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

const formatDateForInput = (date) => {
  return date.toISOString().split('T')[0];
};

// Separate function to fetch chart data (latest 20 records)
const fetchChartData = async () => {
  if (isFetchingCharts.value) return;
  
  isFetchingCharts.value = true;
  
  try {
    console.log('📊 Fetching latest data for charts...')
    
    // Use the recent endpoint to get latest data for charts
    const response = await api.get('/npk-data/recent', {
      params: {
        hours: 24, // Get last 24 hours
        limit: 20  // Get 20 latest records for charts
      }
    })
    
    const responseData = response.data

    if (responseData.data && Array.isArray(responseData.data)) {
      const processedChartData = responseData.data.map((reading, index) => {
        const timestamp = parseBackendTimestamp(reading.timestamp)
        
        return {
          id: reading.id || `chart_${index}`,
          nitrogen: reading.nitrogen?.toFixed(2) || '--',
          phosphorus: reading.phosphorus?.toFixed(2) || '--',
          potassium: reading.potassium?.toFixed(2) || '--',
          date: formatDateForDisplay(reading.timestamp),
          time: formatTimeForDisplay(reading.timestamp),
          rawTimestamp: timestamp,
          deviceId: reading.device_id || 'esp32-1',
          soilPh: reading.soilPh?.toFixed(2) || '--',
          timestampMs: timestamp.getTime()
        }
      })

      // Update chart data with latest 20 records
      updateChartsWithData(processedChartData)
      
      console.log(`✅ Chart data loaded: ${processedChartData.length} latest records`)
    }
    
  } catch (error) {
    console.error('❌ Chart data fetch error:', error.message)
    // Fallback: use current page data for charts if chart-specific fetch fails
    if (npkData.value.length > 0) {
      updateChartsWithData(npkData.value.slice(0, 20))
    }
  } finally {
    isFetchingCharts.value = false
  }
}

// Paginated data fetching for table
const fetchPageData = async (page = 1, limit = 20) => {
  if (isFetching.value) return;
  
  isFetching.value = true;
  
  try {
    console.log(`📄 Fetching page ${page} with ${limit} items`)
    
    const response = await api.get('/npk-data', {
      params: {
        page: page,
        limit: limit
      }
    })
    
    const responseData = response.data

    if (responseData.data && Array.isArray(responseData.data)) {
      const processedData = responseData.data.map((reading, index) => {
        const timestamp = parseBackendTimestamp(reading.timestamp)
        
        return {
          id: reading.id || `esp32-1_${index}`,
          nitrogen: reading.nitrogen?.toFixed(2) || '--',
          phosphorus: reading.phosphorus?.toFixed(2) || '--',
          potassium: reading.potassium?.toFixed(2) || '--',
          date: formatDateForDisplay(reading.timestamp),
          time: formatTimeForDisplay(reading.timestamp),
          rawTimestamp: timestamp,
          deviceId: reading.device_id || 'esp32-1',
          soilPh: reading.soilPh?.toFixed(2) || '--',
          timestampMs: timestamp.getTime()
        }
      })

      // Update table data only
      npkData.value = processedData
      dataCache.value = processedData
      
      // Update pagination info from API response
      if (responseData.pagination) {
        totalItems.value = responseData.pagination.totalItems
        totalPagesFromAPI.value = responseData.pagination.totalPages
        itemsPerPage.value = responseData.pagination.itemsPerPage
        currentPage.value = responseData.pagination.currentPage
      }
      
      console.log(`✅ Page ${page} loaded: ${processedData.length} records`)
    }
    
  } catch (error) {
    console.error('❌ Page fetch error:', error.message)
    // Fallback to cached data if available
    npkData.value = dataCache.value || []
    window.showToast('Failed to load data. Please try again.', 'error')
  } finally {
    isFetching.value = false
  }
}

const updateChartsWithData = (data) => {
  const validChartData = data
    .filter(reading => reading.nitrogen !== '--' && reading.phosphorus !== '--' && reading.potassium !== '--')
    .map(reading => ({
      timestamp: reading.rawTimestamp,
      nitrogen: Number(reading.nitrogen),
      phosphorus: Number(reading.phosphorus),
      potassium: Number(reading.potassium)
    }))
    .sort((a, b) => a.timestamp - b.timestamp) // Sort ascending for proper timeline
    .slice(-20) // Take the last 20 items (most recent)
  
  chartData.value = validChartData
  initializeChartData(validChartData)
  PRINT_CHART_DATA_LIMIT = data.length
}

// Real-time functions (for charts and first page)
const realTime = async () => {
  if (isUpdating.value || isFetching.value || isFetchingCharts.value) return;
  
  isUpdating.value = true;
  
  try {
    console.log('🔄 Polling for new NPK data...')
    
    // Fetch latest data for charts
    await fetchChartData()
    
    // If we're on the first page, also update the table
    if (currentPage.value === 1) {
      await fetchPageData(1, itemsPerPage.value)
    }
    
  } catch (error) {
    console.error("❌ Error fetching NPK data:", error)
  } finally {
    isUpdating.value = false;
  }
}

const startPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
  
  pollingInterval.value = setInterval(async () => {
    if (pollingEnabled.value && !isUpdating.value) {
      await realTime()
    }
  }, pollingIntervalTime.value)
}

const stopPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
}

// Chart functions (updated to use chartData)
const initializeChartData = (data) => {
  const validChartData = data
    .filter(item => {
      const validN = item.nitrogen !== '--' && !isNaN(Number(item.nitrogen)) && Number(item.nitrogen) > 0
      const validP = item.phosphorus !== '--' && !isNaN(Number(item.phosphorus)) && Number(item.phosphorus) > 0
      const validK = item.potassium !== '--' && !isNaN(Number(item.potassium)) && Number(item.potassium) > 0
      return validN && validP && validK
    })
    .map(item => ({
      timestamp: item.timestamp || new Date(),
      nitrogen: Number(item.nitrogen),
      phosphorus: Number(item.phosphorus),
      potassium: Number(item.potassium)
    }))
    .sort((a, b) => a.timestamp - b.timestamp) // Ascending for proper timeline
    .slice(-20) // Take last 20 (most recent)

  console.log(`📈 Chart data: ${validChartData.length} valid entries`)

  chartData.value = validChartData

  if (validChartData.length > 0) {
    const latestReading = validChartData[validChartData.length - 1] // Last item is most recent
    currentNitrogenValue.value = latestReading.nitrogen.toFixed(2)
    currentPhosphorusValue.value = latestReading.phosphorus.toFixed(2)
    currentPotassiumValue.value = latestReading.potassium.toFixed(2)
    
    const formattedTime = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    lastUpdated.value = formattedTime
    
    const nitrogenValues = validChartData.map(item => item.nitrogen)
    const phosphorusValues = validChartData.map(item => item.phosphorus)
    const potassiumValues = validChartData.map(item => item.potassium)
    
    nitrogenStats.value = {
      min: Math.min(...nitrogenValues).toFixed(2),
      max: Math.max(...nitrogenValues).toFixed(2),
      avg: (nitrogenValues.reduce((sum, val) => sum + val, 0) / nitrogenValues.length).toFixed(2)
    }
    
    phosphorusStats.value = {
      min: Math.min(...phosphorusValues).toFixed(2),
      max: Math.max(...phosphorusValues).toFixed(2),
      avg: (phosphorusValues.reduce((sum, val) => sum + val, 0) / phosphorusValues.length).toFixed(2)
    }
    
    potassiumStats.value = {
      min: Math.min(...potassiumValues).toFixed(2),
      max: Math.max(...potassiumValues).toFixed(2),
      avg: (potassiumValues.reduce((sum, val) => sum + val, 0) / potassiumValues.length).toFixed(2)
    }
  } else {
    currentNitrogenValue.value = '--'
    currentPhosphorusValue.value = '--'
    currentPotassiumValue.value = '--'
    lastUpdated.value = '--'
    
    nitrogenStats.value = { min: '--', max: '--', avg: '--' }
    phosphorusStats.value = { min: '--', max: '--', avg: '--' }
    potassiumStats.value = { min: '--', max: '--', avg: '--' }
  }
  
  initializeChart()
}

const initializeChart = () => {
  nextTick(() => {
    setTimeout(() => {
      try {
        initializeNitrogenChart();
        initializePhosphorusChart();
        initializePotassiumChart();
        chartsInitialized.value = true;
      } catch (error) {
        console.error('Error initializing charts:', error)
      }
    }, 300);
  });
}

// Chart initialization functions
const initializeNitrogenChart = () => {
  if (!nitrogenChartCanvas.value) {
    console.warn('Nitrogen chart canvas not available');
    return;
  }
  
  const container = nitrogenChartCanvas.value.parentElement;
  if (!container) {
    console.warn('Nitrogen chart container not available');
    return;
  }
  
  if (nitrogenChart.value) {
    try {
      nitrogenChart.value.destroy();
    } catch (error) {
      console.warn('Error destroying nitrogen chart:', error);
    }
  }
  
  try {
    const ctx = nitrogenChartCanvas.value.getContext('2d');
    nitrogenChartCanvas.value.width = container.clientWidth;
    nitrogenChartCanvas.value.height = container.clientHeight;
    
    const minVal = nitrogenStats.value.min !== '--' ? parseFloat(nitrogenStats.value.min) : 0;
    const maxVal = nitrogenStats.value.max !== '--' ? parseFloat(nitrogenStats.value.max) : 100;
    
    nitrogenChart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.value.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          });
        }),
        datasets: [{
          label: 'Nitrogen (mg/kg)',
          data: chartData.value.map(item => item.nitrogen),
          borderColor: '#22c55e',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#22c55e',
          pointBorderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        animation: false,
        scales: {
          y: {
            beginAtZero: false,
            min: Math.max(0, (minVal || 0) * 0.9),
            max: (maxVal || 100) * 1.1,
            ticks: {
              font: { size: 11 },
              color: '#22c55e',
              padding: 8
            },
            grid: {
              color: 'rgba(34, 197, 94, 0.1)',
              drawBorder: false
            }
          },
          x: {
            ticks: {
              font: { size: 10 },
              maxRotation: 45,
              color: '#64748b'
            },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            titleColor: '#22c55e',
            bodyColor: '#22c55e',
            borderColor: '#22c55e',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
            titleFont: { size: 12, weight: '600' },
            bodyFont: { size: 12 },
            callbacks: {
              label: function(context) {
                return `${context.raw.toFixed(2)} mg/kg`;
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error initializing nitrogen chart:', error);
  }
}

const initializePhosphorusChart = () => {
  if (!phosphorusChartCanvas.value) {
    console.warn('Phosphorus chart canvas not available');
    return;
  }
  
  const container = phosphorusChartCanvas.value.parentElement;
  if (!container) {
    console.warn('Phosphorus chart container not available');
    return;
  }
  
  if (phosphorusChart.value) {
    try {
      phosphorusChart.value.destroy();
    } catch (error) {
      console.warn('Error destroying phosphorus chart:', error);
    }
  }
  
  try {
    const ctx = phosphorusChartCanvas.value.getContext('2d');
    phosphorusChartCanvas.value.width = container.clientWidth;
    phosphorusChartCanvas.value.height = container.clientHeight;
    
    const minVal = phosphorusStats.value.min !== '--' ? parseFloat(phosphorusStats.value.min) : 0;
    const maxVal = phosphorusStats.value.max !== '--' ? parseFloat(phosphorusStats.value.max) : 100;
    
    phosphorusChart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.value.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          });
        }),
        datasets: [{
          label: 'Phosphorus (mg/kg)',
          data: chartData.value.map(item => item.phosphorus),
          borderColor: '#3b82f6',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#3b82f6',
          pointBorderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        animation: false,
        scales: {
          y: {
            beginAtZero: false,
            min: Math.max(0, (minVal || 0) * 0.9),
            max: (maxVal || 100) * 1.1,
            ticks: {
              font: { size: 11 },
              color: '#3b82f6',
              padding: 8
            },
            grid: {
              color: 'rgba(59, 130, 246, 0.1)',
              drawBorder: false
            }
          },
          x: {
            ticks: {
              font: { size: 10 },
              maxRotation: 45,
              color: '#64748b'
            },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            titleColor: '#3b82f6',
            bodyColor: '#3b82f6',
            borderColor: '#3b82f6',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
            titleFont: { size: 12, weight: '600' },
            bodyFont: { size: 12 },
            callbacks: {
              label: function(context) {
                return `${context.raw.toFixed(2)} mg/kg`;
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error initializing phosphorus chart:', error);
  }
}

const initializePotassiumChart = () => {
  if (!potassiumChartCanvas.value) {
    console.warn('Potassium chart canvas not available');
    return;
  }
  
  const container = potassiumChartCanvas.value.parentElement;
  if (!container) {
    console.warn('Potassium chart container not available');
    return;
  }
  
  if (potassiumChart.value) {
    try {
      potassiumChart.value.destroy();
    } catch (error) {
      console.warn('Error destroying potassium chart:', error);
    }
  }
  
  try {
    const ctx = potassiumChartCanvas.value.getContext('2d');
    potassiumChartCanvas.value.width = container.clientWidth;
    potassiumChartCanvas.value.height = container.clientHeight;
    
    const minVal = potassiumStats.value.min !== '--' ? parseFloat(potassiumStats.value.min) : 0;
    const maxVal = potassiumStats.value.max !== '--' ? parseFloat(potassiumStats.value.max) : 100;
    
    potassiumChart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.value.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          });
        }),
        datasets: [{
          label: 'Potassium (mg/kg)',
          data: chartData.value.map(item => item.potassium),
          borderColor: '#a855f7',
          backgroundColor: 'rgba(168, 85, 247, 0.1)',
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 4,
          pointHoverRadius: 6,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#a855f7',
          pointBorderWidth: 2,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
          mode: 'index',
          intersect: false,
        },
        animation: false,
        scales: {
          y: {
            beginAtZero: false,
            min: Math.max(0, (minVal || 0) * 0.9),
            max: (maxVal || 100) * 1.1,
            ticks: {
              font: { size: 11 },
              color: '#a855f7',
              padding: 8
            },
            grid: {
              color: 'rgba(168, 85, 247, 0.1)',
              drawBorder: false
            }
          },
          x: {
            ticks: {
              font: { size: 10 },
              maxRotation: 45,
              color: '#64748b'
            },
            grid: { display: false }
          }
        },
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: 'rgba(255, 255, 255, 0.95)',
            titleColor: '#a855f7',
            bodyColor: '#a855f7',
            borderColor: '#a855f7',
            borderWidth: 1,
            padding: 12,
            cornerRadius: 8,
            displayColors: false,
            titleFont: { size: 12, weight: '600' },
            bodyFont: { size: 12 },
            callbacks: {
              label: function(context) {
                return `${context.raw.toFixed(2)} mg/kg`;
              }
            }
          }
        }
      }
    });
  } catch (error) {
    console.error('Error initializing potassium chart:', error);
  }
}

// Chart update functions
const updateNitrogenChart = () => {
  if (!nitrogenChart.value || !chartData.value || chartData.value.length === 0) {
    return;
  }
  
  try {
    nitrogenChart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    
    nitrogenChart.value.data.datasets[0].data = chartData.value.map(item => item.nitrogen)
    
    const minVal = nitrogenStats.value.min !== '--' ? parseFloat(nitrogenStats.value.min) : 0;
    const maxVal = nitrogenStats.value.max !== '--' ? parseFloat(nitrogenStats.value.max) : 100;
    
    if (!isNaN(minVal) && !isNaN(maxVal)) {
      nitrogenChart.value.options.scales.y.min = Math.max(0, minVal * 0.9)
      nitrogenChart.value.options.scales.y.max = maxVal * 1.1
    }
    
    nitrogenChart.value.update('none')
  } catch (error) {
    console.error('Error updating nitrogen chart:', error)
  }
}

const updatePhosphorusChart = () => {
  if (!phosphorusChart.value || !chartData.value || chartData.value.length === 0) {
    return;
  }
  
  try {
    phosphorusChart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    
    phosphorusChart.value.data.datasets[0].data = chartData.value.map(item => item.phosphorus)
    
    const minVal = phosphorusStats.value.min !== '--' ? parseFloat(phosphorusStats.value.min) : 0;
    const maxVal = phosphorusStats.value.max !== '--' ? parseFloat(phosphorusStats.value.max) : 100;
    
    if (!isNaN(minVal) && !isNaN(maxVal)) {
      phosphorusChart.value.options.scales.y.min = Math.max(0, minVal * 0.9)
      phosphorusChart.value.options.scales.y.max = maxVal * 1.1
    }
    
    phosphorusChart.value.update('none')
  } catch (error) {
    console.error('Error updating phosphorus chart:', error)
  }
}

const updatePotassiumChart = () => {
  if (!potassiumChart.value || !chartData.value || chartData.value.length === 0) {
    return;
  }
  
  try {
    potassiumChart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    
    potassiumChart.value.data.datasets[0].data = chartData.value.map(item => item.potassium)
    
    const minVal = potassiumStats.value.min !== '--' ? parseFloat(potassiumStats.value.min) : 0;
    const maxVal = potassiumStats.value.max !== '--' ? parseFloat(potassiumStats.value.max) : 100;
    
    if (!isNaN(minVal) && !isNaN(maxVal)) {
      potassiumChart.value.options.scales.y.min = Math.max(0, minVal * 0.9)
      potassiumChart.value.options.scales.y.max = maxVal * 1.1
    }
    
    potassiumChart.value.update('none')
  } catch (error) {
    console.error('Error updating potassium chart:', error)
  }
}

const updateChart = () => {
  updateNitrogenChart()
  updatePhosphorusChart()
  updatePotassiumChart()
}

const debounce = (func, wait) => {
  let timeout
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout)
      func(...args)
    }
    clearTimeout(timeout)
    timeout = setTimeout(later, wait)
  }
}

const debouncedUpdateChart = debounce(updateChart, 300)

// Resize handler function
const handleResize = () => {
  if (nitrogenChart.value && nitrogenChartCanvas.value) {
    const container = nitrogenChartCanvas.value.parentElement;
    if (container) {
      nitrogenChartCanvas.value.width = container.clientWidth;
      nitrogenChartCanvas.value.height = container.clientHeight;
      try {
        nitrogenChart.value.resize();
      } catch (error) {
        console.warn('Error resizing nitrogen chart:', error);
      }
    }
  }
  
  if (phosphorusChart.value && phosphorusChartCanvas.value) {
    const container = phosphorusChartCanvas.value.parentElement;
    if (container) {
      phosphorusChartCanvas.value.width = container.clientWidth;
      phosphorusChartCanvas.value.height = container.clientHeight;
      try {
        phosphorusChart.value.resize();
      } catch (error) {
        console.warn('Error resizing phosphorus chart:', error);
      }
    }
  }
  
  if (potassiumChart.value && potassiumChartCanvas.value) {
    const container = potassiumChartCanvas.value.parentElement;
    if (container) {
      potassiumChartCanvas.value.width = container.clientWidth;
      potassiumChartCanvas.value.height = container.clientHeight;
      try {
        potassiumChart.value.resize();
      } catch (error) {
        console.warn('Error resizing potassium chart:', error);
      }
    }
  }
}

// Pagination functions
const nextPage = async () => {
  if (currentPage.value < totalPages.value && !isFetching.value) {
    const nextPageNum = currentPage.value + 1
    await fetchPageData(nextPageNum, itemsPerPage.value)
  }
}

const prevPage = async () => {
  if (currentPage.value > 1 && !isFetching.value) {
    const prevPageNum = currentPage.value - 1
    await fetchPageData(prevPageNum, itemsPerPage.value)
  }
}

const goToPage = async (page) => {
  if (typeof page === 'number' && page !== currentPage.value && !isFetching.value) {
    await fetchPageData(page, itemsPerPage.value)
  }
}

// Computed properties
const showingText = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value + 1
  const end = Math.min(currentPage.value * itemsPerPage.value, totalItems.value)
  return `Showing ${start} - ${end} of ${totalItems.value}`
})

const paginationNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 1) return [1]
  
  if (current === 1) {
    return [1, '..', total]
  } else if (current === total) {
    return [1, '..', total]
  } else {
    return [current, '...', total]
  }
})

const totalPages = computed(() => {
  return totalPagesFromAPI.value || Math.ceil(totalItems.value / itemsPerPage.value)
})

const filteredData = computed(() => {
  let result = [...npkData.value]

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

// UI methods
const getNitrogenTextClass = (nitrogen) => {
  const nitrogenValue = parseFloat(nitrogen)
  if (nitrogenValue >= 50) return 'text-green-600'
  if (nitrogenValue >= 30) return 'text-green-500'
  if (nitrogenValue >= 20) return 'text-yellow-600'
  return 'text-red-600'
}

const getPhosphorusTextClass = (phosphorus) => {
  const phosphorusValue = parseFloat(phosphorus)
  if (phosphorusValue >= 120) return 'text-blue-600'
  if (phosphorusValue >= 80) return 'text-blue-500'
  if (phosphorusValue >= 50) return 'text-sky-600'
  return 'text-red-600'
}

const getPotassiumTextClass = (potassium) => {
  const potassiumValue = parseFloat(potassium)
  if (potassiumValue >= 140) return 'text-purple-600'
  if (potassiumValue >= 100) return 'text-purple-500'
  if (potassiumValue >= 80) return 'text-indigo-600'
  return 'text-red-600'
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
    start: formatDateForInput(startDate),
    end: formatDateForInput(endDate)
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
  
  if (startDate > endDate) {
    printDateError.value = 'Start date cannot be after end date';
    return;
  }

  try {
    isLoading.value = true;
    showPrintModal.value = false;
    
    // Fetch data for the selected date range using the backend range endpoint
    const response = await api.get('/npk-data/range', {
      params: {
        from_date: printDateRange.value.start,
        to_date: printDateRange.value.end
      }
    });
    
    const data = response.data.data || [];
    
    // Process the data for printing
    const npkRows = data.map((reading, index) => {
      try {
        const timestamp = parseBackendTimestamp(reading.timestamp);
        
        return {
          id: reading.id || `print_${index}`,
          date: formatDateForDisplay(reading.timestamp),
          time: formatTimeForDisplay(reading.timestamp),
          device: reading.device_id || 'esp32-1',
          nitrogen: reading.nitrogen?.toFixed(2) || '--',
          phosphorus: reading.phosphorus?.toFixed(2) || '--',
          potassium: reading.potassium?.toFixed(2) || '--',
          rawTimestamp: timestamp
        };
      } catch (error) {
        console.error('Error processing reading for print:', reading, error);
        return null;
      }
    }).filter(reading => reading !== null);

    if (npkRows.length === 0) {
      window.showToast('No data found for the selected date range', 'warning');
      isLoading.value = false;
      return;
    }

    // Sort by timestamp (newest first)
    npkRows.sort((a, b) => b.rawTimestamp - a.rawTimestamp);

    // Generate print content
    await generatePrintContent(npkRows, printDateRange.value);
    
  } catch (error) {
    console.error('Error fetching data for print:', error);
    window.showToast('Error fetching data for printing', 'error');
  } finally {
    isLoading.value = false;
  }
}

const generatePrintContent = async (npkRows, dateRange) => {
  const now = new Date();
  const formattedDate = now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  });

  // Prepare chart data
  const printChartData = npkRows
    .filter(item => item.nitrogen !== '--' && item.phosphorus !== '--' && item.potassium !== '--')
    .map(item => ({
      timestamp: item.rawTimestamp, 
      nitrogen: Number(item.nitrogen),
      phosphorus: Number(item.phosphorus),
      potassium: Number(item.potassium)
    }))
    .sort((a, b) => a.timestamp - b.timestamp);

  // Calculate statistics with safe defaults
  const nitrogenValues = printChartData.map(item => item.nitrogen);
  const phosphorusValues = printChartData.map(item => item.phosphorus);
  const potassiumValues = printChartData.map(item => item.potassium);
  
  const nitrogenStats = {
    min: nitrogenValues.length > 0 ? Math.min(...nitrogenValues) : 0,
    max: nitrogenValues.length > 0 ? Math.max(...nitrogenValues) : 0,
    avg: nitrogenValues.length > 0 ? nitrogenValues.reduce((sum, val) => sum + val, 0) / nitrogenValues.length : 0
  };
  
  const phosphorusStats = {
    min: phosphorusValues.length > 0 ? Math.min(...phosphorusValues) : 0,
    max: phosphorusValues.length > 0 ? Math.max(...phosphorusValues) : 0,
    avg: phosphorusValues.length > 0 ? phosphorusValues.reduce((sum, val) => sum + val, 0) / phosphorusValues.length : 0
  };
  
  const potassiumStats = {
    min: potassiumValues.length > 0 ? Math.min(...potassiumValues) : 0,
    max: potassiumValues.length > 0 ? Math.max(...potassiumValues) : 0,
    avg: potassiumValues.length > 0 ? potassiumValues.reduce((sum, val) => sum + val, 0) / potassiumValues.length : 0
  };

  let chartImage = '';
  
  // Generate chart if we have data
  if (printChartData.length > 0) {
    chartImage = await generateChartImage(printChartData, nitrogenStats, phosphorusStats, potassiumStats);
  }

  // Generate the print HTML
  generatePrintHTML(chartImage, npkRows, formattedDate, now, printChartData.length, nitrogenStats, phosphorusStats, potassiumStats, dateRange);
}

const generateChartImage = async (chartData, nitrogenStats, phosphorusStats, potassiumStats) => {
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
          datasets: [
            {
              label: 'Nitrogen',
              data: chartData.map(item => item.nitrogen),
              borderColor: '#10b981',
              backgroundColor: 'rgba(16, 185, 129, 0.1)',
              borderWidth: 2,
              tension: 0.4,
              fill: true
            },
            {
              label: 'Phosphorus',
              data: chartData.map(item => item.phosphorus),
              borderColor: '#3b82f6',
              backgroundColor: 'rgba(59, 130, 246, 0.1)',
              borderWidth: 2,
              tension: 0.4,
              fill: true
            },
            {
              label: 'Potassium',
              data: chartData.map(item => item.potassium),
              borderColor: '#8b5cf6',
              backgroundColor: 'rgba(139, 92, 246, 0.1)',
              borderWidth: 2,
              tension: 0.4,
              fill: true
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
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: 'NPK Levels (mg/kg)',
                font: { size: 14, weight: '600' }
              },
              ticks: {
                font: { size: 12 }
              }
            },
            x: {
              ticks: {
                font: { size: 10 },
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

const generatePrintHTML = (chartImage, npkRows, formattedDate, now, chartRecordCount, nitrogenStats, phosphorusStats, potassiumStats, dateRange) => {
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>NPK Analysis Data - ${dateRange.start} to ${dateRange.end}</title>
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
          color: #10b981;
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
          color: #10b981;
          font-weight: 600;
          background-color: #f0fdf4;
          padding: 8px;
          border-radius: 6px;
          border: 1px solid #bbf7d0;
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
        .nitrogen { color: #10b981; font-weight: 500; }
        .phosphorus { color: #3b82f6; font-weight: 500; }
        .potassium { color: #8b5cf6; font-weight: 500; }
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
        }
        .nitrogen-stat { color: #10b981; }
        .phosphorus-stat { color: #3b82f6; }
        .potassium-stat { color: #8b5cf6; }
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
        <h1>NPK Analysis Report</h1>
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
          <span class="summary-value">${npkRows.length}</span>
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
      
      ${chartImage ? `
        <div class="section-header">NPK Trend Analysis</div>
        <div class="chart-title">NPK Levels Over Time</div>
        <div class="chart-info">Showing ${chartRecordCount} data points from selected date range</div>
        <img src="${chartImage}" class="chart-image" alt="NPK Chart" />
        
        <div class="stats-summary">
          <div class="stat-item">
            <h4 class="nitrogen-stat">Nitrogen Statistics</h4>
            <div class="stat-values">
              Min: ${nitrogenStats.min.toFixed(2)} mg/kg<br>
              Avg: ${nitrogenStats.avg.toFixed(2)} mg/kg<br>
              Max: ${nitrogenStats.max.toFixed(2)} mg/kg
            </div>
          </div>
          <div class="stat-item">
            <h4 class="phosphorus-stat">Phosphorus Statistics</h4>
            <div class="stat-values">
              Min: ${phosphorusStats.min.toFixed(2)} mg/kg<br>
              Avg: ${phosphorusStats.avg.toFixed(2)} mg/kg<br>
              Max: ${phosphorusStats.max.toFixed(2)} mg/kg
            </div>
          </div>
          <div class="stat-item">
            <h4 class="potassium-stat">Potassium Statistics</h4>
            <div class="stat-values">
              Min: ${potassiumStats.min.toFixed(2)} mg/kg<br>
              Avg: ${potassiumStats.avg.toFixed(2)} mg/kg<br>
              Max: ${potassiumStats.max.toFixed(2)} mg/kg
            </div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">No chart data available for the selected date range</p>'}
      
      <div class="section-header">Detailed NPK Sensor Readings</div>
      <table>
        <thead>
          <tr>
            <th style="width: 10%">ID</th>
            <th style="width: 15%">Date</th>
            <th style="width: 12%">Time</th>
            <th style="width: 10%">Device</th>
            <th style="width: 15%">Nitrogen (mg/kg)</th>
            <th style="width: 15%">Phosphorus (mg/kg)</th>
            <th style="width: 15%">Potassium (mg/kg)</th>
          </tr>
        </thead>
        <tbody>
          ${npkRows.map(row => `
            <tr>
              <td>${row.id}</td>
              <td>${row.date}</td>
              <td>${row.time}</td>
              <td>${row.device}</td>
              <td><span class="nitrogen">${row.nitrogen}</span></td>
              <td><span class="phosphorus">${row.phosphorus}</span></td>
              <td><span class="potassium">${row.potassium}</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by NPK Analysis System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
      </div>
      
      <div class="no-print" style="text-align: center; margin-top: 20px;">
        <button onclick="window.print()" style="padding: 10px 20px; background: #10b981; color: white; border: none; border-radius: 5px; cursor: pointer;">
          Print Report
        </button>
        <button onclick="window.close()" style="padding: 10px 20px; background: #666; color: white; border: none; border-radius: 5px; cursor: pointer; margin-left: 10px;">
          Close
        </button>
      </div>

      <script>
        // Auto-print when the window loads
        window.onload = function() {
          setTimeout(() => {
            window.print();
          }, 500);
        };
      <\/script>
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

// Export function (simplified version)
const exportData = async (format) => {
  try {
    isLoading.value = true
    console.log(`📤 Starting ${format.toUpperCase()} export...`)
    
    // For exports, fetch all data without pagination
    let allData = []
    
    try {
      console.log('🚀 Fetching all NPK data for export...')
      const response = await api.get('/npk-data/all')
      
      if (response.data && Array.isArray(response.data)) {
        allData = response.data.map((reading, index) => {
          const timestamp = parseBackendTimestamp(reading.timestamp)
          
          return {
            id: reading.id || `export_${index}`,
            nitrogen: reading.nitrogen?.toFixed(2) || '--',
            phosphorus: reading.phosphorus?.toFixed(2) || '--',
            potassium: reading.potassium?.toFixed(2) || '--',
            date: formatDateForDisplay(reading.timestamp),
            time: formatTimeForDisplay(reading.timestamp),
            rawTimestamp: timestamp,
            deviceId: reading.device_id || 'esp32-1',
            soilPh: reading.soilPh?.toFixed(2) || '--',
            timestampMs: timestamp.getTime()
          }
        })
        
        // Sort by timestamp (newest first)
        allData.sort((a, b) => b.timestampMs - a.timestampMs)
        
        console.log(`✅ Fetched ${allData.length} records for export`)
      }
    } catch (error) {
      console.error('❌ Error fetching all data for export:', error)
      
      // Fallback: If /all endpoint doesn't exist, fetch all pages sequentially
      console.log('🔄 Trying fallback method: fetching all pages...')
      allData = await fetchAllPages()
    }

    if (!allData.length) {
      window.showToast('No data available for export', 'warning')
      isLoading.value = false
      return
    }

    const exportHeaders = [
      'ID',
      'Date',
      'Time', 
      'Device',
      'Nitrogen (mg/kg)',
      'Phosphorus (mg/kg)',
      'Potassium (mg/kg)',
      'Soil pH'
    ]

    const exportRows = allData.map(row => [
      row.id,
      row.date,
      row.time,
      row.deviceId,
      row.nitrogen,
      row.phosphorus,
      row.potassium,
      row.soilPh
    ])

    const timestamp = new Date().toISOString().split('T')[0]

    if (format === 'csv') {
      let csvContent = exportHeaders.join(',') + '\n'
      exportRows.forEach(row => {
        csvContent += row.map(val => `"${val}"`).join(',') + '\n'
      })
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      saveAs(blob, `npk_data_${timestamp}.csv`)
      window.showToast(`Exported ${allData.length} NPK records as CSV`, 'success')
      
    } else if (format === 'pdf') {
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      })
      
      const pageWidth = doc.internal.pageSize.getWidth()
      const margin = 10
      const tableWidth = pageWidth - (margin * 2)
      
      // Title
      doc.setFontSize(18)
      doc.setTextColor(16, 163, 74) // green-600
      doc.text('NPK Data Report', pageWidth / 2, 20, { align: 'center' })
      
      // Subtitle
      doc.setFontSize(10)
      doc.setTextColor(100, 100, 100)
      doc.text(`Generated on: ${new Date().toLocaleString()}`, pageWidth / 2, 28, { align: 'center' })
      doc.text(`Total Records: ${allData.length}`, pageWidth / 2, 34, { align: 'center' })
      
      // Calculate optimal column widths based on content
      const columnStyles = calculateColumnWidths(exportHeaders, exportRows, tableWidth)
      
      // Table
      autoTable(doc, {
        head: [exportHeaders],
        body: exportRows,
        startY: 40,
        margin: { horizontal: margin },
        tableWidth: tableWidth,
        styles: { 
          fontSize: 8,
          cellPadding: 3,
          overflow: 'linebreak',
          textColor: [51, 51, 51],
          cellWidth: 'wrap'
        },
        headStyles: {
          fillColor: [16, 163, 74], // green-600
          textColor: 255,
          fontStyle: 'bold',
          fontSize: 9,
          cellPadding: 4
        },
        bodyStyles: {
          cellPadding: 3
        },
        alternateRowStyles: {
          fillColor: [240, 253, 244] // green-50
        },
        columnStyles: columnStyles,
        theme: 'grid',
        didDrawPage: function (data) {
          // Footer
          doc.setFontSize(8)
          doc.setTextColor(150, 150, 150)
          doc.text(
            `Page ${data.pageNumber} of ${doc.getNumberOfPages()}`,
            pageWidth / 2,
            doc.internal.pageSize.height - 10,
            { align: 'center' }
          )
        },
        willDrawCell: function (data) {
          // Add some visual separation for better readability
          if (data.section === 'body' && data.row.index % 5 === 0 && data.row.index > 0) {
            doc.setDrawColor(220, 220, 220)
            doc.setLineWidth(0.2)
            doc.line(
              data.cell.x,
              data.cell.y + data.cell.height,
              data.cell.x + data.cell.width,
              data.cell.y + data.cell.height
            )
          }
        }
      })
      
      doc.save(`npk_report_${timestamp}.pdf`)
      window.showToast(`Exported ${allData.length} NPK records as PDF`, 'success')
    }
    
  } catch (error) {
    console.error('❌ Export error:', error)
    window.showToast('Error exporting data. Please try again.', 'error')
  } finally {
    isLoading.value = false
    activeDropdown.value = null
  }
}

// Helper function to calculate optimal column widths
const calculateColumnWidths = (headers, rows, totalWidth) => {
  const columnStyles = {}
  const minWidths = {
    0: 15, // ID - minimum width
    1: 25, // Date
    2: 20, // Time
    3: 20, // Device
    4: 30, // Nitrogen
    5: 35, // Phosphorus  
    6: 30, // Potassium
    7: 20  // Soil pH
  }
  
  const maxWidths = {
    0: 25, // ID - maximum width
    1: 35, // Date
    2: 25, // Time
    3: 30, // Device
    4: 40, // Nitrogen
    5: 45, // Phosphorus
    6: 40, // Potassium
    7: 25  // Soil pH
  }
  
  // Calculate total minimum width required
  let totalMinWidth = Object.values(minWidths).reduce((sum, width) => sum + width, 0)
  
  // If total minimum width is less than available width, distribute extra space
  if (totalMinWidth < totalWidth) {
    const extraSpace = totalWidth - totalMinWidth
    const extraPerColumn = extraSpace / headers.length
    
    // Apply calculated widths
    headers.forEach((_, index) => {
      let calculatedWidth = minWidths[index] + extraPerColumn
      // Don't exceed max width
      calculatedWidth = Math.min(calculatedWidth, maxWidths[index])
      columnStyles[index] = { cellWidth: calculatedWidth }
    })
  } else {
    // Use minimum widths if table is too wide
    headers.forEach((_, index) => {
      columnStyles[index] = { cellWidth: minWidths[index] }
    })
  }
  
  return columnStyles
}

const updateCurrentDate = () => {
  const now = new Date()
  currentDate.value = now.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric'
  })
}

// Watchers
watch([searchQuery, activeFilters], () => {
  currentPage.value = 1
})

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside);

  // Initial data fetch - both chart data and first page
  Promise.all([
    fetchChartData(), // Fetch latest 20 for charts
    fetchPageData(1, itemsPerPage.value) // Fetch first page for table
  ]).then(() => {
    isLoading.value = false;
    // Start polling after initial data is loaded
    startPolling();
  });
  
  // Use ResizeObserver to handle container resizing
  const resizeObserver = new ResizeObserver(() => {
    if (chartsInitialized.value) {
      handleResize();
    }
  });
  
  // Observe all chart containers
  if (nitrogenChartCanvas.value) {
    resizeObserver.observe(nitrogenChartCanvas.value.parentElement);
  }
  if (phosphorusChartCanvas.value) {
    resizeObserver.observe(phosphorusChartCanvas.value.parentElement);
  }
  if (potassiumChartCanvas.value) {
    resizeObserver.observe(potassiumChartCanvas.value.parentElement);
  }
  
  // Also listen to window resize
  window.addEventListener('resize', handleResize);
  
  updateCurrentDate();
  const dateInterval = setInterval(updateCurrentDate, 60000);
  
  window.dateUpdateInterval = dateInterval;
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  
  // Clean up polling
  stopPolling();
  
  window.removeEventListener('resize', handleResize);
  
  if (window.dateUpdateInterval) {
    clearInterval(window.dateUpdateInterval);
  }
});
</script>
  
<style>
/* Your existing styles */
canvas {
  display: block;
  max-width: 100%;
  height: auto;
}

tr {
  border-bottom: 1px solid #cbcbcb !important;
}

.chart-container {
  position: relative;
  width: 100%;
  height: 100%;
}

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

.from-green-50 {
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

.to-green-50 {
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

  th div, td div {
    max-width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
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