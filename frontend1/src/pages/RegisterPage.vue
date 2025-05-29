<template>
  <div class="register-container">
    <div class="form-box">
      <h1>Register</h1>
      <form @submit.prevent="handleRegister">
        <input v-model="username" placeholder="Username" required />
        <input v-model="email" type="email" placeholder="Email" required />
        <input v-model="password" type="password" placeholder="Password" required />
        <button type="submit">Register</button>
      </form>

      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async handleRegister() {
      try {
        
        const API_URL = import.meta.env.VITE_API_URL;
        const response = await fetch(`${API_URL}/register`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password
          })
        });

        const data = await response.json();

        if (!response.ok) {
          this.message = data.error || 'Registration failed.';
        } else {
          this.message = data.message;
        }
      } catch (error) {
        this.message = 'Something went wrong. Check console.';
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  min-height: 91vh;
  display: flex;
  padding: 2rem;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #c8e6c9, #90caf9);
}

.form-box {
  background-color: #fff;
  padding: 2rem 2.5rem;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h2 {
  margin-bottom: 1.5rem;
  color: #333;
}

input {
  display: block;
  width: 100%;
  padding: 10px 14px;
  margin-bottom: 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

button {
  width: 100%;
  background-color: #007bff;
  color: white;
  padding: 10px 14px;
  font-size: 1rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

.message {
  margin-top: 1rem;
  color: #e63946;
}
</style>
