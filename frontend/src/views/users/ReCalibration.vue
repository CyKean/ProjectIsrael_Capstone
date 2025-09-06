<template>
  <!-- Container Wrapper with optimized spacing -->
  <div class="flex-1 w-full px-2 sm:px-6 md:px-8 lg:px-10 overflow-hidden">
    <!-- Main Container -->
    <!-- removed hover effect and fixed width to align with navbar -->
    <!-- Added mobile-specific overflow and height classes for scrollability -->
    <div class="bg-white rounded-[20px] shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-green-100 w-full max-w-full h-[calc(100vh-75px)] md:h-[calc(100vh-130px)] overflow-hidden md:overflow-visible">
      <!-- Content Wrapper -->
      <!-- Added mobile overflow scrolling while preserving desktop flex behavior -->
      <div class="p-0 h-full flex flex-col overflow-y-auto md:overflow-visible">
        <!-- Header Section with Light Green Background -->
        <div class="bg-gradient-to-r from-green-50 to-emerald-50 border-b border-green-100 rounded-t-[20px] p-4 md:px-6 md:py-4 flex-shrink-0">
          <div class="flex items-center flex-col md:flex-row justify-between">
            <div>
              <h1 class="text-md md:text-xl font-semibold text-gray-800 mb-1">WiFi/Device Configuration</h1>
              <!-- made subtitle text smaller to match Device Control page font size -->
              <p class="text-xs text-gray-600">Configure and calibrate your ESP32 sensor devices</p>
            </div>
          </div>
        </div>

        <!-- Main Content Area -->
        <div class="p-4 md:p-6 lg:p-8 flex-1 flex items-stretch min-h-0 md:min-h-auto">
          <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 lg:gap-6 w-full min-h-full md:min-h-auto">
            <!-- Left Container - WiFi Indicator -->
             <div class="lg:col-span-1 bg-gradient-to-br from-green-50 to-emerald-50 border border-green-200 rounded-2xl p-3 md:p-6 transition-all duration-300 relative group">
              <div class="flex flex-col items-center justify-center h-full min-h-[150px] md:min-h-[200px] space-y-3 md:space-y-4">
                <!-- WiFi Symbol -->
                <div class="relative p-4 md:p-6 bg-white/50 rounded-full shadow-sm cursor-pointer" @click="checkInternetConnection">
                  <svg width="120" height="90" viewBox="0 0 80 60" class="md:w-[180px] md:h-[135px] transition-all duration-500 drop-shadow-sm">
                    <!-- WiFi Base Dot -->
                    <circle 
                      cx="40" 
                      cy="50" 
                      r="4" 
                      :fill="getWifiArcColor(connectionStrength)"
                      class="drop-shadow-sm"
                    />
                    
                    <!-- Dynamic WiFi Arcs -->
                    <path 
                      v-for="(arc, index) in wifiArcs" 
                      :key="index"
                      :d="arc.path" 
                      stroke-width="4" 
                      fill="none" 
                      stroke-linecap="round"
                      :stroke="connectionStrength >= arc.threshold ? getWifiArcColor(connectionStrength) : '#d1d5db'"
                      :opacity="connectionStrength >= arc.threshold ? 1 : 0.3"
                      class="transition-all duration-500 drop-shadow-sm"
                    />
                  </svg>
                  <!-- Refresh icon -->
                  <RefreshCw class="w-4 h-4 absolute top-2 right-2 text-gray-400 opacity-0 group-hover:opacity-100 transition-opacity" />
                </div>

                <!-- Connection Details -->
                <div class="text-center space-y-1 md:space-y-2">
                  <h3 class="text-sm md:text-base font-semibold text-gray-800">
                    {{ networkName || 'Internet Connection' }}
                  </h3>
                  <div class="flex items-center justify-center space-x-2">
                    <div 
                      class="w-2 h-2 rounded-full transition-colors duration-300 animate-pulse"
                      :class="isOnline ? 'bg-green-500' : 'bg-red-500'"
                    ></div>
                    <span 
                      class="text-xs md:text-sm font-medium transition-colors duration-300"
                      :class="isOnline ? 'text-green-600' : 'text-red-600'"
                    >
                      {{ getConnectionStatus() }}
                    </span>
                  </div>
                  <p class="text-xs md:text-sm text-gray-600">
                    Speed: {{ networkSpeed }} | Strength: {{ connectionStrength }}%
                  </p>
                  <p class="text-xs text-gray-500">
                    IP: {{ deviceIpAddress || 'Unknown' }}
                  </p>
                  <!-- Connection Type -->
                  <p class="text-xs text-blue-500 font-medium">
                    {{ connectionType }}
                  </p>
                  <!-- Last Check Time -->
                  <p class="text-xs text-gray-400">
                    Last check: {{ lastCheckedTime }}
                  </p>
                </div>
              </div>
            </div>

            <!-- changed from col-span-3 to col-span-2 for middle container -->
            <div class="lg:col-span-2 bg-gradient-to-br from-gray-50 to-slate-50 border border-gray-200 rounded-2xl p-4 md:p-6 transition-all duration-300">
              <div class="flex flex-col h-full min-h-[200px] space-y-4">
                <!-- Header -->
                <div class="text-center">
                  <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Settings class="w-6 h-6 text-white" />
                  </div>
                  <h2 class="text-xl font-semibold text-gray-800 mb-2">ESP32 Configuration</h2>
                  <p class="text-sm text-gray-600">Enter device details and manage calibration</p>
                </div>

                <!-- Form Content -->
                <div class="flex-1 flex flex-col justify-center space-y-4">
                  <!-- IP Address Input -->
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">ESP32 IP Address</label>
                    <div class="relative">
                      <input
                        v-model="esp32Config.ipAddress"
                        type="text"
                        :placeholder="savedIPPlaceholder"
                        class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all duration-200"
                        :class="{ 'border-red-300 focus:ring-red-500': esp32Config.ipAddress && !isValidIP(esp32Config.ipAddress) }"
                      />
                      <div v-if="isValidIP(esp32Config.ipAddress)" class="absolute right-3 top-1/2 transform -translate-y-1/2">
                        <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                      </div>
                    </div>
                    <p class="text-xs text-gray-500 mt-1">Enter the local IP address of your ESP32 device</p>
                  </div>

                  <!-- Action Buttons -->
                  <div class="space-y-3">
                    <!-- Changed button colors from blue to green gradient -->
                    <!-- Primary Save IP Button -->
                    <button 
                      @click="saveIPAddress"
                      :disabled="!isValidIP(esp32Config.ipAddress) || isSaving"
                      class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-300 disabled:to-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-all duration-300 flex items-center justify-center space-x-2 disabled:cursor-not-allowed relative overflow-hidden"
                    >
                      <!-- Changed loading animation dots from blue to green -->
                      <!-- Loading Animation -->
                      <div v-if="isSaving" class="absolute inset-0 bg-gradient-to-r from-green-400 to-emerald-500 flex items-center justify-center">
                        <div class="flex space-x-1">
                          <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 0ms"></div>
                          <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 150ms"></div>
                          <div class="w-2 h-2 bg-white rounded-full animate-bounce" style="animation-delay: 300ms"></div>
                        </div>
                      </div>
                      
                      <!-- Button Content -->
                      <div v-if="!isSaving" class="flex items-center space-x-2">
                        <Save class="w-4 h-4" />
                        <span>Save IP Address</span>
                      </div>
                      
                      <!-- Loading Text -->
                      <span v-if="isSaving" class="text-white font-medium">Saving...</span>
                    </button>

                    <!-- Secondary Actions -->
                    <div class="grid grid-cols-2 gap-2">
                      <button 
                        @click="testConnection"
                        class="bg-white hover:bg-gray-50 border border-gray-300 hover:border-gray-400 text-gray-700 font-medium py-2 px-3 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 text-sm"
                      >
                        <Zap class="w-4 h-4" />
                        <span>Test Connection</span>
                      </button>
                      
                      <button 
                        @click="showDeviceInfo"
                        class="bg-white hover:bg-gray-50 border border-gray-300 hover:border-gray-400 text-gray-700 font-medium py-2 px-3 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 text-sm"
                      >
                        <Info class="w-4 h-4" />
                        <span>Device Info</span>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Connection Status -->
                <div class="flex items-center justify-between text-sm pt-3 border-t border-gray-200">
                  <div class="flex items-center space-x-2">
                    <div 
                      class="w-2 h-2 rounded-full animate-pulse"
                      :class="connectionStatus.connected ? 'bg-green-500' : 'bg-red-500'"
                    ></div>
                    <span 
                      class="font-medium transition-colors duration-300"
                      :class="connectionStatus.connected ? 'text-green-600' : 'text-red-600'"
                    >
                      {{ connectionStatus.connected ? 'Device Connected' : 'Device Disconnected' }}
                    </span>
                  </div>
                  <span class="text-gray-500">{{ connectionStatus.lastSeen }}</span>
                </div>
              </div>
            </div>

            <!-- Right Container - ESP32 Recalibration Options -->
            <div class="lg:col-span-1 bg-gradient-to-br from-emerald-50 to-green-50 border border-emerald-200 rounded-2xl p-4 md:p-6 transition-all duration-300">
              <div class="flex flex-col h-full min-h-[200px] space-y-4">
                <!-- Header -->
                <div class="text-center">
                  <div class="w-10 h-10 bg-emerald-500 rounded-full flex items-center justify-center mx-auto mb-3">
                    <RefreshCw class="w-5 h-5 text-white" />
                  </div>
                  <h3 class="text-lg font-semibold text-gray-800 mb-2">Device Recalibration</h3>
                  <p class="text-xs text-gray-600">Quick access to ESP32 devices</p>
                </div>

                <!-- ESP32 Recalibration Buttons -->
                <div class="flex-1 flex flex-col justify-center space-y-3">
                  <button 
                    @click="navigateToRecalibration('esp32-1')"
                    class="w-full bg-gradient-to-r from-emerald-500 to-green-600 hover:from-emerald-600 hover:to-green-700 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 text-sm"
                    :disabled="deviceStatus.esp1 === 'offline'"
                    :class="deviceStatus.esp1 === 'offline' ? 'opacity-50 cursor-not-allowed' : ''"
                  >
                    <Cpu class="w-4 h-4" />
                    <span>ESP32-1 Recalibrate</span>
                    <span v-if="deviceStatus.esp1 === 'checking'" class="ml-2">
                      <RefreshCw class="w-3 h-3 animate-spin" />
                    </span>
                  </button>

                  <button 
                    @click="navigateToRecalibration('esp32-2')"
                    class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 text-sm"
                    :disabled="deviceStatus.esp2 === 'offline'"
                    :class="deviceStatus.esp2 === 'offline' ? 'opacity-50 cursor-not-allowed' : ''"
                  >
                    <Cpu class="w-4 h-4" />
                    <span>ESP32-2 Recalibrate</span>
                    <span v-if="deviceStatus.esp2 === 'checking'" class="ml-2">
                      <RefreshCw class="w-3 h-3 animate-spin" />
                    </span>
                  </button>

                  <button 
                    @click="navigateToRecalibration('esp32-3')"
                    class="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 flex items-center justify-center space-x-2 text-sm"
                    :disabled="deviceStatus.esp3 === 'offline'"
                    :class="deviceStatus.esp3 === 'offline' ? 'opacity-50 cursor-not-allowed' : ''"
                  >
                    <Cpu class="w-4 h-4" />
                    <span>ESP32-3 Recalibrate</span>
                    <span v-if="deviceStatus.esp3 === 'checking'" class="ml-2">
                      <RefreshCw class="w-3 h-3 animate-spin" />
                    </span>
                  </button>
                </div>

                <!-- Quick Status - Made Dynamic -->
                <div class="text-center pt-3 border-t border-emerald-200">
                  <p class="text-xs" :class="allDevicesOnline ? 'text-green-600' : 'text-red-600'">
                    {{ deviceStatusMessage }}
                  </p>
                  <div class="flex justify-center space-x-1 mt-1">
                    <div 
                      class="w-2 h-2 rounded-full transition-colors duration-300"
                      :class="deviceStatus.esp1 === 'online' ? 'bg-green-500' : 'bg-red-500'"
                    ></div>
                    <div 
                      class="w-2 h-2 rounded-full transition-colors duration-300"
                      :class="deviceStatus.esp2 === 'online' ? 'bg-green-500' : 'bg-red-500'"
                    ></div>
                    <div 
                      class="w-2 h-2 rounded-full transition-colors duration-300"
                      :class="deviceStatus.esp3 === 'online' ? 'bg-green-500' : 'bg-red-500'"
                    ></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-if="activeModal" class="fixed inset-0 z-[9999] overflow-y-auto">
    <!-- Backdrop with blur effect -->
    <div class="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" @click="closeModal"></div>
    
    <!-- Modal container with proper centering -->
    <div class="flex min-h-full items-center justify-center p-4">
      <!-- ESP32-1 Modal - FIXED HEIGHT AND WIDTH -->
      <div v-if="activeModal === 'esp1'" class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        <!-- Modal Header - Fixed -->
        <div class="flex items-center justify-between p-6 border-b border-gray-100 flex-shrink-0">
          <div class="flex items-center flex-row space-x-4 md:space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl flex items-center justify-center">
              <Cpu class="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h2 class="text-md md:text-lg font-semibold text-gray-800">ESP32-1 Configuration</h2>
              <p class="text-xs md:text-sm text-gray-500">NPK + Soil pH Monitoring</p>
            </div>
          </div>
          <button @click="closeModal" class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors">
            <X class="w-4 h-4" />
          </button>
        </div>

        <!-- Modal Content - Scrollable -->
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-6">
            <!-- WiFi and Server Settings -->
            <div class="space-y-4">
              <!-- Changed WiFi icon background from blue to green -->
              <div class="flex items-center space-x-2 mb-3">
                <div class="w-6 h-6 bg-green-50 rounded-lg flex items-center justify-center">
                  <Wifi class="w-3 h-3 text-green-600" />
                </div>
                <h3 class="font-medium text-gray-800">WiFi and Server Settings</h3>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-2">WiFi SSID</label>
                  <input v-model="esp1Config.wifiSSID" type="text" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="WiFi network name">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-2">WiFi Password</label>
                  <div class="relative">
                    <input v-model="esp1Config.wifiPassword" :type="showPassword.esp1 ? 'text' : 'password'" class="w-full px-3 py-2 pr-10 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="WiFi password">
                    <button @click="togglePassword('esp1')" type="button" class="absolute inset-y-0 right-0 flex items-center justify-center w-10 text-gray-400 hover:text-gray-600 transition-colors">
                      <EyeOff v-if="!showPassword.esp1" class="w-4 h-4" />
                      <Eye v-else class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-2">Server URL</label>
                <input v-model="esp1Config.serverURL" type="url" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="http://192.168.x.x">
              </div>
            </div>

            <!-- NPK Sensor Offset Section -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-3">
                <div class="w-6 h-6 bg-purple-50 rounded-lg flex items-center justify-center">
                  <BarChart3 class="w-3 h-3 text-purple-600" />
                </div>
                <h3 class="font-medium text-gray-800">NPK Sensor Offset Section</h3>
              </div>
              
              <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <!-- Nitrogen Offset -->
                <div class="relative">
                  <label class="block text-sm font-medium text-green-600 mb-2">Nitrogen (mg/kg)</label>
                  <input 
                    v-model.number="esp1Config.nitrogenOffset" 
                    type="number" 
                    step="0.1" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                    placeholder="0.0"
                    @focus="showTooltip.nitrogen = true"
                    @blur="showTooltip.nitrogen = false"
                  >
                  <!-- Simplified Tooltip -->
                  <div v-if="showTooltip.nitrogen" class="absolute z-50 top-full left-0 mt-2 w-56 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <Info class="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">Calibration Offset</div>
                        <div>Enter + or - value to adjust reading if sensor is slightly off</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>

                <!-- Phosphorus Offset -->
                <div class="relative">
                  <!-- Changed phosphorus label color from blue to green -->
                  <label class="block text-sm font-medium text-green-600 mb-2">Phosphorus (mg/kg)</label>
                  <input 
                    v-model.number="esp1Config.phosphorusOffset" 
                    type="number" 
                    step="0.1" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                    placeholder="0.0"
                    @focus="showTooltip.phosphorus = true"
                    @blur="showTooltip.phosphorus = false"
                  >
                  <!-- Simplified Tooltip -->
                  <div v-if="showTooltip.phosphorus" class="absolute z-50 top-full left-0 mt-2 w-56 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <!-- Changed tooltip icon color from blue to green -->
                      <Info class="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">Calibration Offset</div>
                        <div>Enter + or - value to adjust reading if sensor is slightly off</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>

                <!-- Potassium Offset -->
                <div class="relative">
                  <!-- Changed potassium label color from purple to green -->
                  <label class="block text-sm font-medium text-green-600 mb-2">Potassium (mg/kg)</label>
                  <input 
                    v-model.number="esp1Config.potassiumOffset" 
                    type="number" 
                    step="0.1" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                    placeholder="0.0"
                    @focus="showTooltip.potassium = true"
                    @blur="showTooltip.potassium = false"
                  >
                  <!-- Simplified Tooltip -->
                  <div v-if="showTooltip.potassium" class="absolute z-50 top-full left-0 mt-2 w-56 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <!-- Changed tooltip icon color from purple to green -->
                      <Info class="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">Calibration Offset</div>
                        <div>Enter + or - value to adjust reading if sensor is slightly off</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Soil pH Sensor Offset Section -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-3">
                <div class="w-6 h-6 bg-orange-50 rounded-lg flex items-center justify-center">
                  <Droplets class="w-3 h-3 text-orange-600" />
                </div>
                <h3 class="font-medium text-gray-800">Soil pH Sensor Offset Section</h3>
              </div>
              
              <div class="max-w-xs relative">
                <label class="block text-sm font-medium text-orange-600 mb-2">pH Offset</label>
                <input 
                  v-model.number="esp1Config.phOffset" 
                  type="number" 
                  step="0.1" 
                  class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-sm" 
                  placeholder="0.0"
                  @focus="showTooltip.ph = true"
                  @blur="showTooltip.ph = false"
                >
                <!-- Fixed Tooltip for pH -->
                <div v-if="showTooltip.ph" class="absolute z-50 top-full left-0 mt-2 w-60 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                  <div class="flex items-start space-x-2">
                    <Info class="w-3 h-3 text-orange-400 flex-shrink-0 mt-0.5" />
                    <div class="leading-relaxed">
                      <div class="font-medium mb-1">pH Calibration</div>
                      <div>Enter + or - value to adjust reading</div>
                      <div class="text-gray-300 mt-1">Example: -0.3 or +0.5</div>
                    </div>
                  </div>
                  <!-- Left-aligned Arrow -->
                  <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ESP32-2 Modal -->
      <div v-if="activeModal === 'esp2'" class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        <!-- Modal Header - Fixed -->
        <div class="flex items-center justify-between p-6 border-b border-gray-100 flex-shrink-0">
          <div class="flex items-center flex-row space-x-4 md:space-x-3">
            <!-- Changed ESP32-2 modal header icon background from blue to green -->
            <div class="w-10 h-10 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl flex items-center justify-center">
              <Cloud class="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h2 class="text-md md:text-lg font-semibold text-gray-800">ESP32-2 Configuration</h2>
              <p class="text-xs md:text-sm text-gray-500">Environmental Monitoring</p>
            </div>
          </div>
          <button @click="closeModal" class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors">
            <X class="w-4 h-4" />
          </button>
        </div>

        <!-- Modal Content - Scrollable -->
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-6">
            <!-- WiFi Configuration -->
            <div class="space-y-4">
              <!-- Changed WiFi icon background from blue to green -->
              <div class="flex items-center space-x-2 mb-3">
                <div class="w-6 h-6 bg-green-50 rounded-lg flex items-center justify-center">
                  <Wifi class="w-3 h-3 text-green-600" />
                </div>
                <h3 class="font-medium text-gray-800">WiFi Settings</h3>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-2">Network SSID</label>
                  <!-- Changed focus ring from blue to green -->
                  <input v-model="esp2Config.wifiSSID" type="text" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="WiFi network name">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-2">Password</label>
                  <div class="relative">
                    <!-- Changed focus ring from blue to green -->
                    <input v-model="esp2Config.wifiPassword" :type="showPassword.esp2 ? 'text' : 'password'" class="w-full px-3 py-2 pr-10 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="WiFi password">
                    <button @click="togglePassword('esp2')" type="button" class="absolute inset-y-0 right-0 flex items-center justify-center w-10 text-gray-400 hover:text-gray-600 transition-colors">
                      <EyeOff v-if="!showPassword.esp2" class="w-4 h-4" />
                      <Eye v-else class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-2">API Endpoint</label>
                <!-- Changed focus ring from blue to green -->
                <input v-model="esp2Config.apiURL" type="url" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="https://api.example.com">
              </div>
            </div>

            <!-- Environmental Sensor Calibration -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-3">
                <div class="w-6 h-6 bg-purple-50 rounded-lg flex items-center justify-center">
                  <BarChart3 class="w-3 h-3 text-purple-600" />
                </div>
                <h3 class="font-medium text-gray-800">Environmental Sensors</h3>
              </div>
              
              <!-- DHT21 Temperature & Humidity Offsets -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="relative">
                  <label class="block text-sm font-medium text-red-600 mb-2">Temp Offset (°C)</label>
                  <input 
                    v-model="esp2Config.tempOffset" 
                    type="number" 
                    step="0.1" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-red-500/20 focus:border-red-500 transition-all text-sm" 
                    placeholder="0.0"
                    @focus="showTooltip.tempOffset = true"
                    @blur="showTooltip.tempOffset = false"
                  >
                  <!-- Temperature Offset Tooltip -->
                  <div v-if="showTooltip.tempOffset" class="absolute z-50 top-full left-0 mt-2 w-56 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <Info class="w-3 h-3 text-red-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">DHT21 Temperature</div>
                        <div>Apply if temperature is consistently off</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>
                
                <div class="relative">
                  <!-- Changed humidity label color from blue to green -->
                  <label class="block text-sm font-medium text-green-600 mb-2">Humidity Offset (%)</label>
                  <input 
                    v-model="esp2Config.humidityOffset" 
                    type="number" 
                    step="0.1" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                    placeholder="0.0"
                    @focus="showTooltip.humidityOffset = true"
                    @blur="showTooltip.humidityOffset = false"
                  >
                  <!-- Humidity Offset Tooltip -->
                  <div v-if="showTooltip.humidityOffset" class="absolute z-50 top-full left-0 mt-2 w-56 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <!-- Changed tooltip icon color from blue to green -->
                      <Info class="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">DHT21 Humidity</div>
                        <div>Apply if humidity reading is incorrect</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>
              </div>
              
              <!-- Auto Watering Threshold -->
              <div class="relative max-w-xs">
                <label class="block text-sm font-medium text-green-600 mb-2">Auto Watering Threshold (%)</label>
                <input 
                  v-model="esp2Config.wateringThreshold" 
                  type="number" 
                  class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                  placeholder="30"
                  @focus="showTooltip.wateringThreshold = true"
                  @blur="showTooltip.wateringThreshold = false"
                >
                <!-- Watering Threshold Tooltip -->
                <div v-if="showTooltip.wateringThreshold" class="absolute z-50 top-full left-0 mt-2 w-64 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                  <div class="flex items-start space-x-2">
                    <Info class="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                    <div class="leading-relaxed">
                      <div class="font-medium mb-1">Auto Watering</div>
                      <div>If soil moisture falls below this %, the water pump will turn ON.</div>
                    </div>
                  </div>
                  <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                </div>
              </div>
              
              <!-- Soil Moisture Sensor Calibration -->
              <div class="space-y-3">
                <!-- Changed info box background from blue to green -->
                <div class="text-sm text-gray-600 bg-green-50 p-3 rounded-lg border border-green-200">
                  <div class="flex items-start space-x-2">
                    <Info class="w-4 h-4 text-green-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <div class="font-medium text-green-800 mb-1">Soil Sensor Calibration</div>
                      <div class="text-green-700">Calibrate soil sensor: measure sensor reading in air and in water to set dry/wet reference.</div>
                    </div>
                  </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-orange-600 mb-2">Air Value (Dry Soil)</label>
                    <input 
                      v-model="esp2Config.airValue" 
                      type="number" 
                      class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-orange-500/20 focus:border-orange-500 transition-all text-sm" 
                      placeholder="1024"
                    >
                  </div>
                  <div>
                    <!-- Changed water value label color from cyan to green -->
                    <label class="block text-sm font-medium text-green-600 mb-2">Water Value (Wet Soil)</label>
                    <input 
                      v-model="esp2Config.waterValue" 
                      type="number" 
                      class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                      placeholder="0"
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- ESP32-3 Modal -->
      <div v-if="activeModal === 'esp3'" class="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden flex flex-col">
        <!-- Modal Header - Fixed -->
        <div class="flex items-center justify-between p-6 border-b border-gray-100 flex-shrink-0">
          <div class="flex items-center flex-row space-x-4 md:pace-x-3">
            <!-- Changed ESP32-3 modal header icon background from cyan to green -->
            <div class="w-10 h-10 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl flex items-center justify-center">
              <Droplets class="w-5 h-5 text-green-600" />
            </div>
            <div>
              <h2 class="text-md md:text-lg font-semibold text-gray-800">ESP32-3 Configuration</h2>
              <p class="text-xs md:text-sm text-gray-500">Water Level Monitoring</p>
            </div>
          </div>
          <button @click="closeModal" class="w-8 h-8 flex items-center justify-center rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-colors">
            <X class="w-4 h-4" />
          </button>
        </div>

        <!-- Modal Content - Scrollable -->
        <div class="flex-1 overflow-y-auto p-6">
          <div class="space-y-6">
            <!-- WiFi Configuration -->
            <div class="space-y-4">
              <!-- Changed WiFi icon background from blue to green -->
              <div class="flex items-center space-x-2 mb-3">
                <div class="w-6 h-6 bg-green-50 rounded-lg flex items-center justify-center">
                  <Wifi class="w-3 h-3 text-green-600" />
                </div>
                <h3 class="font-medium text-gray-800">WiFi Settings</h3>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-2">Network SSID</label>
                  <!-- Changed focus ring from cyan to green -->
                  <input v-model="esp3Config.wifiSSID" type="text" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="WiFi network name">
                </div>
                <div>
                  <label class="block text-sm font-medium text-gray-600 mb-2">Password</label>
                  <div class="relative">
                    <!-- Changed focus ring from cyan to green -->
                    <input v-model="esp3Config.wifiPassword" :type="showPassword.esp3 ? 'text' : 'password'" class="w-full px-3 py-2 pr-10 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="WiFi password">
                    <button @click="togglePassword('esp3')" type="button" class="absolute inset-y-0 right-0 flex items-center justify-center w-10 text-gray-400 hover:text-gray-600 transition-colors">
                      <EyeOff v-if="!showPassword.esp3" class="w-4 h-4" />
                      <Eye v-else class="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-600 mb-2">API Endpoint</label>
                <!-- Changed focus ring from cyan to green -->
                <input v-model="esp3Config.apiURL" type="url" class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" placeholder="https://api.example.com">
              </div>
            </div>

            <!-- Tank Calibration -->
            <div class="space-y-4">
              <div class="flex items-center space-x-2 mb-3">
                <div class="w-6 h-6 bg-purple-50 rounded-lg flex items-center justify-center">
                  <BarChart3 class="w-3 h-3 text-purple-600" />
                </div>
                <h3 class="font-medium text-gray-800">Water Tank Calibration</h3>
              </div>
              
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <!-- Tank Height -->
                <div class="relative">
                  <!-- Changed tank height label color from cyan to green -->
                  <label class="block text-sm font-medium text-green-600 mb-2">Tank Height (cm)</label>
                  <input 
                    v-model="esp3Config.tankHeight" 
                    type="number" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                    placeholder="100"
                    @focus="showTooltip.tankHeight = true"
                    @blur="showTooltip.tankHeight = false"
                  >
                  <!-- Tank Height Tooltip -->
                  <div v-if="showTooltip.tankHeight" class="absolute z-50 top-full left-0 mt-2 w-64 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <!-- Changed tooltip icon color from cyan to green -->
                      <Info class="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">Tank Height</div>
                        <div>The full vertical height of the water tank (from bottom to top edge). Used to calculate percentage level.</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>

                <!-- Alert Level -->
                <div class="relative">
                  <!-- Changed alert level label color from blue to green -->
                  <label class="block text-sm font-medium text-green-600 mb-2">Alert Level (%)</label>
                  <input 
                    v-model="esp3Config.alertLevel" 
                    type="number" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                    placeholder="20"
                    @focus="showTooltip.alertLevel = true"
                    @blur="showTooltip.alertLevel = false"
                  >
                  <!-- Alert Level Tooltip -->
                  <div v-if="showTooltip.alertLevel" class="absolute z-50 top-full left-0 mt-2 w-64 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <!-- Changed tooltip icon color from blue to green -->
                      <Info class="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">Alert Threshold</div>
                        <div>If water level drops below this percentage, the system triggers alerts (e.g., LED or buzzer).</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>

                <!-- Full Distance -->
                <div class="relative">
                  <label class="block text-sm font-medium text-green-600 mb-2">Full Distance (cm)</label>
                  <input 
                    v-model="esp3Config.fullDistance" 
                    type="number" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-green-500/20 focus:border-green-500 transition-all text-sm" 
                    placeholder="5"
                    @focus="showTooltip.fullDistance = true"
                    @blur="showTooltip.fullDistance = false"
                  >
                  <!-- Full Distance Tooltip -->
                  <div v-if="showTooltip.fullDistance" class="absolute z-50 top-full left-0 mt-2 w-64 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <Info class="w-3 h-3 text-green-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">Full Tank Distance</div>
                        <div>The measured distance (in cm) from the ultrasonic sensor to the water surface when the tank is full.</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>

                <!-- Empty Distance -->
                <div class="relative">
                  <label class="block text-sm font-medium text-red-600 mb-2">Empty Distance (cm)</label>
                  <input 
                    v-model="esp3Config.emptyDistance" 
                    type="number" 
                    class="w-full px-3 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:ring-2 focus:ring-red-500/20 focus:border-red-500 transition-all text-sm" 
                    placeholder="95"
                    @focus="showTooltip.emptyDistance = true"
                    @blur="showTooltip.emptyDistance = false"
                  >
                  <!-- Empty Distance Tooltip -->
                  <div v-if="showTooltip.emptyDistance" class="absolute z-50 top-full left-0 mt-2 w-64 px-3 py-2 bg-gray-800 text-white text-xs rounded-lg shadow-xl pointer-events-none">
                    <div class="flex items-start space-x-2">
                      <Info class="w-3 h-3 text-red-400 flex-shrink-0 mt-0.5" />
                      <div class="leading-relaxed">
                        <div class="font-medium mb-1">Empty Tank Distance</div>
                        <div>The measured distance from the ultrasonic sensor to the tank floor when the tank is empty. Helps define 0% water level.</div>
                      </div>
                    </div>
                    <div class="absolute bottom-full left-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-800"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <div v-if="showLoadingModal" class="fixed inset-0 z-[10000] overflow-y-auto">
    <!-- Backdrop -->
    <div class="fixed inset-0 bg-black/60 backdrop-blur-sm transition-opacity"></div>
    
    <!-- Modal container -->
    <div class="flex min-h-full items-center justify-center p-4">
      <div class="relative bg-white rounded-2xl shadow-2xl w-full max-w-md p-8 text-center">
        <!-- Loading Animation -->
        <div class="mb-6">
          <div class="relative w-16 h-16 mx-auto">
            <!-- Spinning circle -->
            <div class="absolute inset-0 border-4 border-gray-200 rounded-full"></div>
            <div class="absolute inset-0 border-4 border-green-500 rounded-full border-t-transparent animate-spin"></div>
            <!-- Inner pulsing dot -->
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            </div>
          </div>
        </div>
        
        <!-- Loading Text -->
        <h3 class="text-lg font-semibold text-gray-800 mb-2">Saving IP Address</h3>
        <p class="text-gray-600 mb-4">Please wait while we save your configuration...</p>
        
        <!-- Progress dots -->
        <div class="flex justify-center space-x-1">
          <div class="w-2 h-2 bg-green-500 rounded-full animate-bounce" style="animation-delay: 0ms"></div>
          <div class="w-2 h-2 bg-green-500 rounded-full animate-bounce" style="animation-delay: 150ms"></div>
          <div class="w-2 h-2 bg-green-500 rounded-full animate-bounce" style="animation-delay: 300ms"></div>
        </div>
      </div>
    </div>
  </div>

</template>

<script setup>
import { 
  Search, 
  Download, 
  Cpu, 
  Cloud, 
  Droplets, 
  CheckCircle, 
  Settings, 
  BarChart3, 
  Container, 
  Database, 
  Zap, 
  Save, 
  RotateCcw, 
  Upload, 
  X, 
  Wifi, 
  Eye, 
  EyeOff, 
  XCircle, 
  Info,
  RefreshCcw,
  Check,
  RefreshCw
} from 'lucide-vue-next'

import { ref, onMounted, onBeforeUnmount, watch, reactive, onUnmounted, computed } from 'vue'
import api from '../../api/index.js'

// const backendBaseUrl = import.meta.env.VITE_BACKEND_URL || 'https://project-israel-backend.onrender.com';

const searchQuery = ref('')

const deviceStatus = reactive({
  esp1: 'checking', // 'online', 'offline', 'checking'
  esp2: 'checking',
  esp3: 'checking'
})

const networkDetails = reactive({
  ipAddress: '',
  ssid: '',
  signalStrength: 0,
  isConnected: false
});

let pollingIntervalId = null;
let deviceStatusIntervalId = null;
let internetCheckIntervalId = null;

const isOnline = computed(() => deviceInternetStatus.isOnline);
const connectionStrength = computed(() => deviceInternetStatus.connectionStrength);
const networkName = computed(() => deviceInternetStatus.networkName);
const deviceIpAddress = computed(() => deviceInternetStatus.deviceIpAddress);
const connectionType = computed(() => deviceInternetStatus.connectionType);
const networkSpeed = computed(() => deviceInternetStatus.networkSpeed);
const lastCheckedTime = computed(() => formatLastUpdated(deviceInternetStatus.lastChecked));

const deviceInternetStatus = reactive({
  isOnline: navigator.onLine,
  connectionStrength: 100,
  networkName: 'Checking...',
  ssid: 'Detecting...',
  deviceIpAddress: '',
  connectionType: 'Unknown',
  networkType: 'unknown', // 'wifi', 'ethernet', 'cellular', 'hotspot'
  networkSpeed: 'Unknown',
  lastChecked: new Date(),
  latency: 0,
  canDetectSsid: false
});

const detectNetworkInfo = async () => {
  try {
    // @ts-ignore
    const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
    
    if (connection) {
      deviceInternetStatus.connectionType = connection.effectiveType || 'unknown';
      deviceInternetStatus.networkSpeed = connection.downlink ? `${connection.downlink} Mbps` : 'Unknown';
      
      const strengthMap = { 'slow-2g': 25, '2g': 40, '3g': 60, '4g': 85, '5g': 95 };
      deviceInternetStatus.connectionStrength = strengthMap[connection.effectiveType] || 75;
    }
    
    // Use a more reliable approach for network name/SSID
    await detectNetworkNameReliable();
    
  } catch (e) {
    console.log('Network detection error:', e);
    await detectNetworkNameReliable();
  }
};

const detectNetworkNameReliable = async () => {
  try {
    // Method 1: Try to get network info from IP geolocation
    const ipResponse = await fetch('https://ipapi.co/json/');
    if (ipResponse.ok) {
      const ipData = await ipResponse.json();
      
      // Use ISP/organization as network name
      if (ipData.org || ipData.isp) {
        deviceInternetStatus.networkName = ipData.org || ipData.isp;
        deviceInternetStatus.ssid = deviceInternetStatus.networkName;
        return;
      }
    }
  } catch (error) {
    console.log('IP geolocation failed:', error);
  }
  
  try {
    // Method 2: Try another IP service
    const ipResponse2 = await fetch('https://ipinfo.io/json');
    if (ipResponse2.ok) {
      const ipData = await ipResponse2.json();
      if (ipData.org) {
        deviceInternetStatus.networkName = ipData.org;
        deviceInternetStatus.ssid = deviceInternetStatus.networkName;
        return;
      }
    }
  } catch (error) {
    console.log('Second IP service failed:', error);
  }
  
  // Method 3: Fallback based on connection type
  // @ts-ignore
  const connection = navigator.connection || navigator.mozConnection || navigator.webkitConnection;
  
  if (connection && connection.type) {
    switch(connection.type) {
      case 'wifi':
        deviceInternetStatus.networkName = 'Wi-Fi Network';
        deviceInternetStatus.ssid = 'Wi-Fi';
        break;
      case 'ethernet':
        deviceInternetStatus.networkName = 'Wired Connection';
        deviceInternetStatus.ssid = 'Ethernet';
        break;
      case 'cellular':
        deviceInternetStatus.networkName = 'Mobile Network';
        deviceInternetStatus.ssid = 'Cellular';
        break;
      default:
        deviceInternetStatus.networkName = 'Internet Connection';
        deviceInternetStatus.ssid = 'Network';
    }
  } else {
    // Final fallback
    deviceInternetStatus.networkName = 'Internet Connection';
    deviceInternetStatus.ssid = 'Network';
  }
};

const checkInternetConnection = async () => {
  try {
    deviceInternetStatus.lastChecked = new Date();
    
    // Check basic online status
    deviceInternetStatus.isOnline = navigator.onLine;
    
    if (!deviceInternetStatus.isOnline) {
      deviceInternetStatus.connectionStrength = 0;
      deviceInternetStatus.networkName = 'Offline';
      deviceInternetStatus.ssid = 'Offline';
      return;
    }

    // Update network information
    await detectNetworkInfo();

    // Test latency with a CORS-friendly endpoint
    await testLatency();
    
    // Try to get public IP address
    await getPublicIpAddress();
    
    console.log('Internet connection check completed:', deviceInternetStatus);
    
  } catch (error) {
    console.error('Error checking internet connection:', error);
    deviceInternetStatus.connectionStrength = Math.max(0, deviceInternetStatus.connectionStrength - 20);
  }
};


// Test network latency with CORS-friendly endpoints
const testLatency = async () => {
  try {
    const startTime = performance.now();
    
    // Use a CORS-friendly endpoint for latency test
    const testEndpoints = [
      'https://corsproxy.io/?https://httpbin.org/get',
      'https://api.allorigins.win/raw?url=https://httpbin.org/get',
      'https://jsonplaceholder.typicode.com/posts/1'
    ];
    
    let success = false;
    
    for (const endpoint of testEndpoints) {
      try {
        const response = await fetch(endpoint, {
          method: 'GET',
          cache: 'no-cache',
          headers: {
            'Accept': 'application/json'
          }
        });
        
        if (response.ok) {
          success = true;
          break;
        }
      } catch (e) {
        continue; // Try next endpoint
      }
    }
    
    const latency = performance.now() - startTime;
    deviceInternetStatus.latency = Math.round(latency);
    
    if (success) {
      // Adjust strength based on latency
      if (latency < 100) deviceInternetStatus.connectionStrength = Math.min(100, deviceInternetStatus.connectionStrength + 10);
      else if (latency > 500) deviceInternetStatus.connectionStrength = Math.max(0, deviceInternetStatus.connectionStrength - 20);
    } else {
      // If all endpoints failed, reduce strength
      deviceInternetStatus.connectionStrength = Math.max(0, deviceInternetStatus.connectionStrength - 30);
    }
    
  } catch (error) {
    deviceInternetStatus.connectionStrength = Math.max(0, deviceInternetStatus.connectionStrength - 30);
  }
};

// Get public IP address with better error handling
const getPublicIpAddress = async () => {
  try {
    // Try multiple IP services
    const ipServices = [
      'https://api.ipify.org?format=json',
      'https://ipapi.co/json/',
      'https://jsonip.com/'
    ];
    
    for (const service of ipServices) {
      try {
        const response = await fetch(service, { 
          timeout: 3000,
          headers: {
            'Accept': 'application/json'
          }
        });
        
        if (response.ok) {
          const data = await response.json();
          deviceInternetStatus.deviceIpAddress = data.ip || data.ipaddress || 'Unknown';
          return; // Success, exit the function
        }
      } catch (error) {
        continue; // Try next service
      }
    }
    
    // If all services failed
    deviceInternetStatus.deviceIpAddress = 'Cannot determine';
    
  } catch (error) {
    deviceInternetStatus.deviceIpAddress = 'Error fetching IP';
  }
};


const connectionStatus = reactive({
  connected: false,
  lastSeen: 'Never connected'
})

const allDevicesOnline = computed(() => {
  return deviceStatus.esp1 === 'online' && 
         deviceStatus.esp2 === 'online' && 
         deviceStatus.esp3 === 'online'
})

const deviceStatusMessage = computed(() => {
  if (deviceStatus.esp1 === 'checking' || deviceStatus.esp2 === 'checking' || deviceStatus.esp3 === 'checking') {
    return 'Checking device status...'
  }
  return allDevicesOnline.value ? 'All devices online' : 'Some devices offline'
})

const testDeviceConnection = async (device, url) => {
  try {
    deviceStatus[device] = 'checking'
    
    // Use a timeout to prevent hanging requests
    const controller = new AbortController()
    const timeoutId = setTimeout(() => controller.abort(), 5000) // 5 second timeout
    
    const response = await fetch(url, {
      method: 'HEAD',
      signal: controller.signal,
      mode: 'no-cors' // Handle CORS issues
    })
    
    clearTimeout(timeoutId)
    deviceStatus[device] = 'online'
    return true
  } catch (error) {
    console.log(`${device} is offline:`, error)
    deviceStatus[device] = 'offline'
    return false
  }
}

const checkAllDeviceConnections = async () => {
  const devices = [
    { id: 'esp1', url: 'http://npkdevice.local' },
    { id: 'esp2', url: 'http://esp32env.local' },
    { id: 'esp3', url: 'http://waterlevel.local' }
  ]
  
  // Test all devices in parallel
  await Promise.all(devices.map(device => 
    testDeviceConnection(device.id, device.url)
  ))
}

const navigateToRecalibration = async (device) => {
  let domain;
  
  switch(device) {
    case 'esp32-1':
      domain = 'npkdevice.local';
      break;
    case 'esp32-2':
      domain = 'esp32env.local';
      break;
    case 'esp32-3':
      domain = 'waterlevel.local';
      break;
    default:
      domain = device;
  }
  
  // Test connection before navigating
  const isOnline = await testDeviceConnection(device.replace('esp32-', 'esp'), `http://${domain}`)
  
  if (isOnline) {
    window.location.href = `http://${domain}`;
  } else {
    showToastMessage(`${device} is currently offline`, 'error')
  }
}

const testConnection = async () => {
  if (!isValidIP(esp32Config.ipAddress)) {
    showToastMessage('Please enter a valid IP address', 'error');
    return;
  }

  try {
    showLoadingModal.value = true;
    
    // Check backend connection first with shorter timeout
    const backendPing = await api.get(`/system/ping`, { timeout: 3000 });
    if (!backendPing.data?.success) {
      throw new Error('Backend service unavailable');
    }
    
    // Use backend proxy to test ESP32 connection with shorter timeout
    const connectionTest = await api.get(`/esp32/test-connection`, {
      params: { ip_address: esp32Config.ipAddress },
      timeout: 8000  // Increased to 8 seconds to account for backend processing
    });

    showToastMessage('Connection successful to both backend and ESP32', 'success');
    
    // Update connection status dynamically
    connectionStatus.connected = true;
    connectionStatus.lastSeen = new Date().toLocaleTimeString();
    
    // Update WiFi signal strength
    if (connectionTest.data.signal_strength) {
      wifiDetails.signalStrength = connectionTest.data.signal_strength;
    }
    
    return connectionTest.data;
  } catch (error) {
    console.error('Connection test failed:', error);
    
    // Update connection status on error
    connectionStatus.connected = false;
    connectionStatus.lastSeen = 'Connection failed';
    
    let errorMessage = 'Connection test failed';
    
    if (error.code === 'ECONNABORTED') {
      errorMessage = 'Connection timeout - device may be offline or unreachable';
    } else if (error.response) {
      errorMessage = `Error: ${error.response.data?.detail || error.response.statusText}`;
    } else if (error.message) {
      errorMessage = error.message;
    }
    
    showToastMessage(errorMessage, 'error');
    return null;
  } finally {
    showLoadingModal.value = false;
  }
}

const esp32Config = reactive({
  ipAddress: ''
})

const isValidIP = (ip) => {
  const ipRegex = /^(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
  return ipRegex.test(ip);
};

const activeModal = ref(null) 

const esp1Config = reactive({
  wifiSSID: '',
  wifiPassword: '',
  serverURL: '',
  nitrogenOffset: 0,
  phosphorusOffset: 0,
  potassiumOffset: 0,
  phOffset: 0
})

const esp2Config = reactive({
  wifiSSID: '',
  wifiPassword: '',
  apiURL: '',
  tempOffset: 0,
  humidityOffset: 0,
  wateringThreshold: 30,
  airValue: 1024,
  waterValue: 0
})

const esp3Config = reactive({
  wifiSSID: '',
  wifiPassword: '',
  apiURL: '',
  tankHeight: 0,
  alertLevel: 20,
  fullDistance: 0,
  emptyDistance: 0
})

const showPassword = reactive({
  esp1: false,
  esp2: false,
  esp3: false
})

// Tooltip visibility states
const showTooltip = reactive({
  nitrogen: false,
  phosphorus: false,
  potassium: false,
  ph: false,
  tempOffset: false,
  humidityOffset: false,
  wateringThreshold: false,
  tankHeight: false,
  alertLevel: false,
  fullDistance: false,
  emptyDistance: false
})

const savedConfigs = reactive({
  esp1: null,
  esp2: null,
  esp3: null
})

const unsubscribeFns = reactive({
  esp1: null,
  esp2: null,
  esp3: null
})

const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('info') 
const tooltipTimeout = ref(null)
const isSaving = ref(false)
const showLoadingModal = ref(false);


const saveIPAddress = async () => {
  if (!isValidIP(esp32Config.ipAddress)) {
    showToastMessage('Please enter a valid IP address', 'error');
    return;
  }

  try {
    showLoadingModal.value = true;
    const response = await api.post(
      `/esp32/ip`,
      { ip: esp32Config.ipAddress },  // Ensure this matches your backend expectation
      {
        headers: {
          'Content-Type': 'application/json'
        }
      }
    );
    
    showToastMessage(response.data.message, 'success');
    localStorage.setItem('esp32IpAddress', esp32Config.ipAddress);
  } catch (error) {
    console.error('Error details:', error.response?.data);
    showToastMessage(
      error.response?.data?.detail || 
      error.response?.data?.message || 
      'Failed to save IP address', 
      'error'
    );
  } finally {
    showLoadingModal.value = false;
  }
};

const fetchSavedIP = async () => {
  try {
    const response = await api.get(`esp32/ip`);
    if (response.data?.ip) {
      esp32Config.ipAddress = response.data.ip;
    }
  } catch (error) {
    console.error('Failed to fetch saved IP:', error);
    // Fallback to default or show message
    esp32Config.ipAddress = '192.168.1.14';
  }
};

// const testConnection = async () => {
//   if (!isValidIP(esp32Config.ipAddress)) {
//     showToastMessage('Please enter a valid IP address', 'error');
//     return;
//   }

//   try {
//     showLoadingModal.value = true;
    
//     // Check backend connection
//     const backendPing = await api.get(`/system/ping`);
//     if (!backendPing.data?.success) {
//       throw new Error('Backend service unavailable');
//     }
    
//     // Use backend proxy to test ESP32 connection
//     const connectionTest = await api.get(`/esp32/test-connection`, {
//       params: { ip_address: esp32Config.ipAddress },
//       timeout: 5000 // 5s timeout for backend+ESP32
//     });

//     showToastMessage('Connection successful to both backend and ESP32', 'success');
//     connectionStatus.connected = true;
//     connectionStatus.lastSeen = new Date().toLocaleTimeString();
    
//     // Update WiFi signal strength
//     if (connectionTest.data.signal_strength) {
//       wifiDetails.signalStrength = connectionTest.data.signal_strength;
//     }
    
//     return {
//       backend: {
//         status: 'connected',
//         version: backendPing.data.version,
//         uptime: backendPing.data.uptime
//       },
//       esp32: {
//         status: 'connected',
//         ip: esp32Config.ipAddress,
//         signalStrength: connectionTest.data.signal_strength,
//         firmware: connectionTest.data.firmware || 'unknown',
//         responseTime: connectionTest.data.response_time_ms
//       }
//     };
//   } catch (error) {
//     console.error('Connection test failed:', error);
    
//     if (error.response) {
//       // Backend returned error
//       showToastMessage(`Error: ${error.response.data?.detail || 'Connection test failed'}`, 'error');
//     } else if (error.code === 'ECONNABORTED') {
//       showToastMessage('Connection timed out', 'error');
//     } else {
//       showToastMessage(error.message, 'error');
//     }
    
//     connectionStatus.connected = false;
//     connectionStatus.lastSeen = 'Disconnected';
//     return {
//       backend: { status: 'error' },
//       esp32: { status: 'error' }
//     };
//   } finally {
//     showLoadingModal.value = false;
//   }
// };

const showDeviceInfo = async () => {
  if (!isValidIP(esp32Config.ipAddress)) {
    showToastMessage('Please enter a valid IP address', 'error');
    return;
  }

  try {
    showLoadingModal.value = true;
    
    // Get backend info
    const backendInfo = await api.get(`/system/info`);
    
    // Get ESP32 info through backend
    const espInfo = await api.get(`/esp32/device-info`, {
      params: { ip_address: esp32Config.ipAddress },
      timeout: 5000
    });

    const info = {
      backend: {
        version: backendInfo.data.version,
        status: 'running',
        uptime: formatUptime(backendInfo.data.uptime),
        lastESP32Contact: espInfo.data.last_contact || 'unknown'
      },
      esp32: {
        model: espInfo.data.model || 'ESP32',
        firmware: espInfo.data.firmware || 'unknown',
        macAddress: espInfo.data.mac || 'unknown',
        flashSize: espInfo.data.flash || 'unknown',
        freeHeap: espInfo.data.free_heap || 'unknown',
        uptime: formatUptime(espInfo.data.uptime),
        sensors: espInfo.data.sensors || [],
        sensorReadings: espInfo.data.sensor_readings || {}
      }
    };
    
    showToastMessage(
      `Device Info: ${info.esp32.model}, Firmware ${info.esp32.firmware}, ${info.esp32.flashSize} Flash`,
      'success'
    );
    
    console.log('Device Information:', info);
    return info;
  } catch (error) {
    console.error('Failed to get device info:', error);
    
    let errorMessage = 'Failed to retrieve device information';
    if (error.response) {
      errorMessage += `: ${error.response.data?.detail || error.response.statusText}`;
    } else if (error.code === 'ECONNABORTED') {
      errorMessage = 'Connection timed out (5s)';
    } else {
      errorMessage += `: ${error.message}`;
    }
    
    showToastMessage(errorMessage, 'error');
    return null;
  } finally {
    showLoadingModal.value = false;
  }
};

const formatUptime = (seconds) => {
  if (!seconds) return 'unknown';
  
  const days = Math.floor(seconds / (3600 * 24));
  const hours = Math.floor((seconds % (3600 * 24)) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  return [
    days > 0 ? `${days}d` : '',
    hours > 0 ? `${hours}h` : '',
    mins > 0 ? `${mins}m` : '',
    `${secs}s`
  ].filter(Boolean).join(' ');
};

const openModal = (esp) => {
  activeModal.value = esp;
  document.body.style.overflow = 'hidden';
}

const closeModal = () => {
  activeModal.value = null;
  // Restore body scroll when modal is closed
  document.body.style.overflow = 'auto';
}

function togglePassword(device) {
  showPassword[device] = !showPassword[device]
}

function resetTooltips() {
  Object.keys(showTooltip).forEach(key => {
    showTooltip[key] = false
  })
}

const showToastMessage = (message, severity = 'info', persistKey = null) => {
  window.showToast(message, severity)
}

onBeforeUnmount(() => {
  document.body.style.overflow = 'auto';
})

onUnmounted(() => {
  Object.values(unsubscribeFns).forEach(unsubscribe => {
    if (unsubscribe) unsubscribe()
  })
})

function formatConfigData(device, data) {
  switch(device) {
    case 'esp1':
      return {
        wifiSSID: data.wifiSSID || '',
        wifiPassword: data.wifiPassword || '',
        serverURL: data.serverURL || '',
        nitrogenOffset: data.nitrogenOffset || 0,
        phosphorusOffset: data.phosphorusOffset || 0,
        phOffset: data.phOffset || 0
      }
    case 'esp2':
      return {
        wifiSSID: data.wifiSSID || '',
        wifiPassword: data.wifiPassword || '',
        apiURL: data.apiURL || '',
        tempOffset: data.tempOffset || 0,
        humidityOffset: data.humidityOffset || 0,
        wateringThreshold: data.wateringThreshold || 30,
        airValue: data.airValue || 1024,
        waterValue: data.waterValue || 0
      }
    case 'esp3':
      return {
        wifiSSID: data.wifiSSID || '',
        wifiPassword: data.wifiPassword || '',
        apiURL: data.apiURL || '',
        tankHeight: data.tankHeight || 0,
        alertLevel: data.alertLevel || 20,
        fullDistance: data.fullDistance || 0,
        emptyDistance: data.emptyDistance || 0
      }
    default:
      return {}
  }
}

function updateFormConfig(device, configData) {
  if (!configData) return
  
  if (device === 'esp1') {
    Object.assign(esp1Config, configData)
  } else if (device === 'esp2') {
    Object.assign(esp2Config, configData)
  } else if (device === 'esp3') {
    Object.assign(esp3Config, configData)
  }
}

watch(activeModal, (newDevice) => {
  if (!newDevice) return
  
  if (savedConfigs[newDevice]) {
    updateFormConfig(newDevice, savedConfigs[newDevice])
  }
})

watch([esp1Config, esp2Config, esp3Config], ([newEsp1, newEsp2, newEsp3], [oldEsp1, oldEsp2, oldEsp3]) => {
  const configs = JSON.parse(localStorage.getItem('esp32Configurations') || '{}');
  configs.esp1 = newEsp1;
  configs.esp2 = newEsp2;
  configs.esp3 = newEsp3;
  localStorage.setItem('esp32Configurations', JSON.stringify(configs));
}, { deep: true })

// const navigateToRecalibration = (device) => {
//   let domain;
  
//   switch(device) {
//     case 'esp32-1':
//       domain = 'npkdevice.local';
//       break;
//     case 'esp32-2':
//       domain = 'esp32env.local';
//       break;
//     case 'esp32-3':
//       domain = 'waterlevel.local';
//       break;
//     default:
//       // Fallback in case of unexpected device value
//       domain = device;
//   }
  
//   // Redirect to the appropriate local domain
//   window.location.href = `http://${domain}`;
// }

// Add to your script setup
const wifiArcs = computed(() => [
  { path: 'M 30 42 Q 40 32 50 42', threshold: 25 },
  { path: 'M 22 35 Q 40 15 58 35', threshold: 50 },
  { path: 'M 14 28 Q 40 5 66 28', threshold: 75 },
  { path: 'M 6 21 Q 40 -5 74 21', threshold: 90 }
]);

const getConnectionStatus = () => {
  if (!deviceInternetStatus.isOnline) return 'Offline';
  if (deviceInternetStatus.connectionStrength < 25) return 'Very Weak';
  if (deviceInternetStatus.connectionStrength < 50) return 'Weak';
  if (deviceInternetStatus.connectionStrength < 75) return 'Good';
  if (deviceInternetStatus.connectionStrength < 90) return 'Strong';
  return 'Excellent';
};

// WiFi arc colors
const getWifiArcColor = (strength) => {
  if (!deviceInternetStatus.isOnline) return '#ef4444'; // red-500 when offline
  if (strength >= 75) return '#10b981'; // green-500
  if (strength >= 50) return '#eab308'; // yellow-500  
  if (strength >= 25) return '#f97316'; // orange-500
  return '#ef4444'; // red-500
};

const formatLastUpdated = (timestamp) => {
  if (!timestamp) return 'Never';
  
  const now = new Date();
  const updated = new Date(timestamp);
  const diffMs = now - updated;
  const diffSecs = Math.floor(diffMs / 1000);
  const diffMins = Math.floor(diffMs / 60000);
  
  if (diffSecs < 10) return 'Just now';
  if (diffSecs < 60) return `${diffSecs}s ago`;
  if (diffMins < 60) return `${diffMins}m ago`;
  
  return updated.toLocaleTimeString();
};

// Listen to online/offline events
const setupNetworkListeners = () => {
  window.addEventListener('online', () => {
    deviceInternetStatus.isOnline = true;
    checkInternetConnection();
  });
  
  window.addEventListener('offline', () => {
    deviceInternetStatus.isOnline = false;
    deviceInternetStatus.connectionStrength = 0;
    deviceInternetStatus.lastChecked = new Date();
  });
};

// Add this watch and Firestore listener
let unsubscribeNetworkListener = null;

const POLLING_INTERVAL = 5000;

// Function to fetch network details from MongoDB
const fetchNetworkDetails = async () => {
  try {
    const response = await api.get('/network/backend');
    const data = response.data;

    if (data) {
      networkDetails.ipAddress = data.ip_address || '';
      networkDetails.ssid = data.ssid || '';
      
      // Update WiFi details if available
      if (data.signal_strength) {
        wifiDetails.signalStrength = data.signal_strength;
      }
    }

    console.log(data)
  } catch (error) {
    console.error("MongoDB network error:", error);
  }
};

onMounted(() => {
  fetchSavedIP();
  fetchNetworkDetails();
  
  // Setup device internet connection monitoring
  setupNetworkListeners();
  checkInternetConnection();
  
  // Check device connections on mount
  checkAllDeviceConnections();
  
  // Set up polling for network details
  pollingIntervalId = setInterval(fetchNetworkDetails, POLLING_INTERVAL);
  
  // Set up polling for device status (every 30 seconds)
  deviceStatusIntervalId = setInterval(checkAllDeviceConnections, 30000);
  
  // Check internet connection periodically (every 60 seconds)
  internetCheckIntervalId = setInterval(checkInternetConnection, 60000);
});

onUnmounted(() => {
  // Clean up all intervals
  if (pollingIntervalId) clearInterval(pollingIntervalId);
  if (deviceStatusIntervalId) clearInterval(deviceStatusIntervalId);
  if (internetCheckIntervalId) clearInterval(internetCheckIntervalId);
});

</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: rgba(20, 83, 45, 0.1);
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: rgba(20, 83, 45, 0.5);
  border-radius: 3px;
  transition: background-color 200ms;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(20, 83, 45, 0.7);
}

* {
  transition: all 200ms ease-in-out;
}

@supports (-webkit-touch-callout: none) {
  .h-screen {
    height: -webkit-fill-available;
  }
}

* {
  scrollbar-width: thin;
  scrollbar-color: rgba(20, 83, 45, 0.5) rgba(20, 83, 45, 0.1);
}

input:focus,
button:focus {
  outline: 2px solid #3b82f6;
  outline-offset: 2px;
}

/* Added mobile scrolling optimizations for iOS Safari and smooth scrolling */
@media (max-width: 768px) {
  .overflow-y-auto {
    -webkit-overflow-scrolling: touch;
    scroll-behavior: smooth;
  }
  
  /* iOS Safari specific optimizations */
  .flex-1 {
    min-height: 0;
  }
}

/* Tooltip Animation */
.tooltip-enter-active,
.tooltip-leave-active {
  transition: all 0.2s ease;
}

.tooltip-enter-from,
.tooltip-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

.tooltip-enter-to,
.tooltip-leave-from {
  opacity: 1;
  transform: translateY(0);
}

@media (max-width: 1024px) {
  .grid-cols-1.lg\\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .grid-cols-1.lg\\:grid-cols-3 {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .grid-cols-1.md\\:grid-cols-3 {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .grid-cols-1.md\\:grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .text-lg {
    font-size: 1rem;
  }
  
  .space-x-3 > :not([hidden]) ~ :not([hidden]) {
    margin-left: 0.5rem;
  }
}

@media (max-width: 640px) {
  .max-w-2xl {
    max-width: 95vw;
  }
  
  .p-6 {
    padding: 1rem;
  }
  
  .space-x-3 {
    flex-direction: column;
    space: 0;
  }
  
  .space-x-3 > :not([hidden]) ~ :not([hidden]) {
    margin-left: 0;
    margin-top: 0.5rem;
  }

  .flex-wrap.gap-3 {
    flex-direction: column;
  }
  
  .flex-wrap.gap-3 button {
    width: 100%;
    justify-content: center;
  }
}
</style>