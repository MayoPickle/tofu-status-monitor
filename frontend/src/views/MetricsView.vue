<template>
  <div class="metrics">
    <h1>Detailed Metrics</h1>
    
    <div v-if="loading">
      <p>Loading data...</p>
    </div>
    
    <div v-else-if="error">
      <p class="error">{{ error }}</p>
    </div>
    
    <div v-else>
      <div class="card">
        <h2>Weekly Averages</h2>
        <div class="chart-container">
          <LineChart 
            v-if="weeklyChartData.labels.length" 
            :chart-data="weeklyChartData"
            :options="chartOptions"
          />
          <p v-else>No weekly average data available</p>
        </div>
      </div>
      
      <div class="card">
        <h2>Recent Requests</h2>
        <table class="metrics-table">
          <thead>
            <tr>
              <th>Time</th>
              <th>Status</th>
              <th>Response Time</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="metric in recentMetrics" :key="metric.id" :class="{ 'error-row': !isSuccessful(metric) }">
              <td>{{ formatDate(metric.timestamp) }}</td>
              <td>{{ metric.status_code }}</td>
              <td>{{ formatResponseTime(metric.request_time) }}</td>
            </tr>
          </tbody>
        </table>
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
  name: 'MetricsView',
  components: {
    LineChart
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
    
    const weeklyChartData = computed(() => {
      return {
        labels: weeklyAverages.value.map(avg => {
          const date = new Date(avg.week_start)
          return `${date.getMonth() + 1}/${date.getDate()}`
        }),
        datasets: [
          {
            label: 'Weekly Average Response Time (ms)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgb(75, 192, 192)',
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
      weeklyChartData,
      chartOptions
    }
  }
}
</script>

<style scoped>
.metrics {
  max-width: 100%;
}

.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
}

.card h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.25rem;
  color: #2c3e50;
}

.chart-container {
  height: 300px;
  position: relative;
  margin-bottom: 1.5rem;
}

.metrics-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.metrics-table th {
  text-align: left;
  padding: 0.75rem;
  background-color: #f5f7fa;
  border-bottom: 2px solid #e1e4e8;
  font-weight: 600;
}

.metrics-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #e1e4e8;
}

.error-row {
  background-color: rgba(229, 57, 53, 0.05);
}

.error {
  color: #e53935;
  background-color: rgba(229, 57, 53, 0.1);
  padding: 1rem;
  border-radius: 4px;
  margin: 1rem 0;
}
</style> 