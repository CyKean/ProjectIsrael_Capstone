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
        name: 'PROJECT ISRAEL',
        short_name: 'PJIR',
        description: 'Project Israel',
        theme_color: '#ffffff',
        icons: [
          {
            src: 'maskable_icon_x192.png', // Place these in /public
            sizes: '192x192',
            type: 'image/png',
            purpose: 'any',
          },
          {
            src: 'maskable_icon_x512.png', // Use the same logo for 512x512
            sizes: '512x512',
            type: 'image/png',
            purpose: 'any',
          },
        ],
        screenshot: [
          {
            src: 'screenshot-desktop.png',
            sizes: '1920x1080',
            type: 'image/png',
            form_factor: 'wide',
          },
          {
            src: 'screenshot-mobile.png',
            sizes: '720x1280',
            type: 'image/png',
            form_factor: 'narrow',
          }
        ]
      },
      workbox: {
        maximumFileSizeToCacheInBytes: 50000000,
        globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'], // Files to cache
      },
    }),
  ],
})