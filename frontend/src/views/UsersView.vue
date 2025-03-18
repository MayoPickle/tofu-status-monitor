<template>
  <div class="users-container">
    <div class="page-header">
      <div class="header-content">
        <h1>User Management</h1>
        <p class="subtitle">Manage user accounts and permissions</p>
      </div>
      
      <button v-if="isAdmin" class="add-user-button" @click="showAddUserModal = true">
        <svg viewBox="0 0 24 24" class="button-icon">
          <path d="M15,14C12.33,14 7,15.33 7,18V20H23V18C23,15.33 17.67,14 15,14M6,10V7H4V10H1V12H4V15H6V12H9V10M15,12A4,4 0 0,0 19,8A4,4 0 0,0 15,4A4,4 0 0,0 11,8A4,4 0 0,0 15,12Z" />
        </svg>
        Add New User
      </button>
    </div>
    
    <div v-if="!isAdmin" class="access-denied">
      <svg viewBox="0 0 24 24" class="access-denied-icon">
        <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,7C13.4,7 14.8,8.1 14.8,9.5V11C15.4,11 16,11.6 16,12.3V15.8C16,16.4 15.4,17 14.7,17H9.2C8.6,17 8,16.4 8,15.7V12.2C8,11.6 8.6,11 9.2,11V9.5C9.2,8.1 10.6,7 12,7M12,8.2C11.2,8.2 10.5,8.7 10.5,9.5V11H13.5V9.5C13.5,8.7 12.8,8.2 12,8.2Z" />
      </svg>
      <h2>Access Denied</h2>
      <p>You don't have permission to manage users. Please contact your administrator.</p>
    </div>
    
    <div v-else>
      <!-- Search and Filter Section -->
      <div class="controls-section">
        <div class="search-box">
          <svg viewBox="0 0 24 24" class="search-icon">
            <path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
          </svg>
          <input 
            type="text" 
            v-model="searchQuery" 
            placeholder="Search users..."
            class="search-input"
          >
        </div>
        
        <div class="filter-box">
          <select v-model="roleFilter" class="role-filter">
            <option value="">All Roles</option>
            <option value="admin">Admin</option>
            <option value="maintainer">Maintainer</option>
            <option value="user">User</option>
            <option value="guest">Guest</option>
          </select>
        </div>
      </div>
      
      <!-- Users Grid -->
      <div class="users-grid">
        <div v-for="user in filteredUsers" :key="user.id" class="user-card">
          <div class="user-card-header">
            <div class="user-avatar">{{ getUserInitials(user.name || user.username) }}</div>
            <div class="user-info">
              <h3 class="user-name">{{ user.name || user.username }}</h3>
              <span class="role-badge" :class="user.role">{{ user.role }}</span>
            </div>
            <div class="card-actions">
              <button class="action-button edit" @click="editUser(user)" title="Edit User">
                <svg viewBox="0 0 24 24">
                  <path d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z" />
                </svg>
              </button>
              <button class="action-button delete" @click="deleteUser(user)" title="Delete User">
                <svg viewBox="0 0 24 24">
                  <path d="M19,4H15.5L14.5,3H9.5L8.5,4H5V6H19M6,19A2,2 0 0,0 8,21H16A2,2 0 0,0 18,19V7H6V19Z" />
                </svg>
              </button>
            </div>
          </div>
          
          <div class="user-card-body">
            <div class="detail-item">
              <svg viewBox="0 0 24 24" class="detail-icon">
                <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
              </svg>
              <span>{{ user.username }}</span>
            </div>
            <div class="detail-item">
              <svg viewBox="0 0 24 24" class="detail-icon">
                <path d="M20,8L12,13L4,8V6L12,11L20,6M20,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V6C22,4.89 21.1,4 20,4Z" />
              </svg>
              <span>{{ user.email }}</span>
            </div>
            <div class="assigned-sites">
              <div class="sites-header">
                <svg viewBox="0 0 24 24" class="detail-icon">
                  <path d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z" />
                </svg>
                <span>Assigned Sites</span>
              </div>
              <div class="site-badges">
                <span v-for="siteId in user.assignedSites" 
                      :key="siteId" 
                      class="site-badge">
                  {{ getSiteName(siteId) }}
                </span>
                <button 
                  v-if="user.role !== 'admin' && user.role !== 'maintainer'"
                  class="assign-sites-button"
                  @click="openAssignSitesModal(user)">
                  <svg viewBox="0 0 24 24" class="button-icon">
                    <path d="M19,13H13V19H11V13H5V11H11V5H13V11H19V13Z" />
                  </svg>
                  Assign
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Add/Edit User Modal -->
    <div v-if="showAddUserModal || showEditUserModal" class="modal-backdrop" @click.self="closeModals">
      <div class="modal user-modal">
        <div class="modal-header">
          <h3>{{ showEditUserModal ? 'Edit User' : 'Add New User' }}</h3>
          <button class="close-button" @click="closeModals">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label for="user-name">Name</label>
            <input type="text" id="user-name" v-model="formData.name" placeholder="Full Name">
          </div>
          <div class="form-group">
            <label for="user-username">Username</label>
            <input type="text" id="user-username" v-model="formData.username" placeholder="Username">
          </div>
          <div class="form-group">
            <label for="user-email">Email</label>
            <input type="email" id="user-email" v-model="formData.email" placeholder="Email Address">
          </div>
          <div class="form-group">
            <label for="user-password">Password</label>
            <input type="password" id="user-password" v-model="formData.password" placeholder="Password">
            <small v-if="showEditUserModal">Leave blank to keep the current password</small>
          </div>
          <div class="form-group">
            <label for="user-role">Role</label>
            <select id="user-role" v-model="formData.role">
              <option value="admin">Admin</option>
              <option value="maintainer">Maintainer</option>
              <option value="user">User</option>
              <option value="guest">Guest</option>
            </select>
          </div>
          
          <div v-if="formData.role === 'user'" class="form-group">
            <label>Assigned Sites</label>
            <div class="site-checkbox-list">
              <div class="site-checkbox" v-for="site in monitoredSites" :key="site.id">
                <input 
                  type="checkbox" 
                  :id="'site-' + site.id" 
                  :value="site.id" 
                  v-model="formData.assignedSites"
                >
                <label :for="'site-' + site.id">{{ site.name }}</label>
              </div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-button" @click="closeModals">Cancel</button>
          <button class="save-button" @click="saveUser" :disabled="!isFormValid">
            {{ showEditUserModal ? 'Update User' : 'Add User' }}
          </button>
        </div>
      </div>
    </div>
    
    <!-- Assign Sites Modal -->
    <div v-if="showAssignSitesModal" class="modal-backdrop" @click.self="closeModals">
      <div class="modal assign-sites-modal">
        <div class="modal-header">
          <h3>Assign Sites to {{ selectedUser?.name }}</h3>
          <button class="close-button" @click="closeModals">×</button>
        </div>
        <div class="modal-body">
          <div class="site-list">
            <div class="site-item" v-for="site in monitoredSites" :key="site.id">
              <input 
                type="checkbox" 
                :id="'assign-site-' + site.id" 
                :value="site.id" 
                v-model="assignedSites"
              >
              <label :for="'assign-site-' + site.id">{{ site.name }}</label>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="cancel-button" @click="closeModals">Cancel</button>
          <button class="save-button" @click="saveSiteAssignments">
            Save Assignments
          </button>
        </div>
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-backdrop" @click.self="closeModals">
      <div class="modal delete-modal">
        <div class="modal-header">
          <h3>Confirm Delete</h3>
          <button class="close-button" @click="closeModals">×</button>
        </div>
        <div class="modal-body">
          <p>Are you sure you want to delete user <strong>{{ selectedUser?.name }}</strong>?</p>
          <p class="warning">This action cannot be undone.</p>
        </div>
        <div class="modal-footer">
          <button class="cancel-button" @click="closeModals">Cancel</button>
          <button class="delete-button confirm" @click="confirmDeleteUser">
            Delete User
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import userStore, { ROLES } from '../store/userStore'

export default {
  name: 'UsersView',
  setup() {
    // User state
    const users = ref([])
    
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
    
    // Form data
    const formData = ref({
      id: null,
      name: '',
      username: '',
      email: '',
      password: '',
      role: ROLES.USER,
      assignedSites: []
    })
    
    // Selected user for operations
    const selectedUser = ref(null)
    
    // Assigned sites for the site assignment modal
    const assignedSites = ref([])
    
    // Search and filter state
    const searchQuery = ref('')
    const roleFilter = ref('')
    
    // Load users on mount
    onMounted(() => {
      loadUsers()
    })
    
    // Load users from the store
    const loadUsers = () => {
      users.value = userStore.getUserList()
    }
    
    // Get site name by ID
    const getSiteName = (siteId) => {
      const site = monitoredSites.value.find(site => site.id === siteId)
      return site ? site.name : siteId
    }
    
    // Open add user modal
    const showAddUser = () => {
      formData.value = {
        id: null,
        name: '',
        username: '',
        email: '',
        password: '',
        role: ROLES.USER,
        assignedSites: []
      }
      showAddUserModal.value = true
    }
    
    // Open edit user modal
    const editUser = (user) => {
      formData.value = {
        id: user.id,
        name: user.name,
        username: user.username,
        email: user.email,
        password: '', // Don't prefill password
        role: user.role,
        assignedSites: [...user.assignedSites]
      }
      selectedUser.value = user
      showEditUserModal.value = true
    }
    
    // Open assign sites modal
    const openAssignSitesModal = (user) => {
      selectedUser.value = user
      assignedSites.value = [...user.assignedSites]
      showAssignSitesModal.value = true
    }
    
    // Open delete confirmation modal
    const deleteUser = (user) => {
      selectedUser.value = user
      showDeleteModal.value = true
    }
    
    // Save user (add or update)
    const saveUser = () => {
      if (showEditUserModal.value) {
        // Update existing user
        const updateData = { ...formData.value }
        if (!updateData.password) {
          delete updateData.password // Don't update password if blank
        }
        userStore.updateUser(updateData.id, updateData)
      } else {
        // Add new user
        userStore.addUser(formData.value)
      }
      
      loadUsers()
      closeModals()
    }
    
    // Save site assignments
    const saveSiteAssignments = () => {
      if (selectedUser.value) {
        userStore.assignSitesToUser(selectedUser.value.id, assignedSites.value)
        loadUsers()
        closeModals()
      }
    }
    
    // Confirm user deletion
    const confirmDeleteUser = () => {
      if (selectedUser.value) {
        userStore.deleteUser(selectedUser.value.id)
        loadUsers()
        closeModals()
      }
    }
    
    // Close all modals
    const closeModals = () => {
      showAddUserModal.value = false
      showEditUserModal.value = false
      showAssignSitesModal.value = false
      showDeleteModal.value = false
      selectedUser.value = null
    }
    
    // Form validation
    const isFormValid = computed(() => {
      const { name, username, email, password, role } = formData.value
      
      // For new users, all fields are required
      if (showAddUserModal.value) {
        return name && username && email && password && role
      }
      
      // For editing, password can be blank
      return name && username && email && role
    })
    
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
    
    const getUserInitials = (name) => {
      if (!name) return '?'
      return name
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .substring(0, 2)
    }
    
    return {
      users,
      isAdmin,
      monitoredSites,
      showAddUserModal,
      showEditUserModal,
      showAssignSitesModal,
      showDeleteModal,
      formData,
      selectedUser,
      assignedSites,
      searchQuery,
      roleFilter,
      filteredUsers,
      getUserInitials,
      getSiteName,
      showAddUser,
      editUser,
      openAssignSitesModal,
      deleteUser,
      saveUser,
      saveSiteAssignments,
      confirmDeleteUser,
      closeModals,
      isFormValid
    }
  }
}
</script>

<style scoped>
.users-container {
  padding: 2rem;
  max-width: 1400px;
  margin: 0 auto;
  min-height: calc(100vh - 4rem);
  background-color: var(--bg-body);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.header-content h1 {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.5px;
}

.subtitle {
  color: var(--text-secondary);
  margin-top: 0.5rem;
  font-size: 1rem;
}

.add-user-button {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1.75rem;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-weight: 600;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: 0 2px 4px rgba(42, 157, 143, 0.1);
}

.add-user-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(42, 157, 143, 0.2);
}

.button-icon {
  width: 1.25rem;
  height: 1.25rem;
  fill: currentColor;
}

.controls-section {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 1.5rem;
  margin-bottom: 2.5rem;
  padding: 1.5rem;
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.search-box {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1.25rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  fill: var(--text-secondary);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3.25rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background-color: var(--bg-body);
  color: var(--text-primary);
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(42, 157, 143, 0.1);
}

.role-filter {
  min-width: 180px;
  padding: 1rem 2.5rem 1rem 1.25rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background-color: var(--bg-body);
  color: var(--text-primary);
  font-size: 0.9375rem;
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%236B7280'%3E%3Cpath d='M7 10l5 5 5-5H7z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 1rem center;
  background-size: 1.25rem;
  transition: all 0.2s ease;
}

.role-filter:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(42, 157, 143, 0.1);
}

.users-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 1.5rem;
  margin: 0 -0.75rem;
  padding: 0.75rem;
}

.user-card {
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid var(--border-color);
}

.user-card:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-lg);
  border-color: var(--primary);
}

.user-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background-color: var(--bg-body);
  border-bottom: 1px solid var(--border-color);
}

.user-avatar {
  width: 3.5rem;
  height: 3.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--primary);
  color: white;
  border-radius: 50%;
  font-weight: 600;
  font-size: 1.25rem;
  box-shadow: 0 2px 4px rgba(42, 157, 143, 0.2);
}

.user-info {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0 0 0.375rem;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.role-badge {
  display: inline-flex;
  align-items: center;
  padding: 0.375rem 0.75rem;
  border-radius: 2rem;
  font-size: 0.8125rem;
  font-weight: 500;
  text-transform: capitalize;
  letter-spacing: 0.025em;
}

.role-badge.admin {
  background-color: rgba(231, 111, 81, 0.1);
  color: var(--danger);
}

.role-badge.maintainer {
  background-color: rgba(82, 183, 136, 0.1);
  color: var(--success);
}

.role-badge.user {
  background-color: rgba(42, 157, 143, 0.1);
  color: var(--primary);
}

.role-badge.guest {
  background-color: rgba(108, 117, 125, 0.1);
  color: var(--gray);
}

.card-actions {
  display: flex;
  gap: 0.5rem;
  margin-left: auto;
  padding-left: 1rem;
}

.action-button {
  padding: 0.625rem;
  border: none;
  border-radius: var(--radius);
  background-color: transparent;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
}

.action-button svg {
  width: 1.25rem;
  height: 1.25rem;
  transition: fill 0.2s ease;
}

.action-button.edit:hover {
  background-color: rgba(42, 157, 143, 0.1);
  color: var(--primary);
}

.action-button.delete:hover {
  background-color: rgba(231, 111, 81, 0.1);
  color: var(--danger);
}

.user-card-body {
  padding: 1.5rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.75rem 0;
  color: var(--text-secondary);
  font-size: 0.9375rem;
}

.detail-item:not(:last-child) {
  border-bottom: 1px dashed var(--border-color);
}

.detail-icon {
  width: 1.25rem;
  height: 1.25rem;
  fill: currentColor;
  flex-shrink: 0;
}

.detail-item span {
  flex: 1;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.assigned-sites {
  margin-top: 1.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.sites-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  color: var(--text-secondary);
  font-weight: 500;
  font-size: 0.9375rem;
}

.site-badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.site-badge {
  padding: 0.375rem 0.75rem;
  background-color: var(--bg-body);
  border: 1px solid var(--border-color);
  border-radius: 2rem;
  font-size: 0.8125rem;
  color: var(--text-secondary);
  transition: all 0.2s ease;
}

.site-badge:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.assign-sites-button {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  padding: 0.375rem 0.75rem;
  background-color: transparent;
  border: 1px dashed var(--primary);
  border-radius: 2rem;
  color: var(--primary);
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.assign-sites-button:hover {
  background-color: var(--primary);
  color: white;
}

.assign-sites-button .button-icon {
  width: 1rem;
  height: 1rem;
}

.access-denied {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow);
}

.access-denied-icon {
  width: 5rem;
  height: 5rem;
  fill: var(--danger);
  margin-bottom: 2rem;
  opacity: 0.9;
}

.access-denied h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
}

.access-denied p {
  color: var(--text-secondary);
  max-width: 400px;
  line-height: 1.6;
}

/* Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal {
  background-color: var(--bg-body);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  width: 100%;
  max-width: 500px;
  max-height: 90vh;
  overflow-y: auto;
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.close-button {
  padding: 0.5rem;
  margin: -0.5rem;
  border: none;
  background: none;
  color: var(--text-secondary);
  font-size: 1.5rem;
  line-height: 1;
  cursor: pointer;
  border-radius: var(--radius);
  transition: all 0.2s ease;
}

.close-button:hover {
  background-color: var(--bg-hover);
  color: var(--text-primary);
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 0.5rem;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background-color: var(--bg-secondary);
  color: var(--text-primary);
  font-size: 0.9375rem;
  transition: all 0.2s ease;
}

.form-group input:focus,
.form-group select:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(42, 157, 143, 0.1);
}

.form-group small {
  display: block;
  margin-top: 0.5rem;
  color: var(--text-secondary);
  font-size: 0.8125rem;
}

.site-checkbox-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 0.75rem;
  margin-top: 0.75rem;
}

.site-checkbox {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  border-radius: var(--radius);
  transition: background-color 0.2s ease;
}

.site-checkbox:hover {
  background-color: var(--bg-hover);
}

.site-checkbox input[type="checkbox"] {
  width: 1rem;
  height: 1rem;
  margin: 0;
}

.site-checkbox label {
  margin: 0;
  font-weight: normal;
  cursor: pointer;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.cancel-button,
.save-button {
  padding: 0.875rem 1.75rem;
  border-radius: var(--radius);
  font-weight: 500;
  font-size: 0.9375rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.cancel-button {
  background-color: transparent;
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
}

.cancel-button:hover {
  background-color: var(--bg-hover);
  border-color: var(--text-secondary);
}

.save-button {
  background-color: var(--primary);
  border: none;
  color: white;
  box-shadow: 0 2px 4px rgba(42, 157, 143, 0.1);
}

.save-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(42, 157, 143, 0.2);
}

.save-button:disabled {
  background-color: var(--gray);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.delete-button.confirm {
  background-color: var(--danger);
  color: white;
}

.delete-button.confirm:hover {
  background-color: var(--danger-dark);
}

.warning {
  color: var(--danger);
  font-weight: 500;
}

@media (max-width: 768px) {
  .users-container {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    margin-bottom: 2rem;
  }
  
  .header-content h1 {
    font-size: 1.75rem;
  }
  
  .controls-section {
    grid-template-columns: 1fr;
    padding: 1rem;
  }
  
  .users-grid {
    grid-template-columns: 1fr;
    margin: 0;
    padding: 0;
  }
  
  .user-card-header {
    padding: 1rem;
  }
  
  .user-card-body {
    padding: 1rem;
  }
  
  .modal {
    margin: 1rem;
  }
}

@media (max-width: 480px) {
  .page-header {
    padding-bottom: 1rem;
  }
  
  .add-user-button {
    width: 100%;
    justify-content: center;
  }
  
  .user-avatar {
    width: 3rem;
    height: 3rem;
    font-size: 1rem;
  }
  
  .modal-header,
  .modal-body,
  .modal-footer {
    padding: 1rem;
  }
  
  .site-checkbox-list {
    grid-template-columns: 1fr;
  }
}
</style> 