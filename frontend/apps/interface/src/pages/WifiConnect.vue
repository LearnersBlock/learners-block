<template>
  <q-page class="flex flex-col justify-center items-center p-3">
    <div class="text-h4 mb-6 text-gray-600">
      {{ $t('wifi') }}
    </div>
    <q-form
      @submit="connect"
      class="mb-6 flex flex-col"
    >
      <div class="text-subtitle1 mb-6 text-center">
        {{ $t('network_absent') }}
      </div>
      <q-select
        class="mb-5"
        :label="$t('select_ssid')"
        rounded
        outlined
        v-model="wifiSsid"
        :options="ssids"
        option-label="ssid"
      />
      <q-input
        filled
        v-model="password"
        :label="$t('password')"
        type="password"
      />
      <q-btn
        :label="$t('connect')"
        class="mt-4"
        type="submit"
        color="white"
        rounded
        outline
        :disabled="!wifiSsid"
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
        @click="$router.replace('/settings')"
      />
    </q-form>
  </q-page>
</template>

<script lang="ts">
import Axios from 'app/node_modules/axios'
import { useQuasar } from 'quasar'
import { defineComponent, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    const ssids = ref<any>([])
    const password = ref<string>('')
    const submitting = ref<boolean>(false)
    const username = ref<string>('')
    const wifiSsid = ref<any>('')

    onMounted(() => {
      fetchNetworks()
    })

    // Send connect request
    async function connect () {
      submitting.value = true
      await Axios.post('http://192.168.42.1:8080/connect', {
        ssid: wifiSsid.value.ssid,
        identity: username.value,
        passphrase: password.value
      }, { withCredentials: false }).then(() => {
        $q.notify({
          type: 'positive',
          multiLine: true,
          timeout: 0,
          actions: [
            {
              label: t('close'),
              color: 'white',
              handler: () => { /* ... */ }
            }
          ],
          message: t('connection_reset_request')
        })
      }).catch(function (error) {
        console.log(error)
        $q.notify({
          type: 'negative',
          multiLine: true,
          timeout: 0,
          actions: [
            {
              label: t('close'),
              color: 'white',
              handler: () => { /* ... */ }
            }
          ],
          message: t('network_connect_fail')
        })
      })
      submitting.value = false
    }

    async function fetchNetworks () {
      $q.loading.show({
        delay: 300 // ms
      })
      await Axios.get('http://192.168.42.1:8080/networks', { withCredentials: false }).then((response) => {
        ssids.value = response.data
        if (ssids.value.length === 0) {
          $q.notify({
            type: 'warning',
            multiLine: true,
            timeout: 0,
            actions: [
              {
                label: t('close'),
                color: 'white',
                handler: () => { /* ... */ }
              }
            ],
            message: t('no_networks')
          })
        }
      }).catch(function (error) {
        console.log(error)
        $q.notify({
          type: 'negative',
          multiLine: true,
          timeout: 0,
          actions: [
            {
              label: t('close'),
              color: 'white',
              handler: () => { /* ... */ }
            }
          ],
          message: t('network_fetch_fail')
        })
      })
      submitting.value = false
      $q.loading.hide()
    }

    return {
      connect,
      password,
      ssids,
      submitting,
      wifiSsid
    }
  }
})

</script>

<style scoped>

</style>
