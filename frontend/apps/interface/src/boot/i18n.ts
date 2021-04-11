import { createI18n } from 'vue-i18n'
import messages from 'src/i18n'
// you'll need to create the src/i18n/index.js file too

const i18n = createI18n({
  locale: 'en-US',
  messages
})

export default ({ app }) => {
  // Set i18n instance on app
  app.use(i18n)
}

export { i18n }
