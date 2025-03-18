<template>
  <div class="metrics">
    <div class="metrics-header">
      <div class="title-section">
        <h1>Detailed Metrics</h1>
        <p class="subtitle">Performance analysis and monitoring statistics</p>
      </div>
      <div class="metrics-actions">
        <div class="refresh-info">
          <font-awesome-icon :icon="['fas', 'sync-alt']" class="refresh-icon" />
          <span class="refresh-text">Auto-refreshing every 60s</span>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="loading-indicator">
      <font-awesome-icon :icon="['fas', 'circle-notch']" spin class="spinner" />
      <p class="loading-text">Loading metrics data...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="error-icon" />
      {{ error }}
    </div>
    
    <div v-else>
      <div class="card">
        <h2>
          <font-awesome-icon :icon="['fas', 'chart-line']" class="card-icon" />
          Weekly Averages
        </h2>
        <div class="chart-container">
          <LineChart 
            v-if="weeklyChartData.labels.length" 
            :chartData="weeklyChartData"
            :options="chartOptions"
          />
          <p v-else class="no-data">
            <font-awesome-icon :icon="['fas', 'info-circle']" />
            No weekly average data available
          </p>
        </div>
      </div>
      
      <div class="card">
        <h2>
          <font-awesome-icon :icon="['fas', 'history']" class="card-icon" />
          Recent Requests
        </h2>
        <div class="table-wrapper">
          <table class="metrics-table">
            <thead>
              <tr>
                <th>
                  <font-awesome-icon :icon="['fas', 'clock']" />
                  Time
                </th>
                <th>
                  <font-awesome-icon :icon="['fas', 'server']" />
                  Status
                </th>
                <th>
                  <font-awesome-icon :icon="['fas', 'tachometer-alt']" />
                  Response Time
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="metric in recentMetrics" :key="metric.id" :class="{ 'error-row': !isSuccessful(metric) }">
                <td class="timestamp">{{ formatDate(metric.timestamp) }}</td>
                <td>
                  <span class="status-cell" :class="isSuccessful(metric) ? 'success' : 'error'">
                    <font-awesome-icon :icon="getStatusIcon(metric)" class="status-icon" />
                    {{ metric.status_code }}
                  </span>
                </td>
                <td class="response-time">{{ formatResponseTime(metric.request_time) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
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
  faSyncAlt, 
  faCircleNotch, 
  faExclamationTriangle, 
  faChartLine, 
  faHistory, 
  faInfoCircle,
  faClock,
  faServer,
  faTachometerAlt,
  faCheckCircle,
  faTimesCircle
} from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(
  faSyncAlt, 
  faCircleNotch, 
  faExclamationTriangle, 
  faChartLine, 
  faHistory, 
  faInfoCircle,
  faClock,
  faServer,
  faTachometerAlt,
  faCheckCircle,
  faTimesCircle
)

export default {
  name: 'MetricsView',
  components: {
    LineChart,
    FontAwesomeIcon
  },
  setup() {
    const apiUrl = process.env.VUE_APP_API_URL || 'http://localhost:8000'
    const loading = ref(true)
    const error = ref(null)
    const recentMetrics = ref([])
    const weeklyAverages = ref([])
    
    const fetchData = async () => {
      loading.value = true
      error.value = null
      
      try {
        // Fetch recent metrics
        const metricsResponse = await axios.get(`${apiUrl}/metrics/recent`, {
          params: { limit: 100 }
        })
        recentMetrics.value = metricsResponse.data
        
        // Fetch weekly averages
        const averagesResponse = await axios.get(`${apiUrl}/metrics/averages`, {
          params: { weeks: 12 }
        })
        weeklyAverages.value = averagesResponse.data.sort((a, b) => 
          new Date(a.week_start) - new Date(b.week_start)
        )
        
        loading.value = false
      } catch (err) {
        error.value = `Error loading data: ${err.message}`
        loading.value = false
        console.error(err)
      }
    }
    
    const formatDate = (timestamp) => {
      return new Date(timestamp).toLocaleString()
    }
    
    const formatResponseTime = (time) => {
      if (time < 0) return 'Error'
      return `${(time * 1000).toFixed(2)} ms`
    }
    
    const isSuccessful = (metric) => {
      return metric.status_code >= 200 && metric.status_code < 300
    }
    
    const getStatusIcon = (metric) => {
      return isSuccessful(metric) ? ['fas', 'check-circle'] : ['fas', 'times-circle']
    }
    
    const weeklyChartData = computed(() => {
      return {
        labels: weeklyAverages.value.map(avg => {
          const date = new Date(avg.week_start)
          return `${date.getMonth() + 1}/${date.getDate()}`
        }),
        datasets: [
          {
            label: 'Weekly Average Response Time (ms)',
            backgroundColor: 'rgba(42, 157, 143, 0.2)',
            borderColor: 'rgb(42, 157, 143)',
            data: weeklyAverages.value.map(avg => avg.average_time * 1000), // Convert to ms
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
            text: 'Average Response Time (ms)'
          }
        },
        x: {
          title: {
            display: true,
            text: 'Week Starting'
          }
        }
      }
    }
    
    onMounted(() => {
      fetchData()
      // Refresh data every 60 seconds
      setInterval(fetchData, 60000)
    })
    
    return {
      loading,
      error,
      recentMetrics,
      weeklyAverages,
      formatDate,
      formatResponseTime,
      isSuccessful,
      getStatusIcon,
      weeklyChartData,
      chartOptions
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

.metrics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.title-section h1 {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(120deg, var(--primary) 0%, var(--primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0;
}

.metrics-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.refresh-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  border: 1px solid var(--border-color);
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.refresh-icon {
  font-size: 1rem;
  animation: rotate 2s linear infinite;
  display: inline-block;
  color: var(--primary);
}

.refresh-text {
  font-weight: 500;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .metrics-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .metrics-actions {
    width: 100%;
  }

  .refresh-info {
    width: 100%;
    justify-content: center;
  }
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

.metrics-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.875rem;
}

.metrics-table th {
  text-align: left;
  padding: 1rem;
  background-color: var(--bg-body);
  border-bottom: 2px solid var(--border-color);
  font-weight: 600;
  color: var(--text-primary);
  position: sticky;
  top: 0;
  z-index: 10;
}

.metrics-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
  transition: var(--transition);
}

.metrics-table tr {
  transition: var(--transition);
}

.metrics-table tr:hover {
  background-color: var(--bg-body);
}

.metrics-table tr.error-row {
  background-color: rgba(231, 111, 81, 0.05);
}

.metrics-table tr.error-row:hover {
  background-color: rgba(231, 111, 81, 0.1);
}

.table-wrapper {
  max-height: 500px;
  overflow-y: auto;
  border-radius: var(--radius);
  background-color: var(--bg-secondary);
  scrollbar-width: thin;
  scrollbar-color: var(--primary) var(--bg-secondary);
}

.table-wrapper::-webkit-scrollbar {
  width: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.table-wrapper::-webkit-scrollbar-thumb {
  background-color: var(--primary);
  border-radius: 4px;
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
  font-size: 2rem;
  color: var(--primary);
}

.loading-text {
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
}

.error {
  color: var(--danger);
  background-color: rgba(231, 111, 81, 0.1);
  padding: 1.25rem;
  border-radius: var(--radius);
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border: 1px solid rgba(231, 111, 81, 0.2);
}

.error::before {
  content: '⚠️';
  font-size: 1.25rem;
}

.error-icon {
  color: var(--danger);
  font-size: 1.25rem;
  margin-right: 0.5rem;
}

.status-cell {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius);
  font-weight: 500;
  font-size: 0.875rem;
}

.status-cell.success {
  background-color: rgba(82, 183, 136, 0.1);
  color: var(--success);
}

.status-cell.error {
  background-color: rgba(231, 111, 81, 0.1);
  color: var(--danger);
}

.status-icon {
  margin-right: 0.5rem;
}

.response-time {
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
  font-size: 0.875rem;
  color: var(--text-primary);
}

.timestamp {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-style: italic;
}

@media (max-width: 768px) {
  .metrics {
    padding: 1rem;
  }

  .metrics-table th,
  .metrics-table td {
    padding: 0.75rem;
  }

  .chart-container {
    height: 300px;
  }
}
</style> 