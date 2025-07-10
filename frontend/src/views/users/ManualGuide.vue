<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Beautiful Header -->
    <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <button 
              @click="goBack" 
              class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <ArrowLeft class="h-5 w-5 text-gray-600" />
            </button>
            <div class="flex items-center space-x-3">
              <div class="p-2 bg-emerald-500 rounded-lg">
                <BookOpen class="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 class="text-lg font-semibold text-gray-900">Manual Guide</h1>
                <p class="text-sm text-gray-500">Project Israel</p>
              </div>
            </div>
          </div>
          <div class="flex items-center space-x-3">
            <div class="relative">
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search..."
                class="w-64 px-4 py-2 bg-gray-100 rounded-lg border-0 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:bg-white transition-all"
                @input="handleSearch"
              />
              <Search class="absolute right-3 top-2.5 h-4 w-4 text-gray-400" />
            </div>
            <button @click="handleDownload" class="p-2 rounded-lg hover:bg-gray-100 transition-colors">
              <Download class="h-5 w-5 text-gray-600" />
            </button>
            <div class="w-8 h-8 bg-gray-300 rounded-full"></div>
          </div>
        </div>
      </div>
    </header>

    <div class="max-w-7xl mx-auto px-6 py-6">
      <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <!-- Beautiful Sidebar -->
        <div class="lg:col-span-1 space-y-6">
          <!-- Navigation Card -->
          <div class="bg-white rounded-xl border border-gray-200 p-6">
            <div class="flex items-center space-x-2 mb-4">
              <div class="w-2 h-2 bg-blue-500 rounded-full"></div>
              <h2 class="font-semibold text-gray-900">Quick Navigation</h2>
            </div>
            <nav class="space-y-1">
              <button
                v-for="section in sections"
                :key="section.id"
                @click="activeSection = section.id"
                :class="[
                  'w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-all flex items-center space-x-3 hover:scale-105',
                  activeSection === section.id
                    ? 'bg-emerald-500 text-white'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900 hover:shadow-md hover:border-l-4 hover:border-emerald-500'
                ]"
              >
                <component :is="section.icon" class="h-4 w-4" />
                <span>{{ section.title }}</span>
              </button>
            </nav>
          </div>

          <!-- System Metrics Slideshow Card -->
          <div class="bg-white rounded-xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-all">
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-semibold text-gray-900">System Metrics</h3>
              <div class="flex space-x-1">
                <div 
                  v-for="(_, index) in 4" 
                  :key="index"
                  :class="[
                    'w-2 h-2 rounded-full transition-colors duration-300',
                    currentMetricIndex === index ? 'bg-emerald-500' : 'bg-gray-300'
                  ]"
                ></div>
              </div>
            </div>
            
            <!-- Beautiful Slideshow Container with Seamless Backgrounds -->
            <div class="relative rounded-lg h-24 overflow-hidden">
              <!-- Slide 1: 8 Sections - Agriculture/Greenhouse Theme -->
              <div 
                v-show="currentMetricIndex === 0"
                class="absolute inset-0 bg-gradient-to-br from-emerald-400 via-emerald-500 to-green-600 flex flex-col justify-center items-center transition-opacity duration-500"
                :class="currentMetricIndex === 0 ? 'opacity-100' : 'opacity-0'"
              >
                <!-- Background Pattern -->
                <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
                <div class="absolute top-2 right-2 opacity-20">
                  <Cpu class="h-6 w-6 text-white" />
                </div>
                <div class="relative text-center text-white z-10">
                  <div class="text-3xl font-bold mb-1">1</div>
                  <div class="text-sm font-medium opacity-90">Greenhouse</div>
                </div>
              </div>

              <!-- Slide 2: 24/7 Monitoring - Monitoring/Tech Theme -->
              <div 
                v-show="currentMetricIndex === 1"
                class="absolute inset-0 bg-gradient-to-br from-blue-400 via-blue-500 to-indigo-600 flex flex-col justify-center items-center transition-opacity duration-500"
                :class="currentMetricIndex === 1 ? 'opacity-100' : 'opacity-0'"
              >
                <!-- Background Pattern -->
                <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
                <div class="absolute top-2 right-2 opacity-20">
                  <Monitor class="h-6 w-6 text-white" />
                </div>
                <div class="relative text-center text-white z-10">
                  <div class="text-3xl font-bold mb-1">24/7</div>
                  <div class="text-sm font-medium opacity-90">Monitoring</div>
                </div>
              </div>

              <!-- Slide 3: AI Powered - AI/Tech Theme -->
              <div 
                v-show="currentMetricIndex === 2"
                class="absolute inset-0 bg-gradient-to-br from-purple-400 via-purple-500 to-violet-600 flex flex-col justify-center items-center transition-opacity duration-500"
                :class="currentMetricIndex === 2 ? 'opacity-100' : 'opacity-0'"
              >
                <!-- Background Pattern -->
                <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
                <div class="absolute top-2 right-2 opacity-20">
                  <Zap class="h-6 w-6 text-white" />
                </div>
                <div class="relative text-center text-white z-10">
                  <div class="text-3xl font-bold mb-1">ML</div>
                  <div class="text-sm font-medium opacity-90">Powered</div>
                </div>
              </div>

              <!-- Slide 4: 100% Reliable - Security/Reliability Theme -->
              <div 
                v-show="currentMetricIndex === 3"
                class="absolute inset-0 bg-gradient-to-br from-orange-400 via-orange-500 to-red-500 flex flex-col justify-center items-center transition-opacity duration-500"
                :class="currentMetricIndex === 3 ? 'opacity-100' : 'opacity-0'"
              >
                <!-- Background Pattern -->
                <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-transparent"></div>
                <div class="absolute top-2 right-2 opacity-20">
                  <Shield class="h-6 w-6 text-white" />
                </div>
                <div class="relative text-center text-white z-10">
                  <div class="text-3xl font-bold mb-1">100%</div>
                  <div class="text-sm font-medium opacity-90">Reliable</div>
                </div>
              </div>
              
              <!-- Navigation Arrows - Now properly integrated -->
              <button 
                @click="previousMetric"
                class="absolute left-2 top-1/2 transform -translate-y-1/2 p-1.5 rounded-full bg-black/20 backdrop-blur-sm hover:bg-black/30 transition-all z-30"
              >
                <ChevronLeft class="h-4 w-4 text-white" />
              </button>
              <button 
                @click="nextMetric"
                class="absolute right-2 top-1/2 transform -translate-y-1/2 p-1.5 rounded-full bg-black/20 backdrop-blur-sm hover:bg-black/30 transition-all z-30"
              >
                <ChevronRight class="h-4 w-4 text-white" />
              </button>
            </div>
          </div>
        </div>

        <!-- Beautiful Main Content -->
        <div class="lg:col-span-3">
          <!-- Welcome Section -->
          <div v-if="activeSection === 'welcome'" class="space-y-6">
            <!-- Beautiful Hero Card - More Standard Size -->
            <div class="bg-gradient-to-r from-emerald-500 to-teal-600 rounded-xl p-6 text-white hover:shadow-lg hover:shadow-emerald-200 transition-all">
              <div class="flex items-center space-x-3">
                <div class="bg-white/20 p-2.5 rounded-lg">
                  <BookOpen class="h-5 w-5" />
                </div>
                <div>
                  <h1 class="text-xl font-bold mb-1">Manual Guide</h1>
                  <h2 class="text-lg font-semibold text-emerald-100">Project Israel</h2>
                  <p class="text-sm text-emerald-100">Agricultural monitoring and management system</p>
                </div>
              </div>
              <div class="flex items-center space-x-3 mt-4">
                <div class="flex items-center space-x-2 bg-white/20 rounded-full px-3 py-1">
                  <Zap class="h-3.5 w-3.5" />
                  <span class="text-xs font-medium">Machine Learning</span>
                </div>
                <div class="flex items-center space-x-2 bg-white/20 rounded-full px-3 py-1">
                  <Clock class="h-3.5 w-3.5" />
                  <span class="text-xs font-medium">Real-time</span>
                </div>
                <div class="flex items-center space-x-2 bg-white/20 rounded-full px-3 py-1">
                  <Monitor class="h-3.5 w-3.5" />
                  <span class="text-xs font-medium">24/7 Monitoring</span>
                </div>
              </div>
            </div>

            <!-- Beautiful Feature Cards with Enhanced Hover Effects -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div 
                v-for="feature in welcomeFeatures" 
                :key="feature.id"
                class="feature-card bg-white rounded-xl border border-gray-200 p-6 cursor-pointer transition-all duration-300 hover:shadow-lg relative overflow-hidden group"
                :class="`hover:border-${feature.hoverColor} hover:shadow-${feature.hoverColor}-100`"
                @click="activeSection = feature.id"
              >
                <!-- Colored border effect on hover -->
                <div :class="`absolute inset-x-0 top-0 h-1 transform scale-x-0 origin-left transition-transform duration-300 group-hover:scale-x-100 ${feature.hoverColor}`"></div>
                
                <div class="flex items-center space-x-3 mb-4">
                  <div :class="['p-2 rounded-lg transition-all duration-300 group-hover:scale-110', feature.bgColor]">
                    <component :is="feature.icon" class="h-5 w-5 text-white" />
                  </div>
                  <h3 class="font-semibold text-gray-900">{{ feature.title }}</h3>
                </div>
                <p class="text-gray-600 text-sm mb-4">{{ feature.description }}</p>
                <div class="flex items-center text-sm font-medium transition-all duration-300" :class="`text-${feature.textColor} group-hover:text-${feature.hoverTextColor}`">
                  <span>Get Started</span>
                  <ArrowRight class="h-4 w-4 ml-1 transition-transform duration-300 group-hover:translate-x-1" />
                </div>
              </div>
            </div>
          </div>

          <!-- System Overview Section -->
          <div v-if="activeSection === 'overview'" class="space-y-6">
            <div class="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg hover:border-blue-300 hover:shadow-blue-100 transition-all">
              <div class="flex items-center space-x-3 mb-6">
                <div class="p-2 bg-blue-500 rounded-lg">
                  <Monitor class="h-5 w-5 text-white" />
                </div>
                <div>
                  <h2 class="text-xl font-semibold text-gray-900">System Overview</h2>
                  <p class="text-gray-500">Understanding your dashboard</p>
                </div>
              </div>
              
              <div class="space-y-6">
                <div class="border-l-4 border-blue-500 pl-4">
                  <h3 class="font-semibold text-gray-900 mb-2">Dashboard Navigation</h3>
                  <p class="text-gray-600 mb-4">The main dashboard provides real-time monitoring with these sections:</p>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div 
                      v-for="nav in navigationItems" 
                      :key="nav.name" 
                      class="flex items-center space-x-2 p-3 bg-gray-50 rounded-lg transition-all duration-300 hover:shadow-md hover:bg-white hover:scale-105"
                      :class="`hover:border-l-4 hover:border-${nav.hoverColor}`"
                    >
                      <div :class="['w-2 h-2 rounded-full', nav.color]"></div>
                      <div>
                        <span class="font-medium text-gray-900">{{ nav.name }}</span>
                        <p class="text-sm text-gray-600">{{ nav.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Other Sections -->
          <div v-if="activeSection !== 'welcome' && activeSection !== 'overview'" class="space-y-6">
            <div class="bg-white rounded-xl border border-gray-200 p-6 hover:shadow-lg transition-all" :class="`hover:border-${getSectionColor(activeSection)}-300 hover:shadow-${getSectionColor(activeSection)}-100`">
              <div class="flex items-center space-x-3 mb-6">
                <div class="p-2 rounded-lg transition-all" :class="`bg-${getSectionColor(activeSection)}-500`">
                  <component :is="getCurrentSectionIcon()" class="h-5 w-5 text-white" />
                </div>
                <div>
                  <h2 class="text-xl font-semibold text-gray-900">{{ getCurrentSectionTitle() }}</h2>
                  <p class="text-gray-500">Comprehensive guide and instructions</p>
                </div>
              </div>
              
              <div class="text-center py-12">
                <div class="p-4 bg-gray-100 rounded-lg inline-block mb-4 transition-transform hover:scale-110 hover:shadow-md">
                  <component :is="getCurrentSectionIcon()" class="h-8 w-8 text-gray-600" />
                </div>
                <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ getCurrentSectionTitle() }}</h3>
                <p class="text-gray-600 max-w-md mx-auto">
                  Detailed content for this section is being prepared with step-by-step instructions.
                </p>
                <button class="mt-4 px-4 py-2 text-white rounded-lg transition-all hover:shadow-md hover:scale-105" :class="`bg-${getSectionColor(activeSection)}-500 hover:bg-${getSectionColor(activeSection)}-600`">
                  Coming Soon
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Beautiful Floating Button -->
    <div class="fixed bottom-6 right-6">
      <button class="p-3 bg-emerald-500 text-white rounded-full shadow-lg hover:bg-emerald-600 hover:scale-110 transition-all">
        <HelpCircle class="h-5 w-5" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ArrowLeft, Search, Download, BookOpen, Monitor, Cpu, TrendingUp,
  Droplets, Settings, BarChart3, HelpCircle, ArrowRight, Zap, Clock,
  ChevronLeft, ChevronRight, Shield
} from 'lucide-vue-next'

const router = useRouter()
const activeSection = ref('welcome')
const currentMetricIndex = ref(0)
const searchQuery = ref('')
let slideInterval = null

const sections = [
  { id: 'welcome', title: 'Welcome', icon: BookOpen },
  { id: 'overview', title: 'System Overview', icon: Monitor },
  { id: 'crop-prediction', title: 'Crop Prediction', icon: TrendingUp },
  { id: 'weather', title: 'Weather Forecasting', icon: Droplets },
  { id: 'device-control', title: 'Device Control', icon: Settings },
  { id: 'soil-analysis', title: 'Soil Analysis', icon: BarChart3 },
  { id: 'hardware', title: 'Hardware Setup', icon: Cpu },
  { id: 'troubleshooting', title: 'Troubleshooting', icon: HelpCircle }
]

const welcomeFeatures = [
  {
    id: 'overview',
    title: 'System Overview',
    description: 'Learn about the main dashboard and navigation.',
    icon: Monitor,
    bgColor: 'bg-blue-500',
    hoverColor: 'bg-blue-500',
    textColor: 'blue-600',
    hoverTextColor: 'blue-700'
  },
  {
    id: 'hardware',
    title: 'Hardware Setup',
    description: 'Configure your ESP32 sensors and devices.',
    icon: Cpu,
    bgColor: 'bg-green-500',
    hoverColor: 'bg-green-500',
    textColor: 'green-600',
    hoverTextColor: 'green-700'
  },
  {
    id: 'crop-prediction',
    title: 'AI Predictions',
    description: 'Understand crop yield forecasting.',
    icon: TrendingUp,
    bgColor: 'bg-purple-500',
    hoverColor: 'bg-purple-500',
    textColor: 'purple-600',
    hoverTextColor: 'purple-700'
  },
  {
    id: 'device-control',
    title: 'Device Control',
    description: 'Manage your IoT devices remotely.',
    icon: Settings,
    bgColor: 'bg-orange-500',
    hoverColor: 'bg-orange-500',
    textColor: 'orange-600',
    hoverTextColor: 'orange-700'
  }
]

const stats = [
  { value: '8', label: 'Sections' },
  { value: '24/7', label: 'Monitoring' },
  { value: 'AI', label: 'Powered' },
  { value: '100%', label: 'Reliable' }
]

const navigationItems = [
  { name: 'Overview', description: 'Main dashboard', color: 'bg-emerald-500', hoverColor: 'emerald-500' },
  { name: 'Crop Prediction', description: 'AI forecasting', color: 'bg-blue-500', hoverColor: 'blue-500' },
  { name: 'Weather', description: 'Weather data', color: 'bg-purple-500', hoverColor: 'purple-500' },
  { name: 'Device Control', description: 'IoT management', color: 'bg-orange-500', hoverColor: 'orange-500' },
  { name: 'Soil Analysis', description: 'Soil data', color: 'bg-green-500', hoverColor: 'green-500' },
  { name: 'Sensor Data', description: 'Live readings', color: 'bg-red-500', hoverColor: 'red-500' }
]

const getSectionColor = (sectionId) => {
  const colorMap = {
    'welcome': 'emerald',
    'overview': 'blue',
    'crop-prediction': 'purple',
    'weather': 'sky',
    'device-control': 'orange',
    'soil-analysis': 'green',
    'hardware': 'teal',
    'troubleshooting': 'red'
  }
  return colorMap[sectionId] || 'emerald'
}

const getStatColor = (index) => {
  const colors = ['text-emerald-600', 'text-blue-600', 'text-purple-600', 'text-orange-600']
  return colors[index] || 'text-gray-600'
}

const getCurrentSectionTitle = () => {
  const section = sections.find(s => s.id === activeSection.value)
  return section ? section.title : 'Welcome'
}

const getCurrentSectionIcon = () => {
  const section = sections.find(s => s.id === activeSection.value)
  return section ? section.icon : BookOpen
}

const nextMetric = () => {
  currentMetricIndex.value = (currentMetricIndex.value + 1) % 4
}

const previousMetric = () => {
  currentMetricIndex.value = currentMetricIndex.value === 0 ? 3 : currentMetricIndex.value - 1
}

const handleSearch = () => {
  console.log('Searching for:', searchQuery.value)
  if (searchQuery.value.trim()) {
    const matchingSection = sections.find(section => 
      section.title.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
    if (matchingSection) {
      activeSection.value = matchingSection.id
    }
  }
}

const handleDownload = () => {
  console.log('Downloading manual guide...')
  const content = `Manual Guide - Project Israel
  
Agricultural Monitoring and Management System

Sections:
${sections.map(section => `- ${section.title}`).join('\n')}

System Metrics:
${stats.map(stat => `- ${stat.label}: ${stat.value}`).join('\n')}

Generated on: ${new Date().toLocaleDateString()}
`
  
  const element = document.createElement('a')
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(content))
  element.setAttribute('download', 'project-israel-manual-guide.txt')
  element.style.display = 'none'
  document.body.appendChild(element)
  element.click()
  document.body.removeChild(element)
}

const startSlideshow = () => {
  if (slideInterval) {
    clearInterval(slideInterval)
  }
  slideInterval = setInterval(() => {
    nextMetric()
  }, 3000)
}

const stopSlideshow = () => {
  if (slideInterval) {
    clearInterval(slideInterval)
  }
}

const goBack = () => {
  router.go(-1)
}

onMounted(() => {
  startSlideshow()
})

onUnmounted(() => {
  stopSlideshow()
})
</script>

<style scoped>
/* Beautiful transitions */
* {
  transition: all 0.2s ease;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}

/* Focus styles */
button:focus-visible {
  outline: 2px solid #10b981;
  outline-offset: 2px;
}

/* Feature card hover effects */
.feature-card:hover {
  transform: translateY(-3px);
}

/* Fix for dynamic class binding in Vue with Tailwind */
.bg-blue-500 { background-color: #3b82f6; }
.bg-green-500 { background-color: #22c55e; }
.bg-purple-500 { background-color: #a855f7; }
.bg-orange-500 { background-color: #f97316; }
.bg-emerald-500 { background-color: #10b981; }
.bg-red-500 { background-color: #ef4444; }
.bg-sky-500 { background-color: #0ea5e9; }
.bg-teal-500 { background-color: #14b8a6; }

.text-blue-600 { color: #2563eb; }
.text-green-600 { color: #16a34a; }
.text-purple-600 { color: #9333ea; }
.text-orange-600 { color: #ea580c; }
.text-emerald-600 { color: #059669; }
.text-red-600 { color: #dc2626; }
.text-sky-600 { color: #0284c7; }
.text-teal-600 { color: #0d9488; }

.text-blue-700 { color: #1d4ed8; }
.text-green-700 { color: #15803d; }
.text-purple-700 { color: #7e22ce; }
.text-orange-700 { color: #c2410c; }
.text-emerald-700 { color: #047857; }
.text-red-700 { color: #b91c1c; }
.text-sky-700 { color: #0369a1; }
.text-teal-700 { color: #0f766e; }

.hover\:border-blue-500:hover { border-color: #3b82f6; }
.hover\:border-green-500:hover { border-color: #22c55e; }
.hover\:border-purple-500:hover { border-color: #a855f7; }
.hover\:border-orange-500:hover { border-color: #f97316; }
.hover\:border-emerald-500:hover { border-color: #10b981; }
.hover\:border-red-500:hover { border-color: #ef4444; }
.hover\:border-sky-500:hover { border-color: #0ea5e9; }
.hover\:border-teal-500:hover { border-color: #14b8a6; }

.hover\:border-blue-300:hover { border-color: #93c5fd; }
.hover\:border-green-300:hover { border-color: #86efac; }
.hover\:border-purple-300:hover { border-color: #d8b4fe; }
.hover\:border-orange-300:hover { border-color: #fdba74; }
.hover\:border-emerald-300:hover { border-color: #6ee7b7; }
.hover\:border-red-300:hover { border-color: #fca5a5; }
.hover\:border-sky-300:hover { border-color: #7dd3fc; }
.hover\:border-teal-300:hover { border-color: #5eead4; }

.hover\:shadow-blue-100:hover { --tw-shadow-color: #dbeafe; }
.hover\:shadow-green-100:hover { --tw-shadow-color: #dcfce7; }
.hover\:shadow-purple-100:hover { --tw-shadow-color: #f3e8ff; }
.hover\:shadow-orange-100:hover { --tw-shadow-color: #ffedd5; }
.hover\:shadow-emerald-100:hover { --tw-shadow-color: #d1fae5; }
.hover\:shadow-red-100:hover { --tw-shadow-color: #fee2e2; }
.hover\:shadow-sky-100:hover { --tw-shadow-color: #e0f2fe; }
.hover\:shadow-teal-100:hover { --tw-shadow-color: #ccfbf1; }
</style>
