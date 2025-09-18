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

// import { defineStore } from 'pinia';
// import { ref, computed } from 'vue';
// import { useRouter } from 'vue-router';

// export const useUserStore = defineStore('user', () => {
//   const router = useRouter();
  
//   // State
//   const user = ref(null);
//   const userId = ref(null);
//   const sessionStart = ref(null);
//   const authType = ref(null);
//   const isFreshLogin = ref(false);
//   const justVerified = ref(false);
//   let sessionDurationTimer = null;

//   // Configuration - adjust these values as needed
//   const config = {
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
//     const sessionTooLong = sessionStart.value ? (now - sessionStart.value) >= config.sessionDuration : false;
    
//     return !sessionTooLong;
//   });
  
//   const userProfile = computed(() => ({
//     name: user.value?.name || 'Guest',
//     email: user.value?.email || '',
//     phoneNumber: user.value?.phoneNumber || '',
//     profilePicture: user.value?.profilePicture || '',
//     avatar: user.value?.avatar || { icon: '👤' },
//     verified: user.value?.verified || false,
//     authType: user.value?.authType || authType.value
//   }));

//   const isFreshLoginState = computed(() => isFreshLogin.value);
//   const isJustVerified = computed(() => justVerified.value);

//   // Function to fetch complete user data from server
//   const fetchUserData = async (id) => {
//     try {
//       debugLog('Fetching user data from server for ID:', id);
      
//       // Import API dynamically to avoid circular dependencies
//       const apiModule = await import('../api/index.js');
//       const api = apiModule.default;
      
//       const response = await api.get(`/users/${id}`);
//       const userData = response.data.user;
      
//       debugLog('Fetched user data:', userData);
      
//       return {
//         _id: userData._id || id,
//         id: userData.id || id,
//         name: userData.name || '',
//         phoneNumber: userData.phoneNumber || '',
//         authType: userData.authType || authType.value,
//         avatar: userData.avatar || { icon: '👤' },
//         createdAt: userData.createdAt || new Date(),
//         updatedAt: userData.updatedAt || new Date(),
//         verified: userData.verified || false
//       };
//     } catch (error) {
//       debugLog('Error fetching user data:', error);
//       throw error;
//     }
//   };

//   // Load user function
//   const loadUser = async () => {
//     try {
//       const storedUser = localStorage.getItem('user');
//       if (!storedUser) {
//         debugLog('No user data found in localStorage');
//         return false;
//       }

//       const parsedData = JSON.parse(storedUser);
//       const { user: userData, userId: id, sessionStart: startTime, authType: storedAuthType } = parsedData;
      
//       const now = Date.now();
      
//       // Check if session has expired based on stored timestamp
//       if (startTime && (now - startTime) >= config.sessionDuration) {
//         debugLog('Session expired before loading');
//         clearUser();
//         return false;
//       }

//       user.value = userData;
//       userId.value = id;
//       sessionStart.value = startTime;
//       authType.value = storedAuthType || userData.authType;
      
//       debugLog('User loaded from storage:', {
//         user: user.value,
//         userId: userId.value,
//         authType: authType.value,
//         sessionStart: new Date(sessionStart.value)
//       });

//       startSessionTimers();
//       return true;
//     } catch (e) {
//       debugLog("Failed to parse user data:", e);
//       clearUser();
//       return false;
//     }
//   };

//   // Set user function
//   const setUser = async (userData, id = null) => {
//     try {
//       const userIdToUse = id || userData._id || userData.id;
      
//       let completeUserData = userData;
      
//       // If we have a user ID but incomplete data, fetch complete data
//       if (userIdToUse && (!userData.name || !userData.phoneNumber || !userData.authType)) {
//         try {
//           completeUserData = await fetchUserData(userIdToUse);
//         } catch (error) {
//           debugLog('Failed to fetch user data, using provided data:', error);
//           // Continue with provided data even if incomplete
//         }
//       }

//       const now = Date.now();
//       user.value = completeUserData;
//       userId.value = userIdToUse;
//       sessionStart.value = now;
//       authType.value = completeUserData.authType;
//       isFreshLogin.value = true; // Set fresh login flag
      
//       localStorage.setItem('user', JSON.stringify({
//         user: completeUserData,
//         userId: userIdToUse,
//         sessionStart: now,
//         authType: authType.value
//       }));

//       debugLog('User set:', {
//         user: user.value,
//         userId: userId.value,
//         authType: authType.value,
//         sessionStart: new Date(sessionStart.value),
//         isFreshLogin: isFreshLogin.value
//       });

//       startSessionTimers();
      
//       // Clear the fresh login flag after a short delay
//       setTimeout(() => {
//         isFreshLogin.value = false;
//       }, 5000); // 5 seconds should be enough
//     } catch (error) {
//       debugLog('Error setting user:', error);
//       throw error;
//     }
//   };

//   // Update user function
//   const updateUser = (updates) => {
//     if (!user.value) return;
    
//     user.value = { ...user.value, ...updates };
    
//     // Update localStorage
//     const storedData = JSON.parse(localStorage.getItem('user') || '{}');
//     localStorage.setItem('user', JSON.stringify({
//       ...storedData,
//       user: user.value
//     }));
    
//     debugLog('User updated:', user.value);
//   };

//   // Mark user as verified
//   const markAsVerified = () => {
//     if (!user.value) return;
    
//     user.value.verified = true;
//     justVerified.value = true;
    
//     // Update localStorage
//     const storedData = JSON.parse(localStorage.getItem('user') || '{}');
//     localStorage.setItem('user', JSON.stringify({
//       ...storedData,
//       user: user.value
//     }));
    
//     debugLog('User marked as verified:', user.value);
    
//     // Clear the verification flag after a short time
//     setTimeout(() => {
//       justVerified.value = false;
//     }, 5000); // 5 seconds should be enough
//   };

//   // Clear user function
//   const clearUser = () => {
//     debugLog('Clearing user data');
//     user.value = null;
//     userId.value = null;
//     sessionStart.value = null;
//     authType.value = null;
//     isFreshLogin.value = false;
//     justVerified.value = false;
//     localStorage.removeItem('user');
//     clearTimers();
//   };

//   // Logout function
//   const logout = () => {
//     debugLog('Logging out user');
//     clearUser();
//     // Only redirect if we're not already on the login page
//     if (router.currentRoute.value.path !== '/login') {
//       router.push('/login');
//     }
//   };

//   // Session management
//   const startSessionTimers = () => {
//     debugLog('Starting session timers');
//     clearTimers();
    
//     const now = Date.now();
//     const timeSinceSessionStart = sessionStart.value ? now - sessionStart.value : 0;
    
//     debugLog('Timer state:', {
//       sessionStart: new Date(sessionStart.value),
//       timeSinceSessionStart
//     });

//     // Set timer for absolute session duration
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

//   const clearTimers = () => {
//     debugLog('Clearing all timers');
//     if (sessionDurationTimer) clearTimeout(sessionDurationTimer);
//     sessionDurationTimer = null;
//   };

//   // Initialize store
//   loadUser();

//   return {
//     // State
//     user,
//     userId,
//     authType,
//     config,
    
//     // Getters
//     isAuthenticated,
//     isSessionValid,
//     userProfile,
//     isFreshLoginState,
//     isJustVerified,
    
//     // Actions
//     loadUser,
//     setUser,
//     updateUser,
//     markAsVerified,
//     clearUser,
//     logout,
//     startSessionTimers,
//     clearTimers,
//     fetchUserData
//   };
// });