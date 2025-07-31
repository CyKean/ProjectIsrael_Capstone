import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    vue(),
    VitePWA({
      registerType: 'autoUpdate', // Auto-update service worker
      includeAssets: ['favicon.ico', 'apple-touch-icon.png'], // Cached assets
      manifest: {
        name: 'My Vue PWA',
        short_name: 'VuePWA',
        description: 'My Awesome Vue.js PWA',
        theme_color: '#ffffff',
        icons: [
          {
            src: 'public/images/logo/logo.png', // Place these in /public
            sizes: '192x192',
            type: 'image/png',
          },
          {
            src: 'pwa-512x512.png',
            sizes: '512x512',
            type: 'image/png',
          },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'], // Files to cache
      },
    }),
  ],
})