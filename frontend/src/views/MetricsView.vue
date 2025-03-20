<template>
  <div class="metrics">
    <h1 class="page-title">Metrics & Monitoring</h1>
    
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
        <select id="instance-selector" v-model="selectedInstance" @change="onInstanceChange">
          <option v-for="instance in instancesForSite" :key="instance.id" :value="instance.id">
            {{ instance.name }}
          </option>
        </select>
      </div>
      
      <div class="selector">
        <label for="endpoint-selector">Endpoint:</label>
        <select id="endpoint-selector" v-model="selectedEndpoint" @change="loadEndpointData">
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
      <div class="chart-container">
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
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { LineChart } from 'vue-chart-3'

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
  faTachometerAlt
} from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(
  faChartLine, 
  faInfoCircle, 
  faServer, 
  faCheckCircle,
  faExclamationTriangle,
  faTachometerAlt
)

// Mock data for sites, instances, endpoints
const mockSites = [
  { id: 1, name: 'Production' },
  { id: 2, name: 'Staging' },
  { id: 3, name: 'Development' }
]

const mockInstances = [
  { id: 1, name: 'Instance 1', siteId: 1 },
  { id: 2, name: 'Instance 2', siteId: 1 },
  { id: 3, name: 'Instance 1', siteId: 2 },
  { id: 4, name: 'Instance 1', siteId: 3 },
  { id: 5, name: 'Instance 2', siteId: 3 }
]

const mockEndpoints = [
  { id: 1, siteId: 1, path: '/api/users', method: 'GET', status: 'Online', fullUrl: 'https://yudoufu.org/tofu/api/users' },
  { id: 2, siteId: 1, path: '/api/auth/login', method: 'POST', status: 'Online', fullUrl: 'https://yudoufu.org/tofu/api/auth/login' },
  { id: 3, siteId: 1, path: '/api/rooms', method: 'GET', status: 'Warning', fullUrl: 'https://yudoufu.org/tofu/api/rooms' },
  { id: 4, siteId: 2, path: '/api/users', method: 'GET', status: 'Online', fullUrl: 'https://staging.yudoufu.org/tofu/api/users' },
  { id: 5, siteId: 2, path: '/api/auth/login', method: 'POST', status: 'Online', fullUrl: 'https://staging.yudoufu.org/tofu/api/auth/login' },
  { id: 6, siteId: 2, path: '/api/status', method: 'GET', status: 'Online', fullUrl: 'https://staging.yudoufu.org/tofu/status' },
  { id: 7, siteId: 3, path: '/api/users', method: 'GET', status: 'Online', fullUrl: 'https://dev.yudoufu.org/tofu/api/users' },
  { id: 8, siteId: 3, path: '/api/auth/login', method: 'POST', status: 'Warning', fullUrl: 'https://dev.yudoufu.org/tofu/api/auth/login' },
  { id: 9, siteId: 3, path: '/api/health', method: 'GET', status: 'Online', fullUrl: 'https://dev.yudoufu.org/tofu/health' }
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
    const sites = ref(mockSites)
    const instances = ref(mockInstances)
    const endpoints = ref(mockEndpoints)
    
    const selectedSite = ref(1)
    const selectedInstance = ref(1)
    const selectedEndpoint = ref(null)
    
    const responseTimeData = ref([])
    
    // Computed properties for filtered data
    const instancesForSite = computed(() => {
      return instances.value.filter(instance => instance.siteId === selectedSite.value)
    })
    
    const endpointsForSite = computed(() => {
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
        // Generate mock time series data for the selected endpoint
        responseTimeData.value = generateTimeSeriesData(selectedEndpoint.value)
      }
    }
    
    // Initialize with data for the default selections
    onMounted(() => {
      onSiteChange()
    })
    
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
      loadEndpointData
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
</style> 