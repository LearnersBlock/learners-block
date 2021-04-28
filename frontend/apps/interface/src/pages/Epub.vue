<template>
  <q-page>
    <div v-if="show">
      <div
        v-touch-swipe.mouse.left.right.up="touchMoveToPage"
        style="position: absolute;z-index: 2000 !important; height: 67vh; width: 96%"
      />
      <div
        class="bg-white"
        :style="'height: ' + this.$q.screen.height + 'px;'"
        id="epub-render"
      />
      <q-page-sticky
        position="bottom-right"
        :offset="[18, 18]"
      >
        <q-fab
          v-if="!this.$q.fullscreen.isActive"
          v-model="fabRight"
          vertical-actions-align="right"
          color="white"
          padding="xs"
          icon="keyboard_arrow_up"
          text-color="primary"
          direction="up"
        >
          <q-fab-action
            label-position="left"
            v-if="this.$q.fullscreen.isCapable"
            color="primary"
            :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
            text-color="white"
            @click="toggle"
            :label="$t('full_screen')"
          />
          <q-fab-action
            label-position="left"
            @click="redirect"
            color="primary"
            text-color="white"
            class="material-icons"
            icon="arrow_back_ios"
            :label="$t('back')"
          />
          <q-select
            filled
            v-model="chapter"
            :options="toc"
            rounded
            dense
            option-value="href"
            option-label="label"
            option-disable="inactive"
            emit-value
            bg-color="primary"
            map-options
            @update:model-value="goToExcerpt"
          >
            <template #prepend>
              <q-icon
                name="menu_book"
                color="white"
              />
            </template>
          </q-select>
        </q-fab>
      </q-page-sticky>
      <q-inner-loading :showing="!show">
        <q-spinner
          size="5em"
          color="primary"
        />
      </q-inner-loading>
    </div>
  </q-page>
</template>

<script>
import ePub from 'epubjs'
import { watch, ref } from 'vue'

export default {
  name: 'EpubReader',
  data () {
    watch(() => this.$q.fullscreen.isActive, val => {
      // Fix for Safari where first page is not stored on load
      if (val) {
        if (!this.rendition.location) {
          this.rendition.display()
        }
      }
    })
    return {
      fabRight: ref(true),
      newEpub: [],
      show: false,
      book: {},
      rendition: {},
      chapter: '',
      toc: []
    }
  },
  mounted () {
    this.loadEpub()
    if (this.$q.platform.is.mobile) {
      this.$q.notify({ type: 'info', multiLine: true, message: this.$t('swipe_instruction') })
    } else {
      this.$q.notify({ type: 'info', multiLine: true, message: this.$t('click_swipe_instruction') })
    }
  },
  methods: {
    toggle () {
      this.$q.fullscreen.toggle()
        .then(() => {
          this.$q.notify({ type: 'info', multiLine: true, message: this.$t('swipe_up_exit') })
        })
        .catch((err) => {
          alert(err)
          console.error(err)
        })
    },
    loadEpub (e) {
      const epub = this.$route.query.url
      if (!epub) {
        this.$q.notify({ type: 'negative', message: `${this.$t('error')} Did you pass a URL to a file?` })
        this.show = true
        return
      }
      this.book = ePub(e ? e.target.result : epub)
      this.book.loaded.navigation.then(({ toc }) => {
        this.toc = toc
      })
      this.book.ready.then(() => {
        this.show = true
      })
      this.rendition = this.book.renderTo('epub-render', {
        method: 'default',
        height: '100%',
        width: '96vw'
      })
      this.rendition.display()
      document.getElementById('add')
    },
    redirect () {
      location.href = '/settings'
    },
    nextPage () {
      this.rendition.next()
    },
    previousPage () {
      this.rendition.prev()
    },
    touchMoveToPage ({ ...info }) {
      if (info.direction === 'left') {
        this.nextPage()
      } else if (info.direction === 'right') {
        this.previousPage()
      } else if (info.direction === 'up' && this.$q.fullscreen.isActive) {
        this.$q.fullscreen.toggle()
      }
    },
    goToExcerpt () {
      if (Number.isInteger(this.chapter.toLowerCase().indexOf('xhtml'))) {
        this.rendition.display(this.chapter)
      } else {
        this.rendition.display(`epubcfi(${this.chapter})`)
      }
    }
  }
}
</script>
