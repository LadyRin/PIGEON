<script setup lang="ts">
import { computed } from 'vue'
const page = defineModel<number>('page', {
  required: true
})

const itemsPerPage = defineModel<number>('itemsPerPage', {
  required: true
})

const props = defineProps<{
  optionValues: number[]
  pagination: {
    pageCount: number
    pageStart: number
    pageStop: number
    itemsLength: number
  }
}>()

const emit = defineEmits(['fetch'])

const canPrevious = computed(() => page.value > 1)
const canNext = computed(() => page.value < props.pagination.pageCount)

const previousPage = () => {
  if (page.value > 1) {
    page.value--
    emit('fetch')
  }
}

const nextPage = () => {
  if (page.value < props.pagination.pageCount) {
    page.value++
    emit('fetch')
  }
}
</script>

<template>
  <div class="pagination">
    <span>Items per page:</span>
    <select v-model="itemsPerPage" @change="emit('fetch')">
      <option v-for="value in props.optionValues" :value="value" :key="value">{{ value }}</option>
    </select>

    <span>{{ pagination.pageStart + 1 }} - {{ pagination.pageStop }} of {{ pagination.itemsLength }}</span>
    <button id="previous-page" @click="previousPage" :disabled="!canPrevious">
      <span class="material-symbols-outlined">arrow_back</span>
    </button>
    <button id="next-page" @click="nextPage" :disabled="!canNext">
      <span class="material-symbols-outlined">arrow_forward</span>
    </button>
  </div>
</template>

<style scoped lang="scss">
.pagination {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
  align-self: flex-end;

  button {
    display: flex;
    padding: 0.4rem;
    justify-content: center;
    align-items: center;
    text-transform: uppercase;
    color: var(--theme-text);

    background-color: var(--theme-panel);
    border: none;
    border-radius: 50%;

    transition: background-color 0.2s;

    &:hover:not(:disabled) {
      background-color: var(--theme-panel-secondary);
    }

    &:disabled {
      background-color: var(--theme-panel-secondary);
      color: #666;
    }
  }
}

select {
  padding: 0.4rem;
  border: none;
  border-radius: 0.2rem;
  background-color: var(--theme-panel);
  color: var(--theme-text);

  transition: background-color 0.2s;

  &:disabled {
    background-color: var(--theme-panel-secondary);
    color: #666;
  }
}
</style>
