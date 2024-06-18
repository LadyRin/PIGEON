<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { popupUtil } from '@/utils/Popup'

const message = ref('')
const isOpen = ref(false)
const resolve = ref<Function | null>(null)
const reject = ref<Function | null>(null)

const open = (m: string) => {
  message.value = m
  isOpen.value = true
  return new Promise<boolean>((rs, rj) => {
    resolve.value = rs
    reject.value = rj
  })
}

defineExpose({
  open
})

const confirm = () => {
  resolve.value?.(true)
  isOpen.value = false
}

const cancel = () => {
  resolve.value?.(false)
  isOpen.value = false
}

onMounted(() => {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      cancel()
    }
  })

  popupUtil.registerConfirmPopup(open)
})
</script>

<template>
  <div class="background" v-if="isOpen" @click="cancel">
    <div class="popup">
      <div class="popup-content">
        <p>{{ message }}</p>
        <div class="popup-buttons">
          <button class="cancel-button" @click.stop="cancel">No</button>
          <button class="confirm-button" @click.stop="confirm">Yes</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/popup.scss';
</style>
