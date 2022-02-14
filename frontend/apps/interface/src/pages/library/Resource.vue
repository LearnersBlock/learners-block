<template>
  <q-page class="row justify-evenly q-mb-lg" style="width: 90vw">
    <!-- Loading Spinner -->
    <div v-if="fetchResourceLoading" class="row items-center">
      <q-spinner color="primary" size="6em" />
    </div>
    <!-- Resource container -->
    <div
      v-if="fetchedResource?.resources_by_id"
      class="resource_container q-mt-xl q-mb-xl"
    >
      <div>
        <q-img
          :src="
            fetchedResource.resources_by_id?.logo?.id
              ? API_URL +
                '/assets/' +
                fetchedResource.resources_by_id.logo.id +
                '?key=lib-thumbnail'
              : require('../../assets/default.jpg')
          "
          spinner-color="grey"
          class="resource_image"
        />
      </div>
      <div class="text-h4 mt-5">
        {{ fetchedResource.resources_by_id.name }}
      </div>
      <div class="q-pa-sm">
        <!-- eslint-disable-next-line vue/no-v-html -->
        <span v-html="fetchedResource.resources_by_id.description" />
      </div>
      <q-separator class="q-mt-sm" />
      <div class="q-mt-md text-left">
        <div
          v-if="fetchedResource.resources_by_id.author"
          class="resource_info"
        >
          <div>
            {{ $t('author_colon') }}
          </div>
          <div>
            <a
              :href="fetchedResource.resources_by_id.author_website"
              target="_blank"
              >{{ fetchedResource.resources_by_id.author }}
            </a>
          </div>
        </div>
        <div
          v-if="fetchedResource.resources_by_id.languages?.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('languages') }}
          </div>
          <div>
            <q-badge
              v-for="language in fetchedResource.resources_by_id.languages"
              :key="language.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-caption text-weight-medium"
              multi-line
              color="secondary"
            >
              {{ language.languages_id.language }}
            </q-badge>
          </div>
        </div>
        <div
          v-if="fetchedResource.resources_by_id.formats?.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('formats') }}
          </div>
          <div>
            <q-badge
              v-for="format in fetchedResource.resources_by_id.formats"
              :key="format.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-caption text-weight-medium"
              multi-line
              color="secondary"
            >
              {{ $t(format.formats_id.key) }}
            </q-badge>
          </div>
        </div>
        <div
          v-if="fetchedResource.resources_by_id.size"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('size') }}
          </div>
          <div>{{ fetchedResource.resources_by_id.size }} GB</div>
        </div>
        <div
          v-if="fetchedResource.resources_by_id.subjects?.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('subjects') }}
          </div>
          <div>
            <q-badge
              v-for="subject in fetchedResource.resources_by_id.subjects"
              :key="subject.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-caption text-weight-medium"
              multi-line
              color="secondary"
            >
              {{ $t(subject.subjects_id.key) }}
            </q-badge>
          </div>
        </div>
        <div
          v-if="fetchedResource.resources_by_id.levels?.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('level') }}
          </div>
          <div>
            <q-badge
              v-for="level in fetchedResource.resources_by_id.levels"
              :key="level.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-caption text-weight-medium"
              multi-line
              color="secondary"
            >
              {{ $t(level.levels_id.key) }}
            </q-badge>
          </div>
        </div>
      </div>
      <div class="mt-4 mb-1">
        <q-btn
          class="q-mb-sm text-weight-bold"
          glossy
          rounded
          unelevated
          size="sm"
          color="primary"
          icon="download"
          :label="exitLoop ? $t('download') : $t('cancel')"
          @click="downloadFiles()"
        />
        <q-btn
          v-if="fetchedResource.resources_by_id.sample_url"
          class="q-ml-sm q-mb-sm text-weight-bold"
          glossy
          rounded
          unelevated
          size="sm"
          color="primary"
          icon="visibility"
          :label="$t('sample')"
          @click="viewSample"
        />
      </div>
      <q-linear-progress
        v-if="!exitLoop"
        size="30px"
        :value="downloadProgress / 100"
        color="primary"
      >
        <div class="absolute-full flex flex-center">
          <q-badge
            v-if="downloadProgress"
            class="q-mr-sm text-caption"
            color="white"
            text-color="black"
            :label="`${Number(downloadProgress)} % `"
          />
          <q-badge
            v-if="downloadProgress"
            class="text-caption"
            color="white"
            text-color="black"
            :label="`${Number(downloadedMb)} Mb`"
          />
        </div>
      </q-linear-progress>
    </div>
    <q-page-sticky position="top-left" :offset="[25, 20]">
      <q-btn
        class="text-weight-bold"
        rounded
        outline
        color="white"
        size="sm"
        text-color="primary"
        icon="arrow_back"
        @click="$router.back()"
      />
    </q-page-sticky>
  </q-page>
</template>

<script lang="ts">
/* eslint-disable camelcase */
import Axios from 'axios'
import { useQuasar } from 'quasar'
import { useQuery } from '@vue/apollo-composable'
import { computed, defineComponent, ref } from 'vue'
import { GET_RESOURCE } from '../../gql/resource/queries'
import { useStore } from '../../store'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'

export default defineComponent({
  name: 'IntLibraryResources',
  setup() {
    // Import required features
    const $q = useQuasar()
    const route = useRoute()
    const $store = useStore() as any
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    // Set required constants
    const API_URL = ref(process.env.LIBRARYAPI)
    const downloadedMb = ref<any>()
    const downloadProgress = ref<any>()
    const exitLoop = ref<boolean>(true)

    const api = computed(() => {
      return $store.getters.GET_API
    })

    // Apollo interfaces
    interface ApolloResource {
      author: string
      // eslint-disable-next-line camelcase
      author_website: any
      description: string
      download_url: any
      formats: Array<{ id: any; formats_id: { key: string } }>
      languages: Array<{ id: any; languages_id: { language: string } }>
      levels: Array<{ id: any; levels_id: { key: string } }>
      logo: any
      name: string
      resource: any
      sample_url: string
      size: any
      subjects: Array<{ id: any; subjects_id: { key: string } }>
    }

    interface ApolloResources {
      // eslint-disable-next-line camelcase
      resources_by_id: ApolloResource
    }

    interface ApolloVars {
      id: any
    }

    // Fetch resources
    const { result: fetchedResource, loading: fetchResourceLoading } = useQuery<
      ApolloResources,
      ApolloVars
    >(GET_RESOURCE, { id: route.params.id })

    function delay(ms: number) {
      return new Promise((resolve) => setTimeout(resolve, ms))
    }

    async function downloadFiles() {
      try {
        if (exitLoop.value === false) {
          void Axios.get(`${api.value}/v1/download/stop`)
          stopDownload()
        } else {
          // Start the download process
          await Axios.post(`${api.value}/v1/download/fetch`, {
            download_url: fetchedResource.value?.resources_by_id.download_url
          })

          // Monitor the download process through the stream
          const position = ref<number | undefined>(0)
          const progress = ref<any>('')
          const xhr = new XMLHttpRequest()
          xhr.open('GET', `${api.value}/v1/download/stream`)
          xhr.send()

          exitLoop.value = false

          while (exitLoop.value === false) {
            const messages = xhr.responseText.split('\n\n')
            messages.slice(position.value, -1).forEach(function (value) {
              if (value) {
                progress.value = JSON.parse(value)
              }
            })

            // Handle errors
            if (progress.value.error || xhr.status > 200) {
              if (progress.value.error === 'Out of disk space') {
                $q.notify({
                  type: 'negative',
                  message: `${t('error')} - ${t('no_space')}`
                })
              } else {
                $q.notify({
                  type: 'negative',
                  message: `${t('error')} - ${progress.value.error}`
                })
              }
              stopDownload()
              return
            }

            downloadedMb.value = progress.value.mbytes
            if (progress.value.progress) {
              downloadProgress.value = Number(progress.value.progress)
            } else {
              downloadProgress.value = 0
            }
            position.value = messages.length - 1

            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
              $q.notify({ type: 'positive', message: t('download_complete') })
              stopDownload()
              return
            }
            await delay(1000)
          }
        }
      } catch (e) {
        console.log(e)
        stopDownload()
      }
    }

    function stopDownload() {
      exitLoop.value = true
      downloadedMb.value = 0
      downloadProgress.value = 0
    }

    const viewSample = () => {
      window.open(fetchedResource.value?.resources_by_id.sample_url)
    }

    return {
      API_URL,
      downloadFiles,
      downloadedMb,
      downloadProgress,
      exitLoop,
      fetchedResource,
      fetchResourceLoading,
      viewSample
    }
  }
})
</script>

<style scoped lang="scss">
.resource {
  &_image {
    width: 10rem;
    margin-bottom: 1rem;
    @media only screen and (max-width: 1050px) {
      display: block;
      margin-left: auto;
      margin-right: auto;
      width: 8rem;
    }
  }

  &_info {
    display: grid;
    grid-template-columns: 0.5fr 1fr;
    @media only screen and (max-width: 900px) {
      text-align: center;
      grid-template-columns: 0.5fr 0.5fr;
    }
    @media only screen and (max-width: 650px) {
      text-align: center;
      grid-template-columns: 0.5fr 0.5fr;
    }
    @media only screen and (max-width: 525px) {
      text-align: center;
      grid-template-columns: 0.5fr 0.5fr;
    }
  }

  &_container {
    min-width: 90%;

    @media only screen and (max-width: 900px) {
      width: 70%;
      text-align: center;
    }
    @media only screen and (max-width: 650px) {
      width: 85%;
      text-align: center;
    }
    @media only screen and (max-width: 525px) {
      width: 95%;
      text-align: center;
    }
  }
}
</style>
