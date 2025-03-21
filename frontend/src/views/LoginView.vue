<template>
  <div class="login-container">
    <!-- Add modern background elements -->
    <div class="floating-dots">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
    <div class="grid-lines"></div>
    <div class="planet-ring"></div>
    <div class="orbital-path"></div>
    <div class="stars">
      <div class="star" v-for="n in 80" :key="n" :style="{ 
        top: Math.random() * 100 + '%', 
        left: Math.random() * 100 + '%',
        width: (Math.random() * 2 + 1) + 'px',
        height: (Math.random() * 2 + 1) + 'px',
        animationDelay: Math.random() * 5 + 's'
      }"></div>
    </div>
    
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
  position: relative;
  overflow: hidden;
  z-index: 1;
}

/* Modern background elements */
.login-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(58, 134, 255, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 90% 80%, rgba(251, 86, 7, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(42, 157, 143, 0.08) 0%, transparent 70%);
  z-index: -1;
}

/* Planet */
.login-container::after {
  content: "";
  position: absolute;
  width: 220px;
  height: 220px;
  top: -40px;
  right: -30px;
  background: radial-gradient(circle, rgba(42, 157, 143, 0.5) 0%, rgba(58, 134, 255, 0.3) 60%, transparent 100%);
  border-radius: 50%;
  box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
              inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  z-index: -1;
  animation: planetRotate 60s infinite linear;
  filter: blur(4px);
}

@keyframes planetRotate {
  0% {
    box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
                inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  }
  50% {
    box-shadow: inset -20px 20px 40px rgba(255, 255, 255, 0.4),
                inset 10px -10px 30px rgba(0, 0, 40, 0.6);
  }
  100% {
    box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
                inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  }
}

/* Planet Ring */
.planet-ring {
  position: absolute;
  top: -50px;
  right: -70px;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  z-index: -1;
  overflow: visible;
  transform: rotateX(75deg) rotateY(15deg);
  pointer-events: none;
  animation: orbitRotate 80s infinite linear;
}

@keyframes orbitRotate {
  from { transform: rotateX(75deg) rotateY(15deg) rotateZ(0deg); }
  to { transform: rotateX(75deg) rotateY(15deg) rotateZ(360deg); }
}

.planet-ring::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 260px;
  height: 260px;
  transform: translate(-50%, -50%);
  border: 10px solid rgba(251, 186, 114, 0.2);
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(251, 186, 114, 0.4);
}

.planet-ring::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 220px;
  height: 220px;
  transform: translate(-50%, -50%);
  border: 6px solid rgba(58, 134, 255, 0.2);
  border-radius: 50%;
}

/* Additional ring */
.login-container .orbital-path {
  position: absolute;
  top: 25%;
  left: -15%;
  width: 150vh;
  height: 150vh;
  border: 1px dashed rgba(58, 134, 255, 0.1);
  border-radius: 50%;
  animation: orbit-rotate 150s linear infinite;
}

@keyframes orbit-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Floating Dots */
.login-container .floating-dots {
  position: absolute;
  z-index: -1;
  pointer-events: none;
  width: 100%;
  height: 100%;
}

.login-container .floating-dots .dot {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: rgba(58, 134, 255, 0.3);
  animation: float 8s infinite ease-in-out;
}

.login-container .floating-dots .dot:nth-child(1) {
  top: 15%;
  left: 10%;
  width: 4px;
  height: 4px;
  animation-delay: 0s;
  background-color: rgba(58, 134, 255, 0.3);
}

.login-container .floating-dots .dot:nth-child(2) {
  top: 25%;
  left: 20%;
  width: 8px;
  height: 8px;
  animation-delay: 1s;
  animation-duration: 10s;
  background-color: rgba(42, 157, 143, 0.3);
}

.login-container .floating-dots .dot:nth-child(3) {
  top: 60%;
  left: 5%;
  width: 6px;
  height: 6px;
  animation-delay: 2s;
  animation-duration: 7s;
  background-color: rgba(251, 86, 7, 0.3);
}

.login-container .floating-dots .dot:nth-child(4) {
  top: 70%;
  left: 80%;
  width: 5px;
  height: 5px;
  animation-delay: 3s;
  animation-duration: 9s;
  background-color: rgba(58, 134, 255, 0.3);
}

.login-container .floating-dots .dot:nth-child(5) {
  top: 40%;
  left: 85%;
  width: 7px;
  height: 7px;
  animation-delay: 4s;
  animation-duration: 8s;
  background-color: rgba(42, 157, 143, 0.3);
}

.login-container .floating-dots .dot:nth-child(6) {
  top: 30%;
  left: 60%;
  width: 4px;
  height: 4px;
  animation-delay: 2.5s;
  animation-duration: 11s;
  background-color: rgba(251, 86, 7, 0.3);
}

.login-container .floating-dots .dot:nth-child(7) {
  top: 80%;
  left: 30%;
  width: 6px;
  height: 6px;
  animation-delay: 3.5s;
  animation-duration: 9s;
  background-color: rgba(251, 86, 7, 0.3);
}

.login-container .floating-dots .dot:nth-child(8) {
  top: 15%;
  left: 70%;
  width: 5px;
  height: 5px;
  animation-delay: 4.5s;
  animation-duration: 10s;
  background-color: rgba(58, 134, 255, 0.3);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0);
  }
  25% {
    transform: translateY(-25px) translateX(15px);
  }
  50% {
    transform: translateY(10px) translateX(-12px);
  }
  75% {
    transform: translateY(15px) translateX(8px);
  }
}

/* Stars */
.stars {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -2;
  pointer-events: none;
}

.star {
  position: absolute;
  background-color: white;
  border-radius: 50%;
  opacity: 0.4;
  animation: twinkle 4s infinite ease-in-out;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(0.8); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

/* Grid Lines */
.grid-lines {
  position: absolute;
  z-index: -1;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  opacity: 0.06;
  background-image: 
    linear-gradient(to right, var(--primary) 1px, transparent 1px),
    linear-gradient(to bottom, var(--primary) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: grid-pulse 10s infinite ease-in-out;
}

@keyframes grid-pulse {
  0%, 100% { opacity: 0.04; }
  50% { opacity: 0.09; }
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
  position: relative;
  z-index: 2;
  backdrop-filter: blur(10px);
}

/* Add card glow effect */
.login-card::after {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: var(--radius-lg);
  box-shadow: 0 0 40px rgba(58, 134, 255, 0.15);
  opacity: 0;
  transition: opacity 0.5s ease;
  z-index: -1;
  pointer-events: none;
}

.login-card:hover::after {
  opacity: 1;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  padding: 2rem 2rem 1.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* Add subtle space gradient behind the header */
.login-header::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(ellipse at top center, rgba(58, 134, 255, 0.1) 0%, transparent 70%);
  z-index: 0;
}

.logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 1rem;
  position: relative;
}

.logo-icon {
  width: 64px;
  height: 64px;
  fill: var(--primary);
  margin-bottom: 1rem;
  filter: drop-shadow(0 4px 12px rgba(58, 134, 255, 0.5));
  animation: pulse 4s infinite ease-in-out;
  position: relative;
  z-index: 1;
}

/* Add glow effect to logo */
.logo::before {
  content: "";
  position: absolute;
  width: 80px;
  height: 80px;
  top: -8px;
  left: 50%;
  transform: translateX(-50%);
  background: radial-gradient(circle, rgba(58, 134, 255, 0.3) 0%, transparent 70%);
  border-radius: 50%;
  filter: blur(10px);
  z-index: 0;
}

@keyframes pulse {
  0%, 100% {
    filter: drop-shadow(0 4px 12px rgba(58, 134, 255, 0.4));
    transform: scale(1) rotate(0deg);
  }
  33% {
    filter: drop-shadow(0 8px 20px rgba(58, 134, 255, 0.7));
    transform: scale(1.05) rotate(2deg);
  }
  66% {
    filter: drop-shadow(0 6px 16px rgba(58, 134, 255, 0.5));
    transform: scale(1.02) rotate(-2deg);
  }
}

.login-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 0.5rem;
  letter-spacing: -0.5px;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.auth-subtitle {
  color: var(--text-secondary);
  margin: 0;
  font-size: 1rem;
  position: relative;
  z-index: 1;
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
  backdrop-filter: blur(5px);
  border: 1px solid rgba(255, 0, 110, 0.2);
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
  animation: error-pulse 2s infinite ease-in-out;
}

@keyframes error-pulse {
  0%, 100% { opacity: 0.8; transform: scale(1); }
  50% { opacity: 1; transform: scale(1.1); }
}

.auth-content {
  padding: 0 2rem 2rem;
  position: relative;
}

/* Add subtle space particle effects for form */
.auth-content::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 90% 10%, rgba(58, 134, 255, 0.05) 0%, transparent 20%),
    radial-gradient(circle at 10% 90%, rgba(42, 157, 143, 0.05) 0%, transparent 20%);
  z-index: -1;
  pointer-events: none;
}

.login-form {
  margin-bottom: 1.5rem;
  position: relative;
}

.form-group {
  margin-bottom: 1.5rem;
  position: relative;
}

.form-label {
  display: block;
  margin-bottom: 0.75rem;
  font-weight: 500;
  color: var(--text-primary);
  transition: color 0.3s ease;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper::after {
  content: "";
  position: absolute;
  bottom: 0;
  left: 12%;
  width: 0%;
  height: 2px;
  background: linear-gradient(to right, var(--primary), var(--primary-light));
  transition: width 0.3s ease, left 0.3s ease;
  border-radius: 2px;
  opacity: 0;
}

.input-wrapper:focus-within::after {
  width: 76%;
  left: 12%;
  opacity: 1;
}

.input-icon {
  position: absolute;
  left: 1rem;
  width: 20px;
  height: 20px;
  fill: var(--text-secondary);
  transition: all 0.3s ease;
  z-index: 1;
}

.input-wrapper:focus-within .input-icon {
  fill: var(--primary);
  filter: drop-shadow(0 0 3px rgba(58, 134, 255, 0.4));
  transform: scale(1.1);
}

.form-control {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  background-color: var(--bg-primary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  font-size: 1rem;
  color: var(--text-primary);
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
}

.form-control:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(58, 134, 255, 0.15);
  transform: translateY(-1px);
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
  padding: 1rem;
  font-size: 1rem;
  margin-top: 1.5rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  position: relative;
  overflow: hidden;
  transition: all 0.4s cubic-bezier(0.17, 0.67, 0.83, 0.67);
  z-index: 1;
}

/* Add glow effect on hover */
.submit-button::before {
  content: "";
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: linear-gradient(135deg, var(--primary-light), var(--primary-dark));
  z-index: -1;
  border-radius: var(--radius);
  opacity: 0;
  transition: opacity 0.3s ease;
  filter: blur(8px);
}

.submit-button:hover::before {
  opacity: 0.8;
}

/* Add cosmic space particle effect */
.submit-button::after {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.7s ease;
  z-index: 1;
}

.submit-button:hover::after {
  left: 100%;
}

.submit-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(58, 134, 255, 0.3);
}

.submit-button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
  background: linear-gradient(135deg, var(--gray), var(--gray-dark));
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  position: relative;
  z-index: 2;
}

.loading-dots {
  display: flex;
  align-items: center;
  gap: 4px;
}

.loading-dots .dot {
  width: 5px;
  height: 5px;
  background-color: currentColor;
  border-radius: 50%;
  animation: dot-pulse 1.5s infinite ease-in-out;
}

.loading-dots .dot:nth-child(2) {
  animation-delay: 0.2s;
}

.loading-dots .dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes dot-pulse {
  0%, 100% {
    opacity: 0.4;
    transform: scale(0.8);
  }
  50% {
    opacity: 1;
    transform: scale(1.3);
  }
}

.auth-options {
  padding: 1.5rem 0;
  border-top: 1px solid var(--border-color);
  margin-bottom: 1.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

/* Add subtle line glow effect */
.auth-options::after {
  content: "";
  position: absolute;
  top: 0;
  left: 30%;
  width: 40%;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--primary), transparent);
  filter: blur(1px);
  animation: line-glow 4s infinite ease-in-out;
}

@keyframes line-glow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.switch-mode-button {
  width: 100%;
  padding: 0.85rem;
  font-size: 0.95rem;
  border: 1px solid var(--border-color);
  position: relative;
  overflow: hidden;
  z-index: 1;
  transition: all 0.3s ease;
}

.switch-mode-button:hover {
  border-color: var(--primary);
  color: var(--primary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* Add subtle hover animation */
.switch-mode-button::after {
  content: "";
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(58, 134, 255, 0.1), transparent);
  transition: left 0.5s ease;
  z-index: -1;
}

.switch-mode-button:hover::after {
  left: 100%;
}

/* Demo Accounts Section */
.demo-section {
  animation: fadeUp 0.7s ease;
  position: relative;
}

@keyframes fadeUp {
  from {
    opacity: 0;
    transform: translateY(20px);
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
  position: relative;
  display: inline-block;
  left: 50%;
  transform: translateX(-50%);
}

/* Add underline effect */
.demo-title::after {
  content: "";
  position: absolute;
  bottom: -4px;
  left: 25%;
  width: 50%;
  height: 2px;
  background: linear-gradient(to right, transparent, var(--primary), transparent);
  border-radius: var(--radius);
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
  transition: all 0.3s cubic-bezier(0.17, 0.67, 0.83, 0.67);
  position: relative;
  overflow: hidden;
}

.account-item::before {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: linear-gradient(135deg, transparent, rgba(255, 255, 255, 0.05), transparent);
  z-index: 0;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.account-item:hover {
  transform: translateY(-3px) scale(1.01);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
  border-color: var(--primary);
  z-index: 1;
}

.account-item:hover::before {
  opacity: 1;
}

.account-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--radius);
  flex-shrink: 0;
  transition: all 0.3s ease;
  z-index: 1;
  position: relative;
  overflow: hidden;
}

.account-icon-wrapper::after {
  content: "";
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.account-item:hover .account-icon-wrapper {
  transform: scale(1.1) rotate(-5deg);
}

.account-item:hover .account-icon-wrapper::after {
  opacity: 1;
}

.account-icon-wrapper.admin {
  background-color: rgba(58, 134, 255, 0.15);
}

.account-icon-wrapper.maintainer {
  background-color: rgba(251, 86, 7, 0.15);
}

.account-icon-wrapper.user {
  background-color: rgba(34, 197, 94, 0.15);
}

.account-icon {
  width: 24px;
  height: 24px;
  transition: all 0.3s ease;
}

.account-item:hover .account-icon {
  transform: scale(1.1);
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
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
  z-index: 1;
}

.account-name {
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 0.25rem;
  transition: color 0.3s ease;
}

.account-item:hover .account-name {
  color: var(--primary);
}

.account-credentials {
  font-size: 0.875rem;
  color: var(--text-secondary);
  font-family: monospace;
  transition: color 0.3s ease;
}

.guest-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  width: 100%;
  padding: 0.85rem;
  font-size: 0.95rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  background: linear-gradient(to right, var(--bg-secondary), var(--bg-primary), var(--bg-secondary));
  background-size: 200% 100%;
}

.guest-button:hover {
  background-position: right center;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
  border-color: var(--primary-light);
  color: var(--primary);
}

.guest-icon {
  width: 22px;
  height: 22px;
  fill: currentColor;
  transition: all 0.3s ease;
}

.guest-button:hover .guest-icon {
  transform: rotate(15deg);
  fill: var(--primary);
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