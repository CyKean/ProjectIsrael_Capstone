<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 relative overflow-hidden">
    <!-- Falling Leaves Animation - Fixed -->
    <div class="absolute inset-0 pointer-events-none z-0 overflow-hidden">
      <div v-for="i in leafCount" :key="`leaf1-${i}`" 
           class="leaf absolute animate-fall"
           :style="{
             left: `${Math.random() * 100}%`,
             top: `${Math.random() * -200}%`,
             animationDuration: `${15 + Math.random() * 15}s`,
             animationDelay: `${Math.random() * -30}s`,
             transform: `scale(${isMobile ? 0.8 : 1})`
           }">
        <img 
          src="/public/images/leaves-plants/fall-leaf1.png"
          alt="" 
          class="w-16 xs:w-20 sm:w-24 h-16 xs:h-20 sm:h-24 opacity-50"
        />
      </div>
      
      <div v-for="i in leafCount" :key="`leaf2-${i}`" 
           class="leaf absolute animate-fall"
           :style="{
             left: `${Math.random() * 100}%`,
             top: `${Math.random() * -200}%`,
             animationDuration: `${15 + Math.random() * 15}s`,
             animationDelay: `${Math.random() * -30}s`,
             transform: `scale(${isMobile ? 0.8 : 1})`
           }">
        <img 
          src="/public/images/leaves-plants/fall-leaf2.png"
          alt="" 
          class="w-20 xs:w-24 sm:w-28 h-20 xs:h-24 sm:h-28 opacity-50"
        />
      </div>
    </div>

    <transition name="page-transition" mode="out-in" @before-leave="beforeLeave" @enter="enter" @after-enter="afterEnter">
      <div :key="transitionKey" class="page-content relative z-10" :style="contentStyle">
        <div class="max-w-3xl w-[95%] xs:w-[90%] sm:w-[85%] md:w-full min-h-[400px] xs:min-h-[450px] sm:min-h-[500px] flex shadow-xl rounded-xl overflow-hidden relative z-20">
          <!-- Left Side - Image and Branding -->
          <div class="hidden md:flex md:w-1/2 bg-[#2B5329] text-white p-4 sm:p-6 md:p-8 flex-col justify-end relative">
            <!-- Background Image -->
            <div 
              class="absolute inset-0 bg-cover bg-center"
              style="background-image: url('/public/images/greenhouse.jpg');"
            ></div>
            <!-- Dark gradient overlay -->
            <div class="absolute inset-0 bg-gradient-to-r from-[#1A3A1A] via-[#2B5329]/95 to-[#2B5329]/85"></div>
            
            <!-- Content -->
            <div class="relative flex flex-col items-center z-10 mt-0 pt-4 mb-auto">
              <div class="w-32 xs:w-36 sm:w-40 h-32 xs:h-36 sm:h-40 mb-2 relative overflow-visible">
                <img 
                  src="/images/plants.gif"
                  alt="Growing plant animation"   
                  class="w-[130%] h-[130%] max-w-none object-contain mix-blend-multiply filter brightness-100 contrast-100 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
                />
              </div>
              <h2 class="text-xl xs:text-2xl font-bold mb-1">Welcome Back!</h2>
              <p class="text-xs xs:text-sm text-gray-200/90 mt-1 text-center font-light">Your trusted partner in crop recommendations and agricultural wisdom.</p>
            </div>

            <div class="relative flex justify-center z-10">
              <button 
                @click="handleBackToWebsite" 
                class="text-white hover:text-[#FFA500] flex items-center gap-1 xs:gap-2 transition-colors duration-300 border border-white/50 rounded-lg px-3 xs:px-4 py-1.5 xs:py-2 hover:bg-white/20"
              >
                <ArrowLeft class="h-3 xs:h-4 w-3 xs:w-4" />
                <span class="text-xs xs:text-sm">Back to website</span>
              </button>
            </div>
          </div>

          <!-- Right Side - Login Form -->
          <div class="w-full md:w-1/2 bg-white p-4 xs:p-6 flex flex-col">
            <div class="w-full max-w-xs mx-auto flex-1 flex flex-col justify-center">
              <h2 class="text-lg xs:text-xl font-bold text-[#2B5329] text-center mb-4 xs:mb-6">Login to your Account</h2>

              <form class="space-y-3 xs:space-y-4" @submit.prevent="handleLogin">
                <div>
                  <label for="phoneNumber" class="block text-xs xs:text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    id="phoneNumber"
                    type="tel"
                    maxlength="13"
                    inputmode="numeric"
                    v-model="form.phoneNumber"
                    required
                    class="block w-full px-3 py-1.5 xs:py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329] transition-all duration-200 text-sm xs:text-base"
                    placeholder="Enter your phone number"
                  />
                </div>

                <div>
                  <label class="block text-xs xs:text-sm font-medium text-gray-700 mb-1 xs:mb-2">Choose Login Type</label>
                  <!-- Enhanced Radio Button Style Design with Green Color -->
                  <div class="flex bg-gray-50 rounded-lg p-0.5 xs:p-1 border border-gray-200">
                    <label class="flex-1 cursor-pointer">
                      <input
                        type="radio"
                        name="authType"
                        value="password"
                        v-model="form.authType"
                        class="sr-only"
                      />
                      <div :class="[
                        'flex items-center justify-center px-2 xs:px-3 py-1.5 xs:py-2 rounded-md text-xs xs:text-sm font-medium transition-all duration-200',
                        form.authType === 'password'
                          ? 'bg-[#2B5329] text-white shadow-md'
                          : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                      ]">
                        <Key class="h-3 xs:h-4 w-3 xs:w-4 mr-1 xs:mr-1.5" />
                        <span>Password</span>
                      </div>
                    </label>
                    <label class="flex-1 cursor-pointer">
                      <input
                        type="radio"
                        name="authType"
                        value="pin"
                        v-model="form.authType"
                        class="sr-only"
                      />
                      <div :class="[
                        'flex items-center justify-center px-2 xs:px-3 py-1.5 xs:py-2 rounded-md text-xs xs:text-sm font-medium transition-all duration-200',
                        form.authType === 'pin'
                          ? 'bg-[#2B5329] text-white shadow-md'
                          : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                      ]">
                        <Hash class="h-3 xs:h-4 w-3 xs:w-4 mr-1 xs:mr-1.5" />
                        <span class="whitespace-nowrap">4-digit PIN</span>
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Password Input -->
                <div v-if="form.authType === 'password'">
                  <label for="password" class="block text-xs xs:text-sm font-medium text-gray-700 mb-1">Password</label>
                  <div class="space-y-1 xs:space-y-1.5">
                    <div class="relative">
                      <input
                        id="password"
                        :type="showPassword ? 'text' : 'password'"
                        v-model="form.password"
                        required
                        class="block w-full px-3 py-1.5 xs:py-2 pr-8 xs:pr-10 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329] transition-all duration-200 text-sm xs:text-base"
                        placeholder="Enter your password"
                      />
                      <button
                        type="button"
                        @click="showPassword = !showPassword"
                        class="absolute right-2 xs:right-3 top-1/2 transform -translate-y-1/2 flex items-center justify-center text-gray-500 hover:text-gray-700 w-5 xs:w-6 h-5 xs:h-6"
                        :aria-label="showPassword ? 'Hide password' : 'Show password'"
                      >
                        <Eye v-if="!showPassword" class="h-3.5 xs:h-4 w-3.5 xs:w-4" />
                        <EyeOff v-else class="h-3.5 xs:h-4 w-3.5 xs:w-4" />
                      </button>
                    </div>
                  </div>
                </div>

                <!-- PIN Input with 4 separate boxes -->
                <div v-else>
                  <label class="block text-xs xs:text-sm font-medium text-gray-700 mb-1">Enter 4-digit PIN</label>
                  <div class="flex gap-1.5 xs:gap-2 justify-center">
                    <input
                      v-for="(digit, index) in pinDigits"
                      :key="index"
                      :ref="el => pinInputs[index] = el"
                      type="text"
                      maxlength="1"
                      inputmode="numeric"
                      pattern="[0-9]"
                      v-model="pinDigits[index]"
                      @input="handlePinInput(index, $event)"
                      @keydown="handlePinKeydown(index, $event)"
                      @paste="handlePinPaste($event)"
                      class="w-8 xs:w-10 h-8 xs:h-10 text-center text-sm xs:text-base font-semibold border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329] transition-all duration-200"
                      :class="{
                        'border-[#2B5329] bg-green-50': pinDigits[index],
                        'border-red-300 animate-pulse': pinError && !pinDigits[index]
                      }"
                    />
                  </div>
                  <p v-if="pinError" class="text-red-500 text-xs mt-1 text-center">Please enter all 4 digits</p>
                </div>

                <div class="flex items-center justify-end">
                  <router-link to="/forgotpassword" class="text-xs text-[#2B5329] hover:text-[#FFA500] transition-colors">
                    Forgot password?
                  </router-link>
                </div>

                <!-- Sign In Button -->
                <button 
                  type="submit" 
                  :disabled="isLoading || !isFormValid"
                  class="w-full flex justify-center py-1.5 xs:py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-[#2B5329] hover:bg-[#1F3D1F] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFA500] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed mt-4 xs:mt-6 text-sm xs:text-base"
                >
                  {{ isLoading ? "Signing In..." : "Sign In" }}
                </button>

                <div class="text-center mt-2 xs:mt-3 mb-2 xs:mb-4">
                  <p class="text-xs text-gray-600">
                    Don't have an account? 
                    <button 
                      @click="handleRequestNow" 
                      class="text-[#2B5329] hover:text-[#FFA500] font-medium transition-colors"
                    >
                      Request Now
                    </button>
                  </p>
                </div>
              </form>
            </div>
          </div>
        </div>
        <LoadingPage 
          :is-visible="isLoading"
          title="Signing you in..."
          message="Please wait while we verify your credentials"
          @loading-complete="onLoadingComplete"
        />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Eye, EyeOff, Chrome, Facebook, Key, Hash } from 'lucide-vue-next'
import LoadingPage from '../layout/LoadingPage.vue'
import api from '../../api/index.js'
import { auth, googleProvider, signInWithPopup } from "../../api/firebase.js"
import toastr from 'toastr'
import {
  getFirestore,
  collection,
  addDoc,
  query,
  where,
  getDocs
} from "firebase/firestore"
import { useUserStore } from '../../utils/user' // adjust path as needed
const userStore = useUserStore()

const db = getFirestore();

const router = useRouter()
const showPassword = ref(false)
const isMobile = ref(window.innerWidth < 640)
const transitionKey = ref(0)
const contentStyle = ref({})
const pinError = ref(false)
const isLoading = ref(false)

const form = ref({
  authType: 'password',  // or 'pin'
  phoneNumber: '',
  password: '',
  pin: '',
});

// PIN-related reactive data
const pinDigits = ref(['', '', '', ''])
const pinInputs = ref([])

// Computed property to check if PIN is complete
const isPinComplete = computed(() => {
  return pinDigits.value.every(digit => digit !== '')
})

// Computed property to check if password is entered
const isPasswordValid = computed(() => {
  return form.value.password.trim().length > 0
})

// Computed property to check if phone number is entered
const isPhoneValid = computed(() => {
  return form.value.phoneNumber.trim().length > 0
})

// Computed property to check if form is valid for submission
const isFormValid = computed(() => {
  const phoneValid = isPhoneValid.value
  
  if (form.value.authType === 'password') {
    return phoneValid && isPasswordValid.value
  } else {
    return phoneValid && isPinComplete.value
  }
})

// Watch for PIN completion
const updatePinValue = () => {
  form.value.pin = pinDigits.value.join('')
}

// PIN input handlers
const handlePinInput = (index, event) => {
  const value = event.target.value.replace(/[^0-9]/g, '')
  
  if (value.length > 1) {
    // Handle multiple characters (paste)
    const digits = value.split('').slice(0, 4)
    digits.forEach((digit, i) => {
      if (index + i < 4) {
        pinDigits.value[index + i] = digit
      }
    })
    // Focus on the next empty input or the last one
    const nextIndex = Math.min(index + digits.length, 3)
    nextTick(() => {
      pinInputs.value[nextIndex]?.focus()
    })
  } else {
    pinDigits.value[index] = value
    
    // Auto-focus next input
    if (value && index < 3) {
      nextTick(() => {
        pinInputs.value[index + 1]?.focus()
      })
    }
  }
  
  updatePinValue()
  pinError.value = false
}

const handlePinKeydown = (index, event) => {
  // Handle backspace
  if (event.key === 'Backspace' && !pinDigits.value[index] && index > 0) {
    nextTick(() => {
      pinInputs.value[index - 1]?.focus()
    })
  }
  
  // Handle arrow keys
  if (event.key === 'ArrowLeft' && index > 0) {
    nextTick(() => {
      pinInputs.value[index - 1]?.focus()
    })
  }
  
  if (event.key === 'ArrowRight' && index < 3) {
    nextTick(() => {
      pinInputs.value[index + 1]?.focus()
    })
  }
}

const handlePinPaste = (event) => {
  event.preventDefault()
  const pastedData = event.clipboardData.getData('text').replace(/[^0-9]/g, '')
  const digits = pastedData.split('').slice(0, 4)
  
  digits.forEach((digit, index) => {
    if (index < 4) {
      pinDigits.value[index] = digit
    }
  })
  
  updatePinValue()
  
  // Focus on the next empty input or the last filled one
  const nextIndex = Math.min(digits.length, 3)
  nextTick(() => {
    pinInputs.value[nextIndex]?.focus()
  })
}

const handleResize = () => {
  isMobile.value = window.innerWidth < 640
}

const leafCount = ref(20) // Fixed leafCount to be a constant value

const handleBackToWebsite = () => {
  transitionKey.value++
  contentStyle.value = { 
    position: 'relative', 
    left: '0px', 
    transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)' 
  }

  setTimeout(() => {
    router.push('/')
  }, 500)
}

const onLoadingComplete = () => {
  isLoading.value = false
}

const handleRequestNow = () => {
  transitionKey.value++
  contentStyle.value = { 
    position: 'relative', 
    left: '0px', 
    transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)' 
  }

  setTimeout(() => {
    router.push('/register')
  }, 500)
}

function isValidPhilippinePhoneNumber(number) {
  const cleaned = number.trim(); // only trim whitespace
  return /^(\+639|09)\d{9}$/.test(cleaned);
}

function toE164(phone) {
  const trimmed = phone.trim();
  if (trimmed.startsWith('+63')) return trimmed;
  const cleaned = trimmed.replace(/\D/g, '');
  if (cleaned.startsWith('0')) return '+63' + cleaned.slice(1);
  if (cleaned.startsWith('63')) return '+' + cleaned;
  return null;
}

const handleLogin = async () => {
  isLoading.value = true

  const { phoneNumber, password, pin, authType } = form.value
  const trimmedPhone = phoneNumber.trim()

  if (!isValidPhilippinePhoneNumber(trimmedPhone)) {
    window.showToast('Invalid Philippine phone number.', 'warning')
    isLoading.value = false
    return
  }

  const formattedPhone = toE164(trimmedPhone)
  if (!formattedPhone) {
    window.showToast('Could not format phone number.', 'warning')
    isLoading.value = false
    return
  }

  if (authType === 'pin' && !isPinComplete.value) {
    pinError.value = true
    window.showToast('Please enter all 4 digits of your PIN.', 'warning')
    isLoading.value = false
    return
  }

  const credential = authType === 'pin' ? pin : password
  if (!credential.trim()) {
    window.showToast(`Please enter your ${authType}.`, 'warning')
    isLoading.value = false
    return
  }

  try {
    const usersRef = collection(db, 'users')
    const q = query(usersRef, where('phoneNumber', '==', formattedPhone))
    const snapshot = await getDocs(q)

    if (snapshot.empty) {
      window.showToast('No account found with this phone number.', 'failed')
      return
    }

    const userDoc = snapshot.docs[0]
    const userData = userDoc.data()

    if (!userData.verified) {
      window.showToast('Account is not verified.', 'failed')
      return
    }

    if (authType === 'password' && userData.password !== password) {
      window.showToast('Incorrect password.', 'failed')
      return
    }

    if (authType === 'pin' && userData.pin !== pin) {
      window.showToast('Incorrect PIN.', 'failed')
      return
    }

    // Store the complete user data including the document ID
    const completeUserData = {
      ...userData,
      id: userDoc.id  // Make sure to include the document ID
    }

    // Save to store and localStorage
    userStore.setUser(completeUserData)
    localStorage.setItem('user', JSON.stringify({
      user: completeUserData,
      userId: userDoc.id
    }))

    window.showToast('Login successful!', 'success')
    router.push('/app/dashboard')
  } catch (error) {
    console.error('Login error:', error)
    window.showToast('Login failed.', 'failed')
  } finally {
    isLoading.value = false
  }
}

const handleGoogleLogin = async () => {
  try {
    const result = await signInWithPopup(auth, googleProvider);
    const user = result.user;

    console.log("✅ Google User:", user);

    const idToken = await user.getIdToken();
    const response = await api.post("/auth/google-login", {
      idToken: idToken
    });

    console.log("✅ Backend Response:", response.data);

    const { user: userData } = response.data;

    // ✅ Ensure a profile picture is set
    if (!userData.profilePicture) {
      userData.profilePicture = generateProfilePicture(userData.email);
    }

    // ✅ Save user info in localStorage/sessionStorage
    localStorage.setItem("user", JSON.stringify(userData));

    // ✅ Display user info in UI
    user.value = userData;  // If using Vue's ref()

    toastr.success("Google login successful!");
    router.push("/dashboard");
  } catch (error) {
    console.error("❌ Google Login Error:", error);
    toastr.error(error.response?.data?.detail || "Google login failed.");
  }
};

// ✅ Helper function for default profile picture
const generateProfilePicture = (email) => {
  const initials = email[0].toUpperCase();
  return `https://dummyimage.com/100x100/000/fff.png&text=${initials}`;
};

onMounted(() => {
  window.addEventListener('resize', handleResize)
  // Check for remembered email
  // const rememberedEmail = localStorage.getItem('rememberedEmail')
  // if (rememberedEmail) {
  //   email.value = rememberedEmail
  //   rememberMe.value = true
  // }
  
  localStorage.clear() //
  sessionStorage.clear() //
  
  if(localStorage.clear()){
    console.log('cleared local storage')
  }

})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const beforeLeave = (el) => {
  const { left } = el.getBoundingClientRect()
  el.style.left = left + 'px'
  el.style.position = 'absolute'
}

const enter = (el) => {
  const { left } = el.getBoundingClientRect()
  el.style.left = `${left + 50}px` 
  el.style.opacity = 0
}

const afterEnter = (el) => {
  el.style.left = ''
  el.style.position = ''
  el.style.opacity = ''
}
</script>

<style scoped>
@keyframes fall {
  0% {
    transform: translateY(-100%) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.4;
  }
  90% {
    opacity: 0.4;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0;
  }
}

.animate-fall {
  animation: fall linear infinite;
  will-change: transform, opacity;
  animation-play-state: running !important;
}

.leaf {
  pointer-events: none;
  z-index: 10;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
}

* {
  font-family: 'Poppins', sans-serif;
}

h2 {
  font-family: 'Poppins', sans-serif;
  font-weight: 600;
}

button, input, label {
  font-family: 'Poppins', sans-serif;
}

/* Page transition styles */
.page-transition-enter-active,
.page-transition-leave-active {
  transition: opacity 0.5s ease, transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  position: absolute;
  width: 100%;
}

.page-transition-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.page-transition-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

/* Responsive adjustments */
@media (max-width: 640px) {
  .page-content {
    padding: 1rem;
  }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .page-content {
    padding: 2rem;
  }
}

input[type="checkbox"]:checked {
  background-color: #2B5329;
  border-color: #2B5329;
}

input[type="checkbox"]:focus {
  --tw-ring-color: #2B5329;
  --tw-ring-offset-width: 0px;
}

/* Hide default radio buttons */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* PIN input animations */
@keyframes pulse {
  0%, 100% {
    border-color: #d1d5db;
  }
  50% {
    border-color: #ef4444;
  }
}

.animate-pulse {
  animation: pulse 1s ease-in-out infinite;
}
</style>