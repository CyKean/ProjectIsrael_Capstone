// utils/motor.js
import { defineStore } from 'pinia'

export const useMotorStore = defineStore('motor', {
  state: () => ({
    status: false,
    lastUpdated: null,
    history: []
  }),
  actions: {
    setStatus(status) {
      this.status = status
      this.lastUpdated = new Date()
    },
    addToHistory(entry) {
      this.history.unshift(entry)
      // Keep only last 100 entries
      if (this.history.length > 100) {
        this.history.pop()
      }
    }
  }
})