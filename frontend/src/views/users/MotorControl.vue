<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">
      <div class="bg-gradient-to-r from-emerald-50 to-white p-4 md:p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-sm md:text-xl font-semibold text-gray-800 mb-1">Motor Control Data Table</h1>
            <div class="flex items-center text-xs md:text-sm text-gray-500">
              <span class="text-emerald-600 font-medium">Motor Control</span>
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
      <div class="flex-1 overflow-auto md:overflow-hidden flex flex-col md:flex-row">
        <!-- Live Graph Container - Smaller width compared to table, now scrollable -->
        <div class="w-full md:w-1/3 lg:w-1/3 md:max-w-[33.333%] border-r border-gray-200 bg-white p-4 md:overflow-y-auto flex-shrink-0">
          <div class="mb-3">
            <h3 class="text-xs md:text-sm font-semibold text-gray-700">Motor Activity Monitor</h3>
            <p class="text-[10px] md:text-xs text-gray-500">Real-time status tracking</p>
          </div>
          
          <!-- Motor Status Graph Container - FIXED: Add container constraints -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4 max-w-full">
            <!-- Graph Header with improved styling -->
            <div class="p-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
              <div class="flex items-center gap-4">
                <div class="flex items-center">
                  <div class="w-3 h-3 rounded-full bg-purple-500 mr-1.5"></div>
                  <span class="text-[10px] md:text-xs font-medium text-gray-700">Status</span>
                </div>
              </div>
              <div class="text-[10px] md:text-xs text-gray-500">
                Last updated: {{ lastUpdated }}
              </div>
            </div>
            
            <!-- Graph Canvas with current values overlay - FIXED: Add strict size constraints -->
            <div class="h-[320px] p-3 relative w-full overflow-hidden">
              <canvas 
                ref="chartCanvas" 
                class="w-full h-full max-w-full"
                :style="{ maxWidth: '100%', maxHeight: '320px' }"
              ></canvas>
              
              <!-- Current Status Indicator -->
              <div class="absolute top-3 left-3 bg-white/95 backdrop-blur-sm rounded-md px-2 py-1 shadow-sm border border-gray-100" style="max-width: 100px; z-index: 10;">
                <div class="text-[10px] font-medium text-gray-500 mb-0.5">Current Status</div>
                <div class="flex items-center">
                  <div class="w-1.5 h-1.5 rounded-full" :class="currentStatus === 'ON' ? 'bg-green-500' : 'bg-red-500'" mr-1></div>
                  <div class="text-xs font-bold" :class="currentStatus === 'ON' ? 'text-green-600' : 'text-red-600'">
                    {{ currentStatus }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Enhanced Graph Footer with Stats -->
            <div class="border-t border-gray-100 p-3">
              <!-- Status Stats -->
              <div>
                <div class="flex items-center mb-2">
                  <div class="w-3 h-3 rounded-full bg-purple-500 mr-1.5"></div>
                  <div class="text-sm font-medium text-gray-700">Status Summary</div>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-purple-50/50 rounded-md p-2">
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">ON Count</div>
                    <div class="text-sm font-semibold text-purple-600">{{ statusStats.onCount }}</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">OFF Count</div>
                    <div class="text-sm font-semibold text-purple-600">{{ statusStats.offCount }}</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Switches</div>
                    <div class="text-sm font-semibold text-purple-600">{{ statusStats.switches }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Motor Information Card -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Motor Information</h4>
            <div class="space-y-2 text-xs">
              <div class="flex justify-between">
                <span class="text-gray-500">Motor ID:</span>
                <span class="font-medium text-gray-700">{{ currentDeviceId }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Controller:</span>
                <span class="font-medium text-gray-700">{{ currentUser }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-500">Status:</span>
                <span class="font-medium" :class="currentStatus === 'ON' ? 'text-green-600' : 'text-red-600'">
                  {{ currentStatus }}
                </span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- Table Container - Larger width -->
        <div class="w-full md:w-2/3 lg:w-2/3 md:max-w-[66.666%] flex flex-col flex-grow min-w-0">
          <!-- Mobile Card View (shown on small screens) -->
          <div class="sm:hidden flex-1 overflow-auto bg-white p-3 space-y-3">
            <div v-for="(row, index) in paginatedData" :key="index" 
                class="bg-gray-50 rounded-lg p-3 border border-gray-200">
              <div class="flex justify-between items-start mb-2">
                <div>
                  <div class="text-xs font-medium text-gray-900">{{ row.date }}</div>
                  <div class="text-[10px] text-gray-500">{{ row.time }}</div>
                </div>
                <span 
                  :class="[
                    'px-2 py-0.5 rounded-full text-[10px] font-medium',
                    row.status === 'ON' ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
                  ]"
                >
                  {{ row.status }}
                </span>
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Device ID</div>
                  <div class="text-xs font-semibold text-teal-600">{{ row.deviceId || '--' }}</div>
                </div>
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">User</div>
                  <div class="text-xs font-semibold text-blue-600">{{ row.user || '--' }}</div>
                </div>
          
              </div>
            </div>
            
            <div v-if="paginatedData.length === 0 && !isLoading" 
                class="flex flex-col items-center justify-center py-8">
              <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
              <p class="text-gray-500 text-xs font-medium">No motor control data found</p>
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
                    <th class="w-[10%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium text-gray-500 uppercase tracking-wider border-b">
                      ID
                    </th>
                    <th class="w-[15%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-teal-600">Device ID</div>
                      <div class="text-gray-400 text-[10px]">IDENTIFIER</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-purple-600">Motor Status</div>
                      <div class="text-gray-400 text-[10px]">ON/OFF</div>
                    </th>
                    <th class="w-[15%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-blue-600">User</div>
                      <div class="text-gray-400 text-[10px]">CONTROLLER</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-gray-600">Date</div>
                      <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-gray-600">Time</div>
                      <div class="text-gray-400 text-[10px]">HH:MM:SS AM/PM</div>
                    </th>
                  </tr>
                </thead>
              </table>
            </div>
            
            <!-- Scrollable Body with enhanced styling -->
            <div class="flex-1 overflow-y-auto">
              <table class="min-w-full w-[600px]">
                <tbody>
                  <tr 
                    v-for="(row, index) in paginatedData" 
                    :key="index"
                    class="border-b border-gray-50 last:border-0"
                  >
                    <td class="w-[10%] px-4 py-3.5 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-700">{{ row.id }}</div>
                    </td>
                    <td class="w-[15%] px-4 py-3.5 whitespace-nowrap">
                      <div class="text-sm font-medium text-teal-600">{{ row.deviceId || '--' }}</div>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                      <span 
                        :class="[
                          'px-3 py-1 rounded-full text-sm font-medium',
                          row.status === 'ON' ? 'bg-purple-100 text-purple-800' : 'bg-gray-100 text-gray-800'
                        ]"
                      >
                        {{ row.status }}
                      </span>
                    </td>
                    <td class="w-[15%] px-4 py-3.5 whitespace-nowrap">
                      <div class="text-sm font-medium text-blue-600">{{ row.user || '--' }}</div>
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
                    <td colspan="6" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <FileSearch class="h-16 w-16 text-gray-300 mb-4" />
                        <p class="text-gray-500 text-lg font-medium">No motor control data found</p>
                        <p class="text-gray-400 text-sm mt-1">Try adjusting your search or filters</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Mobile Pagination -->
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
    </div>
  </div>

  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Motor Control Data" 
    message="Please wait while we fetch the latest motor control logs"
  />
</template>
  
<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Search, Filter, Download, ChevronDown, ChevronRight, ChevronLeft, ArrowUpDown, FileText, FileSearch, Printer, MoreHorizontal } from 'lucide-vue-next'
import LoadingPage from '../layout/LoadingPage.vue'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun } from 'docx'
import { saveAs } from 'file-saver'
import api from '../../api/index'

import Chart from 'chart.js/auto'

const motorData = ref([])
const isLoading = ref(false)

const chartCanvas = ref(null)
const chart = ref(null)

const chartData = ref([])

const currentStatus = ref('--')
const currentDeviceId = ref('--')
const currentUser = ref('--')
const lastUpdated = ref('--')
const statusStats = ref({
  onCount: 0,
  offCount: 0,
  switches: 0
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
  
  const tempMotorRows = sortedData.value.map(row => ({
    id: row.id,
    deviceId: row.deviceId,
    status: row.status,
    user: row.user,
    date: row.date,
    time: row.time
  }));
  
  const printChartData = chartData.value
    .slice(-PRINT_CHART_DATA_LIMIT)
    .map(item => ({
      timestamp: item.timestamp,
      status: item.status,
      value: item.status === 'ON' ? 1 : 0
    }))
    .sort((a, b) => a.timestamp - b.timestamp); 
  
  console.log(`📊 Print chart will show ${printChartData.length} motor status records`);
  
  const onCount = printChartData.filter(item => item.status === 'ON').length;
  const offCount = printChartData.filter(item => item.status === 'OFF').length;
  const totalCount = printChartData.length;
  const onPercentage = totalCount > 0 ? ((onCount / totalCount) * 100).toFixed(1) : 0;
  
  let chartImage = '';
  
  try {
    const ctx = tempCanvas.getContext('2d');
    
    const motorChart = new Chart(ctx, {
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
            label: 'Motor Status',
            data: printChartData.map(item => item.value),
            borderColor: '#a855f7', 
            backgroundColor: 'rgba(168, 85, 247, 0.15)',
            borderWidth: 3,
            tension: 0.1,
            fill: true,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#a855f7',
            pointBorderWidth: 2,
            stepped: true
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
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const value = context.raw === 1 ? 'ON' : 'OFF';
                return `Status: ${value}`;
              }
            }
          }
        },
        scales: {
          y: {
            type: 'linear',
            display: true,
            title: {
              display: true,
              text: 'Status (ON/OFF)',
              color: '#a855f7',
              font: {
                size: 14,
                weight: '600'
              }
            },
            min: -0.2,
            max: 1.2,
            ticks: {
              font: { size: 12 },
              color: '#a855f7',
              padding: 10,
              stepSize: 1,
              callback: function(value) {
                return value === 0 ? 'OFF' : value === 1 ? 'ON' : '';
              }
            },
            grid: {
              color: 'rgba(168, 85, 247, 0.1)',
              drawBorder: false
            }
          },
          x: {
            ticks: {
              font: { size: 10 },
              color: '#64748b',
              maxTicksLimit: 10,
              maxRotation: 45
            },
            grid: {
              display: false,
              drawBorder: false
            }
          }
        }
      }
    });
    
    setTimeout(async () => {
      try {
        chartImage = tempCanvas.toDataURL('image/png', 1.0);
        
        motorChart.destroy();
        document.body.removeChild(tempContainer);
        
        generatePrintHTML(chartImage, tempMotorRows, formattedDate, now, 
                         printChartData.length, onCount, offCount, onPercentage);
      } catch (error) {
        console.error('Error capturing chart:', error);
        document.body.removeChild(tempContainer);
        generatePrintHTML('', tempMotorRows, formattedDate, now, 0, 0, 0, 0);
      }
    }, 500);
    
  } catch (error) {
    console.error('Error creating chart:', error);
    document.body.removeChild(tempContainer);
    generatePrintHTML('', tempMotorRows, formattedDate, now, 0, 0, 0, 0);
  }
};

const generatePrintHTML = (chartImage, tempMotorRows, formattedDate, now, 
                          chartRecordCount, onCount, offCount, onPercentage) => {
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Motor Control Data Report</title>
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
        .status-on { color: #059669; font-weight: 500; }
        .status-off { color: #dc2626; font-weight: 500; }
        .device-id { color: #0891b2; }
        .user { color: #7c3aed; }
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
          grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
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
        .stat-item.on { border-left: 4px solid #059669; }
        .stat-item.off { border-left: 4px solid #dc2626; }
        .stat-item.percentage { border-left: 4px solid #7c3aed; }
        .stat-item h4 {
          margin: 0 0 10px 0;
          font-size: 14px;
          font-weight: 600;
        }
        .stat-item.on h4 { color: #059669; }
        .stat-item.off h4 { color: #dc2626; }
        .stat-item.percentage h4 { color: #7c3aed; }
        .stat-values {
          font-size: 18px;
          font-weight: bold;
          color: #374151;
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
        <h1>Motor Control Data Report</h1>
        <div class="date">${formattedDate}</div>
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-item">
          <span class="summary-label">Total Records:</span>
          <span class="summary-value">${tempMotorRows.length}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Chart Data Points:</span>
          <span class="summary-value">${chartRecordCount}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Date Range:</span>
          <span class="summary-value">${tempMotorRows.length > 0 ? tempMotorRows[tempMotorRows.length-1].date + ' to ' + tempMotorRows[0].date : 'N/A'}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Report Generated:</span>
          <span class="summary-value">${now.toLocaleString()}</span>
        </div>
      </div>
      
      <div class="section-header">Motor Status Trend Analysis</div>
      ${chartImage ? `
        <div class="chart-title">Motor Status Over Time</div>
        <div class="chart-info">Showing ${chartRecordCount} most recent data points</div>
        <img src="${chartImage}" class="chart-image" alt="Motor Status Chart" />
        
        <div class="stats-summary">
          <div class="stat-item on">
            <h4>ON Count</h4>
            <div class="stat-values">${onCount}</div>
          </div>
          <div class="stat-item off">
            <h4>OFF Count</h4>
            <div class="stat-values">${offCount}</div>
          </div>
          <div class="stat-item percentage">
            <h4>ON Percentage</h4>
            <div class="stat-values">${onPercentage}%</div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">Chart could not be generated</p>'}
      
      <div class="section-header">Detailed Motor Control Logs</div>
      <table>
        <thead>
          <tr>
            <th style="width: 8%">ID</th>
            <th style="width: 15%">Device ID</th>
            <th style="width: 12%">Status</th>
            <th style="width: 15%">User</th>
            <th style="width: 15%">Date</th>
            <th style="width: 15%">Time</th>
          </tr>
        </thead>
        <tbody>
          ${tempMotorRows.map(row => `
            <tr>
              <td>${row.id}</td>
              <td><span class="device-id">${row.deviceId || '--'}</span></td>
              <td><span class="status-${row.status.toLowerCase()}">${row.status}</span></td>
              <td><span class="user">${row.user || '--'}</span></td>
              <td>${row.date}</td>
              <td>${row.time}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by Motor Control Monitoring System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
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

const fetchMotorControlData = async (showLoading = false) => {
  try {
    if (showLoading) {
      isLoading.value = true
    }
    
    // Fetch current status
    const currentResponse = await api.get('/motor-control/current')
    const currentData = currentResponse.data
    
    // Fetch history (no limit parameter)
    const historyResponse = await api.get('/motor-control/history')
    const motorDataFromApi = historyResponse.data
    
    const processedData = motorDataFromApi.map((data, index) => {
      let formattedDate = '--'
      let formattedTime = '--'
      let timestampSeconds = 0
      
      try {
        // Handle MongoDB timestamp - various formats
        let timestamp
        if (data.timestamp instanceof Date) {
          timestamp = data.timestamp
        } else if (data.timestamp && typeof data.timestamp === 'object' && data.timestamp._seconds) {
          // Firebase timestamp format
          timestamp = new Date(data.timestamp._seconds * 1000)
        } else if (typeof data.timestamp === 'string') {
          // ISO string format
          timestamp = new Date(data.timestamp)
        } else {
          timestamp = new Date()
        }
        
        formattedDate = timestamp.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: '2-digit'
        })

        formattedTime = timestamp.toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        })
        
        timestampSeconds = timestamp.getTime() / 1000
      } catch (e) {
        console.error("Error formatting date:", e)
      }

      // Handle status from various fields
      let status = 'OFF'
      if (data.status !== undefined && data.status !== null) {
        status = data.status ? 'ON' : 'OFF'
      } else if (data.action) {
        status = data.action.toLowerCase() === 'on' ? 'ON' : 'OFF'
      }

      const deviceId = data.device_id || data.deviceId || 'main_motor'
      const user = data.user || data.triggeredBy || 'system'

      return {
        id: index + 1,
        timestamp: timestampSeconds,
        rawTimestamp: data.timestamp,
        deviceId: deviceId,
        status: status,
        user: user,
        date: formattedDate,
        time: formattedTime,
        action: data.action || '',
        source: data.triggeredBy || 'manual',
        scheduleId: data.scheduleId || ''
      }
    })

    motorData.value = processedData
    
    // Initialize chart with limited data to prevent performance issues
    const limitedChartData = processedData.slice(-15) // Only use last 100 entries for chart
    initializeChartData(limitedChartData)
    
    // Update current values from the current status endpoint
    if (currentData) {
      currentStatus.value = currentData.status ? 'ON' : 'OFF'
      currentDeviceId.value = currentData.device_id || 'main_motor'
      currentUser.value = currentData.user || 'system'
      
      if (currentData.timestamp) {
        let timestamp
        if (currentData.timestamp instanceof Date) {
          timestamp = currentData.timestamp
        } else if (currentData.timestamp && typeof currentData.timestamp === 'object' && currentData.timestamp._seconds) {
          timestamp = new Date(currentData.timestamp._seconds * 1000)
        } else if (typeof currentData.timestamp === 'string') {
          timestamp = new Date(currentData.timestamp)
        } else {
          timestamp = new Date()
        }
        
        const formattedTime = timestamp.toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        })
        lastUpdated.value = formattedTime
      }
    }
    
    if (showLoading) {
      isLoading.value = false
    }

    PRINT_CHART_DATA_LIMIT = motorData.value // Limit chart data for printing
    
  } catch (error) {
    console.error("❌ Error fetching motor control data:", error)
    isLoading.value = false
  }
}

const pollingInterval = ref(null)

const setupDataPolling = () => {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }
  
  pollingInterval.value = setInterval(async () => {
    try {
      const response = await api.get('/motor-control/latest')
      const latestData = response.data[0] // Get first item from array
      
      if (latestData) {
        // Handle timestamp conversion
        let timestamp
        if (latestData.timestamp instanceof Date) {
          timestamp = latestData.timestamp
        } else if (latestData.timestamp && typeof latestData.timestamp === 'object' && latestData.timestamp._seconds) {
          timestamp = new Date(latestData.timestamp._seconds * 1000)
        } else if (typeof latestData.timestamp === 'string') {
          timestamp = new Date(latestData.timestamp)
        } else {
          timestamp = new Date()
        }
        
        const status = latestData.status ? 'ON' : 'OFF'
        const deviceId = latestData.device_id || 'main_motor'
        const user = latestData.user || latestData.triggeredBy || 'system'
        
        // Check if this is a new status update
        const lastEntry = chartData.value[chartData.value.length - 1]
        const isNewEntry = !lastEntry || 
                          lastEntry.status !== status || 
                          lastEntry.timestamp.getTime() !== timestamp.getTime()
        
        if (isNewEntry) {
          const newChartData = [
            ...chartData.value,
            {
              timestamp,
              status,
              deviceId,
              user,
              source: latestData.triggeredBy || 'polling'
            }
          ]
          
          if (newChartData.length > 50) {
            newChartData.splice(0, newChartData.length - 50)
          }
          
          chartData.value = newChartData
          
          currentStatus.value = status
          currentDeviceId.value = deviceId
          currentUser.value = user
          
          const formattedTime = timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
          })
          lastUpdated.value = formattedTime
          
          const onCount = newChartData.filter(item => item.status === 'ON').length
          const offCount = newChartData.filter(item => item.status === 'OFF').length
          
          let switches = 0
          for (let i = 1; i < newChartData.length; i++) {
            if (newChartData[i].status !== newChartData[i-1].status) {
              switches++
            }
          }
          
          statusStats.value = {
            onCount,
            offCount,
            switches
          }
          
          if (chart.value) {
            try {
              // Update chart data directly
              const labels = newChartData.map(item => 
                item.timestamp.toLocaleTimeString('en-US', {
                  hour: '2-digit',
                  minute: '2-digit',
                  hour12: true
                })
              )
              
              const statusValues = newChartData.map(item => item.status === 'ON' ? 1 : 0)
              
              chart.value.data.labels = labels
              chart.value.data.datasets[0].data = statusValues
              
              requestAnimationFrame(() => {
                chart.value.update('none')
              })
            } catch (error) {
              console.error('Chart update error:', error)
            }
          }
        }
      }
    } catch (error) {
      console.error("Error in data polling:", error)
    }
  }, 5000) // Poll every 5 seconds
  
  return pollingInterval.value
}

const initializeChartData = (data) => {
  const initialChartData = data.slice(0, 50)
    .map(item => {
      // Handle timestamp from various formats
      let timestamp
      if (item.rawTimestamp instanceof Date) {
        timestamp = item.rawTimestamp
      } else if (item.rawTimestamp && typeof item.rawTimestamp === 'object' && item.rawTimestamp._seconds) {
        timestamp = new Date(item.rawTimestamp._seconds * 1000)
      } else if (typeof item.rawTimestamp === 'string') {
        timestamp = new Date(item.rawTimestamp)
      } else {
        timestamp = new Date()
      }
      
      return {
        timestamp: timestamp,
        status: item.status,
        deviceId: item.deviceId,
        user: item.user
      }
    })
    .sort((a, b) => a.timestamp - b.timestamp)

  chartData.value = initialChartData

  if (initialChartData.length > 0) {
    const latestReading = initialChartData[initialChartData.length - 1]
    currentStatus.value = latestReading.status
    currentDeviceId.value = latestReading.deviceId
    currentUser.value = latestReading.user
    
    const formattedTime = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    lastUpdated.value = formattedTime
    
    const onCount = initialChartData.filter(item => item.status === 'ON').length
    const offCount = initialChartData.filter(item => item.status === 'OFF').length
    
    let switches = 0
    for (let i = 1; i < initialChartData.length; i++) {
      if (initialChartData[i].status !== initialChartData[i-1].status) {
        switches++
      }
    }
    
    statusStats.value = {
      onCount,
      offCount,
      switches
    }
  }
  
  // Wait for DOM to be ready, then initialize chart
  nextTick(() => {
    setTimeout(() => {
      initializeChart()
    }, 100)
  })
}

const initializeChart = () => {
  if (!chartCanvas.value) {
    console.warn('Chart canvas not available');
    return;
  }
  
  // Destroy existing chart
  if (chart.value) {
    chart.value.destroy();
    chart.value = null;
  }
  
  try {
    const ctx = chartCanvas.value.getContext('2d');
    if (!ctx) {
      console.error('Could not get canvas context');
      return;
    }
    
    // Ensure chartData has valid values
    const statusValues = chartData.value.map(item => {
      return item.status === 'ON' ? 1 : 0;
    });
    
    // Ensure we have valid labels
    const labels = chartData.value.map(item => {
      if (!item.timestamp || !(item.timestamp instanceof Date) || isNaN(item.timestamp)) {
        return '--:--';
      }
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      });
    });
    
    chart.value = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [
          {
            label: 'Motor Status',
            data: statusValues,
            borderColor: '#a855f7',
            backgroundColor: 'rgba(168, 85, 247, 0.15)',
            borderWidth: 3,
            tension: 0.1,
            fill: true,
            pointRadius: 5,
            pointHoverRadius: 7,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#a855f7',
            pointBorderWidth: 2,
            stepped: true
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
          duration: 800,
          easing: 'easeOutQuart'
        },
        layout: {
          padding: {
            top: 20,
            left: 20,
            right: 20,
            bottom: 20
          }
        },
        scales: {
          y: {
            type: 'linear',
            display: true,
            title: {
              display: true,
              text: 'Status (ON/OFF)',
              color: '#a855f7',
              font: {
                size: 14,
                weight: '600'
              },
              padding: {
                bottom: 15
              }
            },
            min: -0.2,
            max: 1.2,
            ticks: {
              font: {
                size: 12
              },
              color: '#a855f7',
              padding: 10,
              stepSize: 1,
              callback: function(value) {
                return value === 0 ? 'OFF' : value === 1 ? 'ON' : '';
              }
            },
            grid: {
              color: 'rgba(168, 85, 247, 0.1)',
              drawBorder: false,
              lineWidth: 1
            }
          },
          x: {
            ticks: {
              font: {
                size: 11
              },
              maxRotation: 45,
              padding: 10,
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
            padding: 15,
            cornerRadius: 8,
            displayColors: true,
            boxWidth: 10,
            boxHeight: 10,
            usePointStyle: true,
            titleFont: {
              size: 13,
              weight: '600'
            },
            bodyFont: {
              size: 12
            },
            callbacks: {
              label: function(context) {
                const value = context.raw === 1 ? 'ON' : 'OFF';
                return `Status: ${value}`;
              }
            }
          }
        }
      }
    });
    
  } catch (error) {
    console.error('Error initializing chart:', error);
  }
};

const updateChart = () => {
  if (chart.value && chartData.value.length > 0 && chartCanvas.value) {
    try {
      // Update labels safely
      const labels = chartData.value.map(item => {
        if (!item.timestamp || !(item.timestamp instanceof Date) || isNaN(item.timestamp)) {
          return '--:--'
        }
        return item.timestamp.toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        })
      })
      
      // Update data values
      const statusValues = chartData.value.map(item => item.status === 'ON' ? 1 : 0)
      
      // Update chart data
      chart.value.data.labels = labels
      chart.value.data.datasets[0].data = statusValues
      
      // Update the chart without animation to prevent performance issues
      chart.value.update('none')
    } catch (error) {
      console.error('Error updating chart:', error)
    }
  }
}

const handleResize = () => {
  if (chart.value) {
    // Just resize the existing chart, don't recreate
    chart.value.resize()
  }
}

const filters = ref({
  id: { min: '', max: '' },
  deviceId: { min: '', max: '' },
  status: { min: '', max: '' },
  user: { min: '', max: '' },
  date: { min: '', max: '' },
  time: { min: '', max: '' }
})

const statusFilter = ref('')
const textFilters = ref({
  deviceId: '',
  user: ''
})

const searchQuery = ref('')
const itemsPerPage = ref(20)
const currentPage = ref(1)
const activeDropdown = ref(null)
const sortKey = ref('id')
const sortDirection = ref('asc')
const activeFilters = ref({})
const activeTextFilters = ref({})

const filterFields = [
  { key: 'id', label: 'ID' },
  { key: 'deviceId', label: 'Device ID' },
  { key: 'status', label: 'Motor Status' },
  { key: 'user', label: 'User' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const headers = [
  { key: 'id', label: 'ID' },
  { key: 'deviceId', label: 'Device ID' },
  { key: 'status', label: 'Motor Status' },
  { key: 'user', label: 'User' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const exportFormats = ['csv', 'pdf']

const filteredData = computed(() => {
  let result = [...motorData.value]

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  if (statusFilter.value) {
    result = result.filter(row => row.status === statusFilter.value)
  }

  Object.keys(activeTextFilters.value).forEach(key => {
    const value = activeTextFilters.value[key]
    if (value) {
      result = result.filter(row => 
        String(row[key]).toLowerCase().includes(value.toLowerCase())
      )
    }
  })

  Object.keys(activeFilters.value).forEach(key => {
    if (key === 'status') return
    
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
    
    if (aValue === '' || aValue === undefined || aValue === '--') aValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    if (bValue === '' || bValue === undefined || bValue === '--') bValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    
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

  const newTextFilters = {}
  Object.keys(textFilters.value).forEach(key => {
    if (textFilters.value[key]) {
      newTextFilters[key] = textFilters.value[key]
    }
  })

  activeFilters.value = newFilters
  activeTextFilters.value = newTextFilters
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
    saveAs(blob, 'motor_control_data.csv')
    window.showToast('Motor Control exported as CSV', 'success')
  } else if (format === 'pdf') {
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm'
    });
    
    doc.setFontSize(16);
    doc.text('Motor Control Report', 105, 15, { align: 'center' });
    
    doc.setFontSize(10);
    const dateStr = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    doc.text(`Generated on: ${dateStr}`, 105, 22, { align: 'center' });
    
    doc.setFontSize(12);
    doc.text('Current Status:', 15, 30);
    doc.text(`Motor: ${currentStatus.value}`, 15, 36);
    doc.text(`Device ID: ${currentDeviceId.value}`, 15, 42);
    doc.text(`Controller: ${currentUser.value}`, 15, 48);
    doc.text(`Last Updated: ${lastUpdated.value}`, 15, 54);
    
    if (chartCanvas.value) {
      try {
        const canvas = chartCanvas.value;
        const chartImage = canvas.toDataURL('image/png');
        
        const imgWidth = 180; 
        const imgHeight = (canvas.height * imgWidth) / canvas.width;
        doc.addImage(chartImage, 'PNG', (210 - imgWidth) / 2, 60, imgWidth, imgHeight);
        
        doc.setFontSize(10);
        doc.text('Motor Activity Statistics:', 15, 60 + imgHeight + 10);
        doc.text(`ON Count: ${statusStats.value.onCount}`, 15, 60 + imgHeight + 16);
        doc.text(`OFF Count: ${statusStats.value.offCount}`, 15, 60 + imgHeight + 22);
        doc.text(`Status Switches: ${statusStats.value.switches}`, 15, 60 + imgHeight + 28);
        
        doc.addPage();
        doc.setFontSize(14);
        doc.text('Motor Control Data Table', 105, 15, { align: 'center' });
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
            fillColor: [139, 92, 246], 
            textColor: 255 
          },
          alternateRowStyles: {
            fillColor: [245, 243, 255] 
          },
          margin: { top: 20 },
          columnStyles: {
            0: { cellWidth: 15 }, 
            1: { cellWidth: 25 }, 
            2: { cellWidth: 20 }, 
            3: { cellWidth: 20 }, 
            4: { cellWidth: 20 },
            5: { cellWidth: 20 }  
          }
        });
      } catch (error) {
        console.error('Error adding chart to PDF:', error);
        doc.text('Motor Status Chart Not Available', 105, 60, { align: 'center' });
        autoTable(doc, {
          head: [exportHeaders],
          body: exportRows,
          startY: 70,
          styles: { fontSize: 10 }
        });
      }
    } else {
      doc.text('Motor Status Chart Not Available', 105, 60, { align: 'center' });
      autoTable(doc, {
        head: [exportHeaders],
        body: exportRows,
        startY: 70,
        styles: { fontSize: 10 }
      });
    }
    
    doc.save('motor_control_report.pdf');
    window.showToast('Motor Control report exported as PDF', 'success');
  }

  activeDropdown.value = null
}

watch([searchQuery, activeFilters, activeTextFilters, statusFilter, itemsPerPage], () => {
  currentPage.value = 1
})

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  fetchMotorControlData(true)
  const pollingInterval = setupDataPolling() 
  
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  
  if (chart.value) {
    chart.value.destroy()
    chart.value = null
  }
  
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
  
  window.removeEventListener('resize', handleResize)
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

/* FIXED Canvas styling - prevent compression */
canvas {
  display: block !important;
  width: 100% !important;
  height: 100% !important;
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

/* Add animation for refresh icon */
.animate-spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
