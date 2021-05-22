import { boot } from 'quasar/wrappers'
import { DefaultApolloClient } from '@vue/apollo-composable'
import fetch from 'node-fetch'
import { provide } from '@vue/composition-api'
import { ApolloClient, createHttpLink, InMemoryCache } from '@apollo/client/core'

const httpLink = createHttpLink({
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment
  uri: 'https://library-api.learnersblock.org/graphql', fetch
})

// Create the apollo client
export const apolloClient = new ApolloClient({
  link: httpLink,
  cache: new InMemoryCache({ addTypename: false }),
  connectToDevTools: true
})

// "async" is optional;
// more info on params: https://quasar.dev/quasar-cli/boot-files
export default boot(({ app }) => {
  app.setup = () => {
    provide(DefaultApolloClient, apolloClient)
    return {}
  }
})
