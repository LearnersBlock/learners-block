<template>
  <q-page class="flex flex-col justify-center items-center p-3">
    <div class="text-h4 mb-3 text-gray-600">
      {{ $t('wifi') }}
    </div>
    <q-form
      class="mb-5 flex flex-col"
      :style="$q.screen.gt.sm ? 'min-width: 40vw' : 'min-width: 90vw'"
      @submit="connect"
    >
      <q-select
        v-model="wifiSsid"
        class="mb-3"
        :label="$t('select_ssid')"
        rounded
        outlined
        :options="ssids"
        option-label="ssid"
      >
        <template #after>
          <q-btn
            class="mt-1"
            round
            dense
            flat
            color="primary"
            icon="refresh"
            :disable="!refreshCompatible"
            @click="fetchNetworks()"
          />
          <q-tooltip
            v-if="!refreshCompatible"
            class="text-caption text-center"
            anchor="top middle"
            self="center middle"
            :offset="[20, 20]"
          >
            {{ $t('refresh_not_compatible') }}
          </q-tooltip>
        </template>
      </q-select>
      <q-input
        v-if="wifiSsid && wifiSsid.security.toLowerCase() === 'hidden'"
        v-model="hiddenNetworkName"
        class="mb-3"
        filled
        :label="$t('network_name')"
      />
      <q-select
        v-if="wifiSsid && wifiSsid.security.toLowerCase() === 'hidden'"
        v-model="hiddenSecurity"
        class="mb-3"
        rounded
        outlined
        :label="$t('security')"
        :options="securityOptions"
      />
      <q-input
        v-if="wifiSsid && (wifiSsid.security.toLowerCase() === 'enterprise' || hiddenSecurity.toLowerCase() === 'enterprise')"
        v-model="username"
        class="mb-3"
        filled
        :label="$t('username')"
      />
      <q-input
        v-model="password"
        filled
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
        class="mt-3"
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

    const hiddenNetworkName = ref<any>('')
    const hiddenSecurity = ref<any>('')
    const hostname = ref<any>(window.location.hostname)
    const password = ref<string>('')
    const refreshCompatible = ref<boolean>(false)
    const ssids = ref<any>([])
    const submitting = ref<boolean>(false)
    const username = ref<string>('')
    const wifiSsid = ref<any>('')

    onMounted(() => {
      fetchNetworks()
    })

    // Send connect request
    function connect () {
      submitting.value = true
      Axios.post(`http://${hostname.value}:9090/v1/wifi/connect`, {
        hiddenNetworkName: hiddenNetworkName.value,
        hiddenSecurity: hiddenSecurity.value,
        passphrase: password.value,
        ssid: wifiSsid.value.ssid,
        type: wifiSsid.value.security,
        username: username.value
      }).catch(function (error) {
        // Only return an error if the request failed to send
        // A timeout is expected as the device is connecting to new network
        if (error.response && !error.request) {
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
        }
      })
      wifiSsid.value = ''
      username.value = ''
      password.value = ''

      // Delay to improve interface interaction
      setTimeout(() => {
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
        submitting.value = false
      }, 2000)
    }

    async function fetchNetworks () {
      $q.loading.show()
      await Axios.get(`http://${hostname.value}:9090/v1/wifi/list_access_points`).then((response) => {
        refreshCompatible.value = response.data.compatible
        ssids.value = response.data.ssids
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
        ssids.value.push({
          ssid: t('enter_hidden_network'),
          security: 'HIDDEN'
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
          message: t('network_fetch_fail')
        })
      })
      submitting.value = false
      $q.loading.hide()
    }

    return {
      connect,
      fetchNetworks,
      hiddenNetworkName,
      hiddenSecurity,
      password,
      refreshCompatible,
      securityOptions: [
        'OPEN', 'ENTERPRISE', 'WEP/WPA/WPA2'
      ],
      ssids,
      submitting,
      username,
      wifiSsid
    }
  }
})

</script>

<style scoped>

</style>
