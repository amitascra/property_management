<template>
  <div class="relative w-full h-[500px] md:h-[600px] overflow-hidden bg-gray-900">
    <!-- Slides -->
    <transition-group name="slide-fade">
      <div
        v-for="(slide, index) in slides"
        :key="index"
        v-show="currentSlide === index"
        class="absolute inset-0 w-full h-full"
      >
        <!-- Background Image with Overlay -->
        <div class="absolute inset-0">
          <img
            :src="slide.image"
            :alt="slide.title"
            class="w-full h-full object-cover"
          />
          <div class="absolute inset-0 bg-gradient-to-r from-black/70 via-black/50 to-transparent"></div>
        </div>

        <!-- Content -->
        <div class="relative h-full flex items-center">
          <div class="container mx-auto px-4">
            <div class="max-w-3xl text-white">
              <!-- Subtitle -->
              <div
                v-if="slide.subtitle"
                class="inline-block px-4 py-2 mb-4 bg-property-blue/20 backdrop-blur-sm border border-property-blue/30 rounded-full text-sm font-medium text-property-blue-100 animate-fade-in-up"
                :style="{ animationDelay: '0.2s' }"
              >
                {{ slide.subtitle }}
              </div>

              <!-- Title -->
              <h1
                class="text-4xl md:text-6xl font-bold mb-6 leading-tight animate-fade-in-up"
                :style="{ animationDelay: '0.4s' }"
              >
                {{ slide.title }}
              </h1>

              <!-- Description -->
              <p
                v-if="slide.description"
                class="text-xl md:text-2xl mb-8 text-gray-200 animate-fade-in-up"
                :style="{ animationDelay: '0.6s' }"
              >
                {{ slide.description }}
              </p>

              <!-- Button -->
              <div
                v-if="slide.button_text"
                class="animate-fade-in-up"
                :style="{ animationDelay: '0.8s' }"
              >
                <router-link
                  :to="slide.button_link || '/properties'"
                  class="inline-flex items-center px-8 py-4 bg-property-blue hover:bg-property-blue-600 text-white font-semibold rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
                >
                  {{ slide.button_text }}
                  <svg class="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                  </svg>
                </router-link>
              </div>
            </div>
          </div>
        </div>

        <!-- Thumbnail Preview (bottom) -->
        <div
          v-if="slide.image"
          class="absolute bottom-8 left-1/2 transform -translate-x-1/2 hidden md:block"
        >
          <div class="flex space-x-2">
            <div
              v-for="(s, i) in slides"
              :key="i"
              @click="goToSlide(i)"
              class="w-20 h-14 rounded-lg overflow-hidden cursor-pointer border-2 transition-all duration-300"
              :class="currentSlide === i ? 'border-property-blue scale-110' : 'border-white/30 opacity-60 hover:opacity-100'"
            >
              <img :src="s.image" :alt="s.title" class="w-full h-full object-cover" />
            </div>
          </div>
        </div>
      </div>
    </transition-group>

    <!-- Navigation Arrows -->
    <button
      v-if="slides.length > 1"
      @click="prevSlide"
      class="absolute left-4 top-1/2 transform -translate-y-1/2 bg-white/10 hover:bg-white/20 backdrop-blur-sm text-white p-3 rounded-full transition-all duration-300 hover:scale-110 z-10"
      aria-label="Previous slide"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
      </svg>
    </button>

    <button
      v-if="slides.length > 1"
      @click="nextSlide"
      class="absolute right-4 top-1/2 transform -translate-y-1/2 bg-white/10 hover:bg-white/20 backdrop-blur-sm text-white p-3 rounded-full transition-all duration-300 hover:scale-110 z-10"
      aria-label="Next slide"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
      </svg>
    </button>

    <!-- Dot Indicators -->
    <div
      v-if="slides.length > 1"
      class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex space-x-2 z-10 md:hidden"
    >
      <button
        v-for="(slide, index) in slides"
        :key="index"
        @click="goToSlide(index)"
        class="w-3 h-3 rounded-full transition-all duration-300"
        :class="currentSlide === index ? 'bg-property-blue w-8' : 'bg-white/50 hover:bg-white/80'"
        :aria-label="`Go to slide ${index + 1}`"
      ></button>
    </div>

    <!-- Progress Bar -->
    <div
      v-if="slides.length > 1 && autoplay"
      class="absolute bottom-0 left-0 right-0 h-1 bg-white/20"
    >
      <div
        class="h-full bg-property-blue transition-all duration-100 ease-linear"
        :style="{ width: `${progress}%` }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'

const props = defineProps({
  slides: {
    type: Array,
    required: true,
    default: () => []
  },
  autoplay: {
    type: Boolean,
    default: true
  },
  interval: {
    type: Number,
    default: 5000
  }
})

const currentSlide = ref(0)
const progress = ref(0)
let autoplayInterval = null
let progressInterval = null

const nextSlide = () => {
  currentSlide.value = (currentSlide.value + 1) % props.slides.length
  resetProgress()
}

const prevSlide = () => {
  currentSlide.value = currentSlide.value === 0 ? props.slides.length - 1 : currentSlide.value - 1
  resetProgress()
}

const goToSlide = (index) => {
  currentSlide.value = index
  resetProgress()
}

const resetProgress = () => {
  progress.value = 0
  if (progressInterval) {
    clearInterval(progressInterval)
  }
  startProgress()
}

const startProgress = () => {
  if (!props.autoplay || props.slides.length <= 1) return
  
  const step = 100 / (props.interval / 100)
  progressInterval = setInterval(() => {
    progress.value += step
    if (progress.value >= 100) {
      progress.value = 0
    }
  }, 100)
}

const startAutoplay = () => {
  if (!props.autoplay || props.slides.length <= 1) return
  
  autoplayInterval = setInterval(() => {
    nextSlide()
  }, props.interval)
  
  startProgress()
}

const stopAutoplay = () => {
  if (autoplayInterval) {
    clearInterval(autoplayInterval)
  }
  if (progressInterval) {
    clearInterval(progressInterval)
  }
}

onMounted(() => {
  if (props.slides.length > 0) {
    startAutoplay()
  }
})

onUnmounted(() => {
  stopAutoplay()
})
</script>

<style scoped>
.slide-fade-enter-active {
  transition: all 0.8s ease;
}

.slide-fade-leave-active {
  transition: all 0.8s ease;
}

.slide-fade-enter-from {
  transform: translateX(100%);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fadeInUp 0.8s ease-out forwards;
  opacity: 0;
}
</style>
