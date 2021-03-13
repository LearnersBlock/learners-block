<template>
  <div class="flex flex-col w-100 items-center justify-center">
    <router-link class="mt-40"  to="/">
        <q-btn color="primary" class="mb-28">
          {{$t('home')}}
        </q-btn>
        </router-link>
    <q-form
      @submit="login"
      class="w-1/5 mb-6 self-center"
    >
      <div class="text-h4 mb-6 text-gray-600">Login</div>

      <q-input
        filled
        v-model="password"
        label="Your password"
        type="password"
      />

      <q-btn
        label="Login"
        class="mt-4"
        type="submit"
        color="primary"
      />
    </q-form>
</div>
</template>

<script lang="ts">
import { defineComponent, ref } from '@vue/composition-api'

export default defineComponent({
  setup (_, { root }) {
    // Username
    const username = ref<string>('lb')
    // Password
    const password = ref<string>('')

    // Login and show message
    const login = async () => {
      root.$store.dispatch('LOGIN', { username: username.value, password: password.value })
        .then(() => {
          root.$q.notify({
            type: 'positive',
            message: root.$t('login_successfull') as string
          })
          root.$router.push('/settings')
        })
        .catch(e => {
          root.$q.notify({
            type: 'negative',
            message: e.message
          })
        })
    }

    return {
      username,
      password,
      login
    }
  }
})
</script>

<style scoped>

</style>
