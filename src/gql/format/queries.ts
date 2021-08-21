import gql from 'graphql-tag'

export const GET_FORMATS = gql`
  query formats{
      formats(where: { 
          resources: { name_contains: null }
        }, sort: "type:asc") {
          id
          type
      }
  }
`
