import { createRouter, createWebHistory } from 'vue-router'

import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import TasksPage from '../pages/TasksPage.vue'


const routes = [
  { path: '/', redirect: '/tasks' },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/tasks', component: TasksPage, meta: {requiresAuth: true} },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  console.log('Route guard:', { to: to.path, requiresAuth: to.meta.requiresAuth, token })

  if (to.meta.requiresAuth && !token) {
    console.log('No token, redirecting to /login')
    next('/login')
  } else {
    next()
  }
})



export default router
