<template>
  <head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 relative overflow-hidden">
    <!-- Falling Leaves Animation (kept the same as login) -->
    <div class="absolute inset-0 pointer-events-none z-10 overflow-hidden">
      <div v-for="i in (isMobile ? 12 : 20)" :key="`leaf1-${i}`" 
           class="leaf absolute animate-fall"
           :style="{
             left: `${Math.random() * 100}%`,
             top: `${Math.random() * -200}%`,
             animationDuration: `${15 + Math.random() * 15}s`,
             animationDelay: `${Math.random() * -30}s`,
             transform: `scale(${isMobile ? 0.7 : 0.95})`
           }">
        <img 
          src="/public/images/leaves-plants/fall-leaf1.png"
          alt="" 
          class="w-20 sm:w-24 h-20 sm:h-24 opacity-50"
        />
      </div>
      
      <div v-for="i in (isMobile ? 12 : 20)" :key="`leaf2-${i}`" 
           class="leaf absolute animate-fall"
           :style="{
             left: `${Math.random() * 100}%`,
             top: `${Math.random() * -200}%`,
             animationDuration: `${15 + Math.random() * 15}s`,
             animationDelay: `${Math.random() * -30}s`,
             transform: `scale(${isMobile ? 0.7 : 0.95})`
           }">
        <img 
          src="/public/images/leaves-plants/fall-leaf2.png"
          alt="" 
          class="w-24 sm:w-28 h-24 sm:h-28 opacity-50"
        />
      </div>
    </div>

    <div class="max-w-3xl w-[95%] sm:w-[90%] md:w-[85%] lg:w-full min-h-[500px] flex shadow-xl rounded-xl overflow-hidden relative z-20">
      <!-- Left Side - Image and Branding -->
      <div class="hidden md:flex md:w-1/2 bg-[#2B5329] text-white p-6 md:p-8 flex-col justify-end relative">
        <!-- Background Image -->
        <div 
          class="absolute inset-0 bg-cover bg-center"
          style="background-image: url('/public/images/greenhouse.jpg');"
        ></div>
        <!-- Dark gradient overlay -->
        <div class="absolute inset-0 bg-gradient-to-r from-[#1A3A1A] via-[#2B5329]/95 to-[#2B5329]/85"></div>
        
        <!-- Content -->
        <div class="relative flex flex-col items-center z-10 mt-0 pt-4 mb-auto">
          <div class="w-40 h-40 sm:w-48 sm:h-48 mb-2 relative overflow-visible">
            <img 
              src="/images/plants.gif"
              alt="Growing plant animation"   
              class="w-[130%] h-[130%] max-w-none object-contain mix-blend-multiply filter brightness-100 contrast-100 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2"
            />
          </div>
          <h2 class="text-2xl font-bold mb-1">Reset Password</h2>
          <p class="text-sm text-gray-200/90 mt-1 text-center font-light">Don't worry! It happens. Please enter the phone number associated with your account.</p>
        </div>

        <div class="relative flex justify-center z-10">
          <button 
            @click="handleBackToLogin" 
            class="text-white hover:text-[#FFA500] flex items-center gap-2 transition-colors duration-300 border border-white/50 rounded-lg px-4 py-2 hover:bg-white/20"
          >
            <ArrowLeft class="h-4 w-4" />
            <span class="text-sm">Back to Login</span>
          </button>
        </div>
      </div>

      <!-- Right Side - Reset Password Form -->
      <div class="w-full md:w-1/2 bg-white p-6 flex flex-col">
        <div class="w-[90%] max-w-xs mx-auto flex-1 flex flex-col justify-center">
          <h2 class="text-xl font-bold text-[#2B5329] text-center mb-2">
            {{ currentStep === 1 ? 'Forgot Password' : 
               currentStep === 2 ? 'Verify Code' : 'Create New Password' }}
          </h2>
          <p v-if="currentStep === 1" class="text-sm text-gray-600 text-center mb-6">
            Enter your phone number and we'll send you a verification code to reset your password
          </p>

          <!-- Step 1: Phone Number Input -->
          <form v-if="currentStep === 1" @submit.prevent="handleSendResetCode" class="space-y-4">
            <div>
              <label for="phoneNumber" class="block text-sm font-medium text-gray-700">Phone Number</label>
              <input 
                id="phoneNumber"
                type="tel"
                maxlength="13"
                inputmode="numeric"
                v-model="phoneNumber"
                required 
                class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]"
                placeholder="e.g., 09123456789"
              />
            </div>

            <button 
              type="submit" :disabled="isLoading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-[#2B5329] hover:bg-[#1F3D1F] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFA500] transition-colors duration-200"
            >
             {{ isLoading ? "Sending Verification Code..." : "Send Verification Code" }}
            </button>
          </form>

          <!-- Step 2: Verification Code -->
          <form v-if="currentStep === 2" @submit.prevent="handleVerifyCode" class="space-y-6">
            <div class="text-center">
              <h3 class="text-sm font-semibold text-[#2B5329] mb-2">Enter the 6-digit code</h3>
              <p class="text-sm text-gray-600">We sent to your phone number</p>
            </div>

            <div class="flex justify-center gap-2">
              <template v-for="i in 6" :key="i">
                <input
                  type="text"
                  :ref="el => codeRefs[i-1] = el"
                  v-model="verificationDigits[i-1]"
                  maxlength="1"
                  class="w-12 h-12 text-center text-lg border-2 border-gray-300 rounded-lg focus:border-[#2B5329] focus:ring-2 focus:ring-[#2B5329] focus:outline-none transition-colors"
                  @input="handleCodeInput($event, i-1)"
                  @keydown.delete="handleBackspace($event, i-1)"
                  @keydown.left="focusPrevious(i-1)"
                  @keydown.right="focusNext(i-1)"
                  @paste="handlePaste"
                />
              </template>
            </div>

            <button 
              type="submit" :disabled="isLoading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-[#2B5329] hover:bg-[#1F3D1F] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFA500] transition-colors duration-200"
            >
              {{ isLoading ? "Verifying Code..." : "Verify Code" }}
            </button>

            <div class="text-center mt-4">
              <p class="text-sm text-gray-600">
                Didn't receive the code? 
                <button 
                  type="button"
                  @click="handleResendCode" 
                  class="text-[#2B5329] hover:text-[#FFA500] font-medium transition-colors ml-1"
                  :disabled="resendTimer > 0"
                >
                  {{ resendTimer > 0 ? `Resend in ${resendTimer}s` : 'Resend Code' }}
                </button>
              </p>
            </div>
          </form>

          <!-- Step 3: New Password / PIN -->
          <form v-if="currentStep === 3" @submit.prevent="handleResetPassword" class="space-y-4">
            <div class="text-center mb-4">
              <p class="text-sm text-gray-600">Choose how you'd like to secure your account.</p>
            </div>

            <!-- Auth Type Choice -->
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Choose New Login Type</label>
              <div class="flex gap-2">
                <button
                  type="button"
                  @click="resetAuthType = 'password'"
                  :class="[
                    'px-4 py-1.5 rounded-md text-sm font-medium transition w-full',
                    resetAuthType === 'password'
                      ? 'bg-[#2B5329] text-white shadow'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  New Password
                </button>
                <button
                  type="button"
                  @click="resetAuthType = 'pin'"
                  :class="[
                    'px-4 py-1.5 rounded-md text-sm font-medium transition w-full',
                    resetAuthType === 'pin'
                      ? 'bg-[#2B5329] text-white shadow'
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  ]"
                >
                  New 4-digit PIN
                </button>
              </div>
            </div>

            <!-- Password Inputs -->
            <div v-if="resetAuthType === 'password'" class="space-y-4">
              <div>
                <label for="newPassword" class="block text-sm font-medium text-gray-700">New Password</label>
                <div class="relative">
                  <input 
                    :type="showPassword ? 'text' : 'password'"
                    id="newPassword" 
                    v-model="newPassword"
                    required 
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]"
                  />
                  <button type="button" @click="showPassword = !showPassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                    <Eye v-if="!showPassword" class="h-4 w-4" /><EyeOff v-else class="h-4 w-4" />
                  </button>
                </div>
              </div>
              <div>
                <label for="confirmPassword" class="block text-sm font-medium text-gray-700">Confirm Password</label>
                <div class="relative">
                  <input 
                    :type="showConfirmPassword ? 'text' : 'password'"
                    id="confirmPassword" 
                    v-model="confirmPassword"
                    required 
                    class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]"
                  />
                  <button type="button" @click="showConfirmPassword = !showConfirmPassword" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500">
                    <Eye v-if="!showConfirmPassword" class="h-4 w-4" /><EyeOff v-else class="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>

            <!-- PIN Inputs -->
            <div v-else class="space-y-4">
              <div>
                <label for="newPin" class="block text-sm font-medium text-gray-700">New 4-digit PIN</label>
                <input id="newPin" type="password" v-model="newPin" required maxlength="4" pattern="\d*" inputmode="numeric" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]" />
              </div>
              <div>
                <label for="confirmNewPin" class="block text-sm font-medium text-gray-700">Confirm PIN</label>
                <input id="confirmNewPin" type="password" v-model="confirmNewPin" required maxlength="4" pattern="\d*" inputmode="numeric" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329]" />
              </div>
            </div>

            <button 
              type="submit" :disabled="isLoading"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-[#2B5329] hover:bg-[#1F3D1F] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFA500] transition-colors duration-200"
            >
              {{ isLoading ? "Resetting..." : "Reset Credentials" }}
            </button>
          </form>
        </div>
        <LoadingPage 
          :is-visible="isLoading"
          :title="loadingTitle"
          message="Please wait while we process your request..."
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft, Eye, EyeOff } from 'lucide-vue-next'
import api from '../../api/index.js'
import toastr from 'toastr'
import LoadingPage from '../layout/LoadingPage.vue'
import { getFirestore, collection, query, where, getDocs, doc, updateDoc, serverTimestamp } from "firebase/firestore";

const router = useRouter()
const currentStep = ref(1)
const phoneNumber = ref('')
const verificationCode = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const isMobile = ref(window.innerWidth < 640)
const verificationDigits = ref(['', '', '', '', '', ''])
const codeRefs = ref([])
const resendTimer = ref(0)
const isLoading = ref(false);
let resendInterval = null

const resetAuthType = ref('password') // 'password' or 'pin'
const newPin = ref('')
const confirmNewPin = ref('')

const db = getFirestore();

const loadingTitle = computed(() => {
  if (currentStep.value === 1) return "Sending Verification Code...";
  if (currentStep.value === 2) return "Verifying Code...";
  if (currentStep.value === 3) return "Resetting Credentials...";
  return "Loading...";
});

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

const handleResize = () => {
  isMobile.value = window.innerWidth < 640
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (resendInterval) {
    clearInterval(resendInterval)
  }
})

const handleCodeInput = (event, index) => {
  const value = event.target.value
  // Only allow numbers
  if (!/^\d*$/.test(value)) {
    verificationDigits.value[index] = ''
    return
  }
  
  // Auto-advance to next input
  if (value && index < 5) {
    codeRefs.value[index + 1]?.focus()
  }
}

const handleBackspace = (event, index) => {
  if (!verificationDigits.value[index] && index > 0) {
    codeRefs.value[index - 1]?.focus()
  }
}

const focusPrevious = (index) => {
  if (index > 0) {
    codeRefs.value[index - 1]?.focus()
  }
}

const focusNext = (index) => {
  if (index < 5) {
    codeRefs.value[index + 1]?.focus()
  }
}

const handlePaste = (event) => {
  event.preventDefault()
  const pastedData = event.clipboardData.getData('text')
  const numbers = pastedData.match(/\d/g)
  if (numbers) {
    numbers.slice(0, 6).forEach((num, i) => {
      verificationDigits.value[i] = num
    })
  }
}

const startResendTimer = () => {
  resendTimer.value = 30
  resendInterval = setInterval(() => {
    if (resendTimer.value > 0) {
      resendTimer.value--
    } else {
      clearInterval(resendInterval)
    }
  }, 1000)
}

// Step 1: Request password reset
const handleSendResetCode = async () => {
  const trimmedPhone = phoneNumber.value.trim()
  if (!isValidPhilippinePhoneNumber(trimmedPhone)) {
    toastr.error('Please enter a valid Philippine phone number.')
    return
  }

  const formattedPhone = toE164(trimmedPhone)
  if (!formattedPhone) {
    toastr.error('Could not format phone number.')
    return
  }

  isLoading.value = true;

  try {
    // 1. Check if phone number exists in Firebase users collection
    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('phoneNumber', '==', formattedPhone));
    const snapshot = await getDocs(q);

    if (snapshot.empty) {
      toastr.error('This phone number is not registered yet.');
      isLoading.value = false;
      return; // Stop execution if not registered
    }

    // 2. Generate OTP
    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    const userDoc = snapshot.docs[0];

    // 3. Update user document with OTP
    await updateDoc(doc(db, 'users', userDoc.id), {
      otp,
      otpSentAt: serverTimestamp()
    });

    // 4. Call backend to send OTP
    await api.post('/otp/send', {
      number: formattedPhone,
      message: `Your password reset code is: ${otp}`
    });

    toastr.success('A password reset code has been sent to your phone.');
    currentStep.value = 2; // 5. Move to verification step
    startResendTimer(); // Start the cooldown timer

  } catch (error) {
    console.error("Error sending reset code:", error.response?.data || error);
    toastr.error(error.response?.data?.detail || "Error sending reset code.");
  } finally {
    isLoading.value = false;
  }
};

const handleResendCode = async () => {
  if (resendTimer.value > 0) return;
  isLoading.value = true;
  try {
    const trimmedPhone = phoneNumber.value.trim();
    if (!isValidPhilippinePhoneNumber(trimmedPhone)) {
      toastr.error('Invalid phone number.');
      isLoading.value = false;
      return;
    }
    const formattedPhone = toE164(trimmedPhone);

    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('phoneNumber', '==', formattedPhone));
    const snapshot = await getDocs(q);

    if (snapshot.empty) {
      toastr.error('This phone number is not registered.');
      isLoading.value = false;
      return;
    }

    const otp = Math.floor(100000 + Math.random() * 900000).toString();
    const userDoc = snapshot.docs[0];

    await updateDoc(doc(db, 'users', userDoc.id), {
      otp,
      otpSentAt: serverTimestamp()
    });

    await api.post('/otp/send', {
      number: formattedPhone,
      message: `Your new password reset code is: ${otp}`
    });

    toastr.success("A new code has been sent to your phone.");
    startResendTimer();

  } catch (error) {
    console.error("Error resending code:", error.response?.data || error);
    toastr.error(error.response?.data?.detail || "Error resending code.");
  } finally {
    isLoading.value = false;
  }
};

// ✅ Step 2: Verify the 6-digit code
const handleVerifyCode = async () => {
  const code = verificationDigits.value.join('').trim();

  if (code.length !== 6) {
    toastr.warning('Please enter the 6-digit code.');
    return;
  }

  isLoading.value = true;

  try {
    const formattedPhone = toE164(phoneNumber.value);
    const q = query(collection(db, 'users'), where('phoneNumber', '==', formattedPhone));
    const querySnapshot = await getDocs(q);

    if (querySnapshot.empty) {
      toastr.error('User not found. Please start over.');
      currentStep.value = 1;
      return;
    }

    const userDoc = querySnapshot.docs[0];
    const userData = userDoc.data();

    if (userData.otp !== code) {
      toastr.error('Invalid verification code.');
      return;
    }

    await updateDoc(doc(db, 'users', userDoc.id), {
      otp: '', // Clear OTP after successful verification
    });

    toastr.success('Code verified successfully!');
    currentStep.value = 3; // Move to password reset step

  } catch (error) {
    console.error('Error verifying code:', error);
    toastr.error('An error occurred during verification.');
  } finally {
    isLoading.value = false;
  }
};


const handleResetPassword = async () => {
  isLoading.value = true;

  const formattedPhone = toE164(phoneNumber.value);
  if (!formattedPhone) {
    toastr.error('Invalid phone number format.');
    isLoading.value = false;
    return;
  }

  const updateData = {
    authType: resetAuthType.value,
    updatedAt: serverTimestamp()
  };

  if (resetAuthType.value === 'password') {
    if (newPassword.value !== confirmPassword.value) {
      toastr.warning('Passwords do not match!');
      isLoading.value = false;
      return;
    }
    if (newPassword.value.length < 6) {
      toastr.warning('Password must be at least 6 characters long.');
      isLoading.value = false;
      return;
    }
    updateData.password = newPassword.value;
    updateData.pin = ''; // Clear PIN when setting a password
  } else { // authType is 'pin'
    if (newPin.value !== confirmNewPin.value) {
      toastr.warning('PINs do not match!');
      isLoading.value = false;
      return;
    }
    if (!/^\d{4}$/.test(newPin.value)) {
        toastr.warning('PIN must be 4 digits.');
        isLoading.value = false;
        return;
    }
    updateData.pin = newPin.value;
    updateData.password = ''; // Clear password when setting a PIN
  }

  try {
    const usersRef = collection(db, 'users');
    const q = query(usersRef, where('phoneNumber', '==', formattedPhone));
    const snapshot = await getDocs(q);

    if (snapshot.empty) {
      toastr.error('Could not find an account with that phone number.');
      isLoading.value = false;
      return;
    }

    const userDocRef = snapshot.docs[0].ref;
    await updateDoc(userDocRef, updateData);

    toastr.success('Your credentials have been reset successfully.');
    router.push('/login');
  } catch (error) {
    console.error("Error resetting password:", error);
    toastr.error("An error occurred while resetting your credentials.");
  } finally {
    isLoading.value = false;
  }
};

const handleBackToLogin = () => {
  router.push('/login')
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
}

.leaf {
  pointer-events: none;
  z-index: 10;
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

/* Replace the existing input type="text" styles */
input[type="text"] {
  -webkit-appearance: none;
  appearance: none;
  margin: 0;
  caret-color: #2B5329;
  text-align: center;
  font-size: 1.25rem;
}

input[type="text"]::-webkit-outer-spin-button,
input[type="text"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="text"]:focus {
  outline: none;
  border-color: #2B5329;
}
</style>
