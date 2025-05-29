<script setup>
import { RouterLink, RouterView } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>

<template>
  <header>
    <nav>
      <RouterLink to="/tasks">Tasks</RouterLink>

      <template v-if="!auth.token">
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/register">Register</RouterLink>
      </template>

      <template v-else>
        <div class="dropdown">
          <button class="dropbtn">{{ auth.user }} ⬇️</button>
          <div class="dropdown-content">
            <RouterLink to="/update-username">Update Username</RouterLink>
            <RouterLink to="/change-password">Change Password</RouterLink>
            <a @click="auth.logout()">Logout</a>
          </div>
        </div>
      </template>
    </nav>
  </header>

  <main>
    <RouterView />
  </main>
</template>


<style scoped>

.dropdown {
  position: relative;
  display: inline-block;
}

.dropbtn {
  background-color: transparent;
  border: none;
  color: white;
  font-weight: bold;
  cursor: pointer;
}

.dropdown-content {
  display: none;
  position: absolute;
  right: 0;
  background-color: white;
  min-width: 160px;
  box-shadow: 0px 8px 16px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  display: block;
  padding: 12px;
  text-decoration: none;
  color: black;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #18c867;
  color: white;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}


.logo-area h1 {
  margin: 0;
  font-size: 1.5rem;
}


nav {
  display: flex;
  gap: 1.5rem;
}

nav a {
  color: white;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s;
}

nav a:hover {
  color: #f0f0f0;
}

nav a.router-link-exact-active {
  border-bottom: 2px solid white;
}


main {
  flex-grow: 1;
  background-color: #f5f5f5;
  min-height: calc(100vh - 80px); 

}

</style>
