<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 px-3 xs:px-4 sm:px-6 relative overflow-hidden">
    <transition name="page-transition" mode="out-in" @before-leave="beforeLeave" @enter="enter" @after-enter="afterEnter">
      <div :key="transitionKey" class="page-content" :style="contentStyle">
        <!-- Falling Leaves Animation -->
        <div class="absolute inset-0 pointer-events-none z-10 overflow-hidden">
          <div v-for="i in (isMobile ? 12 : 20)" :key="`leaf1-${i}`" 
               class="leaf absolute animate-fall"
               :style="{
                 left: `${Math.random() * 100}%`,
                 top: `${Math.random() * -200}%`,
                 animationDuration: `${15 + Math.random() * 15}s`,
                 animationDelay: `${Math.random() * -30}s`,
                 transform: `scale(${isMobile ? 0.6 : 0.9})`
               }">
            <img 
              src="/public/images/leaves-plants/fall-leaf1.png"
              alt="" 
              class="w-16 xs:w-20 sm:w-24 h-16 xs:h-20 sm:h-24 opacity-50"
            />
          </div>
          
          <div v-for="i in (isMobile ? 12 : 20)" :key="`leaf2-${i}`" 
               class="leaf absolute animate-fall"
               :style="{
                 left: `${Math.random() * 100}%`,
                 top: `${Math.random() * -200}%`,
                 animationDuration: `${15 + Math.random() * 15}s`,
                 animationDelay: `${Math.random() * -30}s`,
                 transform: `scale(${isMobile ? 0.6 : 0.9})`
               }">
            <img 
              src="/public/images/leaves-plants/fall-leaf2.png"
              alt="" 
              class="w-20 xs:w-24 sm:w-28 h-20 xs:h-24 sm:h-28 opacity-50"
            />
          </div>
        </div>

        <div class="max-w-3xl w-[95%] xs:w-[90%] sm:w-[85%] md:w-full min-h-[400px] xs:min-h-[450px] sm:min-h-[500px] flex shadow-xl rounded-xl overflow-hidden relative z-20">
          <!-- Left Side - Image and Branding -->
          <div class="hidden md:flex md:w-1/2 bg-[#2B5329] text-white p-4 sm:p-6 md:p-8 flex-col justify-between relative">
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
              <h2 class="text-xl xs:text-2xl font-bold mb-1">Verify Your Account</h2>
              <p class="text-xs xs:text-sm text-gray-200/90 mt-1 text-center font-light">Almost there! Enter your code to unlock access and discover the best solutions for your crops.</p>
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

          <!-- Right Side - Verification Form -->
          <div class="w-full md:w-1/2 bg-white p-4 xs:p-5 sm:p-6 flex flex-col">
            <div class="w-full max-w-xs mx-auto flex-1 flex flex-col justify-center">
              <h2 class="text-lg xs:text-xl font-bold text-[#2B5329] text-center mb-4 xs:mb-6">Verify Your Phone Number</h2>

              <form class="space-y-3 xs:space-y-4" @submit.prevent="handleVerification">
                <div>
                  <label class="block text-xs xs:text-sm font-medium text-gray-700 text-center mb-3 xs:mb-4">
                    Enter the 6-digit code we sent to your phone number
                  </label>
                  <div class="flex justify-center gap-1.5 xs:gap-2">
                    <input 
                      v-for="(digit, index) in 6"
                      :key="index"
                      type="text"
                      v-model="verificationCode[index]"
                      maxlength="1"
                      @input="handleCodeInput($event, index)"
                      @keydown.delete="handleBackspace($event, index)"
                      @keydown.left="focusPrevious(index)"
                      @keydown.right="focusNext(index)"
                      class="w-8 xs:w-10 h-8 xs:h-10 text-center border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329] text-sm xs:text-base font-semibold"
                      ref="codeInputs"
                    />
                  </div>
                </div>

                <button 
                  type="submit" 
                  class="w-full flex justify-center py-1.5 xs:py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-[#2B5329] hover:bg-[#1F3D1F] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFA500] transition-colors duration-200 mt-4 xs:mt-6 text-sm xs:text-base"
                >
                  {{ isLoading ? "Verifying..." : "Verify" }}
                </button>

                <div class="text-center mt-4 xs:mt-6">
                  <p class="text-xs xs:text-sm text-gray-600">
                    Didn't receive the code?
                    <button 
                      type="button"
                      @click="resendCode" 
                      class="text-[#2B5329] hover:text-[#FFA500] font-medium transition-colors ml-1 disabled:opacity-50 disabled:cursor-not-allowed"
                      :disabled="resendTimer > 0 || isResendingCode"
                    >
                      {{ isResendingCode ? 'Sending...' : (resendTimer > 0 ? `Resend in ${resendTimer}s` : 'Resend Code') }}
                    </button>
                  </p>
                </div>
              </form>
            </div>
          </div>
        </div>
        <LoadingPage 
          :is-visible="isLoading"
          title="Verifying your account..."
          message="Please wait while we set up your new account"
          @loading-complete="onLoadingComplete"
        />
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ArrowLeft } from 'lucide-vue-next'
import api from '../../api/index.js'
import { useUserStore } from '../../utils/user'
import LoadingPage from '../layout/LoadingPage.vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const verificationCode = ref(['', '', '', '', '', ''])
const codeInputs = ref([])
const isMobile = ref(window.innerWidth < 640)
const transitionKey = ref(0)
const contentStyle = ref({})
const resendTimer = ref(0)
const uid = ref(null);
const isLoading = ref(false);
const phone = route.query.phone;
const isResendingCode = ref(false);


const handleResize = () => {
  isMobile.value = window.innerWidth < 640
}

onMounted(() => {
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

const handleCodeInput = (event, index) => {
  const input = event.target
  input.value = input.value.replace(/[^0-9]/g, '')
  verificationCode.value[index] = input.value

  if (input.value && index < 5) {
    codeInputs.value[index + 1].focus()
  }
}

const handleBackspace = (event, index) => {
  if (!verificationCode.value[index] && index > 0) {
    codeInputs.value[index - 1].focus()
  }
}

const focusPrevious = (index) => {
  if (index > 0) {
    codeInputs.value[index - 1].focus()
  }
}

const focusNext = (index) => {
  if (index < 5) {
    codeInputs.value[index + 1].focus()
  }
}

onMounted(() => {
  const phone = route.query.phone;

  if (!phone) {
    console.error("❌ Phone number is missing from the route");
  } else {
    console.log("✅ Phone number from route:", phone);
    // You can now fetch the user data by phone if needed
    // fetchUserByPhone(phone); // optional: implement this if needed
  }
});

const resendCode = async () => {
  if (resendTimer.value > 0 || isResendingCode.value) return;

  isResendingCode.value = true;

  try {
    const formattedPhone = phone.startsWith("+63")
      ? phone
      : phone.replace(/^0/, "+63");

    // Call the backend resend OTP endpoint
    const response = await api.post("/auth/resend-otp", {
      phoneNumber: formattedPhone
    });

    if (response.data.success) {
      const otp = response.data.otp; // Get OTP from backend response
      
      // Send OTP via SMS (if your SMS service is working)
      try {
        await api.post("/sms/send-sms", {
          number: formattedPhone,
          message: `Your new OTP code is: ${otp}`
        });
        window.showToast("A new OTP has been sent to your phone.", 'success');
      } catch (smsError) {
        console.error("SMS sending failed:", smsError);
        // Still show success but indicate SMS might not have been delivered
        window.showToast("New OTP generated. SMS delivery may be delayed.", 'info');
      }
      
      // For development
      if (process.env.NODE_ENV === 'development') {
        console.log("New OTP:", otp);
        localStorage.setItem('debug_otp', otp);
      }
      
      startResendCooldown();
    } else {
      window.showToast(response.data.message || "Failed to resend OTP.", 'failed');
    }
  } catch (error) {
    console.error("Resend code error:", error);
    window.showToast("Failed to resend OTP. Please try again.", 'failed');
  } finally {
    isResendingCode.value = false;
  }
};

// const resendCode = async () => {
//   if (resendTimer.value > 0 || isResendingCode.value) return;

//   isResendingCode.value = true;

//   try {
//     const formattedPhone = phone.startsWith("+63")
//       ? phone
//       : phone.replace(/^0/, "+63");

//     // 1. First try to send SMS
//     window.showToast("Sending OTP...", 'info');
    
//     // Generate OTP locally first (for the message)
//     const otp = Math.floor(100000 + Math.random() * 900000).toString();
    
//     try {
//       // Try to send SMS first
//       await api.post("/sms/send-sms", {
//         number: formattedPhone,
//         message: `Your new OTP code is: ${otp}`
//       });
      
//       // 2. If SMS is successful, then save to backend
//       const response = await api.post("/auth/resend-otp", {
//         phoneNumber: formattedPhone,
//         otp: otp // Send the OTP we already used in SMS
//       });

//       if (response.data.success) {
//         window.showToast("A new OTP has been sent to your phone.", 'success');
        
//         // For development
//         if (process.env.NODE_ENV === 'development') {
//           console.log("OTP:", otp);
//           localStorage.setItem('debug_otp', otp);
//         }
        
//         startResendCooldown();
//       } else {
//         window.showToast("OTP sent but failed to save. Please try again.", 'warning');
//       }
      
//     } catch (smsError) {
//       // If SMS fails, don't save to database
//       console.error("SMS sending failed:", smsError);
//       window.showToast("Failed to send OTP. Please check your connection.", 'failed');
//       return; // Exit early, don't save to database
//     }

//   } catch (error) {
//     console.error("Resend code error:", error);
    
//     if (error.response && error.response.data) {
//       const errorDetail = error.response.data.detail || error.response.data.message;
//       window.showToast(errorDetail || "Failed to resend OTP.", 'failed');
//     } else {
//       window.showToast("Failed to resend OTP. Please try again.", 'failed');
//     }
//   } finally {
//     isResendingCode.value = false;
//   }
// };

const handleVerification = async () => {
  const code = verificationCode.value.join("").trim();

  if (code.length !== 6) {
    window.showToast("Please enter the 6-digit code.", 'warning');
    return;
  }

  isLoading.value = true;

  try {
    // Call the backend OTP verification endpoint
    const response = await api.post('/auth/verify-otp', {
      phoneNumber: phone, // This should be the phone number from your component state
      otp: code
    });

    if (response.data.success) {
      // Clear user data - more defensive approach
      const userStore = useUserStore();
      if (userStore && typeof userStore.clearUser === 'function') {
        userStore.clearUser();
      } else {
        console.warn("userStore.clearUser is not available");
        if (userStore) userStore.user = null; // Fallback
      }
      
      localStorage.removeItem('user');
      localStorage.removeItem('otpPhone');

      window.showToast("Phone number verified! Please log in.", 'success');
      router.push("/login");
    } else {
      window.showToast(response.data.message || "Verification failed.", 'failed');
    }
  } catch (error) {
    console.error("Verification error:", error);
    
    // Handle different error responses
    if (error.response && error.response.data) {
      const errorDetail = error.response.data.detail || error.response.data.message;
      window.showToast(errorDetail || "Verification failed. Please try again.", 'failed');
    } else {
      window.showToast("Verification failed. Please try again.", 'failed');
    }
  } finally {
    isLoading.value = false;
  }
};

// Start a 90-second cooldown for resending the code
const startResendCooldown = () => {
  resendTimer.value = 130;
  const interval = setInterval(() => {
    if (resendTimer.value > 0) {
      resendTimer.value--;
    } else {
      clearInterval(interval);
    }
  }, 1000);
};

// Auto-focus first input on mount
onMounted(() => {
  codeInputs.value[0]?.focus();
});

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
</style>