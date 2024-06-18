<script setup lang="ts">
import { ref } from 'vue'

const model = defineModel()
const show = ref(false)

defineProps({
  name: String,
  id: String,
  placeholder: String,
  required: Boolean
})
</script>

<template>
  <div class="input-wrapper">
    <input v-model="model" :type="show ? 'text' : 'password'" :name="name" :id="id" placeholder=" " :required="required" />
    <label :for="id">{{ placeholder }}</label>
    <span draggable="false" @click="show = !show" class="material-symbols-outlined eye-icon">
      {{ show ? 'visibility' : 'visibility_off' }}
    </span>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/input.scss';
</style>
