import gql from 'graphql-tag'

export const GET_SUBJECTS = gql`
  query subjects{
      subjects(where: { 
          resources: { name_contains: null }
        }, sort: "subject:asc") {
          id
          subject
      }
  }
`
