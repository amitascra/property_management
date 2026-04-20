<template>
  <div>
    <!-- Hero Slider -->
    <HeroSlider 
      v-if="websiteSettings.data?.hero_slides?.length"
      :slides="websiteSettings.data.hero_slides"
      :autoplay="true"
      :interval="5000"
    />
    
    <!-- Fallback Hero Section -->
    <section v-else class="relative bg-gradient-to-br from-property-blue to-property-blue-600 text-white py-20">
      <div class="container mx-auto px-4">
        <div class="max-w-3xl">
          <h1 class="text-4xl md:text-5xl font-bold mb-6">
            {{ websiteSettings.data?.tagline || 'Find Your Dream Property' }}
          </h1>
          <p class="text-xl mb-8 text-blue-100">
            Discover the perfect home or investment opportunity with our extensive collection of premium properties.
          </p>
          <div class="flex flex-col sm:flex-row gap-4">
            <router-link to="/properties">
              <Button variant="solid" class="bg-white text-property-blue hover:bg-gray-100">
                Browse Properties
              </Button>
            </router-link>
            <router-link to="/contact">
              <Button variant="outline" class="border-white text-white hover:bg-white hover:text-property-blue">
                Contact Us
              </Button>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Featured Properties -->
    <section v-if="websiteSettings.data?.show_featured_properties" class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-property-ink mb-4">{{ websiteSettings.data?.featured_section_title || 'Featured Properties' }}</h2>
          <p class="text-property-body max-w-2xl mx-auto">
            {{ websiteSettings.data?.featured_section_description || 'Explore our handpicked selection of premium properties available for sale and rent.' }}
          </p>
        </div>

        <div v-if="featuredProperties.loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-property-blue"></div>
        </div>

        <div v-else-if="featuredProperties.data?.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <PropertyCard 
            v-for="property in featuredProperties.data" 
            :key="property.name"
            :property="property"
          />
        </div>

        <div v-else class="text-center py-12 text-property-body">
          <p>No featured properties available at the moment.</p>
        </div>

        <div class="text-center mt-8">
          <router-link to="/properties">
            <Button variant="solid">View All Properties</Button>
          </router-link>
        </div>
      </div>
    </section>

    <!-- About Brief -->
    <section v-if="websiteSettings.data?.show_about_section" class="py-16 bg-property-bg-base">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 class="text-3xl font-bold text-property-ink mb-6">{{ websiteSettings.data?.about_section_title || 'About Us' }}</h2>
            <div v-if="websiteSettings.data?.about_section_content" v-html="websiteSettings.data.about_section_content" class="text-property-body mb-6 prose max-w-none"></div>
            <div v-else>
              <p class="text-property-body mb-4">
                With over a decade of experience in the real estate industry, we have helped thousands of clients find their perfect property. Our commitment to excellence and customer satisfaction sets us apart.
              </p>
              <p class="text-property-body mb-6">
                Whether you're looking to buy, sell, or rent, our expert team is here to guide you through every step of the process.
              </p>
            </div>
            
            <!-- Stats -->
            <div v-if="websiteSettings.data?.stats?.length" class="grid grid-cols-3 gap-4 mb-6">
              <div v-for="stat in websiteSettings.data.stats" :key="stat.label" class="text-center p-4 bg-white rounded-lg shadow-sm">
                <div class="text-3xl font-bold text-property-blue mb-1">{{ stat.value }}{{ stat.suffix }}</div>
                <div class="text-sm text-property-body">{{ stat.label }}</div>
              </div>
            </div>

            <router-link to="/about">
              <Button variant="outline">Learn More About Us</Button>
            </router-link>
          </div>

          <div class="relative">
            <div v-if="websiteSettings.data?.about_section_image" class="rounded-property-lg overflow-hidden">
              <img :src="websiteSettings.data.about_section_image" alt="About Us" class="w-full h-full object-cover" />
            </div>
            <div v-else class="aspect-w-16 aspect-h-12 bg-gradient-to-br from-property-blue-100 to-property-blue-200 rounded-property-lg overflow-hidden">
              <div class="flex items-center justify-center">
                <svg class="w-32 h-32 text-property-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Why Choose Us -->
    <section v-if="displayFeatures.length" class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-property-ink mb-4">{{ websiteSettings.data?.why_choose_title || 'Why Choose Us' }}</h2>
          <p class="text-property-body max-w-2xl mx-auto">
            We provide comprehensive real estate solutions tailored to your needs.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="feature in displayFeatures" :key="feature.title" class="text-center p-6 bg-property-bg-base rounded-property-lg hover:shadow-md transition-shadow">
            <div class="w-16 h-16 bg-property-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <component :is="getIconComponent(feature.icon)" class="w-8 h-8 text-property-blue" />
            </div>
            <h3 class="text-lg font-semibold text-property-ink mb-2">{{ feature.title }}</h3>
            <p class="text-property-body text-sm">{{ feature.description }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section v-if="websiteSettings.data?.show_cta_section" class="py-16 bg-gradient-to-r from-property-blue to-property-blue-600 text-white">
      <div class="container mx-auto px-4 text-center">
        <h2 class="text-3xl font-bold mb-4">{{ websiteSettings.data?.cta_section_title || 'Ready to Find Your Perfect Property?' }}</h2>
        <p class="text-xl mb-8 text-blue-100 max-w-2xl mx-auto">
          {{ websiteSettings.data?.cta_section_description || 'Get in touch with our expert team today and let us help you make your real estate dreams come true.' }}
        </p>
        
        <div class="flex flex-col sm:flex-row gap-4 justify-center items-center">
          <a 
            :href="`tel:${websiteSettings.data?.contact_phone || '+911234567890'}`" 
            class="flex items-center space-x-2 px-6 py-3 bg-white text-property-blue rounded-lg hover:bg-gray-100 transition-colors font-semibold"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            <span>Call Now</span>
          </a>
          
          <a 
            :href="`https://wa.me/${websiteSettings.data?.whatsapp_number || '911234567890'}?text=Hi!%20I%20am%20interested%20in%20your%20properties.`" 
            target="_blank"
            rel="noopener noreferrer"
            class="flex items-center space-x-2 px-6 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-semibold"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
              <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
            </svg>
            <span>WhatsApp</span>
          </a>
          
          <Button @click="openEnquiry" variant="solid" class="bg-white text-property-blue hover:bg-gray-100">
            Enquire Now
          </Button>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import { createResource } from 'frappe-ui'
import PropertyCard from '@/components/PropertyCard.vue'
import HeroSlider from '@/components/HeroSlider.vue'

const websiteSettings = createResource({
  url: 'property_management.api.get_website_settings',
  auto: true
})

const featuredProperties = createResource({
  url: 'property_management.api.get_featured_properties',
  auto: true
})

const defaultFeatures = [
  {
    title: 'Wide Range',
    description: 'From premium to economy apartments, we have properties for every budget.',
    icon: 'home'
  },
  {
    title: 'Expert Team',
    description: 'Our experienced professionals guide you through every step of the process.',
    icon: 'users'
  },
  {
    title: 'Best Prices',
    description: 'Competitive pricing and transparent dealings with no hidden costs.',
    icon: 'check-circle'
  },
  {
    title: 'Trusted Service',
    description: 'Award-winning real estate firm with proven track record of success.',
    icon: 'shield-check'
  }
]

const displayFeatures = computed(() => {
  return websiteSettings.data?.why_choose_features?.length 
    ? websiteSettings.data.why_choose_features 
    : defaultFeatures
})

const getIconComponent = (iconName) => {
  const icons = {
    'home': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6' })
    ]),
    'users': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z' })
    ]),
    'check-circle': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' })
    ]),
    'shield-check': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z' })
    ]),
    'map-pin': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z' }),
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M15 11a3 3 0 11-6 0 3 3 0 016 0z' })
    ]),
    'phone': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z' })
    ]),
    'star': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z' })
    ]),
    'award': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z' })
    ]),
    'clock': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z' })
    ])
  }
  return icons[iconName] || icons['check-circle']
}

const openEnquiry = () => {
  window.dispatchEvent(new CustomEvent('open-enquiry'))
}
</script>
