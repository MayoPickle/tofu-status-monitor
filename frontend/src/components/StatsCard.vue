<template>
  <BaseCard class="stats-card animate-in" :title="title" :delay="delay">
    <template #header>
      <div class="card-header">
        <h2 class="card-title">{{ title }}</h2>
        <slot name="header-action">
          <button v-if="showRefresh" class="btn btn-outline btn-sm refresh-btn" @click="$emit('refresh')">
            <svg viewBox="0 0 24 24" width="16" height="16">
              <path fill="currentColor" d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" />
            </svg>
            <span>Refresh</span>
          </button>
        </slot>
      </div>
      <div class="card-subtitle">Last 24 hours monitoring statistics</div>
    </template>
    
    <div class="stats-grid">
      <div 
        v-for="(stat, index) in stats" 
        :key="index" 
        class="stat-item animate-in" 
        :class="getStatusClass(stat.class)"
        :style="getStatDelay(index)"
      >
        <div class="stat-icon" v-if="stat.icon">
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path fill="currentColor" :d="getIconPath(stat.icon)" />
          </svg>
        </div>
        <div class="stat-content">
          <div class="stat-header">
            <div class="stat-value" :class="stat.class">
              {{ stat.value }}
            </div>
            <div v-if="stat.class" class="status-indicator" :class="stat.class"></div>
          </div>
          <div class="stat-label">{{ stat.label }}</div>
        </div>
        <div class="stat-bg-indicator" :class="stat.class"></div>
      </div>
    </div>
    
    <template v-if="showTrends" #footer>
      <div class="trends-container">
        <div class="trend-item" v-for="(trend, index) in trends" :key="index">
          <div class="trend-label">{{ trend.label }}</div>
          <div class="trend-value" :class="trend.direction">
            {{ trend.value }}
            <svg v-if="trend.direction === 'up'" viewBox="0 0 24 24" width="16" height="16">
              <path fill="currentColor" d="M7,15L12,10L17,15H7Z" />
            </svg>
            <svg v-else-if="trend.direction === 'down'" viewBox="0 0 24 24" width="16" height="16">
              <path fill="currentColor" d="M7,10L12,15L17,10H7Z" />
            </svg>
          </div>
        </div>
      </div>
    </template>
  </BaseCard>
</template>

<script>
import BaseCard from './BaseCard.vue'

export default {
  name: 'StatsCard',
  components: {
    BaseCard
  },
  props: {
    title: {
      type: String,
      default: 'Statistics'
    },
    stats: {
      type: Array,
      required: true,
      validator: (stats) => {
        return stats.every(stat => 
          typeof stat.value !== 'undefined' && 
          typeof stat.label !== 'undefined'
        )
      }
    },
    showRefresh: {
      type: Boolean,
      default: true
    },
    delay: {
      type: Number,
      default: 0.1
    },
    trends: {
      type: Array,
      default: () => []
    },
    showTrends: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    getStatDelay(index) {
      return { '--delay': `${this.delay + 0.05 + (index * 0.05)}s` }
    },
    getStatusClass(statusClass) {
      if (!statusClass) return '';
      return `bg-status-${statusClass}`;
    },
    getIconPath(iconName) {
      const icons = {
        'globe': 'M17.9,17.39C17.64,16.59 16.89,16 16,16H15V13A1,1 0 0,0 14,12H8V10H10A1,1 0 0,0 11,9V7H13A2,2 0 0,0 15,5V4.59C17.93,5.77 20,8.64 20,12C20,14.08 19.2,15.97 17.9,17.39M11,19.93C7.05,19.44 4,16.08 4,12C4,11.38 4.08,10.78 4.21,10.21L9,15V16A2,2 0 0,0 11,18M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z',
        'check-circle': 'M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z',
        'clock': 'M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z',
        'alert-triangle': 'M13,14H11V10H13M13,18H11V16H13M1,21H23L12,2L1,21Z'
      };
      return icons[iconName] || '';
    }
  }
}
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1.25rem;
  padding: 0.5rem;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-subtitle {
  font-size: 0.85rem;
  color: var(--text-secondary, #6b7280);
  margin-top: 0.25rem;
}

.stat-item {
  display: flex;
  padding: 1.25rem;
  border-radius: 8px;
  background-color: white;
  border: 1px solid #f3f4f6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  transition: all 0.2s ease;
  position: relative;
  overflow: hidden;
}

.stat-item:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.stat-icon {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  margin-right: 1rem;
  color: #6b7280;
}

.stat-content {
  flex-grow: 1;
  z-index: 1;
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  letter-spacing: -0.5px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-left: 0.5rem;
}

/* Status indicator colors */
.status-indicator.excellent {
  background-color: #16a34a;
  box-shadow: 0 0 6px rgba(22, 163, 74, 0.5);
}

.status-indicator.good {
  background-color: #2563eb;
  box-shadow: 0 0 6px rgba(37, 99, 235, 0.5);
}

.status-indicator.average {
  background-color: #d97706;
  box-shadow: 0 0 6px rgba(217, 119, 6, 0.5);
}

.status-indicator.poor {
  background-color: #dc2626;
  box-shadow: 0 0 6px rgba(220, 38, 38, 0.5);
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  font-weight: 500;
}

/* Background indicator for status */
.stat-bg-indicator {
  position: absolute;
  top: 0;
  right: 0;
  width: 8px;
  height: 100%;
  opacity: 0.8;
}

.stat-bg-indicator.excellent {
  background-color: #16a34a;
}

.stat-bg-indicator.good {
  background-color: #2563eb;
}

.stat-bg-indicator.average {
  background-color: #d97706;
}

.stat-bg-indicator.poor {
  background-color: #dc2626;
}

/* Status text colors */
.stat-value.excellent {
  color: #16a34a;
}

.stat-value.good {
  color: #2563eb;
}

.stat-value.average {
  color: #d97706;
}

.stat-value.poor {
  color: #dc2626;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-weight: 500;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.85rem;
  border-radius: var(--radius, 6px);
}

.trends-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 0.5rem;
  border-top: 1px solid #f3f4f6;
  padding-top: 1rem;
}

.trend-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.trend-label {
  font-size: 0.85rem;
  color: #6b7280;
}

.trend-value {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-weight: 500;
  font-size: 0.85rem;
}

.trend-value.up {
  color: #16a34a;
}

.trend-value.down {
  color: #dc2626;
}

/* Media queries */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .trends-container {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .refresh-btn {
    width: 100%;
    justify-content: center;
    margin-top: 0.5rem;
  }
}
</style> 