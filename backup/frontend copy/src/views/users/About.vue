<template>
  <div class="min-h-screen bg-white font-poppins about-section">
    <!-- Top Section with Layered Rectangles -->
    <div class="relative overflow-visible">
      <!-- Layered rectangles container -->
      <div class="relative custom-height overflow-visible">
        <!-- Bottom green rectangle -->
        <div class="absolute top-0 left-0 right-0 h-full">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" preserveAspectRatio="none" class="w-full h-full">
            <path d="M0,0 L1440,0 L1440,90 Q1220,120 720,120 Q220,120 0,90 Z" fill="#4CAF50" />
          </svg>
        </div>
        
        <!-- Top beige rectangle -->
        <div class="absolute top-0 left-0 right-0 h-[85%]">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120" preserveAspectRatio="none" class="w-full h-full">
            <path d="M0,0 L1440,0 L1440,70 Q1220,100 720,100 Q220,100 0,70 Z" fill="#FFE4B5" />
          </svg>
        </div>

        <!-- Content overlay -->
        <div class="absolute inset-x-0 bottom-0 flex flex-col items-center translate-y-[60%] z-10 overflow-visible px-4 sm:px-0">
          <div class="text-center w-full">
            <div class="inline-block bg-white px-6 sm:px-16 py-2 sm:py-3 rounded-xl">
              <h1 class="text-3xl sm:text-4xl md:text-6xl font-bold text-[#4CAF50]">
                ABOUT US
              </h1>
            </div>
            <p class="text-sm sm:text-base md:text-lg text-black max-w-3xl mx-auto mt-4 bg-white/80 rounded-lg p-2">
              Pioneering sustainable agriculture through innovative technology and traditional wisdom
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Content Section -->
    <div class="relative bg-white pt-32 sm:pt-40 pb-8 px-4">
      <div class="container mx-auto max-w-7xl">
        <!-- Three Column Layout -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-8 max-w-6xl mx-auto -mt-16">
          <!-- Mission -->
          <div class="bg-white rounded-xl p-4 sm:p-6 relative border-2 border-[#4CAF50] mt-12 sm:mt-0">
            <div class="absolute -top-8 left-1/2 transform -translate-x-1/2">
              <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center">
                <Lightbulb class="w-8 sm:w-9 h-8 sm:h-9 text-yellow-500" />
              </div>
            </div>
            <h2 class="text-xl sm:text-2xl font-bold text-[#FFD700] text-center mt-8 mb-4">
              Our Mission
            </h2>
            <p class="text-sm sm:text-base text-black text-center">
              Project Israel combines centuries of farming wisdom with cutting-edge technology to revolutionize sustainable agriculture. We're committed to developing innovative solutions that help farmers maximize yields while minimizing environmental impact.
            </p>
          </div>

          <!-- 100% Organic Crops Card -->
          <div class="bg-white rounded-xl p-4 sm:p-6 relative border-2 border-[#4CAF50] mt-12 sm:mt-0">
            <div class="absolute -top-8 left-1/2 transform -translate-x-1/2">
              <div class="w-16 h-16 bg-[#E8F5E9] rounded-full flex items-center justify-center">
                <Sprout class="w-8 sm:w-9 h-8 sm:h-9 text-green-600" />
              </div>
            </div>
            <h2 class="text-xl sm:text-2xl font-bold text-[#4CAF50] text-center mt-8 mb-4">
              100% Organic Crops
            </h2>
            <p class="text-sm sm:text-base text-black text-center mb-4">
              All our crops are grown using organic farming methods, ensuring the highest quality produce while protecting the environment.
            </p>
            <div class="text-xs sm:text-sm text-gray-600 text-center border-t border-gray-200 pt-4">
              <h3 class="font-semibold mb-2">Our Goals:</h3>
              <ul class="space-y-2">
                <li>✓ Sustainable Farming Practices</li>
                <li>✓ Zero Chemical Usage</li>
                <li>✓ Biodiversity Protection</li>
              </ul>
            </div>
          </div>

          <!-- Vision -->
          <div class="bg-white rounded-xl p-4 sm:p-6 relative border-2 border-[#4CAF50] mt-12 sm:mt-0">
            <div class="absolute -top-8 left-1/2 transform -translate-x-1/2">
              <div class="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center">
                <Eye class="w-8 sm:w-9 h-8 sm:h-9 text-yellow-500" />
              </div>
            </div>
            <h2 class="text-xl sm:text-2xl font-bold text-[#FFD700] text-center mt-8 mb-4">
              Our Vision
            </h2>
            <p class="text-sm sm:text-base text-black text-center">
              Project Israel combines centuries of farming wisdom with cutting-edge technology to revolutionize sustainable agriculture. We're committed to developing innovative solutions that help farmers maximize yields while minimizing environmental impact.
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Information and Features Section -->
    <div class="container mx-auto px-4 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 max-w-6xl mx-auto">
        <!-- Left Column - Information Cards -->
        <div class="space-y-4">
          <!-- Contact Card -->
          <div class="bg-[#FFE4B5] rounded-xl p-4 shadow-lg flex flex-col sm:flex-row items-center sm:items-start gap-4 transform transition-transform duration-300 hover:-translate-y-1 hover:bg-[#FFE4B5]/90">
            <div class="w-16 sm:w-20 h-16 sm:h-20 bg-[#E8F5E9] rounded-lg flex items-center justify-center">
              <MessageSquare class="w-8 sm:w-12 h-8 sm:h-12 text-green-600" />
            </div>
            <div class="text-left sm:text-left">
              <h3 class="font-bold text-base sm:text-lg uppercase mb-2 text-black">CONTACT</h3>
              <p class="text-sm sm:text-base text-black">09292664302</p>
              <p class="text-sm sm:text-base text-black break-words">maryhelpofChristiansSchool@gmail.com</p>
            </div>
          </div>

          <!-- Owner Card -->
          <div class="bg-[#FFE4B5] rounded-xl p-4 shadow-lg flex flex-col sm:flex-row items-center sm:items-start gap-4 transform transition-transform duration-300 hover:-translate-y-1 hover:bg-[#FFE4B5]/90">
            <div class="w-16 sm:w-20 h-16 sm:h-20 bg-[#E8F5E9] rounded-lg flex items-center justify-center">
              <School class="w-8 sm:w-12 h-8 sm:h-12 text-green-600" />
            </div>
            <div class="text-left sm:text-left">
              <h3 class="font-bold text-base sm:text-lg uppercase mb-2 text-black">OWNER</h3>
              <p class="text-sm sm:text-base text-black">Mary Help of Christians School (INC),</p>
              <p class="text-sm sm:text-base text-black">Don Bosco</p>
            </div>
          </div>

          <!-- Location Card -->
          <div class="bg-[#FFE4B5] rounded-xl p-4 shadow-lg flex flex-col sm:flex-row items-center sm:items-start gap-4 transform transition-transform duration-300 hover:-translate-y-1 hover:bg-[#FFE4B5]/90">
            <div 
              @click="showMapModal = true"
              class="w-16 sm:w-20 h-16 sm:h-20 bg-[#E8F5E9] rounded-lg flex items-center justify-center cursor-pointer hover:opacity-90 transition-opacity overflow-hidden relative group"
            >
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3689.0848031780247!2d121.21258467484937!3d13.404935686951763!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33bce88ac908b113%3A0xad738f4ed48f873f!2sMary%20Help%20of%20Christians%20School%20(Mindoro)%2C%20Inc.!5e1!3m2!1sen!2sph!4v1739719936279!5m2!1sen!2sph"
                class="w-full h-full"
                style="border:0"
                loading="lazy"
                referrerpolicy="no-referrer-when-downgrade"
              ></iframe>
              <div class="absolute inset-0 bg-black/40 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <button class="bg-white text-black text-xs px-2 py-1 rounded-md hover:bg-gray-100 transition-colors">
                  View Map
                </button>
              </div>
            </div>
            <div class="text-left sm:text-left">
              <h3 class="font-bold text-base sm:text-lg uppercase mb-2 text-black">LOCATION</h3>
              <p class="text-sm sm:text-base text-black">Parang, Calapan City,</p>
              <p class="text-sm sm:text-base text-black">Oriental Mindoro</p>
            </div>
          </div>
        </div>

        <!-- Right Column - Features Panel -->
        <div class="bg-[#E8F5E9] rounded-xl p-4 sm:p-6 shadow-lg relative min-h-[450px]">
          <h2 class="text-xl sm:text-2xl font-bold text-green-700 mb-6 uppercase">PROJECT ISRAEL FEATURES</h2>
          
          <div class="space-y-4 relative z-10">
            <div v-for="feature in features" :key="feature" 
                 class="bg-white rounded-lg p-3 flex items-center gap-2 transform transition-transform duration-300 hover:translate-x-2">
              <CheckCircle2 class="w-4 sm:w-5 h-4 sm:h-5 text-green-600 flex-shrink-0" />
              <span class="text-sm sm:text-base text-black">{{ feature }}</span>
            </div>
          </div>

          <!-- Farmer Illustration -->
          <img 
            src="/public/images/farmer.png" 
            alt="Farmer Illustration"
            class="absolute bottom-0 right-0 w-32 sm:w-48 h-auto pointer-events-none"
          />
        </div>
      </div>
    </div>

    <!-- Map Modal -->
    <Teleport to="body">
      <div v-if="showMapModal" 
           class="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-2 sm:p-4"
           @click.self="closeModal">
        <div class="bg-white rounded-xl w-full max-w-4xl h-[80vh] relative">
          <button 
            @click="closeModal"
            class="absolute right-2 sm:right-4 top-2 sm:top-4 z-10 bg-white rounded-full p-2 shadow-lg hover:bg-gray-100 transition-colors"
          >
            <XIcon class="w-5 h-5 sm:w-6 sm:h-6 text-gray-600" />
          </button>
          <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3689.0848031780247!2d121.21258467484937!3d13.404935686951763!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x33bce88ac908b113%3A0xad738f4ed48f873f!2sMary%20Help%20of%20Christians%20School%20(Mindoro)%2C%20Inc.!5e1!3m2!1sen!2sph!4v1739719936279!5m2!1sen!2sph"
            class="w-full h-full rounded-xl"
            style="border:0"
            allowfullscreen=""
            loading="lazy"
            referrerpolicy="no-referrer-when-downgrade"
          ></iframe>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script>
import { ref } from 'vue'
import { Lightbulb, Eye, Users, Sprout, MessageSquare, School, CheckCircle2, XIcon } from 'lucide-vue-next'

export default {
  name: 'AboutPage',
  components: {
    Lightbulb,
    Eye,
    Users,
    Sprout,
    MessageSquare,
    School,
    CheckCircle2,
    XIcon
  },
  setup() {
    const showMapModal = ref(false)
    const closeModal = () => {
      showMapModal.value = false
    }

    const features = ref([
      'Real-Time Soil Monitoring',
      'Automated Watering System',
      'Smart Crop Selection',
      'Weather-Based Crop Forecasting',
      'Remote Monitoring & Control',
      'Task Scheduling & Alerts'
    ])

    return {
      showMapModal,
      features,
      closeModal
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

.container {
  max-width: 1280px;
  margin: 0 auto;
}

.custom-height {
  height: 100px;
  overflow: visible;
}

.absolute {
  position: absolute;
  z-index: 10;
}

/* Responsive breakpoints */
@media (min-width: 640px) {
  .custom-height {
    height: 120px;
  }
}

@media (min-width: 768px) {
  .custom-height {
    height: 140px;
  }
}

@media (min-width: 1024px) {
  .custom-height {
    height: 180px;
  }
}

svg {
  filter: none;
}

.rounded-xl {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.border-2 {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
              0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

.w-12.h-12 {
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.w-12.h-12:hover {
  transform: scale(1.1);
}

h2 {
  letter-spacing: 0.025em;
}

p {
  line-height: 1.7;
}

.stats-card {
  background-color: #E8F5E9;
  transition: all 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 8px -1px rgba(0, 0, 0, 0.1);
}

html {
  scroll-behavior: smooth;
}

/* Mobile optimizations */
@media (max-width: 640px) {
  .grid {
    gap: 1rem;
  }
  
  .space-y-4 > * {
    margin-top: 1rem;
  }
  
  .px-16 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
  
  .text-4xl {
    font-size: 1.875rem;
  }
  
  .w-20, .h-20 {
    width: 4rem;
    height: 4rem;
  }

  .max-w-4xl {
    width: 95%;
    margin: 0 auto;
  }
}

/* Navigation styles */
:deep(nav) {
  position: relative;
  z-index: 50;
}

/* Card hover effects */
.bg-\[#FFE4B5\] {
  transition: all 0.3s ease;
}

.bg-\[#FFE4B5\]:hover {
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}

/* Feature items hover effect */
.bg-white {
  transition: all 0.3s ease;
}

.bg-white:hover {
  background-color: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

/* Icon container styles */
.w-20.h-20.bg-\[#E8F5E9\] {
  transition: all 0.3s ease;
}

.w-20.h-20.bg-\[#E8F5E9\]:hover {
  transform: scale(1.05);
}

/* Font family */
.font-poppins {
  font-family: 'Poppins', sans-serif;
}

/* Additional spacing adjustments */
.content-section {
  margin-bottom: -2rem;
}

.information-section {
  margin-top: -2rem;
}

/* Google Maps styles */
.gm-style-cc {
  display: none;
}

[ref="miniMap"],
[ref="fullMap"] {
  background: #E8F5E9;
}

/* Custom map control */
.custom-map-control {
  margin: 10px;
  padding: 5px;
}

.custom-map-control button {
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
}

/* Smooth transitions */
.grid,
.flex,
.text-4xl,
.px-16,
.w-20,
.h-20 {
  transition: all 0.3s ease;
}

/* Ensure content is readable on all devices */
@media (max-width: 480px) {
  .text-sm {
    font-size: 0.8125rem;
  }
  
  .text-base {
    font-size: 0.9375rem;
  }
  
  .space-y-4 {
    margin-top: 0.75rem;
  }
}

/* Improve touch targets on mobile */
@media (max-width: 640px) {
  button,
  [role="button"] {
    min-height: 44px;
    min-width: 44px;
  }
}
</style>