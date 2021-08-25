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
        rounded
        outline
      />
      <q-btn
        :label="$t('cancel')"
        color="primary"
        text-color="white"
        class="mt-4"
        @click="$router.replace('/settings')"
        rounded
        unelevated
      />
    </q-form>
  </q-page>
</template>

<script lang="ts">
import Axios from 'app/node_modules/axios'
import { useQuasar } from 'quasar'
import { useStore } from '../store'
import { computed, defineComponent, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    const $router = useRouter()
    const $store = useStore()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    // New password
    const newPassword = ref<string>('')
    const api = computed(() => {
      return $store.getters.GET_API
    })

    // Reset password
    const resetPassword = async () => {
      $q.loading.show({
        delay: 300 // ms
      })
      const response = await Axios.post(`${api.value}/v1/setpassword`, { password: newPassword.value })
      if (response.status === 200) {
        $q.notify({ type: 'positive', message: t('password_set_success') })
        newPassword.value = ''
        $router.replace('/settings')
      } else {
        $q.notify({ type: 'negative', message: t('error') })
      }
      $q.loading.hide()
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
