// router/guards.js
import { useUserStore } from '../utils/user';

export function setupRouterGuards(router, { setupActivityTracking }) {
  router.beforeEach(async (to, from, next) => {
    const userStore = useUserStore();
    const cleanupTracking = setupActivityTracking?.(userStore);

    try {
      await userStore.loadUser();

      // Public routes bypass
      if (to.meta.isPublic) return next();

      // Verification route exception
      if (to.path === '/auth/verify-otp') return next();

      // Auth checks
      if (!userStore.user) {
        cleanupTracking?.();
        return next('/login');
      }

      if (!userStore.user.verified && to.path !== '/auth/verify-otp') {
        cleanupTracking?.();
        return next('/auth/verify-otp');
      }

      // Redirect authed users from auth pages
      if (['/login', '/register'].includes(to.path)) {
        cleanupTracking?.();
        return next('/app/dashboard');
      }

      // Start session timer for protected routes
      if (to.meta.requiresAuth) {
        userStore.startSessionTimer?.();
      }

      next();
    } catch (error) {
      console.error('Router guard error:', error);
      cleanupTracking?.();
      next('/login');
    }
  });
}