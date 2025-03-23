<template>
  <div class="metrics">
    <h1 class="page-title">Metrics & Monitoring</h1>
    
    <!-- Debug controls (only visible in development mode) -->
    <div v-if="isDevelopment" class="debug-controls">
      <h3>Debug Tools</h3>
      <div class="debug-buttons">
        <button @click="debugSetRole('admin')" :class="{ active: userStore.isAdmin() }">Admin</button>
        <button @click="debugSetRole('maintainer')" :class="{ active: userStore.isMaintainer() }">Maintainer</button>
        <button @click="debugSetRole('user')" :class="{ active: userStore.isUser() }">User</button>
        <button @click="debugSetRole('guest')" :class="{ active: userStore.isGuest() }">Guest</button>
      </div>
      <div class="debug-info">
        <p>Current Role: <strong>{{ currentUserRole }}</strong></p>
        <p>Has VIEW_DETAILED_METRICS: <strong>{{ canViewDetailedMetrics ? 'Yes' : 'No' }}</strong></p>
        <p>Has ACCESS_HISTORICAL: <strong>{{ canAccessHistoricalData ? 'Yes' : 'No' }}</strong></p>
        <p>Accessible Sites: <strong>{{ userStore.getAccessibleSites().join(', ') }}</strong></p>
        <p>Site Permissions for 'main': <strong>{{ JSON.stringify(userStore.state?.currentUser?.sitePermissions?.main || []) }}</strong></p>
        <p>Has SITE_VIEW_METRICS for 'main': <strong>{{ userStore.hasSitePermission('main', SITE_PERMISSIONS.SITE_VIEW_METRICS) ? 'Yes' : 'No' }}</strong></p>
        <p>Filtered Sites Count: <strong>{{ accessibleSites.length }}</strong></p>
      </div>
    </div>
    
    <!-- Restricted access message if user doesn't have required permissions -->
    <div v-if="!canViewDetailedMetrics" class="restricted-access">
      <font-awesome-icon :icon="['fas', 'lock']" class="restricted-icon" />
      <h2>Restricted Access</h2>
      <p>You don't have permission to view detailed metrics.</p>
      <p>Please contact an administrator to request access.</p>
    </div>
    
    <!-- Message for users with no accessible sites -->
    <div v-else-if="sites.length === 0" class="restricted-access">
      <font-awesome-icon :icon="['fas', 'server']" class="restricted-icon" />
      <h2>No Sites Available</h2>
      <p>You don't have permission to access any sites with detailed metrics.</p>
      <p>Please contact an administrator to request site access.</p>
    </div>
    
    <!-- Main content only visible to users with correct permissions and accessible sites -->
    <div v-else>
      <div class="selectors-container">
        <div class="selector">
          <label for="site-selector">Site:</label>
          <select id="site-selector" v-model="selectedSite" @change="onSiteChange">
            <option v-for="site in sites" :key="site.id" :value="site.id">
              {{ site.name }}
            </option>
          </select>
        </div>
        
        <div class="selector">
          <label for="instance-selector">Instance:</label>
          <select id="instance-selector" v-model="selectedInstance" @change="onInstanceChange" :disabled="!selectedSite">
            <option v-for="instance in instancesForSite" :key="instance.id" :value="instance.id">
              {{ instance.name }}
            </option>
          </select>
        </div>
        
        <div class="selector">
          <label for="endpoint-selector">Endpoint:</label>
          <select id="endpoint-selector" v-model="selectedEndpoint" @change="loadEndpointData" :disabled="!selectedSite">
            <option v-for="endpoint in endpointsForSite" :key="endpoint.id" :value="endpoint.id">
              {{ endpoint.path }}
            </option>
          </select>
        </div>
      </div>
      
      <div class="metrics-badges">
        <div class="badge online">
          <div class="badge-icon">
            <font-awesome-icon :icon="['fas', 'check-circle']" />
          </div>
          <div class="badge-content">
            <div class="badge-title">Online Endpoints</div>
            <div class="badge-value">{{ stats.onlineEndpoints }}</div>
          </div>
        </div>
        
        <div class="badge warning">
          <div class="badge-icon">
            <font-awesome-icon :icon="['fas', 'exclamation-triangle']" />
          </div>
          <div class="badge-content">
            <div class="badge-title">Warning Endpoints</div>
            <div class="badge-value">{{ stats.warningEndpoints }}</div>
          </div>
        </div>
        
        <div class="badge response">
          <div class="badge-icon">
            <font-awesome-icon :icon="['fas', 'tachometer-alt']" />
          </div>
          <div class="badge-content">
            <div class="badge-title">Avg Response Time</div>
            <div class="badge-value">{{ stats.avgResponseTime }} ms</div>
          </div>
        </div>
      </div>
      
      <div class="metrics-chart-container card">
        <h2>
          <font-awesome-icon :icon="['fas', 'chart-line']" class="card-icon" />
          Response Time History
          <span class="chart-subtitle" v-if="selectedEndpoint">
            for {{ currentEndpointDetails.path }} ({{ currentEndpointDetails.instance }})
          </span>
        </h2>
        
        <div v-if="!canAccessHistoricalData" class="restricted-feature">
          <font-awesome-icon :icon="['fas', 'lock']" />
          <p>You don't have permission to view historical data.</p>
        </div>
        
        <div v-else class="chart-container">
          <LineChart 
            v-if="chartData.labels.length" 
            :chartData="chartData"
            :options="chartOptions"
          />
          <p v-else class="no-data">
            <font-awesome-icon :icon="['fas', 'info-circle']" />
            Select an endpoint to view response time data
          </p>
        </div>
      </div>
      
      <div class="endpoint-details card" v-if="selectedEndpoint">
        <h2>
          <font-awesome-icon :icon="['fas', 'server']" class="card-icon" />
          Endpoint Details
        </h2>
        
        <div class="detail-item">
          <strong>URL:</strong> {{ currentEndpointDetails.fullUrl }}
        </div>
        
        <div class="detail-item">
          <strong>Method:</strong> <span class="method-badge">{{ currentEndpointDetails.method }}</span>
        </div>
        
        <div class="detail-item">
          <strong>Instance:</strong> {{ currentEndpointDetails.instance }}
        </div>
        
        <div class="detail-item">
          <strong>Status:</strong> 
          <span class="status-badge" :class="currentEndpointDetails.status === 'Online' ? 'online' : 'warning'">
            {{ currentEndpointDetails.status }}
          </span>
        </div>
        
        <div class="detail-item">
          <strong>Latest Response:</strong> {{ currentEndpointDetails.latestResponse }}
        </div>
        
        <div class="detail-item">
          <strong>Uptime:</strong> {{ currentEndpointDetails.uptime }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { LineChart } from 'vue-chart-3'
import userStore, { PERMISSIONS, DATA_PERMISSIONS, SITE_PERMISSIONS, ROLES } from '@/store/userStore'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

// Import FontAwesome core
import { library } from '@fortawesome/fontawesome-svg-core'
// Import FontAwesome component
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// Import specific icons
import { 
  faChartLine, 
  faInfoCircle, 
  faServer, 
  faCheckCircle,
  faExclamationTriangle,
  faTachometerAlt,
  faLock
} from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(
  faChartLine, 
  faInfoCircle, 
  faServer, 
  faCheckCircle,
  faExclamationTriangle,
  faTachometerAlt,
  faLock
)

// Mock data for sites, instances, endpoints
const mockSites = [
  { id: 'main', name: 'Production' },
  { id: 'backup', name: 'Staging' },
  { id: 'staging', name: 'Development' }
]

const mockInstances = [
  { id: 1, name: 'Instance 1', siteId: 'main' },
  { id: 2, name: 'Instance 2', siteId: 'main' },
  { id: 3, name: 'Instance 1', siteId: 'backup' },
  { id: 4, name: 'Instance 1', siteId: 'staging' },
  { id: 5, name: 'Instance 2', siteId: 'staging' }
]

const mockEndpoints = [
  { id: 1, siteId: 'main', path: '/api/users', method: 'GET', status: 'Online', fullUrl: 'https://yudoufu.org/tofu/api/users' },
  { id: 2, siteId: 'main', path: '/api/auth/login', method: 'POST', status: 'Online', fullUrl: 'https://yudoufu.org/tofu/api/auth/login' },
  { id: 3, siteId: 'main', path: '/api/rooms', method: 'GET', status: 'Warning', fullUrl: 'https://yudoufu.org/tofu/api/rooms' },
  { id: 4, siteId: 'backup', path: '/api/users', method: 'GET', status: 'Online', fullUrl: 'https://staging.yudoufu.org/tofu/api/users' },
  { id: 5, siteId: 'backup', path: '/api/auth/login', method: 'POST', status: 'Online', fullUrl: 'https://staging.yudoufu.org/tofu/api/auth/login' },
  { id: 6, siteId: 'backup', path: '/api/status', method: 'GET', status: 'Online', fullUrl: 'https://staging.yudoufu.org/tofu/status' },
  { id: 7, siteId: 'staging', path: '/api/users', method: 'GET', status: 'Online', fullUrl: 'https://dev.yudoufu.org/tofu/api/users' },
  { id: 8, siteId: 'staging', path: '/api/auth/login', method: 'POST', status: 'Warning', fullUrl: 'https://dev.yudoufu.org/tofu/api/auth/login' },
  { id: 9, siteId: 'staging', path: '/api/health', method: 'GET', status: 'Online', fullUrl: 'https://dev.yudoufu.org/tofu/health' }
]

// Generate mock time series data for response times
const generateTimeSeriesData = (endpointId) => {
  const now = new Date()
  const data = []
  
  // Generate data for the last 30 days
  for (let i = 0; i < 30; i++) {
    const date = new Date(now)
    date.setDate(date.getDate() - (29 - i))
    
    // Different pattern based on endpoint ID for variety
    let baseValue = 100
    if (endpointId % 3 === 0) {
      baseValue = 150
    } else if (endpointId % 2 === 0) {
      baseValue = 80
    }
    
    // Add some randomness
    const value = baseValue + Math.random() * 50 - 25
    
    data.push({
      date: date.toISOString().split('T')[0],
      value: Math.round(value)
    })
  }
  
  return data
}

export default {
  name: 'MetricsView',
  components: {
    LineChart,
    FontAwesomeIcon
  },
  setup() {
    const sites = ref([])
    const instances = ref(mockInstances)
    const endpoints = ref(mockEndpoints)
    
    const selectedSite = ref(null)
    const selectedInstance = ref(null)
    const selectedEndpoint = ref(null)
    
    const responseTimeData = ref([])
    
    // Check permissions for various features
    const canViewDetailedMetrics = computed(() => {
      return userStore.hasPermission(PERMISSIONS.VIEW_DETAILED_METRICS)
    })
    
    const canAccessHistoricalData = computed(() => {
      return userStore.hasDataPermission(DATA_PERMISSIONS.ACCESS_HISTORICAL)
    })
    
    // Filter sites based on user permissions
    const accessibleSites = computed(() => {
      // Get the list of site IDs the user can access
      const accessibleSiteIds = userStore.getAccessibleSites()
      
      // For debugging purposes
      console.log('Accessible Site IDs:', accessibleSiteIds);
      
      // Filter the mockSites array to only include sites the user can access
      // AND the user has the SITE_VIEW_METRICS permission for that site
      const filteredSites = mockSites.filter(site => {
        const canAccess = accessibleSiteIds.includes(site.id);
        const hasMetricsPermission = userStore.hasSitePermission(site.id, SITE_PERMISSIONS.SITE_VIEW_METRICS);
        
        // For debugging
        console.log(`Site ${site.id}: canAccess=${canAccess}, hasMetricsPermission=${hasMetricsPermission}`);
        
        return canAccess && hasMetricsPermission;
      });
      
      // If we have filtered sites, return them
      if (filteredSites.length > 0) {
        return filteredSites;
      }
      
      // If the user has global VIEW_DETAILED_METRICS permission but no site-specific permissions,
      // show at least the main site for demo purposes
      if (canViewDetailedMetrics.value && accessibleSiteIds.includes('main')) {
        return mockSites.filter(site => site.id === 'main');
      }
      
      // Otherwise, return empty array (no sites accessible)
      return [];
    })
    
    // Computed properties for filtered data
    const instancesForSite = computed(() => {
      if (!selectedSite.value) return []
      return instances.value.filter(instance => instance.siteId === selectedSite.value)
    })
    
    const endpointsForSite = computed(() => {
      if (!selectedSite.value) return []
      return endpoints.value.filter(endpoint => endpoint.siteId === selectedSite.value)
    })
    
    const currentEndpointDetails = computed(() => {
      if (!selectedEndpoint.value) return {}
      
      const endpoint = endpoints.value.find(e => e.id === selectedEndpoint.value)
      if (!endpoint) return {}
      
      // Add instance-specific information
      return {
        ...endpoint,
        instance: instances.value.find(i => i.id === selectedInstance.value)?.name || 'Unknown',
        latestResponse: `${80 + Math.floor(Math.random() * 40)} ms`,
        uptime: `${99.7 + Math.random() * 0.3}%`
      }
    })
    
    // Compute stats for the selected site
    const stats = computed(() => {
      if (!selectedSite.value) return { onlineEndpoints: 0, warningEndpoints: 0, avgResponseTime: 0 }
      
      // Get all endpoints for the current site
      const siteEndpoints = endpoints.value.filter(endpoint => endpoint.siteId === selectedSite.value)
      
      const onlineEndpoints = siteEndpoints.filter(e => e.status === 'Online').length
      const warningEndpoints = siteEndpoints.filter(e => e.status === 'Warning').length
      
      // Simulate average response time
      const avgResponseTime = Math.round(90 + Math.random() * 30)
      
      return {
        onlineEndpoints,
        warningEndpoints,
        avgResponseTime
      }
    })
    
    // Computed property for chart data
    const chartData = computed(() => {
      if (!responseTimeData.value.length) {
        return { labels: [], datasets: [] }
      }
      
      return {
        labels: responseTimeData.value.map(point => point.date),
        datasets: [
          {
            label: 'Response Time (ms)',
            backgroundColor: 'rgba(42, 157, 143, 0.2)',
            borderColor: 'rgb(42, 157, 143)',
            data: responseTimeData.value.map(point => point.value),
            tension: 0.2
          }
        ]
      }
    })
    
    // Chart options
    const chartOptions = computed(() => {
      return {
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
              text: 'Date'
            }
          }
        }
      }
    })
    
    // Methods for handling selection changes
    const onSiteChange = () => {
      // Reset instance selection to the first instance of the site
      const firstInstanceForSite = instancesForSite.value[0]
      if (firstInstanceForSite) {
        selectedInstance.value = firstInstanceForSite.id
      } else {
        selectedInstance.value = null
      }

      // Reset endpoint selection to the first endpoint of the site
      const firstEndpointForSite = endpointsForSite.value[0]
      if (firstEndpointForSite) {
        selectedEndpoint.value = firstEndpointForSite.id
        loadEndpointData()
      } else {
        selectedEndpoint.value = null
        responseTimeData.value = []
      }
    }
    
    const onInstanceChange = () => {
      // When instance changes, we keep the same endpoint but reload data
      // This simulates getting instance-specific data for the same endpoint
      loadEndpointData()
    }
    
    const loadEndpointData = () => {
      if (selectedEndpoint.value) {
        // Only load historical data if user has permission
        if (canAccessHistoricalData.value) {
          // Generate mock time series data for the selected endpoint
          responseTimeData.value = generateTimeSeriesData(selectedEndpoint.value)
        } else {
          // Clear historical data if no permission
          responseTimeData.value = []
        }
      }
    }
    
    // Initialize with data for the default selections
    onMounted(() => {
      // Initialize sites based on user permissions
      sites.value = accessibleSites.value
      
      // Set default selected site if user has access to any sites
      if (sites.value.length > 0) {
        selectedSite.value = sites.value[0].id
        onSiteChange()
      } else {
        // If user doesn't have access to any sites, show empty state
        selectedSite.value = null
        selectedInstance.value = null
        selectedEndpoint.value = null
      }
    })
    
    // Debug helpers (only for development)
    const currentUserRole = computed(() => {
      if (userStore.isAdmin()) return 'Admin'
      if (userStore.isMaintainer()) return 'Maintainer'
      if (userStore.isUser()) return 'User'
      return 'Guest'
    })

    const isDevelopment = computed(() => {
      return process.env.NODE_ENV === 'development'
    })

    const debugSetRole = (role) => {
      // This is a simplified mock of userStore for debugging purposes
      // In a real app, this would be handled by the backend
      const mockUser = {
        id: 1,
        username: 'debug_user',
        email: 'debug@example.com',
        role: ROLES[role.toUpperCase()],
        sitePermissions: {},
        permissions: [],
        dataPermissions: []
      }
      
      // Set global permissions based on role
      if (role === 'admin') {
        // Admins have all permissions
        mockUser.permissions = Object.values(PERMISSIONS);
        mockUser.dataPermissions = Object.values(DATA_PERMISSIONS);
      } else if (role === 'maintainer') {
        // Maintainers have most permissions except some admin-only ones
        mockUser.permissions = [
          PERMISSIONS.VIEW_DETAILED_METRICS,
          PERMISSIONS.EDIT_SETTINGS,
          PERMISSIONS.CREATE_REPORTS
        ];
        mockUser.dataPermissions = [DATA_PERMISSIONS.ACCESS_HISTORICAL];
      } else if (role === 'user') {
        // Regular users have limited permissions
        mockUser.permissions = [PERMISSIONS.VIEW_DETAILED_METRICS];
        mockUser.dataPermissions = [DATA_PERMISSIONS.ACCESS_HISTORICAL];
      } else {
        // Guests have minimal permissions
        mockUser.permissions = [];
        mockUser.dataPermissions = [];
      }
      
      // Initialize sitePermissions structure for all sites to prevent undefined errors
      mockSites.forEach(site => {
        mockUser.sitePermissions[site.id] = [];
      });
      
      // Set site permissions based on role
      if (role === 'admin') {
        // Admin has all permissions for all sites
        mockSites.forEach(site => {
          mockUser.sitePermissions[site.id] = Object.values(SITE_PERMISSIONS);
        });
      } else if (role === 'maintainer') {
        // Maintainer has view and metrics permissions for all sites
        mockSites.forEach(site => {
          mockUser.sitePermissions[site.id] = [
            SITE_PERMISSIONS.SITE_VIEW,
            SITE_PERMISSIONS.SITE_VIEW_METRICS,
            SITE_PERMISSIONS.SITE_EDIT
          ];
        });
      } else if (role === 'user') {
        // Regular users only have access to main site with limited permissions
        mockUser.sitePermissions['main'] = [
          SITE_PERMISSIONS.SITE_VIEW,
          SITE_PERMISSIONS.SITE_VIEW_METRICS
        ];
      } else {
        // Guests only have view access to main site
        mockUser.sitePermissions['main'] = [
          SITE_PERMISSIONS.SITE_VIEW
        ];
      }
      
      // Update userStore with mock user for testing
      userStore.state.currentUser = mockUser;
      userStore.state.isAuthenticated = true;
      
      console.log(`Debug - Set role to ${role}:`, {
        permissions: mockUser.permissions,
        dataPermissions: mockUser.dataPermissions,
        sitePermissions: mockUser.sitePermissions
      });
      
      // Refresh the site list
      sites.value = accessibleSites.value;
      console.log('Accessible sites after role change:', sites.value);
      
      // Reset selections if necessary
      if (sites.value.length > 0) {
        selectedSite.value = sites.value[0].id;
        onSiteChange();
      } else {
        selectedSite.value = null;
        selectedInstance.value = null;
        selectedEndpoint.value = null;
        responseTimeData.value = [];
      }
    }
    
    return {
      sites,
      selectedSite,
      selectedInstance,
      selectedEndpoint,
      instancesForSite,
      endpointsForSite,
      stats,
      chartData,
      chartOptions,
      currentEndpointDetails,
      onSiteChange,
      onInstanceChange,
      loadEndpointData,
      canViewDetailedMetrics,
      canAccessHistoricalData,
      userStore,
      // Debug items
      currentUserRole,
      debugSetRole,
      isDevelopment,
      // Expose permissions for template
      SITE_PERMISSIONS,
      // Expose computed property for debug
      accessibleSites
    }
  }
}
</script>

<style scoped>
.metrics {
  max-width: 100%;
  padding: 1.5rem;
  background-color: var(--bg-body);
  min-height: 100%;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
  color: var(--text-primary);
}

.restricted-access {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 3rem;
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  margin: 2rem auto;
  max-width: 500px;
}

.restricted-access h2 {
  font-size: 1.5rem;
  margin: 1rem 0;
  color: var(--text-primary);
}

.restricted-access p {
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.restricted-icon {
  font-size: 3rem;
  color: var(--warning);
}

.restricted-feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: var(--bg-body);
  border-radius: var(--radius);
  color: var(--text-secondary);
  text-align: center;
  height: 100%;
}

.restricted-feature svg {
  font-size: 2rem;
  color: var(--warning);
  margin-bottom: 1rem;
}

.selectors-container {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.selector {
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

.selector label {
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 0.5rem;
  color: var(--text-secondary);
}

.selector select {
  padding: 0.5rem;
  border-radius: var(--radius);
  border: 1px solid var(--border-color);
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: var(--transition);
}

.selector select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 2px rgba(42, 157, 143, 0.2);
}

.selector select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.metrics-badges {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
}

.badge {
  display: flex;
  align-items: center;
  padding: 1rem;
  border-radius: var(--radius);
  background-color: var(--bg-secondary);
  box-shadow: var(--shadow);
  flex: 1;
  min-width: 200px;
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.badge:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.badge-icon {
  font-size: 1.75rem;
  margin-right: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
}

.badge.online .badge-icon {
  color: var(--success);
  background-color: rgba(82, 183, 136, 0.1);
}

.badge.warning .badge-icon {
  color: var(--warning);
  background-color: rgba(233, 196, 106, 0.1);
}

.badge.response .badge-icon {
  color: var(--primary);
  background-color: rgba(42, 157, 143, 0.1);
}

.badge-content {
  display: flex;
  flex-direction: column;
}

.badge-title {
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-bottom: 0.25rem;
}

.badge-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
}

.card {
  background: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
  transition: var(--transition);
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

.card-icon {
  color: var(--primary);
  margin-right: 0.5rem;
}

.chart-container {
  height: 400px;
  position: relative;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--bg-body);
  border-radius: var(--radius);
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-style: italic;
  height: 100%;
}

.endpoint-details {
  display: flex;
  flex-direction: column;
}

.detail-item {
  display: flex;
  margin-bottom: 1rem;
  font-size: 0.875rem;
}

.detail-item strong {
  min-width: 150px;
  font-weight: 600;
}

.method-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius);
  background-color: var(--primary);
  color: white;
  font-weight: 500;
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius);
  font-weight: 500;
}

.status-badge.online {
  background-color: var(--success);
  color: white;
}

.status-badge.warning {
  background-color: var(--warning);
  color: white;
}

.chart-subtitle {
  font-size: 0.875rem;
  font-weight: normal;
  color: var(--text-secondary);
  margin-left: 0.5rem;
}

@media (max-width: 768px) {
  .metrics {
    padding: 1rem;
  }
  
  .selectors-container {
    flex-direction: column;
    gap: 1rem;
  }
  
  .metrics-badges {
    flex-direction: column;
    gap: 1rem;
  }
  
  .chart-container {
    height: 300px;
  }
}

/* Debug UI styles */
.debug-controls {
  background-color: #f3f7f9;
  border: 1px solid #e0e6ea;
  border-radius: var(--radius);
  padding: 1rem;
  margin-bottom: 1.5rem;
}

.debug-controls h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  font-size: 1rem;
  color: #4a5568;
}

.debug-buttons {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.debug-buttons button {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #fff;
  cursor: pointer;
  font-size: 0.875rem;
  transition: all 0.2s;
}

.debug-buttons button:hover {
  background-color: #f8f9fa;
}

.debug-buttons button.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
}

.debug-info {
  background-color: #fff;
  padding: 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
}

.debug-info p {
  margin: 0.25rem 0;
}
</style> 