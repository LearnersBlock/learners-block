<template>
  <q-layout view="hHh lpR fFf">
    <q-header class="bg-white" bordered reveal>
      <q-toolbar v-if="!hideHeader">
        <div class="ml-2">
          <router-link to="/">
            <img alt="" src="../assets/lb-logo-full.svg" />
          </router-link>
        </div>
        <q-toolbar-title class="text-h5 q-mt-xs">
          <router-link
            class="text-white"
            style="text-decoration: none"
            to="/"
          />
        </q-toolbar-title>
        <q-btn
          class="ml-3 mr-3"
          icon="translate"
          color="primary"
          padding="0"
          outline
          flat
          dense
        >
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
        </q-btn>
        <q-btn
          class="ml-3 mr-3"
          icon="settings"
          color="primary"
          padding="0"
          outline
          flat
          dense
          @click="settings"
        />
        <q-btn
          v-if="isAuthenticated"
          class="ml-3 mr-3"
          icon="logout"
          color="primary"
          padding="0"
          outline
          flat
          dense
          @click="logout"
        />
      </q-toolbar>
    </q-header>
    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">
import { Quasar, useQuasar } from 'quasar'
import { useStore } from '../store'
import { computed, defineComponent, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRouter } from 'vue-router'
import type { QuasarLanguage } from 'quasar'

export default defineComponent({
  name: 'IntMainLayout',
  setup() {
    // Import required features
    const $q = useQuasar()
    const $router = useRouter()
    const $store = useStore()
    const { locale } = useI18n({ useScope: 'global' })

    // Set constants
    const hideHeader = ref<boolean>(false)
    const languages = ref([
      // Language updates must be changed here and in the webpackInclude magic comment below
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
        label: 'русский',
        value: 'ru'
      },
      {
        label: 'Türk',
        value: 'tr'
      }
    ])

    // Watch for page changes to update header status
    watch(
      () => $router.currentRoute.value.path,
      (val) => {
        if (val.includes('captive_portal') || val.includes('epub_reader')) {
          hideHeader.value = true
        } else {
          hideHeader.value = false
        }
      }
    )

    const isAuthenticated = computed(() => {
      return $store.getters.isAuthenticated
    })

    onMounted(() => {
      // Hide header on full screen routes
      if (
        $router.currentRoute.value.path.includes('captive_portal') ||
        $router.currentRoute.value.path.includes('epub_reader')
      ) {
        hideHeader.value = true
      }

      const langCookie = ref<any>($q.localStorage.getItem('lang'))
      if (langCookie.value) {
        changeLanguage(langCookie.value as string)
      }

      const usersLocale = $q.lang.getLocale()
      if (
        !localStorage.getItem('lang') &&
        usersLocale &&
        languages.value.find((language) => language.value === usersLocale)
      ) {
        changeLanguage(usersLocale)
      }
    })

    const changeLanguage = (value: string) => {
      void import(
        /* webpackInclude: /(en-US|ar|de|es|fr|it|tr|pt-BR|ru)\.js$/ */
        `quasar/lang/${value}`
      ).then((lang) => {
        locale.value = value
        Quasar.lang.set(lang.default as QuasarLanguage)
        $q.cookies.set('lang', value, {
          sameSite: 'Lax',
          path: '/',
          expires: 365
        })
        localStorage.setItem('lang', value)
      })
    }

    const logout = async () => {
      $q.loading.show({
        delay: 300 // ms
      })
      await $store.dispatch('LOGOUT')
      // Catching errors to facilitate auto login
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      await $router.replace('/').catch(() => {})
      $q.loading.hide()
    }

    const settings = async () => {
      $q.loading.show({
        delay: 300 // ms
      })
      // Catching errors to facilitate auto login
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      await $router.push('/settings').catch(() => {})

      $q.loading.hide()
    }

    return {
      changeLanguage,
      hideHeader,
      isAuthenticated,
      languages,
      logout,
      settings
    }
  }
})
</script>
