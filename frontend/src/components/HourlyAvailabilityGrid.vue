<template>
  <BaseCard class="hourly-availability-card animate-in" title="24h Availability Grid" :delay="0.2">
    <template #header>
      <div class="card-header">
        <div class="header-content">
          <h2 class="card-title">24-Hour Availability Monitoring</h2>
          <div class="card-subtitle">Displays hourly service status and performance metrics for the past 24 hours</div>
        </div>
        <slot name="header-action">
          <button v-if="showRefresh" class="btn btn-outline btn-sm refresh-btn" @click="$emit('refresh')">
            <svg viewBox="0 0 24 24" width="16" height="16">
              <path fill="currentColor" d="M17.65,6.35C16.2,4.9 14.21,4 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20C15.73,20 18.84,17.45 19.73,14H17.65C16.83,16.33 14.61,18 12,18A6,6 0 0,1 6,12A6,6 0 0,1 12,6C13.66,6 15.14,6.69 16.22,7.78L13,11H20V4L17.65,6.35Z" />
            </svg>
            <span>Refresh</span>
          </button>
        </slot>
      </div>
    </template>
    
    <!-- Summary Statistics -->
    <div class="summary-section">
      <div class="summary-stat-card">
        <div class="summary-icon success-icon">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M12 2C6.5 2 2 6.5 2 12S6.5 22 12 22 22 17.5 22 12 17.5 2 12 2M10 17L5 12L6.41 10.59L10 14.17L17.59 6.58L19 8L10 17Z" />
          </svg>
        </div>
        <div class="summary-content">
          <div class="summary-value" :class="getAvgSuccessRateClass">{{ averageSuccessRate.toFixed(2) }}%</div>
          <div class="summary-label">Avg Success Rate</div>
        </div>
      </div>
      
      <div class="summary-stat-card">
        <div class="summary-icon response-icon">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M12,20A8,8 0 0,0 20,12A8,8 0 0,0 12,4A8,8 0 0,0 4,12A8,8 0 0,0 12,20M12,2A10,10 0 0,1 22,12A10,10 0 0,1 12,22C6.47,22 2,17.5 2,12A10,10 0 0,1 12,2M12.5,7V12.25L17,14.92L16.25,16.15L11,13V7H12.5Z" />
          </svg>
        </div>
        <div class="summary-content">
          <div class="summary-value" :class="getAvgResponseTimeClass">{{ averageResponseTime.toFixed(0) }} ms</div>
          <div class="summary-label">Avg Response Time</div>
        </div>
      </div>
      
      <div class="summary-stat-card">
        <div class="summary-icon requests-icon">
          <svg viewBox="0 0 24 24" width="20" height="20">
            <path fill="currentColor" d="M17,3H7A2,2 0 0,0 5,5V21L12,18L19,21V5C19,3.89 18.1,3 17,3Z" />
          </svg>
        </div>
        <div class="summary-content">
          <div class="summary-value">{{ totalRequests }}</div>
          <div class="summary-label">Total Requests</div>
        </div>
      </div>
    </div>
    
    <!-- 24-Hour Grid -->
    <div class="grid-container">
      <div class="timeline-indicator">
        <div class="timeline-label">Past</div>
        <div class="timeline-line"></div>
        <div class="timeline-label">Now</div>
      </div>
      
      <div class="grid-wrapper">
        <div class="grid-row hour-labels">
          <div class="grid-label">Time</div>
          <div v-for="hour in hourLabels" :key="hour" class="hour-label">
            {{ hour }}
          </div>
        </div>
        
        <div class="grid-row">
          <div 
            class="grid-label" 
            @mouseover="checkTooltipPosition($event, 0)" 
            @mouseleave="hoveredCell = null"
          >Status</div>
          <div
            v-for="(status, index) in hourlyStatus"
            :key="index"
            class="grid-cell"
            :class="getCellClass(status)"
            @mouseover="checkTooltipPosition($event, index + 1)"
            @mouseleave="hoveredCell = null"
          ></div>
        </div>
      </div>
    </div>
    
    <template #footer>
      <div class="grid-footer">
        <div class="legend">
          <h3 class="legend-title">Status Legend</h3>
          <div class="legend-items">
            <div class="legend-item">
              <div class="legend-color status-good-legend"></div>
              <div class="legend-text">Good (Success &gt; 95%, Response &lt; 3000ms)</div>
            </div>
            <div class="legend-item">
              <div class="legend-color status-warning-legend"></div>
              <div class="legend-text">Warning (Success &gt; 95%, Response &gt; 3000ms)</div>
            </div>
            <div class="legend-item">
              <div class="legend-color status-error-legend"></div>
              <div class="legend-text">Error (Success &lt; 95%)</div>
            </div>
            <div class="legend-item">
              <div class="legend-color status-unknown-legend"></div>
              <div class="legend-text">No Data</div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </BaseCard>
  
  <!-- Tooltip portal (outside BaseCard) -->
  <div v-if="hoveredCell !== null" class="tooltip-portal" :style="getTooltipStyle()">
    <div class="cell-tooltip" :class="getTooltipPositionClass(hoveredCell)">
      <template v-if="hoveredCell === 0">
        <div class="tooltip-time">Status Legend</div>
        <div class="tooltip-stats">
          <div class="tooltip-stat">
            <span class="tooltip-label status-good-text">Good:</span>
            <span class="tooltip-value">Success &gt; 95%, Response &lt; 3000ms</span>
          </div>
          <div class="tooltip-stat">
            <span class="tooltip-label status-warning-text">Warning:</span>
            <span class="tooltip-value">Success &gt; 95%, Response &gt; 3000ms</span>
          </div>
          <div class="tooltip-stat">
            <span class="tooltip-label status-error-text">Error:</span>
            <span class="tooltip-value">Success &lt; 95%</span>
          </div>
        </div>
      </template>
      <template v-else>
        <div class="tooltip-time">{{ getTooltipTime(hoveredCell - 1) }}</div>
        <div class="tooltip-stats">
          <div class="tooltip-stat">
            <span class="tooltip-label">Success Rate:</span>
            <span class="tooltip-value" :class="getSuccessRateClass(hourlyStatus[hoveredCell - 1].successRate)">
              {{ hourlyStatus[hoveredCell - 1].successRate.toFixed(1) }}%
            </span>
          </div>
          <div class="tooltip-stat">
            <span class="tooltip-label">Response Time:</span>
            <span class="tooltip-value" :class="getResponseTimeClass(hourlyStatus[hoveredCell - 1].responseTime)">
              {{ hourlyStatus[hoveredCell - 1].responseTime.toFixed(0) }}ms
            </span>
          </div>
          <div class="tooltip-stat">
            <span class="tooltip-label">Requests:</span>
            <span class="tooltip-value">{{ hourlyStatus[hoveredCell - 1].requestCount }}</span>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue';
import BaseCard from './BaseCard.vue';

export default {
  name: 'HourlyAvailabilityGrid',
  components: {
    BaseCard
  },
  props: {
    hourlyData: {
      type: Array,
      default: () => []
    },
    showRefresh: {
      type: Boolean,
      default: true
    }
  },
  setup(props) {
    const currentHour = new Date().getHours();
    const hoveredCell = ref(null);
    const isTooltipBottom = ref(false);
    const cellPosition = ref({ top: 0, left: 0, width: 0, height: 0 });
    
    // Check viewport position on cell hover
    const checkTooltipPosition = (event, index) => {
      // Store the cell index and position
      hoveredCell.value = index;
      
      // Get absolute position of the cell
      const cellRect = event.target.getBoundingClientRect();
      
      // Store cell position for tooltip positioning
      cellPosition.value = {
        top: cellRect.top + window.scrollY,
        left: cellRect.left + window.scrollX,
        width: cellRect.width,
        height: cellRect.height,
        centerX: cellRect.left + (cellRect.width / 2),
        centerY: cellRect.top + (cellRect.height / 2)
      };
      
      // If cell is close to the top of the viewport, show tooltip below
      if (cellRect.top < 150) {
        isTooltipBottom.value = true;
      } else {
        isTooltipBottom.value = false;
      }
    };
    
    // Get tooltip style for positioning
    const getTooltipStyle = () => {
      if (!hoveredCell.value) return {};
      
      // Fixed tooltip width and height for calculations
      const tooltipWidth = 180;
      const tooltipHeight = hoveredCell.value === 0 ? 150 : 130; // Different height for status tooltip
      const verticalGap = 12; // Gap between tooltip and cell
      
      // Calculate position based on the grid cell's position
      const style = {
        position: 'fixed',
        zIndex: 9999,
        pointerEvents: 'none'
      };
      
      const cell = cellPosition.value;
      const index = hoveredCell.value;
      
      // Special handling for leftmost cell (which is the grid-label with text "Status")
      if (index === 0) {
        // Position tooltip to the right of the cell for leftmost cell
        style.left = `${cell.left + cell.width + 5}px`;
        style.top = `${cell.top - tooltipHeight / 2 + cell.height / 2}px`;
        // Add special class
        style['--is-leftmost'] = 'true';
        return style;
      }
      
      // Center position
      let xPos = cell.centerX - (tooltipWidth / 2);
      
      // Ensure tooltip stays within viewport horizontally
      if (xPos < 10) {
        xPos = 10; // Left edge padding
      } else if (xPos + tooltipWidth > window.innerWidth - 10) {
        xPos = window.innerWidth - tooltipWidth - 10; // Right edge padding
      }
      
      style.left = `${xPos}px`;
      
      // Calculate arrow position offset
      // This positions the arrow directly under the cell center
      const arrowPosition = Math.min(
        Math.max(cell.centerX - xPos, 20), // At least 20px from left edge
        tooltipWidth - 20 // At most 20px from right edge
      );
      
      style['--arrow-left-pos'] = `${arrowPosition}px`;
      
      // Vertical positioning with fixed offset
      if (isTooltipBottom.value) {
        // Position tooltip below the cell with a fixed distance
        style.top = `${cell.top + cell.height + verticalGap}px`;
      } else {
        // Position tooltip above the cell with a fixed distance
        style.top = `${cell.top - tooltipHeight - verticalGap}px`;
      }
      
      return style;
    };
    
    // Generate hour labels (current hour at rightmost position)
    const hourLabels = computed(() => {
      const labels = [];
      for (let i = 23; i >= 0; i--) {
        const hour = (currentHour - i + 24) % 24;
        labels.push(hour.toString().padStart(2, '0'));
      }
      return labels;
    });
    
    // Process hourly status data
    const hourlyStatus = computed(() => {
      if (!props.hourlyData || props.hourlyData.length === 0) {
        // Generate mock data if no data provided
        return Array(24).fill(0).map((_, index) => {
          // Generate random data for demo
          const successRate = Math.random() * 10 + 90; // 90-100%
          const responseTime = Math.random() * 5000; // 0-5000ms
          
          return {
            hour: (currentHour - 23 + index + 24) % 24,
            successRate,
            responseTime,
            requestCount: Math.floor(Math.random() * 200 + 50)
          };
        });
      }
      
      // Map actual data if provided
      return Array(24).fill(null).map((_, index) => {
        const hour = (currentHour - 23 + index + 24) % 24;
        const hourData = props.hourlyData.find(data => data.hour === hour);
        
        if (hourData) {
          return hourData;
        }
        
        return {
          hour,
          successRate: 0,
          responseTime: 0,
          requestCount: 0
        };
      });
    });
    
    // Calculate total requests
    const totalRequests = computed(() => {
      return hourlyStatus.value.reduce((sum, item) => sum + item.requestCount, 0);
    });
    
    // Calculate average metrics
    const averageSuccessRate = computed(() => {
      const validData = hourlyStatus.value.filter(item => item.requestCount > 0);
      if (validData.length === 0) return 0;
      
      const sum = validData.reduce((acc, item) => acc + item.successRate, 0);
      return sum / validData.length;
    });
    
    const averageResponseTime = computed(() => {
      const validData = hourlyStatus.value.filter(item => item.requestCount > 0);
      if (validData.length === 0) return 0;
      
      const sum = validData.reduce((acc, item) => acc + item.responseTime, 0);
      return sum / validData.length;
    });
    
    // Class for average success rate
    const getAvgSuccessRateClass = computed(() => {
      if (averageSuccessRate.value >= 99) return 'excellent';
      if (averageSuccessRate.value >= 97) return 'good';
      if (averageSuccessRate.value >= 95) return 'average';
      return 'poor';
    });
    
    // Class for average response time
    const getAvgResponseTimeClass = computed(() => {
      if (averageResponseTime.value < 100) return 'excellent';
      if (averageResponseTime.value < 500) return 'good';
      if (averageResponseTime.value < 3000) return 'average';
      return 'poor';
    });
    
    // Get success rate class for tooltip
    const getSuccessRateClass = (rate) => {
      if (rate >= 99) return 'excellent';
      if (rate >= 97) return 'good';
      if (rate >= 95) return 'average';
      return 'poor';
    };
    
    // Get response time class for tooltip
    const getResponseTimeClass = (time) => {
      if (time < 100) return 'excellent';
      if (time < 500) return 'good';
      if (time < 3000) return 'average';
      return 'poor';
    };
    
    // Get cell status class based on success rate and response time
    const getCellClass = (status) => {
      if (!status || status.requestCount === 0) {
        return 'status-unknown';
      }
      
      if (status.successRate < 95) {
        return 'status-error';
      }
      
      if (status.responseTime > 3000) {
        return 'status-warning';
      }
      
      return 'status-good';
    };
    
    // Format hour for tooltip
    const getTooltipTime = (index) => {
      const hour = hourlyStatus.value[index].hour;
      return `${hour.toString().padStart(2, '0')}:00 - ${(hour + 1) % 24}:00`;
    };
    
    // Get tooltip position class for edge handling
    const getTooltipPositionClass = (index) => {
      // Combine horizontal and vertical positioning
      let positionClass = '';
      
      // Special case for leftmost cell
      if (index === 0) {
        return 'tooltip-leftmost';
      }
      
      // Horizontal positioning
      if (index < 3) {
        positionClass += ' tooltip-right';
      } else if (index > 20) {
        positionClass += ' tooltip-left';
      }
      
      // Vertical positioning
      if (isTooltipBottom.value) {
        positionClass += ' tooltip-bottom';
      }
      
      return positionClass;
    };
    
    return {
      hourLabels,
      hourlyStatus,
      hoveredCell,
      getCellClass,
      getTooltipTime,
      averageSuccessRate,
      averageResponseTime,
      getAvgSuccessRateClass,
      getAvgResponseTimeClass,
      getSuccessRateClass,
      getResponseTimeClass,
      totalRequests,
      getTooltipPositionClass,
      checkTooltipPosition,
      isTooltipBottom,
      getTooltipStyle,
      cellPosition
    };
  }
};
</script>

<style scoped>
.hourly-availability-card {
  overflow: visible;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background-color: white;
  width: 100%;
  max-width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  background-color: #f9fafb;
}

.header-content {
  flex: 1;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.card-subtitle {
  font-size: 0.85rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

/* Summary Statistics Cards */
.summary-section {
  display: flex;
  flex-wrap: wrap;
  gap: 1.25rem;
  padding: 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  background-color: #fcfcfd;
}

.summary-stat-card {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem;
  border-radius: 0.5rem;
  background-color: white;
  border: 1px solid #f3f4f6;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  min-width: 180px;
  flex: 1;
}

.summary-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #f3f4f6;
  color: #4b5563;
}

.success-icon {
  background-color: rgba(34, 197, 94, 0.1);
  color: #22c55e;
}

.response-icon {
  background-color: rgba(59, 130, 246, 0.1);
  color: #3b82f6;
}

.requests-icon {
  background-color: rgba(99, 102, 241, 0.1);
  color: #6366f1;
}

.summary-content {
  display: flex;
  flex-direction: column;
}

.summary-value {
  font-size: 1.5rem;
  font-weight: 700;
  color: #111827;
  line-height: 1.2;
}

.summary-label {
  font-size: 0.85rem;
  color: #6b7280;
  margin-top: 0.25rem;
}

/* Grid Container */
.grid-container {
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.timeline-indicator {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  width: 100%;
}

.timeline-label {
  font-size: 0.75rem;
  color: #6b7280;
  font-weight: 500;
}

.timeline-line {
  flex: 1;
  height: 2px;
  background: linear-gradient(to right, #e5e7eb, #9ca3af);
  margin: 0 0.5rem;
}

.grid-wrapper {
  width: 100%;
  overflow-x: auto;
  padding-bottom: 0.5rem;
}

.grid-row {
  display: flex;
  align-items: center;
  margin-bottom: 0.75rem;
  flex-wrap: nowrap;
  width: 100%;
}

.grid-label {
  width: 60px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #4b5563;
  flex-shrink: 0;
  text-align: right;
  padding-right: 1rem;
  cursor: pointer;
  transition: color 0.2s ease;
}

.grid-label:hover {
  color: #2563eb;
}

.hour-labels {
  margin-bottom: 0.5rem;
}

.hour-label {
  flex: 1;
  min-width: 30px;
  height: 20px;
  font-size: 0.7rem;
  color: #6b7280;
  text-align: center;
  margin: 0 1px;
}

.grid-cell {
  flex: 1;
  min-width: 30px;
  height: 34px;
  border-radius: 6px;
  margin: 0 1px;
  position: relative;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.grid-cell:hover {
  transform: translateY(-3px);
  z-index: 999;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* Status Colors - Using hardcoded values instead of CSS variables */
.status-good {
  background-color: #22c55e; /* Green */
  border: 1px solid rgba(34, 197, 94, 0.5);
}

.status-warning {
  background-color: #f59e0b; /* Yellow */
  border: 1px solid rgba(245, 158, 11, 0.5);
}

.status-error {
  background-color: #ef4444; /* Red */
  border: 1px solid rgba(239, 68, 68, 0.5);
}

.status-unknown {
  background-color: #e5e7eb; /* Light gray */
  border: 1px dashed #9ca3af; /* Gray dashed border */
}

/* Legend Colors */
.status-good-legend {
  background-color: #22c55e; /* Green */
  border: 1px solid rgba(34, 197, 94, 0.5);
}

.status-warning-legend {
  background-color: #f59e0b; /* Yellow */
  border: 1px solid rgba(245, 158, 11, 0.5);
}

.status-error-legend {
  background-color: #ef4444; /* Red */
  border: 1px solid rgba(239, 68, 68, 0.5);
}

.status-unknown-legend {
  background-color: #e5e7eb; /* Light gray */
  border: 1px dashed #9ca3af; /* Gray dashed border */
}

/* Tooltip Portal */
.tooltip-portal {
  position: fixed;
  z-index: 9999;
  pointer-events: none;
}

/* Tooltip */
.cell-tooltip {
  position: relative;
  width: 180px;
  background-color: white;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.75rem;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
  z-index: 9999;
  pointer-events: none;
  --arrow-left-pos: 90px; /* Default centered arrow */
}

/* Arrow for tooltip */
.cell-tooltip::after {
  content: '';
  position: absolute;
  border-width: 8px;
  border-style: solid;
}

/* Default arrow (pointing down) */
.cell-tooltip:not(.tooltip-bottom):not(.tooltip-leftmost)::after {
  top: 100%;
  left: var(--arrow-left-pos);
  transform: translateX(-50%);
  border-color: white transparent transparent transparent;
}

/* Bottom tooltip arrow (pointing up) */
.tooltip-bottom:not(.tooltip-leftmost)::after {
  bottom: 100%;
  left: var(--arrow-left-pos);
  transform: translateX(-50%);
  border-color: transparent transparent white transparent;
}

/* Leftmost tooltip arrow (pointing left) */
.tooltip-leftmost::after {
  top: 50%;
  left: -16px;
  transform: translateY(-50%);
  border-color: transparent white transparent transparent;
}

/* Tooltip content */
.tooltip-time {
  font-weight: 600;
  font-size: 0.85rem;
  margin-bottom: 0.75rem;
  color: #111827;
  text-align: center;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #f3f4f6;
}

.tooltip-stats {
  font-size: 0.8rem;
  color: #4b5563;
  line-height: 1.5;
}

.tooltip-stat {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.25rem;
}

.tooltip-label {
  color: #6b7280;
}

.tooltip-value {
  font-weight: 600;
  color: #111827;
}

/* Footer */
.grid-footer {
  border-top: 1px solid #e5e7eb;
  padding: 1.25rem 1.5rem;
  background-color: #f9fafb;
}

/* Legend */
.legend-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #4b5563;
  margin: 0 0 0.75rem 0;
}

.legend-items {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  font-size: 0.8rem;
  color: #4b5563;
  margin-right: 1rem;
}

.legend-color {
  width: 16px;
  height: 16px;
  margin-right: 0.5rem;
  border-radius: 4px;
  flex-shrink: 0;
}

/* Status text colors */
.status-good-text {
  color: #22c55e;
  font-weight: 600;
}

.status-warning-text {
  color: #f59e0b;
  font-weight: 600;
}

.status-error-text {
  color: #ef4444;
  font-weight: 600;
}

.status-unknown-text {
  color: #9ca3af;
  font-weight: 600;
}

/* Status colors in metrics */
.excellent {
  color: #16a34a;
}

.good {
  color: #2563eb;
}

.average {
  color: #d97706;
}

.poor {
  color: #dc2626;
}

.refresh-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-weight: 500;
  background-color: white;
  border: 1px solid #e5e7eb;
  color: #4b5563;
  padding: 0.375rem 0.75rem;
  font-size: 0.85rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background-color: #f9fafb;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  transform: translateY(-1px);
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.85rem;
  border-radius: 6px;
}

@media (max-width: 1024px) {
  .summary-section {
    gap: 1rem;
  }
  
  .summary-stat-card {
    min-width: 150px;
  }
}

@media (max-width: 768px) {
  .summary-section {
    flex-direction: column;
    padding: 1rem;
  }
  
  .summary-stat-card {
    width: 100%;
  }
  
  .card-header {
    padding: 1rem;
  }
  
  .grid-container {
    padding: 1rem;
  }
  
  .legend-items {
    flex-direction: column;
    gap: 0.75rem;
  }
}

@media (max-width: 480px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  
  .refresh-btn {
    width: 100%;
    justify-content: center;
    margin-top: 0.5rem;
  }
  
  .grid-container {
    padding: 1rem 0.5rem;
  }
  
  .grid-footer {
    padding: 1rem;
  }
}
</style> 