import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import userStore, { PERMISSIONS } from '../store/userStore'

const routes = [
  {
    path: '/',
    name: 'dashboard',
    component: DashboardView,
    meta: {
      requiresAuth: false,
      permissions: [PERMISSIONS.VIEW_DASHBOARD]
    }
  },
  {
    path: '/metrics',
    name: 'metrics',
    component: () => import(/* webpackChunkName: "metrics" */ '../views/MetricsView.vue'),
    meta: {
      requiresAuth: false,
      permissions: [PERMISSIONS.VIEW_DETAILED_METRICS]
    }
  },
  {
    path: '/users',
    name: 'users',
    component: () => import(/* webpackChunkName: "users" */ '../views/UsersView.vue'),
    meta: {
      requiresAuth: true,
      permissions: [PERMISSIONS.MANAGE_USERS]
    }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import(/* webpackChunkName: "login" */ '../views/LoginView.vue'),
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/about',
    name: 'about',
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
    meta: {
      requiresAuth: false
    }
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Navigation guard for permissions
router.beforeEach((to, from, next) => {
  // Initialize auth in case it hasn't been initialized yet
  if (!userStore.state.currentUser) {
    userStore.initAuth()
  }
  
  // Allow access to login page
  if (to.name === 'login') {
    next()
    return
  }
  
  // Check if the route requires authentication
  if (to.meta.requiresAuth && !userStore.isAuthenticated()) {
    next({ name: 'login' })
    return
  }
  
  // Check for required permissions
  if (to.meta.permissions && to.meta.permissions.length > 0) {
    // Check if the user has at least one of the required permissions
    const hasPermission = to.meta.permissions.some(permission => 
      userStore.hasPermission(permission)
    )
    
    if (!hasPermission) {
      // If user is not logged in, direct to login
      if (!userStore.isAuthenticated()) {
        next({ name: 'login' })
      } else {
        // Otherwise, redirect to dashboard
        next({ name: 'dashboard' })
      }
      return
    }
  }
  
  next()
})

export default router 