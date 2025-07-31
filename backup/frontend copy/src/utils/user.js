// utils/user.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export const useUserStore = defineStore('user', () => {
  const router = useRouter();
  
  // State
  const user = ref(null);
  const userId = ref(null);
  const lastActivity = ref(Date.now());
  const sessionStart = ref(null);
  const showTimeoutWarning = ref(false);
  let inactivityTimer = null;
  let warningTimer = null;
  let sessionDurationTimer = null;

  // Configuration - adjust these values as needed
  const config = {
    warningTimeout: 5 * 60 * 1000,  // 1 minute warning before logout
    inactivityTimeout: 1440 * 60 * 1000, // 30 minutes of inactivity
    sessionDuration: 1440 * 60 * 1000, // 1 hour total session duration
    debug: true // Enable debug logging
  };

  // Helper function for debug logging
  const debugLog = (...args) => {
    if (config.debug) {
      console.log('[UserStore]', ...args);
    }
  };

  // Getters
  const isAuthenticated = computed(() => !!user.value);
  const isSessionValid = computed(() => {
    if (!user.value) return false;
    
    // Check both inactivity and total session duration
    const now = Date.now();
    const inactiveTooLong = (now - lastActivity.value) >= config.inactivityTimeout;
    const sessionTooLong = sessionStart.value ? (now - sessionStart.value) >= config.sessionDuration : false;
    
    return !inactiveTooLong && !sessionTooLong;
  });
  
  const userProfile = computed(() => ({
    name: user.value?.name || 'Guest',
    email: user.value?.email || '',
    phoneNumber: user.value?.phoneNumber || '',
    profilePicture: user.value?.profilePicture || '',
    avatar: user.value?.avatar || { icon: '👤' },
    verified: user.value?.verified || false
  }));

  // Actions
  const loadUser = () => {
    try {
      const storedUser = localStorage.getItem('user');
      if (!storedUser) {
        debugLog('No user data found in localStorage');
        return false;
      }

      const { user: userData, userId: id, sessionStart: startTime } = JSON.parse(storedUser);
      user.value = userData;
      userId.value = id;
      sessionStart.value = startTime || Date.now();
      lastActivity.value = Date.now();
      
      debugLog('User loaded from storage:', {
        user: user.value,
        userId: userId.value,
        sessionStart: new Date(sessionStart.value)
      });

      startSessionTimers();
      return true;
    } catch (e) {
      debugLog("Failed to parse user data:", e);
      clearUser();
      return false;
    }
  };

  const setUser = (userData, id = null) => {
    const completeUserData = {
      name: '',
      phoneNumber: '',
      profilePicture: '',
      avatar: { icon: '👤' },
      verified: false,
      ...userData
    };

    user.value = completeUserData;
    userId.value = id;
    sessionStart.value = Date.now();
    lastActivity.value = Date.now();
    
    localStorage.setItem('user', JSON.stringify({
      user: completeUserData,
      userId: id,
      sessionStart: sessionStart.value
    }));

    debugLog('User set:', {
      user: user.value,
      userId: userId.value,
      sessionStart: new Date(sessionStart.value)
    });

    startSessionTimers();
  };

  const clearUser = () => {
    debugLog('Clearing user data');
    user.value = null;
    userId.value = null;
    sessionStart.value = null;
    localStorage.removeItem('user');
    clearTimers();
    showTimeoutWarning.value = false;
  };

  const logout = () => {
    debugLog('Logging out user');
    clearUser();
    router.push('/login');
  };

  // Session management
  const startSessionTimers = () => {
    debugLog('Starting session timers');
    clearTimers();
    
    const now = Date.now();
    const timeSinceLastActivity = now - lastActivity.value;
    const timeSinceSessionStart = sessionStart.value ? now - sessionStart.value : 0;
    
    debugLog('Timer state:', {
      lastActivity: new Date(lastActivity.value),
      sessionStart: new Date(sessionStart.value),
      timeSinceLastActivity,
      timeSinceSessionStart
    });

    // Set timer for showing warning
    const timeToWarning = config.inactivityTimeout - timeSinceLastActivity - config.warningTimeout;
    if (timeToWarning > 0) {
      warningTimer = setTimeout(() => {
        debugLog('Showing inactivity warning');
        showTimeoutWarning.value = true;
      }, timeToWarning);
    }

    // Set timer for actual logout due to inactivity
    const timeToInactiveLogout = config.inactivityTimeout - timeSinceLastActivity;
    if (timeToInactiveLogout > 0) {
      inactivityTimer = setTimeout(() => {
        debugLog('Logging out due to inactivity');
        logout();
      }, timeToInactiveLogout);
    }

    // Set timer for session duration limit
    if (sessionStart.value) {
      const timeLeft = config.sessionDuration - timeSinceSessionStart;
      if (timeLeft > 0) {
        sessionDurationTimer = setTimeout(() => {
          debugLog('Logging out due to session duration limit');
          logout();
        }, timeLeft);
      } else {
        debugLog('Session already expired');
        logout();
      }
    }
  };

  // In user.js
  const resetInactivityTimer = () => {
    debugLog('Resetting inactivity timer and extending session');
    lastActivity.value = Date.now();
    sessionStart.value = Date.now(); // This resets the session duration clock
    showTimeoutWarning.value = false;
    
    // Update localStorage to persist the new session start time
    if (user.value) {
      localStorage.setItem('user', JSON.stringify({
        user: user.value,
        userId: userId.value,
        sessionStart: sessionStart.value
      }));
    }
    
    startSessionTimers();
  };

  const clearTimers = () => {
    debugLog('Clearing all timers');
    if (inactivityTimer) clearTimeout(inactivityTimer);
    if (warningTimer) clearTimeout(warningTimer);
    if (sessionDurationTimer) clearTimeout(sessionDurationTimer);
    inactivityTimer = null;
    warningTimer = null;
    sessionDurationTimer = null;
  };

  // Initialize store
  loadUser();

  return {
    // State
    user,
    userId,
    showTimeoutWarning,
    config,
    
    // Getters
    isAuthenticated,
    isSessionValid,
    userProfile,
    
    // Actions
    loadUser,
    setUser,
    clearUser,
    logout,
    resetInactivityTimer,
    startSessionTimers,
    clearTimers
  };
});