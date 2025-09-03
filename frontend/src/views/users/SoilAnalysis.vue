<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-full mx-auto w-[calc(100vw-15px)] h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-hidden min-w-0">
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
                @click="printTable"
                class="flex items-center gap-2 px-4 py-2 rounded-lg bg-green-500 text-white text-[10px] md:text-sm font-medium hover:bg-green-600 transition-colors shadow-sm"
              >
                <Printer class="h-4 w-4" />
                <span class="hidden md:block">Print All</span>
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
                {{ esp32_1_Data.length }} readings
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
              <div v-for="(row, index) in paginatedESP32_1_Data" :key="index" 
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
              
              <div v-if="paginatedESP32_1_Data.length === 0 && !isLoading" 
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
                      <th class="w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date & Time
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
                      <th class="w-[20%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-orange-600">pH</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(level)</div>
                      </th>
                    </tr>
                  </thead>

                  <tbody class="divide-y divide-gray-100">
                    <tr 
                      v-for="(row, index) in paginatedESP32_1_Data" 
                      :key="index"
                      class="hover:bg-gray-50 transition-colors"
                    >
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[10px] md:text-xs font-medium text-gray-900">{{ row.date }}</div>
                        <div class="text-[7px] md:text-[10px] text-gray-500">{{ row.time }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[10px] md:text-xs font-semibold text-green-600">{{ row.nitrogen }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[10px] md:text-xs font-semibold text-blue-600">{{ row.phosphorus }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[10px] md:text-xs font-semibold text-purple-600">{{ row.potassium }}</div>
                      </td>
                      <td class="w-[20%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[10px] md:text-xs font-semibold text-orange-600">{{ row.ph }}</div>
                      </td>
                    </tr>

                    <tr v-if="paginatedESP32_1_Data.length === 0 && !isLoading">
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
                  Showing {{ (esp32_1_CurrentPage - 1) * esp32_1_ItemsPerPage + 1 }} - {{ Math.min(esp32_1_CurrentPage * esp32_1_ItemsPerPage, sortedESP32_1_Data.length) }}
                  of {{ sortedESP32_1_Data.length }}
                </div>
                <div class="flex items-center gap-1">
                  <button 
                    @click="prevESP32_1_Page"
                    :disabled="esp32_1_CurrentPage === 1"
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
                        page === esp32_1_CurrentPage 
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
                    :disabled="esp32_1_CurrentPage >= esp32_1_TotalPages"
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
                {{ esp32_2_Data.length }} readings
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
              <div v-for="(row, index) in paginatedESP32_2_Data" :key="index" 
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
              
              <div v-if="paginatedESP32_2_Data.length === 0 && !isLoading" 
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
                      <th class="w-[25%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Date & Time
                      </th>
                      <th class="w-[25%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-red-600">Temperature</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(°C)</div>
                      </th>
                      <th class="w-[25%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-blue-600">Humidity</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(%)</div>
                      </th>
                      <th class="w-[25%] py-2.5 px-3 text-left text-[9px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-cyan-600">Soil Moisture</div>
                        <div class="text-gray-400 text-[6px] md:text-[9px]">(%)</div>
                      </th>
                    </tr>
                  </thead>
                  
                  <tbody class="divide-y divide-gray-100">
                    <tr 
                      v-for="(row, index) in paginatedESP32_2_Data" 
                      :key="index"
                      class="hover:bg-gray-50 transition-colors"
                    >
                      <td class="w-[25%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-medium text-gray-900">{{ row.date }}</div>
                        <div class="text-[7px] md:text-[10px] text-gray-500">{{ row.time }}</div>
                      </td>
                      <td class="w-[25%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-semibold text-red-600">{{ row.temperature }}</div>
                      </td>
                      <td class="w-[25%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-semibold text-blue-600">{{ row.humidity }}</div>
                      </td>
                      <td class="w-[25%] py-2.5 px-3 whitespace-nowrap">
                        <div class="text-[9px] md:text-xs font-semibold text-cyan-600">{{ row.soilMoisture }}</div>
                      </td>
                    </tr>
                    
                    <tr v-if="paginatedESP32_2_Data.length === 0 && !isLoading">
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
                  Showing {{ (esp32_2_CurrentPage - 1) * esp32_2_ItemsPerPage + 1 }} - {{ Math.min(esp32_2_CurrentPage * esp32_2_ItemsPerPage, sortedESP32_2_Data.length) }}
                  of {{ sortedESP32_2_Data.length }}
                </div>
                <div class="flex items-center gap-1">
                  <button 
                    @click="prevESP32_2_Page"
                    :disabled="esp32_2_CurrentPage === 1"
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
                        page === esp32_2_CurrentPage 
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
                    :disabled="esp32_2_CurrentPage >= esp32_2_TotalPages"
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

const isLoading = ref(true)

const esp32_1_Data = ref([]) 
const esp32_2_Data = ref([]) 

const globalSearchQuery = ref('')
const activeDropdown = ref(null)

const filterButton1 = ref(null)
const sortButton1 = ref(null)
const filterButton2 = ref(null)
const sortButton2 = ref(null)

const esp32_1_Container = ref(null)
const esp32_2_Container = ref(null)

const esp32_1_SearchQuery = ref('')
const esp32_1_ItemsPerPage = ref(10)
const esp32_1_CurrentPage = ref(1)
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
const esp32_2_ItemsPerPage = ref(10)
const esp32_2_CurrentPage = ref(1)
const esp32_2_SortKey = ref('timestamp')
const esp32_2_SortDirection = ref('desc')
const esp32_2_ActiveFilters = ref({})
const esp32_2_Filters = ref({
  temperature: { min: '', max: '' },
  humidity: { min: '', max: '' },
  soilMoisture: { min: '', max: '' }
})

const esp32_1_PaginationNumbers = computed(() => {
  const totalPages = esp32_1_TotalPages.value
  const currentPage = esp32_1_CurrentPage.value
  
  if (totalPages <= 1) return [1]
  
  if (currentPage === 1) {
    return [1, '..', totalPages]
  } else if (currentPage === totalPages) {
    return [1, '..', totalPages]
  } else {
    return [currentPage, '..', totalPages]
  }
})

const esp32_2_PaginationNumbers = computed(() => {
  const totalPages = esp32_2_TotalPages.value
  const currentPage = esp32_2_CurrentPage.value
  
  if (totalPages <= 1) return [1]
  
  if (currentPage === 1) {
    return [1, '..', totalPages]
  } else if (currentPage === totalPages) {
    return [1, '..', totalPages]
  } else {
    return [currentPage, '...', totalPages]
  }
})

// Keep the setPage methods
const setESP32_1_Page = (page) => {
  if (page !== '...' && page >= 1 && page <= esp32_1_TotalPages.value) {
    esp32_1_CurrentPage.value = page
  }
}

const setESP32_2_Page = (page) => {
  if (page !== '...' && page >= 1 && page <= esp32_2_TotalPages.value) {
    esp32_2_CurrentPage.value = page
  }
}

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

// Constrained dropdown positioning within each card/table container
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

// Fetch data
const fetchSoilAnalysisData = async () => {
  try {
    isLoading.value = true
    await fetchESP32_1_Data()
    await fetchESP32_2_Data()
    isLoading.value = false
  } catch (error) {
    console.error("❌ Error fetching soil analysis data:", error)
    isLoading.value = false
  }
}

const fetchESP32_1_Data = async () => {
  try {
    const response = await api.get(`/soil-analysis/esp32-1`)
    esp32_1_Data.value = response.data
    console.log(`✅ Fetched ${response.data.length} ESP32-1 readings`)
  } catch (error) {
    console.error("❌ Error fetching ESP32-1 data:", error)
  }
}

const fetchESP32_2_Data = async () => {
  try {
    const response = await api.get(`/soil-analysis/esp32-2`)
    esp32_2_Data.value = response.data
    console.log(`✅ Fetched ${response.data.length} ESP32-2 readings`)
  } catch (error) {
    console.error("❌ Error fetching ESP32-2 data:", error)
  }
}

// Date/time formatting
const formatDate = (date) => {
  if (!date) return '--'
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const day = date.getDate().toString().padStart(2, '0')
  const month = months[date.getMonth()]
  const year = date.getFullYear()
  return `${month} ${day}, ${year}`
}

const formatTime = (date) => {
  if (!date) return '--'
  let hours = date.getHours()
  const minutes = date.getMinutes().toString().padStart(2, '0')
  const ampm = hours >= 12 ? 'PM' : 'AM'
  hours = hours % 12
  hours = hours ? hours : 12
  const displayHours = hours.toString().padStart(2, '0')
  return `${displayHours}:${minutes} ${ampm}`
}

// ESP32-1 computed
const filteredESP32_1_Data = computed(() => {
  let result = [...esp32_1_Data.value]

  // Handle global search
  if (globalSearchQuery.value) {
    const q = globalSearchQuery.value.toLowerCase()
    result = result.filter(row => 
      Object.values(row).some(v => String(v).toLowerCase().includes(q))
    )
  }

  // Handle local search
  if (esp32_1_SearchQuery.value) {
    const q = esp32_1_SearchQuery.value.toLowerCase()
    result = result.filter(row => 
      Object.values(row).some(v => String(v).toLowerCase().includes(q))
    )
  }

  // Handle filters
  Object.keys(esp32_1_ActiveFilters.value).forEach(key => {
    const { min, max } = esp32_1_ActiveFilters.value[key]
    if (min !== '' && max !== '') {
      result = result.filter(row => parseFloat(row[key]) >= min && parseFloat(row[key]) <= max)
    } else if (min !== '') {
      result = result.filter(row => parseFloat(row[key]) >= min)
    } else if (max !== '') {
      result = result.filter(row => parseFloat(row[key]) <= max)
    }
  })

  return result
})

const sortedESP32_1_Data = computed(() => {
  if (!esp32_1_SortKey.value) return filteredESP32_1_Data.value

  return [...filteredESP32_1_Data.value].sort((a, b) => {
    let aValue = a[esp32_1_SortKey.value]
    let bValue = b[esp32_1_SortKey.value]
    if (aValue === '--') aValue = esp32_1_SortDirection.value === 'asc' ? -Infinity : Infinity
    if (bValue === '--') bValue = esp32_1_SortDirection.value === 'asc' ? -Infinity : Infinity
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return esp32_1_SortDirection.value === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
    }
    return esp32_1_SortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
  })
})

const paginatedESP32_1_Data = computed(() => {
  const startIndex = (esp32_1_CurrentPage.value - 1) * esp32_1_ItemsPerPage.value
  const endIndex = startIndex + esp32_1_ItemsPerPage.value
  return sortedESP32_1_Data.value.slice(startIndex, endIndex)
})

const esp32_1_TotalPages = computed(() => Math.ceil(sortedESP32_1_Data.value.length / esp32_1_ItemsPerPage.value))

// ESP32-2 computed - all filtering/sorting done on frontend
const filteredESP32_2_Data = computed(() => {
  let result = [...esp32_2_Data.value]

  // Handle global search
  if (globalSearchQuery.value) {
    const q = globalSearchQuery.value.toLowerCase()
    result = result.filter(row => 
      Object.values(row).some(v => String(v).toLowerCase().includes(q))
    )
  }

  // Handle local search
  if (esp32_2_SearchQuery.value) {
    const q = esp32_2_SearchQuery.value.toLowerCase()
    result = result.filter(row => 
      Object.values(row).some(v => String(v).toLowerCase().includes(q))
    )
  }

  // Handle filters
  Object.keys(esp32_2_ActiveFilters.value).forEach(key => {
    const { min, max } = esp32_2_ActiveFilters.value[key]
    if (min !== '' && max !== '') {
      result = result.filter(row => parseFloat(row[key]) >= min && parseFloat(row[key]) <= max)
    } else if (min !== '') {
      result = result.filter(row => parseFloat(row[key]) >= min)
    } else if (max !== '') {
      result = result.filter(row => parseFloat(row[key]) <= max)
    }
  })

  return result
})

const sortedESP32_2_Data = computed(() => {
  if (!esp32_2_SortKey.value) return filteredESP32_2_Data.value
  return [...filteredESP32_2_Data.value].sort((a, b) => {
    let aValue = a[esp32_2_SortKey.value]
    let bValue = b[esp32_2_SortKey.value]
    if (aValue === '--') aValue = esp32_2_SortDirection.value === 'asc' ? -Infinity : Infinity
    if (bValue === '--') bValue = esp32_2_SortDirection.value === 'asc' ? -Infinity : Infinity
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return esp32_2_SortDirection.value === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue)
    }
    return esp32_2_SortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
  })
})

const paginatedESP32_2_Data = computed(() => {
  const startIndex = (esp32_2_CurrentPage.value - 1) * esp32_2_ItemsPerPage.value
  const endIndex = startIndex + esp32_2_ItemsPerPage.value
  return sortedESP32_2_Data.value.slice(startIndex, endIndex)
})

const esp32_2_TotalPages = computed(() => Math.ceil(sortedESP32_2_Data.value.length / esp32_2_ItemsPerPage.value))


// Methods
const toggleDropdown = async (dropdownName) => {
  if (activeDropdown.value === dropdownName) {
    activeDropdown.value = null
    return
  }
  activeDropdown.value = dropdownName
  await nextTick()
}

const handleClickOutside = (event) => {
  // Close when clicking outside triggers and dropdown panels
  if (!event.target.closest('.dropdown-panel') && !event.target.closest('.dropdown-trigger')) {
    activeDropdown.value = null
  }
}

// ESP32-1 methods
const performESP32_1_Search = () => { esp32_1_CurrentPage.value = 1 }

const applyESP32_1_Filters = () => {
  const newFilters = {}
  Object.keys(esp32_1_Filters.value).forEach(key => {
    const min = parseFloat(esp32_1_Filters.value[key].min)
    const max = parseFloat(esp32_1_Filters.value[key].max)
    if (!isNaN(min) || !isNaN(max)) {
      newFilters[key] = { min: isNaN(min) ? '' : min, max: isNaN(max) ? '' : max }
    }
  })
  esp32_1_ActiveFilters.value = newFilters
  esp32_1_CurrentPage.value = 1
  activeDropdown.value = null
}

const setESP32_1_SortKey = (key) => {
  if (esp32_1_SortKey.value === key) {
    esp32_1_SortDirection.value = esp32_1_SortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    esp32_1_SortKey.value = key
    esp32_1_SortDirection.value = 'asc'
  }
  activeDropdown.value = null
}

const nextESP32_1_Page = () => { if (esp32_1_CurrentPage.value < esp32_1_TotalPages.value) esp32_1_CurrentPage.value++ }
const prevESP32_1_Page = () => { if (esp32_1_CurrentPage.value > 1) esp32_1_CurrentPage.value-- }

// ESP32-2 methods
const performESP32_2_Search = () => { esp32_2_CurrentPage.value = 1 }

const applyESP32_2_Filters = () => {
  const newFilters = {}
  Object.keys(esp32_2_Filters.value).forEach(key => {
    const min = parseFloat(esp32_2_Filters.value[key].min)
    const max = parseFloat(esp32_2_Filters.value[key].max)
    if (!isNaN(min) || !isNaN(max)) {
      newFilters[key] = { min: isNaN(min) ? '' : min, max: isNaN(max) ? '' : max }
    }
  })
  esp32_2_ActiveFilters.value = newFilters
  esp32_2_CurrentPage.value = 1
  activeDropdown.value = null
}

const setESP32_2_SortKey = (key) => {
  if (esp32_2_SortKey.value === key) {
    esp32_2_SortDirection.value = esp32_2_SortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    esp32_2_SortKey.value = key
    esp32_2_SortDirection.value = 'asc'
  }
  activeDropdown.value = null
}

const nextESP32_2_Page = () => { if (esp32_2_CurrentPage.value < esp32_2_TotalPages.value) esp32_2_CurrentPage.value++ }
const prevESP32_2_Page = () => { if (esp32_2_CurrentPage.value > 1) esp32_2_CurrentPage.value-- }

// Export functions
const exportAllData = async (format) => {
  const esp32_1_Headers = ['Date', 'Time', 'Device', 'Nitrogen', 'Phosphorus', 'Potassium', 'pH']
  const esp32_2_Headers = ['Date', 'Time', 'Device', 'Temperature', 'Humidity', 'Soil Moisture']

  const esp32_1_Rows = sortedESP32_1_Data.value.map(row => [
    row.date, row.time, row.deviceId, row.nitrogen, row.phosphorus, row.potassium, row.ph
  ])
  const esp32_2_Rows = sortedESP32_2_Data.value.map(row => [
    row.date, row.time, row.deviceId, row.temperature, row.humidity, row.soilMoisture
  ])

  if (format === 'csv') {
    let csvContent = 'ESP32-1 Data (NPK + pH)\n'
    csvContent += esp32_1_Headers.join(',') + '\n'
    esp32_1_Rows.forEach(row => { csvContent += row.map(val => `"${val}"`).join(',') + '\n' })
    csvContent += '\nESP32-2 Data (Environmental)\n'
    csvContent += esp32_2_Headers.join(',') + '\n'
    esp32_2_Rows.forEach(row => { csvContent += row.map(val => `"${val}"`).join(',') + '\n' })
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    saveAs(blob, 'soil_analysis_combined_data.csv')
    window.showToast && window.showToast('Soil Analysis exported as CSV', 'success')
  } else if (format === 'pdf') {
    const doc = new jsPDF()
    doc.text('ESP32-1 Data (NPK + pH)', 14, 16)
    autoTable(doc, { head: [esp32_1_Headers], body: esp32_1_Rows, startY: 22, styles: { fontSize: 9 } })
    let finalY = doc.lastAutoTable.finalY || 22
    doc.text('ESP32-2 Data (Environmental)', 14, finalY + 10)
    autoTable(doc, { head: [esp32_2_Headers], body: esp32_2_Rows, startY: finalY + 16, styles: { fontSize: 9 } })
    doc.save('soil_analysis_combined_data.pdf')
    window.showToast && window.showToast('Soil Analysis exported as PDF', 'success')
  }
  activeDropdown.value = null
}

const printTable = () => {
  // Close any open dropdowns
  activeDropdown.value = null
  
  // Get the current date for the header
  const now = new Date()
  const formattedDate = now.toLocaleDateString('en-US', { 
    weekday: 'long', 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric' 
  })
  
  // Format the data for printing
  const esp32_1_Rows = sortedESP32_1_Data.value.map(row => ({
    date: row.date,
    time: row.time,
    device: row.deviceId,
    nitrogen: row.nitrogen,
    phosphorus: row.phosphorus,
    potassium: row.potassium,
    ph: row.ph
  }))
  
  const esp32_2_Rows = sortedESP32_2_Data.value.map(row => ({
    date: row.date,
    time: row.time,
    device: row.deviceId,
    temperature: row.temperature,
    humidity: row.humidity,
    soilMoisture: row.soilMoisture
  }))
  
  // Create the HTML content
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
          font-size: 12px;
        }
        th, td {
          border: 1px solid #e5e7eb;
          padding: 8px 12px;
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
      </div>
      
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
      
      <div style="margin-top: 20px; font-size: 12px; color: #6b7280; text-align: center;">
        Generated on ${now.toLocaleString()}
      </div>
    </body>
    </html>
  `
  
  // Create a hidden iframe for printing
  const iframe = document.createElement('iframe')
  iframe.style.position = 'absolute'
  iframe.style.width = '0'
  iframe.style.height = '0'
  iframe.style.border = 'none'
  iframe.style.left = '-9999px' // Move off-screen
  document.body.appendChild(iframe)
  
  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document
  
  // Write content to iframe
  iframeDoc.open()
  iframeDoc.write(tableContent)
  iframeDoc.close()
  
  // Wait for iframe to load and then trigger print
  iframe.onload = function() {
    try {
      // Focus and print
      iframe.contentWindow.focus()
      iframe.contentWindow.print()
      
      // Remove the iframe after printing (with a delay to ensure print dialog shows)
      setTimeout(() => {
        document.body.removeChild(iframe)
      }, 100)
    } catch (error) {
      console.error('Print error:', error)
      document.body.removeChild(iframe)
      
      // Fallback to original method if iframe approach fails
      const printWindow = window.open('', '_blank')
      printWindow.document.write(tableContent)
      printWindow.document.close()
      printWindow.focus()
      printWindow.print()
    }
  }
}

// Watchers
watch([globalSearchQuery, esp32_1_SearchQuery, esp32_1_ActiveFilters], () => { esp32_1_CurrentPage.value = 1 })
watch([globalSearchQuery, esp32_2_SearchQuery, esp32_2_ActiveFilters], () => { esp32_2_CurrentPage.value = 1 })

// Close dropdowns on resize or page-level scrolls, but allow scrolling inside the panel
const handleResize = () => { if (activeDropdown.value) activeDropdown.value = null }
const handleAnyScroll = (e) => {
  if (e?.target && e.target.closest && e.target.closest('.dropdown-panel')) {
    // Allow internal panel scroll without closing
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
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', handleResize)
  document.removeEventListener('scroll', handleAnyScroll, true)
})
</script>

<style scoped>
/* Custom scrollbar for tables */
.overflow-auto::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
.overflow-auto::-webkit-scrollbar-track { background: #f8fafc; }
.overflow-auto::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 3px; }
.overflow-auto::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

/* Ensure table layout is fixed and columns align properly */
.table-fixed { table-layout: fixed; }

/* Smooth transitions */
.transition-colors { transition: color 0.15s ease, background-color 0.15s ease, border-color 0.15s ease; }

/* Table hover effects */
tbody tr:hover { background-color: #f9fafb; }

/* Responsive layout (unchanged) */
@media (max-width: 1024px) {
  .flex-1 { width: 100%; }
  .flex.gap-4 { flex-direction: column; gap: 1rem; }
}

.text-9px { font-size: 9px; line-height: 1.2; }
.text-10px { font-size: 10px; line-height: 1.3; }

/* Dropdown base: allow scrolling and momentum on mobile.
   The JS-inlined maxHeight will still cap the height precisely per container. */
.dropdown-panel {
  max-width: calc(100vw - 32px);
  max-height: calc(100vh - 40px);
  overflow-y: auto;
}

/* Mobile-specific improvements for better touch scrolling */
@media (max-width: 768px) {
  .dropdown-panel {
    -webkit-overflow-scrolling: touch;
  }
}
</style>