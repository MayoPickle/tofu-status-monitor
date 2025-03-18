import { reactive, readonly } from 'vue'
import axios from 'axios'

// API base URL
const API_URL = ''  // 不使用/api前缀，直接让代理处理

// User roles
export const ROLES = {
  ADMIN: 'admin',
  MAINTAINER: 'maintainer',
  USER: 'user',
  GUEST: 'guest'
}

// Permission definitions
export const PERMISSIONS = {
  VIEW_DASHBOARD: 'view_dashboard',
  VIEW_OVERALL_STATUS: 'view_overall_status',
  VIEW_DETAILED_METRICS: 'view_detailed_metrics',
  ADD_SITES: 'add_sites',
  EDIT_SITES: 'edit_sites',
  DELETE_SITES: 'delete_sites',
  MANAGE_USERS: 'manage_users',
  ASSIGN_SITES: 'assign_sites'
}

// Role-based permissions
const rolePermissions = {
  [ROLES.ADMIN]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_OVERALL_STATUS,
    PERMISSIONS.VIEW_DETAILED_METRICS,
    PERMISSIONS.ADD_SITES,
    PERMISSIONS.EDIT_SITES,
    PERMISSIONS.DELETE_SITES,
    PERMISSIONS.MANAGE_USERS,
    PERMISSIONS.ASSIGN_SITES
  ],
  [ROLES.MAINTAINER]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_OVERALL_STATUS,
    PERMISSIONS.VIEW_DETAILED_METRICS,
    PERMISSIONS.ADD_SITES,
    PERMISSIONS.EDIT_SITES
  ],
  [ROLES.USER]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_OVERALL_STATUS,
    PERMISSIONS.VIEW_DETAILED_METRICS
  ],
  [ROLES.GUEST]: [
    PERMISSIONS.VIEW_DASHBOARD,
    PERMISSIONS.VIEW_OVERALL_STATUS
  ]
}

// Mock users for demo purposes
const mockUsers = [
  {
    id: 1,
    username: 'admin',
    password: 'admin123',
    name: 'Admin User',
    email: 'admin@example.com',
    role: ROLES.ADMIN,
    assignedSites: ['main', 'backup', 'staging']
  },
  {
    id: 2,
    username: 'maintainer',
    password: 'maintain123',
    name: 'Maintenance Staff',
    email: 'maintainer@example.com',
    role: ROLES.MAINTAINER,
    assignedSites: ['main', 'backup', 'staging']
  },
  {
    id: 3,
    username: 'user',
    password: 'user123',
    name: 'Regular User',
    email: 'user@example.com',
    role: ROLES.USER,
    assignedSites: ['main']
  }
]

// Create the store state
const state = reactive({
  currentUser: null,
  isAuthenticated: false,
  accessToken: null,
  loading: false,
  error: null,
  users: mockUsers
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

// Add request interceptor for debugging
api.interceptors.request.use(config => {
  console.log('Making request to:', config.url, {
    method: config.method,
    data: config.data,
    headers: config.headers
  })
  return config
})

// Add response interceptor for debugging
api.interceptors.response.use(
  response => {
    console.log('Received response:', {
      status: response.status,
      data: response.data
    })
    return response
  },
  error => {
    console.error('API Error:', {
      message: error.message,
      response: error.response?.data,
      status: error.response?.status
    })
    throw error
  }
)

// Getter methods
const getters = {
  isAuthenticated: () => state.isAuthenticated,
  currentUser: () => state.currentUser,
  hasPermission: (permission) => {
    if (!state.currentUser) {
      return false
    }
    
    const userRole = state.currentUser.role
    return rolePermissions[userRole]?.includes(permission) || false
  },
  isAdmin: () => state.currentUser?.role === ROLES.ADMIN,
  isMaintainer: () => state.currentUser?.role === ROLES.MAINTAINER,
  isUser: () => state.currentUser?.role === ROLES.USER,
  isGuest: () => !state.isAuthenticated || state.currentUser?.role === ROLES.GUEST,
  canAccessSite: (siteId) => {
    if (!state.currentUser) {
      return false
    }
    
    // Admins and maintainers can access all sites
    if (state.currentUser.role === ROLES.ADMIN || state.currentUser.role === ROLES.MAINTAINER) {
      return true
    }
    
    // Users can only access assigned sites
    // Check if assignedSites exists before trying to use includes
    return state.currentUser.assignedSites && state.currentUser.assignedSites.includes(siteId)
  },
  getUserList: () => state.users,
  getUserById: (userId) => state.users.find(user => user.id === userId)
}

// Actions
const actions = {
  // Register a new user
  register: async (userData) => {
    state.loading = true
    state.error = null
    console.log('Registering user with data:', userData)
    
    try {
      const response = await api.post('/register', userData)
      console.log('Registration successful:', response.data)
      return response.data
    } catch (error) {
      console.error('Registration failed:', error)
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
      
      console.log('Login: Sending token request to:', `${API_URL}/token`)
      const tokenResponse = await api.post('/token', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      state.accessToken = tokenResponse.data.access_token
      
      // Get user data
      console.log('Login: Getting user data from:', `${API_URL}/users/me`)
      api.defaults.headers.common['Authorization'] = `Bearer ${state.accessToken}`
      const userResponse = await api.get('/users/me')
      state.currentUser = userResponse.data
      state.isAuthenticated = true
      
      // Store in localStorage for persistence
      localStorage.setItem('user', JSON.stringify(state.currentUser))
      localStorage.setItem('token', state.accessToken)
      
      return state.currentUser
    } catch (error) {
      console.error('Login error details:', error)
      state.error = error.response?.data?.detail || 'Login failed'
      throw new Error(state.error)
    } finally {
      state.loading = false
    }
  },
  
  // Logout action
  logout: () => {
    state.currentUser = { 
      role: ROLES.GUEST,
      assignedSites: []
    }
    state.isAuthenticated = false
    state.accessToken = null
    
    // Clear localStorage
    localStorage.removeItem('user')
    localStorage.removeItem('token')
  },
  
  // Check if user is already logged in from localStorage
  initAuth: () => {
    const storedUser = localStorage.getItem('user')
    const storedToken = localStorage.getItem('token')
    
    if (storedUser && storedToken) {
      state.currentUser = JSON.parse(storedUser)
      state.isAuthenticated = true
      state.accessToken = storedToken
    } else {
      // Set guest user if no stored credentials
      state.currentUser = { 
        role: ROLES.GUEST,
        assignedSites: [] // Initialize with empty array
      }
      state.isAuthenticated = false
    }
  },
  
  // For admin: add a new user
  addUser: (user) => {
    if (!getters.isAdmin()) {
      throw new Error('Only admins can add users')
    }
    
    // Generate a new id
    const newId = Math.max(...state.users.map(u => u.id)) + 1
    
    // Add new user to the list
    state.users.push({
      ...user,
      id: newId
    })
  },
  
  // For admin: update a user
  updateUser: (userId, userData) => {
    if (!getters.isAdmin()) {
      throw new Error('Only admins can update users')
    }
    
    const userIndex = state.users.findIndex(u => u.id === userId)
    
    if (userIndex === -1) {
      throw new Error('User not found')
    }
    
    // Update user data
    state.users[userIndex] = {
      ...state.users[userIndex],
      ...userData
    }
  },
  
  // For admin: delete a user
  deleteUser: (userId) => {
    if (!getters.isAdmin()) {
      throw new Error('Only admins can delete users')
    }
    
    const userIndex = state.users.findIndex(u => u.id === userId)
    
    if (userIndex === -1) {
      throw new Error('User not found')
    }
    
    // Remove user
    state.users.splice(userIndex, 1)
  },
  
  // For admin: assign sites to a user
  assignSitesToUser: (userId, siteIds) => {
    if (!getters.isAdmin()) {
      throw new Error('Only admins can assign sites')
    }
    
    const userIndex = state.users.findIndex(u => u.id === userId)
    
    if (userIndex === -1) {
      throw new Error('User not found')
    }
    
    // Update assigned sites
    state.users[userIndex].assignedSites = siteIds
    
    // If updating the current user, also update the currentUser state
    if (state.currentUser && state.currentUser.id === userId) {
      state.currentUser.assignedSites = siteIds
      localStorage.setItem('user', JSON.stringify(state.currentUser))
    }
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