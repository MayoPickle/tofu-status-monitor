<template>
  <div class="dashboard">
    <!-- 太空背景元素 -->
    <div class="stars">
      <div class="star" v-for="n in 80" :key="n" :style="{ 
        top: Math.random() * 100 + '%', 
        left: Math.random() * 100 + '%',
        width: (Math.random() * 2 + 1) + 'px',
        height: (Math.random() * 2 + 1) + 'px',
        animationDelay: Math.random() * 5 + 's'
      }"></div>
    </div>
    <div class="grid-lines"></div>
    <div class="planet-effect"></div>
    <div class="planet-ring"></div>
    <div class="orbital-path"></div>
    
    <!-- Dashboard Header -->
    <DashboardHeader 
      :connection-status="connectionStatus"
      :connection-status-text="connectionStatusText"
      :error="error"
      :current-user="currentUser"
      @retry-connection="retryConnection"
    />
    
    <div class="dashboard-content">
      <!-- Site Tabs -->
      <SiteTabs 
        v-model="selectedSite" 
        :sites="monitoredSites" 
        :site-status="siteStatus" 
        :show-add-button="canAddSites"
        @add="showAddSiteModal = true"
      />
      
      <!-- Site Content -->
      <transition name="fade-up" mode="out-in">
        <AccessDenied v-if="!canViewCurrentSite" />
        
        <DashboardContent 
          v-else
          :current-status="currentStatus"
          :last-checked="lastChecked"
          :site-url="selectedSiteUrl"
          :http-status="currentHttpStatus"
          :http-status-text="currentHttpStatusText"
          :can-view-detailed-metrics="canViewDetailedMetrics"
          :can-view-metrics="canViewMetrics"
          :can-access-uptime="canAccessUptime"
          :can-access-historical="canAccessHistorical"
          :has-permission-view-alerts="userStore.hasPermission(PERMISSIONS.VIEW_ALERTS)"
          :stats-items="statsItems"
          :stats-trends="statsTrends"
          :uptime-items="uptimeItems"
          :recent-alerts="recentAlerts"
          :chart-data="chartData"
          :chart-options="chartOptions"
          :chart-periods="chartPeriods"
          :initial-chart-period="selectedChartPeriod"
          :hourly-availability-data="hourlyAvailabilityData"
          @refresh-stats="refreshStats"
          @refresh-hourly="fetchHourlyAvailability"
          @update:chart-period="selectedChartPeriod = $event"
        />
      </transition>
    </div>
    
    <!-- Add Site Modal -->
    <AddSiteModal 
      v-model="showAddSiteModal" 
      @submit="addNewSite"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'

// Composables
import useDashboard from '@/composables/useDashboard'

// Components
import DashboardHeader from '@/components/dashboard/DashboardHeader.vue'
import DashboardContent from '@/components/dashboard/DashboardContent.vue'
import AccessDenied from '@/components/dashboard/AccessDenied.vue'
import SiteTabs from '@/components/SiteTabs.vue'
import AddSiteModal from '@/components/AddSiteModal.vue'

// Initialize dashboard composable
const {
  // Status information
  connectionStatus,
  connectionStatusText,
  error,
  currentUser,
  retryConnection,
  
  // Site data
  monitoredSites,
  selectedSite,
  selectedSiteUrl,
  siteStatus,
  canViewCurrentSite,
  canAddSites,
  
  // Stats and metrics
  currentStatus,
  lastChecked,
  currentHttpStatus,
  currentHttpStatusText,
  statsItems,
  statsTrends,
  uptimeItems,
  recentAlerts,
  hourlyAvailabilityData,
  refreshStats,
  
  // Permissions
  canViewDetailedMetrics,
  canViewMetrics,
  canAccessUptime,
  canAccessHistorical,
  userStore,
  PERMISSIONS,
  
  // Chart data
  chartData,
  chartOptions,
  chartPeriods,
  selectedChartPeriod,
  
  // Modal and actions
  showAddSiteModal,
  addNewSite,
  
  // Data fetch methods
  fetchMonitoredSites,
  fetchData,
  fetchAllSiteStatuses,
  fetchUptimeData,
  fetchHistoricalMetrics,
  fetchHourlyAvailability,
  setupDashboard
} = useDashboard()

// Initialize dashboard on component mount
onMounted(async () => {
  // First fetch site information
  await fetchMonitoredSites()
  
  // Then fetch data for the selected site
  fetchData()
  fetchAllSiteStatuses()
  fetchUptimeData()
  
  // Fetch historical data for all periods
  fetchHistoricalMetrics('7d')
  fetchHistoricalMetrics('30d')
  
  // Fetch hourly availability data
  fetchHourlyAvailability()
  
  // Setup dashboard refresh intervals
  setupDashboard()
})
</script>

<style scoped>
@import '@/assets/css/dashboard-styles.css';
@import '@/assets/css/status-colors.css';
@import '@/assets/css/space-theme.css';

/* 太空主题样式 */
.dashboard {
  position: relative;
  min-height: 100%;
  overflow: hidden;
}

/* 星星背景 */
.stars {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -2;
  pointer-events: none;
}

.star {
  position: absolute;
  background-color: white;
  border-radius: 50%;
  opacity: 0.4;
  animation: twinkle 4s infinite ease-in-out;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(0.8); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

/* 网格背景 */
.grid-lines {
  position: fixed;
  z-index: -1;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  opacity: 0.06;
  background-image: 
    linear-gradient(to right, var(--primary) 1px, transparent 1px),
    linear-gradient(to bottom, var(--primary) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: grid-pulse 10s infinite ease-in-out;
}

@keyframes grid-pulse {
  0%, 100% { opacity: 0.04; }
  50% { opacity: 0.09; }
}

/* 行星效果 */
.planet-effect {
  position: fixed;
  width: 280px;
  height: 280px;
  top: -100px;
  right: -100px;
  background: radial-gradient(circle, rgba(42, 157, 143, 0.5) 0%, rgba(58, 134, 255, 0.3) 60%, transparent 100%);
  border-radius: 50%;
  box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
              inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  z-index: -2;
  animation: planetRotate 60s infinite linear;
  filter: blur(4px);
}

@keyframes planetRotate {
  0% {
    box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
                inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  }
  50% {
    box-shadow: inset -20px 20px 40px rgba(255, 255, 255, 0.4),
                inset 10px -10px 30px rgba(0, 0, 40, 0.6);
  }
  100% {
    box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
                inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  }
}

/* 行星环 */
.planet-ring {
  position: fixed;
  top: -120px;
  right: -120px;
  width: 320px;
  height: 320px;
  border-radius: 50%;
  z-index: -1;
  overflow: visible;
  transform: rotateX(75deg) rotateY(15deg);
  pointer-events: none;
  animation: orbitRotate 80s infinite linear;
}

@keyframes orbitRotate {
  from { transform: rotateX(75deg) rotateY(15deg) rotateZ(0deg); }
  to { transform: rotateX(75deg) rotateY(15deg) rotateZ(360deg); }
}

.planet-ring::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 280px;
  height: 280px;
  transform: translate(-50%, -50%);
  border: 10px solid rgba(251, 186, 114, 0.2);
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(251, 186, 114, 0.4);
}

.planet-ring::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 240px;
  height: 240px;
  transform: translate(-50%, -50%);
  border: 6px solid rgba(58, 134, 255, 0.2);
  border-radius: 50%;
}

/* 轨道路径 */
.orbital-path {
  position: fixed;
  top: 10%;
  left: -10%;
  width: 100vh;
  height: 100vh;
  border: 1px dashed rgba(58, 134, 255, 0.1);
  border-radius: 50%;
  animation: orbit-rotate 150s linear infinite;
  z-index: -1;
}

@keyframes orbit-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 内容区域 */
.dashboard-content {
  position: relative;
  z-index: 1;
  backdrop-filter: blur(2px);
}

/* 动画效果 */
.fade-up-enter-active,
.fade-up-leave-active {
  transition: all 0.3s cubic-bezier(0.17, 0.67, 0.83, 0.67);
}

.fade-up-enter-from,
.fade-up-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 适配移动设备 */
@media (max-width: 768px) {
  .planet-effect, .planet-ring {
    display: none;
  }
}
</style> 