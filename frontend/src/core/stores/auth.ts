import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import AxiosClient from '@/utils/AxiosClient'
import { flashMessage } from '@/utils/FlashMessages'

export const useAuthStore = defineStore('auth', () => {
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
        setAccessToken(data.access)
        setRefreshToken(data.refresh)
        userId.value = data.id.toString()
        email.value = data.email
        username.value = data.username
        isAdmin.value = data.is_admin
        isAuthenticated.value = true
        flashMessage.success('Login successful')
      })
      .catch((err) => {
        throw err
      })
  }

  const logout = () => {
    setAccessToken('')
    setRefreshToken('')
    userId.value = ''
    isAuthenticated.value = false
    email.value = ''
    username.value = ''
    isAdmin.value = false
    localStorage.clear()
    flashMessage.success('You have been logged out')
  }

  const refresh = () => {
    return client
      .post('/token/refresh', { refresh: getRefreshToken() })
      .then((result) => result.data as AuthResponse)
      .then((data) => {
        setAccessToken(data.access)
        setRefreshToken(data.refresh)
        return true
      })
      .catch(() => {
        throw new Error('Token is not valid')
      })
  }

  const getAccessToken = () => {
    return localStorage.getItem('accessToken') ?? ''
  }

  const setAccessToken = (token: string) => {
    localStorage.setItem('accessToken', token)
  }

  const getRefreshToken = () => {
    return localStorage.getItem('refreshToken') ?? ''
  }

  const setRefreshToken = (token: string) => {
    localStorage.setItem('refreshToken', token)
  }

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
    getAccessToken,
    userId,
    isAuthenticated,
    email,
    username,
    isAdmin,
    login,
    logout,
    refresh
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

export interface TokenResponse {
  refresh: string
  access: string
}
