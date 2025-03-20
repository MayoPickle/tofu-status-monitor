<template>
  <div class="dashboard">
    <!-- Dashboard Header -->
    <DashboardHeader 
      :connection-status="connectionStatus"
      :connection-status-text="connectionStatusText"
      :error="error"
      :current-user="currentUser"
      @retry-connection="retryConnection"
    />
    
    <div class="dashboard-content">
      <!-- Site Tabs -->
      <SiteTabs 
        v-model="selectedSite" 
        :sites="monitoredSites" 
        :site-status="siteStatus" 
        :show-add-button="canAddSites"
        @add="showAddSiteModal = true"
      />
      
      <!-- Site Content -->
      <transition name="fade-up" mode="out-in">
        <AccessDenied v-if="!canViewCurrentSite" />
        
        <DashboardContent 
          v-else
          :current-status="currentStatus"
          :last-checked="lastChecked"
          :site-url="selectedSiteUrl"
          :http-status="currentHttpStatus"
          :http-status-text="currentHttpStatusText"
          :can-view-detailed-metrics="canViewDetailedMetrics"
          :can-view-metrics="canViewMetrics"
          :can-access-uptime="canAccessUptime"
          :can-access-historical="canAccessHistorical"
          :has-permission-view-alerts="userStore.hasPermission(PERMISSIONS.VIEW_ALERTS)"
          :stats-items="statsItems"
          :stats-trends="statsTrends"
          :uptime-items="uptimeItems"
          :recent-alerts="recentAlerts"
          :chart-data="chartData"
          :chart-options="chartOptions"
          :chart-periods="chartPeriods"
          :initial-chart-period="selectedChartPeriod"
          :hourly-availability-data="hourlyAvailabilityData"
          @refresh-stats="refreshStats"
          @refresh-hourly="fetchHourlyAvailability"
          @update:chart-period="selectedChartPeriod = $event"
        />
      </transition>
    </div>
    
    <!-- Add Site Modal -->
    <AddSiteModal 
      v-model="showAddSiteModal" 
      @submit="addNewSite"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

// Composables
import useDashboard from '@/composables/useDashboard'

// Components
import DashboardHeader from '@/components/dashboard/DashboardHeader.vue'
import DashboardContent from '@/components/dashboard/DashboardContent.vue'
import AccessDenied from '@/components/dashboard/AccessDenied.vue'
import SiteTabs from '@/components/SiteTabs.vue'
import AddSiteModal from '@/components/AddSiteModal.vue'

// Initialize dashboard composable
const {
  // Status information
  connectionStatus,
  connectionStatusText,
  error,
  currentUser,
  retryConnection,
  
  // Site data
  monitoredSites,
  selectedSite,
  selectedSiteUrl,
  siteStatus,
  canViewCurrentSite,
  canAddSites,
  
  // Stats and metrics
  currentStatus,
  lastChecked,
  currentHttpStatus,
  currentHttpStatusText,
  statsItems,
  statsTrends,
  uptimeItems,
  recentAlerts,
  hourlyAvailabilityData,
  refreshStats,
  
  // Permissions
  canViewDetailedMetrics,
  canViewMetrics,
  canAccessUptime,
  canAccessHistorical,
  userStore,
  PERMISSIONS,
  
  // Chart data
  chartData,
  chartOptions,
  chartPeriods,
  selectedChartPeriod,
  
  // Modal and actions
  showAddSiteModal,
  addNewSite,
  
  // Data fetch methods
  fetchMonitoredSites,
  fetchData,
  fetchAllSiteStatuses,
  fetchUptimeData,
  fetchHistoricalMetrics,
  fetchHourlyAvailability,
  setupDashboard
} = useDashboard()

// Initialize dashboard on component mount
onMounted(async () => {
  // First fetch site information
  await fetchMonitoredSites()
  
  // Then fetch data for the selected site
  fetchData()
  fetchAllSiteStatuses()
  fetchUptimeData()
  
  // Fetch historical data for all periods
  fetchHistoricalMetrics('7d')
  fetchHistoricalMetrics('30d')
  
  // Fetch hourly availability data
  fetchHourlyAvailability()
  
  // Setup dashboard refresh intervals
  setupDashboard()
})
</script>

<style>
@import '@/assets/css/dashboard-styles.css';
@import '@/assets/css/status-colors.css';
</style> 