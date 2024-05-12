import '@mdi/font/css/materialdesignicons.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import App from './App.vue'
import router from './router'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import { defaultLocale, languages } from './i18n/index'

const i18n = createI18n({
  legacy: false,
    locale: defaultLocale,
    messages: Object.assign(languages)
  })

const app = createApp(App)
const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets:{mdi}
  },
  components,
  directives,
})
app.use(vuetify)
app.use(createPinia())
app.use(i18n)
app.use(router)
app.mount('#app')
