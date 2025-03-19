<template>
  <div class="login-container">
    <div class="login-card">
      <div class="login-header">
        <div class="logo">
          <svg viewBox="0 0 24 24" class="logo-icon">
            <path d="M12,2L1,21H23L12,2M12,6.7L16,13H8L12,6.7Z" />
          </svg>
          <h1>{{ isRegistering ? 'Create Account' : 'Login to Kepler' }}</h1>
        </div>
        <p class="auth-subtitle">{{ isRegistering ? 'Sign up to monitor your sites' : 'Welcome back! Please sign in to continue' }}</p>
      </div>
      
      <div v-if="error" class="error-message">
        <svg viewBox="0 0 24 24" class="error-icon">
          <path d="M13,13H11V7H13M13,17H11V15H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z" />
        </svg>
        <span>{{ error }}</span>
      </div>
      
      <div class="auth-content">
        <form @submit.prevent="onSubmit" class="login-form">
          <div class="form-group">
            <label for="username" class="form-label">Username</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" class="input-icon">
                <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
              </svg>
              <input 
                type="text" 
                id="username" 
                v-model="username" 
                placeholder="Enter your username"
                class="form-control"
                required
                :disabled="loading"
              />
            </div>
          </div>

          <div v-if="isRegistering" class="form-group">
            <label for="email" class="form-label">Email</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" class="input-icon">
                <path d="M20,8L12,13L4,8V6L12,11L20,6M20,4H4C2.89,4 2,4.89 2,6V18A2,2 0 0,0 4,20H20A2,2 0 0,0 22,18V6C22,4.89 21.1,4 20,4Z" />
              </svg>
              <input 
                type="email" 
                id="email" 
                v-model="email" 
                placeholder="Enter your email"
                class="form-control"
                required
                :disabled="loading"
              />
            </div>
          </div>

          <div v-if="isRegistering" class="form-group">
            <label for="name" class="form-label">Full Name</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" class="input-icon">
                <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
              </svg>
              <input 
                type="text" 
                id="name" 
                v-model="name" 
                placeholder="Enter your full name"
                class="form-control"
                :disabled="loading"
              />
            </div>
          </div>
          
          <div class="form-group">
            <label for="password" class="form-label">Password</label>
            <div class="input-wrapper">
              <svg viewBox="0 0 24 24" class="input-icon">
                <path d="M12,17A2,2 0 0,0 14,15C14,13.89 13.1,13 12,13A2,2 0 0,0 10,15A2,2 0 0,0 12,17M18,8A2,2 0 0,1 20,10V20A2,2 0 0,1 18,22H6A2,2 0 0,1 4,20V10C4,8.89 4.9,8 6,8H7V6A5,5 0 0,1 12,1A5,5 0 0,1 17,6V8H18M12,3A3,3 0 0,0 9,6V8H15V6A3,3 0 0,0 12,3Z" />
              </svg>
              <input 
                type="password" 
                id="password" 
                v-model="password" 
                :placeholder="isRegistering ? 'Choose a password' : 'Enter your password'"
                class="form-control"
                required
                :disabled="loading"
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            class="btn btn-primary submit-button" 
            :disabled="loading"
          >
            <span v-if="!loading">{{ isRegistering ? 'Create Account' : 'Sign In' }}</span>
            <span v-else class="loading-text">
              <span class="loading-dots">
                <span class="dot"></span>
                <span class="dot"></span>
                <span class="dot"></span>
              </span>
              Please wait
            </span>
          </button>
        </form>

        <div class="auth-options">
          <button 
            class="btn btn-outline switch-mode-button" 
            @click="toggleMode"
            :disabled="loading"
          >
            {{ isRegistering ? 'Already have an account? Sign In' : 'Need an account? Sign Up' }}
          </button>
        </div>
        
        <div v-if="!isRegistering" class="demo-section">
          <h3 class="demo-title">Demo Accounts</h3>
          
          <div class="demo-accounts">
            <div class="account-item" @click="fillCredentials('admin', 'admin123')">
              <div class="account-icon-wrapper admin">
                <svg viewBox="0 0 24 24" class="account-icon">
                  <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M12,5A3,3 0 0,1 15,8A3,3 0 0,1 12,11A3,3 0 0,1 9,8A3,3 0 0,1 12,5M17.13,17C15.92,18.85 14.11,20.24 12,20.92C9.89,20.24 8.08,18.85 6.87,17C6.53,16.5 6.24,16 6,15.47C6,13.82 8.71,12.47 12,12.47C15.29,12.47 18,13.79 18,15.47C17.76,16 17.47,16.5 17.13,17Z" />
                </svg>
              </div>
              <div class="account-info">
                <div class="account-name">Admin</div>
                <div class="account-credentials">admin / admin123</div>
              </div>
            </div>
            
            <div class="account-item" @click="fillCredentials('maintainer', 'maintain123')">
              <div class="account-icon-wrapper maintainer">
                <svg viewBox="0 0 24 24" class="account-icon">
                  <path d="M12,15.5A3.5,3.5 0 0,1 8.5,12A3.5,3.5 0 0,1 12,8.5A3.5,3.5 0 0,1 15.5,12A3.5,3.5 0 0,1 12,15.5M19.43,12.97C19.47,12.65 19.5,12.33 19.5,12C19.5,11.67 19.47,11.34 19.43,11L21.54,9.37C21.73,9.22 21.78,8.95 21.66,8.73L19.66,5.27C19.54,5.05 19.27,4.96 19.05,5.05L16.56,6.05C16.04,5.66 15.5,5.32 14.87,5.07L14.5,2.42C14.46,2.18 14.25,2 14,2H10C9.75,2 9.54,2.18 9.5,2.42L9.13,5.07C8.5,5.32 7.96,5.66 7.44,6.05L4.95,5.05C4.73,4.96 4.46,5.05 4.34,5.27L2.34,8.73C2.21,8.95 2.27,9.22 2.46,9.37L4.57,11C4.53,11.34 4.5,11.67 4.5,12C4.5,12.33 4.53,12.65 4.57,12.97L2.46,14.63C2.27,14.78 2.21,15.05 2.34,15.27L4.34,18.73C4.46,18.95 4.73,19.03 4.95,18.95L7.44,17.94C7.96,18.34 8.5,18.68 9.13,18.93L9.5,21.58C9.54,21.82 9.75,22 10,22H14C14.25,22 14.46,21.82 14.5,21.58L14.87,18.93C15.5,18.67 16.04,18.34 16.56,17.94L19.05,18.95C19.27,19.03 19.54,18.95 19.66,18.73L21.66,15.27C21.78,15.05 21.73,14.78 21.54,14.63L19.43,12.97Z" />
                </svg>
              </div>
              <div class="account-info">
                <div class="account-name">Maintainer</div>
                <div class="account-credentials">maintainer / maintain123</div>
              </div>
            </div>
            
            <div class="account-item" @click="fillCredentials('user', 'user123')">
              <div class="account-icon-wrapper user">
                <svg viewBox="0 0 24 24" class="account-icon">
                  <path d="M12,4A4,4 0 0,1 16,8A4,4 0 0,1 12,12A4,4 0 0,1 8,8A4,4 0 0,1 12,4M12,14C16.42,14 20,15.79 20,18V20H4V18C4,15.79 7.58,14 12,14Z" />
                </svg>
              </div>
              <div class="account-info">
                <div class="account-name">User</div>
                <div class="account-credentials">user / user123</div>
              </div>
            </div>
          </div>
          
          <button class="btn btn-outline guest-button" @click="continueAsGuest">
            <svg viewBox="0 0 24 24" class="guest-icon">
              <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,8.39C13.57,9.4 15.42,10 17.42,10C18.2,10 18.95,9.91 19.67,9.74C19.88,10.45 20,11.21 20,12C20,16.41 16.41,20 12,20C9,20 6.39,18.34 5,15.89L6.61,14V16H13.5C14.33,16 15,15.33 15,14.5C15,12.57 13.43,11 11.5,11H9V8.39C10,8.14 10.95,8 12,8.39Z" />
            </svg>
            Continue as Guest
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import store from '../store/userStore'

export default {
  name: 'LoginView',
  setup() {
    const router = useRouter()
    const username = ref('')
    const email = ref('')
    const name = ref('')
    const password = ref('')
    const loading = ref(false)
    const error = ref('')
    const isRegistering = ref(false)
    
    const onSubmit = async () => {
      console.log('Form submitted', { isRegistering: isRegistering.value })
      if (isRegistering.value) {
        await handleRegister()
      } else {
        await handleLogin()
      }
    }
    
    const handleLogin = async () => {
      console.log('handleLogin called')
      if (!username.value || !password.value) {
        error.value = 'Please enter both username and password'
        return
      }
      
      loading.value = true
      error.value = ''
      
      try {
        await store.login(username.value, password.value)
        router.push('/')
      } catch (err) {
        console.error('Login error:', err)
        error.value = err.message || 'Login failed. Please try again.'
      } finally {
        loading.value = false
      }
    }

    const handleRegister = async () => {
      console.log('handleRegister called')
      if (!username.value || !password.value || !email.value) {
        error.value = 'Please fill in all required fields'
        return
      }
      
      loading.value = true
      error.value = ''
      console.log('Attempting to register with:', {
        username: username.value,
        email: email.value,
        name: name.value
      })
      
      try {
        const response = await store.register({
          username: username.value,
          email: email.value,
          name: name.value,
          password: password.value
        })
        console.log('Registration response:', response)
        await store.login(username.value, password.value)
        router.push('/')
      } catch (err) {
        console.error('Registration error:', err)
        error.value = err.message || 'Registration failed. Please try again.'
      } finally {
        loading.value = false
      }
    }
    
    const continueAsGuest = () => {
      store.logout()
      router.push('/')
    }
    
    const fillCredentials = (user, pass) => {
      username.value = user
      password.value = pass
    }

    const toggleMode = () => {
      isRegistering.value = !isRegistering.value
      error.value = ''
      username.value = ''
      email.value = ''
      name.value = ''
      password.value = ''
    }
    
    return {
      username,
      email,
      name,
      password,
      loading,
      error,
      isRegistering,
      onSubmit,
      continueAsGuest,
      fillCredentials,
      toggleMode
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100%;
  padding: 2rem;
  background-color: var(--bg-body);
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(58, 134, 255, 0.05) 0%, transparent 30%),
    radial-gradient(circle at 90% 80%, rgba(251, 86, 7, 0.05) 0%, transparent 30%);
}

.login-card {
  width: 100%;
  max-width: 480px;
  background-color: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  overflow: hidden;
  border: 1px solid var(--border-color);
  transition: var(--transition);
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  padding: 2rem 2rem 1.5rem;
  text-align: center;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
}

.logo-icon {
  width: 56px;
  height: 56px;
  fill: var(--primary);
  margin-bottom: 1rem;
  filter: drop-shadow(0 2px 8px rgba(58, 134, 255, 0.4));
  animation: pulse 3s infinite ease-in-out;
}

@keyframes pulse {
  0%, 100% {
    filter: drop-shadow(0 2px 8px rgba(58, 134, 255, 0.4));
  }
  50% {
    filter: drop-shadow(0 4px 12px rgba(58, 134, 255, 0.6));
  }
}

.login-header h1 {
  font-size: 1.75rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem;
  letter-spacing: -0.5px;
}

.auth-subtitle {
  color: var(--text-secondary);
  margin: 0;
  font-size: 0.95rem;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background-color: rgba(255, 0, 110, 0.1);
  color: var(--danger);
  padding: 1rem 2rem;
  border-radius: var(--radius);
  margin: 0 2rem 1rem;
  animation: shake 0.5s ease;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
  20%, 40%, 60%, 80% { transform: translateX(5px); }
}

.error-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  fill: var(--danger);
}

.auth-content {
  padding: 0 2rem 2rem;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
  color: var(--text-primary);
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 1rem;
  width: 20px;
  height: 20px;
  fill: var(--text-secondary);
}

.form-control {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 3rem;
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  font-size: 1rem;
  color: var(--text-primary);
  transition: var(--transition);
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(58, 134, 255, 0.15);
}

.form-control::placeholder {
  color: var(--text-secondary);
  opacity: 0.7;
}

.form-control:disabled {
  background-color: var(--bg-secondary);
  opacity: 0.7;
  cursor: not-allowed;
}

.submit-button {
  width: 100%;
  padding: 0.875rem;
  font-size: 1rem;
  margin-top: 1rem;
}

.submit-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.loading-dots {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dot {
  width: 4px;
  height: 4px;
  background-color: currentColor;
  border-radius: 50%;
  animation: dot-pulse 1.5s infinite ease-in-out;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dot-pulse {
  0%, 100% {
    opacity: 0.4;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.2);
  }
}

.auth-options {
  padding: 1.5rem 0;
  border-top: 1px solid var(--border-color);
  margin-bottom: 1.5rem;
  text-align: center;
}

.switch-mode-button {
  width: 100%;
  padding: 0.75rem;
  font-size: 0.95rem;
}

/* Demo Accounts Section */
.demo-section {
  animation: fadeUp 0.5s ease;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.demo-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1rem;
  letter-spacing: -0.5px;
  text-align: center;
}

.demo-accounts {
  display: grid;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.account-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border-radius: var(--radius);
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  cursor: pointer;
  transition: var(--transition);
}

.account-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
  border-color: var(--border-color);
}

.account-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius);
  flex-shrink: 0;
}

.account-icon-wrapper.admin {
  background-color: rgba(58, 134, 255, 0.1);
}

.account-icon-wrapper.maintainer {
  background-color: rgba(251, 86, 7, 0.1);
}

.account-icon-wrapper.user {
  background-color: rgba(34, 197, 94, 0.1);
}

.account-icon {
  width: 24px;
  height: 24px;
}

.account-icon-wrapper.admin .account-icon {
  fill: var(--primary);
}

.account-icon-wrapper.maintainer .account-icon {
  fill: var(--secondary);
}

.account-icon-wrapper.user .account-icon {
  fill: var(--success);
}

.account-info {
  flex: 1;
}

.account-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
}

.account-credentials {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-family: monospace;
}

.guest-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.75rem;
  font-size: 0.95rem;
  transition: var(--transition);
}

.guest-icon {
  width: 20px;
  height: 20px;
  fill: currentColor;
}

/* Media queries for responsive design */
@media (max-width: 768px) {
  .login-container {
    padding: 1rem;
  }
  
  .login-card {
    max-width: 100%;
  }
  
  .auth-content {
    padding: 0 1.5rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .login-header {
    padding: 1.5rem 1.5rem 1rem;
  }
  
  .error-message {
    margin: 0 1rem 1rem;
    padding: 0.75rem 1rem;
  }
  
  .form-group {
    margin-bottom: 1rem;
  }
}
</style> 