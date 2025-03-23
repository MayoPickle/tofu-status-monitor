<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal assign-sites-modal">
      <div class="modal-header">
        <h3>Manage Site Permissions for {{ userName }}</h3>
        <button class="close-button" @click="$emit('close')">×</button>
      </div>
      <div class="modal-body">
        <div class="site-permissions-container">
          <div v-for="site in monitoredSites" :key="site.id" class="site-permissions-card">
            <div class="site-header">
              <input 
                type="checkbox" 
                :id="'site-' + site.id" 
                :checked="isSiteSelected(site.id)"
                @change="toggleSite(site.id, $event)"
              >
              <label :for="'site-' + site.id">{{ site.name }}</label>
            </div>
            
            <div v-if="isSiteSelected(site.id)" class="permissions-list">
              <div v-for="(label, permission) in permissionLabels" :key="permission" class="permission-item">
                <input 
                  type="checkbox" 
                  :id="`${site.id}-${permission}`" 
                  :checked="hasPermission(site.id, permission)"
                  @change="togglePermission(site.id, permission, $event)"
                >
                <label :for="`${site.id}-${permission}`">{{ label }}</label>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="cancel-button" @click="$emit('close')">Cancel</button>
        <button class="save-button" @click="$emit('save', sitePermissions)">
          Save Permissions
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, reactive, watch } from 'vue'
import { SITE_PERMISSIONS } from '@/store/userStore'

// Permission labels
const PERMISSION_LABELS = {
  [SITE_PERMISSIONS.SITE_VIEW]: 'View',
  [SITE_PERMISSIONS.SITE_VIEW_METRICS]: 'View Metrics',
  [SITE_PERMISSIONS.SITE_CONFIGURE]: 'Configure',
  [SITE_PERMISSIONS.SITE_ADD]: 'Add',
  [SITE_PERMISSIONS.SITE_EDIT]: 'Edit',
  [SITE_PERMISSIONS.SITE_DELETE]: 'Delete'
}

export default {
  name: 'AssignSitesModal',
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
  emits: ['close', 'save'],
  setup(props) {
    // Track permissions for each site
    const sitePermissions = reactive({})
    
    // Load user's existing permissions
    watch(() => props.user, (user) => {
      if (user && user.sitePermissions) {
        // Clone the user's site permissions
        Object.keys(user.sitePermissions).forEach(siteId => {
          sitePermissions[siteId] = [...user.sitePermissions[siteId]]
        })
      }
    }, { immediate: true })
    
    const userName = computed(() => {
      return props.user ? props.user.name || props.user.username : ''
    })
    
    // Check if a site is selected (has any permissions)
    const isSiteSelected = (siteId) => {
      return siteId in sitePermissions
    }
    
    // Check if site has a specific permission
    const hasPermission = (siteId, permission) => {
      return sitePermissions[siteId]?.includes(permission) || false
    }
    
    // Toggle site selection
    const toggleSite = (siteId, event) => {
      if (event.target.checked) {
        // Add site with default view permission
        sitePermissions[siteId] = [SITE_PERMISSIONS.SITE_VIEW]
      } else {
        // Remove site and all its permissions
        delete sitePermissions[siteId]
      }
    }
    
    // Toggle a specific permission for a site
    const togglePermission = (siteId, permission, event) => {
      if (!sitePermissions[siteId]) {
        sitePermissions[siteId] = []
      }
      
      if (event.target.checked) {
        // Add permission if it doesn't exist
        if (!sitePermissions[siteId].includes(permission)) {
          sitePermissions[siteId].push(permission)
        }
        
        // If adding a permission that requires view, add view too
        if (!sitePermissions[siteId].includes(SITE_PERMISSIONS.SITE_VIEW)) {
          sitePermissions[siteId].push(SITE_PERMISSIONS.SITE_VIEW)
        }
      } else {
        // Remove permission
        const index = sitePermissions[siteId].indexOf(permission)
        if (index !== -1) {
          sitePermissions[siteId].splice(index, 1)
        }
        
        // If removing the view permission, remove all permissions
        if (permission === SITE_PERMISSIONS.SITE_VIEW) {
          delete sitePermissions[siteId]
        }
      }
    }
    
    return {
      sitePermissions,
      userName,
      isSiteSelected,
      hasPermission,
      toggleSite,
      togglePermission,
      permissionLabels: PERMISSION_LABELS
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';

.site-permissions-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 1rem;
}

.site-permissions-card {
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  overflow: hidden;
  background-color: var(--bg-body);
}

.site-header {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  background-color: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.site-header label {
  font-weight: 600;
  margin-left: 0.5rem;
  cursor: pointer;
}

.permissions-list {
  padding: 0.5rem 1rem;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.5rem;
}

.permission-item {
  display: flex;
  align-items: center;
  padding: 0.25rem 0;
}

.permission-item label {
  margin-left: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}
</style> 