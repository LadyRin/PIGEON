<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { eventService } from '@/core/services'
import { eventThemeService } from '@/core/services'
import { eventTypeService } from '@/core/services'
import { mailingListService } from '@/core/services'
import { Event } from '@/core/resources/Event'
import { EventTheme } from '@/core/resources/EventTheme'
import { EventType } from '@/core/resources/EventType'
import { MailingList } from '@/core/resources/MailingList'
import { useAuthStore } from '@/core/stores/auth'
import TextInput from '@/components/input/TextInput.vue'
import TextAreaInput from '@/components/input/TextAreaInput.vue'
import { flashMessage } from '@/utils/FlashMessages'
import { handleError } from '@/utils/ErrorHandler'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()
const event = ref<Event>(new Event())
const authStore = useAuthStore()

const eventThemes = ref<EventTheme[]>([])
const eventTypes = ref<EventType[]>([])
const mailingLists = ref<MailingList[]>([])

const id = Number(route.params.id)

onMounted(() => {
  eventThemeService.getAll(authStore.accessToken).then((data) => {
    eventThemes.value = data
  })

  eventTypeService.getAll(authStore.accessToken).then((data) => {
    eventTypes.value = data
  })

  mailingListService.getAll(authStore.accessToken).then((data) => {
    mailingLists.value = data
  })

  if (id) {
    eventService
      .get(id, authStore.accessToken)
      .then((data) => {
        event.value = data
      })
      .catch(() => {
        flashMessage.error('Évènement non trouvé')
        router.push({ name: 'EventList' })
      })
  }
})

const create = async () => {
  eventService
    .create(event.value, authStore.accessToken)
    .then(() => {
      flashMessage.success('Évènement créé avec succès')
      router.push({ name: 'EventList' })
    })
    .catch(handleError)
}

const edit = async () => {
  eventService
    .update(event.value, authStore.accessToken)
    .then(() => {
      flashMessage.success('Évènement modifié avec succès')
      router.push({ name: 'EventList' })
    })
    .catch(handleError)
}
</script>

<template>
  <div class="container">
    <form>
      <h2 v-if="id">Modifier l'évènement</h2>
      <h2 v-else>Créer un évènement</h2>

      <div class="form-group">
        <TextInput v-model="event.title" placeholder="Titre" />
        <TextAreaInput v-model="event.description" placeholder="Description" />

        <div class="horizontal">
          <div class="horizontal">
            <h4>Type:</h4>
            <select v-model="event.event_type">
              <option value="" disabled selected>Type d'évènement</option>
              <option v-for="eventType in eventTypes" :key="eventType.id" :value="eventType">
                {{ eventType.name }}
              </option>
            </select>
          </div>
          <div class="horizontal">
            <h4>Thème:</h4>
            <select v-model="event.theme">
              <option value="" disabled selected>Thème de l'évènement</option>
              <option v-for="eventTheme in eventThemes" :key="eventTheme.id" :value="eventTheme">
                {{ eventTheme.name }}
              </option>
            </select>
          </div>
        </div>

        <h4>Personnes concernées:</h4>
        <select v-model="event.mailing_list">
          <option value="" disabled selected>Personnes concernées</option>
          <option v-for="mailingList in mailingLists" :key="mailingList.id" :value="mailingList">
            {{ mailingList.name }}
          </option>
        </select>

        <h4>Intervenant:</h4>
        <div class="horizontal">
          <TextInput v-model="event.speaker_first_name" placeholder="Prénom" />
          <TextInput v-model="event.speaker_last_name" placeholder="Nom" />
        </div>
        <TextInput v-model="event.speaker_from" placeholder="Provenance" />
        <TextInput v-model="event.speaker_comment" placeholder="Commentaire" />
        <h4>
          <label for="date">Date:</label>
        </h4>
        <input v-model="event.date" type="date" />

        <div class="horizontal">
          <div class="horizontal">
            <h4>De</h4>
            <input v-model="event.start_time" type="time" id="start-time" />
          </div>
          <div class="horizontal">
            <h4>à</h4>
            <input v-model="event.end_time" type="time" id="end-time" />
          </div>
        </div>
      </div>

      <button v-if="id" type="button" class="submit-button" @click="edit">Mettre à jour</button>
      <button v-else type="button" class="submit-button" @click="create">Créer</button>
    </form>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/form.scss';
@import '@/assets/styles/input.scss';

.horizontal {
  display: flex;
  flex-wrap: wrap;
  justify-content: stretch;
  align-items: center;
  gap: 16px;
}
</style>
