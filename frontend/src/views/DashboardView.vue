<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Dashboard</h1>
      <div class="user-info">
        <div class="connection-status" :class="connectionStatus">
          <span v-if="connectionStatus === 'connected'" class="status-icon">●</span>
          <span v-else-if="connectionStatus === 'reconnecting'" class="status-icon">◌</span>
          <span v-else class="status-icon">✕</span>
          <span class="status-text">{{ connectionStatusText }}</span>
        </div>
        <div class="user-profile" v-if="currentUser">
          <span class="username">{{ currentUser.name || currentUser.username || 'Guest' }}</span>
          <span class="role-badge" :class="currentUser.role">{{ currentUser.role }}</span>
        </div>
      </div>
    </div>
    
    <div v-if="loading && !error">
      <div class="loading-indicator">
        <div class="spinner"></div>
        <p>Loading data...</p>
      </div>
    </div>
    
    <div v-if="error" class="error-container">
      <p class="error">{{ error }}</p>
      <button v-if="connectionStatus === 'disconnected'" class="retry-button" @click="retryConnection">
        Retry Connection
      </button>
    </div>
    
    <div v-if="monitoredSites.length === 0" class="no-sites-message">
      <h2>No Monitoring Sites Available</h2>
      <p>You don't have access to any monitoring sites. Please contact your administrator.</p>
    </div>
    
    <div v-if="(!loading || connectionStatus === 'reconnecting') && monitoredSites.length > 0">
      <!-- Site selection tabs -->
      <div class="site-tabs">
        <button 
          v-for="site in monitoredSites" 
          :key="site.id"
          :class="['site-tab', { active: selectedSite === site.id }]"
          @click="selectedSite = site.id"
        >
          {{ site.name }}
          <span 
            v-if="siteStatus[site.id]" 
            class="site-status-indicator"
            :class="{'status-good': siteStatus[site.id] === 'Good', 'status-bad': siteStatus[site.id] === 'Bad'}"
          ></span>
        </button>
        <button v-if="canAddSites" class="site-tab add-site-button" @click="showAddSiteModal = true">
          <span class="add-icon">+</span> Add Site
        </button>
      </div>
      
      <!-- Access Denied -->
      <div v-if="!canViewCurrentSite" class="access-denied">
        <h2>Access Denied</h2>
        <p>You don't have permission to view this monitoring site.</p>
      </div>
      
      <!-- Dashboard content for selected site -->
      <div v-if="canViewCurrentSite" class="dashboard-grid" :class="{ 'limited-view': !canViewDetailedMetrics }">
        <div class="card status-card">
          <h2>Current Status</h2>
          <div class="status" :class="{'status-good': currentStatus === 'Good', 'status-bad': currentStatus === 'Bad', 'status-unknown': currentStatus === 'Unknown'}">
            {{ currentStatus }}
          </div>
          <p class="last-checked">Last checked: {{ lastChecked }}</p>
          <div class="url-info">
            <span class="url-label">Monitoring URL:</span>
            <span class="url-value">{{ selectedSiteUrl }}</span>
          </div>
        </div>
        
        <!-- Detailed metrics only shown to authorized users -->
        <div v-if="canViewDetailedMetrics" class="card">
          <h2>24h Statistics</h2>
          <div class="stats">
            <div class="stat">
              <span class="stat-label">Total Requests:</span>
              <span class="stat-value">{{ stats.total_requests_24h }}</span>
            </div>
            <div class="stat">
              <span class="stat-label">Success Rate:</span>
              <span class="stat-value" :class="successRateClass">{{ stats.success_rate_24h.toFixed(2) }}%</span>
            </div>
            <div class="stat">
              <span class="stat-label">Avg Response Time:</span>
              <span class="stat-value" :class="responseTimeClass">{{ (stats.avg_response_time_24h * 1000).toFixed(2) }} ms</span>
            </div>
            <div class="stat">
              <span class="stat-label">Failed Requests:</span>
              <span class="stat-value">{{ stats.failed_requests_24h }}</span>
            </div>
          </div>
        </div>
        
        <div v-if="canViewDetailedMetrics" class="card">
          <h2>Uptime</h2>
          <div class="stats">
            <div class="stat">
              <span class="stat-label">Last 24h:</span>
              <span class="stat-value" :class="getUptimeClass(24)">{{ calculateUptime(24) }}%</span>
            </div>
            <div class="stat">
              <span class="stat-label">Last 7 days:</span>
              <span class="stat-value" :class="getUptimeClass(168)">{{ calculateUptime(168) }}%</span>
            </div>
            <div class="stat">
              <span class="stat-label">Last 30 days:</span>
              <span class="stat-value" :class="getUptimeClass(720)">{{ calculateUptime(720) }}%</span>
            </div>
            <div class="stat">
              <span class="stat-label">Current Month:</span>
              <span class="stat-value" :class="getUptimeClass(0)">{{ calculateMonthlyUptime() }}%</span>
            </div>
          </div>
        </div>
        
        <div v-if="canViewDetailedMetrics" class="card alerts-card">
          <h2>Recent Alerts</h2>
          <div v-if="recentAlerts.length" class="alerts-list">
            <div v-for="(alert, index) in recentAlerts" :key="index" class="alert-item" :class="alert.severity">
              <span class="alert-time">{{ formatAlertTime(alert.timestamp) }}</span>
              <span class="alert-message">{{ alert.message }}</span>
            </div>
          </div>
          <p v-else class="no-data">No recent alerts</p>
        </div>
        
        <div class="card full-width chart-card" :class="{ 'limited-data': !canViewDetailedMetrics }">
          <div class="chart-header">
            <h2>Response Times</h2>
            <div v-if="canViewDetailedMetrics" class="chart-controls">
              <button 
                v-for="period in chartPeriods" 
                :key="period.value" 
                :class="['chart-period-button', { active: selectedChartPeriod === period.value }]"
                @click="selectedChartPeriod = period.value"
              >
                {{ period.label }}
              </button>
            </div>
          </div>
          
          <div v-if="!canViewDetailedMetrics" class="limited-access-message">
            <p>You have limited access to this monitoring site.</p>
            <p>Login with higher privileges to view detailed metrics and historical data.</p>
          </div>
          
          <div v-else class="chart-container">
            <LineChart 
              v-if="chartData.labels.length" 
              :chart-data="chartData"
              :options="chartOptions"
            />
            <p v-else class="no-data">No data available</p>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Add Site Modal (hidden by default) -->
    <div v-if="showAddSiteModal && canAddSites" class="modal-backdrop" @click.self="showAddSiteModal = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Add Monitoring Site</h3>
          <button class="close-button" @click="showAddSiteModal = false">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="site-name">Site Name</label>
            <input type="text" id="site-name" v-model="newSite.name" placeholder="Production API">
          </div>
          <div class="form-group">
            <label for="site-url">URL to Monitor</label>
            <input type="text" id="site-url" v-model="newSite.url" placeholder="https://api.example.com/health">
          </div>
          <div class="form-group">
            <label for="site-id">Site ID (for API)</label>
            <input type="text" id="site-id" v-model="newSite.id" placeholder="prod-api">
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-button" @click="showAddSiteModal = false">Cancel</button>
          <button class="add-button" @click="addNewSite" :disabled="!isNewSiteValid">Add Site</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import axios from 'axios'
import { LineChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'
import userStore, { PERMISSIONS } from '../store/userStore'

Chart.register(...registerables)

export default {
  name: 'DashboardView',
  components: {
    LineChart
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
    const monitoredSites = ref([
      { id: 'main', name: 'Main API', url: 'https://api.example.com' },
      { id: 'backup', name: 'Backup API', url: 'https://backup-api.example.com' },
      { id: 'staging', name: 'Staging', url: 'https://staging-api.example.com' }
    ])
    
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
      return (hours + Math.random() * 4.9).toFixed(2)
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
    const addNewSite = () => {
      if (isNewSiteValid.value) {
        monitoredSites.value.push({ ...newSite.value })
        showAddSiteModal.value = false
        newSite.value = { id: '', name: '', url: '' }
        selectedSite.value = monitoredSites.value[monitoredSites.value.length - 1].id
      }
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
    
    // Format alert time
    const formatAlertTime = (timestamp) => {
      const date = new Date(timestamp)
      const now = new Date()
      const diffMs = now - date
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60))
      
      if (diffHours < 24) {
        return `${diffHours}h ago`
      } else {
        return date.toLocaleDateString()
      }
    }
    
    // Check if current user can access the site
    const canViewCurrentSite = computed(() => {
      return userStore.canAccessSite(selectedSite.value)
    })
    
    onMounted(() => {
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
      recentMetrics,
      stats,
      currentStatus,
      lastChecked,
      chartData,
      chartOptions,
      monitoredSites: accessibleSites,
      selectedSite,
      calculateUptime,
      connectionStatus,
      connectionStatusText,
      retryConnection,
      chartPeriods,
      selectedChartPeriod,
      showAddSiteModal: computed(() => showAddSiteModal.value && canAddSites.value),
      newSite,
      isNewSiteValid,
      addNewSite,
      selectedSiteUrl,
      siteStatus,
      recentAlerts,
      formatAlertTime,
      getUptimeClass,
      successRateClass,
      responseTimeClass,
      calculateMonthlyUptime,
      canViewDetailedMetrics,
      canAddSites,
      isAdmin,
      canViewCurrentSite,
      currentUser: computed(() => userStore.currentUser())
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 100%;
  height: 100%;
  background-color: var(--bg-body);
}

.dashboard-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  margin-bottom: 1rem;
  border-radius: var(--radius);
  background-color: var(--bg-secondary);
  box-shadow: var(--shadow);
}

.dashboard-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(120deg, var(--primary) 0%, var(--primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1.25rem;
}

.connection-status {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius);
  background-color: var(--bg-body);
  border: 1px solid var(--border-color);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.connection-status::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  transition: var(--transition);
}

.connection-status.connected::before {
  background-color: var(--success);
  box-shadow: 0 0 10px var(--success);
}

.connection-status.reconnecting::before {
  background-color: var(--secondary);
  box-shadow: 0 0 10px var(--secondary);
  animation: pulse 2s infinite;
}

.connection-status.disconnected::before {
  background-color: var(--danger);
  box-shadow: 0 0 10px var(--danger);
}

.status-icon {
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  transition: var(--transition);
}

.connection-status.connected .status-icon {
  color: var(--success);
  background-color: rgba(82, 183, 136, 0.1);
}

.connection-status.reconnecting .status-icon {
  color: var(--secondary);
  background-color: rgba(233, 196, 106, 0.1);
  animation: pulse 2s infinite;
}

.connection-status.disconnected .status-icon {
  color: var(--danger);
  background-color: rgba(231, 111, 81, 0.1);
}

.status-text {
  font-weight: 500;
  font-size: 0.875rem;
  color: var(--text-primary);
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.25rem;
  background-color: var(--bg-body);
  border-radius: var(--radius);
  border: 1px solid var(--border-color);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.user-profile::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 3px;
  height: 100%;
  background: linear-gradient(to bottom, var(--primary), var(--primary-light));
  opacity: 0;
  transition: var(--transition);
}

.user-profile:hover::before {
  opacity: 1;
}

.username {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
  letter-spacing: 0.5px;
  transition: var(--transition);
}

.role-badge.admin {
  background-color: rgba(231, 111, 81, 0.1);
  color: var(--danger);
}

.role-badge.maintainer {
  background-color: rgba(82, 183, 136, 0.1);
  color: var(--success);
}

.role-badge.user {
  background-color: rgba(42, 157, 143, 0.1);
  color: var(--primary);
}

.role-badge.guest {
  background-color: rgba(108, 117, 125, 0.1);
  color: var(--gray);
}

.site-tabs {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 2rem;
  padding: 0.5rem;
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow-x: auto;
  scrollbar-width: thin;
}

.site-tab {
  padding: 0.75rem 1.5rem;
  border: none;
  background-color: transparent;
  color: var(--text-secondary);
  font-weight: 500;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  white-space: nowrap;
  position: relative;
}

.site-tab:hover {
  color: var(--primary);
  background-color: rgba(42, 157, 143, 0.1);
}

.site-tab.active {
  color: var(--primary);
  background-color: rgba(42, 157, 143, 0.15);
}

.site-tab .site-status-indicator {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  transition: var(--transition);
}

.site-status-indicator.status-good {
  background-color: var(--success);
  box-shadow: 0 0 8px var(--success);
}

.site-status-indicator.status-bad {
  background-color: var(--danger);
  box-shadow: 0 0 8px var(--danger);
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.card {
  background: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  transition: var(--transition);
  border: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
  opacity: 0;
  transition: var(--transition);
}

.card:hover::before {
  opacity: 1;
}

.card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.status {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  margin: 1.5rem 0;
  transition: var(--transition);
}

.status.status-good {
  color: var(--success);
  text-shadow: 0 0 15px rgba(82, 183, 136, 0.4);
}

.status.status-bad {
  color: var(--danger);
  text-shadow: 0 0 15px rgba(231, 111, 81, 0.4);
}

.status.status-unknown {
  color: var(--gray);
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.stat {
  padding: 1rem;
  background-color: var(--bg-body);
  border-radius: var(--radius);
  transition: var(--transition);
}

.stat:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
  display: block;
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  transition: var(--transition);
}

.stat-value.excellent {
  color: var(--success);
  text-shadow: 0 0 10px rgba(82, 183, 136, 0.3);
}

.stat-value.good {
  color: var(--primary);
  text-shadow: 0 0 10px rgba(42, 157, 143, 0.3);
}

.stat-value.average {
  color: var(--secondary);
  text-shadow: 0 0 10px rgba(233, 196, 106, 0.3);
}

.stat-value.poor {
  color: var(--danger);
  text-shadow: 0 0 10px rgba(231, 111, 81, 0.3);
}

.chart-card {
  grid-column: 1 / -1;
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.chart-controls {
  display: flex;
  gap: 0.5rem;
  background-color: var(--bg-body);
  padding: 0.25rem;
  border-radius: var(--radius);
}

.chart-period-button {
  padding: 0.5rem 1rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
}

.chart-period-button:hover {
  color: var(--primary);
  background-color: rgba(42, 157, 143, 0.1);
}

.chart-period-button.active {
  color: var(--primary);
  background-color: rgba(42, 157, 143, 0.15);
}

.chart-container {
  height: 400px;
  position: relative;
}

.alerts-card .alerts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.alert-item {
  padding: 1rem;
  border-radius: var(--radius);
  background-color: var(--bg-body);
  border-left: 4px solid;
  transition: var(--transition);
}

.alert-item:hover {
  transform: translateX(4px);
}

.alert-item.info {
  border-left-color: var(--primary);
}

.alert-item.warning {
  border-left-color: var(--secondary);
}

.alert-item.critical {
  border-left-color: var(--danger);
}

.alert-time {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
  display: block;
}

.alert-message {
  color: var(--text-primary);
}

.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 1rem;
}

.spinner {
  width: 48px;
  height: 48px;
  border: 4px solid var(--bg-secondary);
  border-top-color: var(--primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.error-container {
  text-align: center;
  padding: 2rem;
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.retry-button {
  margin-top: 1rem;
  padding: 0.75rem 2rem;
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
  color: white;
  border: none;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
}

.retry-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(42, 157, 143, 0.3);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@media (max-width: 768px) {
  .user-info {
    flex-direction: column;
    align-items: stretch;
    gap: 0.75rem;
    width: 100%;
  }

  .connection-status,
  .user-profile {
    width: 100%;
  }

  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .stats {
    grid-template-columns: 1fr;
  }
  
  .chart-header {
    flex-direction: column;
    gap: 1rem;
  }
  
  .chart-controls {
    width: 100%;
    justify-content: center;
  }
}

.no-data {
  text-align: center;
  color: #666;
  margin-top: 1rem;
}

.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  width: 80%;
  max-width: 600px;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
}

.modal-body {
  margin-bottom: 1rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}

.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.5rem;
}

.cancel-button,
.add-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-button {
  background-color: #f0f0f0;
}

.cancel-button:hover {
  background-color: #e0e0e0;
}

.add-button {
  background-color: #2c3e50;
  color: white;
}

.add-button:hover {
  background-color: #34495e;
}

.stat-value.excellent {
  color: #42b983;
  font-weight: bold;
}

.stat-value.good {
  color: #2c9f6e;
  font-weight: bold;
}

.stat-value.average {
  color: #e6a23c;
  font-weight: bold;
}

.stat-value.poor {
  color: #e53935;
  font-weight: bold;
}

.connection-status.connected .status-icon {
  color: #42b983;
}

.connection-status.reconnecting .status-icon {
  color: #e6a23c;
  animation: blink 1s infinite;
}

.connection-status.disconnected .status-icon {
  color: #e53935;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.alert-item {
  display: flex;
  padding: 0.75rem;
  border-radius: 4px;
  border-left: 4px solid;
}

.alert-item.info {
  background-color: rgba(54, 162, 235, 0.1);
  border-left-color: #36a2eb;
}

.alert-item.warning {
  background-color: rgba(255, 159, 64, 0.1);
  border-left-color: #ff9f40;
}

.alert-item.critical {
  background-color: rgba(229, 57, 53, 0.1);
  border-left-color: #e53935;
}

.alert-time {
  margin-right: 0.75rem;
  color: #666;
  font-size: 0.85rem;
  white-space: nowrap;
}

.status-card .url-info {
  margin-top: 1rem;
  padding-top: 0.5rem;
  border-top: 1px dashed #eee;
  font-size: 0.9rem;
}

.url-label {
  color: #666;
  margin-right: 0.5rem;
}

.url-value {
  word-break: break-all;
  font-family: monospace;
}

.add-site-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.add-icon {
  font-size: 1.2rem;
}

/* Disable button styling */
.add-button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.last-checked {
  color: #666;
  font-size: 0.9rem;
}

.no-sites-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.no-sites-message h2 {
  margin-bottom: 1rem;
}

.no-sites-message p {
  text-align: center;
}

.access-denied {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.access-denied h2 {
  margin-bottom: 1rem;
}

.access-denied p {
  text-align: center;
}

.limited-view {
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.limited-data {
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
}

.limited-access-message {
  padding: 1rem;
  text-align: center;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1.25rem;
  background-color: var(--bg-body);
  border-radius: var(--radius);
  border: 1px solid var(--border-color);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.username {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.875rem;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius);
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: capitalize;
  letter-spacing: 0.5px;
  transition: var(--transition);
}

.role-badge.admin {
  background-color: rgba(231, 111, 81, 0.1);
  color: var(--danger);
}

.role-badge.maintainer {
  background-color: rgba(82, 183, 136, 0.1);
  color: var(--success);
}

.role-badge.user {
  background-color: rgba(42, 157, 143, 0.1);
  color: var(--primary);
}

.role-badge.guest {
  background-color: rgba(108, 117, 125, 0.1);
  color: var(--gray);
}

.chart-card.limited-data {
  position: relative;
}

.limited-access-message {
  background-color: rgba(247, 247, 247, 0.9);
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  color: #666;
}

.limited-access-message p:first-child {
  font-weight: 500;
  margin-bottom: 0.5rem;
}
</style> 