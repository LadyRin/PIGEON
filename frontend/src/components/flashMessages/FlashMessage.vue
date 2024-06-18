<script setup lang="ts">
import type { FlashMessage } from '@/utils/FlashMessages'
import { onMounted } from 'vue'

defineProps<{
  message: FlashMessage
}>()

const emit = defineEmits(['click'])

onMounted(() => {
  startTimer()
})

let timer: any

const startTimer = () => {
  timer = setTimeout(() => {
    emit('click')
  }, 5000)
}

const stopTimer = () => {
  clearTimeout(timer)
}
</script>

<template>
  <div class="flash-message" :class="[message.type]" @mouseenter="stopTimer" @mouseleave="startTimer">
    <span class="material-symbols-outlined close-button" @click="$emit('click')"> close </span>
    <div class="flash-message__title">
      {{ message.title }}
    </div>
    <div class="flash-message__content">
      {{ message.text }}
    </div>
  </div>
</template>

<style scoped lang="scss">
.flash-message {
  position: relative;
  padding: 1rem;
  border-radius: 0.25rem;
  border: 1px solid transparent;
  box-shadow: 0 0 0.5rem rgba(0, 0, 0, 0.1);
  opacity: 1;
  pointer-events: auto;

  width: clamp(10rem, 100%, 40rem);

  &:hover {
    filter: brightness(0.95);
  }

  &.success {
    background-color: var(--theme-success);
    border-color: #badbcc;
  }

  &.error {
    background-color: var(--theme-error);
    border-color: #f5c2c7;
  }

  &.info {
    background-color: var(--theme-info);
    border-color: #bee5eb;
  }

  &.warning {
    background-color: var(--theme-warning);
    border-color: #ffeeba;
  }
}

.flash-message__title {
  font-weight: bold;
}

.close-button {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  font-size: 2rem;
  color: var(--theme-color);
  cursor: pointer;
  border-radius: 50%;
  transition: background-color 0.3s;

  &:hover {
    background-color: #00000020;
  }
}
</style>
