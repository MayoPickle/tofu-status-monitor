<template>
  <div class="card">
    <h2>
      <font-awesome-icon :icon="['fas', 'chart-line']" class="card-icon" />
      Weekly Averages
    </h2>
    <div class="chart-container">
      <LineChart 
        v-if="chartData.labels.length" 
        :chartData="chartData"
        :options="chartOptions"
      />
      <p v-else class="no-data">
        <font-awesome-icon :icon="['fas', 'info-circle']" />
        No weekly average data available
      </p>
    </div>
  </div>
</template>

<script>
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js'
import { LineChart } from 'vue-chart-3'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
)

// Import FontAwesome core
import { library } from '@fortawesome/fontawesome-svg-core'
// Import FontAwesome component
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
// Import specific icons
import { faChartLine, faInfoCircle } from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(faChartLine, faInfoCircle)

export default {
  name: 'WeeklyAveragesChart',
  components: {
    LineChart,
    FontAwesomeIcon
  },
  props: {
    weeklyAverages: {
      type: Array,
      required: true
    }
  },
  computed: {
    chartData() {
      return {
        labels: this.weeklyAverages.map(avg => {
          const date = new Date(avg.week_start)
          return `${date.getMonth() + 1}/${date.getDate()}`
        }),
        datasets: [
          {
            label: 'Weekly Average Response Time (ms)',
            backgroundColor: 'rgba(42, 157, 143, 0.2)',
            borderColor: 'rgb(42, 157, 143)',
            data: this.weeklyAverages.map(avg => avg.average_time * 1000), // Convert to ms
            tension: 0.2
          }
        ]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: 'Average Response Time (ms)'
            }
          },
          x: {
            title: {
              display: true,
              text: 'Week Starting'
            }
          }
        }
      }
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

.chart-container {
  height: 400px;
  position: relative;
  margin-bottom: 1.5rem;
  padding: 1rem;
  background-color: var(--bg-body);
  border-radius: var(--radius);
}

.no-data {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  font-style: italic;
}

@media (max-width: 768px) {
  .chart-container {
    height: 300px;
  }
}
</style> 