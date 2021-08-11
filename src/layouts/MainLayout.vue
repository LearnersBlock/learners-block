<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <q-btn
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          v-if="isInIndex"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
        <div class="q-ml-sm q-mt-sm">
          <a href="/">
            <img
              alt=""
              src="../assets/lb-logo-white-full.svg"
            >
          </a>
        </div>
        <q-toolbar-title class="josefin text-h5 q-mt-xs">
          <a
            class="text-white"
            style="text-decoration:none;"
            href="https://library.learnersblock.org"
            target="_self"
          />
        </q-toolbar-title>
        <q-item
          v-if="!onDevice"
          clickable
        >
          <span class="material-icons">
            translate
          </span>
          <q-tooltip class="text-caption text-center">
            {{ $t('switch_language') }}
          </q-tooltip>
          <q-menu>
            <q-list style="min-width: 100px">
              <q-item
                @click="changeLanguage(language.value)"
                v-for="language in languages"
                :key="language.value"
                clickable
                v-close-popup
              >
                <q-item-section>{{ language.label }}</q-item-section>
              </q-item>
            </q-list>
          </q-menu>
        </q-item>
        <q-item
          v-if="!onDevice"
          clickable
          @click="redirect('https://airtable.com/shrkg3MkzXLd7hBts')"
        >
          <span class="material-icons">
            send
          </span>
          <q-tooltip class="text-caption text-center">
            {{ $t('submit_resource') }}
          </q-tooltip>
        </q-item>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      v-if="isInIndex"
      bordered
      class="bg-white"
    >
      <q-list>
        <q-item-label
          header
          class="text-grey-8 text-h5 text-center q-mt-md"
        >
          {{ $t('search_options') }}
        </q-item-label>
        <q-separator class="q-mt-md" />
        <q-input
          outlined
          class="q-mt-lg q-mx-auto w-90"
          v-model="keyword"
          clearable
          @keyup="searchResourcesString"
          :label="$t('keywords')"
        />
        <q-select
          class="w-90 q-mx-auto q-mt-md"
          outlined
          v-if="fetchedLanguages"
          v-model="selectedLanguages"
          :label="$t('languages')"
          :option-label="(lang) => lang.language"
          :option-value="(lang) => lang.id"
          :options="fetchedLanguages.languages"
          @update:model-value="searchResources"
          multiple
          map-options
          emit-value
        >
          <template #option="{ itemProps, opt, selected, toggleOption }">
            <q-item
              v-bind="itemProps"
              v-on="itemProps"
            >
              <q-item-section>
                <q-item-label v-html="opt.language" />
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  :model-value="selected"
                  @update:model-value="toggleOption(opt)"
                />
              </q-item-section>
            </q-item>
          </template>
        </q-select>
        <q-select
          class="w-90 q-mx-auto q-mt-md"
          outlined
          v-model="selectedLevels"
          v-if="fetchedLevels"
          :options="fetchedLevels.levels"
          :option-label="(level) => level.level"
          :option-value="(level) => level.id"
          :label="$t('level')"
          @update:model-value="searchResources"
          multiple
          emit-value
          map-options
        >
          <template #option="{ itemProps, opt, selected, toggleOption }">
            <q-item
              v-bind="itemProps"
              v-on="itemProps"
            >
              <q-item-section>
                <q-item-label v-html="opt.level" />
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  :model-value="selected"
                  @update:model-value="toggleOption(opt)"
                />
              </q-item-section>
            </q-item>
          </template>
        </q-select>
        <q-select
          class="w-90 q-mx-auto q-mt-md"
          outlined
          v-model="selectedTags"
          v-if="fetchedTags"
          :options="fetchedTags.tags"
          :option-label="(tag) => tag.tag"
          :option-value="(tag) => tag.id"
          :label="$t('tags')"
          @update:model-value="searchResources"
          multiple
          emit-value
          map-options
        >
          <template #option="{ itemProps, opt, selected, toggleOption }">
            <q-item
              v-bind="itemProps"
              v-on="itemProps"
            >
              <q-item-section>
                <q-item-label v-html="opt.tag" />
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  :model-value="selected"
                  @update:model-value="toggleOption(opt)"
                />
              </q-item-section>
            </q-item>
          </template>
        </q-select>
        <q-select
          class="w-90 q-mx-auto q-mt-md"
          outlined
          v-model="selectedFormats"
          v-if="fetchedFormats"
          :options="fetchedFormats.formats"
          :option-label="(format) => format.type"
          :option-value="(format) => format.id"
          :label="$t('formats')"
          @update:model-value="searchResources"
          multiple
          emit-value
          map-options
        >
          <template #option="{ itemProps, opt, selected, toggleOption }">
            <q-item
              v-bind="itemProps"
              v-on="itemProps"
            >
              <q-item-section>
                <q-item-label v-html="opt.type" />
              </q-item-section>
              <q-item-section side>
                <q-toggle
                  :model-value="selected"
                  @update:model-value="toggleOption(opt)"
                />
              </q-item-section>
            </q-item>
          </template>
        </q-select>
        <div class="w-90 q-ml-lg q-mt-sm text-grey-9">
          <q-checkbox
            left-label
            size="xs"
            v-model="directDownload"
            :label="$t('direct_download')"
          >
            <q-tooltip
              class="text-body2 text-center"
              anchor="top middle"
            >
              {{ $t('display_only_direct_download') }}
            </q-tooltip>
          </q-checkbox>
        </div>
        <q-btn
          rounded
          color="primary"
          class="q-ml-md q-mt-md"
          @click="resetInputs"
        >
          {{ $t('reset') }}
        </q-btn>
        <div
          v-if="fetchedResourcesLength"
          class="q-ml-md q-mt-md text-grey"
        >
          {{ $t('total_entries') }} {{ fetchedResourcesLength.resourcesConnection.aggregate.totalCount }}
        </div>
        <div class="q-ml-md q-mt-md q-mb-sm text-grey absolute-bottom">
          {{ $t('powered_by') }} <a
            href="https://learnersblock.org"
            target="_blank"
            style="text-decoration: underline; color: inherit"
          >LearnersBlock.org</a>
        </div>
      </q-list>
    </q-drawer>
    <q-page-container>
      <router-view
        v-slot="{ Component, route }"
        :keyword="keyword"
        :formats="selectedFormats"
        :tags="selectedTags"
        :levels="selectedLevels"
        :languages="selectedLanguages"
      >
        <component
          :is="Component"
          :key="route.meta.usePathKey ? route.path : undefined"
          ref="view"
        />
      </router-view>
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">

import { useQuery } from '@vue/apollo-composable'
import { GET_LANGUAGES } from '../gql/language/queries'
import { GET_FORMATS } from '../gql/format/queries'
import { GET_TAGS } from '../gql/tag/queries'
import { GET_LEVELS } from '../gql/level/queries'
import { GET_RESOURCES_LENGTH } from '../gql/resource/queries'
import { Loading, Quasar, useQuasar } from 'quasar'
import { computed, defineComponent, onMounted, provide, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'MainLayout',
  setup () {
    // Import required features
    const $q = useQuasar()
    const { locale } = useI18n({ useScope: 'global' })
    const $router = useRouter()
    const $store = useStore()

    const directDownload = ref(false)
    provide('direct-download', directDownload)

    // Drawer toggle
    const leftDrawerOpen = ref(false)
    // Keyword input
    const keyword = ref<string>('')
    // Router view reference in order to call method from parent to child
    const view = ref<any>(null)
    // Selected languages for select dropdown - IDs
    const selectedLanguages = ref<string[]>([])
    // Selected formats
    const selectedFormats = ref<[]>([])
    // Selected tags
    const selectedTags = ref<string[]>([])
    // Selected level
    const selectedLevels = ref<string[]>([])
    // Searching a new string
    const searching = ref<boolean>(false)
    // Read envs for page state
    const onDevice = ref<any>(process.env.ONDEVICE)
    // Languages for i18n
    const languages = ref<[]>([
      {
        label: 'English',
        value: 'en-US'
      },
      {
        label: 'اَلْعَرَبِيَّةُ',
        value: 'ar'
      },
      {
        label: 'Deutsche',
        value: 'de'
      },
      {
        label: 'Español',
        value: 'es'
      },
      {
        label: 'Français',
        value: 'fr'
      },
      {
        label: 'Italiana',
        value: 'it'
      },
      {
        label: 'Português',
        value: 'pt-BR'
      },
      {
        label: 'Türk',
        value: 'tr'
      }
    ] as any)
    // Selected language for i18n
    const selectedLanguage = ref(locale)
    // Fetch languages query
    const { result: fetchedLanguages, loading: fetchLanguagesLoading, refetch: fetchLanguages } = useQuery(GET_LANGUAGES)
    // Fetch formats query
    const { result: fetchedFormats, loading: fetchFormatsLoading, refetch: fetchFormats } = useQuery(GET_FORMATS)
    // Fetch tags query
    const { result: fetchedTags, loading: fetchTagsLoading, refetch: fetchTags } = useQuery(GET_TAGS)
    // Fetch level query
    const { result: fetchedLevels, loading: fetchLevelsLoading, refetch: fetchLevels } = useQuery(GET_LEVELS)
    // Fetch language cookie
    const langCookie = ref<any>($q.localStorage.getItem('lang'))
    // Fetch resources query
    const {
      result: fetchedResourcesLength
    } = useQuery(GET_RESOURCES_LENGTH, {})

    onMounted(async () => {
      Loading.show()
      if (langCookie.value) {
        locale.value = langCookie.value
        Quasar.lang.set(langCookie.value)
      }
      await fetchLanguages()
      await fetchFormats()
      await fetchTags()
      await fetchLevels()
      Loading.hide()
    })

    // If keyword input is cleared, then execute the query
    watch(() => keyword.value, (newValue) => {
      if (newValue === null) {
        searchResources()
      }
    })

    // Switch i18n language according to selectedLanguage input
    const changeLanguage = (value: string) => {
      import(
        /* webpackInclude: /(en-US|ar|de|es|fr|it|tr|pt-BR)\.js$/ */
        'quasar/lang/' + value
      ).then((lang) => {
        locale.value = value
        Quasar.lang.set(lang.default)
      })
    }

    function delay (ms: number) {
      return new Promise(resolve => setTimeout(resolve, ms))
    }

    // Used to disable the drawer once the user goes to a specific resource
    const isInIndex = computed(() => {
      return $router.currentRoute.value.path === '/'
    })

    // Method to call fetchFilteredResources from parent to child
    const searchResources = async () => {
      Loading.show()
      window.scrollTo(0, 0)
      $store.commit('savedResources/resourceLimit', 40)
      await view.value.fetchFilteredResources(keyword.value, selectedFormats.value, selectedLanguages.value, selectedTags.value, selectedLevels.value)
      Loading.hide()
    }

    // Method to call fetchFilteredResources from parent to child
    const searchResourcesString = async () => {
      if (!searching.value) {
        searching.value = true
        await delay(1000)
        Loading.show()
        window.scrollTo(0, 0)
        $store.commit('savedResources/resourceLimit', 40)
        await view.value.fetchFilteredResources(keyword.value, selectedFormats.value, selectedLanguages.value, selectedTags.value, selectedLevels.value)
        Loading.hide()
        searching.value = false
      }
    }

    function redirect (url) {
      window.open(url, '_blank')
    }

    const resetInputs = async () => {
      Loading.show()
      window.scrollTo(0, 0)
      keyword.value = ''
      selectedLanguages.value = []
      selectedFormats.value = []
      selectedTags.value = []
      selectedLevels.value = []
      await view.value.fetchFilteredResources(keyword.value, selectedFormats.value, selectedLanguages.value, selectedTags.value, selectedLevels.value)
      Loading.hide()
    }

    return {
      changeLanguage,
      directDownload,
      fetchedLanguages,
      fetchFormatsLoading,
      fetchLanguagesLoading,
      fetchedResourcesLength,
      fetchedTags,
      fetchTagsLoading,
      fetchedLevels,
      fetchLevelsLoading,
      fetchedFormats,
      isInIndex,
      keyword,
      languages,
      leftDrawerOpen,
      onDevice,
      redirect,
      resetInputs,
      selectedLanguages,
      selectedFormats,
      selectedTags,
      selectedLevels,
      selectedLanguage,
      searchResources,
      searchResourcesString,
      view
    }
  }
})

</script>
