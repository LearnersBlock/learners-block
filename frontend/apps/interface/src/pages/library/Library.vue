<template>
  <q-page
    class="mt-3 row justify-evenly"
    style="min-width: 70vw"
  >
    <div
      v-if="filteredResources && !fetchResourcesLoading"
      class="resource_container q-mb-md"
    >
      <div class="flex row">
        <div
          class="col"
        >
          <q-btn
            class="q-mt-sm q-mb-md text-weight-bold"
            rounded
            outline
            no-wrap
            color="white"
            size="sm"
            text-color="primary"
            :label="$t('settings')"
            icon="arrow_back"
            :to="{ name: 'settings' }"
          />
        </div>
        <div
          v-if="searchBox"
          class="col"
        >
          <q-input
            v-model="searchInput"
            class="q-mb-lg"
            dense
            debounce="1500"
            hide-bottom-space
            :label="$t('search')"
          >
            <template #append>
              <q-btn
                icon="close"
                flat
                padding="0"
                class="cursor-pointer"
                @click="searchInput = ''"
              />
            </template>
          </q-input>
        </div>
        <div>
          <q-btn
            v-if="!searchBox"
            class="q-mt-sm"
            icon="search"
            outline
            rounded
            color="white"
            size="sm"
            text-color="primary"
            @click="searchBox = true"
          />
        </div>
      </div>
      <div
        v-if="!filteredResources?.length"
        class="text-h3 text-center text-grey mt-4"
      >
        {{ $t('no_results_found') }}
      </div>
      <router-link
        v-for="resource in filteredResources"
        :key="resource.id"
        class="resource q-mb-md items-center text-black"
        :to="'/library/resource/' + resource.id"
      >
        <div class="col-2">
          <q-img
            :src="resource.logo?.id ? API_URL + '/assets/' + resource.logo.id + '?key=lib-thumbnail' : require('../../assets/default.jpg')"
            loading="lazy"
            spinner-color="grey"
            class="resource_image"
          />
        </div>
        <div class="col">
          <div class="resource_info">
            <div
              class="text-h4 resource_name"
            >
              {{ resource.name }}
            </div>
            <!-- eslint-disable-next-line vue/no-v-html -->
            <span v-html="resource.description" />
            <div class="resource_languages">
              <div>
                <q-badge
                  v-for="language in resource.languages"
                  :key="language.id"
                  class="q-pa-sm q-mr-sm q-mt-sm multi-line text-caption text-weight-large"
                  color="secondary"
                >
                  {{ language.languages_id.language }}
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
            </div>
          </div>
        </div>
      </router-link>
    </div>
    <q-page-sticky
      position="bottom-right"
      :offset="[20, 15]"
    >
      <q-btn
        class="text-weight-bold"
        rounded
        outline
        color="white"
        size="sm"
        text-color="primary"
        icon="keyboard_arrow_up"
        @click="scrollTop()"
      />
    </q-page-sticky>
  </q-page>
</template>

<script lang="ts">
/* eslint-disable camelcase */
import { useQuasar } from 'quasar'
import { useQuery } from '@vue/apollo-composable'
import { GET_RESOURCES } from '../../gql/resource/queries'
import { computed, defineComponent, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useStore } from '../../store'

export default defineComponent({
  name: 'IntLibrary',
  setup () {
    // Apollo interfaces
    interface ApolloResource {
      name: string;
      description: string;
      languages: Array<{ id: any; languages_id: {language: string} }>;
      id: number;
      logo: any;
      resources: any;
      size: any;
    }

    interface ApolloResources {
      resources: ApolloResource[];
    }

    // Import required features
    const $q = useQuasar()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()
    const $store = useStore() as any

    // Constants for resource fetching
    const API_URL = ref(process.env.LIBRARYAPI)
    const searchBox = ref<boolean>(false)
    const searchInput = ref<string>($store.state.searchInput.searchInput as string)

    // Show search box if field is populated
    if (searchInput.value) {
      searchBox.value = true
    }

    // Fetch resources
    const {
      result: fetchedResources,
      loading: fetchResourcesLoading,
      onError: apiError
    } = useQuery<ApolloResources>(GET_RESOURCES)

    // Compute filtered resources for search function
    const filteredResources = computed(() => {
      const filtered = fetchedResources.value?.resources.filter(
        (res) =>
          res.name.toLowerCase().includes(searchInput.value.toLowerCase()) ||
          res.description.toLowerCase().includes(searchInput.value.toLowerCase()) ||
          res.languages.some(({ languages_id }) => languages_id.language.toLowerCase() === searchInput.value.toLowerCase())
      )
      return filtered
    })

    // Display loading indicator on search result change
    watch(() => filteredResources.value, () => {
      // Start loading indicator for better user experience
      $q.loading.show({
        delay: 1 // ms delay before showing indicator
      })

      // Store current search term for use later
      $store.commit('searchInput/searchInput', searchInput.value)

      // Stop loading indicator
      setTimeout(() => {
        $q.loading.hide()
      }, 400) // ms delay before cancelling indicator
    })

    // Error handler for when online API is unavailable
    apiError((e) => {
      console.log(e)
      $q.notify({
        type: 'negative',
        message: t('library_api_down'),
        timeout: 0,
        actions: [
          { label: t('close'), color: 'black', handler: () => { /* ... */ } }
        ]
      })
    })

    function scrollTop () {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }

    return {
      API_URL,
      fetchResourcesLoading,
      filteredResources,
      scrollTop,
      searchBox,
      searchInput
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

  &_image {
    margin-right: 2.5rem;
    width: 8rem;
     @media only screen and (max-width: 960px) {
       margin: auto;
       margin-right: 0;
       width: 7rem;
       height: auto;
       margin-bottom: 1.5rem;
      }
      @media screen and (max-width: 1680px) {
      width: 7rem;
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
