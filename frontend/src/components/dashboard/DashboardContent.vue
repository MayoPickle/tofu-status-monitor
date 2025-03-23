<template>
  <div class="dashboard-layout">
    <!-- 标准网格布局 - 卡片组件 -->
    <div class="dashboard-grid" :class="{ 'limited-view': !canViewDetailedMetrics }">
      <!-- Status Card - 基本状态卡片，所有用户可见 -->
      <StatusCard 
        :status="currentStatus" 
        :last-checked="lastChecked" 
        :url="siteUrl"
        :http-status="httpStatus"
        :http-status-text="httpStatusText"
      />
      
      <!-- Uptime Card - 需要上线时间数据权限 -->
      <UptimeCard 
        v-if="canAccessUptime && canViewMetrics" 
        :uptime-items="uptimeItems"
      />
      
      <!-- Alerts Card - 需要查看警报权限 -->
      <AlertsCard 
        v-if="hasPermissionViewAlerts && canViewMetrics" 
        :alerts="recentAlerts"
      />
    </div>
    
    <!-- Statistics Card - 需要详细指标权限和站点指标查看权限 -->
    <div class="full-width-container" v-if="canViewDetailedMetrics && canViewMetrics">
      <StatsCard 
        title="24h Statistics"
        :stats="statsItems"
        :trends="statsTrends"
        :show-trends="true"
        @refresh="$emit('refresh-stats')"
      />
    </div>
    
    <!-- 小时可用度网格 - 占据整行宽度 -->
    <div class="full-width-container" v-if="canViewDetailedMetrics && canViewMetrics">
      <HourlyAvailabilityGrid
        :hourly-data="hourlyAvailabilityData"
        @refresh="$emit('refresh-hourly')"
      />
    </div>
    
    <!-- Response Time Chart Card - 需要历史数据访问权限和站点指标查看权限 -->
    <div class="full-width-container">
      <ChartCard 
        title="Response Times"
        v-model="selectedChartPeriod"
        :periods="chartPeriods"
        :limited="!canViewMetrics || !canAccessHistorical"
        :has-chart-data="chartData.labels.length > 0"
        :extra-classes="['response-times-card', { 'limited-data': !canViewMetrics || !canAccessHistorical }]"
      >
        <div v-if="!canAccessHistorical && selectedChartPeriod !== '24h'" class="permission-notice">
          <p>您没有查看历史数据的权限</p>
        </div>
        <LineChart 
          v-else-if="chartData.labels.length && canViewMetrics" 
          :chart-data="chartData"
          :options="chartOptions"
          class="chart-wrapper"
        />
      </ChartCard>
    </div>
  </div>
</template>

<script>
import { ref, watch } from 'vue'
import { LineChart } from 'vue-chart-3'
import StatusCard from '@/components/StatusCard.vue'
import StatsCard from '@/components/StatsCard.vue'
import UptimeCard from '@/components/UptimeCard.vue'
import AlertsCard from '@/components/AlertsCard.vue'
import ChartCard from '@/components/ChartCard.vue'
import HourlyAvailabilityGrid from '@/components/HourlyAvailabilityGrid.vue'

export default {
  name: 'DashboardContent',
  components: {
    LineChart,
    StatusCard,
    StatsCard,
    UptimeCard,
    AlertsCard,
    ChartCard,
    HourlyAvailabilityGrid
  },
  props: {
    currentStatus: {
      type: String,
      required: true
    },
    lastChecked: {
      type: String,
      required: true
    },
    siteUrl: {
      type: String,
      required: true
    },
    httpStatus: {
      type: Number,
      default: null
    },
    httpStatusText: {
      type: String,
      default: ''
    },
    canViewDetailedMetrics: {
      type: Boolean,
      required: true
    },
    canViewMetrics: {
      type: Boolean,
      required: true
    },
    canAccessUptime: {
      type: Boolean,
      required: true
    },
    canAccessHistorical: {
      type: Boolean,
      required: true
    },
    hasPermissionViewAlerts: {
      type: Boolean,
      required: true
    },
    statsItems: {
      type: Array,
      required: true
    },
    statsTrends: {
      type: Array,
      default: () => []
    },
    uptimeItems: {
      type: Array,
      required: true
    },
    recentAlerts: {
      type: Array,
      required: true
    },
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      required: true
    },
    chartPeriods: {
      type: Array,
      required: true
    },
    initialChartPeriod: {
      type: String,
      default: '24h'
    },
    hourlyAvailabilityData: {
      type: Array,
      default: () => []
    }
  },
  setup(props, { emit }) {
    const selectedChartPeriod = ref(props.initialChartPeriod);
    
    watch(selectedChartPeriod, (newValue) => {
      emit('update:chartPeriod', newValue);
    });
    
    return {
      selectedChartPeriod
    };
  }
}
</script>

<style scoped>
.dashboard-layout {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 1.5rem;
}

.limited-view {
  grid-template-columns: 1fr;
  max-width: 500px;
  margin: 0 auto;
}

.full-width-container {
  width: 100%;
}

@media (max-width: 768px) {
  .dashboard-layout {
    gap: 1rem;
  }
  
  .dashboard-grid {
    gap: 1rem;
  }
}
</style> 