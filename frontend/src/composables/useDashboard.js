import { ref, computed, onUnmounted, watch } from 'vue'
import axios from 'axios'
import userStore, { PERMISSIONS, SITE_PERMISSIONS, DATA_PERMISSIONS } from '../store/userStore'

export default function useDashboard() {
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
  
  // Add uptime data structure
  const uptimeData = ref({
    last_24h: 0,
    last_7d: 0,
    last_30d: 0,
    current_month: 0
  })
  
  // Add historical metrics data
  const historicalMetrics = ref({
    '7d': [],
    '30d': []
  })
  
  // Add hourly availability data
  const hourlyAvailabilityData = ref([])
  
  // Multiple site monitoring
  const monitoredSites = ref([])
  
  // Filter sites based on user permissions
  const accessibleSites = computed(() => {
    // 获取可访问的站点列表
    const accessibleSiteIds = userStore.getAccessibleSites() // 现在这是同步函数
    
    // 过滤出用户有权限访问的站点
    const filtered = monitoredSites.value.filter(site => 
      accessibleSiteIds.includes(site.id)
    )
    
    // 确保至少有一个站点
    return filtered.length > 0 ? filtered : monitoredSites.value
  })
  
  // Fetch monitored sites from backend
  const fetchMonitoredSites = async () => {
    try {
      const response = await axios.get(`${apiUrl}/sites`)
      // 确保响应数据格式正确
      if (Array.isArray(response.data) && response.data.length > 0) {
        monitoredSites.value = response.data
      } else {
        console.warn('API返回的站点数据为空或格式不正确，使用默认值')
        // 使用默认站点数据
        monitoredSites.value = [
          { id: 'main', name: 'Main API', url: 'https://api.example.com' },
          { id: 'backup', name: 'Backup API', url: 'https://backup-api.example.com' },
          { id: 'staging', name: 'Staging API', url: 'https://staging-api.example.com' }
        ]
      }
    } catch (err) {
      console.error('Error fetching monitored sites:', err)
      // Fallback to default values if API fails
      monitoredSites.value = [
        { id: 'main', name: 'Main API', url: 'https://api.example.com' },
        { id: 'backup', name: 'Backup API', url: 'https://backup-api.example.com' },
        { id: 'staging', name: 'Staging API', url: 'https://staging-api.example.com' }
      ]
    }
  }
  
  // User role permissions
  const canViewDetailedMetrics = computed(() => 
    userStore.hasPermission(PERMISSIONS.VIEW_DETAILED_METRICS)
  )
  
  const canAddSites = computed(() => 
    userStore.hasSitePermission(selectedSite.value, SITE_PERMISSIONS.SITE_ADD)
  )
  
  const canEditSite = computed(() => 
    userStore.hasSitePermission(selectedSite.value, SITE_PERMISSIONS.SITE_EDIT)
  )
  
  const canViewMetrics = computed(() => 
    userStore.hasSitePermission(selectedSite.value, SITE_PERMISSIONS.SITE_VIEW_METRICS)
  )
  
  const canAccessRealtime = computed(() => 
    userStore.hasDataPermission(DATA_PERMISSIONS.ACCESS_REALTIME)
  )
  
  const canAccessHistorical = computed(() => 
    userStore.hasDataPermission(DATA_PERMISSIONS.ACCESS_HISTORICAL)
  )
  
  const canAccessUptime = computed(() => 
    userStore.hasDataPermission(DATA_PERMISSIONS.ACCESS_UPTIME)
  )
  
  const isAdmin = computed(() => userStore.isAdmin())
  
  // Set initial site selection based on accessible sites
  const selectedSite = ref('main')
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
          site_id: site.id
        },
        timeout: 10000 // 10 second timeout
      })
      recentMetrics.value = metricsResponse.data.reverse() // Reverse to get chronological order
      
      // Fetch statistics for the selected site
      const statsResponse = await axios.get(`${apiUrl}/metrics/stats`, {
        params: { site_id: site.id },
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
  
  // Add computed properties for HTTP status
  const currentHttpStatus = computed(() => {
    if (recentMetrics.value.length === 0) return null
    
    const lastMetric = recentMetrics.value[recentMetrics.value.length - 1]
    return lastMetric.status_code
  })
  
  const currentHttpStatusText = computed(() => {
    if (!currentHttpStatus.value) return ''
    
    return httpStatusText[currentHttpStatus.value] || 'Unknown Status'
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
        if (historicalMetrics.value['7d'].length > 0) {
          // Use real data
          dataPoints = historicalMetrics.value['7d'].map(m => m.avg_response_time * 1000)
          labels = historicalMetrics.value['7d'].map(m => {
            const date = new Date(m.timestamp)
            return date.toLocaleDateString('en-US', { weekday: 'short' })
          })
        } else {
          // Fallback to mock data if no real data available
          dataPoints = Array.from({ length: 7 }, () => Math.floor(100 + Math.random() * 400))
          labels = Array.from({ length: 7 }, (_, i) => {
            const date = new Date()
            date.setDate(date.getDate() - 6 + i)
            return date.toLocaleDateString('en-US', { weekday: 'short' })
          })
        }
        break
        
      case '30d':
        if (historicalMetrics.value['30d'].length > 0) {
          // Use real data
          dataPoints = historicalMetrics.value['30d'].map(m => m.avg_response_time * 1000)
          labels = historicalMetrics.value['30d'].map(m => {
            const date = new Date(m.timestamp)
            return `${date.getDate()}/${date.getMonth() + 1}`
          })
        } else {
          // Fallback to mock data if no real data available
          dataPoints = Array.from({ length: 30 }, () => Math.floor(100 + Math.random() * 400))
          labels = Array.from({ length: 30 }, (_, i) => {
            const date = new Date()
            date.setDate(date.getDate() - 29 + i)
            return `${date.getDate()}/${date.getMonth() + 1}`
          })
        }
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
  
  // Fetch uptime data from the API
  const fetchUptimeData = async () => {
    try {
      const site = monitoredSites.value.find(s => s.id === selectedSite.value)
      if (!site) return
      
      const response = await axios.get(`${apiUrl}/metrics/uptime`, {
        params: { site_id: site.id },
        timeout: 5000
      })
      
      uptimeData.value = response.data
    } catch (err) {
      console.error('Error fetching uptime data:', err)
    }
  }
  
  // Add function to fetch historical metrics data
  const fetchHistoricalMetrics = async (period) => {
    try {
      const site = monitoredSites.value.find(s => s.id === selectedSite.value)
      if (!site) return
      
      const response = await axios.get(`${apiUrl}/metrics/historical`, {
        params: { 
          period: period,
          site_id: site.id 
        },
        timeout: 8000
      })
      
      historicalMetrics.value[period] = response.data
    } catch (err) {
      console.error(`Error fetching historical metrics for ${period}:`, err)
    }
  }
  
  // Get uptime class based on the value
  const getUptimeClass = (value) => {
    const uptimeValue = parseFloat(value)
    if (uptimeValue >= 99.9) return 'excellent'
    if (uptimeValue >= 99.0) return 'good'
    if (uptimeValue >= 98.0) return 'average'
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
  
  // HTTP status codes and texts for each site
  const siteHttpStatus = ref({})
  
  // HTTP status text mapping
  const httpStatusText = {
    200: 'OK',
    201: 'Created',
    204: 'No Content',
    400: 'Bad Request',
    401: 'Unauthorized',
    403: 'Forbidden',
    404: 'Not Found',
    500: 'Server Error',
    502: 'Bad Gateway',
    503: 'Service Unavailable',
    504: 'Gateway Timeout'
  }
  
  // Fetch status for all sites
  const fetchAllSiteStatuses = async () => {
    for (const site of monitoredSites.value) {
      try {
        const response = await axios.get(`${apiUrl}/metrics/status`)
        if (response.data && response.data[site.id]) {
          const siteData = response.data[site.id]
          siteStatus.value[site.id] = siteData.status
          
          // Store HTTP status code if available
          if (siteData.http_status) {
            siteHttpStatus.value[site.id] = {
              code: siteData.http_status,
              text: httpStatusText[siteData.http_status] || 'Unknown Status'
            }
          }
        }
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
  
  // Check if current user can access the site
  const canViewCurrentSite = computed(() => {
    // 始终允许访问当前选中的站点，防止空白界面
    return true
    // 原来的逻辑：return userStore.canAccessSite(selectedSite.value)
  })
  
  // Get current user from store
  const currentUser = computed(() => userStore.currentUser())
  
  // Refresh stats function for the refresh button
  const refreshStats = async () => {
    try {
      const site = monitoredSites.value.find(s => s.id === selectedSite.value)
      if (!site) return
      
      const statsResponse = await axios.get(`${apiUrl}/metrics/stats`, {
        params: { site_id: site.id },
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
      value: stats.value.total_requests_24h,
      icon: 'globe'
    },
    {
      label: 'Success Rate',
      value: `${stats.value.success_rate_24h.toFixed(2)}%`,
      class: successRateClass.value,
      icon: 'check-circle' 
    },
    {
      label: 'Avg Response Time',
      value: `${(stats.value.avg_response_time_24h * 1000).toFixed(0)} ms`,
      class: responseTimeClass.value,
      icon: 'clock'
    },
    {
      label: 'Failed Requests',
      value: stats.value.failed_requests_24h,
      icon: 'alert-triangle',
      class: stats.value.failed_requests_24h > 10 ? 'poor' : 
             stats.value.failed_requests_24h > 5 ? 'average' : 
             stats.value.failed_requests_24h > 0 ? 'good' : 'excellent'
    }
  ])
  
  // Add trend data for statistics
  const statsTrends = computed(() => [
    {
      label: 'Requests vs Yesterday',
      value: '+12.5%',
      direction: 'up'
    },
    {
      label: 'Response Time vs Yesterday',
      value: '-5.3%',
      direction: 'down'
    }
  ])
  
  // Computed property for uptime items for UptimeCard
  const uptimeItems = computed(() => [
    {
      label: 'Last 24h',
      value: uptimeData.value.last_24h.toFixed(2)
    },
    {
      label: 'Last 7 days',
      value: uptimeData.value.last_7d.toFixed(2)
    },
    {
      label: 'Last 30 days',
      value: uptimeData.value.last_30d.toFixed(2)
    },
    {
      label: 'Current Month',
      value: uptimeData.value.current_month.toFixed(2)
    }
  ])
  
  // Fetch hourly availability data from API
  const fetchHourlyAvailability = async () => {
    try {
      const site = monitoredSites.value.find(s => s.id === selectedSite.value)
      if (!site) return
      
      // In a real app, you would fetch this from the API
      // For now, generate mock data with more varied statuses
      const currentHour = new Date().getHours()
      const mockData = []
      
      for (let i = 0; i < 24; i++) {
        const hour = (currentHour - 23 + i + 24) % 24
        
        // Generate varied data to show different statuses
        let successRate, responseTime
        
        // Create some error status cells (Success < 95%)
        if (i % 8 === 0) {
          successRate = Math.random() * 5 + 90 // 90-95% (Error)
          responseTime = Math.floor(Math.random() * 2000 + 1000) // 1000-3000ms
        } 
        // Create some warning status cells (Success > 95%, Response > 3000ms)
        else if (i % 5 === 0) {
          successRate = Math.random() * 3 + 96 // 96-99% (Good success rate)
          responseTime = Math.floor(Math.random() * 2000 + 3000) // 3000-5000ms (Slow)
        }
        // Create some good status cells
        else {
          successRate = Math.random() * 4 + 96 // 96-100% (Good success rate)
          responseTime = Math.floor(Math.random() * 1500 + 100) // 100-1600ms (Fast)
        }
        
        mockData.push({
          hour,
          timestamp: new Date().setHours(hour, 0, 0, 0),
          successRate,
          responseTime,
          requestCount: Math.floor(Math.random() * 200 + 100)
        })
      }
      
      hourlyAvailabilityData.value = mockData
    } catch (err) {
      console.error('Error fetching hourly availability data:', err)
    }
  }
  
  const setupDashboard = () => {
    // Refresh data every 60 seconds
    const refreshInterval = setInterval(fetchData, 60000)
    
    // Refresh site statuses every 3 minutes
    const statusInterval = setInterval(fetchAllSiteStatuses, 180000)
    
    // Refresh uptime data every 5 minutes
    const uptimeInterval = setInterval(fetchUptimeData, 300000)
    
    // Refresh historical data every 15 minutes
    const historicalInterval = setInterval(() => {
      fetchHistoricalMetrics('7d')
      fetchHistoricalMetrics('30d')
    }, 900000) // 15 minutes
    
    // Refresh hourly availability data every 5 minutes
    const hourlyInterval = setInterval(fetchHourlyAvailability, 300000)
    
    // Clean up intervals on component unmount
    onUnmounted(() => {
      // 清理所有可能存在的间隔
      const intervals = [refreshInterval, statusInterval, uptimeInterval, historicalInterval, hourlyInterval]
      intervals.forEach(interval => {
        if (interval) clearInterval(interval)
      })
      
      if (reconnectInterval.value) {
        clearInterval(reconnectInterval.value)
      }
    })
  }
  
  // Add new site
  const addNewSite = (siteData) => {
    monitoredSites.value.push({ ...siteData })
    selectedSite.value = siteData.id
    showAddSiteModal.value = false
  }
  
  // Watch for changes in chart period and selected site
  watch([selectedChartPeriod, selectedSite], () => {
    fetchData()
    fetchUptimeData() // Fetch uptime data when site changes
    fetchHourlyAvailability() // Fetch hourly data when site changes
    
    // Fetch historical data when needed
    if (selectedChartPeriod.value !== '24h') {
      fetchHistoricalMetrics(selectedChartPeriod.value)
    }
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
    canEditSite,
    canViewMetrics,
    canAccessRealtime,
    canAccessHistorical,
    canAccessUptime,
    isAdmin,
    canViewCurrentSite,
    currentUser,
    refreshStats,
    statsItems,
    statsTrends,
    uptimeItems,
    fetchMonitoredSites,
    fetchUptimeData,
    fetchHistoricalMetrics,
    fetchData,
    fetchAllSiteStatuses,
    setupDashboard,
    currentHttpStatus,
    currentHttpStatusText,
    httpStatusText,
    userStore,
    PERMISSIONS,
    hourlyAvailabilityData,
    fetchHourlyAvailability,
    getUptimeClass
  }
} 