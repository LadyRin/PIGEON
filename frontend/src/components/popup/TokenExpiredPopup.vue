<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { tokenExpirationUtil } from '@/utils/TokenExpirationUtil'
import { useAuthStore } from '@/core/stores/auth'
import { useRouter } from 'vue-router'

const isOpen = ref(false)
const store = useAuthStore()
const router = useRouter()

const open = () => {
  isOpen.value = true
}

const confirm = () => {
  isOpen.value = false
  store.logout()
  router.push('/login')
}

onMounted(() => {
  tokenExpirationUtil.registerHandler(open)
})
</script>

<template>
  <div class="background" v-if="isOpen">
    <div class="popup">
      <div class="popup-content">
        <p>Your session has expired. Please log in again.</p>
        <div class="popup-buttons">
          <button class="confirm-button" @click.stop="confirm">Ok</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/popup.scss';
</style>
