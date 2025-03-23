<template>
  <div class="metrics-header">
    <div class="title-section">
      <h1>Detailed Metrics</h1>
      <p class="subtitle">Performance analysis and monitoring statistics</p>
    </div>
    <div class="metrics-actions">
      <div class="refresh-info">
        <font-awesome-icon :icon="['fas', 'sync-alt']" class="refresh-icon" />
        <span class="refresh-text">Auto-refreshing every 60s</span>
      </div>
    </div>
  </div>
</template>

<script>
// Import FontAwesome core
import { library } from '@fortawesome/fontawesome-svg-core'
// Import FontAwesome component
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// Import specific icons
import { faSyncAlt } from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(faSyncAlt)

export default {
  name: 'MetricsHeader',
  components: {
    FontAwesomeIcon
  }
}
</script>

<style scoped>
.metrics-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.title-section {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.title-section h1 {
  font-size: 1.75rem;
  font-weight: 700;
  background: linear-gradient(120deg, var(--primary) 0%, var(--primary-light) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin: 0;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 0.875rem;
  margin: 0;
}

.metrics-actions {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.refresh-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0.75rem;
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  border: 1px solid var(--border-color);
  font-size: 0.75rem;
  color: var(--text-secondary);
}

.refresh-icon {
  font-size: 1rem;
  animation: rotate 2s linear infinite;
  display: inline-block;
  color: var(--primary);
}

.refresh-text {
  font-weight: 500;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .metrics-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .metrics-actions {
    width: 100%;
  }

  .refresh-info {
    width: 100%;
    justify-content: center;
  }
}
</style> 