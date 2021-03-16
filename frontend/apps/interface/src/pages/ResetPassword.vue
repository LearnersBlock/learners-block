<template>
  <q-page class="flex flex-col justify-center items-center">
    <q-form
      @submit="resetPassword"
      class="mb-6 flex flex-col"
    >
      <div class="text-h4 mb-6 text-gray-600">
        {{ $t('set_password') }}
      </div>
      <q-input
        filled
        v-model="newPassword"
        :label="$t('your_new_password')"
        type="password"
      />

      <q-btn
        :label="$t('set_password')"
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
import { computed, defineComponent, ref } from '@vue/composition-api'
import Axios from 'app/node_modules/axios'

export default defineComponent({
  setup (_, { root }) {
    // New password
    const newPassword = ref<string>('')
    const api = computed(() => {
      return root.$store.getters.GET_API
    })
    // Reset password
    const resetPassword = async () => {
      const response = await Axios.post(`${api.value}/v1/setpassword`, { password: newPassword.value })
      if (response.status === 200) {
        root.$q.notify({ type: 'positive', message: root.$tc('password_set_success') })
        newPassword.value = ''
      } else {
        root.$q.notify({ type: 'negative', message: root.$tc('error') })
      }
    }

    return {
      newPassword,
      resetPassword
    }
  }
})
</script>

<style scoped>

</style>
