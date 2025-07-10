<template>
      <div class="flex-1 w-full px-4 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
        <!-- Enhanced main container with more appealing design -->
        <div class="bg-white rounded-lg shadow-lg border border-gray-100 h-[calc(100vh-140px)] flex flex-col overflow-hidden">
          <!-- Gradient header for visual appeal -->
          <div class="bg-gradient-to-r from-green-50 to-white p-6 border-b border-gray-100 rounded-t-lg">
            <!-- Header with controls aligned side by side -->
            <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <!-- Title and breadcrumb with enhanced styling -->
              <div>
                <h1 class="text-xl font-semibold text-gray-800 mb-1">NPK Data Table</h1>
                <div class="flex items-center text-sm text-gray-500">
                  <span class="text-green-600 font-medium">NPK Analysis</span>
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
                    placeholder="Search NPK measurements..."
                    class="w-full pl-10 pr-4 py-2.5 rounded-lg border border-gray-200 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 text-sm text-gray-700 placeholder-gray-400 shadow-sm"
                    v-model="searchQuery"
                    @input="performSearch"
                  />
                </div>
  
                <!-- Filter Button with enhanced styling -->
                <div class="relative">
                  <button 
                    @click.stop="toggleDropdown('filter')"
                    class="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-gray-200 bg-white text-sm text-gray-700 hover:text-green-600 transition-colors shadow-sm"
                  >
                    <Filter class="h-4 w-4 text-gray-500" />
                    Filter
                    <ChevronDown class="h-4 w-4 text-gray-400" :class="{ 'transform rotate-180': activeDropdown === 'filter' }" />
                  </button>
                  
                  <div 
                    v-show="activeDropdown === 'filter'"
                    class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50 overflow-hidden"
                    @click.stop
                  >
                    <div class="p-4 space-y-4 max-h-[400px] overflow-y-auto">
                      <div v-for="field in filterFields" :key="field.key" class="space-y-2">
                        <label class="block text-sm font-medium text-gray-700">{{ field.label }}</label>
                        <div class="flex items-center gap-2">
                          <input
                            v-model="filters[field.key].min"
                            type="number"
                            placeholder="Min"
                            class="w-full px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-green-500 focus:border-green-500"
                          />
                          <span class="text-gray-400">-</span>
                          <input
                            v-model="filters[field.key].max"
                            type="number"
                            placeholder="Max"
                            class="w-full px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-green-500 focus:border-green-500"
                          />
                        </div>
                      </div>
                      <button 
                        @click="applyFilters"
                        class="w-full px-4 py-2 bg-green-500 text-white rounded-lg text-sm font-medium hover:bg-green-600 transition-colors"
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
                    class="flex items-center gap-2 px-4 py-2.5 rounded-lg border border-gray-200 bg-white text-sm text-gray-700 hover:text-green-600 transition-colors shadow-sm"
                  >
                    <ArrowUpDown class="h-4 w-4 text-gray-500" />
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
                        class="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center justify-between"
                      >
                        {{ header.label }}
                        <ArrowUpDown v-if="sortKey === header.key" class="h-3 w-3 text-green-500" />
                      </button>
                    </div>
                  </div>
                </div>
  
                <!-- Export Button with enhanced styling -->
                <div class="relative">
                  <button 
                    @click.stop="toggleDropdown('export')"
                    class="flex items-center gap-2 px-4 py-2.5 rounded-lg bg-green-500 text-white text-sm font-medium hover:bg-green-600 transition-colors shadow-sm"
                  >
                    <Download class="h-4 w-4" />
                    Export
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
                        @click="exportData(format)"
                        class="w-full px-4 py-2 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center"
                      >
                        <span v-if="format === 'csv'" class="mr-2 text-green-500"><FileText class="h-4 w-4" /></span>
                        <span v-else-if="format === 'pdf'" class="mr-2 text-red-500"><FileText class="h-4 w-4" /></span>
                        <span v-else class="mr-2 text-blue-500"><FileText class="h-4 w-4" /></span>
                        Export as {{ format.toUpperCase() }}
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Table and Graph Section - Flex container for side-by-side layout -->
          <div class="flex-1 overflow-hidden flex flex-col md:flex-row">
            <!-- Live Graph Container - Three Separate Charts -->
<div class="w-full md:w-1/3 lg:w-1/3 border-r border-gray-200 bg-white p-4 overflow-y-auto">
  <div class="mb-3 flex items-center justify-between">
    <div>
      <h3 class="text-sm font-semibold text-gray-700">Live NPK Analysis</h3>
      <p class="text-xs text-gray-500">Real-time soil monitoring</p>
    </div>
    
    <!-- Minimalist Last Updated Status -->
    <div class="text-right">
      <div class="flex items-center gap-1.5 text-xs text-gray-500 mb-0.5">
        <Clock class="h-3 w-3" />
        <span>Last Updated</span>
        <div class="w-1.5 h-1.5 bg-green-400 rounded-full animate-pulse"></div>
      </div>
      <div class="text-sm font-mono font-semibold text-gray-800">
        {{ lastUpdated || '--:--:-- --' }}
      </div>
      <div class="text-xs text-gray-400">
        {{ currentDate }}
      </div>
    </div>
  </div>
  
  <!-- Nitrogen Graph -->
  <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
    <div class="p-3 border-b border-gray-100 bg-green-50 flex justify-between items-center">
      <div class="flex items-center gap-2">
        <div class="w-3 h-3 rounded-full bg-green-500"></div>
        <span class="text-sm font-semibold text-green-700">Nitrogen (mg/kg)</span>
      </div>
      <div class="text-xs text-gray-500">
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
        <span class="text-sm font-semibold text-blue-700">Phosphorus (mg/kg)</span>
      </div>
      <div class="text-xs text-gray-500">
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
        <span class="text-sm font-semibold text-purple-700">Potassium (mg/kg)</span>
      </div>
      <div class="text-xs text-gray-500">
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
          <span class="text-xs text-green-600 font-medium">20-60 mg/kg</span>
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
            <div class="w-full md:w-2/3 lg:w-2/3 flex flex-col">
              <!-- Fixed Header with enhanced styling -->
              <div class="w-full border-b border-gray-200 sticky top-0 z-10 bg-gray-50">
                <table class="min-w-full">
                  <thead>
                    <tr>
                      <th class="w-[10%] py-3.5 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                        ID
                      </th>
                      <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                        <div class="text-green-600">Nitrogen</div>
                        <div class="text-gray-400 text-[10px]">(mg/kg)</div>
                      </th>
                      <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                        <div class="text-blue-600">Phosphorus</div>
                        <div class="text-gray-400 text-[10px]">(mg/kg)</div>
                      </th>
                      <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                        <div class="text-purple-600">Potassium</div>
                        <div class="text-gray-400 text-[10px]">(mg/kg)</div>
                      </th>
                      <th class="w-[15%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                        <div class="text-gray-600">Date</div>
                        <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                      </th>
                      <th class="w-[15%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                        <div class="text-gray-600">Time</div>
                        <div class="text-gray-400 text-[10px]">HH:MM:SS AM/PM</div>
                      </th>
                    </tr>
                  </thead>
                </table>
              </div>
              
              <!-- Scrollable Body with enhanced styling -->
              <div class="flex-1 overflow-y-auto">
                <table class="min-w-full">
                  <tbody>
                    <tr 
                      v-for="(row, index) in paginatedData" 
                      :key="index"
                      class="border-b border-gray-50 last:border-0"
                    >
                      <td class="w-[10%] px-4 py-3.5 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-700">{{ row.id }}</div>
                      </td>
                      <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                        <div class="text-sm font-medium" :class="getNitrogenTextClass(row.nitrogen)">
                          {{ row.nitrogen }}
                        </div>
                      </td>
                      <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                        <div class="text-sm font-medium" :class="getPhosphorusTextClass(row.phosphorus)">
                          {{ row.phosphorus }}
                        </div>
                      </td>
                      <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                        <div class="text-sm font-medium" :class="getPotassiumTextClass(row.potassium)">
                          {{ row.potassium }}
                        </div>
                      </td>
                      <td class="w-[15%] px-4 py-3.5 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-700">{{ row.date }}</div>
                      </td>
                      <td class="w-[15%] px-4 py-3.5 whitespace-nowrap">
                        <div class="text-sm font-medium text-gray-700">{{ row.time }}</div>
                      </td>
                    </tr>
                    <!-- Empty state when no data - Enhanced styling -->
                    <tr v-if="paginatedData.length === 0 && !isLoading">
                      <td colspan="6" class="px-6 py-16 text-center">
                        <div class="flex flex-col items-center justify-center">
                          <FileSearch class="h-16 w-16 text-gray-300 mb-4" />
                          <p class="text-gray-500 text-lg font-medium">No NPK data found</p>
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
          <div class="border-t border-gray-100 py-4 px-6 bg-gradient-to-r from-white to-green-50 rounded-b-lg">
            <!-- Enhanced Pagination -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
              <div class="text-sm text-gray-600 flex items-center gap-2">
                <span class="hidden sm:inline">Showing</span>
                <select 
                  v-model="itemsPerPage" 
                  class="bg-white border border-gray-200 rounded-lg px-2 py-1.5 text-sm font-medium text-gray-700 focus:outline-none focus:ring-1 focus:ring-green-500 focus:border-green-500 shadow-sm"
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
                  class="inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium transition-colors rounded-md
                    disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                    enabled:text-gray-700 enabled:hover:text-green-600 enabled:hover:bg-green-50"
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
                      'relative inline-flex items-center justify-center w-8 h-8 text-sm transition-colors mx-0.5 rounded-md',
                      page === currentPage
                        ? 'text-white bg-green-500 font-semibold'
                        : page === '...'
                          ? 'cursor-default text-gray-400'
                          : 'text-gray-700 hover:text-green-600 hover:bg-green-50'
                    ]"
                  >
                    {{ page }}
                  </button>
                </div>
  
                <button 
                  @click="nextPage"
                  :disabled="currentPage >= totalPages"
                  class="inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium transition-colors rounded-md
                    disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                    enabled:text-gray-700 enabled:hover:text-green-600 enabled:hover:bg-green-50"
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
    <LoadingPage 
      :isVisible="isLoading" 
      title="Loading NPK Data" 
      message="Please wait while we fetch the latest soil nutrient measurements"
    />
    <Settings />
</template>
  
<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
// Add Clock to the imports
import { Search, Filter, Download, ChevronDown, ChevronRight, ChevronLeft, ArrowUpDown, FileText, FileSearch, Clock } from 'lucide-vue-next'
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

// Chart.js import
import Chart from 'chart.js/auto'

const db = getFirestore()
const npkData = ref([])
const isLoading = ref(true)

// Chart references - Update to have separate charts
const nitrogenChartCanvas = ref(null)
const phosphorusChartCanvas = ref(null)
const potassiumChartCanvas = ref(null)
const nitrogenChart = ref(null)
const phosphorusChart = ref(null)
const potassiumChart = ref(null)

// Chart data
const chartData = ref([])

// Current values and stats
const currentNitrogenValue = ref('--')
const currentPhosphorusValue = ref('--')
const currentPotassiumValue = ref('--')
const lastUpdated = ref('--')
// Add currentDate reactive variable after the other refs
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

// Prefetch data cache
const dataCache = ref(null)

// Fetch NPK data from Firebase
const fetchNPKData = async () => {
  try {
    // If we already have cached data, use it immediately to show something
    if (dataCache.value) {
      npkData.value = dataCache.value
      isLoading.value = false
      initializeChartData(dataCache.value)
    } else {
      isLoading.value = true
    }
    
    // Fetch from the 3sensor_readings collection structure
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

          // Only include readings that have NPK data
          if (data.nitrogen !== undefined && data.phosphorus !== undefined && data.potassium !== undefined) {
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
    
    console.log(`📊 Total NPK readings fetched: ${allReadings.length}`)
    
    // Process NPK readings
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

          // Format time as 12-hour format with AM/PM (e.g., "2:30:45 PM")
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

        // Format NPK values - handle missing values from different devices
        const nitrogen = reading.nitrogen !== undefined && reading.nitrogen !== null 
          ? Number(reading.nitrogen).toFixed(2) 
          : '--'
        
        const phosphorus = reading.phosphorus !== undefined && reading.phosphorus !== null 
          ? Number(reading.phosphorus).toFixed(2) 
          : '--'
          
        const potassium = reading.potassium !== undefined && reading.potassium !== null 
          ? Number(reading.potassium).toFixed(2) 
          : '--'

        // Return processed data
        return {
          id: index + 1,
          timestamp: timestampSeconds,
          nitrogen: nitrogen,
          phosphorus: phosphorus,
          potassium: potassium,
          date: formattedDate,
          time: formattedTime,
          rawTimestamp: reading.timestamp,
          deviceId: reading.deviceId // Keep track of which device the reading came from
        }
      })

    // Cache the data for future use
    dataCache.value = processedData
    
    // Update the UI with minimal delay
    npkData.value = processedData
    isLoading.value = false
    
    // Initialize chart data after loading
    initializeChartData(processedData)
  } catch (error) {
    console.error("❌ Error fetching NPK data:", error)
    isLoading.value = false
    
    // If we have cached data, use it as fallback
    if (dataCache.value) {
      npkData.value = dataCache.value
      initializeChartData(dataCache.value)
    }
  }
}

// Setup real-time listener for NPK data
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
        return data.nitrogen !== undefined && data.phosphorus !== undefined && data.potassium !== undefined
      })
      .map(doc => {
        const data = doc.data()
        const timestamp = data.timestamp?.toDate?.() || 
          (data.timestamp?.seconds ? new Date(data.timestamp.seconds * 1000) : new Date())
        
        return {
          timestamp,
          nitrogen: Number(data.nitrogen),
          phosphorus: Number(data.phosphorus),
          potassium: Number(data.potassium),
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
      currentNitrogenValue.value = latestReading.nitrogen.toFixed(2)
      currentPhosphorusValue.value = latestReading.phosphorus.toFixed(2)
      currentPotassiumValue.value = latestReading.potassium.toFixed(2)
      
      // Update last updated time with 12-hour format
      const formattedTime = latestReading.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      })
      lastUpdated.value = formattedTime
      
      // Calculate nitrogen stats
      const nitrogenValues = combinedRealtimeData.map(item => item.nitrogen)
      nitrogenStats.value = {
        min: Math.min(...nitrogenValues).toFixed(2),
        max: Math.max(...nitrogenValues).toFixed(2),
        avg: (nitrogenValues.reduce((sum, val) => sum + val, 0) / nitrogenValues.length).toFixed(2)
      }
      
      // Calculate phosphorus stats
      const phosphorusValues = combinedRealtimeData.map(item => item.phosphorus)
      phosphorusStats.value = {
        min: Math.min(...phosphorusValues).toFixed(2),
        max: Math.max(...phosphorusValues).toFixed(2),
        avg: (phosphorusValues.reduce((sum, val) => sum + val, 0) / phosphorusValues.length).toFixed(2)
      }
      
      // Calculate potassium stats
      const potassiumValues = combinedRealtimeData.map(item => item.potassium)
      potassiumStats.value = {
        min: Math.min(...potassiumValues).toFixed(2),
        max: Math.max(...potassiumValues).toFixed(2),
        avg: (potassiumValues.reduce((sum, val) => sum + val, 0) / potassiumValues.length).toFixed(2)
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
    .filter(item => item.nitrogen !== '--' && item.phosphorus !== '--' && item.potassium !== '--') // Filter out missing data
    .map(item => ({
      timestamp: item.rawTimestamp || new Date(),
      nitrogen: Number(item.nitrogen),
      phosphorus: Number(item.phosphorus),
      potassium: Number(item.potassium)
    }))
    .sort((a, b) => a.timestamp - b.timestamp) // Sort by timestamp ascending for the chart

  // Set chart data
  chartData.value = initialChartData

  // Set initial current values and stats
  if (initialChartData.length > 0) {
    const latestReading = initialChartData[initialChartData.length - 1]
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
    
    // Calculate nitrogen stats
    const nitrogenValues = initialChartData.map(item => item.nitrogen)
    nitrogenStats.value = {
      min: Math.min(...nitrogenValues).toFixed(2),
      max: Math.max(...nitrogenValues).toFixed(2),
      avg: (nitrogenValues.reduce((sum, val) => sum + val, 0) / nitrogenValues.length).toFixed(2)
    }
    
    // Calculate phosphorus stats
    const phosphorusValues = initialChartData.map(item => item.phosphorus)
    phosphorusStats.value = {
      min: Math.min(...phosphorusValues).toFixed(2),
      max: Math.max(...phosphorusValues).toFixed(2),
      avg: (phosphorusValues.reduce((sum, val) => sum + val, 0) / phosphorusValues.length).toFixed(2)
    }
    
    // Calculate potassium stats
    const potassiumValues = initialChartData.map(item => item.potassium)
    potassiumStats.value = {
      min: Math.min(...potassiumValues).toFixed(2),
      max: Math.max(...potassiumValues).toFixed(2),
      avg: (potassiumValues.reduce((sum, val) => sum + val, 0) / potassiumValues.length).toFixed(2)
    }
  }
  
  // Initialize the chart
  initializeChart()
}

// Initialize separate charts with enhanced styling for NPK data
const initializeChart = () => {
  nextTick(() => {
    initializeNitrogenChart()
    initializePhosphorusChart()
    initializePotassiumChart()
  })
}

// Initialize Nitrogen Chart
const initializeNitrogenChart = () => {
  if (nitrogenChartCanvas.value) {
    if (nitrogenChart.value) {
      nitrogenChart.value.destroy()
    }
    
    const ctx = nitrogenChartCanvas.value.getContext('2d')
    
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

// Initialize Phosphorus Chart
const initializePhosphorusChart = () => {
  if (phosphorusChartCanvas.value) {
    if (phosphorusChart.value) {
      phosphorusChart.value.destroy()
    }
    
    const ctx = phosphorusChartCanvas.value.getContext('2d')
    
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

// Initialize Potassium Chart
const initializePotassiumChart = () => {
  if (potassiumChartCanvas.value) {
    if (potassiumChart.value) {
      potassiumChart.value.destroy()
    }
    
    const ctx = potassiumChartCanvas.value.getContext('2d')
    
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

// Update the updateChart function to update all three charts:
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

// Helper functions for text color based on NPK values
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

// Initialize filters object
const filters = ref({
  nitrogen: { min: '', max: '' },
  phosphorus: { min: '', max: '' },
  potassium: { min: '', max: '' }
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

const exportFormats = ['csv', 'pdf', 'docs']

// Computed properties with memoization for better performance
const filteredData = computed(() => {
  let result = [...npkData.value]

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

const exportData = (format) => {
  // Get the data to export (all filtered and sorted data, not just current page)
  const dataToExport = sortedData.value

  if (format === 'csv') {
    exportAsCSV(dataToExport)
  } else if (format === 'pdf') {
    exportAsPDF(dataToExport)
  } else if (format === 'docs') {
    exportAsDocs(dataToExport)
  }

  activeDropdown.value = null // Close dropdown after exporting
}

const exportAsCSV = (data) => {
  // Get headers
  const headerRow = headers.map(h => h.label).join(',')

  // Convert data to CSV rows
  const rows = data.map(row => {
    return headers.map(header => {
      // Handle special cases like objects or arrays
      const value = row[header.key]
      if (typeof value === 'string' && value.includes(',')) {
        return `"${value}"`
      }
      return value
    }).join(',')
  })

  // Combine headers and rows
  const csvContent = [headerRow, ...rows].join('\n')

  // Create a blob and download
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.setAttribute('href', url)
  link.setAttribute('download', 'npk_data.csv')
  link.style.visibility = 'hidden'
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const exportAsPDF = (data) => {
  // In a real application, you would use a library like jsPDF
  alert('PDF export would be implemented with a library like jsPDF')
  console.log('Data to export as PDF:', data)
}

const exportAsDocs = (data) => {
  // In a real application, you would use a library to generate DOCS
  alert('DOCS export would be implemented with a library for document generation')
  console.log('Data to export as DOCS:', data)
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
  fetchNPKData()
  
  // Set up realtime listener
  unsubscribe = setupRealtimeListener()
  
  // Set up window resize handler for chart responsiveness
  const handleResize = () => {
    if (nitrogenChart.value) nitrogenChart.value.resize()
    if (phosphorusChart.value) phosphorusChart.value.resize()
    if (potassiumChart.value) potassiumChart.value.resize()
  }
  
  // Use ResizeObserver for better performance than window resize
  if (typeof ResizeObserver !== 'undefined') {
    const resizeObserver = new ResizeObserver(handleResize)
    if (nitrogenChartCanvas.value) {
      resizeObserver.observe(nitrogenChartCanvas.value.parentElement)
    }
    if (phosphorusChartCanvas.value) {
      resizeObserver.observe(phosphorusChartCanvas.value.parentElement)
    }
    if (potassiumChartCanvas.value) {
      resizeObserver.observe(potassiumChartCanvas.value.parentElement)
    }
  } else {
    // Fallback to window resize
    window.addEventListener('resize', handleResize)
  }
  
  // Update current date initially and every minute
  updateCurrentDate()
  const dateInterval = setInterval(updateCurrentDate, 60000) // Update every minute
  
  // Store interval reference for cleanup
  window.dateUpdateInterval = dateInterval
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  
  // Clean up all charts
  if (nitrogenChart.value) nitrogenChart.value.destroy()
  if (phosphorusChart.value) phosphorusChart.value.destroy()
  if (potassiumChart.value) potassiumChart.value.destroy()
  
  // Clean up realtime listener
  if (unsubscribe) {
    unsubscribe()
  }
  
  // Remove resize listener
  window.removeEventListener('resize', () => {})
  
  // Clear date update interval
  if (window.dateUpdateInterval) {
    clearInterval(window.dateUpdateInterval)
  }
})

// Add a function to update the current date
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