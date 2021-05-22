import gql from 'graphql-tag'

export const GET_LEVELS = gql`
  query levels{
      levels(sort: "published_at:asc") {
          id
          level
      }
  }
`
