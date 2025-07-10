import { createWebHistory } from 'vue-router'

const routes = [
  // Public routes
  {
    path: '/',
    name: 'Landing',
    component: () => import('../views/users/LandingPage.vue'),
    meta: { hideSidebar: true, isPublic: true }
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/users/About.vue'),
    meta: { hideSidebar: true, isPublic: true }
  },
  {
    path: '/organicsection',
    name: 'OrganicSection',
    component: () => import('../views/users/OrganicSection.vue'),
    meta: { hideSidebar: true, isPublic: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: { hideSidebar: true, isPublic: true }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue'),
    meta: { hideSidebar: true, isPublic: true }
  },
  {
    path: '/forgotpassword',
    name: 'ForgotPassword',
    component: () => import('../views/auth/ForgotPassword.vue'),
    meta: { hideSidebar: true, isPublic: true }
  },
  {
    path: '/auth/verify-otp',
    name: 'VerifyOTP',
    component: () => import('../views/auth/Verification.vue'),
    meta: { hideSidebar: true, isPublic: true }
  },

  // Authenticated routes (with Sidebar)
  {
    path: '/app',
    component: () => import('../Main.vue'),
    meta: { requiresAuth: true },
    redirect: '/app/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/users/Dashboard.vue')
      },
      {
        path: 'prediction',
        name: 'CropPrediction',
        component: () => import('../views/users/CropPrediction.vue')
      },
      {
        path: 'control',
        name: 'DeviceControl',
        component: () => import('../views/users/DeviceControl.vue')
      },
      {
        path: 'npkData',
        name: 'npkData',
        component: () => import('../views/users/npkData.vue')
      },
      {
        path: 'soilph',
        name: 'SoilPH',
        component: () => import('../views/users/SoilPH.vue')
      },
      {
        path: 'soil-moisture',
        name: 'SoilMoisture',
        component: () => import('../views/users/SoilMoisture.vue')
      },
      {
        path: 'water-level',
        name: 'WaterLevel',
        component: () => import('../views/users/WaterLevel.vue')
      },
      {
        path: 'temperature-humidity',
        name: 'TemperatureHumidity',
        component: () => import('../views/users/TemperatureHumidity.vue')
      },
      {
        path: 'motor-control',
        name: 'MotorControl',
        component: () => import('../views/users/MotorControl.vue')
      },
      {
        path: 'soil',
        name: 'SoilAnalysis',
        component: () => import('../views/users/SoilAnalysis.vue')
      },
      {
        path: 'profile',
        name: 'UserProfile',
        component: () => import('../views/users/UserProfile.vue')
      },
      {
        path: 'weather',
        name: 'WeatherForecast',
        component: () => import('../views/users/WeatherForecast.vue')
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: () => import('../views/users/Notifications.vue')
      },
      {
        path: 'manual-guide',
        name: 'ManualGuide',
        component: () => import('../views/users/ManualGuide.vue')
      },
      {
        path: 'recalibration',
        name: 'Recalibration',
        component: () => import('../views/users/ReCalibration.vue')
      }
    ]
  },
  // Fallback route for 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/error/NotFound.vue')
  }
]

export const userRoutes = routes