<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import PublicLayout from './layouts/PublicLayout.vue'

const route = useRoute()

const layout = computed(() => {
  const layoutType = route.meta.layout
  if (layoutType === 'public') {
    return PublicLayout
  }
  // Default layout (no wrapper for admin/login)
  return 'div'
})
</script>
