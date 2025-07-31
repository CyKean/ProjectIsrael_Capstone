<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-15px)] h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-hidden">
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
          <div class="flex items-center gap-2 flex-wrap md:flex-nowrap">
            <!-- Wider search bar -->
            <div class="relative w-72">
              <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search measurements..."
                class="w-full pl-10 pr-4 py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 text-xs md:text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                v-model="searchQuery"
                @input="performSearch"
              />
            </div>

            <!-- Filter Button with enhanced styling -->
            <div class="relative">
              <button 
                @click.stop="toggleDropdown('filter')"
                class="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-gray-200 bg-white text-xs md:text-sm text-gray-700 hover:text-emerald-600 transition-colors shadow-sm"
              >
                <Filter class="h-3 w-3 md:h-4 md:w-4 text-gray-500" />
                Filter
                <ChevronDown class="h-4 w-4 text-gray-400" :class="{ 'transform rotate-180': activeDropdown === 'filter' }" />
              </button>
              
              <div 
                v-show="activeDropdown === 'filter'"
                class="absolute w-[250px] md:right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                @click.stop
              >
                <div class="p-4 space-y-4 max-h-[400px] overflow-y-auto">
                  <div v-for="field in filterFields" :key="field.key" class="space-y-2">
                    <label class="block text-xs md:text-sm font-medium text-gray-700">{{ field.label }}</label>
                    <div class="flex items-center gap-2">
                      <input
                        v-model="filters[field.key].min"
                        type="number"
                        placeholder="Min"
                        class="w-full px-3 py-1.5 text-xs md:text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
                      />
                      <span class="text-gray-400">-</span>
                      <input
                        v-model="filters[field.key].max"
                        type="number"
                        placeholder="Max"
                        class="w-full px-3 py-1.5 text-xs md:text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
                      />
                    </div>
                  </div>
                  <button 
                    @click="applyFilters"
                    class="w-full px-4 py-2 bg-emerald-500 text-white rounded-lg text-xs md:text-sm font-medium hover:bg-emerald-600 transition-colors"
                  >
                    Apply Filters
                  </button>
                </div>
              </div>
            </div>

            <!-- Sort Button with enhanced styling -->
            <div class="relative">
              <button 
                @click.stop="toggleDropdown('sort')"
                class="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-gray-200 bg-white text-xs md:text-sm text-gray-700 hover:text-emerald-600 transition-colors shadow-sm"
              >
                <ArrowUpDown class="h-3 w-3 md:h-4 md:w-4 text-gray-500" />
                Sort
                <ChevronDown class="h-4 w-4 text-gray-400" :class="{ 'transform rotate-180': activeDropdown === 'sort' }" />
              </button>
              
              <div 
                v-show="activeDropdown === 'sort'"
                class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                @click.stop
              >
                <div class="py-1">
                  <button
                    v-for="header in headers"
                    :key="header.key"
                    @click="setSortKey(header.key)"
                    class="w-full px-4 py-2 text-left text-xs md:text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between"
                  >
                    {{ header.label }}
                    <ArrowUpDown v-if="sortKey === header.key" class="h-3 w-3 text-emerald-500" />
                  </button>
                </div>
              </div>
            </div>

            <!-- Export Button with enhanced styling -->
            <div class="relative">
              <button 
                @click.stop="toggleDropdown('export')"
                class="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-emerald-500 text-white text-xs md:text-sm font-medium hover:bg-emerald-600 transition-colors shadow-sm"
              >
                <Download class="h-3 w-3 md:h-4 md:w-4" />
                Export
                <ChevronDown class="h-4 w-4" :class="{ 'transform rotate-180': activeDropdown === 'export' }" />
              </button>
              
              <div 
                v-show="activeDropdown === 'export'"
                class="absolute md:right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                @click.stop
              >
                <div class="py-1">
                  <button
                    v-for="format in exportFormats"
                    :key="format"
                    @click="exportData(format)"
                    class="w-full px-4 py-2 text-left text-xs md:text-sm text-gray-700 hover:bg-gray-50 flex items-center"
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

      <!-- Table and Graph Section - Flex container for side-by-side layout -->
      <div class="flex-1 overflow-auto md:overflow-hidden flex flex-col md:flex-row">
        <!-- Live Graph Container - Smaller width compared to table, now scrollable -->
        <div class="w-full md:w-1/3 lg:w-1/3 border-r border-gray-200 bg-white p-4 md:overflow-y-auto">
          <div class="mb-3">
            <h3 class="text-xs md:text-sm font-semibold text-gray-700">Live Temperature & Humidity</h3>
            <p class="text-[10px] md:text-xs text-gray-500">Real-time monitoring</p>
          </div>
          
          <!-- Enhanced Combined Graph Container -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
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
            
            <!-- Graph Canvas with current values overlay -->
            <div class="h-[280px] p-3 relative">
              <canvas ref="chartCanvas" class="w-full h-full"></canvas>
              
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
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4">
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
        
        <!-- Table Container - Larger width -->
        <div class="w-full md:w-2/3 lg:w-2/3 flex flex-col">
          <!-- Fixed Header with enhanced styling -->
          <div class="w-full border-b border-gray-200 sticky top-0 z-10 bg-gray-50">
            <table class="hidden md:block min-w-full">
              <thead>
                <tr>
                  <th class="w-[10%] py-3.5 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    ID
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-red-600">Temperature</div>
                    <div class="text-gray-400 text-[10px]">(°C)</div>
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-blue-600">Humidity</div>
                    <div class="text-gray-400 text-[10px]">(%)</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-gray-600">Date</div>
                    <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-gray-600">Time</div>
                    <div class="text-gray-400 text-[10px]">HH:MM:SS</div>
                  </th>
                </tr>
              </thead>
            </table>
          </div>
          
          <!-- Scrollable Body with enhanced styling -->
          <div class="flex-1 overflow-y-auto">
            <table class="w-[600px] min-w-full">
              <thead class="md:hidden">
                <tr>
                  <th class="w-[10%] py-3.5 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    ID
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-red-600">Temperature</div>
                    <div class="text-gray-400 text-[10px]">(°C)</div>
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-blue-600">Humidity</div>
                    <div class="text-gray-400 text-[10px]">(%)</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-gray-600">Date</div>
                    <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-gray-600">Time</div>
                    <div class="text-gray-400 text-[10px]">HH:MM:SS</div>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr 
                  v-for="(row, index) in paginatedData" 
                  :key="index"
                  class="border-b border-gray-50 last:border-0"
                >
                  <td class="w-[10%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-700">{{ row.id }}</div>
                  </td>
                  <td class="w-[25%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium" :class="getTemperatureTextClass(row.temperature)">
                      {{ row.temperature }}°C
                    </div>
                  </td>
                  <td class="w-[25%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium" :class="getHumidityTextClass(row.humidity)">
                      {{ row.humidity }}%
                    </div>
                  </td>
                  <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-700">{{ row.date }}</div>
                  </td>
                  <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-700">{{ row.time }}</div>
                  </td>
                </tr>
                <!-- Empty state when no data - Enhanced styling -->
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
      </div>

      <!-- Fixed Pagination Section with enhanced styling -->
      <div class="border-t border-gray-100 py-4 px-6 bg-gradient-to-r from-white to-emerald-50 rounded-b-lg">
        <!-- Enhanced Pagination -->
        <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div class="text-xs md:text-sm text-gray-600 flex items-center gap-2">
            <span class="hidden sm:inline">Showing</span>
            <select 
              v-model="itemsPerPage" 
              class="bg-white border border-gray-200 rounded-lg px-2 py-1.5 text-xs md:text-sm font-medium text-gray-700 focus:outline-none focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500 shadow-sm"
              @change="updatePagination"
            >
              <option value="20">20</option>
              <option value="25">25</option>
              <option value="30">30</option>
              <option value="50">50</option>
            </select>
            <span class="hidden sm:inline">entries per page</span>
            <span class="text-gray-400 mx-2 hidden sm:inline">|</span>
            <span>
              {{ (currentPage - 1) * itemsPerPage + 1 }} - {{ Math.min(currentPage * itemsPerPage, sortedData.length) }}
              <span class="text-gray-400">of</span>
              {{ sortedData.length }}
            </span>
          </div>

          <div class="flex items-center gap-1">
            <button 
              @click="prevPage"
              :disabled="currentPage === 1"
              class="inline-flex items-center justify-center px-3 py-1.5 text-xs md:text-sm font-medium transition-colors rounded-md
                disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                enabled:text-gray-700 enabled:hover:text-emerald-600 enabled:hover:bg-emerald-50"
            >
              <ChevronLeft class="w-4 h-4 mr-1" />
              Prev
            </button>

            <div class="flex items-center">
              <button
                v-for="page in displayedPages"
                :key="page"
                @click="goToPage(page)"
                :class="[
                  'relative inline-flex items-center justify-center w-8 h-8 text-xs md:text-sm transition-colors mx-0.5 rounded-md',
                  page === currentPage
                    ? 'text-white bg-emerald-500 font-semibold'
                    : page === '...'
                      ? 'cursor-default text-gray-400'
                      : 'text-gray-700 hover:text-emerald-600 hover:bg-emerald-50'
                ]"
              >
                {{ page }}
              </button>
            </div>

            <button 
              @click="nextPage"
              :disabled="currentPage >= totalPages"
              class="inline-flex items-center justify-center px-3 py-1.5 text-xs md:text-sm font-medium transition-colors rounded-md
                disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                enabled:text-gray-700 enabled:hover:text-emerald-600 enabled:hover:bg-emerald-50"
            >
              Next
              <ChevronRight class="w-4 h-4 ml-1" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Loading Page Component -->
  <!-- <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Temperature & Humidity Data" 
    message="Please wait while we fetch the latest temperature and humidity measurements"
  />
  <Settings /> -->
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
  limit
} from 'firebase/firestore'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun } from 'docx'
import { saveAs } from 'file-saver'

// Chart.js import
import Chart from 'chart.js/auto'

const db = getFirestore()
const tempHumidityData = ref([])
const isLoading = ref(true)

// Chart references
const chartCanvas = ref(null)
const chart = ref(null)

// Chart data
const chartData = ref([])

// Current values and stats
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

// Prefetch data cache
const dataCache = ref(null)

// ✅ UPDATED: Modified to fetch from new 3sensor_readings collection structure
const fetchTempHumidityData = async () => {
  try {
    // If we already have cached data, use it immediately to show something
    if (dataCache.value) {
      tempHumidityData.value = dataCache.value
      isLoading.value = false
      initializeChartData(dataCache.value)
    } else {
      isLoading.value = true
    }
    
    // Fetch from the new 3sensor_readings collection structure
    const allReadings = []
    const deviceIds = ['esp32-1', 'esp32-2', 'esp32-3']
    
    // Fetch readings from all devices
    for (const deviceId of deviceIds) {
      try {
        const readingsQuery = query(
          collection(db, '3sensor_readings', deviceId, 'readings'),
          orderBy('timestamp', 'desc'),
          limit(100) // Limit per device to avoid too much data
        )
        
        const snapshot = await getDocs(readingsQuery)
        
        snapshot.docs.forEach(doc => {
          const data = doc.data()
          const timestamp = data.timestamp
          const jsDate = timestamp?.toDate ? timestamp.toDate() : new Date(timestamp.seconds * 1000)

          // Only include readings that have both temperature and humidity
          if (data.temperature !== undefined && data.humidity !== undefined) {
            allReadings.push({
              id: doc.id,
              deviceId: deviceId,
              ...data,
              timestamp: jsDate,
            })
          }
        })
        
        console.log(`✅ Fetched ${snapshot.docs.length} readings from ${deviceId}`)
      } catch (deviceError) {
        console.error(`❌ Error fetching data from ${deviceId}:`, deviceError)
      }
    }

    // Sort all readings by timestamp (latest first)
    allReadings.sort((a, b) => b.timestamp - a.timestamp)
    
    console.log(`📊 Total temperature & humidity readings fetched: ${allReadings.length}`)
    
    // Process temperature and humidity readings
    const processedData = allReadings
      .map((reading, index) => {
        // Handle timestamp
        let formattedDate = '--'
        let formattedTime = '--'
        let timestampSeconds = 0
        
        try {
          const timestamp = reading.timestamp
          
          // Format date as "MMM DD, YYYY" (e.g., "May 09, 2024")
          formattedDate = timestamp.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit'
          });

          // ✅ CHANGED: Format time as 12-hour format with AM/PM (e.g., "2:30:45 PM")
          formattedTime = timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          });
          
          timestampSeconds = timestamp.getTime() / 1000
        } catch (e) {
          console.error("Error formatting date:", e)
        }

        // Format temperature and humidity - handle missing values from different devices
        const temperature = reading.temperature !== undefined && reading.temperature !== null 
          ? Number(reading.temperature).toFixed(2) 
          : '--'
        
        const humidity = reading.humidity !== undefined && reading.humidity !== null 
          ? Number(reading.humidity).toFixed(2) 
          : '--'

        // Return processed data
        return {
          id: index + 1,
          timestamp: timestampSeconds,
          temperature: temperature,
          humidity: humidity,
          date: formattedDate,
          time: formattedTime,
          rawTimestamp: reading.timestamp,
          deviceId: reading.deviceId // Keep track of which device the reading came from
        }
      })

    // Cache the data for future use
    dataCache.value = processedData
    
    // Update the UI with minimal delay
    tempHumidityData.value = processedData
    isLoading.value = false
    
    // Initialize chart data after loading
    initializeChartData(processedData)
  } catch (error) {
    console.error("❌ Error fetching temperature and humidity data:", error)
    isLoading.value = false
    
    // If we have cached data, use it as fallback
    if (dataCache.value) {
      tempHumidityData.value = dataCache.value
      initializeChartData(dataCache.value)
    }
  }
}

// ✅ UPDATED: Modified real-time listener for new collection structure
const setupRealtimeListener = () => {
  const deviceIds = ['esp32-1', 'esp32-2', 'esp32-3']
  const unsubscribeFunctions = []
  
  // Set up listeners for all devices
  deviceIds.forEach(deviceId => {
    const realtimeQuery = query(
      collection(db, '3sensor_readings', deviceId, 'readings'),
      orderBy('timestamp', 'desc'),
      limit(10) // Limit per device for real-time updates
    )
    
    // Set up the listener with error handling and debouncing
    let debounceTimer = null
    let lastUpdateTime = Date.now()
    
    const unsubscribe = onSnapshot(realtimeQuery, (snapshot) => {
      // Debounce updates to prevent too frequent rendering
      if (debounceTimer) clearTimeout(debounceTimer)
      
      // If it's been less than 500ms since the last update, debounce
      const now = Date.now()
      const timeSinceLastUpdate = now - lastUpdateTime
      
      if (timeSinceLastUpdate < 500) {
        debounceTimer = setTimeout(() => processSnapshot(snapshot, deviceId), 500 - timeSinceLastUpdate)
      } else {
        processSnapshot(snapshot, deviceId)
        lastUpdateTime = now
      }
    }, (error) => {
      console.error(`Error in realtime listener for ${deviceId}:`, error)
    })
    
    unsubscribeFunctions.push(unsubscribe)
  })
  
  // Combined data from all devices
  let combinedRealtimeData = []
  
  function processSnapshot(snapshot, deviceId) {
    // Process the data for the charts from this specific device
    const deviceData = snapshot.docs
      .filter(doc => {
        const data = doc.data()
        return data.temperature !== undefined && data.humidity !== undefined
      })
      .map(doc => {
        const data = doc.data()
        const timestamp = data.timestamp?.toDate?.() || 
          (data.timestamp?.seconds ? new Date(data.timestamp.seconds * 1000) : new Date())
        
        return {
          timestamp,
          temperature: Number(data.temperature),
          humidity: Number(data.humidity),
          deviceId: deviceId
        }
      })
    
    // Update combined data (remove old data from this device and add new)
    combinedRealtimeData = combinedRealtimeData.filter(item => item.deviceId !== deviceId)
    combinedRealtimeData.push(...deviceData)
    
    // Sort by timestamp and limit to most recent 20 readings
    combinedRealtimeData.sort((a, b) => a.timestamp - b.timestamp)
    combinedRealtimeData = combinedRealtimeData.slice(-20)
    
    // Update chart data
    chartData.value = combinedRealtimeData
    
    // Update current values and stats
    if (combinedRealtimeData.length > 0) {
      // Get the most recent values
      const latestReading = combinedRealtimeData[combinedRealtimeData.length - 1]
      currentTempValue.value = latestReading.temperature.toFixed(2)
      currentHumidityValue.value = latestReading.humidity.toFixed(2)
      
      // ✅ CHANGED: Update last updated time to 12-hour format
      const formattedTime = latestReading.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      })
      lastUpdated.value = formattedTime
      
      // Calculate temperature stats
      const tempValues = combinedRealtimeData.map(item => item.temperature)
      tempStats.value = {
        min: Math.min(...tempValues).toFixed(2),
        max: Math.max(...tempValues).toFixed(2),
        avg: (tempValues.reduce((sum, val) => sum + val, 0) / tempValues.length).toFixed(2)
      }
      
      // Calculate humidity stats
      const humidityValues = combinedRealtimeData.map(item => item.humidity)
      humidityStats.value = {
        min: Math.min(...humidityValues).toFixed(2),
        max: Math.max(...humidityValues).toFixed(2),
        avg: (humidityValues.reduce((sum, val) => sum + val, 0) / humidityValues.length).toFixed(2)
      }
    }
    
    // Use requestAnimationFrame for smoother chart updates
    requestAnimationFrame(() => {
      updateChart()
    })
  }
  
  // Return function to unsubscribe from all listeners
  return () => {
    unsubscribeFunctions.forEach(unsubscribe => unsubscribe())
  }
}

// Initialize chart data from fetched data
const initializeChartData = (data) => {
  // Take the most recent 20 entries for initial chart data
  const initialChartData = data.slice(0, 20)
    .filter(item => item.temperature !== '--' && item.humidity !== '--') // Filter out missing data
    .map(item => ({
      timestamp: item.rawTimestamp || new Date(),
      temperature: Number(item.temperature),
      humidity: Number(item.humidity)
    }))
    .sort((a, b) => a.timestamp - b.timestamp) // Sort by timestamp ascending for the chart

  // Set chart data
  chartData.value = initialChartData

  // Set initial current values and stats
  if (initialChartData.length > 0) {
    const latestReading = initialChartData[initialChartData.length - 1]
    currentTempValue.value = latestReading.temperature.toFixed(2)
    currentHumidityValue.value = latestReading.humidity.toFixed(2)
    
    // ✅ CHANGED: Format time as 12-hour format with AM/PM
    const formattedTime = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    lastUpdated.value = formattedTime
    
    // Calculate temperature stats
    const tempValues = initialChartData.map(item => item.temperature)
    tempStats.value = {
      min: Math.min(...tempValues).toFixed(2),
      max: Math.max(...tempValues).toFixed(2),
      avg: (tempValues.reduce((sum, val) => sum + val, 0) / tempValues.length).toFixed(2)
    }
    
    // Calculate humidity stats
    const humidityValues = initialChartData.map(item => item.humidity)
    humidityStats.value = {
      min: Math.min(...humidityValues).toFixed(2),
      max: Math.max(...humidityValues).toFixed(2),
      avg: (humidityValues.reduce((sum, val) => sum + val, 0) / humidityValues.length).toFixed(2)
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
      
      // Create new chart with both temperature and humidity datasets and enhanced styling
      chart.value = new Chart(ctx, {
        type: 'line',
        data: {
          labels: chartData.value.map(item => {
            // ✅ CHANGED: Chart labels to 12-hour format with AM/PM
            return item.timestamp.toLocaleTimeString('en-US', {
              hour: '2-digit',
              minute: '2-digit',
              hour12: true
            })
          }),
          datasets: [
            {
              label: 'Temperature (°C)',
              data: chartData.value.map(item => item.temperature),
              borderColor: '#ef4444', // red-500
              backgroundColor: 'rgba(239, 68, 68, 0.15)', // red-500 with opacity
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
              borderColor: '#3b82f6', // blue-500
              backgroundColor: 'rgba(59, 130, 246, 0.15)', // blue-500 with opacity
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
              min: Math.max(0, Math.floor(tempStats.value.min * 0.95)),
              max: Math.ceil(tempStats.value.max * 1.05),
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
              min: Math.max(0, Math.floor(humidityStats.value.min * 0.95)),
              max: Math.min(100, Math.ceil(humidityStats.value.max * 1.05)),
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

// Update the chart with new data - optimized for performance
const updateChart = () => {
  if (chart.value && chartData.value.length > 0) {
    // ✅ CHANGED: Update chart labels to 12-hour format with AM/PM
    chart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    
    // Update temperature dataset
    chart.value.data.datasets[0].data = chartData.value.map(item => item.temperature)
    
    // Update humidity dataset
    chart.value.data.datasets[1].data = chartData.value.map(item => item.humidity)
    
    // Update y-axis scales based on new data
    chart.value.options.scales['y-temperature'].min = Math.max(0, Math.floor(tempStats.value.min * 0.95))
    chart.value.options.scales['y-temperature'].max = Math.ceil(tempStats.value.max * 1.05)
    
    chart.value.options.scales['y-humidity'].min = Math.max(0, Math.floor(humidityStats.value.min * 0.95))
    chart.value.options.scales['y-humidity'].max = Math.min(100, Math.ceil(humidityStats.value.max * 1.05))
    
    // Use a more performant update
    chart.value.update('none') // 'none' mode skips animations for better performance
  }
}

// Helper functions for text color
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

// Initialize filters object
const filters = ref({
  temperature: { min: '', max: '' },
  humidity: { min: '', max: '' }
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

// Computed properties with memoization for better performance
const filteredData = computed(() => {
  let result = [...tempHumidityData.value]

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
    saveAs(blob, 'temperature_humidity_data.csv')
    window.showToast('Temperature & Humidity exported as CSV', 'success')
  } else if (format === 'pdf') {
    // PDF Export
    const doc = new jsPDF()
    doc.text('Temperature & Humidity Data Table', 14, 16)
    autoTable(doc, {
      head: [exportHeaders],
      body: exportRows,
      startY: 22,
      styles: { fontSize: 10 }
    })
    doc.save('temperature_humidity_data.pdf')
    window.showToast('Temperature & Humidity exported as PDF', 'success')
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
          new Paragraph({ text: 'Temperature & Humidity Data Table', heading: 'Heading1' }),
          new Table({ rows: tableRows })
        ]
      }]
    })
    const buffer = await Packer.toBlob(docxDoc)
    saveAs(buffer, 'temperature_humidity_data.docx')
  }

  activeDropdown.value = null // Close dropdown after exporting
}

// Watch for changes that should reset pagination
watch([searchQuery, activeFilters, itemsPerPage], () => {
  currentPage.value = 1
})

// Cleanup function for charts and listener
let unsubscribe = null

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  // Implement progressive loading strategy
  // 1. First try to get data from cache (if any)
  // 2. Then fetch fresh data
  fetchTempHumidityData()
  
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