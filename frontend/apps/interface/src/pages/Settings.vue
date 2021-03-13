<template>
    <q-page class="py-10 px-52">
<q-page-sticky position="top-left" :offset="[18, 18]">
        <router-link color="secondary" class="back text-h6 cursor-pointer" to="/">
        <q-btn color="white" text-color="primary" class="text-subtitle2 text-weight-bold">
          {{$t('home')}}
        </q-btn>
        </router-link>
   </q-page-sticky>
        <div class="text-5xl text-gray-600">{{ $t('settings') }}</div>
        <hr class="mt-6 mb-6" />
   <div class="flex flex-col">
     <q-list>
     <q-item-label header class="text-2xl">Enable components</q-item-label>
     <q-item class="flex">
        <q-item-section>
              <q-item-label class="josefin text-xl">{{$t('files')}}</q-item-label>
              <q-item-label class="text-base" caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
        </q-item-section>
       <q-toggle
        v-model="files"
        icon="folder"
        class="self-end"
        size="lg"
        v-if="!filesLoading"
        @input="updateFiles"
      >
      </q-toggle>
      <q-spinner
        v-if="filesLoading"
        color="primary"
        size="3em"
      />
     </q-item>
     <q-item >
         <q-item-section>
              <q-item-label class="josefin text-xl">{{$t('website')}}</q-item-label>
              <q-item-label class="text-base" caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
        </q-item-section>
    <q-toggle
        v-model="website"
        icon="web"
        size="lg"
        class="ml-auto"
        v-if="!websiteLoading"
        @input="updateWebsite"
      />
       <q-spinner
       v-if="websiteLoading"
        color="primary"
        size="3em"
      />
     </q-item>

      <q-item>
         <q-item-section>
              <q-item-label class="josefin text-xl">{{$t('makerspace')}}</q-item-label>
              <q-item-label class="text-base" caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
        </q-item-section>
      <q-toggle
        v-model="makerspace"
        icon="space_bar"
        size="lg"
        v-if="!makerspaceLoading"
        @input="updateMakerspace"
      />
        <q-spinner
        v-if="makerspaceLoading"
        color="primary"
        size="3em"
      />
     </q-item>

     <q-item>
        <q-item-section>
              <q-item-label class="josefin text-xl">{{$t('library')}}</q-item-label>
              <q-item-label class="text-base" caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
        </q-item-section>
      <q-toggle
        v-model="library"
        icon="import_contacts"
        size="lg"
        v-if="!libraryLoading"
        @input="updateLibrary"
      />
       <q-spinner
        v-if="libraryLoading"
        color="primary"
        size="3em"
      />
     </q-item>

   </q-list>
   <q-separator spaced />
   <q-item-label header class="text-2xl">Login</q-item-label>

   <q-separator spaced />
   <q-item-label header class="text-2xl">Wi-Fi</q-item-label>
    <div>
   <div class="text-lg ml-4">
     <div v-if="!wifi">
      Status: {{$t('disconnect')}}
   </div>
   <div v-else>
     Status: {{$t('connect')}}
     </div>
     </div>
      <q-btn
        v-model="wifi"
        color="primary"
        @click="connectDisconnectWifi"
        class="ml-4 mt-3 mb-3"
        :label="!wifi ? $t('connect'): $t('disconnect')"
      />
        <q-spinner
        v-if="loading"
        color="primary"
        size="3em"
      />
    </div>
   <q-separator spaced />

   </div>
   <q-list bordered class="rounded-borders mt-10 ">
      <q-expansion-item
        expand-separator
        icon="build"
        :label="$t('advanced')"
        class="w-full"
      >
         <div class="text-lg ml-6 mt-6">
      Set a new hostname:
   </div>
       <q-card>
        <q-card-section>
          <q-input filled class="ml-1 mr-2"
             :rules="[(val) =>
             !val.includes(' ') &&
             val.length <= 32
             && val === val.toLowerCase()
             && regexp.test(val)
             || $t('invalid_input')]"
             v-model="newHostname"
             :label="$t('hostname')"
             lazy-rules
              />
            <q-btn color="primary" @click="updateHostname" :label="$t('set')" class="px-4 ml-4 mt-3 text-md mb-6" />
            <q-separator spaced />

        <div>
               <q-item class="flex">
        <q-item-section>
              <q-item-label class="josefin text-xl mt-3">{{$t('Portainer')}}</q-item-label>
              <q-item-label class="text-base" caption lines="2">Secondary line text. Lorem ipsum dolor sit amet, consectetur adipiscit elit.</q-item-label>
        </q-item-section>
        
          <q-toggle
          class="mt-3"
            v-model="portainer"
            @input="updatePortainer"
            v-if="!portainerLoading"
            :label="$t('portainer')"
            icon="widgets"
            size="lg"
          />
            <q-spinner
            v-if="portainerLoading"
            color="primary"
            size="3em"
          />
               </q-item>
        </div>
        <a :href="'http://' + hostname + ':9000'" target="_blank" v-if="portainer">Hostname</a>
          </q-card-section>
        </q-card>
      </q-expansion-item>
   </q-list>
   <div class="text-center text-2xl mt-10 mb-4 text-gray-600">
      System Info
   </div>
   <div class="flex flex-col text-center text-gray">
    <span class="text-gray-600"><span>{{$t('total_storage')}}: </span>{{ sysInfo.storage.total }}</span>
    <span class="text-gray-600"><span>{{$t('available_storage') }}: </span> {{ sysInfo.storage.available }}</span>
    <span class="text-gray-600"><span>{{$t('version') }}: </span>{{ sysInfo.versions.lb }}</span>
   </div>
  </q-page>
</template>

<script lang="ts">
import { computed, defineComponent, onMounted, ref } from '@vue/composition-api'
import Axios from 'app/node_modules/axios'

export default defineComponent({
  setup (_, { root }) {
    const files = ref<boolean>(false)
    const website = ref<boolean>(false)
    const library = ref<boolean>(false)
    const makerspace = ref<boolean>(false)
    const wifi = ref<boolean>(false)
    const portainer = ref<boolean>(false)
    const hostname = ref<string>('')
    const newHostname = ref<string>('')
    const filesLoading = ref<boolean>(false)
    const websiteLoading = ref<boolean>(false)
    const libraryLoading = ref<boolean>(false)
    const makerspaceLoading = ref<boolean>(false)
    const portainerLoading = ref<boolean>(false)
    const loading = ref<boolean>(false)
    const sysInfo = ref<{storage: {total: string, available: string}, versions:{lb: string}}>({ storage: { total: '', available: '' }, versions: { lb: '' } })
    // Regular expression for input validation
    // eslint-disable-next-line prefer-regex-literals
    const regexp = ref(new RegExp('^[a-z0-9-_]*$'))
    // Get api from store
    const api = computed(() => {
      return root.$store.getters.GET_API
    })
    onMounted(async () => {
      // Get settings
      const fetchedSettings = await Axios.get(`${api.value}/v1/settingsui`)
      files.value = fetchedSettings.data.files
      website.value = fetchedSettings.data.website
      library.value = fetchedSettings.data.library
      makerspace.value = fetchedSettings.data.makerspace

      // Get portainer status
      const fetchedPortainer = await Axios.get(`${api.value}/v1/portainer/status`)
      portainer.value = fetchedPortainer.data.message === 'Running'
      // Get SystemInfo
      const fetchedSysInfo = await Axios.get(`${api.value}/v1/system/info`)
      sysInfo.value = fetchedSysInfo.data
      // Get connection status
      const fetchedConnectionStatus = await Axios.get(`${api.value}/v1/wifi/connectionstatus`)
      wifi.value = fetchedConnectionStatus.data.running !== false
      // Get hostname
      const fetchedHostName = await Axios.get(`${api.value}/v1/hostname`)
      hostname.value = fetchedHostName.data.hostname
    })

    const connectDisconnectWifi = async () => {
      if (wifi.value === true) {
        await Axios.get(`${api.value}/v1/wifi/forget`)
        wifi.value = false
      } else {
        window.open(`${hostname.value}.local:8080`)
      }
    }

    const updateFiles = async () => {
      filesLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        files: files.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        filesLoading.value = false
      }, 1000)
    }

    const updateWebsite = async () => {
      websiteLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        website: website.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        websiteLoading.value = false
      }, 1000)
    }

    const updateLibrary = async () => {
      libraryLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        library: library.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        libraryLoading.value = false
      }, 1000)
    }

    const updateMakerspace = async () => {
      makerspaceLoading.value = true
      await Axios.post(`${api.value}/v1/setui`, {
        makerspace: makerspace.value ? 'TRUE' : 'FALSE'
      })
      setTimeout(() => {
        makerspaceLoading.value = false
      }, 1000)
    }

    const updatePortainer = async () => {
      portainerLoading.value = true

      if (portainer.value) {
        await Axios.get(`${api.value}/v1/portainer/start`)
      } else {
        await Axios.get(`${api.value}/v1/portainer/stop`)
      }

      setTimeout(() => {
        portainerLoading.value = false
      }, 1000)
    }

    const updateHostname = async () => {
      if (newHostname.value) {
        await Axios.get(`${api.value}/v1/hostconfig/${newHostname.value}`)
        const fetchedHostname = await Axios.get(`${api.value}/v1/hostname`)
        hostname.value = fetchedHostname.data.hostname
        newHostname.value = ''
      }
    }

    return {
      files,
      website,
      library,
      makerspace,
      wifi,
      portainer,
      updateFiles,
      updateWebsite,
      updateLibrary,
      updateMakerspace,
      websiteLoading,
      makerspaceLoading,
      portainerLoading,
      libraryLoading,
      filesLoading,
      sysInfo,
      hostname,
      loading,
      updatePortainer,
      regexp,
      newHostname,
      updateHostname,
      connectDisconnectWifi
    }
  }
})
</script>

<style scoped>

</style>
