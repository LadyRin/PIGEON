<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue'
import { EventTheme } from '@/core/resources/EventTheme'
import { EventType } from '@/core/resources/EventType'
import { MailingList } from '@/core/resources/MailingList'
import { eventThemeService } from '@/core/services'
import { eventTypeService } from '@/core/services'
import { mailingListService } from '@/core/services'
import { useAuthStore } from '@/core/stores/auth'
import { popupUtil } from '@/utils/Popup'
import { APIResource } from '@/core/resources/APIResource'
import { handleError } from '@/utils/ErrorHandler'
import { APIResourceService } from '@/core/services/APIService'

const store = useAuthStore()

interface Resource {
  constructor: any
  service: APIResourceService<any>
  list: Ref<any[]>
  displayName: string
}

const resources: Record<string, Resource> = {
  EventTheme: {
    constructor: EventTheme,
    service: eventThemeService,
    list: ref<EventTheme[]>([]),
    displayName: 'Thèmes'
  },
  EventType: {
    constructor: EventType,
    service: eventTypeService,
    list: ref<EventType[]>([]),
    displayName: 'Types'
  },
  MailingList: {
    constructor: MailingList,
    service: mailingListService,
    list: ref<MailingList[]>([]),
    displayName: 'Listes de diffusion'
  }
}

const fetchResources = () => {
  for (const key in resources) {
    const { service, list } = resources[key]
    service.getAll(store.accessToken).then((data: any) => {
      list.value = data
    })
  }
}

onMounted(() => {
  fetchResources()
})

const create = async (resource: APIResource) => {
  const service = resources[resource.constructor.name].service
  const list = resources[resource.constructor.name].list

  const res = await popupUtil.resourceEdit(resource)
  if (!res) {
    fetchResources()
    return
  }

  service
    .create(res, store.accessToken)
    .then((data: any) => {
      list.value.push(data)
    })
    .catch(handleError)
}

const edit = async (resource: APIResource) => {
  const service = resources[resource.constructor.name].service
  const list = resources[resource.constructor.name].list

  const res = await popupUtil.resourceEdit(resource)
  if (!res) {
    fetchResources()
    return
  }

  service
    .update(res, store.accessToken)
    .then((data: any) => {
      const index = list.value.findIndex((r: any) => r.id === data.id)
      list.value[index] = data
    })
    .catch(handleError)
}

const _delete = async (resource: APIResource) => {
  const service = resources[resource.constructor.name].service
  const list = resources[resource.constructor.name].list

  const res = await popupUtil.confirm(`Are you sure you want to delete ${resource.constructor.name} ${resource.getIdentifier()}?`)
  if (!res) {
    fetchResources()
    return
  }

  service
    .delete(resource, store.accessToken)
    .then(() => {
      const index = list.value.findIndex((r: any) => r.id === resource.getIdentifier())
      list.value.splice(index, 1)
    })
    .catch(handleError)
}
</script>

<template>
  <div class="container">
    <h1>Admin Panel</h1>

    <div class="admin-panel">
      <div class="admin-panel-item" v-for="(resource, key) in resources" :key="key">
        <h2>
          {{ resource.displayName }}
          <button class="material-symbols-outlined" @click="create(new resource.constructor())">add</button>
        </h2>
        <ul>
          <li v-for="r in resource.list.value" :key="r.id">
            <span>
              {{ r.name }}
            </span>
            <span>
              <button class="material-symbols-outlined" @click="edit(r)">edit</button>
              <button class="material-symbols-outlined" @click="_delete(r)">delete</button>
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
