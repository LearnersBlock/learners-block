import gql from 'graphql-tag'

export const GET_TAGS = gql`
  query tags{
      tags(sort: "published_at:asc") {
          id
          tag
      }
  }
`
