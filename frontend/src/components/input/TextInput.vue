<script setup lang="ts">
const model = defineModel()

defineProps({
  name: String,
  id: String,
  placeholder: String,
  type: String,
  required: Boolean,
  disabled: Boolean,
  maxlength: String
})
</script>

<template>
  <div class="input-wrapper" :class="{ disabled: disabled }">
    <input
      v-model="model"
      :type="type"
      :name="name"
      :id="id"
      placeholder=" "
      :required="required"
      :disabled="disabled"
      :maxlength="maxlength" />
    <label :for="id">{{ placeholder }}</label>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/input.scss';
</style>
