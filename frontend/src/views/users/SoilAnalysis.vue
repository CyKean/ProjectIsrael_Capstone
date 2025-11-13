<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-full mx-auto w-[calc(100vw-15px)] h-[calc(100vh-85px)] mt-1 md:h-[calc(100vh-130px)] flex flex-col overflow-hidden min-w-0">
      <div class="bg-gradient-to-r from-emerald-50 to-white p-3 md:p-5 border-b border-gray-100 rounded-t-lg">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          <div>
            <h1 class="text-sm md:text-lg font-semibold text-gray-800 mb-1">Soil Analysis Measurements</h1>
            <div class="flex flex-col md:flex-row md:items-center text-xs sm:text-sm text-gray-500 flex-wrap">
              <span class="text-emerald-600 font-medium whitespace-nowrap">ESP32-1: NPK + pH Sensors</span>
              <div class="w-1 h-1 rounded-full bg-gray-300 mx-2 flex-shrink-0"></div>
              <span class="text-emerald-600 font-medium whitespace-nowrap">ESP32-2: Environmental Sensors</span>
            </div>
          </div>
            
          <div class="flex items-center gap-2">
            <div class="relative w-[8.5rem] md:w-64">
              <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search all measurements..."
                class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 text-xs md:text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                v-model="globalSearchQuery"
                @input="performGlobalSearch"
              />
            </div>

            <div class="relative flex items-center gap-2">
              <button 
                @click.stop="toggleDropdown('export')"
                class="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 text-white text-[10px] md:text-sm font-medium hover:bg-emerald-600 transition-colors shadow-sm dropdown-trigger"
              >
                <Download class="h-4 w-4" />
                <span class="hidden md:block">Export All</span>
                <ChevronDown class="h-4 w-4" :class="{ 'transform rotate-180': activeDropdown === 'export' }" />
              </button>
              <button 
                @click="openPrintModal"
                class="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-500 text-white text-[10px] md:text-sm font-medium hover:bg-green-600 transition-colors shadow-sm"
              >
                <Printer class="h-4 w-4" />
                <span class="hidden md:block">Print</span>
              </button>
              
              <div 
                v-show="activeDropdown === 'export'"
                class="absolute right-0 md:mr-[4.5rem] top-full mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-[9999] overflow-hidden dropdown-panel"
                @click.stop
              >
                <div class="py-1">
                  <button
                    v-for="format in exportFormats"
                    :key="format"
                    @click="exportAllData(format)"
                    class="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                  >
                    <FileText class="h-4 w-4 mr-2" :class="format === 'csv' ? 'text-emerald-500' : format === 'pdf' ? 'text-red-500' : 'text-blue-500'" />
                    Export as {{ format.toUpperCase() }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="flex-1 flex flex-col lg:flex-row gap-4 p-2 md:p-4 overflow-auto">
        <!-- ESP32-1 Container -->
        <div ref="esp32_1_Container" class="flex-1 bg-gray-50 rounded-xl border border-gray-200 flex flex-col overflow-hidden min-h-[500px] md:min-h-0">
          <div class="bg-white border-b border-gray-200 p-3 relative">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-green-500"></div>
                <div>
                  <h3 class="text-xs md:text-sm font-semibold text-gray-800">ESP32-1 Sensors</h3>
                  <p class="text-[10px] md:text-xs text-gray-500">NPK + Soil pH Measurements</p>
                </div>
              </div>
              <div class="text-[10px] md:text-xs text-green-600 bg-green-100 px-2 py-1 rounded-full font-medium">
                {{ esp32_1_PaginationMeta.totalItems }} readings
              </div>
            </div>
            
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
              <div class="relative flex-1 min-w-0">
                <Search class="absolute left-2.5 top-1/2 transform -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search ESP32-1 data..."
                  class="w-full pl-8 pr-3 py-1.5 rounded-md border border-gray-200 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 text-xs"
                  v-model="esp32_1_SearchQuery"
                  @input="performESP32_1_Search"
                />
              </div>
              
              <div class="flex gap-2">
                <div class="relative">
                  <button 
                    ref="filterButton1"
                    @click.stop="toggleDropdown('filter-esp32-1')"
                    class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-gray-200 bg-white text-xs text-gray-600 hover:text-green-600 transition-colors dropdown-trigger"
                  >
                    <Filter class="h-3.5 w-3.5" />
                    Filter
                  </button>
                  
                  <div 
                    v-show="activeDropdown === 'filter-esp32-1'"
                    class="fixed bg-white rounded-lg shadow-xl border border-gray-200 z-[9999] dropdown-panel"
                    :style="getDropdownStyle('filter-esp32-1')"
                    @click.stop
                  >
                    <div class="p-3 space-y-3 w-64 max-h-[300px] overflow-y-hidden">
                      <div v-for="field in esp32_1_FilterFields" :key="field.key" class="space-y-1.5">
                        <label class="block text-xs font-medium text-gray-700">{{ field.label }}</label>
                        <div class="flex items-center gap-2">
                          <input
                            v-model="esp32_1_Filters[field.key].min"
                            type="number"
                            placeholder="Min"
                            class="w-full px-2.5 py-1.5 text-xs border border-gray-200 rounded-md focus:ring-1 focus:ring-green-500 focus:border-green-500"
                          />
                          <span class="text-gray-400 text-xs">-</span>
                          <input
                            v-model="esp32_1_Filters[field.key].max"
                            type="number"
                            placeholder="Max"
                            class="w-full px-2.5 py-1.5 text-xs border border-gray-200 rounded-md focus:ring-1 focus:ring-green-500 focus:border-green-500"
                          />
                        </div>
                      </div>
                      <button 
                        @click="applyESP32_1_Filters"
                        class="w-full px-3 py-1.5 bg-green-500 text-white rounded-md text-xs font-medium hover:bg-green-600 transition-colors"
                      >
                        Apply Filters
                      </button>
                    </div>
                  </div>
                </div>
                
                <div class="relative">
                  <button 
                    ref="sortButton1"
                    @click.stop="toggleDropdown('sort-esp32-1')"
                    class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-gray-200 bg-white text-xs text-gray-600 hover:text-green-600 transition-colors dropdown-trigger"
                  >
                    <ArrowUpDown class="h-3.5 w-3.5" />
                    Sort
                  </button>

                  <div 
                    v-show="activeDropdown === 'sort-esp32-1'"
                    class="fixed bg-white rounded-lg shadow-xl border border-gray-200 z-[9999] dropdown-panel"
                    :style="getDropdownStyle('sort-esp32-1')"
                    @click.stop
                  >
                    <div class="py-1 w-48">
                      <button
                        v-for="header in esp32_1_Headers"
                        :key="header.key"
                        @click="setESP32_1_SortKey(header.key)"
                        class="w-full px-3 py-1.5 text-left text-xs text-gray-700 hover:bg-gray-50 flex items-center justify-between"
                      >
                        {{ header.label }}
                        <ArrowUpDown v-if="esp32_1_SortKey === header.key" class="h-3 w-3 text-green-500" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="flex-1 flex flex-col min-h-0">
            <!-- Mobile Card View (shown on small screens) -->
            <div class="sm:hidden flex-1 overflow-auto bg-white p-3 space-y-3">
              <div v-for="(row, index) in esp32_1_Data" :key="index" 
                  class="bg-gray-50 rounded-lg p-3">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <div class="text-xs font-medium text-gray-900">{{ row.date }}</div>
                    <div class="text-[10px] text-gray-500">{{ row.time }}</div>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Nitrogen</div>
                    <div class="text-xs font-semibold text-green-600">{{ row.nitrogen }} mg/kg</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Phosphorus</div>
                    <div class="text-xs font-semibold text-blue-600">{{ row.phosphorus }} mg/kg</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Potassium</div>
                    <div class="text-xs font-semibold text-purple-600">{{ row.potassium }} mg/kg</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">pH</div>
                    <div class="text-xs font-semibold text-orange-600">{{ row.ph }} level</div>
                  </div>
                </div>
              </div>
              
              <div v-if="esp32_1_Data.length === 0 && !isLoading" 
                  class="flex flex-col items-center justify-center py-8">
                <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
                <p class="text-gray-500 text-xs font-medium">No ESP32-1 data found</p>
                <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
              </div>
            </div>

            <!-- Desktop Table View (shown on medium screens and up) -->
            <div class="hidden sm:flex flex-1 flex-col min-h-0">
              <div class="flex-1 overflow-auto bg-white">
                <table class="min-w-full table-fixed">
                  <thead class="bg-gray-50 border-b border-gray-200 sticky top-0 z-10">
                    <tr>
                      <th class="border-b border-gray-200 w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date & Time
                      </th>
                      <th class="border-b border-gray-200 w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-green-600">Nitrogen</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="border-b border-gray-200 w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-blue-600">Phosphorus</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="border-b border-gray-200 w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-purple-600">Potassium</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(mg/kg)</div>
                      </th>
                      <th class="border-b border-gray-200 w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-orange-600">pH</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(level)</div>
                      </th>
                    </tr>
                  </thead>

                  <tbody class="divide-y divide-gray-100">
                    <tr 
                      v-for="(row, index) in esp32_1_Data" 
                      :key="index"
                      class="hover:bg-gray-50 transition-colors"
                    >
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[10px] md:text-xs font-medium text-gray-900">{{ row.date }}</div>
                        <div class="text-[7px] md:text-[10px] text-gray-500">{{ row.time }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[10px] md:text-xs font-semibold text-green-600">{{ row.nitrogen }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[10px] md:text-xs font-semibold text-blue-600">{{ row.phosphorus }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[10px] md:text-xs font-semibold text-purple-600">{{ row.potassium }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[10px] md:text-xs font-semibold text-orange-600">{{ row.ph }}</div>
                      </td>
                    </tr>

                    <tr v-if="esp32_1_Data.length === 0 && !isLoading">
                      <td colspan="5" class="px-4 py-8 text-center">
                        <div class="flex flex-col items-center justify-center">
                          <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
                          <p class="text-gray-500 text-xs font-medium">No ESP32-1 data found</p>
                          <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div class="border-t border-gray-200 py-2 px-3 bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="text-[10px] md:text-xs text-gray-600">
                  Showing {{ (esp32_1_PaginationMeta.currentPage - 1) * esp32_1_PaginationMeta.itemsPerPage + 1 }} - {{ Math.min(esp32_1_PaginationMeta.currentPage * esp32_1_PaginationMeta.itemsPerPage, esp32_1_PaginationMeta.totalItems) }}
                  of {{ esp32_1_PaginationMeta.totalItems }}
                </div>
                <div class="flex items-center gap-1">
                  <button 
                    @click="prevESP32_1_Page"
                    :disabled="!esp32_1_PaginationMeta.hasPrevPage"
                    class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600"
                  >
                    <ChevronLeft class="w-3.5 h-3.5" />
                  </button>
                  
                  <div class="flex items-center gap-1">
                    <button
                      v-for="(page, index) in esp32_1_PaginationNumbers"
                      :key="index"
                      @click="setESP32_1_Page(page)"
                      :disabled="page === '...'"
                      :class="[
                        'px-2 py-1 text-[10px] md:text-xs rounded min-w-[20px]',
                        page === esp32_1_PaginationMeta.currentPage 
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
                    @click="nextESP32_1_Page"
                    :disabled="!esp32_1_PaginationMeta.hasNextPage"
                    class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600"
                  >
                    <ChevronRight class="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- ESP32-2 Container -->
        <div ref="esp32_2_Container" class="flex-1 bg-gray-50 rounded-xl border border-gray-200 flex flex-col overflow-hidden min-h-[500px] md:min-h-0">
          <div class="bg-white border-b border-gray-200 p-3 relative">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-blue-500"></div>
                <div>
                  <h3 class="text-xs md:text-sm font-semibold text-gray-800">ESP32-2 Sensors</h3>
                  <p class="text-[10px] md:text-xs text-gray-500">Environmental Measurements</p>
                </div>
              </div>
              <div class="text-[10px] md:text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-full font-medium">
                {{ esp32_2_PaginationMeta.totalItems }} readings
              </div>
            </div>

            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-2">
              <div class="relative flex-1 min-w-0">
                <Search class="absolute left-2.5 top-1/2 transform -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                <input
                  type="text"
                  placeholder="Search ESP32-2 data..."
                  class="w-full pl-8 pr-3 py-1.5 rounded-md border border-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-xs"
                  v-model="esp32_2_SearchQuery"
                  @input="performESP32_2_Search"
                />
              </div>
              
              <div class="flex gap-2">
                <div class="relative">
                  <button 
                    ref="filterButton2"
                    @click.stop="toggleDropdown('filter-esp32-2')"
                    class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-gray-200 bg-white text-xs text-gray-600 hover:text-blue-600 transition-colors dropdown-trigger"
                  >
                    <Filter class="h-3.5 w-3.5" />
                    Filter
                  </button>
                  
                  <div 
                    v-show="activeDropdown === 'filter-esp32-2'"
                    class="fixed bg-white rounded-lg shadow-xl border border-gray-200 z-[9999] dropdown-panel"
                    :style="getDropdownStyle('filter-esp32-2')"
                    @click.stop
                  >
                    <div class="p-3 space-y-3 w-64 max-h-[300px] overflow-y-auto">
                      <div v-for="field in esp32_2_FilterFields" :key="field.key" class="space-y-1.5">
                        <label class="block text-xs font-medium text-gray-700">{{ field.label }}</label>
                        <div class="flex items-center gap-2">
                          <input
                            v-model="esp32_2_Filters[field.key].min"
                            type="number"
                            placeholder="Min"
                            class="w-full px-2.5 py-1.5 text-xs border border-gray-200 rounded-md focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                          />
                          <span class="text-gray-400 text-xs">-</span>
                          <input
                            v-model="esp32_2_Filters[field.key].max"
                            type="number"
                            placeholder="Max"
                            class="w-full px-2.5 py-1.5 text-xs border border-gray-200 rounded-md focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
                          />
                        </div>
                      </div>
                      <button 
                        @click="applyESP32_2_Filters"
                        class="w-full px-3 py-1.5 bg-blue-500 text-white rounded-md text-xs font-medium hover:bg-blue-600 transition-colors"
                      >
                        Apply Filters
                      </button>
                    </div>
                  </div>
                </div>
                
                <div class="relative">
                  <button 
                    ref="sortButton2"
                    @click.stop="toggleDropdown('sort-esp32-2')"
                    class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-gray-200 bg-white text-xs text-gray-600 hover:text-blue-600 transition-colors dropdown-trigger"
                  >
                    <ArrowUpDown class="h-3.5 w-3.5" />
                    Sort
                  </button>
                  
                  <div 
                    v-show="activeDropdown === 'sort-esp32-2'"
                    class="fixed bg-white rounded-lg shadow-xl border border-gray-200 z-[9999] dropdown-panel"
                    :style="getDropdownStyle('sort-esp32-2')"
                    @click.stop
                  >
                    <div class="py-1 w-48">
                      <button
                        v-for="header in esp32_2_Headers"
                        :key="header.key"
                        @click="setESP32_2_SortKey(header.key)"
                        class="w-full px-3 py-1.5 text-left text-xs text-gray-700 hover:bg-gray-50 flex items-center justify-between"
                      >
                        {{ header.label }}
                        <ArrowUpDown v-if="esp32_2_SortKey === header.key" class="h-3 w-3 text-blue-500" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="flex-1 flex flex-col min-h-0">
            <!-- Mobile Card View (shown on small screens) -->
            <div class="sm:hidden flex-1 overflow-auto bg-white p-3 space-y-3">
              <div v-for="(row, index) in esp32_2_Data" :key="index" 
                  class="bg-gray-50 rounded-lg p-3">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <div class="text-xs font-medium text-gray-900">{{ row.date }}</div>
                    <div class="text-[10px] text-gray-500">{{ row.time }}</div>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Temperature</div>
                    <div class="text-xs font-semibold text-red-600">{{ row.temperature }}°C</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Humidity</div>
                    <div class="text-xs font-semibold text-blue-600">{{ row.humidity }}%</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Soil Moisture</div>
                    <div class="text-xs font-semibold text-cyan-600">{{ row.soilMoisture }}%</div>
                  </div>
                </div>
              </div>
              
              <div v-if="esp32_2_Data.length === 0 && !isLoading" 
                  class="flex flex-col items-center justify-center py-8">
                <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
                <p class="text-gray-500 text-xs font-medium">No ESP32-2 data found</p>
                <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
              </div>
            </div>

            <!-- Desktop Table View (shown on medium screens and up) -->
            <div class="hidden sm:flex flex-1 flex-col min-h-0">
              <div class="flex-1 overflow-auto bg-white">
                <table class="min-w-full table-fixed">
                  <thead class="bg-gray-50 border-b border-gray-200 sticky top-0 z-10">
                    <tr>
                      <th class="w-[25%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200">
                        Date & Time
                      </th>
                      <th class="w-[25%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200">
                        <div class="text-red-600">Temperature</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(°C)</div>
                      </th>
                      <th class="w-[25%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200">
                        <div class="text-blue-600">Humidity</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(%)</div>
                      </th>
                      <th class="w-[25%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200">
                        <div class="text-cyan-600">Soil Moisture</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(%)</div>
                      </th>
                    </tr>
                  </thead>
                  
                  <tbody class="divide-y divide-gray-100">
                    <tr 
                      v-for="(row, index) in esp32_2_Data" 
                      :key="index"
                      class="hover:bg-gray-50 transition-colors"
                    >
                      <td class="w-[25%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-xs font-medium text-gray-900">{{ row.date }}</div>
                        <div class="text-[7px] md:text-[10px] text-gray-500">{{ row.time }}</div>
                      </td>
                      <td class="w-[25%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-xs font-semibold text-red-600">{{ row.temperature }}</div>
                      </td>
                      <td class="w-[25%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-xs font-semibold text-blue-600">{{ row.humidity }}</div>
                      </td>
                      <td class="w-[25%] py-2.5 px-3 whitespace-nowrap border-b border-gray-200">
                        <div class="text-[9px] md:text-xs font-semibold text-cyan-600">{{ row.soilMoisture }}</div>
                      </td>
                    </tr>
                    
                    <tr v-if="esp32_2_Data.length === 0 && !isLoading">
                      <td colspan="4" class="px-4 py-8 text-center">
                        <div class="flex flex-col items-center justify-center">
                          <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
                          <p class="text-gray-500 text-xs font-medium">No ESP32-2 data found</p>
                          <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div class="border-t border-gray-200 py-2 px-3 bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="text-[10px] md:text-xs text-gray-600">
                  Showing {{ (esp32_2_PaginationMeta.currentPage - 1) * esp32_2_PaginationMeta.itemsPerPage + 1 }} - {{ Math.min(esp32_2_PaginationMeta.currentPage * esp32_2_PaginationMeta.itemsPerPage, esp32_2_PaginationMeta.totalItems) }}
                  of {{ esp32_2_PaginationMeta.totalItems }}
                </div>
                <div class="flex items-center gap-1">
                  <button 
                    @click="prevESP32_2_Page"
                    :disabled="!esp32_2_PaginationMeta.hasPrevPage"
                    class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-blue-600"
                  >
                    <ChevronLeft class="w-3.5 h-3.5" />
                  </button>
                  
                  <div class="flex items-center gap-1">
                    <button
                      v-for="(page, index) in esp32_2_PaginationNumbers"
                      :key="index"
                      @click="setESP32_2_Page(page)"
                      :disabled="page === '...'"
                      :class="[
                        'px-2 py-1 text-[10px] md:text-xs rounded min-w-[20px]',
                        page === esp32_2_PaginationMeta.currentPage 
                          ? 'bg-blue-500 text-white font-medium' 
                          : page === '...' 
                            ? 'text-gray-400 cursor-default' 
                            : 'text-gray-700 hover:text-blue-600 hover:bg-gray-100'
                      ]"
                    >
                      {{ page }}
                    </button>
                  </div>
                  
                  <button 
                    @click="nextESP32_2_Page"
                    :disabled="!esp32_2_PaginationMeta.hasNextPage"
                    class="px-2 py-1 text-[10px] md:text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-blue-600"
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
  </div>

  <!-- Print Range Selection Modal -->
  <div v-if="showPrintModal" class="fixed inset-0 bg-gray-900 bg-opacity-50 flex items-center justify-center z-[10000] p-4">
    <div class="bg-white rounded-lg shadow-xl w-full max-w-md">
      <div class="p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="px-6 py-4 border-b border-gray-200">
            <h3 class="text-lg font-semibold text-gray-800">Select Date Range for Print</h3>
            <p class="text-sm text-gray-500 mt-1">Choose the date range for the soil moisture data you want to print</p>
          </div>
          <button @click="closePrintModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <div class="space-y-4">
          <!-- Date Range Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Date Range</label>
            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs text-gray-500 mb-1">From Date</label>
                <input
                  type="date"
                  v-model="printDateRange.start"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm"
                />
              </div>
              <div>
                <label class="block text-xs text-gray-500 mb-1">To Date</label>
                <input
                  type="date"
                  v-model="printDateRange.end"
                  class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 text-sm"
                />
              </div>
            </div>
          </div>

          <!-- Device Selection -->
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Devices to Print</label>
            <div class="space-y-2">
              <label class="flex items-center">
                <input
                  type="checkbox"
                  v-model="printDevices.esp32_1"
                  class="rounded border-gray-300 text-green-600 focus:ring-green-500"
                />
                <span class="ml-2 text-sm text-gray-700">ESP32-1 (NPK + pH Sensors)</span>
              </label>
              <label class="flex items-center">
                <input
                  type="checkbox"
                  v-model="printDevices.esp32_2"
                  class="rounded border-gray-300 text-green-600 focus:ring-green-500"
                />
                <span class="ml-2 text-sm text-gray-700">ESP32-2 (Environmental Sensors)</span>
              </label>
            </div>
          </div>

          <!-- Summary -->
          <div class="bg-green-50 border border-green-200 rounded-md p-3">
            <h4 class="text-sm font-medium text-green-700 mb-2">Print Summary</h4>
            <div class="text-xs text-green-600 space-y-1">
              <div>Date Range: {{ formatDisplayDate(printDateRange.start) }} to {{ formatDisplayDate(printDateRange.end) }}</div>
              <div>Devices: {{ getSelectedDevicesText() }}</div>
            </div>
          </div>
        </div>

        <div class="flex justify-end gap-3 mt-6">
          <button
            @click="closePrintModal"
            class="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            Cancel
          </button>
          <button
            @click="generatePrint"
            :disabled="!isPrintValid"
            class="px-4 py-2 text-sm font-medium text-white bg-green-600 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Generate Print
          </button>
        </div>
      </div>
    </div>
  </div>

  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Soil Analysis Data" 
    message="Fetching data from ESP32-1 and ESP32-2 sensors..."
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
import api from '../../api/index.js'

// Print functionality variables
const showPrintModal = ref(false)
const printDateRange = ref({
  start: '',
  end: ''
})
const printDevices = ref({
  esp32_1: true,
  esp32_2: true
})
const printDataType = ref('current') // 'current' or 'range'
const estimatedRecords = ref(0)

// Existing variables
const isLoading = ref(true)
const esp32_1_Data = ref([]) 
const esp32_2_Data = ref([])
const esp32_1_PaginationMeta = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20,
  hasNextPage: false,
  hasPrevPage: false
})
const esp32_2_PaginationMeta = ref({
  currentPage: 1,
  totalPages: 1,
  totalItems: 0,
  itemsPerPage: 20,
  hasNextPage: false,
  hasPrevPage: false
})
const globalSearchQuery = ref('')
const activeDropdown = ref(null)
const filterButton1 = ref(null)
const sortButton1 = ref(null)
const filterButton2 = ref(null)
const sortButton2 = ref(null)
const esp32_1_Container = ref(null)
const esp32_2_Container = ref(null)
const esp32_1_SearchQuery = ref('')
const esp32_1_SortKey = ref('timestamp')
const esp32_1_SortDirection = ref('desc')
const esp32_1_ActiveFilters = ref({})
const esp32_1_Filters = ref({
  nitrogen: { min: '', max: '' },
  phosphorus: { min: '', max: '' },
  potassium: { min: '', max: '' },
  ph: { min: '', max: '' }
})
const esp32_2_SearchQuery = ref('')
const esp32_2_SortKey = ref('timestamp')
const esp32_2_SortDirection = ref('desc')
const esp32_2_ActiveFilters = ref({})
const esp32_2_Filters = ref({
  temperature: { min: '', max: '' },
  humidity: { min: '', max: '' },
  soilMoisture: { min: '', max: '' }
})

// Computed properties
const esp32_1_PaginationNumbers = computed(() => {
  const totalPages = esp32_1_PaginationMeta.value.totalPages
  const currentPage = esp32_1_PaginationMeta.value.currentPage
  
  if (totalPages <= 1) return [1]
  
  if (currentPage === 1) {
    return totalPages <= 3 ? Array.from({length: totalPages}, (_, i) => i + 1) : [1, 2, '...', totalPages]
  } else if (currentPage === totalPages) {
    return totalPages <= 3 ? Array.from({length: totalPages}, (_, i) => i + 1) : [1, '...', totalPages - 1, totalPages]
  } else {
    return [1, '...', currentPage, '...', totalPages]
  }
})

const esp32_2_PaginationNumbers = computed(() => {
  const totalPages = esp32_2_PaginationMeta.value.totalPages
  const currentPage = esp32_2_PaginationMeta.value.currentPage
  
  if (totalPages <= 1) return [1]
  
  if (currentPage === 1) {
    return totalPages <= 3 ? Array.from({length: totalPages}, (_, i) => i + 1) : [1, 2, '...', totalPages]
  } else if (currentPage === totalPages) {
    return totalPages <= 3 ? Array.from({length: totalPages}, (_, i) => i + 1) : [1, '...', totalPages - 1, totalPages]
  } else {
    return [1, '...', currentPage, '...', totalPages]
  }
})

const isPrintValid = computed(() => {
  const hasValidDateRange = printDateRange.value.start && printDateRange.value.end
  const hasValidDevices = printDevices.value.esp32_1 || printDevices.value.esp32_2
  return hasValidDateRange && hasValidDevices
})

// Print functionality methods
const openPrintModal = () => {
  // Set default date range (last 7 days)
  const endDate = new Date()
  const startDate = new Date()
  startDate.setDate(startDate.getDate() - 7)
  
  printDateRange.value = {
    start: startDate.toISOString().split('T')[0],
    end: endDate.toISOString().split('T')[0]
  }
  
  console.log('🎯 Print modal opened with date range:', printDateRange.value)
  
  showPrintModal.value = true
  estimateRecords()
}

// Simplify the closePrintModal function:
const closePrintModal = () => {
  showPrintModal.value = false
}

const formatDisplayDate = (dateString) => {
  if (!dateString) return 'Not selected'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  })
}

const getSelectedDevicesText = () => {
  const devices = []
  if (printDevices.value.esp32_1) devices.push('ESP32-1')
  if (printDevices.value.esp32_2) devices.push('ESP32-2')
  return devices.join(', ') || 'None selected'
}

const estimateRecords = async () => {
  try {
    console.log('🔢 Estimating records for date range:', printDateRange.value)
    
    let total = 0
    
    if (printDevices.value.esp32_1) {
      try {
        console.log('📊 Counting ESP32-1 records...')
        const response = await api.get('/soil-analysis/esp32-1/count', {
          params: {
            startDate: printDateRange.value.start,
            endDate: printDateRange.value.end
          }
        })
        console.log('✅ ESP32-1 count:', response.data.count)
        total += response.data.count
      } catch (error) {
        console.error('❌ Error counting ESP32-1 records:', error)
        console.error('Error details:', error.response?.data || error.message)
      }
    }
    
    if (printDevices.value.esp32_2) {
      try {
        console.log('📊 Counting ESP32-2 records...')
        const response = await api.get('/soil-analysis/esp32-2/count', {
          params: {
            startDate: printDateRange.value.start,
            endDate: printDateRange.value.end
          }
        })
        console.log('✅ ESP32-2 count:', response.data.count)
        total += response.data.count
      } catch (error) {
        console.error('❌ Error counting ESP32-2 records:', error)
        console.error('Error details:', error.response?.data || error.message)
      }
    }
    
    console.log('🎯 Total estimated records:', total)
    estimatedRecords.value = total
    
  } catch (error) {
    console.error('❌ Error estimating records:', error)
    estimatedRecords.value = 0
  }
}

const generatePrint = async () => {
  try {
    console.log('🖨️ Generating print for date range...')
    console.log('📅 Date Range:', printDateRange.value)
    console.log('📱 Selected Devices:', printDevices.value)
    
    isLoading.value = true
    closePrintModal()

    let esp32_1_Rows = []
    let esp32_2_Rows = []

    // Always use date range data
    console.log('📊 Fetching data for range:', printDateRange.value.start, 'to', printDateRange.value.end)
    
    // Fetch data for selected date range
    if (printDevices.value.esp32_1) {
      try {
        console.log('🚀 Making API call for ESP32-1 range data...')
        const response = await api.get('/soil-analysis/esp32-1/range', {
          params: {
            startDate: printDateRange.value.start,
            endDate: printDateRange.value.end,
            sortBy: 'timestamp',
            sortOrder: 'desc'
          }
        })
        console.log('✅ ESP32-1 API response received:', response.data.length, 'records')
        
        esp32_1_Rows = response.data.map(row => ({
          date: row.date,
          time: row.time,
          device: row.deviceId,
          nitrogen: row.nitrogen,
          phosphorus: row.phosphorus,
          potassium: row.potassium,
          ph: row.ph
        }))
        console.log('📊 ESP32-1 processed rows:', esp32_1_Rows.length)
      } catch (error) {
        console.error('❌ Error fetching ESP32-1 range data:', error)
        console.error('Error details:', error.response?.data || error.message)
        window.showToast && window.showToast('Error fetching ESP32-1 data', 'error')
      }
    }
    
    if (printDevices.value.esp32_2) {
      try {
        console.log('🚀 Making API call for ESP32-2 range data...')
        const response = await api.get('/soil-analysis/esp32-2/range', {
          params: {
            startDate: printDateRange.value.start,
            endDate: printDateRange.value.end,
            sortBy: 'timestamp',
            sortOrder: 'desc'
          }
        })
        console.log('✅ ESP32-2 API response received:', response.data.length, 'records')
        
        esp32_2_Rows = response.data.map(row => ({
          date: row.date,
          time: row.time,
          device: row.deviceId,
          temperature: row.temperature,
          humidity: row.humidity,
          soilMoisture: row.soilMoisture
        }))
        console.log('📊 ESP32-2 processed rows:', esp32_2_Rows.length)
      } catch (error) {
        console.error('❌ Error fetching ESP32-2 range data:', error)
        console.error('Error details:', error.response?.data || error.message)
        window.showToast && window.showToast('Error fetching ESP32-2 data', 'error')
      }
    }

    console.log('📈 FINAL PRINT DATA SUMMARY:')
    console.log('ESP32-1 rows to print:', esp32_1_Rows.length)
    console.log('ESP32-2 rows to print:', esp32_2_Rows.length)

    // Generate print content
    await printTableContent(esp32_1_Rows, esp32_2_Rows)
    
  } catch (error) {
    console.error('❌ Error generating print:', error)
    window.showToast && window.showToast('Error generating print', 'error')
  } finally {
    isLoading.value = false
  }
}

const printTableContent = async (esp32_1_Rows, esp32_2_Rows) => {
  const now = new Date()
  const formattedDate = now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
  
  let rangeText = ''
  if (printDataType.value === 'range') {
    rangeText = `Date Range: ${formatDisplayDate(printDateRange.value.start)} to ${formatDisplayDate(printDateRange.value.end)}`
  } else {
    rangeText = 'Current Page Data Only'
  }

  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Soil Analysis Data</title>
      <style>
        body {
          font-family: Arial, sans-serif;
          margin: 20px;
          color: #333;
        }
        .header {
          text-align: center;
          margin-bottom: 20px;
          border-bottom: 2px solid #10b981;
          padding-bottom: 10px;
        }
        .header h1 {
          color: #10b981;
          margin: 0;
        }
        .header .date {
          color: #6b7280;
          font-size: 14px;
        }
        .header .range {
          color: #6b7280;
          font-size: 12px;
          margin-top: 5px;
        }
        .section-header {
          margin: 25px 0 15px 0;
          padding: 10px;
          background-color: #f3f4f6;
          border-radius: 5px;
          font-size: 16px;
          font-weight: bold;
        }
        table {
          width: 100%;
          border-collapse: collapse;
          margin-top: 10px;
          font-size: 10px;
        }
        th, td {
          border: 1px solid #e5e7eb;
          padding: 6px 8px;
          text-align: left;
        }
        th {
          background-color: #f3f4f6;
          font-weight: bold;
        }
        tr:nth-child(even) {
          background-color: #f9fafb;
        }
        .nitrogen { color: #059669; }
        .phosphorus { color: #2563eb; }
        .potassium { color: #7c3aed; }
        .ph { color: #ea580c; }
        .temperature { color: #dc2626; }
        .humidity { color: #2563eb; }
        .soil-moisture { color: #0891b2; }
        .summary {
          font-size: 11px;
          color: #6b7280;
          margin: 10px 0;
          padding: 8px;
          background-color: #f3f4f6;
          border-radius: 4px;
        }
        @media print {
          body {
            margin: 0;
            padding: 15px;
          }
          .no-print {
            display: none;
          }
          .header {
            page-break-after: avoid;
          }
          table {
            page-break-inside: auto;
          }
          tr {
            page-break-inside: avoid;
            page-break-after: auto;
          }
        }
        @page {
          size: portrait;
          margin: 0.5in;
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>Soil Analysis Data</h1>
        <div class="date">${formattedDate}</div>
        <div class="range">${rangeText}</div>
        <div class="summary">
          Devices: ${getSelectedDevicesText()} | 
          ESP32-1 Records: ${esp32_1_Rows.length} | 
          ESP32-2 Records: ${esp32_2_Rows.length}
        </div>
      </div>
      
      ${printDevices.value.esp32_1 && esp32_1_Rows.length > 0 ? `
        <div class="section-header">ESP32-1: NPK + pH Sensors (${esp32_1_Rows.length} readings)</div>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Device</th>
              <th>Nitrogen (mg/kg)</th>
              <th>Phosphorus (mg/kg)</th>
              <th>Potassium (mg/kg)</th>
              <th>pH Level</th>
            </tr>
          </thead>
          <tbody>
            ${esp32_1_Rows.map(row => `
              <tr>
                <td>${row.date}</td>
                <td>${row.time}</td>
                <td>${row.device}</td>
                <td><span class="nitrogen">${row.nitrogen}</span></td>
                <td><span class="phosphorus">${row.phosphorus}</span></td>
                <td><span class="potassium">${row.potassium}</span></td>
                <td><span class="ph">${row.ph}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      ` : ''}
      
      ${printDevices.value.esp32_2 && esp32_2_Rows.length > 0 ? `
        <div class="section-header">ESP32-2: Environmental Sensors (${esp32_2_Rows.length} readings)</div>
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Device</th>
              <th>Temperature (°C)</th>
              <th>Humidity (%)</th>
              <th>Soil Moisture (%)</th>
            </tr>
          </thead>
          <tbody>
            ${esp32_2_Rows.map(row => `
              <tr>
                <td>${row.date}</td>
                <td>${row.time}</td>
                <td>${row.device}</td>
                <td><span class="temperature">${row.temperature}</span></td>
                <td><span class="humidity">${row.humidity}</span></td>
                <td><span class="soil-moisture">${row.soilMoisture}</span></td>
              </tr>
            `).join('')}
          </tbody>
        </table>
      ` : ''}
      
      ${esp32_1_Rows.length === 0 && esp32_2_Rows.length === 0 ? `
        <div style="text-align: center; padding: 40px; color: #6b7280;">
          No data found for the selected criteria.
        </div>
      ` : ''}
      
      <div style="margin-top: 20px; font-size: 10px; color: #6b7280; text-align: center;">
        Generated on ${now.toLocaleString()} | Total Records: ${esp32_1_Rows.length + esp32_2_Rows.length}
      </div>
    </body>
    </html>
  `
  
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
      
      const printWindow = window.open('', '_blank')
      printWindow.document.write(tableContent)
      printWindow.document.close()
      printWindow.focus()
      printWindow.print()
    }
  }
}

// Watchers for print functionality
watch([() => printDateRange.value.start, () => printDateRange.value.end, () => printDevices.value], () => {
  if (printDataType.value === 'range') {
    estimateRecords()
  }
})

watch(() => printDataType.value, (newValue) => {
  if (newValue === 'range') {
    estimateRecords()
  } else {
    estimatedRecords.value = 0
  }
})

// Your existing methods and variables continue below...
// (All the existing methods like fetchSoilAnalysisData, fetchESP32_1_Data, etc. remain exactly the same)

// Filter and header definitions
const esp32_1_FilterFields = [
  { key: 'nitrogen', label: 'Nitrogen (mg/kg)' },
  { key: 'phosphorus', label: 'Phosphorus (mg/kg)' },
  { key: 'potassium', label: 'Potassium (mg/kg)' },
  { key: 'ph', label: 'pH Level' }
]

const esp32_2_FilterFields = [
  { key: 'temperature', label: 'Temperature (°C)' },
  { key: 'humidity', label: 'Humidity (%)' },
  { key: 'soilMoisture', label: 'Soil Moisture (%)' }
]

const esp32_1_Headers = [
  { key: 'timestamp', label: 'Date & Time' },
  { key: 'nitrogen', label: 'Nitrogen' },
  { key: 'phosphorus', label: 'Phosphorus' },
  { key: 'potassium', label: 'Potassium' },
  { key: 'ph', label: 'pH' }
]

const esp32_2_Headers = [
  { key: 'timestamp', label: 'Date & Time' },
  { key: 'temperature', label: 'Temperature' },
  { key: 'humidity', label: 'Humidity' },
  { key: 'soilMoisture', label: 'Soil Moisture' }
]

const exportFormats = ['csv', 'pdf']

// Set page methods with data fetching
const setESP32_1_Page = async (page) => {
  if (page !== '...' && page >= 1 && page <= esp32_1_PaginationMeta.value.totalPages) {
    await fetchESP32_1_Data(page)
  }
}

const setESP32_2_Page = async (page) => {
  if (page !== '...' && page >= 1 && page <= esp32_2_PaginationMeta.value.totalPages) {
    await fetchESP32_2_Data(page)
  }
}

// Dropdown positioning (unchanged)
const getDropdownStyle = (dropdownId) => {
  let buttonRef = null
  let containerRef = null

  if (dropdownId === 'filter-esp32-1') {
    buttonRef = filterButton1.value
    containerRef = esp32_1_Container.value
  } else if (dropdownId === 'sort-esp32-1') {
    buttonRef = sortButton1.value
    containerRef = esp32_1_Container.value
  } else if (dropdownId === 'filter-esp32-2') {
    buttonRef = filterButton2.value
    containerRef = esp32_2_Container.value
  } else if (dropdownId === 'sort-esp32-2') {
    buttonRef = sortButton2.value
    containerRef = esp32_2_Container.value
  }

  if (!buttonRef) return {}

  const btnRect = buttonRef.getBoundingClientRect()
  const viewportWidth = window.innerWidth
  const viewportHeight = window.innerHeight
  const containerRect = containerRef?.getBoundingClientRect?.() || {
    left: 0, top: 0, right: viewportWidth, bottom: viewportHeight, width: viewportWidth, height: viewportHeight
  }

  const isFilter = dropdownId.includes('filter')
  const preferredWidth = isFilter ? 288 : 192 // px
  const defaultHeight = isFilter ? 320 : 200  // px

  // Compute width that fits inside the container (with padding)
  const minWidth = 160
  const availableWidth = Math.max(minWidth, containerRect.width - 16)
  const actualWidth = Math.min(preferredWidth, availableWidth)

  const isMobile = window.matchMedia('(max-width: 768px)').matches

  // Horizontal positioning (clamped to container)
  const padding = 8
  const minLeft = containerRect.left + padding
  const maxLeft = containerRect.right - padding - actualWidth
  let left = Math.min(Math.max(btnRect.left, minLeft), Math.max(minLeft, maxLeft))

  // Always below button; scroll if not enough space (mobile priority)
  let top = btnRect.bottom + 8

  if (isMobile) {
    const bottomSpace = containerRect.bottom - padding - top
    const maxHeight = Math.max(120, Math.min(defaultHeight, bottomSpace))
    return {
      left: `${left}px`,
      top: `${top}px`,
      width: `${actualWidth}px`,
      maxHeight: `${maxHeight}px`
    }
  }

  // Desktop clamp inside container
  const maxTop = containerRect.bottom - padding - defaultHeight
  const minTop = containerRect.top + padding
  top = Math.min(Math.max(top, minTop), Math.max(minTop, maxTop))
  const maxHeight = Math.min(defaultHeight, containerRect.bottom - padding - top)

  return {
    left: `${left}px`,
    top: `${top}px`,
    width: `${actualWidth}px`,
    maxHeight: `${maxHeight}px`
  }
}

// Fetch data with pagination
const fetchESP32_1_Data = async (page = 1) => {
  try {
    const params = {
      page,
      limit: esp32_1_PaginationMeta.value.itemsPerPage,
      sortBy: esp32_1_SortKey.value,
      sortOrder: esp32_1_SortDirection.value
    }

    // Add search if exists
    if (esp32_1_SearchQuery.value) {
      params.search = esp32_1_SearchQuery.value
    }

    // Add global search if exists
    if (globalSearchQuery.value) {
      params.search = globalSearchQuery.value
    }

    // Add filters if any active
    const activeFilters = Object.keys(esp32_1_ActiveFilters.value).filter(key => 
      esp32_1_ActiveFilters.value[key].min !== '' || esp32_1_ActiveFilters.value[key].max !== ''
    )
    
    if (activeFilters.length > 0) {
      params.filters = JSON.stringify(esp32_1_ActiveFilters.value)
    }

    const response = await api.get(`/soil-analysis/esp32-1`, { params })
    esp32_1_Data.value = response.data.data
    esp32_1_PaginationMeta.value = response.data.pagination
    
    console.log(`✅ Fetched ${response.data.data.length} ESP32-1 readings (page ${page})`)
  } catch (error) {
    console.error("❌ Error fetching ESP32-1 data:", error)
  }
}

const fetchESP32_2_Data = async (page = 1) => {
  try {
    const params = {
      page,
      limit: esp32_2_PaginationMeta.value.itemsPerPage,
      sortBy: esp32_2_SortKey.value,
      sortOrder: esp32_2_SortDirection.value
    }

    // Add search if exists
    if (esp32_2_SearchQuery.value) {
      params.search = esp32_2_SearchQuery.value
    }

    // Add global search if exists
    if (globalSearchQuery.value) {
      params.search = globalSearchQuery.value
    }

    // Add filters if any active
    const activeFilters = Object.keys(esp32_2_ActiveFilters.value).filter(key => 
      esp32_2_ActiveFilters.value[key].min !== '' || esp32_2_ActiveFilters.value[key].max !== ''
    )
    
    if (activeFilters.length > 0) {
      params.filters = JSON.stringify(esp32_2_ActiveFilters.value)
    }

    const response = await api.get(`/soil-analysis/esp32-2`, { params })
    esp32_2_Data.value = response.data.data
    esp32_2_PaginationMeta.value = response.data.pagination
    
    console.log(`✅ Fetched ${response.data.data.length} ESP32-2 readings (page ${page})`)
  } catch (error) {
    console.error("❌ Error fetching ESP32-2 data:", error)
  }
}

// Main fetch function
const fetchSoilAnalysisData = async () => {
  try {
    isLoading.value = true
    await Promise.all([
      fetchESP32_1_Data(1),
      fetchESP32_2_Data(1)
    ])
    isLoading.value = false
  } catch (error) {
    console.error("❌ Error fetching soil analysis data:", error)
    isLoading.value = false
  }
}

// Search methods
const performESP32_1_Search = async () => {
  esp32_1_PaginationMeta.value.currentPage = 1
  await fetchESP32_1_Data(1)
}

const performESP32_2_Search = async () => {
  esp32_2_PaginationMeta.value.currentPage = 1
  await fetchESP32_2_Data(1)
}

const performGlobalSearch = async () => {
  esp32_1_PaginationMeta.value.currentPage = 1
  esp32_2_PaginationMeta.value.currentPage = 1
  await Promise.all([
    fetchESP32_1_Data(1),
    fetchESP32_2_Data(1)
  ])
}

// Filter methods
const applyESP32_1_Filters = async () => {
  const newFilters = {}
  Object.keys(esp32_1_Filters.value).forEach(key => {
    const min = parseFloat(esp32_1_Filters.value[key].min)
    const max = parseFloat(esp32_1_Filters.value[key].max)
    if (!isNaN(min) || !isNaN(max)) {
      newFilters[key] = { min: isNaN(min) ? '' : min, max: isNaN(max) ? '' : max }
    }
  })
  esp32_1_ActiveFilters.value = newFilters
  esp32_1_PaginationMeta.value.currentPage = 1
  await fetchESP32_1_Data(1)
  activeDropdown.value = null
}

const applyESP32_2_Filters = async () => {
  const newFilters = {}
  Object.keys(esp32_2_Filters.value).forEach(key => {
    const min = parseFloat(esp32_2_Filters.value[key].min)
    const max = parseFloat(esp32_2_Filters.value[key].max)
    if (!isNaN(min) || !isNaN(max)) {
      newFilters[key] = { min: isNaN(min) ? '' : min, max: isNaN(max) ? '' : max }
    }
  })
  esp32_2_ActiveFilters.value = newFilters
  esp32_2_PaginationMeta.value.currentPage = 1
  await fetchESP32_2_Data(1)
  activeDropdown.value = null
}

// Sort methods
const setESP32_1_SortKey = async (key) => {
  if (esp32_1_SortKey.value === key) {
    esp32_1_SortDirection.value = esp32_1_SortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    esp32_1_SortKey.value = key
    esp32_1_SortDirection.value = 'asc'
  }
  await fetchESP32_1_Data(1)
  activeDropdown.value = null
}

const setESP32_2_SortKey = async (key) => {
  if (esp32_2_SortKey.value === key) {
    esp32_2_SortDirection.value = esp32_2_SortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    esp32_2_SortKey.value = key
    esp32_2_SortDirection.value = 'asc'
  }
  await fetchESP32_2_Data(1)
  activeDropdown.value = null
}

// Pagination navigation
const nextESP32_1_Page = async () => {
  if (esp32_1_PaginationMeta.value.currentPage < esp32_1_PaginationMeta.value.totalPages) {
    await fetchESP32_1_Data(esp32_1_PaginationMeta.value.currentPage + 1)
  }
}

const prevESP32_1_Page = async () => {
  if (esp32_1_PaginationMeta.value.currentPage > 1) {
    await fetchESP32_1_Data(esp32_1_PaginationMeta.value.currentPage - 1)
  }
}

const nextESP32_2_Page = async () => {
  if (esp32_2_PaginationMeta.value.currentPage < esp32_2_PaginationMeta.value.totalPages) {
    await fetchESP32_2_Data(esp32_2_PaginationMeta.value.currentPage + 1)
  }
}

const prevESP32_2_Page = async () => {
  if (esp32_2_PaginationMeta.value.currentPage > 1) {
    await fetchESP32_2_Data(esp32_2_PaginationMeta.value.currentPage - 1)
  }
}

// Export function (uses separate endpoints for all data)
const exportAllData = async (format) => {
  try {
    isLoading.value = true
    console.log(`📤 Starting export in ${format.toUpperCase()} format...`)
    
    // For exports, fetch all data without pagination using the /all endpoints
    const [esp32_1_Response, esp32_2_Response] = await Promise.all([
      api.get('/soil-analysis/esp32-1/all'),
      api.get('/soil-analysis/esp32-2/all')
    ])

    console.log('✅ Export data fetched:', {
      esp32_1: esp32_1_Response.data.length,
      esp32_2: esp32_2_Response.data.length
    })

    const esp32_1_Headers = ['Date', 'Time', 'Device', 'Nitrogen (mg/kg)', 'Phosphorus (mg/kg)', 'Potassium (mg/kg)', 'pH Level']
    const esp32_2_Headers = ['Date', 'Time', 'Device', 'Temperature (°C)', 'Humidity (%)', 'Soil Moisture (%)']

    const esp32_1_Rows = esp32_1_Response.data.map(row => [
      row.date, 
      row.time, 
      row.deviceId || 'ESP32-1', 
      row.nitrogen, 
      row.phosphorus, 
      row.potassium, 
      row.ph
    ])
    
    const esp32_2_Rows = esp32_2_Response.data.map(row => [
      row.date, 
      row.time, 
      row.deviceId || 'ESP32-2', 
      row.temperature, 
      row.humidity, 
      row.soilMoisture
    ])

    if (format === 'csv') {
      let csvContent = 'ESP32-1 Data (NPK + pH Sensors)\n'
      csvContent += esp32_1_Headers.join(',') + '\n'
      esp32_1_Rows.forEach(row => { 
        csvContent += row.map(val => `"${val}"`).join(',') + '\n' 
      })
      csvContent += '\nESP32-2 Data (Environmental Sensors)\n'
      csvContent += esp32_2_Headers.join(',') + '\n'
      esp32_2_Rows.forEach(row => { 
        csvContent += row.map(val => `"${val}"`).join(',') + '\n' 
      })
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      saveAs(blob, `soil_analysis_data_${new Date().toISOString().split('T')[0]}.csv`)
      window.showToast && window.showToast(`Exported ${esp32_1_Rows.length + esp32_2_Rows.length} records as CSV`, 'success')
      
    } else if (format === 'pdf') {
      const doc = new jsPDF()
      const pageWidth = doc.internal.pageSize.getWidth()
      
      // Title
      doc.setFontSize(16)
      doc.setTextColor(16, 185, 129) // emerald color
      doc.text('Soil Analysis Data Report', pageWidth / 2, 15, { align: 'center' })
      
      // Date
      doc.setFontSize(10)
      doc.setTextColor(100, 100, 100)
      doc.text(`Generated on: ${new Date().toLocaleString()}`, pageWidth / 2, 22, { align: 'center' })
      
      // ESP32-1 Data
      doc.setFontSize(12)
      doc.setTextColor(0, 0, 0)
      doc.text(`ESP32-1: NPK + pH Sensors (${esp32_1_Rows.length} records)`, 14, 32)
      
      autoTable(doc, {
        head: [esp32_1_Headers],
        body: esp32_1_Rows,
        startY: 38,
        styles: { 
          fontSize: 8,
          cellPadding: 2
        },
        headStyles: {
          fillColor: [16, 185, 129],
          textColor: 255,
          fontStyle: 'bold'
        },
        alternateRowStyles: {
          fillColor: [245, 245, 245]
        },
        margin: { top: 10 }
      })
      
      let finalY = doc.lastAutoTable.finalY + 10
      
      // Check if we need a new page
      if (finalY > doc.internal.pageSize.getHeight() - 50) {
        doc.addPage()
        finalY = 20
      }
      
      // ESP32-2 Data
      doc.setFontSize(12)
      doc.text(`ESP32-2: Environmental Sensors (${esp32_2_Rows.length} records)`, 14, finalY)
      
      autoTable(doc, {
        head: [esp32_2_Headers],
        body: esp32_2_Rows,
        startY: finalY + 6,
        styles: { 
          fontSize: 8,
          cellPadding: 2
        },
        headStyles: {
          fillColor: [59, 130, 246],
          textColor: 255,
          fontStyle: 'bold'
        },
        alternateRowStyles: {
          fillColor: [245, 245, 245]
        }
      })
      
      // Summary
      finalY = doc.lastAutoTable.finalY + 10
      doc.setFontSize(9)
      doc.setTextColor(100, 100, 100)
      doc.text(`Total Records: ${esp32_1_Rows.length + esp32_2_Rows.length}`, 14, finalY)
      
      doc.save(`soil_analysis_data_${new Date().toISOString().split('T')[0]}.pdf`)
      window.showToast && window.showToast(`Exported ${esp32_1_Rows.length + esp32_2_Rows.length} records as PDF`, 'success')
    }
    
  } catch (error) {
    console.error('❌ Error exporting data:', error)
    console.error('Error details:', error.response?.data || error.message)
    window.showToast && window.showToast('Error exporting data. Please try again.', 'error')
  } finally {
    isLoading.value = false
    activeDropdown.value = null
  }
}


// Dropdown methods
const toggleDropdown = async (dropdownName) => {
  if (activeDropdown.value === dropdownName) {
    activeDropdown.value = null
    return
  }
  activeDropdown.value = dropdownName
  await nextTick()
}

const handleClickOutside = (event) => {
  if (!event.target.closest('.dropdown-panel') && !event.target.closest('.dropdown-trigger')) {
    activeDropdown.value = null
  }
}

// Real-time polling
const realTime = async () => {
  try {
    await Promise.all([
      fetchESP32_1_Data(esp32_1_PaginationMeta.value.currentPage),
      fetchESP32_2_Data(esp32_2_PaginationMeta.value.currentPage)
    ])
  } catch (error) {
    console.error("❌ Error fetching soil analysis data:", error)
  }
}

const pollingInterval = ref(null)
const pollingEnabled = ref(true)
const pollingIntervalTime = ref(30000) // 30 seconds

const startPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
  
  pollingInterval.value = setInterval(async () => {
    if (pollingEnabled.value) {
      console.log('🔄 Polling for new soil analysis data...')
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

// Watchers
watch([globalSearchQuery, esp32_1_SearchQuery, esp32_1_ActiveFilters], () => { 
  esp32_1_PaginationMeta.value.currentPage = 1 
})
watch([globalSearchQuery, esp32_2_SearchQuery, esp32_2_ActiveFilters], () => { 
  esp32_2_PaginationMeta.value.currentPage = 1 
})

// Event handlers
const handleResize = () => { if (activeDropdown.value) activeDropdown.value = null }
const handleAnyScroll = (e) => {
  if (e?.target && e.target.closest && e.target.closest('.dropdown-panel')) {
    return
  }
  if (activeDropdown.value) activeDropdown.value = null
}

// Lifecycle
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', handleResize)
  document.addEventListener('scroll', handleAnyScroll, true)
  fetchSoilAnalysisData()
  
  // Start polling after initial load
  setTimeout(() => {
    startPolling()
  }, 5000)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('scroll', handleAnyScroll, true)
  stopPolling()
})
</script>

<style scoped>
/* Your existing styles remain the same */
.overflow-auto::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.overflow-auto::-webkit-scrollbar-track { background: #f8fafc; }
.overflow-auto::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
.overflow-auto::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.table-fixed { table-layout: fixed; }
.transition-colors { transition: color 0.15s ease, background-color 0.15s ease, border-color 0.15s ease; }

tbody tr {
  border-bottom: 1px solid #cbcbcb !important;
}

tbody td:last-child {
  border-right: none;
}

tbody tr:hover { background-color: #f9fafb; }

@media (max-width: 1024px) {
  .flex-1 { width: 100%; }
  .flex.gap-4 { flex-direction: column; gap: 1rem ; }
}

.text-9px { font-size: 9px; line-height: 1.2; }
.text-10px { font-size: 10px; line-height: 1.3; }

.dropdown-panel {
  max-width: calc(100vw - 32px);
  max-height: calc(100vh - 40px);
  overflow-y: auto;
}

@media (max-width: 768px) {
  .dropdown-panel {
    -webkit-overflow-scrolling: touch;
  }
}
</style>