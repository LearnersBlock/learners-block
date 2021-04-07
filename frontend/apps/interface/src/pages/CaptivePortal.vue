<template>
  <div>
    <div class="mt-10 text-4xl text-gray-600 text-center ml-2 mr-2">
      {{ $t('welcome_lb') }}
    </div><br>
    <div class="text-xl text-center text-gray-500 ml-2 mr-2">
      {{ $t('visit_to_begin') }}
      <br><br>
      http://{{ hostname }}.local
      <span
        @click="copyUrl();$q.notify($t('url_copied'));"
        class="material-icons text-h6 mb-1 q-ml-sm cursor-pointer clipboard-sampleUrl"
      >
        content_copy
        <q-tooltip>
          <span class="text-subtitle1">Copy to clipboard</span>
        </q-tooltip>
      </span>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from 'vue'
import Axios from 'app/node_modules/axios'
import { copyToClipboard } from 'quasar'
import { useStore } from '../store'

export default defineComponent({
  setup () {
    const $store = useStore()
    const hostname = ref<string>('')
    const api = computed(() => {
      return $store.getters.GET_API
    })

    const copyUrl = () => {
      copyToClipboard('http://' + hostname.value + '.local')
    }

    const fetchHostname = async () => {
      const fetchedHostName = await Axios.get(`${api.value}/v1/hostname`)
      hostname.value = fetchedHostName.data.hostname
    }

    fetchHostname()

    return {
      copyUrl,
      hostname
    }
  }
})
</script>

<style scoped>

</style>
