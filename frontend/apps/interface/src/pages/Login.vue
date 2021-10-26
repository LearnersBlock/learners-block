<template>
  <q-page class="flex flex-col justify-center items-center">
    <q-form
      class="mb-6 flex flex-col"
      @submit="login"
    >
      <div class="text-h4 mb-6 text-gray-600">
        {{ $t('login') }}
      </div>
      <q-input
        v-model="password"
        filled
        :type="isPwd ? 'password' : 'text'"
        :label="$t('password')"
      >
        <template #append>
          <q-icon
            :name="isPwd ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPwd = !isPwd"
          />
        </template>
      </q-input>

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
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    const route = useRoute()
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
          if (route.params.data) {
            $router.replace(route.params.data as string)
          } else {
            $router.replace('/settings')
          }
        })
        .catch((e: { message: never}) => {
          $q.notify({
            type: 'negative',
            message: e.message,
            timeout: 0,
            actions: [
              { label: t('close'), color: 'black', handler: () => { /* ... */ } }
            ]
          })
          submitting.value = false
        })
    }

    return {
      isPwd: ref(true),
      login,
      password,
      submitting
    }
  }
})
</script>

<style scoped>

</style>
