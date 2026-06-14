import { defineStore } from 'pinia'
import { ref } from 'vue'

export interface AuthUser {
  id: number
  username: string
  role: string
}

const USER_KEY = 'auth_user'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<AuthUser | null>(JSON.parse(localStorage.getItem(USER_KEY) || 'null'))
  const token = ref<string>(localStorage.getItem('auth_token') || '')

  function setAuth(u: AuthUser, t: string) {
    user.value = u
    token.value = t
    localStorage.setItem(USER_KEY, JSON.stringify(u))
    localStorage.setItem('auth_token', t)
  }

  function logout() {
    user.value = null
    token.value = ''
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem('auth_token')
  }

  const isLoggedIn = () => !!token.value

  return { user, token, setAuth, logout, isLoggedIn }
})
