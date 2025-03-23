<template>
  <div class="controls-section">
    <div class="search-box">
      <svg viewBox="0 0 24 24" class="search-icon">
        <path d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
      </svg>
      <input 
        type="text" 
        :value="searchQuery" 
        @input="$emit('update:searchQuery', $event.target.value)"
        placeholder="Search users..."
        class="search-input"
      >
    </div>
    
    <div class="filter-box">
      <select 
        :value="roleFilter" 
        @change="$emit('update:roleFilter', $event.target.value)" 
        class="role-filter"
      >
        <option value="">All Roles</option>
        <option value="admin">Admin</option>
        <option value="maintainer">Maintainer</option>
        <option value="user">User</option>
        <option value="guest">Guest</option>
      </select>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SearchFilter',
  props: {
    searchQuery: {
      type: String,
      required: true
    },
    roleFilter: {
      type: String,
      required: true
    }
  },
  emits: ['update:searchQuery', 'update:roleFilter']
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 