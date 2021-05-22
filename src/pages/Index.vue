<template ref="indexPage">
  <q-page class="row items-center justify-evenly">
    <q-spinner
      color="primary"
      size="10%"
      v-if="fetchResourcesLoading"
    />
    <div
      v-if="fetchedResources && !fetchResourcesLoading"
      class="resource_container"
    >
      <q-btn
        v-if="onDevice"
        @click="redirect"
        rounded
        color="white"
        text-color="primary"
        class="ml-3 mt-9 text-subtitle2 text-weight-bold"
      >
        <span class="material-icons mr-1 mb-.5">
          arrow_back_ios
        </span>
        <div class="mt-0.5">
          {{ $t('settings') }}
        </div>
      </q-btn>
      <div
        v-if="fetchedResources.resources"
        class="resource_box q-mt-lg q-mb-xl"
      >
        <router-link
          class="resource q-mt-md items-center"
          tag="div"
          :to="'/resource/' + resource.id"
          v-for="resource in fetchedResources.resources"
          :key="resource.id"
        >
          <div v-if="resource.logo && resource.logo.formats && resource.logo.formats.thumbnail && resource.logo.formats.thumbnail.url">
            <img
              class="resource_image"
              :src="'https://library-api.learnersblock.org' + resource.logo.formats.thumbnail.url"
            >
          </div>
          <div v-else>
            <img
              class="resource_image"
              :src="resource.logo ? 'https://library-api.learnersblock.org' + resource.logo.url : require('../assets/default.jpg')"
            >
          </div>
          <div class="resource_info">
            <div
              dir="auto"
              class="text-h3 resource_name josefin sans"
            >
              {{ resource.name }}
            </div>
            <div
              dir="auto"
              class="text-h6 q-mt-md resource_description"
            >
              {{ resource.description }}
            </div>
            <div class="resource_languages">
              <div>
                <q-badge
                  class="q-pa-sm q-mr-sm q-mt-sm multi-line text-body2 text-weight-large"
                  color="primary"
                  v-for="language in resource.languages"
                  :key="language.id"
                >
                  {{ $t(language.language) }}
                </q-badge>
              </div>
            </div>
            <div
              v-if="resource.size"
              class="text-subtitle1 resource_size"
            >
              {{ $t('size') }}: {{ resource.size }} GB
            </div>
          </div>
        </router-link>
      </div>
      <div
        v-if="fetchedResources.resources == '' && !fetchResourcesLoading"
        class="text-h3 text-center text-grey"
      >
        {{ $t('no_results_found') }}
      </div>
      <div
        v-if="!disableButton"
        class="text-center"
      >
        <q-btn
          v-if="fetchedResources.resources.length && !fetchResourcesLoading && fetchedResourcesLength"
          :disabled="fetchedResources.resources.length >= fetchedResourcesLength.resourcesConnection.aggregate.totalCount"
          color="grey-6"
          @click="loadMore"
          class="resource_button q-mb-xl"
        >
          {{ $t('load_more') }}
        </q-btn>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { useQuery } from '@vue/apollo-composable'
import { defineComponent, onMounted, ref } from '@vue/composition-api'
import { GET_RESOURCES, GET_RESOURCES_LENGTH } from '../gql/resource/queries'
import { Loading } from 'quasar'

export default defineComponent({
  name: 'PageIndex',
  props: {
    formats: {
      type: Array
    },
    tags: {
      type: Array
    },
    levels: {
      type: Array
    },
    keyword: {
      type: String
    },
    languages: {
      type: Array
    }
  },
  setup (props) {
    // Read envs for page state
    const onDevice = ref<any>(process.env.ONDEVICE)
    // Loading boolean in case the api is very fast, the UI still loads for a lil bit - better User Experience
    const limit = ref<number>(250)
    const disableButton = ref<boolean>(true)
    // Fetch resources query
    const {
      result: fetchedResources,
      loading: fetchResourcesLoading,
      refetch: fetchResources
    } = useQuery(GET_RESOURCES, { limit: 250 })

    const {
      result: fetchedResourcesLength,
      loading: fetchResourcesLengthLoading,
      refetch: fetchResourcesLength
    } = useQuery(GET_RESOURCES_LENGTH, {})

    // On mount, enable loading and fetch resources
    onMounted(async () => {
      await fetchResources()
    })

    const loadMore = async () => {
      limit.value = limit.value + 30
      await fetchFilteredResources()
    }

    // Enable loading and filter resources according to all inputs
    const fetchFilteredResources = async (
      keyword:string = props.keyword!,
      formats: string[] = props.formats! as string[],
      languages: string[] = props.languages as string[],
      tags: string[] = props.tags as string[],
      levels: string[] = props.levels as string[]) => {
      Loading.show()
      await fetchResourcesLength(
        {
          keyword,
          languages,
          formats,
          tags,
          levels
        }
      )
      await fetchResources({
        keyword,
        languages,
        formats,
        tags,
        levels,
        limit: limit.value
      } as any)
      Loading.hide()
    }

    function redirect () {
      location.href = '/settings'
    }

    return {
      disableButton,
      fetchedResources,
      fetchFilteredResources,
      fetchResourcesLoading,
      fetchedResourcesLength,
      fetchResourcesLengthLoading,
      limit,
      loadMore,
      onDevice,
      redirect
    }
  }
})
</script>

<style lang="scss" scoped>
.resource {
  box-shadow: 0 .3rem 1rem .1rem rgba(0,0,0,.2);
  padding: 2rem;
  display: flex;
  position: relative;
  cursor: pointer;
  border-radius: .3rem;
  transition: all .15s ease-in-out;
  @media only screen and (max-width: 960px) {
    flex-direction: column;
    text-align: center;
  }

  &:hover {
    box-shadow: 0 .3rem 1rem .1rem rgba(0,0,0,.3);
    transform: translateY(-.1rem);
  }

  &_image {
    height: auto;
    margin-right: 2rem;
    width: 10rem;
     @media only screen and (max-width: 960px) {
       margin: auto;
       width: 10rem;
       height: auto;
       margin-bottom: 2rem;

      }
      @media screen and (max-width: 1680px) {
      width: 10rem;
      height: auto;
      align-self: center;
      }
    }

  &_languages {
    display: flex;
    align-self: flex-start;
     @media only screen and (max-width: 960px) {
      margin-top: 1rem;
      margin: auto;
    }
     @media only screen and (max-width: 600px) {
       flex-direction: column;
       margin: auto;
    }
  }

  &_name {
      @media only screen and (max-width: 800px) {
      font-size: 1.7rem;
    }
  }

   &_description {
      @media only screen and (max-width: 800px) {
      font-size: 1.2rem;
    }
  }

  &_size {
    position: absolute;
    right: 2.25rem;
    bottom: 1.5rem;
    @media only screen and (max-width: 960px) {
      position: relative;
      right: .3rem;
      margin-top: 3rem;
    }
    @media only screen and (max-width: 800px) {
      position: relative;
      right: .3rem;
      margin-top: 3rem;
    }
  }

  &_info {
    display: flex;
    flex-direction: column;
    justify-content: center;

  }

  &_container {
    position: absolute;
    top: 2rem;
    width: 70%;
  }
}
</style>
