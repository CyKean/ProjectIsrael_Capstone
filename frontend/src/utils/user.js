// // utils/user.js
// import { defineStore } from 'pinia';
// import { ref, computed } from 'vue';
// import { useRouter } from 'vue-router';

// export const useUserStore = defineStore('user', () => {
//   const router = useRouter();
  
//   // State
//   const user = ref(null);
//   const userId = ref(null);
//   const lastActivity = ref(Date.now());
//   const sessionStart = ref(null);
//   const showTimeoutWarning = ref(false);
//   let inactivityTimer = null;
//   let warningTimer = null;
//   let sessionDurationTimer = null;

//   // Configuration - adjust these values as needed
//   const config = {
//     warningTimeout: 5 * 60 * 1000,  // 5 minute warning before inactivity logout
//     inactivityTimeout: 10 * 60 * 1000, // 30 minutes of inactivity
//     sessionDuration: 240 * 60 * 60 * 1000, // 24 hours total session duration
//     debug: true // Enable debug logging
//   };

//   // Helper function for debug logging
//   const debugLog = (...args) => {
//     if (config.debug) {
//       console.log('[UserStore]', ...args);
//     }
//   };

//   // Getters
//   const isAuthenticated = computed(() => !!user.value);
//   const isSessionValid = computed(() => {
//     if (!user.value) return false;
    
//     const now = Date.now();
//     const inactiveTooLong = (now - lastActivity.value) >= config.inactivityTimeout;
//     const sessionTooLong = sessionStart.value ? (now - sessionStart.value) >= config.sessionDuration : false;
    
//     return !inactiveTooLong && !sessionTooLong;
//   });
  
//   const userProfile = computed(() => ({
//     name: user.value?.name || 'Guest',
//     email: user.value?.email || '',
//     phoneNumber: user.value?.phoneNumber || '',
//     profilePicture: user.value?.profilePicture || '',
//     avatar: user.value?.avatar || { icon: '👤' },
//     verified: user.value?.verified || false
//   }));

//   // Actions
//   const loadUser = () => {
//     try {
//       const storedUser = localStorage.getItem('user');
//       if (!storedUser) {
//         debugLog('No user data found in localStorage');
//         return false;
//       }

//       const parsedData = JSON.parse(storedUser);
//       const { user: userData, userId: id, sessionStart: startTime, lastActivity: lastActive } = parsedData;
      
//       const now = Date.now();
      
//       // Check if session has expired based on stored timestamp
//       if (startTime && (now - startTime) >= config.sessionDuration) {
//         debugLog('Session expired before loading');
//         clearUser();
//         return false;
//       }
      
//       // Check if inactive period has exceeded
//       if (lastActive && (now - lastActive) >= config.inactivityTimeout) {
//         debugLog('Inactivity period exceeded before loading');
//         clearUser();
//         return false;
//       }

//       user.value = userData;
//       userId.value = id;
//       sessionStart.value = startTime; // Keep original session start time
//       lastActivity.value = now; // Update last activity to now
      
//       localStorage.setItem('user', JSON.stringify({
//         user: userData,
//         userId: id,
//         sessionStart: startTime,
//         lastActivity: lastActivity.value
//       }));

//       debugLog('User loaded from storage:', {
//         user: user.value,
//         userId: userId.value,
//         sessionStart: new Date(sessionStart.value),
//         lastActivity: new Date(lastActivity.value)
//       });

//       startSessionTimers();
//       return true;
//     } catch (e) {
//       debugLog("Failed to parse user data:", e);
//       clearUser();
//       return false;
//     }
//   };

//   const setUser = (userData, id = null) => {
//     const completeUserData = {
//       name: '',
//       phoneNumber: '',
//       profilePicture: '',
//       avatar: { icon: '👤' },
//       verified: false,
//       ...userData
//     };

//     const now = Date.now();
//     user.value = completeUserData;
//     userId.value = id;
//     sessionStart.value = now;
//     lastActivity.value = now;
    
//     localStorage.setItem('user', JSON.stringify({
//       user: completeUserData,
//       userId: id,
//       sessionStart: now,
//       lastActivity: now
//     }));

//     debugLog('User set:', {
//       user: user.value,
//       userId: userId.value,
//       sessionStart: new Date(sessionStart.value),
//       lastActivity: new Date(lastActivity.value)
//     });

//     startSessionTimers();
//   };

//   const clearUser = () => {
//     debugLog('Clearing user data');
//     user.value = null;
//     userId.value = null;
//     sessionStart.value = null;
//     lastActivity.value = Date.now();
//     localStorage.removeItem('user');
//     clearTimers();
//     showTimeoutWarning.value = false;
//   };

//   const logout = () => {
//     debugLog('Logging out user');
//     clearUser();
//     router.push('/login');
//   };

//   // Session management
//   const startSessionTimers = () => {
//     debugLog('Starting session timers');
//     clearTimers();
    
//     const now = Date.now();
//     const timeSinceLastActivity = now - lastActivity.value;
//     const timeSinceSessionStart = sessionStart.value ? now - sessionStart.value : 0;
    
//     debugLog('Timer state:', {
//       lastActivity: new Date(lastActivity.value),
//       sessionStart: new Date(sessionStart.value),
//       timeSinceLastActivity,
//       timeSinceSessionStart
//     });

//     // Only set timers if session hasn't expired
//     if (timeSinceSessionStart < config.sessionDuration) {
//       // 1. Set timer for showing inactivity warning
//       const timeToWarning = config.inactivityTimeout - timeSinceLastActivity - config.warningTimeout;
//       if (timeToWarning > 0) {
//         warningTimer = setTimeout(() => {
//           debugLog('Showing inactivity warning');
//           showTimeoutWarning.value = true;
//         }, timeToWarning);
//       }

//       // 2. Set timer for actual inactivity logout
//       const timeToInactiveLogout = config.inactivityTimeout - timeSinceLastActivity;
//       if (timeToInactiveLogout > 0) {
//         inactivityTimer = setTimeout(() => {
//           debugLog('Logging out due to inactivity');
//           logout();
//         }, timeToInactiveLogout);
//       } else {
//         debugLog('Inactivity period already exceeded');
//         logout();
//       }
//     }

//     // 3. Set timer for absolute session duration
//     if (sessionStart.value) {
//       const timeLeft = config.sessionDuration - timeSinceSessionStart;
//       if (timeLeft > 0) {
//         sessionDurationTimer = setTimeout(() => {
//           debugLog('Logging out due to session duration limit');
//           logout();
//         }, timeLeft);
//       } else {
//         debugLog('Session already expired');
//         logout();
//       }
//     }
//   };

//   const resetInactivityTimer = () => {
//     debugLog('Resetting inactivity timer');
//     lastActivity.value = Date.now();
//     showTimeoutWarning.value = false;
    
//     // Update localStorage with new lastActivity
//     if (user.value) {
//       localStorage.setItem('user', JSON.stringify({
//         user: user.value,
//         userId: userId.value,
//         sessionStart: sessionStart.value,
//         lastActivity: lastActivity.value
//       }));
//     }
    
//     startSessionTimers();
//   };

//   const clearTimers = () => {
//     debugLog('Clearing all timers');
//     if (inactivityTimer) clearTimeout(inactivityTimer);
//     if (warningTimer) clearTimeout(warningTimer);
//     if (sessionDurationTimer) clearTimeout(sessionDurationTimer);
//     inactivityTimer = null;
//     warningTimer = null;
//     sessionDurationTimer = null;
//   };

//   // Initialize store
//   loadUser();

//   return {
//     // State
//     user,
//     userId,
//     showTimeoutWarning,
//     config,
    
//     // Getters
//     isAuthenticated,
//     isSessionValid,
//     userProfile,
    
//     // Actions
//     loadUser,
//     setUser,
//     clearUser,
//     logout,
//     resetInactivityTimer,
//     startSessionTimers,
//     clearTimers
//   };
// });

// utils/user.js
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export const useUserStore = defineStore('user', () => {
  const router = useRouter();
  
  // State
  const user = ref(null);
  const userId = ref(null);
  const sessionStart = ref(null);
  let sessionDurationTimer = null;

  // Configuration - adjust these values as needed
  const config = {
    sessionDuration: 240 * 60 * 60 * 1000, // 24 hours total session duration
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
    
    const now = Date.now();
    const sessionTooLong = sessionStart.value ? (now - sessionStart.value) >= config.sessionDuration : false;
    
    return !sessionTooLong;
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

      const parsedData = JSON.parse(storedUser);
      const { user: userData, userId: id, sessionStart: startTime } = parsedData;
      
      const now = Date.now();
      
      // Check if session has expired based on stored timestamp
      if (startTime && (now - startTime) >= config.sessionDuration) {
        debugLog('Session expired before loading');
        clearUser();
        return false;
      }

      user.value = userData;
      userId.value = id;
      sessionStart.value = startTime;
      
      localStorage.setItem('user', JSON.stringify({
        user: userData,
        userId: id,
        sessionStart: startTime
      }));

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

    const now = Date.now();
    user.value = completeUserData;
    userId.value = id;
    sessionStart.value = now;
    
    localStorage.setItem('user', JSON.stringify({
      user: completeUserData,
      userId: id,
      sessionStart: now
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
    const timeSinceSessionStart = sessionStart.value ? now - sessionStart.value : 0;
    
    debugLog('Timer state:', {
      sessionStart: new Date(sessionStart.value),
      timeSinceSessionStart
    });

    // Set timer for absolute session duration
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

  const clearTimers = () => {
    debugLog('Clearing all timers');
    if (sessionDurationTimer) clearTimeout(sessionDurationTimer);
    sessionDurationTimer = null;
  };

  // Initialize store
  loadUser();

  return {
    // State
    user,
    userId,
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
    startSessionTimers,
    clearTimers
  };
});