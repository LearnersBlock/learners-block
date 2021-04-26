<template>
  <q-page padding>
    <div
      class="row col-12"
      v-if="show"
    >
      <q-select
        class="col mt-1 ml-1"
        filled
        v-model="chapter"
        :options="toc"
        :label="$t('chapter')"
        dense
        option-value="href"
        option-label="label"
        option-disable="inactive"
        emit-value
        map-options
        @update:model-value="goToExcerpt"
      />
    </div>
    <div>
      <div>
        <div
          class="col-12"
          v-touch-swipe.mouse.left.right.up="touchMoveToPage"
          style="position: absolute;z-index: 2000 !important; height: 67vh; width: 96%"
        />
      </div>
      <div
        :style="'height: calc(100vh - ' + this.readerHeight + '); background-color: white;'"
        id="epub-render"
      />
      <q-page-sticky
        position="bottom-right"
        :offset="[18, 18]"
      >
        <q-btn
          v-if="!this.$q.fullscreen.isActive"
          rounded
          color="white"
          size="xs"
          :icon="$q.fullscreen.isActive ? 'fullscreen_exit' : 'fullscreen'"
          text-color="primary"
          @click="toggle"
        />
      </q-page-sticky>
    </div>
    <q-inner-loading :showing="!show">
      <q-spinner
        size="5rem"
        color="primary"
      />
    </q-inner-loading>
  </q-page>
</template>

<script>
import ePub from 'epubjs'
import { watch } from 'vue'

export default {
  name: 'EpubReader',
  data () {
    const readerHeight = '145px'
    watch(() => this.$q.fullscreen.isActive, val => {
      if (val) {
        this.readerHeight = '10px'
      } else {
        this.readerHeight = '145px'
      }
    })
    return {
      readerHeight,
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
    toggle (e) {
      const target = e.target.parentNode.parentNode.parentNode.parentNode.parentNode
      this.$q.fullscreen.toggle(target)
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
        this.$q.notify({ type: 'negative', message: this.$t('error') })
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
