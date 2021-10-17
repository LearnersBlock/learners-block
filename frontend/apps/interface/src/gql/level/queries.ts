import gql from 'graphql-tag'

export const GET_LEVELS = gql`
  query levels{
      levels(where: { 
          resources: { name_contains: null }
        }, sort: "published_at:asc") {
          id
          level
      }
  }
`
