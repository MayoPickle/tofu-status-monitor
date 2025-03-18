import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { Chart, registerables } from 'chart.js'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

// Register Chart.js components
Chart.register(...registerables)

const app = createApp(App)

// Register FontAwesome component globally
app.component('font-awesome-icon', FontAwesomeIcon)

app.use(router)
app.mount('#app') 