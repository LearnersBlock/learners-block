<template>
  <q-page class="flex flex-col justify-center items-center">
    <q-form
      @submit="login"
      class="mb-6 flex flex-col"
    >
      <div class="text-h4 mb-6 text-gray-600">
        {{ $t('login') }}
      </div>

      <q-input
        filled
        v-model="password"
        :label="$t('your_password')"
        type="password"
      />

      <q-btn
        :label="$t('login')"
        class="mt-4"
        type="submit"
        color="white"
        text-color="primary"
      />
      <q-btn
        color="primary"
        text-color="white"
        class="mt-4"
        to="/"
      >
        {{ $t('cancel') }}
      </q-btn>
    </q-form>
  </q-page>
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