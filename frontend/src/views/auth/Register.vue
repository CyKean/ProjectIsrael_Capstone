<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-3 xs:px-4 sm:px-6 lg:px-8 py-4 xs:py-6 relative overflow-hidden">
    <!-- Falling Leaves Animation -->
    <div class="absolute inset-0 pointer-events-none z-0 overflow-hidden">
      <div v-for="i in leafCount" :key="`leaf1-${i}`"
           class="leaf absolute animate-fall"
           :style="{
             left: `${leafPositions[i].left}%`,
             top: `${leafPositions[i].top}%`,
             animationDuration: `${leafPositions[i].duration}s`,
             animationDelay: `${leafPositions[i].delay}s`,
             transform: `scale(${isMobile ? 0.6 : 0.9})`
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
             left: `${leafPositions[i].left}%`,
             top: `${leafPositions[i].top}%`,
             animationDuration: `${leafPositions[i].duration}s`,
             animationDelay: `${leafPositions[i].delay}s`,
             transform: `scale(${isMobile ? 0.6 : 0.9})`
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
          <div class="hidden md:flex md:w-1/2 bg-[#2B5329] text-white p-4 sm:p-6 md:p-8 flex-col justify-between relative">
            <!-- Background Image -->
            <div
              class="absolute inset-0 bg-cover bg-center"
              style="background-image: url('/public/images/greenhouse.jpg');"
            ></div>
            <div class="absolute inset-0 bg-gradient-to-r from-[#1A3A1A] via-[#2B5329]/95 to-[#2B5329]/85"></div>

            <div class="relative flex flex-col items-center z-10 mt-0 pt-4 mb-auto">
              <div class="w-32 xs:w-36 sm:w-40 h-32 xs:h-36 sm:h-40 mb-2 relative overflow-visible">
                <img
                  src="/images/plants.gif"
                  alt="Growing plant animation"
                  class="w-[130%] h-[130%] max-w-none object-contain mix-blend-multiply filter brightness-100 contrast-100 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
                />
              </div>
              <h2 class="text-xl xs:text-2xl font-bold mb-1">Harvesting Knowledge</h2>
              <p class="text-xs xs:text-sm text-gray-200/90 mt-1 text-center font-light">Your trusted partner in crop recommendations and agricultural wisdom.</p>
            </div>

            <!-- Back to Website -->
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

          <!-- Right Side - Registration Form -->
          <div class="w-full md:w-1/2 bg-white p-4 xs:p-5 flex justify-center items-center">
            <div class="w-full max-w-[280px] xs:max-w-[300px] mx-auto">
              <h2 class="text-xl xs:text-2xl font-bold text-[#2B5329] mb-1 xs:mb-2 text-center">Create an account</h2>
              <p class="text-xs text-gray-600 mb-3 xs:mb-4 text-center">Enter your personal data to create an account</p>

              <form @submit.prevent="handleSubmit" class="space-y-2 xs:space-y-3">
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
                  <div class="space-y-1 relative">
                    <div class="relative">
                      <input
                        id="password"
                        :type="showPassword ? 'text' : 'password'"
                        v-model="form.password"
                        required
                        @input="checkPasswordStrength"
                        @focus="showPasswordRequirements = true"
                        @blur="handlePasswordBlur"
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

                    <!-- Password strength indicator -->
                    <div class="flex gap-1 h-1 mt-1">
                      <div
                        v-for="(segment, index) in 4"
                        :key="index"
                        :class="[
                          'flex-1 rounded-full transition-all duration-300',
                          index < passwordStrength ? strengthColors[passwordStrength - 1] : 'bg-gray-200'
                        ]"
                      ></div>
                    </div>

                    <!-- Floating Password Requirements Tooltip -->
                    <transition
                      enter-active-class="transition-all duration-200 ease-out"
                      enter-from-class="opacity-0 transform scale-95"
                      enter-to-class="opacity-100 transform scale-100"
                      leave-active-class="transition-all duration-150 ease-in"
                      leave-from-class="opacity-100 transform scale-100"
                      leave-to-class="opacity-0 transform scale-95"
                    >
                      <div 
                        v-show="showPasswordRequirements && (form.password.length > 0 || passwordFieldFocused)"
                        class="absolute top-full left-0 mt-1 w-full xs:w-64 p-2 xs:p-3 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
                      >
                        <div class="text-xs font-medium text-gray-700 mb-1 xs:mb-2">Password Requirements:</div>
                        <div class="space-y-1">
                          <div class="flex items-center gap-2 text-xs">
                            <div :class="[
                              'w-1.5 h-1.5 xs:w-2 xs:h-2 rounded-full transition-colors duration-200',
                              form.password.length >= 8 ? 'bg-green-500' : 'bg-gray-300'
                            ]"></div>
                            <span :class="form.password.length >= 8 ? 'text-green-600' : 'text-gray-500'">
                              At least 8 characters
                            </span>
                          </div>
                          <div class="flex items-center gap-2 text-xs">
                            <div :class="[
                              'w-1.5 h-1.5 xs:w-2 xs:h-2 rounded-full transition-colors duration-200',
                              /[A-Z]/.test(form.password) ? 'bg-green-500' : 'bg-gray-300'
                            ]"></div>
                            <span :class="/[A-Z]/.test(form.password) ? 'text-green-600' : 'text-gray-500'">
                              One uppercase letter
                            </span>
                          </div>
                          <div class="flex items-center gap-2 text-xs">
                            <div :class="[
                              'w-1.5 h-1.5 xs:w-2 xs:h-2 rounded-full transition-colors duration-200',
                              /[0-9]/.test(form.password) ? 'bg-green-500' : 'bg-gray-300'
                            ]"></div>
                            <span :class="/[0-9]/.test(form.password) ? 'text-green-600' : 'text-gray-500'">
                              One number
                            </span>
                          </div>
                          <div class="flex items-center gap-2 text-xs">
                            <div :class="[
                              'w-1.5 h-1.5 xs:w-2 xs:h-2 rounded-full transition-colors duration-200',
                              /[^A-Za-z0-9]/.test(form.password) ? 'bg-green-500' : 'bg-gray-300'
                            ]"></div>
                            <span :class="/[^A-Za-z0-9]/.test(form.password) ? 'text-green-600' : 'text-gray-500'">
                              One special character
                            </span>
                          </div>
                        </div>
                      </div>
                    </transition>
                  </div>
                </div>

                <!-- PIN Input with 4 separate boxes -->
                <div v-else>
                  <label class="block text-xs xs:text-sm font-medium text-gray-700 mb-2 xs:mb-3">Enter 4-digit PIN</label>
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

                <button
                  type="submit" 
                  :disabled="isLoading || !isFormValid"
                  class="w-full flex justify-center py-1.5 xs:py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-[#2B5329] hover:bg-[#1F3D1F] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFA500] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed mt-4 xs:mt-6 text-sm xs:text-base"
                >
                  {{ isLoading ? "Signing Up..." : "Sign Up" }}
                </button>
              </form>

              <div class="mt-3 xs:mt-4 text-center">
                <span class="text-xs text-[#2B5329]">Already have an account? </span> 
                <button
                  @click="handleLoginTransition"
                  class="text-[#2B5329] hover:text-[#FFA500] transition-colors inline-flex items-center gap-1 cursor-pointer"
                >
                  <span class="text-xs font-bold">Login</span>
                </button>
              </div>
            </div>
          </div>
        </div>
        <LoadingPage
          :is-visible="isLoading"
          title="Creating your account..."
          message="Please wait while we set up your new account"
          @loading-complete="onLoadingComplete"
        />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'
import { ArrowLeft, Eye, EyeOff, LogIn, Key, Hash } from 'lucide-vue-next'
import { useRouter } from 'vue-router'
import LoadingPage from '../layout/LoadingPage.vue'
import { useUserStore } from '../../utils/user'
import api from '../../api/index.js' // Assuming this is your configured Axios instance
import toastr from "toastr"
import axios from 'axios'

const userStore = useUserStore()
const router = useRouter();
const transitionKey = ref(0);
const contentStyle = ref({});
const useEmail = ref(true); // Not currently used but kept for potential future use

const form = ref({
  authType: 'password',  // or 'pin'
  phoneNumber: '',
  password: '',
  pin: '',
});

// Computed property to check if password is entered
const isPasswordValid = computed(() => {
  return form.value.password.trim().length > 0
})

// Computed property to check if phone number is entered
const isPhoneValid = computed(() => {
  return form.value.phoneNumber.trim().length > 0
})

// Computed property to check if PIN is complete
const isPinComplete = computed(() => {
  if (form.value.authType !== 'pin') return true
  return pinDigits.value.every(digit => digit !== '' && digit.trim().length === 1)
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

const message = ref(""); // Not currently used
const showPassword = ref(false)
const passwordStrength = ref(0)
const isMobile = ref(false)
const isLoading = ref(false)
const pinError = ref(false)
const showPasswordRequirements = ref(false)
const passwordFieldFocused = ref(false)
// const recaptchaContainer = ref(null); // For the reCAPTCHA DOM element - removed
// let globalRecaptchaVerifier = null; // Stores the reCAPTCHA verifier instance - removed

// PIN-related reactive data
const pinDigits = ref(['', '', '', ''])
const pinInputs = ref([])

// Leaf-related reactive data
const leafCount = ref(0)
const leafPositions = ref({})

// Function to generate leaf positions
const generateLeafPositions = () => {
  const positions = {}
  for (let i = 1; i <= leafCount.value; i++) {
    positions[i] = {
      left: Math.random() * 100,
      top: Math.random() * -200,
      duration: 15 + Math.random() * 15,
      delay: Math.random() * -30
    }
  }
  return positions
}

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

function isValidPhilippinePhoneNumber(number) {
  const cleaned = number.trim();
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

const handlePasswordBlur = () => {
  passwordFieldFocused.value = false
  setTimeout(() => {
    if (!passwordFieldFocused.value) {
      showPasswordRequirements.value = false
    }
  }, 150)
}


const avatarOptions = ref([
  { id: 1, icon: '🌱', name: 'Seedling' },
  { id: 2, icon: '🌿', name: 'Herb' },
  { id: 3, icon: '🌾', name: 'Wheat' },
  { id: 4, icon: '🌽', name: 'Corn' },
  { id: 5, icon: '🥕', name: 'Carrot' },
  { id: 6, icon: '🍅', name: 'Tomato' },
  { id: 7, icon: '🥬', name: 'Lettuce' },
  { id: 8, icon: '🌻', name: 'Sunflower' },
  { id: 9, icon: '🌳', name: 'Tree' },
  { id: 10, icon: '🍃', name: 'Leaves' },
  { id: 11, icon: '🌵', name: 'Cactus' },
  { id: 12, icon: '🌸', name: 'Blossom' },
  { id: 13, icon: '🍄', name: 'Mushroom' },
  { id: 14, icon: '🌺', name: 'Hibiscus' },
  { id: 15, icon: '🌹', name: 'Rose' },
  { id: 16, icon: '🌷', name: 'Tulip' },
  { id: 17, icon: '🥦', name: 'Broccoli' },
  { id: 18, icon: '🌶️', name: 'Pepper' },
  { id: 19, icon: '🥒', name: 'Cucumber' },
  { id: 20, icon: '🍆', name: 'Eggplant' },
  { id: 21, icon: '🥔', name: 'Potato' },
  { id: 22, icon: '🧄', name: 'Garlic' },
  { id: 23, icon: '🧅', name: 'Onion' },
  { id: 24, icon: '🥜', name: 'Peanut' }
])

const handleSubmit = async () => {
  const { phoneNumber, password, pin, authType } = form.value
  const credentialValue = authType === 'password' ? password : pin
  const trimmedPhone = String(phoneNumber).trim()

  if (!isValidPhilippinePhoneNumber(trimmedPhone)) {
    window.showToast('Enter a valid PH number.', 'warning')
    return
  }

  const formattedPhone = toE164(trimmedPhone)
  if (!formattedPhone) {
    window.showToast('Invalid phone format.', 'warning')
    return
  }

  if (!credentialValue || !credentialValue.trim()) {
    window.showToast(`Please enter your ${authType}.`, 'warning')
    return
  }

  if (authType === 'pin' && !isPinComplete.value) {
    pinError.value = true
    window.showToast('Please enter all 4 digits of your PIN.', 'warning')
    return
  }

  isLoading.value = true

  try {
    // Call the new backend registration endpoint
    const response = await api.post('/auth/register', {
      phoneNumber: formattedPhone,
      credential: credentialValue,
      authType: authType
    })

    if (response.data.success) {
      window.showToast(response.data.message, 'success')
      
      // Clear any existing session before redirecting
      try {
        userStore.clearUser()
      } catch (error) {
        console.error('Error clearing user store:', error)
        localStorage.removeItem('user') // Fallback cleanup
      }

      localStorage.setItem('otpPhone', formattedPhone)
      // For testing, you might want to store the OTP in development
      if (process.env.NODE_ENV === 'development') {
        localStorage.setItem('debug_otp', response.data.otp)
        console.log('DEBUG OTP:', response.data.otp)
      }
      
      router.push(`/auth/verify-otp?phone=${encodeURIComponent(formattedPhone)}`)
    } else {
      window.showToast(response.data.message || 'Registration failed.', 'failed')
    }

  } catch (error) {
    console.error('Registration error:', error)
    window.showToast(
      error?.response?.data?.detail || 
      error?.response?.data?.message || 
      'Registration failed. Please try again.', 
      'failed'
    )
  } finally {
    isLoading.value = false
  }
}

const handleResize = () => {
  isMobile.value = window.innerWidth < 640
  leafCount.value = window.innerWidth < 640 ? 12 : 20
  leafPositions.value = generateLeafPositions()
}

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

const handleLoginTransition = () => {
  transitionKey.value++
  contentStyle.value = {
    position: 'relative',
    left: '0px',
    transition: 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)'
  }

  setTimeout(() => {
    router.push('/login')
  }, 500)
}

const strengthColors = [
  'bg-red-500',    // Weak
  'bg-yellow-500', // Fair
  'bg-blue-500',   // Good
  'bg-green-500'   // Strong
]

const checkPasswordStrength = () => {
  const password = form.value.password
  let strength = 0

  if (password.length >= 8) strength++
  if (password.match(/[A-Z]/)) strength++
  if (password.match(/[0-9]/)) strength++
  if (password.match(/[^A-Za-z0-9]/)) strength++

  passwordStrength.value = strength
}

const onLoadingComplete = () => {
  isLoading.value = false
}

onMounted(() => {
  handleResize();
  window.addEventListener('resize', handleResize);
  // reCAPTCHA setup removed
});

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  // reCAPTCHA cleanup removed
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

:root {
  font-family: 'Poppins', sans-serif;
}

h2, p, label, input, button, a, span {
  font-family: 'Poppins', sans-serif;
}

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
