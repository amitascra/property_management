<template>
  <div>
    <div v-if="property.loading" class="container mx-auto px-4 py-12 text-center">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-property-blue"></div>
      <p class="text-property-body mt-4">Loading property details...</p>
    </div>

    <div v-else-if="property.data" class="bg-property-bg-base">
      <!-- Image Gallery -->
      <section class="bg-gradient-to-br from-gray-900 to-gray-800">
        <div class="container mx-auto px-4 py-12">
          <div class="max-w-6xl mx-auto">
            <!-- Main Image -->
            <div class="relative h-[500px] bg-gray-800 rounded-2xl overflow-hidden shadow-2xl mb-4">
              <img 
                v-if="property.data.featured_image || property.data.image" 
                :src="property.data.featured_image || property.data.image" 
                :alt="property.data.title"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-32 h-32 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                </svg>
              </div>
              <!-- Image overlay with property type badge -->
              <div class="absolute top-4 left-4">
                <span v-if="property.data.property_type" class="px-4 py-2 bg-white/90 backdrop-blur-sm text-property-ink font-semibold rounded-full shadow-lg">
                  {{ property.data.property_type }}
                </span>
              </div>
            </div>
            
            <!-- Thumbnail Gallery -->
            <div v-if="property.data.images?.length" class="grid grid-cols-4 gap-4">
              <div 
                v-for="(img, index) in property.data.images.slice(0, 4)" 
                :key="index"
                class="relative h-24 bg-gray-800 rounded-lg overflow-hidden cursor-pointer hover:opacity-80 transition-opacity"
              >
                <img 
                  :src="img.image" 
                  :alt="img.title || `Image ${index + 1}`"
                  class="w-full h-full object-cover"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Property Details -->
      <section class="py-8">
        <div class="container mx-auto px-4">
          <div class="max-w-6xl mx-auto">
            <div class="flex flex-col lg:flex-row gap-8">
              <!-- Main Content -->
              <div class="flex-1">
                <!-- Header -->
                <div class="bg-white rounded-property-lg p-6 shadow-sm mb-6">
                  <div class="flex items-start justify-between mb-4">
                    <div>
                      <h1 class="text-3xl font-bold text-property-ink mb-2">
                        {{ property.data.title || property.data.name }}
                      </h1>
                      <div class="flex items-center text-property-body">
                        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                        <span>{{ property.data.location || 'Location not specified' }}</span>
                      </div>
                    </div>
                    <div class="text-right">
                      <div class="text-3xl font-bold text-property-blue">
                        {{ formatPrice(property.data.price) }}
                      </div>
                      <div v-if="property.data.status" class="mt-2">
                        <span 
                          class="px-3 py-1 rounded-full text-xs font-semibold"
                          :class="getStatusClass(property.data.status)"
                        >
                          {{ property.data.status }}
                        </span>
                      </div>
                    </div>
                  </div>

                  <!-- Key Specs -->
                  <div class="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t border-property-border">
                    <div v-if="property.data.bedrooms" class="text-center p-3 bg-property-bg-base rounded-lg">
                      <div class="text-2xl font-bold text-property-blue mb-1">{{ property.data.bedrooms }}</div>
                      <div class="text-sm text-property-body">Bedrooms</div>
                    </div>
                    <div v-if="property.data.bathrooms" class="text-center p-3 bg-property-bg-base rounded-lg">
                      <div class="text-2xl font-bold text-property-blue mb-1">{{ property.data.bathrooms }}</div>
                      <div class="text-sm text-property-body">Bathrooms</div>
                    </div>
                    <div v-if="property.data.area" class="text-center p-3 bg-property-bg-base rounded-lg">
                      <div class="text-2xl font-bold text-property-blue mb-1">{{ property.data.area }}</div>
                      <div class="text-sm text-property-body">Sqft</div>
                    </div>
                    <div v-if="property.data.property_type" class="text-center p-3 bg-property-bg-base rounded-lg">
                      <div class="text-lg font-bold text-property-blue mb-1">{{ property.data.property_type }}</div>
                      <div class="text-sm text-property-body">Type</div>
                    </div>
                  </div>
                </div>

                <!-- Description -->
                <div class="bg-white rounded-property-lg p-6 shadow-sm mb-6">
                  <h2 class="text-2xl font-bold text-property-ink mb-4 flex items-center">
                    <svg class="w-6 h-6 mr-2 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    Description
                  </h2>
                  <div 
                    class="text-property-body leading-relaxed prose prose-sm max-w-none"
                    v-html="property.data.description || '&lt;p class=&quot;text-gray-500 italic&quot;&gt;No description available for this property.&lt;/p&gt;'"
                  >
                  </div>
                </div>

                <!-- Amenities -->
                <div v-if="property.data.amenities?.length" class="bg-white rounded-property-lg p-6 shadow-sm mb-6">
                  <h2 class="text-2xl font-bold text-property-ink mb-6 flex items-center">
                    <svg class="w-6 h-6 mr-2 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" />
                    </svg>
                    Amenities
                  </h2>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div 
                      v-for="(amenity, index) in property.data.amenities" 
                      :key="index" 
                      class="flex items-start p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg border border-blue-100 hover:shadow-md transition-shadow"
                    >
                      <div class="flex-shrink-0 w-10 h-10 bg-property-blue rounded-full flex items-center justify-center mr-3">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                        </svg>
                      </div>
                      <div class="flex-1">
                        <h3 class="font-semibold text-property-ink">{{ typeof amenity === 'string' ? amenity : amenity.name }}</h3>
                        <p v-if="typeof amenity === 'object' && amenity.description" class="text-sm text-property-body mt-1">{{ amenity.description }}</p>
                      </div>
                    </div>
                  </div>
                </div>
                
                <!-- Additional Details -->
                <div class="bg-white rounded-property-lg p-6 shadow-sm mb-6">
                  <h2 class="text-2xl font-bold text-property-ink mb-6 flex items-center">
                    <svg class="w-6 h-6 mr-2 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                    Additional Details
                  </h2>
                  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div v-if="property.data.parking_spaces" class="flex items-center p-3 bg-gray-50 rounded-lg">
                      <svg class="w-5 h-5 text-property-blue mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                      </svg>
                      <div>
                        <span class="text-sm text-property-body">Parking Spaces</span>
                        <p class="font-semibold text-property-ink">{{ property.data.parking_spaces }}</p>
                      </div>
                    </div>
                    <div v-if="property.data.floor_number" class="flex items-center p-3 bg-gray-50 rounded-lg">
                      <svg class="w-5 h-5 text-property-blue mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                      </svg>
                      <div>
                        <span class="text-sm text-property-body">Floor</span>
                        <p class="font-semibold text-property-ink">{{ property.data.floor_number }}</p>
                      </div>
                    </div>
                    <div v-if="property.data.furnishing_status" class="flex items-center p-3 bg-gray-50 rounded-lg">
                      <svg class="w-5 h-5 text-property-blue mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                      </svg>
                      <div>
                        <span class="text-sm text-property-body">Furnishing</span>
                        <p class="font-semibold text-property-ink">{{ property.data.furnishing_status }}</p>
                      </div>
                    </div>
                    <div v-if="property.data.property_age" class="flex items-center p-3 bg-gray-50 rounded-lg">
                      <svg class="w-5 h-5 text-property-blue mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <div>
                        <span class="text-sm text-property-body">Property Age</span>
                        <p class="font-semibold text-property-ink">{{ property.data.property_age }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Sidebar - Contact Form -->
              <aside class="lg:w-96 flex-shrink-0">
                <div class="bg-white rounded-property-lg p-6 shadow-sm sticky top-20">
                  <h3 class="text-xl font-semibold text-property-ink mb-4">Interested in this property?</h3>
                  
                  <form @submit.prevent="submitEnquiry" class="space-y-4 mb-6">
                    <div>
                      <FormControl
                        v-model="enquiryForm.name"
                        label="Full Name"
                        type="text"
                        placeholder="Your name"
                        :required="true"
                      />
                    </div>
                    
                    <div>
                      <FormControl
                        v-model="enquiryForm.email"
                        label="Email"
                        type="email"
                        placeholder="your@email.com"
                        :required="true"
                      />
                    </div>
                    
                    <div>
                      <FormControl
                        v-model="enquiryForm.phone"
                        label="Phone"
                        type="tel"
                        placeholder="+91 1234567890"
                        :required="true"
                      />
                    </div>
                    
                    <div>
                      <FormControl
                        v-model="enquiryForm.message"
                        label="Message"
                        type="textarea"
                        placeholder="I'm interested in this property..."
                        :rows="3"
                      />
                    </div>

                    <ErrorMessage v-if="enquiryError" :message="enquiryError" />

                    <Button 
                      type="submit" 
                      variant="solid" 
                      class="w-full"
                      :loading="submittingEnquiry"
                    >
                      Send Enquiry
                    </Button>
                  </form>

                  <!-- Quick Actions -->
                  <div class="space-y-3 pt-6 border-t border-property-border">
                    <a 
                      href="tel:+911234567890" 
                      class="flex items-center justify-center space-x-2 w-full px-4 py-3 bg-property-blue text-white rounded-lg hover:bg-property-blue-600 transition-colors font-medium"
                    >
                      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                      </svg>
                      <span>Call Now</span>
                    </a>
                    
                    <a 
                      :href="whatsappUrl"
                      target="_blank"
                      rel="noopener noreferrer"
                      class="flex items-center justify-center space-x-2 w-full px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-medium"
                    >
                      <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                      </svg>
                      <span>WhatsApp</span>
                    </a>
                  </div>
                </div>
              </aside>
            </div>
          </div>
        </div>
      </section>
    </div>

    <div v-else class="container mx-auto px-4 py-12 text-center">
      <svg class="w-16 h-16 text-property-hint mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
      <h2 class="text-2xl font-semibold text-property-ink mb-2">Property Not Found</h2>
      <p class="text-property-body mb-4">The property you're looking for doesn't exist or has been removed.</p>
      <router-link to="/properties">
        <Button variant="solid">Browse All Properties</Button>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { createResource, FormControl, ErrorMessage } from 'frappe-ui'

const route = useRoute()

const property = createResource({
  url: 'property_management.api.get_property_details',
  params: {
    property_id: route.params.id
  },
  auto: true
})

const enquiryForm = ref({
  name: '',
  email: '',
  phone: '',
  message: ''
})

const enquiryError = ref('')
const submittingEnquiry = ref(false)

const submitEnquiryResource = createResource({
  url: 'property_management.api.submit_enquiry',
  onSuccess() {
    submittingEnquiry.value = false
    enquiryForm.value = { name: '', email: '', phone: '', message: '' }
    enquiryError.value = ''
    alert('Thank you! Your enquiry has been submitted successfully.')
  },
  onError(err) {
    submittingEnquiry.value = false
    enquiryError.value = err.message || 'Failed to submit enquiry'
  }
})

const submitEnquiry = () => {
  enquiryError.value = ''
  
  if (!enquiryForm.value.name || !enquiryForm.value.email || !enquiryForm.value.phone) {
    enquiryError.value = 'Please fill in all required fields'
    return
  }

  submittingEnquiry.value = true
  submitEnquiryResource.submit({
    ...enquiryForm.value,
    property_id: route.params.id,
    property_name: property.data?.title || property.data?.name
  })
}

const formatPrice = (price) => {
  if (!price) return 'Price on request'
  const numPrice = typeof price === 'string' ? parseFloat(price) : price
  if (numPrice >= 10000000) return `₹${(numPrice / 10000000).toFixed(2)} Cr`
  if (numPrice >= 100000) return `₹${(numPrice / 100000).toFixed(2)} Lac`
  return `₹${numPrice.toLocaleString('en-IN')}`
}

const getStatusClass = (status) => {
  const s = status?.toLowerCase()
  if (s === 'available' || s === 'for sale') return 'bg-green-500 text-white'
  if (s === 'sold') return 'bg-red-500 text-white'
  if (s === 'reserved') return 'bg-yellow-500 text-white'
  return 'bg-gray-500 text-white'
}

const whatsappUrl = computed(() => {
  const message = `Hi! I'm interested in ${property.data?.title || property.data?.name}. Please provide more details.`
  return `https://wa.me/911234567890?text=${encodeURIComponent(message)}`
})
</script>
