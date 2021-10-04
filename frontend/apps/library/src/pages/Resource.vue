<template>
  <q-page class="row justify-evenly q-mb-lg">
    <!-- Loading Spinner -->
    <div
      v-if="fetchResourceLoading"
      class="row items-center"
    >
      <q-spinner
        color="primary"
        size="6em"
      />
    </div>
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
            rounded
            outline
            color="white"
            size="sm"
            text-color="primary"
            :label="$t('back')"
            icon="arrow_back"
            :loading="backButtonLoading"
            @click="backButtonLoading = true, $router.go(-1)"
          />
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
      <div class="q-mt-md text-left text-body1">
        <div
          v-if="fetchedResource.resource.author"
          class="resource_info"
        >
          <div>
            {{ $t('author') }}
          </div>
          <div>
            <a
              :href="fetchedResource.resource.author_website"
              target="_blank"
            >{{ fetchedResource.resource.author }}
            </a>
          </div>
        </div>
        <div
          v-if="fetchedResource.resource.categories && fetchedResource.resource.categories.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('categories') }}
          </div>
          <div>
            <q-badge
              v-for="category in fetchedResource.resource.categories"
              :key="category.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-body2 text-weight-medium"
              color="secondary"
            >
              {{ $t(category.category) }}
            </q-badge>
          </div>
        </div>
        <div
          v-if="fetchedResource.resource.languages && fetchedResource.resource.languages.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('languages') }}
          </div>
          <div>
            <q-badge
              v-for="language in fetchedResource.resource.languages"
              :key="language.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-body2 text-weight-medium"
              color="secondary"
            >
              {{ $t(language.language) }}
            </q-badge>
          </div>
        </div>
        <div
          v-if="fetchedResource.resource.formats && fetchedResource.resource.formats.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('formats') }}
          </div>
          <div>
            <q-badge
              v-for="format in fetchedResource.resource.formats"
              :key="format.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-body2 text-weight-medium"
              color="secondary"
            >
              {{ format.type }}
            </q-badge>
          </div>
        </div>
        <div
          v-if="fetchedResource.resource.size"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('size') }}
          </div>
          <div>
            {{ fetchedResource.resource.size }} GB
          </div>
        </div>
        <div
          v-if="fetchedResource.resource.host"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('host') }}
          </div>
          <div>
            {{ fetchedResource.resource.host }}
          </div>
        </div>
        <div
          v-if="fetchedResource.resource.subjects && fetchedResource.resource.subjects.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('subjects') }}
          </div>
          <div>
            <q-badge
              v-for="subject in fetchedResource.resource.subjects"
              :key="subject.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-body2 text-weight-medium"
              color="secondary"
            >
              {{ subject.subject }}
            </q-badge>
          </div>
        </div>
        <div
          v-if="fetchedResource.resource.levels && fetchedResource.resource.levels.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('level') }}
          </div>
          <div>
            <q-badge
              v-for="level in fetchedResource.resource.levels"
              :key="level.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-body2 text-weight-medium"
              color="secondary"
            >
              {{ level.level }}
            </q-badge>
          </div>
        </div>
        <div
          v-if="fetchedResource.resource.licenses && fetchedResource.resource.licenses.length"
          class="resource_info q-mt-sm"
        >
          <div>
            {{ $t('licenses') }}
          </div>
          <div>
            <q-badge
              v-for="license in fetchedResource.resource.licenses"
              :key="license.id"
              class="q-mr-xs q-mt-xs q-mb-xs multi-line text-body2 text-weight-medium"
              color="secondary"
            >
              {{ license.license }}
            </q-badge>
          </div>
        </div>
      </div>
      <q-spinner
        v-if="!exitLoop"
        color="primary"
        size="3em"
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
          v-if="fetchedResource.resource.sample"
          class="q-mt-lg q-ml-sm q-mb-lg"
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
          :value="downloadProgress/100"
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
      <div
        v-else
        class="q-mt-lg "
      >
        <q-btn
          v-if="fetchedResource.resource.download_url || fetchedResource.resource.author_website"
          glossy
          unelevated
          color="primary"
          :icon="fetchedResource.resource.download_url ? 'download': 'pageview'"
          rounded
          :label="fetchedResource.resource.download_url ? $t('download'): $t('explore')"
          :disable-main-btn="!fetchedResource.resource.download_url"
          @click="downloadZip(fetchedResource.resource.download_url ? fetchedResource.resource.download_url: fetchedResource.resource.author_website)"
        />
        <q-btn
          v-if="fetchedResource.resource.sample"
          class="q-ml-sm"
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
import Axios from 'axios'
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
    // eslint-disable-next-line @typescript-eslint/unbound-method
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
          // Start the download process
          await Axios.post(`http://${hostname.value}:9090/v1/download/fetch`, { download_url: fetchedResource.value.resource.download_url },
            {
              validateStatus: function (status) {
                if (status !== 200) {
                  $q.notify({ type: 'negative', message: t('error') })
                  throw new Error()
                } else {
                  return status === 200
                }
              }
            })

          // Monitor the download process through stream
          const position = ref<any>(0)
          const progress = ref<any>('')
          const xhr = new XMLHttpRequest()
          xhr.open('GET', `http://${hostname.value}:9090/v1/download/stream`)
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
                $q.notify({ type: 'negative', message: `${t('error')} - ${t('no_space')}` })
              } else {
                $q.notify({ type: 'negative', message: `${t('error')} - ${progress.value.error}` })
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

    const downloadZip = (link) => {
      window.open(link)
    }

    function stopDownload () {
      exitLoop.value = true
      downloadedMb.value = 0
      downloadProgress.value = 0
    }

    const viewSample = () => {
      window.open(fetchedResource.value.resource.sample)
    }

    return {
      backButtonLoading: ref(false),
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
