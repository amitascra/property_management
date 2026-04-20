<template>
  <header class="sticky top-0 z-50 bg-white border-b border-property-border shadow-sm">
    <div class="container mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <router-link to="/" class="flex items-center space-x-2">
          <div class="w-10 h-10 bg-property-blue rounded-lg flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </div>
          <span class="text-xl font-bold text-property-ink">Property Management</span>
        </router-link>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-8">
          <router-link 
            v-for="link in navLinks" 
            :key="link.path"
            :to="link.path"
            class="text-property-body hover:text-property-blue transition-colors font-medium"
            active-class="text-property-blue"
          >
            {{ link.label }}
          </router-link>
        </nav>

        <!-- CTA Buttons -->
        <div class="hidden md:flex items-center space-x-3">
          <a 
            :href="`tel:${contactPhone}`" 
            class="flex items-center space-x-2 px-4 py-2 text-property-blue hover:bg-property-blue-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            <span class="font-medium">Call Us</span>
          </a>
          
          <!-- Logged In State -->
          <template v-if="session.isLoggedIn">
            <router-link to="/dashboard">
              <Button variant="outline">Dashboard</Button>
            </router-link>
            <Button @click="handleLogout" variant="solid" :loading="session.logout.loading">
              Logout
            </Button>
          </template>
          
          <!-- Logged Out State -->
          <template v-else>
            <router-link to="/signin">
              <Button variant="outline">Sign In</Button>
            </router-link>
            <router-link to="/signup">
              <Button variant="solid">Sign Up</Button>
            </router-link>
          </template>
        </div>

        <!-- Mobile Menu Button -->
        <button 
          @click="mobileMenuOpen = !mobileMenuOpen"
          class="md:hidden p-2 text-property-body hover:text-property-blue"
        >
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path v-if="!mobileMenuOpen" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <!-- Mobile Menu -->
      <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-property-border">
        <nav class="flex flex-col space-y-3">
          <router-link 
            v-for="link in navLinks" 
            :key="link.path"
            :to="link.path"
            @click="mobileMenuOpen = false"
            class="text-property-body hover:text-property-blue transition-colors font-medium py-2"
            active-class="text-property-blue"
          >
            {{ link.label }}
          </router-link>
        </nav>
        <div class="flex flex-col space-y-2 mt-4 pt-4 border-t border-property-border">
          <a 
            :href="`tel:${contactPhone}`" 
            class="flex items-center justify-center space-x-2 px-4 py-2 text-property-blue hover:bg-property-blue-100 rounded-lg transition-colors"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
            </svg>
            <span class="font-medium">Call Us</span>
          </a>
          
          <!-- Logged In State -->
          <template v-if="session.isLoggedIn">
            <router-link to="/dashboard" @click="mobileMenuOpen = false">
              <Button variant="outline" class="w-full">Dashboard</Button>
            </router-link>
            <Button @click="handleLogout" variant="solid" class="w-full" :loading="session.logout.loading">
              Logout
            </Button>
          </template>
          
          <!-- Logged Out State -->
          <template v-else>
            <router-link to="/signin" @click="mobileMenuOpen = false">
              <Button variant="outline" class="w-full">Sign In</Button>
            </router-link>
            <router-link to="/signup" @click="mobileMenuOpen = false">
              <Button variant="solid" class="w-full">Sign Up</Button>
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { createResource } from 'frappe-ui'
import { session } from '@/data/session'
import { useRouter } from 'vue-router'

const router = useRouter()
const mobileMenuOpen = ref(false)

const navLinks = [
  { path: '/', label: 'Home' },
  { path: '/properties', label: 'Properties' },
  { path: '/about', label: 'About Us' },
  { path: '/contact', label: 'Contact' },
]

// Fetch website settings for dynamic phone number
const websiteSettings = createResource({
  url: 'property_management.api.get_website_settings',
  auto: true
})

const contactPhone = computed(() => websiteSettings.data?.contact_phone || '+91 1234567890')

const handleLogout = () => {
  session.logout.submit()
  mobileMenuOpen.value = false
}

defineEmits(['open-enquiry'])
</script>
