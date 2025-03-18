<template>
  <div id="app">
    <div class="app-container">
      <!-- Left Sidebar Navigation -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <h1>Tofu Monitor</h1>
        </div>
        <nav class="sidebar-nav">
          <router-link to="/" class="nav-item">
            <span class="nav-icon">📊</span>
            <span>Dashboard</span>
          </router-link>
          <router-link to="/metrics" class="nav-item" v-if="canViewDetailedMetrics">
            <span class="nav-icon">📈</span>
            <span>Metrics</span>
          </router-link>
          <router-link to="/users" class="nav-item" v-if="isAdmin">
            <span class="nav-icon">👥</span>
            <span>User Management</span>
          </router-link>
          <router-link to="/about" class="nav-item">
            <span class="nav-icon">ℹ️</span>
            <span>About</span>
          </router-link>
        </nav>
        
        <div class="sidebar-footer">
          <div class="user-info" v-if="currentUser">
            <div class="user-avatar">{{ userInitials }}</div>
            <div class="user-details">
              <div class="user-name">{{ displayName }}</div>
              <div class="user-role">{{ currentUser.role }}</div>
            </div>
          </div>
          
          <div class="auth-actions">
            <router-link v-if="!isAuthenticated" to="/login" class="login-button">
              Login
            </router-link>
            <button v-else class="logout-button" @click="handleLogout">
              Logout
            </button>
          </div>
        </div>
      </aside>
      
      <!-- Main Content Area -->
      <main class="content">
        <router-view/>
      </main>
    </div>
    
    <footer>
      <p>Tofu Monitor &copy; {{ new Date().getFullYear() }}</p>
    </footer>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import userStore, { PERMISSIONS } from './store/userStore'

export default {
  setup() {
    const router = useRouter()
    
    const currentUser = computed(() => userStore.currentUser())
    const isAuthenticated = computed(() => userStore.isAuthenticated())
    const isAdmin = computed(() => userStore.isAdmin())
    const canViewDetailedMetrics = computed(() => 
      userStore.hasPermission(PERMISSIONS.VIEW_DETAILED_METRICS)
    )
    
    const displayName = computed(() => {
      if (!currentUser.value) return 'Guest'
      return currentUser.value.name || currentUser.value.username || 'Guest'
    })
    
    const userInitials = computed(() => {
      if (!currentUser.value || !displayName.value || displayName.value === 'Guest') {
        return 'G'
      }
      
      // Get initials from the display name
      return displayName.value
        .split(' ')
        .map(n => n[0])
        .join('')
        .toUpperCase()
        .substring(0, 2)
    })
    
    const handleLogout = () => {
      userStore.logout()
      router.push('/login')
    }
    
    return {
      currentUser,
      isAuthenticated,
      isAdmin,
      canViewDetailedMetrics,
      displayName,
      userInitials,
      handleLogout
    }
  }
}
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
    Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: #f5f7fa;
  color: #333;
  overflow: hidden; /* Prevent body scrollbar */
}

#app {
  height: 100vh; /* Full viewport height */
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Prevent app scrollbar */
}

.app-container {
  flex: 1;
  display: flex;
  overflow: hidden; /* Prevent container scrollbar */
}

/* Sidebar Styles */
.sidebar {
  width: 250px;
  background-color: #2c3e50;
  color: white;
  display: flex;
  flex-direction: column;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  overflow-y: auto; /* Allow sidebar to scroll if needed */
}

.sidebar-header {
  padding: 1.5rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h1 {
  margin: 0;
  font-size: 1.5rem;
}

.sidebar-nav {
  padding: 1rem 0;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.nav-item {
  display: flex;
  align-items: center;
  color: #9cb3c9;
  text-decoration: none;
  padding: 0.75rem 1rem;
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
}

.nav-item:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

.nav-item.router-link-active {
  color: white;
  background-color: rgba(255, 255, 255, 0.05);
  border-left: 3px solid #42b983;
}

.nav-icon {
  margin-right: 10px;
  font-size: 1.1rem;
}

/* Sidebar Footer */
.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  margin-top: auto;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.user-avatar {
  width: 36px;
  height: 36px;
  background-color: #42b983;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 0.75rem;
}

.user-details {
  overflow: hidden;
}

.user-name {
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.8rem;
  color: #9cb3c9;
  text-transform: capitalize;
}

.auth-actions {
  display: flex;
}

.login-button, .logout-button {
  width: 100%;
  padding: 0.75rem;
  border-radius: 4px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button {
  background-color: #42b983;
  color: white;
  text-decoration: none;
}

.login-button:hover {
  background-color: #3aa876;
}

.logout-button {
  background-color: transparent;
  color: #9cb3c9;
  border: 1px solid #9cb3c9;
}

.logout-button:hover {
  background-color: rgba(255, 255, 255, 0.1);
  color: white;
}

/* Main Content Area */
.content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto; /* Only this container should scroll */
}

footer {
  background-color: #2c3e50;
  color: white;
  text-align: center;
  padding: 1rem;
}
</style> 