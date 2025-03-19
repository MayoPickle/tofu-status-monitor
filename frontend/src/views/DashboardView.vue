<template>
  <div class="dashboard">
    <!-- Dashboard Header with Overview Information -->
    <div class="dashboard-header">
      <div class="dashboard-title">
        <h1>Dashboard Overview</h1>
        <p class="text-secondary">Real-time monitoring and system performance</p>
      </div>
      <div class="user-info">
        <div class="connection-status" :class="connectionStatus">
          <span v-if="connectionStatus === 'connected'" class="status-icon pulse-success">●</span>
          <span v-else-if="connectionStatus === 'reconnecting'" class="status-icon pulse-warning">◌</span>
          <span v-else class="status-icon pulse-danger">✕</span>
          <span class="status-text">{{ connectionStatusText }}</span>
        </div>
        <div class="user-profile" v-if="currentUser">
          <span class="username">{{ currentUser.name || currentUser.username || 'Guest' }}</span>
          <span class="badge" :class="'badge-' + (currentUser.role === 'admin' ? 'primary' : 'secondary')">{{ currentUser.role }}</span>
        </div>
      </div>
    </div>
    
    <!-- Loading State -->
    <transition name="fade-up" mode="out-in">
      <div v-if="loading && !error" class="loading-container">
        <div class="spinner"></div>
        <p>Loading data...</p>
      </div>
    </transition>
    
    <!-- Error State -->
    <transition name="fade-up" mode="out-in">
      <div v-if="error" class="error-container card">
        <div class="error-icon">
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path fill="currentColor" d="M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M15.59,7L12,10.59L8.41,7L7,8.41L10.59,12L7,15.59L8.41,17L12,13.41L15.59,17L17,15.59L13.41,12L17,8.41L15.59,7Z" />
          </svg>
        </div>
        <p class="error">{{ error }}</p>
        <button v-if="connectionStatus === 'disconnected'" class="btn btn-primary" @click="retryConnection">
          Retry Connection
        </button>
      </div>
    </transition>
    
    <!-- No Sites Message -->
    <transition name="fade-up" mode="out-in">
      <div v-if="monitoredSites.length === 0" class="no-sites-message card">
        <div class="empty-state">
          <svg viewBox="0 0 24 24" width="48" height="48">
            <path fill="currentColor" d="M19,20H4C2.89,20 2,19.1 2,18V6C2,4.89 2.89,4 4,4H10L12,6H19A2,2 0 0,1 21,8H21L4,8V18L6.14,10H23.21L20.93,18.5C20.7,19.37 19.92,20 19,20Z" />
          </svg>
          <h2>No Monitoring Sites Available</h2>
          <p>You don't have access to any monitoring sites. Please contact your administrator.</p>
        </div>
      </div>
    </transition>
    
    <!-- Dashboard Content (visible when there are sites and data is loaded) -->
    <div v-if="(!loading || connectionStatus === 'reconnecting') && monitoredSites.length > 0">
      <!-- Site Selection Tabs -->
      <SiteTabs 
        v-model="selectedSite" 
        :sites="monitoredSites" 
        :site-status="siteStatus" 
        :show-add-button="canAddSites"
        @add="showAddSiteModal = true"
      />
      
      <!-- Access Denied -->
      <transition name="fade-up" mode="out-in">
        <div v-if="!canViewCurrentSite" class="access-denied card">
          <div class="empty-state">
            <svg viewBox="0 0 24 24" width="48" height="48">
              <path fill="currentColor" d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,5A3,3 0 0,1 15,8A3,3 0 0,1 12,11A3,3 0 0,1 9,8A3,3 0 0,1 12,5M17.13,17C15.92,18.85 14.11,20.24 12,20.92C9.89,20.24 8.08,18.85 6.87,17C6.53,16.5 6.24,16 6,15.47C6,13.82 8.71,12.47 12,12.47C15.29,12.47 18,13.79 18,15.47C17.76,16 17.47,16.5 17.13,17Z" />
            </svg>
            <h2>Access Denied</h2>
            <p>You don't have permission to view this monitoring site.</p>
          </div>
        </div>
      </transition>
      
      <!-- Dashboard content for selected site -->
      <transition name="fade-up" mode="out-in">
        <div v-if="canViewCurrentSite" class="dashboard-grid" :class="{ 'limited-view': !canViewDetailedMetrics }">
          <!-- Status Card -->
          <StatusCard 
            :status="currentStatus" 
            :last-checked="lastChecked" 
            :url="selectedSiteUrl"
          />
          
          <!-- Statistics Card (for authorized users) -->
          <StatsCard 
            v-if="canViewDetailedMetrics" 
            title="24h Statistics"
            :stats="statsItems"
            @refresh="refreshStats"
          />
          
          <!-- Uptime Card -->
          <UptimeCard 
            v-if="canViewDetailedMetrics" 
            :uptime-items="uptimeItems"
          />
          
          <!-- Alerts Card -->
          <AlertsCard 
            v-if="canViewDetailedMetrics" 
            :alerts="recentAlerts"
          />
          
          <!-- Response Time Chart Card -->
          <ChartCard 
            title="Response Times"
            v-model="selectedChartPeriod"
            :periods="chartPeriods"
            :limited="!canViewDetailedMetrics"
            :has-chart-data="chartData.labels.length > 0"
            :extra-classes="{ 'limited-data': !canViewDetailedMetrics }"
          >
            <LineChart 
              v-if="chartData.labels.length && canViewDetailedMetrics" 
              :chart-data="chartData"
              :options="chartOptions"
            />
          </ChartCard>
        </div>
      </transition>
    </div>
    
    <!-- Add Site Modal -->
    <AddSiteModal 
      v-model="showAddSiteModal" 
      @submit="addNewSite"
    />
  </div>
</template>

<script>
import { ref, onMounted, computed, watch, onUnmounted, reactive } from 'vue'
import axios from 'axios'
import { LineChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'
import userStore, { PERMISSIONS } from '../store/userStore'

// Import components
import StatusCard from '@/components/StatusCard.vue'
import StatsCard from '@/components/StatsCard.vue'
import UptimeCard from '@/components/UptimeCard.vue'
import AlertsCard from '@/components/AlertsCard.vue'
import ChartCard from '@/components/ChartCard.vue'
import SiteTabs from '@/components/SiteTabs.vue'
import AddSiteModal from '@/components/AddSiteModal.vue'

Chart.register(...registerables)

export default {
  name: 'DashboardView',
  components: {
    LineChart,
    StatusCard,
    StatsCard,
    UptimeCard,
    AlertsCard,
    ChartCard,
    SiteTabs,
    AddSiteModal
  },
  setup() {
    const apiUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000'
    const loading = ref(true)
    const error = ref(null)
    const recentMetrics = ref([])
    const connectionStatus = ref('connected') // 'connected', 'reconnecting', 'disconnected'
    const reconnectAttempts = ref(0)
    const maxReconnectAttempts = 5
    const reconnectInterval = ref(null)
    const stats = ref({
      total_requests_24h: 0,
      successful_requests_24h: 0,
      failed_requests_24h: 0,
      success_rate_24h: 0,
      avg_response_time_24h: 0
    })
    
    // Multiple site monitoring
    const monitoredSites = ref([])
    
    // Fetch monitored sites from backend
    const fetchMonitoredSites = async () => {
      try {
        const response = await axios.get(`${apiUrl}/sites`)
        monitoredSites.value = response.data
      } catch (err) {
        console.error('Error fetching monitored sites:', err)
        // Fallback to default values if API fails
        monitoredSites.value = [
          { id: 'main', name: 'Main API', url: 'Loading...' }
        ]
      }
    }
    
    // User role permissions
    const canViewDetailedMetrics = computed(() => 
      userStore.hasPermission(PERMISSIONS.VIEW_DETAILED_METRICS)
    )
    
    const canAddSites = computed(() => 
      userStore.hasPermission(PERMISSIONS.ADD_SITES)
    )
    
    const isAdmin = computed(() => userStore.isAdmin())
    
    // Filter sites based on user permissions
    const accessibleSites = computed(() => {
      if (isAdmin.value || userStore.isMaintainer()) {
        return monitoredSites.value
      }
      
      // Regular users can only see their assigned sites
      return monitoredSites.value.filter(site => 
        userStore.canAccessSite(site.id)
      )
    })
    
    const selectedSite = ref('main')
    
    // Set initial site selection based on accessible sites
    watch(() => accessibleSites.value, (sites) => {
      if (sites.length > 0 && !sites.some(site => site.id === selectedSite.value)) {
        selectedSite.value = sites[0].id
      }
    }, { immediate: true })
    
    const fetchData = async () => {
      if (connectionStatus.value === 'disconnected' && reconnectAttempts.value >= maxReconnectAttempts) {
        return // Stop trying if max attempts reached
      }
      
      loading.value = connectionStatus.value !== 'reconnecting' // Don't show loading if reconnecting
      error.value = null
      
      try {
        // Get the current selected site
        const site = monitoredSites.value.find(s => s.id === selectedSite.value)
        
        // Fetch recent metrics for the selected site
        const metricsResponse = await axios.get(`${apiUrl}/metrics/recent`, {
          params: { 
            limit: 20,
            site: site.id
          },
          timeout: 10000 // 10 second timeout
        })
        recentMetrics.value = metricsResponse.data.reverse() // Reverse to get chronological order
        
        // Fetch statistics for the selected site
        const statsResponse = await axios.get(`${apiUrl}/metrics/stats`, {
          params: { site: site.id },
          timeout: 10000 // 10 second timeout
        })
        stats.value = statsResponse.data
        
        // Reset connection status if previously reconnecting
        if (connectionStatus.value === 'reconnecting') {
          connectionStatus.value = 'connected'
          reconnectAttempts.value = 0
          if (reconnectInterval.value) {
            clearInterval(reconnectInterval.value)
            reconnectInterval.value = null
          }
        }
        
        loading.value = false
      } catch (err) {
        console.error('API Error:', err)
        
        // Handle different error scenarios
        if (err.code === 'ECONNABORTED') {
          error.value = 'Connection timed out. Server may be under heavy load.'
        } else if (err.response) {
          // The server responded with an error status code
          error.value = `Server error: ${err.response.status} - ${err.response.statusText}`
        } else if (err.request) {
          // Request was made but no response received
          if (connectionStatus.value === 'connected') {
            connectionStatus.value = 'reconnecting'
            reconnectAttempts.value = 1
            error.value = 'Connection to server lost. Attempting to reconnect...'
            
            // Setup reconnect interval if not already set
            if (!reconnectInterval.value) {
              reconnectInterval.value = setInterval(() => {
                if (reconnectAttempts.value < maxReconnectAttempts) {
                  reconnectAttempts.value++
                  error.value = `Connection to server lost. Reconnect attempt ${reconnectAttempts.value}/${maxReconnectAttempts}...`
                  fetchData()
                } else {
                  connectionStatus.value = 'disconnected'
                  error.value = 'Unable to connect to the server. Please check your network connection or try again later.'
                  clearInterval(reconnectInterval.value)
                }
              }, 5000) // Try every 5 seconds
            }
          }
        } else {
          // Something else happened
          error.value = `Error loading data: ${err.message}`
        }
        
        loading.value = false
      }
    }
    
    const currentStatus = computed(() => {
      if (recentMetrics.value.length === 0) return 'Unknown'
      
      const lastMetric = recentMetrics.value[recentMetrics.value.length - 1]
      return (lastMetric.status_code >= 200 && lastMetric.status_code < 300) ? 'Good' : 'Bad'
    })
    
    const lastChecked = computed(() => {
      if (recentMetrics.value.length === 0) return 'Never'
      
      const lastMetric = recentMetrics.value[recentMetrics.value.length - 1]
      return new Date(lastMetric.timestamp).toLocaleString()
    })
    
    const chartData = computed(() => {
      let dataPoints = []
      let labels = []
      
      switch (selectedChartPeriod.value) {
        case '24h':
          dataPoints = recentMetrics.value.map(m => m.request_time * 1000)
          labels = recentMetrics.value.map(m => {
            const date = new Date(m.timestamp)
            return `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
          })
          break
          
        case '7d':
          // Mock data for 7 days - in a real app this would come from the API
          dataPoints = Array.from({ length: 7 }, () => Math.floor(100 + Math.random() * 400))
          labels = Array.from({ length: 7 }, (_, i) => {
            const date = new Date()
            date.setDate(date.getDate() - 6 + i)
            return date.toLocaleDateString('en-US', { weekday: 'short' })
          })
          break
          
        case '30d':
          // Mock data for 30 days - in a real app this would come from the API
          dataPoints = Array.from({ length: 30 }, () => Math.floor(100 + Math.random() * 400))
          labels = Array.from({ length: 30 }, (_, i) => {
            const date = new Date()
            date.setDate(date.getDate() - 29 + i)
            return `${date.getDate()}/${date.getMonth() + 1}`
          })
          break
      }
      
      return {
        labels,
        datasets: [
          {
            label: 'Response Time (ms)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            data: dataPoints,
            tension: 0.2
          }
        ]
      }
    })
    
    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: 'Response Time (ms)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Time'
          }
        }
      }
    }
    
    // Calculate uptime percentage (placeholder function)
    const calculateUptime = (hours) => {
      // This is a placeholder - in a real app, you'd calculate this from actual data
      // For now, just return a random value between 95 and 99.9
      return (95 + Math.random() * 4.9).toFixed(2)
    }
    
    // Calculate monthly uptime
    const calculateMonthlyUptime = () => {
      // In a real app, this would calculate uptime for the current month
      return (97 + Math.random() * 2.9).toFixed(2)
    }
    
    // Get uptime class based on the value
    const getUptimeClass = (hours) => {
      const value = parseFloat(hours ? calculateUptime(hours) : calculateMonthlyUptime())
      if (value >= 99.9) return 'excellent'
      if (value >= 99.0) return 'good'
      if (value >= 98.0) return 'average'
      return 'poor'
    }
    
    // Retry connection after disconnect
    const retryConnection = () => {
      connectionStatus.value = 'reconnecting'
      reconnectAttempts.value = 1
      fetchData()
    }
    
    // Connection status text
    const connectionStatusText = computed(() => {
      switch (connectionStatus.value) {
        case 'connected': return 'Connected'
        case 'reconnecting': return `Reconnecting (${reconnectAttempts.value}/${maxReconnectAttempts})`
        case 'disconnected': return 'Disconnected'
        default: return 'Unknown'
      }
    })
    
    // Selected site URL
    const selectedSiteUrl = computed(() => {
      const site = monitoredSites.value.find(s => s.id === selectedSite.value)
      return site ? site.url : ''
    })
    
    // Success rate styling
    const successRateClass = computed(() => {
      const rate = stats.value.success_rate_24h
      if (rate >= 99.9) return 'excellent'
      if (rate >= 99.0) return 'good'
      if (rate >= 95.0) return 'average'
      return 'poor'
    })
    
    // Response time styling
    const responseTimeClass = computed(() => {
      const time = stats.value.avg_response_time_24h * 1000 // ms
      if (time < 100) return 'excellent'
      if (time < 300) return 'good'
      if (time < 1000) return 'average'
      return 'poor'
    })
    
    // Site statuses
    const siteStatus = ref({})
    
    // Fetch status for all sites
    const fetchAllSiteStatuses = async () => {
      for (const site of monitoredSites.value) {
        try {
          const response = await axios.get(`${apiUrl}/metrics/status`, {
            params: { site: site.id },
            timeout: 5000
          })
          siteStatus.value[site.id] = response.data.status
        } catch (err) {
          console.error(`Error fetching status for ${site.id}:`, err)
          siteStatus.value[site.id] = 'Bad'
        }
      }
    }
    
    // Chart periods
    const chartPeriods = [
      { label: '24h', value: '24h' },
      { label: '7d', value: '7d' },
      { label: '30d', value: '30d' }
    ]
    const selectedChartPeriod = ref('24h')
    
    // Add site modal
    const showAddSiteModal = ref(false)
    const newSite = ref({
      id: '',
      name: '',
      url: ''
    })
    
    // Check if new site is valid
    const isNewSiteValid = computed(() => {
      return newSite.value.id && 
             newSite.value.name && 
             newSite.value.url && 
             newSite.value.url.startsWith('http')
    })
    
    // Add new site
    const addNewSite = (siteData) => {
      monitoredSites.value.push({ ...siteData })
      selectedSite.value = siteData.id
    }
    
    // Mock recent alerts (in a real app, these would come from the API)
    const recentAlerts = ref([
      { 
        timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000), // 2 hours ago
        message: 'Response time threshold exceeded (500ms)', 
        severity: 'warning'
      },
      { 
        timestamp: new Date(Date.now() - 12 * 60 * 60 * 1000), // 12 hours ago
        message: 'Service unavailable for 3 minutes', 
        severity: 'critical'
      },
      { 
        timestamp: new Date(Date.now() - 25 * 60 * 60 * 1000), // 25 hours ago
        message: 'SSL certificate expiring in 10 days', 
        severity: 'info'
      }
    ])
    
    // Format alert time - now moved to AlertsCard component
    
    // Check if current user can access the site
    const canViewCurrentSite = computed(() => {
      return userStore.canAccessSite(selectedSite.value)
    })
    
    // Get current user from store
    const currentUser = computed(() => userStore.currentUser())
    
    // Computed property for status badge class - now in StatusCard component
    
    // Refresh stats function for the refresh button
    const refreshStats = async () => {
      try {
        const site = monitoredSites.value.find(s => s.id === selectedSite.value)
        if (!site) return
        
        const statsResponse = await axios.get(`${apiUrl}/metrics/stats`, {
          params: { site: site.id },
          timeout: 5000 // shorter timeout for a quick refresh
        })
        
        stats.value = statsResponse.data
      } catch (err) {
        console.error('Error refreshing stats:', err)
      }
    }
    
    // Computed property for stats items for StatsCard
    const statsItems = computed(() => [
      {
        label: 'Total Requests',
        value: stats.value.total_requests_24h
      },
      {
        label: 'Success Rate',
        value: `${stats.value.success_rate_24h.toFixed(2)}%`,
        class: successRateClass.value
      },
      {
        label: 'Avg Response Time',
        value: `${(stats.value.avg_response_time_24h * 1000).toFixed(2)} ms`,
        class: responseTimeClass.value
      },
      {
        label: 'Failed Requests',
        value: stats.value.failed_requests_24h
      }
    ])
    
    // Computed property for uptime items for UptimeCard
    const uptimeItems = computed(() => [
      {
        label: 'Last 24h',
        value: calculateUptime(24)
      },
      {
        label: 'Last 7 days',
        value: calculateUptime(168)
      },
      {
        label: 'Last 30 days',
        value: calculateUptime(720)
      },
      {
        label: 'Current Month',
        value: calculateMonthlyUptime()
      }
    ])
    
    onMounted(async () => {
      // First fetch site information
      await fetchMonitoredSites()
      
      // Then fetch data for the selected site
      fetchData()
      fetchAllSiteStatuses()
      
      // Refresh data every 60 seconds
      const refreshInterval = setInterval(fetchData, 60000)
      
      // Refresh site statuses every 3 minutes
      const statusInterval = setInterval(fetchAllSiteStatuses, 180000)
      
      // Clean up intervals on component unmount
      onUnmounted(() => {
        clearInterval(refreshInterval)
        clearInterval(statusInterval)
        if (reconnectInterval.value) {
          clearInterval(reconnectInterval.value)
        }
      })
    })
    
    // Watch for changes in chart period and selected site
    watch([selectedChartPeriod, selectedSite], () => {
      fetchData()
    })
    
    return {
      loading,
      error,
      stats,
      currentStatus,
      lastChecked,
      chartData,
      chartOptions,
      monitoredSites: accessibleSites,
      selectedSite,
      connectionStatus,
      connectionStatusText,
      retryConnection,
      chartPeriods,
      selectedChartPeriod,
      showAddSiteModal,
      addNewSite,
      selectedSiteUrl,
      siteStatus,
      recentAlerts,
      canViewDetailedMetrics,
      canAddSites,
      isAdmin,
      canViewCurrentSite,
      currentUser,
      refreshStats,
      statsItems,
      uptimeItems,
      fetchMonitoredSites
    }
  }
}
</script>

<style scoped>
.dashboard {
  width: 100%;
}

/* Dashboard Header */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1rem;
  background-color: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-color);
}

.dashboard-title h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
  letter-spacing: -0.5px;
}

.text-secondary {
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.connection-status {
  display: flex;
  align-items: center;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  background-color: var(--bg-secondary);
  font-weight: 500;
  border: 1px solid var(--border-color);
}

.status-icon {
  margin-right: 0.5rem;
  font-size: 0.75rem;
}

.pulse-success {
  color: var(--success);
  animation: pulse 2s infinite;
}

.pulse-warning {
  color: var(--accent);
  animation: pulse 2s infinite;
}

.pulse-danger {
  color: var(--danger);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% {
    opacity: 1;
    text-shadow: 0 0 0 currentColor;
  }
  50% {
    opacity: 0.6;
    text-shadow: 0 0 10px currentColor;
  }
  100% {
    opacity: 1;
    text-shadow: 0 0 0 currentColor;
  }
}

.connected {
  color: var(--success);
}

.reconnecting {
  color: var(--accent);
}

.disconnected {
  color: var(--danger);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.5rem 0.75rem;
  border-radius: var(--radius);
  background-color: var(--bg-secondary);
  border: 1px solid var(--border-color);
}

.username {
  font-weight: 500;
  color: var(--text-primary);
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.badge-primary {
  background-color: rgba(58, 134, 255, 0.1);
  color: var(--primary);
}

.badge-secondary {
  background-color: rgba(251, 86, 7, 0.1);
  color: var(--secondary);
}

/* Loading and Error States */
.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  padding: 3rem;
  background-color: var(--bg-card);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow);
  margin-bottom: 1.5rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(58, 134, 255, 0.2);
  border-radius: 50%;
  border-top-color: var(--primary);
  animation: spin 1s ease-in-out infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
}

.error-icon {
  color: var(--danger);
}

.error {
  color: var(--danger);
  font-weight: 500;
}

.no-sites-message, .access-denied {
  padding: 3rem 2rem;
  text-align: center;
  margin-bottom: 1.5rem;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  color: var(--text-secondary);
}

.empty-state svg {
  color: var(--text-secondary);
  opacity: 0.5;
}

.empty-state h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.empty-state p {
  max-width: 400px;
  margin: 0 auto;
}

/* Dashboard Grid */
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.limited-view {
  grid-template-columns: 1fr;
  max-width: 500px;
  margin: 0 auto;
}

/* Animations */
.fade-up-enter-active,
.fade-up-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
  
  .user-info {
    width: 100%;
    flex-direction: column;
    align-items: flex-start;
  }
  
  .connection-status, .user-profile {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style> 