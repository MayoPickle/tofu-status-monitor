<template>
  <div class="mobile-user-card">
    <div class="mobile-card-header">
      <div class="mobile-user-info">
        <div class="user-avatar">{{ getUserInitials(user.name || user.username) }}</div>
        <div>
          <h3 class="mobile-user-name">{{ user.name || user.username }}</h3>
          <span class="role-badge" :class="user.role">{{ user.role }}</span>
        </div>
      </div>
      <div class="mobile-actions">
        <button class="action-button edit" @click="$emit('edit', user)" title="Edit User">
          <svg viewBox="0 0 24 24">
            <path d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
          </svg>
        </button>
        <button class="action-button delete" @click="$emit('delete', user)" title="Delete User">
          <svg viewBox="0 0 24 24">
            <path d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
          </svg>
        </button>
      </div>
    </div>
    <div class="mobile-card-body">
      <div class="mobile-detail-item">
        <span class="mobile-label">Username:</span>
        <span class="mobile-value">{{ user.username }}</span>
      </div>
      <div class="mobile-detail-item">
        <span class="mobile-label">Email:</span>
        <span class="mobile-value">{{ user.email }}</span>
      </div>
      <div class="mobile-detail-item">
        <span class="mobile-label">Sites:</span>
        <div class="mobile-site-permissions">
          <div v-if="user.sitePermissions && Object.keys(user.sitePermissions).length > 0">
            <div v-for="(permissions, siteId) in user.sitePermissions" 
                  :key="siteId" 
                  class="site-permission-item">
              <span class="site-badge">{{ getSiteName(siteId) }}</span>
              <div class="site-permissions-list">
                <span v-for="permission in permissions" 
                      :key="permission" 
                      class="permission-badge">
                  {{ formatPermission(permission) }}
                </span>
              </div>
            </div>
          </div>
          <span v-else class="no-sites-message">No sites assigned</span>
          <button 
            class="assign-sites-button"
            @click="$emit('assign-sites', user)">
            <svg viewBox="0 0 24 24" class="button-icon">
              <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
            </svg>
            Manage Sites
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { SITE_PERMISSIONS } from '@/store/userStore'

const PERMISSION_LABELS = {
  [SITE_PERMISSIONS.SITE_VIEW]: 'View',
  [SITE_PERMISSIONS.SITE_VIEW_METRICS]: 'View Metrics',
  [SITE_PERMISSIONS.SITE_CONFIGURE]: 'Configure',
  [SITE_PERMISSIONS.SITE_ADD]: 'Add',
  [SITE_PERMISSIONS.SITE_EDIT]: 'Edit',
  [SITE_PERMISSIONS.SITE_DELETE]: 'Delete'
}

export default {
  name: 'UserCard',
  props: {
    user: {
      type: Object,
      required: true
    },
    monitoredSites: {
      type: Array,
      required: true
    }
  },
  emits: ['edit', 'delete', 'assign-sites'],
  methods: {
    getUserInitials(name) {
      if (!name) return '?'
      return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .substring(0, 2)
    },
    getSiteName(siteId) {
      const site = this.monitoredSites.find(site => site.id === siteId)
      return site ? site.name : siteId
    },
    canAssignSites(user) {
      return user.role !== 'admin' && user.role !== 'maintainer'
    },
    formatPermission(permission) {
      return PERMISSION_LABELS[permission] || permission.replace('site_', '').replace('_', ' ')
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 