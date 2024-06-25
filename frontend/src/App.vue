<script setup lang="ts">
import ConfirmPopup from '@/components/popup/ConfirmPopup.vue'
import PromptPopup from '@/components/popup/PromptPopup.vue'
import AlertPopup from '@/components/popup/AlertPopup.vue'
import ResourceEditPopup from '@/components/popup/ResourceEditPopup.vue'
import TokenExpiredPopup from '@/components/popup/TokenExpiredPopup.vue'
import FlashContainer from '@/components/flashMessages/FlashContainer.vue'
import NavbarComponent from '@/components/NavbarComponent.vue'
import { onMounted, ref, watch } from 'vue'
import { tokenExpirationUtil } from '@/utils/TokenExpirationUtil'
import { useAuthStore } from '@/core/stores/auth'

const theme = ref(localStorage.getItem('theme') || 'dark')
const store = useAuthStore()
let interval: any

onMounted(() => {
  document.body.className = theme.value

  interval = setInterval(() => {
    console.log('Refreshing')
    if (store.isAuthenticated) {
      store.refresh().catch(() => {
        tokenExpirationUtil.warnTokenIsExpired()
        clearInterval(interval)
      })
    }
  }, 1000 * 60)
})

watch(theme, (value) => {
  localStorage.setItem('theme', value)
  document.body.className = value
})
</script>

<template>
  <TokenExpiredPopup />
  <ResourceEditPopup />
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
  padding: 100px 0;
  min-height: calc(100vh - 100px);
  height: fit-content;
  width: 100%;
  position: relative;
  overflow: auto;
}

.theme-selector {
  position: fixed;
  top: 110px;
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
