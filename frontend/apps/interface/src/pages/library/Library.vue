<template>
  <q-page class="mt-3 row justify-evenly">
    <!-- Loading Spinner -->
    <div
      v-if="fetchResourcesLoading"
      class="row items-center"
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
        class="q-mb-md text-weight-bold"
        rounded
        outline
        color="white"
        size="sm"
        text-color="primary"
        :label="$t('settings')"
        icon="arrow_back"
        :to="{ name: 'settings' }"
      />
      <router-link
        v-for="resource in fetchedResources.resources"
        :key="resource.id"
        class="resource q-mb-md items-center text-black"
        tag="div"
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
  </q-page>
</template>

<script lang="ts">
/* eslint-disable camelcase */
import { useQuasar } from 'quasar'
import { useQuery } from '@vue/apollo-composable'
import { GET_RESOURCES } from '../../gql/resource/queries'
import { defineComponent, ref } from 'vue'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    // Constants for resource fetching
    const API_URL = ref(process.env.LIBRARYAPI)

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

    // Fetch resources
    const {
      result: fetchedResources,
      loading: fetchResourcesLoading,
      onError: apiError
    } = useQuery<ApolloResources>(GET_RESOURCES)

    // Error handler for when online API is unavailable
    apiError(() => {
      $q.notify({
        type: 'negative',
        message: t('library_api_down'),
        timeout: 0,
        actions: [
          { label: t('close'), color: 'black', handler: () => { /* ... */ } }
        ]
      })
    })

    return {
      API_URL,
      fetchedResources,
      fetchResourcesLoading
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
