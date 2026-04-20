<template>
  <Dialog 
    v-model="isOpen" 
    :options="{ title: 'Send Enquiry', size: 'lg' }"
  >
    <template #body-content>
      <form @submit.prevent="submitEnquiry" class="space-y-4">
        <div>
          <FormControl
            v-model="form.name"
            label="Full Name"
            type="text"
            placeholder="Enter your name"
            :required="true"
          />
        </div>
        
        <div>
          <FormControl
            v-model="form.email"
            label="Email Address"
            type="email"
            placeholder="your.email@example.com"
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
        
        <div v-if="propertyName">
          <FormControl
            :modelValue="propertyName"
            label="Property Interest"
            type="text"
            :disabled="true"
          />
        </div>
        
        <div>
          <FormControl
            v-model="form.message"
            label="Message"
            type="textarea"
            placeholder="Tell us about your requirements..."
            :rows="4"
          />
        </div>

        <ErrorMessage v-if="error" :message="error" />

        <div class="flex justify-end space-x-3 pt-4">
          <Button @click="isOpen = false" variant="ghost">
            Cancel
          </Button>
          <Button 
            type="submit" 
            variant="solid"
            :loading="submitting"
          >
            Submit Enquiry
          </Button>
        </div>
      </form>
    </template>
  </Dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { Dialog, FormControl, ErrorMessage } from 'frappe-ui'
import { createResource } from 'frappe-ui'

const props = defineProps({
  modelValue: Boolean,
  propertyId: String,
  propertyName: String
})

const emit = defineEmits(['update:modelValue', 'success'])

const isOpen = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

const form = ref({
  name: '',
  email: '',
  phone: '',
  message: ''
})

const error = ref('')
const submitting = ref(false)

const submitEnquiryResource = createResource({
  url: 'property_management.api.submit_enquiry',
  onSuccess() {
    submitting.value = false
    emit('success')
    isOpen.value = false
    // Reset form
    form.value = {
      name: '',
      email: '',
      phone: '',
      message: ''
    }
    error.value = ''
  },
  onError(err) {
    submitting.value = false
    error.value = err.message || 'Failed to submit enquiry. Please try again.'
  }
})

const submitEnquiry = async () => {
  error.value = ''
  
  // Basic validation
  if (!form.value.name || !form.value.email || !form.value.phone) {
    error.value = 'Please fill in all required fields'
    return
  }

  submitting.value = true
  
  submitEnquiryResource.submit({
    name: form.value.name,
    email: form.value.email,
    phone: form.value.phone,
    message: form.value.message,
    property_id: props.propertyId,
    property_name: props.propertyName
  })
}

// Reset error when modal closes
watch(isOpen, (newVal) => {
  if (!newVal) {
    error.value = ''
  }
})
</script>
