import { reactive, readonly } from 'vue'
import axios from 'axios'

// API base URL
const API_URL = process.env.VUE_APP_API_URL || 'http://localhost:8000'

// User roles
export const ROLES = {
  ADMIN: 'admin',
  MAINTAINER: 'maintainer',
  USER: 'user',
  GUEST: 'guest'
}

// 全局功能权限
export const PERMISSIONS = {
  // 视图权限
  VIEW_DASHBOARD: 'view_dashboard',        // 查看仪表板
  VIEW_OVERALL_STATUS: 'view_overall_status', // 查看整体状态
  VIEW_DETAILED_METRICS: 'view_detailed_metrics', // 查看详细指标
  VIEW_ALERTS: 'view_alerts',              // 查看警报
  
  // 管理权限
  MANAGE_USERS: 'manage_users',            // 管理用户
  MANAGE_SYSTEM: 'manage_system',          // 管理系统配置
}

// 站点特定权限
export const SITE_PERMISSIONS = {
  SITE_VIEW: 'site_view',                  // 查看站点基本状态
  SITE_VIEW_METRICS: 'site_view_metrics',  // 查看站点详细指标
  SITE_CONFIGURE: 'site_configure',        // 配置站点
  SITE_ADD: 'site_add',                    // 添加站点
  SITE_EDIT: 'site_edit',                  // 编辑站点
  SITE_DELETE: 'site_delete',              // 删除站点
}

// 数据访问权限
export const DATA_PERMISSIONS = {
  ACCESS_REALTIME: 'access_realtime',      // 访问实时数据
  ACCESS_HISTORICAL: 'access_historical',  // 访问历史数据
  ACCESS_UPTIME: 'access_uptime',          // 访问正常运行时间数据
  EXPORT_DATA: 'export_data',              // 导出数据
}

// 基于角色的全局权限映射
const roleGlobalPermissions = {
  [ROLES.ADMIN]: [
    // 所有全局权限
    ...Object.values(PERMISSIONS),
    // 所有数据权限
    ...Object.values(DATA_PERMISSIONS)
  ],
  [ROLES.MAINTAINER]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_OVERALL_STATUS,
    PERMISSIONS.VIEW_DETAILED_METRICS,
    PERMISSIONS.VIEW_ALERTS,
    DATA_PERMISSIONS.ACCESS_REALTIME,
    DATA_PERMISSIONS.ACCESS_HISTORICAL,
    DATA_PERMISSIONS.ACCESS_UPTIME,
  ],
  [ROLES.USER]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_OVERALL_STATUS,
    PERMISSIONS.VIEW_DETAILED_METRICS,
    DATA_PERMISSIONS.ACCESS_REALTIME,
    DATA_PERMISSIONS.ACCESS_UPTIME,
  ],
  [ROLES.GUEST]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_OVERALL_STATUS,
    DATA_PERMISSIONS.ACCESS_REALTIME,
  ]
}

// 基于角色的默认站点权限 - 仅用于创建新用户时的初始化
const roleDefaultSitePermissions = {
  [ROLES.ADMIN]: [
    ...Object.values(SITE_PERMISSIONS)
  ],
  [ROLES.MAINTAINER]: [
    SITE_PERMISSIONS.SITE_VIEW,
    SITE_PERMISSIONS.SITE_VIEW_METRICS,
    SITE_PERMISSIONS.SITE_CONFIGURE,
    SITE_PERMISSIONS.SITE_EDIT
  ],
  [ROLES.USER]: [
    SITE_PERMISSIONS.SITE_VIEW,
    SITE_PERMISSIONS.SITE_VIEW_METRICS
  ],
  [ROLES.GUEST]: [
    SITE_PERMISSIONS.SITE_VIEW
  ]
}

// 创建最小状态，只保存当前用户和认证信息
const state = reactive({
  currentUser: null,
  isAuthenticated: false,
  accessToken: null,
  loading: false,
  error: null
})

// HTTP client setup
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  },
  timeout: 10000 // 10 seconds timeout
})

// Add request interceptor for authorization
api.interceptors.request.use(config => {
  // Add authorization header if we have a token
  if (state.accessToken) {
    config.headers.Authorization = `Bearer ${state.accessToken}`
  }
  return config
})

// Getter methods
const getters = {
  isAuthenticated: () => state.isAuthenticated,
  currentUser: () => state.currentUser,
  
  // 检查全局权限
  hasPermission: (permission) => {
    if (!state.currentUser) {
      return false
    }
    
    const userRole = state.currentUser.role
    return roleGlobalPermissions[userRole]?.includes(permission) || false
  },
  
  // 检查数据访问权限
  hasDataPermission: (permission) => {
    if (!state.currentUser) {
      return false
    }
    
    const userRole = state.currentUser.role
    return roleGlobalPermissions[userRole]?.includes(permission) || false
  },
  
  // 检查站点权限
  hasSitePermission: (siteId, permission) => {
    if (!state.currentUser) {
      return false
    }
    
    // 管理员拥有所有站点的所有权限
    if (state.currentUser.role === ROLES.ADMIN) {
      return true
    }
    
    // 检查用户特定站点权限
    return state.currentUser.sitePermissions?.[siteId]?.includes(permission) || false
  },
  
  // 获取用户可访问的站点列表 (同步方法)
  getAccessibleSites: () => {
    if (!state.currentUser) {
      return ['main'] // 返回默认站点，确保至少有一个站点可访问
    }
    
    // 管理员和维护人员可以访问所有站点
    if (state.currentUser.role === ROLES.ADMIN || state.currentUser.role === ROLES.MAINTAINER) {
      return ['main', 'backup', 'staging'] // 返回所有已知站点
    }
    
    // 其他用户只能访问有权限的站点
    const userSites = Object.keys(state.currentUser.sitePermissions || {})
    return userSites.length > 0 ? userSites : ['main'] // 确保至少有一个站点
  },
  
  // 检查是否可以访问特定站点
  canAccessSite: (siteId) => {
    if (!state.currentUser) {
      return false
    }
    
    // 管理员和维护人员可以访问所有站点
    if (state.currentUser.role === ROLES.ADMIN || state.currentUser.role === ROLES.MAINTAINER) {
      return true
    }
    
    // 其他用户检查站点权限
    return !!state.currentUser.sitePermissions?.[siteId]
  },
  
  isAdmin: () => state.currentUser?.role === ROLES.ADMIN,
  isMaintainer: () => state.currentUser?.role === ROLES.MAINTAINER,
  isUser: () => state.currentUser?.role === ROLES.USER,
  isGuest: () => !state.isAuthenticated || state.currentUser?.role === ROLES.GUEST
}

// Actions
const actions = {
  // Register a new user
  register: async (userData) => {
    state.loading = true
    state.error = null
    
    try {
      const response = await api.post('/register', userData)
      return response.data
    } catch (error) {
      state.error = error.response?.data?.detail || 'Registration failed'
      throw new Error(state.error)
    } finally {
      state.loading = false
    }
  },
  
  // Login action
  login: async (username, password) => {
    state.loading = true
    state.error = null
    
    try {
      // Get token
      const formData = new FormData()
      formData.append('username', username)
      formData.append('password', password)
      
      const tokenResponse = await api.post('/token', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      state.accessToken = tokenResponse.data.access_token
      
      // Get user data
      api.defaults.headers.common['Authorization'] = `Bearer ${state.accessToken}`
      const userResponse = await api.get('/users/me')
      state.currentUser = userResponse.data
      state.isAuthenticated = true
      
      // Store token in localStorage for persistence (only token, not user data)
      localStorage.setItem('token', state.accessToken)
      
      return state.currentUser
    } catch (error) {
      state.error = error.response?.data?.detail || 'Login failed'
      throw new Error(state.error)
    } finally {
      state.loading = false
    }
  },
  
  // Logout action
  logout: () => {
    state.currentUser = null
    state.isAuthenticated = false
    state.accessToken = null
    
    // Clear localStorage
    localStorage.removeItem('token')
    
    // Remove Authorization header
    delete api.defaults.headers.common['Authorization']
  },
  
  // Check if user is already logged in from localStorage
  initAuth: async () => {
    const storedToken = localStorage.getItem('token')
    
    if (storedToken) {
      try {
        state.accessToken = storedToken
        api.defaults.headers.common['Authorization'] = `Bearer ${storedToken}`
        
        // Fetch current user with the token
        const userResponse = await api.get('/users/me')
        state.currentUser = userResponse.data
        state.isAuthenticated = true
      } catch (error) {
        console.error('Failed to authenticate with stored token:', error)
        actions.logout() // Clear invalid token
      }
    }
  },
  
  // API Functions for User Management
  // These functions directly call the API without local caching
  
  // Get all users (admin only)
  getAllUsers: async () => {
    if (!state.isAuthenticated || !state.accessToken) {
      console.warn('Not authenticated, cannot get users list')
      return [] // 返回空数组而不是抛出错误
    }
    
    try {
      // 确保请求头中包含授权信息
      const response = await api.get('/users', {
        headers: {
          'Authorization': `Bearer ${state.accessToken}`
        }
      })
      return response.data
    } catch (error) {
      console.error('Failed to get users:', error)
      // 不抛出错误，返回空数组
      return []
    }
  },
  
  // Add a new user (admin only)
  addUser: async (userData) => {
    try {
      const response = await api.post('/register', userData)
      return response.data
    } catch (error) {
      console.error('Failed to add user:', error)
      throw new Error(error.response?.data?.detail || 'Failed to add user')
    }
  },
  
  // Update a user (admin only)
  updateUser: async (userId, userData) => {
    try {
      const response = await api.put(`/users/${userId}`, userData)
      return response.data
    } catch (error) {
      console.error('Failed to update user:', error)
      throw new Error(error.response?.data?.detail || 'Failed to update user')
    }
  },
  
  // Delete a user (admin only)
  deleteUser: async (userId) => {
    try {
      await api.delete(`/users/${userId}`)
      return true
    } catch (error) {
      console.error('Failed to delete user:', error)
      throw new Error(error.response?.data?.detail || 'Failed to delete user')
    }
  },
  
  // Update a user's permissions (admin only)
  updateUserPermissions: async (userId, permissions) => {
    try {
      const response = await api.put(`/users/${userId}/permissions`, {
        sitePermissions: permissions
      })
      return response.data
    } catch (error) {
      console.error('Failed to update permissions:', error)
      throw new Error(error.response?.data?.detail || 'Failed to update permissions')
    }
  },
  
  // Migrate user permissions (admin only)
  migrateUserPermissions: async () => {
    try {
      const response = await api.post('/admin/migrate-user-permissions')
      return response.data
    } catch (error) {
      console.error('Failed to migrate permissions:', error)
      throw new Error(error.response?.data?.detail || 'Failed to migrate permissions')
    }
  },
  
  // Get default site permissions for a role (helper function)
  getDefaultSitePermissions: (role) => {
    return roleDefaultSitePermissions[role] || [SITE_PERMISSIONS.SITE_VIEW]
  }
}

// Create the store object
const store = {
  state: readonly(state),
  ...getters,
  ...actions
}

// Initialize auth when the store is imported
store.initAuth()

// Export the store
export default store 