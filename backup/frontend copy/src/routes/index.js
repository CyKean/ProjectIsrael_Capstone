// router/index.js
import { createRouter, createWebHistory } from 'vue-router';
import { authRoutes } from './auth.js';
import { userRoutes } from './users.js';
import { useUserStore } from '../utils/user';

const router = createRouter({
  history: createWebHistory(),
  routes: [...authRoutes, ...userRoutes]
});

function setupActivityTracking(userStore) {
  const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart'];
  
  const handler = () => {
    if (userStore.isAuthenticated) {
      userStore.resetInactivityTimer();
    }
  };

  // Add event listeners
  events.forEach(event => window.addEventListener(event, handler));

  // Also track visibility changes
  const visibilityHandler = () => {
    if (document.visibilityState === 'visible' && userStore.isAuthenticated) {
      userStore.resetInactivityTimer();
    }
  };
  document.addEventListener('visibilitychange', visibilityHandler);

  // Cleanup function
  return () => {
    events.forEach(event => window.removeEventListener(event, handler));
    document.removeEventListener('visibilitychange', visibilityHandler);
  };
}

router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  
  try {
    // Load user from storage
    const userLoaded = await userStore.loadUser();
    
    // Setup activity tracking
    const cleanup = setupActivityTracking(userStore);

    // Route checks
    const isPublic = to.meta.isPublic;
    const isLoggedIn = userStore.isAuthenticated;
    const isVerified = userStore.user?.verified;

    if (userStore.config.debug) {
      console.log('[Router] Navigation:', {
        to: to.path,
        isPublic,
        isLoggedIn,
        isVerified,
        userLoaded
      });
    }

    // Verification page is always accessible
    if (to.path === '/auth/verify-otp') {
      return next();
    }

    // Protected routes
    if (!isPublic) {
      if (!isLoggedIn) {
        if (userStore.config.debug) console.log('[Router] Redirecting to login (not authenticated)');
        cleanup();
        return next('/login');
      }
      if (!isVerified) {
        if (userStore.config.debug) console.log('[Router] Redirecting to OTP verification (not verified)');
        cleanup();
        return next('/auth/verify-otp');
      }
    }

    // Redirect authenticated users away from auth pages
    if (isLoggedIn && isVerified && 
        ['/login', '/register', '/forgotpassword'].includes(to.path)) {
      if (userStore.config.debug) console.log('[Router] Redirecting to dashboard (already authenticated)');
      cleanup();
      return next('/app/dashboard');
    }

    // Start session timers if authenticated and verified
    if (isLoggedIn && isVerified && userLoaded) {
      if (userStore.config.debug) console.log('[Router] Starting session timers');
      userStore.startSessionTimers();
    }

    cleanup();
    next();
  } catch (error) {
    console.error('[Router] Error:', error);
    next('/login');
  }
});

export default router;