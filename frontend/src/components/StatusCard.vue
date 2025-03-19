<template>
  <BaseCard title="Current Status" class="status-card animate-in" :delay="delay">
    <template #header>
      <h2 class="card-title">{{ title }}</h2>
      <div class="badge" :class="statusClass">{{ status }}</div>
    </template>
    
    <div class="status-info">
      <p class="last-checked">
        <svg viewBox="0 0 24 24" width="18" height="18" class="icon">
          <path fill="currentColor" d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z" />
        </svg>
        Last checked: {{ lastChecked }}
      </p>
      <div class="url-info">
        <svg viewBox="0 0 24 24" width="18" height="18" class="icon">
          <path fill="currentColor" d="M16.36,14C16.44,13.34 16.5,12.68 16.5,12C16.5,11.32 16.44,10.66 16.36,10H19.74C19.9,10.64 20,11.31 20,12C20,12.69 19.9,13.36 19.74,14M14.59,19.56C15.19,18.45 15.65,17.25 15.97,16H18.92C17.96,17.65 16.43,18.93 14.59,19.56M14.34,14H9.66C9.56,13.34 9.5,12.68 9.5,12C9.5,11.32 9.56,10.65 9.66,10H14.34C14.43,10.65 14.5,11.32 14.5,12C14.5,12.68 14.43,13.34 14.34,14M12,19.96C11.17,18.76 10.5,17.43 10.09,16H13.91C13.5,17.43 12.83,18.76 12,19.96M8,8H5.08C6.03,6.34 7.57,5.06 9.4,4.44C8.8,5.55 8.35,6.75 8,8M5.08,16H8C8.35,17.25 8.8,18.45 9.4,19.56C7.57,18.93 6.03,17.65 5.08,16M4.26,14C4.1,13.36 4,12.69 4,12C4,11.31 4.1,10.64 4.26,10H7.64C7.56,10.66 7.5,11.32 7.5,12C7.5,12.68 7.56,13.34 7.64,14M12,4.03C12.83,5.23 13.5,6.57 13.91,8H10.09C10.5,6.57 11.17,5.23 12,4.03M18.92,8H15.97C15.65,6.75 15.19,5.55 14.59,4.44C16.43,5.07 17.96,6.34 18.92,8M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
        </svg>
        <span class="url-value">{{ url }}</span>
      </div>
    </div>
  </BaseCard>
</template>

<script>
import BaseCard from './BaseCard.vue'

export default {
  name: 'StatusCard',
  components: {
    BaseCard
  },
  props: {
    title: {
      type: String,
      default: 'Current Status'
    },
    status: {
      type: String,
      default: 'Unknown'
    },
    lastChecked: {
      type: String,
      required: true
    },
    url: {
      type: String,
      required: true
    },
    delay: {
      type: Number,
      default: 0
    }
  },
  computed: {
    statusClass() {
      if (this.status === 'Good') return 'badge-success'
      if (this.status === 'Bad') return 'badge-danger'
      return 'badge-warning'
    }
  }
}
</script>

<style scoped>
.status-info {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.last-checked, .url-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.icon {
  flex-shrink: 0;
  color: var(--text-secondary);
}

.url-value {
  font-family: monospace;
  word-break: break-all;
}

.badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: capitalize;
}

.badge-success {
  background-color: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.badge-danger {
  background-color: rgba(255, 0, 110, 0.1);
  color: var(--danger);
}

.badge-warning {
  background-color: rgba(251, 191, 36, 0.1);
  color: var(--accent);
}
</style> 