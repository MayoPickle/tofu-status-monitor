<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <svg viewBox="0 0 24 24" class="logo-icon">
          <path d="M12,2L1,21H23L12,2M12,6.7L16,13H8L12,6.7Z" />
        </svg>
        <h1>Login to Kepler</h1>
      </div>
      
      <div v-if="error" class="error-message">
        <svg viewBox="0 0 24 24" class="error-icon">
          <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
        </svg>
        <span>{{ error }}</span>
      </div>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" class="input-icon">
              <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
            </svg>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              placeholder="Enter your username"
              required
              :disabled="loading"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="password">Password</label>
          <div class="input-wrapper">
            <svg viewBox="0 0 24 24" class="input-icon">
              <path d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z" />
            </svg>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              placeholder="Enter your password"
              required
              :disabled="loading"
            />
          </div>
        </div>
        
        <button type="submit" class="login-button" :disabled="loading">
          <span v-if="loading" class="spinner">
            <svg viewBox="0 0 24 24">
              <path d="M12,4V2A10,10 0 0,0 2,12H4A8,8 0 0,1 12,4Z" />
            </svg>
          </span>
          <span v-else>Sign in</span>
        </button>
      </form>
      
      <div class="login-divider">
        <span>or try a demo account</span>
      </div>
      
      <div class="demo-accounts">
        <div class="account-item" @click="fillCredentials('admin', 'admin123')">
          <svg viewBox="0 0 24 24" class="account-icon admin-icon">
            <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1Z" />
          </svg>
          <div class="account-info">
            <div class="account-name">Admin</div>
            <div class="account-credentials">admin / admin123</div>
          </div>
        </div>
        <div class="account-item" @click="fillCredentials('maintainer', 'maintain123')">
          <svg viewBox="0 0 24 24" class="account-icon maintainer-icon">
            <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z" />
          </svg>
          <div class="account-info">
            <div class="account-name">Maintainer</div>
            <div class="account-credentials">maintainer / maintain123</div>
          </div>
        </div>
        <div class="account-item" @click="fillCredentials('user', 'user123')">
          <svg viewBox="0 0 24 24" class="account-icon user-icon">
            <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
          </svg>
          <div class="account-info">
            <div class="account-name">User</div>
            <div class="account-credentials">user / user123</div>
          </div>
        </div>
      </div>
      
      <div class="guest-login">
        <button class="guest-button" @click="continueAsGuest">
          <svg viewBox="0 0 24 24" class="guest-icon">
            <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,8.39C13.57,9.4 15.42,10 17.42,10C18.2,10 18.95,9.91 19.67,9.74C19.88,10.45 20,11.21 20,12C20,16.41 16.41,20 12,20C9,20 6.39,18.34 5,15.89L6.61,14V16H13.5C14.33,16 15,15.33 15,14.5C15,12.57 13.43,11 11.5,11H9V8.39C10,8.14 10.95,8 12,8.39Z" />
          </svg>
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
      userStore.logout()
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
  min-height: calc(100vh - 100px);
  padding: 2rem;
}

.login-card {
  background-color: var(--bg-secondary);
  border-radius: var(--radius);
  box-shadow: var(--shadow-lg);
  padding: 2rem;
  width: 100%;
  max-width: 420px;
}

.login-header {
  margin-bottom: 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.logo-icon {
  width: 48px;
  height: 48px;
  fill: var(--primary);
  margin-bottom: 1rem;
}

.login-header h1 {
  margin: 0;
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--text-primary);
}

.error-message {
  display: flex;
  align-items: center;
  background-color: rgba(231, 111, 81, 0.1);
  color: var(--danger);
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
}

.error-icon {
  width: 20px;
  height: 20px;
  fill: var(--danger);
  margin-right: 8px;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
  font-size: 0.9rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  width: 18px;
  height: 18px;
  fill: var(--gray);
}

.form-group input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  font-size: 1rem;
  outline: none;
  transition: var(--transition);
  background-color: var(--bg-primary);
  color: var(--text-primary);
}

.form-group input:focus {
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(42, 157, 143, 0.2);
}

.login-button {
  width: 100%;
  padding: 0.85rem;
  background-color: var(--primary);
  color: white;
  border: none;
  border-radius: var(--radius);
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: var(--transition);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-button:hover {
  background-color: var(--primary-dark);
}

.login-button:disabled {
  background-color: var(--gray-light);
  cursor: not-allowed;
}

.spinner {
  display: inline-block;
  animation: spin 1s linear infinite;
  width: 20px;
  height: 20px;
}

.spinner svg {
  width: 100%;
  height: 100%;
  fill: white;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.login-divider {
  text-align: center;
  margin: 1.5rem 0;
  position: relative;
}

.login-divider::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 0;
  right: 0;
  height: 1px;
  background-color: var(--border-color);
  z-index: 1;
}

.login-divider span {
  display: inline-block;
  background-color: var(--bg-secondary);
  padding: 0 1rem;
  position: relative;
  z-index: 2;
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.demo-accounts {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.account-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  border: 1px solid var(--border-color);
  background-color: var(--bg-secondary);
}

.account-item:hover {
  background-color: rgba(42, 157, 143, 0.05);
}

.account-icon {
  width: 24px;
  height: 24px;
  margin-right: 12px;
}

.admin-icon {
  fill: var(--primary);
}

.maintainer-icon {
  fill: var(--secondary);
}

.user-icon {
  fill: var(--accent);
}

.account-info {
  flex: 1;
}

.account-name {
  font-weight: 500;
  color: var(--text-primary);
}

.account-credentials {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.guest-login {
  text-align: center;
}

.guest-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.75rem;
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  cursor: pointer;
  transition: var(--transition);
  font-weight: 500;
  font-size: 0.9rem;
}

.guest-button:hover {
  background-color: rgba(42, 157, 143, 0.05);
}

.guest-icon {
  width: 18px;
  height: 18px;
  fill: var(--gray);
  margin-right: 8px;
}
</style> 