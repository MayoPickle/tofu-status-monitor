<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal assign-sites-modal">
      <div class="modal-header">
        <h3>Assign Sites to {{ userName }}</h3>
        <button class="close-button" @click="$emit('close')">×</button>
      </div>
      <div class="modal-body">
        <div class="site-list">
          <div class="site-item" v-for="site in monitoredSites" :key="site.id">
            <input 
              type="checkbox" 
              :id="'assign-site-' + site.id" 
              :value="site.id" 
              v-model="selectedSites"
            >
            <label :for="'assign-site-' + site.id">{{ site.name }}</label>
          </div>
        </div>
      </div>
      <div class="modal-footer">
        <button class="cancel-button" @click="$emit('close')">Cancel</button>
        <button class="save-button" @click="$emit('save', selectedSites)">
          Save Assignments
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch } from 'vue'

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
    const selectedSites = ref([])
    
    // Update selected sites when user changes
    watch(() => props.user, (newUser) => {
      if (newUser && newUser.assignedSites) {
        selectedSites.value = [...newUser.assignedSites]
      } else {
        selectedSites.value = []
      }
    }, { immediate: true })
    
    const userName = computed(() => {
      return props.user ? props.user.name || props.user.username : ''
    })
    
    return {
      selectedSites,
      userName
    }
  }
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 