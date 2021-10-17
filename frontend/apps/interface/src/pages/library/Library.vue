<template>
  <q-page class="row items-center justify-evenly mt-3">
    <div
      v-if="!apiIsUp"
      class="text-h3"
    >
      {{ $t('under_maintenance') }}
    </div>
    <div
      v-else-if="fetchResourcesLoading || (fetchedResources.length == 0 && endOfResults == false)"
    >
      <q-spinner
        color="primary"
        size="6em"
      />
    </div>
    <div
      v-else-if="fetchedResources && !fetchResourcesLoading"
      class="resource_container"
    >
      <q-btn
        class="q-mb-md text-subtitle2 text-weight-bold"
        rounded
        outline
        color="white"
        size="sm"
        text-color="primary"
        :label="$t('settings')"
        icon="arrow_back"
        :to="{ name: 'settings' }"
      />
      <div
        v-if="fetchedResources.resources == '' && !fetchResourcesLoading"
        class="text-h3 text-center text-grey"
      >
        {{ $t('no_results_found') }}
      </div>
      <div
        v-else-if="fetchedResources.resources && !fetchResourcesLoading"
      >
        <q-infinite-scroll
          :offset="4000"
          @load="loadMore"
        >
          <router-link
            v-for="resource in fetchedResources.resources"
            :key="resource.id"
            class="resource q-mb-md items-center text-black"
            tag="div"
            :to="'/library/resource/' + resource.id"
          >
            <div v-if="resource">
              <q-badge
                v-for="license in resource.licenses"
                :key="license.id"
                class="q-mt-sm q-mr-sm text-body2"
                color="secondary"
                floating
                rounded
                transparent
                multi-line
              >
                {{ $t(license.license.toLowerCase()) }}
              </q-badge>
            </div>
            <div class="col-2">
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
                  :src="resource.logo ? 'https://library-api.learnersblock.org' + resource.logo.url : require('../../assets/default.jpg')"
                >
              </div>
            </div>
            <div class="col">
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
                      v-for="language in resource.languages"
                      :key="language.id"
                      class="q-pa-sm q-mr-sm q-mt-sm multi-line text-body2 text-weight-large"
                      color="secondary"
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
            v-if="!endOfResults"
            #loading
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
    </div>
  </q-page>
</template>

<script lang="ts">
/* eslint-disable vue/require-default-prop */
import { useQuery } from '@vue/apollo-composable'
import { GET_RESOURCES } from '../../gql/resource/queries'
import { defineComponent, onMounted, ref } from 'vue'
import { useStore } from '../../store'

export default defineComponent({
  name: 'Library',
  setup () {
    // Import required features
    const apiIsUp = ref<boolean>(true)
    const $store = useStore() as any

    // Constants for resource fetching
    const endOfResults = ref<boolean>(false)
    const numberOfResults = ref<number>(40)

    // Fetch resources query
    const {
      result: fetchedResources,
      loading: fetchResourcesLoading,
      refetch: fetchResources,
      onError: apiError
    } = useQuery(GET_RESOURCES, { limit: numberOfResults.value })

    apiError(() => {
      apiIsUp.value = false
    })

    // On mount, enable loading and fetch resources
    onMounted(() => {
      if ($store.state.savedResources.resources) {
        $store.state.savedResources.limit = $store.state.savedResources.resources.resources.length
        fetchedResources.value = $store.state.savedResources.resources
      } else {
        $store.commit('savedResources/resourceLimit', numberOfResults.value)
        $store.commit('savedResources/updateResources', fetchedResources)
      }
    })

    // Enable loading and filter resources according to all inputs
    async function fetchFilteredResources () {
      await fetchResources(
        { limit: $store.state.savedResources.limit })
      $store.commit('savedResources/updateResources', fetchedResources)
      endOfResults.value = false
    }

    // Load more resources when reaching bottom of results
    async function loadMore (_index, done) {
      if (endOfResults.value) {
        setTimeout(() => {
          if (done) {
            done()
          }
        }, 2000)
      } else if ($store.state.savedResources.limit > $store.state.savedResources.resources.resources.length) {
        endOfResults.value = true
        if (done) {
          done()
        }
      } else {
        $store.commit('savedResources/resourceLimit', parseInt($store.state.savedResources.limit) + numberOfResults.value)
        await fetchFilteredResources()
        if (done) {
          done()
        }
      }
    }

    return {
      apiIsUp,
      endOfResults,
      fetchedResources,
      fetchResourcesLoading,
      loadMore
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
    top: 2rem;
    width: 90%;
  }
}
</style>
