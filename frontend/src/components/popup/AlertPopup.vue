<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { popupUtil } from '@/utils/Popup'

const message = ref('')
const isOpen = ref(false)
const resolve = ref<Function | null>(null)

const open = (m: string) => {
  message.value = m
  isOpen.value = true
  return new Promise<void>((rs) => {
    resolve.value = rs
  })
}

defineExpose({
  open
})

onMounted(() => {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      confirm()
    }
  })

  popupUtil.registerAlertPopup(open)
})

const confirm = () => {
  resolve.value?.()
  isOpen.value = false
}
</script>

<template>
  <div class="background" v-if="isOpen">
    <div class="popup">
      <div class="popup-content">
        <p>{{ message }}</p>
        <div class="popup-buttons">
          <button @click.stop="confirm">Ok</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/popup.scss';

</style>
