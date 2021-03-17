<template>
  <div id="q-app row items-center justify-evenly">
    <router-view v-if="apiIsUp" />
    <div
      v-else
      class="text-h2 q-mt-xl q-ml-xl text-center"
    >
      {{ $t('api_down') }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from '@vue/composition-api'
import Axios from 'app/node_modules/axios'

export default defineComponent({
  name: 'App',
  setup (_, { root }) {
    const apiIsUp = ref<boolean>(true)
    const api = computed(() => {
      return root.$store.getters.GET_API
    })

    const fetchPing = async () => {
      try {
        await Axios.get(`${api.value}`)
        apiIsUp.value = true
      } catch (e) {
        apiIsUp.value = false
      }
    }

    Axios.interceptors.response.use(function (response) {
      return response
    }, function (error) {
      if (error.response.status === 401) {
        root.$store.dispatch('LOGOUT')
        root.$router.push('/401')
      } else {
        console.log(error.response.status)
        root.$router.push('/' + error.response.status)
      }
      return Promise.reject(error)
    })

    fetchPing()

    return {
      apiIsUp
    }
  }
})
</script>

<style lang="scss">

</style>
