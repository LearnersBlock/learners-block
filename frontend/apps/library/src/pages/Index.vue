<template ref="indexPage">
  <q-page class="row items-center justify-evenly">
    <div v-if="!apiIsUp">
      {{ $t('under_maintenance') }}
    </div>
    <div
      v-if="fetchedResources && !fetchResourcesLoading"
      class="resource_container"
    >
      <q-btn
        v-if="onDevice"
        @click="redirect"
        rounded
        outline
        color="white"
        text-color="primary"
        class="q-mb-md text-subtitle2 text-weight-bold"
      >
        <span class="material-icons">
          arrow_back_ios
        </span>
        <div>
          {{ $t('settings') }}
        </div>
      </q-btn>
      <div
        v-if="fetchedResources.resources"
      >
        <q-infinite-scroll
          @load="loadMore"
          :offset="2000"
        >
          <router-link
            class="resource q-mb-md items-center text-black"
            tag="div"
            :to="'/resource/' + resource.id"
            v-for="resource in filteredResources"
            :key="resource.id"
          >
            <div v-if="resource.logo && resource.logo.formats && resource.logo.formats.thumbnail && resource.logo.formats.thumbnail.url">
              <q-img
                :src="'https://library-api.learnersblock.org' + resource.logo.formats.thumbnail.url"
                loading="lazy"
                spinner-color="grey"
                class="resource_image"
              />
            </div>
            <div v-else>
              <img
                class="resource_image"
                :src="resource.logo ? 'https://library-api.learnersblock.org' + resource.logo.url : require('../assets/default.jpg')"
              >
            </div>
            <div class="resource_info">
              <div
                class="text-h4 resource_name"
                dir="auto"
              >
                {{ resource.name }}
              </div>
              <div
                class="text-body1"
                dir="auto"
              >
                {{ resource.description }}
              </div>
              <div class="resource_languages">
                <div>
                  <q-badge
                    class="q-pa-sm q-mr-sm q-mt-md multi-line text-body2 text-weight-large"
                    color="secondary"
                    v-for="language in resource.languages"
                    :key="language.id"
                  >
                    {{ $t(language.language) }}
                  </q-badge>
                </div>
              </div>
              <div class="column resource_size text-center q-mb-xs">
                <div
                  v-if="resource.size"
                  class="col"
                >
                  {{ $t('size') }} {{ resource.size }} GB
                </div>
                <div
                  v-if="resource.download_url"
                  style="line-height: 0px;"
                >
                  <q-badge color="secondary">
                    {{ $t('direct_download') }}
                  </q-badge>
                </div>
              </div>
            </div>
          </router-link>
          <div
            v-if="endOfResults"
            class="text-h3 text-center text-grey q-mt-lg"
          >
            <q-icon
              name="done_outline"
              class="q-mb-lg"
            />
          </div>
          <template
            #loading
            v-if="!endOfResults"
          >
            <div class="row justify-center q-my-md q-mb-xl">
              <q-spinner-dots
                color="primary"
                size="60px"
              />
            </div>
          </template>
        </q-infinite-scroll>
      </div>
      <div
        v-if="fetchedResources.resources == '' && !fetchResourcesLoading"
        class="text-h3 text-center text-grey"
      >
        {{ $t('no_results_found') }}
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
/* eslint-disable vue/require-default-prop */
import { useQuery } from '@vue/apollo-composable'
import { GET_RESOURCES } from '../gql/resource/queries'
import { computed, defineComponent, inject, onMounted, ref } from 'vue'
import { useStore } from 'vuex'

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
    // Import required features
    const apiIsUp = ref<boolean>(true)
    const { onError } = useQuery(GET_RESOURCES, { limit: 1 })
    const $store = useStore()

    // Direct download boolean from MainLayout
    const directDownload = ref<any>(inject('direct-download'))

    // Constants for resource fetching
    const endOfResults = ref<boolean>(false)
    const numberOfResults = ref<number>(40)

    onError(() => {
      apiIsUp.value = false
    })
    // Read envs for page state
    const onDevice = ref<any>(process.env.ONDEVICE)
    // Fetch resources query
    const {
      result: fetchedResources,
      loading: fetchResourcesLoading,
      refetch: fetchResources
    } = useQuery(GET_RESOURCES, { limit: numberOfResults.value }) as any

    // On mount, enable loading and fetch resources
    onMounted(async () => {
      if ($store.state.savedResources.resources) {
        $store.state.savedResources.limit = $store.state.savedResources.resources.resources.length
        fetchedResources.value = $store.state.savedResources.resources
      } else {
        $store.commit('savedResources/resourceLimit', numberOfResults.value)
        await $store.commit('savedResources/updateResources', fetchedResources)
      }
    })

    // Enable loading and filter resources according to all inputs
    const fetchFilteredResources = async (
      keyword: string = props.keyword!,
      formats: string[] = props.formats! as string[],
      languages: string[] = props.languages as string[],
      tags: string[] = props.tags as string[],
      levels: string[] = props.levels as string[]) => {
      await fetchResources(
        {
          keyword,
          languages,
          formats,
          tags,
          levels,
          limit: $store.state.savedResources.limit
        } as any)
      $store.commit('savedResources/updateResources', fetchedResources)
      endOfResults.value = false
    }

    const filteredResources = computed(() => {
      if (directDownload.value) {
        return fetchedResources.value.resources.filter(resource => resource.download_url)
      } else {
        return fetchedResources.value.resources
      }
    })

    // Load more resources when reaching bottom of results
    async function loadMore (_index, done) {
      if (endOfResults.value) {
        setTimeout(() => {
          done()
        }, 2000)
      } else if ($store.state.savedResources.limit > $store.state.savedResources.resources.resources.length) {
        endOfResults.value = true
        done()
      } else {
        $store.commit('savedResources/resourceLimit', $store.state.savedResources.limit + numberOfResults.value)
        await fetchFilteredResources()
        done()
      }
    }

    function redirect () {
      location.href = '/settings'
    }

    return {
      apiIsUp,
      directDownload,
      endOfResults,
      fetchedResources,
      fetchFilteredResources,
      fetchResourcesLoading,
      filteredResources,
      loadMore,
      onDevice,
      redirect
    }
  }
})
</script>

<style scoped lang="scss">
.resource {
  box-shadow: 0 .3rem 1rem .1rem rgba(0,0,0,.2);
  padding: 2rem;
  display: flex;
  position: relative;
  cursor: pointer;
  border-radius: .3rem;
  transition: all .15s ease-in-out;
  text-decoration: none;
  @media only screen and (max-width: 960px) {
    flex-direction: column;
    text-align: center;
  }

  &:hover {
    box-shadow: 0 .3rem 1rem .1rem rgba(0,0,0,.3);
    transform: translateY(-.1rem);
  }

  &_image {
    margin-right: 2.5rem;
    width: 8rem;
     @media only screen and (max-width: 960px) {
       margin: auto;
       margin-right: 0;
       width: 10rem;
       height: auto;
       margin-bottom: 1.5rem;

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

  &_size {
    position: absolute;
    right: 2.25rem;
    bottom: .1rem;
    @media only screen and (max-width: 960px) {
      position: relative;
      right: .3rem;
      margin-top: 1.5rem;
    }
    @media only screen and (max-width: 800px) {
      position: relative;
      right: .3rem;
      margin-top: 1rem;
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
    width: 90%;
  }
}
</style>
