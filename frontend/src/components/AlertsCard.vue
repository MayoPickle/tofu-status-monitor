<template>
  <BaseCard class="alerts-card animate-in" :title="title" :delay="delay">
    <template #header>
      <h2 class="card-title">{{ title }}</h2>
      <span class="alerts-count" v-if="alerts.length">{{ alerts.length }}</span>
    </template>
    
    <div v-if="alerts.length" class="alerts-list">
      <div 
        v-for="(alert, index) in alerts" 
        :key="index" 
        class="alert-item animate-in" 
        :class="alert.severity"
        :style="{ '--delay': delay + 0.05 + (index * 0.05) + 's' }"
      >
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
  </BaseCard>
</template>

<script>
import BaseCard from './BaseCard.vue'

export default {
  name: 'AlertsCard',
  components: {
    BaseCard
  },
  props: {
    title: {
      type: String,
      default: 'Recent Alerts'
    },
    alerts: {
      type: Array,
      default: () => []
    },
    delay: {
      type: Number,
      default: 0.2
    }
  },
  methods: {
    formatAlertTime(timestamp) {
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
  }
}
</script>

<style scoped>
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
</style> 