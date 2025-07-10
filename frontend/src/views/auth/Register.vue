<template>
  <head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-4 py-6 sm:px-6 lg:px-8 relative overflow-hidden">
    <!-- Falling Leaves Animation - Moved outside transition -->
    <div class="absolute inset-0 pointer-events-none z-0 overflow-hidden">
      <div v-for="i in leafCount" :key="`leaf1-${i}`"
           class="leaf absolute animate-fall"
           :style="{
             left: `${leafPositions[i].left}%`,
             top: `${leafPositions[i].top}%`,
             animationDuration: `${leafPositions[i].duration}s`,
             animationDelay: `${leafPositions[i].delay}s`,
             transform: `scale(${isMobile ? 0.7 : 0.95})`
           }">
        <img
          src="/public/images/leaves-plants/fall-leaf1.png"
          alt=""
          class="w-20 sm:w-24 h-20 sm:h-24 opacity-50"
        />
      </div>

      <div v-for="i in leafCount" :key="`leaf2-${i}`"
           class="leaf absolute animate-fall"
           :style="{
             left: `${leafPositions[i].left}%`,
             top: `${leafPositions[i].top}%`,
             animationDuration: `${leafPositions[i].duration}s`,
             animationDelay: `${leafPositions[i].delay}s`,
             transform: `scale(${isMobile ? 0.7 : 0.95})`
           }">
        <img
          src="/public/images/leaves-plants/fall-leaf2.png"
          alt=""
          class="w-24 sm:w-28 h-24 sm:h-28 opacity-50"
        />
      </div>
    </div>

    <transition name="page-transition" mode="out-in" @before-leave="beforeLeave" @enter="enter" @after-enter="afterEnter">
      <div :key="transitionKey" class="page-content relative z-10" :style="contentStyle">
        <div class="max-w-3xl w-[95%] sm:w-[90%] md:w-[85%] lg:w-full min-h-[500px] flex shadow-xl rounded-xl overflow-hidden relative z-20">
          <!-- Left Side - Image and Branding -->
          <div class="hidden md:flex md:w-1/2 bg-[#2B5329] text-white p-6 md:p-8 flex-col justify-between relative">
            <!-- Background Image -->
            <div
              class="absolute inset-0 bg-cover bg-center"
              style="background-image: url('/public/images/greenhouse.jpg');"
            ></div>
            <div class="absolute inset-0 bg-gradient-to-r from-[#1A3A1A] via-[#2B5329]/95 to-[#2B5329]/85"></div>

            <div class="relative flex flex-col items-center z-10 mt-0 pt-4 mb-auto">
              <div class="w-40 h-40 sm:w-48 sm:h-48 mb-2 relative overflow-visible">
                <img
                  src="/images/plants.gif"
                  alt="Growing plant animation"
                  class="w-[130%] h-[130%] max-w-none object-contain mix-blend-multiply filter brightness-100 contrast-100 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
                />
              </div>
              <h2 class="text-2xl font-bold mb-1">Harvesting Knowledge</h2>
              <p class="text-sm text-gray-200/90 mt-1 text-center font-light">Your trusted partner in crop recommendations and agricultural wisdom.</p>
            </div>

            <!-- Back to Website - Centered -->
            <div class="relative flex justify-center z-10">
              <button
                @click="handleBackToWebsite"
                class="text-white hover:text-[#FFA500] flex items-center gap-2 transition-colors duration-300 border border-white/50 rounded-lg px-4 py-2 hover:bg-white/20"
              >
                <ArrowLeft class="h-4 w-4" />
                <span class="text-sm">Back to website</span>
              </button>
            </div>
          </div>

          <!-- Right Side - Registration Form -->
          <div class="w-full md:w-1/2 bg-white p-5 flex justify-center items-center">
            <div class="max-w-[300px] w-full mx-auto">
              <h2 class="text-2xl font-bold text-[#2B5329] mb-2 text-center">Create an account</h2>
              <p class="text-xs text-gray-600 mb-4 text-center">Enter your personal data to create an account</p>

              <form @submit.prevent="handleSubmit" class="space-y-3">
                <!-- <div class="flex space-x-4">
                  <button
                    type="button"
                    @click="useEmail = true"
                    :class="['px-4 py-2 border rounded-md', useEmail ? 'bg-[#2B5329] text-white' : 'bg-gray-200']"
                  >
                    Register with Email
                  </button>
                  <button
                    type="button"
                    @click="useEmail = false"
                    :class="['px-4 py-2 border rounded-md', !useEmail ? 'bg-[#2B5329] text-white' : 'bg-gray-200']"
                  >
                    Register with Phone
                  </button>
                </div> -->
                <!-- <div class="grid grid-cols-2 gap-3">
                  <div>
                    <label for="firstName" class="block text-sm font-medium text-gray-700 mb-1">First name</label>
                    <input
                      id="firstName"
                      type="text"
                      v-model="form.firstName"
                      required
                      class="block w-full px-3 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]"
                    />
                  </div>
                  <div>
                    <label for="lastName" class="block text-sm font-medium text-gray-700 mb-1">Last name</label>
                    <input
                      id="lastName"
                      type="text"
                      v-model="form.lastName"
                      required
                      class="block w-full px-3 py-1 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]"
                    />
                  </div>
                </div> -->

                <div>
                  <label for="phoneNumber" class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    id="phoneNumber"
                    type="tel"
                    maxlength="13"
                    inputmode="numeric"
                    v-model="form.phoneNumber"
                    required
                    class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329] transition-all duration-200"
                    placeholder="Enter your phone number"
                  />
                </div>

                <!-- Email Input -->
                <!-- <div v-if="useEmail">
                  <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email</label>
                  <input
                    id="email"
                    type="email"
                    v-model="form.email"
                    required
                    class="block w-full px-3 py-1 border rounded-md"
                  />
                </div> -->

                <!-- Phone Number Input -->
                <!-- <div v-else>
                  <label for="phone" class="block text-sm font-medium text-gray-700 mb-1">Phone Number</label>
                  <input
                    id="phone"
                    type="tel"
                    v-model="form.phone"
                    required
                    class="block w-full px-3 py-1 border rounded-md"
                  />
                </div> -->

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Choose Login Type</label>
                  <!-- Enhanced Radio Button Style Design with Green Color -->
                  <div class="flex bg-gray-50 rounded-lg p-1 border border-gray-200">
                    <label class="flex-1 cursor-pointer">
                      <input
                        type="radio"
                        name="authType"
                        value="password"
                        v-model="form.authType"
                        class="sr-only"
                      />
                      <div :class="[
                        'flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium transition-all duration-200',
                        form.authType === 'password'
                          ? 'bg-[#2B5329] text-white shadow-md'
                          : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                      ]">
                        <Key class="h-4 w-4 mr-1.5" />
                        Password
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
                        'flex items-center justify-center px-3 py-2 rounded-md text-sm font-medium transition-all duration-200',
                        form.authType === 'pin'
                          ? 'bg-[#2B5329] text-white shadow-md'
                          : 'text-gray-600 hover:text-gray-800 hover:bg-gray-100'
                      ]">
                        <Hash class="h-4 w-4 mr-1.5" />
                        4-digit PIN
                      </div>
                    </label>
                  </div>
                </div>

                <!-- Password Input -->
                <div v-if="form.authType === 'password'">
                  <label for="password" class="block text-sm font-medium text-gray-700 mb-1">Password</label>
                  <div class="space-y-1.5 relative">
                    <div class="relative">
                      <input
                        id="password"
                        :type="showPassword ? 'text' : 'password'"
                        v-model="form.password"
                        required
                        @input="checkPasswordStrength"
                        @focus="showPasswordRequirements = true"
                        @blur="handlePasswordBlur"
                        class="block w-full px-3 py-2 pr-10 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329] transition-all duration-200"
                        placeholder="Enter your password"
                      />
                      <button
                        type="button"
                        @click="showPassword = !showPassword"
                        class="absolute right-3 top-2 bottom-2 flex items-center justify-center text-gray-500 hover:text-gray-700 w-6 h-6"
                      >
                        <Eye v-if="!showPassword" class="h-4 w-4" />
                        <EyeOff v-else class="h-4 w-4" />
                      </button>
                    </div>

                    <!-- Password strength indicator -->
                    <div class="flex gap-1.5 h-1">
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
                        class="absolute top-full left-0 mt-2 w-64 p-3 bg-white rounded-lg shadow-lg border border-gray-200 z-50"
                      >
                        <div class="text-xs font-medium text-gray-700 mb-2">Password Requirements:</div>
                        <div class="space-y-1">
                          <div class="flex items-center gap-2 text-xs">
                            <div :class="[
                              'w-2 h-2 rounded-full transition-colors duration-200',
                              form.password.length >= 8 ? 'bg-green-500' : 'bg-gray-300'
                            ]"></div>
                            <span :class="form.password.length >= 8 ? 'text-green-600' : 'text-gray-500'">
                              At least 8 characters
                            </span>
                          </div>
                          <div class="flex items-center gap-2 text-xs">
                            <div :class="[
                              'w-2 h-2 rounded-full transition-colors duration-200',
                              /[A-Z]/.test(form.password) ? 'bg-green-500' : 'bg-gray-300'
                            ]"></div>
                            <span :class="/[A-Z]/.test(form.password) ? 'text-green-600' : 'text-gray-500'">
                              One uppercase letter
                            </span>
                          </div>
                          <div class="flex items-center gap-2 text-xs">
                            <div :class="[
                              'w-2 h-2 rounded-full transition-colors duration-200',
                              /[0-9]/.test(form.password) ? 'bg-green-500' : 'bg-gray-300'
                            ]"></div>
                            <span :class="/[0-9]/.test(form.password) ? 'text-green-600' : 'text-gray-500'">
                              One number
                            </span>
                          </div>
                          <div class="flex items-center gap-2 text-xs">
                            <div :class="[
                              'w-2 h-2 rounded-full transition-colors duration-200',
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
                  <label class="block text-sm font-medium text-gray-700 mb-3">Enter 4-digit PIN</label>
                  <div class="flex gap-2 justify-center">
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
                      class="w-10 h-10 text-center text-lg font-semibold border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329] transition-all duration-200"
                      :class="{
                        'border-[#2B5329] bg-green-50': pinDigits[index],
                        'border-red-300 animate-pulse': pinError && !pinDigits[index]
                      }"
                    />
                  </div>
                  <p v-if="pinError" class="text-red-500 text-xs mt-1 text-center">Please enter all 4 digits</p>
                </div>


                <!-- <div class="flex items-center">
                  <input
                    type="checkbox"
                    id="terms"
                    v-model="form.acceptTerms"
                    required
                    class="h-4 w-4 rounded border-gray-300 text-[#2B5329] focus:ring-[#2B5329]"
                  />
                  <label for="terms" class="ml-2 text-xs text-gray-600">
                    I agree to the
                    <a href="#" class="text-[#2B5329] hover:text-[#FFA500] transition-colors">Terms & Conditions</a>
                  </label>
                </div> -->

                 <!-- <div id="recaptcha-container"></div> reCAPTCHA container removed -->

                <button
                  type="submit" 
                  :disabled="isLoading || !isFormValid"
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-[#2B5329] hover:bg-[#1F3D1F] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFA500] transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed mt-6"
                >
                  {{ isLoading ? "Signing Up..." : "Sign Up" }}
                </button>
              </form>

              <div class="mt-4">
                <!-- <div class="relative">
                  <div class="absolute inset-0 flex items-center">
                    <div class="w-full border-t border-gray-300"></div>
                  </div>
                  <div class="relative flex justify-center text-sm">
                    <span class="px-2 bg-white text-gray-500 text-xs">Or register with</span>
                  </div>
                </div> -->

                <div class="mt-4 grid grid-cols-1 gap-3">
                  <!-- <button
                    type="button" @click="handleGoogleRegister"
                    class="flex items-center justify-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-[#3a8a3a] hover:text-white hover:border-[#3a8a3a] hover:transform hover:-translate-y-1 transition-all duration-300"
                  >
                    <Chrome class="h-4 w-4 mr-1.5" />
                    Google
                  </button> -->
                  <!-- <button
                    type="button"
                    class="flex items-center justify-center px-3 py-1.5 border border-gray-300 rounded-md shadow-sm bg-white text-sm font-medium text-gray-700 hover:bg-[#3a8a3a] hover:text-white hover:border-[#3a8a3a] hover:transform hover:-translate-y-1 transition-all duration-300"
                  >
                    <Facebook class="h-4 w-4 mr-1.5" />
                    Facebook
                  </button> -->
                </div>

                <div class="mt-4 text-center">
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
import api from '../../api/index.js' // Assuming this is your configured Axios instance
import toastr from "toastr"
import axios from 'axios'
import {
  getFirestore,
  collection,
  addDoc,
  query,
  where,
  getDocs,
  serverTimestamp,
  doc, // Added import
  updateDoc // Added import
} from "firebase/firestore"

const db = getFirestore();
// const auth = getAuth(); // Firebase auth instance removed (was for reCAPTCHA)
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
  // Hide tooltip after a short delay to allow for interaction
  setTimeout(() => {
    if (!passwordFieldFocused.value) {
      showPasswordRequirements.value = false
    }
  }, 150)
}

// function setupRecaptcha() - removed

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
    toastr.error('Enter a valid PH number.')
    return
  }

  const formattedPhone = toE164(trimmedPhone)
  if (!formattedPhone) {
    toastr.error('Invalid phone format.')
    return
  }

  if (!credentialValue || !credentialValue.trim()) {
    toastr.error(`Please enter your ${authType}.`)
    return
  }

  if (authType === 'pin' && !isPinComplete.value) {
    pinError.value = true
    toastr.warning('Please enter all 4 digits of your PIN.')
    return
  }

  isLoading.value = true

  try {
    const usersRef = collection(db, 'users')
    const q = query(usersRef, where('phoneNumber', '==', formattedPhone))
    const snapshot = await getDocs(q)

    let userDocId = null
    const userExists = !snapshot.empty
    let isVerified = false

    // Generate random OTP
    const otp = Math.floor(100000 + Math.random() * 900000).toString()

    // Pick random avatar
    const randomAvatar = avatarOptions.value[Math.floor(Math.random() * avatarOptions.value.length)]

    if (userExists) {
      const existingUser = snapshot.docs[0]
      userDocId = existingUser.id
      const data = existingUser.data()
      isVerified = data.verified

      if (isVerified) {
        toastr.info('Phone number already verified.')
        isLoading.value = false
        return
      }

      await updateDoc(doc(db, 'users', userDocId), {
        authType,
        password: authType === 'password' ? credentialValue : '',
        pin: authType === 'pin' ? credentialValue : '',
        otp,
        otpSentAt: serverTimestamp(),
        avatar: randomAvatar,
        updatedAt: serverTimestamp()
      })

      toastr.info('User found. Sending OTP again...')
    } else {
      const newUserRef = await addDoc(usersRef, {
        phoneNumber: formattedPhone,
        authType,
        password: authType === 'password' ? credentialValue : '',
        pin: authType === 'pin' ? credentialValue : '',
        otp,
        otpSentAt: serverTimestamp(),
        verified: false,
        avatar: randomAvatar,
        createdAt: serverTimestamp()
      })
      userDocId = newUserRef.id
      toastr.success('User registered. Sending OTP...')
    }

    // 🔁 Call FastAPI backend to send OTP via Vonage
    await api.post('/otp/send', {
      number: formattedPhone,
      message: `Your OTP code is: ${otp}`
    })

    localStorage.setItem('otpPhone', formattedPhone)
    toastr.success('OTP sent successfully.')
    router.push(`/auth/verify-otp?phone=${encodeURIComponent(formattedPhone)}`)

  } catch (error) {
    console.error('❌ Error:', error)
    toastr.error(error?.response?.data?.detail || 'An error occurred. Please try again.')
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

// const handleGoogleRegister = async () => { // Kept for reference if needed later
//   try {
//     const result = await signInWithPopup(auth, googleProvider); // Note: 'auth' would be undefined here now
//     const user = result.user;
//     console.log("✅ Google User:", user);
//     const idToken = await user.getIdToken();
//     const response = await api.post("/auth/google-register", { idToken });
//     console.log("✅ Backend Response:", response.data);
//     const { user: userData } = response.data;
//     if (!userData.profilePicture) {
//       userData.profilePicture = generateProfilePicture(userData.email);
//     }
//     localStorage.setItem("user", JSON.stringify(userData));
//     // user.value = userData; // If using Vue's ref() for user state
//     toastr.success("Registration successful!");
//     router.push("/dashboard");
//   } catch (error) {
//     console.error("❌ Google Registration Error:", error);
//     toastr.error(error.response?.data?.detail || "Google registration failed.");
//   }
// };

// const generateProfilePicture = (email) => { // Kept for reference
//   const initials = email[0].toUpperCase();
//   return `https://dummyimage.com/100x100/000/fff.png&text=${initials}`;
// };

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
