<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 w-[calc(100vw-1rem)] sm:w-full h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-hidden mx-auto">        <!-- Gradient header for visual appeal -->
      <!-- Gradient header for visual appeal -->
      <div class="bg-gradient-to-r from-emerald-50 to-white p-4 md:p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-sm md:text-xl font-semibold text-gray-800 mb-1">Water Level Data Table</h1>
            <div class="flex items-center text-xs md:text-sm text-gray-500">
              <span class="text-emerald-600 font-medium">Water Level</span>
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
            <h3 class="text-xs md;text-sm font-semibold text-gray-700">Live Water Level</h3>
            <p class="text-[10px] md:text-xs text-gray-500">Real-time monitoring</p>
          </div>
          
          <!-- Enhanced Combined Graph Container -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm overflow-hidden flex flex-col mb-4">
            <!-- Graph Header with improved styling -->
            <div class="p-3 border-b border-gray-100 bg-gray-50 flex justify-between items-center">
              <div class="flex items-center">
                <div class="w-3 h-3 rounded-full bg-blue-500 mr-1.5"></div>
                <span class="text-[10px] md:text-xs font-medium text-gray-700">Level (%)</span>
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
                  <div class="w-1.5 h-1.5 rounded-full bg-blue-500 mr-1"></div>
                  <div class="text-xs font-bold text-blue-600">
                    {{ currentWaterLevelValue }}%
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Enhanced Graph Footer with Stats -->
            <div class="border-t border-gray-100 p-3">
              <!-- Water Level Stats -->
              <div>
                <div class="flex items-center mb-2">
                  <div class="w-3 h-3 rounded-full bg-blue-500 mr-1.5"></div>
                  <div class="text-sm font-medium text-gray-700">Water Level</div>
                </div>
                <div class="grid grid-cols-3 gap-2 bg-blue-50/50 rounded-md p-2">
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Min</div>
                    <div class="text-sm font-semibold text-blue-600">{{ waterLevelStats.min }}%</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Avg</div>
                    <div class="text-sm font-semibold text-blue-600">{{ waterLevelStats.avg }}%</div>
                  </div>
                  <div class="flex flex-col items-center p-1.5 bg-white rounded shadow-sm">
                    <div class="text-xs text-gray-500 mb-1">Max</div>
                    <div class="text-sm font-semibold text-blue-600">{{ waterLevelStats.max }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Water Status Guide -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4 mb-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Water Drum Status Guide</h4>
            <div class="space-y-3">
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-emerald-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Full</span>
                </div>
                <span class="text-xs text-gray-500">80% - 100%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-blue-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Sufficient</span>
                </div>
                <span class="text-xs text-gray-500">40% - 80%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-yellow-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Low</span>
                </div>
                <span class="text-xs text-gray-500">20% - 40%</span>
              </div>
              <div class="flex items-center justify-between">
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 rounded-full bg-red-500 mr-2"></span>
                  <span class="text-xs font-medium text-gray-700">Empty</span>
                </div>
                <span class="text-xs text-gray-500">< 20%</span>
              </div>
            </div>
          </div>
          
          <!-- Water Level Indicators -->
          <div class="bg-white rounded-lg border border-gray-100 shadow-sm p-4">
            <h4 class="text-sm font-semibold text-gray-700 mb-2">Water Drum Capacity</h4>
            <div class="space-y-3">
              <div>
                <div class="flex items-center mb-1">
                  <div class="w-2 h-2 rounded-full bg-blue-500 mr-1"></div>
                  <span class="text-xs font-medium text-gray-700">Current Water Level</span>
                </div>
                <div class="h-4 bg-gray-100 rounded-full overflow-hidden relative">
                  <div class="absolute inset-0 flex">
                    <div class="h-full bg-red-500 w-[20%] flex items-center justify-center">
                      <span class="text-[8px] text-white font-bold">Empty</span>
                    </div>
                    <div class="h-full bg-yellow-500 w-[20%] flex items-center justify-center">
                      <span class="text-[8px] text-white font-bold">Low</span>
                    </div>
                    <div class="h-full bg-blue-500 w-[40%] flex items-center justify-center">
                      <span class="text-[8px] text-white font-bold">Sufficient</span>
                    </div>
                    <div class="h-full bg-emerald-500 w-[20%] flex items-center justify-center">
                      <span class="text-[8px] text-white font-bold">Full</span>
                    </div>
                  </div>
                </div>
                <div class="flex justify-between mt-1 text-[10px] text-gray-500">
                  <span>0%</span>
                  <span>20%</span>
                  <span>40%</span>
                  <span>80%</span>
                  <span>100%</span>
                </div>
              </div>
              <div class="mt-3 text-xs text-gray-600">
                <p class="mb-1"><span class="font-medium">Refill needed:</span> When water level drops below 20%</p>
                <p><span class="font-medium">Optimal usage:</span> Keep water level between 40% - 80%</p>
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
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Water Level</div>
                  <div class="text-xs font-semibold text-blue-600">{{ row.waterLevel }}%</div>
                </div>
                <div>
                  <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Status</div>
                  <span 
                    :class="[
                      'px-2 py-0.5 rounded-full text-[10px] font-medium',
                      row.status === 'FULL' ? 'bg-emerald-100 text-emerald-800' :
                      row.status === 'SUFFICIENT' ? 'bg-blue-100 text-blue-800' :
                      row.status === 'LOW' ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    ]"
                  >
                    {{ row.status }}
                  </span>
                </div>
              </div>
            </div>
            
            <div v-if="paginatedData.length === 0 && !isLoading" 
                class="flex flex-col items-center justify-center py-8">
              <FileSearch class="h-10 w-10 text-gray-300 mb-2" />
              <p class="text-gray-500 text-xs font-medium">No water level data found</p>
              <p class="text-gray-400 text-[10px]">Try adjusting your search or filters</p>
            </div>
          </div>

          <!-- Desktop Table View (shown on medium screens and up) -->
          <div class="hidden sm:flex flex-1 flex-col min-h-0">
            <!-- Single Table Structure for Perfect Alignment -->
            <div class="flex-1 overflow-auto">
              <table class="w-full min-w-[600px] table-fixed">
                <thead class="sticky top-0 z-10 bg-gray-300 border-b border-gray-200">
                <tr>
                  <th class="w-[10%] py-3.5 px-4 text-left text-xs font-medium bg-gray-100 text-gray-800 uppercase tracking-wider">
                    ID
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-emerald-600">Water Status</div>
                    <div class="text-gray-400 text-[10px]">CONDITION</div>
                  </th>
                  <th class="w-[25%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-blue-600">Water Level</div>
                    <div class="text-gray-400 text-[10px]">PERCENTAGE (%)</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-gray-600">Date</div>
                    <div class="text-gray-400 text-[10px]">MMM DD, YYYY</div>
                  </th>
                  <th class="w-[20%] py-3.5 px-4 text-left text-xs bg-gray-100 font-medium uppercase tracking-wider">
                    <div class="text-gray-600">Time</div>
                    <div class="text-gray-400 text-[10px]">HH:MM:SS AM/PM</div>
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
                    <span 
                      :class="[
                        'px-3 py-1 rounded-full text-xs font-medium',
                        row.status === 'FULL' ? 'bg-emerald-100 text-emerald-800' :
                        row.status === 'SUFFICIENT' ? 'bg-blue-100 text-blue-800' :
                        row.status === 'LOW' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      ]"
                    >
                      {{ row.status }}
                    </span>
                  </td>
                  <td class="w-[25%] px-4 py-3.5 whitespace-nowrap">
                    <div class="text-sm font-medium text-blue-600">
                      {{ row.waterLevel }}%
                    </div>
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
                        <p class="text-gray-500 text-lg font-medium">No water level data found</p>
                        <p class="text-gray-400 text-sm mt-1">Try adjusting your search or filters</p>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Pagination Section (similar to your example) -->
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

  <!-- Loading Page Component -->
  <LoadingPage 
    :isVisible="isLoading" 
    title="Loading Water Level Data" 
    message="Please wait while we fetch the latest water level measurements"
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

const waterLevelData = ref([])
const isLoading = ref(true)

const chartCanvas = ref(null)
const chart = ref(null)

const chartData = ref([])

const currentWaterLevelValue = ref('--')
const lastUpdated = ref('--')
const waterLevelStats = ref({
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
  
  const tempWaterLevelRows = sortedData.value.map(row => ({
    id: row.id,
    date: row.date,
    time: row.time,
    waterLevel: row.waterLevel,
    status: row.status
  }));
  
  // FIXED: Use ALL water level data instead of just chartData
  const allWaterLevelData = waterLevelData.value
    .filter(item => item.waterLevel !== undefined && item.waterLevel !== null && item.waterLevel !== '--')
    .map(item => {
      let timestamp;
      try {
        if (item.rawTimestamp && typeof item.rawTimestamp.toDate === 'function') {
          timestamp = item.rawTimestamp.toDate();
        } else if (item.rawTimestamp?.seconds) {
          timestamp = new Date(item.rawTimestamp.seconds * 1000);
        } else {
          // Parse from date and time strings
          const dateTimeStr = `${item.date} ${item.time}`;
          timestamp = new Date(dateTimeStr);
          if (isNaN(timestamp.getTime())) {
            timestamp = new Date(); // Fallback to current date if parsing fails
          }
        }
      } catch (e) {
        console.error("Error parsing timestamp:", e);
        timestamp = new Date();
      }
      
      return {
        timestamp: timestamp,
        value: Number(item.waterLevel)
      };
    })
    .sort((a, b) => a.timestamp - b.timestamp);
  
  console.log(`📊 Print chart will show ALL ${allWaterLevelData.length} records`);
  
  const waterLevelValues = allWaterLevelData.map(item => item.value);
  
  const waterLevelMin = waterLevelValues.length > 0 ? Math.min(...waterLevelValues) : 0;
  const waterLevelMax = waterLevelValues.length > 0 ? Math.max(...waterLevelValues) : 100;
  const waterLevelAvg = waterLevelValues.length > 0 ? 
    (waterLevelValues.reduce((sum, val) => sum + val, 0) / waterLevelValues.length) : 0;
  
  let chartImage = '';
  
  try {
    const ctx = tempCanvas.getContext('2d');
    
    // For very large datasets, adjust the chart display to prevent overcrowding
    const displayLabels = allWaterLevelData.length > 100 ? 
      allWaterLevelData.map((item, index) => index % Math.ceil(allWaterLevelData.length / 20) === 0 ? 
        item.timestamp.toLocaleTimeString('en-US', {
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        }) : '') : 
      allWaterLevelData.map(item => item.timestamp.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      }));
    
    const waterLevelChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: displayLabels,
        datasets: [
          {
            label: 'Water Level (%)',
            data: allWaterLevelData.map(item => item.value),
            borderColor: '#3b82f6', 
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            borderWidth: 3,
            tension: 0.4,
            fill: true,
            pointRadius: allWaterLevelData.length > 100 ? 0 : 3, // Hide points for large datasets
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#3b82f6',
            pointBorderWidth: 2,
            yAxisID: 'y-waterlevel'
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
            enabled: allWaterLevelData.length <= 100 // Disable tooltips for large datasets
          }
        },
        scales: {
          'y-waterlevel': {
            type: 'linear',
            display: true,
            position: 'left',
            title: {
              display: true,
              text: 'Water Level (%)',
              color: '#3b82f6',
              font: {
                size: 14,
                weight: '600'
              }
            },
            beginAtZero: false,
            min: Math.max(0, Math.floor(waterLevelMin * 0.95)),
            max: Math.min(100, Math.ceil(waterLevelMax * 1.05)),
            ticks: {
              font: { size: 12 },
              color: '#3b82f6',
              padding: 8
            },
            grid: {
              color: 'rgba(59, 130, 246, 0.1)'
            }
          },
          x: {
            ticks: {
              font: { size: 10 },
              color: '#64748b',
              maxTicksLimit: 10,
              maxRotation: 45,
              callback: function(value, index) {
                // Only show labels that aren't empty
                return this.getLabelForValue(value) || null;
              }
            }
          }
        }
      }
    });
    
    setTimeout(async () => {
      try {
        chartImage = tempCanvas.toDataURL('image/png', 1.0);
        
        waterLevelChart.destroy();
        document.body.removeChild(tempContainer);
        
        generatePrintHTML(chartImage, tempWaterLevelRows, formattedDate, now, 
                         allWaterLevelData.length, waterLevelMin, waterLevelMax, waterLevelAvg);
      } catch (error) {
        console.error('Error capturing chart:', error);
        document.body.removeChild(tempContainer);
        generatePrintHTML('', tempWaterLevelRows, formattedDate, now, 0, 0, 0, 0);
      }
    }, 500);
    
  } catch (error) {
    console.error('Error creating chart:', error);
    document.body.removeChild(tempContainer);
    generatePrintHTML('', tempWaterLevelRows, formattedDate, now, 0, 0, 0, 0);
  }
};

const generatePrintHTML = (chartImage, tempWaterLevelRows, formattedDate, now, 
                          chartRecordCount, waterLevelMin, waterLevelMax, waterLevelAvg) => {
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Water Level Data Report</title>
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
        .waterlevel { color: #3b82f6; font-weight: 500; }
        .status-full { color: #059669; }
        .status-sufficient { color: #3b82f6; }
        .status-low { color: #d97706; }
        .status-empty { color: #dc2626; }
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
          grid-template-columns: 1fr;
          gap: 15px;
          margin: 20px 0;
          text-align: center;
        }
        .stat-item {
          padding: 15px;
          background-color: #f8fafc;
          border-radius: 8px;
          border: 1px solid #e2e8f0;
          border-left: 4px solid #3b82f6;
        }
        .stat-item h4 {
          margin: 0 0 10px 0;
          font-size: 14px;
          font-weight: 600;
          color: #3b82f6;
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
        <h1>Water Level Data Report</h1>
        <div class="date">${formattedDate}</div>
      </div>
      
      <div class="summary">
        <h3>Report Summary</h3>
        <div class="summary-item">
          <span class="summary-label">Total Records:</span>
          <span class="summary-value">${tempWaterLevelRows.length}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Chart Data Points:</span>
          <span class="summary-value">${chartRecordCount}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Date Range:</span>
          <span class="summary-value">${tempWaterLevelRows.length > 0 ? tempWaterLevelRows[tempWaterLevelRows.length-1].date + ' to ' + tempWaterLevelRows[0].date : 'N/A'}</span>
        </div>
        <div class="summary-item">
          <span class="summary-label">Report Generated:</span>
          <span class="summary-value">${now.toLocaleString()}</span>
        </div>
      </div>
      
      <div class="section-header">Water Level Trend Analysis</div>
      ${chartImage ? `
        <div class="chart-title">Water Level Over Time</div>
        <div class="chart-info">Showing ${chartRecordCount} most recent data points</div>
        <img src="${chartImage}" class="chart-image" alt="Water Level Chart" />
        
        <div class="stats-summary">
          <div class="stat-item">
            <h4>Water Level Statistics</h4>
            <div class="stat-values">
              Min: ${waterLevelMin.toFixed(2)}%<br>
              Avg: ${waterLevelAvg.toFixed(2)}%<br>
              Max: ${waterLevelMax.toFixed(2)}%
            </div>
          </div>
        </div>
      ` : '<p style="text-align: center; color: #6b7280;">Chart could not be generated</p>'}
      
      <div class="section-header">Detailed Water Level Readings</div>
      <table>
        <thead>
          <tr>
            <th style="width: 8%">ID</th>
            <th style="width: 15%">Date</th>
            <th style="width: 12%">Time</th>
            <th style="width: 15%">Water Level</th>
            <th style="width: 15%">Status</th>
          </tr>
        </thead>
        <tbody>
          ${tempWaterLevelRows.map(row => `
            <tr>
              <td>${row.id}</td>
              <td>${row.date}</td>
              <td>${row.time}</td>
              <td><span class="waterlevel">${row.waterLevel}%</span></td>
              <td><span class="status-${row.status.toLowerCase()}">${row.status}</span></td>
            </tr>
          `).join('')}
        </tbody>
      </table>
      
      <div class="footer">
        Generated by Water Level Monitoring System • ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
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

const fetchWaterLevelData = async () => {
  try {
    if (dataCache.value) {
      waterLevelData.value = dataCache.value
      isLoading.value = false
      initializeChartData(dataCache.value)
    } else {
      isLoading.value = true
    }
    
    const response = await api.get('/water-level/readings')
    const waterData = response.data
    
    const processedData = waterData
      .filter(item => item.waterLevel !== undefined)
      .map((item, index) => {
        let formattedDate = '--'
        let formattedTime = '--'
        let timestampSeconds = 0
        
        try {
          const timestamp = item.timestamp ? new Date(item.timestamp) : new Date()
          
          formattedDate = timestamp.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: '2-digit'
          });

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

        const waterLevel = item.waterLevel !== undefined && item.waterLevel !== null 
          ? Number(item.waterLevel).toFixed(2) 
          : '--'
        
        const status = calculateWaterStatus(Number(item.waterLevel))

        return {
          id: index + 1,
          timestamp: timestampSeconds,
          waterLevel: waterLevel,
          status: status,
          date: formattedDate,
          time: formattedTime,
          rawTimestamp: item.timestamp
        }
      })

    dataCache.value = processedData
    
    waterLevelData.value = processedData
    isLoading.value = false
    
    initializeChartData(processedData)
    PRINT_CHART_DATA_LIMIT = processedData.length
  } catch (error) {
    console.error("❌ Error fetching water level data:", error)
    isLoading.value = false
    
    if (dataCache.value) {
      waterLevelData.value = dataCache.value
      initializeChartData(dataCache.value)
    }
  }
}

const setupRealtimeListener = () => {
  // For MongoDB, we'll use polling instead of realtime listener
  // You can implement WebSocket or Server-Sent Events for true realtime
  const pollInterval = setInterval(async () => {
    try {
      const response = await api.get('/water-level/latest')
      const newData = response.data
      
      if (newData && newData.length > 0) {
        processNewData(newData)
      }
    } catch (error) {
      console.error("Error polling for new data:", error)
    }
  }, 5000) // Poll every 5 seconds

  return () => clearInterval(pollInterval)
}

const processNewData = (newDataArray) => {
  const newData = []
  
  newDataArray.forEach(item => {
    try {
      if (item.waterLevel === undefined || item.waterLevel === null) return
      
      let timestamp
      if (item.timestamp) {
        timestamp = new Date(item.timestamp)
      } else {
        timestamp = new Date()
      }
      
      const value = parseFloat(item.waterLevel)
      if (!isNaN(value)) {
        newData.push({
          timestamp,
          value: value
        })
      }
    } catch (e) {
      console.error("Error processing item:", e)
    }
  })
  
  newData.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime())
  
  // Update chart data with new readings
  chartData.value = [...chartData.value, ...newData].slice(-100) // Keep last 100 readings
  
  if (newData.length > 0) {
    const latestReading = newData[newData.length - 1]
    currentWaterLevelValue.value = latestReading.value.toFixed(2)
    
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    
    const values = chartData.value.map(item => item.value).filter(val => !isNaN(val))
    if (values.length > 0) {
      waterLevelStats.value = {
        min: Math.min(...values).toFixed(2),
        max: Math.max(...values).toFixed(2),
        avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2)
      }
    }
  }
  
  requestAnimationFrame(() => {
    updateChart()
  })
}

const initializeChartData = (data) => {
  const initialChartData = []
  
  data.slice(0, 20).forEach(item => {
    try {
      let timestamp
      if (item.rawTimestamp && typeof item.rawTimestamp.toDate === 'function') {
        timestamp = item.rawTimestamp.toDate()
      } else if (item.rawTimestamp?.seconds) {
        timestamp = new Date(item.rawTimestamp.seconds * 1000)
      } else {
        timestamp = new Date()
      }
      
      const value = parseFloat(item.waterLevel)
      if (!isNaN(value)) {
        initialChartData.push({
          timestamp,
          value: value
        })
      }
    } catch (e) {
      console.error("Error processing item:", e)
    }
  })
  
  initialChartData.sort((a, b) => a.timestamp.getTime() - b.timestamp.getTime())
  
  chartData.value = initialChartData
  
  if (initialChartData.length > 0) {
    const latestReading = initialChartData[initialChartData.length - 1]
    currentWaterLevelValue.value = latestReading.value.toFixed(2)
    
    lastUpdated.value = latestReading.timestamp.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    })
    
    const values = initialChartData.map(item => item.value).filter(val => !isNaN(val))
    if (values.length > 0) {
      waterLevelStats.value = {
        min: Math.min(...values).toFixed(2),
        max: Math.max(...values).toFixed(2),
        avg: (values.reduce((sum, val) => sum + val, 0) / values.length).toFixed(2)
      }
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
            label: 'Water Level (%)',
            data: chartData.value.map(item => item.value),
            borderColor: '#3b82f6', 
            backgroundColor: 'rgba(59, 130, 246, 0.15)',
            borderWidth: 2.5,
            tension: 0.4,
            fill: true,
            pointRadius: 3,
            pointHoverRadius: 5,
            pointBackgroundColor: '#ffffff',
            pointBorderColor: '#3b82f6',
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
              min: Math.max(0, Math.floor(waterLevelStats.value.min * 0.95)),
              max: Math.min(100, Math.ceil(waterLevelStats.value.max * 1.05)),
              title: {
                display: true,
                text: 'Level (%)',
                color: '#3b82f6',
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
                  return `Level: ${context.raw.toFixed(2)}%`;
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
    
    chart.value.options.scales.y.min = Math.max(0, Math.floor(waterLevelStats.value.min * 0.95))
    chart.value.options.scales.y.max = Math.min(100, Math.ceil(waterLevelStats.value.max * 1.05))
    
    chart.value.update('none') 
  }
}

const calculateWaterStatus = (level) => {
  if (level >= 80) return 'FULL'
  if (level >= 40) return 'SUFFICIENT'
  if (level >= 20) return 'LOW'
  return 'EMPTY'
}

const filters = ref({
  waterLevel: { min: '', max: '' }
})

const searchQuery = ref('')
const itemsPerPage = ref(20)
const currentPage = ref(1)
const activeDropdown = ref(null)
const sortKey = ref('id')
const sortDirection = ref('asc')
const activeFilters = ref({})

const filterFields = [
  { key: 'waterLevel', label: 'Water Level (%)' }
]

const headers = [
  { key: 'id', label: 'ID' },
  { key: 'status', label: 'Water Status' },
  { key: 'waterLevel', label: 'Water Level (%)' },
  { key: 'date', label: 'Date' },
  { key: 'time', label: 'Time' }
]

const exportFormats = ['csv', 'pdf']

const filteredData = computed(() => {
  let result = [...waterLevelData.value]

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
      pages.push(2, '...', total)
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

const getChartImage = async () => {
  if (!chartCanvas.value) return null;
  
  return new Promise((resolve) => {
    const imageData = chartCanvas.value.toDataURL('image/png', 1.0);
    resolve(imageData);
  });
};

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
    saveAs(blob, 'water_level_data.csv')
    window.showToast('Water Level exported as CSV', 'success')
  } else if (format === 'pdf') {
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm'
    });
    
    doc.setFontSize(16);
    doc.text('Water Level Data Report', 105, 15, { align: 'center' });
    
    doc.setFontSize(10);
    const dateStr = new Date().toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
    doc.text(`Generated on: ${dateStr}`, 105, 22, { align: 'center' });
    
    doc.setFontSize(12);
    doc.text('Current Reading:', 15, 30);
    doc.text(`Water Level: ${currentWaterLevelValue.value}%`, 15, 36);
    doc.text(`Status: ${calculateWaterStatus(Number(currentWaterLevelValue.value))}`, 15, 42);
    
    if (chartCanvas.value) {
      const canvas = chartCanvas.value;
      const chartImage = canvas.toDataURL('image/png');
      
      const imgWidth = 180; 
      const imgHeight = (canvas.height * imgWidth) / canvas.width;
      doc.addImage(chartImage, 'PNG', (210 - imgWidth) / 2, 50, imgWidth, imgHeight);
      
      doc.setFontSize(10);
      doc.text('Water Level Statistics:', 15, 50 + imgHeight + 10);
      doc.text(`Minimum: ${waterLevelStats.value.min}%`, 15, 50 + imgHeight + 16);
      doc.text(`Average: ${waterLevelStats.value.avg}%`, 15, 50 + imgHeight + 22);
      doc.text(`Maximum: ${waterLevelStats.value.max}%`, 15, 50 + imgHeight + 28);
      
      doc.text('Status Guide:', 15, 50 + imgHeight + 38);
      doc.text(`Full: 80% - 100%`, 15, 50 + imgHeight + 44);
      doc.text(`Sufficient: 40% - 80%`, 15, 50 + imgHeight + 50);
      doc.text(`Low: 20% - 40%`, 15, 50 + imgHeight + 56);
      doc.text(`Empty: < 20%`, 15, 50 + imgHeight + 62);
      
      doc.addPage();
      doc.setFontSize(14);
      doc.text('Water Level Data Table', 105, 15, { align: 'center' });
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
        margin: { top: 20 },
        columnStyles: {
          0: { cellWidth: 15 }, 
          1: { cellWidth: 25 }, 
          2: { cellWidth: 25 }, 
          3: { cellWidth: 20 }, 
          4: { cellWidth: 20 } 
        }
      });
    } else {
      doc.text('Water Level Chart Not Available', 105, 50, { align: 'center' });
      autoTable(doc, {
        head: [exportHeaders],
        body: exportRows,
        startY: 60,
        styles: { fontSize: 10 }
      });
    }
    
    doc.save('water_level_report.pdf');
    window.showToast('Water Level report exported as PDF', 'success');
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
          new Paragraph({ text: 'Water Level Data Table', heading: 'Heading1' }),
          new Table({ rows: tableRows })
        ]
      }]
    })
    const buffer = await Packer.toBlob(docxDoc)
    saveAs(buffer, 'water_level_data.docx')
  }

  activeDropdown.value = null 
}

watch([searchQuery, activeFilters, itemsPerPage], () => {
  currentPage.value = 1
})

let unsubscribe = null

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  
  fetchWaterLevelData()
  
  unsubscribe = setupRealtimeListener()
  
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