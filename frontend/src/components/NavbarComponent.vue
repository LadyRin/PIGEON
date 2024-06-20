<script setup lang="ts">
import { useAuthStore } from '@/core/stores/auth'
import { useRouter } from 'vue-router'
const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav v-if="authStore.isAuthenticated">
    <div class="left">
      <div class="title">
        <h2>
          <span class="material-symbols-outlined">raven</span>
          PIGEON
        </h2>
        <h2>Event Management</h2>
      </div>
      <div class="links">
        <router-link to="/events">Évènements</router-link>

        <router-link to="/events/new">Nouvel Évènement</router-link>

        <router-link v-if="authStore.isAdmin" to="/admin">Admin</router-link>
      </div>
    </div>

    <div class="right">
      <span>
        Bienvenue, <span class="you">{{ authStore.username }}</span>
      </span>
      <span class="material-symbols-outlined logout" @click="logout"> logout </span>
    </div>
  </nav>
  <nav v-else>
    <div class="left">
      <div class="title">
        <h2>
          <span class="material-symbols-outlined">raven</span>
          PIGEON
        </h2>
        <h2>Event Management</h2>
      </div>
    </div>
  </nav>
</template>

<style scoped lang="scss">
nav {
  background-color: var(--theme-panel-secondary);
  color: var(--theme-text);
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100px;
  min-height: 100px;
  transition: background-color 0.2s;
}

.left {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  width: 100%;

  .title {
    border-right: 1px solid var(--theme-text);
    padding: 0 1rem;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    h2 {
      margin: 0;
      font-size: 1.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }

    span {
      text-align: center;
    }
  }

  .links {
    display: flex;
    flex-direction: row;

    a {
      text-decoration: none;
      color: var(--theme-text);
      height: 100%;
      display: flex;
      align-items: center;
      background-color: var(--theme-panel-secondary);
      border-radius: 0.5rem;
      padding: 0.5rem 1rem;
      transition: background-color 0.2s;

      &:hover {
        background-color: var(--theme-panel);
      }
    }
  }
}

.right {
  display: flex;
  text-align: right;
  gap: 1rem;

  .you {
    font-weight: bold;
    color: var(--main-color);
  }
}

.logout {
  cursor: pointer;
  margin-right: 1rem;
  padding: 0.5rem;
  border-radius: 0.5rem;
  background-color: var(--theme-panel-secondary);
  transition: background-color 0.2s;

  &:hover {
    background-color: var(--theme-panel);
  }
}
</style>
