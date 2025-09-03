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
                    <div class="p-3 sm:p-4 space-y-3 sm:space-y-4 max-h-[60vh] sm:max-h-[400px] md:w-[400px] overflow-y-auto">
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
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Soil Moisture</div>
                  <div class="text-xs font-semibold text-blue-600">{{ row.soilMoisture }}%</div>
                </div>
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Status</div>
                  <span 
                    :class="[
                      'px-2 py-0.5 rounded-full text-[10px] font-medium',
                      row.soilStatus === 'WET' ? 'bg-emerald-100 text-emerald-800' :
                      row.soilStatus === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ row.soilStatus }}
                  </span>
                </div>
              </div>
            </div>
            
            <div v-if="paginatedData.length === 0 && !isLoading" 
                class="flex flex-col items-center justify-center py-8">
              <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
              <p class="text-gray-500 text-xs font-medium">No soil moisture data found</p>
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

          <!-- Pagination with new style -->
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
                  :disabled="currentPage >= totalPages"
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
    title="Loading Soil Moisture Data" 
    message="Please wait while we fetch the latest soil moisture measurements"
  />
  <!-- <Settings /> -->
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

const soilMoistureData = ref([])
const isLoading = ref(true)

const chartCanvas = ref(null)
const chart = ref(null)

const chartData = ref([])

const currentMoistureValue = ref('--')
const lastUpdated = ref('--')
const moistureStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})

let PRINT_CHART_DATA_LIMIT = 0

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
  
  const soilMoistureRows = sortedData.value.map(row => ({
    id: row.id,
    date: row.date,
    time: row.time,
    device: row.deviceId || 'N/A',
    soilMoisture: row.soilMoisture,
    soilStatus: row.soilStatus
  }));
  
  // Get ALL data for the chart
  const printChartData = soilMoistureData.value
    .filter(item => item.soilMoisture !== '--')
    .map(item => ({
      timestamp: item.rawTimestamp,
      value: Number(item.soilMoisture)
    }))
    .sort((a, b) => a.timestamp - b.timestamp); 
  
  console.log(`📊 Print chart will show ${printChartData.length} records`);
  
  // Calculate overall statistics from ALL data
  const printChartValues = printChartData.map(item => item.value);
  const overallMin = printChartValues.length > 0 ? Math.min(...printChartValues) : 0;
  const overallMax = printChartValues.length > 0 ? Math.max(...printChartValues) : 100;
  const overallAvg = printChartValues.length > 0 ? 
    (printChartValues.reduce((sum, val) => sum + val, 0) / printChartValues.length) : 0;
  
  console.log(`📈 Data range: ${overallMin}% - ${overallMax}% (Avg: ${overallAvg.toFixed(2)}%)`);
  
  // For the chart display, use all data but adjust scaling to show the actual range
  const chartDisplayData = printChartData;
  
  let chartImage = '';
  
  try {
    const ctx = tempCanvas.getContext('2d');
    
    // Calculate dynamic y-axis scaling based on actual data range
    const dataRange = overallMax - overallMin;
    const yAxisPadding = dataRange * 0.1; // 10% padding
    const yMin = Math.max(0, Math.floor(overallMin - yAxisPadding));
    const yMax = Math.min(100, Math.ceil(overallMax + yAxisPadding));
    
    console.log(`📊 Y-axis range: ${yMin}% - ${yMax}%`);
    
    const tempChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: chartDisplayData.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          })
        }),
        datasets: [{
          label: 'Soil Moisture (%)',
          data: chartDisplayData.map(item => item.value), 
          borderColor: '#10b981', 
          backgroundColor: 'rgba(16, 185, 129, 0.15)', 
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 2,
          pointHoverRadius: 4,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#10b981',
          pointBorderWidth: 1.5
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
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                return `Moisture: ${context.raw.toFixed(1)}%`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            min: yMin, // Use dynamic min based on data
            max: yMax, // Use dynamic max based on data
            title: {
              display: true,
              text: 'Moisture (%)',
              color: '#10b981',
              font: {
                size: 14,
                weight: '600'
              }
            },
            ticks: {
              font: { size: 12 },
              color: '#64748b',
              stepSize: calculateStepSize(dataRange), // Dynamic step size
              callback: function(value) {
                return value + '%'; // Add percentage sign to y-axis labels
              }
            },
            grid: {
              color: 'rgba(100, 116, 139, 0.2)'
            }
          },
          x: {
            ticks: {
              font: { size: 9 },
              color: '#64748b',
              maxTicksLimit: 10,
              maxRotation: 45,
              callback: function(value, index, values) {
                // Show fewer labels for better readability
                return index % Math.ceil(values.length / 10) === 0 ? this.getLabelForValue(value) : '';
              }
            },
            grid: {
              display: false // Hide x-axis grid lines for cleaner look
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
        
        generatePrintHTML(chartImage, soilMoistureRows, formattedDate, now, printChartData.length, overallMin, overallMax, overallAvg);
      } catch (error) {
        console.error('Error capturing chart:', error);
        document.body.removeChild(tempContainer);
        generatePrintHTML('', soilMoistureRows, formattedDate, now, 0, 0, 0, 0);
      }
    }, 500);
    
  } catch (error) {
    console.error('Error creating chart:', error);
    document.body.removeChild(tempContainer);
    generatePrintHTML('', soilMoistureRows, formattedDate, now, 0, 0, 0, 0);
  }
};

// Helper function to calculate appropriate step size for y-axis
function calculateStepSize(dataRange) {
  if (dataRange <= 10) return 1;
  if (dataRange <= 20) return 2;
  if (dataRange <= 50) return 5;
  if (dataRange <= 100) return 10;
  return 20;
}

const generatePrintHTML = (chartImage, soilMoistureRows, formattedDate, now, chartRecordCount, printMin, printMax, printAvg) => {
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Soil Moisture Analysis Data</title>
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
        .soil-moisture { color: #10b981; font-weight: 500; }
        .status-wet { color: #059669; }
        .status-medium { color: #d97706; }
        .status-dry { color: #dc2626; }
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
          color: #10b981;
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
        <h1>Soil Moisture Analysis Report</h1>
        <div class="date">${formattedDate}</div>
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-item">
          <span class="summary-label">Total Records:</span>
          <span class="summary-value">${soilMoistureRows.length}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Chart Data Points:</span>
          <span class="summary-value">${chartRecordCount}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Date Range:</span>
          <span class="summary-value">${soilMoistureRows.length > 0 ? soilMoistureRows[soilMoistureRows.length-1].date + ' to ' + soilMoistureRows[0].date : 'N/A'}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Report Generated:</span>
          <span class="summary-value">${now.toLocaleString()}</span>
        </div>
      </div>
      
      <div class="section-header">Soil Moisture Trend Analysis</div>
      ${chartImage ? `
        <div class="chart-title">Soil Moisture Levels Over Time</div>
        <div class="chart-info">Showing ${chartRecordCount} most recent data points</div>
        <img src="${chartImage}" class="chart-image" alt="Soil Moisture Chart" />
        
        <div class="stats-summary">
          <div class="stat-item">
            <h4>Soil Moisture</h4>
            <div class="stat-values">
              Min: ${printMin.toFixed(2)}%<br>
              Avg: ${printAvg.toFixed(2)}%<br>
              Max: ${printMax.toFixed(2)}%
            </div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">Chart could not be generated</p>'}
      
      <div class="section-header">Detailed Soil Moisture Sensor Readings</div>
      <table>
        <thead>
          <tr>
            <th style="width: 10%">ID</th>
            <th style="width: 15%">Date</th>
            <th style="width: 12%">Time</th>
            <th style="width: 10%">Device</th>
            <th style="width: 15%">Soil Moisture</th>
            <th style="width: 15%">Soil Status</th>
          </tr>
        </thead>
        <tbody>
          ${soilMoistureRows.map(row => `
            <tr>
              <td>${row.id}</td>
              <td>${row.date}</td>
              <td>${row.time}</td>
              <td>${row.device}</td>
              <td><span class="soil-moisture">${row.soilMoisture}%</span></td>
              <td>
                <span class="${
                  row.soilStatus === 'WET' ? 'status-wet' :
                  row.soilStatus === 'MEDIUM' ? 'status-medium' : 'status-dry'
                }">${row.soilStatus}</span>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by Soil Moisture Analysis System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
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

const fetchSoilMoistureData = async () => {
  try {
    isLoading.value = true
    console.log('🌱 Fetching soil moisture data...')

    const response = await api.get(`/soil-moisture`, {
      headers: {
        'Accept': 'application/json',
      }
    })

    console.log('📊 API Response:', response)
    
    let data
    if (response && typeof response === 'object') {
      if (response.data !== undefined) {
        data = response.data
        console.log('📊 Response status:', response.status)
      } else if (Array.isArray(response)) {
        data = response
      } else {
        data = response
      }
    }

    console.log('📊 Response data:', data)

    if (!Array.isArray(data)) {
      console.error('❌ Expected array but got:', typeof data, data)
      throw new Error(`Expected array but got: ${typeof data}`)
    }

    console.log('📊 Number of items received:', data.length)

    if (data.length === 0) {
      console.log('📭 No soil moisture data found in database')
      soilMoistureData.value = []
      isLoading.value = false
      return
    }

    const processedData = data.map((reading, index) => {
      let timestamp
      if (reading.timestamp) {
        if (typeof reading.timestamp === 'string') {
          timestamp = new Date(reading.timestamp)
        } else if (reading.timestamp instanceof Date) {
          timestamp = reading.timestamp
        } else {
          console.warn('Unknown timestamp format:', reading.timestamp)
          timestamp = new Date()
        }
      } else {
        timestamp = new Date()
      }

      const soilMoistureValue = reading.soilMoisture !== undefined ? reading.soilMoisture : 
                               reading.value !== undefined ? reading.value : 
                               reading.moisture !== undefined ? reading.moisture : 0

      return {
        id: `${index + 1}`,
        timestamp: timestamp.getTime() / 1000,
        soilMoisture: Number(soilMoistureValue).toFixed(2),
        soilStatus: calculateSoilStatus(Number(soilMoistureValue)),
        date: timestamp.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: '2-digit'
        }),
        time: timestamp.toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        }),
        rawTimestamp: timestamp, 
        deviceId: reading.deviceId || reading.device_id || 'unknown'
      }
    })

    soilMoistureData.value = processedData
    dataCache.value = processedData
    isLoading.value = false
    
    initializeChartData(processedData)
    PRINT_CHART_DATA_LIMIT = processedData.length
    
    console.log(`✅ Successfully loaded ${processedData.length} soil moisture readings`)

  } catch (error) {
    console.error("❌ Error fetching soil moisture data:", error)
    isLoading.value = false
    soilMoistureData.value = []
  }
}


let socket = null
const setupRealtimeListener = () => {
  try {
    // Connect to WebSocket for real-time updates
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsUrl = `${wsProtocol}//${window.location.host.replace('3000', '8000')}/ws/soil-moisture`
    
    socket = new WebSocket(wsUrl)
    
    socket.onopen = () => {
      console.log('WebSocket connected for real-time soil moisture updates')
    }
    
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data)
      processRealtimeData(data)
    }
    
    socket.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
    
    socket.onclose = () => {
      console.log('WebSocket connection closed')
    }
    
    return () => {
      if (socket) {
        socket.close()
      }
    }
  } catch (error) {
    console.error('Error setting up WebSocket:', error)
    return () => {} // Return empty cleanup function
  }
}

let debounceTimer = null
let lastUpdateTime = Date.now()
let combinedRealtimeData = []

const processRealtimeData = (data) => {
  let timestamp
  if (data.timestamp) {
    if (typeof data.timestamp === 'string') {
      timestamp = new Date(data.timestamp)
    } else if (data.timestamp instanceof Date) {
      timestamp = data.timestamp
    } else {
      timestamp = new Date()
    }
  } else {
    timestamp = new Date()
  }
  
  const newDataPoint = {
    timestamp,
    value: data.soilMoisture,
    deviceId: data.deviceId || 'unknown'
  }
  
  combinedRealtimeData.push(newDataPoint)
  combinedRealtimeData = combinedRealtimeData.slice(-20) 
  
  chartData.value = combinedRealtimeData
  
  if (combinedRealtimeData.length > 0) {
    const latestReading = combinedRealtimeData[combinedRealtimeData.length - 1]
    currentMoistureValue.value = latestReading.value.toFixed(2)
    
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    
    const values = combinedRealtimeData.map(item => item.value)
    moistureStats.value = {
      min: Math.min(...values).toFixed(2),
      max: Math.max(...values).toFixed(2),
      avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2)
    }
  }
  
  requestAnimationFrame(() => {
    updateChart()
  })
}

const updateRealtimeData = (snapshot, deviceId) => {
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
  
  combinedRealtimeData = combinedRealtimeData.filter(item => item.deviceId !== deviceId)
  combinedRealtimeData.push(...newData)
  
  combinedRealtimeData.sort((a, b) => a.timestamp - b.timestamp)
  combinedRealtimeData = combinedRealtimeData.slice(-20)
  
  chartData.value = combinedRealtimeData
  
  if (combinedRealtimeData.length > 0) {
    const latestReading = combinedRealtimeData[combinedRealtimeData.length - 1]
    currentMoistureValue.value = latestReading.value.toFixed(2)
    
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    
    const values = combinedRealtimeData.map(item => item.value)
    moistureStats.value = {
      min: Math.min(...values).toFixed(2),
      max: Math.max(...values).toFixed(2),
      avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2)
    }
  }
  
  requestAnimationFrame(() => {
    updateChart()
  })
}

const initializeChartData = (data) => {
  const initialChartData = data.slice(0, 20)
    .map(item => ({
      timestamp: item.rawTimestamp, 
      value: Number(item.soilMoisture),
      deviceId: item.deviceId || 'unknown'
    }))
    .sort((a, b) => a.timestamp - b.timestamp) 
  
  chartData.value = initialChartData
  combinedRealtimeData = initialChartData
  
  if (initialChartData.length > 0) {
    const latestReading = initialChartData[initialChartData.length - 1]
    currentMoistureValue.value = latestReading.value.toFixed(2)
    
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
  
  initializeChart()
}

const initializeChart = () => {
  nextTick(() => {
    if (chartCanvas.value) {
      if (chart.value) {
        chart.value.destroy()
      }
      
      const ctx = chartCanvas.value.getContext('2d')
      
      chart.value = new Chart(ctx, {
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
            label: 'Soil Moisture (%)',
            data: chartData.value.map(item => item.value),
            borderColor: '#10b981', 
            backgroundColor: 'rgba(16, 185, 129, 0.15)',
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
            duration: 500,
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

const updateChart = () => {
  if (chart.value && chartData.value.length > 0) {
    chart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    
    chart.value.data.datasets[0].data = chartData.value.map(item => item.value)
    
    const values = chartData.value.map(item => item.value)
    if (values.length > 0) {
      chart.value.options.scales.y.min = Math.max(0, Math.min(...values) * 0.95)
      chart.value.options.scales.y.max = Math.min(100, Math.max(...values) * 1.05)
    }
    
    chart.value.update('none') 
  }
}

const calculateSoilStatus = (moisture) => {
  if (moisture >= 70) return 'WET'
  if (moisture >= 30 && moisture < 70) return 'MEDIUM'
  return 'DRY'
}

const filters = ref({
  soilMoisture: { min: '', max: '' }
})

const searchQuery = ref('')
const itemsPerPage = ref(20) 
const currentPage = ref(1)
const activeDropdown = ref(null)
const sortKey = ref('date')
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

const filteredData = computed(() => {
  let result = [...soilMoistureData.value]

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
    saveAs(blob, 'soil_moisture_data.csv')
    window.showToast('Soil Moisture exported as CSV', 'success')
  } else if (format === 'pdf') {
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm'
    })
    
    doc.setFontSize(16)
    doc.text('Soil Moisture Data Report', 105, 15, { align: 'center' })
    
    doc.setFontSize(10)
    const dateStr = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    })
    doc.text(`Generated on: ${dateStr}`, 105, 22, { align: 'center' })
    
    doc.setFontSize(12)
    doc.text('Current Moisture Status:', 15, 30)
    doc.text(`Value: ${currentMoistureValue.value}%`, 15, 36)
    doc.text(`Status: ${calculateSoilStatus(currentMoistureValue.value)}`, 15, 42)
    
    if (chartCanvas.value) {
      const canvas = chartCanvas.value
      const chartImage = canvas.toDataURL('image/png')
      
      const imgWidth = 180 
      const imgHeight = (canvas.height * imgWidth) / canvas.width
      doc.addImage(chartImage, 'PNG', (210 - imgWidth) / 2, 50, imgWidth, imgHeight)
      
      doc.setFontSize(10)
      doc.text('Moisture Statistics:', 15, 50 + imgHeight + 10)
      doc.text(`Minimum: ${moistureStats.value.min}%`, 15, 50 + imgHeight + 16)
      doc.text(`Average: ${moistureStats.value.avg}%`, 15, 50 + imgHeight + 22)
      doc.text(`Maximum: ${moistureStats.value.max}%`, 15, 50 + imgHeight + 28)
      
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
          fillColor: [16, 185, 129], 
          textColor: 255 
        },
        alternateRowStyles: {
          fillColor: [241, 245, 249] 
        },
        margin: { top: 20 }
      })
    } else {
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

  activeDropdown.value = null
}

watch([searchQuery, activeFilters, itemsPerPage], () => {
  currentPage.value = 1
})

let unsubscribe = null

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  fetchSoilMoistureData()
  const cleanup = setupRealtimeListener()
  
  // Store cleanup function
  unsubscribe = cleanup
  
  // Resize handler (remains the same)
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
  
  if (unsubscribe) {
    unsubscribe()
  }
  
  if (socket) {
    socket.close()
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