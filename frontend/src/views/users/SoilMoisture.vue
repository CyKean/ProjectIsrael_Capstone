<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">        <!-- Gradient header for visual appeal -->      <!-- Gradient header for visual appeal -->
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
          <div class="flex flex-col sm:flex-row items-stretch gap-2">
            <!-- Search bar - full width on mobile, fixed width on larger screens -->
            <div class="relative flex-1 sm:w-56 md:w-72 min-w-0">
              <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search measurements..."
                class="w-full pl-10 pr-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 text-xs sm:text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                v-model="searchQuery"
                @input="performSearch"
              />
            </div>

            <!-- Button group - horizontal on all screens but wraps if needed -->
            <div class="flex flex-wrap sm:flex-nowrap gap-2">
              <!-- Filter Button -->
              <div class="relative flex-1 sm:flex-none min-w-[100px]">
                <button 
                  @click.stop="toggleDropdown('filter')"
                  class="w-full flex items-center justify-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 bg-white text-xs sm:text-sm text-gray-700 hover:text-emerald-600 transition-colors shadow-sm"
                >
                  <Filter class="h-3 sm:h-4 w-3 sm:w-4 text-gray-500" />
                  <span>Filter</span>
                  <ChevronDown class="h-3 sm:h-4 w-3 sm:w-4 text-gray-400" :class="{ 'transform rotate-180': activeDropdown === 'filter' }" />
                </button>
                
                <div 
                  v-show="activeDropdown === 'filter'"
                  class="fixed sm:absolute left-4 right-4 sm:left-auto sm:right-0 mt-2 w-auto sm:w-[250px] md:w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                  @click.stop
                >
                  <div class="p-3 sm:p-4 space-y-3 sm:space-y-4 max-h-[60vh] sm:max-h-[400px] md:w-[400px] overflow-y-auto">
                    <div v-for="field in filterFields" :key="field.key" class="space-y-2">
                      <label class="block text-xs sm:text-sm font-medium text-gray-700">{{ field.label }}</label>
                      <div class="flex items-center gap-2">
                        <input
                          v-model="filters[field.key].min"
                          type="number"
                          placeholder="Min"
                          class="w-full px-3 py-1.5 text-xs sm:text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
                        />
                        <span class="text-gray-400">-</span>
                        <input
                          v-model="filters[field.key].max"
                          type="number"
                          placeholder="Max"
                          class="w-full px-3 py-1.5 text-xs sm:text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
                        />
                      </div>
                    </div>
                    <button 
                      @click="applyFilters"
                      class="w-full px-4 py-2 bg-emerald-500 text-white rounded-lg text-xs sm:text-sm font-medium hover:bg-emerald-600 transition-colors"
                    >
                      Apply Filters
                    </button>
                  </div>
                </div>
              </div>

              <!-- Sort Button -->
              <div class="relative flex-1 sm:flex-none min-w-[100px]">
                <button 
                  @click.stop="toggleDropdown('sort')"
                  class="w-full flex items-center justify-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg border border-gray-200 bg-white text-xs sm:text-sm text-gray-700 hover:text-emerald-600 transition-colors shadow-sm"
                >
                  <ArrowUpDown class="h-3 sm:h-4 w-3 sm:w-4 text-gray-500" />
                  <span>Sort</span>
                  <ChevronDown class="h-3 sm:h-4 w-3 sm:w-4 text-gray-400" :class="{ 'transform rotate-180': activeDropdown === 'sort' }" />
                </button>
                
                <div 
                  v-show="activeDropdown === 'sort'"
                  class="fixed sm:absolute left-4 right-4 sm:left-auto sm:right-0 mt-2 w-auto sm:w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                  @click.stop
                >
                  <div class="py-1">
                    <button
                      v-for="header in headers"
                      :key="header.key"
                      @click="setSortKey(header.key)"
                      class="w-full px-4 py-2 text-left text-xs sm:text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between"
                    >
                      {{ header.label }}
                      <ArrowUpDown v-if="sortKey === header.key" class="h-3 w-3 text-emerald-500" />
                    </button>
                  </div>
                </div>
              </div>

              <!-- Export Button -->
              <div class="relative flex-1 sm:flex-none min-w-[100px]">
                <button 
                  @click.stop="toggleDropdown('export')"
                  class="w-full flex items-center justify-center gap-2 px-3 sm:px-4 py-2 sm:py-2.5 rounded-lg bg-emerald-500 text-white text-xs sm:text-sm font-medium hover:bg-emerald-600 transition-colors shadow-sm"
                >
                  <Download class="h-3 sm:h-4 w-3 sm:w-4" />
                  <span>Export</span>
                  <ChevronDown class="h-3 sm:h-4 w-3 sm:w-4" :class="{ 'transform rotate-180': activeDropdown === 'export' }" />
                </button>
                
                <div 
                  v-show="activeDropdown === 'export'"
                  class="fixed sm:absolute left-4 right-4 sm:left-auto sm:right-0 mt-2 w-auto sm:w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                  @click.stop
                >
                  <div class="py-1">
                    <button
                      v-for="format in exportFormats"
                      :key="format"
                      @click="exportData(format)"
                      class="w-full px-4 py-2 text-left text-xs sm:text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                    >
                      <span v-if="format === 'csv'" class="mr-2 text-emerald-500"><FileText class="h-4 w-4" /></span>
                      <span v-else-if="format === 'pdf'" class="mr-2 text-red-500"><FileText class="h-4 w-4" /></span>
                      Export as {{ format.toUpperCase() }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Table and Graph Section - Flex container for side-by-side layout -->
      <div class="flex-1 overflow-auto md:overflow-hidden flex flex-col md:flex-row">
        <!-- Live Graph Container - Smaller width compared to table, now scrollable -->
        <div class="w-full md:w-1/3 lg:w-1/3 border-r border-gray-200 bg-white p-4 md:overflow-y-auto">
          <div class="mb-3">
            <h3 class="text-sm font-semibold text-gray-700">Live Soil Moisture</h3>
            <p class="text-xs text-gray-500">Real-time monitoring</p>
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
          <!-- Single Table Structure for Perfect Alignment -->
          <div class="flex-1 overflow-auto">
            <table class="w-full min-w-[600px] table-fixed">
              <!-- Fixed Header -->
              <thead class="sticky top-0 z-10 bg-gray-50 border-b border-gray-200">
                <tr>
                  <th class="w-[10%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium text-gray-500 uppercase tracking-wider">
                    ID
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-blue-600">Soil Moisture</div>
                    <div class="text-gray-400 text-[10px]">PERCENTAGE (%)</div>
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-emerald-600">Soil Status</div>
                    <div class="text-gray-400 text-[10px]">CONDITION</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-gray-600">Date</div>
                    <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider">
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
                  <td class="w-[10%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-700">{{ row.id }}</div>
                  </td>
                  <td class="w-[25%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium text-blue-600">
                      {{ row.soilMoisture }}
                    </div>
                  </td>
                  <td class="w-[25%] px-4 py-3.5 whitespace-nowrap">
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
                  <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-700">{{ row.date }}</div>
                  </td>
                  <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
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
      </div>

      <!-- Fixed Pagination Section with enhanced styling -->
      <div class="border-t border-gray-100 py-3 sm:py-4 px-4 sm:px-6 bg-gradient-to-r from-white to-emerald-50 rounded-b-lg">
        <!-- Enhanced Pagination -->
        <div class="flex flex-col md:flex-row items-center justify-between gap-3 sm:gap-4">
          <!-- Entries selector and info -->
          <div class="text-xs sm:text-sm text-gray-600 flex flex-col md:flex-row items-center gap-2">
            <div class="flex items-center gap-2">
              <span class="hidden sm:inline">Showing</span>
              <select 
                v-model="itemsPerPage" 
                class="bg-white border border-gray-200 rounded-lg px-2 py-1 text-xs sm:text-sm font-medium text-gray-700 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 shadow-sm"
                @change="updatePagination"
              >
                <option value="20">20</option>
                <option value="25">25</option>
                <option value="30">30</option>
                <option value="50">50</option>
              </select>
              <span class="hidden sm:inline">entries per page</span>
            </div>
            <span class="hidden xs:inline text-gray-400 mx-2">|</span>
            <span class="text-center xs:text-left">
              {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, sortedData.length) }}
              <span class="text-gray-400">of</span>
              {{ sortedData.length }}
            </span>
          </div>

          <!-- Page navigation -->
          <div class="flex items-center gap-1">
            <button 
              @click="prevPage"
              :disabled="currentPage === 1"
              class="inline-flex items-center justify-center px-2 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm font-medium transition-colors rounded-md
                disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                enabled:text-gray-700 enabled:hover:text-emerald-600 enabled:hover:bg-emerald-50"
            >
              <ChevronLeft class="w-3 sm:w-4 h-3 sm:h-4 mr-0 sm:mr-1" />
              <span class="hidden xs:inline">Prev</span>
            </button>

            <div class="flex items-center">
              <button
                v-for="page in displayedPages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'relative inline-flex items-center justify-center w-6 sm:w-8 h-6 sm:h-8 text-xs sm:text-sm transition-colors mx-0.5 rounded-md',
                  page === currentPage
                    ? 'text-white bg-emerald-500 font-semibold'
                    : page === '...'
                      ? 'cursor-default text-gray-400'
                      : 'text-gray-700 hover:text-emerald-600 hover:hover:bg-emerald-50'
                ]"
              >
                {{ page }}
              </button>
            </div>

            <button 
              @click="nextPage"
              :disabled="currentPage >= totalPages"
              class="inline-flex items-center justify-center px-2 sm:px-3 py-1 sm:py-1.5 text-xs sm:text-sm font-medium transition-colors rounded-md
                disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                enabled:text-gray-700 enabled:hover:text-emerald-600 enabled:hover:bg-emerald-50"
            >
              <span class="hidden xs:inline">Next</span>
              <ChevronRight class="w-3 sm:w-4 h-3 sm:h-4 ml-0 sm:ml-1" />
            </button>
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
  <!-- <Settings /> -->
</template>
  
<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
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
  onSnapshot,
  limit,
  Timestamp
} from 'firebase/firestore'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun } from 'docx'
import { saveAs } from 'file-saver'

// Chart.js import
import Chart from 'chart.js/auto'

const db = getFirestore()
const soilMoistureData = ref([])
const isLoading = ref(true)

// Chart references
const chartCanvas = ref(null)
const chart = ref(null)

// Chart data
const chartData = ref([])

// Current values and stats
const currentMoistureValue = ref('--')
const lastUpdated = ref('--')
const moistureStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})

// Prefetch data cache
const dataCache = ref(null)

// ✅ MODIFIED: Updated to fetch from new 3sensor_readings collection structure
const fetchSoilMoistureData = async () => {
  try {
    // If we already have cached data, use it immediately to show something
    if (dataCache.value) {
      soilMoistureData.value = dataCache.value
      isLoading.value = false
      initializeChartData(dataCache.value)
    } else {
      isLoading.value = true
    }
    
    // Fetch from all ESP32 devices that might have soil moisture data
    const allReadings = []
    
    // Fetch from esp32-2 (primary soil moisture sensor)
    try {
      const esp32_2_query = query(
        collection(db, "3sensor_readings", "esp32-2", "readings"),
        orderBy("timestamp", "desc")
      )
      const esp32_2_snapshot = await getDocs(esp32_2_query)
      
      esp32_2_snapshot.docs.forEach(doc => {
        const data = doc.data()
        if (data.soilMoisture !== undefined && data.soilMoisture !== null) {
          allReadings.push({
            ...data,
            deviceId: 'esp32-2',
            docId: doc.id
          })
        }
      })
      console.log(`📥 ESP32-2 Soil Moisture readings: ${esp32_2_snapshot.docs.length}`)
    } catch (error) {
      console.error("❌ Error fetching from ESP32-2:", error)
    }

    // Fetch from esp32-1 (backup soil moisture sensor if available)
    try {
      const esp32_1_query = query(
        collection(db, "3sensor_readings", "esp32-1", "readings"),
        orderBy("timestamp", "desc")
      )
      const esp32_1_snapshot = await getDocs(esp32_1_query)
      
      esp32_1_snapshot.docs.forEach(doc => {
        const data = doc.data()
        if (data.soilMoisture !== undefined && data.soilMoisture !== null) {
          allReadings.push({
            ...data,
            deviceId: 'esp32-1',
            docId: doc.id
          })
        }
      })
      console.log(`📥 ESP32-1 Soil Moisture readings: ${esp32_1_snapshot.docs.length}`)
    } catch (error) {
      console.error("❌ Error fetching from ESP32-1:", error)
    }

    // Fetch from esp32-3 (additional soil moisture sensor if available)
    try {
      const esp32_3_query = query(
        collection(db, "3sensor_readings", "esp32-3", "readings"),
        orderBy("timestamp", "desc")
      )
      const esp32_3_snapshot = await getDocs(esp32_3_query)
      
      esp32_3_snapshot.docs.forEach(doc => {
        const data = doc.data()
        if (data.soilMoisture !== undefined && data.soilMoisture !== null) {
          allReadings.push({
            ...data,
            deviceId: 'esp32-3',
            docId: doc.id
          })
        }
      })
      console.log(`📥 ESP32-3 Soil Moisture readings: ${esp32_3_snapshot.docs.length}`)
    } catch (error) {
      console.error("❌ Error fetching from ESP32-3:", error)
    }

    // Sort all readings by timestamp (newest first)
    allReadings.sort((a, b) => {
      const aTime = a.timestamp instanceof Timestamp ? a.timestamp.toDate() : new Date(a.timestamp.seconds * 1000)
      const bTime = b.timestamp instanceof Timestamp ? b.timestamp.toDate() : new Date(b.timestamp.seconds * 1000)
      return bTime - aTime
    })

    // Process soil moisture readings
    const processedData = allReadings
      .filter(reading => reading.soilMoisture !== undefined)
      .map((reading, index) => {
        // Handle timestamp
        let formattedDate = '--'
        let formattedTime = '--'
        let timestampSeconds = 0
        
        try {
          const timestamp = reading.timestamp instanceof Timestamp 
            ? reading.timestamp.toDate() 
            : new Date(reading.timestamp.seconds * 1000)
          
          // Format date as "MMM DD, YYYY" (e.g., "May 09, 2024")
          formattedDate = timestamp.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit'
          });

          // ✅ MODIFIED: Changed hour12 from false to true for 12-hour format
          formattedTime = timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          });
          
          timestampSeconds = reading.timestamp instanceof Timestamp 
            ? reading.timestamp.seconds 
            : timestamp.getTime() / 1000
        } catch (e) {
          console.error("Error formatting date:", e)
        }

        // Calculate soil status based on moisture level
        const soilMoisture = reading.soilMoisture !== undefined && reading.soilMoisture !== null 
          ? Number(reading.soilMoisture).toFixed(2) 
          : '--'
        
        const soilStatus = calculateSoilStatus(Number(reading.soilMoisture))

        // Return processed data
        return {
          id: index + 1,
          timestamp: timestampSeconds,
          soilMoisture: soilMoisture,
          soilStatus: soilStatus,
          date: formattedDate,
          time: formattedTime,
          rawTimestamp: reading.timestamp,
          deviceId: reading.deviceId
        }
      })

    // Cache the data for future use
    dataCache.value = processedData
    
    // Update the UI with minimal delay
    soilMoistureData.value = processedData
    isLoading.value = false
    
    // Initialize chart data after loading
    initializeChartData(processedData)
    
    console.log(`✅ Total processed soil moisture readings: ${processedData.length}`)
  } catch (error) {
    console.error("❌ Error fetching soil moisture data:", error)
    isLoading.value = false
    
    // If we have cached data, use it as fallback
    if (dataCache.value) {
      soilMoistureData.value = dataCache.value
      initializeChartData(dataCache.value)
    }
  }
}

// ✅ MODIFIED: Updated real-time listener for new collection structure
const setupRealtimeListener = () => {
  // Set up listeners for all ESP32 devices
  const unsubscribeFunctions = []
  
  // ESP32-2 listener (primary soil moisture sensor)
  const esp32_2_query = query(
    collection(db, "3sensor_readings", "esp32-2", "readings"),
    orderBy("timestamp", "desc"),
    limit(10)
  )
  
  const unsubscribe2 = onSnapshot(esp32_2_query, (snapshot) => {
    processRealtimeSnapshot(snapshot, 'esp32-2')
  }, (error) => {
    console.error("Error in ESP32-2 realtime listener:", error)
  })
  
  unsubscribeFunctions.push(unsubscribe2)

  // ESP32-1 listener (backup soil moisture sensor)
  const esp32_1_query = query(
    collection(db, "3sensor_readings", "esp32-1", "readings"),
    orderBy("timestamp", "desc"),
    limit(10)
  )
  
  const unsubscribe1 = onSnapshot(esp32_1_query, (snapshot) => {
    processRealtimeSnapshot(snapshot, 'esp32-1')
  }, (error) => {
    console.error("Error in ESP32-1 realtime listener:", error)
  })
  
  unsubscribeFunctions.push(unsubscribe1)

  // Return a function that unsubscribes from all listeners
  return () => {
    unsubscribeFunctions.forEach(unsubscribe => unsubscribe())
  }
}

// Process realtime snapshot data
let debounceTimer = null
let lastUpdateTime = Date.now()
let combinedRealtimeData = []

const processRealtimeSnapshot = (snapshot, deviceId) => {
  // Debounce updates to prevent too frequent rendering
  if (debounceTimer) clearTimeout(debounceTimer)
  
  // If it's been less than 500ms since the last update, debounce
  const now = Date.now()
  const timeSinceLastUpdate = now - lastUpdateTime
  
  if (timeSinceLastUpdate < 500) {
    debounceTimer = setTimeout(() => updateRealtimeData(snapshot, deviceId), 500 - timeSinceLastUpdate)
  } else {
    updateRealtimeData(snapshot, deviceId)
    lastUpdateTime = now
  }
}

const updateRealtimeData = (snapshot, deviceId) => {
  // Process the data for the chart
  const newData = snapshot.docs
    .filter(doc => doc.data().soilMoisture !== undefined)
    .map(doc => {
      const data = doc.data()
      const timestamp = data.timestamp instanceof Timestamp 
        ? data.timestamp.toDate() 
        : new Date(data.timestamp.seconds * 1000)
      
      return {
        timestamp,
        value: Number(data.soilMoisture),
        deviceId
      }
    })
  
  // Update combined realtime data
  combinedRealtimeData = combinedRealtimeData.filter(item => item.deviceId !== deviceId)
  combinedRealtimeData.push(...newData)
  
  // Sort by timestamp and keep only the most recent 20 readings
  combinedRealtimeData.sort((a, b) => a.timestamp - b.timestamp)
  combinedRealtimeData = combinedRealtimeData.slice(-20)
  
  // Update chart data
  chartData.value = combinedRealtimeData
  
  // Update current value and stats
  if (combinedRealtimeData.length > 0) {
    // Get the most recent value
    const latestReading = combinedRealtimeData[combinedRealtimeData.length - 1]
    currentMoistureValue.value = latestReading.value.toFixed(2)
    
    // ✅ MODIFIED: Changed hour12 from false to true for 12-hour format
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    
    // Calculate stats
    const values = combinedRealtimeData.map(item => item.value)
    moistureStats.value = {
      min: Math.min(...values).toFixed(2),
      max: Math.max(...values).toFixed(2),
      avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2)
    }
  }
  
  // Use requestAnimationFrame for smoother chart updates
  requestAnimationFrame(() => {
    updateChart()
  })
}

// Initialize chart data from fetched data
const initializeChartData = (data) => {
  // Take the most recent 20 entries for initial chart data
  const initialChartData = data.slice(0, 20)
    .map(item => ({
      timestamp: item.rawTimestamp instanceof Timestamp 
        ? item.rawTimestamp.toDate() 
        : new Date(item.rawTimestamp.seconds * 1000),
      value: Number(item.soilMoisture),
      deviceId: item.deviceId || 'unknown'
    }))
    .sort((a, b) => a.timestamp - b.timestamp) // Sort by timestamp ascending for the chart
  
  chartData.value = initialChartData
  combinedRealtimeData = initialChartData
  
  // Set initial current value and stats
  if (initialChartData.length > 0) {
    const latestReading = initialChartData[initialChartData.length - 1]
    currentMoistureValue.value = latestReading.value.toFixed(2)
    
    // ✅ MODIFIED: Changed hour12 from false to true for 12-hour format
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    
    const values = initialChartData.map(item => item.value)
    moistureStats.value = {
      min: Math.min(...values).toFixed(2),
      max: Math.max(...values).toFixed(2),
      avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2)
    }
  }
  
  // Initialize the chart
  initializeChart()
}

// Initialize the chart with enhanced styling
const initializeChart = () => {
  nextTick(() => {
    if (chartCanvas.value) {
      // Destroy existing chart if it exists
      if (chart.value) {
        chart.value.destroy()
      }
      
      const ctx = chartCanvas.value.getContext('2d')
      
      // Create new chart with enhanced styling
      chart.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.value.map(item => {
            // ✅ MODIFIED: Changed hour12 from false to true for 12-hour format
            return item.timestamp.toLocaleTimeString('en-US', {
              hour: '2-digit',
              minute: '2-digit',
              hour12: true
            })
          }),
          datasets: [{
            label: 'Soil Moisture (%)',
            data: chartData.value.map(item => item.value),
            borderColor: '#10b981', // emerald-500
            backgroundColor: 'rgba(16, 185, 129, 0.15)', // emerald-500 with opacity
            borderWidth: 2.5,
            tension: 0.4,
            fill: true,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#10b981',
            pointBorderWidth: 1.5
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
            duration: 500, // Reduced for better performance
            easing: 'easeOutQuart'
          },
          layout: {
            padding: {
              top: 10,
              left: 10,
              right: 10,
              bottom: 10
            }
          },
          scales: {
            y: {
              beginAtZero: false,
              min: Math.max(0, Math.floor(moistureStats.value.min * 0.95)),
              max: Math.min(100, Math.ceil(moistureStats.value.max * 1.05)),
              title: {
                display: true,
                text: 'Moisture (%)',
                color: '#10b981',
                font: {
                  size: 11,
                  weight: '600'
                },
                padding: {
                  bottom: 10
                }
              },
              ticks: {
                font: {
                  size: 10
                },
                color: '#64748b', // slate-500
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
                color: '#64748b' // slate-500
              },
              grid: {
                display: false,
                drawBorder: false
              }
            }
          },
          plugins: {
            legend: {
              display: false, // Hide legend to improve performance
            },
            tooltip: {
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              titleColor: '#334155', // slate-700
              bodyColor: '#334155', // slate-700
              borderColor: '#e2e8f0', // slate-200
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
                  return `Moisture: ${context.raw.toFixed(2)}%`;
                }
              }
            }
          }
        }
      })
    }
  })
}

// Update the chart with new data - optimized for performance
const updateChart = () => {
  if (chart.value && chartData.value.length > 0) {
    // Update only what's needed
    chart.value.data.labels = chartData.value.map(item => {
      // ✅ MODIFIED: Changed hour12 from false to true for 12-hour format
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    
    // Update dataset
    chart.value.data.datasets[0].data = chartData.value.map(item => item.value)
    
    // Update y-axis scale based on new data
    chart.value.options.scales.y.min = Math.max(0, Math.floor(moistureStats.value.min * 0.95))
    chart.value.options.scales.y.max = Math.min(100, Math.ceil(moistureStats.value.max * 1.05))
    
    // Use a more performant update
    chart.value.update('none') // 'none' mode skips animations for better performance
  }
}

// Function to determine soil status based on moisture level
const calculateSoilStatus = (moisture) => {
  if (moisture >= 70) return 'WET'
  if (moisture >= 30 && moisture < 70) return 'MEDIUM'
  return 'DRY'
}

// Initialize filters object
const filters = ref({
  soilMoisture: { min: '', max: '' }
})

// Reactive state
const searchQuery = ref('')
const itemsPerPage = ref(20) // Default to 20 items per page
const currentPage = ref(1)
const activeDropdown = ref(null)
const sortKey = ref('id')
const sortDirection = ref('asc')
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

// Computed properties with memoization for better performance
const filteredData = computed(() => {
  let result = [...soilMoistureData.value]

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  // Apply range filters
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
    
    // Handle empty values
    if (aValue === '' || aValue === undefined) aValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    if (bValue === '' || bValue === undefined) bValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    
    // Handle string comparison
    if (typeof aValue === 'string' && typeof bValue === 'string') {
      return sortDirection.value === 'asc' 
        ? aValue.localeCompare(bValue)
        : bValue.localeCompare(aValue)
    }
    
    // Handle numeric comparison
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
    // If 7 or fewer pages, show all
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // Always show first page
    pages.push(1)

    if (current <= 3) {
      // If near start, show 2-5 then ellipsis
      pages.push(2, 3, 4, 5, '...', total)
    } else if (current >= total - 2) {
      // If near end, show ellipsis then last 4
      pages.push('...', total - 4, total - 3, total - 2, total - 1, total)
    } else {
      // Otherwise show ellipsis, current -1, current, current + 1, ellipsis
      pages.push('...', current - 1, current, current + 1, '...', total)
    }
  }

  return pages
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

const performSearch = () => {
  currentPage.value = 1 // Reset to first page when searching
}

const applyFilters = () => {
  // Create a new object with only the filters that have values
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
  currentPage.value = 1 // Reset to first page when filtering
  activeDropdown.value = null // Close dropdown after applying
}

const setSortKey = (key) => {
  if (sortKey.value === key) {
    // Toggle direction if clicking the same column
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortDirection.value = 'asc' // Default to ascending for new column
  }
  activeDropdown.value = null // Close dropdown after sorting
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
  currentPage.value = 1 // Reset to first page when changing items per page
}

const goToPage = (page) => {
  if (typeof page === 'number') {
    currentPage.value = page
  }
}

const exportData = async (format) => {
  // Get the data to export (all filtered and sorted data, not just current page)
  const dataToExport = sortedData.value
  if (!dataToExport.length) return

  // Prepare headers and rows
  const exportHeaders = headers.map(h => h.label)
  const exportRows = dataToExport.map(row =>
    headers.map(header => row[header.key] ?? '')
  )

  if (format === 'csv') {
    // CSV Export
    let csvContent = exportHeaders.join(',') + '\n'
    exportRows.forEach(row => {
      csvContent += row.map(val => `"${val}"`).join(',') + '\n'
    })
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    saveAs(blob, 'soil_moisture_data.csv')
    window.showToast('Soil Moisture exported as CSV', 'success')
  } else if (format === 'pdf') {
    // PDF Export with graph
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm'
    })
    
    // Add title
    doc.setFontSize(16)
    doc.text('Soil Moisture Data Report', 105, 15, { align: 'center' })
    
    // Add current date
    doc.setFontSize(10)
    const dateStr = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
    doc.text(`Generated on: ${dateStr}`, 105, 22, { align: 'center' })
    
    // Add summary stats
    doc.setFontSize(12)
    doc.text('Current Moisture Status:', 15, 30)
    doc.text(`Value: ${currentMoistureValue.value}%`, 15, 36)
    doc.text(`Status: ${calculateSoilStatus(currentMoistureValue.value)}`, 15, 42)
    
    // Add the chart image
    if (chartCanvas.value) {
      // Convert canvas to image data URL
      const canvas = chartCanvas.value
      const chartImage = canvas.toDataURL('image/png')
      
      // Add chart image to PDF (centered, with some margin)
      const imgWidth = 180 // mm
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      doc.addImage(chartImage, 'PNG', (210 - imgWidth) / 2, 50, imgWidth, imgHeight)
      
      // Add stats below the chart
      doc.setFontSize(10)
      doc.text('Moisture Statistics:', 15, 50 + imgHeight + 10)
      doc.text(`Minimum: ${moistureStats.value.min}%`, 15, 50 + imgHeight + 16)
      doc.text(`Average: ${moistureStats.value.avg}%`, 15, 50 + imgHeight + 22)
      doc.text(`Maximum: ${moistureStats.value.max}%`, 15, 50 + imgHeight + 28)
      
      // Add the data table on a new page
      doc.addPage()
      doc.setFontSize(14)
      doc.text('Soil Moisture Data Table', 105, 15, { align: 'center' })
      autoTable(doc, {
        head: [exportHeaders],
        body: exportRows,
        startY: 22,
        styles: { 
          fontSize: 8,
          cellPadding: 2,
          overflow: 'linebreak'
        },
        headStyles: {
          fillColor: [16, 185, 129], // emerald-500
          textColor: 255 // white
        },
        alternateRowStyles: {
          fillColor: [241, 245, 249] // slate-50
        },
        margin: { top: 20 }
      })
    } else {
      // Fallback if chart isn't available
      doc.text('Soil Moisture Chart Not Available', 105, 50, { align: 'center' })
      autoTable(doc, {
        head: [exportHeaders],
        body: exportRows,
        startY: 60,
        styles: { fontSize: 10 }
      })
    }
    
    doc.save('soil_moisture_report.pdf')
    window.showToast('Soil Moisture report exported as PDF', 'success')
  } else if (format === 'docs') {
    // Word Export (DOCX)
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
          new Paragraph({ text: 'Soil Moisture Data Table', heading: 'Heading1' }),
          new Table({ rows: tableRows })
        ]
      }]
    })
    const buffer = await Packer.toBlob(docxDoc)
    saveAs(buffer, 'soil_moisture_data.docx')
  }

  activeDropdown.value = null // Close dropdown after exporting
}

// Watch for changes that should reset pagination
watch([searchQuery, activeFilters, itemsPerPage], () => {
  currentPage.value = 1
})

// Cleanup function for chart and listener
let unsubscribe = null

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  // Implement progressive loading strategy
  // 1. First try to get data from cache (if any)
  // 2. Then fetch fresh data
  fetchSoilMoistureData()
  
  // Set up realtime listener
  unsubscribe = setupRealtimeListener()
  
  // Set up window resize handler for chart responsiveness
  const handleResize = () => {
    if (chart.value) {
      chart.value.resize()
    }
  }
  
  // Use ResizeObserver for better performance than window resize
  if (typeof ResizeObserver !== 'undefined') {
    const resizeObserver = new ResizeObserver(handleResize)
    if (chartCanvas.value) {
      resizeObserver.observe(chartCanvas.value.parentElement)
    }
  } else {
    // Fallback to window resize
    window.addEventListener('resize', handleResize)
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  
  // Clean up chart
  if (chart.value) {
    chart.value.destroy()
  }
  
  // Clean up realtime listener
  if (unsubscribe) {
    unsubscribe()
  }
  
  // Remove resize listener
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