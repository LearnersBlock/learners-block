<template>
  <div id="q-app row items-center justify-evenly">
    <router-view v-if="apiIsUp" />
    <div
      v-else
      class="text-h2 q-mt-xl q-ml-xl"
    >
      {{ $t('under_maintenance') }}
    </div>
  </div>
</template>
<script lang="ts">
import { useQuery } from '@vue/apollo-composable'
import { defineComponent, ref } from '@vue/composition-api'
import { GET_RESOURCES } from './gql/resource/queries'

export default defineComponent({
  name: 'App',
  setup () {
    const apiIsUp = ref<boolean>(true)
    const { onError } = useQuery(GET_RESOURCES)

    onError(() => {
      setTimeout(() => {
        apiIsUp.value = false
      }, 1000)
    })
    return {
      apiIsUp
    }
  }
})
</script>
