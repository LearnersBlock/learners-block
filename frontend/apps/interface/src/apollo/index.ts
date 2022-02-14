/* eslint-disable @typescript-eslint/no-unused-vars */
import type { ApolloClientOptions } from '@apollo/client/core'
import { createHttpLink, InMemoryCache } from '@apollo/client/core'
import type { BootFileParams } from '@quasar/app'

export /* async */ function getClientOptions(
  /* {app, router, ...} */ options?: Partial<BootFileParams<any>>
) {
  return <ApolloClientOptions<unknown>>Object.assign(
    // General options.
    <ApolloClientOptions<unknown>>{
      link: createHttpLink({
        uri: `${process.env.LIBRARYAPI}/graphql`
      }),

      cache: new InMemoryCache()
    },

    // dev/prod options.
    process.env.DEV
      ? {
          //
        }
      : {},
    process.env.PROD
      ? {
          //
        }
      : {},

    // For ssr mode, when on server.
    process.env.MODE === 'ssr' && process.env.SERVER
      ? {
          ssrMode: true
        }
      : {},
    // For ssr mode, when on client.
    process.env.MODE === 'ssr' && process.env.CLIENT
      ? {
          ssrForceFetchDelay: 100
        }
      : {}
  )
}
