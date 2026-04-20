<template>
  <div class="min-h-screen bg-property-bg-base">
    <!-- Loading State -->
    <div v-if="dashboardData.loading" class="container mx-auto px-4 py-12 text-center">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-property-blue"></div>
      <p class="text-property-body mt-4">Loading your dashboard...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="dashboardData.error" class="container mx-auto px-4 py-12">
      <div class="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <svg class="w-16 h-16 text-red-500 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <h2 class="text-xl font-semibold text-red-800 mb-2">Unable to Load Dashboard</h2>
        <p class="text-red-600">{{ dashboardData.error }}</p>
      </div>
    </div>

    <!-- Dashboard Content -->
    <div v-else-if="dashboardData.data" class="container mx-auto px-4 py-8">
      <!-- Welcome Header -->
      <div class="bg-gradient-to-r from-property-blue to-indigo-600 rounded-2xl p-8 mb-8 text-white shadow-xl">
        <div class="flex items-center justify-between">
          <div>
            <h1 class="text-3xl font-bold mb-2">Welcome back, {{ dashboardData.data.tenant_profile?.tenant_name }}!</h1>
            <p class="text-blue-100">Here's your property dashboard overview</p>
          </div>
          <div class="hidden md:block">
            <svg class="w-24 h-24 opacity-20" fill="currentColor" viewBox="0 0 24 24">
              <path d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <!-- Active Tenancy -->
        <div class="bg-white rounded-xl p-6 shadow-sm border-l-4 border-green-500">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-medium text-property-body">Tenancy Status</h3>
            <svg class="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-property-ink">{{ dashboardData.data.active_tenancy ? 'Active' : 'Inactive' }}</p>
          <p class="text-xs text-property-body mt-1">{{ dashboardData.data.active_tenancy?.agreement_type || 'No active lease' }}</p>
        </div>

        <!-- Monthly Rent -->
        <div class="bg-white rounded-xl p-6 shadow-sm border-l-4 border-blue-500">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-medium text-property-body">Monthly Rent</h3>
            <svg class="w-8 h-8 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-property-ink">{{ formatCurrency(dashboardData.data.active_tenancy?.monthly_rent) }}</p>
          <p class="text-xs text-property-body mt-1">Due on {{ dashboardData.data.active_tenancy?.rent_due_date }}th of month</p>
        </div>

        <!-- Service Requests -->
        <div class="bg-white rounded-xl p-6 shadow-sm border-l-4 border-orange-500">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-medium text-property-body">Service Requests</h3>
            <svg class="w-8 h-8 text-orange-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-property-ink">{{ dashboardData.data.service_requests?.length || 0 }}</p>
          <p class="text-xs text-property-body mt-1">{{ openRequestsCount }} open</p>
        </div>

        <!-- Lease Expiry -->
        <div class="bg-white rounded-xl p-6 shadow-sm border-l-4 border-purple-500">
          <div class="flex items-center justify-between mb-2">
            <h3 class="text-sm font-medium text-property-body">Lease Expires</h3>
            <svg class="w-8 h-8 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
          </div>
          <p class="text-2xl font-bold text-property-ink">{{ daysUntilExpiry }}</p>
          <p class="text-xs text-property-body mt-1">{{ formatDate(dashboardData.data.active_tenancy?.lease_end_date) }}</p>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Unit Details -->
          <div v-if="dashboardData.data.unit_details" class="bg-white rounded-xl shadow-sm overflow-hidden">
            <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
              <h2 class="text-xl font-bold text-property-ink flex items-center">
                <svg class="w-6 h-6 mr-2 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                Your Unit
              </h2>
            </div>
            <div class="p-6">
              <div class="flex items-start justify-between mb-4">
                <div>
                  <h3 class="text-2xl font-bold text-property-ink">Unit {{ dashboardData.data.unit_details.unit_number }}</h3>
                  <p class="text-property-body">{{ dashboardData.data.unit_details.unit_type }}</p>
                </div>
                <span class="px-4 py-2 bg-green-100 text-green-800 rounded-full text-sm font-semibold">Occupied</span>
              </div>

              <div class="grid grid-cols-2 md:grid-cols-3 gap-4 mb-4">
                <div class="bg-gray-50 rounded-lg p-4">
                  <p class="text-xs text-property-body mb-1">Carpet Area</p>
                  <p class="text-lg font-semibold text-property-ink">{{ dashboardData.data.unit_details.carpet_area }} sq.ft</p>
                </div>
                <div class="bg-gray-50 rounded-lg p-4">
                  <p class="text-xs text-property-body mb-1">Built-up Area</p>
                  <p class="text-lg font-semibold text-property-ink">{{ dashboardData.data.unit_details.built_up_area }} sq.ft</p>
                </div>
                <div class="bg-gray-50 rounded-lg p-4">
                  <p class="text-xs text-property-body mb-1">Facing</p>
                  <p class="text-lg font-semibold text-property-ink">{{ dashboardData.data.unit_details.facing || 'N/A' }}</p>
                </div>
              </div>

              <div class="border-t border-gray-200 pt-4">
                <p class="text-sm text-property-body mb-2"><strong>Building:</strong> {{ dashboardData.data.unit_details.building }}</p>
                <p class="text-sm text-property-body"><strong>Floor:</strong> {{ dashboardData.data.unit_details.floor }}</p>
              </div>
            </div>
          </div>

          <!-- Invoices & Payments -->
          <div class="bg-white rounded-xl shadow-sm overflow-hidden">
            <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
              <h2 class="text-xl font-bold text-property-ink flex items-center">
                <svg class="w-6 h-6 mr-2 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                Invoices & Payments
              </h2>
            </div>
            <div class="p-6">
              <div v-if="dashboardData.data.invoices?.length" class="space-y-4">
                <div 
                  v-for="invoice in dashboardData.data.invoices" 
                  :key="invoice.name"
                  class="border border-gray-200 rounded-lg overflow-hidden"
                >
                  <!-- Invoice Header -->
                  <div class="bg-gray-50 px-4 py-3 flex items-center justify-between">
                    <div class="flex items-center space-x-3">
                      <svg class="w-5 h-5 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                      </svg>
                      <div>
                        <h4 class="font-semibold text-property-ink">{{ invoice.name }}</h4>
                        <p class="text-xs text-property-body">Posted: {{ formatDate(invoice.posting_date) }}</p>
                      </div>
                    </div>
                    <span 
                      class="px-3 py-1 rounded-full text-xs font-semibold"
                      :class="getInvoiceStatusClass(invoice.status)"
                    >
                      {{ invoice.status }}
                    </span>
                  </div>
                  
                  <!-- Invoice Details -->
                  <div class="px-4 py-3 bg-white">
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-3">
                      <div>
                        <p class="text-xs text-property-body">Total Amount</p>
                        <p class="text-sm font-semibold text-property-ink">{{ formatCurrency(invoice.grand_total) }}</p>
                      </div>
                      <div>
                        <p class="text-xs text-property-body">Outstanding</p>
                        <p class="text-sm font-semibold" :class="invoice.outstanding_amount > 0 ? 'text-orange-600' : 'text-green-600'">
                          {{ formatCurrency(invoice.outstanding_amount) }}
                        </p>
                      </div>
                      <div>
                        <p class="text-xs text-property-body">Due Date</p>
                        <p class="text-sm font-semibold text-property-ink">{{ formatDate(invoice.due_date) }}</p>
                      </div>
                      <div>
                        <p class="text-xs text-property-body">Payments</p>
                        <p class="text-sm font-semibold text-property-ink">{{ invoice.payments?.length || 0 }}</p>
                      </div>
                    </div>
                    
                    <!-- Payment Details -->
                    <div v-if="invoice.payments && invoice.payments.length > 0" class="mt-3 pt-3 border-t border-gray-200">
                      <p class="text-xs font-semibold text-property-body mb-2">Payment History:</p>
                      <div class="space-y-2">
                        <div 
                          v-for="payment in invoice.payments" 
                          :key="payment.name"
                          class="flex items-center justify-between text-sm bg-green-50 rounded px-3 py-2"
                        >
                          <div class="flex items-center space-x-2">
                            <svg class="w-4 h-4 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <div>
                              <p class="font-medium text-green-800">{{ payment.name }}</p>
                              <p class="text-xs text-green-600">{{ formatDate(payment.posting_date) }} • {{ payment.mode_of_payment }}</p>
                            </div>
                          </div>
                          <div class="text-right">
                            <p class="font-semibold text-green-800">{{ formatCurrency(payment.allocated_amount) }}</p>
                            <p v-if="payment.reference_no" class="text-xs text-green-600">Ref: {{ payment.reference_no }}</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-8 text-property-body">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <p>No invoices yet</p>
              </div>
            </div>
          </div>

          <!-- Service Requests -->
          <div class="bg-white rounded-xl shadow-sm overflow-hidden">
            <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200 flex items-center justify-between">
              <h2 class="text-xl font-bold text-property-ink flex items-center">
                <svg class="w-6 h-6 mr-2 text-property-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                Service Requests
              </h2>
              <button 
                @click="showServiceRequestModal = true"
                class="px-4 py-2 bg-property-blue text-white rounded-lg hover:bg-property-blue-600 transition-colors text-sm font-semibold"
              >
                + New Request
              </button>
            </div>
            <div class="p-6">
              <div v-if="dashboardData.data.service_requests?.length" class="space-y-3">
                <div 
                  v-for="request in dashboardData.data.service_requests.slice(0, 5)" 
                  :key="request.name"
                  class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div class="flex items-start justify-between mb-2">
                    <div class="flex-1">
                      <h4 class="font-semibold text-property-ink">{{ request.request_type }} - {{ request.category }}</h4>
                      <p class="text-sm text-property-body mt-1">{{ stripHtml(request.description)?.substring(0, 100) }}{{ stripHtml(request.description)?.length > 100 ? '...' : '' }}</p>
                    </div>
                    <span 
                      class="px-3 py-1 rounded-full text-xs font-semibold ml-4"
                      :class="getStatusClass(request.status)"
                    >
                      {{ request.status }}
                    </span>
                  </div>
                  <div class="flex items-center justify-between text-xs text-property-body mt-3">
                    <span class="flex items-center">
                      <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                      </svg>
                      {{ formatDate(request.requested_date) }}
                    </span>
                    <span 
                      class="px-2 py-1 rounded text-xs font-medium"
                      :class="getPriorityClass(request.priority)"
                    >
                      {{ request.priority }}
                    </span>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-8 text-property-body">
                <svg class="w-16 h-16 mx-auto mb-4 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                <p>No service requests yet</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Sidebar -->
        <div class="space-y-6">
          <!-- Lease Information -->
          <div v-if="dashboardData.data.active_tenancy" class="bg-white rounded-xl shadow-sm overflow-hidden">
            <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-bold text-property-ink">Lease Information</h2>
            </div>
            <div class="p-6 space-y-4">
              <div>
                <p class="text-xs text-property-body mb-1">Lease Period</p>
                <p class="text-sm font-semibold text-property-ink">
                  {{ formatDate(dashboardData.data.active_tenancy.lease_start_date) }} - 
                  {{ formatDate(dashboardData.data.active_tenancy.lease_end_date) }}
                </p>
              </div>
              <div>
                <p class="text-xs text-property-body mb-1">Security Deposit</p>
                <p class="text-sm font-semibold text-property-ink">{{ formatCurrency(dashboardData.data.active_tenancy.security_deposit) }}</p>
              </div>
              <div>
                <p class="text-xs text-property-body mb-1">Maintenance Charges</p>
                <p class="text-sm font-semibold text-property-ink">{{ formatCurrency(dashboardData.data.active_tenancy.maintenance_charges) }}</p>
              </div>
            </div>
          </div>

          <!-- Recent Payments -->
          <div class="bg-white rounded-xl shadow-sm overflow-hidden">
            <div class="bg-gradient-to-r from-gray-50 to-gray-100 px-6 py-4 border-b border-gray-200">
              <h2 class="text-lg font-bold text-property-ink">Recent Payments</h2>
            </div>
            <div class="p-6">
              <div v-if="dashboardData.data.rent_history?.length" class="space-y-3">
                <div 
                  v-for="payment in dashboardData.data.rent_history.slice(0, 3)" 
                  :key="payment.payment_date"
                  class="flex items-center justify-between py-2 border-b border-gray-100 last:border-0"
                >
                  <div>
                    <p class="text-sm font-semibold text-property-ink">{{ formatCurrency(payment.amount) }}</p>
                    <p class="text-xs text-property-body">{{ payment.month_year || formatDate(payment.payment_date) }}</p>
                  </div>
                  <span 
                    class="px-2 py-1 rounded text-xs font-semibold"
                    :class="payment.status === 'Paid' ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'"
                  >
                    {{ payment.status }}
                  </span>
                </div>
              </div>
              <div v-else class="text-center py-4 text-property-body text-sm">
                No payment history
              </div>
            </div>
          </div>

          <!-- Quick Actions -->
          <div class="bg-gradient-to-br from-property-blue to-indigo-600 rounded-xl p-6 text-white shadow-lg">
            <h3 class="text-lg font-bold mb-4">Quick Actions</h3>
            <div class="space-y-3">
              <button 
                @click="showServiceRequestModal = true"
                class="w-full bg-white text-property-blue py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors flex items-center justify-center"
              >
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Submit Service Request
              </button>
              <button class="w-full bg-white/20 backdrop-blur-sm text-white py-3 rounded-lg font-semibold hover:bg-white/30 transition-colors flex items-center justify-center">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                </svg>
                Pay Rent
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Service Request Modal -->
    <div v-if="showServiceRequestModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <div class="sticky top-0 bg-white border-b border-gray-200 px-6 py-4 flex items-center justify-between">
          <h3 class="text-2xl font-bold text-property-ink">New Service Request</h3>
          <button @click="closeServiceRequestModal" class="text-gray-400 hover:text-gray-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <form @submit.prevent="submitServiceRequest" class="p-6 space-y-4">
          <div>
            <label class="block text-sm font-medium text-property-ink mb-2">Request Type</label>
            <select v-model="serviceRequestForm.request_type" required class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-property-blue focus:border-transparent">
              <option value="">Select type...</option>
              <option value="Maintenance">Maintenance</option>
              <option value="Repair">Repair</option>
              <option value="Complaint">Complaint</option>
              <option value="Emergency">Emergency</option>
              <option value="Inspection">Inspection</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-property-ink mb-2">Category</label>
            <select v-model="serviceRequestForm.category" required class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-property-blue focus:border-transparent">
              <option value="">Select category...</option>
              <option value="Plumbing">Plumbing</option>
              <option value="Electrical">Electrical</option>
              <option value="AC/HVAC">AC/HVAC</option>
              <option value="Cleaning">Cleaning</option>
              <option value="Security">Security</option>
              <option value="Appliances">Appliances</option>
              <option value="Structural">Structural</option>
              <option value="Pest Control">Pest Control</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-property-ink mb-2">Priority</label>
            <select v-model="serviceRequestForm.priority" required class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-property-blue focus:border-transparent">
              <option value="Low">Low</option>
              <option value="Medium">Medium</option>
              <option value="High">High</option>
              <option value="Emergency">Emergency</option>
            </select>
          </div>

          <div>
            <label class="block text-sm font-medium text-property-ink mb-2">Description</label>
            <textarea 
              v-model="serviceRequestForm.description" 
              required 
              rows="4"
              placeholder="Please describe the issue in detail..."
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-property-blue focus:border-transparent"
            ></textarea>
          </div>

          <div v-if="serviceRequestError" class="p-4 bg-red-50 border border-red-200 rounded-lg text-red-800 text-sm">
            {{ serviceRequestError }}
          </div>

          <div v-if="serviceRequestSuccess" class="p-4 bg-green-50 border border-green-200 rounded-lg text-green-800 text-sm">
            {{ serviceRequestSuccess }}
          </div>

          <div class="flex space-x-3 pt-4">
            <button 
              type="submit" 
              :disabled="submittingRequest"
              class="flex-1 bg-property-blue text-white py-3 rounded-lg font-semibold hover:bg-property-blue-600 transition-colors disabled:opacity-50"
            >
              {{ submittingRequest ? 'Submitting...' : 'Submit Request' }}
            </button>
            <button 
              type="button" 
              @click="closeServiceRequestModal"
              class="px-6 py-3 border-2 border-gray-300 text-gray-700 rounded-lg font-semibold hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { createResource } from 'frappe-ui'

const dashboardData = createResource({
  url: 'property_management.api.get_tenant_dashboard',
  auto: true,
  onSuccess(data) {
    console.log('Dashboard data loaded:', data)
  },
  onError(error) {
    console.error('Dashboard error:', error)
  }
})

const showServiceRequestModal = ref(false)
const submittingRequest = ref(false)
const serviceRequestError = ref('')
const serviceRequestSuccess = ref('')

const serviceRequestForm = ref({
  request_type: '',
  category: '',
  priority: 'Medium',
  description: ''
})

const openRequestsCount = computed(() => {
  if (!dashboardData.data?.service_requests) return 0
  return dashboardData.data.service_requests.filter(r => r.status === 'Open' || r.status === 'In Progress').length
})

const daysUntilExpiry = computed(() => {
  if (!dashboardData.data?.active_tenancy?.lease_end_date) return 'N/A'
  const endDate = new Date(dashboardData.data.active_tenancy.lease_end_date)
  const today = new Date()
  const diffTime = endDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  return diffDays > 0 ? `${diffDays} days` : 'Expired'
})

const formatCurrency = (amount) => {
  if (!amount) return '₹0'
  return `₹${parseFloat(amount).toLocaleString('en-IN')}`
}

const formatDate = (date) => {
  if (!date) return 'N/A'
  return new Date(date).toLocaleDateString('en-IN', { year: 'numeric', month: 'short', day: 'numeric' })
}

const getStatusClass = (status) => {
  const classes = {
    'Open': 'bg-blue-100 text-blue-800',
    'In Progress': 'bg-yellow-100 text-yellow-800',
    'Resolved': 'bg-green-100 text-green-800',
    'Closed': 'bg-gray-100 text-gray-800',
    'Cancelled': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPriorityClass = (priority) => {
  const classes = {
    'Low': 'bg-gray-100 text-gray-700',
    'Medium': 'bg-blue-100 text-blue-700',
    'High': 'bg-orange-100 text-orange-700',
    'Emergency': 'bg-red-100 text-red-700'
  }
  return classes[priority] || 'bg-gray-100 text-gray-700'
}

const stripHtml = (html) => {
  if (!html) return ''
  const tmp = document.createElement('div')
  tmp.innerHTML = html
  return tmp.textContent || tmp.innerText || ''
}

const getInvoiceStatusClass = (status) => {
  const classes = {
    'Paid': 'bg-green-100 text-green-800',
    'Unpaid': 'bg-red-100 text-red-800',
    'Overdue': 'bg-red-100 text-red-800',
    'Partly Paid': 'bg-yellow-100 text-yellow-800',
    'Return': 'bg-gray-100 text-gray-800',
    'Draft': 'bg-gray-100 text-gray-800',
    'Submitted': 'bg-blue-100 text-blue-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const submitServiceRequest = async () => {
  if (!dashboardData.data?.unit_details?.name) {
    serviceRequestError.value = 'No active unit found'
    return
  }

  serviceRequestError.value = ''
  serviceRequestSuccess.value = ''
  submittingRequest.value = true

  try {
    const response = await createResource({
      url: 'property_management.api.create_service_request',
      params: {
        unit: dashboardData.data.unit_details.name,
        request_type: serviceRequestForm.value.request_type,
        category: serviceRequestForm.value.category,
        priority: serviceRequestForm.value.priority,
        description: serviceRequestForm.value.description
      }
    }).submit()

    serviceRequestSuccess.value = 'Service request submitted successfully!'
    
    // Reset form
    serviceRequestForm.value = {
      request_type: '',
      category: '',
      priority: 'Medium',
      description: ''
    }

    // Reload dashboard data
    setTimeout(() => {
      dashboardData.reload()
      closeServiceRequestModal()
    }, 2000)
  } catch (error) {
    serviceRequestError.value = error.message || 'Failed to submit service request'
  } finally {
    submittingRequest.value = false
  }
}

const closeServiceRequestModal = () => {
  showServiceRequestModal.value = false
  serviceRequestError.value = ''
  serviceRequestSuccess.value = ''
  serviceRequestForm.value = {
    request_type: '',
    category: '',
    priority: 'Medium',
    description: ''
  }
}
</script>
