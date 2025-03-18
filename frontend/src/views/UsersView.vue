<template>
  <div class="users-container">
    <h1>User Management</h1>
    
    <div v-if="!isAdmin" class="access-denied">
      <h2>Access Denied</h2>
      <p>You don't have permission to manage users. Please contact your administrator.</p>
    </div>
    
    <div v-else>
      <!-- Add User Button -->
      <button class="add-user-button" @click="showAddUserModal = true">
        <span class="add-icon">+</span> Add New User
      </button>
      
      <!-- Users Table -->
      <div class="users-table-wrapper">
        <table class="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Assigned Sites</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.id }}</td>
              <td>{{ user.name }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>
                <span class="role-badge" :class="user.role">{{ user.role }}</span>
              </td>
              <td>
                <div class="assigned-sites">
                  <span 
                    v-for="siteId in user.assignedSites" 
                    :key="siteId" 
                    class="site-badge"
                  >
                    {{ getSiteName(siteId) }}
                  </span>
                  <button 
                    v-if="user.role !== 'admin' && user.role !== 'maintainer'"
                    class="site-assign-button" 
                    @click="openAssignSitesModal(user)"
                  >
                    Assign
                  </button>
                </div>
              </td>
              <td>
                <div class="action-buttons">
                  <button class="edit-button" @click="editUser(user)">Edit</button>
                  <button class="delete-button" @click="deleteUser(user)">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
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
  padding: 1rem;
}

.users-container h1 {
  margin-bottom: 2rem;
}

.access-denied {
  text-align: center;
  padding: 3rem;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.add-user-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.add-user-button:hover {
  background-color: #34495e;
}

.add-icon {
  font-size: 1.2rem;
}

.users-table-wrapper {
  overflow-x: auto;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.users-table th, .users-table td {
  padding: 1rem;
  text-align: left;
}

.users-table th {
  background-color: #f8f9fa;
  font-weight: 600;
}

.users-table tr:not(:last-child) {
  border-bottom: 1px solid #e9ecef;
}

.role-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-size: 0.85rem;
  font-weight: 500;
  text-transform: capitalize;
}

.role-badge.admin {
  background-color: #e53935;
  color: white;
}

.role-badge.maintainer {
  background-color: #42b983;
  color: white;
}

.role-badge.user {
  background-color: #3490dc;
  color: white;
}

.role-badge.guest {
  background-color: #adb5bd;
  color: white;
}

.assigned-sites {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  align-items: center;
}

.site-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background-color: #e9ecef;
  border-radius: 4px;
  font-size: 0.85rem;
}

.site-assign-button {
  padding: 0.25rem 0.5rem;
  border: 1px solid #3490dc;
  background-color: transparent;
  color: #3490dc;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.site-assign-button:hover {
  background-color: #3490dc;
  color: white;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.edit-button, .delete-button {
  padding: 0.5rem 0.75rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
}

.edit-button {
  background-color: #3490dc;
  color: white;
}

.edit-button:hover {
  background-color: #2779bd;
}

.delete-button {
  background-color: #e53935;
  color: white;
}

.delete-button:hover {
  background-color: #c53030;
}

.modal.user-modal, .modal.assign-sites-modal {
  max-width: 500px;
}

.modal.delete-modal {
  max-width: 400px;
}

.modal-backdrop, .modal, .modal-header, .modal-body, .modal-footer,
.form-group, .site-checkbox-list, .site-checkbox, .site-list, .site-item {
  /* These styles are already defined in your DashboardView */
}

.warning {
  color: #e53935;
  font-weight: 500;
}

.delete-button.confirm {
  width: auto;
  padding: 0.75rem 1.5rem;
}

.site-checkbox-list, .site-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.site-checkbox, .site-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.save-button {
  padding: 0.75rem 1.5rem;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.save-button:hover {
  background-color: #34495e;
}

.save-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}
</style> 