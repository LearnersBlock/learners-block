import gql from 'graphql-tag'

export const GET_RESOURCES = gql`
query resources {
  resources(filter: { download_url: { _nempty: true } }, sort: ["name"], limit: -1) {
    id
    name
    description
    languages {
      id
      languages_id {
        language
      }
    }
    size
    logo {
      id
    }
  }
}
`

export const GET_RESOURCE = gql`
query resources($id: ID!) {
  resources_by_id(id: $id) {
    id
    name
    description
    author
    author_website
    sample_url
    formats {
      id
      formats_id {
        key
      }
    }
    download_url
    languages {
      id
      languages_id {
        language
      }
    }
    subjects {
      id
      subjects_id {
        key
      }
    }
    levels {
      id
      levels_id {
        key
      }
    }
    size
    logo {
      id
    }
  }
}
`
