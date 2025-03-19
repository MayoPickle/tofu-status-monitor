<template>
  <div class="metrics">
    <MetricsHeader />
    
    <LoadingError :loading="loading" :error="error">
      <WeeklyAveragesChart :weeklyAverages="weeklyAverages" />
      <RecentRequestsTable :metrics="recentMetrics" />
    </LoadingError>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import MetricsHeader from '@/components/MetricsHeader.vue'
import WeeklyAveragesChart from '@/components/WeeklyAveragesChart.vue'
import RecentRequestsTable from '@/components/RecentRequestsTable.vue'
import LoadingError from '@/components/LoadingError.vue'

export default {
  name: 'MetricsView',
  components: {
    MetricsHeader,
    WeeklyAveragesChart,
    RecentRequestsTable,
    LoadingError
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
    
    onMounted(() => {
      fetchData()
      // Refresh data every 60 seconds
      setInterval(fetchData, 60000)
    })
    
    return {
      loading,
      error,
      recentMetrics,
      weeklyAverages
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

@media (max-width: 768px) {
  .metrics {
    padding: 1rem;
  }
}
</style> 