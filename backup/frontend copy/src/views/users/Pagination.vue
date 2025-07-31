<template>
  <div class="bg-gray-50/50 border-t border-gray-200 px-8 py-[-10px] flex items-center justify-between">
    <div class="flex items-center mt-4">
      <span class="text-base text-gray-600 mr-3 ">Items per page</span>
      <select 
        v-model="localItemsPerPage" 
        class="border border-gray-200 rounded-md text-base py-2 pl-4 pr-10 focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500 bg-white"
        @change="$emit('update:itemsPerPage', localItemsPerPage)"
      >
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="30">30</option>
        <option value="40">40</option>
        <option value="50">50</option>
      </select>
    </div>

    <div class="flex items-center space-x-[-5px] mt-4">
      <button 
        @click="$emit('previous')"
        :disabled="currentPage === 1"
        class="px-4 py-2 text-base text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
      >
        Previous
      </button>
      
      <div class="flex items-center">
        <template v-for="page in displayedPages" :key="page">
          <button 
            v-if="page !== '...'"
            @click="$emit('update:currentPage', page)"
            :class="[
              'min-w-[40px] h-10 flex items-center justify-center rounded text-base mx-1 transition-colors duration-150',
              currentPage === page 
                ? 'bg-gray-900 text-white' 
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            {{ page }}
          </button>
          <span v-else class="px-2 text-gray-400 text-base">...</span>
        </template>
      </div>

      <button 
        @click="$emit('next')"
        :disabled="currentPage === totalPages"
        class="px-4 py-2 text-base text-gray-600 hover:text-gray-900 disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
      >
        <span>Next</span>
        <svg 
          class="w-5 h-5 ml-1" 
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path 
            stroke-linecap="round" 
            stroke-linejoin="round" 
            stroke-width="2" 
            d="M9 5l7 7-7 7"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  itemsPerPage: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:currentPage', 'update:itemsPerPage', 'previous', 'next'])

const localItemsPerPage = ref(props.itemsPerPage)

const displayedPages = computed(() => {
  const pages = []
  const maxVisiblePages = 7 // Show more page numbers
  
  if (props.totalPages <= maxVisiblePages) {
    for (let i = 1; i <= props.totalPages; i++) {
      pages.push(i)
    }
  } else {
    pages.push(1)
    
    if (props.currentPage > 4) {
      pages.push('...')
    }
    
    const start = Math.max(2, props.currentPage - 2)
    const end = Math.min(props.totalPages - 1, props.currentPage + 2)
    
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
    
    if (props.currentPage < props.totalPages - 3) {
      pages.push('...')
    }
    
    pages.push(props.totalPages)
  }
  
  return pages
})
</script>

<style scoped>
select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.75rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
  -webkit-print-color-adjust: exact;
  print-color-adjust: exact;
  appearance: none;
}
</style>