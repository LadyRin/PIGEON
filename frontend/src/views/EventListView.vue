<script setup lang="ts">
import EventComponent from '@/components/EventComponent.vue'
import { Event } from '@/core/resources/Event'
import { onMounted, ref } from 'vue'
import { eventService } from '@/core/services'
import { useAuthStore } from '@/core/stores/auth'
import { flashMessage } from '@/utils/FlashMessages'
import { handleError } from '@/utils/ErrorHandler'
import { popupUtil } from '@/utils/Popup'

const authStore = useAuthStore()
const events = ref<Event[]>([])

const fetchEvents = () => {
  eventService.getAll(authStore.accessToken).then((data) => {
    events.value = data
  })
}

onMounted(() => {
  fetchEvents()
})

const deleteEvent = async (event: Event) => {
  const confirmed = await popupUtil.confirm('Êtes-vous sûr de vouloir supprimer cet événement?')

  if (!confirmed) return

  eventService
    .delete(event, authStore.accessToken)
    .then(() => {
      flashMessage.success('Événement supprimé avec succès')
      fetchEvents()
    })
    .catch(handleError)
}
</script>

<template>
  <div class="container">
    <h1>Évènements</h1>
    <div class="event-list">
      <EventComponent v-for="event in events" :key="event.id" :event="event" @delete="deleteEvent(event)" />
    </div>
  </div>
</template>

<style scoped lang="scss">
.container {
  padding: 0 50px;
  gap: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
}

.event-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
  width: 100%;
}
</style>
