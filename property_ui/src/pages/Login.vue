<template>
  <div class="min-h-screen flex">
    <!-- Left Side - Branding -->
    <div class="hidden lg:flex lg:w-1/2 bg-gradient-to-br from-property-blue to-property-blue-600 relative overflow-hidden">
      <div class="absolute inset-0 opacity-10">
        <svg class="w-full h-full" viewBox="0 0 100 100" preserveAspectRatio="none">
          <defs>
            <pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse">
              <path d="M 10 0 L 0 0 0 10" fill="none" stroke="white" stroke-width="0.5"/>
            </pattern>
          </defs>
          <rect width="100" height="100" fill="url(#grid)" />
        </svg>
      </div>
      
      <div class="relative z-10 flex flex-col justify-center px-12 text-white">
        <div class="mb-8">
          <svg class="w-16 h-16 mb-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
          <h1 class="text-4xl font-bold mb-2">Welcome Back</h1>
          <p class="text-blue-100 text-lg">Sign in to access your property dashboard</p>
        </div>
        
        <div class="space-y-4">
          <div class="flex items-start space-x-3">
            <svg class="w-6 h-6 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <div>
              <h3 class="font-semibold">Manage Your Properties</h3>
              <p class="text-blue-100 text-sm">Access and manage all your property listings in one place</p>
            </div>
          </div>
          <div class="flex items-start space-x-3">
            <svg class="w-6 h-6 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <div>
              <h3 class="font-semibold">Track Leads</h3>
              <p class="text-blue-100 text-sm">Monitor and respond to property inquiries instantly</p>
            </div>
          </div>
          <div class="flex items-start space-x-3">
            <svg class="w-6 h-6 mt-1 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <div>
              <h3 class="font-semibold">Analytics & Insights</h3>
              <p class="text-blue-100 text-sm">Get detailed insights on property performance</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side - Form -->
    <div class="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 bg-white">
      <div class="w-full max-w-md">
        <!-- Logo for mobile -->
        <div class="lg:hidden text-center mb-8">
          <svg class="w-12 h-12 mx-auto text-property-blue" fill="currentColor" viewBox="0 0 24 24">
            <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
          </svg>
        </div>

        <div class="text-center mb-8">
          <h2 class="text-3xl font-bold text-property-ink mb-2">Sign In</h2>
          <p class="text-property-body">Enter your credentials to access your account</p>
        </div>

        <form class="space-y-6" @submit.prevent="submit">
          <div>
            <label for="email" class="block text-sm font-medium text-property-ink mb-2">
              Email Address
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 12a4 4 0 10-8 0 4 4 0 008 0zm0 0v1.5a2.5 2.5 0 005 0V12a9 9 0 10-9 9m4.5-1.206a8.959 8.959 0 01-4.5 1.207" />
                </svg>
              </div>
              <input
                id="email"
                name="email"
                type="email"
                required
                placeholder="johndoe@email.com"
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-property-blue focus:border-transparent transition-all"
              />
            </div>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-property-ink mb-2">
              Password
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <input
                id="password"
                name="password"
                type="password"
                required
                placeholder="••••••••"
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-property-blue focus:border-transparent transition-all"
              />
            </div>
          </div>

          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input
                id="remember-me"
                name="remember-me"
                type="checkbox"
                class="h-4 w-4 text-property-blue focus:ring-property-blue border-gray-300 rounded"
              />
              <label for="remember-me" class="ml-2 block text-sm text-property-body">
                Remember me
              </label>
            </div>
            <div class="text-sm">
              <a href="#" class="font-medium text-property-blue hover:text-property-blue-600">
                Forgot password?
              </a>
            </div>
          </div>

          <Button 
            type="submit" 
            :loading="session.login.loading" 
            class="w-full py-3 bg-property-blue hover:bg-property-blue-600 text-white font-semibold rounded-lg transition-colors shadow-lg hover:shadow-xl"
          >
            Sign In
          </Button>

          <div class="relative my-6">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-4 bg-white text-property-body">New to our platform?</span>
            </div>
          </div>

          <div class="text-center">
            <router-link 
              to="/signup" 
              class="inline-flex items-center justify-center w-full py-3 border-2 border-property-blue text-property-blue font-semibold rounded-lg hover:bg-property-blue hover:text-white transition-all"
            >
              Create an Account
            </router-link>
          </div>
        </form>

        <p class="mt-8 text-center text-xs text-gray-500">
          By signing in, you agree to our 
          <a href="#" class="text-property-blue hover:underline">Terms of Service</a> and 
          <a href="#" class="text-property-blue hover:underline">Privacy Policy</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { session } from "../data/session"

function submit(e) {
	const formData = new FormData(e.target)
	session.login.submit({
		email: formData.get("email"),
		password: formData.get("password"),
	})
}
</script>
