import gql from 'graphql-tag'

export const GET_RESOURCES = gql`
  query resources($keyword: String, $languages: [String], $formats: [String], $subjects: [String], $levels: [String], $categories: [String], $limit: Int){
      resources(
        where: { 
          _or: [{name_contains: $keyword},{description_contains: $keyword}]
          subjects: {id_in: $subjects}
          levels: {id_in: $levels}
          categories: {id_in: $categories}
          languages: {id_in: $languages}
          formats: {id_in: $formats}
        }, sort: "published_at:desc",limit:$limit) {
          id
          name
          download_url
          description
          languages {
            id
            language
          }
          licenses {
            id
            license
          }
          size
          logo {
            formats
            url
          }
      }
  }
`

export const GET_RESOURCE = gql`
  query resource($id: ID!){
      resource(id: $id) {
          id
          name
          description
          author
          author_website
          host
          sample
          formats {
            id
            type
          }
          uid
          download_url
          languages {
            id
            language
          }
          licenses {
            id
            license
          }
          subjects {
            id
            subject
          }
          levels {
            id
            level
          }
          categories {
            id
            category
          }
          size
          logo {
            formats 
            url
          }
      }
  }
`

export const GET_RESOURCES_LENGTH = gql`
  query resourcesConnection {
    resourcesConnection {
      aggregate {
        totalCount
      }
    }
  }
`
