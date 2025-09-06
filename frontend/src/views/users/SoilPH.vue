<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">
      
      <!-- Gradient header for visual appeal - CHANGED TO EMERALD (GREEN) -->
      <div class="bg-gradient-to-r from-emerald-50 to-white p-4 md:p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-sm md:text-xl font-semibold text-gray-800 mb-1">Soil pH Data Table</h1>
            <div class="flex items-center text-xs md:text-sm text-gray-500">
              <span class="text-emerald-600 font-medium">Soil pH</span>
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

      <!-- FIXED: Table and Graph Section - Always maintain consistent layout -->
      <div class="flex-1 overflow-y-auto md:overflow-hidden flex flex-col md:flex-row min-h-0">
        
        <!-- FIXED: Live Graph Container - Fixed width that doesn't expand -->
        <div class="w-full md:w-1/3 lg:w-1/3 md:min-w-[300px] md:max-w-[400px] border-r border-gray-200 bg-white p-4 overflow-y-auto flex-shrink-0">
          <div class="mb-3">
            <h3 class="text-xs md:text-sm font-semibold text-gray-700">Live Soil pH</h3>
            <p class="text-[10px] md:text-xs text-gray-500">Real-time monitoring</p>
          </div>
          
          <!-- Enhanced Combined Graph Container -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
            <!-- Graph Header with improved styling -->
            <div class="p-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full bg-orange-500 mr-1.5"></div>
                <span class="text-[10px] md:text-xs font-medium text-gray-700">pH Level</span>
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
                  <div class="w-1.5 h-1.5 rounded-full bg-orange-500 mr-1"></div>
                  <div class="text-xs font-bold text-orange-600">
                    {{ currentPhValue }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Enhanced Graph Footer with Stats -->
            <div class="border-t border-gray-100 p-3">
              <!-- pH Stats -->
              <div>
                <div class="flex items-center mb-2">
                  <div class="w-3 h-3 rounded-full bg-orange-500 mr-1.5"></div>
                  <div class="text-sm font-medium text-gray-700">Soil pH</div>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-orange-50/50 rounded-md p-2">
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Min</div>
                    <div class="text-sm font-semibold text-orange-600">{{ phStats.min }}</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Avg</div>
                    <div class="text-sm font-semibold text-orange-600">{{ phStats.avg }}</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Max</div>
                    <div class="text-sm font-semibold text-orange-600">{{ phStats.max }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Soil pH Status Information -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">pH Status Guide</h4>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-red-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Acidic</span>
                </div>
                <span class="text-xs text-gray-500">< 3.5 - 6.5</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-green-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Neutral</span>
                </div>
                <span class="text-xs text-gray-500">6.6 - 7.3</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Alkaline</span>
                </div>
                <span class="text-xs text-gray-500">7.4 - >9.0</span>
              </div>
            </div>
          </div>
          
          <!-- Optimal Ranges section -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Optimal Ranges</h4>
            <div class="space-y-3">
              <div>
                <div class="flex items-center mb-1">
                  <div class="w-2 h-2 rounded-full bg-orange-500 mr-1"></div>
                  <span class="text-xs font-medium text-gray-700">Soil pH</span>
                </div>
                <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
                  <div class="h-full rounded-full" style="width: 100%; background: linear-gradient(to right, #dc2626 0%, #ea580c 16.67%, #eab308 33.33%, #16a34a 50%, #2563eb 66.67%, #9333ea 83.33%, #7c3aed 100%);"></div>
                </div>
                <div class="flex justify-between mt-1 text-[10px] text-gray-500">
                  <span>3.5</span>
                  <span>6.5</span>
                  <span>7.3</span>
                  <span>9.0</span>
                </div>
                <div class="flex justify-between mt-1 text-[9px] text-gray-400">
                  <span>Acidic</span>
                  <span>Neutral</span>
                  <span>Alkaline</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- FIXED: Table Container - Takes remaining space with consistent width -->
        <div class="w-full md:w-2/3 lg:w-2/3 flex flex-col min-w-0 flex-grow">
          
          <!-- Mobile Card View (shown on small screens) -->
          <div class="sm:hidden flex-1 overflow-auto bg-white p-3 space-y-3">
            <!-- Show loading state or empty state consistently -->
            <div v-if="isLoading" class="flex flex-col items-center justify-center py-12">
              <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-emerald-500 mb-2"></div>
              <p class="text-gray-500 text-xs">Loading soil pH data...</p>
            </div>
            
            <div v-else-if="paginatedData.length === 0" class="flex flex-col items-center justify-center py-8">
              <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
              <p class="text-gray-500 text-xs font-medium">No soil pH data found</p>
              <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
            </div>
            
            <div v-else>
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
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Soil pH</div>
                    <div class="text-xs font-semibold text-orange-600">{{ row.soilPh }}</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">pH Status</div>
                    <span 
                      :class="[
                        'px-2 py-0.5 rounded-full text-[10px] font-medium',
                        row.phStatus === 'NEUTRAL' ? 'bg-green-100 text-green-800' :
                        row.phStatus === 'ACIDIC' ? 'bg-red-100 text-red-800' :
                        'bg-blue-100 text-blue-800'
                      ]"
                    >
                      {{ row.phStatus }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Desktop Table View (shown on medium screens and up) -->
          <div class="hidden sm:flex flex-1 flex-col min-h-0">
            
            <!-- FIXED: Always show table structure even when loading -->
            <div class="flex-1 overflow-y-auto">
              <table class="w-full min-w-full">
                <thead>
                  <tr>
                    <th class="w-[10%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium text-gray-500 uppercase tracking-wider border-b">
                      ID
                    </th>
                    <th class="w-[20%] md:w-[25%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-orange-600">Soil pH</div>
                      <div class="text-gray-400 text-[10px]">pH LEVEL</div>
                    </th>
                    <th class="w-[20%] md:w-[25%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-orange-600">pH Status</div>
                      <div class="text-gray-400 text-[10px]">CONDITION</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-gray-600">Date</div>
                      <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                    </th>
                    <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider border-b">
                      <div class="text-gray-600">Time</div>
                      <div class="text-gray-400 text-[10px]">HH:MM:SS</div>
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <!-- Loading state row -->
                  <tr v-if="isLoading">
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mb-4"></div>
                        <p class="text-gray-500 text-lg font-medium">Loading soil pH data...</p>
                        <p class="text-gray-400 text-sm mt-1">Please wait while we fetch your data</p>
                      </div>
                    </td>
                  </tr>
                  
                  <!-- Data rows -->
                  <tr v-else-if="paginatedData.length > 0"
                      v-for="(row, index) in paginatedData" 
                      :key="index"
                      class="border-b border-gray-50 last:border-0">
                    <td class="w-[10%] px-4 py-3.5 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-700">{{ row.id }}</div>
                    </td>
                    <td class="w-[25%] px-4 py-3.5 whitespace-nowrap">
                      <div class="text-sm font-medium text-orange-600">{{ row.soilPh }}</div>
                    </td>
                    <td class="w-[25%] px-4 py-3.5 whitespace-nowrap">
                      <span 
                        :class="[
                          'px-3 py-1 rounded-full text-xs font-medium',
                          row.phStatus === 'NEUTRAL' ? 'bg-green-100 text-green-800' :
                          row.phStatus === 'ACIDIC' ? 'bg-red-100 text-red-800' :
                          'bg-blue-100 text-blue-800'
                        ]"
                      >
                        {{ row.phStatus }}
                      </span>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-700">{{ row.date }}</div>
                    </td>
                    <td class="w-[20%] px-4 py-3.5 whitespace-nowrap">
                      <div class="text-sm font-medium text-gray-700">{{ row.time }}</div>
                    </td>
                  </tr>
                  
                  <!-- Empty state row -->
                  <tr v-else>
                    <td colspan="5" class="px-6 py-16 text-center">
                      <div class="flex flex-col items-center justify-center">
                        <FileSearch class="h-16 w-16 text-gray-300 mb-4" />
                        <p class="text-gray-500 text-lg font-medium">No soil pH data found</p>
                        <p class="text-gray-400 text-sm mt-1">Try adjusting your search or filters</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- Mobile Pagination -->
        <div class="border-t border-gray-200 py-2 px-3 bg-gray-50 sm:hidden" v-if="!isLoading && paginatedData.length > 0">
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

  <!-- Loading Page Component -->
  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Soil pH Data" 
    message="Please wait while we fetch the latest soil pH measurements"
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
import api from '../../api/index'
import Chart from 'chart.js/auto'

const soilPhData = ref([])
const isLoading = ref(true)
const chartCanvas = ref(null)
const chart = ref(null)
const chartData = ref([])
const currentPhValue = ref('--')
const lastUpdated = ref('--')
const phStats = ref({
  min: '--',
  max: '--',
  avg: '--'
})
const dataCache = ref(null)
const combinedRealtimeData = ref([]) 

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
  
  const soilPhRows = sortedData.value.map(row => ({
    id: row.id,
    date: row.date,
    time: row.time,
    device: row.deviceId || 'N/A',
    soilPh: row.soilPh,
    phStatus: row.phStatus
  }));
  
  const printChartData = soilPhData.value
    .slice(0, PRINT_CHART_DATA_LIMIT)
    .filter(item => item.soilPh !== '--')
    .map(item => ({
      timestamp: item.rawTimestamp, 
      value: Number(item.soilPh)
    }))
    .sort((a, b) => a.timestamp - b.timestamp);
  
  // Calculate min and max values for x-axis labels
  const values = printChartData.map(item => item.value);
  const minValue = Math.min(...values);
  const maxValue = Math.max(...values);
  
  let chartImage = '';
  
  try {
    const ctx = tempCanvas.getContext('2d');
    
    const tempChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: printChartData.map(item => {
          return item.timestamp.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
          })
        }),
        datasets: [{
          label: 'Soil pH',
          data: printChartData.map(item => item.value), 
          borderColor: '#f97316', 
          backgroundColor: 'rgba(249, 115, 22, 0.15)', 
          borderWidth: 3,
          tension: 0.4,
          fill: true,
          pointRadius: 3, 
          pointHoverRadius: 5,
          pointBackgroundColor: '#ffffff',
          pointBorderColor: '#f97316',
          pointBorderWidth: 2
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
                return `pH: ${context.raw.toFixed(1)}`;
              }
            }
          }
        },
        scales: {
          y: {
            beginAtZero: false,
            min: Math.max(0, Math.floor(minValue * 0.95)),
            max: Math.min(14, Math.ceil(maxValue * 1.05)),
            title: {
              display: true,
              text: 'pH Level',
              color: '#f97316',
              font: {
                size: 14,
                weight: '600'
              }
            },
            ticks: {
              font: { size: 12 },
              color: '#64748b',
              callback: function(value) {
                // Show min and max values on y-axis
                if (value === minValue || value === maxValue) {
                  return value.toFixed(1);
                }
                return value;
              }
            },
            grid: {
              color: 'rgba(100, 116, 139, 0.2)'
            }
          },
          x: {
            ticks: {
              font: { size: 10 },
              color: '#64748b',
              maxTicksLimit: 8,
              maxRotation: 45,
              callback: function(value, index, values) {
                // Show first, last, min, and max labels
                if (index === 0 || index === values.length - 1) {
                  return this.getLabelForValue(value);
                }
                
                // Find indices of min and max values
                const data = this.chart.data.datasets[0].data;
                const minIndex = data.indexOf(minValue);
                const maxIndex = data.indexOf(maxValue);
                
                if (index === minIndex || index === maxIndex) {
                  return this.getLabelForValue(value);
                }
                
                // Show fewer labels for better readability
                if (values.length > 10 && index % Math.floor(values.length / 4) !== 0) {
                  return '';
                }
                
                return this.getLabelForValue(value);
              }
            },
            title: {
              display: true,
              text: `Time (Min: ${minValue.toFixed(1)}, Max: ${maxValue.toFixed(1)})`,
              color: '#64748b',
              font: {
                size: 12,
                weight: '600'
              }
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
        
        generatePrintHTML(chartImage, soilPhRows, formattedDate, now, printChartData.length, minValue, maxValue);
      } catch (error) {
        console.error('Error capturing chart:', error);
        document.body.removeChild(tempContainer);
        generatePrintHTML('', soilPhRows, formattedDate, now, 0, minValue, maxValue);
      }
    }, 500);
    
  } catch (error) {
    console.error('Error creating chart:', error);
    document.body.removeChild(tempContainer);
    generatePrintHTML('', soilPhRows, formattedDate, now, 0, minValue, maxValue);
  }
};

const generatePrintHTML = (chartImage, soilPhRows, formattedDate, now, chartRecordCount, minValue, maxValue) => {
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Soil pH Analysis Data</title>
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
        .chart-range {
          text-align: center;
          margin-bottom: 15px;
          font-size: 12px;
          color: #f97316;
          font-weight: 600;
          background-color: #fffbeb;
          padding: 8px;
          border-radius: 6px;
          border: 1px solid #fef3c7;
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
        .soil-ph { color: #f97316; font-weight: 500; }
        .status-neutral { color: #059669; }
        .status-acidic { color: #dc2626; }
        .status-alkaline { color: #2563eb; }
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
          color: #f97316;
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
        <h1>Soil pH Analysis Report</h1>
        <div class="date">${formattedDate}</div>
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-item">
          <span class="summary-label">Total Records:</span>
          <span class="summary-value">${soilPhRows.length}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Chart Data Points:</span>
          <span class="summary-value">${chartRecordCount}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">pH Range:</span>
          <span class="summary-value">${minValue.toFixed(1)} - ${maxValue.toFixed(1)}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Date Range:</span>
          <span class="summary-value">${soilPhRows.length > 0 ? soilPhRows[soilPhRows.length-1].date + ' to ' + soilPhRows[0].date : 'N/A'}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Report Generated:</span>
          <span class="summary-value">${now.toLocaleString()}</span>
        </div>
      </div>
      
      <div class="section-header">Soil pH Trend Analysis</div>
      ${chartImage ? `
        <div class="chart-title">Soil pH Levels Over Time</div>
        <div class="chart-info">Showing ${chartRecordCount} most recent data points</div>
        <div class="chart-range">pH Range: ${minValue.toFixed(1)} (Min) - ${maxValue.toFixed(1)} (Max)</div>
        <img src="${chartImage}" class="chart-image" alt="Soil pH Chart" />
        
        <div class="stats-summary">
          <div class="stat-item">
            <h4>Soil pH Statistics</h4>
            <div class="stat-values">
              Current: ${currentPhValue.value}<br>
              Min: ${minValue.toFixed(1)} | Avg: ${phStats.value.avg} | Max: ${maxValue.toFixed(1)}
            </div>
          </div>
          <div class="stat-item">
            <h4>Data Points</h4>
            <div class="stat-values">
              Total: ${chartRecordCount}<br>
              Time Range: ${soilPhRows.length > 0 ? soilPhRows[soilPhRows.length-1].date + ' to ' + soilPhRows[0].date : 'N/A'}
            </div>
          </div>
          <div class="stat-item">
            <h4>pH Status</h4>
            <div class="stat-values">
              ${minValue < 6.6 ? 'Acidic' : minValue <= 7.3 ? 'Neutral' : 'Alkaline'} Range<br>
              Optimal: 6.6 - 7.3
            </div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">Chart could not be generated</p>'}
      
      <div class="section-header">Detailed Soil pH Sensor Readings</div>
      <table>
        <thead>
          <tr>
            <th style="width: 10%">ID</th>
            <th style="width: 15%">Date</th>
            <th style="width: 12%">Time</th>
            <th style="width: 10%">Device</th>
            <th style="width: 15%">Soil pH</th>
            <th style="width: 15%">pH Status</th>
          </tr>
        </thead>
        <tbody>
          ${soilPhRows.map(row => `
            <tr>
              <td>${row.id}</td>
              <td>${row.date}</td>
              <td>${row.time}</td>
              <td>${row.device}</td>
              <td><span class="soil-ph">${row.soilPh}</span></td>
              <td>
                <span class="${
                  row.phStatus === 'NEUTRAL' ? 'status-neutral' :
                  row.phStatus === 'ACIDIC' ? 'status-acidic' : 'status-alkaline'
                }">${row.phStatus}</span>
              </td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by Soil pH Analysis System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
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

const fetchSoilPhData = async () => {
  try {
    isLoading.value = true;
    
    console.log('Fetching data from:', `/soil-ph/readings`);
    
    const response = await api.get(`/soil-ph/readings`);
    
    console.log('API Response:', response);
    
    const data = response.data;
    
    console.log('API Data:', data);
    
    const processedData = Array.isArray(data) ? data.map((reading, index) => {
      try {
        let timestamp;
        if (reading.timestamp instanceof Date) {
          timestamp = reading.timestamp;
        } else if (typeof reading.timestamp === 'number') {
          timestamp = new Date(reading.timestamp * 1000);
        } else if (reading.timestamp && reading.timestamp._seconds) {
          timestamp = new Date(reading.timestamp._seconds * 1000);
        } else {
          timestamp = new Date();
        }
        
        const formattedDate = timestamp.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'short',
          day: '2-digit'
        });

        const formattedTime = timestamp.toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit',
          hour12: true
        });

        const soilPhValue = reading.soilPh !== undefined ? Number(reading.soilPh) : 
                           reading.ph !== undefined ? Number(reading.ph) : null;

        const soilPh = soilPhValue !== null ? soilPhValue.toFixed(1) : '--';
        const phStatus = calculatePhStatus(soilPhValue);

        return {
          id: `${index}`,
          timestamp: timestamp.getTime() / 1000,
          soilPh: soilPh,
          phStatus: phStatus,
          date: formattedDate,
          time: formattedTime,
          rawTimestamp: timestamp,
          deviceId: reading.deviceId || reading.device_id || 'esp32-1'
        };
      } catch (error) {
        console.error('Error processing reading:', reading, error);
        return null;
      }
    }).filter(reading => reading !== null) : [];

    dataCache.value = processedData;
    soilPhData.value = processedData;
    isLoading.value = false;
    
    initializeChartData(processedData);
    PRINT_CHART_DATA_LIMIT = processedData.value
    
    console.log(`✅ Processed ${processedData.length} readings`);
    
  } catch (error) {
    console.error("❌ Error in fetchSoilPhData:", error);
    isLoading.value = false;
    
    if (dataCache.value) {
      soilPhData.value = dataCache.value;
      initializeChartData(dataCache.value);
    }
  }
};


const setupRealtimeListener = () => {
  const pollingInterval = setInterval(async () => {
    try {
      const response = await api.get(`/soil-ph/readings/realtime`);
      const data = response.data; 
      console.log('Realtime data:', data);
      
      if (!Array.isArray(data)) {
        console.error('Realtime data is not an array:', data);
        return;
      }
      
      processRealtimeData(data);
    } catch (error) {
      console.error('Polling error:', error);
    }
  }, 5000); 
  
  return () => {
    clearInterval(pollingInterval);
  };
};

const processRealtimeData = (data) => {
  if (!Array.isArray(data)) {
    console.error('Realtime data is not an array:', data);
    return;
  }
  
  const newData = data
    .filter(item => item && item.soilPh !== undefined && item.soilPh !== null && item.soilPh !== '--')
    .map(item => {
      try {
        const timestamp = item.timestamp ? new Date(item.timestamp * 1000) : new Date();
        
        return {
          timestamp,
          value: Number(item.soilPh),
          deviceId: item.deviceId || 'esp32-1'
        };
      } catch (error) {
        console.error('Error processing realtime item:', item, error);
        return null;
      }
    })
    .filter(item => item !== null); 
  
  combinedRealtimeData.value = [...newData];
  
  combinedRealtimeData.value.sort((a, b) => a.timestamp - b.timestamp);
  combinedRealtimeData.value = combinedRealtimeData.value.slice(-20);
  
  chartData.value = combinedRealtimeData.value;
  
  if (combinedRealtimeData.value.length > 0) {
    const latestReading = combinedRealtimeData.value[combinedRealtimeData.value.length - 1];
    currentPhValue.value = latestReading.value.toFixed(1);
    
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    });
    
    const values = combinedRealtimeData.value.map(item => item.value);
    phStats.value = {
      min: Math.min(...values).toFixed(1),
      max: Math.max(...values).toFixed(1),
      avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(1)
    };
  }
  
  requestAnimationFrame(() => {
    updateChart();
  });
};

const fetchStats = async () => {
  try {
    const response = await api.get(`/soil-ph/stats?hours=24`);
    
    if (!response.ok) {
      console.error('Stats fetch failed:', response.status, response.statusText);
      return;
    }
    
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      console.error('Expected JSON but got:', contentType);
      return;
    }
    
    const stats = await response.json();
    console.log('Stats data:', stats); 
    
    phStats.value = {
      min: typeof stats.min === 'number' ? stats.min.toFixed(1) : '--',
      max: typeof stats.max === 'number' ? stats.max.toFixed(1) : '--',
      avg: typeof stats.avg === 'number' ? stats.avg.toFixed(1) : '--'
    };
  } catch (error) {
    console.error('Error fetching stats:', error);
  }
};

const updateRealtimeData = (snapshot, deviceId) => {
  const newData = snapshot.docs
    .filter(doc => doc.data().soilPh !== undefined)
    .map(doc => {
      const data = doc.data()
      const timestamp = data.timestamp instanceof Timestamp 
        ? data.timestamp.toDate() 
        : new Date(data.timestamp.seconds * 1000)
      
      return {
        timestamp,
        value: Number(data.soilPh),
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
    currentPhValue.value = latestReading.value.toFixed(1)
    
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    
    const values = combinedRealtimeData.map(item => item.value)
    phStats.value = {
      min: Math.min(...values).toFixed(1),
      max: Math.max(...values).toFixed(1),
      avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(1)
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
      value: Number(item.soilPh),
      deviceId: item.deviceId || 'esp32-1'
    }))
    .sort((a, b) => a.timestamp - b.timestamp); 
  
  chartData.value = initialChartData;
  combinedRealtimeData.value = initialChartData; 
  
  if (initialChartData.length > 0) {
    const latestReading = initialChartData[initialChartData.length - 1];
    currentPhValue.value = latestReading.value.toFixed(1);
    
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    });
    
    const values = initialChartData.map(item => item.value);
    phStats.value = {
      min: Math.min(...values).toFixed(1),
      max: Math.max(...values).toFixed(1),
      avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(1)
    };
  }
  
  initializeChart();
};

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
            label: 'Soil pH',
            data: chartData.value.map(item => item.value),
            borderColor: '#f97316',
            backgroundColor: 'rgba(249, 115, 22, 0.15)',
            borderWidth: 2.5,
            tension: 0.4,
            fill: true,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#f97316',
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
              min: Math.max(0, Math.floor(phStats.value.min * 0.95)),
              max: Math.min(14, Math.ceil(phStats.value.max * 1.05)),
              title: {
                display: true,
                text: 'pH Level',
                color: '#f97316',
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
                  return `pH: ${context.raw.toFixed(1)}`;
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
    
    chart.value.options.scales.y.min = Math.max(0, Math.floor(phStats.value.min * 0.95))
    chart.value.options.scales.y.max = Math.min(14, Math.ceil(phStats.value.max * 1.05))
    
    chart.value.update('none') 
  }
}

const calculatePhStatus = (ph) => {
  if (ph < 6.6) return 'ACIDIC'
  if (ph >= 6.6 && ph <= 7.3) return 'NEUTRAL'
  return 'ALKALINE'
}

const filters = ref({
  soilPh: { min: '', max: '' }
})

const searchQuery = ref('')
const itemsPerPage = ref(20) 
const currentPage = ref(1)
const activeDropdown = ref(null)
const sortKey = ref('date')
const sortDirection = ref('asc')
const activeFilters = ref({})

const filterFields = [
  { key: 'soilPh', label: 'Soil pH Level' }
]

const headers = [
  { key: 'id', label: 'ID' },
  { key: 'soilPh', label: 'Soil pH' },
  { key: 'phStatus', label: 'pH Status' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const exportFormats = ['csv', 'pdf']

const filteredData = computed(() => {
  let result = [...soilPhData.value]

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
    saveAs(blob, 'soil_ph_data.csv')
    window.showToast('Soil PH exported as CSV', 'success')
  } else if (format === 'pdf') {
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm'
    })
    
    doc.setFontSize(16)
    doc.text('Soil pH Data Report', 105, 15, { align: 'center' })
    
    doc.setFontSize(10)
    doc.text(`Generated: ${new Date().toLocaleDateString()}`, 105, 22, { align: 'center' })
    
    if (chartCanvas.value) {
      try {
        const chartImage = chartCanvas.value.toDataURL('image/png', 1.0)
        
        const imgWidth = 160 
        const imgHeight = 90 
        doc.addImage(chartImage, 'PNG', (210 - imgWidth) / 2, 30, imgWidth, imgHeight)
        
        doc.setFontSize(12)
        doc.text('Soil pH Trend', 105, 125, { align: 'center' })
        
        doc.setFontSize(10)
        doc.text(
          `Current: ${currentPhValue.value} | Min: ${phStats.value.min} | Avg: ${phStats.value.avg} | Max: ${phStats.value.max}`,
          105,
          130,
          { align: 'center' }
        )
      } catch (error) {
        console.error('Error adding chart to PDF:', error)
      }
    }
    
    autoTable(doc, {
      head: [exportHeaders],
      body: exportRows,
      startY: 135,
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
      columnStyles: {
        0: { cellWidth: 'auto' },
        1: { cellWidth: 'auto' },
        2: { cellWidth: 'auto' },
        3: { cellWidth: 'auto' },
        4: { cellWidth: 'auto' }
      }
    })
    
    doc.save('soil_ph_report.pdf')
    window.showToast('Soil pH report exported as PDF', 'success')
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
          new Paragraph({ text: 'Soil pH Data Table', heading: 'Heading1' }),
          new Table({ rows: tableRows })
        ]
      }]
    })
    const buffer = await Packer.toBlob(docxDoc)
    saveAs(buffer, 'soil_ph_data.docx')
  }

  activeDropdown.value = null 
}

watch([searchQuery, activeFilters, itemsPerPage], () => {
  currentPage.value = 1
})

let cleanupRealtime = null

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  fetchSoilPhData()
  cleanupRealtime = setupRealtimeListener()
  
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
  
  if (cleanupRealtime) {
    cleanupRealtime()
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