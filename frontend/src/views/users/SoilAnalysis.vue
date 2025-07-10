<template>
  <div class="h-screen flex bg-white font-poppins overflow-hidden">
    <main class="flex-1 flex flex-col h-screen pt-32">
      <div class="flex-1 w-full px-4 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
        <!-- Enhanced main container with more appealing design -->
        <div class="bg-white rounded-lg shadow-lg border border-gray-100 h-[calc(100vh-140px)] flex flex-col overflow-hidden">
          <!-- Keep original gradient header -->
          <div class="bg-gradient-to-r from-emerald-50 to-white p-5 border-b border-gray-100 rounded-t-lg">
            <!-- Header with controls aligned side by side -->
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
              <!-- Title and breadcrumb with enhanced styling -->
              <div>
                <h1 class="text-lg font-semibold text-gray-800 mb-1">Soil Analysis Measurements</h1>
                <div class="flex items-center text-sm text-gray-500">
                  <span class="text-emerald-600 font-medium">ESP32-1: NPK + pH Sensors</span>
                  <div class="w-1 h-1 rounded-full bg-gray-300 mx-2"></div>
                  <span class="text-emerald-600 font-medium">ESP32-2: Environmental Sensors</span>
                </div>
              </div>
              
              <!-- Global controls -->
              <div class="flex items-center gap-2">
                <!-- Global search bar -->
                <div class="relative w-64">
                  <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search all measurements..."
                    class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                    v-model="globalSearchQuery"
                    @input="performGlobalSearch"
                  />
                </div>

                <!-- Export Button -->
                <div class="relative">
                  <button 
                    @click.stop="toggleDropdown('export')"
                    class="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 text-white text-sm font-medium hover:bg-emerald-600 transition-colors shadow-sm"
                  >
                    <Download class="h-4 w-4" />
                    Export All
                    <ChevronDown class="h-4 w-4" :class="{ 'transform rotate-180': activeDropdown === 'export' }" />
                  </button>
                  
                  <div 
                    v-show="activeDropdown === 'export'"
                    class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
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

          <!-- Dual table container with proper spacing -->
          <div class="flex-1 overflow-hidden flex gap-4 p-4">
            <!-- ESP32-1 Table (NPK + pH) -->
            <div class="flex-1 bg-gray-50 rounded-xl border border-gray-200 flex flex-col overflow-hidden">
              <!-- ESP32-1 Header -->
              <div class="bg-white border-b border-gray-200 p-3">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center gap-2">
                    <div class="w-2 h-2 rounded-full bg-green-500"></div>
                    <div>
                      <h3 class="text-sm font-semibold text-gray-800">ESP32-1 Sensors</h3>
                      <p class="text-xs text-gray-500">NPK + Soil pH Measurements</p>
                    </div>
                  </div>
                  <div class="text-xs text-green-600 bg-green-100 px-2 py-1 rounded-full font-medium">
                    {{ esp32_1_Data.length }} readings
                  </div>
                </div>
                
                <!-- ESP32-1 Controls -->
                <div class="flex items-center gap-2">
                  <div class="relative flex-1">
                    <Search class="absolute left-2.5 top-1/2 transform -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search ESP32-1 data..."
                      class="w-full pl-8 pr-3 py-1.5 rounded-md border border-gray-200 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 text-xs"
                      v-model="esp32_1_SearchQuery"
                      @input="performESP32_1_Search"
                    />
                  </div>
                  
                  <button 
                    @click.stop="toggleDropdown('filter-esp32-1')"
                    class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-gray-200 bg-white text-xs text-gray-600 hover:text-green-600 transition-colors"
                  >
                    <Filter class="h-3.5 w-3.5" />
                    Filter
                  </button>
                  
                  <button 
                    @click.stop="toggleDropdown('sort-esp32-1')"
                    class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-gray-200 bg-white text-xs text-gray-600 hover:text-green-600 transition-colors"
                  >
                    <ArrowUpDown class="h-3.5 w-3.5" />
                    Sort
                  </button>
                </div>

                <!-- ESP32-1 Filter Dropdown -->
                <div 
                  v-show="activeDropdown === 'filter-esp32-1'"
                  class="absolute mt-2 w-72 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                  @click.stop
                >
                  <div class="p-3 space-y-3 max-h-[250px] overflow-y-auto">
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

                <!-- ESP32-1 Sort Dropdown -->
                <div 
                  v-show="activeDropdown === 'sort-esp32-1'"
                  class="absolute mt-2 w-40 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                  @click.stop
                >
                  <div class="py-1">
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

              <!-- ESP32-1 Table -->
              <div class="flex-1 overflow-hidden flex flex-col">
                <!-- Fixed Header -->
                <div class="bg-gray-50 border-b border-gray-200 sticky top-0 z-10">
                  <table class="min-w-full">
                    <thead>
                      <tr>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Date & Time
                        </th>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          <div class="text-green-600">Nitrogen</div>
                          <div class="text-gray-400 text-[9px]">(mg/kg)</div>
                        </th>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          <div class="text-blue-600">Phosphorus</div>
                          <div class="text-gray-400 text-[9px]">(mg/kg)</div>
                        </th>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          <div class="text-purple-600">Potassium</div>
                          <div class="text-gray-400 text-[9px]">(mg/kg)</div>
                        </th>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          <div class="text-orange-600">pH</div>
                          <div class="text-gray-400 text-[9px]">(level)</div>
                        </th>
                      </tr>
                    </thead>
                  </table>
                </div>
                
                <!-- Scrollable Body -->
                <div class="flex-1 overflow-y-auto bg-white">
                  <table class="min-w-full">
                    <tbody class="divide-y divide-gray-100">
                      <tr 
                        v-for="(row, index) in paginatedESP32_1_Data" 
                        :key="index"
                        class="hover:bg-gray-50 transition-colors"
                      >
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-medium text-gray-900">{{ row.date }}</div>
                          <div class="text-[10px] text-gray-500">{{ row.time }}</div>
                        </td>
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-semibold text-green-600">{{ row.nitrogen }}</div>
                        </td>
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-semibold text-blue-600">{{ row.phosphorus }}</div>
                        </td>
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-semibold text-purple-600">{{ row.potassium }}</div>
                        </td>
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-semibold text-orange-600">{{ row.ph }}</div>
                        </td>
                      </tr>
                      
                      <!-- Empty state -->
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

                <!-- ESP32-1 Pagination -->
                <div class="border-t border-gray-200 py-2 px-3 bg-gray-50">
                  <div class="flex items-center justify-between">
                    <div class="text-xs text-gray-600">
                      Showing {{ (esp32_1_CurrentPage - 1) * esp32_1_ItemsPerPage + 1 }} - {{ Math.min(esp32_1_CurrentPage * esp32_1_ItemsPerPage, sortedESP32_1_Data.length) }}
                      of {{ sortedESP32_1_Data.length }}
                    </div>
                    <div class="flex items-center gap-1">
                      <button 
                        @click="prevESP32_1_Page"
                        :disabled="esp32_1_CurrentPage === 1"
                        class="px-2 py-1 text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600"
                      >
                        <ChevronLeft class="w-3.5 h-3.5" />
                      </button>
                      <span class="px-2 py-1 text-xs bg-green-500 text-white rounded font-medium">{{ esp32_1_CurrentPage }}</span>
                      <button 
                        @click="nextESP32_1_Page"
                        :disabled="esp32_1_CurrentPage >= esp32_1_TotalPages"
                        class="px-2 py-1 text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-green-600"
                      >
                        <ChevronRight class="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- ESP32-2 Table (Environmental Sensors) -->
            <div class="flex-1 bg-gray-50 rounded-xl border border-gray-200 flex flex-col overflow-hidden">
              <!-- ESP32-2 Header -->
              <div class="bg-white border-b border-gray-200 p-3">
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center gap-2">
                    <div class="w-2 h-2 rounded-full bg-blue-500"></div>
                    <div>
                      <h3 class="text-sm font-semibold text-gray-800">ESP32-2 Sensors</h3>
                      <p class="text-xs text-gray-500">Environmental Measurements</p>
                    </div>
                  </div>
                  <div class="text-xs text-blue-600 bg-blue-100 px-2 py-1 rounded-full font-medium">
                    {{ esp32_2_Data.length }} readings
                  </div>
                </div>
                
                <!-- ESP32-2 Controls -->
                <div class="flex items-center gap-2">
                  <div class="relative flex-1">
                    <Search class="absolute left-2.5 top-1/2 transform -translate-y-1/2 h-3.5 w-3.5 text-gray-400" />
                    <input
                      type="text"
                      placeholder="Search ESP32-2 data..."
                      class="w-full pl-8 pr-3 py-1.5 rounded-md border border-gray-200 focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500 text-xs"
                      v-model="esp32_2_SearchQuery"
                      @input="performESP32_2_Search"
                    />
                  </div>
                  
                  <button 
                    @click.stop="toggleDropdown('filter-esp32-2')"
                    class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-gray-200 bg-white text-xs text-gray-600 hover:text-blue-600 transition-colors"
                  >
                    <Filter class="h-3.5 w-3.5" />
                    Filter
                  </button>
                  
                  <button 
                    @click.stop="toggleDropdown('sort-esp32-2')"
                    class="flex items-center gap-1.5 px-2.5 py-1.5 rounded-md border border-gray-200 bg-white text-xs text-gray-600 hover:text-blue-600 transition-colors"
                  >
                    <ArrowUpDown class="h-3.5 w-3.5" />
                    Sort
                  </button>
                </div>

                <!-- ESP32-2 Filter Dropdown -->
                <div 
                  v-show="activeDropdown === 'filter-esp32-2'"
                  class="absolute mt-2 w-72 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                  @click.stop
                >
                  <div class="p-3 space-y-3 max-h-[250px] overflow-y-auto">
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

                <!-- ESP32-2 Sort Dropdown -->
                <div 
                  v-show="activeDropdown === 'sort-esp32-2'"
                  class="absolute mt-2 w-40 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                  @click.stop
                >
                  <div class="py-1">
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

              <!-- ESP32-2 Table -->
              <div class="flex-1 overflow-hidden flex flex-col">
                <!-- Fixed Header -->
                <div class="bg-gray-50 border-b border-gray-200 sticky top-0 z-10">
                  <table class="min-w-full">
                    <thead>
                      <tr>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          Date & Time
                        </th>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          <div class="text-red-600">Temperature</div>
                          <div class="text-gray-400 text-[9px]">(°C)</div>
                        </th>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          <div class="text-blue-600">Humidity</div>
                          <div class="text-gray-400 text-[9px]">(%)</div>
                        </th>
                        <th class="py-2.5 px-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                          <div class="text-cyan-600">Soil Moisture</div>
                          <div class="text-gray-400 text-[9px]">(%)</div>
                        </th>
                      </tr>
                    </thead>
                  </table>
                </div>
                
                <!-- Scrollable Body -->
                <div class="flex-1 overflow-y-auto bg-white">
                  <table class="min-w-full">
                    <tbody class="divide-y divide-gray-100">
                      <tr 
                        v-for="(row, index) in paginatedESP32_2_Data" 
                        :key="index"
                        class="hover:bg-gray-50 transition-colors"
                      >
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-medium text-gray-900">{{ row.date }}</div>
                          <div class="text-[10px] text-gray-500">{{ row.time }}</div>
                        </td>
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-semibold text-red-600">{{ row.temperature }}</div>
                        </td>
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-semibold text-blue-600">{{ row.humidity }}</div>
                        </td>
                        <td class="py-2.5 px-3 whitespace-nowrap">
                          <div class="text-xs font-semibold text-cyan-600">{{ row.soilMoisture }}</div>
                        </td>
                      </tr>
                      
                      <!-- Empty state -->
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

                <!-- ESP32-2 Pagination -->
                <div class="border-t border-gray-200 py-2 px-3 bg-gray-50">
                  <div class="flex items-center justify-between">
                    <div class="text-xs text-gray-600">
                      Showing {{ (esp32_2_CurrentPage - 1) * esp32_2_ItemsPerPage + 1 }} - {{ Math.min(esp32_2_CurrentPage * esp32_2_ItemsPerPage, sortedESP32_2_Data.length) }}
                      of {{ sortedESP32_2_Data.length }}
                    </div>
                    <div class="flex items-center gap-1">
                      <button 
                        @click="prevESP32_2_Page"
                        :disabled="esp32_2_CurrentPage === 1"
                        class="px-2 py-1 text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-blue-600"
                      >
                        <ChevronLeft class="w-3.5 h-3.5" />
                      </button>
                      <span class="px-2 py-1 text-xs bg-blue-500 text-white rounded font-medium">{{ esp32_2_CurrentPage }}</span>
                      <button 
                        @click="nextESP32_2_Page"
                        :disabled="esp32_2_CurrentPage >= esp32_2_TotalPages"
                        class="px-2 py-1 text-xs rounded disabled:opacity-50 disabled:cursor-not-allowed text-gray-700 hover:text-blue-600"
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
    </main>

    <!-- Loading Page Component -->
    <LoadingPage 
      :isVisible="isLoading" 
      title="Loading Soil Analysis Data" 
      message="Fetching data from ESP32-1 and ESP32-2 sensors..."
    />

    <Settings />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { Search, Filter, Download, ChevronDown, ChevronRight, ChevronLeft, ArrowUpDown, FileText, FileSearch } from 'lucide-vue-next'
import Sidebar from '../layout/Sidebar.vue'
import LoadingPage from '../layout/LoadingPage.vue'
import Settings from '../layout/Settings.vue'
import {
  getFirestore,
  collection,
  query,
  orderBy,
  getDocs,
  limit
} from 'firebase/firestore'

const db = getFirestore()
const isLoading = ref(true)

// Separate data for each ESP32
const esp32_1_Data = ref([]) // NPK + pH data
const esp32_2_Data = ref([]) // Environmental data (temp, humidity, soil moisture)

// Global search
const globalSearchQuery = ref('')
const activeDropdown = ref(null)

// ESP32-1 state
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

// ESP32-2 state
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

const exportFormats = ['csv', 'pdf', 'docs']

// Fetch data from both ESP32 devices separately
const fetchSoilAnalysisData = async () => {
  try {
    isLoading.value = true
    
    // Fetch ESP32-1 data (NPK + pH)
    await fetchESP32_1_Data()
    
    // Fetch ESP32-2 data (Environmental)
    await fetchESP32_2_Data()
    
    isLoading.value = false
  } catch (error) {
    console.error("❌ Error fetching soil analysis data:", error)
    isLoading.value = false
  }
}

const fetchESP32_1_Data = async () => {
  try {
    const readingsQuery = query(
      collection(db, '3sensor_readings', 'esp32-1', 'readings'),
      orderBy('timestamp', 'desc'),
      limit(200)
    )
    
    const snapshot = await getDocs(readingsQuery)
    
    const processedData = snapshot.docs
      .filter(doc => {
        const data = doc.data()
        // Only include readings that have NPK or pH data
        return data.nitrogen !== undefined || data.phosphorus !== undefined || 
               data.potassium !== undefined || data.soilPh !== undefined
      })
      .map((doc, index) => {
        const data = doc.data()
        const timestamp = data.timestamp?.toDate ? data.timestamp.toDate() : new Date(data.timestamp.seconds * 1000)
        
        return {
          id: index + 1,
          timestamp: timestamp.getTime() / 1000,
          date: formatDate(timestamp),
          time: formatTime(timestamp),
          nitrogen: data.nitrogen !== undefined && data.nitrogen !== null ? Number(data.nitrogen).toFixed(2) : '--',
          phosphorus: data.phosphorus !== undefined && data.phosphorus !== null ? Number(data.phosphorus).toFixed(2) : '--',
          potassium: data.potassium !== undefined && data.potassium !== null ? Number(data.potassium).toFixed(2) : '--',
          ph: data.soilPh !== undefined && data.soilPh !== null ? Number(data.soilPh).toFixed(2) : '--',
          deviceId: 'esp32-1'
        }
      })
    
    esp32_1_Data.value = processedData
    console.log(`✅ Fetched ${processedData.length} ESP32-1 readings`)
  } catch (error) {
    console.error("❌ Error fetching ESP32-1 data:", error)
  }
}

const fetchESP32_2_Data = async () => {
  try {
    const readingsQuery = query(
      collection(db, '3sensor_readings', 'esp32-2', 'readings'),
      orderBy('timestamp', 'desc'),
      limit(200)
    )
    
    const snapshot = await getDocs(readingsQuery)
    
    const processedData = snapshot.docs
      .filter(doc => {
        const data = doc.data()
        // Only include readings that have environmental data
        return data.temperature !== undefined || data.humidity !== undefined || data.soilMoisture !== undefined
      })
      .map((doc, index) => {
        const data = doc.data()
        const timestamp = data.timestamp?.toDate ? data.timestamp.toDate() : new Date(data.timestamp.seconds * 1000)
        
        return {
          id: index + 1,
          timestamp: timestamp.getTime() / 1000,
          date: formatDate(timestamp),
          time: formatTime(timestamp),
          temperature: data.temperature !== undefined && data.temperature !== null ? Number(data.temperature).toFixed(2) : '--',
          humidity: data.humidity !== undefined && data.humidity !== null ? Number(data.humidity).toFixed(2) : '--',
          soilMoisture: data.soilMoisture !== undefined && data.soilMoisture !== null ? Number(data.soilMoisture).toFixed(2) : '--',
          deviceId: 'esp32-2'
        }
      })
    
    esp32_2_Data.value = processedData
    console.log(`✅ Fetched ${processedData.length} ESP32-2 readings`)
  } catch (error) {
    console.error("❌ Error fetching ESP32-2 data:", error)
  }
}

// Date and time formatting functions
const formatDate = (date) => {
  if (!date) return '--'
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
  const day = date.getDate().toString().padStart(2, '0')
  const month = months[date.getMonth()]
  const year = date.getFullYear()
  return `${month} ${day}, ${year}`
}

// MODIFIED: Convert military time to 12-hour format with AM/PM
const formatTime = (date) => {
  if (!date) return '--'
  let hours = date.getHours()
  const minutes = date.getMinutes().toString().padStart(2, '0')
  const ampm = hours >= 12 ? 'PM' : 'AM'
  
  // Convert 24-hour to 12-hour format
  hours = hours % 12
  hours = hours ? hours : 12 // 0 should be 12
  const displayHours = hours.toString().padStart(2, '0')
  
  return `${displayHours}:${minutes} ${ampm}`
}

// ESP32-1 computed properties
const filteredESP32_1_Data = computed(() => {
  let result = [...esp32_1_Data.value]

  // Apply global search
  if (globalSearchQuery.value) {
    const query = globalSearchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  // Apply ESP32-1 specific search
  if (esp32_1_SearchQuery.value) {
    const query = esp32_1_SearchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  // Apply range filters
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
      return esp32_1_SortDirection.value === 'asc' 
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }
    
    return esp32_1_SortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
  })
})

const paginatedESP32_1_Data = computed(() => {
  const startIndex = (esp32_1_CurrentPage.value - 1) * esp32_1_ItemsPerPage.value
  const endIndex = startIndex + esp32_1_ItemsPerPage.value
  return sortedESP32_1_Data.value.slice(startIndex, endIndex)
})

const esp32_1_TotalPages = computed(() => {
  return Math.ceil(sortedESP32_1_Data.value.length / esp32_1_ItemsPerPage.value)
})

// ESP32-2 computed properties
const filteredESP32_2_Data = computed(() => {
  let result = [...esp32_2_Data.value]

  // Apply global search
  if (globalSearchQuery.value) {
    const query = globalSearchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  // Apply ESP32-2 specific search
  if (esp32_2_SearchQuery.value) {
    const query = esp32_2_SearchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  // Apply range filters
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
      return esp32_2_SortDirection.value === 'asc' 
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }
    
    return esp32_2_SortDirection.value === 'asc' ? aValue - bValue : bValue - aValue
  })
})

const paginatedESP32_2_Data = computed(() => {
  const startIndex = (esp32_2_CurrentPage.value - 1) * esp32_2_ItemsPerPage.value
  const endIndex = startIndex + esp32_2_ItemsPerPage.value
  return sortedESP32_2_Data.value.slice(startIndex, endIndex)
})

const esp32_2_TotalPages = computed(() => {
  return Math.ceil(sortedESP32_2_Data.value.length / esp32_2_ItemsPerPage.value)
})

// Methods
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

// Global search
const performGlobalSearch = () => {
  esp32_1_CurrentPage.value = 1
  esp32_2_CurrentPage.value = 1
}

// ESP32-1 methods
const performESP32_1_Search = () => {
  esp32_1_CurrentPage.value = 1
}

const applyESP32_1_Filters = () => {
  const newFilters = {}
  Object.keys(esp32_1_Filters.value).forEach(key => {
    const min = parseFloat(esp32_1_Filters.value[key].min)
    const max = parseFloat(esp32_1_Filters.value[key].max)
    
    if (!isNaN(min) || !isNaN(max)) {
      newFilters[key] = {
        min: isNaN(min) ? '' : min,
        max: isNaN(max) ? '' : max
      }
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

const nextESP32_1_Page = () => {
  if (esp32_1_CurrentPage.value < esp32_1_TotalPages.value) {
    esp32_1_CurrentPage.value++
  }
}

const prevESP32_1_Page = () => {
  if (esp32_1_CurrentPage.value > 1) {
    esp32_1_CurrentPage.value--
  }
}

// ESP32-2 methods
const performESP32_2_Search = () => {
  esp32_2_CurrentPage.value = 1
}

const applyESP32_2_Filters = () => {
  const newFilters = {}
  Object.keys(esp32_2_Filters.value).forEach(key => {
    const min = parseFloat(esp32_2_Filters.value[key].min)
    const max = parseFloat(esp32_2_Filters.value[key].max)
    
    if (!isNaN(min) || !isNaN(max)) {
      newFilters[key] = {
        min: isNaN(min) ? '' : min,
        max: isNaN(max) ? '' : max
      }
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

const nextESP32_2_Page = () => {
  if (esp32_2_CurrentPage.value < esp32_2_TotalPages.value) {
    esp32_2_CurrentPage.value++
  }
}

const prevESP32_2_Page = () => {
  if (esp32_2_CurrentPage.value > 1) {
    esp32_2_CurrentPage.value--
  }
}

// Export functions
const exportAllData = (format) => {
  if (format === 'csv') {
    exportAsCSV()
  } else if (format === 'pdf') {
    exportAsPDF()
  } else if (format === 'docs') {
    exportAsDocs()
  }
  activeDropdown.value = null
}

const exportAsCSV = () => {
  // Combine both datasets for export
  const esp32_1_Headers = ['Date', 'Time', 'Device', 'Nitrogen', 'Phosphorus', 'Potassium', 'pH']
  const esp32_2_Headers = ['Date', 'Time', 'Device', 'Temperature', 'Humidity', 'Soil Moisture']
  
  let csvContent = 'ESP32-1 Data (NPK + pH)\n'
  csvContent += esp32_1_Headers.join(',') + '\n'
  
  sortedESP32_1_Data.value.forEach(row => {
    csvContent += `${row.date},${row.time},${row.deviceId},${row.nitrogen},${row.phosphorus},${row.potassium},${row.ph}\n`
  })
  
  csvContent += '\n\nESP32-2 Data (Environmental)\n'
  csvContent += esp32_2_Headers.join(',') + '\n'
  
  sortedESP32_2_Data.value.forEach(row => {
    csvContent += `${row.date},${row.time},${row.deviceId},${row.temperature},${row.humidity},${row.soilMoisture}\n`
  })

  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', 'soil_analysis_combined_data.csv')
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const exportAsPDF = () => {
  alert('PDF export would be implemented with a library like jsPDF')
}

const exportAsDocs = () => {
  alert('DOCS export would be implemented with a library for document generation')
}

// Watch for changes that should reset pagination
watch([globalSearchQuery, esp32_1_SearchQuery, esp32_1_ActiveFilters], () => {
  esp32_1_CurrentPage.value = 1
})

watch([globalSearchQuery, esp32_2_SearchQuery, esp32_2_ActiveFilters], () => {
  esp32_2_CurrentPage.value = 1
})

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  fetchSoilAnalysisData()
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Custom scrollbar for tables */
.overflow-y-auto::-webkit-scrollbar {
  width: 4px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: #f8fafc;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Smooth transitions */
.transition-colors {
  transition: color 0.15s ease, background-color 0.15s ease, border-color 0.15s ease;
}

/* Table hover effects */
tbody tr:hover {
  background-color: #f9fafb;
}

/* Responsive design */
@media (max-width: 1024px) {
  .flex-1 {
    width: 100%;
  }
  
  .flex.gap-4 {
    flex-direction: column;
    gap: 1rem;
  }
}

.text-9px {
  font-size: 9px;
  line-height: 1.2;
}

.text-10px {
  font-size: 10px;
  line-height: 1.3;
}
</style>