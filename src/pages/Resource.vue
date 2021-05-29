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
          :offset="[18, 18]"
        >
          <router-link
            color="secondary"
            class="back text-h6 cursor-pointer"
            tag="div"
            to="/"
          >
            <q-btn
              color="white"
              text-color="primary"
              class="text-subtitle2 text-weight-bold"
            >
              {{ $t('back') }}
            </q-btn>
          </router-link>
        </q-page-sticky>
      </q-item>
      <div v-if="fetchedResource.resource.logo && fetchedResource.resource.logo.formats && fetchedResource.resource.logo.formats.thumbnail && fetchedResource.resource.logo.formats.thumbnail.url">
        <img
          class="resource_image q-mt-xl"
          :src="'https://library-api.learnersblock.org' + fetchedResource.resource.logo.formats.thumbnail.url"
        >
      </div>
      <div v-else>
        <img
          class="resource_image q-mt-xl"
          :src="fetchedResource.resource.logo ? 'https://library-api.learnersblock.org' + fetchedResource.resource.logo.url : require('../assets/default.jpg')"
        >
      </div>
      <div
        dir="auto"
        class="text-h2 josefin sans resource_name"
      >
        {{ fetchedResource.resource.name }}
      </div>
      <div
        dir="auto"
        class="text-h6 q-mt-md resource_description"
      >
        {{ fetchedResource.resource.description }}
      </div>
      <q-separator class="q-mt-md" />
      <div class="resource_info q-mt-lg text-left">
        <div class="text-h6 q-mt-sm resource_info-label">
          {{ $t('author') }}:
        </div>
        <div
          v-if="fetchedResource.resource.author"
          class="text-h6 q-mt-sm"
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
        <div class="text-h6 q-mt-sm resource_info-label">
          {{ $t('languages') }}:
        </div>
        <div
          v-if="fetchedResource.resource.languages && fetchedResource.resource.languages.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="primary"
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
        <div class="text-h6 q-mt-sm resource_info-label">
          {{ $t('formats') }}:
        </div>
        <div
          v-if="fetchedResource.resource.formats && fetchedResource.resource.formats.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="primary"
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
        <div class="text-h6 q-mt-sm resource_info-label">
          {{ $t('size') }}:
        </div>
        <div
          v-if="fetchedResource.resource.size"
          class="text-h6 q-mt-sm"
        >
          {{ fetchedResource.resource.size }} GB
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-h6 q-mt-sm resource_info-label">
          {{ $t('host') }}:
        </div>
        <div
          v-if="fetchedResource.resource.host"
          class="text-h6 q-mt-sm"
        >
          {{ fetchedResource.resource.host }}
        </div>
        <div
          class="q-mt-sm"
          v-else
        >
          {{ '--' }}
        </div>
        <div class="text-h6 q-mt-sm resource_info-label">
          {{ $t('tags') }}:
        </div>
        <div
          v-if="fetchedResource.resource.tags && fetchedResource.resource.tags.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="primary"
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
        <div class="text-h6 q-mt-sm resource_info-label">
          {{ $t('level') }}:
        </div>
        <div
          v-if="fetchedResource.resource.levels && fetchedResource.resource.levels.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="primary"
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
        <div class="text-h6 q-mt-sm resource_info-label">
          {{ $t('licenses') }}:
        </div>
        <div
          v-if="fetchedResource.resource.licenses && fetchedResource.resource.licenses.length"
        >
          <q-badge
            class="q-mt-sm q-pa-sm q-mr-sm q-mb-sm multi-line text-body2 text-weight-medium resource_language"
            color="primary"
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

      <div v-if="onDevice">
        <q-btn
          class="q-mt-lg q-mb-lg"
          glossy
          rounded
          :disable="!fetchedResource.resource.rsync && !fetchedResource.resource.download_url"
          color="primary"
          icon="download"
          :label="exitLoop ? $t('download'): $t('cancel')"
          @click="downloadToBlock"
        />

        <q-tooltip
          v-if="!fetchedResource.resource.rsync && !fetchedResource.resource.download_url"
          anchor="top middle"
          self="center middle"
          :offset="[10, 10]"
          style="font-size: 16px"
        >
          {{ $t('resource_not_available') }}
        </q-tooltip>

        <q-btn
          class="q-mt-lg q-ml-sm q-mb-lg"
          v-if="fetchedResource.resource.sample"
          glossy
          split
          rounded
          color="primary"
          icon="visibility"
          :label="$t('sample')"
          @click="viewSample"
        />
        <q-linear-progress
          v-if="downloadStarted"
          size="25px"
          :value="downloadProgress"
          color="primary"
        >
          <div class="absolute-full flex flex-center">
            <q-badge
              v-if="fetchedResource.resource.rsync && downloadTransferred && downloadSpeed && downloadProgress < 2"
              color="white"
              text-color="black"
              :label="$t('transferred') + ': ' + downloadTransferred + ' - ' + $t('download_speed') + ': ' + downloadSpeed"
            />
            <q-badge
              v-if="!fetchedResource.resource.rsync && downloadProgress < 2"
              color="white"
              text-color="black"
              :label="(downloadProgress*100).toFixed(2) + '% '"
            />
            <q-badge
              v-if="!fetchedResource.resource.rsync && downloadProgress < 2"
              color="white"
              text-color="black"
              :label="(downloadedMb).toFixed(2) + 'Mb'"
            />
            <q-badge
              v-if="downloadProgress == 2"
              color="white"
              text-color="black"
              :label="$t('download_complete')"
            />

            <q-badge
              v-if="checkingFiles"
              color="white"
              text-color="black"
              :label="$t('checking_files')"
            />
          </div>
        </q-linear-progress>
      </div>

      <div
        v-else
        class="q-mt-lg "
      >
        <q-btn-dropdown
          v-if="fetchedResource.resource.download_url || fetchedResource.resource.rsync"
          glossy
          split
          @click="downloadZip"
          color="primary"
          icon="download"
          rounded
          :label="$t('download')"
          :disable-main-btn="!fetchedResource.resource.download_url"
          :disable-dropdown="!fetchedResource.resource.rsync"
        >
          <q-list>
            <q-item
              clickable
              v-close-popup
              @click="copyRsync();$q.notify($t('rsync_url_copied'));"
            >
              <q-item-section>
                <q-item-label>{{ $t('rsync') }}</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
        <q-btn
          class="q-ml-sm"
          v-if="fetchedResource.resource.sample"
          glossy
          split
          rounded
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
import { copyToClipboard, useQuasar } from 'quasar'
import { useQuery } from '@vue/apollo-composable'
import { defineComponent, ref } from 'vue'
import { GET_RESOURCE } from 'src/gql/resource/queries'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'

export default defineComponent({
  setup () {
    const $q = useQuasar()
    const { t } = useI18n()
    const route = useRoute()
    // Fetch resources
    const { result: fetchedResource, loading: fetchResourceLoading } = useQuery(GET_RESOURCE, { id: route.params.id })

    // Fetch RSync hostname status
    const checkingFiles = ref<boolean>(false)
    const downloadedMb = ref<number>()
    const downloadProgress = ref<any>()
    const downloadStarted = ref<boolean>(false)
    const downloadSpeed = ref<any>()
    const downloadTransferred = ref<any>()
    const exitLoop = ref<boolean>(true)
    const hostname = ref<any>(window.location.hostname)
    const onDevice = ref<any>(process.env.ONDEVICE)

    // Bottom button functions
    const viewSample = () => {
      window.open(fetchedResource.value.resource.sample)
    }

    function delay (ms: number) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }

    const downloadZip = () => {
      window.open(fetchedResource.value.resource.download_url)
    }

    async function stopDownload () {
      exitLoop.value = true
      checkingFiles.value = false
      downloadSpeed.value = 0
      downloadTransferred.value = 0
      await delay(1500)
      downloadProgress.value = 2
    }

    async function downloadFiles () {
      try {
        if (exitLoop.value === false) {
          Axios.get(`http://${hostname.value}:9090/v1/download/stop`)
          stopDownload()
        } else {
          Axios.post(`http://${hostname.value}:9090/v1/download/fetch`, { download_url: fetchedResource.value.resource.download_url })
          exitLoop.value = false
          while (exitLoop.value === false) {
            await delay(1500)
            const response = await Axios.get(`http://${hostname.value}:9090/v1/download/status`)

            if (response.data.progress === 'space-error') {
              $q.notify({ type: 'negative', message: t('no_space') })
              stopDownload()
              return
            } else if (response.data.progress === 'error') {
              $q.notify({ type: 'negative', message: t('error') })
              stopDownload()
              return
            } else if (response.data.progress === 1) {
              $q.notify({ type: 'positive', message: t('download_complete') })
              downloadProgress.value = 2
              stopDownload()
              return
            } else {
              checkingFiles.value = false
              downloadProgress.value = response.data.progress
              downloadedMb.value = response.data.MBytes
            }
          }
        }
      } catch (e) {
        stopDownload()
      }
    }

    async function rsyncFiles () {
      try {
        if (exitLoop.value === false) {
          Axios.get(`http://${hostname.value}:9090/v1/rsync/stop`)
          stopDownload()
        } else {
          Axios.post(`http://${hostname.value}:9090/v1/rsync/fetch`, { rsync_url: fetchedResource.value.resource.rsync })
          exitLoop.value = false
          while (exitLoop.value === false) {
            await delay(1500)
            const response = await Axios.get(`http://${hostname.value}:9090/v1/rsync/status`)
            if (response.data.progress === 'space-error') {
              $q.notify({ type: 'negative', message: t('no_space') })
              stopDownload()
              return
            } else if (response.data.progress === 'error') {
              stopDownload()
              downloadFiles()
              return
            } else if (response.data.progress === 'checking-files') {
              checkingFiles.value = true
            } else if (response.data.progress === 'complete') {
              $q.notify({ type: 'positive', message: t('download_complete') })
              downloadProgress.value = 2
              stopDownload()
              return
            } else {
              checkingFiles.value = false
              downloadProgress.value = response.data.progress
              downloadSpeed.value = response.data.speed
              downloadTransferred.value = response.data.transferred
            }
          }
        }
      } catch (e) {
        stopDownload()
      }
    }

    const downloadToBlock = async () => {
      downloadStarted.value = true
      if (fetchedResource.value.resource.rsync) {
        rsyncFiles()
      } else {
        downloadFiles()
      }
    }

    const copyRsync = () => {
      copyToClipboard(fetchedResource.value.resource.rsync)
    }

    return {
      checkingFiles,
      copyRsync,
      downloadedMb,
      downloadProgress,
      downloadSpeed,
      downloadStarted,
      downloadToBlock,
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
        width: 15rem;
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

      &-label {
         @media only screen and (max-width: 470px) {
            font-size: 1.2rem;
        }
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

    &_description {
      @media only screen and (max-width: 1300px) {
        font-size: 1.2rem;
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
