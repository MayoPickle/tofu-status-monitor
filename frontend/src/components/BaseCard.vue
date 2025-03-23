<template>
  <div class="card" :class="classes" :style="animationStyle">
    <div class="card-header" v-if="$slots.header || title">
      <slot name="header">
        <h2 class="card-title">{{ title }}</h2>
      </slot>
    </div>
    <div class="card-body">
      <slot></slot>
    </div>
    <div class="card-footer" v-if="$slots.footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseCard',
  props: {
    title: {
      type: String,
      default: ''
    },
    classes: {
      type: [String, Object, Array],
      default: ''
    },
    delay: {
      type: Number,
      default: 0
    },
    animateIn: {
      type: Boolean,
      default: true
    }
  },
  computed: {
    animationStyle() {
      if (!this.animateIn) return {}
      return { '--delay': `${this.delay}s` }
    }
  }
}
</script>

<style scoped>
.card {
  border-radius: var(--radius-md);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  background-color: var(--bg-card);
  transition: var(--transition);
  overflow: hidden;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-body {
  padding: 1.25rem;
}

.card-footer {
  padding: 1.25rem;
  border-top: 1px solid var(--border-color);
}

.card.animate-in {
  animation: fadeIn 0.5s ease forwards;
  opacity: 0;
  transform: translateY(10px);
  animation-delay: var(--delay, 0s);
}

@keyframes fadeIn {
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (max-width: 480px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
}
</style> 