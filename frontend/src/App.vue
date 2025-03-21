<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <div class="app-container">
      <!-- Left Sidebar Navigation -->
      <aside class="sidebar">
        <div class="sidebar-header">
          <div class="logo">
            <svg viewBox="0 0 24 24" class="logo-icon">
              <path d="M12,2L1,21H23L12,2M12,6.7L16,13H8L12,6.7Z" />
            </svg>
            <h1>Kepler</h1>
          </div>
          <!-- Add stars for space theme -->
          <div class="stars">
            <div class="star"></div>
            <div class="star"></div>
            <div class="star"></div>
            <div class="star"></div>
            <div class="star"></div>
            <div class="star"></div>
            <div class="star"></div>
          </div>
        </div>
        <nav class="sidebar-nav">
          <router-link to="/" class="nav-item">
            <span class="nav-icon">
              <svg viewBox="0 0 24 24"><path d="M13,3V9H21V3M13,21H21V11H13M3,21H11V15H3M3,13H11V3H3V13Z" /></svg>
            </span>
            <span>Dashboard</span>
          </router-link>
          <router-link to="/metrics" class="nav-item" v-if="canViewDetailedMetrics">
            <span class="nav-icon">
              <svg viewBox="0 0 24 24"><path d="M16,11.78L20.24,4.45L21.97,5.45L16.74,14.5L10.23,10.75L5.46,19H22V21H2V3H4V17.54L9.5,8L16,11.78Z" /></svg>
            </span>
            <span>Metrics</span>
          </router-link>
          <router-link to="/users" class="nav-item" v-if="isAdmin">
            <span class="nav-icon">
              <svg viewBox="0 0 24 24"><path d="M12,5.5A3.5,3.5 0 0,1 15.5,9A3.5,3.5 0 0,1 12,12.5A3.5,3.5 0 0,1 8.5,9A3.5,3.5 0 0,1 12,5.5M5,8C5.56,8 6.08,8.15 6.53,8.42C6.38,9.85 6.8,11.27 7.66,12.38C7.16,13.34 6.16,14 5,14A3,3 0 0,1 2,11A3,3 0 0,1 5,8M19,8A3,3 0 0,1 22,11A3,3 0 0,1 19,14C17.84,14 16.84,13.34 16.34,12.38C17.2,11.27 17.62,9.85 17.47,8.42C17.92,8.15 18.44,8 19,8M5.5,18.25C5.5,16.18 8.41,14.5 12,14.5C15.59,14.5 18.5,16.18 18.5,18.25V20H5.5V18.25M0,20V18.5C0,17.11 1.89,15.94 4.45,15.6C3.86,16.28 3.5,17.22 3.5,18.25V20H0M24,20H20.5V18.25C20.5,17.22 20.14,16.28 19.55,15.6C22.11,15.94 24,17.11 24,18.5V20Z" /></svg>
            </span>
            <span>User Management</span>
          </router-link>
          <router-link to="/about" class="nav-item">
            <span class="nav-icon">
              <svg viewBox="0 0 24 24"><path d="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" /></svg>
            </span>
            <span>About</span>
          </router-link>
          <router-link to="/cursor-presentation" class="nav-item">
            <span class="nav-icon">
              <svg viewBox="0 0 24 24"><path d="M4 7V21H18V7H4M4 5H18C19.11 5 20 5.89 20 7V21C20 22.11 19.11 23 18 23H4C2.89 23 2 22.11 2 21V7C2 5.89 2.89 5 4 5M15.25 14C15.25 15.27 14.71 16.34 13.83 17.01L14.92 18.1C15.44 17.9 15.91 17.6 16.32 17.2C17.21 16.31 17.75 15.24 17.75 14C17.75 12.76 17.21 11.69 16.32 10.8C15.91 10.4 15.44 10.1 14.92 9.9L13.83 11C14.71 11.67 15.25 12.73 15.25 14M11.75 14C11.75 12.73 12.29 11.67 13.17 11L12.08 9.9C11.56 10.1 11.09 10.4 10.68 10.8C9.79 11.69 9.25 12.76 9.25 14C9.25 15.24 9.79 16.31 10.68 17.2C11.09 17.6 11.56 17.9 12.08 18.1L13.17 17C12.29 16.34 11.75 15.27 11.75 14M12.5 5.5L14 4L15.5 5.5H12.5Z" /></svg>
            </span>
            <span>Cursor Presentation</span>
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
              Sign in
            </router-link>
            <button v-else class="logout-button" @click="handleLogout">
              Sign out
            </button>
          </div>
        </div>
      </aside>
      
      <!-- Main Content Area -->
      <main class="content">
        <header class="content-header">
          <div class="page-title">
            <h1>{{ $route.name }}</h1>
          </div>
          <div class="header-actions">
            <div class="theme-toggle" @click="toggleDarkMode">
              <svg v-if="!isDarkMode" viewBox="0 0 24 24" class="theme-icon">
                <path d="M12,18C11.11,18 10.26,17.8 9.5,17.45C11.56,16.5 13,14.42 13,12C13,9.58 11.56,7.5 9.5,6.55C10.26,6.2 11.11,6 12,6A6,6 0 0,1 18,12A6,6 0 0,1 12,18M20,8.69V4H15.31L12,0.69L8.69,4H4V8.69L0.69,12L4,15.31V20H8.69L12,23.31L15.31,20H20V15.31L23.31,12L20,8.69Z" />
              </svg>
              <svg v-else viewBox="0 0 24 24" class="theme-icon">
                <path d="M17.75,4.09L15.22,6.03L16.13,9.09L13.5,7.28L10.87,9.09L11.78,6.03L9.25,4.09L12.44,4L13.5,1L14.56,4L17.75,4.09M21.25,11L19.61,12.25L20.2,14.23L18.5,13.06L16.8,14.23L17.39,12.25L15.75,11L17.81,10.95L18.5,9L19.19,10.95L21.25,11M18.97,15.95C19.8,15.87 20.69,17.05 20.16,17.8C19.84,18.25 19.5,18.67 19.08,19.07C15.17,23 8.84,23 4.94,19.07C1.03,15.17 1.03,8.83 4.94,4.93C5.34,4.53 5.76,4.17 6.21,3.85C6.96,3.32 8.14,4.21 8.06,5.04C7.79,7.9 8.75,10.87 10.95,13.06C13.14,15.26 16.1,16.22 18.97,15.95M17.33,17.97C14.5,17.81 11.7,16.64 9.53,14.5C7.36,12.31 6.2,9.5 6.04,6.68C3.23,9.82 3.34,14.64 6.35,17.66C9.37,20.67 14.19,20.78 17.33,17.97Z" />
              </svg>
            </div>
          </div>
        </header>
        <div class="content-wrapper">
          <router-view v-slot="{ Component }">
            <transition name="fade" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </div>
      </main>
    </div>
    
    <footer>
      <p>Kepler &copy; {{ new Date().getFullYear() }} by Valtech</p>
    </footer>
  </div>
</template>

<script>
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import userStore, { PERMISSIONS } from './store/userStore'

export default {
  setup() {
    const router = useRouter()
    const isDarkMode = ref(localStorage.getItem('darkMode') === 'true')
    
    // Watch for dark mode changes and update root class
    watch(isDarkMode, (newValue) => {
      if (newValue) {
        document.documentElement.classList.add('dark-mode')
      } else {
        document.documentElement.classList.remove('dark-mode')
      }
    }, { immediate: true })
    
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
    
    // Toggle dark mode
    const toggleDarkMode = () => {
      isDarkMode.value = !isDarkMode.value
      localStorage.setItem('darkMode', isDarkMode.value)
    }
    
    return {
      currentUser,
      isAuthenticated,
      isAdmin,
      canViewDetailedMetrics,
      displayName,
      userInitials,
      handleLogout,
      isDarkMode,
      toggleDarkMode
    }
  }
}
</script>

<style>
:root {
  /* Modern Color Palette */
  --primary: #3a86ff;
  --primary-light: #4d9aff;
  --primary-dark: #2b6fd9;
  --secondary: #fb5607;
  --accent: #ffbe0b;
  --danger: #ff006e;
  --success: #22c55e;
  --dark: #0a2540;
  --light: #f8fafc;
  --gray: #64748b;
  --gray-light: #e2e8f0;
  --gray-dark: #334155;
  
  /* Shadow & Effects */
  --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-md: 0 6px 12px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  --radius-sm: 4px;
  --radius: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-full: 9999px;
  --transition: all 0.2s ease;
  
  /* Light mode (default) */
  --bg-body: #f8fafc;
  --bg-primary: #ffffff;
  --bg-secondary: #ffffff;
  --bg-card: #ffffff;
  --text-primary: #0a2540;
  --text-secondary: #64748b;
  --border-color: #e2e8f0;
}

/* Dark mode */
:root.dark-mode {
  --primary: #60a5fa;
  --primary-light: #93c5fd;
  --primary-dark: #3b82f6;
  --secondary: #fb5607;
  --accent: #fbbf24;
  --bg-body: #0f172a;
  --bg-primary: #1e293b;
  --bg-secondary: #1e293b;
  --bg-card: #1e293b;
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
  --border-color: #334155;
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  margin: 0;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu,
    Cantarell, 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--bg-body);
  color: var(--text-primary);
  overflow: hidden;
  line-height: 1.6;
  transition: background-color 0.3s ease, color 0.3s ease;
}

#app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background-color: var(--bg-body);
}

.app-container {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* Sidebar Styles */
.sidebar {
  width: 280px;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow);
  overflow-y: auto;
  z-index: 10;
  border-right: 1px solid var(--border-color);
  transition: width 0.3s ease;
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

/* Planet effect behind the logo */
.sidebar-header::after {
  content: "";
  position: absolute;
  width: 120px;
  height: 120px;
  top: -50px;
  right: -50px;
  background: radial-gradient(circle, rgba(42, 157, 143, 0.15) 0%, rgba(58, 134, 255, 0.1) 50%, transparent 80%);
  border-radius: 50%;
  z-index: -1;
  box-shadow: 0 0 30px rgba(42, 157, 143, 0.1);
}

/* Planet ring effect */
.sidebar-header::before {
  content: "";
  position: absolute;
  width: 140px;
  height: 30px;
  top: -5px;
  right: -60px;
  border: 2px solid rgba(58, 134, 255, 0.1);
  border-radius: 50%;
  transform: rotateX(70deg);
  z-index: -1;
  box-shadow: inset 0 0 15px rgba(58, 134, 255, 0.2);
  animation: rotate-ring 20s linear infinite;
}

/* Add tiny stars */
.sidebar-header .stars {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -2;
  overflow: hidden;
}

.sidebar-header .star {
  position: absolute;
  width: 2px;
  height: 2px;
  background-color: white;
  border-radius: 50%;
  opacity: 0.6;
  animation: twinkle 4s infinite ease-in-out;
}

.sidebar-header .star:nth-child(1) {
  top: 25%;
  left: 15%;
  animation-delay: 0s;
}

.sidebar-header .star:nth-child(2) {
  top: 35%;
  left: 30%;
  width: 1px;
  height: 1px;
  animation-delay: 0.5s;
}

.sidebar-header .star:nth-child(3) {
  top: 65%;
  left: 10%;
  width: 1.5px;
  height: 1.5px;
  animation-delay: 1s;
}

.sidebar-header .star:nth-child(4) {
  top: 75%;
  left: 35%;
  animation-delay: 1.5s;
}

.sidebar-header .star:nth-child(5) {
  top: 20%;
  left: 50%;
  width: 1px;
  height: 1px;
  animation-delay: 2s;
}

.sidebar-header .star:nth-child(6) {
  top: 45%;
  left: 20%;
  animation-delay: 2.5s;
}

.sidebar-header .star:nth-child(7) {
  top: 55%;
  left: 55%;
  width: 1.5px;
  height: 1.5px;
  animation-delay: 3s;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.4; transform: scale(1); }
  50% { opacity: 0.9; transform: scale(1.2); }
}

@keyframes rotate-ring {
  from { transform: rotateX(70deg) rotateZ(0deg); }
  to { transform: rotateX(70deg) rotateZ(360deg); }
}

.logo {
  display: flex;
  align-items: center;
  position: relative;
}

/* Add glow halo effect */
.logo::before {
  content: "";
  position: absolute;
  width: 40px;
  height: 40px;
  left: -4px;
  top: -4px;
  background: radial-gradient(circle, rgba(58, 134, 255, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  filter: blur(5px);
  z-index: 0;
}

.logo-icon {
  width: 32px;
  height: 32px;
  margin-right: 0.75rem;
  fill: var(--primary);
  position: relative;
  z-index: 1;
}

.sidebar-header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: -0.5px;
  position: relative;
  z-index: 1;
}

.sidebar-nav {
  padding: 1.5rem 0;
  display: flex;
  flex-direction: column;
  flex: 1;
  position: relative;
}

/* Grid background for navigation */
.sidebar-nav::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(to right, rgba(58, 134, 255, 0.05) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(58, 134, 255, 0.05) 1px, transparent 1px);
  background-size: 20px 20px;
  opacity: 0.3;
  z-index: -1;
  pointer-events: none;
}

/* Add a subtle space gradient to the navigation area */
.sidebar-nav::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(ellipse at 10% 20%, rgba(58, 134, 255, 0.05) 0%, transparent 50%),
    radial-gradient(ellipse at 90% 80%, rgba(42, 157, 143, 0.06) 0%, transparent 60%);
  z-index: -2;
  pointer-events: none;
}

.nav-item {
  display: flex;
  align-items: center;
  color: var(--text-secondary);
  text-decoration: none;
  padding: 0.85rem 1.5rem;
  margin: 0.5rem 0.75rem;
  border-radius: var(--radius);
  transition: all 0.3s cubic-bezier(0.17, 0.67, 0.83, 0.67);
  font-weight: 500;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(5px);
  border: 1px solid transparent;
}

.nav-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(120deg, transparent, rgba(58, 134, 255, 0.05), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
  z-index: -1;
}

.nav-item:hover {
  background-color: rgba(58, 134, 255, 0.08);
  color: var(--primary);
  transform: translateX(4px) scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border-left: 1px solid rgba(58, 134, 255, 0.3);
}

.nav-item:hover::before {
  transform: translateX(100%);
}

.nav-item.router-link-active {
  color: var(--primary);
  background-color: rgba(58, 134, 255, 0.12);
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(58, 134, 255, 0.2);
  border-left: 2px solid var(--primary);
}

.nav-item.router-link-active::after {
  content: '';
  position: absolute;
  width: 3px;
  height: 70%;
  background: linear-gradient(to bottom, var(--primary), var(--primary-light));
  left: 0;
  top: 15%;
  border-radius: 0 2px 2px 0;
  box-shadow: 0 0 12px rgba(58, 134, 255, 0.8);
  animation: glow 2s infinite alternate;
}

@keyframes glow {
  0% { box-shadow: 0 0 8px rgba(58, 134, 255, 0.6); }
  100% { box-shadow: 0 0 16px rgba(58, 134, 255, 0.9); }
}

.nav-icon {
  margin-right: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  background-color: rgba(58, 134, 255, 0.08);
  border-radius: var(--radius);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.nav-icon::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at center, rgba(58, 134, 255, 0.2) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-item:hover .nav-icon {
  background-color: rgba(58, 134, 255, 0.18);
  transform: rotate(-5deg) scale(1.1);
  box-shadow: 0 0 8px rgba(58, 134, 255, 0.2);
}

.nav-item:hover .nav-icon::before {
  opacity: 1;
}

.nav-item.router-link-active .nav-icon {
  background-color: rgba(58, 134, 255, 0.25);
  box-shadow: 0 0 12px rgba(58, 134, 255, 0.25);
}

.nav-icon svg {
  width: 18px;
  height: 18px;
  fill: currentColor;
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 1px rgba(0, 0, 0, 0.1));
}

.nav-item:hover .nav-icon svg {
  transform: scale(1.15);
  filter: drop-shadow(0 0 4px rgba(58, 134, 255, 0.4));
  animation: float 1s ease-in-out infinite alternate;
}

.nav-item.router-link-active .nav-icon svg {
  filter: drop-shadow(0 0 5px rgba(58, 134, 255, 0.5));
}

@keyframes float {
  0% { transform: translateY(0) scale(1.15); }
  100% { transform: translateY(-2px) scale(1.15); }
}

/* Add subtle animation to nav text */
.nav-item span:not(.nav-icon) {
  position: relative;
  transition: all 0.3s ease;
}

.nav-item:hover span:not(.nav-icon) {
  transform: translateX(2px);
  text-shadow: 0 0 8px rgba(58, 134, 255, 0.3);
}

.nav-item.router-link-active span:not(.nav-icon) {
  text-shadow: 0 0 5px rgba(58, 134, 255, 0.4);
}

/* Add cosmic particles to active nav item */
.nav-item.router-link-active::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 20% 30%, rgba(58, 134, 255, 0.15) 0%, transparent 15%),
    radial-gradient(circle at 80% 70%, rgba(58, 134, 255, 0.1) 0%, transparent 20%);
  z-index: -1;
}

/* Sidebar Footer */
.sidebar-footer {
  padding: 1.5rem;
  border-top: 1px solid var(--border-color);
  margin-top: auto;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.user-avatar {
  width: 40px;
  height: 40px;
  background-color: var(--primary);
  color: white;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 0.75rem;
  font-size: 0.875rem;
  box-shadow: 0 2px 6px rgba(58, 134, 255, 0.3);
}

.user-details {
  overflow: hidden;
}

.user-name {
  font-weight: 600;
  color: var(--text-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.user-role {
  font-size: 0.8rem;
  color: var(--gray);
  text-transform: capitalize;
}

.auth-actions {
  display: flex;
}

.login-button, .logout-button {
  width: 100%;
  padding: 0.75rem;
  border-radius: var(--radius);
  text-align: center;
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
  border: none;
  font-size: 0.9rem;
}

.login-button {
  background-color: var(--primary);
  color: white;
  text-decoration: none;
  box-shadow: 0 2px 6px rgba(58, 134, 255, 0.3);
}

.login-button:hover {
  background-color: var(--primary-dark);
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(58, 134, 255, 0.4);
}

.logout-button {
  background-color: transparent;
  color: var(--gray-dark);
  border: 1px solid var(--gray-light);
}

.logout-button:hover {
  background-color: rgba(255, 0, 110, 0.05);
  color: var(--danger);
  border-color: var(--danger);
}

/* Content Styles */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.content-header {
  padding: 1.25rem 2rem;
  background-color: var(--bg-secondary);
  backdrop-filter: blur(8px);
  box-shadow: var(--shadow-sm);
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

/* Add subtle space background to header */
.content-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 80% 20%, rgba(58, 134, 255, 0.05) 0%, transparent 50%),
    radial-gradient(circle at 20% 80%, rgba(42, 157, 143, 0.04) 0%, transparent 40%);
  opacity: 0.7;
  z-index: -1;
}

.page-title h1 {
  font-size: 1.6rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.5px;
  position: relative;
  display: inline-block;
}

/* Add underline glow effect to page title */
.page-title h1::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 30%;
  height: 2px;
  background: linear-gradient(to right, var(--primary), transparent);
  border-radius: var(--radius);
  opacity: 0.8;
  box-shadow: 0 0 8px rgba(58, 134, 255, 0.5);
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-toggle {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: var(--transition);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
}

.theme-toggle:hover {
  background-color: var(--bg-secondary);
  transform: rotate(15deg);
}

.theme-icon {
  width: 20px;
  height: 20px;
  fill: var(--text-secondary);
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background-color: var(--bg-body);
  position: relative;
}

/* Add subtle grid to content background */
.content-wrapper::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    linear-gradient(to right, rgba(58, 134, 255, 0.03) 1px, transparent 1px),
    linear-gradient(to bottom, rgba(58, 134, 255, 0.03) 1px, transparent 1px);
  background-size: 30px 30px;
  z-index: -1;
  pointer-events: none;
}

footer {
  background-color: var(--bg-secondary);
  text-align: center;
  padding: 1rem;
  box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.05);
  color: var(--text-secondary);
  font-size: 0.875rem;
  border-top: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

/* Add subtle star effect to footer */
footer::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: radial-gradient(circle at 10% 50%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
                    radial-gradient(circle at 30% 70%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
                    radial-gradient(circle at 50% 30%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
                    radial-gradient(circle at 70% 60%, rgba(255, 255, 255, 0.1) 1px, transparent 1px),
                    radial-gradient(circle at 90% 40%, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
  background-size: 100px 100px;
  opacity: 0.5;
  z-index: 0;
}

footer p {
  position: relative;
  z-index: 1;
}

/* Card Styles */
.card {
  background-color: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: all 0.3s cubic-bezier(0.17, 0.67, 0.83, 0.67);
  overflow: hidden;
  position: relative;
}

/* Add subtle gradient background to card */
.card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(58, 134, 255, 0.03) 0%, transparent 50%, rgba(42, 157, 143, 0.02) 100%);
  opacity: 0.6;
  z-index: 0;
  pointer-events: none;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
  border-color: rgba(58, 134, 255, 0.2);
}

.card-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: relative;
  z-index: 1;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  position: relative;
  z-index: 1;
  display: inline-block;
}

/* Add glow effect to card title */
.card-title::before {
  content: "";
  position: absolute;
  top: 50%;
  left: -10px;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background-color: var(--primary);
  opacity: 0.8;
  box-shadow: 0 0 10px 2px rgba(58, 134, 255, 0.3);
  transform: translateY(-50%);
  z-index: -1;
}

.card-body {
  padding: 1.25rem;
  position: relative;
  z-index: 1;
}

.card-footer {
  padding: 1.25rem;
  border-top: 1px solid var(--border-color);
  position: relative;
  z-index: 1;
}

/* Button Styles */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  border-radius: var(--radius);
  font-weight: 500;
  transition: var(--transition);
  cursor: pointer;
  border: none;
  font-size: 0.875rem;
}

.btn-primary {
  background-color: var(--primary);
  color: white;
  box-shadow: 0 2px 4px rgba(58, 134, 255, 0.3);
}

.btn-primary:hover {
  background-color: var(--primary-dark);
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(58, 134, 255, 0.4);
}

.btn-secondary {
  background-color: var(--secondary);
  color: white;
  box-shadow: 0 2px 4px rgba(251, 86, 7, 0.3);
}

.btn-secondary:hover {
  background-color: #e64a00;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px rgba(251, 86, 7, 0.4);
}

.btn-outline {
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}

.btn-outline:hover {
  background-color: var(--bg-secondary);
  border-color: var(--primary);
  color: var(--primary);
}

/* Badge Styles */
.badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-full);
  font-size: 0.75rem;
  font-weight: 500;
}

.badge-primary {
  background-color: rgba(58, 134, 255, 0.1);
  color: var(--primary);
}

.badge-success {
  background-color: rgba(34, 197, 94, 0.1);
  color: var(--success);
}

.badge-danger {
  background-color: rgba(255, 0, 110, 0.1);
  color: var(--danger);
}

.badge-warning {
  background-color: rgba(251, 191, 36, 0.1);
  color: var(--accent);
}

/* Form Controls */
.form-control {
  display: block;
  width: 100%;
  padding: 0.5rem 0.75rem;
  font-size: 0.875rem;
  border-radius: var(--radius);
  border: 1px solid var(--border-color);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  transition: var(--transition);
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.15);
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-primary);
}

.form-group {
  margin-bottom: 1rem;
}

/* Transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    width: 64px;
  }

  .sidebar-header h1,
  .nav-item span:not(.nav-icon),
  .user-details {
    display: none;
  }

  .sidebar-footer {
    padding: 1rem 0.5rem;
  }

  .user-avatar {
    margin-right: 0;
  }
  
  .content-wrapper {
    padding: 1rem;
  }
  
  .content-header {
    padding: 1rem;
  }
}
</style> 