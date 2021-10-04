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
import Axios from 'axios'
import { defineComponent, ref } from 'vue'

export default defineComponent({
  name: 'App',
  setup () {
    const apiIsUp = ref<boolean>(true)

    Axios.get('http://' + window.location.hostname + ':9090')
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
