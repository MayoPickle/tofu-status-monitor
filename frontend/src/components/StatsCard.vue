<template>
  <BaseCard class="stats-card animate-in" :title="title" :delay="delay">
    <template #header>
      <h2 class="card-title">{{ title }}</h2>
      <slot name="header-action">
        <button v-if="showRefresh" class="btn btn-outline btn-sm refresh-btn" @click="$emit('refresh')">
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path fill="currentColor" d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" />
          </svg>
          Refresh
        </button>
      </slot>
    </template>
    
    <div class="stats-grid">
      <div 
        v-for="(stat, index) in stats" 
        :key="index" 
        class="stat-item animate-in" 
        :style="getStatDelay(index)"
      >
        <div class="stat-value" :class="stat.class">{{ stat.value }}</div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>
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
    }
  },
  methods: {
    getStatDelay(index) {
      return { '--delay': `${this.delay + 0.05 + (index * 0.05)}s` }
    }
  }
}
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.25rem;
}

.stat-item {
  text-align: center;
  padding: 1rem;
  border-radius: var(--radius);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  transition: var(--transition);
}

.stat-item:hover {
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.stat-value {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
}

.stat-label {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: 1fr;
  }
}
</style> 