<template>
  <div class="container">
    <div class="login-box">
      <div class="logo-section">
       
        <h1>Welcome Back</h1>
        <p>Please login to your account</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <label for="email">Email</label>
        <input
          id="email"
          v-model="email"
          type="email"
          required
          placeholder="you@example.com"
        />

        <label for="password">Password</label>
        <input
          id="password"
          v-model="password"
          type="password"
          required
          placeholder="••••••••"
        />

        <div v-if="error" class="error-message">{{ error }}</div>

        <button>
         <span v-if="!loading">Login</span>
         <span v-else class="spinner"></span>
        </button>

      </form>

      <p class="register-text">
        Don’t have an account?
        <router-link to="/register" class="register-link">Register</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const loading = ref(false)
const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const auth = useAuthStore()

const handleLogin = async () => {
  error.value = ''
  loading.value= true                 

  try {
    const API_URL = import.meta.env.VITE_API_URL;
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email: email.value, password: password.value }),
    })

    const data = await res.json()

    if (!res.ok) {
      throw new Error(data.error || 'Login failed')
    }

    auth.setToken(data['access token'])
    auth.setUser(data.username)

    router.push('/tasks')
  } catch (err) {
    error.value = err.message
  }finally{
    loading.value= false
    
  }
}
</script>

<style scoped>

.container {
  min-height: 91vh;
  display: flex;
  padding: 2rem ;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #c8e6c9, #90caf9);
  
}

.spinner {
  display: inline-block;
  width: 18px;
  height: 18px;
  border: 3px solid rgba(255, 255, 255, 0.6);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  vertical-align: middle;
  margin: 0 auto;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}


.login-box {
  background: white;
  padding: 40px 30px;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.logo-section {
  margin-bottom: 30px;
}

.logo {
  width: 64px;
  height: 64px;
  margin-bottom: 15px;
}

/* Titles */
h1 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 5px;
}

p {
  color: #666;
  font-size: 0.9rem;
}

/* Form styling */
.login-form {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  font-weight: 600;
  margin-bottom: 5px;
  color: #444;
  font-size: 0.9rem;
}

input {
  padding: 10px 12px;
  margin-bottom: 20px;
  border: 1.5px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s ease;
}

input:focus {
  border-color: #3b82f6; /* blue */
  outline: none;
  box-shadow: 0 0 5px rgba(59,130,246,0.5);
}

/* Error message */
.error-message {
  color: #e53e3e;
  margin-bottom: 15px;
  font-size: 0.85rem;
  text-align: center;
}

/* Button */
button {
  background-color: #3b82f6;
  color: white;
  font-weight: 700;
  padding: 12px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #2563eb;
}

/* Register link */
.register-text {
  margin-top: 25px;
  font-size: 0.9rem;
  color: #555;
}

.register-link {
  color: #3b82f6;
  font-weight: 600;
  text-decoration: none;
}

.register-link:hover {
  text-decoration: underline;
}
</style>
