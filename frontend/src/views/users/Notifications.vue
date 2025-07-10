<template>
  <div class="h-screen flex bg-gradient-to-br from-green-50 to-emerald-100 font-poppins overflow-hidden">
    
    <!-- Loading Overlay -->
    <div v-if="isLoading" class="fixed inset-0 bg-black/20 backdrop-blur-sm z-50 flex items-center justify-center">
      <div class="bg-white rounded-2xl shadow-2xl border-2 border-transparent bg-gradient-to-r from-yellow-200 via-emerald-200 to-green-300 p-0.5 max-w-md mx-4">
        <div class="bg-white rounded-2xl p-8 text-center">
          <!-- Notification Icon Animation -->
          <div class="mb-6 relative">
            <div class="w-20 h-20 mx-auto bg-gradient-to-br from-emerald-400 to-green-500 rounded-2xl flex items-center justify-center shadow-lg">
              <Bell class="h-10 w-10 text-white animate-bounce" />
            </div>
            <!-- Notification Badge -->
            <div class="absolute -top-1 -right-1 w-6 h-6 bg-red-500 rounded-full flex items-center justify-center">
              <span class="text-white text-xs font-bold">!</span>
            </div>
          </div>
          
          <!-- Loading Dots -->
          <div class="flex justify-center space-x-2 mb-6">
            <div 
              v-for="i in 5" 
              :key="i"
              class="w-2 h-2 rounded-full transition-all duration-300"
              :class="loadingDotIndex === i - 1 ? 'bg-emerald-500 scale-125' : 'bg-gray-300'"
            ></div>
          </div>
          
          <!-- Loading Text -->
          <h3 class="text-xl font-semibold text-gray-800 mb-2">Loading Notifications</h3>
          <p class="text-gray-600 text-sm">Please wait while we fetch your latest alerts and updates</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="flex-1 flex flex-col h-screen pt-32">
      <!-- Container Wrapper -->
      <div class="flex-1 w-full px-4 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
        <!-- Main Container - Enhanced Design -->
        <div class="bg-white rounded-2xl shadow-md border border-emerald-100 h-[calc(100vh-140px)] overflow-hidden">
          <!-- Content Wrapper -->
          <div class="flex flex-col h-full">
            <!-- Enhanced Header Section -->
            <div class="p-5 border-b border-emerald-100 bg-gradient-to-r from-emerald-50 to-white">
              <!-- Header with improved layout -->
              <div class="flex items-center justify-between mb-5">
                <div class="flex items-center space-x-3">
                  <div class="p-2.5 bg-emerald-500 rounded-xl shadow-sm">
                    <Bell class="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <h1 class="text-xl font-semibold text-gray-800">Notifications</h1>
                    <p class="text-sm text-gray-500">Stay updated with your latest alerts and updates</p>
                  </div>
                </div>
                <div class="flex items-center space-x-2">
                  <button 
                    @click="markAllAsRead"
                    :disabled="isLoading"
                    class="flex items-center px-4 py-2 bg-emerald-500 hover:bg-emerald-600 text-white rounded-lg text-sm font-medium transition-colors shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    <Check class="h-4 w-4 mr-1.5" />
                    Mark all read
                  </button>
                  <button 
                    @click="goBack"
                    class="flex items-center px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg text-sm font-medium transition-colors"
                  >
                    <ArrowLeft class="h-4 w-4 mr-1.5" />
                    Back
                  </button>
                </div>
              </div>

              <!-- Enhanced Filters and Search -->
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <div class="flex flex-wrap items-center gap-2">
                  <button 
                    v-for="filter in filters" 
                    :key="filter.value"
                    @click="activeFilter = filter.value"
                    :disabled="isLoading"
                    :class="[
                      'px-3 py-1.5 text-sm font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed',
                      activeFilter === filter.value 
                        ? 'bg-emerald-500 text-white shadow-sm' 
                        : 'bg-white text-gray-700 hover:bg-gray-100 border border-gray-200'
                    ]"
                  >
                    {{ filter.label }}
                  </button>
                </div>
                
                <div class="relative w-full sm:w-64">
                  <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <Search class="h-4 w-4 text-gray-400" />
                  </div>
                  <input 
                    type="text"
                    v-model="searchQuery"
                    :disabled="isLoading"
                    placeholder="Search notifications..."
                    class="w-full pl-10 pr-4 py-2 text-sm bg-white border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 shadow-sm disabled:opacity-50 disabled:cursor-not-allowed"
                  />
                </div>
              </div>
            </div>

            <!-- Scrollable Notifications Content with fixed spacing -->
            <div class="flex-1 overflow-y-auto notification-scroll">
              <!-- Empty State -->
              <div v-if="!isLoading && filteredNotifications.length === 0" class="py-16 flex flex-col items-center justify-center">
                <div class="bg-gray-100 p-4 rounded-full mb-4">
                  <BellOff class="h-8 w-8 text-gray-400" />
                </div>
                <h3 class="text-lg font-medium text-gray-900 mb-1">No notifications</h3>
                <p class="text-sm text-gray-500 text-center">
                  {{ searchQuery ? 'No results found for your search.' : 'You don\'t have any notifications yet.' }}
                </p>
              </div>

              <!-- Notifications - Enhanced Design with Consistent Spacing -->
              <div v-else-if="!isLoading" class="divide-y divide-gray-100">
                <!-- Today's Notifications -->
                <div v-if="todayNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-emerald-50 px-3 py-2 rounded-lg">
                    <CalendarClock class="h-4 w-4 text-emerald-600 mr-2" />
                    <span class="text-sm font-medium text-emerald-700">Today</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in todayNotifications" 
                      :key="notification.id"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm"
                      :class="{ 'bg-blue-50/30 border-blue-200': !notification.read }"
                    >
                      <div class="flex items-start gap-3">
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationTypeClass(notification.type).bgColor"
                        >
                          <component 
                            :is="getNotificationTypeClass(notification.type).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2">{{ notification.message }}</p>
                          <div class="flex items-center gap-2">
                            <span 
                              class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                              :class="getNotificationTypeClass(notification.type).badgeColor"
                            >
                              {{ notification.type }}
                            </span>
                            <div v-if="!notification.read" class="flex items-center text-blue-600 text-xs font-medium">
                              <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                              Unread
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Yesterday's Notifications -->
                <div v-if="yesterdayNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-orange-50 px-3 py-2 rounded-lg">
                    <CalendarDays class="h-4 w-4 text-orange-600 mr-2" />
                    <span class="text-sm font-medium text-orange-700">Yesterday</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in yesterdayNotifications" 
                      :key="notification.id"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm"
                      :class="{ 'bg-blue-50/30 border-blue-200': !notification.read }"
                    >
                      <div class="flex items-start gap-3">
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationTypeClass(notification.type).bgColor"
                        >
                          <component 
                            :is="getNotificationTypeClass(notification.type).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2">{{ notification.message }}</p>
                          <div class="flex items-center gap-2">
                            <span 
                              class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                              :class="getNotificationTypeClass(notification.type).badgeColor"
                            >
                              {{ notification.type }}
                            </span>
                            <div v-if="!notification.read" class="flex items-center text-blue-600 text-xs font-medium">
                              <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                              Unread
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- A Few Days Ago Notifications (2-6 days) -->
                <div v-if="fewDaysAgoNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-blue-50 px-3 py-2 rounded-lg">
                    <CalendarDays class="h-4 w-4 text-blue-600 mr-2" />
                    <span class="text-sm font-medium text-blue-700">A few days ago</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in fewDaysAgoNotifications" 
                      :key="notification.id"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm"
                      :class="{ 'bg-blue-50/30 border-blue-200': !notification.read }"
                    >
                      <div class="flex items-start gap-3">
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationTypeClass(notification.type).bgColor"
                        >
                          <component 
                            :is="getNotificationTypeClass(notification.type).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2">{{ notification.message }}</p>
                          <div class="flex items-center gap-2">
                            <span 
                              class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                              :class="getNotificationTypeClass(notification.type).badgeColor"
                            >
                              {{ notification.type }}
                            </span>
                            <div v-if="!notification.read" class="flex items-center text-blue-600 text-xs font-medium">
                              <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                              Unread
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- A Week Ago Notifications (7-13 days) -->
                <div v-if="weekAgoNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-purple-50 px-3 py-2 rounded-lg">
                    <History class="h-4 w-4 text-purple-600 mr-2" />
                    <span class="text-sm font-medium text-purple-700">A week ago</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in weekAgoNotifications" 
                      :key="notification.id"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm"
                      :class="{ 'bg-blue-50/30 border-blue-200': !notification.read }"
                    >
                      <div class="flex items-start gap-3">
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationTypeClass(notification.type).bgColor"
                        >
                          <component 
                            :is="getNotificationTypeClass(notification.type).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2">{{ notification.message }}</p>
                          <div class="flex items-center gap-2">
                            <span 
                              class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                              :class="getNotificationTypeClass(notification.type).badgeColor"
                            >
                              {{ notification.type }}
                            </span>
                            <div v-if="!notification.read" class="flex items-center text-blue-600 text-xs font-medium">
                              <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                              Unread
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- A Few Weeks Ago Notifications (14-29 days) -->
                <div v-if="fewWeeksAgoNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-indigo-50 px-3 py-2 rounded-lg">
                    <History class="h-4 w-4 text-indigo-600 mr-2" />
                    <span class="text-sm font-medium text-indigo-700">A few weeks ago</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in fewWeeksAgoNotifications" 
                      :key="notification.id"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm"
                      :class="{ 'bg-blue-50/30 border-blue-200': !notification.read }"
                    >
                      <div class="flex items-start gap-3">
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationTypeClass(notification.type).bgColor"
                        >
                          <component 
                            :is="getNotificationTypeClass(notification.type).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2">{{ notification.message }}</p>
                          <div class="flex items-center gap-2">
                            <span 
                              class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                              :class="getNotificationTypeClass(notification.type).badgeColor"
                            >
                              {{ notification.type }}
                            </span>
                            <div v-if="!notification.read" class="flex items-center text-blue-600 text-xs font-medium">
                              <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                              Unread
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- A Month Ago Notifications (30+ days) -->
                <div v-if="monthAgoNotifications.length > 0" class="px-5 py-4">
                  <div class="flex items-center mb-3 bg-gray-50 px-3 py-2 rounded-lg">
                    <History class="h-4 w-4 text-gray-600 mr-2" />
                    <span class="text-sm font-medium text-gray-700">A month ago</span>
                  </div>
                  <div class="space-y-2.5">
                    <div 
                      v-for="notification in monthAgoNotifications" 
                      :key="notification.id"
                      class="group p-3 rounded-xl border border-gray-100 hover:border-emerald-200 bg-white hover:bg-gray-50/50 transition-all duration-200 shadow-sm"
                      :class="{ 'bg-blue-50/30 border-blue-200': !notification.read }"
                    >
                      <div class="flex items-start gap-3">
                        <div 
                          class="flex-shrink-0 w-8 h-8 rounded-lg flex items-center justify-center shadow-sm"
                          :class="getNotificationTypeClass(notification.type).bgColor"
                        >
                          <component 
                            :is="getNotificationTypeClass(notification.type).icon" 
                            class="h-4 w-4 text-white" 
                          />
                        </div>
                        <div class="flex-1 min-w-0">
                          <div class="flex items-start justify-between mb-1">
                            <h3 class="text-sm font-medium text-gray-900 line-clamp-1">{{ notification.title }}</h3>
                            <span class="text-xs text-gray-500 whitespace-nowrap ml-3 bg-gray-50 px-1.5 py-0.5 rounded">{{ formatTime(notification.time) }}</span>
                          </div>
                          <p class="text-sm text-gray-600 mb-2 line-clamp-2">{{ notification.message }}</p>
                          <div class="flex items-center gap-2">
                            <span 
                              class="inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium"
                              :class="getNotificationTypeClass(notification.type).badgeColor"
                            >
                              {{ notification.type }}
                            </span>
                            <div v-if="!notification.read" class="flex items-center text-blue-600 text-xs font-medium">
                              <div class="h-1.5 w-1.5 rounded-full bg-blue-500 mr-1"></div>
                              Unread
                            </div>
                          </div>
                        </div>
                        <div class="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                          <button 
                            v-if="!notification.read"
                            @click.stop="markAsRead(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-emerald-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Mark as read"
                          >
                            <Check class="h-4 w-4" />
                          </button>
                          <button 
                            @click.stop="deleteNotification(notification.id)"
                            class="p-1.5 text-gray-400 hover:text-red-500 hover:bg-gray-100 rounded-lg transition-colors"
                            title="Delete"
                          >
                            <Trash2 class="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- No notifications in current view -->
                <div v-if="paginatedNotifications.length === 0 && filteredNotifications.length > 0" class="px-5 py-12 text-center">
                  <Bell class="h-10 w-10 text-gray-300 mx-auto mb-3" />
                  <p class="text-gray-500">No notifications on this page</p>
                  <button 
                    @click="currentPage = 1"
                    class="mt-3 text-sm text-emerald-600 hover:text-emerald-700"
                  >
                    Go to first page
                  </button>
                </div>
              </div>
            </div>

            <!-- Enhanced Pagination Footer with Items Per Page Selector -->
            <div class="px-5 py-4 border-t border-gray-100 bg-gradient-to-r from-white to-emerald-50/30">
              <div class="flex flex-col sm:flex-row items-center justify-between gap-4">
                <div class="flex items-center gap-3">
                  <div class="flex items-center">
                    <span class="text-sm text-gray-600 mr-2">Show</span>
                    <select 
                      v-model="itemsPerPage" 
                      @change="handleItemsPerPageChange"
                      :disabled="isLoading"
                      class="bg-white border border-gray-200 text-gray-700 rounded-lg px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-emerald-500/20 focus:border-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      <option v-for="option in itemsPerPageOptions" :key="option" :value="option">
                        {{ option }}
                      </option>
                    </select>
                    <span class="text-sm text-gray-600 ml-2">per page</span>
                  </div>
                  
                  <div class="hidden sm:flex items-center">
                    <span class="text-sm text-gray-600 mr-2">|</span>
                    <span class="text-sm text-gray-600">
                      Showing <span class="font-medium">{{ (currentPage - 1) * itemsPerPage + 1 }}-{{ Math.min(currentPage * itemsPerPage, filteredNotifications.length) }}</span> of <span class="font-medium">{{ filteredNotifications.length }}</span>
                    </span>
                  </div>
                </div>
                
                <!-- Smart Pagination with Enhanced Design -->
                <div class="flex items-center gap-2">
                  <button 
                    @click="prevPage"
                    :disabled="currentPage === 1 || isLoading"
                    class="inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium transition-colors rounded-lg
                      disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                      enabled:text-gray-700 enabled:hover:text-emerald-600 enabled:hover:bg-emerald-50 enabled:border enabled:border-gray-200"
                  >
                    <ChevronLeft class="w-4 h-4 mr-1" />
                    Prev
                  </button>

                  <div class="flex items-center gap-1">
                    <button
                      v-for="page in displayedPages"
                      :key="page"
                      @click="goToPage(page)"
                      :disabled="isLoading"
                      :class="[
                        'relative inline-flex items-center justify-center w-8 h-8 text-sm transition-colors rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed',
                        page === currentPage
                          ? 'text-white bg-emerald-500 shadow-sm'
                          : page === '...'
                            ? 'cursor-default text-gray-400'
                            : 'text-gray-700 hover:text-emerald-600 hover:bg-emerald-50 border border-gray-200'
                      ]"
                    >
                      {{ page }}
                    </button>
                  </div>

                  <button 
                    @click="nextPage"
                    :disabled="currentPage >= totalPages || totalPages === 0 || isLoading"
                    class="inline-flex items-center justify-center px-3 py-1.5 text-sm font-medium transition-colors rounded-lg
                      disabled:opacity-50 disabled:cursor-not-allowed disabled:text-gray-400
                      enabled:text-gray-700 enabled:hover:text-emerald-600 enabled:hover:bg-emerald-50 enabled:border enabled:border-gray-200"
                  >
                    Next
                    <ChevronRight class="w-4 h-4 ml-1" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    <Settings />
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { eventBus } from '../../eventBus'
import {
  Bell, BellOff, Check, ArrowLeft, Search, ChevronLeft, ChevronRight,
  AlertTriangle, Info, AlertCircle, Droplet, Leaf, BarChart, Cog, Trash2,
  CalendarClock, CalendarDays, History
} from 'lucide-vue-next'
import Sidebar from '../layout/Sidebar.vue'
import Settings from '../layout/Settings.vue'
import {
  getFirestore,
  collection,
  getDocs,
  query,
  orderBy,
  doc,
  updateDoc,
  deleteDoc
} from 'firebase/firestore'
import { getCurrentInstance } from 'vue'

// Firestore DB reference
const db = getFirestore()

// Loading state
const isLoading = ref(true)
const loadingDotIndex = ref(0)
let loadingInterval = null

// Filters
const filters = [
  { label: 'All', value: 'all' },
  { label: 'Unread', value: 'unread' },
  { label: 'System', value: 'system' },
  { label: 'Alerts', value: 'alert' },
  { label: 'Data', value: 'data' }
]

const activeFilter = ref('all')
const searchQuery = ref('')
const currentPage = ref(1)

// Items per page options and default value
const itemsPerPageOptions = [4, 10, 15, 20, 25, 30]
const itemsPerPage = ref(4) // Default is 4

// Store user preference in localStorage
const loadUserPreferences = () => {
  try {
    const savedItemsPerPage = localStorage.getItem('notificationsPerPage')
    if (savedItemsPerPage) {
      const parsedValue = parseInt(savedItemsPerPage)
      if (itemsPerPageOptions.includes(parsedValue)) {
        itemsPerPage.value = parsedValue
      }
    }
  } catch (error) {
    console.error('Error loading user preferences:', error)
  }
}

const saveUserPreferences = () => {
  try {
    localStorage.setItem('notificationsPerPage', itemsPerPage.value.toString())
  } catch (error) {
    console.error('Error saving user preferences:', error)
  }
}

const handleItemsPerPageChange = () => {
  currentPage.value = 1 // Reset to first page when changing items per page
  saveUserPreferences() // Save user preference
}

const notifications = ref([])
const NOTIF_COLLECTION = "notifications"

// Loading animation
const startLoadingAnimation = () => {
  loadingInterval = setInterval(() => {
    loadingDotIndex.value = (loadingDotIndex.value + 1) % 5
  }, 300)
}

const stopLoadingAnimation = () => {
  if (loadingInterval) {
    clearInterval(loadingInterval)
    loadingInterval = null
  }
}

// Enhanced Back Navigation Function
const goBack = () => {
  try {
    // Check if there's history to go back to
    if (window.history.length > 1) {
      // Use Vue Router's go method to go back in history
      if (window.history.state && window.history.state.back) {
        window.history.back()
      } else {
        // Fallback: Use Vue Router's go method
        const router = getCurrentInstance()?.appContext.app.config.globalProperties.$router
        if (router) {
          router.go(-1)
        } else {
          // Final fallback: Use browser's native back
          window.history.back()
        }
      }
    } else {
      // If no history, fallback to dashboard
      const router = getCurrentInstance()?.appContext.app.config.globalProperties.$router
      if (router) {
        router.push('/dashboard')
      } else {
        // If router is not available, try to navigate using window.location
        window.location.href = '/dashboard'
      }
    }
  } catch (error) {
    console.error('Error navigating back:', error)
    // Fallback to dashboard on any error
    try {
      const router = getCurrentInstance()?.appContext.app.config.globalProperties.$router
      if (router) {
        router.push('/dashboard')
      } else {
        window.location.href = '/dashboard'
      }
    } catch (fallbackError) {
      console.error('Fallback navigation also failed:', fallbackError)
    }
  }
}

// Alternative simpler back function using router
const { $router } = getCurrentInstance()?.appContext.app.config.globalProperties || {}

const goBackSimple = () => {
  try {
    // Try to go back in browser history
    if ($router) {
      $router.go(-1)
    } else {
      window.history.back()
    }
  } catch (error) {
    console.error('Error going back:', error)
    // Fallback to dashboard
    if ($router) {
      $router.push('/dashboard')
    } else {
      window.location.href = '/dashboard'
    }
  }
}

// Use the simpler version for better compatibility
const goBackFinal = () => {
  // Check if we can go back in history
  if (window.history.length > 1) {
    window.history.back()
  } else {
    // If no history, redirect to dashboard
    if ($router) {
      $router.push('/dashboard')
    } else {
      window.location.href = '/dashboard'
    }
  }
}

// Fetch notifications from Firebase
const fetchNotifications = async () => {
  try {
    isLoading.value = true
    startLoadingAnimation()
    
    // Add minimum loading time for better UX (1.5 seconds)
    const [notificationsData] = await Promise.all([
      (async () => {
        const q = query(collection(db, 'notifications'), orderBy('timestamp', 'desc'))
        const snapshot = await getDocs(q)
        return snapshot.docs.map(doc => {
          const data = doc.data()
          const rawTimestamp = data.timestamp
          const parsedTime = rawTimestamp?.toDate?.() ?? null

          return {
            id: doc.id,
            ...data,
            time: parsedTime
          }
        })
      })(),
      new Promise(resolve => setTimeout(resolve, 1500)) // Minimum loading time
    ])

    notifications.value = notificationsData
    console.log('Fetched notifications:', notifications.value)
  } catch (error) {
    console.error('Failed to fetch notifications:', error)
  } finally {
    stopLoadingAnimation()
    isLoading.value = false
  }
}

onMounted(() => {
  loadUserPreferences() // Load user preferences on mount
  fetchNotifications()
  eventBus.on('notification-saved-success', fetchNotifications)
})

onUnmounted(() => {
  stopLoadingAnimation()
})

// Computed: Filtered notifications
const filteredNotifications = computed(() => {
  let result = [...notifications.value]

  if (activeFilter.value === 'unread') {
    result = result.filter(n => !n.read)
  } else if (activeFilter.value === 'system') {
    result = result.filter(n => n.type === 'system')
  } else if (activeFilter.value === 'alert') {
    result = result.filter(n => ['warning', 'critical'].includes(n.severity))
  } else if (activeFilter.value === 'data') {
    result = result.filter(n => n.type === 'data')
  }

  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(n =>
      n.title?.toLowerCase().includes(query) ||
      n.message?.toLowerCase().includes(query)
    )
  }

  return result
})

// Smart Pagination logic
const totalPages = computed(() =>
  Math.ceil(filteredNotifications.value.length / itemsPerPage.value) || 1
)

const paginatedNotifications = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value
  return filteredNotifications.value.slice(start, start + itemsPerPage.value)
})

// Smart pagination display logic
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

// Pagination methods
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

const goToPage = (page) => {
  if (typeof page === 'number') {
    currentPage.value = page
  }
}

watch([activeFilter, searchQuery], () => {
  currentPage.value = 1
})

// Enhanced date comparison helpers
const isSameDay = (dateA, dateB) => {
  return (
    dateA?.getFullYear() === dateB.getFullYear() &&
    dateA?.getMonth() === dateB.getMonth() &&
    dateA?.getDate() === dateB.getDate()
  )
}

const isToday = (date) => {
  if (!date) return false
  const today = new Date()
  return isSameDay(date, today)
}

const isYesterday = (date) => {
  if (!date) return false
  const yesterday = new Date()
  yesterday.setDate(yesterday.getDate() - 1)
  return isSameDay(date, yesterday)
}

const getDaysAgo = (date) => {
  if (!date) return 0
  const now = new Date()
  const diffTime = Math.abs(now - new Date(date))
  return Math.ceil(diffTime / (1000 * 60 * 60 * 24))
}

// Enhanced notification grouping by time periods
const todayNotifications = computed(() =>
  paginatedNotifications.value.filter(n => isToday(n.time))
)

const yesterdayNotifications = computed(() =>
  paginatedNotifications.value.filter(n => isYesterday(n.time))
)

// A few days ago (2-6 days)
const fewDaysAgoNotifications = computed(() =>
  paginatedNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 2 && daysAgo <= 6
  })
)

// A week ago (7-13 days)
const weekAgoNotifications = computed(() =>
  paginatedNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 7 && daysAgo <= 13
  })
)

// A few weeks ago (14-29 days)
const fewWeeksAgoNotifications = computed(() =>
  paginatedNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 14 && daysAgo <= 29
  })
)

// A month ago (30+ days)
const monthAgoNotifications = computed(() =>
  paginatedNotifications.value.filter(n => {
    const daysAgo = getDaysAgo(n.time)
    return daysAgo >= 30
  })
)

const markAsRead = async (id) => {
  try {
    const notifIndex = notifications.value.findIndex(n => n.id === id);
    if (notifIndex !== -1) {
      notifications.value[notifIndex].read = true;

      // Firestore update
      const notifRef = doc(db, NOTIF_COLLECTION, id);
      await updateDoc(notifRef, { read: true });
    }
  } catch (err) {
    console.error("❌ Failed to mark as read:", err);
  }
};

const markAllAsRead = async () => {
  try {
    const updates = notifications.value.map(async (n) => {
      if (!n.read) {
        n.read = true;
        const notifRef = doc(db, NOTIF_COLLECTION, n.id);
        return updateDoc(notifRef, { read: true });
      }
    });
    await Promise.all(updates);
  } catch (err) {
    console.error("❌ Failed to mark all as read:", err);
  }
};

const deleteNotification = async (id) => {
  try {
    const index = notifications.value.findIndex(n => n.id === id);
    if (index !== -1) {
      notifications.value.splice(index, 1);

      // Firestore delete
      const notifRef = doc(db, NOTIF_COLLECTION, id);
      await deleteDoc(notifRef);
    }
  } catch (err) {
    console.error("❌ Failed to delete notification:", err);
  }
};

// Format notification time
const formatTime = (time) => {
  if (!time) return 'Unknown time'
  const now = new Date()
  const diff = now - new Date(time)
  const mins = Math.floor(diff / 60000)
  const hours = Math.floor(diff / 3600000)
  const days = Math.floor(diff / 86400000)

  if (mins < 60) return `${mins} min${mins !== 1 ? 's' : ''} ago`
  if (hours < 24) return `${hours} hour${hours !== 1 ? 's' : ''} ago`
  if (days < 7) return `${days} day${days !== 1 ? 's' : ''} ago`
  return new Date(time).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  })
}

// UI helpers
const getNotificationTypeClass = (type) => {
  switch (type) {
    case 'alert':
      return { bgColor: 'bg-red-500', badgeColor: 'bg-red-100 text-red-800', icon: AlertCircle }
    case 'warning':
      return { bgColor: 'bg-orange-500', badgeColor: 'bg-orange-100 text-orange-800', icon: AlertTriangle }
    case 'info':
      return { bgColor: 'bg-blue-500', badgeColor: 'bg-blue-100 text-blue-800', icon: Info }
    case 'success':
      return { bgColor: 'bg-green-500', badgeColor: 'bg-green-100 text-green-800', icon: Check }
    case 'water':
      return { bgColor: 'bg-cyan-500', badgeColor: 'bg-cyan-100 text-cyan-800', icon: Droplet }
    case 'system':
      return { bgColor: 'bg-purple-500', badgeColor: 'bg-purple-100 text-purple-800', icon: Cog }
    case 'data':
      return { bgColor: 'bg-indigo-500', badgeColor: 'bg-indigo-100 text-indigo-800', icon: BarChart }
    default:
      return { bgColor: 'bg-gray-500', badgeColor: 'bg-gray-100 text-gray-800', icon: Bell }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

/* Enhanced scrollbar styling */
.notification-scroll::-webkit-scrollbar {
  width: 5px;
  height: 5px;
}

.notification-scroll::-webkit-scrollbar-track {
  background: rgba(20, 83, 45, 0.05);
  border-radius: 4px;
}

.notification-scroll::-webkit-scrollbar-thumb {
  background: rgba(20, 83, 45, 0.2);
  border-radius: 4px;
  transition: background-color 200ms;
}

.notification-scroll::-webkit-scrollbar-thumb:hover {
  background: rgba(20, 83, 45, 0.4);
}

/* Firefox scrollbar styling */
.notification-scroll {
  scrollbar-width: thin;
  scrollbar-color: rgba(20, 83, 45, 0.2) rgba(20, 83, 45, 0.05);
}

/* Line clamp utilities */
.line-clamp-1 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 1;
}

.line-clamp-2 {
  overflow: hidden;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
}

/* Focus styles */
:focus-visible {
  outline: 2px solid #10b981;
  outline-offset: 2px;
}

/* Responsive design */
@media (max-width: 768px) {
  .p-5 {
    padding: 1rem;
  }
  
  .px-5 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .py-4 {
    padding-top: 0.75rem;
    padding-bottom: 0.75rem;
  }
  
  .gap-3 {
    gap: 0.5rem;
  }
}

@media (max-width: 640px) {
  .text-xl {
    font-size: 1.125rem;
  }
  
  .px-3 {
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }
  
  .py-1\.5 {
    padding-top: 0.25rem;
    padding-bottom: 0.25rem;
  }
  
  .w-8, .h-8 {
    width: 1.75rem;
    height: 1.75rem;
  }
}

/* Animation for unread indicator */
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.bg-blue-500 {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

/* Print styles */
@media print {
  .shadow-sm,
  .shadow-md,
  .hover\:shadow-lg {
    box-shadow: none !important;
  }
  
  .bg-gradient-to-r,
  .bg-gradient-to-br {
    background: white !important;
  }
  
  .border {
    border-color: #e5e7eb !important;
  }
}
</style>