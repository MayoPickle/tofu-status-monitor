<template>
  <BaseCard class="uptime-card animate-in" :title="title" :delay="delay">
    <template #header>
      <h2 class="card-title">{{ title }}</h2>
      <div class="uptime-indicator" :class="indicatorClass"></div>
    </template>
    
    <div class="uptime-stats">
      <div v-for="(item, index) in uptimeItems" :key="index" class="uptime-item">
        <div class="uptime-label">{{ item.label }}</div>
        <div class="uptime-value" :class="getUptimeClass(item.value)">{{ item.value }}%</div>
        <div class="uptime-bar">
          <div 
            class="uptime-progress" 
            :style="{ width: item.value + '%' }" 
            :class="getUptimeClass(item.value)"
          ></div>
        </div>
      </div>
    </div>
  </BaseCard>
</template>

<script>
import BaseCard from './BaseCard.vue'

export default {
  name: 'UptimeCard',
  components: {
    BaseCard
  },
  props: {
    title: {
      type: String,
      default: 'Uptime'
    },
    uptimeItems: {
      type: Array,
      required: true,
      validator: (items) => {
        return items.every(item => 
          typeof item.label !== 'undefined' && 
          typeof item.value !== 'undefined'
        )
      }
    },
    delay: {
      type: Number,
      default: 0.15
    }
  },
  computed: {
    indicatorClass() {
      const firstItem = this.uptimeItems[0]
      if (!firstItem) return ''
      return this.getUptimeClass(firstItem.value)
    }
  },
  methods: {
    getUptimeClass(value) {
      const numValue = parseFloat(value)
      if (numValue >= 99.9) return 'excellent'
      if (numValue >= 99.0) return 'good'
      if (numValue >= 98.0) return 'average'
      return 'poor'
    }
  }
}
</script>

<style scoped>
.uptime-card :deep(.card-header) {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.uptime-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.uptime-stats {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.uptime-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.uptime-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-weight: 500;
}

.uptime-value {
  font-size: 1.25rem;
  font-weight: 600;
}

.uptime-bar {
  width: 100%;
  height: 6px;
  background-color: var(--gray-light);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.uptime-progress {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width 0.5s ease;
}

/* Status Colors */
.excellent {
  color: var(--success);
}

.good {
  color: var(--success);
}

.average {
  color: var(--accent);
}

.poor {
  color: var(--danger);
}

.uptime-progress.excellent, 
.uptime-progress.good {
  background-color: var(--success);
}

.uptime-progress.average {
  background-color: var(--accent);
}

.uptime-progress.poor {
  background-color: var(--danger);
}

.uptime-indicator.excellent, 
.uptime-indicator.good {
  background-color: var(--success);
  box-shadow: 0 0 5px var(--success);
}

.uptime-indicator.average {
  background-color: var(--accent);
  box-shadow: 0 0 5px var(--accent);
}

.uptime-indicator.poor {
  background-color: var(--danger);
  box-shadow: 0 0 5px var(--danger);
}
</style> 