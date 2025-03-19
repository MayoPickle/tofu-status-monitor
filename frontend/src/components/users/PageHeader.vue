<template>
  <div class="page-header">
    <div class="header-content">
      <h1>User Management</h1>
      <p class="subtitle">Manage user accounts and permissions</p>
    </div>
    
    <button v-if="isAdmin" class="add-user-button" @click="$emit('add-user')">
      <svg viewBox="0 0 24 24" class="button-icon">
        <path d="M15,14C12.33,14 7,15.33 7,18V20H23V18C23,15.33 17.67,14 15,14M6,10V7H4V10H1V12H4V15H6V12H9V10M15,12A4,4 0 0,0 19,8A4,4 0 0,0 15,4A4,4 0 0,0 11,8A4,4 0 0,0 15,12Z" />
      </svg>
      Add New User
    </button>
  </div>
</template>

<script>
export default {
  name: 'PageHeader',
  props: {
    isAdmin: {
      type: Boolean,
      required: true
    }
  },
  emits: ['add-user']
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 