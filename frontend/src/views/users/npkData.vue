<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">        <!-- Gradient header for visual appeal -->
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
                    @click="printTable"
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
          <!-- Fixed Header with enhanced styling -->
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
              
              <div v-if="paginatedData.length === 0 && !isLoading" 
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
                      <th class="w-[10%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        ID
                      </th>
                      <th class="w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-green-600">Nitrogen</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-blue-600">Phosphorus</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-purple-600">Potassium</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="w-[15%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-gray-600">Date</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">MMM DD, YYYY</div>
                      </th>
                      <th class="w-[15%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
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
                      <td class="w-[10%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-medium text-gray-700">{{ row.id }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-semibold" :class="getNitrogenTextClass(row.nitrogen)">
                          {{ row.nitrogen }}
                        </div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-semibold" :class="getPhosphorusTextClass(row.phosphorus)">
                          {{ row.phosphorus }}
                        </div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-semibold" :class="getPotassiumTextClass(row.potassium)">
                          {{ row.potassium }}
                        </div>
                      </td>
                      <td class="w-[15%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-medium text-gray-700">{{ row.date }}</div>
                      </td>
                      <td class="w-[15%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-medium text-gray-700">{{ row.time }}</div>
                      </td>
                    </tr>
                    
                    <tr v-if="paginatedData.length === 0 && !isLoading">
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
            Showing {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, sortedData.length) }}
            of {{ sortedData.length }}
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
import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun, NumberValueElement } from 'docx'
import { saveAs } from 'file-saver'
import api from '../../api/index.js'

import Chart from 'chart.js/auto'

const npkData = ref([])
const isLoading = ref(true)

const nitrogenChartCanvas = ref(null)
const phosphorusChartCanvas = ref(null)
const potassiumChartCanvas = ref(null)
const nitrogenChart = ref(null)
const phosphorusChart = ref(null)
const potassiumChart = ref(null)
const chartData = ref([])
const currentNitrogenValue = ref('--')
const currentPhosphorusValue = ref('--')
const currentPotassiumValue = ref('--')
const lastUpdated = ref('--')
const currentDate = ref('')
const nitrogenStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})
const phosphorusStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})
const potassiumStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})

import html2canvas from 'html2canvas';

let PRINT_CHART_DATA_LIMIT = 0;

const printTable = async () => {
  activeDropdown.value = null;
  
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
  
  const npkRows = sortedData.value.map(row => ({
    id: row.id,
    date: row.date,
    time: row.time,
    device: row.deviceId || 'N/A',
    nitrogen: row.nitrogen,
    phosphorus: row.phosphorus,
    potassium: row.potassium
  }));
  
  const printChartData = npkData.value
    .slice(0, PRINT_CHART_DATA_LIMIT) 
    .filter(item => item.nitrogen !== '--' && item.phosphorus !== '--' && item.potassium !== '--')
    .map(item => ({
      timestamp: item.rawTimestamp || new Date(),
      nitrogen: Number(item.nitrogen),
      phosphorus: Number(item.phosphorus),
      potassium: Number(item.potassium)
    }))
    .sort((a, b) => a.timestamp - b.timestamp); 
  
  console.log(`📊 Print chart will show ${printChartData.length} records`);
  
  let combinedChartImage = '';
  
  try {
    const ctx = tempCanvas.getContext('2d');
    
    const tempCombinedChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: printChartData.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          })
        }),
        datasets: [
          {
            label: 'Nitrogen (mg/kg)',
            data: printChartData.map(item => item.nitrogen), 
            borderColor: '#22c55e',
            backgroundColor: 'rgba(34, 197, 94, 0.1)',
            borderWidth: 3,
            tension: 0.4,
            fill: false,
            pointRadius: 3, 
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#22c55e',
            pointBorderWidth: 2,
          },
          {
            label: 'Phosphorus (mg/kg)',
            data: printChartData.map(item => item.phosphorus), 
            borderColor: '#3b82f6',
            backgroundColor: 'rgba(59, 130, 246, 0.1)',
            borderWidth: 3,
            tension: 0.4,
            fill: false,
            pointRadius: 3, 
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#3b82f6',
            pointBorderWidth: 2,
          },
          {
            label: 'Potassium (mg/kg)',
            data: printChartData.map(item => item.potassium), 
            borderColor: '#a855f7',
            backgroundColor: 'rgba(168, 85, 247, 0.1)',
            borderWidth: 3,
            tension: 0.4,
            fill: false,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#a855f7',
            pointBorderWidth: 2,
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
            beginAtZero: false,
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
              maxTicksLimit: 10, 
              maxRotation: 45
            }
          }
        }
      }
    });
    
    setTimeout(async () => {
      try {
        combinedChartImage = tempCanvas.toDataURL('image/png', 1.0);
        
        tempCombinedChart.destroy();
        document.body.removeChild(tempContainer);
        
        generatePrintHTML(combinedChartImage, npkRows, formattedDate, now, printChartData.length);
      } catch (error) {
        console.error('Error capturing combined chart:', error);
        document.body.removeChild(tempContainer);
        generatePrintHTML('', npkRows, formattedDate, now, 0);
      }
    }, 500);
    
  } catch (error) {
    console.error('Error creating combined chart:', error);
    document.body.removeChild(tempContainer);
    generatePrintHTML('', npkRows, formattedDate, now, 0);
  }
};

const generatePrintHTML = (combinedChartImage, npkRows, formattedDate, now, chartRecordCount) => {
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>NPK Soil Analysis Data</title>
      <style>
        /* ... existing styles ... */
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
        /* ... rest of existing styles ... */
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
        .nitrogen { color: #059669; font-weight: 500; }
        .phosphorus { color: #2563eb; font-weight: 500; }
        .potassium { color: #7c3aed; font-weight: 500; }
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
        .stat-item.nitrogen h4 { color: #22c55e; }
        .stat-item.phosphorus h4 { color: #3b82f6; }
        .stat-item.potassium h4 { color: #a855f7; }
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
        <h1>NPK Soil Analysis Report</h1>
        <div class="date">${formattedDate}</div>
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-item">
          <span class="summary-label">Total Records:</span>
          <span class="summary-value">${npkRows.length}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Chart Data Points:</span>
          <span class="summary-value">${chartRecordCount}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Date Range:</span>
          <span class="summary-value">${npkRows.length > 0 ? npkRows[npkRows.length-1].date + ' to ' + npkRows[0].date : 'N/A'}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Report Generated:</span>
          <span class="summary-value">${now.toLocaleString()}</span>
        </div>
      </div>
      
      <div class="section-header">NPK Combined Trends Analysis</div>
      ${combinedChartImage ? `
        <div class="chart-title">NPK Levels Over Time (mg/kg)</div>
        <div class="chart-info">Showing ${chartRecordCount} most recent data points</div>
        <img src="${combinedChartImage}" class="chart-image" alt="Combined NPK Chart" />
        
        <div class="stats-summary">
          <div class="stat-item nitrogen">
            <h4>Nitrogen</h4>
            <div class="stat-values">
              Current: ${currentNitrogenValue.value} mg/kg<br>
              Min: ${nitrogenStats.value.min} | Avg: ${nitrogenStats.value.avg} | Max: ${nitrogenStats.value.max}
            </div>
          </div>
          <div class="stat-item phosphorus">
            <h4>Phosphorus</h4>
            <div class="stat-values">
              Current: ${currentPhosphorusValue.value} mg/kg<br>
              Min: ${phosphorusStats.value.min} | Avg: ${phosphorusStats.value.avg} | Max: ${phosphorusStats.value.max}
            </div>
          </div>
          <div class="stat-item potassium">
            <h4>Potassium</h4>
            <div class="stat-values">
              Current: ${currentPotassiumValue.value} mg/kg<br>
              Min: ${potassiumStats.value.min} | Avg: ${potassiumStats.value.avg} | Max: ${potassiumStats.value.max}
            </div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">Chart could not be generated</p>'}
      
      <div class="section-header">Detailed NPK Sensor Readings</div>
      <table>
        <thead>
          <tr>
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
        Generated by NPK Soil Analysis System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
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
    return [1, '..', total]
  } else if (current === total) {
    return [1, '..', total]
  } else {
    return [current, '...', total]
  }
})

const dataCache = ref(null)

const fetchNPKData = async () => {
  try {
    isLoading.value = true

    const response = await api.get('/npk-data')
    const responseData = response.data
    
    console.log('✅ Data received:', responseData)

    if (Array.isArray(responseData)) {
      const processedData = responseData.map((reading, index) => {
        const timestamp = reading.timestamp?._seconds 
          ? new Date(reading.timestamp._seconds * 1000)
          : new Date(reading.timestamp || Date.now())
        
        return {
          id: `${index}`, 
          nitrogen: reading.nitrogen?.toFixed(2) || '--',
          phosphorus: reading.phosphorus?.toFixed(2) || '--',
          potassium: reading.potassium?.toFixed(2) || '--',
          date: timestamp.toLocaleDateString(),
          time: timestamp.toLocaleTimeString(),
          rawTimestamp: timestamp,
          deviceId: reading.device_id || 'esp32-1',
          soilPh: reading.soilPh?.toFixed(2) || '--',
          timestampMs: timestamp.getTime()
        }
      })
      .sort((a, b) => b.timestampMs - a.timestampMs)
      .map(({ timestampMs, ...reading }) => reading)

      console.log('📊 Processed data (newest first):', processedData)

      npkData.value = processedData
      dataCache.value = processedData
      
      const chartData = processedData
        .filter(reading => reading.nitrogen !== '--' && reading.phosphorus !== '--' && reading.potassium !== '--')
        .map(reading => ({
          timestamp: reading.rawTimestamp,
          nitrogen: Number(reading.nitrogen),
          phosphorus: Number(reading.phosphorus),
          potassium: Number(reading.potassium)
        }))
      
      initializeChartData(chartData)

      PRINT_CHART_DATA_LIMIT = processedData.length
    }
    
  } catch (error) {
    console.error('❌ Fetch error:', error.message)
    npkData.value = dataCache.value || []
  } finally {
    isLoading.value = false
  }
}

const setupRealtimeListener = () => {
  let pollingInterval = null
  
  const startPolling = () => {
    pollingInterval = setInterval(async () => {
      try {
        const response = await api.get(`/npk-data/recent?hours=1&limit=20`)
        const newData = response.data
        
        if (Array.isArray(newData) && newData.length > 0) {
          processNewData(newData)
        }
      } catch (error) {
        console.error('Polling error:', error)
      }
    }, 5000)
  }
  
  const processNewData = (newData) => {
    const chartFormattedData = newData
      .filter(item => item.nitrogen && item.phosphorus && item.potassium)
      .map(item => {
        const timestamp = item.timestamp?._seconds 
          ? new Date(item.timestamp._seconds * 1000)
          : new Date(item.timestamp || Date.now())
        
        return {
          timestamp: timestamp,
          nitrogen: Number(item.nitrogen),
          phosphorus: Number(item.phosphorus),
          potassium: Number(item.potassium)
        }
      })
      // Sort descending (newest first)
      .sort((a, b) => b.timestamp - a.timestamp)
    
    if (chartFormattedData.length === 0) return
    
    // Merge and keep newest 20
    const updatedChartData = [...chartFormattedData, ...chartData.value]
      .sort((a, b) => b.timestamp - a.timestamp)
      .slice(0, 20)
    
    chartData.value = updatedChartData
    
    // Update values - newest is first
    if (updatedChartData.length > 0) {
      const latestReading = updatedChartData[0]
      currentNitrogenValue.value = latestReading.nitrogen.toFixed(2)
      currentPhosphorusValue.value = latestReading.phosphorus.toFixed(2)
      currentPotassiumValue.value = latestReading.potassium.toFixed(2)
      lastUpdated.value = latestReading.timestamp.toLocaleTimeString()
      
      // Update stats...
    }
    
    updateChart()
  }
  
  startPolling()
  
  return () => {
    if (pollingInterval) {
      clearInterval(pollingInterval)
    }
  }
}

const chartsInitialized = ref(false);

const initializeChartData = (data) => {
  // Take only valid data for charts
  const validChartData = data
    .filter(item => {
      const validN = item.nitrogen !== '--' && !isNaN(Number(item.nitrogen)) && Number(item.nitrogen) > 0
      const validP = item.phosphorus !== '--' && !isNaN(Number(item.phosphorus)) && Number(item.phosphorus) > 0
      const validK = item.potassium !== '--' && !isNaN(Number(item.potassium)) && Number(item.potassium) > 0
      return validN && validP && validK
    })
    .map(item => ({
      timestamp: item.rawTimestamp || new Date(),
      nitrogen: Number(item.nitrogen),
      phosphorus: Number(item.phosphorus),
      potassium: Number(item.potassium)
    }))
    // Changed to sort in descending order (newest first)
    .sort((a, b) => b.timestamp - a.timestamp)
    .slice(0, 20)

  console.log(`📈 Chart data: ${validChartData.length} valid entries`)

  // Set chart data
  chartData.value = validChartData

  // Set initial current values and stats only if we have valid data
  if (validChartData.length > 0) {
    // Since we're now sorting newest first, the first element is the latest
    const latestReading = validChartData[0]
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
    
    // Calculate stats only from valid data
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
    // Reset stats if no valid data
    currentNitrogenValue.value = '--'
    currentPhosphorusValue.value = '--'
    currentPotassiumValue.value = '--'
    lastUpdated.value = '--'
    
    nitrogenStats.value = { min: '--', max: '--', avg: '--' }
    phosphorusStats.value = { min: '--', max: '--', avg: '--' }
    potassiumStats.value = { min: '--', max: '--', avg: '--' }
  }
  
  // Initialize the chart
  initializeChart()
}


const initializeChart = () => {
  nextTick(() => {
    // Small delay to ensure DOM is fully rendered
    setTimeout(() => {
      initializeNitrogenChart();
      initializePhosphorusChart();
      initializePotassiumChart();
      chartsInitialized.value = true;
    }, 100);
  });
}

const initializeNitrogenChart = () => {
  if (nitrogenChartCanvas.value) {
    if (nitrogenChart.value) {
      nitrogenChart.value.destroy()
    }
    
    const ctx = nitrogenChartCanvas.value.getContext('2d')
    const container = nitrogenChartCanvas.value.parentElement;
    nitrogenChartCanvas.value.width = container.clientWidth;
    nitrogenChartCanvas.value.height = container.clientHeight;
    
    nitrogenChart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.value.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          })
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
        animation: {
          duration: 750,
          easing: 'easeOutQuart'
        },
        scales: {
          y: {
            beginAtZero: false,
            min: Math.max(0, Math.floor(nitrogenStats.value.min * 0.9)),
            max: Math.ceil(nitrogenStats.value.max * 1.1),
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
    })
  }
}

const initializePhosphorusChart = () => {
  if (phosphorusChartCanvas.value) {
    if (phosphorusChart.value) {
      phosphorusChart.value.destroy()
    }
    
    const ctx = phosphorusChartCanvas.value.getContext('2d')
    const container = phosphorusChartCanvas.value.parentElement;
    phosphorusChartCanvas.value.width = container.clientWidth;
    phosphorusChartCanvas.value.height = container.clientHeight;
    
    phosphorusChart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.value.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          })
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
        animation: {
          duration: 750,
          easing: 'easeOutQuart'
        },
        scales: {
          y: {
            beginAtZero: false,
            min: Math.max(0, Math.floor(phosphorusStats.value.min * 0.9)),
            max: Math.ceil(phosphorusStats.value.max * 1.1),
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
    })
  }
}

const initializePotassiumChart = () => {
  if (potassiumChartCanvas.value) {
    if (potassiumChart.value) {
      potassiumChart.value.destroy()
    }
    
    const ctx = potassiumChartCanvas.value.getContext('2d')
    const container = potassiumChartCanvas.value.parentElement;
    potassiumChartCanvas.value.width = container.clientWidth;
    potassiumChartCanvas.value.height = container.clientHeight;
    
    potassiumChart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartData.value.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          })
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
        animation: {
          duration: 750,
          easing: 'easeOutQuart'
        },
        scales: {
          y: {
            beginAtZero: false,
            min: Math.max(0, Math.floor(potassiumStats.value.min * 0.9)),
            max: Math.ceil(potassiumStats.value.max * 1.1),
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
    })
  }
}

const handleResize = () => {
  if (nitrogenChart.value) {
    const container = nitrogenChartCanvas.value.parentElement;
    nitrogenChartCanvas.value.width = container.clientWidth;
    nitrogenChartCanvas.value.height = container.clientHeight;
    nitrogenChart.value.resize();
  }
  // Repeat for other charts
  if (phosphorusChart.value) {
    const container = phosphorusChartCanvas.value.parentElement;
    phosphorusChartCanvas.value.width = container.clientWidth;
    phosphorusChartCanvas.value.height = container.clientHeight;
    phosphorusChart.value.resize();
  }
  if (potassiumChart.value) {
    const container = potassiumChartCanvas.value.parentElement;
    potassiumChartCanvas.value.width = container.clientWidth;
    potassiumChartCanvas.value.height = container.clientHeight;
    potassiumChart.value.resize();
  }
}

const updateChart = () => {
  updateNitrogenChart()
  updatePhosphorusChart()
  updatePotassiumChart()
}

const updateNitrogenChart = () => {
  if (nitrogenChart.value && chartData.value.length > 0) {
    nitrogenChart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    nitrogenChart.value.data.datasets[0].data = chartData.value.map(item => item.nitrogen)
    nitrogenChart.value.options.scales.y.min = Math.max(0, Math.floor(nitrogenStats.value.min * 0.9))
    nitrogenChart.value.options.scales.y.max = Math.ceil(nitrogenStats.value.max * 1.1)
    nitrogenChart.value.update('none')
  }
}

const updatePhosphorusChart = () => {
  if (phosphorusChart.value && chartData.value.length > 0) {
    phosphorusChart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    phosphorusChart.value.data.datasets[0].data = chartData.value.map(item => item.phosphorus)
    phosphorusChart.value.options.scales.y.min = Math.max(0, Math.floor(phosphorusStats.value.min * 0.9))
    phosphorusChart.value.options.scales.y.max = Math.ceil(phosphorusStats.value.max * 1.1)
    phosphorusChart.value.update('none')
  }
}

const updatePotassiumChart = () => {
  if (potassiumChart.value && chartData.value.length > 0) {
    potassiumChart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    potassiumChart.value.data.datasets[0].data = chartData.value.map(item => item.potassium)
    potassiumChart.value.options.scales.y.min = Math.max(0, Math.floor(potassiumStats.value.min * 0.9))
    potassiumChart.value.options.scales.y.max = Math.ceil(potassiumStats.value.max * 1.1)
    potassiumChart.value.update('none')
  }
}

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

const filters = ref({
  nitrogen: { min: '', max: '' },
  phosphorus: { min: '', max: '' },
  potassium: { min: '', max: '' }
})

const searchQuery = ref('')
const itemsPerPage = ref(20) 
const currentPage = ref(1)
const activeDropdown = ref(null)
const sortKey = ref('date')
const sortDirection = ref('asc')
const activeFilters = ref({})

const filterFields = [
  { key: 'nitrogen', label: 'Nitrogen (mg/kg)' },
  { key: 'phosphorus', label: 'Phosphorus (mg/kg)' },
  { key: 'potassium', label: 'Potassium (mg/kg)' }
]

const headers = [
  { key: 'id', label: 'ID' },
  { key: 'nitrogen', label: 'Nitrogen (mg/kg)' },
  { key: 'phosphorus', label: 'Phosphorus (mg/kg)' },
  { key: 'potassium', label: 'Potassium (mg/kg)' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const exportFormats = ['csv', 'pdf']

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
  const startIndex = (currentPage.value - 1) * itemsPerPage.value
  const endIndex = startIndex + itemsPerPage.value
  return sortedData.value.slice(startIndex, endIndex)
})

const totalPages = computed(() => {
  return Math.ceil(sortedData.value.length / itemsPerPage.value)
})

const displayedPages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const pages = []

  if (total <= 7) {
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    pages.push(1)

    if (current <= 3) {
      pages.push(2, 3, 4, 5, '...', total)
    } else if (current >= total - 2) {
      pages.push('...', total - 4, total - 3, total - 2, total - 1, total)
    } else {
      pages.push('...', current - 1, current, current + 1, '...', total)
    }
  }

  return pages
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

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const updatePagination = () => {
  currentPage.value = 1 
}

const goToPage = (page) => {
  if (typeof page === 'number') {
    currentPage.value = page
  }
}

const exportData = async (format) => {
  const dataToExport = sortedData.value
  if (!dataToExport.length) return

  const exportHeaders = headers.map(h => h.label)
  const exportRows = dataToExport.map(row =>
    headers.map(header => row[header.key] ?? '')
  )

  if (format === 'csv') {
    let csvContent = exportHeaders.join(',') + '\n'
    exportRows.forEach(row => {
      csvContent += row.map(val => `"${val}"`).join(',') + '\n'
    })
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    saveAs(blob, 'npk_data.csv')
    window.showToast('NPK Data exported as CSV', 'success')
  } else if (format === 'pdf') {
     try {
      const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'mm'
      });

      doc.setFontSize(16);
      doc.text('Soil pH Data Report', 105, 15, { align: 'center' });
      
      doc.setFontSize(10);
      doc.text(`Generated: ${new Date().toLocaleDateString()}`, 105, 22, { align: 'center' });

      const chartContainer = document.querySelector('.bg-white.rounded-lg.border.border-gray-100.shadow-sm.overflow-hidden.flex.flex-col.mb-4');
      
      if (chartContainer) {
        window.showToast('Preparing chart for export...', 'info');
        
        const canvas = await html2canvas(chartContainer, {
          scale: 2, 
          logging: false,
          useCORS: true,
          allowTaint: true
        });

        const imgData = canvas.toDataURL('image/png');
        
        const imgWidth = 160; 
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        
        doc.addImage(
          imgData,
          'PNG',
          (210 - imgWidth) / 2, 
          30,                   
          imgWidth,
          imgHeight
        );

        doc.setFontSize(12);
        doc.text('Soil pH Trend Analysis', 105, 30 + imgHeight + 5, { align: 'center' });

        doc.setFontSize(10);
        doc.text(
          `Current: ${currentPhValue.value} | Min: ${phStats.value.min} | Avg: ${phStats.value.avg} | Max: ${phStats.value.max}`,
          105,
          30 + imgHeight + 10,
          { align: 'center' }
        );

        const tableStartY = 30 + imgHeight + 15;
        
        autoTable(doc, {
          head: [exportHeaders],
          body: exportRows,
          startY: tableStartY,
          margin: { horizontal: 10 },
          styles: {
            fontSize: 8,
            cellPadding: 2,
            overflow: 'linebreak'
          },
          headStyles: {
            fillColor: [16, 163, 74], 
            textColor: 255,
            fontStyle: 'bold'
          },
          alternateRowStyles: {
            fillColor: [240, 253, 244] 
          },
          didDrawPage: function(data) {
            doc.setFontSize(8);
            doc.setTextColor(100);
            doc.text(
              `Page ${data.pageCount}`,
              data.settings.margin.left,
              doc.internal.pageSize.height - 10
            );
          }
        });

        doc.save('soil_ph_complete_report.pdf');
        window.showToast('Complete report exported successfully', 'success');
      } else {
        autoTable(doc, {
          head: [exportHeaders],
          body: exportRows,
          startY: 30,
          styles: { fontSize: 10 }
        });
        doc.save('soil_ph_data.pdf');
        window.showToast('Exported table data (chart not found)', 'warning');
      }
    } catch (error) {
      console.error('Export error:', error);
      window.showToast('Export failed: ' + error.message, 'error');
    }
  } else if (format === 'docs') {
    const tableRows = [
      new TableRow({
        children: exportHeaders.map(h => new TableCell({
          children: [new Paragraph({ children: [new TextRun({ text: h, bold: true })] })]
        }))
      }),
      ...exportRows.map(row =>
        new TableRow({
          children: row.map(cell =>
            new TableCell({
              children: [new Paragraph(cell ? cell.toString() : '')]
            })
          )
        })
      )
    ]
    const docxDoc = new Document({
      sections: [{
        children: [
          new Paragraph({ text: 'NPK Data Table', heading: 'Heading1' }),
          new Table({ rows: tableRows })
        ]
      }]
    })
    const buffer = await Packer.toBlob(docxDoc)
    saveAs(buffer, 'npk_data.docx')
  }

  activeDropdown.value = null
}

watch([searchQuery, activeFilters, itemsPerPage], () => {
  currentPage.value = 1
})

let unsubscribe = null

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  
  fetchNPKData();
  
  unsubscribe = setupRealtimeListener();
  
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

// Update the onUnmounted lifecycle hook
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
  
  if (nitrogenChart.value) nitrogenChart.value.destroy();
  if (phosphorusChart.value) phosphorusChart.value.destroy();
  if (potassiumChart.value) potassiumChart.value.destroy();
  
  if (unsubscribe) {
    unsubscribe();
  }
  
  window.removeEventListener('resize', handleResize);
  
  if (window.dateUpdateInterval) {
    clearInterval(window.dateUpdateInterval);
  }
});


const updateCurrentDate = () => {
  const now = new Date()
  currentDate.value = now.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric'
  })
}
</script>
  
<style>
canvas {
  display: block;
  max-width: 100%;
  height: auto;
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