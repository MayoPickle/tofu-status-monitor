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
      <div class="site-tabs-container">
        <div class="site-tabs">
          <button 
            v-for="site in monitoredSites" 
            :key="site.id"
            :class="['site-tab', { active: selectedSite === site.id }]"
            @click="selectedSite = site.id"
          >
            {{ site.name }}
            <transition name="pulse" mode="out-in">
              <span 
                v-if="siteStatus[site.id]" 
                class="site-status-indicator"
                :class="{'status-good': siteStatus[site.id] === 'Good', 'status-bad': siteStatus[site.id] === 'Bad'}"
              ></span>
            </transition>
          </button>
          <button v-if="canAddSites" class="site-tab add-site-button" @click="showAddSiteModal = true">
            <svg viewBox="0 0 24 24" width="16" height="16" class="add-icon">
              <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
            </svg>
            Add Site
          </button>
        </div>
      </div>
      
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
          <div class="card status-card animate-in">
            <div class="card-header">
              <h2 class="card-title">Current Status</h2>
              <div class="badge" :class="statusBadgeClass">{{ currentStatus }}</div>
            </div>
            <div class="card-body">
              <div class="status-info">
                <p class="last-checked">
                  <svg viewBox="0 0 24 24" width="18" height="18" class="icon">
                    <path fill="currentColor" d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z" />
                  </svg>
                  Last checked: {{ lastChecked }}
                </p>
                <div class="url-info">
                  <svg viewBox="0 0 24 24" width="18" height="18" class="icon">
                    <path fill="currentColor" d="M16.36,14C16.44,13.34 16.5,12.68 16.5,12C16.5,11.32 16.44,10.66 16.36,10H19.74C19.9,10.64 20,11.31 20,12C20,12.69 19.9,13.36 19.74,14M14.59,19.56C15.19,18.45 15.65,17.25 15.97,16H18.92C17.96,17.65 16.43,18.93 14.59,19.56M14.34,14H9.66C9.56,13.34 9.5,12.68 9.5,12C9.5,11.32 9.56,10.65 9.66,10H14.34C14.43,10.65 14.5,11.32 14.5,12C14.5,12.68 14.43,13.34 14.34,14M12,19.96C11.17,18.76 10.5,17.43 10.09,16H13.91C13.5,17.43 12.83,18.76 12,19.96M8,8H5.08C6.03,6.34 7.57,5.06 9.4,4.44C8.8,5.55 8.35,6.75 8,8M5.08,16H8C8.35,17.25 8.8,18.45 9.4,19.56C7.57,18.93 6.03,17.65 5.08,16M4.26,14C4.1,13.36 4,12.69 4,12C4,11.31 4.1,10.64 4.26,10H7.64C7.56,10.66 7.5,11.32 7.5,12C7.5,12.68 7.56,13.34 7.64,14M12,4.03C12.83,5.23 13.5,6.57 13.91,8H10.09C10.5,6.57 11.17,5.23 12,4.03M18.92,8H15.97C15.65,6.75 15.19,5.55 14.59,4.44C16.43,5.07 17.96,6.34 18.92,8M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
                  </svg>
                  <span class="url-value">{{ selectedSiteUrl }}</span>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Statistics Card (for authorized users) -->
          <div v-if="canViewDetailedMetrics" class="card stats-card animate-in" style="--delay: 0.1s">
            <div class="card-header">
              <h2 class="card-title">24h Statistics</h2>
              <button class="btn btn-outline btn-sm refresh-btn" @click="refreshStats">
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path fill="currentColor" d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" />
                </svg>
                Refresh
              </button>
            </div>
            <div class="card-body">
              <div class="stats-grid">
                <div class="stat-item animate-in" style="--delay: 0.15s">
                  <div class="stat-value">{{ stats.total_requests_24h }}</div>
                  <div class="stat-label">Total Requests</div>
                </div>
                <div class="stat-item animate-in" style="--delay: 0.2s">
                  <div class="stat-value" :class="successRateClass">{{ stats.success_rate_24h.toFixed(2) }}%</div>
                  <div class="stat-label">Success Rate</div>
                </div>
                <div class="stat-item animate-in" style="--delay: 0.25s">
                  <div class="stat-value" :class="responseTimeClass">{{ (stats.avg_response_time_24h * 1000).toFixed(2) }} ms</div>
                  <div class="stat-label">Avg Response Time</div>
                </div>
                <div class="stat-item animate-in" style="--delay: 0.3s">
                  <div class="stat-value">{{ stats.failed_requests_24h }}</div>
                  <div class="stat-label">Failed Requests</div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Uptime Card -->
          <div v-if="canViewDetailedMetrics" class="card uptime-card animate-in" style="--delay: 0.15s">
            <div class="card-header">
              <h2 class="card-title">Uptime</h2>
              <div class="uptime-indicator" :class="getUptimeClass(24)"></div>
            </div>
            <div class="card-body">
              <div class="uptime-stats">
                <div class="uptime-item">
                  <div class="uptime-label">Last 24h</div>
                  <div class="uptime-value" :class="getUptimeClass(24)">{{ calculateUptime(24) }}%</div>
                  <div class="uptime-bar">
                    <div class="uptime-progress" :style="{ width: calculateUptime(24) + '%' }" :class="getUptimeClass(24)"></div>
                  </div>
                </div>
                <div class="uptime-item">
                  <div class="uptime-label">Last 7 days</div>
                  <div class="uptime-value" :class="getUptimeClass(168)">{{ calculateUptime(168) }}%</div>
                  <div class="uptime-bar">
                    <div class="uptime-progress" :style="{ width: calculateUptime(168) + '%' }" :class="getUptimeClass(168)"></div>
                  </div>
                </div>
                <div class="uptime-item">
                  <div class="uptime-label">Last 30 days</div>
                  <div class="uptime-value" :class="getUptimeClass(720)">{{ calculateUptime(720) }}%</div>
                  <div class="uptime-bar">
                    <div class="uptime-progress" :style="{ width: calculateUptime(720) + '%' }" :class="getUptimeClass(720)"></div>
                  </div>
                </div>
                <div class="uptime-item">
                  <div class="uptime-label">Current Month</div>
                  <div class="uptime-value" :class="getUptimeClass(0)">{{ calculateMonthlyUptime() }}%</div>
                  <div class="uptime-bar">
                    <div class="uptime-progress" :style="{ width: calculateMonthlyUptime() + '%' }" :class="getUptimeClass(0)"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Alerts Card -->
          <div v-if="canViewDetailedMetrics" class="card alerts-card animate-in" style="--delay: 0.2s">
            <div class="card-header">
              <h2 class="card-title">Recent Alerts</h2>
              <span class="alerts-count" v-if="recentAlerts.length">{{ recentAlerts.length }}</span>
            </div>
            <div class="card-body">
              <div v-if="recentAlerts.length" class="alerts-list">
                <div v-for="(alert, index) in recentAlerts" 
                     :key="index" 
                     class="alert-item animate-in" 
                     :class="alert.severity"
                     :style="{ '--delay': 0.25 + index * 0.05 + 's' }">
                  <div class="alert-content">
                    <span class="alert-message">{{ alert.message }}</span>
                    <span class="alert-time">{{ formatAlertTime(alert.timestamp) }}</span>
                  </div>
                </div>
              </div>
              <div v-else class="no-data">
                <svg viewBox="0 0 24 24" width="24" height="24">
                  <path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20M12,7A5,5 0 0,0 7,12A5,5 0 0,0 12,17A5,5 0 0,0 17,12A5,5 0 0,0 12,7M12,15A3,3 0 0,1 9,12A3,3 0 0,1 12,9A3,3 0 0,1 15,12A3,3 0 0,1 12,15Z" />
                </svg>
                <p>No recent alerts</p>
              </div>
            </div>
          </div>
          
          <!-- Response Time Chart Card -->
          <div class="card chart-card full-width animate-in" :class="{ 'limited-data': !canViewDetailedMetrics }" style="--delay: 0.25s">
            <div class="card-header">
              <h2 class="card-title">Response Times</h2>
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
            <div class="card-body">
              <div v-if="!canViewDetailedMetrics" class="limited-access-message">
                <svg viewBox="0 0 24 24" width="24" height="24">
                  <path fill="currentColor" d="M18,8H17V6A5,5 0 0,0 12,1A5,5 0 0,0 7,6V8H6A2,2 0 0,0 4,10V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V10A2,2 0 0,0 18,8M8.9,6C8.9,4.29 10.29,2.9 12,2.9C13.71,2.9 15.1,4.29 15.1,6V8H8.9V6M16,16H13V19H11V16H8V14H11V11H13V14H16V16Z" />
                </svg>
                <div class="limited-access-content">
                  <p class="limited-heading">Limited Access</p>
                  <p>Login with higher privileges to view detailed metrics and historical data.</p>
                </div>
              </div>
              
              <div v-else class="chart-container">
                <LineChart 
                  v-if="chartData.labels.length" 
                  :chart-data="chartData"
                  :options="chartOptions"
                />
                <div v-else class="no-data">
                  <svg viewBox="0 0 24 24" width="24" height="24">
                    <path fill="currentColor" d="M21,21V17.5C21,16.67 20.33,16 19.5,16C18.67,16 18,16.67 18,17.5V21H16V9H14V21H9V2H7V21H3V19H1V21A2,2 0 0,0 3,23H19A2,2 0 0,0 21,21M5,16H7V19H5V16Z" />
                  </svg>
                  <p>No data available</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </div>
    
    <!-- Add Site Modal -->
    <transition name="modal">
      <div v-if="showAddSiteModal && canAddSites" class="modal-backdrop" @click.self="showAddSiteModal = false">
        <div class="modal card">
          <div class="modal-header">
            <h3>Add Monitoring Site</h3>
            <button class="modal-close" @click="showAddSiteModal = false">
              <svg viewBox="0 0 24 24" width="24" height="24">
                <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label class="form-label" for="site-name">Site Name</label>
              <div class="input-wrapper">
                <svg viewBox="0 0 24 24" width="18" height="18" class="input-icon">
                  <path fill="currentColor" d="M17,13H13V17H11V13H7V11H11V7H13V11H17M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
                </svg>
                <input type="text" id="site-name" v-model="newSite.name" placeholder="Production API" class="form-control">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" for="site-url">URL to Monitor</label>
              <div class="input-wrapper">
                <svg viewBox="0 0 24 24" width="18" height="18" class="input-icon">
                  <path fill="currentColor" d="M16.36,14C16.44,13.34 16.5,12.68 16.5,12C16.5,11.32 16.44,10.66 16.36,10H19.74C19.9,10.64 20,11.31 20,12C20,12.69 19.9,13.36 19.74,14M14.59,19.56C15.19,18.45 15.65,17.25 15.97,16H18.92C17.96,17.65 16.43,18.93 14.59,19.56M14.34,14H9.66C9.56,13.34 9.5,12.68 9.5,12C9.5,11.32 9.56,10.65 9.66,10H14.34C14.43,10.65 14.5,11.32 14.5,12C14.5,12.68 14.43,13.34 14.34,14M12,19.96C11.17,18.76 10.5,17.43 10.09,16H13.91C13.5,17.43 12.83,18.76 12,19.96M8,8H5.08C6.03,6.34 7.57,5.06 9.4,4.44C8.8,5.55 8.35,6.75 8,8M5.08,16H8C8.35,17.25 8.8,18.45 9.4,19.56C7.57,18.93 6.03,17.65 5.08,16M4.26,14C4.1,13.36 4,12.69 4,12C4,11.31 4.1,10.64 4.26,10H7.64C7.56,10.66 7.5,11.32 7.5,12C7.5,12.68 7.56,13.34 7.64,14M12,4.03C12.83,5.23 13.5,6.57 13.91,8H10.09C10.5,6.57 11.17,5.23 12,4.03M18.92,8H15.97C15.65,6.75 15.19,5.55 14.59,4.44C16.43,5.07 17.96,6.34 18.92,8M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
                </svg>
                <input type="text" id="site-url" v-model="newSite.url" placeholder="https://api.example.com/health" class="form-control">
              </div>
            </div>
            <div class="form-group">
              <label class="form-label" for="site-id">Site ID (for API)</label>
              <div class="input-wrapper">
                <svg viewBox="0 0 24 24" width="18" height="18" class="input-icon">
                  <path fill="currentColor" d="M6,17C6,15 10,13.9 12,13.9C14,13.9 18,15 18,17V18H6M15,9A3,3 0 0,1 12,12A3,3 0 0,1 9,9A3,3 0 0,1 12,6A3,3 0 0,1 15,9M3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3H5C3.89,3 3,3.9 3,5Z" />
                </svg>
                <input type="text" id="site-id" v-model="newSite.id" placeholder="prod-api" class="form-control">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-outline" @click="showAddSiteModal = false">Cancel</button>
            <button class="btn btn-primary" @click="addNewSite" :disabled="!isNewSiteValid">Add Site</button>
          </div>
        </div>
      </div>
    </transition>
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
    
    // Get current user from store
    const currentUser = computed(() => userStore.currentUser())
    
    // Computed property for status badge class
    const statusBadgeClass = computed(() => {
      if (currentStatus.value === 'Good') return 'badge-success'
      if (currentStatus.value === 'Bad') return 'badge-danger'
      return 'badge-warning'
    })
    
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
        
        // Add a small animation to show the refresh worked
        const statItems = document.querySelectorAll('.stat-item')
        statItems.forEach((item, index) => {
          item.classList.remove('animate-in')
          // Force reflow
          void item.offsetWidth
          item.style.setProperty('--delay', 0.1 + index * 0.05 + 's')
          item.classList.add('animate-in')
        })
      } catch (err) {
        console.error('Error refreshing stats:', err)
      }
    }
    
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
      currentUser,
      statusBadgeClass,
      refreshStats
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

.badge-success {
  background-color: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.badge-danger {
  background-color: rgba(255, 0, 110, 0.1);
  color: var(--danger);
}

.badge-warning {
  background-color: rgba(251, 191, 36, 0.1);
  color: var(--accent);
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

/* Site Tabs */
.site-tabs-container {
  margin-bottom: 1.5rem;
  overflow: hidden;
  border-radius: var(--radius-md);
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.site-tabs {
  display: flex;
  gap: 0.25rem;
  overflow-x: auto;
  padding: 0.75rem;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.site-tabs::-webkit-scrollbar {
  display: none;
}

.site-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
}

.site-tab:hover {
  border-color: var(--primary-light);
  color: var(--primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.site-tab.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
  box-shadow: 0 2px 6px rgba(58, 134, 255, 0.3);
}

.site-status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-left: 0.25rem;
}

.status-good {
  background-color: var(--success);
  box-shadow: 0 0 5px var(--success);
}

.status-bad {
  background-color: var(--danger);
  box-shadow: 0 0 5px var(--danger);
}

.add-site-button {
  background-color: var(--bg-secondary);
  border: 1px dashed var(--border-color);
}

.add-icon {
  fill: currentColor;
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

/* Card Styles */
.card {
  border-radius: var(--radius-md);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  transition: var(--transition);
  overflow: hidden;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-body {
  padding: 1.25rem;
}

/* Status Card */
.status-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.last-checked, .url-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.icon {
  flex-shrink: 0;
  color: var(--text-secondary);
}

.url-value {
  font-family: monospace;
  word-break: break-all;
}

/* Stats Card */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  border-radius: var(--radius);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.stat-item:hover {
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

/* Uptime Card */
.uptime-card .card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.uptime-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.uptime-stats {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.uptime-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.uptime-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.uptime-value {
  font-size: 1.25rem;
  font-weight: 600;
}

.uptime-bar {
  width: 100%;
  height: 6px;
  background-color: var(--gray-light);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.uptime-progress {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.5s ease;
}

/* Alerts Card */
.alerts-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background-color: var(--primary);
  color: white;
  font-size: 0.75rem;
  font-weight: 600;
}

.alerts-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.alert-item {
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  transition: var(--transition);
  border-left: 3px solid;
}

.alert-item:hover {
  transform: translateX(4px);
}

.alert-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.alert-message {
  font-weight: 500;
  color: var(--text-primary);
}

.alert-time {
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.alert-item.info {
  background-color: rgba(58, 134, 255, 0.05);
  border-left-color: var(--primary);
}

.alert-item.warning {
  background-color: rgba(251, 191, 36, 0.05);
  border-left-color: var(--accent);
}

.alert-item.critical {
  background-color: rgba(255, 0, 110, 0.05);
  border-left-color: var(--danger);
}

/* Chart Card */
.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-controls {
  display: flex;
  gap: 0.5rem;
  background-color: var(--bg-primary);
  border-radius: var(--radius);
  padding: 0.25rem;
  border: 1px solid var(--border-color);
}

.chart-period-button {
  padding: 0.375rem 0.75rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.chart-period-button:hover {
  color: var(--primary);
  background-color: rgba(58, 134, 255, 0.05);
}

.chart-period-button.active {
  color: var(--primary);
  background-color: rgba(58, 134, 255, 0.1);
}

.chart-container {
  height: 350px;
  position: relative;
}

.limited-access-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  color: var(--text-secondary);
  height: 100%;
}

.limited-access-message svg {
  color: var(--text-secondary);
  opacity: 0.5;
}

.limited-access-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.limited-heading {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 1rem;
}

.no-data {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  color: var(--text-secondary);
  height: 100%;
  opacity: 0.7;
}

/* Modal Styles */
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
  z-index: 100;
  backdrop-filter: blur(2px);
}

.modal {
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 0.25rem;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.modal-close:hover {
  color: var(--danger);
  background-color: rgba(255, 0, 110, 0.05);
}

.modal-body {
  padding: 1.25rem;
  overflow-y: auto;
}

.modal-footer {
  padding: 1.25rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

/* Status Indicator Colors */
.good, .excellent {
  color: var(--success);
}

.warning, .average {
  color: var(--accent);
}

.critical, .poor {
  color: var(--danger);
}

/* Animations */
.animate-in {
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
  transform: translateY(10px);
  animation-delay: var(--delay, 0s);
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Transitions */
.fade-up-enter-active,
.fade-up-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.pulse-enter-active,
.pulse-leave-active {
  transition: all 0.3s ease;
}

.pulse-enter-from,
.pulse-leave-to {
  transform: scale(0);
  opacity: 0;
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
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
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .chart-controls {
    flex-wrap: wrap;
  }
  
  .site-tabs {
    flex-wrap: nowrap;
  }
}

@media (max-width: 480px) {
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .modal {
    width: 95%;
  }
}
</style> 