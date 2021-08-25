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
        :label="$t('password')"
        type="password"
      />
      <q-btn
        :label="$t('login')"
        class="mt-4"
        type="submit"
        color="white"
        rounded
        outline
        :loading="submitting"
        text-color="primary"
      />
      <q-btn
        :label="$t('cancel')"
        color="primary"
        text-color="white"
        class="mt-4"
        rounded
        unelevated
        @click="$router.replace('/')"
      />
    </q-form>
  </q-page>
</template>

<script lang="ts">
import { useQuasar } from 'quasar'
import { useStore } from '../store'
import { defineComponent, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    const $router = useRouter()
    const $store = useStore()

    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    const password = ref<string>('')
    const submitting = ref<boolean>(false)
    const username = ref<string>('lb')

    // Login and show message
    function login () {
      submitting.value = true
      $store.dispatch('LOGIN', { username: username.value, password: password.value })
        .then(() => {
          $q.notify({
            type: 'positive',
            message: t('login_successfull')
          })
          $router.push('/settings')
        })
        .catch((e: { message: never}) => {
          $q.notify({
            type: 'negative',
            message: e.message
          })
          submitting.value = false
        })
    }

    return {
      login,
      password,
      submitting,
      username
    }
  }
})
</script>

<style scoped>

</style>
