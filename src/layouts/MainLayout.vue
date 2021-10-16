<!-- eslint-disable vue/no-v-html -->
<template>
  <q-layout view="hHh Lpr lff">
    <q-header
      class="bg-white"
      bordered
      reveal
    >
      <q-toolbar>
        <q-btn
          v-if="isInIndex"
          color="primary"
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />
        <div class="q-ml-sm q-mt-sm">
          <a href="/">
            <img
              alt=""
              src="../assets/lb-logo-full.svg"
            >
          </a>
        </div>
        <q-toolbar-title class="josefin text-h5 q-mt-xs">
          <a
            style="text-decoration:none;"
            href="https://library.learnersblock.org"
            target="_self"
          />
        </q-toolbar-title>
        <q-item
          v-if="!onDevice"
          clickable
        >
          <q-icon
            name="translate"
            color="primary"
            size="sm"
          >
            <q-tooltip class="text-caption text-center">
              {{ $t('switch_language') }}
            </q-tooltip>
          </q-icon>
          <q-menu>
            <q-list style="min-width: 100px">
              <q-item
                v-for="language in languages"
                :key="language.value"
                v-close-popup
                clickable
                @click="changeLanguage(language.value)"
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
          <q-icon
            name="send"
            color="primary"
            size="sm"
          >
            <q-tooltip class="text-caption text-center">
              {{ $t('submit_resource') }}
            </q-tooltip>
          </q-icon>
        </q-item>
      </q-toolbar>
    </q-header>
    <q-drawer
      v-if="isInIndex"
      v-model="leftDrawerOpen"
      show-if-above
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
        <q-input
          v-model="keyword"
          outlined
          class="q-mt-sm q-mx-auto w-90"
          clearable
          :label="$t('keywords')"
          @keyup="searchResourcesString"
        />
        <q-select
          v-if="fetchedCategories"
          v-model="selectedCategories"
          class="w-90 q-mx-auto q-mt-md"
          outlined
          :label="$t('categories')"
          :option-label="(category) => category.category"
          :option-value="(category) => category.id"
          :options="fetchedCategories.categories"
          multiple
          map-options
          emit-value
          @update:model-value="searchResources"
        >
          <template #option="{ itemProps, opt, selected, toggleOption }">
            <q-item
              v-bind="itemProps"
              v-on="itemProps"
            >
              <q-item-section>
                <q-item-label v-html="opt.category" />
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
          v-if="fetchedLanguages"
          v-model="selectedLanguages"
          class="w-90 q-mx-auto q-mt-md"
          outlined
          :label="$t('languages')"
          :option-label="(lang) => lang.language"
          :option-value="(lang) => lang.id"
          :options="fetchedLanguages.languages"
          multiple
          map-options
          emit-value
          @update:model-value="searchResources"
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
          v-if="fetchedLevels"
          v-model="selectedLevels"
          class="w-90 q-mx-auto q-mt-md"
          outlined
          :options="fetchedLevels.levels"
          :option-label="(level) => level.level"
          :option-value="(level) => level.id"
          :label="$t('level')"
          multiple
          emit-value
          map-options
          @update:model-value="searchResources"
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
          v-if="fetchedSubjects"
          v-model="selectedSubjects"
          class="w-90 q-mx-auto q-mt-md"
          outlined
          :options="fetchedSubjects.subjects"
          :option-label="(subject) => subject.subject"
          :option-value="(subject) => subject.id"
          :label="$t('subjects')"
          multiple
          emit-value
          map-options
          @update:model-value="searchResources"
        >
          <template #option="{ itemProps, opt, selected, toggleOption }">
            <q-item
              v-bind="itemProps"
              v-on="itemProps"
            >
              <q-item-section>
                <q-item-label v-html="opt.subject" />
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
          v-if="fetchedFormats"
          v-model="selectedFormats"
          class="w-90 q-mx-auto q-mt-md"
          outlined
          :options="fetchedFormats.formats"
          :option-label="(format) => format.type"
          :option-value="(format) => format.id"
          :label="$t('formats')"
          multiple
          emit-value
          map-options
          @update:model-value="searchResources"
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
        <q-btn
          rounded
          color="primary"
          class="q-ml-md q-mt-md"
          @click="resetInputs"
        >
          {{ $t('reset') }}
        </q-btn>
        <q-separator class="q-mt-lg" />
        <div class="q-mt-sm text-grey text-center">
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
        :subjects="selectedSubjects"
        :levels="selectedLevels"
        :languages="selectedLanguages"
        :categories="selectedCategories"
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
import { GET_CATEGORIES } from '../gql/category/queries'
import { GET_LANGUAGES } from '../gql/language/queries'
import { GET_FORMATS } from '../gql/format/queries'
import { GET_LEVELS } from '../gql/level/queries'
import { GET_SUBJECTS } from '../gql/subject/queries'
import { Loading, Quasar, useQuasar } from 'quasar'
import { computed, defineComponent, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'MainLayout',
  setup () {
    // Import required features
    const $q = useQuasar()
    // eslint-disable-next-line @typescript-eslint/unbound-method
    const { locale } = useI18n({ useScope: 'global' })
    const $router = useRouter()
    const $store = useStore()

    // Keyword input
    const keyword = ref<string>('')
    // Drawer toggle
    const leftDrawerOpen = ref(false)
    // Read envs for page state
    const onDevice = ref<any>(process.env.ONDEVICE)
    // Selected languages for select dropdown - IDs
    const selectedCategories = ref<string[]>([])
    // Selected formats
    const selectedFormats = ref<[]>([])
    // Selected languages for select dropdown - IDs
    const selectedLanguages = ref<string[]>([])
    // Selected level
    const selectedLevels = ref<string[]>([])
    // Searching a new string
    const searching = ref<boolean>(false)
    // Selected subjects
    const selectedSubjects = ref<string[]>([])
    // Router view reference in order to call method from parent to child
    const view = ref<any>(null)

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
    // Fetch categories query
    const { result: fetchedCategories, loading: fetchCategoriesLoading } = useQuery(GET_CATEGORIES)
    // Fetch languages query
    const { result: fetchedLanguages, loading: fetchLanguagesLoading } = useQuery(GET_LANGUAGES)
    // Fetch formats query
    const { result: fetchedFormats, loading: fetchFormatsLoading } = useQuery(GET_FORMATS)
    // Fetch subjects query
    const { result: fetchedSubjects, loading: fetchSubjectsLoading } = useQuery(GET_SUBJECTS)
    // Fetch level query
    const { result: fetchedLevels, loading: fetchLevelsLoading } = useQuery(GET_LEVELS)

    onMounted(() => {
      if (onDevice.value) {
        const langCookie = ref<any>($q.localStorage.getItem('lang'))
        if (langCookie.value) {
          // Fetch language cookie
          locale.value = langCookie.value
          Quasar.lang.set(langCookie.value)
        }
      }
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

    function redirect (url) {
      window.open(url, '_blank')
    }

    const resetInputs = async () => {
      Loading.show()
      window.scrollTo(0, 0)
      keyword.value = ''
      selectedLanguages.value = []
      selectedFormats.value = []
      selectedSubjects.value = []
      selectedLevels.value = []
      selectedCategories.value = []
      await view.value.fetchFilteredResources(keyword.value, selectedFormats.value, selectedCategories.value, selectedLanguages.value, selectedSubjects.value, selectedLevels.value, selectedCategories.value)
      Loading.hide()
    }

    // Method to call fetchFilteredResources from parent to child
    const searchResources = async () => {
      Loading.show()
      window.scrollTo(0, 0)
      $store.commit('savedResources/resourceLimit', 40)
      await view.value.fetchFilteredResources(keyword.value, selectedFormats.value, selectedLanguages.value, selectedSubjects.value, selectedLevels.value, selectedCategories.value)
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
        await view.value.fetchFilteredResources(keyword.value, selectedFormats.value, selectedLanguages.value, selectedSubjects.value, selectedLevels.value, selectedCategories.value)
        Loading.hide()
        searching.value = false
      }
    }

    return {
      changeLanguage,
      fetchedCategories,
      fetchCategoriesLoading,
      fetchedLanguages,
      fetchFormatsLoading,
      fetchLanguagesLoading,
      fetchedSubjects,
      fetchSubjectsLoading,
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
      selectedCategories,
      selectedLanguages,
      selectedFormats,
      selectedSubjects,
      selectedLevels,
      selectedLanguage,
      searchResources,
      searchResourcesString,
      view
    }
  }
})

</script>
