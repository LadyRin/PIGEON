import { defineStore } from 'pinia'
import { onMounted, ref, watch } from 'vue'
import AxiosClient from '@/utils/AxiosClient'
import { flashMessage } from '@/utils/FlashMessages'
import type { BookableResource } from '../resources/BookableResource'
import { bookingService } from '../services'
import { useAuthStore } from './auth'

const useBookingStore = defineStore('booking', () => {
  const resources = ref<BookableResource[]>([])

  const fetchResources = async () => {
    try {
      resources.value = await bookingService.getResources(useAuthStore().getAccessToken())
    } catch (err) {
      flashMessage.error('Failed to fetch resources')
    }
  }

  fetchResources()

  return {
    resources
  }
})

export { useBookingStore }
