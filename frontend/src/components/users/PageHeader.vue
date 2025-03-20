<template>
  <div class="page-header">
    <div class="header-content">
      <h1>User Management</h1>
      <p class="subtitle">Manage user accounts and permissions</p>
    </div>
    
    <div v-if="isAdmin" class="header-actions">
      <button class="migrate-button" @click="$emit('migrate-permissions')" :disabled="isMigrating">
        <svg viewBox="0 0 24 24" class="button-icon">
          <path d="M12,5.5L10,8H14L12,5.5M18,10H6L2,22H22L18,10M15,16H9L10.4,12H13.6L15,16Z" />
        </svg>
        {{ isMigrating ? 'Migrating...' : 'Migrate Permissions' }}
      </button>
      
      <button class="add-user-button" @click="$emit('add-user')">
        <svg viewBox="0 0 24 24" class="button-icon">
          <path d="M15,14C12.33,14 7,15.33 7,18V20H23V18C23,15.33 17.67,14 15,14M6,10V7H4V10H1V12H4V15H6V12H9V10M15,12A4,4 0 0,0 19,8A4,4 0 0,0 15,4A4,4 0 0,0 11,8A4,4 0 0,0 15,12Z" />
        </svg>
        Add New User
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PageHeader',
  props: {
    isAdmin: {
      type: Boolean,
      required: true
    },
    isMigrating: {
      type: Boolean,
      default: false
    }
  },
  emits: ['add-user', 'migrate-permissions']
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';

.header-actions {
  display: flex;
  gap: 1rem;
}

.migrate-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.75rem;
  background-color: var(--accent);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(232, 126, 4, 0.1);
}

.migrate-button:hover:not(:disabled) {
  background-color: var(--accent-dark, #e67e22);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(232, 126, 4, 0.2);
}

.migrate-button:disabled {
  background-color: var(--gray);
  cursor: not-allowed;
  opacity: 0.7;
}

@media (max-width: 768px) {
  .header-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .migrate-button,
  .add-user-button {
    width: 100%;
  }
}
</style> 