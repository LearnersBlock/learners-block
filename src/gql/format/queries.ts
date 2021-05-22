import gql from 'graphql-tag'

export const GET_FORMATS = gql`
  query formats{
      formats(sort: "type:asc") {
          id
          type
      }
  }
`
