<template>
  <!-- Using explicit true/false to display nothing when value is empty -->
  <!-- It avoids pages flashing while making a decision on loading state -->
  <router-view
    v-if="apiIsReady == true"
    class="row items-center justify-evenly"
  />
  <div
    v-else-if="apiIsReady == false"
    class="text-gray-600 text-h5 q-mt-xl text-center"
  >
    <div class="m-3">
      <div class="text-center">
        <q-img src="./assets/lb-logo.svg" style="max-width: 175px" />
      </div>
      <div class="text-center mt-3">
        {{ errorMessage }}
      </div>
      <div v-if="loadingSpinner" class="flex justify-center mt-5">
        <q-spinner-clock color="primary" size="2em" />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { AxiosOverride } from 'src/boot/axios'
import { useQuasar } from 'quasar'
import { defineComponent, ref } from 'vue'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  setup() {
    // Import required features
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()
    const $q = useQuasar()

    const apiIsReady = ref<boolean>()
    const apiPath = ref<string>(
      'http://' + window.location.hostname + ':9090/v1/supervisor/state'
    )
    const errorMessage = ref<string>(t('api_unavailable'))
    const loadingSpinner = ref<boolean>(true)
    // If on the captive portal, the check is skipped to allow welcome message to display
    if (!window.location.pathname.includes('captive_portal')) {
      // Check the state of the device to decide on page to display
      AxiosOverride.get(apiPath.value, { timeout: 2000 })
        .then(function (response) {
          if (response.data.message === true) {
            apiIsReady.value = true
          } else {
            void waitApi()
          }
        })
        .catch(function () {
          void waitApi()
        })
    } else {
      apiIsReady.value = true
    }

    // Function for calling delays throughout
    function delay(ms: number) {
      return new Promise((resolve) => setTimeout(resolve, ms))
    }

    // Loop for rechecking when the API is ready
    async function waitApi() {
      const redirecting = ref<boolean>(false)
      // Show message indicating the page will auto-reload
      apiIsReady.value = false
      // Loop x number of times checking for the device to be ready
      for (let i = 0; i < 10; i++) {
        await delay(5000)
        const xhr = new XMLHttpRequest()
        xhr.open('GET', apiPath.value)
        xhr.timeout = 2000
        xhr.onreadystatechange = async function () {
          if (xhr.readyState === XMLHttpRequest.DONE) {
            // If successful status code
            if (xhr.status === 0 || (xhr.status >= 200 && xhr.status < 400)) {
              // If the API response returns true to indicate api is ready
              if (JSON.parse(xhr.responseText).message) {
                redirecting.value = true
                // A short delay to allow the device to settle
                await delay(3000)
                // Reload the page
                apiIsReady.value = true
              }
            }
          }
        }

        // Send another request if not already redirecting
        if (!redirecting.value) {
          xhr.send()
        } else {
          return
        }
      }
      // If no success after x loops, display a different error
      errorMessage.value = t('api_down')
      loadingSpinner.value = false
      $q.notify({
        type: 'negative',
        message: `${t('error')} API is down or device state is False.`
      })

      // Try the original route eventually to avoid a bug prevnting complete access
      await delay(30000)
      apiIsReady.value = true
    }

    return {
      apiIsReady,
      errorMessage,
      loadingSpinner
    }
  }
})
</script>

<style lang="scss"></style>
