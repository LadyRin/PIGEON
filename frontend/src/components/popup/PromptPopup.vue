<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { popupUtil } from '@/utils/Popup'

const message = ref('')
const isOpen = ref(false)
const resolve = ref<Function | null>(null)
const reject = ref<Function | null>(null)
const input = ref('')

const open = (m: string) => {
  message.value = m
  isOpen.value = true
  return new Promise<string | null>((rs, rj) => {
    resolve.value = rs
    reject.value = rj
  })
}

defineExpose({
  open
})

onMounted(() => {
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      cancel()
    }
  })

  popupUtil.registerPromptPopup(open)
})

const confirm = () => {
  resolve.value?.(input.value)
  isOpen.value = false
  input.value = ''
}

const cancel = () => {
  resolve.value?.(null)
  isOpen.value = false
  input.value = ''
}
</script>

<template>
  <div class="background" v-if="isOpen">
    <div class="popup">
      <div class="popup-content">
        <p>{{ message }}</p>
        <div class="popup-prompt">
          <input type="text" v-model="input" />
        </div>
        <div class="popup-buttons">
          <button class="cancel-button" @click.stop="cancel">Cancel</button>
          <button class="confirm-button" @click.stop="confirm">Ok</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/popup.scss';
</style>
