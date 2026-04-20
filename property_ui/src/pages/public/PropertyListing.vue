<template>
  <div>
    <!-- Page Header -->
    <section class="bg-gradient-to-r from-property-blue to-property-blue-600 text-white py-12">
      <div class="container mx-auto px-4">
        <h1 class="text-4xl font-bold mb-2">Browse Properties</h1>
        <p class="text-blue-100">Find your perfect property from our extensive collection</p>
      </div>
    </section>

    <!-- Filters & Listings -->
    <section class="py-8 bg-property-bg-base min-h-screen">
      <div class="container mx-auto px-4">
        <div class="flex flex-col lg:flex-row gap-6">
          <!-- Filters Sidebar -->
          <aside class="lg:w-64 flex-shrink-0">
            <div class="bg-white rounded-property-lg p-6 shadow-sm sticky top-20">
              <h3 class="text-lg font-semibold text-property-ink mb-4">Filters</h3>
              
              <!-- Property Type -->
              <div class="mb-6">
                <label class="block text-sm font-medium text-property-body mb-2">Property Type</label>
                <select 
                  v-model="filters.property_type"
                  class="w-full px-3 py-2 border border-property-border rounded-lg focus:outline-none focus:ring-2 focus:ring-property-blue"
                >
                  <option value="">All Types</option>
                  <option value="Apartment">Apartment</option>
                  <option value="Villa">Villa</option>
                  <option value="Commercial">Commercial</option>
                  <option value="Plot">Plot</option>
                </select>
              </div>

              <!-- Bedrooms -->
              <div class="mb-6">
                <label class="block text-sm font-medium text-property-body mb-2">Bedrooms</label>
                <select 
                  v-model="filters.bedrooms"
                  class="w-full px-3 py-2 border border-property-border rounded-lg focus:outline-none focus:ring-2 focus:ring-property-blue"
                >
                  <option value="">Any</option>
                  <option value="1">1 BHK</option>
                  <option value="2">2 BHK</option>
                  <option value="3">3 BHK</option>
                  <option value="4">4+ BHK</option>
                </select>
              </div>

              <!-- Price Range -->
              <div class="mb-6">
                <label class="block text-sm font-medium text-property-body mb-2">Price Range</label>
                <select 
                  v-model="filters.price_range"
                  class="w-full px-3 py-2 border border-property-border rounded-lg focus:outline-none focus:ring-2 focus:ring-property-blue"
                >
                  <option value="">Any Price</option>
                  <option value="0-5000000">Under ₹50 Lac</option>
                  <option value="5000000-10000000">₹50 Lac - ₹1 Cr</option>
                  <option value="10000000-20000000">₹1 Cr - ₹2 Cr</option>
                  <option value="20000000-50000000">₹2 Cr - ₹5 Cr</option>
                  <option value="50000000-999999999">Above ₹5 Cr</option>
                </select>
              </div>

              <!-- Location -->
              <div class="mb-6">
                <label class="block text-sm font-medium text-property-body mb-2">Location</label>
                <input 
                  v-model="filters.location"
                  type="text"
                  placeholder="Enter location..."
                  class="w-full px-3 py-2 border border-property-border rounded-lg focus:outline-none focus:ring-2 focus:ring-property-blue"
                />
              </div>

              <!-- Apply Filters Button -->
              <Button 
                @click="applyFilters" 
                variant="solid" 
                class="w-full mb-2"
                :loading="properties.loading"
              >
                Apply Filters
              </Button>

              <!-- Clear Filters -->
              <button 
                @click="clearFilters"
                class="w-full text-center text-sm text-property-body hover:text-property-blue transition-colors"
              >
                Clear All Filters
              </button>
            </div>
          </aside>

          <!-- Property Grid -->
          <div class="flex-1">
            <!-- Results Count -->
            <div class="flex items-center justify-between mb-6">
              <div class="text-property-body">
                <span v-if="properties.data">
                  Showing {{ properties.data.length }} properties
                </span>
              </div>
              
              <!-- Sort -->
              <select 
                v-model="sortBy"
                @change="applyFilters"
                class="px-3 py-2 border border-property-border rounded-lg focus:outline-none focus:ring-2 focus:ring-property-blue text-sm"
              >
                <option value="newest">Newest First</option>
                <option value="price_low">Price: Low to High</option>
                <option value="price_high">Price: High to Low</option>
              </select>
            </div>

            <!-- Loading State -->
            <div v-if="properties.loading" class="text-center py-12">
              <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-property-blue"></div>
              <p class="text-property-body mt-4">Loading properties...</p>
            </div>

            <!-- Properties Grid -->
            <div v-else-if="properties.data?.length" class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
              <PropertyCard 
                v-for="property in properties.data" 
                :key="property.name"
                :property="property"
              />
            </div>

            <!-- Empty State -->
            <div v-else class="text-center py-12 bg-white rounded-property-lg">
              <svg class="w-16 h-16 text-property-hint mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
              </svg>
              <h3 class="text-xl font-semibold text-property-ink mb-2">No Properties Found</h3>
              <p class="text-property-body mb-4">Try adjusting your filters to see more results</p>
              <Button @click="clearFilters" variant="outline">Clear Filters</Button>
            </div>

            <!-- Load More (if needed) -->
            <div v-if="properties.data?.length && hasMore" class="text-center mt-8">
              <Button @click="loadMore" variant="outline" :loading="loadingMore">
                Load More Properties
              </Button>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { createResource } from 'frappe-ui'
import PropertyCard from '@/components/PropertyCard.vue'

const filters = reactive({
  property_type: '',
  bedrooms: '',
  price_range: '',
  location: ''
})

const sortBy = ref('newest')
const hasMore = ref(false)
const loadingMore = ref(false)

const properties = createResource({
  url: 'property_management.api.get_properties',
  params: {
    filters: {},
    sort_by: 'newest'
  },
  auto: true
})

const applyFilters = () => {
  const filterParams = {}
  
  if (filters.property_type) {
    filterParams.property_type = filters.property_type
  }
  
  if (filters.bedrooms) {
    filterParams.bedrooms = filters.bedrooms
  }
  
  if (filters.price_range) {
    const [min, max] = filters.price_range.split('-')
    filterParams.price_min = min
    filterParams.price_max = max
  }
  
  if (filters.location) {
    filterParams.location = filters.location
  }

  properties.update({
    params: {
      filters: filterParams,
      sort_by: sortBy.value
    }
  })
  properties.reload()
}

const clearFilters = () => {
  filters.property_type = ''
  filters.bedrooms = ''
  filters.price_range = ''
  filters.location = ''
  sortBy.value = 'newest'
  applyFilters()
}

const loadMore = () => {
  loadingMore.value = true
  // Implement pagination logic here
  setTimeout(() => {
    loadingMore.value = false
  }, 1000)
}

onMounted(() => {
  // Check URL params for filters
  const urlParams = new URLSearchParams(window.location.search)
  if (urlParams.get('type')) {
    filters.property_type = urlParams.get('type')
    applyFilters()
  }
})
</script>
