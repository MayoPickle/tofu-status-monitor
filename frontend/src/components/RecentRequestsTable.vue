<template>
  <div class="card">
    <h2>
      <font-awesome-icon :icon="['fas', 'history']" class="card-icon" />
      Recent Requests
    </h2>
    <div class="table-wrapper">
      <table class="metrics-table">
        <thead>
          <tr>
            <th>
              <font-awesome-icon :icon="['fas', 'clock']" />
              Time
            </th>
            <th>
              <font-awesome-icon :icon="['fas', 'server']" />
              Status
            </th>
            <th>
              <font-awesome-icon :icon="['fas', 'tachometer-alt']" />
              Response Time
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="metric in metrics" :key="metric.id" :class="{ 'error-row': !isSuccessful(metric) }">
            <td class="timestamp">{{ formatDate(metric.timestamp) }}</td>
            <td>
              <span class="status-cell" :class="isSuccessful(metric) ? 'success' : 'error'">
                <font-awesome-icon :icon="getStatusIcon(metric)" class="status-icon" />
                {{ metric.status_code }}
              </span>
            </td>
            <td class="response-time">{{ formatResponseTime(metric.request_time) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
// Import FontAwesome core
import { library } from '@fortawesome/fontawesome-svg-core'
// Import FontAwesome component
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// Import specific icons
import { 
  faHistory, 
  faClock,
  faServer,
  faTachometerAlt,
  faCheckCircle,
  faTimesCircle
} from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(
  faHistory, 
  faClock,
  faServer,
  faTachometerAlt,
  faCheckCircle,
  faTimesCircle
)

export default {
  name: 'RecentRequestsTable',
  components: {
    FontAwesomeIcon
  },
  props: {
    metrics: {
      type: Array,
      required: true
    }
  },
  methods: {
    formatDate(timestamp) {
      return new Date(timestamp).toLocaleString()
    },
    formatResponseTime(time) {
      if (time < 0) return 'Error'
      return `${(time * 1000).toFixed(2)} ms`
    },
    isSuccessful(metric) {
      return metric.status_code >= 200 && metric.status_code < 300
    },
    getStatusIcon(metric) {
      return this.isSuccessful(metric) ? ['fas', 'check-circle'] : ['fas', 'times-circle']
    }
  }
}
</script>

<style scoped>
.card {
  background: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  padding: 1.5rem;
  margin-bottom: 1.5rem;
  border: 1px solid var(--border-color);
  transition: var(--transition);
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, var(--primary) 0%, var(--primary-light) 100%);
  opacity: 0;
  transition: var(--transition);
}

.card:hover::before {
  opacity: 1;
}

.card h2 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-icon {
  color: var(--primary);
  margin-right: 0.5rem;
}

.metrics-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.875rem;
}

.metrics-table th {
  text-align: left;
  padding: 1rem;
  background-color: var(--bg-body);
  border-bottom: 2px solid var(--border-color);
  font-weight: 600;
  color: var(--text-primary);
  position: sticky;
  top: 0;
  z-index: 10;
}

.metrics-table td {
  padding: 1rem;
  border-bottom: 1px solid var(--border-color);
  color: var(--text-primary);
  transition: var(--transition);
}

.metrics-table tr {
  transition: var(--transition);
}

.metrics-table tr:hover {
  background-color: var(--bg-body);
}

.metrics-table tr.error-row {
  background-color: rgba(231, 111, 81, 0.05);
}

.metrics-table tr.error-row:hover {
  background-color: rgba(231, 111, 81, 0.1);
}

.table-wrapper {
  max-height: 500px;
  overflow-y: auto;
  border-radius: var(--radius);
  background-color: var(--bg-secondary);
  scrollbar-width: thin;
  scrollbar-color: var(--primary) var(--bg-secondary);
}

.table-wrapper::-webkit-scrollbar {
  width: 8px;
}

.table-wrapper::-webkit-scrollbar-track {
  background: var(--bg-secondary);
}

.table-wrapper::-webkit-scrollbar-thumb {
  background-color: var(--primary);
  border-radius: 4px;
}

.status-cell {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius);
  font-weight: 500;
  font-size: 0.875rem;
}

.status-cell.success {
  background-color: rgba(82, 183, 136, 0.1);
  color: var(--success);
}

.status-cell.error {
  background-color: rgba(231, 111, 81, 0.1);
  color: var(--danger);
}

.status-icon {
  margin-right: 0.5rem;
}

.response-time {
  font-family: 'Menlo', 'Monaco', 'Consolas', monospace;
  font-size: 0.875rem;
  color: var(--text-primary);
}

.timestamp {
  color: var(--text-secondary);
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .metrics-table th,
  .metrics-table td {
    padding: 0.75rem;
  }
}
</style> 