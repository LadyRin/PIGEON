<script setup lang="ts">
import { onMounted, ref, type Ref } from 'vue'
import { Server } from '@/core/resources/Server'
import { useAuthStore } from '@/core/stores/auth'
import { popupUtil } from '@/utils/Popup'
import { handleError } from '@/utils/ErrorHandler'
import { serverService } from '@/core/services'
import { sshService } from '@/core/services'
import { flashMessage } from '@/utils/FlashMessages'

const store = useAuthStore()
const servers = ref<Server[]>([])
const sshKey = ref<string>('ssh-rsa')

const fetchServers = () => {
  serverService.getAll(store.accessToken).then((data: any) => {
    servers.value = data
  })
}

onMounted(() => {
  fetchServers()
  fetchPublicKey()
})

const create = async (server: Server) => {
  const res = await popupUtil.resourceEdit(server)
  if (!res) {
    fetchServers()
    return
  }

  serverService
    .create(res, store.accessToken)
    .then((data: any) => {
      servers.value.push(data)
    })
    .catch(handleError)
}

const edit = async (server: Server) => {
  const res = await popupUtil.resourceEdit(server)
  if (!res) {
    fetchServers()
    return
  }

  serverService
    .update(res, store.accessToken)
    .then((data: any) => {
      const index = servers.value.findIndex((s: any) => s.id === data.id)
      servers.value[index] = data
    })
    .catch(handleError)
}

const _delete = async (resource: Server) => {
  const res = await popupUtil.confirm(`Are you sure you want to delete ${resource.constructor.name} ${resource.getIdentifier()}?`)
  if (!res) {
    fetchServers()
    return
  }

  serverService
    .delete(resource, store.accessToken)
    .then(() => {
      const index = servers.value.findIndex((r: any) => r.id === resource.getIdentifier())
      servers.value.splice(index, 1)
    })
    .catch(handleError)
}

const generateSSHKey = async () => {
  const confirmed = await popupUtil.confirm(
    'Êtes-vous sûr de vouloir générer une nouvelle paire de clés SSH? Toute connection SSH existante sera perdue.'
  )
  if (!confirmed) {
    return
  }

  sshService.generateKeyPair(store.accessToken).then((data: any) => {
    sshKey.value = data
  })
}

const copySSHKey = async () => {
  navigator.clipboard.writeText(sshKey.value)
  flashMessage.success('Public key copied to clipboard')
}

const fetchPublicKey = async () => {
  sshService.getPublicKey(store.accessToken).then((data: any) => {
    sshKey.value = data
  })
}

const forceUpdate = async () => {
  const confirmed = await popupUtil.confirm('Êtes-vous sûr de vouloir forcer la mise à jour des serveurs?')
  if (!confirmed) {
    return
  }

  sshService.forceUpdate(store.accessToken).then(() => {
    flashMessage.success('Mise à jour des serveurs lancée')
  })
}
</script>

<template>
  <div class="container">
    <h1>Admin - SSH</h1>

    <div class="admin-panel">
      <div class="admin-panel-item">
        <h2>
          Serveurs
          <button class="material-symbols-outlined" @click="create(new Server())">add</button>
        </h2>
        <ul>
          <li v-for="s in servers" :key="s.id">
            <span>
              {{ s.name }}
            </span>
            <span>
              <button class="material-symbols-outlined" @click="edit(s)">edit</button>
              <button class="material-symbols-outlined" @click="_delete(s)">delete</button>
            </span>
          </li>
        </ul>
      </div>
      <div class="admin-panel-item">
        <h2>Clés SSH</h2>

        <button @click="generateSSHKey">Générer une paire de clés</button>
        <div class="horizontal">
          <h3>Clé publique:</h3>
          <code>
            {{ sshKey }}
            <button class="material-symbols-outlined" @click="copySSHKey">content_copy</button>
          </code>
        </div>

        <button @click="forceUpdate">Mettre à jour les serveurs</button>
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

.horizontal {
  display: flex;
  justify-content: stretch;
  width: 100%;
  gap: 16px;
}

code {
  flex: 1;
  word-break: break-all;

  position: relative;
  background-color: var(--theme-panel-secondary);
  padding: 10px;
  padding-right: 60px;
  border-radius: 5px;
  font-family: monospace;
  text-align: left;
  min-height: 10px;

  button {
    position: absolute;
    right: 10px;
    top: 10px;

    background-color: transparent;
    color: var(--theme-text);
    border: none;
    border-radius: 5px;
    padding: 5px 10px;
    cursor: pointer;

    &:hover {
      background-color: var(--theme-panel);
    }

    &:active {
      background-color: var(--theme-panel-tertiary);
    }
  }
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
