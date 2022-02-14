<template>
  <div class="m-3">
    <div class="text-center">
      <q-img src="../assets/lb-logo.svg" style="max-width: 175px" />
    </div>
    <div class="text-h4 text-gray-600 text-center mt-2">
      {{ $t('welcome_lb') }}
    </div>
    <div v-if="hostname" class="text-body1 text-center text-gray-600 mt-2">
      <div>
        {{ $t('visit_to_begin') }}
      </div>
      <div class="mt-4 ml-2">
        {{ hostname }}
        <q-btn
          icon="content_copy"
          padding="0"
          flat
          size="sm"
          @click="copyUrl()"
        >
          <q-tooltip class="text-caption text-center">
            {{ $t('copy_to_clipboard') }}
          </q-tooltip>
        </q-btn>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Axios from 'axios'
import { copyToClipboard, useQuasar } from 'quasar'
import { useStore } from '../store'
import { computed, defineComponent, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  name: 'IntCaptivePortal',
  setup() {
    // Import required features
    const $q = useQuasar()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()
    const $store = useStore()
    const hostname = ref<string>()
    const api = computed(() => {
      return $store.getters.GET_API
    })

    onMounted(() => {
      void fetchHostname()
    })

    const copyUrl = () => {
      if (hostname.value) {
        void copyToClipboard(hostname.value)
      }
      $q.notify(t('url_copied'))
    }

    const fetchHostname = async () => {
      const fetchedHostName = await Axios.get(
        `${api.value}/v1/supervisor/hostname`
      )
      hostname.value = `http://${fetchedHostName.data.hostname}.local`
    }

    return {
      copyUrl,
      hostname
    }
  }
})
</script>

<style scoped></style>
