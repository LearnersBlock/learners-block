<template>
  <div>
    <div class="text-4xl text-gray-600 text-center ml-2 mr-2">
      <center class="mb-5">
        <img
          alt=""
          src="../assets/lb-icon.png"
        >
      </center>
      {{ $t('welcome_lb') }}
    </div><br>
    <div class="text-xl text-center text-gray-500 ml-2 mr-2">
      {{ $t('visit_to_begin') }}
      <br><br>
      {{ hostname }}
      <span
        class="material-icons text-h6 mb-1 q-ml-sm cursor-pointer clipboard-sampleUrl"
        @click="copyUrl();$q.notify($t('url_copied'));"
      >
        content_copy
        <q-tooltip class="text-caption text-center">
          {{ $t('copy_to_clipboard') }}
        </q-tooltip>
      </span>
    </div>
  </div>
</template>

<script lang="ts">
import Axios from 'app/node_modules/axios'
import { copyToClipboard } from 'quasar'
import { useStore } from '../store'
import { computed, defineComponent, onMounted, ref } from 'vue'

export default defineComponent({
  setup () {
    // Import required features
    const $store = useStore()
    const hostname = ref<string>('')
    const api = computed(() => {
      return $store.getters.GET_API
    })

    onMounted(() => {
      fetchHostname()
    })

    const copyUrl = () => {
      copyToClipboard(hostname.value)
    }

    const fetchHostname = async () => {
      const fetchedHostName = await Axios.get(`${api.value}/v1/hostname`)
      hostname.value = `http://${fetchedHostName.data.hostname}.local`
    }

    return {
      copyUrl,
      hostname
    }
  }
})
</script>

<style scoped>

</style>
