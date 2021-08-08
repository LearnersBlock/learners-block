<template>
  <q-page class="row items-center justify-evenly q-mb-lg">
    <!-- Loading Spinner -->
    <q-spinner
      color="primary"
      size="10%"
      v-if="fetchResourceLoading"
    />
    <!-- Resource container -->
    <div
      v-if="fetchedResource"
      class="resource_container q-mb-xl"
    >
      <q-item class="back q-mt-md q-mr-sm">
        <q-page-sticky
          position="top-left"
          :offset="[25, 20]"
        >
          <q-btn
            color="white"
            text-color="primary"
            @click="$router.go(-1)"
            rounded
            outline
          >
            <span class="material-icons">
              arrow_back_ios
            </span>
            {{ $t('back') }}
          </q-btn>
        </q-page-sticky>
      </q-item>
      <div v-if="fetchedResource.resource.logo && fetchedResource.resource.logo.formats && fetchedResource.resource.logo.formats.thumbnail && fetchedResource.resource.logo.formats.thumbnail.url">
        <img
          class="resource_image"
          :src="'https://library-api.learnersblock.org' + fetchedResource.resource.logo.formats.thumbnail.url"
        >
      </div>
      <div v-else>
        <img
          class="resource_image"
          :src="fetchedResource.resource.logo ? 'https://library-api.learnersblock.org' + fetchedResource.resource.logo.url : require('../assets/default.jpg')"
        >
      </div>
      <div
        class="text-h2 resource_name"
        dir="auto"
      >
        {{ fetchedResource.resource.name }}
      </div>
      <div
        class="text-body1 q-pa-sm"
        dir="auto"
      >
        {{ fetchedResource.resource.description }}
      </div>
      <q-separator class="q-mt-sm" />
      <div class="resource_info q-mt-md text-left">
        <div class="text-body1 q-mt-sm">
          {{ $t('author') }}
        </div>
        <div
          v-if="fetchedResource.resource.author"
          class="text-body1 q-mt-sm"
        >
          <a
            :href="fetchedResource.resource.author_website"
            target="_blank"
          >{{ fetchedResource.resource.author }}
          </a>
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-body1 q-mt-sm">
          {{ $t('languages') }}
        </div>
        <div
          v-if="fetchedResource.resource.languages && fetchedResource.resource.languages.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="secondary"
            v-for="language in fetchedResource.resource.languages"
            :key="language.id"
          >
            {{ $t(language.language) }}
          </q-badge>
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-body1 q-mt-sm">
          {{ $t('formats') }}
        </div>
        <div
          v-if="fetchedResource.resource.formats && fetchedResource.resource.formats.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="secondary"
            v-for="format in fetchedResource.resource.formats"
            :key="format.id"
          >
            {{ format.type }}
          </q-badge>
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-body1 q-mt-sm">
          {{ $t('size') }}
        </div>
        <div
          v-if="fetchedResource.resource.size"
          class="text-body1 q-mt-sm"
        >
          {{ fetchedResource.resource.size }} GB
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-body1 q-mt-sm">
          {{ $t('host') }}
        </div>
        <div
          v-if="fetchedResource.resource.host"
          class="text-body1 q-mt-sm"
        >
          {{ fetchedResource.resource.host }}
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-body1 q-mt-sm">
          {{ $t('tags') }}
        </div>
        <div
          v-if="fetchedResource.resource.tags && fetchedResource.resource.tags.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="secondary"
            v-for="tag in fetchedResource.resource.tags"
            :key="tag.id"
          >
            {{ tag.tag }}
          </q-badge>
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-body1 q-mt-sm">
          {{ $t('level') }}
        </div>
        <div
          v-if="fetchedResource.resource.levels && fetchedResource.resource.levels.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="secondary"
            v-for="level in fetchedResource.resource.levels"
            :key="level.id"
          >
            {{ level.level }}
          </q-badge>
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-body1 q-mt-sm">
          {{ $t('licenses') }}
        </div>
        <div
          v-if="fetchedResource.resource.licenses && fetchedResource.resource.licenses.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="secondary"
            v-for="license in fetchedResource.resource.licenses"
            :key="license.id"
          >
            {{ license.license }}
          </q-badge>
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
      </div>
      <q-spinner
        color="primary"
        size="3em"
        v-if="!exitLoop"
      />
      <!-- Code for running on Learner's Block -->
      <div v-if="onDevice">
        <q-btn
          v-if="fetchedResource.resource.author_website && !fetchedResource.resource.download_url"
          class="q-mt-lg q-mb-lg"
          glossy
          rounded
          unelevated
          color="primary"
          icon="pageview"
          :label="$t('explore')"
          @click="downloadZip(fetchedResource.resource.author_website)"
        />
        <q-btn
          v-else-if="fetchedResource.resource.download_url"
          class="q-mt-lg q-mb-lg"
          glossy
          rounded
          unelevated
          color="primary"
          icon="download"
          :label="exitLoop ? $t('download'): $t('cancel')"
          @click="downloadFiles(fetchedResource.resource.download_url)"
        />
        <q-btn
          class="q-mt-lg q-ml-sm q-mb-lg"
          v-if="fetchedResource.resource.sample"
          glossy
          rounded
          unelevated
          color="primary"
          icon="visibility"
          :label="$t('sample')"
          @click="viewSample"
        />
        <q-linear-progress
          v-if="!exitLoop"
          size="30px"
          :value="downloadProgress"
          color="primary"
        >
          <div class="absolute-full flex flex-center">
            <q-badge
              class="q-mr-sm text-caption"
              v-if="downloadProgress"
              color="white"
              text-color="black"
              :label="`${Number(downloadProgress).toFixed(2)*100} % `"
            />
            <q-badge
              class="text-caption"
              v-if="downloadProgress"
              color="white"
              text-color="black"
              :label="`${Number(downloadedMb).toFixed(2)} Mb`"
            />
          </div>
        </q-linear-progress>
      </div>
      <div
        v-else
        class="q-mt-lg "
      >
        <q-btn
          v-if="fetchedResource.resource.download_url || fetchedResource.resource.author_website"
          glossy
          unelevated
          @click="downloadZip(fetchedResource.resource.download_url ? fetchedResource.resource.download_url: fetchedResource.resource.author_website)"
          color="primary"
          :icon="fetchedResource.resource.download_url ? 'download': 'pageview'"
          rounded
          :label="fetchedResource.resource.download_url ? $t('download'): $t('explore')"
          :disable-main-btn="!fetchedResource.resource.download_url"
        />
        <q-btn
          class="q-ml-sm"
          v-if="fetchedResource.resource.sample"
          glossy
          rounded
          unelevated
          color="primary"
          icon="visibility"
          :label="$t('sample')"
          @click="viewSample"
        />
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import Axios from 'app/node_modules/axios'
import { useQuasar } from 'quasar'
import { useQuery } from '@vue/apollo-composable'
import { defineComponent, ref } from 'vue'
import { GET_RESOURCE } from 'src/gql/resource/queries'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    const { t } = useI18n()
    const route = useRoute()

    // Fetch resources
    const { result: fetchedResource, loading: fetchResourceLoading } = useQuery(GET_RESOURCE, { id: route.params.id })

    const downloadedMb = ref<any>()
    const downloadProgress = ref<any>()
    const downloadSpeed = ref<any>()
    const downloadTransferred = ref<any>()
    const exitLoop = ref<boolean>(true)
    const hostname = ref<any>(window.location.hostname)
    const onDevice = ref<any>(process.env.ONDEVICE)

    function delay (ms: number) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }

    async function downloadFiles () {
      try {
        if (exitLoop.value === false) {
          Axios.get(`http://${hostname.value}:9090/v1/download/stop`)
          stopDownload()
        } else {
          const position = ref<any>(0)
          const progress = ref<any>('')
          const xhr = new XMLHttpRequest()
          xhr.open('POST', `http://${hostname.value}:9090/v1/download/fetch`)
          xhr.setRequestHeader('Content-Type', 'application/json')
          xhr.send(JSON.stringify({
            download_url: fetchedResource.value.resource.download_url
          }))

          exitLoop.value = false

          while (exitLoop.value === false) {
            const messages = xhr.responseText.split('\n\n')
            messages.slice(position.value, -1).forEach(function (value) {
              if (value) {
                progress.value = JSON.parse(value)
              }
            })

            // Handle errors
            if (progress.value.error) {
              if (progress.value.error === 'Out of disk space') {
                $q.notify({ type: 'negative', message: `${t('error')} - ${t('no_space')}` })
              } else {
                $q.notify({ type: 'negative', message: `${t('error')} - ${progress.value.error}` })
              }
              stopDownload()
              return
            }

            downloadedMb.value = progress.value.mbytes
            downloadProgress.value = progress.value.progress
            position.value = messages.length - 1

            if (xhr.readyState === XMLHttpRequest.DONE) {
              $q.notify({ type: 'positive', message: t('download_complete') })
              stopDownload()
              return
            }
            await delay(1500)
          }
        }
      } catch (e) {
        console.log(e)
        stopDownload()
      }
    }

    const downloadZip = (link) => {
      window.open(link)
    }

    async function stopDownload () {
      exitLoop.value = true
      downloadedMb.value = 0
      downloadProgress.value = 0
    }

    const viewSample = () => {
      window.open(fetchedResource.value.resource.sample)
    }

    return {
      downloadFiles,
      downloadedMb,
      downloadProgress,
      downloadSpeed,
      downloadTransferred,
      downloadZip,
      exitLoop,
      fetchedResource,
      fetchResourceLoading,
      hostname,
      onDevice,
      viewSample
    }
  }
})
</script>

<style scoped lang="scss">
.resource {
    &_image {
        width: 11rem;
        margin-bottom: 1rem;
        @media only screen and (max-width: 1050px) {
            width: 15rem;
      }
    }

    &_info {
        display: grid;
        grid-template-columns: .5fr 1fr;
        @media only screen and (max-width: 900px) {
            text-align: center;
            grid-template-columns: .5fr .5fr;
        }
        @media only screen and (max-width: 650px) {
            text-align: center;
            grid-template-columns: .5fr .5fr;
        }
        @media only screen and (max-width: 525px) {
            text-align: center;
            grid-template-columns: .5fr .5fr;
        }
    }

    &_name {
      @media only screen and (max-width: 1300px) {
        font-size: 3rem;
      }
       @media only screen and (max-width: 1050px) {
        font-size: 2.6rem;
      }
    }

    &_language {
         @media only screen and (max-width: 470px) {
            margin-top: .4rem;
        }
    }

    &_container {
        width: 80%;

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

.visit {
    position: absolute;
    top: 2rem;
    right: 2rem;
}

</style>
