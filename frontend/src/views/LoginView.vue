<script setup lang="ts">
import TextInput from '@/components/input/TextInput.vue'
import PasswordInput from '@/components/input/PasswordInput.vue'
import { handleError } from '@/utils/ErrorHandler'
import { ref } from 'vue'
import { useAuthStore } from '@/core/stores/auth'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const authStore = useAuthStore()
const router = useRouter()

const login = () => {
  authStore
    .login(username.value, password.value)
    .then(() => {
      console.log('Login successful 2')
      router.push('/')
    })
    .catch(handleError)
}
</script>

<template>
  <div class="container">
    <form @keypress.enter="login">
      <h2>Login</h2>
      <p><em>Login using your LDAP account.</em></p>

      <div class="form-group">
        <TextInput v-model="username" label="Username" placeholder="Username" />
        <PasswordInput v-model="password" label="Password" placeholder="Password" />
      </div>

      <button type="button" class="submit-button" @click="login">Login</button>
    </form>
  </div>
</template>

<style scoped lang="scss">
@import '@/assets/styles/form.scss';
</style>
