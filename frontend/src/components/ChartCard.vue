<template>
  <BaseCard class="chart-card full-width animate-in" :class="extraClasses" :title="title" :delay="delay">
    <template #header>
      <h2 class="card-title">{{ title }}</h2>
      <slot name="header-action">
        <div v-if="periods.length" class="chart-controls">
          <button 
            v-for="period in periods" 
            :key="period.value" 
            :class="['chart-period-button', { active: modelValue === period.value }]"
            @click="$emit('update:modelValue', period.value)"
          >
            {{ period.label }}
          </button>
        </div>
      </slot>
    </template>
    
    <div v-if="limited" class="limited-access-message">
      <svg viewBox="0 0 24 24" width="24" height="24">
        <path fill="currentColor" d="M18,8H17V6A5,5 0 0,0 12,1A5,5 0 0,0 7,6V8H6A2,2 0 0,0 4,10V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V10A2,2 0 0,0 18,8M8.9,6C8.9,4.29 10.29,2.9 12,2.9C13.71,2.9 15.1,4.29 15.1,6V8H8.9V6M16,16H13V19H11V16H8V14H11V11H13V14H16V16Z" />
      </svg>
      <div class="limited-access-content">
        <p class="limited-heading">{{ limitedTitle }}</p>
        <p>{{ limitedMessage }}</p>
      </div>
    </div>
    
    <div v-else class="chart-container">
      <slot></slot>
      <div v-if="!hasChartData" class="no-data">
        <svg viewBox="0 0 24 24" width="24" height="24">
          <path fill="currentColor" d="M21,21V17.5C21,16.67 20.33,16 19.5,16C18.67,16 18,16.67 18,17.5V21H16V9H14V21H9V2H7V21H3V19H1V21A2,2 0 0,0 3,23H19A2,2 0 0,0 21,21M5,16H7V19H5V16Z" />
        </svg>
        <p>{{ noDataMessage }}</p>
      </div>
    </div>
  </BaseCard>
</template>

<script>
import BaseCard from './BaseCard.vue'

export default {
  name: 'ChartCard',
  components: {
    BaseCard
  },
  props: {
    title: {
      type: String,
      default: 'Chart'
    },
    modelValue: {
      type: String,
      default: ''
    },
    periods: {
      type: Array,
      default: () => []
    },
    hasChartData: {
      type: Boolean,
      default: true
    },
    limited: {
      type: Boolean,
      default: false
    },
    limitedTitle: {
      type: String,
      default: 'Limited Access'
    },
    limitedMessage: {
      type: String,
      default: 'Login with higher privileges to view detailed metrics and historical data.'
    },
    noDataMessage: {
      type: String,
      default: 'No data available'
    },
    extraClasses: {
      type: [String, Object],
      default: ''
    },
    delay: {
      type: Number,
      default: 0.25
    }
  },
  emits: ['update:modelValue']
}
</script>

<style scoped>
.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-controls {
  display: flex;
  gap: 0.5rem;
  background-color: var(--bg-primary);
  border-radius: var(--radius);
  padding: 0.25rem;
  border: 1px solid var(--border-color);
}

.chart-period-button {
  padding: 0.375rem 0.75rem;
  border: none;
  background: transparent;
  color: var(--text-secondary);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
}

.chart-period-button:hover {
  color: var(--primary);
  background-color: rgba(58, 134, 255, 0.05);
}

.chart-period-button.active {
  color: var(--primary);
  background-color: rgba(58, 134, 255, 0.1);
}

.chart-container {
  min-height: 350px;
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
}

.limited-access-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 2rem;
  color: var(--text-secondary);
  height: 100%;
}

.limited-access-message svg {
  color: var(--text-secondary);
  opacity: 0.5;
}

.limited-access-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.limited-heading {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 1rem;
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

@media (max-width: 768px) {
  .chart-controls {
    flex-wrap: wrap;
  }
}
</style> 