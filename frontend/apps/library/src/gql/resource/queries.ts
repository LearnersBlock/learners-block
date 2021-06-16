import gql from 'graphql-tag'

export const GET_RESOURCES = gql`
  query resources($keyword: String, $languages: [String], $formats: [String], $tags: [String], $levels: [String], $limit: Int){
      resources(
        where: { 
          _or: [{name_contains: $keyword},{description_contains: $keyword}]
          tags: {id_in: $tags}
          levels: {id_in: $levels}
          languages: {id_in: $languages}
          formats: {id_in: $formats}
        }, sort: "published_at:desc",limit:$limit) {
          id
          name
          description
          languages {
            id
            language
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
          rsync
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
          tags {
            id
            tag
          }
          levels {
            id
            level
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
