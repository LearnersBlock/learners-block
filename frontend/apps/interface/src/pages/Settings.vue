<template>
  <q-page>
    <div class="flex flex-col items-center">
      <div class="max-w-5xl">
        <div>
          <q-btn
            @click="$router.replace('/')"
            rounded
            color="white"
            text-color="primary"
            class="ml-3 mt-9 text-subtitle2 text-weight-bold"
            outline
          >
            <span class="material-icons mr-1 mb-.5">
              arrow_back_ios
            </span>
            <div class="mt-0.5">
              {{ $t('home') }}
            </div>
          </q-btn>
          <div class="mt-9 pl-3 text-5xl text-gray-600">
            {{ $t('settings') }}
          </div>
          <hr class="mt-3">
          <div class="flex flex-col">
            <q-list>
              <q-item-label
                header
                class="pr-12 text-2xl"
              >
                {{ $t('components') }}
              </q-item-label>

              <div class="text-base ml-4 mb-4 text-gray-600">
                {{ $t('click_toggle') }}
              </div>
              <q-item
                clickable
                v-ripple
                tag="a"
                target="_self"
                href="/upload-files/"
              >
                <q-icon
                  name="folder"
                  color="orange"
                  style="font-size: 2em"
                  class="mr-3"
                />
                <q-item-section>
                  <q-item-label class="josefin text-xl">
                    {{ $t('file_manager') }}
                  </q-item-label>
                  <q-item-label class="text-base pr-1 text-gray-500">
                    {{ $t('files_settings_description') }}
                  </q-item-label>
                </q-item-section>
                <q-toggle
                  v-if="!filesLoading"
                  v-model="files"
                  icon="folder"
                  class="self-end"
                  size="lg"
                  :disable="togglesLoading"
                  @update:model-value="updateFiles"
                />
                <q-spinner
                  v-if="filesLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>

              <q-item
                clickable
                v-ripple
                tag="a"
                target="_self"
                :disable="!internet"
                @click="redirect"
              >
                <q-tooltip
                  v-if="!internet"
                  anchor="top middle"
                  self="center middle"
                  :offset="[10, 10]"
                  class="text-caption text-center"
                >
                  {{ $t('need_connection') }}
                </q-tooltip>
                <q-icon
                  name="import_contacts"
                  color="green"
                  style="font-size: 2em"
                  class="mr-3"
                />
                <q-item-section>
                  <q-item-label class="josefin text-xl">
                    {{ $t('library') }}
                  </q-item-label>
                  <q-item-label class="text-base pr-1 text-gray-500">
                    {{ $t('library_settings_description') }}
                  </q-item-label>
                </q-item-section>
                <q-toggle
                  v-model="library"
                  icon="import_contacts"
                  size="lg"
                  :disable="togglesLoading"
                  v-if="!libraryLoading"
                  @update:model-value="updateLibrary"
                />
                <q-spinner
                  v-if="libraryLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>

              <q-item
                clickable
                v-ripple
                tag="a"
                target="_self"
                href="/upload-website/"
              >
                <q-icon
                  name="language"
                  color="yellow"
                  style="font-size: 2em"
                  class="mr-3"
                />
                <q-item-section>
                  <q-item-label class="josefin text-xl">
                    {{ $t('website') }}
                  </q-item-label>
                  <q-item-label class="text-base pr-1 text-gray-500">
                    {{ $t('website_settings_description') }}
                  </q-item-label>
                </q-item-section>
                <q-toggle
                  v-model="website"
                  icon="language"
                  size="lg"
                  class="ml-auto"
                  :disable="togglesLoading"
                  v-if="!websiteLoading"
                  @update:model-value="updateWebsite"
                />
                <q-spinner
                  v-if="websiteLoading"
                  color="primary"
                  size="2em"
                  class="mt-6 mr-6"
                />
              </q-item>
            </q-list>
            <q-separator spaced />
            <q-item-label
              header
              class="text-2xl"
            >
              {{ $t('login') }}
            </q-item-label>
            <q-btn
              outline
              rounded
              no-caps
              color="primary"
              @click="$router.replace('password_reset')"
              :label="$t('set_password')"
              class="ml-3 mr-3 mb-2 text-lg"
            />
            <q-btn
              outline
              rounded
              no-caps
              color="primary"
              @click="disableLoginWarn"
              :label="$t('disable_password')"
              class="ml-3 mr-3 mb-2 text-lg"
            />
            <q-separator spaced />
            <q-item-label
              header
              class="text-2xl"
            >
              {{ $t('wifi') }}
            </q-item-label>
            <div>
              <div class="text-lg ml-4">
                <div v-if="wifiLoading">
                  {{ $t('status') }} {{ $t('loading') }}
                </div>
                <div v-else-if="!wifi">
                  {{ $t('status') }} {{ $t('disconnected') }}
                </div>
                <div v-else>
                  {{ $t('status') }} {{ $t('connected') }}
                </div>
              </div>
            </div>
            <q-btn
              outline
              rounded
              :loading="wifiLoading"
              no-caps
              v-model="wifi"
              color="primary"
              @click="wifiWarn"
              class="ml-3 mr-3 mt-1 mb-2 text-lg"
              :disable="wifiLoading"
              :label="!wifi ? $t('connect'): $t('disconnect')"
            />
          </div>
          <q-list
            bordered
            class="rounded-borders mt-2"
          >
            <q-expansion-item
              expand-separator
              icon="build"
              :label="$t('advanced')"
              class="w-full"
            >
              <q-card>
                <q-card-section>
                  <div class="mr-3 ml-3">
                    <div class="text-2xl text-gray-700">
                      {{ $t('choose_start_page') }}
                    </div>
                    <div class="text-base text-gray-500">
                      {{ $t('start_page_desc') }}
                    </div>
                    <q-select
                      v-if="!filesLoading"
                      rounded
                      outlined
                      v-model="startPage"
                      :options="pages"
                      class="mb-4"
                      @update:model-value="changeStartPage"
                    />
                    <div
                      class="text-lg"
                      v-if="customStartPageInput"
                    >
                      {{ $t('choose_new_path') }}
                    </div>
                    <q-input
                      v-if="customStartPageInput"
                      ref="startPathValid"
                      filled
                      :placeholder="$t('your_new_path')"
                      class="ml-1 mr-1"
                      :rules="[(value) =>
                        !value.substr(0,1).includes('/') &&
                        !value.substr(-1).includes('/') &&
                        !value.includes(' ') &&
                        !value.includes('\\')
                        || $t('invalid_path_input')]"
                      v-model="newStartPath"
                    />
                    <q-btn
                      v-if="customStartPageInput"
                      outline
                      rounded
                      no-caps
                      color="primary"
                      @click="newStartPathWarn"
                      :label="$t('set_custom_startpage')"
                      class="full-width ml-3 mr-3 sm:mt-1 mb-3 text-lg"
                    />
                    <q-separator spaced />
                    <div class="text-2xl text-gray-700 mt-5 mb-1">
                      {{ $t('set_hostname_desc') }}
                    </div>
                    <q-input
                      ref="hostnameValid"
                      filled
                      class="ml-1 mr-1"
                      :rules="[(val) =>
                        !val.includes(' ') &&
                        val.length <= 32
                        && val === val.toLowerCase()
                        && regexp.test(val)
                        || $t('invalid_input')]"
                      v-model="newHostname"
                      :placeholder="$t('your_new_name')"
                    />
                    <q-btn
                      outline
                      rounded
                      :disable="newHostname"
                      no-caps
                      color="primary"
                      @click="hostnameWarn"
                      :label="$t('set_hostname')"
                      class="full-width ml-3 mr-3 sm:mt-1 mb-3 text-lg"
                    />
                  </div>
                  <q-separator
                    class="mr-3 ml-3"
                    spaced
                  />
                  <div>
                    <q-item class="flex">
                      <q-item-section>
                        <q-item-label class="text-2xl text-gray-700">
                          {{ $t('portainer') }}
                        </q-item-label>
                        <q-item-label class="text-base pr-1 text-gray-500">
                          {{ $t('portainer_settings_description') }}
                        </q-item-label>
                      </q-item-section>
                      <q-toggle
                        class="mt-3 self-end"
                        v-model="portainer"
                        @update:model-value="updatePortainer"
                        :disable="portainerLoading"
                        v-if="!portainerLoading"
                        icon="widgets"
                        size="lg"
                      />
                      <q-spinner
                        v-if="portainerLoading"
                        color="primary"
                        size="2em"
                        class="mt-4 mr-6"
                      />
                    </q-item>
                  </div>
                  <div
                    class="pl-6"
                    v-if="portainer"
                  >
                    {{ $t('portainer_starting_at') }} <a
                      href="/portainer/"
                      target="_blank"
                    >http://{{ windowHostname }}/portainer/</a>
                  </div>
                </q-card-section>
              </q-card>
            </q-expansion-item>
          </q-list>
          <div class="text-center text-2xl mt-6 mb-4 text-gray-600">
            {{ $t('system_info') }}
          </div>
          <div
            v-if="!sysInfoLoading"
            class="flex flex-col text-center text-gray pb-5"
          >
            <span class="text-gray-600"><span>{{ $t('total_storage') }} </span> {{ sysInfo.storage.total }}</span>
            <span class="text-gray-600"><span>{{ $t('available_storage') }} </span> {{ sysInfo.storage.available }}</span>
            <span class="text-gray-600"><span>{{ $t('version') }} </span> {{ sysInfo.versions.lb }}</span>
          </div>
          <div
            v-else
            class="flex flex-col text-center text-gray pb-5"
          >
            <span class="text-gray-600"><span>Loading...</span>{{ sysInfo.versions.lb }}</span>
          </div>
        </div>
      </div>
    </div>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from 'vue'
import Axios from 'app/node_modules/axios'
import { useQuasar } from 'quasar'
import { useStore } from '../store'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  name: 'Settings',
  setup () {
    // Import required features
    const $store = useStore()
    const $q = useQuasar()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { t } = useI18n()

    const currentStartPage = ref<any>()
    const customStartPageInput = ref<boolean>(false)
    const files = ref<boolean>(false)
    const filesLoading = ref<boolean>(false)
    const hostname = ref<string>('')
    const hostnameValid = ref()
    const internet = ref<boolean>(false)
    const library = ref<boolean>(false)
    const libraryLoading = ref<boolean>(false)
    const loading = ref<boolean>(false)
    const newHostname = ref<string>('')
    const newStartPath = ref<string>('')
    const pages = [
      t('lb_welcome_page'), t('file_manager'), t('library'), t('website'), t('custom_start_page')
    ]
    const portainer = ref<boolean>(false)
    const portainerLoading = ref<boolean>(true)
    // Regular expression for input validation
    // eslint-disable-next-line prefer-regex-literals
    const regexp = ref(new RegExp('^[a-z0-9-_]*$'))
    const startPage = ref<string>('-')
    const startPathValid = ref()
    const sysInfoLoading = ref<boolean>(true)
    const sysInfo = ref<{storage: {total: string, available: string}, versions:{lb: string}}>({ storage: { total: '', available: '' }, versions: { lb: '' } })
    const togglesLoading = ref<boolean>(true)
    const website = ref<boolean>(false)
    const websiteLoading = ref<boolean>(false)
    const wifi = ref<boolean>(false)
    const wifiLoading = ref<boolean>(true)
    const windowHostname = ref<string>(window.location.hostname)

    // Get api from store
    const api = computed(() => {
      return $store.getters.GET_API
    })

    // API calls for onMounted
    const fetchedSettings = Axios.get(`${api.value}/v1/settingsui`)
    const fetchedPortainer = Axios.get(`${api.value}/v1/portainer/status`, {
      validateStatus: function (status) {
        return status < 500 // Resolve only if the status code is less than 500
      }
    })
    const fetchedSysInfo = Axios.get(`${api.value}/v1/system/info`)
    const fetchedConnectionStatus = Axios.get(`${api.value}/v1/wifi/connectionstatus`)
    const fetchedInternetConnectionStatus = Axios.get(`${api.value}/v1/internet/connectionstatus`)
    const fetchedHostName = Axios.get(`${api.value}/v1/hostname`)

    onMounted(() => {
      apiCall()
      apiCallStatus()
    })

    async function apiCall (): Promise<void> {
      filesLoading.value = true
      libraryLoading.value = true
      websiteLoading.value = true
      await Axios.all([fetchedSettings, fetchedSysInfo, fetchedInternetConnectionStatus,
        fetchedHostName]).then(Axios.spread(function (res1, res2, res3, res4): void {
        // Get settings
        currentStartPage.value = res1.data.start_page
        files.value = res1.data.files
        website.value = res1.data.website
        library.value = res1.data.library
        togglesLoading.value = false
        // Get SystemInfo
        sysInfo.value = res2.data
        sysInfoLoading.value = false
        // Get internet connection status
        internet.value = res3.data.connected !== false
        // Get hostname
        hostname.value = res4.data.hostname
      })).catch(e => {
        console.log(e.message)
      })

      if (currentStartPage.value === '/') {
        startPage.value = t('lb_welcome_page')
      } else if (currentStartPage.value === 'files') {
        startPage.value = t('file_manager')
      } else if (currentStartPage.value === 'library') {
        startPage.value = t('library')
      } else if (currentStartPage.value === 'website') {
        startPage.value = t('website')
      } else {
        startPage.value = currentStartPage.value
      }

      filesLoading.value = false
      libraryLoading.value = false
      websiteLoading.value = false
    }

    async function apiCallStatus (): Promise<void> {
      await Axios.all([fetchedPortainer,
        fetchedConnectionStatus]).then(Axios.spread(function (res1, res2): void {
        // Get portainer status
        portainer.value = res1.data.container_status === 'Running'
        // Get connection status
        wifi.value = res2.data.running !== false
      })).catch(e => {
        console.log(e.message)
      })
      wifiLoading.value = false
      portainerLoading.value = false
    }

    const changeStartPage = async () => {
      if (startPage.value === t('lb_welcome_page')) {
        currentStartPage.value = '/'
      } else if (startPage.value === t('file_manager')) {
        currentStartPage.value = 'files'
      } else if (startPage.value === t('library')) {
        currentStartPage.value = 'library'
      } else if (startPage.value === t('website')) {
        currentStartPage.value = 'website'
      } else if (startPage.value === t('custom_start_page')) {
        customStartPageInput.value = true
        return
      }

      if (startPage.value === t('lb_welcome_page')) {
        await Axios.post(`${api.value}/v1/setui`, {
          start_page: currentStartPage.value
        })
        $q.dialog({
          title: t('success'),
          message: `${t('path_changed_to')} ${startPage.value}`
        })
      } else {
        $q.dialog({
          title: t('confirm'),
          message: t('change_path_warning'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          Axios.post(`${api.value}/v1/setui`, {
            start_page: currentStartPage.value
          })
          $q.dialog({
            title: t('success'),
            message: `${t('path_changed_to')} ${startPage.value}`
          })
        })
      }
    }

    const connectDisconnectWifi = async () => {
      await Axios.get(`${api.value}/v1/wifi/forget`)
    }

    const disableLogin = async () => {
      const response = await Axios.post(`${api.value}/v1/setpassword`, { password: ' ' })
      if (response.status === 200) {
        $q.notify({ type: 'positive', message: t('login_disabled') })
      } else {
        $q.notify({ type: 'negative', message: t('error') })
      }
    }

    function disableLoginWarn () {
      $q.dialog({
        title: t('confirm'),
        message: t('are_you_sure'),
        cancel: true,
        persistent: true
      }).onOk(() => {
        disableLogin()
      })
    }

    function hostnameWarn () {
      if (hostnameValid.value.validate() && newHostname.value !== '') {
        $q.dialog({
          title: t('confirm'),
          message: t('change_hostname_warning'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          updateHostname()

          $q.dialog({
            title: t('success'),
            message: t('hostname_changed_notification')
          })
        })
      } else {
        $q.notify({ type: 'negative', message: t('invalid_hostname') })
      }
    }

    function newStartPathWarn () {
      if (startPathValid.value.validate() && newStartPath.value !== '') {
        $q.dialog({
          title: t('confirm'),
          message: t('change_path_warning'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          Axios.post(`${api.value}/v1/setui`, {
            start_page: newStartPath.value
          })

          $q.dialog({
            title: t('success'),
            message: `${t('path_changed_to')} '/${newStartPath.value}'`
          })
        })
      } else {
        $q.notify({ type: 'negative', message: t('invalid_path_input') })
      }
    }

    function redirect () {
      location.href = '/upload-library/'
    }

    const updateFiles = async () => {
      filesLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        files: files.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        filesLoading.value = false
      }, 1)
    }

    const updateLibrary = async () => {
      libraryLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        library: library.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        libraryLoading.value = false
      }, 1)
    }

    const updatePortainer = async () => {
      portainerLoading.value = true
      if (portainer.value) {
        const portainerStarter = await Axios.get(`${api.value}/v1/portainer/start`, {
          validateStatus: function (status) {
            return status < 500 // Resolve only if the status code is less than 500
          }
        })
        if (portainerStarter.status === 404) {
          $q.notify({ type: 'negative', message: t('portainer_unavailable') })
          portainer.value = false
        }
      } else {
        await Axios.get(`${api.value}/v1/portainer/stop`)
      }

      setTimeout(() => {
        portainerLoading.value = false
      }, 1)
    }

    const updateWebsite = async () => {
      websiteLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        website: website.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        websiteLoading.value = false
      }, 1)
    }

    const updateHostname = async () => {
      if (newHostname.value) {
        await Axios.post(`${api.value}/v1/hostconfig`, {
          hostname: newHostname.value
        })
      }
    }

    function wifiWarn () {
      if (internet.value && !wifi.value) {
        $q.notify({ type: 'negative', message: t('internet_no_wifi') })
      } else if (wifi.value === false) {
        window.open('http://' + window.location.hostname + ':8080/?lang=' + $q.lang.isoName)
      } else {
        $q.dialog({
          title: t('confirm'),
          message: t('disconnect_wifi'),
          cancel: true,
          persistent: true
        }).onOk(() => {
          connectDisconnectWifi()
          wifi.value = false
        })
      }
    }

    return {
      changeStartPage,
      customStartPageInput,
      disableLogin,
      disableLoginWarn,
      files,
      filesLoading,
      hostname,
      hostnameValid,
      hostnameWarn,
      internet,
      library,
      libraryLoading,
      loading,
      newHostname,
      newStartPath,
      newStartPathWarn,
      pages,
      portainer,
      portainerLoading,
      redirect,
      regexp,
      startPage,
      startPathValid,
      sysInfo,
      sysInfoLoading,
      togglesLoading,
      updateFiles,
      updateLibrary,
      updatePortainer,
      updateWebsite,
      website,
      websiteLoading,
      wifi,
      wifiLoading,
      wifiWarn,
      windowHostname
    }
  }
})
</script>

<style scoped>

</style>
