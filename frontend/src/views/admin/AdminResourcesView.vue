<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { EventTheme } from '@/core/resources/EventTheme'
import { EventType } from '@/core/resources/EventType'
import { MailingList } from '@/core/resources/MailingList'
import { useAuthStore } from '@/core/stores/auth'
import { popupUtil } from '@/utils/Popup'
import { APIResource } from '@/core/resources/APIResource'
import { handleError } from '@/utils/ErrorHandler'
import { APIResourceService } from '@/core/services/APIService'
import { eventThemeService, mailingListService, eventTypeService } from '@/core/services'

const store = useAuthStore()

const themes = ref<EventTheme[]>([])
const types = ref<EventType[]>([])
const mailingLists = ref<MailingList[]>([])

const fetchResources = () => {
  eventThemeService
    .getAll(store.accessToken)
    .then((data) => {
      themes.value = data
    })
    .catch(handleError)

  eventTypeService
    .getAll(store.accessToken)
    .then((data) => {
      types.value = data
    })
    .catch(handleError)

  mailingListService
    .getAll(store.accessToken)
    .then((data) => {
      mailingLists.value = data
    })
    .catch(handleError)
}

onMounted(() => {
  fetchResources()
})

const create = async (resource: APIResource, service: APIResourceService<any>, list: any[]) => {
  const res = await popupUtil.resourceEdit(resource)
  if (!res) {
    fetchResources()
    return
  }

  service
    .create(res, store.accessToken)
    .then((data: any) => {
      list.push(data)
    })
    .catch(handleError)
}

const edit = async (resource: APIResource, service: APIResourceService<any>, list: any[]) => {
  const res = await popupUtil.resourceEdit(resource)
  if (!res) {
    fetchResources()
    return
  }

  service
    .update(res, store.accessToken)
    .then((data: any) => {
      const index = list.findIndex((r: any) => r.id === data.id)
      list[index] = data
    })
    .catch(handleError)
}

const _delete = async (resource: APIResource, service: APIResourceService<any>, list: any[]) => {
  const res = await popupUtil.confirm(`Are you sure you want to delete this resource?`)
  if (!res) {
    fetchResources()
    return
  }

  service
    .delete(resource, store.accessToken)
    .then(() => {
      const index = list.findIndex((r: any) => r.id === resource.getIdentifier())
      list.splice(index, 1)
    })
    .catch(handleError)
}
</script>

<template>
  <div class="container">
    <h1>Admin - Resources</h1>

    <div class="admin-panel">
      <div class="admin-panel-item">
        <h2>
          Event Themes
          <button class="material-symbols-outlined" @click="create(new EventTheme(), eventThemeService, themes)">add</button>
        </h2>
        <ul>
          <li v-for="r in themes" :key="r.id">
            <span>
              {{ r.name }}
            </span>
            <span>
              <button class="material-symbols-outlined" @click="edit(r, eventThemeService, themes)">edit</button>
              <button class="material-symbols-outlined" @click="_delete(r, eventThemeService, themes)">delete</button>
            </span>
          </li>
        </ul>
      </div>
      <div class="admin-panel-item">
        <h2>
          Event Types
          <button class="material-symbols-outlined" @click="create(new EventType(), eventTypeService, types)">add</button>
        </h2>
        <ul>
          <li v-for="r in types" :key="r.id">
            <span>
              {{ r.name }}
            </span>
            <span>
              <button class="material-symbols-outlined" @click="edit(r, eventTypeService, types)">edit</button>
              <button class="material-symbols-outlined" @click="_delete(r, eventTypeService, types)">delete</button>
            </span>
          </li>
        </ul>
      </div>
      <div class="admin-panel-item">
        <h2>
          Mailing Lists
          <button class="material-symbols-outlined" @click="create(new MailingList(), mailingListService, mailingLists)">add</button>
        </h2>
        <ul>
          <li v-for="r in mailingLists" :key="r.id">
            <span>
              {{ r.name }}
            </span>
            <span>
              <button class="material-symbols-outlined" @click="edit(r, mailingListService, mailingLists)">edit</button>
              <button class="material-symbols-outlined" @click="_delete(r, mailingListService, mailingLists)">delete</button>
            </span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/input.scss';
@import '@/assets/styles/form.scss';
.container {
  padding: 0 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  text-align: center;
}

.admin-panel {
  display: flex;

  justify-content: space-between;
}

.admin-panel-item {
  flex: 1;
  background-color: var(--theme-panel);
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;

  h2 {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
  }

  button {
    background-color: transparent;
    color: var(--theme-text);
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;

    &:hover {
      background-color: var(--theme-panel-secondary);
    }

    &:active {
      background-color: var(--theme-panel-tertiary);
    }
  }
}

ul {
  list-style: none;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

li {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  border: 1px solid var(--theme-border-color);
  border-radius: 5px;
  background-color: var(--theme-panel-secondary);
  padding: 10px;

  .material-symbols-outlined {
    background-color: transparent;
    color: var(--theme-text);
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;

    &:hover {
      background-color: var(--theme-panel-tertiary);
    }

    &:active {
      background-color: var(--theme-panel);
    }
  }
}
</style>
