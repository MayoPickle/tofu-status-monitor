<template>
  <transition name="modal">
    <div v-if="modelValue" class="modal-backdrop" @click.self="$emit('update:modelValue', false)">
      <div class="modal card">
        <div class="modal-header">
          <h3>{{ title }}</h3>
          <button class="modal-close" @click="$emit('update:modelValue', false)">
            <svg viewBox="0 0 24 24" width="24" height="24">
              <path fill="currentColor" d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z" />
            </svg>
          </button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label class="form-label" for="site-name">Site Name</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" width="18" height="18" class="input-icon">
                <path fill="currentColor" d="M17,13H13V17H11V13H7V11H11V7H13V11H17M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
              </svg>
              <input 
                type="text" 
                id="site-name" 
                v-model="form.name" 
                placeholder="Production API" 
                class="form-control"
              >
            </div>
          </div>
          <div class="form-group">
            <label class="form-label" for="site-url">URL to Monitor</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" width="18" height="18" class="input-icon">
                <path fill="currentColor" d="M16.36,14C16.44,13.34 16.5,12.68 16.5,12C16.5,11.32 16.44,10.66 16.36,10H19.74C19.9,10.64 20,11.31 20,12C20,12.69 19.9,13.36 19.74,14M14.59,19.56C15.19,18.45 15.65,17.25 15.97,16H18.92C17.96,17.65 16.43,18.93 14.59,19.56M14.34,14H9.66C9.56,13.34 9.5,12.68 9.5,12C9.5,11.32 9.56,10.65 9.66,10H14.34C14.43,10.65 14.5,11.32 14.5,12C14.5,12.68 14.43,13.34 14.34,14M12,19.96C11.17,18.76 10.5,17.43 10.09,16H13.91C13.5,17.43 12.83,18.76 12,19.96M8,8H5.08C6.03,6.34 7.57,5.06 9.4,4.44C8.8,5.55 8.35,6.75 8,8M5.08,16H8C8.35,17.25 8.8,18.45 9.4,19.56C7.57,18.93 6.03,17.65 5.08,16M4.26,14C4.1,13.36 4,12.69 4,12C4,11.31 4.1,10.64 4.26,10H7.64C7.56,10.66 7.5,11.32 7.5,12C7.5,12.68 7.56,13.34 7.64,14M12,4.03C12.83,5.23 13.5,6.57 13.91,8H10.09C10.5,6.57 11.17,5.23 12,4.03M18.92,8H15.97C15.65,6.75 15.19,5.55 14.59,4.44C16.43,5.07 17.96,6.34 18.92,8M12,2C6.47,2 2,6.5 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
              </svg>
              <input 
                type="text" 
                id="site-url" 
                v-model="form.url" 
                placeholder="https://api.example.com/health" 
                class="form-control"
              >
            </div>
          </div>
          <div class="form-group">
            <label class="form-label" for="site-id">Site ID (for API)</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" width="18" height="18" class="input-icon">
                <path fill="currentColor" d="M6,17C6,15 10,13.9 12,13.9C14,13.9 18,15 18,17V18H6M15,9A3,3 0 0,1 12,12A3,3 0 0,1 9,9A3,3 0 0,1 12,6A3,3 0 0,1 15,9M3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V5A2,2 0 0,0 19,3H5C3.89,3 3,3.9 3,5Z" />
              </svg>
              <input 
                type="text" 
                id="site-id" 
                v-model="form.id" 
                placeholder="prod-api" 
                class="form-control"
              >
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-outline" @click="$emit('update:modelValue', false)">Cancel</button>
          <button class="btn btn-primary" @click="submit" :disabled="!isFormValid">{{ submitText }}</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import { reactive, computed } from 'vue'

export default {
  name: 'AddSiteModal',
  props: {
    modelValue: {
      type: Boolean,
      default: false
    },
    title: {
      type: String,
      default: 'Add Monitoring Site'
    },
    submitText: {
      type: String,
      default: 'Add Site'
    }
  },
  emits: ['update:modelValue', 'submit'],
  setup(props, { emit }) {
    const form = reactive({
      name: '',
      url: '',
      id: ''
    })
    
    const isFormValid = computed(() => {
      return form.name && 
             form.url && 
             form.url.startsWith('http') &&
             form.id
    })
    
    const submit = () => {
      if (isFormValid.value) {
        emit('submit', { ...form })
        emit('update:modelValue', false)
        
        // Reset form
        form.name = ''
        form.url = ''
        form.id = ''
      }
    }
    
    return {
      form,
      isFormValid,
      submit
    }
  }
}
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  backdrop-filter: blur(2px);
}

.modal {
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  margin: 0;
  color: var(--text-primary);
}

.modal-close {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--text-secondary);
  padding: 0.25rem;
  border-radius: var(--radius);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
}

.modal-close:hover {
  color: var(--danger);
  background-color: rgba(255, 0, 110, 0.05);
}

.modal-body {
  padding: 1.25rem;
  overflow-y: auto;
}

.modal-footer {
  padding: 1.25rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
}

.input-wrapper {
  position: relative;
}

.input-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-secondary);
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  font-size: 1rem;
  color: var(--text-primary);
  transition: var(--transition);
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.15);
}

/* Animations */
.modal-enter-active,
.modal-leave-active {
  transition: all 0.3s ease;
}

.modal-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.modal-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

@media (max-width: 480px) {
  .modal {
    width: 95%;
  }
}
</style> 