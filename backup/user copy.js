// stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    uid: null
  }),
  actions: {
    setUser(user, uid) {
      this.user = user
      this.uid = uid
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('uid', uid)
    },
    loadUser() {
      const storedUser = localStorage.getItem('user')
      const storedUid = localStorage.getItem('uid')
      if (storedUser && storedUid) {
        this.user = JSON.parse(storedUser)
        this.uid = storedUid
      }
    },
    logout() {
      this.user = null
      this.uid = null
      localStorage.removeItem('user')
      localStorage.removeItem('uid')
    }
  }
})

//=========================


// utils/user.js
// import { defineStore } from 'pinia';
// import { ref, computed } from 'vue';
// import { useRouter } from 'vue-router';

// export const useUserStore = defineStore('user', () => {
//   const router = useRouter();
  
//   // State
//   const user = ref(null);
//   const userId = ref(null);
//   const lastActivity = ref(Date.now());
//   const showTimeoutWarning = ref(false);
//   let inactivityTimer = null;
//   let warningTimer = null;

//   // Configuration - adjust these values as needed
//   const config = {
//     warningTimeout: 1 * 60 * 1000,  // 5 minute warning before logout
//     inactivityTimeout: 2 * 60 * 1000 // 30 minutes of inactivity
//   };

//   // Getters
//   const isAuthenticated = computed(() => !!user.value);
//   const isSessionValid = computed(() => {
//     if (!user.value) return false;
//     return (Date.now() - lastActivity.value < config.inactivityTimeout);
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
//     const storedUser = localStorage.getItem('user');
//     if (!storedUser) return false;

//     try {
//       const { user: userData, userId: id } = JSON.parse(storedUser);
//       user.value = userData;
//       userId.value = id;
//       lastActivity.value = Date.now();
//       startInactivityTimer();
//       return true;
//     } catch (e) {
//       console.error("Failed to parse user data:", e);
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

//     user.value = completeUserData;
//     userId.value = id;
//     lastActivity.value = Date.now();
    
//     localStorage.setItem('user', JSON.stringify({
//       user: completeUserData,
//       userId: id
//     }));

//     startInactivityTimer();
//   };

//   const clearUser = () => {
//     user.value = null;
//     userId.value = null;
//     localStorage.removeItem('user');
//     clearTimers();
//     showTimeoutWarning.value = false;
//   };

//   const logout = () => {
//     clearUser();
//     router.push('/login');
//   };

//   // Session management
//   const startInactivityTimer = () => {
//     clearTimers();
    
//     // Set timer for showing warning
//     warningTimer = setTimeout(() => {
//       showTimeoutWarning.value = true;
//     }, config.inactivityTimeout - config.warningTimeout);
    
//     // Set timer for actual logout
//     inactivityTimer = setTimeout(() => {
//       logout();
//     }, config.inactivityTimeout);
//   };

//   const resetInactivityTimer = () => {
//     lastActivity.value = Date.now();
//     showTimeoutWarning.value = false;
//     startInactivityTimer();
//   };

//   const clearTimers = () => {
//     if (inactivityTimer) clearTimeout(inactivityTimer);
//     if (warningTimer) clearTimeout(warningTimer);
//     inactivityTimer = null;
//     warningTimer = null;
//   };

//   // Initialize store
//   loadUser();

//   return {
//     // State
//     user,
//     userId,
//     showTimeoutWarning,
    
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
//     startInactivityTimer,
//     clearTimers
//   };
// });



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
//   const showTimeoutWarning = ref(false);
//   let inactivityTimer = null;
//   let warningTimer = null;

//   // Configuration - adjust these values as needed
//   const config = {
//     warningTimeout: 5 * 60 * 1000,  // 5 minute warning before logout
//     inactivityTimeout: 30 * 60 * 1000 // 30 minutes of inactivity
//   };

//   // Getters
//   const isAuthenticated = computed(() => !!user.value);
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
//     const storedUser = localStorage.getItem('user');
//     if (!storedUser) return false;

//     try {
//       const { user: userData, userId: id } = JSON.parse(storedUser);
//       user.value = userData;
//       userId.value = id;
//       lastActivity.value = Date.now();
//       startInactivityTimer();
//       return true;
//     } catch (e) {
//       console.error("Failed to parse user data:", e);
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

//     user.value = completeUserData;
//     userId.value = id;
//     lastActivity.value = Date.now();
    
//     localStorage.setItem('user', JSON.stringify({
//       user: completeUserData,
//       userId: id
//     }));

//     startInactivityTimer();
//   };

//   const clearUser = () => {
//     user.value = null;
//     userId.value = null;
//     localStorage.removeItem('user');
//     clearTimers();
//     showTimeoutWarning.value = false;
//   };

//   const logout = () => {
//     clearUser();
//     router.push('/login');
//   };

//   // Session management
//   const startInactivityTimer = () => {
//     clearTimers();
    
//     // Set timer for showing warning
//     warningTimer = setTimeout(() => {
//       showTimeoutWarning.value = true;
//     }, config.inactivityTimeout - config.warningTimeout);
    
//     // Set timer for actual logout
//     inactivityTimer = setTimeout(() => {
//       logout();
//     }, config.inactivityTimeout);
//   };

//   const resetInactivityTimer = () => {
//     lastActivity.value = Date.now();
//     showTimeoutWarning.value = false;
//     startInactivityTimer();
//   };

//   const clearTimers = () => {
//     if (inactivityTimer) clearTimeout(inactivityTimer);
//     if (warningTimer) clearTimeout(warningTimer);
//     inactivityTimer = null;
//     warningTimer = null;
//   };

//   // Initialize store
//   loadUser();

//   return {
//     // State
//     user,
//     userId,
//     showTimeoutWarning,
    
//     // Getters
//     isAuthenticated,
//     userProfile,
    
//     // Actions
//     loadUser,
//     setUser,
//     clearUser,
//     logout,
//     resetInactivityTimer,
//     startInactivityTimer
//   };
// });