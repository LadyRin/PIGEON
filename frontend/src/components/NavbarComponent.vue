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
    <div class="title">
      <h2>
        <span class="material-symbols-outlined">raven</span>
        PIGEON
      </h2>
      <h2>Event Management</h2>
    </div>

    <span class="material-symbols-outlined logout" @click="logout"> logout </span>
  </nav>
  <nav v-else>
    <div class="title">
      <h2>
        <span class="material-symbols-outlined">raven</span>
        PIGEON
      </h2>
      <h2>Event Management</h2>
    </div>
  </nav>
</template>

<style scoped lang="scss">
nav {
  background-color: var(--theme-panel-secondary);
  color: var(--theme-text);
  padding: 1rem;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100px;

  ul {
    display: flex;
    flex-direction: row;
    list-style-type: none;
    padding: 0;
    align-items: center;
    gap: 1rem;
  }
}

.title {
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

.logout {
  cursor: pointer;
}
</style>
