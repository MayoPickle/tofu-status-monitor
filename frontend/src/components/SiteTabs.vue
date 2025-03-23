<template>
  <div class="site-tabs-container">
    <div class="site-tabs">
      <button 
        v-for="site in sites" 
        :key="site.id"
        :class="['site-tab', { active: modelValue === site.id }]"
        @click="$emit('update:modelValue', site.id)"
      >
        {{ site.name }}
        <transition name="pulse" mode="out-in">
          <span 
            v-if="siteStatus[site.id]" 
            class="site-status-indicator"
            :class="{'status-good': siteStatus[site.id] === 'Good', 'status-bad': siteStatus[site.id] === 'Bad'}"
          ></span>
        </transition>
      </button>
      <button v-if="showAddButton" class="site-tab add-site-button" @click="$emit('add')">
        <svg viewBox="0 0 24 24" width="16" height="16" class="add-icon">
          <path fill="currentColor" d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
        </svg>
        Add Site
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SiteTabs',
  props: {
    sites: {
      type: Array,
      required: true
    },
    modelValue: {
      type: String,
      required: true
    },
    siteStatus: {
      type: Object,
      default: () => ({})
    },
    showAddButton: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:modelValue', 'add']
}
</script>

<style scoped>
.site-tabs-container {
  margin-bottom: 1.5rem;
  overflow: hidden;
  border-radius: var(--radius-md);
  background-color: var(--bg-card);
  border: 1px solid var(--border-color);
  box-shadow: var(--shadow-sm);
}

.site-tabs {
  display: flex;
  gap: 0.25rem;
  overflow-x: auto;
  padding: 0.75rem;
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.site-tabs::-webkit-scrollbar {
  display: none;
}

.site-tab {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
}

.site-tab:hover {
  border-color: var(--primary-light);
  color: var(--primary);
  transform: translateY(-1px);
  box-shadow: var(--shadow-sm);
}

.site-tab.active {
  background-color: var(--primary);
  color: white;
  border-color: var(--primary);
  box-shadow: 0 2px 6px rgba(58, 134, 255, 0.3);
}

.site-status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  margin-left: 0.25rem;
}

.status-good {
  background-color: var(--success);
  box-shadow: 0 0 5px var(--success);
}

.status-bad {
  background-color: var(--danger);
  box-shadow: 0 0 5px var(--danger);
}

.add-site-button {
  background-color: var(--bg-secondary);
  border: 1px dashed var(--border-color);
}

.add-icon {
  fill: currentColor;
}

/* Animations */
.pulse-enter-active,
.pulse-leave-active {
  transition: all 0.3s ease;
}

.pulse-enter-from,
.pulse-leave-to {
  transform: scale(0);
  opacity: 0;
}

@media (max-width: 768px) {
  .site-tabs {
    flex-wrap: nowrap;
  }
}
</style> 