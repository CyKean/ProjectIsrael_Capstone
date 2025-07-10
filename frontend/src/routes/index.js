import { createRouter, createWebHistory } from 'vue-router'
import { authRoutes } from './auth.js'
import { userRoutes } from './users.js'
import { useUserStore } from '../utils/user'

// Combine all routes
const routes = [
  ...authRoutes,
  ...userRoutes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Global middleware (navigation guard)
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // Restore session from localStorage if needed
  await userStore.loadUser()

  // Check if route is public
  const isPublic = to.matched.some(record => record.meta.isPublic)
  
  // Check authentication and verification status
  const isLoggedIn = !!userStore.user
  const isVerified = userStore.user?.verified === true

  // Handle route access
  if (!isPublic) {
    if (!isLoggedIn) {
      // Not logged in - redirect to login
      return next('/login')
    }
    if (!isVerified && to.path !== '/auth/verify-otp') {
      // Logged in but not verified - redirect to OTP verification
      return next('/auth/verify-otp')
    }
  }

  // Handle already authenticated users trying to access auth pages
  if (isLoggedIn && isVerified && 
      ['/login', '/register', '/auth/verify-otp'].includes(to.path)) {
    return next('/app/dashboard')
  }

  // All checks passed - proceed with navigation
  next()
})

export default router