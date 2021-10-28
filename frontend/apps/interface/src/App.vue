<template>
  <router-view
    v-if="apiIsUp"
    class="row items-center justify-evenly"
  />
  <div
    v-else
    class="text-h4 q-mt-xl text-center"
  >
    {{ $t('api_down') }}
  </div>
</template>

<script lang="ts">
import { AxiosOverride } from 'src/boot/axios'
import { defineComponent, ref } from 'vue'

export default defineComponent({
  setup () {
    const apiIsUp = ref<boolean>(true)

    AxiosOverride.get('http://' + window.location.hostname + ':9090', { timeout: 4000 })
      .catch(function (error) {
        apiIsUp.value = false
        console.log(error)
      })

    return {
      apiIsUp
    }
  }
})
</script>

<style lang="scss">

</style>
