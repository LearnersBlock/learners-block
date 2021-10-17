import gql from 'graphql-tag'

export const GET_LANGUAGES = gql`
  query languages{
      languages(
        where: { 
          resources: { name_contains: null }
        }, sort: "language:asc") {
          id
          language
      }
  }
`
