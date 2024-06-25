<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { popupUtil } from '@/utils/Popup'
import TextInput from '@/components/input/TextInput.vue'

const resource = ref<any>({})
const isOpen = ref(false)
const resolve = ref<Function | null>(null)
const reject = ref<Function | null>(null)
const fields = ref<string[]>([])

const open = (rs: any) => {
  resource.value = rs
  fields.value = Object.keys(Reflect.construct(rs.constructor, [])).filter((field) => field !== 'id')
  isOpen.value = true
  return new Promise<any | null>((rs, rj) => {
    resolve.value = rs
    reject.value = rj
  })
}

defineExpose({
  open
})

onMounted(() => {
  popupUtil.registerResourceEditPopup(open)
})

const confirm = () => {
  console.log(resource.value)
  resolve.value?.(resource.value)
  isOpen.value = false
  resource.value = {}
}

const cancel = () => {
  resolve.value?.(null)
  isOpen.value = false
  resource.value = {}
}
</script>

<template>
  <div class="background" v-if="isOpen">
    <div class="popup">
      <div class="popup-content">
        <h2>Create or edit resource</h2>
        <div class="popup-prompt">
          <div class="form-group">
            <template v-for="field in fields" :key="field">
              <TextInput v-model="resource[field]" :id="field" :placeholder="field" />
            </template>
          </div>
        </div>
        <div class="popup-buttons">
          <button class="cancel-button" @click.stop="cancel">Cancel</button>
          <button class="confirm-button" @click.stop="confirm">Confirm</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/popup.scss';
@import '@/assets/styles/form.scss';

.popup-content {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 2rem;
}

button {
  flex: 1;
  cursor: pointer;
}
</style>
