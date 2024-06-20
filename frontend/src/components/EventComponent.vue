<script setup lang="ts">
import { Event } from '@/core/resources/Event'
import { useAuthStore } from '@/core/stores/auth'
import { computed } from 'vue'

const authStore = useAuthStore()
const userID = Number(authStore.userId)
const props = defineProps<{
  event: Event
}>()

const isOwner = computed(() => props.event.owner?.id == userID)
const isAdmin = computed(() => authStore.isAdmin)

defineEmits(['delete'])
</script>

<template>
  <div class="event" :class="{ 'is-owner': isOwner }">
    <h1>{{ event.title }}</h1>
    <p>
      <strong>{{ event.event_type?.name }}</strong> sur le thème <strong>{{ event.theme?.name }}</strong>
    </p>
    <p class="description">{{ event.description }}</p>

    <div class="details">
      <p>
        Intervenant: {{ event.speaker_first_name }} {{ event.speaker_last_name }}
        <span v-if="event.speaker_from">de "{{ event.speaker_from }}"</span>
      </p>

      <p v-if="isOwner">Organisateur: <span class="you">Vous</span></p>
      <p v-else>Organisateur: {{ event.owner?.first_name }} {{ event.owner?.last_name }}</p>
      <p>Date: {{ new Date(event.date).toLocaleDateString() }}</p>
      <p>Heure: {{ event.start_time }} - {{ event.end_time }}</p>
    </div>

    <div class="actions" v-if="isOwner || isAdmin">
      <router-link :to="'/events/edit/' + event.id" class="material-symbols-outlined">edit</router-link>
      <button @click="$emit('delete')" class="material-symbols-outlined">delete</button>
    </div>
  </div>
</template>

<style scoped lang="scss">
.event {
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 1rem;
  background-color: var(--theme-panel);
  border: 1px solid var(--theme-border-color);
  border-radius: 5px;
  width: 100%;

  &.is-owner {
    border-color: var(--main-color);
  }
}

.description {
  margin: 0.5rem 0;
  white-space: pre-wrap;
  border-left: 3px solid var(--theme-panel-tertiary);
  padding-left: 0.5rem;
}

.you {
  color: var(--main-color);
  font-weight: bold;
}

.actions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: absolute;
  bottom: 10px;
  right: 10px;

  button,
  a {
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
</style>
