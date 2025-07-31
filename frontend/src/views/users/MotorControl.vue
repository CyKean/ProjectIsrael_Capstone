<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-15px)] h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-hidden">
      <!-- Gradient header for visual appeal -->
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
          <div class="flex items-center gap-2 flex-wrap md:flex-nowrap">
            <!-- Wider search bar -->
            <div class="relative w-72">
              <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search motor control logs..."
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
                      <select
                        v-if="field.key === 'status'"
                        v-model="statusFilter"
                        class="w-full px-3 py-1.5 text-xs md:text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
                      >
                        <option value="">All</option>
                        <option value="ON">ON</option>
                        <option value="OFF">OFF</option>
                      </select>
                      <input
                        v-else-if="field.key === 'deviceId' || field.key === 'user'"
                        v-model="textFilters[field.key]"
                        type="text"
                        :placeholder="`Filter by ${field.label}`"
                        class="w-full px-3 py-1.5 text-sm border border-gray-200 rounded-md focus:ring-1 focus:ring-emerald-500 focus:border-emerald-500"
                      />
                      <template v-else>
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
                      </template>
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
            <h3 class="text-xs md:text-sm font-semibold text-gray-700">Motor Activity Monitor</h3>
            <p class="text-[10px] md:text-xs text-gray-500">Real-time status tracking</p>
          </div>
          
          <!-- Motor Status Graph Container -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
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
            
            <!-- Graph Canvas with current values overlay -->
            <div class="h-[280px] p-3 relative">
              <canvas ref="chartCanvas" class="w-full h-full"></canvas>
              
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
        <div class="w-full md:w-2/3 lg:w-2/3 flex flex-col">
          <!-- Fixed Header with enhanced styling -->
          <div class="w-full border-b border-gray-200 sticky top-0 z-10 bg-gray-50">
            <table class="hidden md:blockmin-w-full">
              <thead>
                <tr>
                  <th class="w-[10%] py-3.5 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    ID
                  </th>
                  <th class="w-[15%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-teal-600">Device ID</div>
                    <div class="text-gray-400 text-[10px]">IDENTIFIER</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-purple-600">Motor Status</div>
                    <div class="text-gray-400 text-[10px]">ON/OFF</div>
                  </th>
                  <th class="w-[15%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-blue-600">User</div>
                    <div class="text-gray-400 text-[10px]">CONTROLLER</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-gray-600">Date</div>
                    <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
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
              <thead class=md:hidden>
                <tr>
                  <th class="w-[10%] py-3.5 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b">
                    ID
                  </th>
                  <th class="w-[15%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-teal-600">Device ID</div>
                    <div class="text-gray-400 text-[10px]">IDENTIFIER</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-purple-600">Motor Status</div>
                    <div class="text-gray-400 text-[10px]">ON/OFF</div>
                  </th>
                  <th class="w-[15%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-blue-600">User</div>
                    <div class="text-gray-400 text-[10px]">CONTROLLER</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-gray-600">Date</div>
                    <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs font-medium uppercase tracking-wider border-b">
                    <div class="text-gray-600">Time</div>
                    <div class="text-gray-400 text-[10px]">HH:MM:SS AM/PM</div>
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
  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Motor Control Data" 
    message="Please wait while we fetch the latest motor control logs"
  />
  <Settings />
</template>
  
<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { Search, Filter, Download, ChevronDown, ChevronRight, ChevronLeft, ArrowUpDown, FileText, FileSearch} from 'lucide-vue-next'
import Sidebar from '../layout/Sidebar.vue'
import LoadingPage from '../layout/LoadingPage.vue'
import Settings from '../layout/Settings.vue'
import {
  getFirestore,
  collection,
  query,
  orderBy,
  getDocs,
  where,
  Timestamp,
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
const motorData = ref([])
const isLoading = ref(false) // Changed to false by default

// Chart references
const chartCanvas = ref(null)
const chart = ref(null)

// Chart data
const chartData = ref([])

// Current values and stats
const currentStatus = ref('--')
const currentDeviceId = ref('--')
const currentUser = ref('--')
const lastUpdated = ref('--')
const statusStats = ref({
  onCount: 0,
  offCount: 0,
  switches: 0
})

// Fetch motor control data
const fetchMotorControlData = async (showLoading = false) => {
  try {
    // Only show loading screen if explicitly requested
    if (showLoading) {
      isLoading.value = true
    }
    
    // Query the motor_status collection
    const motorQuery = query(
      collection(db, "motor_status", "history", "logs"),
      orderBy("timestamp", "desc"),  // Latest first
      limit(50) // Limit to 50 records for better performance
    )
    const motorSnapshot = await getDocs(motorQuery)
    
    // Process motor control readings
    const processedData = motorSnapshot.docs.map((doc, index) => {
      const data = doc.data()
      
      // Handle timestamp
      let formattedDate = '--'
      let formattedTime = '--'
      let timestampSeconds = 0
      
      try {
        const timestamp = data.timestamp instanceof Timestamp 
          ? new Date(data.timestamp.toMillis())
          : data.timestamp?.toDate?.() || 
            (data.timestamp?.seconds ? new Date(data.timestamp.seconds * 1000) : new Date())
        
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
        
        timestampSeconds = data.timestamp?.seconds || timestamp.getTime() / 1000
      } catch (e) {
        console.error("Error formatting date:", e)
      }

      // Process status - handle different data types
      let status = 'OFF'; // Default status
      if (data.status !== undefined && data.status !== null) {
        // Convert to string and handle boolean values
        if (typeof data.status === 'boolean') {
          status = data.status ? 'ON' : 'OFF';
        } else if (typeof data.status === 'number') {
          status = data.status === 1 ? 'ON' : 'OFF';
        } else {
          // Handle string or other types
          const statusStr = String(data.status).trim().toUpperCase();
          if (['ON', 'OFF', '1', '0', 'TRUE', 'FALSE'].includes(statusStr)) {
            status = ['ON', '1', 'TRUE'].includes(statusStr) ? 'ON' : 'OFF';
          }
        }
      }

      // Get device ID and user from the data
      const deviceId = data.device_id || data.deviceId || 'main_motor'
      const user = data.user || data.controller || 'system'

      // Return processed data
      return {
        id: index + 1,
        timestamp: timestampSeconds,
        rawTimestamp: data.timestamp,
        deviceId: deviceId,
        status: status,
        user: user,
        date: formattedDate,
        time: formattedTime
      }
    })

    // Update data immediately without artificial delay
    motorData.value = processedData
    
    // Initialize chart data after loading
    initializeChartData(processedData)
    
    // Hide loading indicator if it was shown
    if (showLoading) {
      isLoading.value = false
    }
    
  } catch (error) {
    console.error("❌ Error fetching motor control data:", error)
    isLoading.value = false
  }
}

// Setup real-time listener for chart data
const setupRealtimeListener = () => {
  // Query for the most recent readings (limit to 20 for the chart)
  const realtimeQuery = query(
    collection(db, "motor_status", "history", "logs"),
    orderBy("timestamp", "desc"),
    // limit(20)
  )
  
  // Set up the listener
  return onSnapshot(realtimeQuery, (snapshot) => {
    // Process the data for the charts
    const newData = snapshot.docs
      .map(doc => {
        const data = doc.data()
        const timestamp = data.timestamp instanceof Timestamp 
          ? new Date(data.timestamp.toMillis())
          : data.timestamp?.toDate?.() || 
            (data.timestamp?.seconds ? new Date(data.timestamp.seconds * 1000) : new Date())
        
        // Process status
        let status = 'OFF'; // Default status
        if (data.status !== undefined && data.status !== null) {
          if (typeof data.status === 'boolean') {
            status = data.status ? 'ON' : 'OFF';
          } else if (typeof data.status === 'number') {
            status = data.status === 1 ? 'ON' : 'OFF';
          } else {
            const statusStr = String(data.status).trim().toUpperCase();
            if (['ON', 'OFF', '1', '0', 'TRUE', 'FALSE'].includes(statusStr)) {
              status = ['ON', '1', 'TRUE'].includes(statusStr) ? 'ON' : 'OFF';
            }
          }
        }
        
        // Get device ID and user
        const deviceId = data.device_id || data.deviceId || 'main_motor'
        const user = data.user || data.controller || 'system'
        
        return {
          timestamp,
          status,
          deviceId,
          user
        }
      })
      .sort((a, b) => a.timestamp - b.timestamp) // Sort by timestamp ascending for the chart
    
    // Update chart data
    chartData.value = newData
    
    // Update current values and stats
    if (newData.length > 0) {
      // Get the most recent values
      const latestReading = newData[newData.length - 1]
      currentStatus.value = latestReading.status
      currentDeviceId.value = latestReading.deviceId
      currentUser.value = latestReading.user
      
      // Update last updated time in 12-hour format
      const formattedTime = latestReading.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      })
      lastUpdated.value = formattedTime
      
      // Calculate status stats
      const onCount = newData.filter(item => item.status === 'ON').length
      const offCount = newData.filter(item => item.status === 'OFF').length
      
      // Calculate switches (status changes)
      let switches = 0
      for (let i = 1; i < newData.length; i++) {
        if (newData[i].status !== newData[i-1].status) {
          switches++
        }
      }
      
      statusStats.value = {
        onCount,
        offCount,
        switches
      }
    }
    
    // Update the chart
    updateChart()
  }, (error) => {
    console.error("Error in realtime listener:", error)
  })
}

// Initialize chart data from fetched data
const initializeChartData = (data) => {
  // Take the most recent 20 entries for initial chart data
  const initialChartData = data.slice(0, 20)
    .map(item => ({
      timestamp: item.rawTimestamp instanceof Timestamp 
        ? new Date(item.rawTimestamp.toMillis())
        : item.rawTimestamp?.toDate?.() || 
          (item.rawTimestamp?.seconds ? new Date(item.rawTimestamp.seconds * 1000) : new Date()),
      status: item.status,
      deviceId: item.deviceId,
      user: item.user
    }))
    .sort((a, b) => a.timestamp - b.timestamp) // Sort by timestamp ascending for the chart

  // Set chart data
  chartData.value = initialChartData

  // Set initial current values and stats
  if (initialChartData.length > 0) {
    const latestReading = initialChartData[initialChartData.length - 1]
    currentStatus.value = latestReading.status
    currentDeviceId.value = latestReading.deviceId
    currentUser.value = latestReading.user
    
    // Format time in 12-hour format
    const formattedTime = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    lastUpdated.value = formattedTime
    
    // Calculate status stats
    const onCount = initialChartData.filter(item => item.status === 'ON').length
    const offCount = initialChartData.filter(item => item.status === 'OFF').length
    
    // Calculate switches (status changes)
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
      
      // Convert status to numeric values for the chart (1 for ON, 0 for OFF)
      const statusValues = chartData.value.map(item => item.status === 'ON' ? 1 : 0)
      
      // Create new chart with status dataset only
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
          datasets: [
            {
              label: 'Motor Status',
              data: statusValues,
              borderColor: '#a855f7', // purple-500
              backgroundColor: 'rgba(168, 85, 247, 0.15)', // purple-500 with opacity
              borderWidth: 2.5,
              tension: 0.1,
              fill: true,
              pointRadius: 4,
              pointHoverRadius: 6,
              pointBackgroundColor: '#ffffff',
              pointBorderColor: '#a855f7',
              pointBorderWidth: 1.5,
              stepped: true // Use stepped line for status changes
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
              // Add padding to avoid overlap with the current values indicator
              top: 10,
              left: 10,
              right: 10,
              bottom: 10
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
                  size: 11,
                  weight: '600'
                },
                padding: {
                  bottom: 10
                }
              },
              min: -0.1,
              max: 1.1,
              ticks: {
                font: {
                  size: 10
                },
                color: '#a855f7',
                padding: 8,
                callback: function(value) {
                  return value === 0 ? 'OFF' : value === 1 ? 'ON' : '';
                }
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
              display: false, // Hide legend since we only have one dataset
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
                  const value = context.raw === 1 ? 'ON' : 'OFF';
                  return `Status: ${value}`;
                }
              }
            }
          }
        }
      })
    }
  })
}

// Update the chart with new data
const updateChart = () => {
  if (chart.value && chartData.value.length > 0) {
    chart.value.data.labels = chartData.value.map(item => {
      return item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    })
    
    // Convert status to numeric values for the chart (1 for ON, 0 for OFF)
    const statusValues = chartData.value.map(item => item.status === 'ON' ? 1 : 0)
    
    // Update status dataset
    chart.value.data.datasets[0].data = statusValues
    
    chart.value.update()
  }
}

// Initialize filters object
const filters = ref({
  id: { min: '', max: '' }
})

// Special filter for status since it's not a numeric range
const statusFilter = ref('')

// Text filters for deviceId and user
const textFilters = ref({
  deviceId: '',
  user: ''
})

// Reactive state
const searchQuery = ref('')
const itemsPerPage = ref(20) // Default to 20 items per page
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
  { key: 'user', label: 'User' }
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

// Computed properties
const filteredData = computed(() => {
  let result = [...motorData.value]

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(row => {
      return Object.values(row).some(value => 
        String(value).toLowerCase().includes(query)
      )
    })
  }

  // Apply status filter
  if (statusFilter.value) {
    result = result.filter(row => row.status === statusFilter.value)
  }

  // Apply text filters
  Object.keys(activeTextFilters.value).forEach(key => {
    const value = activeTextFilters.value[key]
    if (value) {
      result = result.filter(row => 
        String(row[key]).toLowerCase().includes(value.toLowerCase())
      )
    }
  })

  // Apply range filters
  Object.keys(activeFilters.value).forEach(key => {
    if (key === 'status') return // Skip status as it's handled separately
    
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
    if (aValue === '' || aValue === undefined || aValue === '--') aValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    if (bValue === '' || bValue === undefined || bValue === '--') bValue = sortDirection.value === 'asc' ? -Infinity : Infinity
    
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

  // Handle numeric filters
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

  // Handle text filters
  const newTextFilters = {}
  Object.keys(textFilters.value).forEach(key => {
    if (textFilters.value[key]) {
      newTextFilters[key] = textFilters.value[key]
    }
  })

  activeFilters.value = newFilters
  activeTextFilters.value = newTextFilters
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
    saveAs(blob, 'motor_control_data.csv')
    window.showToast('Motor Control exported as CSV', 'success')
  } else if (format === 'pdf') {
    // PDF Export
    const doc = new jsPDF()
    doc.text('Motor Control Data Table', 14, 16)
    autoTable(doc, {
      head: [exportHeaders],
      body: exportRows,
      startY: 22,
      styles: { fontSize: 10 }
    })
    doc.save('motor_control_data.pdf')
    window.showToast('Motor Control exported as PDF', 'success')
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
          new Paragraph({ text: 'Motor Control Data Table', heading: 'Heading1' }),
          new Table({ rows: tableRows })
        ]
      }]
    })
    const buffer = await Packer.toBlob(docxDoc)
    saveAs(buffer, 'motor_control_data.docx')
  }

  activeDropdown.value = null // Close dropdown after exporting
}

// Watch for changes that should reset pagination
watch([searchQuery, activeFilters, activeTextFilters, statusFilter, itemsPerPage], () => {
  currentPage.value = 1
})

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  // Initial data fetch with loading indicator only on first load
  fetchMotorControlData(true)
  
  // Set up realtime listener
  setupRealtimeListener()
  
  // Set up window resize handler for chart responsiveness
  window.addEventListener('resize', () => {
    if (chart.value) {
      chart.value.resize()
    }
  })
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  
  // Clean up chart
  if (chart.value) {
    chart.value.destroy()
  }
  
  // Clear the refresh interval
  if (refreshInterval) {
    clearInterval(refreshInterval)
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