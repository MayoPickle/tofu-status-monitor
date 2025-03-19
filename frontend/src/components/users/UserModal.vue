<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal user-modal">
      <div class="modal-header">
        <h3>{{ isEdit ? 'Edit User' : 'Add New User' }}</h3>
        <button class="close-button" @click="$emit('close')">×</button>
      </div>
      <div class="modal-body">
        <div class="form-group">
          <label for="user-name">Name</label>
          <input type="text" id="user-name" v-model="formData.name" placeholder="Full Name">
        </div>
        <div class="form-group">
          <label for="user-username">Username</label>
          <input type="text" id="user-username" v-model="formData.username" placeholder="Username" :disabled="isEdit">
        </div>
        <div class="form-group">
          <label for="user-email">Email</label>
          <input type="email" id="user-email" v-model="formData.email" placeholder="Email Address">
        </div>
        <div class="form-group">
          <label for="user-password">Password</label>
          <input type="password" id="user-password" v-model="formData.password" placeholder="Password">
          <small v-if="isEdit">Leave blank to keep the current password</small>
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
        <button class="cancel-button" @click="$emit('close')">Cancel</button>
        <button class="save-button" @click="$emit('save', formData)" :disabled="!isFormValid">
          {{ isEdit ? 'Update User' : 'Add User' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed, ref, watch } from 'vue'

export default {
  name: 'UserModal',
  props: {
    user: {
      type: Object,
      default: null
    },
    monitoredSites: {
      type: Array,
      required: true
    },
    isEdit: {
      type: Boolean,
      default: false
    }
  },
  emits: ['close', 'save'],
  setup(props) {
    const formData = ref({
      id: null,
      name: '',
      username: '',
      email: '',
      password: '',
      role: 'user',
      assignedSites: []
    })
    
    // Initialize form data when user prop changes
    watch(() => props.user, (newUser) => {
      if (newUser) {
        formData.value = {
          id: newUser.id,
          name: newUser.name || '',
          username: newUser.username || '',
          email: newUser.email || '',
          password: '', // Don't prefill password
          role: newUser.role || 'user',
          assignedSites: [...(newUser.assignedSites || [])]
        }
      } else {
        // Reset form for new user
        formData.value = {
          id: null,
          name: '',
          username: '',
          email: '',
          password: '',
          role: 'user',
          assignedSites: []
        }
      }
    }, { immediate: true })
    
    // Form validation
    const isFormValid = computed(() => {
      const { name, username, email, password, role } = formData.value
      
      // For new users, all fields are required
      if (!props.isEdit) {
        return name && username && email && password && role
      }
      
      // For editing, password can be blank
      return name && username && email && role
    })
    
    return {
      formData,
      isFormValid
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 