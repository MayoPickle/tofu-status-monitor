<template>
  <div id="app" :class="{ 'dark-mode': isDarkMode }">
    <div class="app-container">
      <!-- Left Sidebar Navigation -->
      <aside class="sidebar">
        <!-- Space theme elements -->
        <div class="space-elements">
          <div class="star-particle" v-for="n in 15" :key="`star-${n}`" :style="{ 
            top: Math.random() * 100 + '%', 
            left: Math.random() * 100 + '%',
            width: (Math.random() * 2 + 1) + 'px',
            height: (Math.random() * 2 + 1) + 'px',
            animationDelay: Math.random() * 4 + 's'
          }"></div>
          <div class="orbit-line"></div>
        </div>
        
        <div class="sidebar-header">
          <div class="logo">
            <svg viewBox="0 0 24 24" class="logo-icon">
              <path d="M12,2L1,21H23L12,2M12,6.7L16,13H8L12,6.7Z" />
            </svg>
            <h1>Kepler</h1>
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
  transition: width 0.3s ease, background-color 0.3s ease;
  position: relative;
}

/* Space background for sidebar */
.sidebar::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 80% 10%, rgba(42, 157, 143, 0.08) 0%, transparent 30%),
    radial-gradient(circle at 10% 90%, rgba(58, 134, 255, 0.06) 0%, transparent 30%);
  opacity: 0.6;
  z-index: -1;
  pointer-events: none;
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

@keyframes rotate-ring {
  from { transform: rotateX(70deg) rotateZ(0deg); }
  to { transform: rotateX(70deg) rotateZ(360deg); }
}

.logo {
  display: flex;
  align-items: center;
  position: relative;
}

.logo-icon {
  width: 32px;
  height: 32px;
  margin-right: 0.75rem;
  fill: var(--primary);
  filter: drop-shadow(0 2px 8px rgba(58, 134, 255, 0.5));
  animation: pulse 3s infinite ease-in-out;
  position: relative;
  z-index: 1;
}

/* Add glow effect to the icon */
.logo-icon path {
  fill: var(--primary);
  filter: drop-shadow(0 0 5px var(--primary));
}

@keyframes pulse {
  0%, 100% {
    filter: drop-shadow(0 2px 4px rgba(58, 134, 255, 0.4));
    transform: scale(1);
  }
  50% {
    filter: drop-shadow(0 4px 12px rgba(58, 134, 255, 0.7));
    transform: scale(1.05);
  }
}

.sidebar-header h1 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--primary);
  letter-spacing: -0.5px;
  text-shadow: 0 0 10px rgba(58, 134, 255, 0.3);
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

/* Add meteor effect */
@keyframes meteor {
  0% {
    transform: translateX(0) translateY(0) rotate(45deg);
    opacity: 1;
  }
  70% {
    opacity: 1;
  }
  100% {
    transform: translateX(-500px) translateY(500px) rotate(45deg);
    opacity: 0;
  }
}

.sidebar::after {
  content: "";
  position: absolute;
  top: -100px;
  right: -100px;
  width: 200px;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.4));
  box-shadow: 0 0 10px 1px rgba(255, 255, 255, 0.2);
  transform: rotate(45deg);
  animation: meteor 8s linear infinite;
  animation-delay: 3s;
  z-index: 0;
  pointer-events: none;
}

/* Add a second, smaller meteor */
.sidebar::before {
  content: "";
  position: absolute;
  top: 30%;
  right: -50px;
  width: 100px;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.4));
  box-shadow: 0 0 6px 1px rgba(255, 255, 255, 0.1);
  transform: rotate(45deg);
  animation: meteor 12s linear infinite;
  animation-delay: 8s;
  z-index: 0;
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
  position: relative;
  backdrop-filter: blur(8px);
}

.sidebar-footer::before {
  content: "";
  position: absolute;
  top: 0;
  left: 5%;
  right: 5%;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--primary), transparent);
  opacity: 0.2;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
  position: relative;
  z-index: 1;
}

.user-avatar {
  width: 44px;
  height: 44px;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  color: white;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-right: 0.75rem;
  font-size: 0.875rem;
  box-shadow: 0 3px 8px rgba(58, 134, 255, 0.4);
  position: relative;
  overflow: hidden;
  border: 2px solid rgba(255, 255, 255, 0.1);
}

.user-avatar::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
}

.user-avatar::after {
  content: "";
  position: absolute;
  width: 150%;
  height: 150%;
  top: -25%;
  left: -25%;
  background: linear-gradient(to bottom right, transparent, rgba(255, 255, 255, 0.3), transparent);
  transform: rotate(45deg);
  animation: shimmer 3s infinite linear;
}

@keyframes shimmer {
  0% { transform: translateX(-100%) rotate(45deg); }
  100% { transform: translateX(100%) rotate(45deg); }
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
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.user-role {
  font-size: 0.8rem;
  color: var(--primary);
  text-transform: capitalize;
  opacity: 0.9;
  position: relative;
}

.user-role::after {
  content: "";
  position: absolute;
  height: 1px;
  background: linear-gradient(to right, var(--primary), transparent);
  width: 100%;
  left: 0;
  bottom: -2px;
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
  transition: all 0.3s cubic-bezier(0.17, 0.67, 0.83, 0.67);
  font-weight: 500;
  border: none;
  font-size: 0.9rem;
  position: relative;
  overflow: hidden;
}

.login-button::before, .logout-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(120deg, transparent, rgba(255, 255, 255, 0.1), transparent);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.login-button:hover::before, .logout-button:hover::before {
  transform: translateX(100%);
}

.login-button {
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: white;
  text-decoration: none;
  box-shadow: 0 2px 6px rgba(58, 134, 255, 0.3);
}

.login-button:hover {
  background: linear-gradient(135deg, var(--primary-dark), var(--primary));
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(58, 134, 255, 0.4);
}

.logout-button {
  background-color: transparent;
  color: var(--gray-dark);
  border: 1px solid var(--gray-light);
  backdrop-filter: blur(4px);
}

.logout-button:hover {
  background-color: rgba(255, 0, 110, 0.08);
  color: var(--danger);
  border-color: var(--danger);
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(255, 0, 110, 0.15);
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
  padding: 1rem 2rem;
  background-color: var(--bg-secondary);
  backdrop-filter: blur(8px);
  box-shadow: var(--shadow-sm);
  z-index: 5;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-color);
}

.page-title h1 {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
  letter-spacing: -0.5px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.theme-toggle {
  width: 42px;
  height: 42px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: linear-gradient(135deg, var(--bg-primary) 0%, var(--bg-secondary) 100%);
  border: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
}

.theme-toggle::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(58, 134, 255, 0.1) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.theme-toggle:hover {
  background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
  transform: rotate(15deg) scale(1.1);
  box-shadow: 0 0 15px rgba(58, 134, 255, 0.2);
  border-color: rgba(58, 134, 255, 0.3);
}

.theme-toggle:hover::before {
  opacity: 1;
}

.theme-icon {
  width: 22px;
  height: 22px;
  fill: var(--text-secondary);
  transition: all 0.3s ease;
  filter: drop-shadow(0 1px 2px rgba(0, 0, 0, 0.1));
}

.theme-toggle:hover .theme-icon {
  fill: var(--primary);
  transform: scale(1.1);
  filter: drop-shadow(0 0 4px rgba(58, 134, 255, 0.4));
}

.content-wrapper {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
  background-color: var(--bg-body);
}

footer {
  background-color: var(--bg-secondary);
  text-align: center;
  padding: 1rem;
  box-shadow: 0 -1px 3px rgba(0, 0, 0, 0.05);
  color: var(--text-secondary);
  font-size: 0.875rem;
  border-top: 1px solid var(--border-color);
}

/* Card Styles */
.card {
  background-color: var(--bg-card);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow);
  border: 1px solid var(--border-color);
  transition: var(--transition);
  overflow: hidden;
}

.card:hover {
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.card-header {
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.card-body {
  padding: 1.25rem;
}

.card-footer {
  padding: 1.25rem;
  border-top: 1px solid var(--border-color);
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

/* Additional Space Theme Elements */
.space-elements {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  pointer-events: none;
  z-index: -1;
}

.star-particle {
  position: absolute;
  background-color: white;
  border-radius: 50%;
  opacity: 0.4;
  animation: twinkle 4s infinite ease-in-out;
  z-index: 0;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(1); }
  50% { opacity: 0.7; transform: scale(1.3); }
}

.orbit-line {
  position: absolute;
  width: 200px;
  height: 300px;
  top: 40%;
  left: 50%;
  transform: translate(-50%, -50%) rotateX(80deg) rotateZ(10deg);
  border: 1px dashed rgba(58, 134, 255, 0.1);
  border-radius: 50%;
  z-index: 0;
  animation: orbit-rotate 20s linear infinite;
}

@keyframes orbit-rotate {
  from { transform: translate(-50%, -50%) rotateX(80deg) rotateZ(0deg); }
  to { transform: translate(-50%, -50%) rotateX(80deg) rotateZ(360deg); }
}
</style> 