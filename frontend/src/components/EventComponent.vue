<script setup lang="ts">
import { Event } from '@/core/resources/Event'
import { useAuthStore } from '@/core/stores/auth'
import { computed, ref } from 'vue'
import { formatTime, formatDate } from '@/utils/FormatUtils'

const authStore = useAuthStore()
const userID = Number(authStore.userId)
const props = defineProps<{
  event: Event
}>()

const isOwner = computed(() => props.event.owner?.id == userID)
const isAdmin = computed(() => authStore.isAdmin)

const editable = computed(() => isOwner.value || isAdmin.value)

const showDetails = ref(false)

const timeStatus = computed(() => {
  const now = new Date()
  const start = new Date(props.event.date + 'T' + props.event.start_time)
  const end = new Date(props.event.date + 'T' + props.event.end_time)
  if (now < start) return 'future'
  if (now > end) return 'past'
  return 'current'
})

defineEmits(['delete'])
</script>

<template>
  <div class="event" :class="{ past: timeStatus == 'past' }">
    <div class="info">
      <div>
        <span class="material-symbols-outlined"> calendar_month </span>
        {{ formatDate(event.date) }}
        <div>
          <span class="material-symbols-outlined"> schedule </span>
          {{ formatTime(event.start_time) }} - {{ formatTime(event.end_time) }}
        </div>
        <span v-if="timeStatus == 'current'">(En cours)</span>
        <span v-else-if="timeStatus == 'future'">(À venir)</span>
        <span v-else-if="timeStatus == 'past'">(Passé)</span>
      </div>
      <div>
        <span>Déclaré par: {{ event.owner?.last_name.toUpperCase() }} {{ event.owner?.first_name }}</span>
        <span v-if="isOwner">(Vous)</span>
      </div>
    </div>

    <h1>{{ event.event_type?.name }}: {{ event.title }}</h1>
    <h2>
      <span class="speaker">{{ event.speaker_last_name.toUpperCase() }} {{ event.speaker_first_name }} </span>
      <span v-if="event.speaker_from != ''"> ({{ event.speaker_from }}) </span>
    </h2>
    <p class="theme">({{ event.theme?.name }})</p>

    <div class="description-expand" :class="{ show: showDetails }">
      <div class="description">
        <h3>Sommaire:</h3>
        <p>{{ event.description }}</p>
      </div>
    </div>

    <button @click="showDetails = !showDetails" v-if="event.description">
      <span v-if="showDetails">Cacher</span>
      <span v-else>Détails</span>
    </button>

    <div class="actions" v-if="editable">
      <button @click="$emit('delete', event)">
        <span class="material-symbols-outlined"> delete </span>
      </button>
      <router-link :to="'/events/edit/' + event.id">
        <span class="material-symbols-outlined"> edit </span>
      </router-link>
    </div>
  </div>
</template>

<style scoped lang="scss">
.event {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 1rem;
  background-color: var(--theme-panel);
  border: 1px solid var(--theme-border-color);
  border-radius: 5px;
  width: 100%;
  gap: 0.5rem;

  .actions {
    display: flex;
    justify-content: center;
    align-items: flex-end;
    position: absolute;
    right: 10px;
    bottom: 10px;

    button,
    a {
      display: flex;
      align-items: center;
      justify-content: center;
      text-decoration: none;
      background-color: transparent;
      color: var(--theme-text);
      border: none;
      border-radius: 50%;
      padding: 0.5rem;
      cursor: pointer;

      &:hover {
        background-color: var(--theme-panel-secondary);
      }

      &:visited {
        color: var(--theme-text);
      }
    }
  }

  &.past {
    background-color: var(--theme-panel-secondary);

    button {
      background-color: var(--theme-panel-tertiary);

      &:hover {
        background-color: var(--theme-panel);
      }
    }

    .actions button,
    .actions a {
      background-color: transparent;

      &:hover {
        background-color: var(--theme-panel);
      }
    }
  }

  button {
    background-color: var(--theme-panel-secondary);
    color: var(--theme-text);
    border: none;
    border-radius: 5px;
    padding: 0.5rem;
    cursor: pointer;

    &:hover {
      background-color: var(--theme-panel-tertiary);
    }
  }

  .info {
    display: flex;
    align-self: flex-start;
    justify-content: space-between;
    flex-wrap: wrap;
    width: 100%;
    gap: 0.5rem;

    div {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem;
      margin: 0;
    }

    &.right {
      left: auto;
      right: 10px;
    }
  }

  h1 {
    text-align: center;
    text-wrap: wrap;
    margin: 0;
    font-size: 1.2rem;
  }

  h2 {
    margin: 0;
    font-size: 1rem;

    .speaker {
      font-weight: bold;
      color: var(--main-color);
    }
  }
}

.description-expand {
  width: 100%;
  display: grid;
  grid-template-rows: 0fr;
  transition: all 0.5s ease-in-out;

  &.show {
    grid-template-rows: 1fr;
  }

  .description {
    font-size: 0.9rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
    overflow: hidden;
  }
}
</style>
