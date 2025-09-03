<template>
  <div class="flex-1 w-full px-2 sm:px-6 md:px:8 lg:px-10 overflow-hidden">
    <!-- Enhanced main container with more appealing design -->
    <div class="bg-white rounded-lg shadow-lg border border-gray-100 h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] flex flex-col overflow-auto overflow-x-hidden">
      <!-- Gradient header for visual appeal -->
      <div class="bg-gradient-to-r from-emerald-50 to-white p-4 md:p-6 border-b border-gray-100 rounded-t-lg">
        <!-- Header with controls aligned side by side -->
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <!-- Title and breadcrumb with enhanced styling -->
          <div>
            <h1 class="text-lg md:text-xl font-semibold text-gray-800 mb-1">Device Control</h1>
            <div class="flex items-center text-[10px] md:text-sm text-gray-500">
              <span class="text-emerald-600 font-medium">Device Setup</span>
              <ChevronRight class="h-3.5 w-3.5 mx-1 text-gray-400" />
              <span class="text-gray-600">{{ currentView === 'history' ? 'Schedule History' : 'Overview' }}</span>
            </div>
          </div>
          
          <!-- Controls aligned horizontally with improved styling -->
          <div v-if="currentView === 'history'" class="flex items-center gap-2 flex-wrap md:flex-nowrap">
            <!-- Back to overview button -->
            <button 
              @click="backToOverview()" 
              class="flex items-center gap-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-full px-4 py-2 transition-all duration-300 shadow-sm hover:shadow-md text-sm"
            >
              <ArrowLeft class="w-3 h-4 md:w-4 md:h-4" />
              <span class="text-[10px] md:text-xs">Back to Overview</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Content Wrapper - ONLY THIS SHOULD BE SCROLLABLE -->
      <div v-if="currentView === 'overview'" class="p-2 md:p-8 overflow-y-auto">
        <!-- System Controls Section - KEEPING ORIGINAL 3-COLUMN GRID -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Motor Control Card - Left Position (COMPLETELY UNTOUCHED) -->
          <div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300">
            <div class="flex items-center justify-between mb-6">
              <div class="flex items-center gap-2">
                <!-- Changed icon color from purple to green -->
                <div class="text-green-500">
                  <Droplet class="w-5 h-5" />
                </div>
                <h2 class="text-lg font-medium text-gray-800">Motor Control</h2>
              </div>
            </div>
            
            <!-- Motor Status and Toggle - Ultra Modern Design -->
            <div class="mt-6">
              <div class="flex items-center justify-between mb-4">
                <span class="text-sm font-medium text-gray-700">Motor Status</span>
                <div class="flex items-center gap-2">
                  <div class="w-2.5 h-2.5 rounded-full" :class="waterPumpActive ? 'bg-green-500' : 'bg-gray-300'"></div>
                  <span 
                    class="text-xs font-medium tracking-wider px-2 py-1 rounded-full"
                    :class="waterPumpActive ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-500'"
                  >
                    {{ waterPumpActive ? 'ACTIVE' : 'INACTIVE' }}
                  </span>
                </div>
              </div>
              
              <!-- Ultra Modern Power Button - FIXED CLICKABLE AREA -->
              <div class="flex justify-center mb-8">
                <!-- Entire button container is now clickable -->
                <div 
                  class="relative w-48 h-48 cursor-pointer"
                  @click="showToggleConfirmation()"
                >
                  <!-- Outer glow effect -->
                  <div 
                    class="absolute inset-0 rounded-full blur-xl transition-all duration-500 pointer-events-none"
                    :class="waterPumpActive ? 'bg-green-300 opacity-40' : 'bg-orange-300 opacity-30'"
                  ></div>
                  
                  <!-- Subtle background pattern -->
                  <div class="absolute inset-0 rounded-full overflow-hidden opacity-10 pointer-events-none">
                    <div class="absolute inset-0 bg-gradient-to-br from-white to-transparent"></div>
                    <div v-for="i in 8" :key="`pattern-${i}`" class="absolute w-full h-0.5 bg-white opacity-30"
                      :style="{
                        transform: `rotate(${i * 22.5}deg)`,
                        top: '50%'
                      }"
                    ></div>
                  </div>
                  
                  <!-- Outer ring with subtle gradient -->
                  <div 
                    class="absolute inset-0 rounded-full border-2 transition-all duration-500 pointer-events-none"
                    :class="waterPumpActive ? 'border-green-300 opacity-80' : 'border-orange-300 opacity-60'"
                  >
                    <div class="absolute inset-0 rounded-full bg-gradient-to-b from-white to-transparent opacity-30"></div>
                  </div>
                  
                  <!-- Tick marks around the button - Properly positioned -->
                  <div class="absolute inset-0 pointer-events-none">
                    <div v-for="i in 12" :key="`tick-${i}`" 
                      class="absolute w-1 h-3 rounded-full transition-all duration-300" 
                      :class="waterPumpActive ? 'bg-green-200' : 'bg-orange-200'"
                      :style="{
                        transform: `rotate(${i * 30}deg) translateY(-22px)`,
                        left: 'calc(50% - 0.5px)',
                        top: '50%',
                        transformOrigin: 'center calc(100% + 22px)',
                        opacity: i % 3 === 0 ? '0.8' : '0.4'
                      }"
                    ></div>
                  </div>
                  
                  <!-- Main button with glass morphism effect -->
                  <div 
                    class="absolute inset-6 rounded-full overflow-hidden transition-all duration-500 z-10 glass-button pointer-events-none"
                    :class="waterPumpActive ? 'active-button' : 'inactive-button'"
                  >
                    <!-- Background gradient -->
                    <div 
                      class="absolute inset-0 transition-all duration-500"
                      :class="waterPumpActive ? 'bg-gradient-to-br from-green-400 to-green-600' : 'bg-gradient-to-br from-orange-400 to-orange-600'"
                    ></div>
                    
                    <!-- Glass effect overlay -->
                    <div class="absolute inset-0 bg-white opacity-10"></div>
                    <div class="absolute inset-0 bg-gradient-to-b from-white to-transparent opacity-20"></div>
                    
                    <!-- Highlight effect -->
                    <div class="absolute inset-x-0 top-0 h-1/3 bg-gradient-to-b from-white to-transparent opacity-30 rounded-t-full"></div>
                    
                    <!-- Center content with modern icon -->
                    <div class="absolute inset-0 flex items-center justify-center">
                      <div class="text-center z-20">
                        <!-- Power icon with glow effect -->
                        <div class="relative">
                          <Power class="w-12 h-12 text-white drop-shadow-lg" :class="waterPumpActive ? 'power-icon-on' : 'power-icon-off'" />
                        </div>
                        
                        <!-- Status text with modern font -->
                        <div class="mt-2">
                          <span class="text-2xl font-bold text-white drop-shadow-lg tracking-wider">
                            {{ waterPumpActive ? 'ON' : 'OFF' }}
                          </span>
                        </div>
                      </div>
                    </div>
                    
                    <!-- Animated pulse effect when active -->
                    <div 
                      v-if="waterPumpActive" 
                      class="absolute inset-0 bg-white opacity-0 pulse-animation"
                    ></div>
                  </div>
                  
                  <!-- Inner ring glow -->
                  <div 
                    class="absolute pointer-events-none"
                    :class="waterPumpActive ? 'inset-5 rounded-full border border-green-200 opacity-60' : 'inset-5 rounded-full border border-orange-200 opacity-40'"
                  ></div>
                </div>
              </div>
              
              <!-- Motor Activity History - Modern Clean Design with scrolling -->
              <div class="mt-6 space-y-3">
                <h3 class="text-sm font-medium text-gray-700">Recent Activity</h3>
                <div class="max-h-[200px] overflow-y-auto pr-1 space-y-2">
                  <!-- Loading state -->
                  <div v-if="isLoadingActivities" class="py-8 flex flex-col items-center justify-center">
                    <div class="w-8 h-8 border-2 border-green-500 border-t-transparent rounded-full animate-spin mb-2"></div>
                    <p class="text-sm text-gray-500">Loading activities...</p>
                  </div>
                  
                  <!-- Empty state -->
                  <div v-else-if="filteredMotorActivities.length === 0" class="flex flex-col items-center justify-center py-4 text-center">
                    <p class="text-gray-400 text-sm">No recent activities</p>
                  </div>
                  
                  <!-- Activities list -->
                  <div 
                    v-else
                    v-for="(activity, index) in filteredMotorActivities" 
                    :key="index" 
                    class="flex items-center justify-between bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors"
                  >
                    <div class="flex items-center gap-2">
                      <div class="w-2 h-2 rounded-full" :class="activity.status ? 'bg-green-500' : 'bg-gray-400'"></div>
                      <span class="text-xs text-gray-600">{{ activity.timestamp }}</span>
                    </div>
                    <span 
                      class="text-xs font-medium px-2 py-1 rounded-full"
                      :class="activity.status ? 'bg-green-50 text-green-600' : 'bg-gray-100 text-gray-600'"
                    >
                      {{ activity.status ? 'Turned ON' : 'Turned OFF' }}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Saved Schedules Card - Expanded to take 2/3 of the space (col-span-2) -->
          <div class="bg-white rounded-2xl p-2 md:p-6 border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 md:col-span-2">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <div class="text-green-500">
                  <CalendarClock class="w-5 h-5" />
                </div>
                <h2 class="text-xs md:text-lg font-medium text-gray-800">Saved Schedules</h2>
              </div>
              <div class="flex items-center gap-2 grid grid-cols-1 md:grid-cols-2">
                <!-- View History Button -->
                <button 
                  @click="viewScheduleHistory()" 
                  class="flex items-center gap-1.5 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-full px-2 py-1 md:px-4 md:py-2 transition-all duration-300 shadow-sm hover:shadow-md text-[10px] md:text-sm"
                >
                  <History class="w-4 h-4" />
                  <span>View History</span>
                </button>
                <!-- Add Schedule Button - Slightly larger but not too large -->
                <button 
                  @click="openScheduleModal()" 
                  class="flex items-center gap-1.5 bg-green-500 hover:bg-green-600 text-white font-medium rounded-full px-2 py-1 md:px-4 md:py-2 transition-all duration-300 shadow-sm hover:shadow-md text-[10px] md:text-sm"
                >
                  <Plus class="w-4 h-4" />
                  <span>Add Schedule</span>
                </button>
              </div>
            </div>
            
            <!-- "Upcoming Waterings" text positioned below the heading -->
            <div class="text-xs text-gray-500 mb-4 pl-4">
              Upcoming Waterings
            </div>
            
            <!-- Next Scheduled Watering - Enhanced with modern design -->
            <div class="mb-5 bg-green-50 rounded-xl p-2 md:p-4 flex items-center justify-between border border-green-100 shadow-sm">
              <div class="flex items-center gap-2">
                <div class="bg-green-100 p-1.5 rounded-full">
                  <CalendarClock class="w-4 h-4 text-green-600" />
                </div>
                <span class="text-xs md:text-sm text-gray-700">Next scheduled watering</span>
              </div>
              <span 
                v-if="isLoadingNextWatering" 
                class="text-sm font-medium text-gray-500 bg-gray-100 px-3 py-1 rounded-full flex items-center gap-2"
              >
                <div class="w-3 h-3 border-2 border-gray-300 border-t-gray-600 rounded-full animate-spin"></div>
                Loading...
              </span>
              <span 
                v-else 
                class="text-xs md:text-sm font-medium text-green-700 bg-green-100 px-3 py-1 rounded-full"
              >
                {{ nextWateringTime }}
              </span>
            </div>
            
            <div class="flex items-center justify-between mb-4">
              <div class="text-sm text-gray-500">All scheduled waterings:</div>
              <div class="h-0.5 flex-grow mx-4 bg-gray-100"></div>
            </div>
            
            <!-- Saved Schedules List - Enhanced with better spacing and modern design -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 pr-1 mb-4">
              <div v-if="upcomingSchedules.length === 0" class="flex flex-col items-center justify-center py-12 text-center md:col-span-2 lg:col-span-3">
                <div class="bg-gray-50 p-6 rounded-full mb-4">
                  <CalendarClock class="w-16 h-16 text-gray-200" />
                </div>
                <p class="text-gray-400 font-medium">No upcoming schedules</p>
                <p class="text-xs text-gray-400 mt-2">Add a schedule to see it here</p>
              </div>
              
              <div 
                v-for="(schedule, index) in upcomingSchedules" 
                :key="index"
                class="bg-white rounded-xl p-5 border border-gray-100 hover:border-green-200 transition-all duration-300 hover:shadow-md group relative overflow-hidden"
              >
                <!-- Decorative accent -->
                <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-green-400 to-green-500"></div>
                
                <div class="flex items-center justify-between mb-3">
                  <div class="flex items-center gap-2">
                    <div class="w-2.5 h-2.5 rounded-full bg-green-500"></div>
                    <span class="text-sm font-medium text-gray-700">
                      {{ formatScheduleDateTime(schedule) }}
                    </span>
                  </div>
                  <div class="flex items-center gap-1">
                    <!-- Edit button -->
                    <button 
                      @click="editSchedule(getOriginalIndex(schedule.id))" 
                      class="text-gray-300 group-hover:text-green-500 transition-colors p-1 rounded-full hover:bg-green-50"
                      title="Edit schedule"
                    >
                      <Edit2 class="w-4 h-4" />
                    </button>
                    <!-- Delete button -->
                    <button 
                      @click="removeSchedule(getOriginalIndex(schedule.id))" 
                      class="text-gray-300 group-hover:text-red-500 transition-colors p-1 rounded-full hover:bg-red-50"
                      title="Delete schedule"
                    >
                      <Trash2 class="w-4 h-4" />
                    </button>
                  </div>
                </div>
                
                <div class="flex items-center gap-4 text-xs text-gray-500 mt-3">
                  <div class="flex items-center gap-1.5 bg-gray-50 px-2.5 py-1.5 rounded-full border border-gray-100">
                    <Clock class="w-3.5 h-3.5 text-green-500" />
                    <span>{{ schedule.duration }} min</span>
                  </div>
                  
                  <div class="flex items-center gap-1.5 bg-gray-50 px-2.5 py-1.5 rounded-full border border-gray-100">
                    <Calendar class="w-3.5 h-3.5 text-green-500" />
                    <span>{{ schedule.mode }}</span>
                  </div>
                </div>
                
                <div v-if="schedule.mode === 'weekly'" class="flex flex-wrap gap-1.5 mt-4">
                  <span 
                    v-for="(day, dayIndex) in weekDays" 
                    :key="dayIndex"
                    :class="[
                      'text-xs px-2 py-1 rounded-md transition-colors',
                      schedule.days[dayIndex] 
                        ? 'bg-green-100 text-green-700 border border-green-200' 
                        : 'bg-gray-50 text-gray-400 border border-gray-100'
                    ]"
                  >
                    {{ day.substring(0, 3) }}
                  </span>
                </div>
                
                <!-- Additional settings indicators -->
                <div class="flex items-center gap-2 mt-3">
                  <!-- <div v-if="schedule.skipIfRain" class="flex items-center gap-1 text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                    <CloudRain class="w-3 h-3" />
                    <span>Skip if rain</span>
                  </div> -->
                  <div v-if="schedule.notifyWatering" class="flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2 py-1 rounded-full">
                    <Bell class="w-3 h-3" />
                    <span>Notify</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Schedule History View (MODIFIED to use 1/4 - 3/4 layout) -->
      <div v-else-if="currentView === 'history'" class="flex-1 flex flex-col overflow-hidden">
        
        <!-- Modified layout - 1/4 and 3/4 split -->
        <div class="flex flex-col md:flex-row grid grid-cols-1 md:flex overflow-y-auto">
          
          <!-- LEFT SIDE (1/4) - Filters, Search, Export -->
          <div class="w-full md:w-1/4 border-r border-gray-100 bg-white p-2 mb-3 md:p-4 flex flex-col transition-all duration-300 ease-in-out" 
              :class="showFilters ? 'h-auto' : 'h-[50px] md:h-auto overflow-hidden'">
            
            <!-- Mobile toggle button for filters - IMPROVED VISIBILITY -->
            <button 
              @click="showFilters = !showFilters"
              class="md:hidden flex items-center justify-between w-full bg-emerald-50 hover:bg-emerald-100 p-2 rounded-lg border border-emerald-200 transition-colors"
            >
              <div class="flex items-center gap-3">
                <Filter class="w-3 h-3 text-emerald-600" />
                <span class="text-xs font-medium text-emerald-700">Filters & Options</span>
              </div>
              <ChevronDown class="w-5 h-5 text-emerald-600 transition-transform" :class="{ 'rotate-180': showFilters }" />
            </button>
            
            <!-- Search and Filters Container - Smooth height transition -->
            <div class="transition-all duration-300 ease-in-out overflow-auto" 
                :class="showFilters ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0 md:max-h-none md:opacity-100'">
              
              <!-- Search Bar -->
              <div class="mb-4 mt-2 md:mt-0">
                <div class="relative">
                  <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                  <input
                    type="text"
                    placeholder="Search schedules..."
                    class="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 text-xs"
                    v-model="searchQuery"
                  />
                </div>
              </div>
              
              <!-- Filters Section -->
              <div class="space-y-4 mb-4">
                <h3 class="text-sm font-medium text-gray-700">Filters</h3>
                
                <!-- Date Range -->
                <div class="space-y-2">
                  <label class="text-xs text-gray-500 font-medium">Date Range</label>
                  <div class="flex flex-col space-y-2">
                    <div class="flex items-center">
                      <span class="text-xs text-gray-500 w-14">From:</span>
                      <input 
                        type="date" 
                        v-model="historyFilters.startDate" 
                        class="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                        :max="currentDateFormatted"
                      />
                    </div>
                    <div class="flex items-center">
                      <span class="text-xs text-gray-500 w-14">To:</span>
                      <input 
                        type="date" 
                        :value="currentDateFormatted"
                        class="flex-1 border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500 bg-gray-100"
                        readonly
                      />
                    </div>
                  </div>
                </div>
                
                <!-- Schedule Type -->
                <div class="space-y-2">
                  <label class="text-xs text-gray-500 font-medium">Schedule Type</label>
                  <select 
                    v-model="historyFilters.scheduleType" 
                    class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="all">All Types</option>
                    <option value="one-time">One-time</option>
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="custom">Custom</option>
                  </select>
                </div>
                
                <!-- Duration -->
                <div class="space-y-2">
                  <label class="text-xs text-gray-500 font-medium">Duration</label>
                  <select 
                    v-model="historyFilters.duration" 
                    class="w-full border border-gray-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500"
                  >
                    <option value="all">All Durations</option>
                    <option value="short">Short (< 10 min)</option>
                    <option value="medium">Medium (10-30 min)</option>
                    <option value="long">Long (> 30 min)</option>
                  </select>
                </div>
                
                <!-- Apply Filters Button -->
                <button 
                  @click="applyHistoryFilters" 
                  class="w-full flex items-center justify-center gap-2 px-4 py-3 bg-emerald-500 text-white rounded-lg text-sm font-medium hover:bg-emerald-600 transition-colors shadow-sm"
                >
                  <Filter class="h-4 w-4" />
                  Apply Filters
                </button>
                
                <!-- Clear All Filters (only shown when filters are active) -->
                <button 
                  v-if="hasActiveFilters"
                  @click="clearAllFilters" 
                  class="w-full text-xs text-gray-500 hover:text-gray-700 underline py-2 text-center transition-colors"
                >
                  Clear all filters
                </button>
              </div>
              
              <!-- Active Filters Display -->
              <div v-if="hasActiveFilters" class="mb-6">
                <h3 class="text-xs font-medium text-gray-500 mb-3">Active filters:</h3>
                <div class="flex flex-wrap gap-2">
                  <!-- Date Range Filter Tag -->
                  <div v-if="historyFilters.startDate || historyFilters.endDate" class="flex items-center gap-1 bg-emerald-50 text-emerald-700 text-xs px-3 py-1.5 rounded-full border border-emerald-200">
                    <Calendar class="w-3 h-3" />
                    <span>{{ formatDateRange }}</span>
                    <button @click="clearDateFilter" class="ml-1 text-emerald-600 hover:text-emerald-800">
                      <X class="w-3 h-3" />
                    </button>
                  </div>
                  
                  <!-- Schedule Type Filter Tag -->
                  <div v-if="historyFilters.scheduleType !== 'all'" class="flex items-center gap-1 bg-emerald-50 text-emerald-700 text-xs px-3 py-1.5 rounded-full border border-emerald-200">
                    <CalendarClock class="w-3 h-3" />
                    <span>{{ formatScheduleType }}</span>
                    <button @click="clearTypeFilter" class="ml-1 text-emerald-600 hover:text-emerald-800">
                      <X class="w-3 h-3" />
                    </button>
                  </div>
                  
                  <!-- Duration Filter Tag -->
                  <div v-if="historyFilters.duration !== 'all'" class="flex items-center gap-1 bg-emerald-50 text-emerald-700 text-xs px-3 py-1.5 rounded-full border border-emerald-200">
                    <Clock class="w-3 h-3" />
                    <span>{{ formatDuration }}</span>
                    <button @click="clearDurationFilter" class="ml-1 text-emerald-600 hover:text-emerald-800">
                      <X class="w-3 h-3" />
                    </button>
                  </div>
                </div>
              </div>
              
              <!-- Export Section -->
              <div class="mt-6">
                <h3 class="text-sm font-medium text-gray-700 mb-3">Export Data</h3>
                
                <!-- Export Button with Dropdown -->
                <div class="relative mb-3">
                  <button 
                    @click.stop="toggleDropdown('export', $event)"
                    class="w-full flex items-center justify-between gap-2 px-4 py-3 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors border border-gray-200 shadow-sm"
                  >
                    <div class="flex items-center gap-2">
                      <Download class="h-4 w-4" />
                      <span>Export Options</span>
                    </div>
                    <ChevronDown class="h-4 w-4 transition-transform" :class="{ 'rotate-180': activeDropdown === 'export' }" />
                  </button>
                  
                  <!-- Dropdown Menu - FIXED POSITIONING -->
                  <div 
                    v-show="activeDropdown === 'export'"
                    class="fixed md:absolute left-4 right-4 md:left-0 md:right-0 mt-1 bg-white rounded-lg shadow-xl border border-gray-300 z-[1000] overflow-hidden"
                    :style="dropdownPosition.top ? {
                      top: dropdownPosition.top + 'px',
                      left: dropdownPosition.left + 'px',
                      width: dropdownPosition.width + 'px'
                    } : ''"
                    @click.stop
                    ref="exportDropdown"
                  >
                    <div class="py-1">
                      <button
                        v-for="format in exportFormats"
                        :key="format"
                        @click="exportData(format)"
                        class="w-full px-4 py-2.5 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2 transition-colors"
                      >
                        <FileText class="h-4 w-4" :class="{
                          'text-emerald-500': format === 'csv',
                          'text-red-500': format === 'pdf'
                        }" />
                        <span>Export as {{ format.toUpperCase() }}</span>
                      </button>
                      <!-- Print Button in Dropdown -->
                      <button
                        @click="printTable"
                        class="w-full px-4 py-2.5 text-left text-sm text-gray-700 hover:bg-gray-50 flex items-center gap-2 transition-colors"
                      >
                        <Printer class="h-4 w-4 text-blue-500" />
                        <span>Print Table</span>
                      </button>
                    </div>
                  </div>
                </div>
                                
                <!-- Standalone Print Button (visible on mobile) -->
                <button 
                  @click="printTable"
                  class="w-full flex items-center justify-center gap-2 px-4 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg text-sm font-medium transition-colors shadow-sm md:hidden"
                >
                  <Printer class="h-4 w-4" />
                  <span>Print Table</span>
                </button>
              </div>
            </div>
          </div>
          
          <!-- RIGHT SIDE (3/4) - Table Display -->
          <div class="w-full md:w-3/4 flex-1 flex flex-col overflow-hidden">
            <!-- Mobile Card View (shown on small screens) -->
            <div class="sm:hidden flex-1 overflow-auto bg-white p-3 space-y-3">
              <div v-for="(schedule, index) in paginatedPastSchedules" :key="index" 
                  class="bg-gray-50 rounded-lg p-3 border border-gray-200">
                <div class="flex justify-between items-start mb-2">
                  <div>
                    <div class="text-xs font-medium text-gray-900">{{ schedule.dateTime }}</div>
                  </div>
                  <span class="px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    Completed
                  </span>
                </div>
                <div class="grid grid-cols-2 gap-3">
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Duration</div>
                    <div class="text-xs font-semibold text-blue-600">{{ schedule.duration }} minutes</div>
                  </div>
                  <div>
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Type</div>
                    <div class="text-xs font-semibold text-emerald-600 capitalize">{{ schedule.mode }}</div>
                  </div>
                  <div v-if="schedule.skipIfRain || schedule.notifyWatering" class="col-span-2">
                    <div class="text-[9px] text-gray-500 uppercase tracking-wider mb-1">Settings</div>
                    <div class="flex flex-wrap gap-1">
                      <div v-if="schedule.skipIfRain" class="flex items-center gap-1 text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                        <CloudRain class="w-3 h-3" />
                        <span>Rain skip</span>
                      </div>
                      <div v-if="schedule.notifyWatering" class="flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2 py-1 rounded-full">
                        <Bell class="w-3 h-3" />
                        <span>Notify</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              
              <div v-if="paginatedPastSchedules.length === 0 && !isLoadingHistory" 
                  class="flex flex-col items-center justify-center py-8">
                <History class="h-10 w-10 text-gray-300 mb-2" />
                <p class="text-gray-500 text-xs font-medium">No schedule history found</p>
                <p class="text-gray-400 text-[10px]">Completed schedules will appear here</p>
              </div>
            </div>

            <!-- Desktop Table View (shown on medium screens and up) -->
            <div class="hidden sm:flex flex-1 flex-col min-h-0">
              <!-- Fixed Table Header - Will not scroll -->
              <div class="bg-gray-50 border-b border-gray-200">
                <table class="min-w-full">
                  <thead>
                    <tr>
                      <th class="w-[25%] py-1 px-2 md:py-3 md:px-4 text-left text-[8px] md:text-xs font-medium text-gray-500 uppercase tracking-wider">
                        <div class="text-gray-600">Date & Time</div>
                        <div class="text-gray-400 text-[5px] md:text-[10px] normal-case">MMM DD, YYYY HH:MM</div>
                      </th>
                      <th class="w-[20%] py-1 px-2 md:py-3 md:px-4 text-left text-[8px] md:text-xs font-medium uppercase tracking-wider">
                        <div class="text-blue-600">Duration</div>
                        <div class="text-gray-400 text-[5px] md:text-[10px] normal-case">Minutes</div>
                      </th>
                      <th class="w-[20%] py-1 px-2 md:py-3 md:px-4 text-left text-[8px] md:text-xs font-medium uppercase tracking-wider">
                        <div class="text-emerald-600">Schedule Type</div>
                        <div class="text-gray-400 text-[5px] md:text-[10px] normal-case">Mode</div>
                      </th>
                      <th class="w-[15%] py-1 px-2 md:py-3 md:px-4 text-left text-[8px] md:text-xs font-medium uppercase tracking-wider">
                        <div class="text-gray-600">Status</div>
                        <div class="text-gray-400 text-[5px] md:text-[10px] normal-case">Completion</div>
                      </th>
                      <th class="w-[20%] py-1 px-2 md:py-3 md:px-4 text-left text-[8px] md:text-xs font-medium uppercase tracking-wider">
                        <div class="text-gray-600">Additional Info</div>
                        <div class="text-gray-400 text-[5px] md:text-[10px] normal-case">Settings</div>
                      </th>
                    </tr>
                  </thead>
                </table>
              </div>
              
              <!-- Scrollable Table Body -->
              <div class="flex-1 overflow-y-auto">
                <table class="min-w-full">
                  <tbody>
                    <!-- Loading state -->
                    <tr v-if="isLoadingHistory" class="border-b border-gray-50 last:border-0">
                      <td colspan="5" class="px-4 py-20 text-center">
                        <div class="flex flex-col items-center justify-center">
                          <div class="w-10 h-10 border-2 border-emerald-500 border-t-transparent rounded-full animate-spin mb-4"></div>
                          <p class="text-gray-500">Loading schedule history...</p>
                        </div>
                      </td>
                    </tr>
                    
                    <!-- Empty state -->
                    <tr v-else-if="filteredPastSchedules.length === 0" class="border-b border-gray-50 last:border-0">
                      <td colspan="5" class="px-4 py-20 text-center">
                        <div class="flex flex-col items-center justify-center">
                          <History class="h-16 w-16 text-gray-200 mb-4" />
                          <p class="text-gray-400 font-medium">No schedule history found</p>
                          <p class="text-xs text-gray-400 mt-2">Completed schedules will appear here</p>
                        </div>
                      </td>
                    </tr>
                    
                    <!-- Data rows -->
                    <tr 
                      v-else
                      v-for="(schedule, index) in paginatedPastSchedules" 
                      :key="index"
                      class="border-b border-gray-50 hover:bg-gray-50 transition-colors last:border-0"
                    >
                      <!-- Date & Time -->
                      <td class="w-[25%] px-4 py-3 whitespace-nowrap">
                        <div class="flex items-center gap-2">
                          <div class="w-1 h-1 md:w-2 md:h-2 rounded-full bg-gray-400"></div>
                          <div class="text-xs md:text-sm font-medium text-gray-700">{{ schedule.dateTime }}</div>
                        </div>
                      </td>
                      
                      <!-- Duration -->
                      <td class="w-[20%] px-4 py-3 whitespace-nowrap">
                        <div class="text-xs md:text-sm font-medium text-blue-600">
                          {{ schedule.duration }} minutes
                        </div>
                      </td>
                      
                      <!-- Schedule Type -->
                      <td class="w-[20%] px-4 py-3 whitespace-nowrap">
                        <span class="px-3 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 capitalize">
                          {{ schedule.mode }}
                        </span>
                      </td>
                      
                      <!-- Status -->
                      <td class="w-[15%] px-4 py-3 whitespace-nowrap">
                        <span class="px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                          Completed
                        </span>
                      </td>
                      
                      <!-- Additional Info -->
                      <td class="w-[20%] px-4 py-3">
                        <div class="flex flex-wrap gap-1">
                          <div v-if="schedule.skipIfRain" class="flex items-center gap-1 text-xs text-blue-600 bg-blue-50 px-2 py-1 rounded-full">
                            <CloudRain class="w-3 h-3" />
                            <span>Rain skip</span>
                          </div>
                          <div v-if="schedule.notifyWatering" class="flex items-center gap-1 text-xs text-amber-600 bg-amber-50 px-2 py-1 rounded-full">
                            <Bell class="w-3 h-3" />
                            <span>Notify</span>
                          </div>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Pagination - At the bottom of right side -->
            <div class="border-t border-gray-200 py-2 px-3 bg-gray-50">
              <div class="flex items-center justify-between">
                <div class="text-[10px] md:text-xs text-gray-600">
                  Showing {{ paginationStart }} - {{ paginationEnd }} of {{ filteredPastSchedules.length }}
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
                      :disabled="page === '..'"
                      :class="[
                        'px-2 py-1 text-[10px] md:text-xs rounded min-w-[20px]',
                        page === currentPage 
                          ? 'bg-emerald-500 text-white font-medium' 
                          : page === '..' 
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
  </div>

  <!-- Toggle Confirmation Dialog -->
  <Transition name="modal">
    <div v-if="showToggleConfirmationDialog" class="fixed inset-0 z-[10000] flex items-center justify-center p-4 sm:p-0">
      <div 
        class="fixed inset-0 bg-black/50 backdrop-blur-sm" 
        @click="showToggleConfirmationDialog = false"
      ></div>

      <div class="relative bg-white rounded-xl shadow-xl w-full max-w-md p-6 z-[10001]">
        <div class="flex items-center gap-4 mb-4">
          <div :class="waterPumpActive ? 'bg-red-100' : 'bg-green-100'" class="p-2 rounded-full">
            <Power :class="waterPumpActive ? 'text-red-600' : 'text-green-600'" class="w-6 h-6" />
          </div>
          <h3 class="text-lg font-medium text-gray-900">
            {{ waterPumpActive ? 'Turn OFF Water Pump?' : 'Turn ON Water Pump?' }}
          </h3>
        </div>

        <p class="text-gray-600 mb-6">
          <template v-if="!waterPumpActive && soilMoisture !== null && soilMoisture >= 50">
            The soil moisture is still moist with {{ soilMoisture }}%. Are you sure you want to turn ON?
          </template>
          <template v-else>
            {{ waterPumpActive 
              ? 'Are you sure you want to turn OFF the water pump?' 
              : 'Are you sure you want to turn ON the water pump?' }}
          </template>
        </p>

        <div class="flex justify-end gap-3">
          <button 
            @click="showToggleConfirmationDialog = false" 
            class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 text-sm font-medium rounded-lg px-4 py-2 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="confirmToggleWaterPump"
            :disabled="isTogglingMotor" 
            :class="waterPumpActive 
              ? 'bg-red-600 hover:bg-red-700' 
              : 'bg-green-600 hover:bg-green-700'"
            class="text-white text-sm font-medium rounded-lg px-4 py-2 transition-colors flex items-center gap-2"
          >
            <span v-if="isTogglingMotor">Processing...</span>
            <div v-else class="flex gap-2">
              <Power class="w-4 h-4" />
              <span>{{ waterPumpActive ? 'Turn OFF' : 'Turn ON' }}</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- Modern Watering Schedule Modal with Calendar -->
  <Transition name="modal">
    <div v-if="showScheduleModal" class="fixed inset-0 z-[9999] flex items-center justify-center md:p-4">
      <!-- Backdrop with blur effect -->
      <div 
        class="fixed inset-0 bg-black/50 backdrop-blur-sm" 
        @click="closeScheduleModal"
      ></div>
      
      <!-- Modal Content - Redesigned with modern UI and fixed header and rounded bottom corners -->
      <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[90vh] flex flex-col m-2 md:m-4 z-[10000] overflow-hidden">
        <!-- Modal Header with gradient background - FIXED -->
        <div class="bg-gradient-to-r from-green-500 to-emerald-600 p-2 md:p-6 rounded-t-2xl flex items-center justify-between sticky top-0 z-10">
          <div class="flex items-center gap-3">
            <div class="bg-white/20 p-2 rounded-full">
              <CalendarClock class="w-4 h-4 md:w-6 md:h-6 text-white" />
            </div>
            <h2 class="text-sm md:text-xl font-semibold text-white">
              {{ editingScheduleId !== null ? 'Edit Schedule' : 'New Watering Schedule' }}
            </h2>
          </div>
          <button 
            @click="closeScheduleModal" 
            class="text-white/80 hover:text-white transition-colors bg-white/10 hover:bg-white/20 rounded-full p-1.5"
          >
            <X class="w-4 h-4 md:w-5 md:h-5" />
          </button>
        </div>
        
        <!-- Schedule Type Tabs - FIXED -->
        <div class="px-4 pb-2 pt-2 md:px-6 md:pt-6 md:pb-2 border-b border-gray-100 bg-white sticky md:top-[76px] z-10">
          <div class="flex space-x-2">
            <button 
              @click="wateringMode = 'weekly'" 
              :class="[
                'px-3 py-1 md:px-4 md:py-2 rounded-full text-xs md:text-sm font-medium transition-all',
                wateringMode === 'weekly' 
                  ? 'bg-green-500 text-white shadow-sm' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              Weekly
            </button>
            <button 
              @click="wateringMode = 'daily'" 
              :class="[
                'px-3 py-1 md:px-4 md:py-2 rounded-full text-xs md:text-sm font-medium transition-all',
                wateringMode === 'daily' 
                  ? 'bg-green-500 text-white shadow-sm' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              Daily
            </button>
            <button 
              @click="wateringMode = 'one-time'" 
              :class="[
                'px-3 py-1 md:px-4 md:py-2 rounded-full text-xs md:text-sm font-medium transition-all',
                wateringMode === 'one-time' 
                  ? 'bg-green-500 text-white shadow-sm' 
                  : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
              ]"
            >
              One-time
            </button>
          </div>
        </div>
        
        <!-- Scrollable Content Area -->
        <div class="overflow-y-auto flex-1">
          <!-- Modal Body -->
          <div class="p-4 md:p-6">
            <!-- Calendar for One-time and Custom scheduling -->
            <div v-if="wateringMode === 'one-time' || wateringMode === 'custom'" class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Select Date</label>
              <div class="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden">
                <!-- Calendar Header -->
                <div class="flex items-center justify-between p-4 bg-gray-50 border-b border-gray-200">
                  <button @click="prevMonth" class="p-1 rounded-full hover:bg-gray-200 transition-colors">
                    <ChevronLeft class="w-5 h-5 text-gray-600" />
                  </button>
                  <h3 class="text-sm font-medium text-gray-700">{{ currentMonthName }} {{ currentYear }}</h3>
                  <button @click="nextMonth" class="p-1 rounded-full hover:bg-gray-200 transition-colors">
                    <ChevronRight class="w-5 h-5 text-gray-600" />
                  </button>
                </div>
                
                <!-- Calendar Grid -->
                <div class="p-4">
                  <!-- Day headers -->
                  <div class="grid grid-cols-7 mb-2">
                    <div v-for="day in ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']" :key="day" class="text-xs font-medium text-gray-500 text-center py-2">
                      {{ day }}
                    </div>
                  </div>
                  
                  <!-- Calendar days -->
                  <div class="grid grid-cols-7 gap-1">
                    <div 
                      v-for="(day, index) in calendarDays" 
                      :key="index"
                      @click="!day.isDisabled && selectCalendarDate(day)"
                      :class="[
                        'h-9 flex items-center justify-center rounded-full text-sm transition-all',
                        day.isCurrentMonth ? (day.isDisabled ? 'text-gray-300 cursor-not-allowed' : 'hover:bg-green-50 cursor-pointer') : 'text-gray-400',
                        isSelectedDate(day) ? 'bg-green-500 text-white font-medium hover:bg-green-600' : '',
                        isToday(day) && !isSelectedDate(day) ? 'border border-green-500 text-green-600' : '',
                        day.hasOneTimeSchedule && day.isCurrentMonth && !isSelectedDate(day) ? 'border-2 border-orange-400 text-orange-600 font-medium' : ''
                      ]"
                    >
                      <span class="relative">
                        {{ day.day }}
                        <span v-if="day.hasOneTimeSchedule && day.isCurrentMonth" class="absolute -top-1 -right-1 w-2.5 h-2.5 bg-orange-500 rounded-full border-2 border-white shadow-sm"></span>
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Weekly Schedule - Enhanced UI -->
            <div v-if="wateringMode === 'weekly'" class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Select Days</label>
              <div class="grid grid-cols-7 gap-2">
                <button 
                  v-for="(day, index) in weekDays" 
                  :key="day"
                  @click="toggleWateringDay(index)"
                  :class="[
                    'md:py-3 py-2 px-2 w-[40px] md:w-[80px] rounded-xl transition-all text-xs md:text-sm font-medium relative overflow-hidden',
                    wateringDays[index] 
                      ? 'bg-green-500 text-white shadow-sm' 
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  ]"
                >
                  <span class="relative z-10">{{ day.substring(0, 3) }}</span>
                  <div 
                    v-if="wateringDays[index]" 
                    class="absolute bottom-0 left-0 w-full h-1 bg-green-600"
                  ></div>
                </button>
              </div>
            </div>
            
            <!-- Time of Day - Enhanced UI -->
            <div class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Time of Day</label>
              <div class="flex items-center">
                <div class="bg-gray-50 rounded-xl px-4 py-3 w-full flex items-center justify-center border border-gray-200">
                  <div class="relative">
                    <input 
                      type="text" 
                      v-model="formattedHour" 
                      class="w-16 text-center bg-transparent border-0 text-xl font-medium focus:outline-none focus:ring-0"
                      @blur="validateHour"
                    />
                    <div class="absolute -top-3 left-0 w-full flex justify-center">
                      <button @click="incrementHour" class="text-gray-400 hover:text-gray-600">
                        <ChevronUp class="w-4 h-4" />
                      </button>
                    </div>
                    <div class="absolute -bottom-3 left-0 w-full flex justify-center">
                      <button @click="decrementHour" class="text-gray-400 hover:text-gray-600">
                        <ChevronDown class="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  
                  <span class="text-gray-400 mx-2 text-2xl">:</span>
                  
                  <div class="relative">
                    <input 
                      type="text" 
                      v-model="formattedMinute" 
                      class="w-16 text-center bg-transparent border-0 text-xl font-medium focus:outline-none focus:ring-0"
                      @blur="validateMinute"
                    />
                    <div class="absolute -top-3 left-0 w-full flex justify-center">
                      <button @click="incrementMinute" class="text-gray-400 hover:text-gray-600">
                        <ChevronUp class="w-4 h-4" />
                      </button>
                    </div>
                    <div class="absolute -bottom-3 left-0 w-full flex justify-center">
                      <button @click="decrementMinute" class="text-gray-400 hover:text-gray-600">
                        <ChevronDown class="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                  
                  <!-- AM/PM selector -->
                  <div class="ml-4 flex flex-col bg-white rounded-lg border border-gray-200 overflow-hidden">
                    <button 
                      @click="setAmPm('AM')"
                      :class="[
                        'px-3 py-1 text-xs font-medium transition-colors',
                        isAm ? 'bg-green-500 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'
                      ]"
                    >
                      AM
                    </button>
                    <button 
                      @click="setAmPm('PM')"
                      :class="[
                        'px-3 py-1 text-xs font-medium transition-colors',
                        !isAm ? 'bg-green-500 text-white' : 'bg-white text-gray-600 hover:bg-gray-100'
                      ]"
                    >
                      PM
                    </button>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Duration - Enhanced UI -->
            <div class="mb-6">
              <div class="flex items-center justify-between mb-2">
                <label class="text-sm font-medium text-gray-700">Duration</label>
                <div class="flex items-center gap-2">
                  <span class="text-sm text-gray-500">{{ wateringDuration }} minutes</span>
                </div>
              </div>
              
              <div class="relative">
                <input
                  type="range"
                  v-model.number="wateringDuration"
                  min="1"
                  max="120"
                  step="1"
                  class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-green-500"
                />
                <div class="absolute -top-2 left-0 right-0 flex justify-between px-2 text-xs text-gray-500">
                  <span>1m</span>
                  <span>30m</span>
                  <span>60m</span>
                  <span>90m</span>
                  <span>120m</span>
                </div>
              </div>
              
              <div class="flex items-center justify-between mt-6">
                <div class="flex items-center gap-2">
                  <button 
                    @click="decreaseDuration" 
                    class="bg-gray-100 hover:bg-gray-200 rounded-lg p-2 transition-colors"
                  >
                    <Minus class="w-4 h-4 text-gray-600" />
                  </button>
                  <div class="bg-gray-50 rounded-lg px-4 py-2 w-20 text-center border border-gray-200">
                    <span class="text-lg font-medium">{{ wateringDuration }}</span>
                  </div>
                  <button 
                    @click="increaseDuration" 
                    class="bg-gray-100 hover:bg-gray-200 rounded-lg p-2 transition-colors"
                  >
                    <Plus class="w-4 h-4 text-gray-600" />
                  </button>
                </div>
                <div class="text-sm text-gray-500">
                  Watering duration in minutes
                </div>
              </div>
            </div>
            
            <!-- Custom Schedule - Interval Settings -->
            <div v-if="wateringMode === 'custom'" class="mb-6">
              <label class="block text-sm font-medium text-gray-700 mb-2">Repeat Every</label>
              <div class="flex items-center gap-3">
                <div class="flex-1">
                  <div class="flex items-center">
                    <button 
                      @click="decreaseInterval" 
                      class="bg-gray-100 hover:bg-gray-200 rounded-l-lg p-2.5"
                    >
                      <Minus class="w-4 h-4 text-gray-600" />
                    </button>
                    <input 
                      type="number" 
                      v-model.number="wateringInterval"
                      min="1"
                      max="30"
                      class="w-full bg-gray-50 py-2.5 text-center border-y border-gray-200 text-lg focus:outline-none focus:ring-0"
                    />
                    <button
                      @click="increaseInterval"
                      class="bg-gray-100 hover:bg-gray-200 rounded-r-lg p-2.5"
                    >
                      <Plus class="w-4 h-4 text-gray-600" />
                    </button>
                  </div>
                </div>
                <select
                  v-model="wateringIntervalUnit"
                  class="bg-gray-50 rounded-lg border border-gray-200 text-base text-gray-700 focus:outline-none focus:ring-1 focus:ring-green-500 px-4 py-2.5 flex-1"
                >
                  <option value="hours">Hours</option>
                  <option value="days">Days</option>
                  <option value="weeks">Weeks</option>
                </select>
              </div>
            </div>
            
            <!-- Additional Settings -->
            <div class="mb-6">
              <h3 class="text-sm font-medium text-gray-700 mb-3">Additional Settings</h3>
            
              <div class="space-y-3">
                <!-- Notification -->
                <div class="flex items-center justify-between bg-gray-50 rounded-xl p-4 border border-gray-200">
                  <div class="flex items-center gap-3">
                    <div class="bg-amber-100 p-1.5 rounded-full">
                      <Bell class="w-5 h-5 text-amber-600" />
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-700">Receive notifications</p>
                      <p class="text-xs text-gray-500 mt-0.5">Get notified when watering starts and ends</p>
                    </div>
                  </div>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="notifyWatering" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-green-500"></div>
                  </label>
                </div>
              
                <!-- Water Flow Rate -->
                <div v-if="showAdvancedSettings" class="flex items-center justify-between bg-gray-50 rounded-xl p-4 border border-gray-200">
                  <div class="flex items-center gap-3">
                    <div class="bg-cyan-100 p-1.5 rounded-full">
                      <Droplets class="w-5 h-5 text-cyan-600" />
                    </div>
                    <div>
                      <p class="text-sm font-medium text-gray-700">Water flow rate</p>
                      <p class="text-xs text-gray-500 mt-0.5">Set the water flow intensity</p>
                    </div>
                  </div>
                  <select
                    v-model="waterFlowRate"
                    class="bg-white rounded-lg border border-gray-200 text-sm text-gray-700 focus:outline-none focus:ring-1 focus:ring-green-500 px-3 py-1.5"
                  >
                    <option value="low">Low</option>
                    <option value="medium">Medium</option>
                    <option value="high">High</option>
                  </select>
                </div>
              </div>
            
              <button
                @click="showAdvancedSettings = !showAdvancedSettings"
                class="mt-3 text-sm text-green-600 hover:text-green-700 flex items-center gap-1"
              >
                <span>{{ showAdvancedSettings ? 'Hide' : 'Show' }} advanced settings</span>
                <ChevronDown v-if="!showAdvancedSettings" class="w-4 h-4" />
                <ChevronUp v-else class="w-4 h-4" />
              </button>
            </div>
          
            <!-- Schedule Summary -->
            <div class="bg-gray-50 rounded-xl p-4 border border-gray-200 mb-6">
              <h3 class="text-sm font-medium text-gray-700 mb-2">Schedule Summary</h3>
              <div class="space-y-2 text-sm text-gray-600">
                <div class="flex items-center gap-2">
                  <Calendar class="w-4 h-4 text-gray-500" />
                  <span>{{ scheduleSummary }}</span>
                </div>
                <div class="flex items-center gap-2">
                  <Clock class="w-4 h-4 text-gray-500" />
                  <span>{{ timeDisplay }} for {{ wateringDuration }} minutes</span>
                </div>
               
              </div>
            </div>
          </div>
        </div>
        
        <!-- Modal Footer - FIXED with rounded bottom corners -->
        <div class="p-2 md:p-6 border-t border-gray-100 flex justify-end gap-3 bg-white sticky bottom-0 z-10 rounded-b-2xl">
          <button
            @click="closeScheduleModal"
            :disabled="isLoading"
            class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 text-sm font-medium rounded-lg px-5 py-2.5 transition-colors shadow-sm disabled:opacity-70 disabled:cursor-not-allowed"
          >
            Cancel
          </button>
          <button
            @click="saveWateringSchedule"
            :disabled="isLoading"
            class="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white text-sm font-medium rounded-lg px-5 py-2.5 transition-colors shadow-sm flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
            style="min-width: 150px; min-height: 42px;" 
          >
            <template v-if="isLoading">
              <div class="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span class="ml-2">Saving...</span>
            </template>
            <template v-else>
              <Save class="w-4 h-4" />
              <span>{{ editingScheduleId !== null ? 'Update Schedule' : 'Save Schedule' }}</span>
            </template>
          </button>
        </div>
      </div>
    </div>
  </Transition>

  <!-- Confirmation Dialog for Delete -->
  <Transition name="modal">
    <div v-if="showDeleteConfirmation" class="fixed inset-0 z-[10000] flex items-center justify-center p-4 sm:p-0">
      <div
        class="fixed inset-0 bg-black/50 backdrop-blur-sm"
        @click="showDeleteConfirmation = false"
      ></div>
    
      <div class="relative bg-white rounded-xl shadow-xl w-full max-w-md p-6 z-[10001]">
        <div class="flex items-center gap-4 mb-4">
          <div class="bg-red-100 p-2 rounded-full">
            <AlertTriangle class="w-6 h-6 text-red-600" />
          </div>
          <h3 class="text-lg font-medium text-gray-900">Delete Schedule</h3>
        </div>
      
        <p class="text-gray-600 mb-6">
          Are you sure you want to delete this watering schedule? This action cannot be undone.
        </p>
      
        <div class="flex justify-end gap-3">
          <button
            @click="showDeleteConfirmation = false"
            class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 text-sm font-medium rounded-lg px-4 py-2 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="confirmDeleteSchedule"
            :disabled="isDeletingSchedule"
            class="bg-red-600 hover:bg-red-700 text-white text-sm font-medium rounded-lg px-4 py-2 transition-colors flex items-center gap-2"
          >
            <template v-if="isDeletingSchedule">
              <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Deleting...</span>
            </template>
            <template v-else>
              <Trash2 class="w-4 h-4" />
              <span>Delete</span>
            </template>

          </button>
        </div>
      </div>
    </div>
  </Transition>

  <Transition name="modal">
    <div v-if="showScheduleConfirmationDialog" class="fixed inset-0 z-[10000] flex items-center justify-center p-4 sm:p-0">
      <div class="fixed inset-0 bg-black/50 backdrop-blur-sm" @click="showScheduleConfirmationDialog = false"></div>
      
      <div class="relative bg-white rounded-xl shadow-xl w-full max-w-md p-6 z-[10001]">
        <div class="flex items-center gap-4 mb-4">
          <div class="bg-green-100 p-2 rounded-full">
            <Droplets class="w-6 h-6 text-green-600" />
          </div>
          <h3 class="text-lg font-medium text-gray-900">High Soil Moisture</h3>
        </div>

        <p class="text-gray-600 mb-6">
          The soil moisture is still high with {{ soilMoistureForSchedule }}%. 
          Are you sure you want to add this watering schedule?
        </p>

        <div class="flex justify-end gap-3">
          <button 
            @click="cancelScheduleConfirmation"  
            class="bg-white border border-gray-300 text-gray-700 hover:bg-gray-50 text-sm font-medium rounded-lg px-4 py-2 transition-colors"
          >
            Cancel
          </button>
          <button 
            @click="proceedWithScheduleSave" 
            class="bg-green-600 hover:bg-green-700 text-white text-sm font-medium rounded-lg px-4 py-2 transition-colors flex items-center gap-2"
          >
            <Save class="w-4 h-4" />
            <span>{{ editingScheduleId ? 'Update Anyway' : 'Add Anyway' }}</span>
          </button>
        </div>
      </div>
    </div>
  </Transition>

</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import {
  Droplet,
  Droplets,
  Clock,
  CalendarClock,
  Plus,
  Minus,
  X,
  Calendar,
  ChevronRight,
  ChevronLeft,
  ChevronUp,
  ChevronDown,
  Power,
  CloudRain,
  Bell,
  Save,
  Edit2,
  Trash2,
  AlertTriangle,
  CheckCircle,
  History,
  ArrowLeft,
  Filter,
  Search,
  Download,
  ArrowUpDown,
  FileText,
  FileSearch,
  Info,
  XCircle,
  Printer
} from 'lucide-vue-next'
import axios from 'axios'
import jsPDF from 'jspdf'
import autoTable from 'jspdf-autotable'
import { saveAs } from 'file-saver'
import { Document, Packer, Paragraph, Table, TableRow, TableCell, TextRun } from 'docx'
import api from '../../api/index'

const SCHEDULE_ROOT_DOC = 'schedules_root'
const SCHEDULE_COLLECTION = 'watering_schedules'
const ONE_TIME_SUBCOLLECTION = 'one_time'
const WEEKLY_SUBCOLLECTION = 'weekly'
const DAILY_SUBCOLLECTION = 'daily'
const HISTORY_COLLECTION = 'history'

const API_ENDPOINTS = {
  MOTOR_STATUS: '/motor-status-ph',  // Use Philippine Time endpoint
  MOTOR_HISTORY: '/motor-history-ph', 
  SCHEDULES: '/watering-schedules',
  SCHEDULE_HISTORY: '/schedule-history',
  SOIL_MOISTURE: '/soil-moisture'
}

// View state
const currentView = ref('overview')

// System control values
const waterPumpActive = ref(false)
const motorActivities = ref([])
const isLoadingActivities = ref(true)
const isLoadingNextWatering = ref(true)
const isLoadingHistory = ref(false)
const soilMoisture = ref(null)

// Search and filter state
const searchQuery = ref('')
const activeDropdown = ref(null)
const exportFormats = ['csv', 'pdf']
const showFilterPanel = ref(false)

// Pagination
const itemsPerPage = ref(10)
const currentPage = ref(1)
const totalPages = computed(() => Math.ceil(filteredPastSchedules.value.length / itemsPerPage.value))
// Add these computed properties
const paginationStart = computed(() => {
  return ((currentPage.value - 1) * itemsPerPage.value) + 1
})

const paginationEnd = computed(() => {
  return Math.min(currentPage.value * itemsPerPage.value, filteredPastSchedules.value.length)
})

const paginationNumbers = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  
  if (total <= 1) return [1]
  
  if (current === 1) {
    return [1, '..', total]
  } else if (current === total) {
    return [1, '..', total]
  } else {
    return [current, '..', total]
  }
})

// Modal control
const showScheduleModal = ref(false)
const showAdvancedSettings = ref(false)
const showDeleteConfirmation = ref(false)
const showToast = ref(false)
const toastMessage = ref('')
const toastTimeout = ref(null)
const toastSeverity = ref('info')
const showToggleConfirmationDialog = ref(false)
const showScheduleConfirmationDialog = ref(false)
const soilMoistureForSchedule = ref(null)

// Editing state
const editingScheduleIndex = ref(null)
const scheduleToDeleteIndex = ref(null)
const editingScheduleId = ref(null)
const editingScheduleMode = ref(null)

// Schedule control values
const wateringMode = ref('weekly')
const wateringDays = ref([true, false, true, false, true, false, false])
const weekDays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
const wateringHour = ref(6)
const wateringMinute = ref(30)
const wateringDuration = ref(20)
const wateringInterval = ref(2)
const wateringIntervalUnit = ref('days')
const isAm = ref(true)

// Additional settings
const skipIfRain = ref(false)
const notifyWatering = ref(true)
const waterFlowRate = ref('medium')
let forceUpdateCount = 0;


// Calendar state
const currentDate = ref(new Date())
const selectedDate = ref(new Date())

// Saved schedules
const savedSchedules = ref([])
const isLoadingSchedules = ref(false)
// const nextWateringTime = ref('No schedules set')
const currentTime = ref(Date.now())

// History data
const pastSchedules = ref([])
const historyFilters = ref({
  startDate: '',
  endDate: new Date().toISOString().split('T')[0], 
  scheduleType: 'all',
  duration: 'all'
})

// Loading states
const isLoading = ref(false)
const isTogglingMotor = ref(false)
const isDeletingSchedule = ref(false)

const currentRealTime = ref(new Date())
let realTimeInterval
const nextUpdateTimeout = ref(null)
const activeScheduleEndTime = ref(null)

const showFilters = ref(false)

// Add this method for printing
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
  const tableRows = filteredPastSchedules.value.map(schedule => {
    // Extract date and time properly - handle both string and object formats
    let dateTime = ''
    if (schedule.dateTime) {
      dateTime = schedule.dateTime
    } else if (schedule.completedAt) {
      // If dateTime is not available, try to format completedAt
      const completedDate = new Date(schedule.completedAt)
      dateTime = completedDate.toLocaleString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
    
    // Extract duration properly
    const duration = schedule.duration ? `${schedule.duration} minutes` : ''
    
    // Extract schedule type
    const scheduleType = schedule.mode || schedule.scheduleType || ''
    
    // Extract additional info
    const additionalInfo = []
    if (schedule.skipIfRain) additionalInfo.push('Rain skip')
    if (schedule.notifyWatering) additionalInfo.push('Notify')
    
    return {
      dateTime,
      duration,
      scheduleType,
      additionalInfo: additionalInfo.join(', ')
    }
  })
  
  // Create the HTML content
  const tableContent = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Schedule History</title>
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
        .filters-info {
          margin-bottom: 15px;
          padding: 10px;
          background-color: #f9fafb;
          border-radius: 5px;
          font-size: 14px;
        }
        .filters-info span {
          display: inline-block;
          margin-right: 10px;
          padding: 4px 8px;
          background-color: #e5e7eb;
          border-radius: 4px;
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
        .status-completed {
          background-color: #d1fae5;
          color: #065f46;
          padding: 4px 8px;
          border-radius: 12px;
          display: inline-block;
        }
        .schedule-type {
          background-color: #dbeafe;
          color: #1e40af;
          padding: 4px 8px;
          border-radius: 12px;
          display: inline-block;
        }
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
        <h1>Schedule History</h1>
        <div class="date">${formattedDate}</div>
      </div>
      
      ${hasActiveFilters.value ? `
      <div class="filters-info">
        <strong>Active Filters:</strong>
        ${historyFilters.value.startDate ? `<span>From: ${formatShortDate(historyFilters.value.startDate)}</span>` : ''}
        ${historyFilters.value.scheduleType !== 'all' ? `<span>Type: ${formatScheduleType.value}</span>` : ''}
        ${historyFilters.value.duration !== 'all' ? `<span>Duration: ${formatDuration.value}</span>` : ''}
      </div>
      ` : ''}
      
      <table>
        <thead>
          <tr>
            <th>Date & Time</th>
            <th>Duration</th>
            <th>Schedule Type</th>
            <th>Status</th>
            <th>Additional Info</th>
          </tr>
        </thead>
        <tbody>
          ${tableRows.map(row => `
            <tr>
              <td>${row.dateTime}</td>
              <td>${row.duration}</td>
              <td><span class="schedule-type">${row.scheduleType}</span></td>
              <td><span class="status-completed">Completed</span></td>
              <td>${row.additionalInfo}</td>
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

// Watch for screen size changes to auto-show filters on larger screens
watch(() => window.innerWidth, (width) => {
  if (width >= 768) { // md breakpoint
    showFilters.value = true
  } else {
    showFilters.value = false
  }
}, { immediate: true })

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
  

// =============================================
// NEW SCHEDULE DISPLAY FUNCTIONS
// =============================================

const startRealTimeUpdates = () => {
  stopRealTimeUpdates() // Clear any existing timeouts
  
  // Initial update
  currentRealTime.value = new Date()
  console.log('Initial update:', currentRealTime.value.toLocaleTimeString())
  
  // Schedule next update based on watering schedules
  scheduleNextUpdate()
}

const scheduleNextUpdate = () => {
  const now = new Date()
  
  // 1. Check if we're currently in a watering period
  if (activeScheduleEndTime.value && now < activeScheduleEndTime.value) {
    const msRemaining = activeScheduleEndTime.value - now
    nextUpdateTimeout.value = setTimeout(() => {
      handleWateringComplete()
    }, msRemaining)
    console.log(`Scheduled update for watering end at ${activeScheduleEndTime.value.toLocaleTimeString()}`)
    return
  }
  
  // 2. Find the next upcoming watering schedule
  const upcomingSchedule = findNextUpcomingSchedule()
  
  if (upcomingSchedule) {
    const msUntilStart = upcomingSchedule.startTime - now
    const msUntilEnd = upcomingSchedule.endTime - now
    
    if (msUntilStart > 0) {
      // Schedule is in the future
      nextUpdateTimeout.value = setTimeout(() => {
        activeScheduleEndTime.value = upcomingSchedule.endTime
        scheduleNextUpdate() // Immediately schedule the end time
      }, msUntilStart)
      console.log(`Scheduled update for watering start at ${upcomingSchedule.startTime.toLocaleTimeString()}`)
    } else if (msUntilEnd > 0) {
      // Schedule is currently running
      activeScheduleEndTime.value = upcomingSchedule.endTime
      nextUpdateTimeout.value = setTimeout(() => {
        handleWateringComplete()
      }, msUntilEnd)
      console.log(`Scheduled update for watering end at ${upcomingSchedule.endTime.toLocaleTimeString()}`)
    }
  } else {
    // No schedules - fallback to 60 second updates
    nextUpdateTimeout.value = setTimeout(() => {
      currentRealTime.value = new Date()
      console.log('Fallback update:', currentRealTime.value.toLocaleTimeString())
      scheduleNextUpdate()
    }, 60000)
    console.log('No upcoming schedules, using 60s fallback')
  }
}

const findNextUpcomingSchedule = () => {
  const now = new Date()
  
  // Convert all schedules to start/end times
  const schedules = savedSchedules.value
    .filter(s => !s.completed)
    .map(schedule => {
      let startTime
      
      if (schedule.mode === 'daily') {
        startTime = getNextDailyOccurrence(schedule.scheduledTime)
      } else if (schedule.mode === 'weekly') {
        startTime = getNextWeeklyOccurrence(schedule)
      } else { // one-time
        startTime = new Date(schedule.scheduledTime)
      }
      
      return {
        ...schedule,
        startTime,
        endTime: new Date(startTime.getTime() + (schedule.duration * 60000))
      }
    })
    .filter(s => s.endTime > now)
    .sort((a, b) => a.startTime - b.startTime)
  
  return schedules.length > 0 ? schedules[0] : null
}

const handleWateringComplete = () => {
  currentRealTime.value = new Date()
  activeScheduleEndTime.value = null
  console.log('Watering complete, updating time:', currentRealTime.value.toLocaleTimeString())
  scheduleNextUpdate() // Immediately check for next schedule
}

// Stop updates when component unmounts
const stopRealTimeUpdates = () => {
  if (realTimeInterval) clearInterval(realTimeInterval)
}

const getNextDailyOccurrence = (timeInMs) => {
  const now = currentRealTime.value
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  
  // Convert milliseconds since midnight to hours and minutes
  const hours = Math.floor(timeInMs / (60 * 60 * 1000))
  const minutes = Math.floor((timeInMs % (60 * 60 * 1000)) / (60 * 1000))
  
  const scheduledTime = new Date(today)
  scheduledTime.setHours(hours, minutes, 0, 0)
  
  if (scheduledTime > now) {
    return scheduledTime
  }
  
  // If time has passed today, schedule for tomorrow
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)
  tomorrow.setHours(hours, minutes, 0, 0)
  return tomorrow
}

const getNextWeeklyOccurrence = (schedule) => {
  const now = currentRealTime.value
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  
  // Convert scheduled time (milliseconds since midnight) to hours and minutes
  const timeInMs = schedule.scheduledTime
  const hours = Math.floor(timeInMs / (60 * 60 * 1000))
  const minutes = Math.floor((timeInMs % (60 * 60 * 1000)) / (60 * 1000))
  
  // Find the next scheduled day
  for (let i = 0; i < 14; i++) { // Check next 2 weeks to be safe
    const checkDate = new Date(today)
    checkDate.setDate(checkDate.getDate() + i)
    const dayIndex = (checkDate.getDay() + 6) % 7 // Convert to 0=Monday
    
    if (schedule.days[dayIndex]) {
      const scheduledTime = new Date(checkDate)
      scheduledTime.setHours(hours, minutes, 0, 0)
      
      if (scheduledTime > now) {
        return scheduledTime
      }
    }
  }
  
  return new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000) // Fallback: 1 week from now
}

const formatScheduleDateTime = (schedule) => {
  // This will recompute whenever currentRealTime changes
  const _ = currentRealTime.value
  
  let displayDate
  
  if (schedule.mode === 'daily') {
    displayDate = getNextDailyOccurrence(schedule.scheduledTime)
  } else if (schedule.mode === 'weekly') {
    displayDate = getNextWeeklyOccurrence(schedule)
  } else {
    displayDate = new Date(schedule.scheduledTime)
  }
  
  return displayDate.toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}


// =============================================
// EXISTING FUNCTIONS (PRESERVED)
// =============================================

const getSubcollectionRef = (subcollection) => {
  return collection(db, SCHEDULE_COLLECTION, SCHEDULE_ROOT_DOC, subcollection)
}

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

const oneTimeScheduledDates = computed(() => {
  return savedSchedules.value
    .filter(schedule => schedule.mode === 'one-time' && !schedule.completed)
    .map(schedule => {
      const d = new Date(schedule.scheduledTime)
      return new Date(d.getFullYear(), d.getMonth(), d.getDate()).getTime()
    })
})

const hasActiveFilters = computed(() => {
  return historyFilters.value.startDate ||
         historyFilters.value.endDate ||
         historyFilters.value.scheduleType !== 'all' ||
         historyFilters.value.duration !== 'all'
})

const formatDateRange = computed(() => {
  if (historyFilters.value.startDate && historyFilters.value.endDate) {
    return `${formatShortDate(historyFilters.value.startDate)} - ${formatShortDate(historyFilters.value.endDate)}`
  } else if (historyFilters.value.startDate) {
    return `From ${formatShortDate(historyFilters.value.startDate)}`
  } else if (historyFilters.value.endDate) {
    return `Until ${formatShortDate(historyFilters.value.endDate)}`
  }
  return ''
})

const formatScheduleType = computed(() => {
  return historyFilters.value.scheduleType.charAt(0).toUpperCase() + historyFilters.value.scheduleType.slice(1)
})

const formatDuration = computed(() => {
  const duration = historyFilters.value.duration
  if (duration === 'short') return 'Short (< 10 min)'
  if (duration === 'medium') return 'Medium (10-30 min)'
  if (duration === 'long') return 'Long (> 30 min)'
  return ''
})

const formatShortDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
}

const clearDateFilter = () => {
  // Only clear start date since end date is fixed
  historyFilters.value.startDate = ''
  applyHistoryFilters()
}

const clearTypeFilter = () => {
  historyFilters.value.scheduleType = 'all'
  applyHistoryFilters()
}

const clearDurationFilter = () => {
  historyFilters.value.duration = 'all'
  applyHistoryFilters()
}

const clearAllFilters = () => {
  historyFilters.value.startDate = ''
  historyFilters.value.endDate = ''
  historyFilters.value.scheduleType = 'all'
  historyFilters.value.duration = 'all'
  applyHistoryFilters()
}

const toggleFilterPanel = () => {
  showFilterPanel.value = !showFilterPanel.value
}

// const filteredMotorActivities = computed(() => {
//   const sevenDaysAgo = new Date()
//   sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)

//   return motorActivities.value.filter(activity => {
//     const activityDate = parseActivityTimestamp(activity.timestamp)
//     return activityDate >= sevenDaysAgo
//   })
// })

const filteredMotorActivities = computed(() => {
  return motorActivities.value
})

const isDuplicateSchedule = (newScheduleDetails) => {
  const {
    mode: newMode,
    hour: newHour,
    minute: newMinute,
    duration: newDuration,
    date: newDateObj,
    days: newWeeklyDays
  } = newScheduleDetails

  const activeSchedules = savedSchedules.value.filter(s => s.completed === false)

  return activeSchedules.some(existingSchedule => {
    if (editingScheduleId.value && existingSchedule.id === editingScheduleId.value) {
      return false
    }

    const existingDate = new Date(existingSchedule.scheduledTime)
    const existingStartTime = existingDate.getHours() * 60 + existingDate.getMinutes()
    const existingEndTime = existingStartTime + (existingSchedule.duration || 0)
    const existingMode = existingSchedule.mode

    let dayOverlap = false

    // Check day overlap based on schedule types
    if (newMode === 'one-time') {
      if (existingMode === 'one-time') {
        // Both one-time: check if same date
        dayOverlap = newDateObj.toDateString() === existingDate.toDateString()
      } else if (existingMode === 'daily') {
        // One-time vs daily: daily runs every day
        dayOverlap = true
      } else if (existingMode === 'weekly') {
        // One-time vs weekly: check if one-time falls on a weekly day
        const dayIndex = (existingDate.getDay() + 6) % 7 // Convert to 0=Monday
        dayOverlap = existingSchedule.days?.[dayIndex] || false
      }
    } else if (newMode === 'daily') {
      // Daily runs every day, so always overlaps
      dayOverlap = true
    } else if (newMode === 'weekly') {
      if (existingMode === 'one-time') {
        // Weekly vs one-time: check if one-time falls on a weekly day
        const dayIndex = (existingDate.getDay() + 6) % 7
        dayOverlap = newWeeklyDays[dayIndex]
      } else if (existingMode === 'daily') {
        // Weekly vs daily: check if weekly has any days selected
        dayOverlap = newWeeklyDays.some(day => day)
      } else if (existingMode === 'weekly') {
        // Weekly vs weekly: check if any days overlap
        dayOverlap = newWeeklyDays.some((day, i) => day && existingSchedule.days?.[i])
      }
    }

    // If days overlap, check time overlap
    if (dayOverlap) {
      const newStartTime = newHour * 60 + newMinute
      const newEndTime = newStartTime + newDuration
      
      // Check if time ranges overlap (considering duration)
      return (newStartTime < existingEndTime) && (newEndTime > existingStartTime)
    }

    return false
  })
}

const filteredPastSchedules = computed(() => {
  let filtered = [...pastSchedules.value]

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(schedule => {
      const searchString = [
        schedule.mode,
        schedule.duration?.toString(),
        schedule.waterFlowRate,
        schedule.dateTime,
        getDayName(schedule.dayOfWeek),
        schedule.skipIfRain?.toString(),
        schedule.notifyWatering?.toString()
      ].join(' ').toLowerCase()
      
      return searchString.includes(query)
    })
  }

  // Filter by start date if specified
  if (historyFilters.value.startDate) {
    const startDate = new Date(historyFilters.value.startDate)
    startDate.setHours(0, 0, 0, 0)
    filtered = filtered.filter(schedule => {
      const scheduleDate = new Date(schedule.completedAt)
      return scheduleDate >= startDate
    })
  }

  // Always filter up to today at 23:59:59
   const endDate = new Date()
  endDate.setHours(23, 59, 59, 999)
  
  filtered = filtered.filter(schedule => {
    const scheduleDate = new Date(schedule.completedAt)
    return scheduleDate <= endDate
  })

  if (historyFilters.value.scheduleType !== 'all') {
    filtered = filtered.filter(schedule => schedule.mode === historyFilters.value.scheduleType)
  }

  if (historyFilters.value.duration !== 'all') {
    if (historyFilters.value.duration === 'short') {
      filtered = filtered.filter(schedule => schedule.duration < 10)
    } else if (historyFilters.value.duration === 'medium') {
      filtered = filtered.filter(schedule => schedule.duration >= 10 && schedule.duration <= 30)
    } else if (historyFilters.value.duration === 'long') {
      filtered = filtered.filter(schedule => schedule.duration > 30)
    }
  }

  return filtered
})

const formattedSchedules = (schedulesArray) => {
  return schedulesArray.map(schedule => formatHistoryItem(schedule));
};

const paginatedPastSchedules = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage.value
  const endIndex = startIndex + itemsPerPage.value
  return filteredPastSchedules.value
    .slice(startIndex, endIndex)
    .map(formatHistoryItem)
})

const getOriginalIndex = (scheduleId) => {
  return savedSchedules.value.findIndex(schedule => schedule.id === scheduleId)
}

const exportDropdown = ref(null)
const dropdownPosition = ref({
  top: 0,
  left: 0,
  width: 0
})

// Update the toggleDropdown function to accept event parameter
const toggleDropdown = (dropdown, event = null) => {
  if (activeDropdown.value === dropdown) {
    activeDropdown.value = null
    dropdownPosition.value = { top: 0, left: 0, width: 0 }
  } else {
    activeDropdown.value = dropdown
    
    // Calculate position for dropdown - only for mobile
    if (dropdown === 'export' && window.innerWidth < 768 && event) {
      nextTick(() => {
        const button = event.target.closest('button') || event.target
        if (button && exportDropdown.value) {
          const rect = button.getBoundingClientRect()
          dropdownPosition.value = {
            top: rect.bottom + window.scrollY + 5,
            left: rect.left + window.scrollX,
            width: rect.width
          }
        }
      })
    } else {
      // Reset position for desktop
      dropdownPosition.value = { top: 0, left: 0, width: 0 }
    }
  }
}

// Add click outside handler
const handleClickOutside = (event) => {
  if (activeDropdown.value && 
      !event.target.closest('.relative') && 
      !event.target.closest('.fixed') &&
      !event.target.closest('button')) {
    activeDropdown.value = null
    dropdownPosition.value = { top: 0, left: 0, width: 0 }
  }
}

const getLocalDateString = (date) => {
  const year = date.getFullYear()
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const day = String(date.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
}

const currentDateFormatted = computed(() => {
  const today = new Date()
  const year = today.getFullYear()
  const month = String(today.getMonth() + 1).padStart(2, '0')
  const day = String(today.getDate()).padStart(2, '0')
  return `${year}-${month}-${day}`
})

const viewScheduleHistory = () => {
  currentView.value = 'history'
  
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
  
  historyFilters.value = {
    ...historyFilters.value,
    startDate: thirtyDaysAgo.toISOString().split('T')[0],
    endDate: currentDateFormatted.value // Use computed current date
  }

  currentPage.value = 1
  fetchHistory()
}

const backToOverview = () => {
  currentView.value = 'overview'
}

const applyHistoryFilters = () => {
  currentPage.value = 1
}

const exportData = async (format) => {
  // Use formatted data for export
  const data = filteredPastSchedules.value.map(formatHistoryItem)
  if (!data.length) {
    window.showToast('No data to export', 'warning')
    return
  }

  // Define columns
  const columns = [
    { header: 'Date & Time', key: 'dateTime' },
    { header: 'Duration', key: 'durationText' },
    { header: 'Schedule Type', key: 'mode' },
    { header: 'Status', key: 'completed' },
    { header: 'Additional Info', key: 'additionalInfo' }
  ]

  // Prepare rows
  const rows = data.map(item => [
    item.dateTime || '',
    item.durationText || '',
    item.mode || '',
    'Completed',
    [
      item.skipIfRain ? 'Rain skip' : '',
      item.notifyWatering ? 'Notify' : ''
    ].filter(Boolean).join(', ')
  ])

  if (format === 'csv') {
    let csvContent = columns.map(col => col.header).join(',') + '\n'
    rows.forEach(row => {
      csvContent += row.map(val => `"${val}"`).join(',') + '\n'
    })
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
    saveAs(blob, 'schedule_history.csv')
    window.showToast('Schedule history exported as CSV', 'success')
  } else if (format === 'pdf') {
    const doc = new jsPDF()
    doc.text('Schedule History', 14, 16)
    autoTable(doc, {
      head: [columns.map(col => col.header)],
      body: rows,
      startY: 22,
      styles: { fontSize: 10 }
    })
    doc.save('schedule_history.pdf')
    window.showToast('Schedule history exported as PDF', 'success')
  } else if (format === 'excel' || format === 'word') {
    const tableRows = [
      new TableRow({
        children: columns.map(col => new TableCell({
          children: [new Paragraph({ children: [new TextRun({ text: col.header, bold: true })] })]
        }))
      }),
      ...rows.map(row =>
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
          new Paragraph({ text: 'Schedule History', heading: 'Heading1' }),
          new Table({ rows: tableRows })
        ]
      }]
    })
    const buffer = await Packer.toBlob(docxDoc)
    saveAs(buffer, 'schedule_history.docx')
    window.showToast('Schedule history exported as Word', 'success')
  } else {
    window.showToast('Unknown export format', 'failed')
  }
  activeDropdown.value = null
}
// ...existing code...

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

const showToggleConfirmation = () => {
  if (!waterPumpActive.value) {
    checkSoilMoistureBeforeTurningOn()
  } else {
    showToggleConfirmationDialog.value = true
  }
}

const checkSoilMoistureBeforeTurningOn = async () => {
  try {
    const response = await api.get(API_ENDPOINTS.SOIL_MOISTURE)
    const moisture = response.data.moisture
    
    if (moisture >= 50) {
      showToggleConfirmationDialog.value = true
    } else {
      confirmToggleWaterPump()
    }
  } catch (error) {
    console.error('Error checking soil moisture:', error)
    showToggleConfirmationDialog.value = true
  }
}

let motorStatusInterval = null
const MOTOR_STATUS_POLLING_INTERVAL = 1000

const startMotorStatusPolling = () => {
  stopMotorStatusPolling()
  motorStatusInterval = setInterval(fetchMotorStatus, MOTOR_STATUS_POLLING_INTERVAL)
}

const stopMotorStatusPolling = () => {
  if (motorStatusInterval) {
    clearInterval(motorStatusInterval)
    motorStatusInterval = null
  }
}

const fetchMotorStatus = async (retryCount = 0) => {
  try {
    const response = await api.get(API_ENDPOINTS.MOTOR_STATUS)
    
    if (response.data) {
      if (waterPumpActive.value !== response.data.status) {
        waterPumpActive.value = response.data.status
        console.log('Motor status updated:', response.data.status)
        
        if (!response.data.status) {
          fetchWateringSchedules()
        }
      }
    }
  } catch (error) {
    console.error('Error fetching motor status:', error)
    if (retryCount === 0) {
      window.showToast('Error fetching motor status', 'failed')
    }
    if (retryCount < 2) {
      setTimeout(() => fetchMotorStatus(retryCount + 1), 1000 * (retryCount + 1))
    }
  }
}

const formatSimpleTimestamp = (timestamp) => {
  if (!timestamp) return 'Recent activity'
  
  try {
    let date;
    
    // Handle different timestamp formats
    if (typeof timestamp === 'string') {
      // If it's already a formatted string, return as-is
      if (timestamp.includes('Today') || timestamp.includes('Yesterday') || timestamp.includes(',')) {
        return timestamp;
      }
      date = new Date(timestamp);
    } else if (typeof timestamp === 'object' && timestamp._seconds) {
      // Firebase timestamp format
      date = new Date(timestamp._seconds * 1000);
    } else {
      date = new Date(timestamp);
    }
    
    if (isNaN(date.getTime())) return 'Recent activity'
    
    // Convert to Philippine Time (UTC+8)
    const phTime = new Date(date.getTime() + (8 * 60 * 60 * 1000));
    
    // Get current Philippine time for comparison
    const now = new Date(Date.now() + (8 * 60 * 60 * 1000));
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    
    const activityDate = new Date(phTime.getFullYear(), phTime.getMonth(), phTime.getDate());
    
    // Format the time part
    const timeStr = phTime.toLocaleTimeString('en-PH', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })
    
    // Determine if it's today, yesterday, or another day
    if (activityDate.getTime() === today.getTime()) {
      return `Today, ${timeStr}`
    } 
    else if (activityDate.getTime() === yesterday.getTime()) {
      return `Yesterday, ${timeStr}`
    } 
    else {
      return phTime.toLocaleDateString('en-PH', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    }
  } catch {
    return 'Recent activity'
  }
}

// FIXED: Enhanced fetchMotorActivities with better error handling
let motorActivitiesInterval = null
const MOTOR_ACTIVITIES_POLLING_INTERVAL = 10000 // 10 seconds

const startMotorActivitiesPolling = () => {
  stopMotorActivitiesPolling()
  motorActivitiesInterval = setInterval(fetchMotorActivities, MOTOR_ACTIVITIES_POLLING_INTERVAL)
}

const stopMotorActivitiesPolling = () => {
  if (motorActivitiesInterval) {
    clearInterval(motorActivitiesInterval)
    motorActivitiesInterval = null
  }
}

const fetchMotorActivities = async () => {
  isLoadingActivities.value = true
  try {
    const response = await api.get(`${API_ENDPOINTS.MOTOR_HISTORY}?limit=20`)
    console.log('Motor history API response:', response.data)
    
    // Process the response data safely
    const newActivities = response.data.map(activity => {
      try {
        // Use formattedTime if available, otherwise format the timestamp
        let displayTime = activity.formattedTime;
        
        // If formattedTime is not available, try to format the timestamp
        if (!displayTime && activity.timestamp) {
          displayTime = formatSimpleTimestamp(activity.timestamp);
        }
        
        // Fallback if both are missing
        if (!displayTime) {
          displayTime = 'Recent activity';
        }
        
        return {
          status: activity.status,
          timestamp: displayTime,
          source: activity.source || 'manual',
          // Add unique identifier for comparison
          uniqueId: activity.timestamp || activity.formattedTime || Math.random().toString()
        }
      } catch (error) {
        console.error('Error processing activity:', error, activity)
        return {
          status: activity.status,
          timestamp: 'Recent activity',
          source: activity.source || 'manual',
          uniqueId: Math.random().toString()
        }
      }
    })
    
    // Only update if activities actually changed to avoid unnecessary re-renders
    if (JSON.stringify(motorActivities.value) !== JSON.stringify(newActivities)) {
      motorActivities.value = newActivities
      console.log('Motor activities updated')
    }
    
  } catch (error) {
    console.error('Error fetching motor activities:', error)
    // Don't clear existing activities on error, just keep showing the last good data
  } finally {
    isLoadingActivities.value = false
  }
}

// Enhanced version with timestamp-based comparison for better performance
const fetchMotorActivitiesEnhanced = async () => {
  isLoadingActivities.value = true
  try {
    const response = await api.get(`${API_ENDPOINTS.MOTOR_HISTORY}?limit=20`)
    
    // Get the timestamp of the most recent activity we currently have
    const currentLatestTimestamp = motorActivities.value[0]?.timestamp || ''
    
    // Process new activities
    const newActivities = response.data.map(activity => {
      try {
        let displayTime = activity.formattedTime;
        if (!displayTime && activity.timestamp) {
          displayTime = formatSimpleTimestamp(activity.timestamp);
        }
        if (!displayTime) {
          displayTime = 'Recent activity';
        }
        
        return {
          status: activity.status,
          timestamp: displayTime,
          source: activity.source || 'manual',
          rawTimestamp: activity.timestamp || activity.formattedTime
        }
      } catch (error) {
        return {
          status: activity.status,
          timestamp: 'Recent activity',
          source: activity.source || 'manual',
          rawTimestamp: ''
        }
      }
    })
    
    // Check if we have new activities by comparing the latest timestamp
    const newLatestTimestamp = newActivities[0]?.timestamp || ''
    
    if (newLatestTimestamp !== currentLatestTimestamp) {
      motorActivities.value = newActivities
      console.log('New motor activities detected, updating list')
    }
    
  } catch (error) {
    console.error('Error fetching motor activities:', error)
  } finally {
    isLoadingActivities.value = false
  }
}

// FIXED: Manual toggle with Philippine Time
const confirmToggleWaterPump = async () => {
  try {
    isTogglingMotor.value = true
    const newStatus = !waterPumpActive.value
    
    const response = await api.post(API_ENDPOINTS.MOTOR_STATUS, {
      status: newStatus,
      source: 'manual'
    })
    
    waterPumpActive.value = newStatus
    window.showToast(`Motor turned ${newStatus ? 'ON' : 'OFF'} successfully`, 'success')
    
    // Add to local activities using the formatted time from response
    const newActivity = {
      status: newStatus,
      timestamp: response.data.formattedTime || 'Recent activity',
      source: 'manual'
    }
    
    motorActivities.value.unshift(newActivity)
    
    // Refresh data
    setTimeout(() => {
      fetchMotorStatus()
      fetchMotorActivities()
      if (!newStatus) fetchWateringSchedules()
    }, 1000)
    
  } catch (error) {
    console.error('Error toggling motor:', error)
    waterPumpActive.value = !newStatus
    window.showToast('Error toggling motor status', 'failed')
  } finally {
    isTogglingMotor.value = false
    showToggleConfirmationDialog.value = false
  }
}


const currentMonthName = computed(() => {
  return new Intl.DateTimeFormat('en-US', { month: 'long' }).format(currentDate.value)
})

const currentYear = computed(() => {
  return currentDate.value.getFullYear()
})

const calendarDays = computed(() => {
  const year = currentDate.value.getFullYear()
  const month = currentDate.value.getMonth()
  const today = new Date()
  today.setHours(0, 0, 0, 0)

  const firstDay = new Date(year, month, 1)
  const lastDay = new Date(year, month + 1, 0)

  const firstDayOfWeek = firstDay.getDay()

  const days = []

  const prevMonthLastDay = new Date(year, month, 0).getDate()
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const dayDate = new Date(year, month - 1, prevMonthLastDay - i)
    days.push({
      day: prevMonthLastDay - i,
      month: month - 1,
      year: month === 0 ? year - 1 : year,
      isCurrentMonth: false,
      isDisabled: true
    })
  }

 for (let i = 1; i <= lastDay.getDate(); i++) {
    const dayDate = new Date(year, month, i)
    const isPast = wateringMode.value === 'one-time' && dayDate < today
    days.push({
      day: i,
      month,
      year,
      isCurrentMonth: true,
      isDisabled: isPast,
      hasOneTimeSchedule: oneTimeScheduledDates.value.includes(dayDate.getTime())
    })
  }

  const remainingDays = 42 - days.length
  for (let i = 1; i <= remainingDays; i++) {
    const dayDate = new Date(year, month + 1, i)
    days.push({
      day: i,
      month: month + 1,
      year: month === 11 ? year + 1 : year,
      isCurrentMonth: false,
      isDisabled: false,
      hasOneTimeSchedule: oneTimeScheduledDates.value.includes(dayDate.getTime())
    })
  }

  return days
})

const prevMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() - 1,
    1
  )
}

const nextMonth = () => {
  currentDate.value = new Date(
    currentDate.value.getFullYear(),
    currentDate.value.getMonth() + 1,
    1
  )
}

const selectCalendarDate = (day) => {
  selectedDate.value = new Date(day.year, day.month, day.day)
}

const isSelectedDate = (day) => {
  const selected = selectedDate.value
  return day.day === selected.getDate() &&
         day.month === selected.getMonth() &&
         day.year === selected.getFullYear()
}

const isSelectedDateToday = computed(() => {
  if (!selectedDate.value) return false
  const today = new Date()
  return (
    selectedDate.value.getDate() === today.getDate() &&
    selectedDate.value.getMonth() === today.getMonth() &&
    selectedDate.value.getFullYear() === today.getFullYear()
  )
})

const isToday = (day) => {
  const today = new Date()
  return day.day === today.getDate() &&
         day.month === today.getMonth() &&
         day.year === today.getFullYear()
}

const isOneTimeToday = computed(() => {
  return wateringMode.value === 'one-time' && isSelectedDateToday.value
})

const incrementHour = () => {
  let hour = parseInt(wateringHour.value)
  hour = (hour + 1) % 24
  
  if (isOneTimeToday.value) {
    const currentHour = new Date().getHours()
    if (hour > currentHour) {
      wateringHour.value = hour
      updateAmPm()
    }
  } else {
    wateringHour.value = hour
    updateAmPm()
  }
}

const decrementHour = () => {
  let hour = parseInt(wateringHour.value)
  hour = (hour - 1 + 24) % 24
  
  if (isOneTimeToday.value) {
    const currentHour = new Date().getHours()
    if (hour >= currentHour) {
      wateringHour.value = hour
      updateAmPm()
    }
  } else {
    wateringHour.value = hour
    updateAmPm()
  }
}

const incrementMinute = () => {
  let minute = parseInt(wateringMinute.value)
  minute = (minute + 5) % 60
  
  if (isOneTimeToday.value) {
    const currentMinute = new Date().getMinutes()
    if (minute > currentMinute) {
      wateringMinute.value = minute
    }
  } else {
    wateringMinute.value = minute
  }
}

const decrementMinute = () => {
  let minute = parseInt(wateringMinute.value)
  minute = (minute - 5 + 60) % 60
  
  if (isOneTimeToday.value) {
    const currentMinute = new Date().getMinutes()
    if (minute >= currentMinute) {
      wateringMinute.value = minute
    }
  } else {
    wateringMinute.value = minute
  }
}

const updateAmPm = () => {
  isAm.value = wateringHour.value < 12 || wateringHour.value === 0
  if (wateringHour.value === 12) isAm.value = false
}

const setAmPm = (value) => {
  const currentHour24 = wateringHour.value

  if (value === 'AM') {
    if (currentHour24 >= 12) {
      wateringHour.value = currentHour24 - 12
    }
    isAm.value = true
  } else if (value === 'PM') {
    if (currentHour24 < 12) {
      wateringHour.value = currentHour24 + 12
    }
    isAm.value = false
  }
}

const validateHour = () => {
  let inputHour12 = parseInt(formattedHour.value)
  if (isNaN(inputHour12) || inputHour12 < 1) inputHour12 = 1
  if (inputHour12 > 12) inputHour12 = 12

  let hour24 = inputHour12
  if (isAm.value) {
    if (hour24 === 12) hour24 = 0
  } else {
    if (hour24 < 12) hour24 += 12
  }

  if (isOneTimeToday.value) {
    const currentHour = new Date().getHours()
    if (hour24 < currentHour) {
      hour24 = currentHour
    }
  }

  wateringHour.value = hour24
}

const validateMinute = () => {
  let minute = parseInt(formattedMinute.value)
  if (isNaN(minute) || minute < 0) minute = 0
  if (minute > 59) minute = 59

  if (isOneTimeToday.value) {
    const currentMinute = new Date().getMinutes()
    if (minute < currentMinute) {
      minute = currentMinute
    }
  }

  wateringMinute.value = minute
}

const formattedHour = computed({
  get: () => {
    let displayHour = wateringHour.value
    if (isAm.value) {
      if (displayHour === 0) displayHour = 12
    } else {
      if (displayHour > 12) displayHour -= 12
      else if (displayHour === 0) displayHour = 12
    }
    return displayHour.toString().padStart(2, '0')
  },
  set: (value) => {
    let inputHour12 = parseInt(value)
    if (!isNaN(inputHour12) && inputHour12 >= 1 && inputHour12 <= 12) {
      let hour24 = inputHour12
      if (isAm.value) {
        if (hour24 === 12) hour24 = 0
      } else {
        if (hour24 < 12) hour24 += 12
      }
      wateringHour.value = hour24
    }
  }
})

const formattedMinute = computed({
  get: () => wateringMinute.value.toString().padStart(2, '0'),
  set: (value) => {
    const minute = parseInt(value)
    if (!isNaN(minute) && minute >= 0 && minute <= 59) {
      wateringMinute.value = minute
    }
  }
})

const toggleWateringDay = (index) => {
  wateringDays.value[index] = !wateringDays.value[index]
}

const openScheduleModal = (index = null) => {
  if (index === null) {
    editingScheduleId.value = null
    editingScheduleMode.value = null
    resetScheduleForm()
  } else {
    editingScheduleId.value = savedSchedules.value[index].id
    editingScheduleMode.value = savedSchedules.value[index].mode
    loadScheduleData(index)
  }
  showScheduleModal.value = true
}

const loadScheduleData = (index) => {
  const schedule = savedSchedules.value[index]

  wateringMode.value = schedule.mode

  if (schedule.days && Array.isArray(schedule.days)) {
    wateringDays.value = [...schedule.days]
  } else {
    wateringDays.value = [false,false,false,false,false,false,false]
  }

  const scheduleDate = new Date(schedule.scheduledTime)
  wateringHour.value = scheduleDate.getHours()
  wateringMinute.value = scheduleDate.getMinutes()
  updateAmPm()

  wateringDuration.value = schedule.duration
  skipIfRain.value = schedule.skipIfRain || false
  notifyWatering.value = schedule.notifyWatering === undefined ? true : schedule.notifyWatering
  waterFlowRate.value = schedule.waterFlowRate || 'medium'

  if (schedule.mode === 'custom' && schedule.interval) {
    wateringInterval.value = schedule.interval.value
    wateringIntervalUnit.value = schedule.interval.unit
  }

  if (schedule.mode === 'one-time') {
    selectedDate.value = new Date(schedule.scheduledTime)
    currentDate.value = new Date(selectedDate.value)
  } else {
    selectedDate.value = new Date()
    currentDate.value = new Date()
  }
}

const resetScheduleForm = () => {
  wateringMode.value = 'weekly'
  wateringDays.value = [true, false, true, false, true, false, false]
  
  const now = new Date()
  let minutes = now.getMinutes()
  minutes = Math.ceil(minutes / 5) * 5
  if (minutes >= 60) {
    minutes = 0
    now.setHours(now.getHours() + 1)
  }
  
  wateringHour.value = now.getHours()
  wateringMinute.value = minutes
  wateringDuration.value = 20
  wateringInterval.value = 2
  wateringIntervalUnit.value = 'days'
  skipIfRain.value = false
  notifyWatering.value = true
  waterFlowRate.value = 'medium'
  selectedDate.value = new Date()
  currentDate.value = new Date()
  updateAmPm()
}

const closeScheduleModal = () => {
  showScheduleModal.value = false
  editingScheduleId.value = null
  editingScheduleMode.value = null
}

const increaseDuration = () => {
  if (wateringDuration.value < 120) {
    wateringDuration.value++
  }
}

const decreaseDuration = () => {
  if (wateringDuration.value > 1) {
    wateringDuration.value--
  }
}

const increaseInterval = () => {
  if (wateringInterval.value < 30) {
    wateringInterval.value++
  }
}

const decreaseInterval = () => {
  if (wateringInterval.value > 1) {
    wateringInterval.value--
  }
}

const editSchedule = (index) => {
  openScheduleModal(index)
}

const removeSchedule = (index) => {
  scheduleToDeleteIndex.value = index
  showDeleteConfirmation.value = true
}

const scheduleSummary = computed(() => {
  if (wateringMode.value === 'weekly') {
    const selectedDaysList = weekDays
      .filter((_, index) => wateringDays.value[index])
      .map(day => day.substring(0, 3))
      .join(', ')
    return `Every ${selectedDaysList || 'N/A'}`
  } else if (wateringMode.value === 'daily') {
    return 'Every day'
  } else if (wateringMode.value === 'custom') {
    return `Every ${wateringInterval.value} ${wateringIntervalUnit.value}`
  } else if (wateringMode.value === 'one-time') {
    return selectedDate.value.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric'
    })
  }
  return ''
})

const parseScheduleDateTime = (dateTimeStr) => {
  if (!dateTimeStr) return new Date()

  try {
    const parts = dateTimeStr.split(", ")
    if (parts.length >= 3) {
      const datePart = parts[0] + ', ' + parts[1]
      const timePart = parts[2]
      return new Date(datePart + ', ' + new Date().getFullYear() + ' ' + timePart)
    }
    return new Date(dateTimeStr)
  } catch (error) {
    console.error('Error parsing schedule dateTime:', error, dateTimeStr)
    return new Date()
  }
}

const parseActivityTimestamp = (timestamp) => {
  if (timestamp instanceof Date) {
    return timestamp
  }

  if (typeof timestamp !== 'string') {
    console.error('Invalid timestamp format:', timestamp)
    return new Date()
  }

  if (timestamp.includes(',')) {
    try {
      const dateParts = timestamp.split(', ')
      if (dateParts.length >= 2) {
        const fullDateStr = timestamp
        const date = new Date(fullDateStr)
        if (!isNaN(date.getTime())) {
          return date
        }

        const monthDayPart = dateParts[1]
        let timePart = ''
        if (dateParts.length > 2) {
          timePart = dateParts[2]
        }

        const monthDayMatch = monthDayPart.match(/([A-Za-z]+)\s+(\d+)/)
        if (monthDayMatch) {
          const monthName = monthDayMatch[1]
          const day = parseInt(monthDayMatch[2])
          const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
          const monthIndex = months.findIndex(m => m === monthName)

          if (monthIndex !== -1) {
            const currentYear = new Date().getFullYear()
            const newDate = new Date(currentYear, monthIndex, day)

            if (timePart) {
              const timeMatch = timePart.match(/(\d+):(\d+)\s+(AM|PM)/i)
              if (timeMatch) {
                let hours = parseInt(timeMatch[1])
                const minutes = parseInt(timeMatch[2])
                const ampm = timeMatch[3].toUpperCase()

                if (ampm === 'PM' && hours < 12) {
                  hours += 12
                } else if (ampm === 'AM' && hours === 12) {
                  hours = 0
                }

                newDate.setHours(hours, minutes, 0, 0)
              }
            }

            return newDate
          }
        }
      }
    } catch (error) {
      console.error('Error parsing timestamp:', error, timestamp)
    }
  }

  if (timestamp.startsWith('Today')) {
    const today = new Date()
    const timeStr = timestamp.split(', ')[1]
    const [hours, minutes] = timeStr.split(':')
    const isPM = timeStr.includes('PM')

    today.setHours(
      isPM && hours !== '12' ? parseInt(hours) + 12 : (hours === '12' && !isPM ? 0 : parseInt(hours)),
      parseInt(minutes),
      0,
      0
    )
    return today
  } else if (timestamp.startsWith('Yesterday')) {
    const yesterday = new Date()
    yesterday.setDate(yesterday.getDate() - 1)
    const timeStr = timestamp.split(', ')[1]
    const [hours, minutes] = timeStr.split(':')
    const isPM = timeStr.includes('PM')

    yesterday.setHours(
      isPM && hours !== '12' ? parseInt(hours) + 12 : (hours === '12' && !isPM ? 0 : parseInt(hours)),
      parseInt(minutes),
      0,
      0
    )
    return yesterday
  }

  console.warn('Could not parse timestamp, using current date as fallback:', timestamp)
  return new Date()
}

const getDayName = (dayIndex) => {
  const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
  return days[dayIndex] || ''
}

const timeDisplay = computed(() => {
  let hour12 = wateringHour.value % 12
  if (hour12 === 0) hour12 = 12
  const minute = wateringMinute.value.toString().padStart(2, '0')
  const ampm = isAm.value ? 'AM' : 'PM'
  return `${hour12.toString().padStart(2, '0')}:${minute} ${ampm}`
})

const upcomingSchedules = computed(() => {
  // Add dependency on currentRealTime to force recomputation
  const _ = currentRealTime.value
  
  return savedSchedules.value
    .filter(schedule => schedule.completed === false)
    .map(schedule => ({
      ...schedule,
      formattedDateTime: formatScheduleDateTime(schedule)
    }))
})

let unsubscribeFunctions = []

const fetchWateringSchedules = async () => {
  isLoadingSchedules.value = true
  try {
    const response = await api.get(API_ENDPOINTS.SCHEDULES)
    savedSchedules.value = response.data
    calculateNextWateringTime()
  } catch (error) {
    console.error('Error fetching watering schedules:', error)
    savedSchedules.value = []
  } finally {
    isLoadingSchedules.value = false
  }
}

const nextWateringTime = computed(() => {
  const _ = currentRealTime.value // Dependency to force recomputation
  
  if (savedSchedules.value.length === 0) {
    return 'No upcoming waterings'
  }

  // Get all upcoming schedules with their next occurrence time
  const upcoming = savedSchedules.value
    .filter(s => s.completed === false)
    .map(schedule => {
      let nextOccurrence
      
      if (schedule.mode === 'daily') {
        nextOccurrence = getNextDailyOccurrence(schedule.scheduledTime)
      } else if (schedule.mode === 'weekly') {
        nextOccurrence = getNextWeeklyOccurrence(schedule)
      } else { // one-time
        nextOccurrence = new Date(schedule.scheduledTime)
      }
      
      return {
        ...schedule,
        nextOccurrence: nextOccurrence.getTime(),
        nextOccurrenceDate: nextOccurrence
      }
    })
    .filter(s => s.nextOccurrence >= currentRealTime.value.getTime())
    .sort((a, b) => a.nextOccurrence - b.nextOccurrence)

  if (upcoming.length > 0) {
    // Find the schedule with the closest next occurrence
    const closestSchedule = upcoming.reduce((prev, curr) => 
      (prev.nextOccurrence < curr.nextOccurrence) ? prev : curr
    )
    
    return closestSchedule.nextOccurrenceDate.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })
  }
  
  return 'No upcoming waterings'
})

const calculateNextWateringTime = () => {
  isLoadingNextWatering.value = true
  const now = new Date().getTime()

  const upcoming = savedSchedules.value
    .filter(s => s.completed === false)
    .map(schedule => {
      if (schedule.mode === 'daily') {
        return {
          ...schedule,
          nextOccurrence: getNextDailyOccurrence(schedule.scheduledTime).getTime()
        }
      }
      return {
        ...schedule,
        nextOccurrence: schedule.scheduledTime
      }
    })
    .filter(s => s.nextOccurrence >= now)
    .sort((a, b) => a.nextOccurrence - b.nextOccurrence)

  if (upcoming.length > 0) {
    const nextSchedule = upcoming[0]
    const nextDate = new Date(nextSchedule.nextOccurrence)
    nextWateringTime.value = nextDate.toLocaleString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    })
  } else {
    nextWateringTime.value = 'No upcoming waterings'
  }
  isLoadingNextWatering.value = false
}

const confirmDeleteSchedule = async () => {
  if (scheduleToDeleteIndex.value === null) return
  
  isDeletingSchedule.value = true
  try {
    // Get the schedule ID from the index
    const schedule = savedSchedules.value[scheduleToDeleteIndex.value]
    const scheduleId = schedule.id
    
    await api.delete(`${API_ENDPOINTS.SCHEDULES}/${scheduleId}`)
    window.showToast('Schedule deleted successfully', 'success')
    
    // Refresh schedules
    await fetchWateringSchedules()
  } catch (error) {
    console.error('Error deleting schedule:', error)
    
    if (error.response?.status === 404) {
      window.showToast('Schedule not found or already deleted', 'warning')
    } else {
      window.showToast('Error deleting schedule', 'failed')
    }
  } finally {
    showDeleteConfirmation.value = false
    scheduleToDeleteIndex.value = null
    isDeletingSchedule.value = false
  }
}

const saveWateringSchedule = async () => {
  isLoading.value = true
  
  try {
    // Check for duplicate schedule first
    const scheduledTime = calculateScheduledTime()
    const newScheduleDetails = {
      mode: wateringMode.value,
      hour: wateringHour.value,
      minute: wateringMinute.value,
      duration: wateringDuration.value,
      date: selectedDate.value,
      days: wateringMode.value === 'weekly' ? [...wateringDays.value] : []
    }

    if (isDuplicateSchedule(newScheduleDetails)) {
      window.showToast('A schedule already exists at this time. Please choose a different time.', 'warning')
      isLoading.value = false
      return
    }

    // Then check soil moisture
    const moistureResponse = await api.get(API_ENDPOINTS.SOIL_MOISTURE)
    soilMoistureForSchedule.value = moistureResponse.data.moisture

    if (soilMoistureForSchedule.value !== null && soilMoistureForSchedule.value >= 50) {
      showScheduleConfirmationDialog.value = true
      return
    }
    
    await actuallySaveSchedule()
  } catch (error) {
    console.error("Error in saveWateringSchedule:", error)
    const action = editingScheduleId.value ? 'update' : 'add'
    window.showToast(`Failed to ${action} schedule. Please try again.`, 'failed')
    isLoading.value = false
  }
}

const cancelScheduleConfirmation = () => {
  showScheduleConfirmationDialog.value = false
  isLoading.value = false
  const action = editingScheduleId.value ? 'update' : 'creation'
  window.showToast(`Schedule ${action} canceled due to high soil moisture`, 'info')
}

const proceedWithScheduleSave = async () => {
  showScheduleConfirmationDialog.value = false
  await actuallySaveSchedule()
}

const calculateScheduledTime = () => {
  if (wateringMode.value === 'one-time') {
    // For one-time schedules, create a specific datetime
    const selectedDateTime = new Date(
      selectedDate.value.getFullYear(),
      selectedDate.value.getMonth(),
      selectedDate.value.getDate(),
      wateringHour.value,
      wateringMinute.value,
      0,
      0
    )
    return selectedDateTime.getTime() // Return timestamp in milliseconds
  } else {
    // For daily and weekly schedules, calculate milliseconds since midnight
    return (wateringHour.value * 60 * 60 * 1000) + (wateringMinute.value * 60 * 1000)
  }
}

const actuallySaveSchedule = async () => {
  try {
    const scheduledTime = calculateScheduledTime()
    
    // Format dateTime for display
    let dateTimeDisplay = ''
    if (wateringMode.value === 'one-time') {
      const date = new Date(selectedDate.value)
      dateTimeDisplay = date.toLocaleString('en-US', {
        weekday: 'short',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true
      })
    } else {
      // For daily/weekly: format time only (HH:MM AM/PM)
      let displayHour = wateringHour.value % 12
      if (displayHour === 0) displayHour = 12
      const amPm = wateringHour.value >= 12 ? 'PM' : 'AM'
      dateTimeDisplay = `${displayHour.toString().padStart(2, '0')}:${wateringMinute.value.toString().padStart(2, '0')} ${amPm}`
    }
    
    const scheduleData = {
      mode: wateringMode.value,
      hour: wateringHour.value,
      minute: wateringMinute.value,
      duration: wateringDuration.value,
      days: wateringMode.value === 'weekly' ? [...wateringDays.value] : [],
      skipIfRain: skipIfRain.value,
      notifyWatering: notifyWatering.value,
      waterFlowRate: waterFlowRate.value,
      scheduledTime: scheduledTime,
      dateTime: dateTimeDisplay
    }

    if (editingScheduleId.value) {
      // Use PUT for updates
      await api.put(`${API_ENDPOINTS.SCHEDULES}/${editingScheduleId.value}`, scheduleData)
      window.showToast('Schedule updated successfully', 'success')
    } else {
      // Use POST for new schedules
      await api.post(API_ENDPOINTS.SCHEDULES, scheduleData)
      window.showToast('New schedule saved successfully', 'success')
    }

    closeScheduleModal()
    editingScheduleId.value = null
    await fetchWateringSchedules()
  } catch (error) {
    console.error('Error saving schedule:', error)
    const action = editingScheduleId.value ? 'update' : 'add'
    
    if (error.response?.status === 400 && error.response?.data?.detail?.includes('conflicting')) {
      window.showToast('A conflicting schedule already exists at this time', 'warning')
    } else {
      window.showToast(`Failed to ${action} schedule. Please try again.`, 'failed')
    }
  } finally {
    isLoading.value = false
  }
}

const testBackendConnection = async () => {
  try {
    const response = await api.get('/health')
    console.log('Backend connection successful:', response.data)
    return true
  } catch (error) {
    console.error('Backend connection failed:', error)
    window.showToast('Cannot connect to server. Please check if the backend is running.', 'failed')
    return false
  }
}

watch(() => wateringHour.value, updateAmPm, { immediate: true })
watch(() => isAm.value, () => {
  let currentHour24 = wateringHour.value
  if (isAm.value) {
    if (currentHour24 >= 12) wateringHour.value = currentHour24 - 12
  } else {
    if (currentHour24 < 12) wateringHour.value = currentHour24 + 12
  }
})

const fetchHistory = async () => {
  isLoadingHistory.value = true
  try {
    const response = await api.get(API_ENDPOINTS.SCHEDULE_HISTORY)
    pastSchedules.value = response.data
  } catch (error) {
    console.error('Error fetching schedule history:', error)
    pastSchedules.value = []
  } finally {
    isLoadingHistory.value = false
  }
}

const formatHistoryItem = (schedule) => {
  // Add dependency on forceUpdateCount to trigger recalculations
  const _ = forceUpdateCount;
  
  // For ALL schedule types (including daily), use the completedAt timestamp for history display
  const completedDate = new Date(schedule.completedAt);
  const formattedDate = completedDate.toLocaleString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  let scheduleInfo = '';
  if (schedule.mode === 'weekly') {
    const dayName = getDayName(schedule.dayOfWeek);
    scheduleInfo = `Weekly (${dayName})`;
  } else if (schedule.mode === 'daily') {
    scheduleInfo = 'Daily';
  } else {
    scheduleInfo = 'One-time';
  }

  return {
    ...schedule,
    dateTime: formattedDate,
    mode: schedule.mode,
    duration: schedule.duration,
    skipIfRain: schedule.skipIfRain || false,
    notifyWatering: schedule.notifyWatering || false,
    scheduleInfo,
    durationText: `${schedule.duration} min`,
    flowRateText: schedule.waterFlowRate?.toUpperCase() || 'MEDIUM'
  };
};
onMounted(async () => {
  // Test backend connection first
  const isConnected = await testBackendConnection()
  
  if (isConnected) {
    // Load all data
    await Promise.all([
      fetchMotorStatus(),
      fetchMotorActivities(),
      fetchWateringSchedules(),
      fetchHistory()
    ])

    setInterval(() => {
      fetchWateringSchedules()
    }, 1000)
    
    // Start real-time polling for motor status
    startMotorStatusPolling()
    startMotorActivitiesPolling()
    
    // Set up polling for other data (less frequent)
    setInterval(() => {
      fetchWateringSchedules()
    }, 30000)
  }
  
  // Set up history filters
  const today = new Date()
  const thirtyDaysAgo = new Date()
  thirtyDaysAgo.setDate(today.getDate() - 30)
  
  historyFilters.value = {
    startDate: thirtyDaysAgo.toISOString().split('T')[0],
    endDate: today.toISOString().split('T')[0],
    scheduleType: 'all',
    duration: 'all'
  }
  
  resetScheduleForm()
})

// Clean up polling on unmount
onUnmounted(() => {
  stopMotorStatusPolling()
  stopMotorActivitiesPolling()
})

</script>

<style>
/* Keep your existing styles */
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Modal animations */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

/* Toast animations */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* Power button styles */
.glass-button {
  backdrop-filter: blur(4px);
  transform: translateZ(0);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 
    0 10px 25px -5px rgba(0, 0, 0, 0.1), 
    0 10px 10px -5px rgba(0, 0, 0, 0.04),
    inset 0 -5px 10px -5px rgba(0, 0, 0, 0.1);
}

.active-button {
  box-shadow: 
    0 0 0 2px rgba(34, 197, 94, 0.5),
    0 0 20px 5px rgba(34, 197, 94, 0.5),
    0 0 0 4px rgba(34, 197, 94, 0.3),
    inset 0 -5px 15px -5px rgba(0, 0, 0, 0.2);
}

.inactive-button {
  box-shadow: 
    0 0 0 2px rgba(249, 115, 22, 0.3),
    0 0 15px 2px rgba(249, 115, 22, 0.2),
    0 0 0 4px rgba(249, 115, 22, 0.1),
    inset 0 -5px 15px -5px rgba(0, 0, 0, 0.2);
}

/* Power icon animations */
.power-icon-on {
  filter: drop-shadow(0 0 8px rgba(255, 255, 255, 0.8));
  animation: glow 2s ease-in-out infinite alternate;
}

.power-icon-off {
  filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.5));
}

@keyframes glow {
  from {
    filter: drop-shadow(0 0 5px rgba(255, 255, 255, 0.8));
  }
  to {
    filter: drop-shadow(0 0 15px rgba(255, 255, 255, 0.9));
  }
}

/* Pulse animation for active button */
.pulse-animation {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0% {
    opacity: 0;
  }
  50% {
    opacity: 0.1;
  }
  100% {
    opacity: 0;
  }
}
@media (max-width: 767px) {
  .filters-section {
    transition: all 0.3s ease;
    overflow: hidden;
  }
}
</style>
