<template>
  <div class="min-h-screen flex flex-col bg-property-bg-base">
    <PublicHeader @open-enquiry="enquiryModalOpen = true" />
    
    <main class="flex-1">
      <slot />
    </main>
    
    <PublicFooter />
    
    <!-- WhatsApp Floating Button -->
    <WhatsAppButton />
    
    <!-- Enquiry Modal -->
    <EnquiryModal v-model="enquiryModalOpen" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PublicHeader from './PublicHeader.vue'
import PublicFooter from './PublicFooter.vue'
import WhatsAppButton from '@/components/WhatsAppButton.vue'
import EnquiryModal from '@/components/EnquiryModal.vue'

const enquiryModalOpen = ref(false)
</script>
