<template>
  <q-layout view="lHh Lpr lFf">
    <q-header elevated>
      <q-toolbar>
        <div class="ml-1">
          <a href="/">
            <img
              alt=""
              src="../assets/lb-logo-white-full.svg"
            >
          </a>
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
        <router-link to="/settings">
          <q-item
            class="flex items-center"
            clickable
          >
            <q-icon name="settings" />
          </q-item>
        </router-link>

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

import { computed, defineComponent, onMounted, ref } from '@vue/composition-api'

export default defineComponent({
  name: 'MainLayout',
  setup (_, { root }) {
    const leftDrawerOpen = ref(false)
    const languages = ref([
      {
        label: 'English',
        value: 'en-us'
      },
      {
        label: 'اَلْعَرَبِيَّةُ',
        value: 'ar'
      },
      {
        label: 'Français',
        value: 'fr'
      }
    ])

    const isAuthenticated = computed(() => {
      return root.$store.getters.isAuthenticated
    })

    const changeLanguage = (value: string) => {
      if (value === 'ar') {
        import(
        /* webpackInclude: /(de|en-us)\.js$/ */
          'quasar/lang/' + 'he'
        ).then(lang => {
          root.$q.lang.set(lang.default)
          localStorage.setItem('lang', value)
        })
      } else {
        import(
        /* webpackInclude: /(de|en-us)\.js$/ */
          'quasar/lang/' + 'en-us'
        ).then(lang => {
          root.$q.lang.set(lang.default)
          localStorage.setItem('lang', value)
        })
      }
      root.$i18n.locale = value
    }

    const logout = async () => {
      await root.$store.dispatch('LOGOUT')
      root.$router.push('/')
    }

    onMounted(() => {
      const usersLocale = root.$q.lang.getLocale()
      if (!localStorage.getItem('lang') && usersLocale && languages.value.find(language => language.value === usersLocale)) {
        root.$i18n.locale = usersLocale
        localStorage.setItem('lang', usersLocale)
      }
    })

    return { leftDrawerOpen, languages, changeLanguage, logout, isAuthenticated }
  }
})
</script>
