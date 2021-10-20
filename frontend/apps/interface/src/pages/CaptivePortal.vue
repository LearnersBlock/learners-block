<template>
  <div class="m-3">
    <div class="text-center">
      <q-img
        src="../assets/lb-logo.svg"
        style="max-width: 175px"
      />
    </div>
    <div class="text-4xl text-gray-600 text-center mt-2">
      {{ $t('welcome_lb') }}
    </div>
    <div class="text-xl text-center text-gray-500 mt-2">
      <div>
        {{ $t('visit_to_begin') }}
      </div>
      <div class="mt-4 ml-2">
        {{ hostname }}
        <q-icon
          class="cursor-pointer"
          name="content_copy"
          size="sm"
          @click="copyUrl();$q.notify($t('url_copied'));"
        >
          <q-tooltip class="text-caption text-center">
            {{ $t('copy_to_clipboard') }}
          </q-tooltip>
        </q-icon>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import Axios from 'axios'
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
      const fetchedHostName = await Axios.get(`${api.value}/v1/system/hostname`)
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
