<template>
  <div>
    <div class="mt-10 text-4xl text-gray-600 text-center ml-2 mr-2">
      {{ $t('welcome_lb') }}
    </div><br>
    <div class="text-xl text-center text-gray-500 ml-2 mr-2">
      {{ $t('visit_hostname') }}
      <br><br>
      http://{{ hostname }}
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, ref } from '@vue/composition-api'
import Axios from 'app/node_modules/axios'

export default defineComponent({
  setup (_, { root }) {
    const hostname = ref<string>('')
    const api = computed(() => {
      return root.$store.getters.GET_API
    })

    const fetchHostname = async () => {
      const fetchedHostName = await Axios.get(`${api.value}/v1/hostname`)
      hostname.value = fetchedHostName.data.hostname
    }

    fetchHostname()

    return {
      hostname
    }
  }
})
</script>

<style scoped>

</style>
