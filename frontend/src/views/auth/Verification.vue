<template>
  <head>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  </head>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 relative overflow-hidden">
    <transition name="page-transition" mode="out-in" @before-leave="beforeLeave" @enter="enter" @after-enter="afterEnter">
      <div :key="transitionKey" class="page-content" :style="contentStyle">
        <!-- Falling Leaves Animation - Keeping the same animation -->
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
              <h2 class="text-2xl font-bold mb-1">Verify Your Account</h2>
              <p class="text-sm text-gray-200/90 mt-1 text-center font-light">Almost there! Enter your code to unlock access and discover the best solutions for your crops.</p>
            </div>

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

          <!-- Right Side - Verification Form -->
          <div class="w-full md:w-1/2 bg-white p-6 flex flex-col">
            <div class="w-[90%] max-w-xs mx-auto flex-1 flex flex-col justify-center">
              <h2 class="text-xl font-bold text-[#2B5329] text-center mb-6">Verify Your Phone Number</h2>

              <form class="space-y-4" @submit.prevent="handleVerification">
                <div>
                  <label class="block text-sm font-medium text-gray-700 text-center mb-4">
                    Enter the 6-digit code we sent to your phone number
                  </label>
                  <div class="flex justify-center gap-2">
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
                      class="w-12 h-12 text-center border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-[#2B5329] focus:border-[#2B5329] text-lg font-semibold"
                      ref="codeInputs"
                    />
                  </div>
                </div>

                <button 
                  type="submit" 
                  class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-[#2B5329] hover:bg-[#1F3D1F] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[#FFA500] transition-colors duration-200 mt-6"
                >
                  {{ isLoading ? "Verifying..." : "Verify" }}
                </button>

                <div class="text-center mt-6">
                  <p class="text-sm text-gray-600">
                    Didn't receive the code?
                    <button 
                      type="button"
                      @click="resendCode" 
                      class="text-[#2B5329] hover:text-[#FFA500] font-medium transition-colors ml-1"
                      :disabled="resendTimer > 0"
                    >
                      {{ resendTimer > 0 ? `Resend in ${resendTimer}s` : 'Resend Code' }}
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
import toastr from 'toastr'
import LoadingPage from '../layout/LoadingPage.vue'
// import { auth, googleProvider, signInWithPopup, RecaptchaVerifier, signInWithPhoneNumber, query, where, getDocs } from "../../api/firebase.js"
import { getFirestore, collection, addDoc, query, where, getDocs, updateDoc, doc } from "firebase/firestore";
import { getAuth, signInWithPhoneNumber, RecaptchaVerifier, signInWithPopup, GoogleAuthProvider } from "firebase/auth";
const db = getFirestore();
const auth = getAuth(); // ✅ This is required

const router = useRouter()
const route = useRoute()
const verificationCode = ref(['', '', '', '', '', ''])
const codeInputs = ref([])
const isMobile = ref(window.innerWidth < 640)
const transitionKey = ref(0)
const contentStyle = ref({})
const resendTimer = ref(0)
const uid = ref(null);
const isLoading = ref(false);
const phone = route.query.phone;

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


// ✅ Handle Verification Request

// const handleVerification = async () => {
//   const code = verificationCode.value.join("").trim();

//   if (code.length !== 6) {
//     toastr.warning("Please enter the 6-digit code.");
//     return;
//   }

//   isLoading.value = true;

//   try {
//     const result = await window.confirmationResult.confirm(code);
//     const user = result.user;

//     // ✅ Update Firestore user as verified
//     const q = query(collection(db, "users"), where("phoneNumber", "==", phone));
//     const querySnapshot = await getDocs(q);
//     if (!querySnapshot.empty) {
//       const userDoc = querySnapshot.docs[0];
//       await updateDoc(doc(db, "users", userDoc.id), {
//         verified: true,
//       });
//     }

//     toastr.success("Phone number verified!");
//     router.push("/login");
//   } catch (error) {
//     toastr.error("Invalid verification code.");
//     console.error("Code confirmation error:", error);
//   } finally {
//     isLoading.value = false;
//   }
// };

// ✅ Resend Code and Start Cooldown

const resendCode = async () => {
  if (resendTimer.value > 0) return;

  try {
    const formattedPhone = phone.startsWith("+63")
      ? phone
      : phone.replace(/^0/, "+63");

    const otp = Math.floor(100000 + Math.random() * 900000).toString();

    // 🔁 Save new OTP to Firestore
    const q = query(collection(db, "users"), where("phoneNumber", "==", formattedPhone));
    const snapshot = await getDocs(q);

    if (!snapshot.empty) {
      const userDoc = snapshot.docs[0];
      await updateDoc(doc(db, "users", userDoc.id), {
        otp,
        otpSentAt: serverTimestamp()
      });
    }

    // 🔁 Send OTP via backend (Vonage)
    await api.post("/otp/send", {
      number: formattedPhone,
      message: `Your new OTP code is: ${otp}`
    });

    toastr.success("A new OTP has been sent to your phone.");
    startResendCooldown();
  } catch (error) {
    console.error("Resend code error:", error);
    toastr.error("Failed to resend OTP.");
  }
};

const handleVerification = async () => {
  const code = verificationCode.value.join("").trim();

  if (code.length !== 6) {
    toastr.warning("Please enter the 6-digit code.");
    return;
  }

  console.log("🔐 Verifying code:", code);
  isLoading.value = true;

  try {
    const q = query(collection(db, "users"), where("phoneNumber", "==", phone));
    const querySnapshot = await getDocs(q);

    if (!querySnapshot.empty) {
      const userDoc = querySnapshot.docs[0];
      const userData = userDoc.data();

      if (userData.otp !== code) {
        toastr.error("Invalid verification code.");
        return;
      }

      await updateDoc(doc(db, "users", userDoc.id), {
        verified: true,
        otp: "", // Optional: clear stored OTP
      });

      toastr.success("Phone number verified!");
      router.push("/login");
    } else {
      toastr.error("Phone number not found.");
    }
  } catch (error) {
    console.error("❌ Error verifying OTP:", error);
    toastr.error("Verification failed.");
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