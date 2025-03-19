<template>
  <div class="access-denied">
    <svg viewBox="0 0 24 24" class="access-denied-icon">
      <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,7C13.4,7 14.8,8.1 14.8,9.5V11C15.4,11 16,11.6 16,12.3V15.8C16,16.4 15.4,17 14.7,17H9.2C8.6,17 8,16.4 8,15.7V12.2C8,11.6 8.6,11 9.2,11V9.5C9.2,8.1 10.6,7 12,7M12,8.2C11.2,8.2 10.5,8.7 10.5,9.5V11H13.5V9.5C13.5,8.7 12.8,8.2 12,8.2Z" />
    </svg>
    <h2>Access Denied</h2>
    <p>You don't have permission to manage users. Please contact your administrator.</p>
  </div>
</template>

<script>
export default {
  name: 'AccessDenied'
}
</script>

<style scoped>
@import '@/assets/css/user-styles.css';
</style> 