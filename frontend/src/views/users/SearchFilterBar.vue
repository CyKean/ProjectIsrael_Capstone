<template>
  <div class="flex gap-4 items-center p-4 bg-white rounded-xl shadow-sm">
    <!-- Search Input -->
    <div class="relative flex-1">
      <Search class="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
      <input
        type="text"
        placeholder="Search anything here..."
        class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-green-500/20 focus:border-green-500 text-sm text-gray-800 placeholder-gray-400 bg-white"
        v-model="searchQuery"
      />
    </div>

    <!-- Filter Button -->
    <div class="relative">
      <button 
        @click="toggleFilter"
        class="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-200 bg-white text-sm text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-colors duration-200"
      >
        <Filter class="h-4 w-4 text-gray-400" />
        Filter by Range
        <ChevronDown 
          class="h-4 w-4 text-gray-400 transition-transform duration-200" 
          :class="{ 'transform rotate-180': isFilterOpen }" 
        />
      </button>
      
      <!-- Filter Dropdown (if needed) -->
      <div v-if="isFilterOpen" class="absolute top-full right-0 mt-2 w-64 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
        <!-- Add your filter options here -->
      </div>
    </div>

    <!-- Sort Button -->
    <div class="relative">
      <button 
        @click="toggleSort"
        class="flex items-center gap-2 px-4 py-2 rounded-lg border border-gray-200 bg-white text-sm text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-colors duration-200"
      >
        Sort by
        <ChevronDown 
          class="h-4 w-4 text-gray-400 transition-transform duration-200" 
          :class="{ 'transform rotate-180': isSortOpen }" 
        />
      </button>
      
      <!-- Sort Dropdown (if needed) -->
      <div v-if="isSortOpen" class="absolute top-full right-0 mt-2 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50">
        <!-- Add your sort options here -->
      </div>
    </div>

    <!-- Export Button -->
    <button 
      @click="handleExport"
      class="flex items-center gap-2 px-4 py-2 rounded-lg bg-emerald-500 hover:bg-emerald-600 text-white text-sm font-medium shadow-sm transition-all duration-200 hover:shadow active:transform active:scale-95"
    >
      <Download class="h-4 w-4" />
      Export
      <ChevronDown class="h-4 w-4" />
    </button>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { Search, Filter, ChevronDown, Download } from 'lucide-vue-next'

const searchQuery = ref('')
const isFilterOpen = ref(false)
const isSortOpen = ref(false)

const toggleFilter = () => {
  isFilterOpen.value = !isFilterOpen.value
  if (isFilterOpen.value) isSortOpen.value = false
}

const toggleSort = () => {
  isSortOpen.value = !isSortOpen.value
  if (isSortOpen.value) isFilterOpen.value = false
}

const handleExport = () => {
  console.log('Export clicked')
}

// Close dropdowns when clicking outside
const closeDropdowns = (event) => {
  if (!event.target.closest('.relative')) {
    isFilterOpen.value = false
    isSortOpen.value = false
  }
}

// Add event listener when component is mounted
onMounted(() => {
  document.addEventListener('click', closeDropdowns)
})

// Remove event listener when component is unmounted
onUnmounted(() => {
  document.removeEventListener('click', closeDropdowns)
})
</script>

<style scoped>
/* Optional: Add transition for smoother dropdown animations */
.absolute {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

/* Ensure dropdowns are above other content */
.z-50 {
  z-index: 50;
}
</style>
