<template>
  <div>
    <div v-if="error" class="error-message">
      <svg viewBox="0 0 24 24" class="error-icon">
        <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
      </svg>
      <span>{{ error }}</span>
    </div>
    
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <span>Loading users...</span>
    </div>
    
    <div v-else class="mobile-cards">
      <user-card
        v-for="user in filteredUsers"
        :key="user.id"
        :user="user"
        :monitored-sites="monitoredSites"
        @edit="$emit('edit', user)"
        @delete="$emit('delete', user)"
        @assign-sites="$emit('assign-sites', user)"
      />
    </div>
  </div>
</template>

<script>
import UserCard from './UserCard.vue'

export default {
  name: 'UsersList',
  components: {
    UserCard
  },
  props: {
    filteredUsers: {
      type: Array,
      required: true
    },
    monitoredSites: {
      type: Array,
      required: true
    },
    loading: {
      type: Boolean,
      default: false
    },
    error: {
      type: String,
      default: null
    }
  },
  emits: ['edit', 'delete', 'assign-sites']
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 