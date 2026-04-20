<template>
  <div class="bg-white rounded-property-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow border border-property-border group">
    <!-- Image -->
    <div class="relative h-48 overflow-hidden bg-gray-200">
      <img 
        v-if="property.image" 
        :src="property.image" 
        :alt="property.name"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <div v-else class="w-full h-full flex items-center justify-center bg-gradient-to-br from-property-blue-100 to-property-blue-200">
        <svg class="w-16 h-16 text-property-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
        </svg>
      </div>
      
      <!-- Status Badge -->
      <div v-if="property.status" class="absolute top-3 left-3">
        <span 
          class="px-3 py-1 rounded-full text-xs font-semibold"
          :class="statusClass"
        >
          {{ property.status }}
        </span>
      </div>

      <!-- WhatsApp Quick Action -->
      <a 
        :href="whatsappUrl"
        target="_blank"
        rel="noopener noreferrer"
        class="absolute top-3 right-3 w-10 h-10 bg-green-500 hover:bg-green-600 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity shadow-lg"
        @click.stop
      >
        <svg class="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 24 24">
          <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
        </svg>
      </a>
    </div>

    <!-- Content -->
    <router-link :to="`/properties/${property.name}`" class="block p-4">
      <h3 class="text-lg font-semibold text-property-ink mb-2 group-hover:text-property-blue transition-colors line-clamp-1">
        {{ property.title || property.name }}
      </h3>
      
      <!-- Location -->
      <div class="flex items-center text-property-body text-sm mb-3">
        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
        <span class="line-clamp-1">{{ property.location || 'Location not specified' }}</span>
      </div>

      <!-- Price -->
      <div class="text-2xl font-bold text-property-blue mb-3">
        {{ formatPrice(property.price) }}
      </div>

      <!-- Specs -->
      <div class="flex items-center justify-between text-sm text-property-body border-t border-property-border pt-3">
        <div v-if="property.bedrooms" class="flex items-center">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <span>{{ property.bedrooms }} BHK</span>
        </div>
        
        <div v-if="property.area" class="flex items-center">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
          </svg>
          <span>{{ property.area }} sqft</span>
        </div>
        
        <div v-if="property.property_type" class="flex items-center">
          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <span>{{ property.property_type }}</span>
        </div>
      </div>
    </router-link>

    <!-- View Details Button -->
    <div class="px-4 pb-4">
      <router-link 
        :to="`/properties/${property.name}`"
        class="block w-full text-center px-4 py-2 bg-property-blue text-white rounded-lg hover:bg-property-blue-600 transition-colors font-medium"
      >
        View Details
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  property: {
    type: Object,
    required: true
  }
})

const statusClass = computed(() => {
  const status = props.property.status?.toLowerCase()
  if (status === 'available' || status === 'for sale') {
    return 'bg-green-500 text-white'
  } else if (status === 'sold') {
    return 'bg-red-500 text-white'
  } else if (status === 'reserved') {
    return 'bg-yellow-500 text-white'
  }
  return 'bg-gray-500 text-white'
})

const formatPrice = (price) => {
  if (!price) return 'Price on request'
  
  // Convert to number if string
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  
  if (numPrice >= 10000000) {
    return `₹${(numPrice / 10000000).toFixed(2)} Cr`
  } else if (numPrice >= 100000) {
    return `₹${(numPrice / 100000).toFixed(2)} Lac`
  }
  return `₹${numPrice.toLocaleString('en-IN')}`
}

const whatsappUrl = computed(() => {
  const message = `Hi! I'm interested in ${props.property.title || props.property.name}. Please provide more details.`
  return `https://wa.me/911234567890?text=${encodeURIComponent(message)}`
})
</script>
