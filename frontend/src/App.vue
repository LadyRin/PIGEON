<script setup lang="ts">
import ConfirmPopup from '@/components/popup/ConfirmPopup.vue'
import PromptPopup from '@/components/popup/PromptPopup.vue'
import AlertPopup from '@/components/popup/AlertPopup.vue'
import TokenExpiredPopup from '@/components/popup/TokenExpiredPopup.vue'
import FlashContainer from '@/components/flashMessages/FlashContainer.vue'
import NavbarComponent from '@/components/NavbarComponent.vue'
import { onMounted, ref, watch } from 'vue'
import { useAuthStore } from '@/core/stores/auth'
import { useRouter } from 'vue-router'

const theme = ref(localStorage.getItem('theme') || 'dark')
const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  document.body.className = theme.value
})

watch(theme, (value) => {
  localStorage.setItem('theme', value)
  document.body.className = value
})

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <TokenExpiredPopup />
  <ConfirmPopup />
  <PromptPopup />
  <AlertPopup />
  <FlashContainer />

  <NavbarComponent />

  <div class="router-view">
    <RouterView v-slot="{ Component }">
      <component :is="Component" />
      <div class="theme-selector">
        <button type="button" @click="theme = theme === 'dark' ? 'light' : 'dark'">
          <span v-if="theme === 'dark'" class="material-symbols-outlined">dark_mode</span>
          <span v-else class="material-symbols-outlined">light_mode</span>
        </button>
      </div>
    </RouterView>
  </div>
</template>

<style scoped lang="scss">
.flashes {
  z-index: 1000;
  position: fixed;
}

.router-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-top: 100px;
  height: 100%;
  width: 100%;
  position: relative;
}

.theme-selector {
  position: absolute;
  top: 10px;
  right: 10px;

  button {
    background-color: transparent;
    color: var(--theme-color);
    border: none;
    border-radius: 50%;
    padding: 10px;
    cursor: pointer;
  }
}
</style>
