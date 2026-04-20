<template>
  <div>
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-property-blue to-property-blue-600 text-white py-16">
      <div class="container mx-auto px-4 text-center">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">Contact Us</h1>
        <p class="text-xl text-blue-100 max-w-2xl mx-auto">
          Get in touch with our team. We're here to help you with all your real estate needs.
        </p>
      </div>
    </section>

    <!-- Contact Section -->
    <section class="py-16 bg-property-bg-base">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
          <!-- Contact Form -->
          <div class="bg-white rounded-property-lg p-8 shadow-sm">
            <h2 class="text-2xl font-bold text-property-ink mb-6">Send us a Message</h2>
            
            <form @submit.prevent="submitContact" class="space-y-4">
              <div>
                <FormControl
                  v-model="form.name"
                  label="Full Name"
                  type="text"
                  placeholder="Your name"
                  :required="true"
                />
              </div>
              
              <div>
                <FormControl
                  v-model="form.email"
                  label="Email Address"
                  type="email"
                  placeholder="your@email.com"
                  :required="true"
                />
              </div>
              
              <div>
                <FormControl
                  v-model="form.phone"
                  label="Phone Number"
                  type="tel"
                  placeholder="+91 1234567890"
                  :required="true"
                />
              </div>
              
              <div>
                <FormControl
                  v-model="form.subject"
                  label="Subject"
                  type="select"
                  :options="subjectOptions"
                  :required="true"
                />
              </div>
              
              <div>
                <FormControl
                  v-model="form.message"
                  label="Message"
                  type="textarea"
                  placeholder="Tell us how we can help you..."
                  :rows="5"
                  :required="true"
                />
              </div>

              <ErrorMessage v-if="error" :message="error" />

              <div v-if="successMessage" class="p-4 bg-green-50 border border-green-200 rounded-lg text-green-800">
                {{ successMessage }}
              </div>

              <Button 
                type="submit" 
                variant="solid" 
                class="w-full"
                :loading="submitting"
              >
                Send Message
              </Button>
            </form>
          </div>

          <!-- Contact Information -->
          <div>
            <div class="bg-white rounded-property-lg p-8 shadow-sm mb-6">
              <h2 class="text-2xl font-bold text-property-ink mb-6">Contact Information</h2>
              
              <div class="space-y-6">
                <!-- Office Address -->
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-property-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-semibold text-property-ink mb-1">Office Address</h3>
                    <p class="text-property-body">
                      123 Real Estate Avenue<br>
                      Business District<br>
                      City, State 12345
                    </p>
                  </div>
                </div>

                <!-- Phone -->
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-property-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-semibold text-property-ink mb-1">Phone</h3>
                    <a href="tel:+911234567890" class="text-property-blue hover:underline">
                      +91 1234567890
                    </a>
                    <p class="text-property-body text-sm mt-1">Mon-Sat: 9:00 AM - 7:00 PM</p>
                  </div>
                </div>

                <!-- Email -->
                <div class="flex items-start space-x-4">
                  <div class="w-12 h-12 bg-property-blue-100 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-6 h-6 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div>
                    <h3 class="font-semibold text-property-ink mb-1">Email</h3>
                    <a href="mailto:info@propertymanagement.com" class="text-property-blue hover:underline">
                      info@propertymanagement.com
                    </a>
                    <p class="text-property-body text-sm mt-1">We'll respond within 24 hours</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Quick Contact Options -->
            <div class="bg-white rounded-property-lg p-8 shadow-sm">
              <h3 class="text-xl font-bold text-property-ink mb-4">Quick Contact</h3>
              <div class="space-y-3">
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
                  href="https://wa.me/911234567890?text=Hi!%20I%20would%20like%20to%20know%20more%20about%20your%20services." 
                  target="_blank"
                  rel="noopener noreferrer"
                  class="flex items-center justify-center space-x-2 w-full px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors font-medium"
                >
                  <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                    <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413Z"/>
                  </svg>
                  <span>WhatsApp</span>
                </a>
                
                <a 
                  href="mailto:info@propertymanagement.com"
                  class="flex items-center justify-center space-x-2 w-full px-4 py-3 border-2 border-property-blue text-property-blue rounded-lg hover:bg-property-blue hover:text-white transition-colors font-medium"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span>Email Us</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Map Section -->
    <section class="py-16 bg-white">
      <div class="container mx-auto px-4">
        <div class="max-w-6xl mx-auto">
          <h2 class="text-2xl font-bold text-property-ink mb-6 text-center">Find Us</h2>
          <div class="bg-gray-200 rounded-property-lg overflow-hidden" style="height: 400px;">
            <div class="w-full h-full flex items-center justify-center text-property-body">
              <div class="text-center">
                <svg class="w-16 h-16 text-property-hint mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <p>Map integration available</p>
                <p class="text-sm mt-2">123 Real Estate Avenue, Business District</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { createResource, FormControl, ErrorMessage } from 'frappe-ui'

const form = ref({
  name: '',
  email: '',
  phone: '',
  subject: 'General Enquiry',
  message: ''
})

const subjectOptions = [
  'General Enquiry',
  'Property Enquiry',
  'Partnership Opportunity',
  'Support',
  'Other'
]

const error = ref('')
const successMessage = ref('')
const submitting = ref(false)

const submitContactResource = createResource({
  url: 'property_management.api.submit_contact',
  onSuccess() {
    submitting.value = false
    successMessage.value = 'Thank you for contacting us! We will get back to you soon.'
    form.value = {
      name: '',
      email: '',
      phone: '',
      subject: 'General Enquiry',
      message: ''
    }
    error.value = ''
    
    // Clear success message after 5 seconds
    setTimeout(() => {
      successMessage.value = ''
    }, 5000)
  },
  onError(err) {
    submitting.value = false
    error.value = err.message || 'Failed to submit contact form. Please try again.'
  }
})

const submitContact = () => {
  error.value = ''
  successMessage.value = ''
  
  if (!form.value.name || !form.value.email || !form.value.phone || !form.value.message) {
    error.value = 'Please fill in all required fields'
    return
  }

  submitting.value = true
  submitContactResource.submit(form.value)
}
</script>
