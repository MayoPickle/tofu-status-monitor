<template>
  <div class="dashboard-header">
    <div class="dashboard-title">
      <h1>Service Monitor</h1>
      <div class="text-secondary">
        Current Status: <span :class="connectionStatusClass">{{ connectionStatusText }}</span>
        <button v-if="connectionStatus === 'disconnected'" @click="retryConnection" class="btn btn-sm btn-primary">
          Reconnect
        </button>
      </div>
    </div>
    <div class="user-info">
      <div class="connection-status" v-if="error">
        <div class="alert alert-warning">{{ error }}</div>
      </div>
      <div class="user-profile">
        <span>{{ currentUser ? currentUser.username : 'Guest' }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'DashboardHeader',
  props: {
    connectionStatus: {
      type: String,
      required: true
    },
    connectionStatusText: {
      type: String,
      required: true
    },
    error: {
      type: String,
      default: null
    },
    currentUser: {
      type: Object,
      default: null
    }
  },
  computed: {
    connectionStatusClass() {
      switch (this.connectionStatus) {
        case 'connected': return 'text-success';
        case 'reconnecting': return 'text-warning';
        case 'disconnected': return 'text-danger';
        default: return '';
      }
    }
  },
  methods: {
    retryConnection() {
      this.$emit('retry-connection');
    }
  }
}
</script>

<style scoped>
/* Styles moved to dashboard-styles.css */
</style> 