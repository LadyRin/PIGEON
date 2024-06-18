<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { flashMessage, type FlashMessage } from '@/utils/FlashMessages'
import FlashMessageComponent from './FlashMessage.vue'

const messages = ref<FlashMessage[]>([])

const show = (message: FlashMessage) => {
  messages.value.push(message)
}

onMounted(() => {
  flashMessage.registerHandler(show)
})

const hideFlashMessage = (message: FlashMessage) => {
  messages.value = messages.value.filter((m) => m !== message)
}
</script>

<template>
  <div class="flash-container">
    <TransitionGroup name="flash-message">
      <FlashMessageComponent v-for="(message, index) in messages" :key="index" :message="message" @click="hideFlashMessage(message)" />
    </TransitionGroup>
  </div>
</template>

<style scoped lang="scss">
.flash-container {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  left: 0;
  z-index: 2000;
  pointer-events: none;

  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1rem;
}

.flash-message-enter-active,
.flash-message-leave-active {
  transition:
    transform 0.3s,
    opacity 0.3s,
    filter 0.3s;
}

.flash-message-enter-from {
  transform: translateY(100%);
  opacity: 0;
  filter: brightness(0.8);
}

.flash-message-enter-to,
.flash-message-leave-from {
  transform: translateY(0);
  opacity: 1;
  filter: brightness(1);
}

.flash-message-leave-to {
  transform: translateX(30%);
  opacity: 0;
  filter: brightness(0.8);
}
</style>
