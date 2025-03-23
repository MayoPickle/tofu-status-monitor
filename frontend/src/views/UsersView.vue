<template>
  <div class="users-container">
    <page-header 
      :is-admin="isAdmin"
      :is-migrating="migratingPermissions" 
      @add-user="showAddUserModal = true"
      @migrate-permissions="migratePermissions"
    />
    
    <access-denied v-if="!isAdmin" />
    
    <div v-else>
      <search-filter 
        v-model:search-query="searchQuery" 
        v-model:role-filter="roleFilter" 
      />
      
      <users-list 
        :filtered-users="filteredUsers" 
        :monitored-sites="monitoredSites" 
        :loading="loading" 
        :error="error"
        @edit="editUser"
        @delete="deleteUser"
        @assign-sites="openAssignSitesModal"
      />
    </div>
    
    <!-- Add/Edit User Modal -->
    <user-modal
      v-if="showAddUserModal || showEditUserModal"
      :user="showEditUserModal ? selectedUser : null"
      :monitored-sites="monitoredSites"
      :is-edit="showEditUserModal"
      @close="closeModals"
      @save="saveUser"
    />
    
    <!-- Assign Sites Modal -->
    <assign-sites-modal
      v-if="showAssignSitesModal && selectedUser"
      :user="selectedUser"
      :monitored-sites="monitoredSites"
      @close="closeModals"
      @save="saveSiteAssignments"
    />
    
    <!-- Delete Confirmation Modal -->
    <delete-confirm-modal
      v-if="showDeleteModal && selectedUser"
      :user="selectedUser"
      @close="closeModals"
      @confirm="confirmDeleteUser"
    />
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import userStore from '@/store/userStore'

// Import components
import PageHeader from '@/components/users/PageHeader.vue'
import AccessDenied from '@/components/users/AccessDenied.vue'
import SearchFilter from '@/components/users/SearchFilter.vue'
import UsersList from '@/components/users/UsersList.vue'
import UserModal from '@/components/users/UserModal.vue'
import AssignSitesModal from '@/components/users/AssignSitesModal.vue'
import DeleteConfirmModal from '@/components/users/DeleteConfirmModal.vue'

export default {
  name: 'UsersView',
  components: {
    PageHeader,
    AccessDenied,
    SearchFilter,
    UsersList,
    UserModal,
    AssignSitesModal,
    DeleteConfirmModal
  },
  setup() {
    // User state
    const users = ref([])
    
    // Error and loading states
    const loading = ref(false)
    const error = ref(null)
    
    // Admin check
    const isAdmin = computed(() => userStore.isAdmin())
    
    // Monitored sites (would come from a sites store in a real app)
    const monitoredSites = ref([
      { id: 'main', name: 'Main API', url: 'https://api.example.com' },
      { id: 'backup', name: 'Backup API', url: 'https://backup-api.example.com' },
      { id: 'staging', name: 'Staging', url: 'https://staging-api.example.com' }
    ])
    
    // Modal state
    const showAddUserModal = ref(false)
    const showEditUserModal = ref(false)
    const showAssignSitesModal = ref(false)
    const showDeleteModal = ref(false)
    
    // Selected user for operations
    const selectedUser = ref(null)
    
    // Search and filter state
    const searchQuery = ref('')
    const roleFilter = ref('')
    
    // Migration state
    const migratingPermissions = ref(false)
    
    // Load users on mount
    onMounted(() => {
      loadUsers()
    })
    
    // Load users from backend API
    const loadUsers = async () => {
      if (!isAdmin.value) return
      
      loading.value = true
      error.value = null
      
      try {
        // Get users from API
        users.value = await userStore.getAllUsers()
      } catch (err) {
        console.error('Failed to load users from API:', err)
        error.value = 'Failed to load users. Please try again later.'
      } finally {
        loading.value = false
      }
    }
    
    // Open edit user modal
    const editUser = (user) => {
      selectedUser.value = user
      showEditUserModal.value = true
    }
    
    // Open assign sites modal
    const openAssignSitesModal = (user) => {
      selectedUser.value = user
      showAssignSitesModal.value = true
    }
    
    // Open delete confirmation modal
    const deleteUser = (user) => {
      selectedUser.value = user
      showDeleteModal.value = true
    }
    
    // Save user (add or update)
    const saveUser = async (formData) => {
      try {
        if (showEditUserModal.value) {
          // Update existing user
          const updateData = { ...formData }
          if (!updateData.password) {
            delete updateData.password // Don't update password if blank
          }
          
          // Update user via API
          await userStore.updateUser(selectedUser.value.id, updateData)
        } else {
          // Add new user via API
          await userStore.addUser(formData)
        }
        
        await loadUsers()
        closeModals()
      } catch (err) {
        console.error('Failed to save user:', err)
        error.value = err.message || 'Failed to save user'
      }
    }
    
    // Save site permissions
    const saveSiteAssignments = async (sitePermissions) => {
      if (selectedUser.value) {
        try {
          // Update permissions via API
          await userStore.updateUserPermissions(selectedUser.value.id, sitePermissions)
          
          await loadUsers()
          closeModals()
        } catch (err) {
          console.error('Failed to update site permissions:', err)
          error.value = err.message || 'Failed to update site permissions'
        }
      }
    }
    
    // Confirm user deletion
    const confirmDeleteUser = async () => {
      if (selectedUser.value) {
        try {
          // Delete user via API
          await userStore.deleteUser(selectedUser.value.id)
          
          await loadUsers()
          closeModals()
        } catch (err) {
          console.error('Failed to delete user:', err)
          error.value = err.message || 'Failed to delete user'
        }
      }
    }
    
    // Close all modals
    const closeModals = () => {
      showAddUserModal.value = false
      showEditUserModal.value = false
      showAssignSitesModal.value = false
      showDeleteModal.value = false
      selectedUser.value = null
      error.value = null
    }
    
    // Computed filtered users
    const filteredUsers = computed(() => {
      return users.value.filter(user => {
        const matchesSearch = 
          (user.name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
           user.username.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
           user.email.toLowerCase().includes(searchQuery.value.toLowerCase()))
        
        const matchesRole = !roleFilter.value || user.role === roleFilter.value
        
        return matchesSearch && matchesRole
      })
    })
    
    // Migration function for all users' permissions
    const migratePermissions = async () => {
      try {
        migratingPermissions.value = true
        
        // Call the API to migrate permissions
        const result = await userStore.migrateUserPermissions()
        
        // Show success message
        alert(result.message || 'Permissions migrated successfully')
        
        // Refresh users list
        await loadUsers()
      } catch (err) {
        console.error('Failed to migrate permissions:', err)
        error.value = err.message || 'Failed to migrate permissions'
        alert('Failed to migrate permissions. See console for details.')
      } finally {
        migratingPermissions.value = false
      }
    }
    
    return {
      users,
      isAdmin,
      monitoredSites,
      showAddUserModal,
      showEditUserModal,
      showAssignSitesModal,
      showDeleteModal,
      selectedUser,
      searchQuery,
      roleFilter,
      filteredUsers,
      loading,
      error,
      editUser,
      openAssignSitesModal,
      deleteUser,
      saveUser,
      saveSiteAssignments,
      confirmDeleteUser,
      closeModals,
      migratingPermissions,
      migratePermissions
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 