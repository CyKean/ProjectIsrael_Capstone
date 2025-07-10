// stores/user.js
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null,
    uid: null
  }),
  actions: {
    setUser(user, uid) {
      this.user = user
      this.uid = uid
      localStorage.setItem('user', JSON.stringify(user))
      localStorage.setItem('uid', uid)
    },
    loadUser() {
      const storedUser = localStorage.getItem('user')
      const storedUid = localStorage.getItem('uid')
      if (storedUser && storedUid) {
        this.user = JSON.parse(storedUser)
        this.uid = storedUid
      }
    },
    logout() {
      this.user = null
      this.uid = null
      localStorage.removeItem('user')
      localStorage.removeItem('uid')
    }
  }
})