<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal delete-modal">
      <div class="modal-header">
        <h3>Confirm Delete</h3>
        <button class="close-button" @click="$emit('close')">×</button>
      </div>
      <div class="modal-body">
        <p>Are you sure you want to delete user <strong>{{ userName }}</strong>?</p>
        <p class="warning">This action cannot be undone.</p>
      </div>
      <div class="modal-footer">
        <button class="cancel-button" @click="$emit('close')">Cancel</button>
        <button class="delete-button confirm" @click="$emit('confirm')">
          Delete User
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'DeleteConfirmModal',
  props: {
    user: {
      type: Object,
      required: true
    }
  },
  emits: ['close', 'confirm'],
  setup(props) {
    const userName = computed(() => {
      return props.user.name || props.user.username || 'this user'
    })
    
    return {
      userName
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 