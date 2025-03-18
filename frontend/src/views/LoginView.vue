<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Login to Tofu Monitor</h1>
      
      <div v-if="error" class="error-message">
        {{ error }}
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input 
            type="text" 
            id="username" 
            v-model="username" 
            placeholder="Username"
            required
            :disabled="loading"
          />
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="Password"
            required
            :disabled="loading"
          />
        </div>
        
        <button type="submit" class="login-button" :disabled="loading">
          <span v-if="loading" class="spinner small"></span>
          <span v-else>Login</span>
        </button>
      </form>
      
      <div class="demo-accounts">
        <h3>Demo Accounts</h3>
        <div class="account-list">
          <div class="account-item" @click="fillCredentials('admin', 'admin123')">
            <strong>Admin:</strong> username: admin / password: admin123
          </div>
          <div class="account-item" @click="fillCredentials('maintainer', 'maintain123')">
            <strong>Maintainer:</strong> username: maintainer / password: maintain123
          </div>
          <div class="account-item" @click="fillCredentials('user', 'user123')">
            <strong>User:</strong> username: user / password: user123
          </div>
        </div>
      </div>
      
      <div class="guest-login">
        <p>Or continue as a guest</p>
        <button class="guest-button" @click="continueAsGuest">
          Continue as Guest
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import userStore from '../store/userStore'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const username = ref('')
    const password = ref('')
    const loading = ref(false)
    const error = ref('')
    
    const handleLogin = async () => {
      if (!username.value || !password.value) {
        error.value = 'Please enter both username and password'
        return
      }
      
      loading.value = true
      error.value = ''
      
      try {
        await userStore.login(username.value, password.value)
        router.push('/')
      } catch (err) {
        error.value = err.message || 'Login failed. Please try again.'
      } finally {
        loading.value = false
      }
    }
    
    const continueAsGuest = () => {
      // Explicitly set the guest user state
      userStore.logout() // This now sets state.currentUser to be a guest with an empty assignedSites array
      router.push('/')
    }
    
    const fillCredentials = (user, pass) => {
      username.value = user
      password.value = pass
    }
    
    return {
      username,
      password,
      loading,
      error,
      handleLogin,
      continueAsGuest,
      fillCredentials
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 2rem;
}

.login-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  width: 100%;
  max-width: 450px;
}

.login-card h1 {
  margin-top: 0;
  margin-bottom: 1.5rem;
  text-align: center;
  color: #2c3e50;
}

.error-message {
  color: #e53935;
  background-color: rgba(229, 57, 53, 0.1);
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.login-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #2c3e50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.login-button:hover {
  background-color: #34495e;
}

.login-button:disabled {
  background-color: #95a5a6;
  cursor: not-allowed;
}

.demo-accounts {
  margin: 1.5rem 0;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.demo-accounts h3 {
  margin-top: 0;
  margin-bottom: 0.75rem;
  font-size: 1rem;
  color: #2c3e50;
}

.account-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.account-item {
  padding: 0.5rem;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.account-item:hover {
  background-color: #e9ecef;
}

.guest-login {
  margin-top: 1.5rem;
  text-align: center;
}

.guest-login p {
  margin-bottom: 0.5rem;
  color: #6c757d;
}

.guest-button {
  padding: 0.5rem 1rem;
  background-color: transparent;
  color: #6c757d;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.guest-button:hover {
  background-color: #f8f9fa;
  color: #2c3e50;
}

.spinner.small {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
}
</style> 