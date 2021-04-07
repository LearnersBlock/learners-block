<template>
    <router-view v-if="apiIsUp" class="row items-center justify-evenly" />
    <div
      v-else
      class="text-h4 q-mt-xl text-center"
    >
      {{ $t('api_down') }}
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue'
import Axios from 'app/node_modules/axios'
import { useStore } from './store'

export default defineComponent({
  name: 'App',
  setup () {
    const $store = useStore()
    const apiIsUp = ref<boolean>(true)
    const api = computed(() => {
      return $store.getters.GET_API
    })

    const fetchPing = async () => {
      try {
        await Axios.get(`${api.value}`)
        apiIsUp.value = true
      } catch (e) {
        apiIsUp.value = false
      }
    }

    fetchPing()

    return {
      apiIsUp
    }
  }
})
</script>

<style lang="scss">

</style>
