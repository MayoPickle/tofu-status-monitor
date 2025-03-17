<template>
  <div class="dashboard">
    <h1>Dashboard</h1>
    
    <div v-if="loading">
      <p>Loading data...</p>
    </div>
    
    <div v-else-if="error">
      <p class="error">{{ error }}</p>
    </div>
    
    <div v-else class="dashboard-grid">
      <div class="card">
        <h2>Current Status</h2>
        <div class="status" :class="{'status-good': currentStatus === 'Good', 'status-bad': currentStatus === 'Bad'}">
          {{ currentStatus }}
        </div>
        <p>Last checked: {{ lastChecked }}</p>
      </div>
      
      <div class="card">
        <h2>24h Statistics</h2>
        <div class="stats">
          <div class="stat">
            <span class="stat-label">Total Requests:</span>
            <span class="stat-value">{{ stats.total_requests_24h }}</span>
          </div>
          <div class="stat">
            <span class="stat-label">Success Rate:</span>
            <span class="stat-value">{{ stats.success_rate_24h.toFixed(2) }}%</span>
          </div>
          <div class="stat">
            <span class="stat-label">Avg Response Time:</span>
            <span class="stat-value">{{ (stats.avg_response_time_24h * 1000).toFixed(2) }} ms</span>
          </div>
        </div>
      </div>
      
      <div class="card full-width">
        <h2>Recent Response Times</h2>
        <div class="chart-container">
          <LineChart 
            v-if="chartData.labels.length" 
            :chart-data="chartData"
            :options="chartOptions"
          />
          <p v-else>No data available</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { Line as LineChart } from 'vue-chart-3'
import { Chart, registerables } from 'chart.js'

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
    const stats = ref({
      total_requests_24h: 0,
      successful_requests_24h: 0,
      failed_requests_24h: 0,
      success_rate_24h: 0,
      avg_response_time_24h: 0
    })

    const fetchData = async () => {
      loading.value = true
      error.value = null
      
      try {
        // Fetch recent metrics
        const metricsResponse = await axios.get(`${apiUrl}/metrics/recent`, {
          params: { limit: 20 }
        })
        recentMetrics.value = metricsResponse.data.reverse() // Reverse to get chronological order
        
        // Fetch statistics
        const statsResponse = await axios.get(`${apiUrl}/metrics/stats`)
        stats.value = statsResponse.data
        
        loading.value = false
      } catch (err) {
        error.value = `Error loading data: ${err.message}`
        loading.value = false
        console.error(err)
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
      return {
        labels: recentMetrics.value.map(m => {
          const date = new Date(m.timestamp)
          return `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`
        }),
        datasets: [
          {
            label: 'Response Time (ms)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            data: recentMetrics.value.map(m => m.request_time * 1000), // Convert to ms
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
    
    onMounted(() => {
      fetchData()
      // Refresh data every 60 seconds
      setInterval(fetchData, 60000)
    })
    
    return {
      loading,
      error,
      recentMetrics,
      stats,
      currentStatus,
      lastChecked,
      chartData,
      chartOptions
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 100%;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}

.full-width {
  grid-column: 1 / -1;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
}

.card h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.25rem;
  color: #2c3e50;
}

.status {
  font-size: 2rem;
  font-weight: bold;
  margin: 1rem 0;
}

.status-good {
  color: #42b983;
}

.status-bad {
  color: #e53935;
}

.stats {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.stat-label {
  font-weight: 500;
  color: #666;
}

.stat-value {
  font-weight: bold;
}

.chart-container {
  height: 300px;
  position: relative;
}

.error {
  color: #e53935;
  background-color: rgba(229, 57, 53, 0.1);
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}
</style> 