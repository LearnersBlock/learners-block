<template>
  <router-view />
</template>
<script lang="ts">
import { ApolloClients } from '@vue/apollo-composable'
import { apolloClients } from 'src/extensions/apollo/boot'
import { defineComponent, provide } from 'vue'

export default defineComponent({
  name: 'App',
  setup () {
    provide(ApolloClients, apolloClients)
  }
})
</script>
