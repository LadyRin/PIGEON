import { defineStore } from 'pinia'
import { ref } from 'vue'
import AxiosClient from '@/utils/AxiosClient'
import { buildException } from '@/core/exceptions'

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref('')
  const refreshToken = ref('')
  const userId = ref('')
  const isAuthenticated = ref(false)
  const email = ref('')
  const username = ref('')
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
        isAuthenticated.value = true
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
  }

  return {
    accessToken,
    refreshToken,
    userId,
    isAuthenticated,
    email,
    username,
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
}
