import gql from 'graphql-tag'

export const GET_CATEGORIES = gql`
  query categories{
      categories(where: { 
          resources: { name_contains: null }
        }, sort: "category:asc") {
          id
          category
      }
  }
`
