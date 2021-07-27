<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar v-if="!(currentPath.path == '/captive_portal' || currentPath.path == '/captive_portal/' || currentPath.path == '/epub_reader/')">
        <div class="ml-1">
          <router-link to="/">
            <img
              alt=""
              src="../assets/lb-logo-white-full.svg"
            >
          </router-link>
        </div>

        <q-toolbar-title class="josefin text-h5 q-mt-xs">
          <router-link
            class="text-white"
            style="text-decoration:none;"
            to="/"
          />
        </q-toolbar-title>
        <q-item clickable>
          <span class="material-icons">
            translate
          </span>
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
          @click="settings"
          class="flex items-center"
          clickable
        >
          <q-icon name="settings" />
        </q-item>

        <q-item
          v-if="isAuthenticated"
          @click="logout"
          class="flex items-center"
          clickable
        >
          <q-icon name="logout" />
        </q-item>
      </q-toolbar>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script lang="ts">

import { computed, defineComponent, onMounted, ref } from 'vue'
import { Quasar, useQuasar } from 'quasar'
import { useStore } from '../store'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

export default defineComponent({
  name: 'MainLayout',
  setup () {
    const $router = useRouter()
    const $q = useQuasar()
    const $store = useStore()
    const leftDrawerOpen = ref(false)
    const currentPath = $router.currentRoute.value
    const { locale } = useI18n({ useScope: 'global' })
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
        label: 'Türk',
        value: 'tr'
      }
    ])

    const isAuthenticated = computed(() => {
      return $store.getters.isAuthenticated
    })

    const changeLanguage = (value: string) => {
      import(
        /* webpackInclude: /(en-US|ar|de|es|fr|it|tr|pt-BR)\.js$/ */
        'quasar/lang/' + value
      ).then((lang) => {
        locale.value = value
        Quasar.lang.set(lang.default)
        $q.cookies.set('lang', value, { sameSite: 'Lax', path: '/', expires: 365 })
        localStorage.setItem('lang', value)
      })
    }

    const logout = async () => {
      $q.loading.show({
        delay: 300 // ms
      })
      await $store.dispatch('LOGOUT')
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      await $router.push('/').catch(() => {})
      $q.loading.hide()
    }

    const settings = async () => {
      $q.loading.show({
        delay: 300 // ms
      })
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      await $router.push('/settings').catch(() => {})

      $q.loading.hide()
    }

    onMounted(() => {
      $q.loading.show({
        delay: 300 // ms
      })

      const langCookie = ref<any>($q.localStorage.getItem('lang'))
      if (langCookie.value) {
        changeLanguage(langCookie.value)
      }

      const usersLocale = $q.lang.getLocale()
      if (!localStorage.getItem('lang') && usersLocale && languages.value.find(language => language.value === usersLocale)) {
        changeLanguage(usersLocale)
      }
      $q.loading.hide()
    })

    return { currentPath, leftDrawerOpen, languages, changeLanguage, logout, isAuthenticated, settings }
  }
})
</script>
