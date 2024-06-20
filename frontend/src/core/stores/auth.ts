import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import AxiosClient from '@/utils/AxiosClient'
import { buildException } from '@/core/exceptions'
import { flashMessage } from '@/utils/FlashMessages'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('accessToken') || '')
  const refreshToken = ref(localStorage.getItem('refreshToken') || '')
  const userId = ref(localStorage.getItem('userId') || '')
  const isAuthenticated = ref(localStorage.getItem('isAuthenticated') === 'true')
  const email = ref(localStorage.getItem('email') || '')
  const username = ref(localStorage.getItem('username') || '')
  const isAdmin = ref(localStorage.getItem('isAdmin') === 'true')
  const client: AxiosClient = new AxiosClient(import.meta.env.VITE_API_URL + '/api')

  const login = (_username: string, _password: string) => {
    return client
      .post('/token', { username: _username, password: _password })
      .then((result) => result.data as AuthResponse)
      .then((data) => {
        accessToken.value = data.access
        refreshToken.value = data.refresh
        userId.value = data.id.toString()
        email.value = data.email
        username.value = data.username
        isAdmin.value = data.is_admin
        isAuthenticated.value = true
        flashMessage.success('Login successful')
      })
      .catch((err) => {
        throw buildException(err)
      })
  }

  const logout = () => {
    accessToken.value = ''
    refreshToken.value = ''
    userId.value = ''
    isAuthenticated.value = false
    email.value = ''
    username.value = ''
    isAdmin.value = false
    localStorage.clear()
    flashMessage.success('You have been logged out')
  }

  watch(accessToken, (value) => {
    localStorage.setItem('accessToken', value)
  })

  watch(refreshToken, (value) => {
    localStorage.setItem('refreshToken', value)
  })

  watch(userId, (value) => {
    localStorage.setItem('userId', value)
  })

  watch(isAuthenticated, (value) => {
    localStorage.setItem('isAuthenticated', value.toString())
  })

  watch(email, (value) => {
    localStorage.setItem('email', value)
  })

  watch(username, (value) => {
    localStorage.setItem('username', value)
  })

  watch(isAdmin, (value) => {
    localStorage.setItem('isAdmin', value.toString())
  })

  return {
    accessToken,
    refreshToken,
    userId,
    isAuthenticated,
    email,
    username,
    isAdmin,
    login,
    logout
  }
})

export interface AuthResponse {
  refresh: string
  access: string
  id: number
  email: string
  username: string
  date: string
  is_admin: boolean
}
