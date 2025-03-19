<template>
  <div>
    <div v-if="loading" class="loading-indicator">
      <font-awesome-icon :icon="['fas', 'circle-notch']" spin class="spinner" />
      <p class="loading-text">Loading metrics data...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <font-awesome-icon :icon="['fas', 'exclamation-triangle']" class="error-icon" />
      {{ error }}
    </div>
    
    <slot v-else></slot>
  </div>
</template>

<script>
// Import FontAwesome core
import { library } from '@fortawesome/fontawesome-svg-core'
// Import FontAwesome component
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// Import specific icons
import { faCircleNotch, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(faCircleNotch, faExclamationTriangle)

export default {
  name: 'LoadingError',
  components: {
    FontAwesomeIcon
  },
  props: {
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: [String, null],
      default: null
    }
  }
}
</script>

<style scoped>
.loading-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  gap: 1rem;
}

.spinner {
  font-size: 2rem;
  color: var(--primary);
}

.loading-text {
  color: var(--text-secondary);
  font-size: 0.875rem;
  font-weight: 500;
}

.error {
  color: var(--danger);
  background-color: rgba(231, 111, 81, 0.1);
  padding: 1.25rem;
  border-radius: var(--radius);
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  border: 1px solid rgba(231, 111, 81, 0.2);
}

.error-icon {
  color: var(--danger);
  font-size: 1.25rem;
  margin-right: 0.5rem;
}
</style> 