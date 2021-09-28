<template>
  <q-page>
    <div class="flex flex-col items-center">
      <div class="mt-3 row justify-center">
        <img
          alt=""
          width="100"
          src="../assets/lb-logo.svg"
        >
      </div>
      <div class="mt-5 text-4xl text-gray-600 mb-6 text-center ml-2 mr-2">
        {{ $t('welcome_lb') }}
      </div>
      <q-separator />
      <div
        v-if="settingsLoading"
        class="text-2xl text-gray-500 mt-3 text-center ml-1 mr-1"
      >
        {{ $t('loading') }}
      </div>
      <div
        v-else-if="!settings.website && !settings.files && !settings.library && !slides[0]"
        class="text-2xl text-gray-500 mt-3 text-center ml-1 mr-1"
      >
        {{ $t('enable_components_in') }}
      </div>
      <q-list v-else>
        <q-item
          v-if="settings.files"
          class="cursor-pointer py-3"
          :to="{ name: 'filemanager', params: { data: 'fileshare'} }"
        >
          <q-item-section
            side
            middle
          >
            <q-icon
              name="folder"
              color="orange"
            />
          </q-item-section>
          <q-item-section>
            <q-item-label class="josefin text-2xl pr-12">
              {{ $t('files') }}
            </q-item-label>
            <q-item-label class="text-lg text-gray-500">
              {{ $t('files_description') }}
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-separator v-if="settings.files" />
        <q-item
          v-if="settings.library"
          class="cursor-pointer py-3"
          :to="{ name: 'filemanager', params: { data: 'library'} }"
        >
          <q-item-section
            side
            middle
          >
            <q-icon
              name="import_contacts"
              color="green"
            />
          </q-item-section>
          <q-item-section>
            <q-item-label class="josefin text-2xl pr-12">
              {{ $t('library') }}
            </q-item-label>
            <q-item-label class="text-lg text-gray-500">
              {{ $t('library_description') }}
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-separator v-if="settings.library" />
        <q-item
          v-if="settings.website"
          class="cursor-pointer py-3"
          tag="a"
          target="_self"
          href="/website/"
        >
          <q-item-section
            side
            middle
          >
            <q-icon
              name="language"
              color="yellow"
            />
          </q-item-section>
          <q-item-section>
            <q-item-label class="josefin text-2xl pr-12">
              {{ $t('website') }}
            </q-item-label>
            <q-item-label class="text-lg text-gray-500">
              {{ $t('website_description') }}
            </q-item-label>
          </q-item-section>
        </q-item>
        <q-separator v-if="settings.website" />
      </q-list>
      <div v-if="slides[0] && !settingsLoading">
        <q-item-label
          header
          class="text-2xl mt-2"
        >
          {{ $t('app_store') }}
        </q-item-label>
        <div class="q-pl-md q-pr-md q-pb-md">
          <div class="q-gutter-md">
            <q-carousel
              v-model="slide"
              transition-prev="scale"
              transition-next="scale"
              swipeable
              animated
              control-color="primary"
              navigation
              padding
              arrows
              height="200px"
              class="text-plsrimary text-2xl shadow-1 rounded-borders"
            >
              <q-carousel-slide
                v-for="slide in slides"
                :key="slide.name"
                :name="slide.name"
                class="column no-wrap flex-center cursor-pointer"
                @click="redirect('http://' + windowHostname + ':' + slide.ports)"
              >
                <q-img
                  v-if="slide.logo"
                  :src="slide.logo"
                  style="max-width: 56px"
                />
                <q-icon
                  v-else
                  name="apps"
                  size="56px"
                  color="primary"
                />
                <div class="q-mt-md text-center">
                  {{ slide.long_name }}
                </div>
              </q-carousel-slide>
            </q-carousel>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import Axios from 'app/node_modules/axios'
import { useStore } from '../store'
import { useQuasar } from 'quasar'
import { computed, defineComponent, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup () {
    // Import required features
    const $q = useQuasar()
    const $router = useRouter()
    const $store = useStore()

    // Get API from Store
    const api = computed(() => {
      return $store.getters.GET_API
    })

    // App Store
    const appStoreState = Axios.get(`${api.value}/v1/appstore/status`)
    const jsonKey = ref<any>()
    const slide = ref<any>()
    const slides = ref<any>({})
    const windowHostname = ref<string>(window.location.hostname)

    // Settings for the ui
    const settingsState = Axios.get(`${api.value}/v1/settings/get_ui`)
    const settings = ref<any>({})
    const settingsLoading = ref<boolean>(true)

    // Get settings
    onMounted(async () => {
      await apiCallAwait()
      $q.loading.hide()
    })

    async function apiCallAwait () {
      $q.loading.show()
      await Axios.all([settingsState, appStoreState]).then(Axios.spread(function (res1, res2) {
        // Redirect for Learner's Block Start Page
        if (res1.data.start_page === '/') {
          settings.value = res1.data
          populateAppStore(res2)
          settingsLoading.value = false
        } else if (res1.data.start_page.substring(0, 1) === ':') {
          // Redirect for ports
          setTimeout(() => {
            location.href = `http://${window.location.hostname}${res1.data.start_page}`
          }, 2000)
        } else {
          // Redirect for App Store
          for (let i = 0; i < res2.data.length; i++) {
            if (res2.data[i].name === res1.data.start_page) {
              setTimeout(() => {
                const appPort = Object.keys(res2.data[i].ports)
                const forwardUrl = res2.data[i].ports[appPort[0]]
                location.href = `http://${window.location.hostname}:${forwardUrl}`
              }, 2000)
              return
            }
          }
          // Redirect for custom path
          if (res1.data.start_page === 'files') {
            setTimeout(() => {
              $router.push({ name: 'filemanager', params: { data: 'fileshare' } })
            }, 2000)
          } else if (res1.data.start_page === 'library') {
            setTimeout(() => {
              $router.push({ name: 'filemanager', params: { data: 'library' } })
            }, 2000)
          } else if (res1.data.start_page === 'website') {
            setTimeout(() => {
              location.href = '/website/'
            }, 2000)
          } else {
            populateAppStore(res2)
            settingsLoading.value = false
          }
        }
      })).catch(e => {
        console.log(e.message)
      })
    }

    function populateAppStore (res2) {
      // Populate app store data
      let entry = 0
      slides.value = res2
      for (let i = 0; i < res2.data.length; i++) {
        if (res2.data[i].status.toLowerCase() === 'installed' || res2.data[i].status.toLowerCase() === 'update_available') {
          slides.value[entry] = res2.data[i]
          jsonKey.value = Object.keys(res2.data[i].ports)
          slides.value[entry].ports = slides.value[entry].ports[jsonKey.value[0]]

          entry = entry + 1
        }
      }
      if (slides.value[0]) {
        slide.value = slides.value[0].name
      }
    }

    function redirect (path) {
      window.open(path, '_blank')
    }

    return {
      redirect,
      settings,
      settingsLoading,
      slide,
      slides,
      windowHostname
    }
  }
})
</script>

<style scoped>

</style>
