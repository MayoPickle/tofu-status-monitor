import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Chart, registerables } from 'chart.js'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import axios from 'axios'

// Register Chart.js components
Chart.register(...registerables)

// Configure axios to use the correct base URL for API requests
// The proxy in vue.config.js will handle the actual forwarding
axios.defaults.baseURL = ''

// Add a request interceptor to include the auth token in all requests
axios.interceptors.request.use(config => {
  const token = localStorage.getItem('auth_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
}, error => {
  return Promise.reject(error)
})

const app = createApp(App)

// Register FontAwesome component globally
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(router)
app.mount('#app') 